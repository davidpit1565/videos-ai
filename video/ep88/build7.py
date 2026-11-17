#!/usr/bin/env python3
"""ep88 round 6 builder (torn-paper collage with real scans, high motion density): fast top-funnel cut. lines5.txt (7 lines) + VOICE/<n>.wav -> cues7.json, out/narration7.wav, sfx5.json, hf/index.html [--render name].
Fonts: Big Shoulders Bold (hero, condensed), Fraunces 600 (contrast serif), Inter Display (UI). All open licence (SIL OFL)."""
import json, os, re, sys, subprocess
import soundfile as sf, numpy as np
H = os.path.dirname(os.path.abspath(__file__))
VOICE = os.environ.get("VOICE", H + "/voice5/final")
GAPS = [float(x) for x in os.environ.get("GAPS", "0.3,0.28,0.85,0.3").split(",")]
TAIL = float(os.environ.get("TAIL", "1.4"))
ALL = [l.rstrip("\n") for l in open(H + "/lines5.txt") if l.strip()]
assert len(ALL) == 5 and len(GAPS) == 4
sr = 48000
src = open(H + "/build_head.py").read()
exec(src[src.index("def words_for"):src.index("lines = []; t = 0.0")])   # reuse words_for

import hashlib
def whisper_words(path, text, t0):
    """real word stamps from faster-whisper (small) when the word count matches the script; None otherwise"""
    cache = H + "/voice5/words-cache.json"
    c = json.load(open(cache)) if os.path.exists(cache) else {}
    key = hashlib.md5(open(path, "rb").read()).hexdigest()
    if key not in c:
        out = subprocess.run(["/opt/v311/bin/python", "-c", "import sys,json;from faster_whisper import WhisperModel;m=WhisperModel('small',device='cpu',compute_type='int8');seg,_=m.transcribe(sys.argv[1],language='en',word_timestamps=True);print(json.dumps([[w.word.strip(),w.start,w.end] for s in seg for w in (s.words or [])]))", path], capture_output=True, text=True).stdout
        try: c[key] = json.loads(out.strip().splitlines()[-1])
        except Exception: c[key] = []
        json.dump(c, open(cache, "w"))
    ws = c[key]
    return [[round(t0 + a, 3), round(t0 + b, 3)] for _, a, b in ws] if len(ws) == len(text.split()) else None

lines = []; t = 0.0; parts = []
for j in range(5):
    n = j + 1
    x, s = sf.read(f"{VOICE}/{n}.wav"); assert s == sr; x = x if x.ndim == 1 else x[:, 0]
    d = len(x) / sr
    wf = whisper_words(f"{VOICE}/{n}.wav", ALL[j], t)
    print('line', n, 'whisper word stamps' if wf else 'sentence-silence estimate')
    lines.append(dict(n=n, text=ALL[j], start=round(t, 3), end=round(t + d, 3), words=wf or words_for(x, ALL[j], t)))
    parts.append((int(t * sr), x)); t += d + (GAPS[j] if j < 4 else 0)
D = round(lines[-1]["end"] + TAIL, 2)
nar = np.zeros(int((D + 0.3) * sr))
for i0, x in parts: nar[i0:i0 + len(x)] += x
os.makedirs(H + "/out", exist_ok=True)
sf.write(H + "/out/narration7.wav", nar[:int(D * sr)], sr, subtype="PCM_16")
json.dump(dict(lines=lines, D=D), open(H + "/cues7.json", "w"), indent=1)
S = lambda n: lines[n - 1]["start"]
E = lambda n: lines[n - 1]["end"]
W = lambda n, i: lines[n - 1]["words"][i][0]

# ---- scene boundaries (all derived from the voice)
B = dict(s1=0.0, s2=S(2) - .05, s3=W(2, 5) - .05, p1=S(3) - .05, p2=W(3, 2) - .05, p3=W(3, 5) - .35, p4=W(3, 6) - .08,
         s5=W(3, 10) - .05, s6=S(4) - .05, s7=S(5) - .05, end=E(5) + .25, loop=E(5) + .45)
T = dict(B)
T.update(dict(tapAllow=W(2, 3), flip=W(3, 12) - .12, slam1=W(1, 6)))
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

