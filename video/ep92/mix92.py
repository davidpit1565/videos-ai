#!/usr/bin/env python3
"""ep92 audio. Usage: mix92.py <cues.json> <voice|novoice> <out.wav>   (no music bed; quiet sfx; voice variant = narration92.wav dominant at -14 LUFS)"""
import sys, subprocess, re, numpy as np, soundfile as sf
cues, mode, outp = sys.argv[1], sys.argv[2], sys.argv[3]
sys.argv = [sys.argv[0], cues]
import build92 as b
H = "/home/user/videos-ai/video/ep92"; SFXD = "/home/user/videos-ai/video/ep93/sfx/"; SR = 48000; D = b.D; N = int(D * SR)
def load(p): return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, dtype=np.float32).astype(np.float64)
def t_of_src(s):
    ts = np.linspace(b.P0, b.tI, 4000); ss = np.array([float(b._SRCMAP(t)) for t in ts]); return float(ts[np.argmin(np.abs(ss - s))])
lay = np.zeros(N + SR)
def put(name, t, db):
    x = load(SFXD + name + ".ogg"); x = x / (np.abs(x).max() + 1e-9) * 10 ** (db / 20); i0 = int(t * SR); n = min(len(x), len(lay) - i0)
    if n > 0 and t < D - 0.1: lay[i0:i0 + n] += x[:n]
up = 0 if mode == "voice" else 9           # no-voice file: sfx only, so the same sfx are raised (still sparse, nothing added)
put("impactsoft", 0.03, -24 + up); put("pop_a", t_of_src(2.0), -24 + up); put("pop_b", t_of_src(3.6), -27 + up)
put("ding", b.tH, -22 + up); put("impactsoft", b.END_T, -24 + up)
if mode == "voice":
    nar = load(f"{H}/voice/narration92.wav"); nar = np.pad(nar, (0, max(0, N - len(nar))))[:N]; nar *= 10 ** (-3 / 20) / np.abs(nar).max()
    mix = nar + lay[:N]; target = -14.0
else:
    mix = lay[:N]; target = None
sf.write(f"{H}/out/_pre.wav", mix, SR, subtype='PCM_16')
m = subprocess.run(['ffmpeg', '-i', f"{H}/out/_pre.wav", '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1])
if target is None:
    # sfx-only: raise to the loudest level that keeps true peak under -1 dBTP, capped at -17 LUFS (do not force more)
    peak = float(np.abs(mix).max()); gmax = -1.5 - 20 * np.log10(peak + 1e-9); g = min(-17.0 - I, gmax)
else: g = target - I
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f"{H}/out/_pre.wav", '-af', f'volume={g}dB,alimiter=limit=0.88:attack=3:release=80:level=false,afade=t=out:st={D - 0.35}:d=0.35', '-ar', '48000', outp], check=True)
print("pre", I, "gain", round(g, 2), "D", D)
