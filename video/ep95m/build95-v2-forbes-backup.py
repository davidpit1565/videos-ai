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
D = round(e(8) + 1.0, 2)
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
<path id="f1" pathLength="1" d="M440 130 C520 130 560 190 548 262 C536 330 480 372 440 372 C400 372 344 330 332 262 C320 190 360 130 440 130 Z"/>
<path id="f2" pathLength="1" d="M338 214 C330 130 410 82 470 96 C540 108 566 150 548 214"/>
<circle id="f3" pathLength="1" cx="402" cy="252" r="30"/><circle id="f4" pathLength="1" cx="480" cy="252" r="30"/><path id="f5" pathLength="1" d="M432 252 H450"/>
<path id="f6" pathLength="1" d="M396 320 C420 346 464 346 488 320"/>
<path id="f7" pathLength="1" d="M300 470 C300 410 370 392 440 392 C510 392 580 410 580 470"/>
<rect id="f8" pathLength="1" x="640" y="330" width="170" height="120" rx="8"/><path id="f9" pathLength="1" d="M620 450 H830"/>
<path id="f10" pathLength="1" d="M90 440 H210 V380 C210 350 90 350 90 380 Z"/><path id="f11" pathLength="1" d="M150 350 C130 300 170 280 150 240 M150 330 C190 300 200 280 190 250"/>
</g></svg>'''
markup = f'''
<div class="bgw" data-decor></div>
<div id="cam">
 <div id="s1">
  {MARK.format(id="mk1")}
  <div class="h1c" id="h1c">CHATGPT</div>
  <div class="h1n" id="h1n">CARICATURE<br>PRIVACY WARNING</div>
  <div class="card1" id="card1">{FIG}<div class="warn" id="warn">!</div></div>
  <div class="tag" id="tg1" style="top:1180px;left:100px">DRAWN EXAMPLE</div>
 </div>
 <div id="s2"><div class="ui" id="ui"><div class="uih"><span class="chip dark" id="chGpt">ChatGPT</span></div>
   <div class="typed" id="typed"></div></div>
  <div class="tag" id="tg2" style="top:1090px;left:100px">PROMPT WORDING · FORBES, 9 FEB 2026</div></div>
 <div id="s3"><img class="flogo" id="flogo" src="assets/forbes-logo.png">
  <div class="big3a" id="b3a">TOOK OVER</div><div class="big3b" id="b3b">SOCIAL MEDIA</div>
  <div class="tag" id="tg3" style="top:1090px;left:100px">FORBES · 9 FEB 2026</div></div>
 <div id="s4"><div class="q4a" id="q4a">KEEP ADDING DETAILS</div><div class="q4b" id="q4b">UNTIL IT LOOKS RIGHT</div>
  <div class="bubs"><div class="bub" id="bb0">my job</div><div class="bub" id="bb1">my hobby</div><div class="bub" id="bb2">my pet</div></div>
  <div class="tag" id="tg4" style="top:1130px;left:100px">SECURITY CEO TO FORBES</div></div>
 <div id="s5"><div class="row5" id="r5a"><b class="no">✕</b><span>REAL PHOTO</span></div><div class="row5" id="r5b"><b class="yes">✓</b><span>GENERIC PROMPT</span></div>
  <div class="tag" id="tg5" style="top:1000px;left:100px">EXPERT ADVICE · FORBES</div></div>
 <div id="s6"><div class="h6" id="h6">MEMORY</div>
  <div class="tgl" id="tgl"><span class="onl" id="onl">ON</span><span class="ofl" id="ofl">OFF</span><div class="knob" id="knob"></div></div>
  <div class="tag" id="tg6a" style="top:1000px;left:100px">UK · EU</div><div class="tag" id="tg6b" style="top:1090px;left:100px">AS FORBES REPORTED IN FEB 2026</div></div>
 <div id="s7"><div class="card7" id="card7"><div class="ct7">SAFER WAY</div>
   <div class="r7" id="r7a"><b>1</b><span>DESCRIBE<br>YOURSELF IN WORDS</span></div><div class="r7" id="r7b"><b>2</b><span>OR USE<br>TEMPORARY CHAT</span></div></div></div>
 <div class="tag" id="tgs" style="top:350px;left:740px;z-index:60">SEND THIS</div>
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
.h1c{{position:absolute;left:260px;top:334px;font-size:100px;line-height:100px;font-weight:900;letter-spacing:-.045em;white-space:nowrap}}
.h1n{{position:absolute;left:92px;top:460px;font-size:96px;line-height:98px;font-weight:900;letter-spacing:-.045em;white-space:nowrap}}
.card1{{position:absolute;left:100px;top:700px;width:880px;height:480px;background:#fbfbf8;border:4px solid {INK};border-radius:8px;box-shadow:14px 14px 0 {INK};overflow:hidden}}
.fig{{position:absolute;left:0;top:-14px}}
.warn{{position:absolute;right:40px;top:30px;width:130px;height:130px;border-radius:50%;background:{INK};color:#fff;font-size:100px;line-height:130px;text-align:center;font-weight:900;opacity:0}}
.tag{{position:absolute;height:64px;padding:0 26px;background:{INK};color:#fff;font:700 34px/64px JBM,monospace;letter-spacing:.05em;border-radius:6px;white-space:nowrap;opacity:0}}
.ui{{position:absolute;left:100px;top:420px;width:880px;height:600px;background:#fff;border:4px solid {INK};border-radius:28px;box-shadow:14px 14px 0 {INK}}}
.uih{{position:absolute;left:34px;top:30px}}
.chip{{display:inline-block;height:56px;padding:0 24px;border:4px solid {INK};border-radius:28px;font:700 30px/48px JBM,monospace;background:#fbfbf8;white-space:nowrap}} .chip.dark{{background:{INK};color:#fff}}
.typed{{position:absolute;left:44px;top:120px;width:790px;font-size:64px;line-height:76px;font-weight:500;letter-spacing:-.02em}}
.flogo{{position:absolute;left:190px;top:330px;width:700px;opacity:0}}
.big3a{{position:absolute;left:75px;top:560px;font-size:160px;line-height:160px;font-weight:900;letter-spacing:-.05em;white-space:nowrap;opacity:0}}
.big3b{{position:absolute;left:75px;top:730px;font-size:128px;line-height:128px;font-weight:900;letter-spacing:-.05em;white-space:nowrap;opacity:0}}
.q4a{{position:absolute;left:75px;top:300px;font-size:74px;line-height:80px;font-weight:900;letter-spacing:-.045em;white-space:nowrap;opacity:0}}
.q4b{{position:absolute;left:75px;top:385px;font-size:74px;line-height:80px;font-weight:900;letter-spacing:-.045em;white-space:nowrap;opacity:0}}
.bubs{{position:absolute;left:100px;top:600px;width:880px}} .bub{{display:block;width:540px;margin:0 0 26px 0;padding:22px 34px;background:#fff;border:5px solid {INK};border-radius:28px;font-size:60px;line-height:68px;box-shadow:8px 8px 0 {INK};opacity:0}} .bub:nth-child(2){{margin-left:150px}} .bub:nth-child(3){{margin-left:300px}}
.row5{{position:absolute;left:100px;width:880px;height:230px;background:#fbfbf8;border:4px solid {INK};border-radius:10px;box-shadow:12px 12px 0 {INK};display:flex;align-items:center;gap:36px;padding:0 44px;opacity:0}} #r5a{{top:380px}} #r5b{{top:660px}}
.row5 b{{flex:none;width:130px;height:130px;border-radius:16px;font-size:100px;line-height:126px;text-align:center;font-weight:900}} .no{{background:#fff;color:{INK};border:7px solid {INK}}} .yes{{background:{INK};color:#fff}}
.row5 span{{font-size:78px;line-height:80px;font-weight:900;letter-spacing:-.04em}}
.h6{{position:absolute;left:75px;top:300px;font-size:150px;line-height:150px;font-weight:900;letter-spacing:-.05em;opacity:0}}
.tgl{{position:absolute;left:140px;top:520px;width:800px;height:300px;border:10px solid {INK};border-radius:150px;background:#fbfbf8;box-shadow:14px 14px 0 {INK};opacity:0}}
.knob{{position:absolute;left:520px;top:30px;width:230px;height:230px;border-radius:50%;background:{INK}}}
.onl,.ofl{{position:absolute;top:96px;font-size:110px;line-height:110px;font-weight:900;letter-spacing:-.03em}} .onl{{left:60px}} .ofl{{left:520px;opacity:0;color:#bbb}}
.card7{{position:absolute;left:100px;top:340px;width:880px;height:800px;background:#fbfbf8;border:4px solid {INK};border-radius:8px;box-shadow:14px 14px 0 {INK};opacity:0}}
.ct7{{position:absolute;left:50px;top:40px;font-size:120px;line-height:120px;font-weight:900;letter-spacing:-.045em}}
.r7{{position:absolute;left:50px;width:780px;height:230px;display:flex;align-items:center;gap:34px;opacity:0}} #r7a{{top:230px}} #r7b{{top:500px}}
.r7 b{{flex:none;width:130px;height:130px;border-radius:14px;background:{INK};color:#fff;font-size:88px;line-height:130px;text-align:center;font-weight:900}}
.r7 span{{font-size:60px;line-height:66px;font-weight:900;letter-spacing:-.035em}}
.L{{opacity:0}}
'''
t_priv = W("privacy", 0, default=1.0); t_warn = W("warning", 0, after=t_priv, default=1.6)
t_job = W("job", 0, after=s(2), default=s(2) + 2.0)
t_for = W("forbes", 0, after=s(3), default=s(3) + .6); t_feb = W("february", 0, after=s(3), default=s(3) + 2.0)
t_sec = W("security", 0, after=s(4), default=s(4) + .5); t_pers = W("personal", 0, after=s(4), default=s(4) + 2.0); t_right = W("right", 0, after=t_pers, default=s(4) + 3.6)
t_photo = W("photo", 0, after=s(5), default=s(5) + 1.4); t_gen = W("generic", 0, after=s(5), default=s(5) + 2.6)
t_mem = W("memory", 0, after=s(6), default=s(6) + .4); t_off = W("off", 0, after=s(6), default=s(6) + 1.2)
t_desc = W("describe", 0, after=s(7), default=s(7) + .8); t_temp = W("temporary", 0, after=s(7), default=s(7) + 2.0)
js(f"tl.fromTo('#cam',{{scale:1.0,y:0}},{{scale:1.03,y:-12,duration:{D},ease:'sine.inOut'}},0);")
# S1 hook: mark + CHATGPT, CARICATURE / PRIVACY WARNING, a drawn caricature stand-in being sketched, warning badge slams on
js("gsap.set('#warn',{opacity:0}); gsap.set('#tg1',{opacity:0});")
js(f"tl.fromTo('#mk1',{{rotate:-25}},{{rotate:0,duration:.7,ease:'sine.out',immediateRender:false}},0);")
js("tl.fromTo('#h1n',{x:-18},{x:0,duration:.5,ease:'power2.out',immediateRender:false},0);")
for i in range(1, 12):
    js(f"tl.fromTo('#f{i}',{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:.55,ease:'sine.inOut',immediateRender:false}},{.05 + i * .07:.3f});")
js(f"tl.fromTo('#warn',{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:.2,ease:'expo.out',immediateRender:false}},{max(.5, t_warn - .15):.3f});")
sfx("pop_a.ogg", .2, -8); sfx("impactpunch.ogg", max(.5, t_warn - .15) + .03, -6)
fin("#tg1", .9, .35, 14, 6)
fout("#s1", s(2) - .08, .3)
# S2 prompt typed (wording is Forbes')
js("gsap.set('#s2',{opacity:1}); gsap.set('#ui,#tg2,#chGpt,#typed',{opacity:0});")
fin("#ui", s(2) + .02, .45, 40, 12, .97); sfx("whoosh_b.ogg", s(2) - .04, -9)
fin("#chGpt", s(2) + .3, .3, 14, 6)
js(f"gsap.set('#typed',{{opacity:1}}); (function(){{var el=document.getElementById('typed');el.innerHTML='';var sp=[];for(var i=0;i<{len(PROMPT)};i++){{var q=document.createElement('span');q.textContent={json.dumps(PROMPT)}[i];q.style.opacity=0;el.appendChild(q);sp.push(q);}}window.__sp=sp;}})();")
t0 = s(2) + .6; tn = max(2.0, (e(2) - t0) - .5)
js(f"tl.to(window.__sp,{{opacity:1,duration:.02,stagger:{tn/len(PROMPT):.4f}}},{t0:.3f});")
for k in range(0, 14, 2): sfx("click_a.ogg" if k % 4 == 0 else "click_b.ogg", t0 + k * tn / 14, -14)
fin("#tg2", s(2) + 1.0, .35, 14, 6)
fout("#s2", s(3) - .08, .3)
# S3 Forbes
js("gsap.set('#s3',{opacity:1}); gsap.set('#flogo,#b3a,#b3b,#tg3',{opacity:0});")
fin("#flogo", t_for - .1, .45, 30, 10, .96); sfx("pop_a.ogg", t_for, -8)
fin("#b3a", t_feb - .9, .4, 24, 8); fin("#b3b", t_feb - .5, .4, 24, 8); sfx("impactsoft.ogg", t_feb - .85, -6)
fin("#tg3", t_feb - .1, .35, 14, 6)
fout("#s3", s(4) - .08, .3)
# S4 keep adding details
js("gsap.set('#s4',{opacity:1}); gsap.set('#q4a,#q4b,#bb0,#bb1,#bb2,#tg4',{opacity:0});")
fin("#q4a", t_pers - .5, .4, 24, 8); fin("#q4b", t_right - .6, .4, 24, 8)
for k in range(3):
    tt = s(4) + .8 + k * .55
    fin(f"#bb{k}", tt, .35, 40, 8, .94); sfx("pop_b.ogg" if k % 2 else "pop_a.ogg", tt + .05, -8)
fin("#tg4", t_sec - .1, .35, 14, 6)
fout("#s4", s(5) - .08, .3)
# S5 no real photo / generic prompt
js("gsap.set('#s5',{opacity:1}); gsap.set('#r5a,#r5b,#tg5',{opacity:0});")
fin("#r5a", t_photo - .4, .4, 36, 10, .96); sfx("tick.ogg", t_photo - .3, -7)
fin("#r5b", t_gen - .35, .4, 36, 10, .96); sfx("tick.ogg", t_gen - .25, -7)
fin("#tg5", s(5) + .5, .35, 14, 6)
fout("#s5", s(6) - .08, .3)
# S6 memory toggle
js("gsap.set('#s6',{opacity:1}); gsap.set('#h6,#tgl,#tg6a,#tg6b',{opacity:0});")
fin("#h6", t_mem - .1, .35, 24, 8); fin("#tgl", t_mem + .1, .4, 30, 10, .95)
js(f"tl.to('#knob',{{left:40,duration:.34,ease:'power3.inOut'}},{t_off:.3f});tl.to('#onl',{{opacity:0,duration:.2}},{t_off:.3f});tl.to('#ofl',{{opacity:1,color:'#0f0f0f',duration:.25}},{t_off+.1:.3f});")
sfx("toggle.ogg", t_off + .12, -4)
fin("#tg6a", t_off + .5, .3, 14, 6); fin("#tg6b", t_off + .8, .3, 14, 6)
fout("#s6", s(7) - .08, .3)
# S7 safer way card
js("gsap.set('#s7',{opacity:1}); gsap.set('#card7,#r7a,#r7b',{opacity:0});")
fin("#card7", s(7) - .02, .45, 40, 14, .96); sfx("whoosh_b.ogg", s(7) - .05, -9)
fin("#r7a", t_desc - .2, .35, 24, 8); sfx("pop_a.ogg", t_desc - .1, -8)
fin("#r7b", t_temp - .3, .35, 24, 8); sfx("pop_b.ogg", t_temp - .2, -8)
fout("#s7", s(8) - .1, .3)
# S8 loop
js(f"tl.fromTo('#s1',{{opacity:0,filter:'blur(14px)'}},{{opacity:1,filter:'blur(0px)',duration:.4,ease:'power2.out',immediateRender:false}},{s(8)-.02:.3f});")
js(f"tl.set('#tg1',{{opacity:0}},{s(8)-.02:.3f});")
fin("#tgs", s(8) + .3, .3, 14, 6); sfx("whoosh_c.ogg", s(8) - .05, -10)
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
