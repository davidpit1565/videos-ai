#!/usr/bin/env python3
"""ep91 final8: PURE MEME. A calm face + 'Me with Claude' + one small line / B stressed face + 'Me with ChatGPT' + one small line / C CTA + both faces.
No checklist, no steps, no orange, no asterisk, no lime ring. The picture follows narration91c (cues91c.json). usage: build91_final8.py <out.mp4> | --still t out.png | --timeline | --standin out.html"""
import sys, os, subprocess, numpy as np
os.environ.setdefault("CUES", os.path.dirname(os.path.abspath(__file__)) + "/voice/cues91c.json")
from PIL import Image, ImageDraw
import build91_final7 as b
from build91_final7 import (W, H, FPS, BASE, INK, WHITE, ss, wordt, tl, text_layer, rrect, paste, fnt, FB, FK, FX, PILL_C, PADC, PWC, PILL_G, PADG, PWG, PIX, s2, s3)
L = b.L
D = round(wordt(3, "everything", True) + 1.0, 2)
TA1 = s2 - 0.10; TB0 = TA1 + 0.15            # A out, B in (dip, no overlap)
TB1 = s3 - 0.10; TC0 = TB1 + 0.15
FWD, FHD = 820, 674
def rface(path, box, w, h, r=40, bw=4):
    im = Image.open(path).convert("RGB").crop(box).resize((w, h), Image.LANCZOS); S = 4
    m = Image.new("L", (w * S, h * S), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w * S - 1, h * S - 1), r * S, fill=255); m = m.resize((w, h), Image.LANCZOS)
    o = Image.new("RGBA", (w + 2 * bw, h + 2 * bw), (0, 0, 0, 0)); rm = Image.new("L", ((w + 2 * bw) * S, (h + 2 * bw) * S), 0)
    ImageDraw.Draw(rm).rounded_rectangle((0, 0, (w + 2 * bw) * S - 1, (h + 2 * bw) * S - 1), (r + bw) * S, fill=255)
    o.paste(Image.new("RGBA", o.size, INK + (255,)), (0, 0), rm.resize(o.size, Image.LANCZOS)); o.paste(im, (bw, bw), m); return o
SRC_C = Image.open("/tmp/ep91v5/w_claude.png").convert("RGB"); SRC_G = Image.open("/tmp/ep91v5/w_gpt.png").convert("RGB")
def face_push(src, k, w, h, r=40, bw=4):
    """slow push-in INSIDE the frame (crop window shrinks 0..4%): smooth, no scaling of the card itself"""
    sw, sh = src.size; z = 1 - 0.08 * k; cw, ch = sw * z, sh * z; x0 = (sw - cw) * 0.3; y0 = (sh - ch) * 0.5
    im = src.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.LANCZOS); S = 4
    m = Image.new("L", (w * S, h * S), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w * S - 1, h * S - 1), r * S, fill=255); m = m.resize((w, h), Image.LANCZOS)
    o = Image.new("RGBA", (w + 2 * bw, h + 2 * bw), (0, 0, 0, 0)); rm = Image.new("L", ((w + 2 * bw) * S, (h + 2 * bw) * S), 0)
    ImageDraw.Draw(rm).rounded_rectangle((0, 0, (w + 2 * bw) * S - 1, (h + 2 * bw) * S - 1), (r + bw) * S, fill=255)
    o.paste(Image.new("RGBA", o.size, INK + (255,)), (0, 0), rm.resize(o.size, Image.LANCZOS)); o.paste(im, (bw, bw), m); return o
fl1 = fnt(FB, 60); fl2 = fnt(FB, 54)
LN_A = [("Do this → Done.", fl1)]
LN_B = [("Do this →", fl2), ("47 steps, error, try again...", fl2)]
CTA = [["Send", "this", "to"], ["the", "friend", "who"], ["overcomplicates"], ["everything."]]
fc = fnt(FK, 96); CTA_LH = 122; CTA_Y0 = 288
FW, FH = 440, 420
SRC_C2 = SRC_C; SRC_G2 = SRC_G
FACE_C2 = face_push(SRC_C, 0, FW, FH); FACE_G2 = face_push(SRC_G, 0, FW, FH)
FACE_Y = 412; LINE_Y = 1104
def scene(canvas, t, tin, tout, pill, ppad, pw, src, lines, tline):
    a = ss((t - tin) / 0.15) * (1 - ss((t - (tout - 0.15)) / 0.15))
    if a <= 0.003: return
    k = ss((t - tin) / max(0.5, tout - tin)); dy = -18 * k
    paste(canvas, pill, (W - pw) / 2 - ppad, 290 - ppad + dy, a)
    fi = face_push(src, k, FWD, FHD); paste(canvas, fi, (W - fi.width) / 2, FACE_Y + dy, a)
    la = a * ss((t - tline) / 0.2)
    for j, (txt, f) in enumerate(lines): paste(canvas, text_layer(txt, f, INK), (W - tl(txt, f)) / 2 - 4, LINE_Y + j * 66 + dy, la)
