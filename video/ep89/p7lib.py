"""ep88 round 7 asset helpers. Everything is built from real CC0/public-domain scans (see channel/ep88-image-credits.md):
torn-edge profiles measured from real torn-paper scans (rip_hole1/2), paper textures from real scans (Rijksmuseum coloured paper, newsprint, cardboard),
halftone from real photos. Pieces = RGBA PNG with real-profile torn contour, variable light fibre rim, inner edge highlight, thickness shadow."""
import hashlib, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from scipy import ndimage as ndi

H = os.path.dirname(os.path.abspath(__file__))
A6, A7 = H + "/assets6", H + "/assets7"
OUT = H + "/hf/assets/p7"
os.makedirs(OUT, exist_ok=True)
PAD = 50
_tex = {}

def tex(path):
    if path not in _tex: _tex[path] = Image.open(path).convert("RGB")
    return _tex[path]

# ---------- real torn-edge profiles
def _profiles():
    f = OUT + "/_profiles.npy"
    if os.path.exists(f): return list(np.load(f, allow_pickle=True))
    profs = []
    for name in ("rip_hole2.jpg", "rip_hole1.jpg"):
        g = np.asarray(Image.open(f"{A7}/{name}").convert("L"), float)
        hole = g >= 251
        lab, n = ndi.label(hole)
        if n == 0: continue
        sizes = ndi.sum(hole, lab, range(1, n + 1)); k = int(np.argmax(sizes)) + 1
        m = lab == k
        ys, xs = np.where(m); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        cols = [(x, np.where(m[:, x])[0]) for x in range(x0 + 4, x1 - 4) if m[:, x].any()]
        top = np.array([c[1].min() for c in cols], float); bot = np.array([c[1].max() for c in cols], float)
        rows = [(y, np.where(m[y, :])[0]) for y in range(y0 + 4, y1 - 4) if m[y, :].any()]
        lef = np.array([r[1].min() for r in rows], float); rig = np.array([r[1].max() for r in rows], float)
        for p in (top, bot, lef, rig):
            if len(p) < 40: continue
            xx = np.arange(len(p)); c = np.polyfit(xx, p, 2); r = p - np.polyval(c, xx)
            if r.std() > 0.3: profs.append(r / r.std())
    np.save(f, np.array(profs, dtype=object), allow_pickle=True)
    return profs
PROF = _profiles()

def edge_disp(L, amp, rnd, step=3.0):
    """inward displacement along a side of length L (px), from a real torn profile (random window, mirrored tiling) + fibre noise"""
    p = PROF[rnd.randrange(len(PROF))]
    n = int(L / step) + 3
    seq = []
    pos = rnd.randrange(len(p)); d = rnd.choice((1, -1))
    for _ in range(n):
        seq.append(p[pos]); pos += d
        if pos >= len(p) - 1 or pos <= 0: d = -d; pos = max(1, min(len(p) - 2, pos))
    s = np.array(seq); s = (s - s.min()) / (s.max() - s.min() + 1e-6)
    xs = np.linspace(0, len(s) - 1, int(L))
    d = np.interp(xs, np.arange(len(s)), s) * amp * .7
    lf = ndi.gaussian_filter1d(np.array([rnd.uniform(-1, 1) for _ in range(int(L))]), 16); lf = lf / (np.abs(lf).max() + 1e-6)
    d += (lf + 1) * .5 * amp * .9           # slow wobble: big irregular tear
    d += np.array([rnd.uniform(0, 1.8) for _ in range(int(L))])  # fibre jitter
    return ndi.gaussian_filter1d(d, .7)

def torn_mask(w, h, seed, amp=8, sides="tblr"):
    rnd = random.Random(seed)
    S = 2
    top = edge_disp(w, amp if "t" in sides else .6, rnd); bot = edge_disp(w, amp if "b" in sides else .6, rnd)
    lef = edge_disp(h, amp if "l" in sides else .6, rnd); rig = edge_disp(h, amp if "r" in sides else .6, rnd)
    pts = [(x, top[min(x, w - 1)]) for x in range(0, w, 2)] + [(w - rig[min(y, h - 1)], y) for y in range(0, h, 2)] + \
          [(x, h - bot[min(x, w - 1)]) for x in range(w, 0, -2)] + [(lef[min(y, h - 1)], y) for y in range(h, 0, -2)]
    m = Image.new("L", (w * S, h * S), 0)
    ImageDraw.Draw(m).polygon([(a * S, b * S) for a, b in pts], fill=255)
    return m.resize((w, h), Image.LANCZOS)

# ---------- paper textures
PAPERS = {
    "card": (A6 + "/cardboard.jpg", None), "news": (A6 + "/news1.jpg", None), "news2": (A7 + "/rip_news.jpg", None),
    "red": (A7 + "/pap_red.jpg", (60, 60, 940, 700)), "orange": (A7 + "/pap_orange.jpg", (60, 60, 940, 740)),
    "blue": (A7 + "/pap_blue.jpg", (60, 60, 940, 740)), "purple": (A7 + "/pap_purple.jpg", (60, 60, 940, 760)),
    "ticket": (A7 + "/tix_nz1919.jpg", (14, 14, 1010, 922)), "map": (A7 + "/map_london.jpg", (40, 30, 990, 715)),
    "chart": (A7 + "/map_chart1.jpg", (200, 40, 1000, 660)),
}

