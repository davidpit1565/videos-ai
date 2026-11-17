# /opt/v311/bin/python stitch.py : joins the picked take of every line into narration.wav + narration-cues.json
import json, soundfile as sf, numpy as np, sys
PICK = {1:'55',2:'11',3:'55',4:'11',5:'11',6:'55',7:'11',8:'11',9:'33',10:'T33',11:'11',12:'33'}
lines = open('lines.txt').read().splitlines()
GAP = 0.19; out = []; cues = []; t = 0.0; sr0 = None
for i in range(1, len(lines)+1):
    w, sr = sf.read(f'p/S{i}-{PICK[i]}.wav'); sr0 = sr
    if w.ndim > 1: w = w.mean(1)
    start = t + .05; end = t + len(w)/sr - .08
    out.append(w); cues.append(dict(n=i, line=lines[i-1], start=round(start,2), end=round(end,2)))
    t = end + GAP - .05
    # trailing pad handled by next slice's leading .05
    out.append(np.zeros(int(max(0, (t - (start - .05 + len(w)/sr)))*sr)))
a = np.concatenate(out); sf.write('narration.wav', a, sr0)
json.dump(cues, open('narration-cues.json','w'), indent=1); print(round(len(a)/sr0,2), 's', len(cues), 'lines')
