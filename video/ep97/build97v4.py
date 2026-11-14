#!/usr/bin/env python3
"""ep97 v4 'Guess the newest Claude' (hidden-label quiz), Miki style. Plan: channel/episode-97-v4-plan.md.
The four drawings are the REAL run-2 SVG files (13.11.2026, one try per model, prompt "Draw a pelican riding a
bicycle."; run logs: claude-haiku-5-5, claude-sonnet-5-5, claude-opus-5-5, claude-fable-5-2). They are embedded
untouched as <img>. Letter map: A = Opus 5.5, B = Haiku 5.5, C = Fable 5.2, D = Sonnet 5.5.

Reads voice/narration-raw-cues.json (+ voice/words.json, voice/lines.txt) -> hf/index.html, sfx97.json, cues97.json.
Every timing comes from the cue starts/ends and word times. Robust to a missing/old voice:
  - lines are read by number n=1..7; a missing line falls back to an estimated table (EST);
  - if the cue text does not match voice/lines.txt (old recording), word times are NOT trusted and
    every word time becomes a fraction of its line;
  - EST=1 python3 build97v4.py  forces the estimated table (preview before the voice exists).
"""
import json, os, re
H_ = os.path.dirname(os.path.abspath(__file__))
INK = "#0f0f0f"; ACC = "#D97757"; PAPER = "#fbfbf8"
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())

# ---------------------------------------------------------------- cues
LINES = [l.strip() for l in open(H_ + "/voice/lines.txt") if l.strip()]
EST = {1: (0.08, 1.40), 2: (1.48, 4.40), 3: (4.48, 6.70), 4: (6.78, 9.00), 5: (9.08, 11.20), 6: (11.28, 14.00), 7: (14.08, 16.60)}
try:
    C = json.load(open(H_ + "/voice/narration-raw-cues.json"))
    C = C if isinstance(C, list) else C["lines"]
except Exception:
    C = []
CUE = {c["n"]: c for c in C if "n" in c}
FORCE_EST = os.environ.get("EST") == "1"
STALE = FORCE_EST or any(n not in CUE or norm(CUE[n].get("line", CUE[n].get("text", ""))) != norm(LINES[n - 1]) for n in range(1, 8))
L = {}
for n in range(1, 8):
    if not FORCE_EST and n in CUE:
        L[n] = (float(CUE[n]["start"]), float(CUE[n]["end"]))
    else:
        L[n] = EST[n]
s = lambda n: L[n][0]
e = lambda n: L[n][1]
try:
    WORDS = [] if STALE else json.load(open(H_ + "/voice/words.json"))
except Exception:
    WORDS = []
# words.json is trusted only if it belongs to THIS recording: most of its words are words of lines.txt,
# it is about as long as the script, and it does not run past the last cue (an old words.json fails this)
VOC = {norm(w) for l in LINES for w in l.split()} | {"clawed", "claud", "cloud", "hiku"}
NW = sum(len(l.split()) for l in LINES)
WORDS_OK = bool(WORDS) and sum(norm(w[0]) in VOC for w in WORDS) >= .7 * len(WORDS) and abs(len(WORDS) - NW) <= 8 and WORDS[-1][1] <= e(7) + 1.0
if not WORDS_OK: WORDS = []
def W(word, n, k=0, frac=0.5):
    """start time of the k-th `word` inside line n; default = s(n) + frac * line length."""
    c = 0
    for w, a, b in WORDS:
        if s(n) - .12 <= a <= e(n) + .12 and norm(w) == word:
            if c == k: return a
            c += 1
    return s(n) + frac * (e(n) - s(n))
D = round(e(7) + 1.2, 2)

J = []; SFX = []
def js(x): J.append(x)
def sfx(f, t, g=-6): SFX.append(dict(f=f, t=round(max(0, t), 3), g=g))
def fin(sel, t, d=.4, y=22, blur=8):
    js(f"tl.fromTo('{sel}',{{opacity:0,y:{y},filter:'blur({blur}px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:{d},ease:'power2.out',immediateRender:false}},{max(0,t):.3f});")
def fout(sel, t, d=.28):
    js(f"tl.to('{sel}',{{opacity:0,y:-12,filter:'blur(8px)',duration:{d},ease:'power2.inOut'}},{max(0,t):.3f});")

