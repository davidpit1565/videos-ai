#!/usr/bin/env python3
"""ep91 final5: clean DRAWN panels (no zoom, no crop of the AI art, nothing scaled up) for the 'Me with Claude / Me with ChatGPT' joke.
Meta AI fixes: ChatGPT side = 3 big steps, Claude side = its 5 lines in big dark text, one CTA only (the last), no zoom, 100 px margins.
Real logos only (Claude mark #D97757, ChatGPT mark from video/ep86/assets). Two small face crops from David's own art (native resolution, circle mask).
usage: build91_final5.py <out.mp4> | --still t out.png | --timeline | --standin out.html"""
import sys, os, io, json, re, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
try:
    import cairosvg
except ImportError:
    cairosvg = None   # the mix script (py3.11 env) only needs the timings: logos come from the cache written by the system-python run
HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
CP = os.environ.get("CUES", HERE + "/voice/cues91c.json")
cues = json.load(open(CP)); L = cues["lines"]
BASE = (245, 241, 233); INK = (24, 24, 28); WHITE = (255, 255, 255); ORG = (217, 119, 87); TEAL = (16, 163, 127); TEAL2 = (70, 226, 186)
FB = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"; FK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"; FX = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
def ss(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
def wordt(n, key, end=False):
    for w in L[n - 1]["words"]:
        if key in re.sub(r"[^a-z]", "", w[0].lower()): return w[-1] if end else w[-2]
    raise KeyError((n, key))
s2 = L[1]["start"]; s3 = L[2]["start"]
tCl_end = L[0]["end"]
T_SW1 = max(s2 - 0.1, tCl_end + 0.05)                 # Claude scene starts leaving
T_IN2 = T_SW1 + 0.30                                   # ChatGPT scene starts arriving
T_SW2 = s3 - 0.25                                      # ChatGPT scene leaves
T_IN3 = T_SW2 + 0.30
D = round(wordt(3, "everything", True) + 1.25, 2)

def fnt(p, s): return ImageFont.truetype(p, s)
def tl(txt, f): return f.getlength(txt)
def rgba(size): return Image.new("RGBA", size, (0, 0, 0, 0))
def rrect(size, r, fill, outline=None, width=0, shadow=0):
    pad = shadow * 3 if shadow else 0
    im = rgba((size[0] + 2 * pad, size[1] + 2 * pad))
    if shadow:
        sh = rgba(im.size); ImageDraw.Draw(sh).rounded_rectangle((pad, pad + shadow, pad + size[0], pad + size[1] + shadow), r, fill=(30, 30, 40, 55))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(shadow)))
    ImageDraw.Draw(im).rounded_rectangle((pad, pad, pad + size[0] - 1, pad + size[1] - 1), r, fill=fill, outline=outline, width=width)
    return im, pad
def text_layer(txt, f, col):
    im = rgba((int(tl(txt, f)) + 8, int(f.size * 1.4))); ImageDraw.Draw(im).text((4, int(f.size * 0.12)), txt, font=f, fill=col + (255,)); return im
def logo(svg, size, color=None):
    data = open(svg).read()
    if color: data = data.replace("<path", f"<path fill='{color}'", 1) if "fill=" not in data.split(">")[0] else data
    cache = f"/tmp/ep91v5/logo_{os.path.basename(svg)}_{size}_{color or 'x'}.png".replace('#', '')
    if cairosvg is None: return Image.open(cache).convert("RGBA")
    png = cairosvg.svg2png(bytestring=data.encode(), output_width=size, output_height=size)
    open(cache, "wb").write(png)
    return Image.open(io.BytesIO(png)).convert("RGBA")
def face(path, box, d, ring):
    im = Image.open(path).convert("RGB").crop(box).resize((d * 2, d * 2), Image.LANCZOS) if False else Image.open(path).convert("RGB").crop(box)
    im = im.resize((d, d), Image.LANCZOS); m = Image.new("L", (d * 4, d * 4), 0); ImageDraw.Draw(m).ellipse((0, 0, d * 4 - 1, d * 4 - 1), fill=255); m = m.resize((d, d), Image.LANCZOS)
    o = rgba((d + 16, d + 16)); rm = Image.new("L", (d * 4 + 64, d * 4 + 64), 0); ImageDraw.Draw(rm).ellipse((0, 0, d * 4 + 63, d * 4 + 63), fill=255); rm = rm.resize((d + 16, d + 16), Image.LANCZOS)
    o.paste(Image.new("RGBA", o.size, ring + (255,)), (0, 0), rm); o.paste(im, (8, 8), m); return o
