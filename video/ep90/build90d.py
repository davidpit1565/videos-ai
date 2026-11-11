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
SWD = 884; SX = (W - SWD) // 2
COVER = 128                       # px at the top painted black: iOS status bar (clock/battery)
HOOK_HOLD = 1.4; REWIND = 0.9; HOOK_D = HOOK_HOLD + REWIND
HOOK_SRC = 36.2
FREEZE = 1.3; FINAL_FADE = 0.9; DIP = 0.14

def sstep(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)
def make_speed(v0, steps):
    def v(s):
        cur = v0; out = v0
        for b, w, nv in steps:
            out += (nv - cur) * sstep((s - b) / w + 0.5); cur = nv
        return out
    return v
PIECES = [
    dict(s0=0.8, s1=14.6, v=make_speed(1.5, [(1.5, 1.0, 4.5), (9.8, 0.9, 1.0), (11.0, 0.4, 1.5), (13.0, 0.4, 1.0)])),
    dict(s0=17.7, s1=35.8, v=make_speed(4.5, [(24.4, 0.5, 9.0), (26.4, 0.5, 4.5), (30.5, 1.0, 1.0), (32.0, 0.4, 1.5), (33.3, 0.4, 1.0)])),
    dict(s0=40.1, s1=45.9, v=make_speed(1.0, [(42.4, 0.4, 1.5), (43.8, 0.4, 1.0)])),
    dict(s0=47.9, s1=57.9, v=make_speed(3.5, [(49.6, 0.6, 1.0), (50.7, 0.5, 4.0), (54.4, 0.5, 1.0)])),
]
def build_map():
    t = HOOK_D; maps = []
    for p in PIECES:
        n = int((p["s1"] - p["s0"]) / 0.002) + 1
        ss = np.linspace(p["s0"], p["s1"], n)
        inv = np.array([1.0 / p["v"](s) for s in ss])
        cum = np.concatenate([[0], np.cumsum((inv[1:] + inv[:-1]) / 2 * np.diff(ss))])
        maps.append(dict(t0=t, ss=ss, cum=cum, piece=p)); t += cum[-1]
    return maps, t
MAPS, T_END = build_map()
D = T_END + FREEZE
NP = len(PIECES)
def src_at(t):
    if t < HOOK_HOLD: return None, -1
    if t < HOOK_D: return (t - HOOK_HOLD) / REWIND, -2
    for i, m in enumerate(MAPS):
        if t < m["t0"] + m["cum"][-1]:
            return float(np.interp(t - m["t0"], m["cum"], m["ss"])), i
    return PIECES[-1]["s1"], NP
def ot(s):
    for m in MAPS:
        p = m["piece"]
        if p["s0"] <= s <= p["s1"]: return m["t0"] + float(np.interp(s, m["ss"], m["cum"]))
def dip_gain(t):
    g = 1.0
    for m in MAPS[1:]:
        tb = m["t0"]
        if tb - DIP < t < tb: g = min(g, sstep((tb - t) / DIP))
        elif tb <= t < tb + DIP * 1.2: g = min(g, sstep((t - tb) / (DIP * 1.2)))
    return g
def zoom_img(img, z, ax=0.35, ay=0.30):
    if z <= 1.0005: return img
    h, w = img.shape[:2]; cx, cy = ax * w, ay * h
    return np.asarray(Image.fromarray(img).transform((w, h), Image.AFFINE, (1 / z, 0, cx - cx / z, 0, 1 / z, cy - cy / z), resample=Image.BICUBIC))
def zoom_at(t):
    spans = [(ot(33.4), ot(35.8), 1.0, 1.10), (ot(43.8), ot(45.9), 1.0, 1.08), (ot(51.0), D - FINAL_FADE, 1.0, 1.12)]
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
    return 1.0 - sstep((t - 0.95) / 0.45)
