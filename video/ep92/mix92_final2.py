#!/usr/bin/env python3
"""ep92 final2 audio: existing narration92.wav (no TTS) padded to D + quiet sfx layer (sfx92.json as in final1, plus one pop on the send line); no music bed."""
import subprocess, json, re, os, numpy as np, soundfile as sf
H = os.path.dirname(os.path.abspath(__file__)); SR = 48000; D = 11.9
def load(p, sr=SR): return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout, dtype=np.float32)
nar = load(f"{H}/out/narration92.wav"); N = int(D * SR); nar = np.pad(nar, (0, max(0, N - len(nar))))[:N]
ev = json.load(open(H + '/sfx92.json')) + [dict(f='pop_a.ogg', t=9.78, g=-5)]
lay = np.zeros(N + SR)
for e in ev:
    x = load(f"{H}/sfx/{e['f']}")
    x = x / (np.abs(x).max() + 1e-9) * 10 ** ((-14 + e['g']) / 20); i0 = int(e['t'] * SR); n = min(len(x), len(lay) - i0)
    if n > 0 and e['t'] < D - 0.1: lay[i0:i0 + n] += x[:n]
sf.write(f"{H}/out/sfx2.wav", lay[:N], SR, subtype='PCM_16'); sf.write(f"{H}/out/nar2.wav", nar, SR, subtype='PCM_16')
fc = "[0:a][1:a]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1:LRA=11[o]"
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f"{H}/out/nar2.wav", '-i', f"{H}/out/sfx2.wav", '-filter_complex', fc, '-map', '[o]', '-ar', '48000', f"{H}/out/mix2-pre.wav"], check=True)
m = subprocess.run(['ffmpeg', '-i', f"{H}/out/mix2-pre.wav", '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f"{H}/out/mix2-pre.wav", '-af', f'volume={-14.0 - I}dB,alimiter=limit=0.84:level=false,afade=t=out:st={D - 0.4}:d=0.4', '-ar', '48000', f"{H}/out/mix2.wav"], check=True)
print('pre', I)