def paste(canvas, im, x, y, a=1.0):
    if a <= 0.003: return
    x, y = int(round(x)), int(round(y)); x0, y0 = max(0, x), max(0, y); x1, y1 = min(W, x + im.width), min(H, y + im.height)
    if x1 <= x0 or y1 <= y0: return
    sub = np.asarray(im.crop((x0 - x, y0 - y, x1 - x, y1 - y)), np.float32); al = sub[..., 3:4] / 255 * a
    reg = canvas[y0:y1, x0:x1]; reg[:] = reg * (1 - al) + sub[..., :3] * al

TXT = []   # (text, left, top, size, t0, t1)  -> text-only stand-in for safe_check
def reg_text(t, x, y, sz, t0, t1): TXT.append((t, int(x), int(y), sz, round(t0, 2), round(t1, 2)))

# ---------- static layers ----------
FA = "/home/user/videos-ai/channel/memes-2026-11-10/david-chatgpt/meme3-9x16-gemini.jpg"
claude_logo = logo("/home/user/videos-ai/video/ep86/assets/claude.svg", 70)
gpt_logo_w = logo("/home/user/videos-ai/video/ep86/assets/chatgpt.svg", 70, "#ffffff")
def pill(lbl_a, lbl_b, colb, lg):
    f = fnt(FK, 62); wA = tl(lbl_a, f); wB = tl(lbl_b, f); pw = int(70 + 22 + wA + wB + 90); ph = 104
    im, pad = rrect((pw, ph), 52, INK + (255,), shadow=8)
    im.alpha_composite(lg, (pad + 34, pad + 17)); d = ImageDraw.Draw(im)
    x = pad + 34 + 70 + 22; d.text((x, pad + 14), lbl_a, font=f, fill=WHITE + (255,)); d.text((x + wA, pad + 14), lbl_b, font=f, fill=colb + (255,)); return im, pad, pw
PILL_C, PADC, PWC = pill("Me with ", "Claude", ORG, claude_logo)
PILL_G, PADG, PWG = pill("Me with ", "ChatGPT", TEAL2, gpt_logo_w)
FACE_C = face("/tmp/ep91v5/face_claude.png", (0, 0, 470, 470), 190, ORG)
FACE_G = face("/tmp/ep91v5/face_gpt.png", (40, 110, 360, 430), 190, TEAL)
FACE_C2 = face("/tmp/ep91v5/face_claude.png", (0, 0, 470, 470), 270, ORG)
FACE_G2 = face("/tmp/ep91v5/face_gpt.png", (40, 110, 360, 430), 270, TEAL)

# Claude list
ROWS = ["Listen", "Understand", "Explain simply", "Give clear steps", "Find the best solution"]
CARD_C, CPAD = rrect((880, 590), 40, WHITE + (255,), shadow=10)
fl = fnt(FB, 62)
def check(done_col):
    im = rgba((64, 64)); d = ImageDraw.Draw(im); d.rounded_rectangle((0, 0, 63, 63), 18, fill=done_col + (255,))
    d.line([(15, 33), (27, 45), (49, 20)], fill=WHITE + (255,), width=8, joint="curve"); return im
CHK = check(ORG); BOX = rgba((64, 64)); ImageDraw.Draw(BOX).rounded_rectangle((2, 2, 61, 61), 18, outline=(205, 198, 188, 255), width=5)
ROW_Y0 = 430 + 22; ROW_H = 109
ROW_T = [0.20 + i * 0.40 for i in range(5)]           # checks tick in one by one; the words are all visible from frame 0
# ChatGPT scene
NOTE_W, NOTE_H = 700, 176
note, npad = rrect((NOTE_W, NOTE_H), 14, (255, 244, 196, 255), shadow=8)
nd = ImageDraw.Draw(note); nd.text((npad + 34, npad + 14), "What I asked:", font=fnt(FX, 44), fill=(70, 60, 30, 255))
nd.rounded_rectangle((npad + 34, npad + 90, npad + 34 + 50, npad + 90 + 50), 12, outline=(70, 60, 30, 255), width=5)
nd.line([(npad + 34 + 10, npad + 90 + 26), (npad + 34 + 21, npad + 90 + 38), (npad + 34 + 40, npad + 90 + 12)], fill=(70, 60, 30, 255), width=7)
nd.text((npad + 104, npad + 88), "Do this simple thing", font=fnt(FX, 54), fill=(40, 34, 16, 255))
NOTE = note.rotate(2.2, resample=Image.BICUBIC, expand=True)
STEPS = ["Set up environment", "Configure everything", "Test and debug"]
fs = fnt(FB, 60)
def step_img(i, txt):
    im, pad = rrect((880, 112), 30, WHITE + (255,), outline=TEAL + (255,), width=5, shadow=8)
    d = ImageDraw.Draw(im); d.ellipse((pad + 28, pad + 22, pad + 28 + 68, pad + 22 + 68), fill=TEAL + (255,))
    nf = fnt(FK, 46); nb = str(i + 1); d.text((pad + 28 + 34 - tl(nb, nf) / 2, pad + 22 + 6), nb, font=nf, fill=WHITE + (255,))
    d.text((pad + 124, pad + 19), txt, font=fs, fill=INK + (255,)); return im, pad
