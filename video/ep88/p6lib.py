"""ep88 round 6 asset helpers: real scans (CC0 / public domain from Wikimedia Commons) -> torn paper pieces with fibre rim and baked shadow.
Textures: cardboard photo (CC0), Fayetteville Observer 1865 newspaper scan (public domain), film-grain scan (CC0). Edges are procedural (jittered contour), the paper itself is a real scan."""
import hashlib, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps

H = os.path.dirname(os.path.abspath(__file__))
A6 = H + "/assets6"
OUT = H + "/hf/assets/p6"
os.makedirs(OUT, exist_ok=True)
PAD = 46
_tex = {}


def tex(name):
    if name not in _tex:
        _tex[name] = Image.open(f"{A6}/{name}").convert("RGB")
    return _tex[name]


def paper_crop(kind, w, h, seed):
    """a real-scan crop of size w x h. kind: card | news | white"""
    rnd = random.Random(seed)
    if kind == "card":
        t = tex("cardboard.jpg")
    elif kind == "news":
        t = tex("news1.jpg")
    else:
        t = tex("cardboard.jpg")
    s = 1.0
    cw, ch = int(w / s), int(h / s)
    if kind == "news":
        # take a crop of text columns; scale so the print is readable-ish but small
        sc = 0.45 if w * h < 900000 else 0.7
        cw, ch = int(w / sc), int(h / sc)
        cw, ch = min(cw, t.width - 4), min(ch, t.height - 4)
    cw, ch = min(cw, t.width - 2), min(ch, t.height - 2)
    x0 = rnd.randint(0, t.width - cw - 1); y0 = rnd.randint(0, t.height - ch - 1)
    c = t.crop((x0, y0, x0 + cw, y0 + ch)).resize((w, h), Image.LANCZOS)
    return c


def tint_paper(img, kind, color):
    """kind news: map greys to cream/ink; others: multiply by the colour"""
    if kind == "news":
        g = ImageOps.autocontrast(img.convert("L"), cutoff=2)
        g = g.point(lambda v: int(min(255, 150 + v * 105 / 255)))   # lighten: low contrast so text above stays readable
        lo = np.array((120, 96, 62), float); hi = np.array((236, 222, 188), float)
        a = np.asarray(g, float)[..., None] / 255.0
        rgb = lo + (hi - lo) * a
        return Image.fromarray(rgb.astype("uint8"), "RGB")
    g = ImageOps.autocontrast(img.convert("L"), cutoff=1)
    a = (np.asarray(g, float) / 255.0)[..., None] * 0.18 + 0.82
    rgb = np.array(color, float) * a
    return Image.fromarray(np.clip(rgb, 0, 255).astype("uint8"), "RGB")


def torn_mask(w, h, seed, amp=7, step=26, scale=2):
    rnd = random.Random(seed)
    W, Hh = w * scale, h * scale
    def jit(): return rnd.uniform(0, amp) + rnd.uniform(0, 1.6)
    pts = []
    x = 0
    while x < w: pts.append((x, jit())); x += step * rnd.uniform(.35, 1.2)
    y = 0
    while y < h: pts.append((w - jit(), y)); y += step * rnd.uniform(.35, 1.2)
    x = w
    while x > 0: pts.append((x, h - jit())); x -= step * rnd.uniform(.35, 1.2)
    y = h
    while y > 0: pts.append((jit(), y)); y -= step * rnd.uniform(.35, 1.2)
    m = Image.new("L", (W, Hh), 0)
    ImageDraw.Draw(m).polygon([(px * scale, py * scale) for px, py in pts], fill=255)
    return m.resize((w, h), Image.LANCZOS)


def make_piece(w, h, kind="card", color=(255, 255, 255), seed=1, amp=7, rim=True, shadow=True, step=26):
    """RGBA PNG (w+2*PAD, h+2*PAD): rim + paper + shadow. returns path relative to hf/ and pad"""
    key = hashlib.md5(f"{w}{h}{kind}{color}{seed}{amp}{rim}{shadow}{step}".encode()).hexdigest()[:14]
    rel = f"assets/p6/{key}.png"
    path = H + "/hf/" + rel
    if os.path.exists(path):
        return rel, PAD
    mask = torn_mask(w, h, seed, amp, step)
    paper = tint_paper(paper_crop("news" if kind == "news" else "card", w, h, seed), "news" if kind == "news" else "x", color)
    canvas = Image.new("RGBA", (w + 2 * PAD, h + 2 * PAD), (0, 0, 0, 0))
    big = Image.new("L", canvas.size, 0); big.paste(mask, (PAD, PAD))
    if shadow:
        for off, blur, al in ((16, 16, 0.42), (3, 3, 0.45)):
            sh = Image.new("L", canvas.size, 0)
            sh.paste(big.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * al)), (0, off))
            canvas.alpha_composite(Image.merge("RGBA", (Image.new("L", canvas.size, 30), Image.new("L", canvas.size, 18), Image.new("L", canvas.size, 6), sh)))
    if rim:
        dil = big.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(.8))
        rimc = Image.merge("RGBA", (Image.new("L", canvas.size, 244), Image.new("L", canvas.size, 235), Image.new("L", canvas.size, 212), dil))
        canvas.alpha_composite(rimc)
    pc = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); pc.paste(paper.convert("RGBA"), (PAD, PAD)); pc.putalpha(big)
    canvas.alpha_composite(pc)
    canvas.save(path)
    return rel, PAD
