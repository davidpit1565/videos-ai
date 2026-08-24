#!/usr/bin/env python3
"""One command that listens to a finished narration and says what still needs fixing.

He asked for something that judges the voice by itself instead of him having to
describe what he heard. This is that: it reads a narration and its cue file and
scores every line on the four things that have actually gone wrong so far.

  pacing      the gap to the next line. Negative means two lines overlap — that
              is the "words are cut, no space between sentences" defect, and it
              came from squeezing speech into fixed video slots.
  rate        syllables per second. Above ~6.5 the model starts eliding endings.
  sibilance   4-9 kHz against the 300-3400 Hz body. A dull S reads as a lisp,
              a hot S as a whistle.
  tail        high-frequency energy in the last 120 ms of the line, relative to
              the line's body. This is the R / T / D that he hears swallowed.

Thresholds are not invented. Pacing has a hard floor (an overlap is an overlap),
and everything else is judged against this narration's own median with a robust
deviation, so a line is flagged for being unlike the rest of his own delivery
rather than for missing a number I made up. Absolute floors are only applied
where a measurement exists to back them, and the medians are always printed so
the numbers can be argued with.

  python3 audio/voice_doctor.py audio/voice/ep01-nat.wav
  python3 audio/voice_doctor.py audio/voice/ep01-nat.wav --deep   # per word, needs whisper
"""
import argparse, json, os, re, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MIN_GAP = 0.30          # measured: below this the lines read as one run-on
MAX_RATE = 6.5          # the rate above which build_voice already re-rolls a line
# Deadbands, so the tool cannot chase its own tail: once a repair pass tightens the
# spread, a purely relative fence starts flagging half-decibel differences nobody can
# hear. Below these numbers a line is left alone no matter what the statistics say.
DEAD_LVL = 1.5          # dB of level difference that is audible at all
DEAD_SIB = 5.0          # dB of sibilance residual worth touching
VOWELS = re.compile(r"[aeiouy]+", re.I)
SIBILANT = re.compile(r"sh|ch|ss|s|z|x|c[ei]", re.I)


def load(path):
    with wave.open(path) as w:
        sr = w.getframerate()
        y = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return y, sr


def band(x, sr, lo, hi):
    if len(x) < 256:
        return 0.0
    S = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    f = np.fft.rfftfreq(len(x), 1 / sr)
    m = (f >= lo) & (f < hi)
    return float(np.sqrt((S[m] ** 2).mean())) if m.any() else 0.0


def db(a, b):
    return 20 * np.log10(max(a, 1e-9) / max(b, 1e-9))


def syllables(text):
    n = 0
    for w in re.findall(r"[A-Za-z']+", text):
        c = len(VOWELS.findall(w))
        n += max(1, c - (1 if re.search(r"[^aeiou]e$", w, re.I) else 0))
    return n


def sib_density(text):
    """How much S the line is even supposed to have. A line with two sibilants
    measures darker than a line with nine, and that is the text's doing, not a
    defect — so the S score has to be read against this before anything is judged."""
    syl = max(1, syllables(text))
    return len(SIBILANT.findall(text)) / syl


def expected(xs, ys):
    """Least-squares line through (density, sibilance). Returns a predictor; with
    too few points or no spread it falls back to the plain median."""
    x = np.array(xs, dtype=float); y = np.array(ys, dtype=float)
    if len(x) < 6 or x.std() < 1e-6:
        m = float(np.median(y))
        return (lambda _: m), 0.0
    b, a = np.polyfit(x, y, 1)
    return (lambda t: a + b * t), float(b)


def mad_floor(vals, k=2.5):
    """Robust lower fence: median minus k times the median absolute deviation.
    Judges a line against the rest of his own delivery, not against a guess."""
    v = np.array([x for x in vals if x is not None], dtype=float)
    if len(v) < 4:
        return None, None
    med = float(np.median(v))
    mad = float(np.median(np.abs(v - med))) or 0.5
    return med, med - k * 1.4826 * mad


