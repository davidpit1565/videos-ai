#!/usr/bin/env python3
"""Fail if any spoken line's window in the FINAL mp4 is silent (RMS below -35 dB), so a digital-silence line can never pass again
(ep105 v2 shipped line 11 as zeros and nothing noticed). usage: check_last_line_audio.py <reel.mp4> <cues.json> [--all]
Checks the last line by default, every line with --all. Cues: {"lines":[{n,start,end}]} or a list of the same."""
import json, subprocess, sys
import numpy as np
mp4, cues = sys.argv[1], sys.argv[2]
d = json.load(open(cues)); L = d["lines"] if isinstance(d, dict) else d
L = L if "--all" in sys.argv else L[-1:]
y = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-ac", "1", "-ar", "48000", "-f", "f32le", "-"], capture_output=True).stdout, dtype=np.float32)
bad = 0
for l in L:
    seg = y[int(l["start"] * 48000):int(l["end"] * 48000)]
    r = 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9) if len(seg) else -999
    ok = r >= -35; bad += not ok
    print(f"  {'ok  ' if ok else 'FAIL'} line {l.get('n')}: RMS {r:.1f} dB in {l['start']:.2f}-{l['end']:.2f} s of the final mp4 (floor -35 dB)")
sys.exit(1 if bad else 0)
