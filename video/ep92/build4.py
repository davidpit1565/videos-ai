#!/usr/bin/env python3
"""ep92 final4: three real sentences from the real recording, each as REAL pixel crops (no keyboard, no scroll), enlarged, cut at word gaps of the real lines.
Usage: build4.py <cues4.json> <out.mp4> | --frame T out.png | --timeline"""
import sys, subprocess, json
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/home/user/videos-ai/video/ep92")
_a = sys.argv[1:]
sys.argv = ["x", "/home/user/videos-ai/video/ep92/voice/cues.json"]
import build92 as b
sys.argv = ["x"] + _a
W, H = 1080, 1920; FPS = 30
CUES = json.load(open("/tmp/e4/v/cues4.json")); L = {l["n"]: l for l in CUES["lines"]}; D = CUES["D"]
def sstep(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)
def ease(x):  # smootherstep
    x = min(1.0, max(0.0, x)); return x * x * x * (x * (6 * x - 15) + 10)
SRC = "/root/.claude/uploads/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/739398dd-ScreenRecording_11-11-2026_05-10-31_1.mp4"
def native(t):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", SRC, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    return b.LUT[np.frombuffer(p.stdout, np.uint8).reshape(2622, 1206, 3)]
F9 = native(9.0); F13 = native(13.9)     # scroll 0 (question + first part of answer) / final static frame
def crop(F, x0, x1, y0, y1, scale):
    # name row is native y 786-839: no crop may touch it
    assert not (y0 < 845 and y1 > 780 and F is F9), "crop touches the name row"
    im = Image.fromarray(F[y0:y1, x0:x1]); return im.resize((int(round((x1 - x0) * scale)), int(round((y1 - y0) * scale))), Image.LANCZOS)
SC = 1.65
BUB = crop(F9, 360, 1160, 360, 700, 1.12)
C2 = [crop(F9, 46, 610, 896, 964, SC), crop(F9, 616, 1063, 896, 964, SC), crop(F9, 44, 363, 966, 1036, SC), crop(F9, 367, 734, 966, 1036, SC)]
C3 = [crop(F13, 44, 327, 1866, 1938, 2.15), crop(F13, 44, 423, 1982, 2062, 1.85), crop(F13, 427, 925, 1982, 2062, 1.85)]
W2 = L[2]["words"]; W3 = L[3]["words"]
def span(ws, i, j, lead=0.03): return ws[i][1] - lead, ws[j][2]
T2 = [span(W2, 2, 5), span(W2, 6, 10), span(W2, 11, 14), span(W2, 15, 17)]
T3 = [span(W3, 0, 3), span(W3, 4, 6), span(W3, 7, 9)]
s2, e2, s3, e3, s4, e4 = L[2]["start"], L[2]["end"], L[3]["start"], L[3]["end"], L[4]["start"], L[4]["end"]
B1_OUT = (T2[0][0] - 0.30, T2[0][0] + 0.05)
B2_OUT = (e2 - 0.12, e2 + 0.05)
B3_OUT = (e3 + 0.05, e3 + 0.30)
END_T = s4 - 0.02; HOLD_FROM = D - 1.0
def paste_wiped(canvas, im, cx, cy, t0, t1, feather=70):
    """paste a real-pixel crop centred at (cx,cy), revealed left->right between t0 and t1 with a soft edge; returns nothing"""
    return (im, cx, cy, t0, t1, feather)
def render_layer(items, t):
    lay = np.zeros((H, W, 3), np.float32)
    for im, cx, cy, t0, t1, fe in items:
        if t < t0 - 0.001: continue
        a = np.asarray(im, np.float32); h, w = a.shape[:2]; p = ease((t - t0) / max(0.05, t1 - t0))
        x = np.arange(w, dtype=np.float32); edge = p * (w + fe) - fe
        m = np.clip((edge + fe - x) / fe, 0, 1)[None, :, None] if p < 1 else np.ones((1, w, 1), np.float32)
        rise = (1 - sstep((t - t0) / 0.35)) * 8
        x0 = int(round(cx - w / 2)); y0 = int(round(cy - h / 2 + rise))
        lay[y0:y0 + h, x0:x0 + w] = np.maximum(lay[y0:y0 + h, x0:x0 + w], a * m)
    return lay
