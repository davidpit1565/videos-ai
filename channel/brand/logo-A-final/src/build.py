#!/usr/bin/env python3
"""Final kit for logo direction A. Rebuild: cd src && python3 build.py   (needs fonttools, node + playwright in /opt/node-tools)
Writes into the parent folder. One Chromium at a time (render.js)."""
import os, json, subprocess, base64
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from geomA import geom, fit, allpts, polys, enclosing_circle

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE); BRAND = os.path.dirname(OUT)
TMP = os.path.join(HERE, "_tmp"); os.makedirs(TMP, exist_ok=True)
INK = "#0B0B0B"; WHITE = "#FFFFFF"; Y = "#FFE600"
FONT = os.path.join(BRAND, "logo-v2", "ArchivoBlack-Regular.ttf")
PARAMS = dict(g=0, sep=50)          # chosen drawing: the W is its own letter, its two halves touch
TOP, BOT = 300.0, 735.0             # letter top / baseline in raw units
RAW = geom(**PARAMS)
KEY = 28.0                          # keyline round the check on light, raw units

def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def cr(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)

def mark(mode, f, s):
    """f maps raw points, s = scale. dark: white letters + yellow check. light: ink letters, yellow check with ink keyline."""
    fg = [[f(q) for q in pl] for pl in RAW["fg"]]; y = [[f(q) for q in pl] for pl in RAW["y"]]
    if mode == "dark":
        return polys(fg, WHITE) + polys(y, Y)
    key = polys(y, INK, f' stroke="{INK}" stroke-width="{2 * KEY * s:.2f}" stroke-linejoin="miter" stroke-miterlimit="3"')
    return polys(fg, INK) + key + polys(y, Y)

def circ_fit(R, c=500):
    (cx, cy), r = enclosing_circle(allpts(RAW)); s = R / r
    return (lambda q: (c + (q[0] - cx) * s, c + (q[1] - cy) * s)), s
def box_fit(x, y, h=None, w=None):
    """place by the bounding box: top-left (x,y), given height of the LETTERS (top..baseline) or total width"""
    pts = allpts(RAW); x0 = min(p[0] for p in pts); x1 = max(p[0] for p in pts); y0 = min(p[1] for p in pts)
    s = h / (BOT - TOP) if h else w / (x1 - x0)
    return (lambda q: (x + (q[0] - x0) * s, y + (q[1] - y0) * s)), s, (x1 - x0) * s, (BOT - y0) * s, (TOP - y0) * s

FIELD = {"dark": INK, "light": WHITE}
def avatar_svg(mode, size=None, shape="square", R=392):
    f, s = circ_fit(R)
    wh = f' width="{size}" height="{size}"' if size else ""
    bg = {"square": f'<rect width="1000" height="1000" fill="{FIELD[mode]}"/>',
          "circle": f'<circle cx="500" cy="500" r="500" fill="{FIELD[mode]}"/>'}[shape]
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"{wh}>{bg}{mark(mode, f, s)}</svg>'
def favicon_svg(mode, size=None):
    f, s, w, h, _ = box_fit(0, 0, w=800)
    f2 = lambda q: (f(q)[0] + 100, f(q)[1] + (1000 - h) / 2)
    wh = f' width="{size}" height="{size}"' if size else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"{wh}><rect width="1000" height="1000" rx="190" fill="{FIELD[mode]}"/>'
            f'{mark(mode, f2, s)}</svg>')
def bare_svg(mode):
    pad = 40; f, s, w, h, _ = box_fit(pad, pad, h=400)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w + 2 * pad:.1f} {h + 2 * pad:.1f}">{mark(mode, f, s)}</svg>'

# ---- wordmark outlines (same hand kerning as the earlier kits)
_f = TTFont(FONT); _gs = _f.getGlyphSet(); _cmap = _f.getBestCmap(); UPM = _f["head"].unitsPerEm; CAP = _f["OS/2"].sCapHeight
KERN = {"LL": -10, "LY": -14, "WO": -6}
def text_path(t, cap=100.0, track=-6):
    s = cap / CAP; x = 0.0; d = []
    for i, ch in enumerate(t):
        if ch == " ": x += 0.30 * UPM; continue
        pen = SVGPathPen(_gs); _gs[_cmap[ord(ch)]].draw(TransformPen(pen, (s, 0, 0, -s, x * s, 0))); d.append(pen.getCommands())
        x += _gs[_cmap[ord(ch)]].width + track + KERN.get(t[i:i + 2], 0)
    return " ".join(d), (x - track) * s

