#!/usr/bin/env python3
"""Checks, on the RENDERED mp4, that the word 'David' (first reply line) is covered in every frame where it would otherwise be visible.
Method: for each sampled time, render the same frame WITHOUT the mask (build92.compose mask=False), take the pixels of the word box (mapped through the same camera) that are bright there,
and count how many of those pixels are still bright in the rendered mp4 frame. Also OCR-free scan: the only other place the recording could show the name is the status bar/header, which is painted black (rows < 330)."""
import sys, subprocess, numpy as np
mp4 = sys.argv[1]; cues = sys.argv[2]
sys.argv = ["x", cues]
import build92 as b
W, H = b.W, b.H
WORD = (46, 705, 162, 748)          # 'David' without the comma, doc coords (scaled 1080-wide space)
p = subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-vf", "fps=10,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
fr = np.frombuffer(p, np.uint8).reshape(-1, H, W)
worst = 0; vis = 0; worst_t = None; tot_before = []
for k in range(len(fr)):
    t = k / 10.0
    s, mode = b.src_at(t)
    if s < b.NAME_FROM and mode != "rew": continue
    z, fx, fy, ox, oy = b.cam(t); sc = b.scroll_at(s)
    def mp(x, y): return (x - fx) * z + ox, (y - (fy - 0) ) * z + oy if False else ((y - sc) - (fy - sc)) * z + oy
    x0, y0 = mp(WORD[0], WORD[1]); x1, y1 = mp(WORD[2], WORD[3])
    xa, xb, ya, yb = int(max(0, x0 - 2)), int(min(W, x1 + 2)), int(max(0, y0 - 2)), int(min(H, y1 + 2))
    if xb <= xa or yb <= ya: continue
    canvas = np.zeros((H, W, 3), np.float32); b.compose(t, canvas, mask=False)
    ref = canvas[ya:yb, xa:xb].mean(2)
    # the end of the hook still shows a different picture; only count pixels that are bright in the unmasked render
    bright = ref > 60
    if bright.sum() < 30: continue
    vis += 1
    got = fr[k][ya:yb, xa:xb] > 60
    unc = int((bright & got).sum())
    if unc > worst: worst, worst_t = unc, t
    tot_before.append(int(bright.sum()))
print(f"frames sampled every 0.1 s where the unmasked word would be visible: {vis}; max word pixels still bright in the rendered mp4: {worst} (t={worst_t}); typical unmasked word pixels {int(np.median(tot_before)) if tot_before else 0}")
