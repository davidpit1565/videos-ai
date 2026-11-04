"""env.py <narration.wav> : voices/env.json = amplitude envelope of the narration at 100 Hz (RMS, 10 ms hop, smoothed ~80 ms, normalised to the 95th percentile, 0..1)."""
import sys, json, os, numpy as np, soundfile as sf, soxr
from scipy.ndimage import uniform_filter1d
here = os.path.dirname(os.path.abspath(__file__))
x, sr = sf.read(sys.argv[1], dtype='float32'); x = x.mean(1) if x.ndim > 1 else x
if sr != 16000: x = soxr.resample(x, sr, 16000).astype('float32')
hop = 160; n = len(x) // hop
r = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)       # 10 ms RMS
r = uniform_filter1d(r, 8)                                              # ~80 ms smoothing
r = r / max(1e-9, np.percentile(r, 95)); r = np.clip(r, 0, 1.2)
r[r < .06] = 0
json.dump([round(float(v), 3) for v in r], open(os.path.join(here, 'voices', 'env.json'), 'w'))
print('env', len(r), 'frames (100 Hz), mean %.2f' % r.mean())