# ---------------------------------------------------------------- geometry (safe box x 65-1015, y 269-1248)
CW, CH = 936, 711                      # card at scale 1 (border 6, pad 12, image 900x675)
# letter -> (file, model name, overlay scale to an 800x600 space)
CARD = {"A": ("opus", "Opus 5.5"), "B": ("haiku", "Haiku 5.5"), "C": ("fable", "Fable 5.2"), "D": ("sonnet", "Sonnet 5.5")}
ORDER = "ABCD"
FAN = {  # frame 0: a pile of taped cards, A in front
    "B": dict(x=366, y=764, s=.62, r=-5, o=1),
    "C": dict(x=704, y=790, s=.62, r=6, o=1),
    "D": dict(x=362, y=1030, s=.62, r=3, o=1),
    "A": dict(x=686, y=1012, s=.68, r=-2.5, o=1),
}
FANZ = {"B": 1, "C": 2, "D": 3, "A": 4}
STAGE_R = {"A": -1.2, "B": 1.0, "C": -0.8, "D": 1.2}
def stage(k): return dict(x=65 + CW / 2, y=424 + CH / 2, s=1, r=STAGE_R[k], o=1)
TW, TG, TY = 225, 16.6, 1152           # tray tiles
def tile_x(k): return 65 + ORDER.index(k) * (TW + TG)
def tray(k, o=0): return dict(x=tile_x(k) + 96 + 58, y=TY + 48, s=116 / CW, r=0, o=o)
COL = {  # countdown collage, unequal sizes
    "A": dict(x=326, y=622, s=.54, r=-4, o=1),
    "B": dict(x=768, y=640, s=.50, r=4, o=1),
    "C": dict(x=300, y=1078, s=.47, r=3, o=1),
    "D": dict(x=772, y=1082, s=.45, r=-4, o=1),
}
# ladder end card (thumb left, top, width)
LAD = {"B": (65, 935, 260), "D": (410, 900, 260), "A": (755, 895, 260), "C": (387, 425, 620)}
def lad(k, o=0):
    x, y, w = LAD[k]
    return dict(x=x + w / 2, y=y + w * .75 / 2, s=w / CW, r=0, o=o)

cur = {}
def tf(st): return f"x:{st['x'] - CW / 2:.1f},y:{st['y'] - CH / 2:.1f},scale:{st['s']:.4f},rotation:{st['r']},opacity:{st['o']}"
def place(k, st):
    cur[k] = dict(st); js(f"gsap.set('#c{k}',{{{tf(st)},zIndex:{FANZ[k]}}});")
def mv(k, t, d, to, ease="power3.inOut"):
    js(f"tl.fromTo('#c{k}',{{{tf(cur[k])}}},{{{tf(to)},duration:{d},ease:'{ease}',immediateRender:false}},{max(0,t):.3f});")
    cur[k] = dict(to)
def z(k, t, v): js(f"tl.set('#c{k}',{{zIndex:{v}}},{max(0,t):.3f});")
def thumb(k, t, o, d=.2): js(f"tl.to('#th{k}',{{opacity:{o},duration:{d},ease:'sine.inOut'}},{max(0,t):.3f});")
def lit(k, t, on):
    js(f"tl.to('#ti{k}',{{y:{-8 if on else 0},duration:.3,ease:'power2.inOut'}},{max(0,t):.3f});")
    js(f"tl.to('#ul{k}',{{scaleX:{1 if on else 0},duration:.3,ease:'power2.inOut'}},{max(0,t):.3f});")
def zoom(k, t0, t1, to=1.045):
    js(f"tl.fromTo('#zm{k}',{{scale:1}},{{scale:{to},duration:{max(.3, t1 - t0):.3f},ease:'sine.inOut',immediateRender:false}},{max(0,t0):.3f});")
def unzoom(k, t, d=.4): js(f"tl.to('#zm{k}',{{scale:1,duration:{d},ease:'power2.inOut'}},{max(0,t):.3f});")
FLY = .5
def to_tray(k, t):
    """stage/collage/fan -> tray tile; the card hides in the last moment and the tile thumbnail takes over."""
    mv(k, t, FLY, tray(k, 1)); unzoom(k, t)
    js(f"tl.to('#c{k}',{{opacity:0,duration:.12,ease:'sine.in'}},{t + FLY - .12:.3f});")
    cur[k] = tray(k, 0); thumb(k, t + FLY - .14, 1); lit(k, t, False)
def from_tray(k, t, to):
    js(f"tl.fromTo('#c{k}',{{{tf(tray(k, 0))}}},{{opacity:1,duration:.1,ease:'sine.out',immediateRender:false}},{max(0,t):.3f});")
    cur[k] = tray(k, 1); thumb(k, t, .22); z(k, t, 10); mv(k, t + .02, FLY, to); lit(k, t, True)

# ---------------------------------------------------------------- markup
try:
    from PIL import ImageFont
    _f = ImageFont.truetype(H_ + "/hf/assets/fonts/InterDisplay-Black.otf", 100)
    tw = lambda t: _f.getlength(t) - 3.5 * len(t)      # letter-spacing -.035em
