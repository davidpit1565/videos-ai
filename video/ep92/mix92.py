#!/usr/bin/env python3
"""mix92.py <music_picked.wav> <out.wav> [--eq]  : bed shaped to the ep92 timeline + quiet sfx (video/ep90/sfx), loudnorm -14 LUFS."""
import sys, subprocess, numpy as np, random
import build92b as b
SFX = "/home/user/videos-ai/video/ep90/sfx/"
SR = 48000
def load(path, eq=False):
    af = "highpass=f=140,equalizer=f=1800:t=q:w=0.8:g=3" if eq else "anull"
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-af", af, "-ar", str(SR), "-ac", "1", "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(p.stdout, np.float32).copy()
def sfx(name):
    return load(SFX + name + ".ogg")
music = load(sys.argv[1], "--eq" in sys.argv)
D = b.D; n = int(D * SR)
music = np.pad(music, (0, max(0, n - len(music))))[:n]
t = np.arange(n) / SR
ot = b.ot
def ramp(t, a0, a1, g0, g1):
    f = np.clip((t - a0) / (a1 - a0), 0, 1); f = f * f * (3 - 2 * f); return g0 + (g1 - g0) * f
def ss(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
d0, d1 = ot(33.2), ot(35.8)
duck = 1 - (1 - 10 ** (-7 / 20)) * ss((t - d0) / 0.35) * (1 - ss((t - d1) / 0.3))
s0, s1 = ot(54.25), ot(54.95)
gap = 1 - 0.96 * ss((t - s0) / 0.12) * (1 - ss((t - s1) / 0.45))
env = duck * gap * (1.0 - ss((t - (D - b.FINAL_FADE)) / b.FINAL_FADE))
bed = music * env
rms = float(np.sqrt(np.mean(music ** 2)) + 1e-9)
out = bed.copy()
def put(name, tt, db):
    s = sfx(name); s = s / (np.abs(s).max() + 1e-9)
    i = int(tt * SR)
    if i + len(s) > n: s = s[:n - i]
    out[i:i + len(s)] += s * rms * 10 ** (db / 20)
random.seed(7)
# typing ticks: bursts (not per character), irregular spacing
for a, c in [(1.4, 9.7), (17.9, 30.4), (40.4, 41.6), (48.3, 49.7)]:
    tt = ot(a); te = ot(c)
    while tt < te:
        put(random.choice(["tick", "click_b"]), tt, -17)
        tt += 0.11 + 0.07 * random.random()
for s_ in (10.3, 13.0, 31.5, 50.0): put("pop_a", ot(s_), -13)
put("select", ot(41.7), -11)
put("ding", ot(33.5), -9)
put("pop_b", ot(44.0), -11)
put("impactsoft", ot(54.95), -6)
pk = np.abs(out).max(); 
if pk > 0.95: out *= 0.95 / pk
raw = sys.argv[2] + ".raw.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", raw], input=out.astype(np.float32).tobytes())
m = subprocess.run(["ffmpeg", "-i", raw, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
import re
I = float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", m)[-1])
g = -14.0 - I
pk = float(np.abs(out).max()) * 10 ** (g / 20)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"volume={g}dB,alimiter=limit=0.84:attack=2:release=60:level=false", "-ar", str(SR), "-ac", "1", sys.argv[2]])
import os; os.remove(raw)
print("ok", D)
