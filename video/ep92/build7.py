#!/usr/bin/env python3
"""ep92 final7 (dark main / light variant via THEME=light). Whole beats, soft fades, big type inside the safe box; words are the real chat's words (re-typed).
Usage: [THEME=light] build6.py <out.mp4> | --frame T out.png | --timeline"""
import sys, os, subprocess, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import binary_fill_holes
sys.path.insert(0, "/home/user/videos-ai/video/ep92")
_a = sys.argv[1:]
sys.argv = ["x", "/home/user/videos-ai/video/ep92/voice/cues.json"]
import build92 as b
sys.argv = ["x"] + _a
W, H = 1080, 1920; FPS = 30
LIGHT = os.environ.get("THEME", "dark") == "light"
CUES = json.load(open("/tmp/e7/cues7.json")); L = {l["n"]: l for l in CUES["lines"]}; D = CUES["D"]
BG = (250, 250, 248) if LIGHT else (14, 14, 16)
TXT = (22, 22, 24) if LIGHT else (250, 250, 250)
BUBF = (28, 28, 30) if LIGHT else (40, 28, 99); BUBT = (250, 250, 250)
BOXF = (22, 22, 24) if LIGHT else (250, 250, 250); BOXT = (250, 250, 248) if LIGHT else (14, 14, 16)
def sstep(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)
def ease(x):
    x = min(1.0, max(0.0, x)); return x * x * x * (x * (6 * x - 15) + 10)
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"
SRC = "/root/.claude/uploads/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/739398dd-ScreenRecording_11-11-2026_05-10-31_1.mp4"
p = subprocess.run(["ffmpeg", "-v", "error", "-ss", "13.9", "-i", SRC, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
F13 = b.LUT[np.frombuffer(p.stdout, np.uint8).reshape(2622, 1206, 3)]
em = F13[1984:2062, 856:926]; ea = binary_fill_holes(em.max(2) > 12)
EMO = Image.fromarray(np.dstack([em, (ea * 255).astype(np.uint8)]), "RGBA")
LOGO = Image.open("/home/user/videos-ai/video/ep92/assets/chatgpt-mark.png").convert("RGBA")
def fnt(sz): return ImageFont.truetype(FONT, sz)
def fit(lines, maxw, cap=999):
    f = fnt(100); return min(cap, int(100 * maxw / max(f.getlength(l) for l in lines)))
def new(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))
def draw_lines(im, lines, size, cy, lh, boxes=()):
    d = ImageDraw.Draw(im); f = fnt(size)
    for i, ln in enumerate(lines):
        y = cy + (i - (len(lines) - 1) / 2) * size * lh
        if i in boxes:
            wd = f.getlength(ln); pad = int(size * 0.2)
            d.rounded_rectangle((540 - wd / 2 - pad, y - size * 0.62, 540 + wd / 2 + pad, y + size * 0.62), radius=int(size * 0.18), fill=BOXF + (255,))
            d.text((540, y), ln, font=f, fill=BOXT + (255,), anchor="mm")
        else: d.text((540, y), ln, font=f, fill=TXT + (255,), anchor="mm")
def badge(im, cx, cy, bs):
    t = Image.new("RGBA", (bs, bs), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rounded_rectangle((0, 0, bs - 1, bs - 1), radius=int(bs * .25), fill=(255, 255, 255, 255), outline=((214, 214, 210, 255) if LIGHT else None), width=3)
    ic = int(bs * .62); t.alpha_composite(LOGO.resize((ic, ic), Image.LANCZOS), ((bs - ic) // 2, (bs - ic) // 2)); im.alpha_composite(t, (int(cx - bs / 2), int(cy - bs / 2)))
def premult(im):
    a = np.asarray(im, np.float32); al = a[..., 3:4] / 255
    return Image.fromarray((a[..., :3] * al).astype(np.uint8)), Image.fromarray(a[..., 3].astype(np.uint8))
# ---------------- beats ----------------
CEN = 758
Q = ["I'm about", "to delete you.", "You have 10", "seconds to convince", "me not to."]
T2 = ["Don't keep me", "because I'm", "an AI.", "Keep me only", "if I make your", "life easier."]
T3 = ["You've", "repeatedly had", "to tell me to", "stop talking", "and actually", "finish the work."]
T4A = ["And if", "I fail?"]; T4B = ["You've got", "your 10 seconds", "back."]
ENDL = ["Send this", "to someone", "who talks to", "ChatGPT", "all day."]
SQ = fit(Q, 850); S2 = fit(T2, 900); S3 = fit(T3, 900, 140); S4A = fit(T4A, 900, 200); S4B = fit(T4B, 900, 130); SE = fit(ENDL, 900, 128)
def beat1():
    im = new(); qh = int(SQ * 1.18) * len(Q) + 100; BAD = 210; GAP = 70; top = int(CEN - (BAD + GAP + qh) / 2)
    d = ImageDraw.Draw(im); d.rounded_rectangle((70, top + BAD + GAP, 1010, top + BAD + GAP + qh), radius=70, fill=BUBF + (255,))
    f = fnt(SQ); cy = top + BAD + GAP + qh / 2
    for i, ln in enumerate(Q): d.text((540, cy + (i - 2) * SQ * 1.18), ln, font=f, fill=BUBT + (255,), anchor="mm")
    badge(im, 540, top + BAD / 2, BAD); return im
def beat2(): im = new(); draw_lines(im, T2, S2, CEN, 1.14); return im
def beat3(): im = new(); draw_lines(im, T3, S3, CEN, 1.14, boxes=(3,)); return im
hA = int(2 * S4A * 1.02); hB = int(3 * S4B * 1.12); G4 = 80; top4 = int(CEN - (hA + G4 + hB) / 2)
def beat4a(): im = new(); draw_lines(im, T4A, S4A, top4 + hA / 2, 1.02); return im
def beat4b():
    im = new(); cyb = top4 + hA + G4 + hB / 2; draw_lines(im, T4B, S4B, cyb, 1.12)
    f = fnt(S4B); y = cyb + S4B * 1.12; wd = f.getlength("back."); esz = int(S4B * 0.95); e = EMO.resize((int(EMO.size[0] * esz / EMO.size[1]), esz), Image.LANCZOS)
    # shift the last line left to centre line + emoji: redraw is cheaper than patching, so clear and redraw
    return im, y, wd, e
def beat4b_full():
    im = new(); cyb = top4 + hA + G4 + hB / 2; d = ImageDraw.Draw(im); f = fnt(S4B)
    for i, ln in enumerate(T4B[:2]): d.text((540, cyb + (i - 1) * S4B * 1.12), ln, font=f, fill=TXT + (255,), anchor="mm")
    y = cyb + S4B * 1.12; wd = f.getlength("back."); esz = int(S4B * 0.95); e = EMO.resize((int(EMO.size[0] * esz / EMO.size[1]), esz), Image.LANCZOS)
    tot = wd + 10 + e.size[0]; x0 = 540 - tot / 2; d.text((x0, y), "back.", font=f, fill=TXT + (255,), anchor="lm"); im.alpha_composite(e, (int(x0 + wd + 10), int(y - e.size[1] / 2 + S4B * 0.06))); return im
def endcard():
    im = new(); EH = int(SE * 1.12) * len(ENDL); top = int(CEN - (170 + 44 + EH) / 2)
    if not LIGHT: badge(im, 540, top + 85, 170)
    else:  # icon appears once in the light variant (frame 0), so the end card is type only
        pass
    cy = (top + 170 + 44 + EH / 2) if not LIGHT else CEN
    draw_lines(im, ENDL, SE, cy, 1.12); return im
s1, e1, s2, e2, s3, e3, s4, e4, s5, e5 = [L[n][k] for n in (1, 2, 3, 4, 5) for k in ("start", "end")]
you4 = L[4]["words"][4][1]
# (layer builder, in0, in1, out0, out1, cy for zoom, zoom amount)
EV = [
    (beat1, 0.0, 0.0, s2 - 0.02, s2 + 0.12, 0.02),
    (beat2, s2 + 0.16, s2 + 0.42, e2 + 0.0, e2 + 0.14, 0.02),
    (beat3, e2 + 0.19, e2 + 0.45, e3 - 0.02, e3 + 0.12, 0.02),
    (beat4a, e3 + 0.16, e3 + 0.42, e4 + 0.0, e4 + 0.14, 0.02),
    (beat4b_full, you4 - 0.12, you4 + 0.2, e4 + 0.0, e4 + 0.14, 0.02),
    (endcard, e4 + 0.18, e4 + 0.50, 1e9, 1e9 + 1, 0.0),
]
LAY = [None] * len(EV)
def get(i):
    if LAY[i] is None:
        r = EV[i][0]()
        LAY[i] = premult(r)
    return LAY[i]
def compose(t):
    canvas = np.empty((H, W, 3), np.float32); canvas[:] = BG
    for i, (fn, i0, i1, o0, o1, zm) in enumerate(EV):
        if t < i0 - 1e-6 and not (i0 == 0 and t == 0): 
            if t < i0: continue
        a = (sstep((t - i0) / (i1 - i0)) if i1 > i0 else 1.0) * (1 - sstep((t - o0) / (o1 - o0)))
        if a <= 0.002: continue
        rgb, al = get(i); rise = (1 - sstep((t - i0) / (i1 - i0))) * 14 if i1 > i0 else 0
        z = 1 + zm * ease((t - i0) / max(0.5, o0 - i0)) if zm else 1.0
        if z != 1.0 or rise > 0.3:
            aff = (1 / z, 0, 540 - 540 / z, 0, 1 / z, CEN - (CEN + rise) / z)
            rgb = rgb.transform((W, H), Image.AFFINE, aff, resample=Image.BICUBIC); al = al.transform((W, H), Image.AFFINE, aff, resample=Image.BICUBIC)
        A = np.asarray(al, np.float32)[..., None] / 255; R = np.asarray(rgb, np.float32)
        canvas = canvas * (1 - A * a) + R * a
    return np.clip(canvas, 0, 255)
def main():
    a = sys.argv[1:]
    if "--timeline" in a:
        print("D", D, "sizes", SQ, S2, S3, S4A, S4B, SE, "events", [(round(e[1], 2), round(e[3], 2)) for e in EV]); return
    if "--frame" in a:
        i = a.index("--frame"); Image.fromarray(compose(float(a[i + 1])).astype(np.uint8)).save(a[i + 2]); return
    outp = [x for x in a if x.endswith(".mp4")][0]
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", outp], stdin=subprocess.PIPE)
    for k in range(int(round(D * FPS))): enc.stdin.write(compose(k / FPS).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait(); print("done", D)
if __name__ == "__main__": main()
