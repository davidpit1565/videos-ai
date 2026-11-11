#!/usr/bin/env python3
"""ep92 audio. Usage: mix92.py <cues.json> <voice|novoice|bed> <out.wav> [bed.wav]
voice  = narration92.wav + quiet sfx, -14 LUFS (no bed)       novoice = sfx only (about -17 LUFS, peak < -1.5 dBFS)
bed    = narration + real-library bed (exact length, from audio/pick_real_track.py) ducked under speech (about -15 dB vs voice in 300-3500 Hz),
         slightly lower under line 2 (tender), lifted under line 4 (groove), fade-out; quiet sfx; -14 LUFS, true peak < -1 dBTP."""
import sys, subprocess, re, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
cues, mode, outp = sys.argv[1], sys.argv[2], sys.argv[3]; bedp = sys.argv[4] if len(sys.argv) > 4 else None
sys.argv = [sys.argv[0], cues]
import build92 as b
H = "/home/user/videos-ai/video/ep92"; SFXD = "/home/user/videos-ai/video/ep93/sfx/"; SR = 48000; D = b.D; N = int(D * SR)
def load(p): return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, dtype=np.float32).astype(np.float64)
def t_of_src(s):
    ts = np.linspace(b.P0, b.tI, 4000); ss = np.array([float(b._SRCMAP(t)) for t in ts]); return float(ts[np.argmin(np.abs(ss - s))])
def sst(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
lay = np.zeros(N + SR)
def put(name, t, db):
    x = load(SFXD + name + ".ogg"); x = x / (np.abs(x).max() + 1e-9) * 10 ** (db / 20); i0 = int(t * SR); n = min(len(x), len(lay) - i0)
    if n > 0 and t < D - 0.1: lay[i0:i0 + n] += x[:n]
up = 9 if mode == "novoice" else 0
put("impactsoft", 0.03, -24 + up); put("pop_a", t_of_src(2.0), -24 + up); put("pop_b", t_of_src(3.6), -27 + up)
put("ding", b.tH, -22 + up); put("impactsoft", b.END_T, -24 + up)
t = np.arange(N) / SR
nar = None
if mode != "novoice":
    nar = load(f"{H}/voice/narration92.wav"); nar = np.pad(nar, (0, max(0, N - len(nar))))[:N]; nar *= 10 ** (-3 / 20) / np.abs(nar).max()
mix = lay[:N].copy()
if nar is not None: mix = mix + nar
bedmix = None
if mode == "bed":
    bed = load(bedp); bed = np.pad(bed, (0, max(0, N - len(bed))))[:N]
    sos = butter(4, [300, 3500], btype="band", fs=SR, output="sos")
    # speech envelope (smoothed) -> duck
    sp = np.abs(nar); k = int(0.12 * SR); sp = np.convolve(sp, np.ones(k) / k, "same"); on = (sp > 0.02).astype(float)
    k2 = int(0.25 * SR); on = np.clip(np.convolve(on, np.ones(k2) / k2, "same") * 2.0, 0, 1)
    duck = 1.0 - (1.0 - 10 ** (-6 / 20)) * on                      # 6 dB extra duck while speaking; bed is louder in the gaps
    shape = np.ones(N)
    shape *= 1 - (1 - 10 ** (-2.0 / 20)) * sst((t - b.s2) / 0.6) * (1 - sst((t - b.e2) / 0.8))       # tender: a little lower under line 2
    shape *= 1 + (10 ** (2.5 / 20) - 1) * sst((t - b.tH + 0.3) / 0.5) * (1 - sst((t - b.e4 - 0.3) / 0.8))   # lift on 'And if I fail?'
    shape *= 1 - sst((t - (D - 1.8)) / 1.8)                           # fade-out
    bed_s = bed * duck * shape
    # level: ducked bed (while speaking) -15 dB under the voice in 300-3500 Hz
    voice_band = sosfilt(sos, nar); bed_band = sosfilt(sos, bed_s)
    m = on > 0.9
    vr = np.sqrt(np.mean(voice_band[m] ** 2)); br = np.sqrt(np.mean(bed_band[m] ** 2)) + 1e-9
    gain = vr / br * 10 ** (-15 / 20)
    bedmix = bed_s * gain; mix = mix + bedmix
    print("bed gain", round(20 * np.log10(gain), 2), "dB; voice band rms", round(20 * np.log10(vr), 1), "bed band rms while speaking", round(20 * np.log10(br * gain), 1))
sf.write(f"{H}/out/_pre.wav", mix, SR, subtype='PCM_16')
mm = subprocess.run(['ffmpeg', '-i', f"{H}/out/_pre.wav", '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', mm)[-1])
if mode == "novoice":
    peak = float(np.abs(mix).max()); gmax = -1.5 - 20 * np.log10(peak + 1e-9); g = min(-17.0 - I, gmax)
else: g = -14.0 - I
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f"{H}/out/_pre.wav", '-af', f'volume={g}dB,alimiter=limit=0.88:attack=3:release=80:level=false,afade=t=out:st={D - 0.35}:d=0.35', '-ar', '48000', outp], check=True)
if bedmix is not None:
    sf.write(outp.replace(".wav", "-bedonly.wav"), (bedmix * 10 ** (g / 20)).astype(np.float32), SR, subtype='PCM_16')
print("pre", I, "gain", round(g, 2), "D", D)
