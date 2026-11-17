#!/usr/bin/env python3
"""ep91 final3 (NO voice, ~10 s): one CTA only; the ChatGPT board is shown BIG (zoom 2.6) and scrolled to Step 8; the last second is static with the send line.
Usage: build91_final3.py <out_video.mp4> | --still t out.png"""
import sys, subprocess, numpy as np
from PIL import Image
import build91_final2 as b2
from build91_final2 import kf, win, ss, draw_line, TOP, BOT, X0, WW, Y0, W, H, FPS, BASE, ORG, TEAL, WHT
D = 10.1; T_SEND = 8.25
LAY = kf([(0, 755, 6, 170), (0.9, 755, 6, 170), (1.5, 560, 110, 290), (2.3, 560, 110, 290), (3.0, 200, 112, 648), (6.9, 200, 112, 648),
          (7.4, 410, 120, 410), (8.3, 330, 170, 440), (D, 330, 170, 440)])
V1 = kf([(0, 719, 571, 1.0), (0.9, 719, 571, 1.06), (1.5, 760, 560, 1.3), (2.3, 800, 470, 1.45), (3.0, 820, 420, 1.5), (6.9, 840, 400, 1.55),
         (7.4, 719, 580, 1.0), (8.4, 740, 580, 1.06), (D, 740, 580, 1.06)])
V2 = kf([(0, 719, 1283, 1.0), (0.9, 719, 1300, 1.04), (1.5, 719, 1374, 1.0), (2.3, 719, 1400, 1.02), (3.0, 700, 1620, 1.25), (4.0, 700, 1600, 1.4),
         (4.5, 1161, 1560, 2.6), (6.4, 1161, 2150, 2.6), (6.9, 1161, 2150, 2.6), (7.4, 640, 1900, 1.0), (8.4, 660, 1900, 1.06), (D, 660, 1900, 1.06)])
DIM = kf([(0, 1.0), (2.3, 1.0), (3.0, 0.5), (6.9, 0.5), (7.4, 1.0), (D, 1.0)])
def frame(k):
    t = k / FPS; a, g, b = LAY(t)
    canvas = np.ones((H, W, 3), np.float32) * np.array(BASE, np.float32)
    ta = int(round(a)); tb = int(round(b)); gy = Y0 + ta; by = Y0 + ta + int(round(g))
    canvas[Y0:Y0 + ta, X0:X0 + WW] = np.asarray(win(Y0, ta, V1(t), TOP), np.float32) * DIM(t)
    canvas[by:by + tb, X0:X0 + WW] = np.asarray(win(by, tb, V2(t), BOT), np.float32)
    cy = gy + g / 2; fo = 1.0 - ss((t - (D - 0.4)) / 0.4)
    def seg(t0, t1, fade=0.15): return ss((t - t0) / 0.05) * (1 - ss((t - (t1 - fade)) / fade))
    e1 = seg(1.15, 2.3); e2 = seg(3.25, 6.9); e3 = seg(7.4, 8.2)
    if e1 > 0.01: draw_line(canvas, [("It", WHT, 1.15), ("listens.", ORG, 1.32)], t, cy, 70, e1 * fo)
    if e2 > 0.01: draw_line(canvas, [("It's", WHT, 3.25), ("way", WHT, 3.45), ("more", WHT, 3.65), ("complex.", TEAL, 3.9)], t, cy, 70, e2 * fo)
    if e3 > 0.01: draw_line(canvas, [("Which", WHT, 7.4), ("one", WHT, 7.52), ("are", WHT, 7.64), ("you?", WHT, 7.76)], t, cy, 70, e3 * fo)
    if t >= T_SEND - 0.05:
        es = ss((t - T_SEND) / 0.4) * fo
        draw_line(canvas, [(w, WHT, T_SEND) for w in b2.SEND1.split()], t, cy - 38, 56, es)
        draw_line(canvas, [(w, ORG if w.startswith("overcomplicates") else WHT, T_SEND + 0.1) for w in b2.SEND2.split()], t, cy + 38, 56, es)
    return np.clip(canvas, 0, 255).astype(np.uint8)
if __name__ == "__main__":
    if "--still" in sys.argv:
        i = sys.argv.index("--still"); Image.fromarray(frame(int(float(sys.argv[i + 1]) * FPS))).save(sys.argv[i + 2]); sys.exit()
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                            "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), sys.argv[1]], stdin=subprocess.PIPE)
    for k in range(int(round(D * FPS))): enc.stdin.write(frame(k).tobytes())
    enc.stdin.close(); enc.wait(); print("done", D)
