#!/usr/bin/env python3
"""Episode 92 build: real screen recording, re-timed (eased speed ramps), stacked crops, text overlays.
Usage: build92.py <music.wav|none> <out.mp4> [--timeline]   (--timeline prints the mapping and exits)
No voice. Source recording is read-only; nothing large is written to disk (frames are piped)."""
import sys, subprocess, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC = "/root/.claude/uploads/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/f408da19-ScreenRecording_11-10-2026_21-32-34_1.mp4"
HERE = "/home/user/videos-ai/video/ep92"
FPS = 30
W, H = 1080, 1920
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FONT_B = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"

# ---- source crops (source is 1206x2622). status bar and header are cropped out. ----
SW = 1085                       # scaled width (0.8997), 2 px trimmed each side on the canvas
A_ROWS = (360, 520, 468)        # chat area: src row, src height, out height
B_ROWS = (1380, 400, 360)       # input box + keyboard top (keyboard up)
C_ROWS = (2370, 130, 117)       # input pill (keyboard down)
A_Y, B_Y = 545, 1020
C_Y = 1084
AX = (W - SW) // 2

# ---- time map ----
def sstep(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)

def make_speed(v0, steps):
    """v0 start speed; steps = [(boundary_src_time, width, new_speed)] smooth transitions."""
    def v(s):
        cur = v0; out = v0
        for b, w, nv in steps:
            out = out + (nv - cur) * sstep((s - b) / w + 0.5)
            cur = nv
        return out
    return v

PIECES = [
    # s0, s1, speed fn.  P1: type "Choose a number..", answer 47
    dict(s0=0.8, s1=14.6, v=make_speed(4.5, [(9.8, 0.9, 1.0), (11.0, 0.4, 1.5), (13.0, 0.4, 1.0)])),
    # P2: type "Now we won't be able to talk for 47 days", the begging reply
    dict(s0=17.7, s1=36.3, v=make_speed(4.5, [(24.4, 0.5, 9.0), (26.4, 0.5, 4.5), (30.5, 1.0, 1.0),
                                              (32.0, 0.4, 1.5), (33.3, 0.4, 1.0)])),
    # P3: "Yes", 100
    dict(s0=40.1, s1=45.9, v=make_speed(1.0, [(42.4, 0.4, 1.5), (43.8, 0.4, 1.0)])),
]
HOOK_D = 2.4
DIP = 0.14
FREEZE = 4.5
FINAL_FADE = 0.7

def build_map():
    """Return list of (t_out_start, piece, table) where table maps src->out time (cumulative)."""
    t = HOOK_D
    maps = []
    for p in PIECES:
        n = int((p["s1"] - p["s0"]) / 0.002) + 1
        ss = np.linspace(p["s0"], p["s1"], n)
        inv = np.array([1.0 / p["v"](s) for s in ss])
        cum = np.concatenate([[0], np.cumsum((inv[1:] + inv[:-1]) / 2 * np.diff(ss))])
        maps.append(dict(t0=t, ss=ss, cum=cum, piece=p))
        t += cum[-1]
    return maps, t

MAPS, T_SCREEN_END = build_map()
D = T_SCREEN_END + FREEZE

def src_at(t):
    """-> (src_time, piece_index or -1 for hook / freeze)"""
    if t < HOOK_D:
        return None, -1
    for i, m in enumerate(MAPS):
        end = m["t0"] + m["cum"][-1]
        if t < end:
            s = np.interp(t - m["t0"], m["cum"], m["ss"])
            return float(s), i
    return MAPS[-1]["piece"]["s1"], 3   # freeze on the last real frame

def out_time_of(src_t):
    for m in MAPS:
        p = m["piece"]
        if p["s0"] <= src_t <= p["s1"]:
            return m["t0"] + float(np.interp(src_t, m["ss"], m["cum"]))
    return None

# keyboard-up weight as function of source time
KB = [(10.1, 10.5, 0), (16.0, 16.4, 1), (31.1, 31.5, 0), (36.6, 37.0, 1), (41.7, 42.0, 0)]
def kb_weight(s):
    w = 1.0
    for a, b, tgt in KB:
        if s >= b: w = float(tgt)
        elif s > a:
            f = sstep((s - a) / (b - a)); w = w + (tgt - w) * f
    return w