except Exception:
    tw = lambda t: 60 * len(t)
HF = 86                                                 # headline px (2-line form)
w1 = tw("WHICH PELICAN IS") * HF / 100; w2 = tw("CLAUDE'S NEWEST?") * HF / 100
LOGO = 78
K1 = min(.76, 950 / (w1 + 26 + LOGO + 16 + w2))         # scale of the one-line form
H2X = (w1 + 26) * K1                                    # where line 2 lands in the one-line form

# overlay annotations, drawn in an 800x600 space over each drawing (rings sit AROUND features)
def lab(i, x, y, t, anchor="middle"): return f'<text id="{i}" class="an" x="{x}" y="{y}" text-anchor="{anchor}">{t}</text>'
OV = {
 "B": '<circle id="rB" class="rg dash" cx="690" cy="92" r="52" pathLength="1"/>' + lab("lB", 690, 196, "no sun"),
 "D": '<circle id="rD" class="rg" cx="680" cy="90" r="64" pathLength="1"/>' + lab("lD", 680, 204, "+ sun"),
 "A": '<rect id="rA" class="rg" x="10" y="484" width="780" height="42" rx="21" pathLength="1"/>' + lab("lA", 400, 574, "+ road"),
 "C": '<ellipse id="rC1" class="rg" cx="166" cy="103" rx="104" ry="50" pathLength="1"/>' + lab("lC1", 170, 204, "+ clouds")
      + '<ellipse id="rC2" class="rg" cx="400" cy="504" rx="286" ry="30" pathLength="1"/>' + lab("lC2", 400, 578, "+ shadow"),
}
cards = ""
for k in ORDER:
    f, name = CARD[k]
    cards += f'''<div class="card" id="c{k}"><div class="in" id="in{k}">
 <div class="tape t1" data-decor></div><div class="tape t2" data-decor></div>
 <div class="fr"><div class="zm" id="zm{k}"><img src="assets/draw/{f}-r2.svg"><svg class="ov" viewBox="0 0 800 600">{OV[k]}</svg></div></div>
 <div class="tab">{k}</div></div></div>'''
tiles = ""
for k in ORDER:
    f, name = CARD[k]
    tiles += f'''<div class="tile" id="ti{k}" style="left:{tile_x(k):.1f}px"><span class="tl">{k}</span>
 <div class="tt"><img id="th{k}" src="assets/draw/{f}-r2.svg"></div>
 <svg class="tk" id="tk{k}" viewBox="0 0 40 40"><path d="M6 21 L16 31 L35 8" pathLength="1"/></svg>
 <div class="ul" id="ul{k}"></div></div>'''
STAMP = {"B": "SMALLEST", "C": "NEWEST"}
revs = ""
for k in "BDAC":
    f, name = CARD[k]
    st = f'<div class="stamp{" acc" if k == "C" else ""}" id="st{k}">{STAMP[k]}</div>' if k in STAMP else ""
    revs += f'<div class="rv" id="rv{k}"><span class="rn">{k} = {name.upper()}</span></div>{st}'
ADDS = {"B": "no sun", "D": "+ sun", "A": "+ road"}
ladder = '<div class="lt1 lx" id="lt1">SAME REQUEST, 4 CLAUDES</div><div class="lt2 lx" id="lt2">&ldquo;Draw a pelican riding a bicycle.&rdquo;</div>'
for k in "BDA":
    x, y, w = LAD[k]; f, name = CARD[k]
    ladder += f'''<div class="li" id="li{k}" style="left:{x}px;top:{y}px;width:{w}px"><div class="lth"><img src="assets/draw/{f}-r2.svg"></div>
 <div class="ln"><b>{k}</b>{name}</div><div class="la">{ADDS[k]}</div></div>'''
x, y, w = LAD["C"]
ladder += f'''<div class="li" id="liC" style="left:{x}px;top:{y}px;width:{w}px"><div class="lth"><img src="assets/draw/fable-r2.svg"></div></div>
<div class="lc" id="lcC"><div class="lcl">C</div><div class="lcn">FABLE<br>5.2</div><div class="la big">+ clouds<br>+ shadow</div>
 <svg class="arr" viewBox="0 0 120 60" data-decor><path d="M4 30 H104 M82 10 L106 30 L82 50"/></svg></div>'''
