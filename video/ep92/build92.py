#!/usr/bin/env python3
"""Episode 92: David's real ChatGPT recording ("I'm about to delete you. You have 10 seconds to convince me not to."), full-width framing,
hook text on frame 0, rewind, answer streams, doc-space camera push-ins, end card. Only real pixels from the recording are the chat.
Usage: build92.py <cues.json> <out.mp4> [--timeline] [--frame T out.png] [--nomask]
cues.json = {"lines":[{"n":1,"start":..,"end":..}, ... 5 lines]} (voice cues for final1; reading-time cues for the no-voice final2)."""
import sys, subprocess, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.interpolate import PchipInterpolator

SRC = "/root/.claude/uploads/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/739398dd-ScreenRecording_11-11-2026_05-10-31_1.mp4"
HERE = "/home/user/videos-ai/video/ep92"
FPS = 30; W, H = 1080, 1920
NW, NH = 1080, 2348                       # source scaled to 1080 wide
COVER = 330                               # screen rows above this are painted black (iOS status strip + header icons)
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
HOOK_SRC = 5.7                            # source second shown on frame 0 (answer + 'stop talking' paragraph readable)
HOOK_SHIFT = 255                          # px the chat is pushed down on frame 0 so the hook text sits in the empty black above it
NAME_BOX = (41, 698, 166, 754)            # x0,y0,x1,y1 in DOC coords (scroll 0): 'David' (the comma stays)
NAME_FROM = 3.75                          # source second from which the name can be on screen
END_HOLD = 2.5; FINAL_FADE = 0.55

def sstep(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)

# ---------------- cues ----------------
cues_path = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else f"{HERE}/voice/cues.json"
CU = {l["n"]: l for l in json.load(open(cues_path))["lines"]}
s1, e1 = CU[1]["start"], CU[1]["end"]; s2, e2 = CU[2]["start"], CU[2]["end"]; s3, e3 = CU[3]["start"], CU[3]["end"]
s4, e4 = CU[4]["start"], CU[4]["end"]; s5, e5 = CU[5]["start"], CU[5]["end"]
HOOK_END = max(2.3, e1 + 0.12); REWIND = 0.5; P0 = HOOK_END + REWIND
# ---------------- source time map out->src (monotone, smooth) ----------------
# (out, src): typed text static (fast), send, wait, answer streams ~real time, static hold (invisible cut), scroll, last lines appear
TYPED, SEND, WAIT = 0.30, 0.55, 0.55
tA = P0; tB = P0 + TYPED; tC = tB + SEND; tD = tC + WAIT          # src 0.5 / 1.7 / 2.5 / 3.9
tE = s2 + 0.10                                                     # src 4.4 'Don't keep me' appears with the voice
tF = tE + 2.1                                                      # src 6.3 first part fully streamed (rest is behind the input bar)
tG = s4 - 1.95                                                     # src 9.0 auto-scroll starts, 'Challenge me' comes up
tG2 = tG + 1.4; tG3 = tG + 1.9                                     # src 10.4 / 11.1
tH = s4 + 0.05                                                     # src 11.2 'And if I fail?' appears with line 4
tI = s4 + 0.75                                                     # src 11.7 last line + icons done
MAP = [(0, HOOK_SRC), (HOOK_END, HOOK_SRC)]
MAPPTS = [(tA, 0.5), (tB, 1.7), (tC, 2.5), (tD, 3.9), (tE, 4.4), (tF, 6.3), (tF + 0.3, 6.45), (tG - 0.3, 8.85), (tG, 9.0), (tG2, 10.4), (tG3, 11.1), (tH, 11.2), (tI, 11.7), (tI + 0.01, 11.9), (1000, 11.9)]
_x = np.array([p[0] for p in MAPPTS]); _y = np.array([p[1] for p in MAPPTS])
# the static source stretch 6.45 -> 8.85 is shown as frozen frame (identical pixels), not played
_SRCMAP = PchipInterpolator(_x, _y)
D = e4 + 0.25 + END_HOLD + 0.2
if len(sys.argv) > 1 and "--endcard-after-e5" in sys.argv: pass
D = max(D, e5 + 0.5)
END_T = max(e4 + 0.2, s5 - 0.05)                                   # end card appears as line 5 starts
D = max(e5 + 1.0, END_T + END_HOLD) if s5 - e4 < 1.5 else max(D, END_T + END_HOLD)
def src_at(t):
    if t < HOOK_END: return HOOK_SRC, "hook"
    if t < P0:
        return HOOK_SRC - (HOOK_SRC - 0.5) * sstep((t - HOOK_END) / REWIND), "rew"
    s = float(_SRCMAP(t))
    if 6.45 < s < 8.85: s = 6.45
    return s, "play"