# dips at piece boundaries (screen only)
def dip_gain(t):
    g = 1.0
    for m in MAPS[1:]:
        tb = m["t0"]
        if tb - DIP < t < tb:
            g = min(g, sstep((tb - t) / DIP))
        elif tb <= t < tb + DIP * 1.2:
            g = min(g, sstep((t - tb) / (DIP * 1.2)))
    # hook -> P1 start
    tb = HOOK_D
    if tb - DIP < t < tb: g = min(g, sstep((tb - t) / DIP)) if False else g
    if tb <= t < tb + DIP * 1.2:
        g = min(g, 0.15 + 0.85 * sstep((t - tb) / (DIP * 1.2)))
    return g

# zoom keys on the chat block (out time -> zoom), anchor lower-left
def zoom_at(t):
    keys = []
    keys += [(0.0, 1.0), (HOOK_D, 1.11)]
    m2 = MAPS[1]
    tr = out_time_of(33.4); te = out_time_of(36.3)
    keys += [(tr, 1.0), (te, 1.14)]
    m3 = MAPS[2]
    t100 = out_time_of(44.0)
    keys += [(t100, 1.0), (D - FINAL_FADE, 1.20)]
    keys.sort()
    z = 1.0
    prev = (0.0, 1.0)
    for k in keys:
        if t >= k[0]:
            prev = k
        else:
            f = sstep((t - prev[0]) / max(1e-6, k[0] - prev[0]))
            # only interpolate within the three zoom spans
            if (prev[0] == 0.0 and k[0] == HOOK_D) or (prev[0] == tr and k[0] == te) or (prev[0] == t100 and k[0] == D - FINAL_FADE):
                return prev[1] + (k[1] - prev[1]) * f
            return prev[1]
    return prev[1]

# ---- captions (source-time windows) ----
LOGO = Image.open(f"{HERE}/assets/chatgpt-mark.png").convert("RGBA")

def font(sz, bold=True):
    return ImageFont.truetype(FONT if bold else FONT_B, sz)

def cap_windows():
    ot = out_time_of
    tail = T_SCREEN_END
    return [
        # (text lines, t_in, t_out, size)
        (["I ask ChatGPT", "for a number."], ot(0.8) + 0.1, ot(13.05), 92),
        (["It picks 47."], ot(13.05), ot(14.6), 92),
        (["I tell it: no talking", "for 47 days."], ot(17.7) + 0.1, ot(32.0), 92),
        (["It begs."], ot(33.0), ot(36.3), 92),
        (["I say yes."], ot(40.1) + 0.1, ot(43.9), 92),
        (["It picks a new", "number: 100."], ot(43.9), tail + 1.0, 92),
    ]

def cta_windows():
    tail = T_SCREEN_END
    return [
        (["Try it: ask for a number,", "then ghost it that", "many days."], tail + 1.1, tail + 3.1, 70),
        (["Send this to someone", "who ghosts you."], tail + 3.2, D, 70),
    ]

def draw_text_block(canvas_rgb, lines, size, y, alpha, drift=0, color=(255, 255, 255), accent_last=False):
    """Draw left-aligned bold lines at x=65 with alpha on an RGB canvas (numpy). Returns None."""
    if alpha <= 0.003: return
    f = font(size)
    lay = Image.new("L", (W, 560), 0)
    d = ImageDraw.Draw(lay)
    ly = 0
    for ln in lines:
        d.text((65, ly), ln, font=f, fill=255)
        ly += int(size * 1.08)
    a = np.asarray(lay, dtype=np.float32) / 255.0 * alpha
    y0 = int(round(y + drift))
    h = min(560, H - y0)
    reg = canvas_rgb[y0:y0 + h]
    col = np.array(color, dtype=np.float32)
    reg[:] = reg * (1 - a[:h, :, None]) + col * a[:h, :, None]

