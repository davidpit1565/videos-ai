# /opt/v311/bin/python stitchT.py <hook.wav> <hook-cues.json> : new hook take + the unchanged takes of lines 2-9 cut out of the shipped narration2.wav -> narrationT.wav, narrationT-cues.json, linesT.txt
import json, sys, numpy as np, soundfile as sf
D = '/home/user/videos-ai/video/ep103t/voice/'
hw, hc = sys.argv[1], json.load(open(sys.argv[2]))[0]
old = json.load(open(D + 'narration2-cues.json')); w0, sr = sf.read(D + 'narration2.wav')
if w0.ndim > 1: w0 = w0.mean(1)
h, sh = sf.read(hw)
if h.ndim > 1: h = h.mean(1)
assert sh == sr, (sh, sr)
GAP = old[1]['start'] - old[0]['end']                      # 0.19 s in the shipped cut
a = int(max(0, hc['start'] - .05) * sr); b = int((hc['end'] + .08) * sr)
hook = h[a:b].copy(); f = int(.01 * sr); hook[:f] *= np.linspace(0, 1, f); hook[-f:] *= np.linspace(1, 0, f)
end1 = .05 + (hc['end'] - hc['start']); new2 = end1 + GAP
cut_old = old[1]['start'] - .095; cut_new = new2 - .095   # tail starts here in old / new time
body = hook
pad = int(cut_new * sr) - len(body); assert pad >= 0, pad
y = np.concatenate([body, np.zeros(pad), w0[int(cut_old * sr):]])
delta = new2 - old[1]['start']
cues = [dict(n=1, line=hc['line'], text=hc['line'], start=round(.05, 3), end=round(end1, 3))]
for c in old[1:]: cues.append(dict(n=c['n'], line=c['line'], text=c.get('text', c['line']), start=round(c['start'] + delta, 3), end=round(c['end'] + delta, 3)))
sf.write(D + 'narrationT.wav', y, sr, subtype='PCM_16')
json.dump(cues, open(D + 'narrationT-cues.json', 'w'), indent=1)
open(D + 'linesT.txt', 'w').write('\n'.join(c['line'] for c in cues) + '\n')
print(len(y) / sr, 'delta', round(delta, 3), [(c['n'], c['start'], c['end']) for c in cues])
