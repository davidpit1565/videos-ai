# join4.py <seedA> <seedB> (run with /opt/v311/bin/python): line 4 of v4 = two whole takes of two separate sentences,
# "For Calendly, Cal D I Y." (pl3/L4a-<seedA>.wav) then "For Intercom, Chatwoot." (pl3/L4b-<seedB>.wav), 0.12 s apart, level-matched.
# No cut inside a sentence. Output pl3/L4-90.wav + cues.
import sys, json, numpy as np, soundfile as sf
sa, sb = sys.argv[1], sys.argv[2]
def take(p):
    w, sr = sf.read(f'pl3/L{p}.wav'); c = json.load(open(f'pl3/L{p}-cues.json'))[0]
    x = w[int(max(0, c['start'] - .04) * sr):int(min(len(w), (c['end'] + .08) * sr))].copy(); f = int(.012 * sr)
    x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f); return x, sr
A, sr = take(f'4a-{sa}'); B, _ = take(f'4b-{sb}')
r = lambda x: np.sqrt((x ** 2).mean()); B *= r(A) / r(B)
y = np.concatenate([np.zeros(int(.05 * sr)), A, np.zeros(int(.12 * sr)), B, np.zeros(int(.1 * sr))])
sf.write('pl3/L4-90.wav', y, sr, subtype='PCM_16')
json.dump([{'n': 1, 'line': 'For Calendly, Cal D I Y. For Intercom, Chatwoot.', 'start': 0.09, 'end': round(len(y) / sr - .18, 3)}], open('pl3/L4-90-cues.json', 'w'))
print('dur', round(len(y) / sr, 2))