def eased_alpha(t, t_in, t_out, fin=0.4, fout=0.3):
    if t < t_in or t > t_out: return 0.0, 0.0
    a = sstep((t - t_in) / fin) * (1 - sstep((t - (t_out - fout)) / fout))
    drift = (1 - sstep((t - t_in) / fin)) * 14
    return a, drift

def hook_layer(canvas, t):
    """frame 0 already complete: logo + two big lines. Only fades out at the end of the hook."""
    a = 1.0
    if t > HOOK_D - 0.25: a = 1 - sstep((t - (HOOK_D - 0.25)) / 0.25)
    if a <= 0: return
    # badge: white rounded square with the real mark
    bs = 112
    badge = Image.new("RGBA", (bs, bs), (0, 0, 0, 0))
    dd = ImageDraw.Draw(badge)
    dd.rounded_rectangle((0, 0, bs - 1, bs - 1), radius=28, fill=(255, 255, 255, 255))
    mk = LOGO.resize((70, 70), Image.LANCZOS)
    badge.alpha_composite(mk, ((bs - 70) // 2, (bs - 70) // 2))
    ba = np.asarray(badge, dtype=np.float32) / 255.0
    by, bx = 292, 65
    reg = canvas[by:by + bs, bx:bx + bs]
    reg[:] = reg * (1 - ba[..., 3:4] * a) + ba[..., :3] * 255 * ba[..., 3:4] * a
    draw_text_block(canvas, ["ChatGPT"], 118, 282, a, color=(255, 255, 255)) if False else None
    f = font(124)
    lay = Image.new("L", (W, 330), 0)
    d = ImageDraw.Draw(lay)
    d.text((65 + bs + 26, -8), "ChatGPT", font=f, fill=255)
    lay2 = Image.new("L", (W, 330), 0)
    d2 = ImageDraw.Draw(lay2)
    d2.text((65, 0), "begged me.", font=font(140), fill=255)
    a1 = np.asarray(lay, dtype=np.float32) / 255 * a
    a2 = np.asarray(lay2, dtype=np.float32) / 255 * a
    y1, y2 = 290, 412
    green = np.array([25, 195, 125], dtype=np.float32)
    r = canvas[y1:y1 + 130]; r[:] = r * (1 - a1[:130, :, None]) + 255 * a1[:130, :, None]
    r = canvas[y2:y2 + 170]; r[:] = r * (1 - a2[:170, :, None]) + green * a2[:170, :, None]

def zoom_box(img, z, ax=0.3, ay=0.78):
    """img: HxWx3 uint8 chat block; zoom about anchor, same output size."""
    if z <= 1.0005: return img
    h, w = img.shape[:2]
    pil = Image.fromarray(img)
    cx, cy = ax * w, ay * h
    # output (x,y) <- source (cx + (x-cx)/z, cy + (y-cy)/z)
    a = 1 / z; c = cx - cx / z; e = 1 / z; f_ = cy - cy / z
    return np.asarray(pil.transform((w, h), Image.AFFINE, (a, 0, c, 0, e, f_), resample=Image.BICUBIC))

# ---- source reader ----
STACK_H = A_ROWS[2] + B_ROWS[2] + C_ROWS[2]
FRAME_BYTES = SW * STACK_H * 3
def vf(a=A_ROWS, b=B_ROWS, c=C_ROWS):
    return (f"fps={FPS},split=3[a][b][c];"
            f"[a]crop=1206:{a[1]}:0:{a[0]},scale={SW}:{a[2]}[A];"
            f"[b]crop=1206:{b[1]}:0:{b[0]},scale={SW}:{b[2]}[B];"
            f"[c]crop=1206:{c[1]}:0:{c[0]},scale={SW}:{c[2]}[C];"
            f"[A][B][C]vstack=inputs=3")

def one_frame(src_t):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{src_t}", "-i", SRC, "-filter_complex", vf(),
                        "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    return np.frombuffer(p.stdout, np.uint8).reshape(STACK_H, SW, 3)

class Reader:
    def __init__(self, t0, t1):
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{t0}", "-t", f"{t1 - t0}", "-i", SRC,
                                   "-filter_complex", vf(), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE)
        self.t0 = t0; self.idx = -1; self.cur = None
    def get(self, s):
        want = int(round((s - self.t0) * FPS))
        while self.idx < want:
            buf = self.p.stdout.read(FRAME_BYTES)
            if len(buf) < FRAME_BYTES: break
            self.cur = np.frombuffer(buf, np.uint8).reshape(STACK_H, SW, 3); self.idx += 1
        return self.cur

def compose(stack, kb, gain, zoom, canvas):
    A = stack[:A_ROWS[2]]
    B = stack[A_ROWS[2]:A_ROWS[2] + B_ROWS[2]].astype(np.float32)
    C = stack[A_ROWS[2] + B_ROWS[2]:].astype(np.float32)
    A = zoom_box(np.ascontiguousarray(A), zoom).astype(np.float32)
    x0 = -2
    def put(img, y, k):
        if k <= 0.003: return
        h = img.shape[0]
        canvas[y:y + h, 0:W] += img[:, 2:2 + W] * (k * gain)
    put(A, A_Y, 1.0)
    # fade the bottom of the keyboard crop
    fade = np.ones((B.shape[0], 1, 1), np.float32)
    n = 90
    fade[-n:, 0, 0] = np.linspace(1, 0, n)
    put(B * fade, B_Y, kb)
    put(C, C_Y, 1 - kb)

def main():
    music = sys.argv[1]; outp = sys.argv[2]
    if "--timeline" in sys.argv:
        for m in MAPS:
            p = m["piece"]
            print(f"piece src {p['s0']}-{p['s1']} -> out {m['t0']:.2f}-{m['t0'] + m['cum'][-1]:.2f} ({m['cum'][-1]:.2f}s)")
        print(f"hook 0-{HOOK_D}, screens end {T_SCREEN_END:.2f}, freeze {FREEZE}, D={D:.2f}")
        for c in cap_windows() + cta_windows(): print(c[0], f"{c[1]:.2f}-{c[2]:.2f}")
        return
    hook_stack = one_frame(36.2)
    rd = None
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if music != "none":
        cmd += ["-i", music]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS)]
    if music != "none":
        cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest"]
    cmd += ["-movflags", "+faststart", outp]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(round(D * FPS))
    readers = {}
    caps = cap_windows(); ctas = cta_windows()
    for k in range(n):
        t = k / FPS
        canvas = np.full((H, W, 3), 13.0, np.float32)
        s, pi = src_at(t)
        if pi == -1:
            stack = hook_stack; kb = 0.0
        else:
            if pi not in readers:
                for r in readers.values(): r.p.kill()
                readers.clear()
                if pi < 3:
                    pc = PIECES[pi]; readers[pi] = Reader(pc["s0"], pc["s1"] + 0.2)
                else:
                    readers[pi] = None
            if pi == 3:
                stack = last_stack
            else:
                stack = readers[pi].get(s)
                last_stack = stack
            kb = kb_weight(s)
        gain = 1.0 if pi == -1 else dip_gain(t)
        # screen fades with final fade
        gain *= 1.0 if t < D - FINAL_FADE else 1 - sstep((t - (D - FINAL_FADE)) / FINAL_FADE)
        compose(stack, kb, gain, zoom_at(t), canvas)
        if t < HOOK_D:
            hook_layer(canvas, t)
        else:
            for lines, a_, b_, sz in caps:
                al, dr = eased_alpha(t, a_, b_)
                draw_text_block(canvas, lines, sz, 330, al, dr)
            for lines, a_, b_, sz in ctas:
                al, dr = eased_alpha(t, a_, b_, 0.45, 0.3)
                if b_ == D: al *= 1.0
                draw_text_block(canvas, lines, sz, 330, al * (1.0 if t < D - FINAL_FADE else 1 - sstep((t - (D - FINAL_FADE)) / FINAL_FADE)), dr)
        enc.stdin.write(np.clip(canvas, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()
    for r in readers.values():
        if r: r.p.kill()
    json.dump({"D": D}, open(f"{HERE}/cues92.json", "w"))
    print("done", D)

if __name__ == "__main__":
    main()
