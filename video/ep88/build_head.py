#!/usr/bin/env python3
"""ep88 integrator. lines.txt (8 lines) + VOICE/<n>.wav -> cues.json, out/narration.wav, hf/index.html [--render name].
Env: VOICE (dir with 1..8.wav, default voice/final), GAPS (7 gaps, default below), TAIL (seconds after line 8, default 1.1).
Word times: no whisper here, so words inside a line are placed by sentence: the k-1 longest silences in the line wav split it into its k
sentences, and words are spread over each sentence by letter count. Good to ~0.1-0.2 s; the value card rows use it."""
import json, os, re, sys, subprocess
import soundfile as sf, numpy as np
H = os.path.dirname(os.path.abspath(__file__))
VOICE = os.environ.get("VOICE", H + "/voice/final")
GAPS = [float(x) for x in os.environ.get("GAPS", "0.32,0.34,0.36,0.36,5.0").split(",")]
TAIL = float(os.environ.get("TAIL", "1.1"))
ALL = [l.rstrip("\n") for l in open(H + "/lines.txt") if l.strip()]
assert len(ALL) == 6 and len(GAPS) == 5
sr = 48000


def words_for(x, text, t0):
    """list of [start,end] absolute for each space-separated word."""
    toks = text.split()
    sents = [s for s in re.findall(r"[^.!?]+[.!?]*", text) if s.strip()]
    d = len(x) / sr
    # frame rms 10 ms
    f = int(sr * 0.01); n = len(x) // f
    r = np.sqrt(np.mean(x[:n * f].reshape(n, f) ** 2, axis=1) + 1e-12)
    thr = max(r.max() * 0.04, 1e-4)
    sil = r < thr
    # voiced span
    idx = np.where(~sil)[0]
    a, b = (idx[0], idx[-1] + 1) if len(idx) else (0, n)
    runs = []; i = a
    while i < b:
        if sil[i]:
            j = i
            while j < b and sil[j]: j += 1
            if j - i >= 6: runs.append((j - i, i, j))
            i = j
        else: i += 1
    k = len(sents)
    cuts = sorted(sorted(runs, reverse=True)[:k - 1], key=lambda z: z[1])
    bounds = [a * f / sr]
    segs = []
    for ln, i0, j0 in cuts:
        segs.append((bounds[-1], i0 * f / sr)); bounds.append(j0 * f / sr)
    segs.append((bounds[-1], b * f / sr))
    out = []; wi = 0
    for (s0, s1), s in zip(segs, sents):
        ws = s.split()
        wts = np.array([len(w.strip(".,!?'")) + 2 for w in ws], float); wts /= wts.sum()
        c = s0
        for w, p in zip(ws, wts):
            out.append([round(t0 + c, 3), round(t0 + c + p * (s1 - s0), 3)]); c += p * (s1 - s0)
    assert len(out) == len(toks), (len(out), len(toks), text)
    return out


lines = []; t = 0.0; parts = []
for j in range(6):
    n = j + 1
    x, s = sf.read(f"{VOICE}/{n}.wav"); assert s == sr; x = x if x.ndim == 1 else x[:, 0]
    d = len(x) / sr
    ln = dict(n=n, text=ALL[j], start=round(t, 3), end=round(t + d, 3), words=words_for(x, ALL[j], t))
    lines.append(ln); parts.append((int(t * sr), x)); t += d + (GAPS[j] if j < 5 else 0)
D = round(lines[-1]["end"] + TAIL, 2)
nar = np.zeros(int((D + 0.3) * sr))
for i0, x in parts: nar[i0:i0 + len(x)] += x
os.makedirs(H + "/out", exist_ok=True)
sf.write(H + "/out/narration.wav", nar[:int(D * sr)], sr, subtype="PCM_16")
json.dump(dict(lines=lines, D=D), open(H + "/cues.json", "w"), indent=1)