def lockup_body(mode, x, y, cap):
    """mark + ACTUALLY WORKS on one line; (x,y) = top-left of the whole lockup. returns body, W, H"""
    lh = cap * 1.42                                   # height of the AW letters against the cap height
    f, s, mw, mh, toff = box_fit(x, y, h=lh)
    d, tw = text_path("ACTUALLY WORKS", cap)
    tx = x + mw + cap * 0.42; base = y + toff + lh / 2 + cap / 2
    fg = WHITE if mode == "dark" else INK
    return mark(mode, f, s) + f'<path transform="translate({tx:.1f},{base:.1f})" d="{d}" fill="{fg}"/>', (tx - x) + tw, mh
def lockup_svg(mode, field=True):
    pad = 60; body, W, H = lockup_body(mode, pad, pad, 100)
    rect = f'<rect width="{W + 2 * pad:.1f}" height="{H + 2 * pad:.1f}" fill="{FIELD[mode]}"/>' if field else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W + 2 * pad:.1f} {H + 2 * pad:.1f}">{rect}{body}</svg>', W + 2 * pad, H + 2 * pad
def banner_svg(mode, W, H, lw, cx=None, cy=None, guide=None):
    """field + centred one-line lockup of total width lw"""
    _, w0, h0 = lockup_body(mode, 0, 0, 100); cap = 100 * lw / w0
    _, w, h = lockup_body(mode, 0, 0, cap)
    cx = W / 2 if cx is None else cx; cy = H / 2 if cy is None else cy
    body, _, _ = lockup_body(mode, cx - w / 2, cy - h / 2, cap)
    g = ""
    if guide:
        gx, gy, gw, gh = guide
        g = f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" fill="none" stroke="#FF2D6F" stroke-width="4" stroke-dasharray="18 12"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="{FIELD[mode]}"/>{body}{g}</svg>', (cx - w / 2, cy - h / 2, w, h)

def render(jobs):
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(HERE, "render.js"), jf], check=True, env=dict(os.environ, NODE_PATH="/opt/node-tools/node_modules"))
def sized(svg, **kw):
    return svg.replace("<svg ", "<svg " + " ".join(f'{k}="{v}"' for k, v in kw.items()) + " ", 1)
def W_(p, s): open(os.path.join(OUT, p), "w").write(s)

def export():
    jobs = []; info = {}
    for m in ("dark", "light"):
        W_(f"mark-A-{m}.svg", avatar_svg(m)); W_(f"mark-A-{m}-nofield.svg", bare_svg(m)); W_(f"favicon-A-{m}.svg", favicon_svg(m))
        jobs.append(dict(html=avatar_svg(m, 1080), w=1080, h=1080, out=os.path.join(OUT, f"avatar-A-{m}-1080.png")))
        for n in (32, 64):
            jobs.append(dict(html=favicon_svg(m, n), w=n, h=n, transparent=True, out=os.path.join(OUT, f"favicon-A-{m}-{n}.png")))
        for n in (32, 110):   # circle crops, only for checking
            jobs.append(dict(html=avatar_svg(m, n, "circle"), w=n, h=n, transparent=True, out=os.path.join(TMP, f"crop-{m}-{n}.png")))
        svg, w, h = lockup_svg(m); W_(f"lockup-A-oneline-{m}.svg", svg)
        jobs.append(dict(html=sized(svg, width=1600, height=round(1600 * h / w)), w=1600, h=round(1600 * h / w), out=os.path.join(OUT, f"lockup-A-oneline-{m}.png")))
        yt, box = banner_svg(m, 2560, 1440, 1240); info[f"yt-{m}"] = box
        jobs.append(dict(html=yt, w=2560, h=1440, out=os.path.join(OUT, f"banner-youtube-2560x1440-{m}.png")))
        ytg, _ = banner_svg(m, 2560, 1440, 1240, guide=(507, 508.5, 1546, 423))
        jobs.append(dict(html=ytg, w=2560, h=1440, out=os.path.join(TMP, f"yt-guide-{m}.png")))
        fb, box = banner_svg(m, 1640, 624, 880, cy=290); info[f"fb-{m}"] = box
        jobs.append(dict(html=fb, w=1640, h=624, out=os.path.join(OUT, f"cover-facebook-1640x624-{m}.png")))
    render(jobs)
    json.dump(info, open(os.path.join(TMP, "boxes.json"), "w"), indent=1)
    return info

