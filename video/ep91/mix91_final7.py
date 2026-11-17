#!/usr/bin/env python3
"""ep91 final7 audio: narration91c.wav + real-library bed (exact length, ducked under speech, fade-out) + quiet sfx re-timed to the cue-driven picture;
loudnorm about -14 LUFS, true peak under -1 dBTP.  usage: mix91_final7.py <bed.wav (exact length)> <tag>"""
import subprocess, sys, re, os, json, numpy as np
import soundfile as sf
import build91_final7 as b
H = "/home/user/videos-ai/video/ep91"; SR = 48000; D = b.D
bedp, tag = sys.argv[1], sys.argv[2]
def load(p, sr=SR): return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout, dtype=np.float32).astype(np.float64)
def band(x, sr=SR):
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2; f = np.fft.rfftfreq(len(x), 1 / sr)
    return 10 * np.log10(X[(f >= 300) & (f < 3500)].sum() / len(x) ** 2 + 1e-20)
N = int(D * SR); nar = load(f"{H}/voice/narration91c.wav"); nar = np.pad(nar, (0, max(0, N - len(nar))))[:N]
nar *= 10 ** (-3 / 20) / np.abs(nar).max(); vb = band(nar)
lay = np.zeros(N + SR)
def put(name, t, db):
    x = load(f"{H}/sfx/{name}.ogg"); x = x / (np.abs(x).max() + 1e-9) * 10 ** (db / 20); i0 = int(t * SR); n = min(len(x), len(lay) - i0)
    if n > 0 and t < D - 0.1: lay[i0:i0 + n] += x[:n]
ev = [("impactpunch", .02, -22), ("whoosh_a", b.T_SW1, -25), ("whoosh_b", b.T_IN2, -25), ("pop_a", b.wordt(2, "chat"), -26),
      ("pop_a", b.T_STEPS + 0.1, -25), ("pop_b", b.wordt(2, "tangled"), -26), ("whoosh_c", b.T_SW2, -25), ("pop_a", b.s3, -25),
      ("impactsoft", b.wordt(3, "over") + 0.05, -24), ("pop_b", b.wordt(3, "everything"), -26)] 
for name, t, db in ev: put(name, t, db)
sf.write(f"{H}/out/nar7.wav", nar, SR, subtype='PCM_16'); sf.write(f"{H}/out/sfx7.wav", lay[:N], SR, subtype='PCM_16')
bed = load(bedp); bed = np.pad(bed, (0, max(0, N - len(bed))))[:N]; t_ = np.arange(N) / SR
def ss(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
bed *= (1 - ss((t_ - (D - 0.8)) / 0.8)); sf.write(f"{H}/out/bedraw7-{tag}.wav", bed, SR, subtype='PCM_16')
raw = f"{H}/out/bedshaped7-{tag}.wav"
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f"{H}/out/bedraw7-{tag}.wav", '-af', 'highpass=f=140', '-ar', '48000', raw], check=True)
g = vb - 11 - band(load(raw))
fc = ("[0:a]asplit=2[v1][key];[1:a]volume=%.2fdB[b];[b][key]sidechaincompress=threshold=0.05:ratio=4:attack=12:release=420[duck];[duck]asplit=2[d1][d2];"
      "[v1][d1][2:a]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[o]") % g
wav = f"{H}/out/mix7-{tag}.wav"; duck = f"{H}/out/duck7-{tag}.wav"
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f"{H}/out/nar7.wav", '-i', raw, '-i', f"{H}/out/sfx7.wav", '-filter_complex', fc, '-map', '[o]', '-ar', '48000', wav, '-map', '[d2]', duck], check=True)
m = subprocess.run(['ffmpeg', '-i', wav, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1]); fix = -14.0 - I
tmp = wav[:-4] + '-pre.wav'; os.replace(wav, tmp)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-af', f'volume={fix}dB,alimiter=limit=0.85:attack=3:release=80:level=false', '-ar', '48000', wav], check=True); os.remove(tmp)
print('bed ducked vs voice (300-3500 Hz): %.1f dB; fix %.2f dB; bed gain %.1f dB; lin(with fix) %.3f' % (band(load(duck)) - vb, fix, g, 10 ** (g / 20) * 10 ** (fix / 20)))
