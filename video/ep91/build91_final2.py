#!/usr/bin/env python3
"""ep91 final2 (NEW 9:16 art): two stacked windows onto David's Gemini 9:16 artwork, camera moves with smooth (PCHIP) keyframes,
headline words in the gap, final send line. Voice = existing out/narration91.wav (no TTS). Usage: build91_final2.py <out_video.mp4> [--still t out.png] [--cover]"""
import sys, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.interpolate import PchipInterpolator as P
H0 = "/home/user/videos-ai/video/ep91"
ART = "/home/user/videos-ai/channel/memes-2026-11-10/david-chatgpt/meme3-9x16-gemini.jpg"
W, H, FPS = 1080, 1920, 30
BASE = (11, 15, 26); X0, WW = 65, 950; Y0 = 285
S0 = WW / 1438.0
TOP = (0, 1143); BOT = (1155, 2576)
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
cues = json.load(open(H0 + "/cues91.json")); L = cues["lines"]
Wd = lambda n, i: L[n - 1]["words"][i][0]
D = 11.9
# send line (after "Tag someone who needs the Claude one.")
SEND1, SEND2 = "Send this to the friend who", "overcomplicates everything."
T_SEND = 9.78
art = Image.open(ART).convert("RGB")
def kf(rows):   # rows: list of (t, v...) -> function t -> tuple, PCHIP (smooth, no stops)
    ts = np.array([r[0] for r in rows], float); vs = np.array([r[1:] for r in rows], float)
    f = [P(ts, vs[:, i]) for i in range(vs.shape[1])]
    return lambda t: tuple(float(g(min(max(t, ts[0]), ts[-1]))) for g in f)
# layout (top h, gap, bottom h)
LAY = kf([(0, 755, 6, 170), (0.9, 755, 6, 170), (1.5, 560, 110, 290), (2.2, 560, 110, 290), (2.9, 200, 112, 648), (5.45, 200, 112, 648),
          (6.1, 410, 120, 410), (6.9, 410, 120, 410), (7.6, 330, 170, 440), (D, 330, 170, 440)])
# camera: (t, cx, cy, z)
V1 = kf([(0, 719, 571, 1.0), (0.9, 719, 571, 1.06), (1.5, 760, 560, 1.3), (2.3, 800, 470, 1.45), (2.9, 820, 420, 1.5), (5.45, 840, 400, 1.55),
         (6.1, 719, 580, 1.0), (6.9, 740, 580, 1.06), (7.6, 760, 440, 1.2), (D, 800, 430, 1.32)])
V2 = kf([(0, 719, 1283, 1.0), (0.9, 719, 1300, 1.04), (1.5, 719, 1374, 1.0), (2.3, 719, 1400, 1.02), (2.9, 760, 1740, 1.1), (3.75, 800, 1740, 1.2),
         (4.0, 1040, 1650, 1.8), (4.9, 1040, 1850, 1.8), (5.45, 1040, 2100, 1.8), (6.1, 640, 1900, 1.0), (6.9, 660, 1900, 1.06), (7.6, 700, 1900, 1.14), (D, 740, 1880, 1.26)])
DIM = kf([(0, 1.0), (2.2, 1.0), (2.9, 0.5), (5.45, 0.5), (6.1, 1.0), (D, 1.0)])
def win(rect_y, h, cam, panel):
    cx, cy, z = cam; s = S0 * z; rw, rh = WW / s, h / s
    cx = min(max(cx, rw / 2), 1438 - rw / 2); lo, hi = panel
    cy = min(max(cy, lo + rh / 2), hi - rh / 2) if rh < hi - lo else (lo + hi) / 2
    aff = (1 / s, 0, cx - rw / 2, 0, 1 / s, cy - rh / 2)
    return art.transform((WW, int(round(h))), Image.AFFINE, aff, resample=Image.BICUBIC)
