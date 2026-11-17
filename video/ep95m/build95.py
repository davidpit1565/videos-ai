#!/usr/bin/env python3
"""ep95 'ChatGPT caricature privacy warning' reel, Miki style. Facts only from Forbes (Kate O'Flaherty, 9 Feb 2026).
Reads voice/narration-raw-cues.json (+ voice/words.json) -> hf/index.html, sfx95m.json, cues95m.json."""
import json, os, re
H_ = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(H_ + "/voice/narration-raw-cues.json"))
C = C if isinstance(C, list) else C["lines"]
L = {c["n"]: (c["start"], c["end"]) for c in C}
s = lambda n: L[n][0]
e = lambda n: L[n][1]
D = round(e(6) + 1.4, 2)
INK = "#0f0f0f"
J = []; SFX = []
def js(x): J.append(x)
def sfx(f, t, g=-6): SFX.append(dict(f=f, t=round(t, 3), g=g))
def fin(sel, t, d=.4, y=30, blur=14, sc=None):
    sc_ = f",scale:{sc}" if sc else ""
    js(f"tl.fromTo('{sel}',{{opacity:0,y:{y},filter:'blur({blur}px)'{sc_}}},{{opacity:1,y:0,scale:1,filter:'blur(0px)',duration:{d},ease:'power2.out',immediateRender:false}},{max(0,t):.3f});")
def fout(sel, t, d=.3, blur=14, y=-20):
    js(f"tl.to('{sel}',{{opacity:0,y:{y},filter:'blur({blur}px)',duration:{d},ease:'power1.in'}},{max(0,t):.3f});")
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
PROMPT = "Create a caricature of me and my job based on everything you know about me."
MARK = '<img class="mk" id="{id}" src="assets/chatgpt-mark.svg">'
FIG = f'''<svg viewBox="0 0 880 510" width="880" height="510" class="fig">
<g fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">
<g id="hd"><path id="f1" pathLength="1" d="M440 130 C520 130 560 190 548 262 C536 330 480 372 440 372 C400 372 344 330 332 262 C320 190 360 130 440 130 Z"/>
<path id="f2" pathLength="1" d="M338 214 C330 130 410 82 470 96 C540 108 566 150 548 214"/>
<circle id="f3" pathLength="1" cx="402" cy="252" r="30"/><circle id="f4" pathLength="1" cx="480" cy="252" r="30"/><path id="f5" pathLength="1" d="M432 252 H450"/>
<path id="f6" pathLength="1" d="M396 320 C420 346 464 346 488 320"/></g>
<path id="f7" pathLength="1" d="M300 470 C300 410 370 392 440 392 C510 392 580 410 580 470"/>
<rect id="f8" pathLength="1" x="640" y="330" width="170" height="120" rx="8"/><path id="f9" pathLength="1" d="M620 450 H830"/>
<path id="f10" pathLength="1" d="M90 440 H210 V380 C210 350 90 350 90 380 Z"/><path id="f11" pathLength="1" d="M150 350 C130 300 170 280 150 240 M150 330 C190 300 200 280 190 250"/>
<path id="sp1" d="M640 120 V170 M615 145 H665"/><path id="sp2" d="M240 110 V150 M220 130 H260"/><path id="sp3" d="M700 250 V280 M685 265 H715"/><path id="sp4" d="M180 250 V290 M160 270 H200"/></g></svg>'''
FIG2 = FIG.replace('id="f','id="g').replace('id="sp','id="zp').replace('id="hd"','id="hd2"')
def mini(i, hair, extra):
    return f'''<div class="mf" id="mf{i}"><svg viewBox="0 0 200 200" width="200" height="200"><g fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"><circle cx="100" cy="100" r="58"/>{hair}<circle cx="80" cy="98" r="12"/><circle cx="120" cy="98" r="12"/><path d="M80 134 C92 148 108 148 120 134"/>{extra}</g></svg></div>'''