# ---------------------------------------------------------------- decision sheet (800 css px at 2x = 1600 px)
def av(m, n): return sized(avatar_svg(m, None, "circle"), width=n, height=n, style="display:block;flex:none")
def ig_profile(m, ui):
    return f'''<div class="ui {ui} igp"><div class=row>{av(m, 86)}
      <div class=st><div><b>&mdash;</b><span>posts</span></div><div><b>&mdash;</b><span>followers</span></div><div><b>&mdash;</b><span>following</span></div></div></div>
      <div class=nm>Actually Works</div><div class=bio>Placeholder bio line. Mock-up, not the real profile.</div>
      <div class=btns><span>Follow</span><span>Message</span></div></div>'''
def ig_rows(m, ui):
    return f'''<div class="ui {ui} igr"><div class=row>{av(m, 32)}<div><b>actually_works.ai</b> <i>Follow</i><br><span class=sec>Reel author row (placeholder)</span></div></div>
      <div class=row>{av(m, 32)}<div><b>actually_works.ai</b> Placeholder comment text.<br><span class=sec>&mdash; &nbsp; Reply</span></div></div></div>'''
def yt(m, ui):
    b, _ = banner_svg(m, 1546, 423, 1240 * 0.98)
    return f'''<div class="ui {ui} yt"><div class=ban>{sized(b.replace('width="1546" height="423"', '', 1), width="100%", style="display:block;border-radius:8px")}</div>
      <div class=row>{av(m, 56)}<div><div class=ch>Actually Works</div><div class=sec>@actually_works.ai &middot; &mdash; subscribers &middot; &mdash; videos</div>
      <div class=sec>Placeholder channel description.</div></div></div></div>'''
def site(m):
    svg, w, h = lockup_svg(m, field=False)
    fav = sized(favicon_svg(m), width=16, height=16, style="display:block;flex:none")
    return f'''<div class="ui {'dk' if m == 'dark' else 'lt'} site"><div class="tab">{fav}<span>Actually Works</span><em>&times;</em></div>
      <div class=hd>{sized(svg, height=36, style="display:block;margin:-5px 0 -5px -7px")}<span class=nav style="white-space:nowrap">Episodes &nbsp;&nbsp; About</span></div></div>'''

