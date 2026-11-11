#!/usr/bin/env python3
"""mixbed90g.py <bed.wav (exact length)> <out.wav> : final8 sfx track (decoded from ep90-final8.mp4) + music bed shaped to the timeline.
Bed: light under the hook, -4 dB under typing bursts so the ticks stay audible, -7 dB under the begging reply, 0.5 s near silence
before the punchline then back, fade at the end. sfx boosted so the bed does not bury them; whole mix limited to about -1.5 dBFS."""
import sys, subprocess, re, numpy as np
import build90f as b
SR = 48000; OFF = 1.2
def dec(path, extra=()):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", path, *extra, "-ar", str(SR), "-ac", "1", "-f", "f32le", "-"], capture_output=True).stdout, np.float32).astype(np.float64)
S = dec("out/ep90-final8.mp4"); n = len(S)
bed = dec(sys.argv[1]); bed = np.pad(bed, (0, max(0, n - len(bed))))[:n]
t = np.arange(n) / SR; ot = lambda s: OFF + b.ot(s)
def ss(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
def lin(db): return 10 ** (db / 20)
env = np.ones(n)
env *= 1 - (1 - lin(-5)) * (1 - ss((t - 0.9) / 0.4)) * (t < 1.4)          # a little lighter under the hook, full from the recording
for a, c in [(1.3, 9.5), (18.0, 30.4), (40.4, 41.5), (48.3, 49.6)]:           # typing bursts
    a, c = ot(a), ot(c); env *= 1 - (1 - lin(-4)) * ss((t - a) / 0.2) * (1 - ss((t - c) / 0.25))
d0, d1 = ot(33.2), ot(36.2); env *= 1 - (1 - lin(-7)) * ss((t - d0) / 0.3) * (1 - ss((t - d1) / 0.3))   # begging reply
s0, s1 = ot(54.45), ot(54.95); env *= 1 - 0.96 * ss((t - s0) / 0.1) * (1 - ss((t - s1) / 0.5))           # near silence, groove returns
D = n / SR; env *= 1 - ss((t - (D - 0.9)) / 0.9)
bed *= env
sr = np.sqrt(np.mean(bed[(t > 1.3) & (t < D - 1)] ** 2)) + 1e-9
bed *= lin(-21) / sr                                                       # bed about -21 dBFS RMS
S *= lin(-3) / (np.abs(S).max() + 1e-9)                                    # sfx peak -3 dBFS before limiting
out = S + bed
out = out.astype(np.float32)
raw = sys.argv[2] + ".raw.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", raw], input=out.tobytes())
m = subprocess.run(["ffmpeg", "-i", raw, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", m)[-1]); g = min(-14.0 - I, 9.0)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"volume={g}dB,alimiter=limit=0.66:attack=3:release=80:level=false", "-ar", str(SR), "-ac", "1", sys.argv[2]])
import os; os.remove(raw); print("raw LUFS %.1f gain %.1f" % (I, g))
