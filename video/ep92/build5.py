#!/usr/bin/env python3
"""ep92 final5: same three real sentences, words identical to the real recording, RE-SET in large heavy type (not crops) so they fill the safe box x65-1015 y269-1248.
Only the crying emoji and the real ChatGPT icon are real pixels. Usage: build5.py <out.mp4> | --frame T out.png | --timeline"""
import sys, subprocess, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "/home/user/videos-ai/video/ep92")
_a = sys.argv[1:]
sys.argv = ["x", "/home/user/videos-ai/video/ep92/voice/cues.json"]
import build92 as b
sys.argv = ["x"] + _a
W, H = 1080, 1920; FPS = 30
CUES = json.load(open("/tmp/e4/v/cues4.json")); L = {l["n"]: l for l in CUES["lines"]}; D = CUES["D"]
def sstep(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)
def ease(x):
    x = min(1.0, max(0.0, x)); return x * x * x * (x * (6 * x - 15) + 10)
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"
SRC = "/root/.claude/uploads/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/739398dd-ScreenRecording_11-11-2026_05-10-31_1.mp4"
def native(t):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", SRC, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    return b.LUT[np.frombuffer(p.stdout, np.uint8).reshape(2622, 1206, 3)]
F13 = native(13.9)
EMOJI = Image.fromarray(F13[1984:2062, 856:926]).convert("RGB")      # real crying emoji (Apple), from the real final frame
def wlen(f, s): return f.getlength(s)
def layout(lines, size, cy, lh=1.12, maxw=None):
    """lines = list of list of words -> list of dict(word, x, y, img(L), idx)"""
    f = ImageFont.truetype(FONT, size); sp = wlen(f, " ") * 0.9; out = []; idx = 0
    ys = [cy + (i - (len(lines) - 1) / 2) * size * lh for i in range(len(lines))]
    for i, ln in enumerate(lines):
        ws = [wlen(f, w) for w in ln]; tot = sum(ws) + sp * (len(ln) - 1); x = (W - tot) / 2
        for w, wl in zip(ln, ws):
            bb = f.getbbox(w); pad = 6
            im = Image.new("L", (int(wl) + 2 * pad, int(size * 1.4)), 0); ImageDraw.Draw(im).text((pad, 0), w, font=f, fill=255)
            out.append(dict(word=w, x=int(round(x - pad)), y=int(round(ys[i] - size * 0.7)), img=np.asarray(im, np.float32) / 255, idx=idx, line=i)); idx += 1; x += wl + sp
    return out, tot if False else None
def fit(lines, maxw, cap=999):
    f = ImageFont.truetype(FONT, 100); sp = wlen(f, " ") * 0.9
    wmax = max(sum(wlen(f, w) for w in ln) + sp * (len(ln) - 1) for ln in lines); return min(cap, int(100 * maxw / wmax))
MAXW = 900
# ---- text content: exactly the real words ----
Q = [["I'm", "about"], ["to", "delete", "you."], ["You", "have", "10"], ["seconds", "to", "convince"], ["me", "not", "to."]]
T2L = [["Don't", "keep", "me"], ["because", "I'm"], ["an", "AI."], ["Keep", "me", "only"], ["if", "I", "make", "your"], ["life", "easier."]]
T3A = [["And", "if"], ["I", "fail?"]]
T3B = [["You've", "got"], ["your", "10", "seconds"], ["back."]]
ENDL = [["Send", "this"], ["to", "someone"], ["who", "talks", "to"], ["ChatGPT"], ["all", "day."]]
S2 = fit(T2L, MAXW); S3A = fit(T3A, MAXW, 200); S3B = fit(T3B, MAXW, 130); SQ = fit(Q, 850); SE = fit(ENDL, MAXW, 150)
W2 = L[2]["words"]; W3 = L[3]["words"]
s2, e2, s3, e3, s4, e4 = L[2]["start"], L[2]["end"], L[3]["start"], L[3]["end"], L[4]["start"], L[4]["end"]
# spoken word times: line 2 words index 2..17 ("It said," skipped), line 3 words 0..9, line 4 words
def wt(ws, i): return max(0, ws[i][1] - 0.04)
T2 = [wt(W2, i) for i in range(2, 18)]; T3a = [wt(W3, i) for i in range(0, 4)]; T3b = [wt(W3, i) for i in range(4, 10)]
B1_OUT = (T2[0] - 0.28, T2[0] + 0.05); B2_OUT = (e2 - 0.10, e2 + 0.07); B3_OUT = (e3 + 0.05, e3 + 0.30)
END_T = s4 - 0.02; HOLD_FROM = D - 1.0
def stagger_words(words, times):
    for w, t in zip(words, times): w["t"] = t
    return words
def place(lines, size, cy, times, lh=1.12):
    ws, _ = layout(lines, size, cy, lh); return stagger_words(ws, times)
# vertical layout inside the safe box 269..1248
C2 = place(T2L, S2, 758, T2, 1.14)
hA = int(2 * S3A * 1.02); hB = int(3 * S3B * 1.12); G3 = 80; top3 = int(758 - (hA + G3 + hB) / 2)
SA = place(T3A, S3A, top3 + hA / 2, T3a, 1.02)
SB = place(T3B, S3B, top3 + hA + G3 + hB / 2, T3b, 1.12)
EM_SZ = int(S3B * 0.95); EMO = EMOJI.resize((int(EMOJI.size[0] * EM_SZ / EMOJI.size[1]), EM_SZ), Image.LANCZOS)
_shift = (EMO.size[0] + 6) // 2
for w in SB:
    if w["line"] == 2: w["x"] -= _shift
