#!/usr/bin/env python3
"""ep91 final7: clean DRAWN panels (no zoom, no crop of the AI art, nothing scaled up) for the 'Me with Claude / Me with ChatGPT' joke.
Meta AI fixes: ChatGPT side = 3 big steps, Claude side = its 5 lines in big dark text, one CTA only (the last), no zoom, 100 px margins.
Real logos only (Claude mark #D97757, ChatGPT mark from video/ep86/assets). Two small face crops from David's own art (native resolution, circle mask).
usage: build91_final7.py <out.mp4> | --still t out.png | --timeline | --standin out.html"""
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
BASE = (245, 241, 233); INK = (24, 24, 28); WHITE = (255, 255, 255); LIME = (190, 228, 64)   # no orange, no teal: black/neutral + ONE accent (lime)
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
T_STEPS = T_IN2 + 0.55                                 # all 3 steps together; visible until T_SW2 (>= 2 s)
D = round(wordt(3, "everything", True) + 1.4, 2)

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
def face(path, box, w, h, ring, r=46):
    im = Image.open(path).convert("RGB").crop(box).resize((w, h), Image.LANCZOS); S = 4
    m = Image.new("L", (w * S, h * S), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w * S - 1, h * S - 1), r * S, fill=255); m = m.resize((w, h), Image.LANCZOS)
    o = rgba((w + 16, h + 16)); rm = Image.new("L", ((w + 16) * S, (h + 16) * S), 0); ImageDraw.Draw(rm).rounded_rectangle((0, 0, (w + 16) * S - 1, (h + 16) * S - 1), (r + 8) * S, fill=255)
    o.paste(Image.new("RGBA", o.size, ring + (255,)), (0, 0), rm.resize((w + 16, h + 16), Image.LANCZOS)); o.paste(im, (8, 8), m); return o
def paste(canvas, im, x, y, a=1.0):
    if a <= 0.003: return
    x, y = int(round(x)), int(round(y)); x0, y0 = max(0, x), max(0, y); x1, y1 = min(W, x + im.width), min(H, y + im.height)
    if x1 <= x0 or y1 <= y0: return
    sub = np.asarray(im.crop((x0 - x, y0 - y, x1 - x, y1 - y)), np.float32); al = sub[..., 3:4] / 255 * a
    reg = canvas[y0:y1, x0:x1]; reg[:] = reg * (1 - al) + sub[..., :3] * al

TXT = []   # (text, left, top, size, t0, t1)  -> text-only stand-in for safe_check
def reg_text(t, x, y, sz, t0, t1): TXT.append((t, int(x), int(y), sz, round(t0, 2), round(t1, 2)))

# ---------- static layers ----------
gpt_logo_w = logo("/home/user/videos-ai/video/ep86/assets/chatgpt.svg", 66, "#ffffff")   # the ONLY brand mark in the reel; Claude is named in plain text
PIX = 65
def pill(lbl, lg):
    f = fnt(FK, 66); wl = tl(lbl, f); lw = (66 + 22) if lg else 0; pw = int(44 + lw + wl + 44); ph = 112
    im, pad = rrect((pw, ph), 56, INK + (255,), shadow=8); d = ImageDraw.Draw(im); x = pad + 44
    if lg: im.alpha_composite(lg, (x, pad + 23)); x += lw
    d.text((x, pad + 17), lbl, font=f, fill=WHITE + (255,)); return im, pad, pw
PILL_C, PADC, PWC = pill("Me with Claude", None)
PILL_G, PADG, PWG = pill("Me with ChatGPT", gpt_logo_w)
FS = 396   # large rounded-square faces next to the cards
FCL = "/tmp/ep91v5/face_claude2.png"; FGP = "/tmp/ep91v5/face_gpt2.png"
FACE_C = face(FCL, (0, 0, 520, 520), FS, FS, LIME); FACE_G = face(FGP, (0, 55, 373, 428), FS, FS, LIME)
FW, FH = 460, 440
FACE_C2 = face(FCL, (0, 0, 520, 480), FW, FH, LIME); FACE_G2 = face(FGP, (0, 30, 373, 30 + 353), FW, FH, LIME)
ROWS = [["Listen"], ["Understand"], ["Explain simply"], ["Give clear steps"], ["Find the best solution"]]
FS_L = 54; fl = fnt(FB, FS_L); RH = 72; LH2 = 0
CARD_H = 5 * RH + 26
CARD_C, CPAD = rrect((950, CARD_H), 40, WHITE + (255,), shadow=10)
CARD_Y = 404
FACE_Y = 820
def check(col):
    im = rgba((54, 54)); d = ImageDraw.Draw(im); d.rounded_rectangle((0, 0, 53, 53), 15, fill=col + (255,))
    d.line([(13, 28), (23, 38), (41, 17)], fill=WHITE + (255,), width=7, joint="curve"); return im