def ss(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
def tw(txt, f, sz, tr=0.03): return sum(f.getlength(c) for c in txt) - tr * sz * (len(txt) - 1)
def draw_words(img, items, cy, size, alpha_all=1.0):
    """items: list of (text, color, t_in) in one centred line; per-word soft fade + rise"""
    f = ImageFont.truetype(FONT, size); gap = f.getlength(" ") - 0.03 * size
    total = sum(tw(w, f, size) for w, _, _ in items) + gap * (len(items) - 1)
    return total, f, gap
def draw_line(canvas, items, t, cy, size, fade_out=1.0):
    f = ImageFont.truetype(FONT, size); sp = f.getlength(" ") - 0.03 * size
    total = sum(tw(w, f, size) for w, _, _ in items) + sp * (len(items) - 1); x = (W - total) / 2
    for w, col, tin in items:
        a = ss((t - tin) / 0.28) * fade_out; wd = tw(w, f, size)
        if a > 0.003:
            lay = Image.new("L", (W, size * 2), 0); d = ImageDraw.Draw(lay); xx = x
            for c in w: d.text((xx, 0), c, font=f, fill=255); xx += f.getlength(c) - 0.03 * size
            al = np.asarray(lay, np.float32) / 255 * a; y0 = int(cy - size * 0.62 + (1 - ss((t - tin) / 0.28)) * 16)
            y0 = max(0, min(H - size * 2, y0)); reg = canvas[y0:y0 + size * 2]
            reg[:] = reg * (1 - al[..., None]) + np.array(col, np.float32) * al[..., None]
        x += wd + sp
ORG, TEAL, WHT = (255, 138, 76), (61, 232, 200), (248, 248, 248)
def frame(k):
    t = k / FPS; a, g, b = LAY(t)
    canvas = np.ones((H, W, 3), np.float32) * np.array(BASE, np.float32)
    ta = int(round(a)); tb = int(round(b)); gy = Y0 + ta; by = Y0 + ta + int(round(g))
    wt = np.asarray(win(Y0, ta, V1(t), TOP), np.float32) * DIM(t)
    wb = np.asarray(win(by, tb, V2(t), BOT), np.float32)
    canvas[Y0:Y0 + ta, X0:X0 + WW] = wt; canvas[by:by + tb, X0:X0 + WW] = wb
    cy = gy + g / 2
    fo = 1.0 - ss((t - (D - 0.4)) / 0.4)
    def seg(t0, t1, fade=0.15): return ss((t - t0) / 0.05) * (1 - ss((t - (t1 - fade)) / fade))
    # headlines in the gap (strip), one at a time
    e1 = seg(Wd(1, 3) - 0.1, 2.3); e2 = seg(Wd(2, 3) - 0.1, 5.7); e3 = seg(Wd(3, 0) - 0.1, 7.0); e4 = seg(Wd(4, 0) - 0.1, T_SEND - 0.05)
    if e1 > 0.01: draw_line(canvas, [("It", WHT, Wd(1, 3) - .03), ("listens.", ORG, Wd(1, 4) - .03)], t, cy, 70, e1 * fo)
    if e2 > 0.01: draw_line(canvas, [("It's", WHT, Wd(2, 3) - .03), ("way", WHT, Wd(2, 4) - .03), ("more", WHT, Wd(2, 5) - .03), ("complex.", TEAL, Wd(2, 6) - .03)], t, cy, 70, e2 * fo)
    if e3 > 0.01: draw_line(canvas, [("Which", WHT, Wd(3, 0) - .03), ("one", WHT, Wd(3, 1) - .03), ("are", WHT, Wd(3, 2) - .03), ("you?", WHT, Wd(3, 3) - .03)], t, cy, 70, e3 * fo)
    if e4 > 0.01:
        draw_line(canvas, [("Tag", WHT, Wd(4, 0) - .03), ("someone", WHT, Wd(4, 1) - .03), ("who", WHT, Wd(4, 2) - .03)], t, cy - 38, 60, e4 * fo)
        draw_line(canvas, [("needs", WHT, Wd(4, 3) - .03), ("the", WHT, Wd(4, 4) - .03), ("Claude", ORG, Wd(4, 5) - .03), ("one.", ORG, Wd(4, 6) - .03)], t, cy + 38, 60, e4 * fo)
    if t >= T_SEND - 0.05:
        es = ss((t - T_SEND) / 0.4) * fo
        draw_line(canvas, [(w, WHT, T_SEND) for w in SEND1.split()], t, cy - 38, 56, es)
        draw_line(canvas, [(w, ORG if w.startswith("overcomplicates") else WHT, T_SEND + 0.12) for w in SEND2.split()], t, cy + 38, 56, es)
    canvas *= (0.0 + 1.0 * (1 - (1 - fo) * 0.0))
    return np.clip(canvas, 0, 255).astype(np.uint8)
def cover(path):
    c = np.ones((H, W, 3), np.float32) * np.array(BASE, np.float32); s = W / 1438.0
    pb = art.crop((0, BOT[0], 1438, BOT[1])).resize((W, int(round((BOT[1] - BOT[0]) * s))), Image.LANCZOS)
    y = (H - pb.size[1]) // 2; c[y:y + pb.size[1]] = np.asarray(pb, np.float32)
    Image.fromarray(np.clip(c, 0, 255).astype(np.uint8)).save(path); print("cover panel y", y, y + pb.size[1])
if __name__ == "__main__":
    if "--cover" in sys.argv: cover(sys.argv[sys.argv.index("--cover") + 1]); sys.exit()
    if "--still" in sys.argv:
        i = sys.argv.index("--still"); Image.fromarray(frame(int(float(sys.argv[i + 1]) * FPS))).save(sys.argv[i + 2]); sys.exit()
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                            "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), sys.argv[1]], stdin=subprocess.PIPE)
    for k in range(int(round(D * FPS))): enc.stdin.write(frame(k).tobytes())
    enc.stdin.close(); enc.wait(); print("done", D)