back = SB[-1]; EM_X = back["x"] + back["img"].shape[1] + 4; EM_Y = back["y"] + int(S3B * 0.12)
# bubble
BUB_W, PADV = 940, 60; qh = int(SQ * 1.18) * len(Q) + 2 * PADV - 20
BADGE = 210; GAP = 70; top = int(758 - (BADGE + GAP + qh) / 2); BADGE_CY = top + BADGE // 2; BUB_TOP = top + BADGE + GAP
BUBL = Image.new("RGBA", (BUB_W, qh), (0, 0, 0, 0)); ImageDraw.Draw(BUBL).rounded_rectangle((0, 0, BUB_W - 1, qh - 1), radius=70, fill=(40, 28, 99, 255))
QW, _ = layout(Q, SQ, BUB_TOP + qh / 2 - 6, 1.18)
for w in QW: w['t'] = 0.0
# end card
EH = int(SE * 1.12) * len(ENDL); etop = int(758 - (170 + 44 + EH) / 2); E_BADGE_CY = etop + 85
EW = place(ENDL, SE, etop + 170 + 44 + EH / 2, [END_T + 0.2 + 0.09 * i for i in range(10)], 1.12)
def draw_words(canvas, ws, t, color=250.0, dur=0.22, rise=16):
    for w in ws:
        a = sstep((t - w["t"]) / dur)
        if a <= 0.002: continue
        im = w["img"]; h, wd = im.shape; y0 = int(round(w["y"] + (1 - a) * rise)); x0 = w["x"]
        if y0 < 0 or y0 + h > H or x0 < 0 or x0 + wd > W: continue
        reg = canvas[y0:y0 + h, x0:x0 + wd]; m = (im * a)[..., None]; reg[:] = reg * (1 - m) + color * m
def zoom(lay, z, cy):
    if abs(z - 1) < 1e-4: return lay
    aff = (1 / z, 0, 540 - 540 / z, 0, 1 / z, cy - cy / z)
    return np.asarray(Image.fromarray(np.clip(lay, 0, 255).astype(np.uint8)).transform((W, H), Image.AFFINE, aff, resample=Image.BICUBIC)).astype(np.float32)
def alpha_out(t, o): return 1 - sstep((t - o[0]) / (o[1] - o[0]))
def compose(t):
    canvas = np.zeros((H, W, 3), np.float32)
    a1 = alpha_out(t, B1_OUT)
    if a1 > 0.002:
        lay = np.zeros((H, W, 3), np.float32)
        bub = np.asarray(BUBL, np.float32); x0 = (W - BUB_W) // 2; reg = lay[BUB_TOP:BUB_TOP + qh, x0:x0 + BUB_W]; reg[:] = reg * (1 - bub[..., 3:4] / 255) + bub[..., :3] * bub[..., 3:4] / 255
        draw_words(lay, QW, 99, 250.0)
        b.add_badge(lay, 1.0, W / 2, BADGE_CY, BADGE)
        canvas += zoom(lay, 1 + 0.03 * ease(t / B1_OUT[1]), 758) * a1
    a2 = alpha_out(t, B2_OUT) * sstep((t - (T2[0] - 0.2)) / 0.2)
    if a2 > 0.002:
        lay = np.zeros((H, W, 3), np.float32); draw_words(lay, C2, t); canvas += zoom(lay, 1 + 0.03 * ease((t - T2[0]) / (e2 - T2[0])), 758) * a2
    a3 = alpha_out(t, B3_OUT)
    if a3 > 0.002 and t >= T3a[0]:
        lay = np.zeros((H, W, 3), np.float32); draw_words(lay, SA, t); draw_words(lay, SB, t)
        ea = sstep((t - T3b[-1]) / 0.25)
        if ea > 0.002:
            em = np.asarray(EMO, np.float32); h, wd = em.shape[:2]; reg = lay[EM_Y:EM_Y + h, EM_X:EM_X + wd]; reg[:] = reg * (1 - ea) + em * ea
        canvas += zoom(lay, 1 + 0.03 * ease((t - T3a[0]) / (e3 - T3a[0])), 758) * a3
    ea = sstep((t - END_T) / 0.45)
    if ea > 0.002:
        lay = np.zeros((H, W, 3), np.float32); b.add_badge(lay, 1.0, W / 2, E_BADGE_CY, 170)
        draw_words(lay, EW, t, rise=0)
        z = 1 + 0.025 * ease((min(t, HOLD_FROM) - END_T) / (HOLD_FROM - END_T)); canvas += zoom(lay, z, 758) * min(1.0, ea * 1.0 + (1 if t > END_T + 0.5 else 0))
    return np.clip(canvas, 0, 255)
def main():
    a = sys.argv[1:]
    if "--timeline" in a:
        print("D", D, "sizes q", SQ, "t2", S2, "t3a", S3A, "t3b", S3B, "end", SE, "bubble qh", qh, "top", top, "emoji", EM_X, EM_Y, EMO.size); return
    if "--frame" in a:
        i = a.index("--frame"); Image.fromarray(compose(float(a[i + 1])).astype(np.uint8)).save(a[i + 2]); return
    outp = [x for x in a if x.endswith(".mp4")][0]
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", outp], stdin=subprocess.PIPE)
    for k in range(int(round(D * FPS))): enc.stdin.write(compose(k / FPS).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait(); print("done", D)
if __name__ == "__main__": main()
