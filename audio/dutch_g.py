"""The Flemish G, measured against his own.

Flemish has the "zachte G": a soft palatal fricative, articulated forward, with
modest friction and often some voicing. Netherlands Dutch has the "harde G": a
uvular fricative, further back, louder and hissier, with energy pushed high.

There is no invented threshold here. His own recording IS Flemish — he is Flemish —
so it is the target, and the only question is how far a generated take drifts from
it. Same tool on both sides, one comparison.

  centroid  spectral centre of the fricative. A hard G sits higher than a soft one.
  fric      friction energy 2-6kHz, relative to the vowel that follows it.
  voiced    fraction of the fricative that is periodic. The soft G often is.
"""
import sys, json, argparse, numpy as np

SR = 16000
HOP, WIN = 0.005, 0.020

def load(p):
    import librosa
    y, _ = librosa.load(p, sr=SR, mono=True)
    return y / (np.abs(y).max() + 1e-9)

def frames(y, hop=HOP, win=WIN):
    h, w = int(hop * SR), int(win * SR)
    n = max(0, 1 + (len(y) - w) // h)
    return np.lib.stride_tricks.as_strided(
        y, (n, w), (y.strides[0] * h, y.strides[0])).copy()

def spec(F):
    S = np.abs(np.fft.rfft(F * np.hanning(F.shape[1]), axis=1))
    f = np.fft.rfftfreq(F.shape[1], 1 / SR)
    return S, f

def band(S, f, lo, hi):
    m = (f >= lo) & (f < hi)
    return 20 * np.log10(np.sqrt((S[:, m] ** 2).mean(1)) + 1e-9)

def periodicity(y):
    F = frames(y, HOP, 0.030)
    out = np.zeros(len(F))
    lo, hi = int(SR / 350), min(int(SR / 70), F.shape[1] - 1)
    for i, fr in enumerate(F):
        fr = fr - fr.mean(); e = (fr ** 2).sum()
        if e < 1e-8 or hi <= lo: continue
        a = np.correlate(fr, fr, "full")[len(fr) - 1:]
        out[i] = a[lo:hi].max() / (e + 1e-12)
    return out

def g_words(words):
    """Where the Dutch G fricative actually is.

    Two corrections over a first version. Word-initial "ch" is not this sound —
    "chatbot", "chocolade" are loanwords with /tS/, and counting one of them was
    the same mistake as reading "chat" in English as a /k/. And Dutch G is mostly
    *medial*: uitleggen, agenten, dagen, morgen. Only looking at word-initial G
    found nothing at all in his own recording, which is where it appears least.
    """
    out = []
    for w in words:
        raw = "".join(c for c in w["word"].lower() if c.isalpha())
        if len(raw) < 2:
            continue
        if raw.startswith("g"):
            out.append((w, "G-", 0.0))
        elif "gg" in raw:
            out.append((w, "-gg-", raw.index("gg") / len(raw)))
        elif "g" in raw[1:]:
            out.append((w, "-g-", raw.index("g", 1) / len(raw)))
        if "ch" in raw[1:]:                 # acht, licht, echt — not chatbot
            out.append((w, "-ch", raw.index("ch", 1) / len(raw)))
    return out

def measure(y, at, dur, per, frac=0.0):
    # for a medial G, start the search where in the word the letter sits
    at = at + frac * dur * 0.85
    dur = max(0.08, dur * (1.0 - frac * 0.6))
    a, b = int(at * SR), int((at + min(dur, 0.35)) * SR)
    seg = y[a:b]
    if len(seg) < int(0.06 * SR):
        return None
    F = frames(seg)
    if len(F) < 8:
        return None
    S, f = spec(F)
    lowe, hie = band(S, f, 80, 1000), band(S, f, 2000, 6000)
    # The fricative is where the high band most beats the low band — then grow
    # outward from there. Walking forward from the window start only works for a
    # word-initial G; for a medial one the window opens inside a vowel, the first
    # frame is already below threshold, and the search returns nothing. That is why
    # his own recording measured zero.
    r = hie - lowe
    if len(r) < 6:
        return None
    peak = int(np.argmax(r))
    thr = r.min() + 0.45 * (r.max() - r.min())
    if r[peak] < r.min() + 3:
        return None
    i0, i1 = peak, peak + 1
    while i0 > 0 and r[i0 - 1] > thr:
        i0 -= 1
    while i1 < len(r) and r[i1] > thr:
        i1 += 1
    if i1 - i0 < 3:
        return None
    fr_end = i1
    Sf = S[i0:i1]
    cen = float((f * Sf).sum() / (Sf.sum() + 1e-9))
    vow = band(S[fr_end:min(len(S), fr_end + 14)], f, 2000, 6000)
    if not len(vow):
        return None
    b0 = int(at / HOP) + i0
    pv = per[b0:b0 + (i1 - i0)]
    return dict(centroid=round(cen, 0),
                fric=round(float(hie[:fr_end].mean() - vow.mean()), 1),
                voiced=round(float((pv > 0.45).mean()) if len(pv) else 0.0, 2),
                dur=round((i1 - i0) * HOP * 1000, 0))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav"); ap.add_argument("--words", required=True)
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    y = load(a.wav); per = periodicity(y)
    rows = []
    for w, kind, frac in g_words(json.load(open(a.words))["words"]):
        m = measure(y, float(w["at"]), float(w["dur"]), per, frac)
        if m:
            m.update(word=w["word"], kind=kind, at=round(float(w["at"]), 2))
            rows.append(m)
    print(f"{a.label or a.wav.split('/')[-1]}  {len(rows)} G fricatives")
    if not rows:
        return
    for k in ("centroid", "fric", "voiced", "dur"):
        v = np.array([r[k] for r in rows], dtype=float)
        unit = "Hz" if k == "centroid" else ("dB" if k == "fric" else
                                            ("ms" if k == "dur" else ""))
        print(f"  {k:9s} median {np.median(v):8.1f}{unit}   "
              f"range {v.min():.1f}-{v.max():.1f}")
    for r in sorted(rows, key=lambda r: -r["centroid"])[:6]:
        print(f"    {r['at']:6.2f}s {r['kind']}  {r['centroid']:6.0f}Hz  "
              f"fric {r['fric']:+5.1f}dB  voiced {r['voiced']:.2f}  {r['word']}")

if __name__ == "__main__":
    main()
