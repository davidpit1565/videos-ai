#!/usr/bin/env python3
"""ep91 final11 caption + CTA-card overlay (RGBA, 1080x1920, 30 fps) -> qtrle .mov. Words lit in time with the voice (cues json).
usage: caps11.py <cues.json> <out.mov> [D=10.03] | --still t cues.json out.png"""
import sys, re, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
FK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
W, H, FPS = 1080, 1920, 30
INK = (15, 15, 15); WHITE = (255, 255, 255); LIME = (190, 228, 64); DIM = (150, 150, 158); PLATE = (16, 16, 20)
def ss(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
def norm(w): return re.sub(r"[^a-z']", "", w.lower().replace("’", "'"))
def align(script, wh):
    """map script words to (start,end) using whisper tokens (greedy by letter count)."""
    out = []; i = 0
    for sw in script:
        need = len(norm(sw)); got = 0; s = None; e = None
        while i < len(wh) and (got < need or s is None):
            tok = wh[i]; s = tok[-2] if s is None else s; e = tok[-1]; got += len(norm(tok[0])); i += 1
            if got >= need: break
        out.append((s, e))
    return out
def load(cp, D):
    L = json.load(open(cp))["lines"]
    l1 = align("Me with Claude, it listens.".split(), L[0]["words"]); l2 = align("Me with ChatGPT, it's way more tangled.".split(), L[1]["words"])
    l3 = align("Send this to the friend who overcomplicates everything.".split(), L[2]["words"])
    return L, l1, l2, l3
f_cap = ImageFont.truetype(FK, 80)
def cap_layer(words, wt, t, t0, t1):
    """words: list of str (one line of script), wt: [(s,e)]; plate fades 0.12 s; current word lime, past white, future grey."""
    a = ss((t - t0) / 0.12) * (1 - ss((t - (t1 - 0.12)) / 0.12))
    if a <= 0.003: return None
    # wrap into <= 2 lines at the comma / balanced
    sp = f_cap.getlength(" ")
    full = sum(f_cap.getlength(w) for w in words) + sp * (len(words) - 1)
    if full <= 880: lines = [list(range(len(words)))]
    else:
        best = None
        for k in range(1, len(words)):
            w1 = sum(f_cap.getlength(x) for x in words[:k]) + sp * (k - 1); w2 = sum(f_cap.getlength(x) for x in words[k:]) + sp * (len(words) - k - 1)
            sc = abs(w1 - w2) - (10000 if words[k - 1].endswith(',') else 0)
            if max(w1, w2) <= 880 and (best is None or sc < best[0]): best = (sc, k)
        k = best[1]; lines = [list(range(k)), list(range(k, len(words)))]
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    PY0, PY1 = 1006, 1236
    d.rounded_rectangle((65, PY0, 1015, PY1), 44, fill=PLATE + (int(225 * a),))
    lh = 98; y = (PY0 + PY1) / 2 - lh * len(lines) / 2 + 6
    for ln in lines:
        tot = sum(f_cap.getlength(words[i]) for i in ln) + sp * (len(ln) - 1); x = (W - tot) / 2
        for i in ln:
            s, e = wt[i]
            col = LIME if (s - 0.02 <= t < e + 0.06) else (WHITE if t >= e + 0.06 else DIM)
            d.text((x, y), words[i], font=f_cap, fill=col + (int(255 * a),)); x += f_cap.getlength(words[i]) + sp
        y += lh
    return im
f_card = ImageFont.truetype(FK, 78)
CARD = [["Send", "this", "to"], ["the", "friend", "who"], ["overcomplicates"], ["everything."]]
def card_layer(wt3, t, t0):
    a = ss((t - t0) / 0.2)
    if a <= 0.003: return None
    CW, CH = 900, 420; im = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, CW, CH), 44, fill=(250, 248, 244, 245)); k = 0; ys = [28, 112, 206, 312]; sp = f_card.getlength(" ")
    for li, row in enumerate(CARD):
        tot = sum(f_card.getlength(w) for w in row) + sp * (len(row) - 1); x = (CW - tot) / 2
        for w in row:
            s, e = wt3[k]; k += 1; wl = f_card.getlength(w); cur = (s - 0.02 <= t < e + 0.06)
            if w == "overcomplicates":
                d.rounded_rectangle((x - 18, 206, x + wl + 18, 306), 18, fill=(LIME if cur else (12, 12, 12))); d.text((x, 214), w, font=f_card, fill=(INK if cur else WHITE))
            else:
                if cur: d.rounded_rectangle((x - 8, ys[li] + 10, x + wl + 8, ys[li] + 98), 14, fill=LIME)
                d.text((x, ys[li]), w, font=f_card, fill=INK)
            x += wl + sp
    al = im.getchannel("A").point(lambda v: int(v * a)); im.putalpha(al)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0)); out.paste(im, (90, 420)); return out
def frame(t, ctx):
    L, l1, l2, l3 = ctx
    for words, wt, ln in ((["Me", "with", "Claude,", "it", "listens."], l1, 0), (["Me", "with", "ChatGPT,", "it's", "way", "more", "tangled."], l2, 1)):
        im = cap_layer(words, wt, t, L[ln]["start"] - 0.05, (2.45 if ln == 0 else 5.62))
        if im is not None: return im
    c = card_layer(l3, t, L[2]["start"] + 0.10)
    return c if c is not None else Image.new("RGBA", (W, H), (0, 0, 0, 0))
if __name__ == "__main__":
    if sys.argv[1] == "--still":
        t = float(sys.argv[2]); ctx = load(sys.argv[3], 10.03); fr = frame(t, ctx); bg = Image.new("RGBA", (W, H), (60, 70, 90, 255)); bg.alpha_composite(fr); bg.convert("RGB").save(sys.argv[4]); sys.exit()
    cp, out = sys.argv[1], sys.argv[2]; D = float(sys.argv[3]) if len(sys.argv) > 3 else 10.03; ctx = load(cp, D)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "qtrle", "-pix_fmt", "argb", out], stdin=subprocess.PIPE)
    for k in range(int(round(D * FPS))): enc.stdin.write(np.asarray(frame(k / FPS, ctx), np.uint8).tobytes())
    enc.stdin.close(); enc.wait(); print("done")
