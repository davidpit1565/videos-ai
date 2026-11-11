#!/usr/bin/env python3
"""Hook scene for ep90 final6 (2.2 s): push-in on David's phone still (images/2.webp), real ChatGPT mark painted in
(the generated knot is painted out), grain, gentle indigo pulse, crushed blacks, fade to true black. No voice.
Usage: build90_hook.py <out.mp4> [--still out.png]"""
import sys, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy.ndimage import gaussian_filter

# ======= SWAP THE HOOK WORDING HERE (David has not finally chosen; earlier favourite: "Making ChatGPT crash out") =======
HOOK_LINE1 = "ChatGPT cannot handle rejection."     # appears at 0.1 s, wraps to two lines
HOOK_LINE2 = "47 days."                              # appears at 0.8 s
# ==========================================================================================================================
IMG = "/tmp/claude-0/-home-user/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/images/2.webp"
HERE = "/home/user/videos-ai/video/ep90"
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
W, H, FPS, DUR = 1080, 1920, 30, 2.2
K = W / 941.0
T1_IN, T2_IN, T_OUT, FADE = 0.1, 0.8, 1.8, 0.35
def ss(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)

def load_plate():
    im = Image.open(IMG).convert("RGB").resize((W, H), Image.LANCZOS)
    a = np.asarray(im).astype(np.float64)
    return a
def diffuse_fill(a, mask, it=60, sig=6):
    """fill masked pixels by diffusing the surrounding colours (soft inpaint)"""
    out = a.copy(); m = mask[..., None]
    out[mask > 0.5] = np.median(a[(gaussian_filter(mask, 12) > 0.02) & (mask < 0.5)], axis=0)
    for _ in range(it):
        bl = np.stack([gaussian_filter(out[..., c], sig) for c in range(3)], -1)
        out = np.where(m > 0.5, bl, a)
    return out
def poly_mask(pts, feather=2.0):
    im = Image.new("L", (W, H), 0); ImageDraw.Draw(im).polygon([(x * K, y * K) for x, y in pts], fill=255)
    return gaussian_filter(np.asarray(im).astype(np.float64) / 255, feather)
def ellipse_mask(cx, cy, rx, ry, feather=3.0):
    im = Image.new("L", (W, H), 0); ImageDraw.Draw(im).ellipse([(cx - rx) * K, (cy - ry) * K, (cx + rx) * K, (cy + ry) * K], fill=255)
    return gaussian_filter(np.asarray(im).astype(np.float64) / 255, feather)

# logo placement (original-image coordinates): centre of the generated knot, tilt of the phone surface
LC = (385.0, 726.0); LU = (0.97, -0.17); LV = (0.50, 0.87); LSX, LSY = 88.0, 66.0   # logo width/height in image px

def build_plate():
    a = load_plate()
    glow_src = a.copy()
    # indigo rim mask for the pulse (before edits)
    r, g, b = glow_src[..., 0], glow_src[..., 1], glow_src[..., 2]
    gm = np.clip((b - np.maximum(r, g) - 10) / 55.0, 0, 1); gm = gaussian_filter(gm, 5)
    # 1) paint out the generated knot (+ its halo)
    m1 = ellipse_mask(385, 727, 62, 52, 4)
    a = diffuse_fill(a, (m1 > 0.3).astype(np.float64))
    # 2) paint out the generated placeholder text 'Message ChatGPT...' (slanted strip in the input pill)
    m2 = poly_mask([(383, 962), (386, 932), (548, 890), (548, 924)], 2)
    a = diffuse_fill(a, (m2 > 0.3).astype(np.float64), it=40, sig=3)
    # 3) real ChatGPT mark, warped to the phone's tilt, dim light grey like OLED
    logo = Image.open(f"{HERE}/assets/chatgpt-mark-white.png").convert("RGBA")
    Ls = logo.size[0]
    cx, cy = LC[0] * K, LC[1] * K
    U = np.array(LU) * LSX * K; V = np.array(LV) * LSY * K   # canvas vectors for logo width / height
    # canvas = C + (x/Ls-.5)*U + (y/Ls-.5)*V  ->  invert for PIL (canvas -> logo)
    M = np.array([[U[0] / Ls, V[0] / Ls], [U[1] / Ls, V[1] / Ls]]); Mi = np.linalg.inv(M)
    off = np.array([Ls / 2, Ls / 2]) - Mi @ np.array([cx, cy])
    warped = logo.transform((W, H), Image.AFFINE, (Mi[0, 0], Mi[0, 1], off[0], Mi[1, 0], Mi[1, 1], off[1]), resample=Image.BICUBIC)
    al = np.asarray(warped.split()[3]).astype(np.float64) / 255
    al = gaussian_filter(al, 0.6)
    glow = gaussian_filter(al, 9) * 0.28
    col = np.array([214, 214, 226], np.float64)
    a = a + col * (al[..., None] * 0.80) + np.array([150, 150, 200]) * glow[..., None] * 0.5
    return np.clip(a, 0, 255), gm

