#!/usr/bin/env python3
"""ep90 final12 audio: narration90.wav (existing cloned voice, no TTS) dominant + quiet sfx re-timed to the new beats; NO music bed.
Outputs out/nar12.wav, out/sfx12.wav (for the checks) and out/mix12.wav (-14 LUFS, true peak under -1 dBTP)."""
import subprocess, re, os, random, numpy as np
import soundfile as sf
import build90i as b
H = "/home/user/videos-ai/video/ep90"; SFXD = "/home/user/videos-ai/video/ep93/sfx/"; SR = 48000; D = b.D
def load(p): return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, dtype=np.float32).astype(np.float64)
N = int(D * SR); nar = load(f"{H}/voice/narration90.wav"); nar = np.pad(nar, (0, max(0, N - len(nar))))[:N]
nar *= 10 ** (-3 / 20) / np.abs(nar).max()
lay = np.zeros(N + SR); ot = b.ot
def put(name, t, db):
    x = load(SFXD + name + ".ogg"); x = x / (np.abs(x).max() + 1e-9) * 10 ** (db / 20); i0 = int(t * SR); n = min(len(x), len(lay) - i0)
    if n > 0 and t < D - 0.1: lay[i0:i0 + n] += x[:n]
random.seed(11)
put("impactsoft", 0.02, -24)
for a, c in [(1.3, 9.5), (18.0, 30.4), (40.4, 41.5), (48.3, 49.6)]:
    t, te = ot(a), ot(c)
    while t < te:
        put(random.choice(["tick", "click_b"]), t, -30 + 3 * random.random()); t += 0.13 + 0.07 * random.random()
for s_ in (10.3, 13.0, 31.5, 50.0): put("pop_a", ot(s_), -26)
put("select", ot(41.8), -25); put("ding", ot(33.5), -24); put("pop_b", ot(44.0), -26); put("impactsoft", ot(54.95), -22); put("pop_a", 16.25, -27)
sf.write(f"{H}/out/nar12.wav", nar, SR, subtype='PCM_16'); sf.write(f"{H}/out/sfx12.wav", lay[:N], SR, subtype='PCM_16')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f"{H}/out/nar12.wav", '-i', f"{H}/out/sfx12.wav", '-filter_complex', '[0:a][1:a]amix=inputs=2:normalize=0[o]', '-map', '[o]', '-ar', '48000', f"{H}/out/mix12-pre.wav"], check=True)
m = subprocess.run(['ffmpeg', '-i', f"{H}/out/mix12-pre.wav", '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1]); g = -14.0 - I
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f"{H}/out/mix12-pre.wav", '-af', f'volume={g}dB,alimiter=limit=0.86:attack=3:release=80:level=false,afade=t=out:st={D - 0.35}:d=0.35', '-ar', '48000', f"{H}/out/mix12.wav"], check=True)
print("pre", I, "gain", round(g, 2))
