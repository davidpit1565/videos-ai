"""static assets for ep88 round 6 (real scans/photos -> halftone, grain, blurred foreground scraps)"""
import os, sys, random
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageChops
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p6lib
H = p6lib.H; A6 = p6lib.A6; OUT = p6lib.OUT

def halftone(img, cell=7, mix=.5):
    """real halftone screen of a real photo: sepia base + rotated dot screen; keeps the photo readable"""
    g = ImageOps.autocontrast(img.convert("L"), cutoff=1)
    w, h = g.size
    S = 2
    big = g.resize((w * S, h * S), Image.BICUBIC).rotate(45, expand=True, resample=Image.BICUBIC, fillcolor=255)
    arr = np.asarray(big, float) / 255.0
    W, Hh = big.size
    dots = Image.new("L", (W, Hh), 255)
    d = ImageDraw.Draw(dots)
    c = cell * S
    for y in range(0, Hh, c):
        for x in range(0, W, c):
            v = arr[min(Hh - 1, y + c // 2), min(W - 1, x + c // 2)]
            r = (1 - v) ** .6 * c * .62
            if r > .4: d.ellipse((x + c / 2 - r, y + c / 2 - r, x + c / 2 + r, y + c / 2 + r), fill=int(30 + v * 40))
    dots = dots.rotate(-45, expand=True, resample=Image.BICUBIC, fillcolor=255)
    ox = (dots.width - w * S) // 2; oy = (dots.height - h * S) // 2
    dots = dots.crop((ox, oy, ox + w * S, oy + h * S)).resize((w, h), Image.LANCZOS)
    # sepia/duotone of the photo
    gg = np.asarray(ImageOps.autocontrast(img.convert("L"), cutoff=1), float)[..., None] / 255.0
    lo = np.array((38, 28, 18), float); hi = np.array((244, 232, 204), float)
    sep = lo + (hi - lo) * gg
    # keep a bit of the real colour so the photo reads as a photo
    col = np.asarray(img.convert("RGB"), float)
    base = sep * (1 - .35) + col * .35
    dm = np.asarray(dots, float)[..., None] / 255.0
    out = base * (1 - mix) + base * dm * mix * 1.9
    return Image.fromarray(np.clip(out, 0, 255).astype("uint8"), "RGB")

def crop_to(img, aspect, cx=.5, cy=.5, w=620):
    W, Hh = img.size
    if W / Hh > aspect:
        nw = int(Hh * aspect); x0 = int((W - nw) * cx); box = (x0, 0, x0 + nw, Hh)
    else:
        nh = int(W / aspect); y0 = int((Hh - nh) * cy); box = (0, y0, W, y0 + nh)
    c = img.crop(box)
    return c.resize((w, int(w / aspect)), Image.LANCZOS)

PH = H + "/hf/assets/photos"
srcs = {"beach": (PH + "/beach.jpg", .56, .55), "cake": (PH + "/cake.jpg", .5, .5), "desk": (PH + "/desk.jpg", .45, .5)}
for k, (p, cx, cy) in srcs.items():
    im = Image.open(p).convert("RGB")
    crop_to(im, .82, cx, cy).save(f"{OUT}/ph_{k}.jpg", quality=90)  # raw crop for halftone
for k, f in (("cat1", "cat1.png"), ("cat2", "cat2.jpg")):
    try:
        im = Image.open(f"{A6}/{f}").convert("RGB"); crop_to(im, .82, .5, .5).save(f"{OUT}/ph_{k}.jpg", quality=90)
    except Exception as e:
        print("skip", k, e)
for f in os.listdir(OUT):
    if f.startswith("ph_") and f.endswith(".jpg") and not f.startswith("pht_"):
        im = Image.open(f"{OUT}/{f}"); halftone(im).save(f"{OUT}/pht_{f[3:]}", quality=90)
# background: real cardboard, full frame cover (2880x1920) slightly darkened and warm
bg = Image.open(f"{A6}/cardboard.jpg").convert("RGB")
bg = bg.resize((int(bg.width * 1920 / bg.height), 1920), Image.LANCZOS)
arr = np.asarray(bg, float); gr_ = arr.mean(axis=2, keepdims=True); arr = (gr_ * .5 + arr * .5) * np.array((.72, .68, .62))
Image.fromarray(np.clip(arr, 0, 255).astype("uint8")).save(f"{OUT}/bg_card.jpg", quality=86)
# film grain overlay from the real Kodak scan: high-pass, rotate to portrait, mid-grey based (overlay blend)
gr = Image.open(f"{A6}/grain.jpg").convert("L").rotate(90, expand=True)
gr = gr.resize((1080, int(1080 * gr.height / gr.width)))
if gr.height < 1920: gr = gr.resize((int(gr.width * 1920 / gr.height), 1920))
gr = gr.crop((0, 0, 1080, 1920))
a = np.asarray(gr, float); hp = a - np.asarray(gr.filter(ImageFilter.GaussianBlur(6)), float)
hp = hp / (hp.std() + 1e-6) * 22 + 128
Image.fromarray(np.clip(hp, 0, 255).astype("uint8")).save(f"{OUT}/grain.jpg", quality=85)
# transition sheets: a real newspaper page (scaled small, text unreadable as texture), torn leading edge, soft shadow
for i, (cx, cy) in enumerate(((0, 0), (0, .45))):
    n = Image.open(f"{A6}/news1.jpg").convert("RGB")
    W, Hh = 1400, 2150
    sc = .75
    cw, chh = int(W / sc), int(Hh / sc)
    cw = min(cw, n.width); chh = min(chh, n.height)
    crop = n.crop((0, int((n.height - chh) * cy), cw, int((n.height - chh) * cy) + chh)).resize((W, Hh), Image.LANCZOS)
    rgb = p6lib.tint_paper(crop, "news", (255, 255, 255))
    # torn left edge only
    rnd = random.Random(70 + i)
    m = Image.new("L", (W, Hh), 255); d = ImageDraw.Draw(m)
    pts = [(0, 0)]; y = 0
    while y < Hh: pts.append((rnd.uniform(0, 26) + rnd.uniform(0, 5), y)); y += rnd.uniform(8, 30)
    pts += [(0, Hh)]
    m = Image.new("L", (W, Hh), 0); ImageDraw.Draw(m).polygon([(W, 0)] + [(p[0], p[1]) for p in pts[1:-1]] + [(W, Hh)], fill=255)
    P = 70
    can = Image.new("RGBA", (W + P, Hh + 2 * P), (0, 0, 0, 0))
    big = Image.new("L", can.size, 0); big.paste(m, (P, P))
    sh = Image.new("L", can.size, 0); sh.paste(big.filter(ImageFilter.GaussianBlur(24)).point(lambda v: int(v * .55)), (-18, 0))
    can.alpha_composite(Image.merge("RGBA", (Image.new("L", can.size, 20), Image.new("L", can.size, 12), Image.new("L", can.size, 4), sh)))
    rim = big.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(1))
    can.alpha_composite(Image.merge("RGBA", (Image.new("L", can.size, 244), Image.new("L", can.size, 235), Image.new("L", can.size, 212), rim)))
    pc = Image.new("RGBA", can.size, (0, 0, 0, 0)); pc.paste(rgb.convert("RGBA"), (P, P)); pc.putalpha(big); can.alpha_composite(pc)
    can.save(f"{OUT}/sheet{i}.png")
# blurred foreground scraps (pre-blurred, low contrast): torn news pieces
for i in range(3):
    rel, pad = p6lib.make_piece(420 + i * 90, 300 + i * 50, "news", (255, 255, 255), 200 + i, 9, True, False)
    im = Image.open(H + "/hf/" + rel).convert("RGBA").filter(ImageFilter.GaussianBlur(16))
    r, g, b, al = im.split(); al = al.point(lambda v: int(v * .55)); Image.merge("RGBA", (r, g, b, al)).save(f"{OUT}/fg{i}.png")
print("ok", sorted(os.listdir(OUT))[:40])
