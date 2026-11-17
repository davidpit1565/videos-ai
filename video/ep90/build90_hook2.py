#!/usr/bin/env python3
"""ep90 final7 hook scene (1.1 s): the phone picture (real ChatGPT mark painted in, see build90_hook.py), darkened,
quick push-in, BIG heavy text fully visible from frame 0, soft fade-out, black at the end.  No voice.
Usage: build90_hook2.py <out.mp4> [--still out.png]"""
import sys, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
import build90_hook as bh
from build90_hook import ss, crush, W, H, FPS
# ======= SWAP THE HOOK WORDING HERE (two variables) =======
HOOK_LINE1 = "ChatGPT"
HOOK_LINE2 = "47-day timeout."
# ==========================================================
DUR = 1.1
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
TRACK = 0.03          # tight tracking (em)
def line_width(t, f, size): return sum(f.getlength(c) for c in t) - TRACK * size * (len(t) - 1)
def draw_tight(d, text, f, size, x, y, fill):
    for c in text:
        d.text((x, y), c, font=f, fill=fill); x += f.getlength(c) - TRACK * size
def text_alpha_layer(alpha):
    lines = [HOOK_LINE1, HOOK_LINE2]
    size = int(950 / max(line_width(l, ImageFont.truetype(FONT, 100), 100) / 100 for l in lines))   # widest line = 950 px
    f = ImageFont.truetype(FONT, size); lay = Image.new("L", (W, H), 0); d = ImageDraw.Draw(lay)
    y = 300
    for l in lines:
        wd = line_width(l, f, size); draw_tight(d, l, f, size, (W - wd) / 2, y, 255); y += int(size * 1.02)
    return np.asarray(lay, np.float32) / 255 * alpha, size
def grad():
    y = np.arange(H)[:, None].astype(np.float32)
    return 1 - 0.6 * (1 - np.clip((y - 250) / 520, 0, 1)) ** 1.0 * np.ones((1, W), np.float32)   # darker behind the text (top), fades by ~y 770
GR = None
def frame(plate, gm, k, rng):
    global GR
    t = k / FPS
    z = 1.0 + 0.15 * ss(t / DUR); ax, ay = 0.40 * W, 0.50 * H
    img = np.asarray(Image.fromarray(np.clip(plate, 0, 255).astype(np.uint8)).transform((W, H), Image.AFFINE, (1 / z, 0, ax - ax / z, 0, 1 / z, ay - ay / z), resample=Image.BICUBIC)).astype(np.float32)
    gz = np.asarray(Image.fromarray((gm * 255).astype(np.uint8)).transform((W, H), Image.AFFINE, (1 / z, 0, ax - ax / z, 0, 1 / z, ay - ay / z), resample=Image.BICUBIC)).astype(np.float32) / 255
    pulse = 0.5 * (1 + np.sin(2 * np.pi * 0.8 * t - 1.2))
    img += gz[..., None] * np.array([60, 40, 190], np.float32) * (0.10 + 0.14 * pulse)
    img *= 0.82                                                   # slightly darker so the text pops
    if GR is None: GR = grad()
    img *= GR[..., None]
    img += rng.normal(0, 3.0, (H, W, 1)).astype(np.float32)
    img = crush(img)
    img *= 1.0 - ss((t - 0.7) / 0.35)                              # fade to true black by 1.05 s
    ta = 1.0 - ss((t - 0.72) / 0.28)                               # text fully visible from frame 0, soft fade out
    tl, _ = text_alpha_layer(ta)
    img = img * (1 - tl[..., None]) + np.array([248, 248, 248], np.float32) * tl[..., None]
    return np.clip(img, 0, 255).astype(np.uint8)
def main():
    plate, gm = bh.build_plate()
    if "--still" in sys.argv:
        rng = np.random.default_rng(5); Image.fromarray(frame(plate, gm, 0, rng)).save(sys.argv[sys.argv.index("--still") + 1]); return
    rng = np.random.default_rng(5)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), sys.argv[1]], stdin=subprocess.PIPE)
    for k in range(int(round(DUR * FPS))): enc.stdin.write(frame(plate, gm, k, rng).tobytes())
    enc.stdin.close(); enc.wait()
if __name__ == "__main__": main()