def zoom(lay, z, cy):
    if abs(z - 1) < 1e-4: return lay
    aff = (1 / z, 0, 540 - 540 / z, 0, 1 / z, cy - cy / z)
    return np.asarray(Image.fromarray(np.clip(lay, 0, 255).astype(np.uint8)).transform((W, H), Image.AFFINE, aff, resample=Image.BICUBIC)).astype(np.float32)
# ---- layout ----
BUB_CY = 860; BADGE_CY = 470
CY2 = [640, 775, 895, 1015]            # 4 chunk centres (y)
Y2 = [CY2[0] + 0, CY2[1] + 0, CY2[2] + 0, CY2[3] + 0]
def y_of(i, h_list, gap=34, top=560):
    ys = []; y = top
    for h in h_list: ys.append(y + h / 2); y += h + gap
    return ys
H2 = [im.size[1] for im in C2]; Y2 = y_of(0, H2, 30, 540)
IT2 = [(C2[i], 540, Y2[i], T2[i][0], T2[i][1] + 0.1, 70) for i in range(4)]
H3 = [im.size[1] for im in C3]
Y3a = 640; Y3 = [Y3a, Y3a + H3[0] / 2 + 90 + H3[1] / 2]; Y3.append(Y3[1] + H3[1] / 2 + 24 + H3[2] / 2)
IT3 = [(C3[i], 540, Y3[i], T3[i][0], T3[i][1] + 0.1, 70) for i in range(3)]
IT1 = [(BUB, 540, BUB_CY, 0, 0.01, 1)]
def cy_mid(ys, hs): return (ys[0] - hs[0] / 2 + ys[-1] + hs[-1] / 2) / 2
def alpha_out(t, o): return 1 - sstep((t - o[0]) / (o[1] - o[0]))
def compose(t):
    canvas = np.zeros((H, W, 3), np.float32)
    # beat 1: badge + question bubble (real), slow push
    a1 = alpha_out(t, B1_OUT)
    if a1 > 0.002:
        z = 1 + 0.035 * ease(t / (B1_OUT[1]))
        lay = render_layer(IT1, 99)
        b.add_badge(lay, 1.0, W / 2, BADGE_CY, 190)
        canvas += zoom(lay, z, 760) * a1
    # beat 2
    a2 = alpha_out(t, B2_OUT) * sstep((t - (T2[0][0] - 0.2)) / 0.2)
    if a2 > 0.002 and t >= T2[0][0] - 0.2:
        z = 1 + 0.03 * ease((t - T2[0][0]) / (e2 - T2[0][0])); lay = render_layer(IT2, t)
        canvas += zoom(lay, z, cy_mid(Y2, H2)) * a2
    # beat 3
    a3 = alpha_out(t, B3_OUT)
    if a3 > 0.002 and t >= T3[0][0]:
        z = 1 + 0.03 * ease((t - T3[0][0]) / (e3 - T3[0][0])); lay = render_layer(IT3, t)
        canvas += zoom(lay, z, cy_mid(Y3, H3)) * a3
    # end card: appears with line 4, slow drift, static for the last second
    ea = sstep((t - END_T) / 0.45)
    if ea > 0.002:
        z = 1 + 0.025 * ease((min(t, HOLD_FROM) - END_T) / (HOLD_FROM - END_T))
        lay = np.zeros((H, W, 3), np.float32); b.add_layer(lay, b.END_LAYER, 1.0); b.add_badge(lay, 1.0, W / 2, b.END_Y - 95)
        canvas += zoom(lay, z, 800) * ea
    return np.clip(canvas, 0, 255)
def main():
    a = sys.argv[1:]
    if "--timeline" in a:
        print("D", D, "B1 out", B1_OUT, "T2", [(round(x, 2), round(y, 2)) for x, y in T2], "B2 out", B2_OUT, "T3", [(round(x, 2), round(y, 2)) for x, y in T3], "B3 out", B3_OUT, "end", END_T, "hold", HOLD_FROM)
        print("Y2", Y2, "H2", H2, "Y3", Y3, "H3", H3, "sizes C2", [i.size for i in C2], "C3", [i.size for i in C3], "BUB", BUB.size); return
    if "--frame" in a:
        i = a.index("--frame"); Image.fromarray(compose(float(a[i + 1])).astype(np.uint8)).save(a[i + 2]); return
    outp = [x for x in a if x.endswith(".mp4")][0]
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", outp], stdin=subprocess.PIPE)
    for k in range(int(round(D * FPS))): enc.stdin.write(compose(k / FPS).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait(); print("done", D)
if __name__ == "__main__": main()