def measure(y, sr, cues):
    rows = []
    for i, c in enumerate(cues):
        a, b = int(float(c["start"]) * sr), int(float(c["end"]) * sr)
        seg = y[a:b]
        if len(seg) < int(0.15 * sr):
            rows.append(dict(n=c["n"], line=c["line"], skip=True))
            continue
        body = band(seg, sr, 300, 3400)
        sib = db(band(seg, sr, 4000, 9000), body)
        # the tail has to end on the last actual sound: a cue slot can hold trailing
        # silence, and measuring that only tells you the fade worked
        env = np.convolve(np.abs(seg), np.ones(int(0.01 * sr)) / (0.01 * sr), "same")
        loud = np.where(env > env.max() * 0.05)[0]
        end = loud[-1] + 1 if len(loud) else len(seg)
        tail = seg[max(0, end - int(0.12 * sr)):end]
        tl = db(band(tail, sr, 2000, 8000), body)
        dur = (b - a) / sr
        rows.append(dict(
            n=c["n"], line=c["line"], dur=round(dur, 2),
            gap=(round(float(cues[i + 1]["start"]) - float(c["end"]), 2)
                 if i + 1 < len(cues) else None),
            rate=round(syllables(c["line"]) / dur, 2),
            dens=round(sib_density(c["line"]), 3),
            rms=round(20 * np.log10(max(float(np.sqrt((seg ** 2).mean())), 1e-9)), 1),
            sib=round(sib, 1), tail=round(tl, 1), skip=False))
    return rows


def verdict(rows):
    live = [r for r in rows if not r["skip"]]
    pred, slope = expected([r["dens"] for r in live], [r["sib"] for r in live])
    for r in live:
        r["sib_res"] = round(r["sib"] - pred(r["dens"]), 1)
    sib_med, sib_floor = mad_floor([r["sib_res"] for r in live])
    tail_med, tail_floor = mad_floor([r["tail"] for r in live])
    rms_med, rms_floor = mad_floor([r["rms"] for r in live])
    issues = []
    for r in live:
        if r["gap"] is not None and r["gap"] < 0:
            issues.append((3, r["n"], f"overlaps the next line by {abs(r['gap']):.2f}s",
                           "rebuild the narration naturally and retime the picture "
                           "(export/retime.py) instead of fitting speech to slots"))
        elif r["gap"] is not None and r["gap"] < MIN_GAP:
            issues.append((2, r["n"], f"only {r['gap']:.2f}s before the next line",
                           f"raise --gap; anything under {MIN_GAP}s reads as run-on"))
        if r["rate"] > MAX_RATE:
            issues.append((2, r["n"], f"{r['rate']} syllables/s",
                           "shorten the line; at this rate endings get elided"))
        if tail_floor is not None and r["tail"] < tail_floor:
            issues.append((2, r["n"], f"weak ending ({r['tail']} dB vs median {tail_med:.1f})",
                           "script_lint.py the line and swap the final word, "
                           "or re-roll it with line_doctor.py"))
        if (sib_floor is not None and r["sib_res"] < sib_floor
                and abs(r["sib_res"] - sib_med) >= DEAD_SIB):
            issues.append((1, r["n"], f"dull S ({r['sib']} dB, {r['sib_res']:+.1f} against "
                           f"what this line's own sibilants predict)",
                           "lift 6-8 kHz on this line, or re-roll it"))
        if sib_med is not None and r["sib_res"] > sib_med + max(6, DEAD_SIB):
            issues.append((1, r["n"], f"harsh S ({r['sib']} dB, {r['sib_res']:+.1f} against "
                           f"prediction)", "de-esser is under-doing this line"))
        if (rms_floor is not None and r["rms"] < rms_floor
                and rms_med - r["rms"] >= DEAD_LVL):
            issues.append((1, r["n"], f"quiet ({r['rms']} dBFS vs median {rms_med:.1f})",
                           "level this line before the mix"))
    return issues, dict(sib=sib_med, tail=tail_med, rms=rms_med, sib_slope=slope,
                        sib_floor=sib_floor, tail_floor=tail_floor)


