# /opt/v311/bin/python stitch.py: places the three picked takes at fixed story times -> narration.wav + narration-cues.json
import json, numpy as np, soundfile as sf
def cut(wav, cues, i):
    w, sr = sf.read(wav); w = w.mean(1) if w.ndim > 1 else w
    x = cues[i]; a = max(0, int((x['start'] - .05) * sr)); b = int((x['end'] + .08) * sr); return w[a:b], sr, x
L = open('lines.txt').read().splitlines()
picks = [('p/P33.wav', 'p/P33-cues.json', 0), ('p/R44.wav', 'p/R44-cues.json', 1), ('p/Q11.wav', 'p/Q11-cues.json', 1)]
seg = []
for w, c, i in picks:
    d, sr, x = cut(w, json.load(open(c)), i); seg.append((d, sr, x['end'] - x['start']))
sr = seg[0][1]
s1 = 0.35; e1 = s1 + seg[0][2]; TC = e1 + 0.45; s2 = TC + 1.0; e2 = s2 + seg[1][2]; s3 = e2 + 2.2; e3 = s3 + seg[2][2]
N = int(round((e3 + 1.3) * 100) / 100 * sr); out = np.zeros(N); cues = []
for (d, _, dur), s, e, ln in zip(seg, (s1, s2, s3), (e1, e2, e3), L):
    i0 = int((s - .05) * sr); out[i0:i0 + len(d)] += d; cues.append(dict(n=len(cues) + 1, line=ln, start=round(s, 2), end=round(e, 2)))
sf.write('narration.wav', out, sr); json.dump(cues, open('narration-cues.json', 'w'), indent=1); print(cues)
