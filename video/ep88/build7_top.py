# ---- round 7: real-material torn-paper collage. Real scans only (CC0/PD, credits in channel/ep88-image-credits.md): coloured paper (Rijksmuseum), newsprint,
# tickets, maps, cardboard; torn contours from measured real torn-edge profiles (p7lib); halftone photos; letterpress ink via SVG displacement+erosion.
import random as _r, hashlib as _h
from PIL import ImageFont
sys.path.insert(0, H)
import p7lib
PAD = p7lib.PAD
YEL, BLK, CRM, WHT = (242, 194, 48), (23, 19, 15), (255, 255, 255), (252, 249, 240)
J = []; SFX = []; REG = {}
def js(s): J.append(s)
def sfx(f, t, g=0): SFX.append((f, round(t, 3), g))
def tt(t): return f"{t:.3f}"
FONTF = {"BS": H + "/hf/assets/fonts/BigShoulders-Bold.ttf", "Gloock": H + "/hf/assets/fonts/Gloock-Regular.ttf", "PlexM": H + "/hf/assets/fonts/IBMPlexMono-Bold.ttf", "IDisp": H + "/hf/assets/fonts/InterDisplay-Black.otf"}

def pimg(w, h, kind, color, seed, amp=10, shadow=True, sides="tblr", rimw=6):
    rel, pad = p7lib.make_piece(w, h, kind, color, seed, amp, shadow, sides, rimw=rimw)
    return f'<img class="pbg" src="{rel}" style="left:{-pad}px;top:{-pad}px;width:{w + 2 * pad}px;height:{h + 2 * pad}px">'

def P(inner, id, x, y, w, h, rot=0, kind="card", color=CRM, seed=1, amp=10, z=3, cls="", extra="", sides="tblr"):
    REG[id] = (w, h)
    return (f'<div class="pcw {cls}" id="{id}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z}">'
            f'{pimg(w, h, kind, color, seed, amp, True, sides)}{inner}{extra}</div>')

def strip(id, text, x, y, w, h, rot, paper=("card", YEL), tcolor="#17130F", font="BS", size=120, seed=1, z=4, left=None, align="center", amp=9, ls=None):
    kind, col = paper
    dark = tcolor in ("#17130F", "#3b2a14", "#3b342a", "#5d554a")
    st = f"font-family:{font};font-size:{size}px;line-height:{h}px;color:{tcolor};text-align:{align};"
    if left: st += f"left:{left}px;transform:none;"
    if ls is not None: st += f"letter-spacing:{ls}em;"
    inner = f'<div class="stx {"dk" if dark else "lt"}" id="{id}t" style="{st}">{text}</div>'
    return P(inner, id, x, y, w, h, rot, kind, col or CRM, seed, amp, z)

def tape(id, x, y, rot, w=150, h=44, seed=0, op=.86):
    rel, pad = p7lib.make_piece(w, h, "card", (232, 214, 160), 900 + seed, 4, True, "lr", rim=(250, 244, 226), rimw=3)
    return (f'<img class="tape" id="{id}" src="{rel}" style="left:{x - pad}px;top:{y - pad}px;width:{w + 2 * pad}px;height:{h + 2 * pad}px;transform:rotate({rot}deg);opacity:{op}">')

def stamp(id, text, x, y, rot, size=54, color="#B6402B", ink="A", op=.85, font="BS", box=True, z=20, extra=""):
    b = f"border:4px solid {color};padding:2px 12px 4px;border-radius:7px;" if box else ""
    return (f'<div class="stp ink{ink}" id="{id}" style="left:{x}px;top:{y}px;font:700 {size}px {font};color:{color};{b}opacity:{op};transform:rotate({rot}deg);z-index:{z};{extra}">{text}</div>')

