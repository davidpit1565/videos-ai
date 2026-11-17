# stitch5.py (run with /opt/v311/bin/python): joins the chosen per-line slices p5/S<n>-<seed>.wav into narration-v5.wav + narration-v5-cues.json
import sys, json, os, numpy as np, soundfile as sf
D = os.path.dirname(os.path.abspath(__file__)) + '/'
V = sys.argv[1]
PICK = {1: 11, 2: 11, 3: 22, 4: 99, 5: 11, 6: 11, 7: 11, 8: 11, 9: 22}
lines = [l.strip() for l in open(D + f'lines5{V}.txt') if l.strip()]
out = []; cues = []; t = 0.0; GAP = .06
for n, l in enumerate(lines, 1):
    w, sr = sf.read(D + (f'p5/S1-{V}.wav' if n == 1 else f'p5/S{n}-{PICK[n]}.wav'))
    f = int(.01 * sr); w = w.copy(); w[:f] *= np.linspace(0, 1, f); w[-f:] *= np.linspace(1, 0, f)
    out += [w, np.zeros(int(GAP * sr))]
    cues.append({'n': n, 'line': l, 'start': round(t + .05, 3), 'end': round(t + len(w) / sr - .08, 3)}); t += len(w) / sr + GAP
y = np.concatenate(out); sf.write(D + f'narration-v5{V}.wav', y, sr, subtype='PCM_16')
json.dump(cues, open(D + f'narration-v5{V}-cues.json', 'w'), indent=1); print(sr, round(len(y) / sr, 2))