styles = r'''
@font-face{font-family:"BS";src:url("assets/fonts/BigShoulders-Bold.ttf");font-weight:700}
@font-face{font-family:"Gloock";src:url("assets/fonts/Gloock-Regular.ttf")}
@font-face{font-family:"PlexM";src:url("assets/fonts/IBMPlexMono-Bold.ttf");font-weight:700}
:root{--ink:#17130F;--yel:#F2C230;--red:#B6402B;--lime:#9BE22E}
html,body,#root{background:#8c6f48}
#world{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 960px}
.bgl{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden;background:#a07f52}
.bgimg{position:absolute;left:-900px;top:0;width:2880px;height:1920px}
#flys,#fgl{position:absolute;left:0;top:0;width:1080px;height:1920px;pointer-events:none}
.sset{position:absolute;left:0;top:0;width:1080px;height:1920px;pointer-events:none}
.dc{position:absolute}
.dc.fly{opacity:0}
.fgs{position:absolute;left:0;top:0;opacity:0}
.sc{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0;visibility:hidden}
.cam{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}
.pcw{position:absolute}
.pbg{position:absolute;max-width:none;pointer-events:none}
.stx{position:absolute;left:50%;transform:translateX(-50%);top:0;width:auto;height:100%;white-space:nowrap;letter-spacing:-.005em;text-transform:uppercase;font-weight:700;filter:url(#ink);text-shadow:1.7px 1.2px 0 rgba(182,64,43,.34)}
.stx.dk{mix-blend-mode:multiply}
.stx.lt{text-shadow:1.4px 1px 0 rgba(0,0,0,.3)}
.stx[style*="Gloock"]{text-transform:none;letter-spacing:-.01em}
.stx[style*="PlexM"]{letter-spacing:-.02em}
.rl .stx{text-transform:none!important}
.tape{position:absolute;max-width:none;z-index:12}
.phimg{position:absolute;max-width:none;object-fit:cover}
.pvig{position:absolute;background:radial-gradient(120% 90% at 50% 40%,transparent 60%,rgba(0,0,0,.3))}
.stp{position:absolute;white-space:nowrap;mix-blend-mode:multiply;letter-spacing:.06em;text-transform:uppercase}
.inkA{filter:url(#stA)}.inkB{filter:url(#stB)}.inkAB{filter:url(#stA)}
.fbs{position:absolute;z-index:20;border-radius:50%;background:#fff;box-shadow:0 0 0 6px #fff,0 8px 20px rgba(30,18,6,.45);overflow:hidden}.fbs img{width:100%;height:100%;padding:6px}
.pnum{position:absolute;top:340px;font:700 440px BS;line-height:400px;color:var(--red);opacity:.95;letter-spacing:-.02em;mix-blend-mode:multiply;filter:url(#ink)}
.of4{position:absolute;top:302px;font:700 26px PlexM;letter-spacing:.1em;color:#3b2a14}
.uibody{position:absolute;left:26px;top:24px;right:26px;bottom:28px;background:#f4f1e8;border-radius:22px;overflow:hidden;filter:sepia(.3) contrast(1.12) saturate(.85)}
.copy{position:absolute;left:26px;top:24px;right:26px;bottom:28px;border-radius:22px;pointer-events:none;
 background:radial-gradient(circle at 2.5px 2.5px,rgba(20,16,12,.22) 1.1px,transparent 1.6px) 0 0/5px 5px,linear-gradient(90deg,rgba(0,0,0,.09),transparent 7%,transparent 93%,rgba(0,0,0,.1)),linear-gradient(0deg,rgba(0,0,0,.07),transparent 14%);mix-blend-mode:multiply}
.mkw{position:absolute;z-index:30;pointer-events:none}
.uihd{position:absolute;left:30px;top:26px;font:800 44px IDisp;color:#1b1814}
.uir{position:absolute;left:24px;right:24px;height:106px;display:flex;align-items:center;justify-content:space-between;padding:0 22px;font:700 40px IDisp;color:#34302a;border-bottom:2px solid rgba(40,34,26,.18);gap:14px}
.uir.hot{background:rgba(242,194,48,.6);border-radius:10px;color:#17130F;border-bottom-color:transparent}
.uil{white-space:nowrap;flex:1}
.chev{font:400 60px IDisp;color:#6d6558;line-height:60px}
.fbtop{position:absolute;left:0;top:0;width:100%;height:130px;background:#ece7d8;border-bottom:2px solid rgba(40,34,26,.2)}
.fbsm{position:absolute;left:28px;top:20px;width:90px;height:90px;border-radius:50%;background:#fff;overflow:hidden}.fbsm img{width:100%;height:100%;padding:4px}
.ico{position:absolute;top:34px;width:62px;height:62px;border-radius:50%;background:#cfc7b3}.ico:nth-of-type(1){right:262px}.ico:nth-of-type(2){right:186px}
.avt{position:absolute;right:46px;top:12px;width:106px;height:106px;border-radius:50%;background:linear-gradient(160deg,#C99A62,#8C5A2B);overflow:hidden}
.avh{position:absolute;left:33px;top:20px;width:40px;height:40px;border-radius:50%;background:#F5E7CB}.avb{position:absolute;left:18px;top:64px;width:70px;height:56px;border-radius:50% 50% 0 0;background:#F5E7CB}
.comp{position:absolute;left:20px;right:20px;top:146px;height:76px;display:flex;align-items:center;gap:16px;font:600 32px IDisp;color:#6d6558;border-bottom:2px solid rgba(40,34,26,.16)}
.cav{width:56px;height:56px;border-radius:50%;background:#c9bda3}
.feedimg{position:absolute;left:0;top:232px;width:100%;height:240px;object-fit:cover}
.tapr{position:absolute;right:120px;top:130px;width:90px;height:90px;border-radius:50%;border:8px solid var(--red);opacity:0}
.tg2{position:relative;width:132px;height:74px;border-radius:37px;background:#CBBFA3;flex:none}
.tg2 i{position:absolute;left:4px;top:4px;width:66px;height:66px;border-radius:50%;background:#fff;box-shadow:0 4px 10px rgba(14,14,14,.35)}
.tg2.on{background:#2a2118}.tg2.on i{left:auto;right:4px}
.uinote{position:absolute;left:0;width:100%;top:318px;text-align:center;font:700 22px PlexM;color:#4a3a26}
.btg{position:absolute;background:#CBBFA3;box-shadow:inset 0 -10px 0 rgba(0,0,0,.10)}
.btg i{position:absolute;left:24px;top:24px;border-radius:50%;background:#fff;box-shadow:0 12px 26px rgba(14,14,14,.4)}
.btg.on{background:#2a2118}.btg.on i{left:auto;right:24px}
.mini{position:absolute;inset:0;display:flex;align-items:center;justify-content:space-between;padding:0 50px;gap:20px}
.mini b{font:700 68px BS;line-height:68px;text-transform:uppercase;filter:url(#ink)}
.mini .tg2{width:190px;height:106px;border-radius:53px}.mini .tg2 i{width:94px;height:94px}
.mp{position:absolute;inset:0}
.optin{position:absolute;left:0;top:0;width:100%;height:100%;font:400 232px Gloock;line-height:430px;text-align:center;color:var(--ink);letter-spacing:-.03em;filter:url(#ink);mix-blend-mode:multiply}
.offst{position:absolute;left:90px;top:1050px;width:900px;height:140px;text-align:center;font-family:BS;font-weight:700;font-size:170px;line-height:140px}
.offst span{position:absolute;left:0;width:100%;top:0;opacity:0}
.offf{background:var(--lime);color:var(--ink);border:8px solid var(--ink);border-radius:30px;padding:0 60px;width:auto!important;left:50%!important;transform:translateX(-50%) rotate(-4deg)!important;box-shadow:8px 10px 0 var(--ink)}
.offst .scr{color:#4a3a26}
.burst{position:absolute;left:340px;top:640px;width:400px;height:400px;border-radius:50%;background:radial-gradient(circle,rgba(30,18,6,.55) 2.4px,transparent 3px) 0 0/16px 16px;-webkit-mask-image:radial-gradient(circle,transparent 30%,#000 60%,transparent 100%);opacity:0}
.mavt{position:absolute;left:100px;top:1080px;width:120px;height:120px;border-radius:50%;background:var(--yel);font:700 90px BS;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 6px #fff,0 8px 20px rgba(30,18,6,.45);opacity:0}
.dots2{position:absolute;left:250px;top:1086px;width:230px;height:112px;background:#FBF8EF;border-radius:50px 50px 50px 12px;box-shadow:0 8px 18px rgba(30,18,6,.4);display:flex;align-items:center;justify-content:center;gap:18px;opacity:0}
.dots2 i{display:block;width:26px;height:26px;border-radius:50%;background:var(--ink)}
.ring{position:absolute;left:760px;top:940px;width:110px;height:110px;border-radius:50%;border:10px solid var(--red);opacity:0;z-index:30}
.fing{position:absolute;left:780px;top:1020px;width:100px;height:100px;border-radius:50%;background:rgba(23,19,15,.8);opacity:0;z-index:30}
.sheet{position:absolute;left:0;top:-120px;width:1470px;height:2290px;max-width:none;z-index:80;opacity:0;pointer-events:none}
.ush{position:absolute;left:0;top:-120px;width:1470px;height:2290px;max-width:none;z-index:4;opacity:0;pointer-events:none}
.grainw{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden;z-index:90;pointer-events:none}
.grain{position:absolute;left:-40px;top:-40px;width:1160px;height:2000px;max-width:none;mix-blend-mode:overlay;opacity:.24;pointer-events:none}
'''

