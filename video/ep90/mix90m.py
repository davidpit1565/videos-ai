#!/usr/bin/env python3
"""ep90 final14 audio: narration90b.wav (cloned voice, ep89 recipe, rendered by another agent) dominant + REAL-library music bed (exact length, ducked under speech,
-4 dB tender dip under the begging line, fade-out) + quiet sfx re-timed to the new beats; loudnorm about -14 LUFS, true peak under -1 dBTP.
usage: mix90k.py <bed.wav (exact length)> <tag>  -> out/mix17-<tag>.wav, out/bedshaped17-<tag>.wav, out/gain17-<tag>.json"""
import subprocess, sys, re, os, json, random, numpy as np
import soundfile as sf
import build90m as b
H = "/home/user/videos-ai/video/ep90"; SFXD = "/home/user/videos-ai/video/ep93/sfx/"; SR = 48000; D = b.D
bedp, tag = sys.argv[1], sys.argv[2]
def load(p, sr=SR): return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout, dtype=np.float32).astype(np.float64)
def band(x, sr=SR):
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2; f = np.fft.rfftfreq(len(x), 1 / sr)
    return 10 * np.log10(X[(f >= 300) & (f < 3500)].sum() / len(x) ** 2 + 1e-20)
N = int(D * SR)
nar = load(f"{H}/voice/narration90b.wav"); nar = np.pad(nar, (0, max(0, N - len(nar))))[:N]
cues = json.load(open(f"{H}/voice/cues90b.json"))["lines"]
vb = band(nar)
# sfx layer (quiet), same cues/levels as final12
lay = np.zeros(N + SR); ot = b.ot
def put(name, t, db):
    x = load(SFXD + name + ".ogg"); x = x / (np.abs(x).max() + 1e-9) * 10 ** (db / 20); i0 = int(t * SR); n = min(len(x), len(lay) - i0)
    if n > 0 and t < D - 0.1: lay[i0:i0 + n] += x[:n]
random.seed(11)
put("impactsoft", 0.02, -24)
for a, c in [(8.7, 10.3), (27.2, 30.4), (41.4, 41.9), (49.96, 50.2)]:
    t, te = ot(a), ot(c)
    while t < te: put(random.choice(["tick", "click_b"]), t, -30 + 3 * random.random()); t += 0.13 + 0.07 * random.random()
for s_ in (10.3, 13.0, 31.5, 50.0): put("pop_a", ot(s_), -26)
put("impactsoft", 4.14, -20); put("pop_b", 4.16, -24); put("impactsoft", 10.94, -20); put("pop_b", 10.96, -24); put("subhit", 4.14, -26); put("subhit", 10.94, -26); put("select", ot(41.8), -25); put("ding", ot(33.5), -24); put("pop_b", ot(44.0), -26); put("impactsoft", ot(54.95), -22); put("pop_a", b.end_card_start(), -27)
nar *= 10 ** (-3 / 20) / np.abs(nar).max(); vb = band(nar)
sf.write(f"{H}/out/nar17.wav", nar, SR, subtype='PCM_16'); sf.write(f"{H}/out/sfx17.wav", lay[:N], SR, subtype='PCM_16')
# bed: exact length, highpass 140, fade-out, tender dip under line 4 (the begging line), level about 11 dB under the voice before ducking
bed = load(bedp); bed = np.pad(bed, (0, max(0, N - len(bed))))[:N]; t_ = np.arange(N) / SR
def ss(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
l4 = cues[3]; dip = 1 - (1 - 10 ** (-4 / 20)) * ss((t_ - (l4["start"] - 0.1)) / 0.3) * (1 - ss((t_ - (l4["end"] + 0.1)) / 0.4))
bed *= dip * (1 - ss((t_ - (D - 0.8)) / 0.8))
sf.write(f"{H}/out/bedraw17-{tag}.wav", bed, SR, subtype='PCM_16')
raw = f"{H}/out/bedshaped17-{tag}.wav"
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f"{H}/out/bedraw17-{tag}.wav", '-af', 'highpass=f=140', '-ar', '48000', raw], check=True)
g = vb - 11 - band(load(raw))
fc = ("[0:a]asplit=2[v1][key];[1:a]volume=%.2fdB[b];[b][key]sidechaincompress=threshold=0.05:ratio=4:attack=12:release=420[duck];[duck]asplit=2[d1][d2];"
      "[v1][d1][2:a]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[o]") % g
wav = f"{H}/out/mix17-{tag}.wav"; duck = f"{H}/out/duck17-{tag}.wav"
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f"{H}/out/nar17.wav", '-i', raw, '-i', f"{H}/out/sfx17.wav", '-filter_complex', fc, '-map', '[o]', '-ar', '48000', wav, '-map', '[d2]', duck], check=True)
json.dump(dict(gain_db=g, lin=10 ** (g / 20)), open(f"{H}/out/gain17-{tag}.json", "w"))
m = subprocess.run(['ffmpeg', '-i', wav, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1]); fix = -14.0 - I
tmp = wav[:-4] + '-pre.wav'; os.replace(wav, tmp)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-af', f'volume={fix}dB,alimiter=limit=0.85:attack=3:release=80:level=false', '-ar', '48000', wav], check=True)
os.remove(tmp)
print('bed ducked vs voice (300-3500 Hz): %.1f dB; pre-loudnorm fix %.2f dB; bed gain %.1f dB; lin(with fix) %.3f' % (band(load(duck)) - vb, fix, g, 10 ** (g / 20) * 10 ** (fix / 20)))
