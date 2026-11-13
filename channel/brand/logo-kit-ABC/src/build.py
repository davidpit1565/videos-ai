#!/usr/bin/env python3
"""Logo kit A / B / C for Actually Works. Rebuild: cd src && python3 build.py
Needs fonttools, pillow, node with playwright. Writes everything into the parent folder."""
import os, sys, json, math, base64, subprocess
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
BRAND = os.path.dirname(OUT)
sys.path.insert(0, os.path.join(BRAND, "logo-kit-B", "src"))
from geom import enclosing_circle, variants  # reuse of the B kit geometry

INK = "#0B0B0B"; WHITE = "#FFFFFF"; Y = "#FFE600"
FONT = os.path.join(BRAND, "logo-v2", "ArchivoBlack-Regular.ttf")
NAMES = {"A": "TICK LIGATURE", "B": "THE HIGHLIGHT", "C": "THE WINK"}
SUB = {"A": "AW, the last strokes of the W are a yellow check",
       "B": "heavy A with a yellow marker swipe",
       "C": "a dot and a check: a winking face"}

def P(poly): return " ".join(f"{round(x,1):g},{round(y,1):g}" for x, y in poly)
def poly(pts, fill): return f'<polygon points="{P(pts)}" fill="{fill}"/>'

# ------------------------------------------------------------------ geometry
def geom_A():
    """Five strokes of one width, flat cuts top and bottom, every joint shares a full
    stroke-width edge. The white part stops in a point short of the yellow check, so
    white and yellow never touch (they are 1.07 : 1 against each other)."""
    p, w, top, bot, tick_top, g = 132.0, 96.0, 300.0, 735.0, 185.0, 26.0
    k = p / (bot - top)
    s1 = [(0, bot), (w, bot), (p + w, top), (p, top)]
    s2 = [(p, top), (p + w, top), (2 * p + w, bot), (2 * p, bot)]
    y1 = top + g / (2 * k); y2 = top + (w + g) / (2 * k)
    s3 = [(2 * p, bot), (2 * p + w, bot), (3 * p + w - k * (y2 - top), y2), (3 * p - k * (y1 - top), y1)]
    by0, by1 = 596.0, 664.0   # crossbar, low enough that the counter above it stays open at 32 px
    bar = [(w + k * (bot - by0) - 3, by0), (2 * p - k * (bot - by0) + 3, by0),
           (2 * p - k * (bot - by1) + 3, by1), (w + k * (bot - by1) - 3, by1)]
    s4 = [(3 * p, top), (3 * p + w, top), (4 * p + w, bot), (4 * p, bot)]
    dx = k * (bot - tick_top)
    s5 = [(4 * p, bot), (4 * p + w, bot), (4 * p + w + dx, tick_top), (4 * p + dx, tick_top)]
    return {"fg": [s1, s2, s3, bar], "y": [s4, s5]}

def geom_B():
    v = variants()["b"]           # "B2 optical" from logo-kit-B
    return {"fg": [v["A"]], "y": [v["S"]]}

def geom_C():
    return {"dot": (320.0, 520.0, 105.0),
            "fg": [[(458.9, 470), (581.1, 470), (686.1, 640), (563.9, 640)],
                   [(564.1, 640), (685.9, 640), (910.9, 270), (789.1, 270)]]}

def allpts(g):
    pts = [q for grp in ("fg", "y") for pl in g.get(grp, []) for q in pl]
    if "dot" in g:
        cx, cy, r = g["dot"]
        pts += [(cx + r * math.cos(a / 12 * math.pi), cy + r * math.sin(a / 12 * math.pi)) for a in range(24)]
    return pts

def fit(g, R, centre=(500, 500), shift=(0, 0)):
    (cx, cy), r = enclosing_circle(allpts(g))
    s = R / r
    f = lambda q: (centre[0] + shift[0] + (q[0] - cx) * s, centre[1] + shift[1] + (q[1] - cy) * s)
    o = {k: [[f(q) for q in pl] for pl in g[k]] for k in ("fg", "y") if k in g}
    if "dot" in g:
        x, y = f(g["dot"][:2]); o["dot"] = (x, y, g["dot"][2] * s)
    return o