# ------------------------------------------------------------ timeline (generated)
D_ = D
rnd = _r.Random(7)
def at(t): return tt(t)

def slam(sel, t, dx=0, dy=0, rot=0, s0=1.35, dur=.3, typed=False):
    """text-safe entrance: torn-paper wipe (clip reveal) at the final position + tiny slam; the text box never leaves the safe area"""
    wid, hei = REG.get(sel[1:], (900, 130))
    sx = min(s0, 1.06); ox = max(-40, min(40, dx * .2)); oy = max(-18, min(18, dy * .15))
    L = [-60, -60, -60, -60]
    if dy < 0 and abs(dy) >= abs(dx): L[2] = hei + 60
    elif dy > 0 and abs(dy) > abs(dx): L[0] = hei + 60
    elif dx > 0: L[3] = wid + 60
    else: L[1] = wid + 60
    st = " ".join(f"{v}px" for v in L)
    js(f"tl.fromTo('{sel}',{{clipPath:'inset({st})',x:{ox},y:{oy},scale:{sx},rotation:'+={rot * .5}'}},{{clipPath:'inset(-60px -60px -60px -60px)',x:0,y:0,scale:1,rotation:'-={rot * .5}',duration:{dur},ease:'expo.out',transformOrigin:'50% 50%'}},{at(t)});")