STEP_IM = [step_img(i, t) for i, t in enumerate(STEPS)]
STEP_Y = [652, 780, 908]
ARROW = rgba((40, 28)); ImageDraw.Draw(ARROW).polygon([(4, 4), (36, 4), (20, 24)], fill=TEAL + (255,))
# CTA
CTA = [["Send", "this", "to"], ["the", "friend", "who"], ["overcomplicates"], ["everything."]]
fc = fnt(FK, 94); CTA_LH = 128; CTA_Y0 = 345

def seg(t, a, b, fi=0.3, fo=0.25): return ss((t - a) / fi) * (1 - ss((t - (b - fo)) / fo))

def frame(k):
    t = k / FPS
    canvas = np.ones((H, W, 3), np.float32) * np.array(BASE, np.float32)
    # ===== scene 1: Claude =====
    a1 = 1 - ss((t - T_SW1) / 0.30); r1 = ss((t - T_SW1) / 0.30)
    if a1 > 0.003:
        dy = -36 * r1 - 18 * ss(t / 2.6); br = 1 + 0.03 * np.sin(t * 1.5)
        paste(canvas, PILL_C, (W - PWC) / 2 - PADC, 300 - PADC + dy, a1)
        paste(canvas, CARD_C, 100 - CPAD, 430 - CPAD + dy, a1)
        for i, txt in enumerate(ROWS):
            y = ROW_Y0 + i * ROW_H + dy; ck = ss((t - ROW_T[i]) / 0.28)
            paste(canvas, BOX, 140, y + 14, a1); paste(canvas, CHK, 140, y + 14 - 4 * (1 - ck), a1 * ck)
            paste(canvas, text_layer(txt, fl, INK), 232, y + 6, a1)
        fd = FACE_C.resize((int(176 * br), int(176 * br)), Image.LANCZOS); paste(canvas, fd, 540 - fd.width / 2, 1142 - fd.height / 2 + dy, a1)
    # ===== scene 2: ChatGPT =====
    in2 = ss((t - T_IN2) / 0.35); out2 = 1 - ss((t - T_SW2) / 0.28); a2 = in2 * out2
    if a2 > 0.003:
        dy = 40 * (1 - in2) - 36 * (1 - out2); br = 1 + 0.02 * np.sin((t - T_IN2) * 1.4)
        paste(canvas, PILL_G, (W - PWG) / 2 - PADG, 300 - PADG + dy, a2)
        n2 = ss((t - (wordt(2, "chat") - 0.05)) / 0.4)
        paste(canvas, NOTE, (W - NOTE.width) / 2, 414 + dy - 6 * (1 - n2), a2 * n2)
        for i in range(3):
            tin = [wordt(2, "its"), wordt(2, "more") , wordt(2, "tangled")][i] - 0.1
            si = ss((t - tin) / 0.38); im, pad = STEP_IM[i]
            paste(canvas, im, 100 - pad + 50 * (1 - si) * (-1 if i % 2 else 1), STEP_Y[i] - pad + dy, a2 * si)
            if i < 2: paste(canvas, ARROW, 520, STEP_Y[i] + 112 + 0 + dy, a2 * si)
        fd = FACE_G.resize((int(176 * br), int(176 * br)), Image.LANCZOS); paste(canvas, fd, 540 - fd.width / 2, 1142 - fd.height / 2 + dy, a2 * n2)
    # ===== scene 3: CTA =====
    in3 = ss((t - T_IN3) / 0.3)
    if in3 > 0.003:
        paste(canvas, FACE_C2, 330 - FACE_C2.width / 2, 1090 - FACE_C2.height / 2 + 30 * (1 - in3), in3)
        paste(canvas, FACE_G2, 750 - FACE_G2.width / 2, 1090 - FACE_G2.height / 2 + 30 * (1 - in3), in3)
        times = {"send": wordt(3, "send"), "this": wordt(3, "this"), "to": wordt(3, "to"), "the": wordt(3, "the"), "friend": wordt(3, "friend"), "who": wordt(3, "who"),
                 "overcomplicates": wordt(3, "over"), "everything.": wordt(3, "everything")}
        tOver1 = wordt(3, "over", True)
        for li, row in enumerate(CTA):
            tot = sum(tl(w, fc) for w in row) + (len(row) - 1) * 26; x = (W - tot) / 2; y = CTA_Y0 + li * CTA_LH
            for w in row:
                tw_ = tl(w, fc); tin = times[w.lower()] - 0.05; a = ss((t - tin) / 0.25)
                if w.lower() == "overcomplicates":
                    hb = rgba((int(tw_) + 40, 112)); ImageDraw.Draw(hb).rounded_rectangle((0, 0, hb.width - 1, 111), 22, fill=ORG + (255,))
                    hp = ss((t - tin) / 0.3)
                    paste(canvas, hb, x - 20, y + 16, in3 * hp)
                    paste(canvas, text_layer(w, fc, WHITE), x - 4, y + 4 * (1 - a), a * in3)
                else:
                    paste(canvas, text_layer(w, fc, INK), x - 4, y + 4 * (1 - a), a * in3)
                x += tw_ + 26
    return np.clip(canvas, 0, 255).astype(np.uint8)

