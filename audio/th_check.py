"""Is that a TH, or a T wearing a TH's clothes?

He has flagged "three" three times. The reason it survives every other check is that
the transcriber hears it correctly either way — "three" spelled from a [t] is still the
word "three" — and the ending-energy metric only reads the last 90ms of a word.

English /θ/ and Flemish [t] differ at the START, and they differ in kind rather than
degree:

  /θ/  a weak, diffuse fricative. Noise that lasts 60-120ms and arrives gradually.
  [t]  a stop. Near-silence, then one sharp transient, then straight into the vowel.

So the measurement is duration of frication before voicing, and how abruptly the energy
rose. A high rise over a short window is a stop; a gentle rise over a long one is the
fricative we want. Nothing here decides whether it sounds good — his ear does that —
but it ranks candidates so the ear is choosing between the best few instead of eight.
"""
import sys, json, argparse, numpy as np

SR, HOP, WIN = 16000, 0.0025, 0.010

def load(p):
    import librosa
    y, _ = librosa.load(p, sr=SR, mono=True)
    return y / (np.abs(y).max() + 1e-9)

def frames(y):
    h, w = int(HOP * SR), int(WIN * SR)
    n = max(0, 1 + (len(y) - w) // h)
    return np.lib.stride_tricks.as_strided(
        y, (n, w), (y.strides[0] * h, y.strides[0])).copy()

def band(F, lo, hi):
    S = np.abs(np.fft.rfft(F * np.hanning(F.shape[1]), axis=1))
    f = np.fft.rfftfreq(F.shape[1], 1 / SR)
    m = (f >= lo) & (f < hi)
    return 20 * np.log10(np.sqrt((S[:, m] ** 2).mean(1)) + 1e-9)

def measure(y, at, dur):
    a = max(0, int((at - 0.02) * SR))
    b = min(len(y), int((at + min(dur, 0.30)) * SR))
    F = frames(y[a:b])
    if len(F) < 10:
        return None
    hi = band(F, 3000, 8000)      # where a dental fricative lives
    lo = band(F, 80, 900)         # the vowel behind it
    # voicing starts where the low band overtakes its own floor by a clear margin
    floor = lo[:6].min()
    vi = next((i for i in range(3, len(lo)) if lo[i] > floor + 12), len(lo) - 1)
    if vi < 3:
        return None
    pre = hi[:vi]
    rise = float(np.max(np.diff(pre))) if len(pre) > 2 else 99.0
    return dict(fric_ms=vi * HOP * 1000,
                rise=round(rise, 1),
                energy=round(float(pre.mean() - lo[:6].mean()), 1))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav"); ap.add_argument("--words", required=True)
    ap.add_argument("--word", default="three")
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    y = load(a.wav)
    words = json.load(open(a.words))["words"]
    rows = []
    for w in words:
        raw = "".join(c for c in w["word"].lower() if c.isalnum())
        if raw != a.word and not (a.word == "three" and raw == "3"):
            continue
        m = measure(y, float(w["at"]), float(w["dur"]))
        if m:
            m["at"] = round(float(w["at"]), 2)
            rows.append(m)
    name = a.label or a.wav.split("/")[-1]
    if not rows:
        print(f"{name:22s}  the word never appears")
        return
    for r in rows:
        # A real dental fricative is 45-160ms with audible high-band noise and no
        # single spike. Anything longer with nothing in it is the detector losing the
        # voicing onset, not a very long TH — the first version measured 222ms at
        # -25.8dB, which is silence, and calling that a fricative would have been the
        # measurement lying to agree with me.
        if r["energy"] < -18 or r["fric_ms"] > 160:
            verdict = "unmeasured"
        elif r["fric_ms"] >= 45 and r["rise"] < 9:
            verdict = "fricative"
        else:
            verdict = "stop-like"
        print(f"{name:22s} {r['at']:6.2f}s  frication {r['fric_ms']:5.1f}ms  "
              f"sharpest rise {r['rise']:5.1f}dB  energy {r['energy']:+5.1f}dB  {verdict}")

if __name__ == "__main__":
    main()