CHK = check(INK)
ROW_Y = [CARD_Y + 13 + i * RH for i in range(5)]
# ChatGPT scene starts arriving
T_SW2 = s3 - 0.25                                      # ChatGPT scene leaves
T_IN3 = T_SW2 + 0.30
T_STEPS = T_IN2 + 0.55                                 # all 3 steps together; visible until T_SW2 (>= 2 s)
D = round(wordt(3, "everything", True) + 1.4, 2)

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
def face(path, box, w, h, ring, r=46):
    im = Image.open(path).convert("RGB").crop(box).resize((w, h), Image.LANCZOS); S = 4
    m = Image.new("L", (w * S, h * S), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w * S - 1, h * S - 1), r * S, fill=255); m = m.resize((w, h), Image.LANCZOS)
    o = rgba((w + 16, h + 16)); rm = Image.new("L", ((w + 16) * S, (h + 16) * S), 0); ImageDraw.Draw(rm).rounded_rectangle((0, 0, (w + 16) * S - 1, (h + 16) * S - 1), (r + 8) * S, fill=255)
    o.paste(Image.new("RGBA", o.size, ring + (255,)), (0, 0), rm.resize((w + 16, h + 16), Image.LANCZOS)); o.paste(im, (8, 8), m); return o
def paste(canvas, im, x, y, a=1.0):
    if a <= 0.003: return
    x, y = int(round(x)), int(round(y)); x0, y0 = max(0, x), max(0, y); x1, y1 = min(W, x + im.width), min(H, y + im.height)
    if x1 <= x0 or y1 <= y0: return
    sub = np.asarray(im.crop((x0 - x, y0 - y, x1 - x, y1 - y)), np.float32); al = sub[..., 3:4] / 255 * a
    reg = canvas[y0:y1, x0:x1]; reg[:] = reg * (1 - al) + sub[..., :3] * al

TXT = []   # (text, left, top, size, t0, t1)  -> text-only stand-in for safe_check
def reg_text(t, x, y, sz, t0, t1): TXT.append((t, int(x), int(y), sz, round(t0, 2), round(t1, 2)))

# ---------- static layers ----------
gpt_logo_w = logo("/home/user/videos-ai/video/ep86/assets/chatgpt.svg", 66, "#ffffff")   # the ONLY brand mark in the reel; Claude is named in plain text
PIX = 65
def pill(lbl, lg):
    f = fnt(FK, 66); wl = tl(lbl, f); lw = (66 + 22) if lg else 0; pw = int(44 + lw + wl + 44); ph = 112
    im, pad = rrect((pw, ph), 56, INK + (255,), shadow=8); d = ImageDraw.Draw(im); x = pad + 44
    if lg: im.alpha_composite(lg, (x, pad + 23)); x += lw
    d.text((x, pad + 17), lbl, font=f, fill=WHITE + (255,)); return im, pad, pw
PILL_C, PADC, PWC = pill("Me with Claude", None)
PILL_G, PADG, PWG = pill("Me with ChatGPT", gpt_logo_w)
FS = 396   # large rounded-square faces next to the cards
FCL = "/tmp/ep91v5/face_claude2.png"; FGP = "/tmp/ep91v5/face_gpt2.png"
FACE_C = face(FCL, (0, 0, 520, 520), FS, FS, LIME); FACE_G = face(FGP, (0, 55, 373, 428), FS, FS, LIME)
FW, FH = 460, 440
FACE_C2 = face(FCL, (0, 0, 520, 480), FW, FH, LIME); FACE_G2 = face(FGP, (0, 30, 373, 30 + 353), FW, FH, LIME)
ROWS = [["Listen"], ["Understand"], ["Explain simply"], ["Give clear steps"], ["Find the best solution"]]
FS_L = 54; fl = fnt(FB, FS_L); RH = 72; LH2 = 0
CARD_H = 5 * RH + 26
CARD_C, CPAD = rrect((950, CARD_H), 40, WHITE + (255,), shadow=10)
CARD_Y = 404
FACE_Y = 820
def check(col):
    im = rgba((54, 54)); d = ImageDraw.Draw(im); d.rounded_rectangle((0, 0, 53, 53), 15, fill=col + (255,))
    d.line([(13, 28), (23, 38), (41, 17)], fill=WHITE + (255,), width=7, joint="curve"); return im