markup = f'''
<div class="bgw" data-decor></div>
<div id="cam">
 <div class="hl" id="h1">WHICH PELICAN IS</div>
 <div class="hl" id="h2"><img src="assets/claude-mark.svg">CLAUDE&rsquo;S NEWEST?</div>
 <div class="chip" id="chip">4 Claude models &middot; same request: a pelican on a bike</div>
 <div class="chip" id="chip2">guess: A, B, C or D, below</div>
 {revs}
 <div id="tray">{tiles}</div>
 {cards}
 <div id="count"><svg viewBox="0 0 260 260"><circle class="cbg" cx="130" cy="130" r="112"/><circle id="cring" cx="130" cy="130" r="112" pathLength="1" transform="rotate(-90 130 130)"/></svg>
  <div class="num" id="n3">3</div><div class="num" id="n2">2</div><div class="num" id="n1">1</div></div>
 <div id="ladder">{ladder}</div>
</div>
'''
css = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;color:{INK}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}}
.bgw{{position:absolute;left:-20px;top:-20px;width:1120px;height:1960px;background:#ecebe5 url(assets/bg.jpg);background-size:1120px 1960px}}
#cam{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}}
.hl{{position:absolute;left:65px;font-size:{HF}px;line-height:{HF}px;height:{HF}px;font-weight:900;letter-spacing:-.035em;white-space:nowrap;transform-origin:0 0;display:flex;align-items:center}}
#h1{{top:283px}} #h2{{top:{283 + HF - 6}px}}
#h2 img{{width:{LOGO}px;height:{LOGO}px;margin-right:16px}}
.chip{{position:absolute;left:67px;top:456px;font:700 30px/34px JBM,monospace;letter-spacing:-.01em;white-space:nowrap;transform-origin:0 0;padding-bottom:6px;border-bottom:4px solid {INK}}}
#chip2{{opacity:0;top:354px;border-bottom-color:{ACC}}}
.card{{position:absolute;left:0;top:0;width:{CW}px;height:{CH}px;transform-origin:50% 50%;will-change:transform}}
.in{{position:absolute;inset:0;background:{PAPER};border:6px solid {INK};border-radius:8px;box-shadow:14px 14px 0 {INK};transform-origin:50% 50%}}
.fr{{position:absolute;left:12px;top:12px;width:900px;height:675px;overflow:hidden;border-radius:3px;background:#fff}}
.zm{{position:absolute;inset:0;transform-origin:50% 55%}}
.zm img{{position:absolute;left:0;top:0;width:900px;height:675px;display:block}}
.ov{{position:absolute;left:0;top:0;width:900px;height:675px;overflow:visible}}
.rg{{fill:none;stroke:{ACC};stroke-width:9;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1}}
.rg.dash{{stroke-dasharray:.045 .035;stroke-dashoffset:0;opacity:0;transform-origin:690px 92px}}
.an{{font:700 40px JBM,monospace;fill:{INK};stroke:#fff;stroke-width:9;paint-order:stroke;stroke-linejoin:round;opacity:0}}
.tab{{position:absolute;left:22px;top:-16px;width:112px;height:106px;background:{PAPER};border:6px solid {INK};border-radius:8px;box-shadow:6px 6px 0 {INK};font-size:84px;line-height:92px;font-weight:900;text-align:center;transform:rotate(-4deg)}}
.tape{{position:absolute;width:150px;height:44px;background:rgba(232,221,186,.86);border:1px solid rgba(0,0,0,.14);z-index:3}}
.tape.t1{{right:-40px;top:-12px;transform:rotate(34deg)}} .tape.t2{{left:-40px;bottom:-4px;transform:rotate(34deg)}}
#tray{{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0}}
.tile{{position:absolute;top:{TY}px;width:{TW}px;height:96px}}
.tl{{position:absolute;left:0;top:4px;width:86px;height:88px;font-size:74px;line-height:88px;font-weight:900;text-align:center}}
.tt{{position:absolute;left:96px;top:4px;width:116px;height:88px;border:4px solid {INK};border-radius:5px;background:{PAPER};box-shadow:5px 5px 0 {INK};overflow:hidden}}
.tt img{{position:absolute;left:0;top:0;width:108px;height:81px;opacity:0}}
.tk{{position:absolute;left:64px;top:-14px;width:44px;height:44px;overflow:visible}}
.tk path{{fill:none;stroke:{ACC};stroke-width:8;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1}}
.ul{{position:absolute;left:6px;top:92px;width:74px;height:7px;border-radius:4px;background:{ACC};transform:scaleX(0);transform-origin:0 50%}}
.rv{{position:absolute;left:65px;top:280px;height:100px;display:flex;align-items:center;gap:22px;opacity:0;white-space:nowrap}}
.rl{{width:100px;height:96px;border:6px solid {INK};border-radius:8px;background:{PAPER};box-shadow:6px 6px 0 {INK};font-size:76px;line-height:84px;font-weight:900;text-align:center;transform:rotate(-4deg)}}
.rn{{font-size:84px;line-height:100px;font-weight:900;letter-spacing:-.035em}}
.stamp{{position:absolute;right:118px;top:306px;height:62px;padding:0 16px;border:6px solid {INK};border-radius:8px;font:700 36px/50px JBM,monospace;letter-spacing:.04em;opacity:0;transform-origin:50% 50%}}
.stamp.acc{{border-color:{ACC};color:{ACC}}}
#count{{position:absolute;left:435px;top:700px;width:210px;height:210px;opacity:0;z-index:30}}
#count svg{{position:absolute;inset:0;overflow:visible}}
.cbg{{fill:{PAPER};stroke:{INK};stroke-width:6;filter:drop-shadow(10px 10px 0 {INK})}}
#cring{{fill:none;stroke:{ACC};stroke-width:20;stroke-dasharray:1;stroke-dashoffset:0}}
.num{{position:absolute;inset:0;font-size:124px;line-height:210px;font-weight:900;text-align:center;opacity:0}}
#ladder{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}}
.lx,.li,.lc{{opacity:0}}
.lt1{{position:absolute;left:65px;top:283px;font-size:66px;line-height:70px;font-weight:900;letter-spacing:-.035em;white-space:nowrap}}
.lt2{{position:absolute;left:67px;top:360px;font:700 31px/40px JBM,monospace;white-space:nowrap}}
.li{{position:absolute}}
.lth{{width:100%;aspect-ratio:4/3;border:5px solid {INK};border-radius:6px;background:{PAPER};box-shadow:8px 8px 0 {INK};overflow:hidden}}
.lth img{{width:100%;height:100%;display:block}}
.ln{{margin-top:12px;font-size:31px;line-height:34px;font-weight:900;letter-spacing:-.02em;white-space:nowrap}}
.ln b{{display:inline-block;margin-right:10px;color:{ACC}}}
.la{{font:700 25px/30px JBM,monospace;white-space:nowrap}}
.la.big{{font-size:34px;line-height:44px;margin-top:14px}}
.lc{{position:absolute;left:65px;top:438px;width:310px}}
.lcl{{width:104px;height:100px;border:6px solid {INK};border-radius:8px;background:{PAPER};box-shadow:6px 6px 0 {INK};font-size:80px;line-height:88px;font-weight:900;text-align:center;transform:rotate(-4deg)}}
.lcn{{margin-top:22px;font-size:88px;line-height:84px;font-weight:900;letter-spacing:-.04em}}
.arr{{width:120px;height:60px;margin-top:16px}} .arr path{{fill:none;stroke:{ACC};stroke-width:9;stroke-linecap:round;stroke-linejoin:round}}
'''

# ---------------------------------------------------------------- timeline
tA = max(.9, s(2) - .15)                         # card A flies to the stage, headline shrinks to one line
tR = s(4) - .1                                   # reveal starts
cd0 = max(s(3) + .3, min(e(3) + .05, tR - 1.5))  # countdown start (3 numbers until tR)
cdd = max(.9, tR - cd0)                          # countdown length
dw = (cd0 - .1 - tA) / 4                         # dwell per card in the gallery
tB, tC, tD = tA + dw, tA + 2 * dw, tA + 3 * dw
t5a = W("a", 5, 1, .52) - .15                    # "A adds a road"
t5a = min(max(t5a, s(5) + .7), e(5) - .6)
tL = e(6) + .1                                   # ladder card
tF = e(7) + .2                                   # re-fan to frame 0 (0.8 s), D = e(7) + 1.2

js("gsap.set('#h2',{y:0});")
for k in ORDER: place(k, FAN[k])
# whole picture drifts all the time
js(f"tl.fromTo('#cam',{{scale:1,rotation:0}},{{scale:1.012,rotation:.25,duration:{D / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},0);")
js(f"tl.fromTo('.bgw',{{x:0,y:0}},{{x:-14,y:-12,duration:{D / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},0);")
# beat 1: the fan breathes, card A is already lifting
for i, k in enumerate("BCDA"):
    js(f"tl.fromTo('#in{k}',{{y:0,rotation:0}},{{y:{-9 if i % 2 == 0 else 9},rotation:{1.2 if i % 2 == 0 else -1.1},duration:{.42 + i * .05:.2f},ease:'sine.inOut',yoyo:true,repeat:{2 * max(1, round(tA / (2 * (.42 + i * .05)))) - 1}}},0);")
lift = dict(FAN["A"]); lift.update(y=FAN["A"]["y"] - 52, s=.74, r=-1)
mv("A", 0, tA, lift, "sine.inOut")
tn = min(W("newest", 1, 0, .38), tA - .5)
js(f"tl.fromTo('#h1',{{scale:1}},{{scale:1.045,duration:.24,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{max(.15, tn):.3f});")
js(f"tl.fromTo('#h2 img',{{rotation:0}},{{rotation:90,duration:{tA:.3f},ease:'sine.inOut'}},0);")
sfx("subhit.ogg", .05, -6); sfx("tick.ogg", max(.15, tn), -8)
# beat 2: A to the big stage, the rest into the tray, headline to one line
js(f"tl.to('#h1',{{scale:{K1:.4f},duration:.5,ease:'power3.inOut'}},{tA:.3f});")
js(f"tl.to('#h2',{{scale:{K1:.4f},x:{H2X:.1f},y:{-(HF - 6):.1f},duration:.5,ease:'power3.inOut'}},{tA:.3f});")
js(f"tl.to('#chip',{{y:-102,scale:.93,duration:.5,ease:'power3.inOut'}},{tA:.3f});")
js(f"tl.to('#tray',{{opacity:1,duration:.35,ease:'sine.inOut'}},{tA + .1:.3f});")
z("A", tA, 10); mv("A", tA, FLY, stage("A")); lit("A", tA + .2, True); zoom("A", tA + FLY, tB + .2)
js(f"tl.set('#thA',{{opacity:.22}},{tA:.3f});")
for i, k in enumerate("BCD"):
    to_tray(k, tA + .04 * i)
sfx("whoosh_b.ogg", tA - .02, -9)
def swap(a, b, t):
    z(a, t, 5); to_tray(a, t); from_tray(b, t, stage(b)); sfx("pop_a.ogg" if b in "BD" else "pop_b.ogg", t + .05, -9)
swap("A", "B", tB); zoom("B", tB + FLY, tC + .2)
swap("B", "C", tC); zoom("C", tC + FLY, tD + .2)
swap("C", "D", tD); zoom("D", tD + FLY, cd0 + .2)
# beat 3: collage + visible countdown
fout("#chip", cd0 - .05); fin("#chip2", cd0 + .15)
js(f"tl.to('#tray',{{opacity:0,duration:.3,ease:'sine.inOut'}},{cd0:.3f});")
z("D", cd0, 4); mv("D", cd0, FLY, COL["D"]); unzoom("D", cd0); lit("D", cd0, False)
for i, k in enumerate("ABC"):
    js(f"tl.fromTo('#c{k}',{{{tf(tray(k, 0))}}},{{opacity:1,duration:.1,ease:'sine.out',immediateRender:false}},{cd0 + .03 * i:.3f});")
    cur[k] = tray(k, 1); z(k, cd0, 1 + i); mv(k, cd0 + .02 + .03 * i, FLY, COL[k])
sfx("whoosh_c.ogg", cd0, -10)
js(f"tl.fromTo('#count',{{opacity:0,scale:.7}},{{opacity:1,scale:1,duration:.35,ease:'power3.out',immediateRender:false}},{cd0 + .1:.3f});")
step = cdd / 3
for i, nn in enumerate((3, 2, 1)):
    t = cd0 + .12 + i * step
    js(f"tl.fromTo('#n{nn}',{{opacity:0,scale:.9}},{{opacity:1,scale:1,duration:.2,ease:'power2.out',immediateRender:false}},{t:.3f});")
    js(f"tl.to('#n{nn}',{{opacity:0,scale:1.12,duration:.16,ease:'power2.in'}},{t + step - .17:.3f});")
    js(f"tl.to('#cring',{{strokeDashoffset:{(i + 1) / 3:.4f},duration:{step:.3f},ease:'sine.inOut'}},{cd0 + i * step:.3f});")
    for j, k in enumerate(ORDER):
        js(f"tl.fromTo('#in{k}',{{rotation:0,y:0}},{{rotation:{1.8 if (i + j) % 2 else -1.8},y:-7,duration:{min(.24, step / 2 - .02):.3f},ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{t + .02 * j:.3f});")
    sfx("tick.ogg", t, -6)
# beat 4-6: the reveal, B, D, A, C
js(f"tl.to('#count',{{opacity:0,scale:.8,duration:.25,ease:'power2.in'}},{tR - .05:.3f});")
fout("#chip2", tR - .05); fout("#h1", tR - .05); fout("#h2", tR - .05)
js(f"tl.to('#tray',{{opacity:1,duration:.3,ease:'sine.inOut'}},{tR + .15:.3f});")
z("B", tR, 10); mv("B", tR, FLY, stage("B")); lit("B", tR + .2, True)
js(f"tl.set('#thB',{{opacity:.22}},{tR:.3f});")
for i, k in enumerate("ACD"):
    to_tray(k, tR + .03 * i)
sfx("whoosh_b.ogg", tR, -9)
def tick(k, t):
    js(f"tl.to('#tk{k} path',{{strokeDashoffset:0,duration:.3,ease:'power2.inOut'}},{t:.3f});")
def ring(sel, t, d=.45):
    js(f"tl.to('{sel}',{{strokeDashoffset:0,duration:{d},ease:'power2.inOut'}},{t:.3f});")
def label(sel, t):
    js(f"tl.fromTo('{sel}',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.3,ease:'power2.out',immediateRender:false}},{t:.3f});")
def stamp(k, t, rot):
    js(f"tl.fromTo('#st{k}',{{opacity:0,scale:1.22,rotation:{rot - 8}}},{{opacity:1,scale:1,rotation:{rot},duration:.42,ease:'power3.out',immediateRender:false}},{t:.3f});")
def reveal_hdr(k, t, t_end):
    fin(f"#rv{k}", t)
    if t_end: fout(f"#rv{k}", t_end)
# B = Haiku 5.5, the smallest: no sun
tBn = max(tR + .25, W("haiku", 4, 0, .3) - .12)
reveal_hdr("B", tBn, s(5) - .12); tick("B", tBn + .1); sfx("select.ogg", tBn, -9)
tBs = max(tBn + .3, W("smallest", 4, 0, .55) - .05); stamp("B", tBs, -5); fout("#stB", s(5) - .12); sfx("click_a.ogg", tBs + .1, -8)
tBsun = max(tBs + .3, W("sun", 4, 0, .86) - .12)
js(f"tl.fromTo('#rB',{{opacity:0,scale:.6,rotation:-40}},{{opacity:1,scale:1,rotation:0,duration:.5,ease:'power3.out',immediateRender:false}},{tBsun:.3f});")
label("#lB", tBsun + .12); zoom("B", tR + FLY, s(5)); sfx("tick.ogg", tBsun, -8)
# D = Sonnet 5.5: adds a sun
swap("B", "D", s(5) - .08); reveal_hdr("D", s(5) + .12, t5a - .06); tick("D", s(5) + .25)
tDs = min(max(s(5) + .4, W("sun", 5, 0, .3) - .15), t5a - .5)
ring("#rD", tDs, .4); label("#lD", tDs + .15); zoom("D", s(5) + FLY, t5a + .2); sfx("tick.ogg", tDs, -8)
# A = Opus 5.5: adds a road
swap("D", "A", t5a); reveal_hdr("A", t5a + .2, s(6) - .12); tick("A", t5a + .3)
tAr = min(max(t5a + .45, W("road", 5, 0, .85) - .2), s(6) - .45)
ring("#rA", tAr, .5); label("#lA", tAr + .2); zoom("A", t5a + FLY, s(6) + .1); sfx("tick.ogg", tAr, -8)
# C = Fable 5.2, the newest: clouds and a shadow
swap("A", "C", s(6) - .08)
tCn = max(s(6) + .2, W("fable", 6, 0, .22) - .12)
reveal_hdr("C", tCn, None); tick("C", tCn + .1); sfx("select.ogg", tCn, -9)
tCs = max(tCn + .3, W("newest", 6, 0, .45) - .05); stamp("C", tCs, -5); sfx("impactsoft.ogg", tCs + .05, -6)
tCc = max(tCs + .3, W("clouds", 6, 0, .68) - .15); ring("#rC1", tCc, .45); label("#lC1", tCc + .15); sfx("tick.ogg", tCc, -8)
tCsh = min(max(tCc + .45, W("shadow", 6, 0, .88) - .15), tL - .4); ring("#rC2", tCsh, .5)
js(f"tl.to('#lC1',{{opacity:0,duration:.2,ease:'sine.inOut'}},{tCsh:.3f});"); label("#lC2", tCsh + .15); sfx("tick.ogg", tCsh, -8)
zoom("C", s(6) + FLY - .1, tL + .2, 1.08)
# beat 7: the ladder card (screenshot-able)
fout("#rvC", tL - .05); fout("#stC", tL - .05)
js(f"tl.to('#tray',{{opacity:0,duration:.3,ease:'sine.inOut'}},{tL - .05:.3f});")
lit("C", tL - .05, False)
goC = lad("C", 1); mv("C", tL, .55, goC); unzoom("C", tL, .5)
js(f"tl.to('#cC',{{opacity:0,duration:.15,ease:'sine.in'}},{tL + .45:.3f});"); cur["C"] = lad("C", 0)
for q in ("#rC1", "#rC2", "#lC2"): js(f"tl.to('{q}',{{opacity:0,duration:.25,ease:'sine.inOut'}},{tL:.3f});")
fin("#lt1", tL + .1); fin("#lt2", tL + .22)
for i, k in enumerate("BDA"):
    js(f"tl.fromTo('#li{k}',{{opacity:0,y:70,rotation:{-4 + 3 * i}}},{{opacity:1,y:0,rotation:0,duration:.5,ease:'power3.out',immediateRender:false}},{tL + .2 + .18 * i:.3f});")
    sfx("pop_a.ogg" if i % 2 == 0 else "pop_b.ogg", tL + .25 + .18 * i, -10)
js(f"tl.fromTo('#liC',{{opacity:0}},{{opacity:1,duration:.15,ease:'sine.out',immediateRender:false}},{tL + .45:.3f});")
fin("#lcC", tL + .74); sfx("ding.ogg", tL + .78, -10); sfx("whoosh_c.ogg", tL, -10)
hold = max(.6, tF - (tL + 1.2))
js(f"tl.fromTo('#ladder',{{y:0,rotation:0}},{{y:-10,rotation:-.35,duration:{hold / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tL + 1.2:.3f});")
for i, k in enumerate("BDAC"):
    js(f"tl.fromTo('#li{k} .lth',{{y:0}},{{y:-12,duration:.3,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{s(7) + .45 + i * .32:.3f});")
js(f"tl.fromTo('.arr',{{x:0}},{{x:14,duration:.45,ease:'sine.inOut',yoyo:true,repeat:{2 * max(1, round(hold / .9)) - 1},immediateRender:false}},{tL + 1.1:.3f});")
# loop: everything folds back into the frame-0 fan (letters only, names hidden again)
for q in ("#lt1", "#lt2", "#lcC"): fout(q, tF, .22)
for k in ORDER:
    js(f"tl.to('#li{k}',{{opacity:0,duration:.18,ease:'sine.in'}},{tF + .05:.3f});")
    js(f"tl.set('#c{k}',{{zIndex:{FANZ[k]}}},{tF:.3f});")
    cur[k] = lad(k, 0)
    js(f"tl.fromTo('#c{k}',{{{tf(cur[k])}}},{{opacity:1,duration:.14,ease:'sine.out',immediateRender:false}},{tF:.3f});")
    cur[k] = lad(k, 1); mv(k, tF + .02, .8, FAN[k])
    js(f"tl.set('#tk{k} path',{{strokeDashoffset:1}},{tF:.3f});")
for q in ("#rB", "#lB", "#lD", "#lA", "#rD", "#rA"): js(f"tl.set('{q}',{{opacity:0}},{tF:.3f});")
js(f"tl.set('#h1',{{scale:1,x:0,y:0}},{tF:.3f}); tl.set('#h2',{{scale:1,x:0,y:0}},{tF:.3f}); tl.set('#chip',{{scale:1}},{tF:.3f}); tl.set('#h2 img',{{rotation:0}},{tF:.3f});")
for q in ("#h1", "#h2", "#chip"): fin(q, tF + .3, .45)
sfx("whoosh_c.ogg", tF, -10)

JS = re.sub(r"tl\.set\(([^,]+),\{", r"tl.set(\1,{immediateRender:false,", "\n".join(J))   # a timeline set must not render at build time
json.dump(SFX, open(H_ + "/sfx97.json", "w"), indent=1)
json.dump(dict(lines=[dict(n=n, text=LINES[n - 1], start=s(n), end=e(n)) for n in range(1, 8)], D=D, stale_voice=STALE), open(H_ + "/cues97.json", "w"), indent=1)
html = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Black.otf");font-weight:900}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Medium.otf");font-weight:500}}
@font-face{{font-family:"JBM";src:url("assets/fonts/JetBrainsMono-Bold.ttf");font-weight:700}}
{css}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
{markup}
</div>
<script>
const D={D}; const tl=gsap.timeline({{paused:true}});
{JS}
tl.to({{}},{{duration:.001}},D-.001);
window.__timelines=window.__timelines||{{}}; window.__timelines["main"]=tl; tl.seek(0);
window.__reel={{duration:D,seek:t=>{{tl.seek(t)}}}};   // returns nothing: a returned timeline hangs page.evaluate (safe_check.js)
</script></body></html>'''
open(H_ + "/hf/index.html", "w").write(html)
print(f"D={D} sfx={len(SFX)} js={len(J)} stale_voice={STALE} est={FORCE_EST}")
print("beats: " + " ".join(f"{n}={v:.2f}" for n, v in dict(tA=tA, tB=tB, tC=tC, tD=tD, cd0=cd0, tR=tR, D5=s(5), A5=t5a, C6=s(6), ladder=tL, refan=tF).items()))
if not WORDS_OK: print("NOTE: voice/words.json is missing or from another recording: word-timed beats (stamps, rings, the swap to A) use fractions of their line. Re-run after whisper writes words.json.")
if STALE: print("WARNING: cue text does not match voice/lines.txt (old voice) or EST=1: word times replaced by line fractions.")