RAW = {"A": geom_A(), "B": geom_B(), "C": geom_C()}
# radius of the mark inside the 500-radius avatar circle
FITR = {"A": 400, "B": 392, "C": 322}
AV = {d: fit(RAW[d], FITR[d]) for d in "ABC"}
FAV = {"A": fit(RAW["A"], 455), "B": fit(RAW["B"], 450), "C": fit(RAW["C"], 340)}

def colours(d, mode):
    """field, main colour, accent colour"""
    if d == "C":
        return (Y, INK, INK) if mode == "dark" else (INK, Y, Y)
    return (INK, WHITE, Y) if mode == "dark" else (WHITE, INK, Y)

def elements(d, g, mode):
    field, fg, acc = colours(d, mode)
    s = ""
    if d == "C":
        x, y, r = g["dot"]
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fg}"/>'
        s += "".join(poly(pl, fg) for pl in g["fg"])
        return s
    a = "".join(poly(pl, fg) for pl in g["fg"]); b = "".join(poly(pl, acc) for pl in g["y"])
    if d == "B" and mode == "light":
        return b + a            # layer rule of kit B: on white the letter lies over the swipe
    return a + b

def avatar_svg(d, mode, size=None, shape="square", g=None):
    field, _, _ = colours(d, mode)
    wh = f' width="{size}" height="{size}"' if size else ""
    bg = {"square": f'<rect width="1000" height="1000" fill="{field}"/>',
          "circle": f'<circle cx="500" cy="500" r="500" fill="{field}"/>',
          "round": f'<rect width="1000" height="1000" rx="190" fill="{field}"/>'}[shape]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"{wh}>{bg}'
            f'{elements(d, g or AV[d], mode)}</svg>')

def favicon_svg(d, mode, size=None):
    return avatar_svg(d, mode, size, "circle" if d == "C" else "round", FAV[d])

def bare(d, mode):
    """Mark without a field for lockups. Returns (inner svg, x, y, w, h). C keeps its disc."""
    if d == "C":
        field, _, _ = colours(d, mode)
        return (f'<circle cx="500" cy="500" r="500" fill="{field}"/>' + elements(d, AV[d], mode), 0, 0, 1000, 1000)
    pts = allpts(AV[d])
    x0 = min(q[0] for q in pts); x1 = max(q[0] for q in pts); y0 = min(q[1] for q in pts); y1 = max(q[1] for q in pts)
    return (elements(d, AV[d], mode), x0, y0, x1 - x0, y1 - y0)

# ------------------------------------------------------------------ wordmark outlines
_f = TTFont(FONT); _gs = _f.getGlyphSet(); _cmap = _f.getBestCmap(); UPM = _f["head"].unitsPerEm
CAP = _f["OS/2"].sCapHeight
KERN = {"LL": -10, "LY": -14, "WO": -6}   # same hand kerning as kit B
def text_path(t, cap=100.0, track=-6):
    """Returns (path d, width). Baseline at y=0, cap line at y=-cap."""
    s = cap / CAP; x = 0.0; d = []
    for i, ch in enumerate(t):
        if ch == " ":
            x += 0.30 * UPM; continue
        gn = _cmap[ord(ch)]; pen = SVGPathPen(_gs)
        _gs[gn].draw(TransformPen(pen, (s, 0, 0, -s, x * s, 0)))
        d.append(pen.getCommands())
        x += _gs[gn].width + track + KERN.get(t[i:i + 2], 0)
    return " ".join(d), (x - track) * s

def place_mark(d, mode, x, y, h):
    inner, bx, by, bw, bh = bare(d, mode)
    s = h / bh
    return f'<g transform="translate({x - bx * s:.2f},{y - by * s:.2f}) scale({s:.4f})">{inner}</g>', bw * s