CHK = check(INK)
ROW_Y = []; yy = CARD_Y + 26
for r in ROWS: ROW_Y.append(yy); yy += RH + (LH2 if len(r) > 1 else 0)
ROW_T = [0.20 + i * 0.40 for i in range(5)]
# ChatGPT scene
NOTE_W, NOTE_H = 700, 132
note, npad = rrect((NOTE_W, NOTE_H), 14, (255, 244, 196, 255), shadow=6)
nd = ImageDraw.Draw(note); nd.text((npad + 30, npad + 8), "What I asked:", font=fnt(FX, 38), fill=(70, 60, 30, 255))
nd.rounded_rectangle((npad + 30, npad + 68, npad + 30 + 46, npad + 68 + 46), 11, outline=(70, 60, 30, 255), width=5)
nd.line([(npad + 30 + 9, npad + 68 + 25), (npad + 30 + 19, npad + 68 + 35), (npad + 30 + 37, npad + 68 + 11)], fill=(70, 60, 30, 255), width=6)
nd.text((npad + 92, npad + 62), "Do this simple thing", font=fnt(FX, 50), fill=(40, 34, 16, 255))
NOTE = note.rotate(1.6, resample=Image.BICUBIC, expand=True)
NOTE_Y = 392
STEPS = ["Set up environment", "Configure everything", "Test and debug"]
fs = fnt(FB, 56); SH = 88
def step_img(i, txt):
    im, pad = rrect((950, SH), 28, WHITE + (255,), outline=INK + (255,), width=5, shadow=6)
    d = ImageDraw.Draw(im); d.ellipse((pad + 26, pad + 16, pad + 26 + 56, pad + 16 + 56), fill=LIME + (255,))
    nf = fnt(FK, 38); nb = str(i + 1); d.text((pad + 26 + 28 - tl(nb, nf) / 2, pad + 16 + 6), nb, font=nf, fill=INK + (255,))
    d.text((pad + 108, pad + 12), txt, font=fs, fill=INK + (255,)); return im, pad
STEP_IM = [step_img(i, t) for i, t in enumerate(STEPS)]
STEP_Y = [538, 636, 734]
ARROW = rgba((1, 1))
# CTA
CTA = [["Send", "this", "to"], ["the", "friend", "who"], ["overcomplicates"], ["everything."]]
fc = fnt(FK, 96); CTA_LH = 122; CTA_Y0 = 288

def seg(t, a, b, fi=0.3, fo=0.25): return ss((t - a) / fi) * (1 - ss((t - (b - fo)) / fo))