def sheet():
    cell = lambda lab, a, b: f'<div class=lab>{lab}</div><div class=pair><div>{a}</div><div>{b}</div></div>'
    rows = ""
    for ui, un in (("lt", "LIGHT UI"), ("dk", "DARK UI")):
        rows += cell(f"INSTAGRAM PROFILE HEADER &middot; app in {un} &middot; avatar 86 px", ig_profile("dark", ui), ig_profile("light", ui))
    for ui, un in (("lt", "LIGHT UI"), ("dk", "DARK UI")):
        rows += cell(f"INSTAGRAM REEL-AUTHOR ROW + COMMENT ROW &middot; app in {un} &middot; avatar 32 px", ig_rows("dark", ui), ig_rows("light", ui))
    for ui, un in (("lt", "LIGHT UI"), ("dk", "DARK UI")):
        rows += cell(f"YOUTUBE CHANNEL HEADER &middot; app in {un} &middot; banner safe area + round avatar", yt("dark", ui), yt("light", ui))
    rows += '<div class=lab>SITE HEADER + BROWSER TAB (favicon 16 px) &middot; left: DARK SITE &middot; right: LIGHT SITE</div>' \
            f'<div class=pair><div>{site("dark")}</div><div>{site("light")}</div></div>'
    html = f'''<!doctype html><meta charset=utf-8><style>
*{{box-sizing:border-box}}body{{margin:0;width:800px;background:#d9d6cb;font:12px/1.35 Inter,"Helvetica Neue",Arial,sans-serif;color:#111;padding:0 12px 12px}}
h1{{font:800 17px/1.2 Inter,Arial,sans-serif;margin:0;padding:10px 0 2px}}.sub0{{font-size:11px;color:#444;margin-bottom:8px}}
.heads{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}.heads div{{font:800 13px Inter,Arial,sans-serif;padding:7px 10px;border-radius:6px 6px 0 0}}
.hd1{{background:#0b0b0b;color:#fff}}.hd2{{background:#fff;color:#0b0b0b}}
.lab{{font:700 9.5px Inter,Arial,sans-serif;letter-spacing:.06em;color:#333;margin:7px 0 3px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.ui{{padding:10px 14px;border-radius:4px;overflow:hidden}}.ui.lt{{background:#fff;color:#000}}.ui.dk{{background:#000;color:#f5f5f5}}
.lt .sec,.lt .bio{{color:#737373}}.dk .sec,.dk .bio{{color:#a8a8a8}}
.row{{display:flex;align-items:center;gap:12px}}
.igp .st{{display:flex;gap:26px;margin-left:14px;text-align:center}}.igp .st b{{display:block;font-size:15px}}.igp .st span{{font-size:12px}}
.igp .nm{{font-weight:700;font-size:13px;margin-top:9px}}.igp .bio{{font-size:12px}}
.btns{{display:flex;gap:6px;margin-top:9px}}.btns span{{flex:1;text-align:center;font-weight:600;padding:6px 0;border-radius:8px}}
.lt .btns span{{background:#efefef}}.dk .btns span{{background:#262626}}.btns span:first-child{{background:#0095f6!important;color:#fff}}
.igr .row{{gap:10px;align-items:flex-start;font-size:12px}}.igr .row+.row{{margin-top:10px}}.igr i{{font-style:normal;font-weight:600;border:1px solid currentColor;border-radius:6px;padding:0 6px;font-size:10px;margin-left:4px;opacity:.8}}
.yt.lt{{background:#fff}}.yt.dk{{background:#0f0f0f}}.yt .row{{margin-top:10px}}.yt .ch{{font-weight:700;font-size:16px}}.yt .sec{{font-size:10.5px}}
.yt .sub{{margin-top:9px;text-align:center;font-weight:600;padding:7px;border-radius:18px}}.yt.lt .sub{{background:#0f0f0f;color:#fff}}.yt.dk .sub{{background:#f1f1f1;color:#0f0f0f}}
.site{{padding:0}}.site.dk{{background:#0b0b0b}}.site .tab{{display:flex;align-items:center;gap:7px;font-size:11px;padding:7px 10px;width:170px;border-radius:8px 8px 0 0;margin:6px 0 0 8px}}
.site.lt{{background:#dfe1e5}}.site.dk{{background:#202124}}.site.lt .tab{{background:#fff}}.site.dk .tab{{background:#35363a;color:#e8eaed}}.tab em{{margin-left:auto;font-style:normal;opacity:.6}}
.site .hd{{display:flex;align-items:center;justify-content:space-between;padding:12px 14px;font-size:12px;font-weight:600}}
.site.lt .hd{{background:#fff;border-bottom:1px solid #e6e6e6}}.site.dk .hd{{background:#0b0b0b;border-bottom:1px solid #2a2a2a;color:#fff}}
.site .pg{{padding:12px 14px 16px;font-size:11px}}.site.lt .pg{{background:#fff;color:#737373}}.site.dk .pg{{background:#0b0b0b;color:#a8a8a8}}
</style>
<h1>Logo A &middot; which profile picture: DARK or LIGHT?</h1>
<div class=sub0>Same mark, two files. Mock-ups with placeholder text; dashes stand in for numbers. Phone density (2x).</div>
<div class=heads><div class=hd1>DARK AVATAR &middot; white AW, yellow check, on black</div><div class=hd2>LIGHT AVATAR &middot; black AW, outlined check, on white</div></div>
{rows}'''
    p = os.path.join(TMP, "decide.html"); open(p, "w").write(html)
    render([dict(file=p, w=800, h=1200, scale=2, full=True, out=os.path.join(OUT, "decide-dark-vs-light.png"))])

if __name__ == "__main__":
    info = export(); sheet()
    print("boxes", {k: [round(x) for x in v] for k, v in info.items()})
    for a, b, n in ((Y, INK, "yellow/ink"), (Y, WHITE, "yellow/white"), (WHITE, INK, "white/ink"), (WHITE, Y, "white/yellow"),
                    (INK, "#000000", "ink field/IG dark #000"), (INK, "#0F0F0F", "ink field/YT dark #0f0f0f"), (WHITE, "#FFFFFF", "white field/white UI")):
        print(f"{n}: {cr(a, b):.2f}")