def lockup(d, mode, kind, bgfill=True):
    bg, fg = (INK, WHITE) if mode == "dark" else (WHITE, INK)
    a, aw = text_path("ACTUALLY"); w, ww = text_path("WORKS"); one, ow = text_path("ACTUALLY WORKS")
    pad = 70
    if kind == "h":       # mark left, two plain lines (wordmark-v3 option 1)
        mh = 250 if d != "C" else 262
        m, mw = place_mark(d, mode, pad, pad, mh)
        tx = pad + mw + 62; ty = pad + (mh - 234) / 2
        W = tx + max(aw, ww) + pad; H = mh + 2 * pad
        body = m + f'<path transform="translate({tx:.1f},{ty + 100:.1f})" d="{a}" fill="{fg}"/>' \
                 + f'<path transform="translate({tx:.1f},{ty + 234:.1f})" d="{w}" fill="{fg}"/>'
    elif kind == "line":  # mark left, one line (site header)
        mh = 190
        m, mw = place_mark(d, mode, pad, pad, mh)
        tx = pad + mw + 50; W = tx + ow + pad; H = mh + 2 * pad
        body = m + f'<path transform="translate({tx:.1f},{pad + mh / 2 + 50:.1f})" d="{one}" fill="{fg}"/>'
    else:                 # stacked: mark above, two centred lines, thin underline stroke (wordmark-v3 option 2)
        mh = 300
        W = aw + 2 * pad
        inner, bx, by, bw, bh = bare(d, mode)
        m, mw = place_mark(d, mode, (W - bw * mh / bh) / 2, pad, mh)
        ty = pad + mh + 70
        ux = (W - ww) / 2; uy = ty + 234 + 26; th = 13; rise = ww * math.tan(math.radians(2))
        ucol = Y if mode == "dark" else INK     # yellow on white is 1.27 : 1, so the line is ink there
        ul = poly([(ux - 4, uy + rise / 2), (ux + ww + 4, uy - rise / 2), (ux + ww, uy - rise / 2 + th), (ux - 8, uy + rise / 2 + th)], ucol)
        H = uy + rise / 2 + th + pad
        body = m + f'<path transform="translate({(W - aw) / 2:.1f},{ty + 100:.1f})" d="{a}" fill="{fg}"/>' \
                 + f'<path transform="translate({(W - ww) / 2:.1f},{ty + 234:.1f})" d="{w}" fill="{fg}"/>' + ul
    rect = f'<rect width="{W:.1f}" height="{H:.1f}" fill="{bg}"/>' if bgfill else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H:.1f}">{rect}{body}</svg>', W, H