def frame(k):
    t = k / FPS
    canvas = np.ones((H, W, 3), np.float32) * np.array(BASE, np.float32)
    # ===== scene 1: Claude (all 5 checks ticked from frame 0, nothing animates on the list) =====
    a1 = 1 - ss((t - T_SW1) / 0.30); r1 = ss((t - T_SW1) / 0.30)
    if a1 > 0.003:
        dy = -36 * r1 - 8 * ss(t / 2.6); br = 1 + 0.02 * np.sin(t * 1.5)
        paste(canvas, PILL_C, PIX - PADC, 290 - PADC + dy, a1)
        paste(canvas, CARD_C, PIX - CPAD, CARD_Y - CPAD + dy, a1)
        for i, rr in enumerate(ROWS):
            y = ROW_Y[i] + dy; paste(canvas, CHK, 100, y + 8, a1)
            paste(canvas, text_layer(rr[0], fl, INK), 178, y + 1, a1)
        fd = FACE_C.resize((int((FS + 16) * br), int((FS + 16) * br)), Image.LANCZOS); paste(canvas, fd, 540 - fd.width / 2, FACE_Y + (FS + 16) / 2 - fd.height / 2 + dy, a1)
    # ===== scene 2: ChatGPT (3 steps appear TOGETHER and stay >= 2 s) =====
    in2 = ss((t - T_IN2) / 0.35); out2 = 1 - ss((t - T_SW2) / 0.28); a2 = in2 * out2
    if a2 > 0.003:
        dy = 40 * (1 - in2) - 36 * (1 - out2); br = 1 + 0.02 * np.sin((t - T_IN2) * 1.5)
        paste(canvas, PILL_G, PIX - PADG, 290 - PADG + dy, a2)
        n2 = ss((t - (wordt(2, "chat") - 0.05)) / 0.4)
        paste(canvas, NOTE, (W - NOTE.width) / 2, NOTE_Y + dy - 6 * (1 - n2), a2 * n2)
        si = ss((t - T_STEPS) / 0.45)
        for i in range(3):
            im, pad = STEP_IM[i]; paste(canvas, im, PIX - pad, STEP_Y[i] - pad + dy + 18 * (1 - si), a2 * si)
        fd = FACE_G.resize((int((FS + 16) * br), int((FS + 16) * br)), Image.LANCZOS); paste(canvas, fd, 540 - fd.width / 2, 838 + (FS + 16) / 2 - fd.height / 2 + dy, a2 * n2)
    # ===== scene 3: CTA =====
    in3 = ss((t - T_IN3) / 0.3)
    if in3 > 0.003:
        paste(canvas, FACE_C2, 65 + (FW + 16) / 2 + 0 - FACE_C2.width / 2 , 1010 - FACE_C2.height / 2 + 30 * (1 - in3), in3)
        paste(canvas, FACE_G2, 1015 - (FW + 16) / 2 - FACE_G2.width / 2, 1010 - FACE_G2.height / 2 + 30 * (1 - in3), in3)
        times = {"send": wordt(3, "send"), "this": wordt(3, "this"), "to": wordt(3, "to"), "the": wordt(3, "the"), "friend": wordt(3, "friend"), "who": wordt(3, "who"),
                 "overcomplicates": wordt(3, "over"), "everything.": wordt(3, "everything")}
        for li, row in enumerate(CTA):
            tot = sum(tl(w, fc) for w in row) + (len(row) - 1) * 28; x = (W - tot) / 2; y = CTA_Y0 + li * CTA_LH
            for w in row:
                tw_ = tl(w, fc); tin = times[w.lower()] - 0.05; a = ss((t - tin) / 0.25)
                if w.lower() == "overcomplicates":
                    hb = rgba((int(tw_) + 44, 112)); ImageDraw.Draw(hb).rounded_rectangle((0, 0, hb.width - 1, 111), 22, fill=INK + (255,))
                    paste(canvas, hb, x - 22, y + 12, in3 * ss((t - tin) / 0.3))
                    paste(canvas, text_layer(w, fc, WHITE), x - 4, y + 4 * (1 - a), a * in3)
                else:
                    paste(canvas, text_layer(w, fc, INK), x - 4, y + 4 * (1 - a), a * in3)
                x += tw_ + 28
    return np.clip(canvas, 0, 255).astype(np.uint8)

def collect():
    for i, rr in enumerate(ROWS): reg_text(rr[0], 178, ROW_Y[i] + 8, FS_L, 0, T_SW1 + .3)
    reg_text("Me with Claude", PIX + 44, 290 + 17, 66, 0, T_SW1 + .3)
    reg_text("Me with ChatGPT", PIX + 44 + 88, 290 + 17, 66, T_IN2 + .35, T_SW2 + .28)
    nl = (W - NOTE.width) / 2; t0 = wordt(2, "chat") + .4
    reg_text("What I asked:", int(nl + npad + 30), NOTE_Y + npad + 8, 38, t0, T_SW2)
    reg_text("Do this simple thing", int(nl + npad + 92), NOTE_Y + npad + 56, 50, t0, T_SW2)
    for i, t_ in enumerate(STEPS): reg_text(t_, PIX + 108, STEP_Y[i] + 14, 56, T_STEPS + .45, T_SW2)
    for li, row in enumerate(CTA):
        tot = sum(tl(w, fc) for w in row) + (len(row) - 1) * 28
        reg_text(" ".join(row), int((W - tot) / 2), CTA_Y0 + li * CTA_LH + 12, 96, wordt(3, "send") + 0.3 + 0.3 * li, D)
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
<!-- text-only stand-in for ep91 final7 (positions from build91_final7.py); the reel is drawn by build91_final7.py -->
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
{divs}
</div><script>window.__timelines={{main:gsap.timeline({{paused:true}}).to({{}},{{duration:{D}}})}};</script></body></html>'''); print("standin", len(TXT)); sys.exit()
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                            "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), sys.argv[1]], stdin=subprocess.PIPE)
    for k in range(int(round(D * FPS))): enc.stdin.write(frame(k).tobytes())
    enc.stdin.close(); enc.wait(); print("done", D)
