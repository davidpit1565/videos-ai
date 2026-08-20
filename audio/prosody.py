#!/usr/bin/env python3
"""Does the line sound finished?

He heard it before any tool did: "the melody of 'every chat' sounds like it keeps
going, and it is actually the end of the sentence." That is intonation, and it is
measurable — a statement in English ends with the pitch falling below the speaker's
own median for that line. A flat or rising ending reads as a question, or as a
sentence that has not finished.

Measured on episode 01, seven of seventeen lines ended ABOVE their own median:
"Open Settings." +5.6 semitones, "Write ENGINE below..." +5.5, "Custom
instructions." +4.3. The line he flagged sat at +0.2 — flat, unresolved.

  python3 audio/prosody.py audio/voice/ep01-final3.wav
"""
import argparse, json, os, sys, wave
import numpy as np

FALL_ST = -1.5      # a statement should land at least this far under its own median


def load(path):
    with wave.open(path) as w:
        sr = w.getframerate()
        y = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return y, sr


def f0_track(y, sr, fmin=70, fmax=300, hop=0.01, win=0.04, thresh=0.30):
    """Autocorrelation pitch, one estimate per hop. 0 where unvoiced.

    Deliberately simple: this is a contour question, not a synthesis-grade tracker.
    A frame is voiced only when its autocorrelation peak carries 30% of the frame's
    energy, which keeps breath and room tone out of the contour."""
    n, h = int(win * sr), int(hop * sr)
    lo, hi = int(sr / fmax), int(sr / fmin)
    out = []
    for i in range(0, max(0, len(y) - n), h):
        s = y[i:i + n]
        if np.sqrt((s ** 2).mean()) < 0.005:
            out.append(0.0)
            continue
        s = s - s.mean()
        ac = np.correlate(s, s, "full")[n - 1:]
        if ac[0] <= 0 or hi <= lo:
            out.append(0.0)
            continue
        seg = ac[lo:hi]
        k = int(np.argmax(seg)) + lo
        out.append(sr / k if ac[k] / ac[0] > thresh else 0.0)
    return np.array(out), hop


def final_drop(y, sr, tail=0.18, span=0.35):
    """Semitones between the end of the line and the line's own median pitch, plus
    the slope over the last `span` seconds. Negative means it lands."""
    f0, hop = f0_track(y, sr)
    v = np.where(f0 > 0)[0]
    if len(v) < 8:
        return None, None, None
    med = float(np.median(f0[v]))
    last = v[-1] * hop
    tailv = [f0[i] for i in v if i * hop >= last - tail]
    end = float(np.median(tailv)) if tailv else med
    st = 12 * np.log2(end / med)
    xs = [i * hop for i in v if i * hop >= last - span]
    ys = [f0[i] for i in v if i * hop >= last - span]
    slope = float(np.polyfit(xs, ys, 1)[0]) if len(xs) >= 5 else None
    return float(st), slope, med


def ends_sentence(text):
    return bool(text) and text.strip().rstrip('"”’)').endswith((".", "!", "?"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("--cues", help="defaults to <wav>-cues.json")
    ap.add_argument("--fall", type=float, default=FALL_ST)
    a = ap.parse_args()
    cues_path = a.cues or os.path.splitext(a.wav)[0] + "-cues.json"
    cues = json.load(open(cues_path))
    cues = cues if isinstance(cues, list) else cues["cues"]
    y, sr = load(a.wav)

    print(f"{a.wav}  statement endings must land at or below {a.fall:+.1f} semitones")
    print(f"  {'ln':>3} {'end':>8} {'slope':>7} {'F0':>6}  line")
    bad = []
    for c in cues:
        st, slope, med = final_drop(
            y[int(float(c["start"]) * sr):int(float(c["end"]) * sr)], sr)
        if st is None:
            print(f"  {c['n']:>3}   (too short to measure)")
            continue
        flag = ""
        if ends_sentence(c["line"]) and st > a.fall:
            flag = "  <- unfinished"
            bad.append((c["n"], round(st, 1)))
        print(f"  {c['n']:>3} {st:+7.1f}st {slope:+7.0f} {med:6.0f}  {c['line'][:38]}{flag}")
    print()
    if bad:
        print(f"  {len(bad)} of {len(cues)} statement endings do not land: {bad}")
        print("  -> re-roll those lines; build_voice --prosody does it while generating")
    else:
        print("  every statement ending lands.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
