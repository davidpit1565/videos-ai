#!/usr/bin/env python3
"""Episode 90 final2: WHOLE phone screen (1206x2622 scaled by height to 1920, black side bars), no captions,
one opening title in the empty black area below the chat, rewind to the start, eased typing speed-ups, funny ending kept.
Usage: build90b.py <music.wav|none> <out.mp4> [--timeline]"""
import sys, subprocess, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC = "/root/.claude/uploads/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/f408da19-ScreenRecording_11-10-2026_21-32-34_1.mp4"
HERE = "/home/user/videos-ai/video/ep90"
FPS = 30; W, H = 1080, 1920
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
NW, NH = 1080, 2348; OY_R, OY_T, OYB = 330.0, 350.0, 330   # full-width scaled source; window offsets for replies / typing
COVER = 128                       # px at the top painted black: iOS status bar (clock/battery)
import os as _os
def _load_cues(p): return json.load(open(p))["lines"]
_OLD = _load_cues(HERE + "/voice/cues.json")
_NEWP = HERE + "/voice/cues90b.json"
_NEW = _load_cues(_NEWP) if _os.path.exists(_NEWP) else _OLD
_ob = [0.0]; _nb = [0.0]
for _o, _n in zip(_OLD, _NEW):
    _ob += [_o["start"], _o["end"]]; _nb += [_n["start"], _n["end"]]
def r(t):
    """old narration time -> new narration time (piecewise linear through the line starts/ends)"""
    if t >= _ob[-1]: return t + (_nb[-1] - _ob[-1])
    return float(np.interp(t, _ob, _nb))
REWIND = 0.4; HOOK_D = r(2.5); HOOK_HOLD = HOOK_D - REWIND
HOOK_SRC = 36.2
FINAL_FADE = 0.45; DIP = 0.12; D = r(18.62) + 0.28

def sstep(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)
def make_speed(v0, steps):
    def v(s):
        cur = v0; out = v0
        for b, w, nv in steps:
            out += (nv - cur) * sstep((s - b) / w + 0.5); cur = nv
        return out
    return v
from scipy.interpolate import PchipInterpolator
# voice-driven timeline: anchor pairs (out time, source time) per piece, PCHIP-smoothed (monotone, no speed jumps inside a piece)
ANCH = [
    [(2.5, 1.0), (3.9, 9.7), (4.05, 10.3), (4.25, 10.9), (4.6, 13.0), (5.5, 13.9)],                                  # typing 1 + "47"
    [(5.55, 17.9), (7.05, 24.4), (7.2, 26.4), (9.0, 30.4), (9.1, 31.0), (9.2, 31.6), (9.45, 33.3), (9.5, 33.4), (11.3, 35.2)],   # typing 2, begging reply
    [(11.45, 40.4), (12.0, 41.6), (12.05, 41.7), (12.2, 42.2), (12.35, 43.8), (12.4, 44.0), (12.85, 44.5)],           # "Yes", "100"
    [(12.9, 48.3), (13.25, 49.7), (13.3, 49.9), (13.38, 50.5), (13.45, 54.4), (13.5, 54.7), (14.7, 56.2), (15.5, 57.0)],  # Fahhhhh, laughing reply
]
ANCH = [[(r(t_), s_) for t_, s_ in a_] for a_ in ANCH]
PIECES = [dict(s0=a_[0][1], s1=a_[-1][1]) for a_ in ANCH]
MAPS = []
for a_ in ANCH:
    ts = [x[0] for x in a_]; ss_ = [x[1] for x in a_]
    MAPS.append(dict(t0=ts[0], t1=ts[-1], fs=PchipInterpolator(ts, ss_), fi=PchipInterpolator(ss_, ts)))
T_END = MAPS[-1]["t1"]
NP = len(PIECES)
def src_at(t):
    if t < HOOK_HOLD: return None, -1
    if t < HOOK_D: return (t - HOOK_HOLD) / REWIND, -2
    for i, m in enumerate(MAPS):
        if t < m["t1"]:
            if t < m["t0"]: return PIECES[i]["s0"], i      # tiny gap before the piece starts: hold its first frame
            return float(m["fs"](t)), i
    return PIECES[-1]["s1"], NP
def ot(s):
    for m, p in zip(MAPS, PIECES):
        if p["s0"] <= s <= p["s1"]: return float(m["fi"](s))
def dip_gain(t):
    g = 1.0
    for m in MAPS[1:]:
        tb = m["t0"]
        if tb - DIP < t < tb: g = min(g, sstep((tb - t) / DIP))
        elif tb <= t < tb + DIP * 1.2: g = min(g, sstep((t - tb) / (DIP * 1.2)))
    return g
