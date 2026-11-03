#!/usr/bin/env python3
"""Find the word "Anthropic's" in a take of 'The links to Anthropic's own report are in the caption.', refine its edges to the nearest energy valleys, and measure a PROXY for R emphasis.
Proxy only (no listening): LPC-based F3 track inside the word (a strong American/rhotic R pulls F3 down below ~2300 Hz), plus a 15-40 Hz amplitude-modulation share (trill/tap), plus duration, level and f0 at the edges.
usage: rword.py <wav> [<wav> ...]  -> prints one line per file and writes rword.json"""
import sys, json, numpy as np, librosa
import torch, torchaudio
SR = 16000
_B = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
_M = _B.get_model().eval(); _LAB = _B.get_labels()
TXT = "THE|LINKS|TO|ANTHROPIC'S|OWN|REPORT|ARE|IN|THE|CAPTION"

def env_db(y, hop=0.005, win=0.015):
    h, w = int(hop * SR), int(win * SR)
    n = max(1, (len(y) - w) // h)
    return np.array([20 * np.log10(np.sqrt(np.mean(y[i * h:i * h + w] ** 2)) + 1e-9) for i in range(n)]), hop

def locate(y):
    """CTC forced alignment of the known sentence; returns (start, end) of "Anthropic's" in seconds."""
    with torch.no_grad(): em, _ = _M(torch.tensor(y, dtype=torch.float32)[None])
    em = torch.log_softmax(em, -1); d = {c: i for i, c in enumerate(_LAB)}
    tok = torch.tensor([[d[c] for c in TXT]])
    al, sc = torchaudio.functional.forced_align(em, tok, blank=0)
    spans = torchaudio.functional.merge_tokens(al[0], sc[0]); ratio = len(y) / em.shape[1] / SR
    i = 0
    for w in TXT.split("|"):
        sp = spans[i:i + len(w)]; i += len(w)
        if w.startswith("ANTHROPIC"): return sp[0].start * ratio, sp[-1].end * ratio
    return None

def valley(db, hop, lo, hi):
    a, b = max(0, int(lo / hop)), min(len(db), int(hi / hop) + 1)
    return (a + int(np.argmin(db[a:b]))) * hop

def edges(y):
    r = locate(y)
    if r is None: return None
    ws, we = r
    db, hop = env_db(y)
    a = valley(db, hop, ws - 0.09, ws + 0.02)
    b = valley(db, hop, we - 0.04, we + 0.07)
    return a, b, db, hop

def f3_track(y, a, b):
    seg = librosa.resample(y[int(a * SR):int(b * SR)], orig_sr=SR, target_sr=10000); R = 10000
    out = []
    fl, hl = int(0.025 * R), int(0.010 * R)
    for i in range(0, len(seg) - fl, hl):
        fr = seg[i:i + fl] * np.hanning(fl)
        if np.sqrt(np.mean(fr ** 2)) < 0.01: continue
        fr = np.append(fr[0], fr[1:] - 0.97 * fr[:-1])
        try: A = librosa.lpc(fr, order=12)
        except Exception: continue
        fq = []
        for r in np.roots(A):
            if np.imag(r) <= 0.01: continue
            f = np.angle(r) * R / (2 * np.pi); bw = -np.log(np.abs(r)) * R / np.pi
            if 200 < f < 4800 and bw < 500: fq.append(f)
        fq = sorted(fq)
        if len(fq) >= 3: out.append(fq[2])
    return np.array(out)

def measure(y, a, b):
    f3 = f3_track(y, a, b)
    seg = y[int(a * SR):int(b * SR)]
    e = np.abs(librosa.stft(seg, n_fft=512, hop_length=80)).sum(0) if len(seg) > 512 else np.array([1.0])
    e = e - e.mean(); X = np.abs(np.fft.rfft(e * np.hanning(len(e)))) ** 2; f = np.fft.rfftfreq(len(e), 80 / SR)
    am = float(X[(f >= 15) & (f <= 40)].sum() / (X[(f >= 2) & (f <= 100)].sum() + 1e-12))
    f0, _, _ = librosa.pyin(seg, fmin=70, fmax=400, sr=SR, frame_length=1024); ok = ~np.isnan(f0)
    st = lambda v: float(12 * np.log2(v / 100.0))
    return dict(dur=round(b - a, 3), rms_db=round(float(20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9)), 1),
                f3_low_frac=round(float((f3 < 2300).mean()), 2) if len(f3) else None,
                f3_min=round(float(f3.min())) if len(f3) else None, f3_med=round(float(np.median(f3))) if len(f3) else None,
                am_15_40=round(am, 3), f0_start_st=round(st(np.nanmedian(f0[ok][:4])), 1) if ok.sum() > 6 else None,
                f0_end_st=round(st(np.nanmedian(f0[ok][-4:])), 1) if ok.sum() > 6 else None)

if __name__ == "__main__":
    res = {}
    for p in sys.argv[1:]:
        y, _ = librosa.load(p, sr=SR); y = y / (np.abs(y).max() + 1e-9)
        e = edges(y)
        if e is None: print(p, "NO WORD FOUND"); continue
        a, b, db, hop = e
        m = measure(y, a, b); m.update(a=round(a, 3), b=round(b, 3)); res[p.split("/")[-1]] = m
        print(p.split("/")[-1], m, flush=True)
    json.dump(res, open("rword.json", "w"), indent=1)