def paper_crop(kind, w, h, seed, scale=None):
    rnd = random.Random(seed)
    path, box = PAPERS[kind]
    t = tex(path)
    if box: t = t.crop(box)
    if kind in ("ticket", "map", "chart"):   # keep whole, cover-fit
        s = max(w / t.width, h / t.height); r = t.resize((max(w, int(t.width * s)), max(h, int(t.height * s))), Image.LANCZOS)
        x0 = rnd.randint(0, r.width - w); y0 = rnd.randint(0, r.height - h); return r.crop((x0, y0, x0 + w, y0 + h))
    sc = scale or {"news": .42, "news2": .5}.get(kind, 1.0)
    cw, ch = min(int(w / sc), t.width - 2), min(int(h / sc), t.height - 2)
    x0 = rnd.randint(0, t.width - cw - 1); y0 = rnd.randint(0, t.height - ch - 1)
    return t.crop((x0, y0, x0 + cw, y0 + ch)).resize((w, h), Image.LANCZOS)

def tint(img, kind, color):
    a = np.asarray(img, float)
    if kind in ("news", "news2"):
        g = np.asarray(ImageOps.autocontrast(img.convert("L"), cutoff=2), float) / 255.0
        g = 0.62 + g * 0.38    # low contrast newsprint
        lo = np.array((140, 112, 74), float); hi = np.array((238, 224, 190), float)
        return Image.fromarray((lo + (hi - lo) * g[..., None]).astype("uint8"))
    if kind == "card":
        g = np.asarray(ImageOps.autocontrast(img.convert("L"), cutoff=1), float) / 255.0
        rgb = np.array(color, float) * (0.84 + g[..., None] * 0.16)
        return Image.fromarray(np.clip(rgb, 0, 255).astype("uint8"))
    return img  # real coloured paper / ticket / map: untouched

def make_piece(w, h, kind="card", color=(255, 255, 255), seed=1, amp=9, shadow=True, sides="tblr", rim=(244, 236, 214), rimw=6):
    key = hashlib.md5(f"7{w}{h}{kind}{color}{seed}{amp}{shadow}{sides}{rim}{rimw}".encode()).hexdigest()[:14]
    rel = f"assets/p7/{key}.png"; path = H + "/hf/" + rel
    if os.path.exists(path): return rel, PAD
    rnd = np.random.RandomState(seed)
    mask = np.asarray(torn_mask(w, h, seed, amp, sides), float) / 255.0
    paper = tint(paper_crop(kind, w, h, seed), kind, color)
    cw, ch = w + 2 * PAD, h + 2 * PAD
    M = np.zeros((ch, cw)); M[PAD:PAD + h, PAD:PAD + w] = mask
    # fibre rim: distance outside the mask, variable width (noise-modulated) -> light torn fibres, partial along the edge
    dist_out = ndi.distance_transform_edt(M < .5)
    nz = ndi.gaussian_filter(rnd.rand(ch, cw), 6); nz = (nz - nz.min()) / (nz.max() - nz.min() + 1e-6)
    rw = rimw * (0.35 + 1.5 * nz)
    rim_a = np.clip(1 - dist_out / rw, 0, 1) * (M < .5)
    rim_a *= (0.8 + 0.2 * ndi.gaussian_filter(rnd.rand(ch, cw), 1))
    canvas = np.zeros((ch, cw, 4))
    if shadow:
        for off, blur, al in ((14, 14, .36), (3, 2.2, .5)):
            sh = ndi.shift(ndi.gaussian_filter(M, blur), (off, off * .15), order=1) * al
            sa = sh; canvas[..., 0] = canvas[..., 0] * (1 - sa) + 26 * sa; canvas[..., 1] = canvas[..., 1] * (1 - sa) + 17 * sa
            canvas[..., 2] = canvas[..., 2] * (1 - sa) + 8 * sa; canvas[..., 3] = canvas[..., 3] + sa * (1 - canvas[..., 3])
    # rim (light fibre)
    ra = rim_a[..., None]
    for c in range(3): canvas[..., c] = canvas[..., c] * (1 - rim_a) + rim[c] * rim_a
    canvas[..., 3] = canvas[..., 3] + rim_a * (1 - canvas[..., 3])
    # paper body
    P = np.zeros((ch, cw, 3)); P[PAD:PAD + h, PAD:PAD + w] = np.asarray(paper, float)
    # inner edge highlight (thin lighter edge = thickness) + slight darkening just inside
    dist_in = ndi.distance_transform_edt(M > .5)
    hl = np.clip(1 - dist_in / 1.6, 0, 1) * (M > .5) * .55
    P = P * (1 - hl[..., None]) + np.array(rim, float) * hl[..., None]
    P *= (1 - np.clip(1 - np.abs(dist_in - 3.2) / 2.0, 0, 1)[..., None] * .06)
    for c in range(3): canvas[..., c] = canvas[..., c] * (1 - M) + P[..., c] * M
    canvas[..., 3] = canvas[..., 3] * (1 - M) + M
    canvas[..., 3] *= 255
    Image.fromarray(np.clip(canvas, 0, 255).astype("uint8"), "RGBA").save(path)
    return rel, PAD
