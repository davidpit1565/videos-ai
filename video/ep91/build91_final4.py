#!/usr/bin/env python3
"""ep91 final4 (narration + bed): the 9:16 'Me with Claude / Me with ChatGPT' reel retimed to voice/cues91b.json (4 lines), Meta AI fixes kept
(one CTA only, BIG board scrolled to Step 8, static last second). Headline words follow the voice ("It listens." / "It's way more tangled." / "Which one are you?").
usage: build91_final4.py <out_video.mp4> | --still t out.png | --timeline"""
import sys, os, json, subprocess, numpy as np
from PIL import Image
import build91_final2 as b2
from build91_final2 import kf, win, ss, draw_line, TOP, BOT, X0, WW, Y0, W, H, FPS, BASE, ORG, TEAL, WHT
HERE = os.path.dirname(os.path.abspath(__file__))
CP = HERE + "/voice/cues91b.json"
L = json.load(open(CP if os.path.exists(CP) else HERE + "/cues91.json"))["lines"]
Wd = lambda n, i: L[n - 1]["words"][i][0]; We = lambda n, i: L[n - 1]["words"][i][1]
D = round(L[3]["end"] + 1.1, 2)
t1 = Wd(1, 3); s2 = L[1]["start"]; s3 = L[2]["start"]; s4 = L[3]["start"]
tA = max(0.9, t1 - 0.5); tB0 = s2 - 0.15; tC0 = s3 - 0.1; tD0 = s4 - 0.2
punch = We(2, 2) + 0.05; scroll1 = punch + 0.35; scroll2 = tC0 - 0.65          # board punch after "ChatGPT", scroll to Step 8, hold ~0.5 s before the layout changes
tS = s4 + 0.35                                                                    # static camera for the last part
LAY = kf([(0, 755, 6, 170), (tA, 755, 6, 170), (tA + 0.6, 560, 110, 290), (tB0, 560, 110, 290), (tB0 + 0.7, 200, 112, 648), (tC0, 200, 112, 648),
          (tC0 + 0.55, 410, 120, 410), (tD0, 410, 120, 410), (tD0 + 0.5, 330, 170, 440), (D, 330, 170, 440)])
V1 = kf([(0, 719, 571, 1.0), (tA, 719, 571, 1.06), (tA + 0.6, 760, 560, 1.3), (tB0, 800, 470, 1.45), (tB0 + 0.7, 820, 420, 1.5), (tC0, 840, 400, 1.55),
         (tC0 + 0.55, 719, 580, 1.0), (tS, 740, 580, 1.06), (D, 740, 580, 1.06)])
V2 = kf([(0, 719, 1283, 1.0), (tA, 719, 1300, 1.04), (tA + 0.6, 719, 1374, 1.0), (tB0, 719, 1400, 1.02), (tB0 + 0.7, 700, 1620, 1.25), (punch - 0.05, 700, 1600, 1.4),
         (scroll1, 1161, 1560, 2.6), (scroll2, 1161, 2150, 2.6), (tC0, 1161, 2150, 2.6), (tC0 + 0.55, 640, 1900, 1.0), (tS, 660, 1900, 1.06), (D, 660, 1900, 1.06)])
DIM = kf([(0, 1.0), (tB0, 1.0), (tB0 + 0.7, 0.5), (tC0, 0.5), (tC0 + 0.55, 1.0), (D, 1.0)])
def frame(k):
    t = k / FPS; a, g, b = LAY(t)
    canvas = np.ones((H, W, 3), np.float32) * np.array(BASE, np.float32)
    ta = int(round(a)); tb = int(round(b)); gy = Y0 + ta; by = Y0 + ta + int(round(g))
    canvas[Y0:Y0 + ta, X0:X0 + WW] = np.asarray(win(Y0, ta, V1(t), TOP), np.float32) * DIM(t)
    canvas[by:by + tb, X0:X0 + WW] = np.asarray(win(by, tb, V2(t), BOT), np.float32)
    cy = gy + g / 2; fo = 1.0 - ss((t - (D - 0.4)) / 0.4)
    def seg(t0, t1_, fade=0.15): return ss((t - t0) / 0.05) * (1 - ss((t - (t1_ - fade)) / fade))
    e1 = seg(t1 - 0.1, tB0 + 0.2); e2 = seg(Wd(2, 3) - 0.1, tC0 + 0.4); e3 = seg(s3 - 0.05, tD0 + 0.1)
    if e1 > 0.01: draw_line(canvas, [("It", WHT, Wd(1, 3) - .03), ("listens.", ORG, Wd(1, 4) - .03)], t, cy, 70, e1 * fo)
    if e2 > 0.01: draw_line(canvas, [("It's", WHT, Wd(2, 3) - .03), ("way", WHT, Wd(2, 4) - .03), ("more", WHT, Wd(2, 5) - .03), ("tangled.", TEAL, Wd(2, 6) - .03)], t, cy, 70, e2 * fo)
    if e3 > 0.01: draw_line(canvas, [("Which", WHT, Wd(3, 0) - .03), ("one", WHT, Wd(3, 1) - .03), ("are", WHT, Wd(3, 2) - .03), ("you?", WHT, Wd(3, 3) - .03)], t, cy, 70, e3 * fo)
    if t >= s4 - 0.05:
        es = ss((t - s4) / 0.4) * fo
        draw_line(canvas, [(w, WHT, s4) for w in b2.SEND1.split()], t, cy - 38, 56, es)
        draw_line(canvas, [(w, ORG if w.startswith("overcomplicates") else WHT, Wd(4, 6) - 0.1) for w in b2.SEND2.split()], t, cy + 38, 56, es)
    return np.clip(canvas, 0, 255).astype(np.uint8)
if __name__ == "__main__":
    if "--timeline" in sys.argv:
        print(f"D={D} t1={t1:.2f} tA={tA:.2f} tB0={tB0:.2f} punch={punch:.2f} scroll {scroll1:.2f}-{scroll2:.2f} tC0={tC0:.2f} s3={s3:.2f} tD0={tD0:.2f} s4={s4:.2f} tS={tS:.2f}"); sys.exit()
    if "--still" in sys.argv:
        i = sys.argv.index("--still"); Image.fromarray(frame(int(float(sys.argv[i + 1]) * FPS))).save(sys.argv[i + 2]); sys.exit()
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                            "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), sys.argv[1]], stdin=subprocess.PIPE)
    for k in range(int(round(D * FPS))): enc.stdin.write(frame(k).tobytes())
    enc.stdin.close(); enc.wait(); print("done", D)
