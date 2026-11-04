import sys, json, numpy as np, soundfile as sf, soxr
sys.path.insert(0, '/root/lemo-opuscar/core/audio')
import sfx
from sfx import SR
from scipy.ndimage import uniform_filter1d
import os
H = os.path.dirname(os.path.abspath(__file__)) + '/'
ev = json.load(open(H + 'events.json')); DUR = ev['dur']; N = int(DUR * SR)
# the voice = David's cloned narration, untouched (no compression, no re-normalising); final level is set by mux.sh loudnorm
x, sr = sf.read(H + 'voices/narration.wav', dtype='float32')
if x.ndim > 1: x = x.mean(1)
if sr != SR: x = soxr.resample(x, sr, SR).astype(np.float32)
voice = np.zeros(N, np.float32); voice[:min(N, len(x))] = x[:N]
beat = 60 / 100; f = lambda m: 440 * 2 ** ((m - 69) / 12)
def mallet(fr, d=1.3):
    tt = sfx.t_(d); e = np.exp(-tt / .35)
    y = np.sin(2 * np.pi * fr * tt + 1.2 * np.exp(-tt / .06) * np.sin(2 * np.pi * fr * 3.99 * tt)) * e
    return (y * (1 - np.exp(-tt / .002))).astype(np.float32)
scale = [60, 62, 64, 67, 69, 72, 74, 76]
mus = np.zeros((N, 2), np.float32)
pat = [0, 2, 4, 2, 3, 5, 4, 2, 1, 3, 4, 6, 5, 3, 2, 1]
for i in range(int(DUR / (beat / 2))):
    t0 = i * beat / 2
    if t0 < .2: continue
    m = scale[pat[i % 16] % 8]
    sfx.add(mus, mallet(f(m)), t0, .45 + .15 * (i % 2 == 0), -.2 + .4 * ((i % 3) / 2))
pad = np.zeros((N, 2), np.float32); chords = [[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62]]
for j, ch in enumerate(chords * 6):
    a, b = j * 8 * beat, (j + 1) * 8 * beat
    if a >= DUR: break
    s, e = int(a * SR), min(N, int((b + 1.2) * SR)); seg = np.arange(e - s) / SR
    env = np.minimum(1, seg / 1.2) * np.minimum(1, (b + 1.2 - a - seg) / 1.2)
    for m in ch: pad[s:e] += ((np.sin(2 * np.pi * f(m) * seg) + .35 * np.sin(2 * np.pi * f(m) * 2 * seg)).astype(np.float32) * env * .10)[:, None]
def kick(d=.2):
    tt = sfx.t_(d); ph = 2 * np.pi * (45 * tt + 75 * (1 - np.exp(-tt / .03)) * .03); return (np.sin(ph) * np.exp(-tt / .07)).astype(np.float32)
def hat(d=.05): return (sfx.hp(sfx.noise(d), 6000) * sfx.env_exp(d, .01)).astype(np.float32)
KK, HH = kick(), hat()
for i in range(int(DUR / beat)):
    if i * beat > .1: sfx.add(mus, KK, i * beat, .55); sfx.add(mus, HH, i * beat + beat / 2, .16)
mus = (mus + pad).astype(np.float32)
# fade the bed out over the last 1.5 s
fade = np.clip((DUR - np.arange(N) / SR) / 1.5, 0, 1).astype(np.float32); mus *= fade[:, None]
fo = np.zeros((N, 2), np.float32)
rg = np.random.default_rng(7)
for e in ev['ev']:
    t0 = e['t']; ty = e['type']; vj = float(rg.uniform(.8, 1.15))   # every foley hit gets its own level
    if ty == 'whoosh': sfx.add(fo, sfx.whoosh(.35 + .15 * vj, .5), t0, .45 * vj)
    elif ty == 'click': sfx.add(fo, sfx.click(1.5 + .2 * vj, .6), t0, .4 * vj)
    elif ty == 'tick':
        for k, off in enumerate([0, .17, .41, .58, .84, 1.0]): sfx.add(fo, sfx.click(1.3 + .05 * k, .6), t0 + off, .25 * vj)   # uneven, like a hand
    elif ty == 'tap': sfx.add(fo, sfx.click(1.9 + .3 * vj, .5), t0, .12 * vj)
    elif ty == 'thud': sfx.add(fo, sfx.pop(.7), t0, .5 * vj)
    elif ty == 'ding': sfx.add(fo, sfx.ding(.7), t0, .4)
    elif ty == 'crash': sfx.add(fo, sfx.crash(.8), t0 - .02, .55)
vl = uniform_filter1d(np.abs(voice), int(.12 * SR)); vpk = max(1e-6, np.abs(voice).max())
duck = 1 - np.clip(vl / vpk * 14, 0, 1) * .8
duck = uniform_filter1d(duck, int(.25 * SR))[:, None]
def rms(x): return float(np.sqrt(np.mean(x ** 2) + 1e-12))
sp = np.abs(voice) > .02 * vpk
mg = (rms(voice[sp]) * 10 ** (-17 / 20)) / rms((mus * duck)[sp.nonzero()[0]].reshape(-1))
mix = voice[:, None] + mus * duck * mg + fo * (1 - .5 * (duck < .6)) * .35 * (vpk / .9)
mix = np.stack([sfx.limit(mix[:, 0], .9 * max(vpk, .5)), sfx.limit(mix[:, 1], .9 * max(vpk, .5))], 1).astype(np.float32)
sf.write(H + 'mix.wav', mix, SR); sf.write(H + 'music_only.wav', (mus * mg).astype(np.float32), SR)
print('mix ok', len(mix) / SR, 'music gain', round(mg, 4), 'voice peak', round(vpk, 3))
