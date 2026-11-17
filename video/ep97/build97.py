#!/usr/bin/env python3
"""ep97 'Four Claude AIs. One pelican. Watch it level up.' Miki style.
The four drawings are the REAL SVG files written by four Claude models on 13.11.2026 for the one prompt
"Draw a pelican riding a bicycle." (run 1, no retries; models from the run logs: claude-haiku-5-5,
claude-sonnet-5-5, claude-opus-5, claude-fable-5-2). Reads voice/narration-raw-cues.json (+ voice/words.json)
-> hf/index.html, sfx97.json, cues97.json."""
import json, os, re
H_ = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(H_ + "/voice/narration-raw-cues.json"))
C = C if isinstance(C, list) else C["lines"]
L = {c["n"]: (c["start"], c["end"]) for c in C}
s = lambda n: L[n][0]
e = lambda n: L[n][1]
D = round(e(7) + 1.2, 2)
INK = "#0f0f0f"; ACC = "#D97757"
J = []; SFX = []
def js(x): J.append(x)
def sfx(f, t, g=-6): SFX.append(dict(f=f, t=round(max(0, t), 3), g=g))
def fin(sel, t, d=.35, y=24, blur=10):
    js(f"tl.fromTo('{sel}',{{opacity:0,y:{y},filter:'blur({blur}px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:{d},ease:'power2.out',immediateRender:false}},{max(0,t):.3f});")
def fout(sel, t, d=.25):
    js(f"tl.to('{sel}',{{opacity:0,y:-14,filter:'blur(10px)',duration:{d},ease:'power1.in'}},{max(0,t):.3f});")
try:
    WORDS = json.load(open(H_ + "/voice/words.json"))
except Exception:
    WORDS = []
def W(word, k=0, after=0.0, default=None):
    n = 0
    for w, a, b in WORDS:
        if a >= after and re.sub(r"[^a-z0-9]", "", w.lower()) == word:
            if n == k: return a
            n += 1
    return default

MODELS = [("haiku", "Haiku 5.5"), ("sonnet", "Sonnet 5.5"), ("opus", "Opus 5"), ("fable", "Fable 5.2")]
# card grid inside the safe box x 65-1015, y 269-1248
CW, CH, GAP = 460, 372, 30
POS = [(65, 470), (65 + CW + GAP, 470), (65, 470 + CH + GAP - 6), (65 + CW + GAP, 470 + CH + GAP - 6)]
cards = ""
for i, (k, name) in enumerate(MODELS):
    x, y = POS[i]
    cards += f'''<div class="card" id="c{i}" style="left:{x}px;top:{y}px">
 <div class="tag"><img src="assets/claude-mark.svg"><span>{name}</span></div>
 <div class="box"><div class="ph" id="ph{i}">?</div><img class="dr" id="d{i}" src="assets/draw/{k}.svg"></div>
 <div class="ring" id="r{i}"></div></div>'''
