# stitch.py (/opt/v311/bin/python): joins the chosen per-line takes into narration-v105.wav + narration-v105-cues.json, and ../cues105.json
import json, os, numpy as np, soundfile as sf
D = os.path.dirname(os.path.abspath(__file__)) + '/'
PICK = {1: 11, 2: 11, 3: 11, 4: 22, 5: 77, 6: 33, 7: 11, 8: 33, 9: 66, 10: 11, 11: 77, 12: 11, 13: "ep104"}
lines = [l.strip() for l in open(D + 'lines105.txt') if l.strip()]
out = []; cues = []; t = 0.0; GAP = .06
for n, l in enumerate(lines, 1):
    w, sr = sf.read(D + f'pl/L{n}-{PICK[n]}.wav')
    if w.ndim > 1: w = w.mean(1)
    f = int(.01 * sr); w = w.copy(); w[:f] *= np.linspace(0, 1, f); w[-f:] *= np.linspace(1, 0, f)
    out += [w, np.zeros(int(GAP * sr))]
    cues.append({'n': n, 'line': l, 'text': l, 'start': round(t + .05, 3), 'end': round(t + len(w) / sr - .08, 3)}); t += len(w) / sr + GAP
y = np.concatenate(out); sf.write(D + 'narration-v105.wav', y, sr, subtype='PCM_16')
json.dump(cues, open(D + 'narration-v105-cues.json', 'w'), indent=1)
json.dump({'version': 'v1', 'estimated_timeline': False, 'lines': cues, 'D': round(len(y) / sr, 2)}, open(D + '../cues105.json', 'w'), indent=1)
print(sr, round(len(y) / sr, 2)); [print(c['n'], round(c['end'] - c['start'], 2), c['start']) for c in cues]