def print_(photo, id, x, y, w, h, rot, z=3, stamp_html="", tp=True, seed=40, tape_rot=-4):
    inner = (f'<img class="phimg" src="assets/p7/pht_{photo}.jpg" style="left:14px;top:14px;width:{w - 28}px;height:{h - 62}px">'
             f'<div class="pvig" style="left:14px;top:14px;width:{w - 28}px;height:{h - 62}px"></div>{stamp_html}')
    t_ = tape(id + "tp", w // 2 - 75 + (seed % 5) * 6 - 12, -18, tape_rot, seed=seed) if tp else ""
    return P(inner, id, x, y, w, h, rot, "card", WHT, seed, 5, z, "prn", t_)

def fbsticker(id, x, y, size, rot):
    return f'<div class="fbs" id="{id}" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;transform:rotate({rot}deg)"><img src="assets/facebook.svg"></div>'

# ---- ransom-note letters: each letter on its own scrap (different paper, face, size, tilt)
def ransom(idp, text, cx, y, seeds=0, maxw=900, z=7):
    spec = [("BS", 1.0, "news", None, "#17130F", 1), ("Gloock", .86, "card", YEL, "#17130F", 0), ("IDisp", .74, "card", BLK, "#f1e8d2", 0), ("BS", 1.02, "red", None, "#f7efdc", 1),
            ("PlexM", .82, "card", WHT, "#8f2a1a", 0), ("Gloock", .92, "news", None, "#17130F", 0), ("IDisp", .7, "blue", None, "#f1e8d2", 1), ("BS", 1.05, "card", YEL, "#17130F", 1),
            ("Gloock", .88, "orange", None, "#17130F", 0), ("PlexM", .8, "news", None, "#17130F", 0)]
    rr = _r.Random(11 + seeds)
    items = []
    for i, ch in enumerate(text):
        if ch == " ": items.append(None); continue
        f, k, kind, col, tc, up = spec[(i * 7 + seeds) % len(spec)]
        size = int(104 * k * rr.uniform(.95, 1.08))
        c = ch.upper() if (up or f != "Gloock") else ch.lower()
        font = ImageFont.truetype(FONTF[f], size)
        tw = int(font.getlength(c)); w = max(54, tw + 26); h = int(size * 1.02) + 22
        items.append((c, f, kind, col, tc, size, w, h))
    tot = sum((it[6] + 9) if it else 34 for it in items)
    s = 1.0 if tot <= maxw else maxw / tot
    x = cx - tot * s / 2; out = ""; k = 0
    for it in items:
        if it is None: x += 34 * s; continue
        c, f, kind, col, tc, size, w, h = it
        rot = rr.uniform(-6, 6); dy = rr.uniform(-9, 9)
        w2, h2 = int(w * s), int(h * s); sz2 = int(size * s)
        inner = f'<div class="stx {"dk" if tc in ("#17130F", "#8f2a1a") else "lt"}" style="font-family:{f};font-size:{sz2}px;line-height:{h2}px;color:{tc};text-transform:none;letter-spacing:0">{c}</div>'
        out += P(inner, f"{idp}{k}", int(x), int(y + dy + (118 - h2) / 2), w2, h2, rot, kind, col or CRM, 700 + k + seeds, 6, z, "rl")
        x += (w + 9) * s; k += 1
    return out, k

# ---- hook block
def hookblock(s, hero):
    ids = {"A": ("cake", "cat", "sled"), "B": ("dog", "bikes", "beach")}[hero]
    rl, n = ransom(f"rl{s}", "NEVER POSTED", 540, 588, 3)
    big = stamp(f"stH{s}", "FILE 0417", 330, 430, 4, 30, "#2b3a6b", "A", .85)
    hb = ""
    if s == "":
        ids2 = ("dog", "bikes", "beach")
        hb = (print_(ids2[1], "pax", 66, 806, 300, 400, 7, 2, "", True, 61) + print_(ids2[2], "pcx", 716, 796, 300, 380, -9, 2, "", True, 63, 5)
              + print_(ids2[0] + "_w", "pbx", 250, 735, 580, 484, 2.5, 3, stamp(f"stHx", "NEVER POSTED", 96, 410, -5, 58, "#B6402B", "B", .95), True, 62))
    return (f'<div class="cam" id="hcam{s}">{usheet(0) if s == "" else ""}'
            + strip(f"hA{s}", "FACEBOOK CAN LOOK", 90, 300, 900, 132, -1.2, ("card", YEL), size=91, seed=3, z=5, left=190, align="left")
            + strip(f"hB{s}", "THROUGH PHOTOS YOU", 70, 442, 930, 124, 1.0, ("card", YEL), font="IDisp", size=74, seed=5, z=5, ls=-.02)
            + rl
            + print_(ids[1], f"pa{s}", 66, 806, 300, 400, -9, 2, "", True, 41)
            + print_(ids[2], f"pc{s}", 716, 796, 300, 380, 8, 2, "", True, 43, 5)
            + print_(ids[0] + "_w", f"pb{s}", 250, 735, 580, 484, -3, 3, big, True, 42)
            + hb + fbsticker(f"fbs{s}", 100, 298, 112, -8) + '</div>')

# ---- UI step cards: printed screenshots pasted on paper (photocopy look, real readable UI text, marker circle)
def marker(id, w, h, seed):
    rr = _r.Random(seed)
    cx, cy = w / 2, h / 2; pts = []
    n = 46
    for i in range(n + 1):
        a = -2.2 + (i / n) * 7.3                      # ~1.15 turns: overshoots its start like a real hand
        k = 1 + .06 * rr.uniform(-1, 1) + .05 * (i / n)
        rx = (w / 2 - 14) * k; ry = (h / 2 - 12) * k
        pts.append((cx + rx * np.cos(a) + rr.uniform(-2, 2), cy + ry * np.sin(a) + rr.uniform(-2, 2)))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return (f'<svg class="mk" id="{id}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="position:absolute;left:0;top:0;overflow:visible;z-index:30">'
            f'<path pathLength="1" d="{d}" fill="none" stroke="#C2331F" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="1" filter="url(#rough)" opacity=".92"/></svg>')

def row(label, y, hot=False, tog=None, chev=True, id=""):
    t = ""
    if tog is not None: t = f'<div class="tg2 {"on" if tog else ""}" id="tg4"><i></i></div>'
    elif chev: t = '<span class="chev">&#8250;</span>'
    return f'<div class="uir {"hot" if hot else ""}" id="{id}" style="top:{y}px"><span class="uil">{label}</span>{t}</div>'

def uiblock(n):
    w, h = 900, 524
    if n == 1:
        body = ('<div class="fbtop"><div class="fbsm"><img src="assets/facebook.svg"></div><i class="ico"></i><i class="ico"></i>'
                '<div class="avt" id="hot1"><i class="avh"></i><i class="avb"></i></div></div>'
                '<div class="comp"><div class="cav"></div><span>What\'s on your mind?</span></div><img class="feedimg" src="assets/p7/pht_cat.jpg">')
        mk = marker("mk1", 230, 210, 1); mkpos = "left:634px;top:8px"
    elif n == 2:
        body = ('<div class="uihd">Menu</div>' + row("Help &amp; support", 100) + row("Settings &amp; privacy", 226, True, id="hot2") + row("Log out", 352, chev=False))
        mk = marker("mk2", 860, 150, 2); mkpos = "left:20px;top:228px"
    elif n == 3:
        body = ('<div class="uihd">Settings &amp; privacy</div>' + row("Settings", 100, True, id="hot3") + row("Privacy Checkup", 226) + row("Activity log", 352))
        mk = marker("mk3", 860, 150, 3); mkpos = "left:20px;top:101px"
    else:
        body = ('<div class="uihd">Settings</div>' + row("Notifications", 96) + row("Camera roll sharing suggestions", 206, True, tog=True, chev=False, id="hot4") + row("Language and region", 368)
                + '<div class="uinote">menu names can differ by app version</div>')
        mk = marker("mk4", 868, 190, 4); mkpos = "left:16px;top:186px"
    tp = tape(f"uitp{n}", 60, -16, -5, seed=10 + n) + tape(f"uitq{n}", 700, -16, 4, seed=20 + n)
    inner = f'<div class="uibody">{body}</div><div class="mkw" style="{mkpos}">{mk}</div><div class="copy"></div><div class="tapr" id="tapr{n}"></div>'
    return P(inner, f"ui{n}", 90, 716, w, h, 0.7 * (-1) ** n, "card", WHT, 20 + n, 6, 4, "uic", tp)

def stepscene(n, lines, nx, lx, rots):
    lab = "".join(strip(f"sl{n}{i}", t, lx + i * (14 if n % 2 else -14), 338 + i * 126, 600 + (i % 2) * 40 + (n % 3) * 14, 110, rots[i],
                         ("card", YEL) if i != 1 else ("card", BLK), "#17130F" if i != 1 else "#f1e8d2", ("BS", "IDisp", "BS")[(i + n) % 3] if i != 1 else "Gloock", (92, 70, 92)[(i + n) % 3] if i != 1 else 86, 60 + n * 3 + i, z=5, ls=(0 if (i + n) % 3 != 1 else -.02))
                  for i, t in enumerate(lines))
    return (f'<div class="sc" id="p{n}">__SS_p{n}__<div class="cam" id="pc{n}"><div class="pnum" id="pn{n}" style="left:{nx}px">{n}</div>{lab}'
            f'<div class="of4" id="of{n}" style="left:{lx + 20}px">STEP {n} OF 4</div>{uiblock(n)}</div></div>')

def bigtoggle(id, x, y, w, h, on=True):
    return f'<div class="btg {"on" if on else ""}" id="{id}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{h // 2}px"><i style="width:{h - 48}px;height:{h - 48}px"></i></div>'

def chat():
    return (P('<div class="mini"><b>Camera roll sharing suggestions</b><div class="tg2" id="tg7"><i></i></div></div>', "outb", 110, 650, 860, 240, 1.0, "news", CRM, 91, 9, 3)
            + '<div class="mavt" id="mav">M</div><div class="dots2" id="dots2"><i></i><i></i><i></i></div>'
            + "".join(strip(f"al{k}", "ALLOW", 250 + (k - 1) * 255, 1070, 235, 112, (-3, 2, -2)[k - 1], [("card", YEL), ("red", None), ("orange", None)][k - 1], ["#17130F", "#f7efdc", "#17130F"][k - 1], "BS", 88, 70 + k, z=6) for k in (1, 2, 3)))

# ---- per-scene scrap sets: different composition every scene, 3 depth layers (far/mid/near), cropped by the frame edge
# kinds: real paper textures. entry: (x, y, w, h, rot, layer)
TPL = {
 "A": [(-150, -70, 640, 340, -5, "far"), (600, -60, 520, 250, 7, "mid"), (-190, 720, 420, 520, -8, "far"), (840, 700, 420, 280, 9, "mid"), (-90, 1290, 720, 520, 3, "mid"), (470, 1440, 700, 400, -3, "mid"), (690, 1250, 330, 200, -8, "mid"), (-40, 1730, 480, 260, 5, "near")],
 "B": [(40, -90, 1100, 310, -2, "far"), (860, 300, 300, 560, 6, "mid"), (-120, 1020, 330, 420, 10, "far"), (480, 1290, 640, 440, -5, "mid"), (-70, 1300, 560, 380, 4, "far"), (300, 1610, 560, 330, -2, "mid"), (840, 1700, 330, 260, 12, "near"), (-90, 280, 260, 300, -9, "near")],
 "C": [(-110, 40, 460, 220, 8, "mid"), (700, -80, 480, 300, -6, "far"), (860, 780, 300, 460, -4, "mid"), (-160, 1260, 640, 400, -4, "far"), (420, 1330, 700, 480, 6, "mid"), (60, 1640, 460, 300, 3, "mid"), (-90, 760, 250, 380, 5, "far"), (760, 1700, 400, 260, -7, "near")],
 "D": [(560, -70, 640, 330, 5, "far"), (-120, -40, 400, 300, -8, "mid"), (-170, 640, 340, 600, 4, "far"), (900, 900, 280, 360, 7, "mid"), (150, 1290, 560, 330, 2, "mid"), (-60, 1620, 640, 380, -4, "far"), (620, 1450, 520, 440, 8, "mid"), (800, 1790, 360, 240, -6, "near")],
 "E": [(-80, -90, 560, 360, 4, "far"), (500, -50, 640, 220, -6, "mid"), (900, 560, 260, 520, -5, "far"), (-140, 900, 300, 380, 8, "mid"), (-110, 1310, 560, 460, -7, "mid"), (330, 1590, 700, 400, 3, "far"), (700, 1290, 480, 330, 6, "mid"), (-70, 1790, 380, 220, -3, "near")],
}
KINDS = [("news", None), ("ticket", None), ("red", None), ("map", None), ("news2", None), ("chart", None), ("news", None), ("orange", None), ("map", None), ("ticket", None), ("blue", None)]
STAMPS = [("FILE", "#2b3a6b", -10), ("COPY", "#B6402B", 7), ("NO. 0417", "#1f1b16", -4), ("DRAFT", "#B6402B", 12), ("10.11", "#2b3a6b", -7), ("ORIGINAL", "#2b3a6b", -6)]
SSET = {}
def scrapset(sid, tpl, off, mirror=False, seed=0):
    out = ""; reg = []
    for i, (x, y, w, h, rot, layer) in enumerate(TPL[tpl]):
        if mirror: x, rot = 1080 - x - w, -rot
        kind, col = KINDS[(i * 5 + off) % len(KINDS)]
        if layer == "near": kind, col = ("orange", None) if i % 2 else ("blue", None)
        sd = 500 + off * 31 + i * 7 + seed
        rel, pad = p7lib.make_piece(w, h, kind, col or CRM, sd, 13, True, "tblr", rimw=7)
        fl = {"far": "filter:blur(1.4px) brightness(.9);", "mid": "filter:brightness(1);", "near": "filter:blur(5px) brightness(.8);"}[layer]
        ex = ""
        if i % 3 == 0 and layer != "near": ex += tape(f"{sid}_{i}tp", int(w * .4), -14, (-6, 5, -3)[i % 3], seed=off + i)
        if i % 4 == 1 and layer == "mid":
            tx, col2, r2 = STAMPS[(i + off) % len(STAMPS)]
            ex += stamp(f"{sid}_{i}st", tx, int(w * .12), int(h * .3), r2, 38, col2, "AB"[i % 2], .55 + .1 * (i % 3), box=True, z=4)
        out += (f'<div class="dc L{layer}" id="{sid}_{i}" data-decor style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);{fl}">'
                f'<img class="pbg" src="{rel}" style="left:{-pad}px;top:{-pad}px;width:{w + 2 * pad}px;height:{h + 2 * pad}px">{ex}</div>')
        reg.append((f"{sid}_{i}", layer, x, y, rot))
    SSET[sid] = reg
    return f'<div class="sset" id="ss_{sid}" data-decor>{out}</div>'

fgl = "".join(f'<img class="fgs" id="fg{i}" data-decor src="assets/p6/fg{i}.png">' for i in range(3))
flyers = "".join(f'<div class="dc fly" id="fl{i}" data-decor style="left:0;top:0;width:{w}px;height:{h}px">{pimg(w, h, kk, CRM, 300 + i, 9)}</div>'
                 for i, (w, h, kk) in enumerate(((240, 160, "news"), (280, 180, "ticket"), (200, 140, "red"), (260, 170, "news2"), (220, 150, "orange"), (190, 130, "map"))))

SSH = {"s1": scrapset("s1", "A", 0), "s2": scrapset("s2", "B", 3), "s3": scrapset("s3", "C", 5), "p1": scrapset("p1", "D", 2), "p2": scrapset("p2", "E", 6, True), "p3": scrapset("p3", "A", 8, True),
       "p4": scrapset("p4", "B", 1, True), "s5": scrapset("s5", "C", 7, True), "s6": scrapset("s6", "D", 4, True), "s6b": scrapset("s6b", "C", 12, False, 77), "s7": scrapset("s7", "E", 9), "s2b": scrapset("s2b", "D", 13, True, 31), "s7b": scrapset("s7b", "A", 14, True, 53), "sH": scrapset("sH", "A", 0)}

def usheet(i): return f'<img class="ush" id="ush{i}" data-decor src="assets/p6/sheet{i % 2}.png">'

markup = f'''
<svg width="0" height="0" style="position:absolute"><defs>
<filter id="ink" x="-3%" y="-8%" width="106%" height="116%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3" result="w"/><feDisplacementMap in="SourceGraphic" in2="w" scale="3.6" xChannelSelector="R" yChannelSelector="G" result="d"/>
<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="8" result="g"/><feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  3.4 0 0 0 -0.62" result="m"/><feComposite in="d" in2="m" operator="in"/></filter>
<filter id="rough" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="2" seed="5" result="w"/><feDisplacementMap in="SourceGraphic" in2="w" scale="5" xChannelSelector="R" yChannelSelector="G"/></filter>
<filter id="stA" x="-5%" y="-10%" width="110%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves="2" seed="4" result="g"/><feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  4.2 0 0 0 -1.05" result="m"/><feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="2" result="w"/><feDisplacementMap in="SourceGraphic" in2="w" scale="4" xChannelSelector="R" yChannelSelector="G" result="d"/><feComposite in="d" in2="m" operator="in"/></filter>
<filter id="stB" x="-5%" y="-10%" width="110%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.45" numOctaves="3" seed="12" result="g"/><feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  5 0 0 0 -1.5" result="m"/><feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="2" seed="6" result="w"/><feDisplacementMap in="SourceGraphic" in2="w" scale="5" xChannelSelector="R" yChannelSelector="G" result="d"/><feComposite in="d" in2="m" operator="in"/></filter>
</defs></svg>
<div id="world">
<div class="bgl" id="bgl" data-decor><img class="bgimg" id="bgimg" src="assets/p7/bg_card.jpg"></div>
<div id="flys" data-decor>{flyers}</div>
<div class="sc" id="s1" style="opacity:1;visibility:visible">{SSH["s1"]}{hookblock("", "A")}</div>
<div class="sc" id="s2">{SSH["s2"]}{SSH["s2b"]}<div class="cam" id="c2">{usheet(2)}
 {strip("t2", "ONLY IF YOU TAPPED", 60, 300, 940, 150, 1.6, ("red", None), "#f7efdc", "IDisp", 84, 11, 5, ls=-.02)}
 {P('<div class="mp"></div>', "dlg2", 120, 520, 880, 660, -1.2, "card", WHT, 12, 9, 2)}
 <div id="stk">{print_("cat", "d1", 190, 566, 240, 320, -10, 3, "", False, 51)}{print_("dog", "d2", 390, 540, 260, 340, 3, 3, "", False, 52)}{print_("bikes", "d3", 600, 566, 240, 320, 11, 3, "", False, 53)}</div>
 {strip("nb", "Not now", 160, 940, 280, 190, 0, ("card", (216, 207, 184)), "#5d554a", "IDisp", 54, 21, z=4)}
 {strip("b2", "ALLOW", 470, 930, 470, 210, -1.5, ("card", BLK), "#f1e8d2", "BS", 190, 22, z=5)}
 <div class="ring" id="ring"></div><div class="fing" id="fing"></div></div></div>
<div class="sc" id="s3">{SSH["s3"]}<div class="cam" id="c3">
 {strip("t3a", "HERE'S HOW", 90, 304, 900, 178, -1.2, ("card", YEL), size=150, seed=31, z=5)}
 {strip("t3b", "to stop it", 230, 500, 640, 160, 1.6, ("card", BLK), "#f1e8d2", "Gloock", 124, 32, z=6)}
 {P(bigtoggle("bigtg", 70, 35, 700, 330, True), "tgp", 110, 690, 860, 400, -.8, "card", WHT, 33, 9, 2)}
 {strip("tlab", "Camera roll sharing suggestions", 90, 1120, 900, 80, 0.8, ("orange", None), "#17130F", "PlexM", 32, 34, z=5)}</div></div>
{stepscene(1, ["PROFILE", "PICTURE"], 110, 380, (-1.5, 1.2))}
{stepscene(2, ["SETTINGS &amp;", "PRIVACY"], 730, 120, (1.4, -1.0))}
{stepscene(3, ["SETTINGS"], 120, 400, (-1.2,))}
{stepscene(4, ["CAMERA ROLL", "SHARING", "SUGGESTIONS"], 740, 90, (1.3, -1.1, 1.0))}
<div class="sc" id="s5">{SSH["s5"]}<div class="cam" id="c5">
 {strip("t5", "SWITCH IT OFF", 90, 300, 900, 170, -1.2, ("card", YEL), size=150, seed=51, z=5)}
 {P(bigtoggle("bigtg2", 50, 50, 780, 420, True), "tgp2", 100, 520, 880, 520, .6, "card", WHT, 52, 9, 2)}
 <div class="burst" id="burst"></div>
 <div class="offst" id="offw"><span class="scr" id="scr0">X#7</span><span class="scr" id="scr1">0F?</span><span class="scr" id="scr2">OF#</span><span class="offf" id="offf">OFF</span></div></div></div>
<div class="sc" id="s6">{SSH["s6"]}{SSH["s6b"]}<div class="cam" id="c6">{usheet(1)}
 {strip("t6a", "META SAYS", 290, 296, 500, 110, -2, ("card", BLK), "#f1e8d2", "Gloock", 70, 61, z=6)}
 {P('<div class="optin" id="optin">OPT-IN</div>', "pin6", 110, 440, 860, 420, -1, "news", CRM, 62, 10, 3)}
 {strip("t6b", "NOT USED FOR ADS", 90, 890, 900, 150, 1.0, ("card", YEL), size=120, seed=63, z=5)}
 {strip("t6c", "Meta newsroom, April 2026 · EU and UK", 140, 1090, 800, 64, -0.6, ("news", None), "#3b342a", "IDisp", 30, 64, z=4)}</div></div>
<div class="sc" id="s7">{SSH["s7"]}{SSH["s7b"]}<div class="cam" id="c7">{usheet(3)}
 {strip("t7a", "SEND THIS TO SOMEONE", 90, 292, 900, 120, -1.0, ("card", YEL), size=92, seed=71, z=5)}
 {strip("t7b", "who always taps Allow", 120, 426, 840, 120, 1.0, ("card", BLK), "#f1e8d2", "Gloock", 76, 72, z=6)}
 {chat()}</div></div>
<div class="sc" id="sH">{SSH["sH"]}{hookblock("H", "A")}</div>
<div id="fgl" data-decor>{fgl}</div>
</div>
<img class="sheet" id="sheetA" data-decor src="assets/p6/sheet0.png"><img class="sheet" id="sheetB" data-decor src="assets/p6/sheet1.png">
<div class="grainw" data-decor><img class="grain" id="grain" data-decor src="assets/p6/grain.jpg"></div>
'''
for k_, v_ in list(SSH.items()):
    pass
for n_ in (1, 2, 3, 4):
    markup = markup.replace(f"__SS_p{n_}__", SSH[f"p{n_}"])