# ---------------- scroll ----------------
_sc = np.array(json.load(open(f"{HERE}/scroll.json")))
_scy = _sc[:, 1].copy()
for i in range(2, len(_scy) - 2): _scy[i] = np.median(_sc[i - 2:i + 3, 1])
def scroll_at(s):
    if s <= 8.0: return 0.0
    return float(np.interp(s, _sc[:, 0], _scy))
# ---------------- camera (doc space) ----------------
# key: (out t, z, fx, fy_doc, ox, oy)  doc point (fx,fy) is shown at out (ox,oy) scaled by z
HY = 960 + HOOK_SHIFT * -1 + 0
KEYS = [
    (0.0, 1.00, 540, 960 - HOOK_SHIFT, 540, 960),
    (HOOK_END, 1.022, 540, 960 - HOOK_SHIFT, 540, 960),
    (P0 + 0.00, 1.00, 540, 1390, 540, 960),
    (tC, 1.00, 540, 1390, 540, 960),
    (tD, 1.00, 540, 1290, 540, 960),
    (s2 + 0.25, 1.00, 540, 1290, 540, 960),
    (s2 + 1.35, 1.06, 500, 866, 540, 800),
    (max(e2 - 0.9, s2 + 2.0), 1.07, 500, 905, 540, 800),
    (s3 + 0.55, 1.04, 524, 1310, 540, 780),
    (tG, 1.055, 524, 1445, 540, 780),
    (tG2, 1.04, 524, 2150, 540, 800),
    (tH + 0.25, 1.07, 500, 2590, 540, 800),
    (tI + 1.2, 1.085, 500, 2615, 540, 800),
    (1000, 1.10, 500, 2640, 540, 800),
]
# make times strictly increasing
for i in range(1, len(KEYS)):
    if KEYS[i][0] <= KEYS[i - 1][0] + 0.05: KEYS[i] = (KEYS[i - 1][0] + 0.05,) + KEYS[i][1:]
_kt = [k[0] for k in KEYS]
_cam = [PchipInterpolator(_kt, [k[j] for k in KEYS]) for j in range(1, 6)]
def cam(t):
    return [float(c(min(t, _kt[-1]))) for c in _cam]
# ---------------- contrast LUT (same gentle monotone curve as ep90, identical in R,G,B) ----------------
def _make_lut():
    xs = np.array([0, 40, 80, 129, 140, 255], np.float64); ys = np.array([0, 50, 104, 238, 255, 255], np.float64)
    h = np.diff(xs); d = np.diff(ys) / h; m = np.zeros(len(xs)); m[0] = d[0]; m[-1] = d[-1]
    for i in range(1, len(xs) - 1): m[i] = 0 if d[i - 1] * d[i] <= 0 else 2 / (1 / d[i - 1] + 1 / d[i])
    for i in range(len(d)):
        if d[i] == 0: m[i] = m[i + 1] = 0
        else:
            a, b = m[i] / d[i], m[i + 1] / d[i]; r = a * a + b * b
            if r > 9: tau = 3 / np.sqrt(r); m[i] = tau * a * d[i]; m[i + 1] = tau * b * d[i]
    out = np.zeros(256)
    for x in range(256):
        i = min(np.searchsorted(xs, x, side="right") - 1, len(xs) - 2); t = (x - xs[i]) / h[i]
        out[x] = (2*t**3-3*t**2+1)*ys[i] + (t**3-2*t**2+t)*h[i]*m[i] + (-2*t**3+3*t**2)*ys[i+1] + (t**3-t**2)*h[i]*m[i+1]
    return np.clip(out, 0, 255).round().astype(np.uint8)
LUT = _make_lut()
# ---------------- text ----------------
TRK = 0.03
def _lw(t, f, sz): return sum(f.getlength(c) for c in t) - TRK * sz * (len(t) - 1)
def _size_for(lines, width=940, cap=999):
    ref = ImageFont.truetype(FONT, 100)
    return min(cap, int(width / max(_lw(l, ref, 100) / 100 for l in lines)))
def _text_layer(lines, y, size, lh=1.03):
    lay = Image.new("L", (W, H), 0); d = ImageDraw.Draw(lay); f = ImageFont.truetype(FONT, size)
    for l in lines:
        x = (W - _lw(l, f, size)) / 2
        for c in l: d.text((x, y), c, font=f, fill=255); x += f.getlength(c) - TRK * size
        y += int(size * lh)
    return np.asarray(lay, np.float32) / 255