TITLES = [
    ("t0", "4 CLAUDE AIs DRAW<br>A PELICAN ON A BIKE"),
    ("t1", "NO SEAT"),
    ("t2", "LEGS ON<br>THE PEDALS"),
    ("t3", "IT MOVES FAST"),
    ("t4", "SUN, SHADOW,<br>A REAL BIKE"),
    ("t5", "SAME COMPANY.<br>NOT THE SAME PELICAN."),
    ("t6", "SEND IT TO THE FRIEND<br>WHO THINKS EVERY AI<br>IS THE SAME"),
    ("t7", "4 CLAUDE AIs DRAW<br>A PELICAN ON A BIKE"),
]
titles = "".join(f'<div class="ttl" id="{i}">{tx}</div>' for i, tx in TITLES)
markup = f'''
<div class="bgw" data-decor></div>
<div id="cam">
 {titles}
 {cards}
</div>
'''
css = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;color:{INK}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}}
.bgw{{position:absolute;left:0;top:0;width:1080px;height:1920px;background:#ecebe5 url(assets/bg.jpg);background-size:1080px 1920px}}
#cam{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 860px}}
.ttl{{position:absolute;left:92px;width:860px;top:292px;height:170px;display:flex;align-items:center;font-size:66px;line-height:70px;font-weight:900;letter-spacing:-.035em;opacity:0}}
#t5{{font-size:54px;line-height:58px}} #t6{{font-size:48px;line-height:54px}}
#t0{{opacity:1}}
.card{{position:absolute;width:{CW}px;height:{CH}px;background:#fbfbf8;border:4px solid {INK};border-radius:10px;box-shadow:10px 10px 0 {INK};transform-origin:50% 50%}}
.tag{{position:absolute;left:0;top:0;width:100%;height:56px;display:flex;align-items:center;gap:12px;padding:0 16px;border-bottom:3px solid {INK}}}
.tag img{{width:34px;height:34px}}
.tag span{{font:700 30px/1 JBM,monospace;letter-spacing:.02em;white-space:nowrap}}
.box{{position:absolute;left:10px;top:64px;width:432px;height:292px;overflow:hidden;border-radius:6px}}
.ph{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:150px;font-weight:900;color:#c9c6bc;border:4px dashed #c9c6bc;border-radius:6px}}
.dr{{position:absolute;left:0;top:0;width:432px;height:292px;object-fit:contain;background:#fff;clip-path:inset(0 100% 0 0)}}
.ring{{position:absolute;left:-12px;top:-12px;width:{CW+16}px;height:{CH+16}px;border:7px solid {ACC};border-radius:16px;opacity:0}}
'''
t_lvl = W("level", 0, default=1.6)
js(f"tl.fromTo('#cam',{{scale:1.0,y:0}},{{scale:1.012,y:-6,duration:{D},ease:'sine.inOut'}},0);")
for i in range(4):
    js(f"tl.fromTo('#ph{i}',{{y:0}},{{y:-10,duration:.55,ease:'sine.inOut',yoyo:true,repeat:{max(1,int((s(2)+.2)/.55))}}},{i*.12:.2f});")
js(f"tl.fromTo('#t0',{{scale:1}},{{scale:1.04,duration:.25,ease:'sine.out',yoyo:true,repeat:1,transformOrigin:'0% 50%'}},{max(.2,t_lvl):.3f});")
sfx("subhit.ogg", .05, -6); sfx("tick.ogg", t_lvl, -7)
KEY = {0: ("seat", 2), 1: ("pedals", 3), 2: ("fast", 4), 3: ("sun", 5)}
prev = "#t0"
for i in range(4):
    n = i + 2
    w, _ = KEY[i]
    tw = W(w, 0, after=s(n), default=s(n) + .8)
    js(f"tl.to('#r{i}',{{opacity:1,duration:.2,ease:'power2.out'}},{s(n):.3f});")
    js(f"tl.to('#ph{i}',{{opacity:0,duration:.25}},{s(n)+.05:.3f});")
    if i == 0:
        js("gsap.set('#d0',{clipPath:'inset(0 62% 0 0)'}); gsap.set('#ph0',{opacity:0});")
        js(f"tl.fromTo('#d0',{{clipPath:'inset(0 62% 0 0)'}},{{clipPath:'inset(0 0% 0 0)',duration:{s(2)+.4:.2f},ease:'sine.inOut',immediateRender:false}},0);")
    else:
        js(f"tl.to('#d{i}',{{clipPath:'inset(0 0% 0 0)',duration:.55,ease:'power2.inOut'}},{s(n)+.05:.3f});")
    js(f"tl.fromTo('#c{i}',{{scale:1}},{{scale:1.035,duration:.25,ease:'sine.out',yoyo:true,repeat:1}},{s(n)+.55:.3f});")
    sfx("pop_a.ogg" if i % 2 == 0 else "pop_b.ogg", s(n) + .1, -8)
    fout(prev, tw - .3); fin(f"#t{i+1}", tw - .12); sfx("tick.ogg", tw, -8)
    prev = f"#t{i+1}"
    if i < 3:
        js(f"tl.to('#r{i}',{{opacity:0,duration:.2}},{s(n+1)-.05:.3f});")
# Fable zoom: move card 3 to the centre of the grid and enlarge
fx, fy = POS[3]; cx, cy = 65 + 475 - CW / 2, 470 + 383 - CH / 2
zt = W("sun", 0, after=s(5), default=s(5) + 1.0) + .35
js(f"tl.to('#c3',{{x:{cx-fx:.0f},y:{cy-fy:.0f},scale:1.95,zIndex:5,duration:.6,ease:'power3.inOut'}},{zt:.3f});")
js(f"tl.set('#c3',{{zIndex:5}},{zt:.3f});")
sfx("whoosh_b.ogg", zt - .05, -9); sfx("impactsoft.ogg", zt + .55, -6)
js(f"tl.to('#c3',{{x:0,y:0,scale:1,duration:.55,ease:'power3.inOut'}},{s(6)-.1:.3f});")
js(f"tl.to('#r3',{{opacity:0,duration:.2}},{s(6):.3f});")
fout(prev, s(6) - .1); fin("#t5", s(6) + .15); sfx("whoosh_c.ogg", s(6) - .1, -10)
for i in range(4):
    js(f"tl.fromTo('#c{i}',{{y:0}},{{y:-14,duration:.22,ease:'sine.out',yoyo:true,repeat:1}},{s(6)+.5+i*.16:.3f});")
fout("#t5", s(7) - .1); fin("#t6", s(7) + .05); sfx("tick.ogg", s(7) + .05, -7)
for i in range(4):
    js(f"tl.fromTo('#r{i}',{{opacity:0}},{{opacity:1,duration:.25,yoyo:true,repeat:1,ease:'sine.inOut'}},{s(7)+.2+i*.55:.3f});")
js(f"tl.fromTo('#cam',{{rotation:0}},{{rotation:.35,duration:.9,ease:'sine.inOut',yoyo:true,repeat:{max(1,int((e(7)-s(7))/.9))}}},{s(7):.3f});")
# loop back to frame 0
lt = e(7) + .45
fout("#t6", lt - .05)
for i in range(4):
    js(f"tl.to('#d{i}',{{clipPath:'inset(0 {62 if i==0 else 100}% 0 0)',duration:.4,ease:'power2.in'}},{lt+i*.04:.3f});")
    if i: js(f"tl.to('#ph{i}',{{opacity:1,duration:.3}},{lt+.25:.3f});")
fin("#t7", lt + .25); sfx("whoosh_c.ogg", lt, -10)
JS = "\n".join(J)
json.dump(SFX, open(H_ + "/sfx97.json", "w"), indent=1)
json.dump(dict(lines=[dict(n=c["n"], text=c["line"], start=c["start"], end=c["end"]) for c in C], D=D), open(H_ + "/cues97.json", "w"), indent=1)
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
window.__reel={{duration:D,seek:t=>tl.seek(t)}};
</script></body></html>'''
open(H_ + "/hf/index.html", "w").write(html)
print("D=", D, "sfx", len(SFX), "js", len(J))