def settle(sel, t, dx=0, dy=0, rot=0, s0=1.05, dur=.4):
    js(f"tl.fromTo('{sel}',{{x:{dx},y:{dy},scale:{s0},rotation:'+={rot}'}},{{x:0,y:0,scale:1,rotation:'-={rot}',duration:{dur},ease:'expo.out',transformOrigin:'50% 50%'}},{at(t)});")

def drop(sel, t, dy=-420, dx=0, s0=1, dur=.5, ease="back.out(1.25)", rot=0):
    js(f"tl.fromTo('{sel}',{{y:{dy},x:{dx},scale:{s0},opacity:1,rotation:'+={rot}'}},{{y:0,x:0,scale:1,rotation:'-={rot}',duration:{dur},ease:'{ease}',transformOrigin:'50% 50%'}},{at(t)});")

def tapeslap(sel, t):
    js(f"tl.fromTo('{sel}',{{scale:1.7,opacity:0}},{{scale:1,opacity:.86,duration:.14,ease:'power3.in'}},{at(t)});")

def thump(sel, t, s0=2.1, op=.9, dur=.16):
    js(f"tl.fromTo('{sel}',{{scale:{s0},opacity:0}},{{scale:1,opacity:{op},duration:{dur},ease:'power4.in',transformOrigin:'50% 50%'}},{at(t)});")

def fly(i, t, y0, y1, dirn=1, dur=.7, rot0=-25, rot1=15, s=1):
    x0, x1 = (1250, -420) if dirn > 0 else (-420, 1250)
    js(f"tl.fromTo('#fl{i}',{{x:{x0},y:{y0},rotation:{rot0},opacity:1,scale:{s}}},{{x:{x1},y:{y1},rotation:{rot1},duration:{dur},ease:'power1.inOut'}},{at(t)});")
    js(f"tl.set('#fl{i}',{{opacity:0}},{at(t + dur + .02)});")
    sfx("whoosh_c.ogg", t + .05, -9)

def fgcross(i, t, y, dur=1.0, dirn=1):
    x0, x1 = (1300, -700) if dirn > 0 else (-700, 1300)
    js(f"tl.fromTo('#fg{i}',{{x:{x0},y:{y},rotation:-8,opacity:1}},{{x:{x1},y:{y + 40},rotation:10,duration:{dur},ease:'sine.inOut'}},{at(t)});")
    js(f"tl.set('#fg{i}',{{opacity:0}},{at(t + dur + .02)});")

def swap(old, new, t, k):
    """newsprint sheet sweeps over the whole frame (alternating direction); scenes swap while it covers the picture (no blank dips)"""
    sh = "sheetA" if k % 2 == 0 else "sheetB"
    r = (-2.5, 2.0, -1.5)[k % 3]
    xa, xb = (1160, -1560) if k % 2 == 0 else (-1560, 1160)
    js(f"tl.fromTo('#{sh}',{{x:{xa},y:{[-80, -140, -30][k % 3]},rotation:{r},opacity:1}},{{x:{xb},y:{[-120, -60, -100][k % 3]},rotation:{-r},duration:.22,ease:'power2.inOut'}},{at(t - .11)});")
    js(f"tl.set('#{sh}',{{opacity:0}},{at(t + .13)});")
    if old: js(f"tl.set('#{old}',{{autoAlpha:0}},{at(t - .02)});")
    js(f"tl.set('#{new}',{{autoAlpha:1}},{at(t - .01)});")
    sfx(("whoosh_b.ogg", "whoosh_a.ogg")[k % 2], t - .13, -2)

def usweep(ush, t, k, mid=None):
    """sweep UNDER the strips: the strips stay readable while the picture behind them changes. mid = callable(t_cover) schedules the swap"""
    xa, xb = (1160, -1560) if k % 2 == 0 else (-1560, 1160)
    r = (-2.0, 1.6)[k % 2]
    js(f"tl.fromTo('#{ush}',{{x:{xa},y:-100,rotation:{r},opacity:1}},{{x:{xb},y:-80,rotation:{-r},duration:.24,ease:'power2.inOut'}},{at(t)});")
    js(f"tl.set('#{ush}',{{opacity:0}},{at(t + .26)});")
    sfx("whoosh_a.ogg" if k % 2 == 0 else "whoosh_b.ogg", t, -2)
    if mid: mid(t + .12)

def cam(cid, t0, t1, s0=1.0, s1=1.025, r0=0, r1=0, x0=0, x1=0, y0=0, y1=0, org="540px 760px"):
    js(f"tl.fromTo('#{cid}',{{scale:{s0},rotation:{r0},x:{x0},y:{y0}}},{{scale:{s1},rotation:{r1},x:{x1},y:{y1},duration:{max(.3, t1 - t0):.3f},ease:'sine.inOut',transformOrigin:'{org}'}},{at(t0)});")