def frame(k):
    t = k / FPS
    canvas = np.ones((H, W, 3), np.float32) * np.array(BASE, np.float32)
    scene(canvas, t, -1.0, TA1, PILL_C, PADC, PWC, SRC_C, LN_A, 0.25)
    scene(canvas, t, TB0, TB1, PILL_G, PADG, PWG, SRC_G, LN_B, TB0 + 0.45)
    in3 = ss((t - TC0) / 0.15)
    if in3 > 0.003:
        paste(canvas, FACE_C2, 65, 812 + 12 * (1 - in3), in3); paste(canvas, FACE_G2, 1015 - FACE_G2.width, 812 + 12 * (1 - in3), in3)
        times = {"send": wordt(3, "send"), "this": wordt(3, "this"), "to": wordt(3, "to"), "the": wordt(3, "the"), "friend": wordt(3, "friend"), "who": wordt(3, "who"), "overcomplicates": wordt(3, "over"), "everything.": wordt(3, "everything")}
        for li, row in enumerate(CTA):
            tot = sum(tl(w, fc) for w in row) + (len(row) - 1) * 28; x = (W - tot) / 2; y = CTA_Y0 + li * CTA_LH
            for w in row:
                tw_ = tl(w, fc); tin = max(times[w.lower()] - 0.05, TC0 + 0.1); a = ss((t - tin) / 0.12)
                if w.lower() == "overcomplicates":
                    hb = Image.new("RGBA", (int(tw_) + 44, 112), (0, 0, 0, 0)); ImageDraw.Draw(hb).rounded_rectangle((0, 0, hb.width - 1, 111), 22, fill=INK + (255,))
                    paste(canvas, hb, x - 22, y + 12, in3 * a); paste(canvas, text_layer(w, fc, WHITE), x - 4, y + 4 * (1 - a), a * in3)
                else: paste(canvas, text_layer(w, fc, INK), x - 4, y + 4 * (1 - a), a * in3)
                x += tw_ + 28
    return np.clip(canvas, 0, 255).astype(np.uint8)
TXT = []
def collect():
    f = lambda t, x, y, s, t0, t1: TXT.append((t, int(x), int(y), s, round(t0, 2), round(t1, 2)))
    f("Me with Claude", (W - PWC) / 2 + 44, 290 + 17, 66, 0, TA1)
    f("Me with ChatGPT", (W - PWG) / 2 + 44 + 88, 290 + 17, 66, TB0, TB1)
    for txt, fo in LN_A: f(txt, (W - tl(txt, fo)) / 2, LINE_Y, 60, 0.45, TA1 - 0.15)
    for j, (txt, fo) in enumerate(LN_B): f(txt, (W - tl(txt, fo)) / 2, LINE_Y + j * 66, 54, TB0 + 0.65, TB1 - 0.15)
    for li, row in enumerate(CTA):
        tot = sum(tl(w, fc) for w in row) + (len(row) - 1) * 28
        f(" ".join(row), (W - tot) / 2, CTA_Y0 + li * CTA_LH + 12, 96, wordt(3, "send") + 0.3 + 0.3 * li, D)
if __name__ == "__main__":
    if "--timeline" in sys.argv: print(f"D={D} TA1={TA1:.2f} TB0={TB0:.2f} TB1={TB1:.2f} TC0={TC0:.2f}"); sys.exit()
    if "--still" in sys.argv:
        i = sys.argv.index("--still"); Image.fromarray(frame(int(round(float(sys.argv[i + 1]) * FPS)))).save(sys.argv[i + 2]); sys.exit()
    if "--standin" in sys.argv:
        collect(); out = sys.argv[sys.argv.index("--standin") + 1]
        divs = "\n".join(f'<div class="clip t" data-start="{a}" data-duration="{round(max(0.1, c - a), 2)}" style="left:{x}px;top:{y}px;font-size:{s}px;color:#18181c">{t.replace("&", "&amp;")}</div>' for t, x, y, s, a, c in TXT)
        open(out, "w").write(f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=1080, height=1920">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>html,body{{margin:0;width:1080px;height:1920px;background:#f5f1e9;overflow:hidden;font-family:Inter,Helvetica,Arial,sans-serif;font-weight:900}}.t{{position:absolute;white-space:nowrap;line-height:1.08;letter-spacing:-.03em}}</style></head><body>
<!-- text-only stand-in for ep91 final8 (positions from build91_final8.py) -->
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
{divs}
</div><script>window.__timelines={{main:gsap.timeline({{paused:true}}).to({{}},{{duration:{D}}})}};</script></body></html>'''); sys.exit()
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), sys.argv[1]], stdin=subprocess.PIPE)
    for k in range(int(round(D * FPS))): enc.stdin.write(frame(k).tobytes())
    enc.stdin.close(); enc.wait(); print("done", D)