def zoom_img(img, z, ax=0.5, ay=0.30):
    if z <= 1.0005: return img
    h, w = img.shape[:2]; cx, cy = ax * w, ay * h
    return np.asarray(Image.fromarray(img).transform((w, h), Image.AFFINE, (1 / z, 0, cx - cx / z, 0, 1 / z, cy - cy / z), resample=Image.BICUBIC))
def zoom_at(t):
    spans = [(ot(33.4), ot(35.2), 1.0, 1.02), (ot(55.0), D - FINAL_FADE, 1.0, 1.02)]
    for a, b, z0, z1 in spans:
        if a <= t <= b: return z0 + (z1 - z0) * sstep((t - a) / (b - a))
        if t > b and (a, b) == spans[-1][:2]: return z1
    # hold last value of previous span between spans
    last = 1.0
    for a, b, z0, z1 in spans:
        if t > b: last = 1.0
    return 1.0

LOGO = Image.open(f"{HERE}/assets/chatgpt-mark.png").convert("RGBA")
def title_alpha(t):
    return 1.0 - sstep((t - 1.9) / 0.5)
def title_alpha(t):
    return 1.0 - sstep((t - 1.85) / 0.4)
# ======= HOOK TEXT / END CARD WORDING (variables) =======
HOOK_LINE1 = "I gave ChatGPT"
HOOK_LINE2 = "a 47-day timeout."
END_L1 = "Send this to someone"
END_L2 = "who ghosts you."
# =========================================================
FONT_H = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
TRK = 0.03
def _lw(t, f, sz): return sum(f.getlength(c) for c in t) - TRK * sz * (len(t) - 1)
def _size_for(lines, width=950):
    ref = ImageFont.truetype(FONT_H, 100)
    return int(width / max(_lw(l, ref, 100) / 100 for l in lines))
def _text_block(lines, y, alpha, size):
    lay = Image.new("L", (W, H), 0); d = ImageDraw.Draw(lay); f = ImageFont.truetype(FONT_H, size)
    for l in lines:
        x = (W - _lw(l, f, size)) / 2
        for c in l: d.text((x, y), c, font=f, fill=255); x += f.getlength(c) - TRK * size
        y += int(size * 1.03)
    return np.asarray(lay, np.float32) / 255 * alpha
def title_alpha(t):
    return 1.0 - sstep((t - (HOOK_HOLD - 0.15)) / 0.35)            # fully visible from frame 0, soft fade 1.95-2.3 s