def scraps(sid, s, e, final=False, entrance=True):
    """3 depth layers: far/mid/near drift at different speeds; entrance = every scrap slaps down (scale 1.14 -> 1) a few frames apart"""
    spd = {"far": 14, "mid": 30, "near": 64}
    for i, (eid, layer, x, y, rot) in enumerate(SSET[sid]):
        dx = rnd.choice((-1, 1)) * spd[layer] * rnd.uniform(.6, 1.0); dy = rnd.choice((-1, 1)) * spd[layer] * rnd.uniform(.3, .8); dr = rnd.uniform(.6, 1.6) * rnd.choice((-1, 1))
        dur = (e - s) + .6
        if final:
            js(f"tl.fromTo('#{eid}',{{x:{dx:.1f},y:{dy:.1f},rotation:{rot + dr:.2f}}},{{x:{-dx:.1f},y:{-dy:.1f},rotation:{rot - dr:.2f},duration:{dur:.3f},ease:'sine.out'}},{at(s)});")
        else:
            js(f"tl.fromTo('#{eid}',{{x:{-dx:.1f},y:{-dy:.1f},rotation:{rot - dr:.2f}}},{{x:{dx:.1f},y:{dy:.1f},rotation:{rot + dr:.2f},duration:{dur:.3f},ease:'none'}},{at(s)});")
        if entrance and not final and sid != "s1":
            js(f"tl.fromTo('#{eid}',{{scale:1.14}},{{scale:1,duration:.42,ease:'expo.out',transformOrigin:'50% 50%'}},{at(s + .02 + i * .045)});")
            if i % 3 == 0: sfx("tick.ogg", s + .04 + i * .045, -8)

# --- global
js(f"tl.fromTo('#world',{{scale:1,rotation:-.25}},{{scale:1.014,rotation:.25,duration:{D_ / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1,transformOrigin:'540px 960px'}},0);")
js(f"tl.fromTo('#bgimg',{{x:0}},{{x:-300,duration:{D_ / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},0);")
g_t = 0.0
while g_t < D_:
    js(f"tl.set('#grain',{{x:{rnd.randint(-30, 30)},y:{rnd.randint(-30, 30)}}},{at(g_t)});"); g_t += 1 / 12

# --- HOOK (frame 0 is settled and readable: only small settles, nothing fades in)
t0 = 0.0
settle("#hA", t0, dx=-26, rot=.8, s0=1.03); settle("#hB", t0 + .05, dx=26, rot=-.8, s0=1.03)
js(f"tl.fromTo('#fbs',{{scale:.8,rotation:-30}},{{scale:1,rotation:-8,duration:.5,ease:'back.out(2.2)'}},{at(t0)});")
nl = 11
for k in range(nl):
    js(f"tl.fromTo('#rl{k}',{{scale:1.16,rotation:'+={(-1) ** k * 5}'}},{{scale:1,rotation:'-={(-1) ** k * 5}',duration:.42,ease:'expo.out',transformOrigin:'50% 50%'}},{at(t0 + .03 * k)});")
    js(f"tl.to('#rl{k}',{{y:{(-1) ** k * 5},duration:.9,ease:'sine.inOut',yoyo:true,repeat:2}},{at(t0 + .6 + .05 * k)});")
for sel, dy0, rr_ in (("pa", 40, -8), ("pc", 46, 8), ("pb", 30, -3)):
    drop(f"#{sel}", t0, dy=dy0, dur=.5, ease="power3.out", rot=rr_)
for j, tp_ in enumerate(("pa", "pb", "pc")):
    tapeslap(f"#{tp_}tp", t0 + .38 + j * .09); sfx("tick.ogg", t0 + .38 + j * .09, -4)
thump("#stH", t0 + .7, 1.8, .8, .16); sfx("pop_a.ogg", t0 + .72, -4)
sfx("impactpunch.ogg", t0 + .04, 0); sfx("subhit.ogg", t0 + .04, -3); sfx("whoosh_a.ogg", t0, -2)
js(f"tl.set('#hcam',{{x:0}},0);")
# hero swap under a sweep (strips + ransom row stay readable)
sw = W(1, 5) - .25
def hero_swap(tc):
    js(f"tl.set(['#pa','#pb','#pc'],{{autoAlpha:0}},{at(tc)});")
    for nm in ("pax", "pbx", "pcx"):
        js(f"tl.set('#{nm}',{{autoAlpha:1}},{at(tc)});")
    for j, nm in enumerate(("pax", "pbx", "pcx")):
        js(f"tl.fromTo('#{nm}',{{scale:1.12,rotation:'+={(-6, 4, 6)[j]}'}},{{scale:1,rotation:'-={(-6, 4, 6)[j]}',duration:.4,ease:'expo.out',transformOrigin:'50% 50%'}},{at(tc + .02 + j * .05)});")
        tapeslap(f"#{nm}tp", tc + .15 + j * .07)
    sfx("impactsoft.ogg", tc + .08, -3)
