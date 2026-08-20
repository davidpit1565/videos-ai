"""Delivery, not phonetics.

"Speaks outward and does not pull the viewer in" is not a consonant. What separates
an engaging read from a flat one is measurable with a few seconds of audio: how much
the pitch actually moves, how fast it moves, how much of the time is speech rather
than gap, and how loud the loud parts are against the quiet parts.

Phonetics needs many tokens of one sound. This needs only continuous speech, which
is why it can be measured against an 18-second reference where the consonants cannot.
"""
import sys, json, argparse, numpy as np

SR = 16000
HOP = 0.010

def load(p):
    import librosa
    y, _ = librosa.load(p, sr=SR, mono=True)
    return y / (np.abs(y).max() + 1e-9)

def f0(y):
    import librosa
    f, vflag, _ = librosa.pyin(y, fmin=60, fmax=350, sr=SR,
                               frame_length=1024, hop_length=int(HOP * SR))
    return f, vflag

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav"); ap.add_argument("--words", required=True)
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    y = load(a.wav)
    words = json.load(open(a.words))["words"]
    dur = len(y) / SR
    f, vflag = f0(y)
    v = f[~np.isnan(f)]
    st = 12 * np.log2(v / np.median(v)) if len(v) else np.array([0.0])

    # how much the pitch moves, per second of voiced speech
    d = np.abs(np.diff(12 * np.log2(v))) if len(v) > 1 else np.array([0.0])
    move = float(np.nansum(d) / max(0.1, len(v) * HOP))

    frames_ = np.lib.stride_tricks.as_strided(
        y, (max(0, 1 + (len(y) - 400) // 160), 400),
        (y.strides[0] * 160, y.strides[0]))
    rms = 20 * np.log10(np.sqrt((frames_ ** 2).mean(1)) + 1e-9)
    loud = rms[rms > rms.max() - 35]

    spoken = sum(float(w["dur"]) for w in words)
    syl = sum(max(1, len(__import__("re").findall(r"[aeiouy]+", w["word"].lower())))
              for w in words)
    print(f"{a.label or a.wav.split('/')[-1]}   {dur:.1f}s, {len(words)} words")
    print(f"  rate           {syl / max(0.1, spoken):5.2f} syl/s   "
          f"{len(words) / dur * 60:5.0f} words/min")
    print(f"  speech density {spoken / dur * 100:5.1f}%  of the time is speech")
    print(f"  pitch median   {np.median(v):5.0f} Hz")
    print(f"  pitch range    {np.percentile(st, 90) - np.percentile(st, 10):5.1f} "
          f"semitones (10th-90th)")
    print(f"  pitch movement {move:5.1f} semitones per second of voice")
    print(f"  loudness range {loud.max() - np.percentile(loud, 10):5.1f} dB")

if __name__ == "__main__":
    main()

# Reference measured with this tool, 2026-08-20: instagram.com/reel/DXl2d6lDKKf
# (Miki Michaeli / Videya.be, 18.0s, 72 words) — 239 words/min at 86.6% speech
# density, against 129 wpm at 64.4% for our reel. Pitch range was the opposite of
# the guess: ours is 15.2 semitones against his 8.5, so the read is not flat. The
# audio itself is deliberately not committed.
