#!/usr/bin/env python3
"""mix90c.py <out.wav> : sound design only (no music bed) for ep90 final3, from video/ep93/sfx. Light: peak -6 dBFS."""
import sys, subprocess, random, numpy as np
import build90e as b
SFX = "/home/user/videos-ai/video/ep93/sfx/"; SR = 48000
def sfx(name):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", SFX + name + ".ogg", "-ar", str(SR), "-ac", "1", "-f", "f32le", "-"], capture_output=True)
    s = np.frombuffer(p.stdout, np.float32).astype(np.float64); return s / (np.abs(s).max() + 1e-9)
n = int(b.D * SR); out = np.zeros(n); ot = b.ot
def put(name, tt, db):
    s = sfx(name); i = int(tt * SR); s = s[:max(0, n - i)]
    out[i:i + len(s)] += s * 10 ** (db / 20)
random.seed(7)
for a, c in [(1.4, 9.7), (17.9, 30.4), (40.4, 41.6), (48.3, 49.7)]:   # typing bursts (source seconds)
    tt = ot(a); te = ot(c)
    while tt < te:
        put(random.choice(["tick", "click_b"]), tt, -19 + 3 * random.random()); tt += 0.11 + 0.07 * random.random()
for s_ in (10.3, 13.0, 31.5, 50.0): put("pop_a", ot(s_), -13)
put("select", ot(41.7), -12); put("ding", ot(33.5), -11); put("pop_b", ot(44.0), -12)
put("impactsoft", ot(54.95), -8)          # silence in the file from the previous cue until here (reading the loading dots)
pk = np.abs(out).max(); out *= 10 ** (-3 / 20) / pk
raw = sys.argv[1] + ".raw.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", raw], input=out.astype(np.float32).tobytes())
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", "afade=t=out:st=%.2f:d=%.2f" % (b.D - 0.5, 0.5), "-ar", str(SR), "-ac", "1", sys.argv[1]])
import os; os.remove(raw)
