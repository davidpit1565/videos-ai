# splice3.py (run with /opt/v311/bin/python): line 3 of v3 = "Loom? Try Cap." from the take pl2/L3-43.wav (cut after "Cap.", 1.22 s)
# + "Notion? AppFlowy." from the v2 take pl/L5-11.wav (cut before "Notes", 1.60 s), level-matched, with a 0.5 s pause between
# so the word FREE can land on Cap before Notion starts. Cut points are Whisper word times read on 16.11.2026.
import json, numpy as np, soundfile as sf
A, sr = sf.read('pl2/L3-43.wav'); B, sr2 = sf.read('pl/L5-11.wav'); assert sr == sr2
ca = json.load(open('pl2/L3-43-cues.json'))[0]
segA = A[int(max(0, ca['start'] - .04) * sr):int(1.22 * sr)].copy(); segB = B[0:int(1.60 * sr)].copy()
f = int(.012 * sr)
for x in (segA, segB): x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
r = lambda x: np.sqrt((x ** 2).mean()); segB *= r(segA) / r(segB)
y = np.concatenate([np.zeros(int(.05 * sr)), segA, np.zeros(int(.5 * sr)), segB, np.zeros(int(.1 * sr))])
sf.write('pl2/L3-90.wav', y, sr, subtype='PCM_16')
json.dump([{'n': 1, 'line': 'Loom? Try Cap. Notion? AppFlowy.', 'start': 0.09, 'end': round(len(y) / sr - .18, 3)}], open('pl2/L3-90-cues.json', 'w'))
print('dur', round(len(y) / sr, 2))