js(f"tl.set(['#pax','#pbx','#pcx'],{{autoAlpha:0}},0);")
usweep("ush0", sw, 0, hero_swap)
thump("#stHx", W(1, 6) + .02, 2.1, .92, .18); sfx("impactpunch.ogg", W(1, 6) + .04, -2)
for j in range(2):
    js(f"tl.to('#hA',{{y:-5,duration:.6,ease:'sine.inOut',yoyo:true,repeat:1}},{at(.7 + j * 1.3)});")
fly(0, .35, 1380, 1480, 1, .8); fly(1, .95, 1600, 1520, -1, .8, 20, -10)
fgcross(0, 1.7, 1420, 1.0, 1); fly(2, 2.05, 1330, 1450, 1, .7)
cam("hcam", 0, T["s2"] + .1, 1.0, 1.03, -.4, .5)
scraps("s1", 0, T["s2"] + .1, entrance=False)
sfx("click_a.ogg", T["slam1"], -4)

# --- S2
s = T["s2"]; swap("s1", "s2", s, 0); scraps("s2", s, T["s3"])
slam("#t2", s + .02, dx=300, rot=2, s0=1.1, dur=.38); sfx("impactsoft.ogg", s + .1, -6)
slam("#dlg2", s + .1, dy=300, rot=-1, s0=1.06, dur=.45); sfx("pop_b.ogg", s + .5, -3)
for j, d in enumerate(("d1", "d2", "d3")):
    drop(f"#{d}", s + .3 + j * .12, dy=-340, dx=(-40, 0, 40)[j], dur=.4, ease="power3.out", rot=(-12, 6, 14)[j]); sfx("tick.ogg", s + .6 + j * .12, -3)
slam("#nb", s + .62, dx=-320, s0=1.0, dur=.3)
slam("#b2", s + .74, dx=0, dy=-40, rot=-3, s0=1.06, dur=.34); sfx("impactsoft.ogg", s + .85, -5)
js(f"tl.fromTo('#fing',{{opacity:0,y:60}},{{opacity:1,y:0,duration:.4,ease:'power2.out'}},{at(T['tapAllow'] - .4)});")
js(f"tl.to('#b2',{{scale:.93,duration:.14,ease:'sine.inOut',transformOrigin:'50% 50%'}},{at(T['tapAllow'])});")
js(f"tl.fromTo('#ring',{{opacity:.95,scale:.5}},{{opacity:0,scale:2.6,duration:.7,ease:'power2.out'}},{at(T['tapAllow'] + .02)});")
js(f"tl.to('#b2',{{scale:1,duration:.3,ease:'sine.inOut'}},{at(T['tapAllow'] + .14)});")
js(f"tl.to('#fing',{{opacity:0,duration:.3}},{at(T['tapAllow'] + .45)});")
sfx("select.ogg", T["tapAllow"], 0); sfx("pop_b.ogg", T["tapAllow"] + .06, -3)
fly(3, s + .5, 1370, 1300, -1, .8, 15, -20); fgcross(1, s + 1.3, 1500, 1.1, -1); fly(4, s + 1.8, 1560, 1640, 1, .7)
cam("c2", s, T["s3"], 1.0, 1.02, .6, -.3, 0, -12)
js("tl.set('#ss_s2b',{autoAlpha:0},0);")
def s2_swap(tc):
    js(f"tl.set('#ss_s2',{{autoAlpha:0}},{at(tc)});"); js(f"tl.set('#ss_s2b',{{autoAlpha:1}},{at(tc)});"); sfx("impactsoft.ogg", tc + .05, -5)
usweep("ush2", T["tapAllow"] + .55, 1, s2_swap); scraps("s2b", T["tapAllow"] + .7, T["s3"])

# --- S3
s = T["s3"]; swap("s2", "s3", s, 1); scraps("s3", s, T["p1"])
slam("#t3a", s + .02, dx=-300, rot=1, s0=1.1, dur=.38)
slam("#t3b", s + .18, dx=300, rot=-1, s0=1.1, dur=.38)
slam("#tgp", s + .3, dy=420, rot=1, s0=1.06, dur=.5); sfx("pop_b.ogg", s + .6, -3)
slam("#tlab", s + .55, dy=140, s0=1.0, dur=.35); sfx("tick.ogg", s + .7, -3)
js(f"tl.to('#bigtg i',{{x:-18,duration:.35,ease:'sine.inOut',yoyo:true,repeat:3}},{at(s + .9)});")
fly(5, s + .45, 1400, 1330, 1, .75); fgcross(2, s + .9, 1520, 1.0, 1)
sfx("toggle.ogg", s + .3, -8)
cam("c3", s, T["p1"], 1.03, 1.0, -.4, .3, 0, 0, 0, 0, "540px 900px")

# --- steps
steps = [("p1", "p2", "pc1", "pn1", ["sl10", "sl11"], "ui1", "mk1", "tapr1"), ("p2", "p3", "pc2", "pn2", ["sl20", "sl21"], "ui2", "mk2", "tapr2"),
         ("p3", "p4", "pc3", "pn3", ["sl30"], "ui3", "mk3", "tapr3"), ("p4", "s5", "pc4", "pn4", ["sl40", "sl41", "sl42"], "ui4", "mk4", "tapr4")]