MINIS = [
 mini(0, '<path d="M48 90 C46 40 140 30 152 90"/>', ''),
 mini(1, '<path d="M44 96 C40 30 160 30 156 96 M44 96 C30 130 40 160 52 168"/>', ''),
 mini(2, '<path d="M60 46 H140 M72 46 V30 H128 V46"/>', ''),
 mini(3, '<path d="M50 88 C54 52 146 52 150 88"/>', '<path d="M70 150 C90 176 110 176 130 150"/>'),
 mini(4, '<path d="M46 92 C40 44 100 24 150 56 C160 70 156 84 154 94"/>', '<circle cx="150" cy="150" r="14"/>'),
 mini(5, '<path d="M56 74 L72 40 L100 66 L128 40 L144 74"/>', ''),
]
markup = f'''
<div class="bgw" data-decor></div>
<div id="cam">
 <div id="s1">
  {MARK.format(id="mk1")}
  <div class="h1c" id="h1c">ASK CHATGPT</div>
  <div class="h1n" id="h1n">TO DRAW YOU</div>
  <div class="card1" id="card1">{FIG}</div>
  <div class="tag" id="tg1" style="top:1180px;left:100px">DRAWN EXAMPLE</div>
 </div>
 <div id="s2"><div class="mgrid">{"".join(MINIS)}</div><div class="h2" id="h2">EVERYWHERE<br>ONLINE</div>
  <div class="tag" id="tg2" style="top:1170px;left:100px">DRAWN EXAMPLES</div></div>
 <div id="s3"><img class="mk3" id="mk3" src="assets/chatgpt-mark.svg"><div class="h3a" id="h3a">HERE'S</div><div class="h3b" id="h3b">HOW</div>
  <div class="steps3" id="st3"><div class="st"><b>1</b><span>OPEN CHATGPT</span></div></div></div>
 <div id="s4"><div class="ui" id="ui"><div class="uih"><span class="chip dark" id="chGpt">ChatGPT</span></div>
   <div class="typed" id="typed"></div></div>
  <div class="tag" id="tg4" style="top:1090px;left:100px">2 · TYPE THIS</div></div>
 <div id="s5"><div class="row5" id="r5a"><b class="yes">✓</b><span>TELL IT ABOUT YOU</span></div><div class="row5" id="r5b"><b class="no">✕</b><span>REAL PHOTO</span></div></div>
 <div id="s6"><div class="card1 c6" id="card6">{FIG2}</div><div class="tag" id="tg6" style="top:1180px;left:100px">3 · WATCH IT DRAW YOU</div></div>
 <div id="s7"><div class="card7" id="card7"><div class="ct7">SAVE THIS</div><div class="pr7" id="pr7">Create a caricature of me and my job based on everything you know about me.</div></div></div>
 <div class="tag" id="tgs" style="top:1184px;left:100px;z-index:60">SEND THIS</div>
</div>
'''
css = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;font-weight:500;color:{INK}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}}
.bgw{{position:absolute;left:0;top:0;width:1080px;height:1920px;background:#ecebe5 url(assets/bg.jpg);background-size:1080px 1920px}}
#cam{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}}
#s1,#s2,#s3,#s4,#s5,#s6,#s7{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
#s2,#s3,#s4,#s5,#s6,#s7,#tgs{{opacity:0}}
.mk{{position:absolute;width:150px;height:150px;left:90px;top:320px}}
.h1c{{position:absolute;left:260px;top:346px;font-size:92px;line-height:92px;font-weight:900;letter-spacing:-.045em;white-space:nowrap}}
.h1n{{position:absolute;left:92px;top:490px;font-size:128px;line-height:128px;font-weight:900;letter-spacing:-.045em;white-space:nowrap}}
.card1{{position:absolute;left:100px;top:700px;width:880px;height:480px;background:#fbfbf8;border:4px solid {INK};border-radius:8px;box-shadow:14px 14px 0 {INK};overflow:hidden}}
.fig{{position:absolute;left:0;top:-14px}}
.tag{{position:absolute;height:64px;padding:0 26px;background:{INK};color:#fff;font:700 34px/64px JBM,monospace;letter-spacing:.05em;border-radius:6px;white-space:nowrap;opacity:0}}
.mgrid{{position:absolute;left:100px;top:300px;width:880px;display:flex;flex-wrap:wrap;gap:30px 40px;justify-content:center}}
.mf{{width:250px;height:250px;background:#fbfbf8;border:4px solid {INK};border-radius:10px;box-shadow:8px 8px 0 {INK};display:flex;align-items:center;justify-content:center;opacity:0}}
.h2{{position:absolute;left:75px;top:880px;font-size:112px;line-height:112px;font-weight:900;letter-spacing:-.05em;opacity:0;white-space:nowrap}}
.mk3{{position:absolute;left:100px;top:310px;width:200px;height:200px;opacity:0}}
.h3a{{position:absolute;left:340px;top:310px;font-size:150px;line-height:150px;font-weight:900;letter-spacing:-.05em;opacity:0}}
.h3b{{position:absolute;left:340px;top:475px;font-size:150px;line-height:150px;font-weight:900;letter-spacing:-.05em;opacity:0}}
.steps3{{position:absolute;left:100px;top:700px;width:880px;opacity:0}}
.st{{display:flex;align-items:center;gap:40px;height:240px;background:#fbfbf8;border:4px solid {INK};border-radius:10px;box-shadow:12px 12px 0 {INK};padding:0 44px}}
.st b{{flex:none;width:140px;height:140px;border-radius:16px;background:{INK};color:#fff;font-size:100px;line-height:140px;text-align:center;font-weight:900}} .st span{{font-size:84px;line-height:88px;font-weight:900;letter-spacing:-.04em}}
.ui{{position:absolute;left:100px;top:420px;width:880px;height:600px;background:#fff;border:4px solid {INK};border-radius:28px;box-shadow:14px 14px 0 {INK}}}
.uih{{position:absolute;left:34px;top:30px}}
.chip{{display:inline-block;height:56px;padding:0 24px;border:4px solid {INK};border-radius:28px;font:700 30px/48px JBM,monospace;background:#fbfbf8;white-space:nowrap}} .chip.dark{{background:{INK};color:#fff}}
.typed{{position:absolute;left:44px;top:120px;width:790px;font-size:64px;line-height:76px;font-weight:500;letter-spacing:-.02em}}
.row5{{position:absolute;left:100px;width:880px;height:240px;background:#fbfbf8;border:4px solid {INK};border-radius:10px;box-shadow:12px 12px 0 {INK};display:flex;align-items:center;gap:36px;padding:0 44px;opacity:0}} #r5a{{top:400px}} #r5b{{top:690px}}
.row5 b{{flex:none;width:130px;height:130px;border-radius:16px;font-size:100px;line-height:126px;text-align:center;font-weight:900}} .no{{background:#fff;color:{INK};border:7px solid {INK}}} .yes{{background:{INK};color:#fff}}
.row5 span{{font-size:60px;line-height:64px;font-weight:900;letter-spacing:-.04em}}
.c6{{top:420px;height:700px}} .c6 .fig{{top:60px}}
.card7{{position:absolute;left:100px;top:380px;width:880px;height:700px;background:#fbfbf8;border:4px solid {INK};border-radius:8px;box-shadow:14px 14px 0 {INK};opacity:0}}
.ct7{{position:absolute;left:50px;top:40px;font-size:130px;line-height:130px;font-weight:900;letter-spacing:-.045em}}
.pr7{{position:absolute;left:50px;top:230px;width:780px;font-size:62px;line-height:76px;font-weight:500;letter-spacing:-.02em;border:5px dashed {INK};border-radius:20px;padding:34px 40px}}
.L{{opacity:0}}
'''
t_cart = W("cartoon", 0, default=1.6)
t_took = W("took", 0, after=s(2), default=s(2) + .8); t_soc = W("social", 0, after=s(2), default=s(2) + 1.6)
t_how = W("how", 0, after=s(3), default=s(3) + .5); t_open = W("open", 0, after=s(3), default=s(3) + 1.4)
t_type = W("type", 0, after=s(4), default=s(4) + .3)
t_watch = W("watch", 0, after=s(5), default=s(5) + .4)
t_save = W("save", 0, after=s(6), default=s(6) + .1)
js(f"tl.fromTo('#cam',{{scale:1.0,y:0}},{{scale:1.03,y:-12,duration:{D},ease:'sine.inOut'}},0);")
# S1 hook: ChatGPT mark + CHATGPT / DRAWS YOU AS A CARTOON, a drawn figure sketches itself
js("gsap.set('#tg1',{opacity:0});")
js("tl.fromTo('#mk1',{rotate:-25},{rotate:0,duration:.7,ease:'sine.out',immediateRender:false},0);")
js("tl.fromTo('#h1n',{x:-18},{x:0,duration:.5,ease:'power2.out',immediateRender:false},0);")
js("gsap.set('#f1,#f2',{strokeDasharray:1,strokeDashoffset:0}); gsap.set('#f3,#f4,#f5,#f6,#f7,#f8,#f9,#f10,#f11',{strokeDasharray:1,strokeDashoffset:1});")
for i in range(1, 12):
    js(f"tl.to('#f{i}',{{strokeDashoffset:0,duration:.55,ease:'sine.inOut'}},{.05 + i * .06:.3f});") if i>2 else None
js("gsap.set('#sp1,#sp2,#sp3,#sp4',{opacity:0});")
for k in range(1, 5):
    js(f"tl.fromTo('#sp{k}',{{opacity:0,scale:.2,transformOrigin:'50% 50%'}},{{opacity:1,scale:1,duration:.25,ease:'back.out(2)',immediateRender:false}},{1.0 + k * .12:.3f});")
for k in range(0, 5):
    js(f"tl.to('#hd',{{y:-9,rotate:{2 if k%2==0 else -2},duration:.5,ease:'sine.inOut',yoyo:true,repeat:1,transformOrigin:'440px 300px'}},{1.2 + k * 1.0:.3f});")
sfx("pop_a.ogg", .2, -8); sfx("pop_b.ogg", 1.1, -7)
fin("#tg1", .9, .35, 14, 6)
fout("#s1", s(2) - .08, .3)
# S2 everywhere online: six different drawn faces pop in
js("gsap.set('#s2',{opacity:1}); gsap.set('.mf,#h2,#tg2',{opacity:0});")
for i in range(6):
    tt = s(2) + .05 + i * .16
    fin(f"#mf{i}", tt, .3, 30, 6, .9); sfx("pop_a.ogg" if i % 2 == 0 else "pop_b.ogg", tt + .04, -10)
fin("#h2", t_soc - .5, .4, 24, 8); fin("#tg2", s(2) + 1.4, .35, 14, 6)
fout("#s2", s(3) - .08, .3)
# S3 HERE'S HOW + step 1
js("gsap.set('#s3',{opacity:1}); gsap.set('#mk3,#h3a,#h3b,#st3',{opacity:0});")
fin("#mk3", s(3) + .02, .4, 24, 8, .9); fin("#h3a", s(3) + .08, .35, 24, 8); fin("#h3b", t_how - .05, .35, 24, 8); sfx("impactsoft.ogg", t_how, -6)
fin("#st3", t_open - .3, .4, 36, 10, .96); sfx("pop_a.ogg", t_open - .2, -8)
fout("#s3", s(4) - .08, .3)
# S4 type the prompt (Forbes wording, not named)
js("gsap.set('#s4',{opacity:1}); gsap.set('#ui,#tg4,#chGpt,#typed',{opacity:0});")
fin("#ui", s(4) + .02, .45, 40, 12, .97); sfx("whoosh_b.ogg", s(4) - .04, -9)
fin("#chGpt", s(4) + .25, .3, 14, 6)
js(f"gsap.set('#typed',{{opacity:1}}); (function(){{var el=document.getElementById('typed');el.innerHTML='';var sp=[];for(var i=0;i<{len(PROMPT)};i++){{var q=document.createElement('span');q.textContent={json.dumps(PROMPT)}[i];q.style.opacity=0;el.appendChild(q);sp.push(q);}}window.__sp=sp;}})();")
t0 = s(4) + .6; tn = max(2.0, (e(4) - t0) - .3)
js(f"tl.to(window.__sp,{{opacity:1,duration:.02,stagger:{tn/len(PROMPT):.4f}}},{t0:.3f});")
for k in range(0, 14, 2): sfx("click_a.ogg" if k % 4 == 0 else "click_b.ogg", t0 + k * tn / 14, -14)
fin("#tg4", s(4) + .5, .35, 14, 6)
fout("#s4", s(5) - .08, .3)
# S6 watch it draw you
js("gsap.set('#s6',{opacity:1}); gsap.set('#card6,#tg6',{opacity:0});")
fin("#card6", s(5) + .02, .4, 40, 12, .97); sfx("whoosh_a.ogg", s(5) - .04, -9)
js("gsap.set('#g1,#g2,#g3,#g4,#g5,#g6,#g7,#g8,#g9,#g10,#g11',{strokeDasharray:1,strokeDashoffset:1});")
for i in range(1, 12):
    js(f"tl.to('#g{i}',{{strokeDashoffset:0,duration:.5,ease:'sine.inOut'}},{t_watch + .15 + i * .09:.3f});")
sfx("ding.ogg", t_watch + 1.3, -9)
fin("#tg6", s(5) + .5, .35, 14, 6)
fout("#s6", s(6) - .08, .3)
# S7 save card, then loop to the hook frame
js("gsap.set('#s7',{opacity:1}); gsap.set('#card7',{opacity:0});")
fin("#card7", s(6) - .02, .45, 40, 14, .96); sfx("whoosh_b.ogg", s(6) - .05, -9)
js(f"tl.fromTo('#card7',{{y:0}},{{y:-14,duration:{e(6)-s(6)+.2:.2f},ease:'sine.inOut'}},{s(6)+.4:.3f});")
fout("#s7", e(6) + .1, .3)
js(f"tl.fromTo('#s1',{{opacity:0,filter:'blur(14px)'}},{{opacity:1,filter:'blur(0px)',duration:.4,ease:'power2.out',immediateRender:false}},{e(6)+.15:.3f});")
js(f"tl.set('#tg1',{{opacity:0}},{e(6)+.15:.3f});")
fin("#tgs", e(6) + .35, .3, 14, 6); sfx("whoosh_c.ogg", e(6) + .1, -10)
JS = "\n".join(J)
json.dump(SFX, open(H_ + "/sfx95m.json", "w"), indent=1)
json.dump(dict(lines=[dict(n=c["n"], text=c["line"], start=c["start"], end=c["end"]) for c in C], D=D), open(H_ + "/cues95m.json", "w"), indent=1)
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