def collect():
    for i, txt in enumerate(ROWS): reg_text(txt, 232, ROW_Y0 + i * ROW_H + 6, 62, 0, T_SW1 + .3)
    reg_text("Me with Claude", int((W - PWC) / 2 + 92), 314, 62, 0, T_SW1 + .3)
    reg_text("Me with ChatGPT", int((W - PWG) / 2 + 92), 314, 62, T_IN2 + .35, T_SW2 + .28)
    nl = (W - NOTE.width) / 2
    reg_text("What I asked:", int(nl + npad + 34), 414 + npad + 14, 44, wordt(2, "chat") + .4, T_SW2)
    reg_text("Do this simple thing", int(nl + npad + 104), 414 + npad + 80, 54, wordt(2, "chat") + .4, T_SW2)
    for i, t_ in enumerate(STEPS): reg_text(f"{i+1}  {t_}", 224, STEP_Y[i] + 20, 60, wordt(2, ["its", "more", "tangled"][i]) + .3, T_SW2)
    for li, row in enumerate(CTA):
        tot = sum(tl(w, fc) for w in row) + (len(row) - 1) * 26
        reg_text(" ".join(row), int((W - tot) / 2), CTA_Y0 + li * CTA_LH + 10, 94, wordt(3, "send") + 0.3 + 0.3 * li, D)
if __name__ == "__main__":
    if "--timeline" in sys.argv:
        print(f"D={D} s2={s2:.2f} T_SW1={T_SW1:.2f} T_IN2={T_IN2:.2f} T_SW2={T_SW2:.2f} T_IN3={T_IN3:.2f} s3={s3:.2f}"); sys.exit()
    if "--still" in sys.argv:
        i = sys.argv.index("--still"); Image.fromarray(frame(int(round(float(sys.argv[i + 1]) * FPS)))).save(sys.argv[i + 2]); sys.exit()
    if "--standin" in sys.argv:
        collect(); out = sys.argv[sys.argv.index("--standin") + 1]
        divs = "\n".join(f'<div class="clip t" data-start="{a}" data-duration="{round(max(0.1, b - a), 2)}" style="left:{x}px;top:{y}px;font-size:{s}px;color:#18181c">{t.replace("&", "&amp;")}</div>' for t, x, y, s, a, b in TXT)
        open(out, "w").write(f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=1080, height=1920">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>html,body{{margin:0;width:1080px;height:1920px;background:#f5f1e9;overflow:hidden;font-family:Inter,Helvetica,Arial,sans-serif;font-weight:900}}.t{{position:absolute;white-space:nowrap;line-height:1.08;letter-spacing:-.03em}}</style></head><body>
<!-- text-only stand-in for ep91 final5 (positions from build91_final5.py); the reel is drawn by build91_final5.py -->
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
{divs}
</div><script>window.__timelines={{main:gsap.timeline({{paused:true}}).to({{}},{{duration:{D}}})}};</script></body></html>'''); print("standin", len(TXT)); sys.exit()
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                            "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), sys.argv[1]], stdin=subprocess.PIPE)
    for k in range(int(round(D * FPS))): enc.stdin.write(frame(k).tobytes())
    enc.stdin.close(); enc.wait(); print("done", D)
