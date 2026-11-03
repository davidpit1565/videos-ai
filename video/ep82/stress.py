#!/usr/bin/env python3
"""Syllable stress PROXY for "Anthropic('s)": AN / THRO / PIC (/ S) per take.  English primary stress is an-THROP-ic: THRO should be the most prominent.
Syllables come from the voiced low band (80-1500 Hz) envelope inside the word: the three biggest nuclei at least 60 ms apart, boundaries at the dips between them (the TH fricative sits in the AN|THRO dip).
Per syllable: f0 peak in semitones above the word's median f0, RMS peak (dB) relative to the word's loudest syllable, duration share of the word.
  prominence = f0_rise_st + 0.5 * rms_rel_db + 10 * duration_share      (rms_rel_db <= 0)
PASS = THRO beats AN by >= 1.5 st of f0 peak OR >= 3 dB of RMS peak, AND PIC prominence < THRO prominence.
usage: stress.py <wav> [<wav> ...]   (line-9 takes: word window found by CTC start + the end of the /s/);  wav:a:b = a word window in seconds (e.g. line 2: voice/final/2.wav:0.04:0.616)"""
import sys, json, numpy as np, librosa
from scipy.signal import find_peaks
sys.path.insert(0, ".")
import rword, thword
SR = 16000

def hf_end(y, a, b):
    hf, hop = thword.band_env(y, 3000, 8000); i0, i1 = int(a / hop), min(len(hf), int(b / hop)); w = hf[i0:i1]; ok = np.where(w >= w.max() - 12)[0]
    return (i0 + ok[-1]) * hop + 0.012

def word_window(y):
    ws, we = rword.locate(y)
    return max(0.0, ws - 0.02), hf_end(y, we - 0.04, we + 0.25)

def measure(y, a, b):
    hop = 0.0025
    lf, _ = thword.band_env(y, 80, 1500, hop=hop); db, _ = rword.env_db(y, hop=hop, win=0.015)
    i0, i1 = int(a / hop), int(b / hop)
    seg = lf[i0:i1]; sm = np.convolve(seg, np.ones(5) / 5, mode="same")
    pk, pr = find_peaks(sm, prominence=2.0, distance=int(0.06 / hop))
    if len(pk) < 3: return dict(ok=False, nuclei=len(pk))
    top = sorted(pk[np.argsort(sm[pk])[-3:]])                    # the three biggest nuclei, in time order
    cuts = [i0] + [int(top[k] + np.argmin(sm[top[k]:top[k + 1]])) + i0 for k in range(2)] + [i1]
    f0, _, _ = librosa.pyin(y, fmin=70, fmax=400, sr=SR, frame_length=1024, hop_length=int(hop * SR))
    t = np.arange(len(f0)) * hop
    word_f0 = f0[(t >= a) & (t <= b)]; word_f0 = word_f0[~np.isnan(word_f0)]
    med = np.median(word_f0) if len(word_f0) else 150.0
    syl = []
    for name, c0, c1 in zip(("AN", "THRO", "PIC"), cuts[:3], cuts[1:]):
        w = (t >= c0 * hop) & (t < c1 * hop); ff = f0[w]; ff = ff[~np.isnan(ff)]
        f0rise = 12 * np.log2(ff.max() / med) if len(ff) else 0.0
        rms = float(db[c0:c1].max()); syl.append(dict(name=name, dur=(c1 - c0) * hop, f0_rise_st=float(f0rise), rms_db=rms))
    mx = max(s["rms_db"] for s in syl); tot = sum(s["dur"] for s in syl)
    for s in syl:
        s["rms_rel_db"] = s["rms_db"] - mx; s["dur_share"] = s["dur"] / tot
        s["prominence"] = s["f0_rise_st"] + 0.5 * s["rms_rel_db"] + 10 * s["dur_share"]
    an, th, pic = syl
    df0 = th["f0_rise_st"] - an["f0_rise_st"]; drms = th["rms_db"] - an["rms_db"]
    ok = (df0 >= 1.5 or drms >= 3.0) and pic["prominence"] < th["prominence"]
    return dict(ok=True, pass_=bool(ok), nuclei=len(pk), THRO_minus_AN_f0_st=round(df0, 1), THRO_minus_AN_rms_db=round(drms, 1),
                prom={s["name"]: round(s["prominence"], 1) for s in syl}, f0={s["name"]: round(s["f0_rise_st"], 1) for s in syl},
                rms_rel={s["name"]: round(s["rms_rel_db"], 1) for s in syl}, dur={s["name"]: round(s["dur"], 3) for s in syl}, word=[round(a, 3), round(b, 3)])

if __name__ == "__main__":
    out = {}
    for arg in sys.argv[1:]:
        p, *ab = arg.split(":")
        y, _ = librosa.load(p, sr=SR); y = y / (np.abs(y).max() + 1e-9)
        a, b = (float(ab[0]), float(ab[1])) if ab else word_window(y)
        m = measure(y, a, b); out[arg.split("/")[-1]] = m
        print(arg.split("/")[-1], json.dumps(m), flush=True)
    json.dump(out, open("stress.json", "w"), indent=1)