CAMS = [dict(s0=1.0, s1=1.03, r0=.5, r1=-.4, org="300px 600px"), dict(s0=1.0, s1=1.025, r0=-.3, r1=.4, x0=10, x1=-10, y0=0, y1=-12), dict(s0=1.03, s1=1.0, r0=.4, r1=-.2), dict(s0=1.0, s1=1.03, x0=-12, x1=12)]
prev = "s3"
for i, (a, b, cm, pn, labs, ui, mk, tr) in enumerate(steps):
    s = T[a]; e = T[b]
    swap(prev, a, s, 2 + i); prev = a; scraps(a, s, e + .1)
    js(f"tl.fromTo('#{pn}',{{scale:1.25,opacity:0,x:-30}},{{scale:1,opacity:.95,x:0,duration:.34,ease:'expo.out',transformOrigin:'30% 50%'}},{at(s + .02)});")
    for j, l in enumerate(labs): slam("#" + l, s + .08 + j * .07, dx=(220, -220)[i % 2], rot=-1, s0=1.0, dur=.3)
    slam("#" + ui, s + .12, dy=90, rot=1, s0=1.05, dur=.4)
    js(f"tl.fromTo('#{mk} path',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.42,ease:'power2.inOut'}},{at(s + .5)});")
    js(f"tl.fromTo('#{tr}',{{opacity:.9,scale:.4}},{{opacity:0,scale:2.2,duration:.5,ease:'power2.out'}},{at(s + .5)});")
    sfx("tick.ogg", s + .5, -1); sfx("pop_b.ogg", s + .14, -6)
    if i % 2 == 0: fly(i, s + .25, 1360 + i * 20, 1420, 1, .7)
    else: fgcross(i % 3, s + .3, 1480, .9, -1)
    cam(cm, s, e + .1, **CAMS[i])
    if i == 3: js(f"tl.to('#{ui}',{{y:-6,duration:.9,ease:'sine.inOut'}},{at(s + .7)});")

# --- S5 OFF (the proof)
s = T["s5"]; swap("p4", "s5", s, 6); scraps("s5", s, T["s6"])
slam("#t5", s + .02, dy=-130, rot=-2, s0=1.1, dur=.36)
slam("#tgp2", s + .1, dy=360, rot=1, s0=1.06, dur=.5)
fl = T["flip"]
js(f"tl.to('#bigtg2 i',{{right:384,duration:.34,ease:'power3.inOut'}},{at(fl)});")
js(f"tl.to('#bigtg2',{{backgroundColor:'#9BE22E',duration:.34,ease:'power3.inOut'}},{at(fl)});")
js(f"tl.fromTo('#bigtg2',{{boxShadow:'0 0 0 0 rgba(155,226,46,.9)'}},{{boxShadow:'0 0 0 50px rgba(155,226,46,0)',duration:.6,ease:'power2.out',immediateRender:false}},{at(fl + .3)});")
js(f"tl.fromTo('#burst',{{opacity:.8,scale:.35}},{{opacity:0,scale:2.4,duration:.6,ease:'power2.out',transformOrigin:'50% 50%'}},{at(fl + .25)});")
for j in range(3):
    js(f"tl.set('#scr{j}',{{opacity:1}},{at(fl + .34 + j * .07)});"); js(f"tl.set('#scr{j}',{{opacity:0}},{at(fl + .34 + j * .07 + .07)});")
js(f"tl.fromTo('#offf',{{scale:1.5,opacity:0}},{{scale:1,opacity:1,duration:.34,ease:'expo.out',transformOrigin:'50% 50%'}},{at(fl + .55)});")
js(f"tl.to('#tgp2',{{y:-8,duration:{T['s6'] - T['s5']:.3f},ease:'sine.inOut'}},{at(s + .6)});")
sfx("toggle.ogg", fl + .22, 0); sfx("ding.ogg", fl + .32, -2); sfx("impactsoft.ogg", fl + .38, -5); sfx("pop_a.ogg", fl + .6, -3)
fly(0, fl + .1, 1300, 1560, 1, .6, -10, 30); fly(1, fl + .15, 1300, 1620, -1, .6, 10, -30); fly(2, fl + .2, 1320, 1700, 1, .7)
cam("c5", s, T["s6"], 1.0, 1.035, -.3, .4, 0, 0, 0, 0, "540px 880px")

