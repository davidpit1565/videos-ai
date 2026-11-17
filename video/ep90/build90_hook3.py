#!/usr/bin/env python3
"""ep90 final8 hook scene (1.2 s), LIGHT style: off-white base (#ecebe5) with faint dotted grid + grain, big heavy black text
fully visible from frame 0, a rounded card with the BRIGHTENED phone picture (real ChatGPT mark as in final7). Last ~0.4 s:
text fades, the card expands to full bleed while the push-in carries into the phone's dark screen, then true black.
Usage: build90_hook3.py <out.mp4> [--still out.png] [--t seconds]"""
import sys, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy.ndimage import gaussian_filter
import build90_hook as bh
from build90_hook import ss, W, H, FPS
# ======= SWAP THE HOOK WORDING HERE (two variables) =======
HOOK_LINE1 = "ChatGPT"
HOOK_LINE2 = "47-day timeout."
# ==========================================================
DUR = 1.2
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
TRACK = 0.03; INK = (11, 11, 11); BASE = (236, 235, 229)
CARD0 = (65, 620, 1015, 1530); RAD0 = 46          # usable width, y 620-1530
ANCHOR = (520.0, 960.0)                            # plate point the push-in aims at (the phone screen)
def lw(t, f, s): return sum(f.getlength(c) for c in t) - TRACK * s * (len(t) - 1)
def text_layer(alpha):
    lines = [HOOK_LINE1, HOOK_LINE2]
    size = int(940 / max(lw(l, ImageFont.truetype(FONT, 100), 100) / 100 for l in lines))
    f = ImageFont.truetype(FONT, size); lay = Image.new("L", (W, H), 0); d = ImageDraw.Draw(lay); y = 282
    for l in lines:
        x = (W - lw(l, f, size)) / 2
        for c in l: d.text((x, y), c, font=f, fill=255); x += f.getlength(c) - TRACK * size
        y += int(size * 1.02)
    return np.asarray(lay, np.float32) / 255 * alpha
def make_base():
    b = np.ones((H, W, 3), np.float32) * np.array(BASE, np.float32)
    im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im)
    for yy in range(27, H, 54):
        for xx in range(27, W, 54): d.ellipse([xx - 1.7, yy - 1.7, xx + 1.7, yy + 1.7], fill=255)
    m = np.asarray(im.filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255 * 0.55
    return b * (1 - m[..., None]) + np.array((196, 195, 187), np.float32) * m[..., None]
def bright(plate):
    x = np.clip(plate, 0, 255) / 255.0
    y = np.clip((x ** 0.52) * 1.18, 0, 1)                      # lift shadows + exposure, keep hue
    y = y + np.array([0.0, 0.0, 0.035])[None, None, :] * (1 - y)  # tiny cool lift in the deep shadows
    return np.clip(y * 255, 0, 255)
def rrect(rect, rad, feather=1.0):
    x0, y0, x1, y1 = rect; im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(im).rounded_rectangle([x0, y0, x1, y1], radius=max(rad, 0.01), fill=255)
    return np.asarray(im.filter(ImageFilter.GaussianBlur(feather)), np.float32) / 255
PLATE = GM = BASE_IMG = None
def frame(k, rng, tt=None):
    global PLATE, GM, BASE_IMG
    t = k / FPS if tt is None else tt
    u = ss((t - 0.82) / 0.26)                                    # expansion phase 0.8 -> 1.2
    z = 1.0 + 0.12 * ss(min(t, 0.8) / 0.8) + 1.9 * u * u       # gentle push-in, then through into the screen
    x0, y0, x1, y1 = CARD0
    rect = (x0 * (1 - u), y0 * (1 - u), x1 + (W - x1) * u, y1 + (H - y1) * u); rad = RAD0 * (1 - u)
    float_dy = 7 * np.sin(2 * np.pi * 0.9 * t) * (1 - u)       # gentle float
    rect = (rect[0], rect[1] + float_dy, rect[2], rect[3] + float_dy)
    ccx, ccy = (rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2
    sx, sy = ANCHOR[0] - 150 * u, ANCHOR[1]
    # source window: card pixel (px,py) <- plate (sx + (px-ccx)/z, sy + (py-ccy)/z)
    aff = (1 / z, 0, sx - ccx / z, 0, 1 / z, sy - ccy / z)
    img = np.asarray(Image.fromarray(PLATE).transform((W, H), Image.AFFINE, aff, resample=Image.BICUBIC)).astype(np.float32)
    gz = np.asarray(Image.fromarray((GM * 255).astype(np.uint8)).transform((W, H), Image.AFFINE, aff, resample=Image.BICUBIC)).astype(np.float32) / 255
    pulse = 0.5 * (1 + np.sin(2 * np.pi * 0.8 * t - 1.2))
    img += gz[..., None] * np.array([70, 50, 200], np.float32) * (0.06 + 0.12 * pulse)     # gentle indigo rim pulse
    img += rng.normal(0, 2.5, (H, W, 1)).astype(np.float32)
    img *= 1.0 - ss((t - 1.07) / 0.13)                             # to true black at the very end
    mask = rrect(rect, rad)
    # soft shadow under the card (only while it is a card)
    sh = gaussian_filter(rrect((rect[0] + 4, rect[1] + 14, rect[2] - 4, rect[3] + 14), rad, 1.0), 18) * 0.22 * (1 - u)
    out = BASE_IMG.copy() * (1 - sh[..., None])
    out = out * (1 - mask[..., None]) + img * mask[..., None]
    out += rng.normal(0, 1.6, (H, W, 1)).astype(np.float32) * (1 - mask[..., None])         # grain on the light base
    ta = 1.0 - ss((t - 0.6) / 0.22)
    if ta > 0.003:
        tl = text_layer(ta); out = out * (1 - tl[..., None]) + np.array(INK, np.float32) * tl[..., None]
    out *= 1.0 - ss((t - 1.07) / 0.13)                              # whole frame to pure black (base is hidden by then)
    return np.clip(out, 0, 255).astype(np.uint8)
def main():
    global PLATE, GM, BASE_IMG
    p, gm = bh.build_plate(); PLATE = np.clip(bright(p), 0, 255).astype(np.uint8); GM = gm; BASE_IMG = make_base()
    rng = np.random.default_rng(5)
    if "--still" in sys.argv:
        tt = float(sys.argv[sys.argv.index("--t") + 1]) if "--t" in sys.argv else 0.0
        Image.fromarray(frame(0, rng, tt)).save(sys.argv[sys.argv.index("--still") + 1]); return
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), sys.argv[1]], stdin=subprocess.PIPE)
    for k in range(int(round(DUR * FPS))): enc.stdin.write(frame(k, rng).tobytes())
    enc.stdin.close(); enc.wait()
if __name__ == "__main__": main()