def deep(path, rows):
    """Per-word endings and per-word S, for the lines the cheap pass flagged."""
    from faster_whisper import WhisperModel
    y, sr = load(path)
    m = WhisperModel("base", device="cpu", compute_type="int8",
                     cpu_threads=int(os.environ.get("VOICE_THREADS", "2")))
    segs, _ = m.transcribe(path, word_timestamps=True, language="en")
    out = []
    for s in segs:
        for w in (s.words or []):
            t0, t1 = w.start, w.end
            a, b = int(t0 * sr), int(t1 * sr)
            seg = y[a:b]
            if len(seg) < int(0.06 * sr):
                continue
            body = band(seg, sr, 300, 3400)
            syl = max(1, syllables(w.word))
            out.append(dict(word=w.word.strip(), at=round(t0, 2),
                            dur=round(t1 - t0, 2),
                            # seconds per syllable: this is the "smeared" word he hears —
                            # a word held far longer than the rest of his own delivery
                            per=round((t1 - t0) / syl, 3),
                            tail=round(db(band(seg[-int(0.09 * sr):], sr, 2000, 8000), body), 1),
                            sib=round(db(band(seg, sr, 4000, 9000), body), 1)))
    return out


def watch_burst(path, cues):
    """Did a watched consonant survive as far as the file that actually ships?

    build_voice.py verifies these words on the take before it is polished, then again
    on the line after any rate-correcting stretch — but both checks live inside the
    build, and a caller who does not check the build's exit code ships the file anyway.
    Reel 01 v22 shipped with "three" measuring as a hard burst in the finished mix
    while the take that produced it had passed. This is the same measurement run here,
    against the file check.sh actually gates on, so a broken word cannot reach him
    silently a second time."""
    import burst
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8",
                     cpu_threads=int(os.environ.get("VOICE_THREADS", "2")))
    segs, _ = m.transcribe(path, language="en", word_timestamps=True)
    allw = [{"word": w.word, "at": w.start, "dur": w.end - w.start}
            for sg in segs for w in (sg.words or [])]
    y = burst.load(path)
    # the script writes "3", not "three" — same word the transcriber and build_voice
    # already fold together, so the presence check needs the same digit form
    NUMS = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
            "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10"}
    out = []
    for tw in burst.IN_SCOPE:
        # only words the script actually asked for — a word never spoken this
        # episode has nothing to measure and is not a defect
        digit = NUMS.get(tw)
        pat = r"\b(" + tw + (r"|" + re.escape(digit) if digit else "") + r")\b"
        if not any(re.search(pat, c["line"], re.I) for c in cues):
            continue
        hit = burst.find(allw, tw)
        if hit is None:
            out.append((tw, None, "not in the transcript of the shipped file"))
            continue
        bm = burst.measure(y, float(hit["at"]), float(hit["dur"]))
        if bm is None:
            out.append((tw, None, "could not be measured"))
            continue
        v = burst.verdict(bm)
        out.append((tw, bm["peak"], v))
    return out


def shelf(seg, sr, lo, hi, gain_db):
    """Linear-phase band gain, done in the FFT domain with a smooth edge so the
    correction cannot ring. Used to pull one line's S back toward the others."""
    n = len(seg)
    S = np.fft.rfft(seg)
    f = np.fft.rfftfreq(n, 1 / sr)
    g = np.ones(len(f))
    edge = 800.0
    ramp = np.clip((f - (lo - edge)) / edge, 0, 1) * np.clip(((hi + edge) - f) / edge, 0, 1)
    g = 1 + (10 ** (gain_db / 20) - 1) * ramp
    return np.fft.irfft(S * g, n)