# --- S6 Meta
s = T["s6"]; swap("s5", "s6", s, 7); scraps("s6", s, T["s7"])
slam("#t6a", s + .02, dy=-100, rot=2, s0=1.1, dur=.34)
slam("#pin6", s + .1, dy=60, rot=1, s0=1.06, dur=.42); sfx("pop_b.ogg", s + .45, -3)
js(f"tl.fromTo('#optin',{{scale:1.015}},{{scale:1,duration:.4,ease:'expo.out',transformOrigin:'50% 50%'}},{at(s + .3)});")
slam("#t6b", s + .6, dx=300, rot=-1, s0=1.0, dur=.34); sfx("impactsoft.ogg", s + .65, -6)
slam("#t6c", s + 1.0, dy=60, s0=1.0, dur=.3)
sfx("pop_a.ogg", W(4, 2), -3)
fly(3, s + .4, 1380, 1480, 1, .8); fgcross(0, s + .9, 1540, 1.1, -1); fly(4, s + 1.5, 1330, 1450, -1, .7, 10, -20)
cam("c6", s, T["s7"], 1.02, 1.0, -.5, .5)
js("tl.set('#ss_s6b',{autoAlpha:0},0);")
def s6_swap(tc):
    js(f"tl.set('#ss_s6',{{autoAlpha:0}},{at(tc)});"); js(f"tl.set('#ss_s6b',{{autoAlpha:1}},{at(tc)});")
    sfx("impactsoft.ogg", tc + .05, -5)
usweep("ush1", s + 1.55, 1, s6_swap); scraps("s6b", s + 1.7, T["s7"])

# --- S7 send
s = T["s7"]; swap("s6", "s7", s, 8); scraps("s7", s, T["end"])
slam("#t7a", s + .02, dx=-280, rot=1, s0=1.1, dur=.34); slam("#t7b", s + .16, dx=280, rot=-1, s0=1.1, dur=.34)
slam("#outb", s + .3, dx=300, rot=3, s0=1.06, dur=.4); sfx("pop_b.ogg", s + .65, -3)
js(f"tl.fromTo('#mav',{{opacity:0,scale:.5}},{{opacity:1,scale:1,duration:.38,ease:'back.out(2)'}},{at(s + 1.0)});")
js(f"tl.fromTo('#dots2',{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.3,ease:'power2.out'}},{at(s + 1.1)});")
js(f"tl.to('#dots2 i',{{y:-10,duration:.26,ease:'sine.inOut',yoyo:true,repeat:3,stagger:.09}},{at(s + 1.2)});")
js(f"tl.to('#dots2',{{opacity:0,duration:.16}},{at(s + 1.72)});")
for k in (1, 2, 3):
    slam(f"#al{k}", s + 1.78 + (k - 1) * .26, dy=-70, rot=(4, -4, 4)[k - 1], s0=1.06, dur=.3); sfx("pop_b.ogg", s + 1.9 + (k - 1) * .26, -3)
sfx("riser.ogg", s - 2.2, -7); sfx("ding.ogg", E(5) - .1, -6)
fly(5, s + .5, 1350, 1440, 1, .8); fgcross(1, s + 1.2, 1520, 1.0, 1)
cam("c7", s, T["end"], 1.0, 1.03, -.3, .3, 12, -12)
js("tl.set('#ss_s7b',{autoAlpha:0},0);")
def s7_swap(tc):
    js(f"tl.set('#ss_s7',{{autoAlpha:0}},{at(tc)});"); js(f"tl.set('#ss_s7b',{{autoAlpha:1}},{at(tc)});"); sfx("impactsoft.ogg", tc + .05, -5)
usweep("ush3", s + .62, 0, s7_swap); scraps("s7b", s + .77, T["end"])

# --- loop back to frame 0
swap("s7", "sH", T["loop"], 9)
sfx("whoosh_c.ogg", T["loop"] - .1, -5)
scraps("sH", T["loop"], D_, final=True)
js(f"tl.fromTo('#hcamH',{{scale:1.03,rotation:.5}},{{scale:1,rotation:0,duration:{D_ - T['loop']:.3f},ease:'sine.out',transformOrigin:'540px 760px'}},{at(T['loop'])});")
js(f"tl.set('#sH',{{autoAlpha:0}},0);")

JS = "const D2=" + str(D_) + ";\n" + "\n".join(J)
json.dump([dict(f=f, t=t, g=g) for f, t, g in SFX if t < D_ and t >= 0], open(H + "/sfx7.json", "w"), indent=1)

html = open(H + "/shell8.html").read()
html = (html.replace("__STYLES__", styles).replace("__MARKUP__", markup).replace("__CHROME__", "").replace("__SCRIPTS__", "")
        .replace("__D__", str(D_)).replace("__CUES__", json.dumps(dict(lines=lines, D=D_)))
        .replace("__CALLS__", JS).replace("__NSC__", "1"))
html = re.sub(r'<div class="abs clip" id="gd".*?</div>', '', html, flags=re.S)
os.makedirs(H + "/hf", exist_ok=True)
open(H + "/hf/index.html", "w").write(html)
print("D=", D_, [(l["n"], l["start"], l["end"]) for l in lines])
print("scenes", {k: round(float(v), 2) for k, v in B.items()}, "js lines", len(J), "sfx", len(SFX))
if "--render" in sys.argv:
    name = sys.argv[sys.argv.index("--render") + 1]
    env = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1", DO_NOT_TRACK="1")
    r = subprocess.run(["npx", "--no-install", "hyperframes", "render", "-o", f"{H}/out/{name}.mp4", "--format", "mp4", "--quiet"],
                       cwd=H + "/hf", env=env, capture_output=True, text=True, timeout=3000)
    print(r.stdout[-400:], r.stderr[-800:])
