#!/usr/bin/env python3
"""Syllable cut points of 'Anthropic(s)' inside a window: AN | THRO | PIC(+s). Returns seconds (start, AN|THRO, THRO|PIC, end) from the voiced low-band envelope (2.5 ms hop)."""
import sys, numpy as np, librosa
from scipy.signal import find_peaks
sys.path.insert(0, ".")
import rword, thword, stress
SR = 16000
def cuts(y, a, b):
    hop = 0.0025; lf, _ = thword.band_env(y, 80, 1500, hop=hop)
    i0, i1 = int(a / hop), int(b / hop); seg = lf[i0:i1]; sm = np.convolve(seg, np.ones(5) / 5, mode="same")
    pk, _ = find_peaks(sm, prominence=2.0, distance=int(0.06 / hop))
    top = sorted(pk[np.argsort(sm[pk])[-3:]])
    c = [int(top[k] + np.argmin(sm[top[k]:top[k + 1]])) + i0 for k in range(2)]
    return [a, c[0] * hop, c[1] * hop, b], [round(float(t) * hop + a, 3) for t in top]
if __name__ == "__main__":
    for arg in sys.argv[1:]:
        p, *ab = arg.split(":"); y, _ = librosa.load(p, sr=SR); y /= np.abs(y).max() + 1e-9
        a, b = (float(ab[0]), float(ab[1])) if ab else stress.word_window(y)
        c, nuc = cuts(y, a, b); print(arg.split("/")[-1], "word", round(a, 3), round(b, 3), "cuts", [round(x, 3) for x in c], "nuclei(top3)", nuc)