# ------------------------------------------------------------------ rendering
def render(jobs):
    jf = os.path.join(HERE, "_jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(HERE, "render.js"), jf], check=True); os.remove(jf)

def b64(path): return "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()
def sized(svg, **kw):
    att = " ".join(f'{k}="{v}"' for k, v in kw.items())
    return svg.replace("<svg ", f"<svg {att} ", 1)

def export_assets():
    jobs = []
    for d in "ABC":
        os.makedirs(os.path.join(OUT, d), exist_ok=True)
        for mode in ("dark", "light"):
            open(os.path.join(OUT, d, f"mark-{d}-{mode}.svg"), "w").write(avatar_svg(d, mode))
            open(os.path.join(OUT, d, f"favicon-{d}-{mode}.svg"), "w").write(favicon_svg(d, mode))
            jobs.append(dict(html=avatar_svg(d, mode, 1024), w=1024, h=1024, out=os.path.join(OUT, d, f"avatar-{d}-{mode}-1024.png")))
            for n in (320, 110, 40, 32):
                jobs.append(dict(html=avatar_svg(d, mode, n, "circle"), w=n, h=n, transparent=True,
                                 out=os.path.join(OUT, d, f"avatar-{d}-{mode}-{n}.png")))
            jobs.append(dict(html=favicon_svg(d, mode, 64), w=64, h=64, transparent=True,
                             out=os.path.join(OUT, d, f"favicon-{d}-{mode}-64.png")))
            jobs.append(dict(html=favicon_svg(d, mode, 16), w=16, h=16, transparent=True,
                             out=os.path.join(HERE, f"_fav16-{d}-{mode}.png")))
            for kind, nm in (("h", "horizontal"), ("s", "stacked"), ("line", "oneline")):
                svg, W, H = lockup(d, mode, kind)
                open(os.path.join(OUT, d, f"lockup-{d}-{nm}-{mode}.svg"), "w").write(svg)
                pw = 1600 if kind != "s" else 1000; ph = round(pw * H / W)
                jobs.append(dict(html=sized(svg, width=pw, height=ph), w=pw, h=ph, out=os.path.join(OUT, d, f"lockup-{d}-{nm}-{mode}.png")))
    render(jobs)

# ------------------------------------------------------------------ sheets
CSS = """
*{box-sizing:border-box}html,body{margin:0}body{font-family:Inter,'DejaVu Sans',sans-serif;background:#d9d6cc;color:#0B0B0B}
@font-face{font-family:AB;src:url(FONTURL)}
.ab{font-family:AB}
.top{padding:26px 36px 22px;display:flex;align-items:baseline;gap:22px;flex-wrap:wrap}
.top .l{font-family:AB;font-size:84px;line-height:.8}.top .n{font-family:AB;font-size:34px}.top .s{font-size:19px;color:#444}
.halves{display:flex}
.half{width:50%;padding:28px 36px 36px}
.half.dark{background:#000;color:#f5f5f5}.half.light{background:#fff;color:#0B0B0B}
.cap{font:600 12px/1.3 Inter,sans-serif;letter-spacing:.09em;text-transform:uppercase;opacity:.55;margin:26px 0 10px}
.cap:first-child{margin-top:0}
.avs{display:flex;gap:26px;align-items:flex-start}
.avs .col{display:flex;flex-direction:column;gap:18px}
.avs .row{display:flex;gap:20px;align-items:flex-end}
.avs figure{margin:0;display:flex;flex-direction:column;align-items:center;gap:6px}
.avs figcaption{font-size:11px;opacity:.55}
img,svg{display:block}
.px{image-rendering:pixelated}
.ring{border-radius:50%}.dark .ring{box-shadow:0 0 0 1px #2c2c2c}.light .ring{box-shadow:0 0 0 1px #d6d6d6}
.ig{display:flex;gap:28px;align-items:center}
.ig .h{font-size:20px;font-weight:600}
.ig .st{display:flex;gap:22px;font-size:14px;margin:9px 0}
.ig .st b{font-weight:600}
.ig .bio{font-size:14px;line-height:1.4}
.ig .bio i{opacity:.55;font-style:normal}
.btns{display:flex;gap:8px;margin-top:10px}
.btn{font-size:13px;font-weight:600;padding:6px 18px;border-radius:8px}
.dark .btn{background:#262626}.light .btn{background:#efefef}
.cm{display:flex;gap:12px;align-items:flex-start;font-size:14px;line-height:1.35;margin-bottom:12px}
.cm b{font-weight:600}.cm .m{font-size:12px;opacity:.55;margin-top:3px}
.site{display:flex;align-items:center;justify-content:space-between;padding:10px 18px;border-radius:10px}
.dark .site{background:#0B0B0B;border:1px solid #2a2a2a}.light .site{background:#fff;border:1px solid #dcdcdc}
.site nav{display:flex;gap:26px;font-size:15px;font-weight:500}
.tabbar{display:flex;align-items:flex-end;gap:18px}
.tabs{flex:1;border-radius:10px 10px 0 0;padding:8px 10px 0;height:44px;display:flex}
.dark .tabs{background:#1f2023}.light .tabs{background:#dee1e6}
.tab{display:flex;align-items:center;gap:9px;padding:0 14px;height:36px;border-radius:9px 9px 0 0;font-size:13px;width:250px}
.dark .tab{background:#35363a;color:#e8eaed}.light .tab{background:#fff;color:#202124}
.tab .x{margin-left:auto;opacity:.6}
.lk{display:flex;gap:18px;align-items:center}
.note{font-size:12px;opacity:.55;margin-top:8px;line-height:1.4}
"""

def img(path, size, cls=""): return f'<img class="{cls}" src="{b64(path)}" width="{size}" height="{size}">'
def av(d, mode, n, size=None): return img(os.path.join(OUT, d, f"avatar-{d}-{mode}-{n}.png"), size or n, "ring")
def other(m): return "light" if m == "dark" else "dark"

def half(d, mode):
    ui = mode
    fig = lambda n: f'<figure>{av(d, mode, n)}<figcaption>{n} px</figcaption></figure>'
    x5 = (f'<figure>{img(os.path.join(OUT, d, f"avatar-{d}-{mode}-32.png"), 160, "px")}'
          f'<figcaption>the 32 px file, enlarged x5</figcaption></figure>')
    line, lw, lh = lockup(d, mode, "line", bgfill=False)
    hsvg, hw, hh = lockup(d, mode, "h", bgfill=False)
    ssvg, sw, sh = lockup(d, mode, "s", bgfill=False)
    def comment(m):
        return (f'<div class="cm">{av(d, m, 32)}<div><b>actually_works.ai</b> Placeholder comment text, mock-up only.'
                f'<div class="m">&mdash; &nbsp; Reply &nbsp; <span>({m} avatar file)</span></div></div></div>')
    fav16 = img(os.path.join(HERE, f"_fav16-{d}-{mode}.png"), 16)
    fav64 = img(os.path.join(OUT, d, f"favicon-{d}-{mode}-64.png"), 64)
    return f'''<div class="half {ui}">
<div class="cap">{mode} mode &middot; avatar in the circle crop, real pixel sizes (thin ring = crop edge, mock-up aid)</div>
<div class="avs">{fig(320)}<div class="col"><div class="row">{fig(110)}{fig(40)}{fig(32)}</div>{x5}</div></div>
<div class="cap">Instagram profile header (mock-up, placeholder text, no real numbers)</div>
<div class="ig">{av(d, mode, 320, 110)}
<div><div class="h">actually_works.ai</div>
<div class="st"><span><b>&mdash;</b> posts</span><span><b>&mdash;</b> followers</span><span><b>&mdash;</b> following</span></div>
<div class="bio"><b>Actually Works</b><br><i>Placeholder bio line. Mock-up, not the real profile.</i></div>
<div class="btns"><span class="btn">Follow</span><span class="btn">Message</span></div></div></div>
<div class="cap">Comment row at 32 px: both avatar files on this background</div>
{comment(mode)}{comment(other(mode))}
<div class="cap">Site header (mock-up)</div>
<div class="site">{sized(line, height=40, width=round(40 * lw / lh))}<nav><span>Episodes</span><span>About</span></nav></div>
<div class="cap">Browser tab with the favicon (16 px in the tab, the 64 px file beside it)</div>
<div class="tabbar"><div class="tabs"><div class="tab">{fav16}<span>Actually Works</span><span class="x">&times;</span></div></div>{fav64}</div>
<div class="cap">Lockups: horizontal and stacked (no word in a box; the stacked one has a thin line under WORKS)</div>
<div class="lk">{sized(hsvg, width=400, height=round(400 * hh / hw))}{sized(ssvg, width=230, height=round(230 * sh / sw))}</div>
</div>'''

def kit_html(d):
    return (f'<!doctype html><meta charset="utf-8"><style>{CSS.replace("FONTURL", "file://" + FONT)}</style>'
            f'<div class="top"><span class="l">{d}</span><span class="n">{NAMES[d]}</span>'
            f'<span class="s">{SUB[d]} &middot; draft kit for choosing, nothing is published</span></div>'
            f'<div class="halves">{half(d, "dark")}{half(d, "light")}</div>')

OCSS = """
.band{border-top:4px solid #0B0B0B}
.bt{padding:14px 28px 12px;display:flex;align-items:baseline;gap:16px}
.bt .l{font-family:AB;font-size:60px;line-height:.8}.bt .n{font-family:AB;font-size:26px}.bt .s{font-size:17px;color:#444}
.oh{width:50%;padding:22px 26px 26px}
.oh.dark{background:#000;color:#f5f5f5}.oh.light{background:#fff}
.orow{display:flex;gap:22px;align-items:center}
.ocol{display:flex;flex-direction:column;gap:16px}
.osm{display:flex;gap:14px;align-items:center}
.ocap{font-size:13px;opacity:.6;margin-top:4px}
.oig{display:flex;gap:16px;align-items:center;margin-top:22px}
.oig .h{font-size:19px;font-weight:600}.oig .b{font-size:14px;opacity:.6;margin-top:3px}
.olk{margin-top:22px}
.title{padding:22px 28px 16px}.title h1{font-family:AB;font-size:40px;margin:0 0 6px}.title p{margin:0;font-size:18px;color:#333}
"""
def overview_html():
    bands = ""
    for d in "ABC":
        hs = ""
        for mode in ("dark", "light"):
            hsvg, hw, hh = lockup(d, mode, "h", bgfill=False)
            ssvg, sw, sh = lockup(d, mode, "s", bgfill=False)
            hs += f'''<div class="oh {mode}"><div class="orow">{av(d, mode, 320, 230)}
<div class="ocol"><div class="osm">{av(d, mode, 110)}{av(d, mode, 40)}{av(d, mode, 32)}</div>
<div class="osm">{img(os.path.join(OUT, d, f"avatar-{d}-{mode}-32.png"), 160, "px")}<span class="ocap">32 px<br>x5</span></div></div>
<div style="margin-left:auto">{sized(ssvg, width=200, height=round(200 * sh / sw))}</div></div>
<div class="oig">{av(d, mode, 40)}<div><div class="h">actually_works.ai</div><div class="b">Placeholder bio line (mock-up)</div></div>
<div style="margin-left:auto">{av(d, other(mode), 32)}</div></div>
<div class="olk">{sized(hsvg, width=430, height=round(430 * hh / hw))}</div></div>'''
        bands += (f'<div class="band"><div class="bt"><span class="l">{d}</span><span class="n">{NAMES[d]}</span>'
                  f'<span class="s">{SUB[d]}</span></div><div class="halves">{hs}</div></div>')
    return (f'<!doctype html><meta charset="utf-8"><style>{CSS.replace("FONTURL", "file://" + FONT)}{OCSS}</style>'
            f'<div class="title"><h1>ACTUALLY WORKS &middot; LOGO A / B / C</h1>'
            f'<p>Left: dark mode. Right: light mode. Sizes 230, 110, 40, 32 px, the 32 px file enlarged x5, '
            f'the stacked lockup, a profile line (far right: the other avatar file at 32 px) and the horizontal lockup. The thin ring around each circle is only there to show the crop.</p></div>{bands}')

def sheets():
    jobs = []
    for d in "ABC":
        hp = os.path.join(HERE, f"_kit-{d}.html"); open(hp, "w").write(kit_html(d))
        jobs.append(dict(file=hp, w=1600, h=900, full=True, scale=2, out=os.path.join(OUT, f"kit-{d}.png")))
    hp = os.path.join(HERE, "_overview.html"); open(hp, "w").write(overview_html())
    jobs.append(dict(file=hp, w=1600, h=900, full=True, scale=2, out=os.path.join(OUT, "kit-ABC-overview.png")))
    render(jobs)
    for j in jobs:      # supersampled at 2x, stored at 1600 px wide so "32 px" is 32 real pixels
        im = Image.open(j["out"]); im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
        im.save(j["out"], optimize=True); print(os.path.basename(j["out"]), im.size)
        os.remove(j["file"])
    for f in os.listdir(HERE):
        if f.startswith("_fav16"): os.remove(os.path.join(HERE, f))

if __name__ == "__main__":
    export_assets(); sheets()
    json.dump({d: {k: ([[[round(a, 2), round(b, 2)] for a, b in pl] for pl in v] if k != "dot" else [round(t, 2) for t in v])
                   for k, v in AV[d].items()} for d in "ABC"}, open(os.path.join(HERE, "construction.json"), "w"), indent=1)
