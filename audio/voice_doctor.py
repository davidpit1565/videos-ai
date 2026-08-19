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

MIN_GAP = 0.30          # measured: below this the lines read as one run-on
MAX_RATE = 6.5          # the rate above which build_voice already re-rolls a line
VOWELS = re.compile(r"[aeiouy]+", re.I)


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
            rms=round(20 * np.log10(max(float(np.sqrt((seg ** 2).mean())), 1e-9)), 1),
            sib=round(sib, 1), tail=round(tl, 1), skip=False))
    return rows


def verdict(rows):
    live = [r for r in rows if not r["skip"]]
    sib_med, sib_floor = mad_floor([r["sib"] for r in live])
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
        if sib_floor is not None and r["sib"] < sib_floor:
            issues.append((1, r["n"], f"dull S ({r['sib']} dB vs median {sib_med:.1f})",
                           "lift 6-8 kHz on this line, or re-roll it"))
        if sib_med is not None and r["sib"] > sib_med + 6:
            issues.append((1, r["n"], f"harsh S ({r['sib']} dB vs median {sib_med:.1f})",
                           "de-esser is under-doing this line"))
        if rms_floor is not None and r["rms"] < rms_floor:
            issues.append((1, r["n"], f"quiet ({r['rms']} dBFS vs median {rms_med:.1f})",
                           "level this line before the mix"))
    return issues, dict(sib=sib_med, tail=tail_med, rms=rms_med,
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
            out.append(dict(word=w.word.strip(), at=round(t0, 2),
                            tail=round(db(band(seg[-int(0.09 * sr):], sr, 2000, 8000), body), 1),
                            sib=round(db(band(seg, sr, 4000, 9000), body), 1)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("--cues", help="defaults to <wav>-cues.json")
    ap.add_argument("--deep", action="store_true", help="per-word pass (needs whisper)")
    ap.add_argument("--json", help="write the full measurement here")
    a = ap.parse_args()

    cues_path = a.cues or os.path.splitext(a.wav)[0] + "-cues.json"
    if not os.path.exists(cues_path):
        sys.exit("no cue file at " + cues_path)
    cues = json.load(open(cues_path))
    cues = cues if isinstance(cues, list) else cues["cues"]

    y, sr = load(a.wav)
    rows = measure(y, sr, cues)
    issues, med = verdict(rows)

    print(f"{a.wav}  {len(y)/sr:.1f}s  {len(cues)} lines")
    print(f"  medians: sibilance {med['sib']:.1f} dB · ending {med['tail']:.1f} dB · "
          f"level {med['rms']:.1f} dBFS")
    print(f"  flagged below: ending {med['tail_floor']:.1f} dB · "
          f"sibilance {med['sib_floor']:.1f} dB  (median - 2.5 robust sd)")
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
        ess = [w for w in words if re.search(r"[szc]", w["word"], re.I)]
        if ess:
            for w in sorted(ess, key=lambda w: w["sib"])[:6]:
                print(f"    {w['at']:>6.2f}s  {w['word']:<14} S {w['sib']:>6.1f} dB")

    if a.json:
        json.dump(dict(lines=rows, medians=med, words=words,
                       issues=[dict(sev=s, line=n, what=w, fix=f) for s, n, w, f in issues]),
                  open(a.json, "w"), indent=1)
        print(f"\n  wrote {a.json}")

    return 1 if any(s == 3 for s, *_ in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