def draw_title(canvas, a):
    if a <= 0.003: return
    bs = 100
    badge = Image.new("RGBA", (bs, bs), (0, 0, 0, 0)); dd = ImageDraw.Draw(badge)
    dd.rounded_rectangle((0, 0, bs - 1, bs - 1), radius=25, fill=(255, 255, 255, 255))
    badge.alpha_composite(LOGO.resize((62, 62), Image.LANCZOS), ((bs - 62) // 2, (bs - 62) // 2))
    ba = np.asarray(badge, dtype=np.float32) / 255.0
    by, bx = 292, 65
    reg = canvas[by:by + bs, bx:bx + bs]
    reg[:] = reg * (1 - ba[..., 3:4] * a) + ba[..., :3] * 255 * ba[..., 3:4] * a
    def line(txt, size, x, y, hh):
        lay = Image.new("L", (W, hh), 0); ImageDraw.Draw(lay).text((x, 0), txt, font=ImageFont.truetype(FONT, size), fill=255)
        al = np.asarray(lay, dtype=np.float32) / 255 * a
        r = canvas[y:y + hh]; r[:] = r * (1 - al[..., None]) + np.array((247, 247, 242), np.float32) * al[..., None]
    line("Does your ChatGPT", TS1, 65, 408, 130)
    line("beg too?", 130, 65, 520, 165)

def tf_img(img, z, ax_src, ay_src, ax_out, ay_out):
    if abs(z - 1) < 1e-4 and abs(ay_out - ay_src) < 0.5 and abs(ax_out - ax_src) < 0.5: return img
    h, w = img.shape[:2]
    return np.asarray(Image.fromarray(img).transform((w, h), Image.AFFINE, (1 / z, 0, ax_src - ax_out / z, 0, 1 / z, ay_src - ay_out / z), resample=Image.BICUBIC))

VF = f"fps={FPS},scale={SWD}:{H}"
FB = SWD * H * 3
def one_frame(s):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{s:.3f}", "-i", SRC, "-vf", VF, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    return np.frombuffer(p.stdout, np.uint8).reshape(H, SWD, 3)
class Reader:
    def __init__(self, t0, t1):
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{t0}", "-t", f"{t1 - t0}", "-i", SRC, "-vf", VF, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        self.t0 = t0; self.idx = -1; self.cur = None
    def get(self, s):
        want = int(round((s - self.t0) * FPS))
        while self.idx < want:
            b = self.p.stdout.read(FB)
            if len(b) < FB: break
            self.cur = np.frombuffer(b, np.uint8).reshape(H, SWD, 3); self.idx += 1
        return self.cur

HDR_Y = 290          # frame rows above this (status/header/"47" remnant) are hidden while the view is zoomed in
TS1 = 98
HOOK_Z0, HOOK_Z1, HOOK_AY = 1.17, 1.22, 1010
AXS, AYS = 540, 480
def view(t):
    """-> (zoom, ax_out, ay_out, header_alpha). Hold: zoomed on the real bubbles; then one eased pull-back to the full screen."""
    if t < HOOK_HOLD:
        z = HOOK_Z0 + (HOOK_Z1 - HOOK_Z0) * sstep(t / HOOK_HOLD)
        return z, AXS, HOOK_AY, 0.0
    if t < HOOK_D:
        e = sstep((t - HOOK_HOLD) / REWIND)
        return HOOK_Z1 + (1.0 - HOOK_Z1) * e, AXS, HOOK_AY + (AYS - HOOK_AY) * e, sstep((e - 0.4) / 0.5)
    z = zoom_at(t)
    return z, None, None, 1.0
def compose(frame, gain, t, canvas):
    z, axo, ayo, ha = view(t)
    img = np.zeros((H, W, 3), np.uint8)
    img[:, SX:SX + SWD] = frame
    img[:COVER] = 0
    if ha < 1.0: img[:HDR_Y] = (img[:HDR_Y] * ha).astype(np.uint8)
    if axo is None:
        img = zoom_img(img, z)
    else:
        img = tf_img(img, z, AXS, AYS, axo, ayo)
    canvas[:] += img.astype(np.float32) * gain
    canvas[:COVER] = 0

def main():
    music, outp = sys.argv[1], sys.argv[2]
    if "--timeline" in sys.argv:
        for m in MAPS:
            p = m["piece"]; print(f"src {p['s0']}-{p['s1']} -> out {m['t0']:.2f}-{m['t0'] + m['cum'][-1]:.2f}")
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
        enc.stdin.write(np.clip(canvas, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()
    for r in rd.values(): r.p.kill()
    print("done", D)
if __name__ == "__main__": main()