def repair(y, sr, cues, rows, med, out):
    """Level every line onto the median and pull the sibilance outliers in. Both
    corrections are capped, because a big correction means the line should be
    re-generated rather than patched."""
    z = y.copy()
    fixed = []
    for r, c in zip(rows, cues):
        if r["skip"]:
            continue
        a, b = int(float(c["start"]) * sr), int(float(c["end"]) * sr)
        seg = z[a:b].copy()
        notes = []
        d = med["rms"] - r["rms"]
        if abs(d) >= DEAD_LVL:
            d = float(np.clip(d, -4, 4))
            seg *= 10 ** (d / 20)
            notes.append(f"level {d:+.1f} dB")
        # correct exactly what verdict() flags — no wider, no narrower. An earlier
        # version used its own fence here and left a line flagged that it refused to
        # touch, which is the worst of both.
        res = r.get("sib_res", 0.0)
        dull = (med.get("sib_floor") is not None and res < med["sib_floor"]
                and abs(res - med["sib"]) >= DEAD_SIB)
        harsh = res > med["sib"] + max(6, DEAD_SIB)
        ds = med["sib"] - res if (dull or harsh) else 0.0
        if ds:
            ds = float(np.clip(ds, -5, 5))
            seg = shelf(seg, sr, 4000, 9000, ds)
            notes.append(f"S {ds:+.1f} dB")
        if not notes:
            continue
        k = int(0.02 * sr)
        if len(seg) > 2 * k:            # ramp the edges so the step lands in silence
            m = np.ones(len(seg)); m[:k] = np.linspace(0, 1, k); m[-k:] = np.linspace(1, 0, k)
            seg = z[a:b] * (1 - m) + seg * m
        z[a:b] = seg
        fixed.append((r["n"], ", ".join(notes)))
    z = np.clip(z, -1, 1)
    with wave.open(out, "w") as o:
        o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr)
        o.writeframes((z * 32767).astype(np.int16).tobytes())
    return fixed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("--cues", help="defaults to <wav>-cues.json")
    ap.add_argument("--deep", action="store_true", help="per-word pass (needs whisper)")
    ap.add_argument("--json", help="write the full measurement here")
    ap.add_argument("--repair", help="write a corrected wav here: level and sibilance only")
    ap.add_argument("--no-watch", action="store_true",
                    help="skip the shipped-file consonant check (needs whisper + librosa)")
    ap.add_argument("--accept", default="",
                    help="comma-separated watched words he has already approved by ear for "
                         "this file, e.g. after listening to line_doctor.py candidates. The "
                         "measurement still prints — this does not hide a defect, it records "
                         "that his ear already ruled on it, which is the tie-breaker CLAUDE.md "
                         "gives him when the metric and his ear disagree. Write down why in "
                         "SUNDAY.md; don't reach for this to make a check quietly go away.")
    a = ap.parse_args()
    accepted = {w.strip().lower() for w in a.accept.split(",") if w.strip()}

    cues_path = a.cues or os.path.splitext(a.wav)[0] + "-cues.json"
    if not os.path.exists(cues_path):
        sys.exit("no cue file at " + cues_path)
    cues = json.load(open(cues_path))
    cues = cues if isinstance(cues, list) else cues["cues"]

    y, sr = load(a.wav)
    rows = measure(y, sr, cues)
    issues, med = verdict(rows)

    print(f"{a.wav}  {len(y)/sr:.1f}s  {len(cues)} lines")
    print(f"  medians: ending {med['tail']:.1f} dB · level {med['rms']:.1f} dBFS · "
          f"S residual {med['sib']:+.1f} dB (slope {med['sib_slope']:+.1f} dB per sibilant/syllable)")
    print(f"  flagged below: ending {med['tail_floor']:.1f} dB · "
          f"S residual {med['sib_floor']:+.1f} dB  (median - 2.5 robust sd)")
    print(f"  {'ln':>3} {'dur':>5} {'gap':>6} {'rate':>5} {'sib':>6} {'end':>6} {'lvl':>6}  line")
    for r in rows:
        if r["skip"]:
            print(f"  {r['n']:>3}  (too short to measure)  {r['line'][:40]}")
            continue
        g = "  —  " if r["gap"] is None else f"{r['gap']:+.2f}"
        print(f"  {r['n']:>3} {r['dur']:>5} {g:>6} {r['rate']:>5} {r['sib']:>6} "
              f"{r['tail']:>6} {r['rms']:>6}  {r['line'][:38]}")

    print()
    if not issues:
        print("  nothing flagged. every line sits inside his own spread.")
    else:
        sev = {3: "BAD", 2: "fix", 1: "note"}
        for s, n, what, how in sorted(issues, key=lambda x: (-x[0], x[1])):
            print(f"  [{sev[s]}] line {n:>2}: {what}\n         -> {how}")

    if a.repair:
        # levelling one line moves the median, which can push a second line over the
        # fence — so repair until a pass finds nothing left, rather than once
        print(f"\n  repaired -> {a.repair}")
        cur_y, cur_sr, cur_rows, cur_med, total = y, sr, rows, med, 0
        for it in range(1, 4):
            fixed = repair(cur_y, cur_sr, cues, cur_rows, cur_med, a.repair)
            for n, what in fixed:
                print(f"    pass {it}, line {n:>2}: {what}")
            total += len(fixed)
            if not fixed:
                break
            cur_y, cur_sr = load(a.repair)
            cur_rows = measure(cur_y, cur_sr, cues)
            _, cur_med = verdict(cur_rows)
        if not total:
            print("    nothing needed correcting")

    words = deep(a.wav, rows) if a.deep else None
    if words:
        tail_med, tail_floor = mad_floor([w["tail"] for w in words])
        sib_med, sib_floor = mad_floor([w["sib"] for w in words])
        print(f"\n  per word: {len(words)} words · ending median {tail_med:.1f} dB · "
              f"S median {sib_med:.1f} dB")
        worst = sorted(words, key=lambda w: w["tail"])[:8]
        print("  weakest endings:")
        for w in worst:
            print(f"    {w['at']:>6.2f}s  {w['word']:<14} ending {w['tail']:>6.1f} dB")
        per_med, _ = mad_floor([w["per"] for w in words])
        pv = np.array([w["per"] for w in words])
        ceiling = float(np.median(pv) + 2.5 * 1.4826 * np.median(np.abs(pv - np.median(pv))))
        smeared = sorted([w for w in words if w["per"] > ceiling],
                         key=lambda w: -w["per"])[:8]
        print(f"  held too long (over {ceiling:.3f}s per syllable, median {per_med:.3f}):")
        if not smeared:
            print("    none — no word is held out of line with the rest")
        for w in smeared:
            print(f"    {w['at']:>6.2f}s  {w['word']:<14} {w['per']:.3f}s per syllable "
                  f"({w['dur']:.2f}s)")
        ess = [w for w in words if re.search(r"[szc]", w["word"], re.I)]
        if ess:
            for w in sorted(ess, key=lambda w: w["sib"])[:6]:
                print(f"    {w['at']:>6.2f}s  {w['word']:<14} S {w['sib']:>6.1f} dB")

    if a.json:
        json.dump(dict(lines=rows, medians=med, words=words,
                       issues=[dict(sev=s, line=n, what=w, fix=f) for s, n, w, f in issues]),
                  open(a.json, "w"), indent=1)
        print(f"\n  wrote {a.json}")

    watch_bad = False
    if not a.no_watch:
        try:
            hits = watch_burst(a.wav, cues)
        except ImportError as e:
            hits = None
            print(f"\n  [skip] consonant check needs {e.name} — not installed, not checked")
        if hits:
            print(f"\n  the shipped file, measured:")
            for tw, peak, v in hits:
                note = " (accepted by ear, see SUNDAY.md)" if tw in accepted else ""
                if peak is None:
                    print(f"    \"{tw}\": {v}{note}")
                    if tw not in accepted:
                        watch_bad = True
                    continue
                print(f"    \"{tw}\": {peak:+.1f} dB, {v}{note}")
                if v != "frication" and tw not in accepted:
                    watch_bad = True
            if watch_bad:
                print(f"  the take-level check runs before the mix; this runs on the file "
                      f"that actually ships. Re-roll the flagged line and rebuild.")

    return 1 if (watch_bad or any(s == 3 for s, *_ in issues)) else 0


if __name__ == "__main__":
    sys.exit(main())
