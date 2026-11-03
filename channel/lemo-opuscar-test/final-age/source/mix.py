import sys, json, numpy as np, soundfile as sf, soxr
sys.path.insert(0, '/root/lemo-opuscar/core/audio')
import sfx
from sfx import SR
from scipy.ndimage import uniform_filter1d
H = '/tmp/claude-0/-home-user-videos-ai/55529e32-2ffe-57f5-a74d-513316ab2ea5/scratchpad/lemo-age-final/'
ev = json.load(open(H + 'events.json')); DUR = ev['dur']; N = int(DUR * SR)
dj = json.load(open(H + 'voices/dur.json')); T = {}; c = .3
for k in ['l1','l2','l3','l4','l5','l6','l7','l8','l9']: T[k] = c; c += dj[k] + .22
json.dump(T, open(H + 'cues.json', 'w'))
voice = np.zeros(N, np.float32)
for k, t0 in T.items():
    x, sr = sf.read(H + f'voices/{k}.wav', dtype='float32')
    if x.ndim > 1: x = x.mean(1)
    x = soxr.resample(x, sr, SR).astype(np.float32); i = int(t0 * SR); voice[i:i + len(x)] += x[:N - i]
voice = sfx.compress(voice, .2, 3.0); voice *= 0.9 / max(1e-6, np.abs(voice).max())
beat = 60 / 100; f = lambda m: 440 * 2 ** ((m - 69) / 12)
def mallet(fr, d=1.3):
    tt = sfx.t_(d); e = np.exp(-tt / .35)
    y = np.sin(2 * np.pi * fr * tt + 1.2 * np.exp(-tt / .06) * np.sin(2 * np.pi * fr * 3.99 * tt)) * e
    return (y * (1 - np.exp(-tt / .002))).astype(np.float32)
scale = [60, 62, 64, 67, 69, 72, 74, 76]            # C major pentatonic, all >= MIDI 60 (no sub-bass)
mus = np.zeros((N, 2), np.float32)
pat = [0, 2, 4, 2, 3, 5, 4, 2, 1, 3, 4, 6, 5, 3, 2, 1]
for i in range(int(DUR / (beat / 2))):
    t0 = i * beat / 2
    if t0 < .2: continue
    m = scale[pat[i % 16] % 8]
    sfx.add(mus, mallet(f(m)), t0, .45 + .15 * (i % 2 == 0), -.2 + .4 * ((i % 3) / 2))
pad = np.zeros((N, 2), np.float32); chords = [[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62]]
for j, ch in enumerate(chords * 4):
    a, b = j * 8 * beat, (j + 1) * 8 * beat
    if a >= DUR: break
    s, e = int(a * SR), min(N, int((b + 1.2) * SR)); seg = np.arange(e - s) / SR
    env = np.minimum(1, seg / 1.2) * np.minimum(1, (b + 1.2 - a - seg) / 1.2)
    for m in ch: pad[s:e] += ((np.sin(2 * np.pi * f(m) * seg) + .35 * np.sin(2 * np.pi * f(m) * 2 * seg)).astype(np.float32) * env * .10)[:, None]
mus = (mus + pad).astype(np.float32)
fo = np.zeros((N, 2), np.float32)
for e in ev['ev']:
    t0 = e['t']; ty = e['type']
    if ty == 'whoosh': sfx.add(fo, sfx.whoosh(.35, .5), t0 - .1, .45)
    elif ty == 'click': sfx.add(fo, sfx.click(1.6, .6), t0, .4)
    elif ty == 'tick':
        for k in range(6): sfx.add(fo, sfx.click(1.3 + .05 * k, .6), t0 + k * .21 + .02 * (k % 2), .25)
    elif ty == 'thud': sfx.add(fo, sfx.pop(.7), t0, .5)
    elif ty == 'ding': sfx.add(fo, sfx.ding(.7), t0, .4)
    elif ty == 'crash': sfx.add(fo, sfx.crash(.8), t0 - .02, .55)
vl = uniform_filter1d(np.abs(voice), int(.12 * SR)); duck = 1 - np.clip(vl * 14, 0, 1) * .8
duck = uniform_filter1d(duck, int(.25 * SR))[:, None]
# music level: ~ -17 dB RMS relative to the voice RMS over speaking parts
def rms(x): return float(np.sqrt(np.mean(x ** 2) + 1e-12))
sp = np.abs(voice) > .02
mg = (rms(voice[sp]) * 10 ** (-17 / 20)) / rms((mus * duck)[sp.nonzero()[0]].reshape(-1)) if sp.any() else .1
mix = voice[:, None] + mus * duck * mg + fo * (1 - .5 * (duck < .6)) * .35
mix = np.stack([sfx.limit(mix[:, 0], .9), sfx.limit(mix[:, 1], .9)], 1).astype(np.float32)
sf.write(H + 'mix.wav', mix, SR); sf.write(H + 'music_only.wav', (mus * mg).astype(np.float32), SR)
print('mix ok', len(mix) / SR, 'music gain', round(mg, 4))