def draw_title(canvas, a):
    if a <= 0.003: return
    size = _size_for([HOOK_LINE1, HOOK_LINE2])
    # real ChatGPT badge (icon alone) above the words, left aligned with the text block
    bs = 110
    badge = Image.new("RGBA", (bs, bs), (0, 0, 0, 0)); dd = ImageDraw.Draw(badge)
    dd.rounded_rectangle((0, 0, bs - 1, bs - 1), radius=27, fill=(255, 255, 255, 255))
    badge.alpha_composite(LOGO.resize((68, 68), Image.LANCZOS), ((bs - 68) // 2, (bs - 68) // 2))
    ba = np.asarray(badge, dtype=np.float32) / 255.0
    by, bx = 560, 65
    reg = canvas[by:by + bs, bx:bx + bs]
    reg[:] = reg * (1 - ba[..., 3:4] * a) + ba[..., :3] * 255 * ba[..., 3:4] * a
    tl = _text_block([HOOK_LINE1, HOOK_LINE2], 700, a, size)
    canvas[:] = canvas * (1 - tl[..., None]) + np.array([250, 250, 250], np.float32) * tl[..., None]
def end_card_start(): return r(16.2)
def draw_end(canvas, t):
    t0 = end_card_start()
    if t < t0: return
    a = sstep((t - t0) / 0.35) * (1.0 if t < D - FINAL_FADE else 1 - sstep((t - (D - FINAL_FADE)) / FINAL_FADE))
    size = _size_for([END_L1, END_L2]); tl = _text_block([END_L1, END_L2], 800, a, size)
    canvas[:] = canvas * (1 - tl[..., None]) + np.array([250, 250, 250], np.float32) * tl[..., None]

def tf_img(img, z, ax_src, ay_src, ax_out, ay_out):
    if abs(z - 1) < 1e-4 and abs(ay_out - ay_src) < 0.5 and abs(ax_out - ax_src) < 0.5: return img
    h, w = img.shape[:2]
    return np.asarray(Image.fromarray(img).transform((w, h), Image.AFFINE, (1 / z, 0, ax_src - ax_out / z, 0, 1 / z, ay_src - ay_out / z), resample=Image.BICUBIC))

VF = f"fps={FPS},scale={NW}:{NH}"
FB = NW * NH * 3
def one_frame(s):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{s:.3f}", "-i", SRC, "-vf", VF, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    return np.frombuffer(p.stdout, np.uint8).reshape(NH, NW, 3)
class Reader:
    def __init__(self, t0, t1):
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{t0}", "-t", f"{t1 - t0}", "-i", SRC, "-vf", VF, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        self.t0 = t0; self.idx = -1; self.cur = None
    def get(self, s):
        want = int(round((s - self.t0) * FPS))
        while self.idx < want:
            b = self.p.stdout.read(FB)
            if len(b) < FB: break
            self.cur = np.frombuffer(b, np.uint8).reshape(NH, NW, 3); self.idx += 1
        return self.cur


# contrast: gentle monotone curve, same for R,G,B (no tint). The recording is dimmed: text peaks at ~129/255.
def _make_lut():
    xs = np.array([0, 40, 80, 129, 140, 255], np.float64); ys = np.array([0, 50, 104, 238, 255, 255], np.float64)
    # monotone cubic (Fritsch-Carlson)
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
HOOK_Z0, HOOK_Z1 = 1.0, 1.02    # the full-width framing already spans the content edge to edge: only a hair of push-in is possible without clipping
AXN, AYN = 540.5, 587.0          # source point (new space) the hold/pull-back is anchored on (centre of the old letterboxed hold)
def oy_at(t):
    """vertical window offset (px of the 2348-tall scaled source): reply reading framing, eased shift while typing so the input stays in view"""
    o = OY_R
    for a_, c_ in [(1.3, 9.5), (18.0, 30.4), (40.4, 41.5), (48.3, 49.6)]:
        ta, tc = ot(a_), ot(c_)
        o += (OY_T - OY_R) * sstep((t - ta) / 0.45) * (1 - sstep((t - tc) / 0.45))
    return o
def view(t):
    """-> (z, anchor_src(x,y), anchor_out(x,y)): out = anchor_out + (src - anchor_src) * z"""
    oy = oy_at(max(t, HOOK_D))
    if t < HOOK_HOLD:
        return HOOK_Z0 + (HOOK_Z1 - HOOK_Z0) * sstep(t / HOOK_HOLD), (AXN, AYN), (AXN, AYN - oy)
    if t < HOOK_D:
        e = sstep((t - HOOK_HOLD) / REWIND)
        return HOOK_Z1 + (1.0 - HOOK_Z1) * e, (AXN, AYN), (AXN, AYN - oy)
    z = zoom_at(t)
    ax, ay = 0.5 * W, 0.30 * H
    return z, (ax, oy + ay), (ax, ay)
def compose(frame, gain, t, canvas):
    z, (sx, sy), (ox, oy_) = view(t)
    img = LUT[frame].copy()
    img[:OYB] = 0                                   # status strip, header icons and scrolled-away remnants never show
    aff = (1 / z, 0, sx - ox / z, 0, 1 / z, sy - oy_ / z)
    out = np.asarray(Image.fromarray(img).transform((W, H), Image.AFFINE, aff, resample=Image.BICUBIC))
    canvas[:] += out.astype(np.float32) * gain

def main():
    music, outp = sys.argv[1], sys.argv[2]
    if "--timeline" in sys.argv:
        for m, p in zip(MAPS, PIECES):
            print(f"src {p['s0']}-{p['s1']} -> out {m['t0']:.2f}-{m['t1']:.2f}")
        print(f"hold 0-{HOOK_HOLD}, rewind to {HOOK_D}, end {T_END:.2f}, D={D:.2f}"); return
    hook = one_frame(HOOK_SRC)
    nre = int(round(REWIND * FPS))
    rew = [one_frame(HOOK_SRC - (HOOK_SRC - 0.8) * sstep((k + 1) / nre)) for k in range(nre)]
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if music != "none": cmd += ["-i", music]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS)]
    if music != "none": cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest"]
    cmd += ["-movflags", "+faststart", outp]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    rd = {}; last = hook
    for k in range(int(round(D * FPS))):
        t = k / FPS
        canvas = np.zeros((H, W, 3), np.float32)
        s, pi = src_at(t)
        if pi == -1: frame = hook
        elif pi == -2: frame = rew[min(nre - 1, int(s * nre))]
        elif pi == NP: frame = last
        else:
            if pi not in rd:
                for r in rd.values(): r.p.kill()
                rd.clear(); pc = PIECES[pi]; rd[pi] = Reader(pc["s0"], pc["s1"] + 0.2)
            frame = rd[pi].get(s); last = frame
        gain = (dip_gain(t) if pi >= 0 else 1.0) * (1.0 if t < D - FINAL_FADE else 1 - sstep((t - (D - FINAL_FADE)) / FINAL_FADE))
        compose(frame, gain, t, canvas)
        if t < 2.5: draw_title(canvas, title_alpha(t))
        draw_end(canvas, t)
        enc.stdin.write(np.clip(canvas, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()
    for r in rd.values(): r.p.kill()
    print("done", D)
if __name__ == "__main__": main()
