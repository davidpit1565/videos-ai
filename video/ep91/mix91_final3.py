#!/usr/bin/env python3
"""ep91 final3 audio: NO narration. The same quiet sfx layer as final2 (sfx91.json + one pop on the send line), no bed, scaled to about -18 LUFS, limited under -1 dBTP."""
import subprocess, json, re, os, numpy as np, soundfile as sf
H = os.path.dirname(os.path.abspath(__file__)); SR = 48000; D = 11.9
def load(p): return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, dtype=np.float32)
N = int(D * SR); lay = np.zeros(N + SR)
for e in json.load(open(H + '/sfx91.json')) + [dict(f='pop_a.ogg', t=9.78, g=-5)]:
    x = load(f"{H}/sfx/{e['f']}"); x = x / (np.abs(x).max() + 1e-9) * 10 ** ((-14 + e['g']) / 20); i0 = int(e['t'] * SR); n = min(len(x), len(lay) - i0)
    if n > 0 and e['t'] < D - 0.1: lay[i0:i0 + n] += x[:n]
sf.write(f"{H}/out/sfx3-pre.wav", lay[:N], SR, subtype='PCM_16')
m = subprocess.run(['ffmpeg', '-i', f"{H}/out/sfx3-pre.wav", '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1]); g = -18.0 - I
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f"{H}/out/sfx3-pre.wav", '-af', f'volume={g}dB,alimiter=limit=0.8:attack=2:release=60:level=false,afade=t=out:st={D - 0.4}:d=0.4', '-ar', '48000', f"{H}/out/sfx3.wav"], check=True)
print("pre", I, "gain", round(g, 1))