HOOK_LINES = ["I told ChatGPT", "I'd delete it", "in 10 seconds."]
END_LINES = ["Send this to", "someone who talks", "to ChatGPT", "all day."]
HOOK_SIZE = _size_for(HOOK_LINES, cap=94); END_SIZE = _size_for(END_LINES, cap=104)
HOOK_LAYER = _text_layer(HOOK_LINES, 268, HOOK_SIZE, 1.0)
END_Y = 700
END_LAYER = _text_layer(END_LINES, END_Y, END_SIZE, 1.04)
LOGO = Image.open(f"{HERE}/assets/chatgpt-mark.png").convert("RGBA")
def hook_alpha(t):
    return 1.0 - sstep((t - (HOOK_END - 0.38)) / 0.36) if t < HOOK_END else 0.0
def end_alpha(t):
    a = sstep((t - END_T) / 0.5)
    return a * (1.0 - sstep((t - (D - FINAL_FADE)) / FINAL_FADE))
def add_layer(canvas, layer, a):
    if a > 0.002: canvas[:] = canvas * (1 - layer[..., None] * a) + 250.0 * layer[..., None] * a
def add_badge(canvas, a, cx, cy, bs=120):
    if a <= 0.002: return
    badge = Image.new("RGBA", (bs, bs), (0, 0, 0, 0)); dd = ImageDraw.Draw(badge)
    dd.rounded_rectangle((0, 0, bs - 1, bs - 1), radius=int(bs * .25), fill=(255, 255, 255, 255))
    ic = int(bs * .62); badge.alpha_composite(LOGO.resize((ic, ic), Image.LANCZOS), ((bs - ic) // 2, (bs - ic) // 2))
    ba = np.asarray(badge, np.float32) / 255; x0, y0 = int(cx - bs / 2), int(cy - bs / 2)
    reg = canvas[y0:y0 + bs, x0:x0 + bs]; reg[:] = reg * (1 - ba[..., 3:4] * a) + ba[..., :3] * 255 * ba[..., 3:4] * a
# ---------------- source frames ----------------
VF = f"scale={NW}:{NH}"
_cache = {}
def one_frame(s):
    k = int(round(s * 60))
    if k in _cache: return _cache[k]
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{k / 60:.4f}", "-i", SRC, "-vf", VF, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    fr = np.frombuffer(p.stdout, np.uint8).reshape(NH, NW, 3)
    if len(_cache) > 6: _cache.pop(next(iter(_cache)))
    _cache[k] = fr; return fr
def screen_img(s, mask=True):
    img = LUT[one_frame(s)].copy()
    img[:COVER] = 0
    if mask and s >= NAME_FROM:
        sc = scroll_at(s); x0, y0, x1, y1 = NAME_BOX
        ya, yb = int(round(y0 - sc)), int(round(y1 - sc))
        if yb > 0 and ya < NH: img[max(0, ya):min(NH, yb), x0:x1] = 0
    return img
def compose(t, canvas, mask=True):
    s, mode = src_at(t)
    img = screen_img(s, mask)
    z, fx, fy, ox, oy = cam(t)
    sc = scroll_at(s)
    fys = fy - sc                                 # focus in screen coords
    aff = (1 / z, 0, fx - ox / z, 0, 1 / z, fys - oy / z)
    out = np.asarray(Image.fromarray(img).transform((W, H), Image.AFFINE, aff, resample=Image.BICUBIC)).astype(np.float32)
    gain = 1.0
    ea = end_alpha(t)
    # chat dims softly under the end card, then everything fades to black
    dim = 1.0 - 0.9 * sstep((t - END_T) / 0.6)
    fade = 1.0 - sstep((t - (D - FINAL_FADE)) / FINAL_FADE)
    canvas[:] = out * dim * (fade if t > D - FINAL_FADE else 1.0)
    add_layer(canvas, HOOK_LAYER, hook_alpha(t))
    if ea > 0:
        add_layer(canvas, END_LAYER, ea); add_badge(canvas, ea, W / 2, END_Y - 95)

def main():
    args = sys.argv[1:]
    if "--timeline" in args:
        print(f"hook 0-{HOOK_END:.2f} rewind -> {P0:.2f}; send {tC:.2f}; answer {tE:.2f}; static-cut {tF:.2f}->{tG:.2f}; 'And if I fail' {tH:.2f}; end card {END_T:.2f}; D={D:.2f}")
        print("hook size", HOOK_SIZE, "end size", END_SIZE); return
    if "--frame" in args:
        i = args.index("--frame"); t = float(args[i + 1]); canvas = np.zeros((H, W, 3), np.float32); compose(t, canvas, "--nomask" not in args)
        Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8)).save(args[i + 2]); return
    outp = [a for a in args if a.endswith(".mp4")][0]
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), "-movflags", "+faststart", outp]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(int(round(D * FPS))):
        canvas = np.zeros((H, W, 3), np.float32); compose(k / FPS, canvas)
        enc.stdin.write(np.clip(canvas, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait(); print("done", D)
if __name__ == "__main__": main()