def crush(x, lo=12.0):
    return np.clip((x - lo) / (255.0 - lo), 0, 1) ** 1.05 * 255.0

def text_layer(t):
    """white-ish text, centred, no box; returns float alpha layer HxW (0..1) and draws nothing when hidden"""
    lay = Image.new("L", (W, H), 0); d = ImageDraw.Draw(lay)
    a1 = ss((t - T1_IN) / FADE) * (1 - ss((t - (T_OUT - FADE)) / FADE))
    a2 = ss((t - T2_IN) / FADE) * (1 - ss((t - (T_OUT - FADE)) / FADE))
    out = np.zeros((H, W), np.float32)
    def draw(txt_lines, size, y, alpha):
        if alpha <= 0.003: return
        l = Image.new("L", (W, H), 0); dd = ImageDraw.Draw(l); f = ImageFont.truetype(FONT, size); yy = y
        for ln in txt_lines:
            w = dd.textlength(ln, font=f); dd.text(((W - w) / 2, yy), ln, font=f, fill=int(255 * alpha)); yy += int(size * 1.08)
        np.maximum(out, np.asarray(l, np.float32) / 255, out=out)
    words = HOOK_LINE1.split(); best = None
    f = ImageFont.truetype(FONT, 88)
    lines = [HOOK_LINE1]
    if d.textlength(HOOK_LINE1, font=f) > 900:       # wrap to two lines at the most balanced break
        cands = [(abs(d.textlength(" ".join(words[:i]), font=f) - d.textlength(" ".join(words[i:]), font=f)), i) for i in range(1, len(words))]
        i = min(cands)[1]; lines = [" ".join(words[:i]), " ".join(words[i:])]
    draw(lines, 88, 276, a1)
    y2 = 276 + int(88 * 1.08) * len(lines) + 14
    draw([HOOK_LINE2], 112, y2, a2)
    return out

def frame(plate, gm, k, rng):
    t = k / FPS
    z = 1.0 + 0.30 * ss(t / 2.0)                                   # eased push-in toward the screen
    ax, ay = 0.40 * W, 0.50 * H                                     # aimed at the dark screen
    img = np.asarray(Image.fromarray(np.clip(plate, 0, 255).astype(np.uint8)).transform(
        (W, H), Image.AFFINE, (1 / z, 0, ax - ax / z, 0, 1 / z, ay - ay / z), resample=Image.BICUBIC)).astype(np.float32)
    gz = np.asarray(Image.fromarray((gm * 255).astype(np.uint8)).transform(
        (W, H), Image.AFFINE, (1 / z, 0, ax - ax / z, 0, 1 / z, ay - ay / z), resample=Image.BICUBIC)).astype(np.float32) / 255
    pulse = 0.5 * (1 + np.sin(2 * np.pi * 0.8 * t - 1.2))           # very gentle sine, no flicker
    img += gz[..., None] * np.array([60, 40, 190], np.float32) * (0.10 + 0.14 * pulse)
    img += rng.normal(0, 3.0, (H, W, 1)).astype(np.float32)          # light grain
    img = crush(img)
    bright = 1.0 - ss((t - 1.35) / 0.7)                              # fade to true black by 2.05 s
    img *= bright
    tl = text_layer(t)
    img = img * (1 - tl[..., None]) + np.array([245, 245, 245], np.float32) * tl[..., None]
    return np.clip(img, 0, 255).astype(np.uint8)

def main():
    plate, gm = build_plate()
    if "--still" in sys.argv:
        t = 0.0
        Image.fromarray(np.clip(plate, 0, 255).astype(np.uint8)).save(sys.argv[sys.argv.index("--still") + 1]); return
    out = sys.argv[1]; rng = np.random.default_rng(5)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), out], stdin=subprocess.PIPE)
    for k in range(int(round(DUR * FPS))):
        enc.stdin.write(frame(plate, gm, k, rng).tobytes())
    enc.stdin.close(); enc.wait()
if __name__ == "__main__": main()
