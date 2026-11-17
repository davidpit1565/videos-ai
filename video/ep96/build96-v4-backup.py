#!/usr/bin/env python3
"""ep96 'AI solves black hole math. So I give it one sentence.' Miki style. The game on screen is the REAL game
(video/ep96/game/game.js) built by Claude Fable 5.2 from one sentence on 13.11.2026; here it is re-simulated per frame by its own bot.
Reads voice/narration-raw-cues.json (+ voice/words.json) -> hf/index.html, sfx96.json, cues96.json."""
import json, os, re
H_ = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(H_ + "/voice/narration-raw-cues.json"))
C = C if isinstance(C, list) else C["lines"]
L = {c["n"]: (c["start"], c["end"]) for c in C}
s = lambda n: L[n][0]
e = lambda n: L[n][1]
D = round(e(7) + 1.5, 2)
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
PROMPT = "Build me a game where a cat runs from a vacuum cleaner."
HOLE = f'''<svg viewBox="0 0 880 520" width="880" height="520" class="hole"><g id="hg">
<ellipse cx="440" cy="270" rx="330" ry="92" fill="none" stroke="{INK}" stroke-width="10" stroke-dasharray="26 22" id="ring1"/>
<ellipse cx="440" cy="270" rx="250" ry="62" fill="none" stroke="{INK}" stroke-width="16" id="ring2"/>
<circle cx="440" cy="250" r="150" fill="{INK}" id="disc"/>
<path d="M190 270 A250 62 0 0 0 690 270" fill="none" stroke="#fbfbf8" stroke-width="16"/>
<path d="M190 270 A250 62 0 0 0 690 270" fill="none" stroke="{INK}" stroke-width="16" stroke-dasharray="1 0" opacity="1" transform="translate(0,0)" id="ringfront"/>
</g></svg>'''
DEVS = "".join(f'''<div class="dev" id="dv{i}"><svg viewBox="0 0 240 300" width="240" height="300"><g fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"><rect x="30" y="50" width="180" height="200" rx="14"/><rect x="82" y="110" width="76" height="76" rx="6" fill="{INK}"/>{"".join(f'<path d="M{58+k*42} 50 V22 M{58+k*42} 250 V278"/>' for k in range(4))}<path d="M30 110 H6 M30 190 H6 M210 110 H234 M210 190 H234"/></g><circle id="led{i}" cx="186" cy="76" r="13" fill="{INK}"/></svg></div>''' for i in range(3))
markup = f'''
<div class="bgw" data-decor></div>
<div id="cam">
 <div id="s1">
  <div class="h1a" id="h1a">AI SOLVES</div><div class="h1b" id="h1b">BLACK HOLE MATH</div>
  <div class="card1" id="card1">{HOLE}</div>
  <div class="tag" id="tg1" style="top:1180px;left:100px">2 OPEN PROBLEMS · ANTHROPIC'S CLAIM</div>
 </div>
 <div id="s3"><div class="h3" id="h3">FAMOUS PROOF</div><div class="eq" id="eq">x<sup>n</sup> + y<sup>n</sup> = z<sup>n</sup></div>
  <div class="arrow" id="arw">↓</div><div class="code3" id="code3"><span>theorem fermat :</span><span>&nbsp;&nbsp;proved ✓</span></div><div class="n3b" id="n3b">30 HOURS</div>
  <div class="tag" id="tg3" style="top:1184px;left:100px">FERMAT'S LAST THEOREM · AS CODE</div></div>
 <div id="s4"><div class="h4a" id="h4a">3 WORKING</div><div class="h4b" id="h4b">DEVICES</div><div class="devs">{DEVS}</div>
  <div class="tag" id="tg4" style="top:1100px;left:100px">DESIGNED FROM SCRATCH</div></div>
 <div id="s5"><img class="mkbig" id="mk5" src="assets/claude-mark.svg"><div class="h5a" id="h5a">CLAUDE</div><div class="h5b" id="h5b">FABLE 5.2</div>
  <div class="tag" id="tg5" style="top:1100px;left:100px">NEW THIS WEEK</div></div>
 <div id="s6"><div class="row6" id="r6a"><b class="yes">?</b><span>ANTHROPIC'S OWN CLAIMS</span></div><div class="row6" id="r6b"><b class="no">✕</b><span>NOT CHECKED OUTSIDE YET</span></div></div>
 <div id="s7"><div class="h7a" id="h7a">WHAT WOULD</div><div class="h7b" id="h7b">YOU ASK IT?</div></div>
</div>
'''
css = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;font-weight:500;color:{INK}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}}
.bgw{{position:absolute;left:0;top:0;width:1080px;height:1920px;background:#ecebe5 url(assets/bg.jpg);background-size:1080px 1920px}}
#cam{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}}
#s1,#s3,#s4,#s5,#s6,#s7{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
#s3,#s4,#s5,#s6,#s7{{opacity:0}}
.h1a{{position:absolute;left:88px;top:322px;font-size:150px;line-height:150px;font-weight:900;letter-spacing:-.05em;white-space:nowrap}}
.h1b{{position:absolute;left:88px;top:478px;font-size:96px;line-height:96px;font-weight:900;letter-spacing:-.045em;white-space:nowrap}}
.card1{{position:absolute;left:100px;top:640px;width:880px;height:520px;background:#fbfbf8;border:4px solid {INK};border-radius:8px;box-shadow:14px 14px 0 {INK};overflow:hidden}}
.hole{{position:absolute;left:0;top:0}}
.tag{{position:absolute;height:64px;padding:0 26px;background:{INK};color:#fff;font:700 34px/64px JBM,monospace;letter-spacing:.05em;border-radius:6px;white-space:nowrap;opacity:0}}
.h2{{position:absolute;left:88px;top:300px;font-size:116px;line-height:116px;font-weight:900;letter-spacing:-.05em;white-space:nowrap;opacity:0}}
.ui{{position:absolute;left:100px;top:470px;width:880px;height:560px;background:#fff;border:4px solid {INK};border-radius:28px;box-shadow:14px 14px 0 {INK};opacity:0}}
.uih{{position:absolute;left:34px;top:30px}}
.chip{{display:inline-block;height:56px;padding:0 24px;border:4px solid {INK};border-radius:28px;font:700 30px/48px JBM,monospace;background:{INK};color:#fff;white-space:nowrap}}
.typed{{position:absolute;left:44px;top:120px;width:790px;font-size:68px;line-height:80px;font-weight:500;letter-spacing:-.02em}}
.n3{{position:absolute;left:88px;top:286px;font-size:128px;line-height:128px;font-weight:900;letter-spacing:-.05em;white-space:nowrap;opacity:0}}
.n5{{font-size:92px;top:300px}}
.gcard{{position:absolute;left:100px;top:420px;width:880px;height:760px;background:#fbfbf8;border:4px solid {INK};border-radius:8px;box-shadow:14px 14px 0 {INK};overflow:hidden;opacity:0}}
.gcard canvas{{display:block;width:880px;height:760px}}
.mkbig{{position:absolute;left:340px;top:330px;width:400px;height:400px;opacity:0}}
.h5a{{position:absolute;left:100px;width:880px;text-align:center;top:770px;font-size:150px;line-height:150px;font-weight:900;letter-spacing:-.05em;opacity:0}}
.h5b{{position:absolute;left:100px;width:880px;text-align:center;top:920px;font-size:150px;line-height:150px;font-weight:900;letter-spacing:-.05em;opacity:0}}
.row6{{position:absolute;left:100px;width:880px;height:240px;background:#fbfbf8;border:4px solid {INK};border-radius:10px;box-shadow:12px 12px 0 {INK};display:flex;align-items:center;gap:36px;padding:0 44px;opacity:0}} #r6a{{top:400px}} #r6b{{top:690px}}
.row6 b{{flex:none;width:130px;height:130px;border-radius:16px;font-size:100px;line-height:126px;text-align:center;font-weight:900}} .no{{background:#fff;color:{INK};border:7px solid {INK}}} .yes{{background:{INK};color:#fff}}
.row6 span{{font-size:50px;line-height:56px;font-weight:900;letter-spacing:-.04em}}
.h3{{position:absolute;left:88px;top:300px;font-size:116px;line-height:116px;font-weight:900;letter-spacing:-.05em;white-space:nowrap;opacity:0}}
.eq{{position:absolute;left:100px;top:470px;width:880px;height:220px;background:#fbfbf8;border:4px solid {INK};border-radius:8px;box-shadow:12px 12px 0 {INK};font-size:124px;line-height:210px;text-align:center;font-weight:900;letter-spacing:-.03em;opacity:0}} .eq sup{{font-size:64px}}
.arrow{{position:absolute;left:480px;top:700px;font-size:110px;line-height:110px;font-weight:900;opacity:0}}
.code3{{position:absolute;left:100px;top:820px;width:880px;height:200px;background:{INK};border-radius:14px;box-shadow:12px 12px 0 #8a8a86;padding:28px 40px;color:#fff;font:700 50px/72px JBM,monospace;opacity:0}} .code3 span{{display:block;white-space:nowrap}}
.n3b{{position:absolute;left:88px;top:1040px;font-size:128px;line-height:128px;font-weight:900;letter-spacing:-.05em;white-space:nowrap;opacity:0}}
.h4a{{position:absolute;left:88px;top:300px;font-size:140px;line-height:140px;font-weight:900;letter-spacing:-.05em;white-space:nowrap;opacity:0}}
.h4b{{position:absolute;left:88px;top:440px;font-size:140px;line-height:140px;font-weight:900;letter-spacing:-.05em;white-space:nowrap;opacity:0}}
.devs{{position:absolute;left:100px;top:660px;width:880px;display:flex;justify-content:space-between}} .dev{{width:270px;height:340px;background:#fbfbf8;border:4px solid {INK};border-radius:10px;box-shadow:10px 10px 0 {INK};display:flex;align-items:center;justify-content:center;opacity:0}}
.h7a{{position:absolute;left:88px;top:320px;font-size:128px;line-height:128px;white-space:nowrap;font-weight:900;letter-spacing:-.055em;opacity:0}}
.h7b{{position:absolute;left:88px;top:460px;font-size:128px;line-height:128px;white-space:nowrap;font-weight:900;letter-spacing:-.055em;opacity:0}}
'''
t_hole = W("black", 0, default=.6)
t_two = W("two", 0, after=s(2), default=s(2) + .1)
t_code = W("code", 0, after=s(3), default=s(3) + 1.8); t_thirty = W("thirty", 0, after=s(3), default=s(3) + 2.6) or s(3) + 2.6
t_three = W("three", 0, after=s(4), default=s(4) + .6); t_scr = W("scratch", 0, after=s(4), default=s(4) + 2.0)
t_nob = W("nobody", 0, after=s(6), default=s(6) + 2.2)
js(f"tl.fromTo('#cam',{{scale:1.0,y:0}},{{scale:1.03,y:-12,duration:{D},ease:'sine.inOut'}},0);")
# S1 hook + line 2: the black hole, turning from frame 0
js("gsap.set('#tg1',{opacity:0});")
js(f"tl.fromTo('#ring1',{{strokeDashoffset:0}},{{strokeDashoffset:-1400,duration:{s(3)+1:.2f},ease:'none'}},0);")
js(f"tl.fromTo('#disc',{{scale:.88,transformOrigin:'440px 250px'}},{{scale:1.1,duration:{s(3):.2f},ease:'sine.inOut'}},0);")
js("tl.fromTo('#h1a',{x:-20},{x:0,duration:.5,ease:'power2.out',immediateRender:false},0);")
js(f"tl.fromTo('#h1b',{{scale:1}},{{scale:1.04,duration:.2,ease:'sine.out',yoyo:true,repeat:1,transformOrigin:'0% 50%'}},{max(.1,t_hole):.3f});")
sfx("subhit.ogg", .05, -6); sfx("impactsoft.ogg", max(.1, t_hole), -6)
fin("#tg1", t_two, .35, 14, 6); sfx("tick.ogg", t_two + .05, -7)
fout("#s1", s(3) - .08, .3)
# S3 Fermat as code, 30 hours
js("gsap.set('#s3',{opacity:1}); gsap.set('#h3,#eq,#arw,#code3,#n3b,#tg3',{opacity:0});")
fin("#h3", s(3) + .02, .35, 24, 8); fin("#eq", s(3) + .25, .4, 36, 10, .96); sfx("whoosh_b.ogg", s(3) - .04, -9)
fin("#arw", t_code - .45, .3, -20, 6); fin("#code3", t_code - .25, .4, 36, 10, .96); sfx("pop_a.ogg", t_code - .2, -8)
fin("#n3b", t_thirty - .05, .4, 24, 8, .9); sfx("impactpunch.ogg", t_thirty, -6)
fin("#tg3", s(3) + 1.2, .35, 14, 6)
fout("#s3", s(4) - .08, .3)
# S4 three devices light up
js("gsap.set('#s4',{opacity:1}); gsap.set('#h4a,#h4b,#dv0,#dv1,#dv2,#tg4',{opacity:0});")
fin("#h4a", s(4) + .02, .35, 24, 8); fin("#h4b", s(4) + .25, .35, 24, 8)
for k in range(3):
    tt = t_three + .15 + k * .28
    fin(f"#dv{k}", tt, .35, 40, 8, .92); sfx("pop_a.ogg" if k % 2 == 0 else "pop_b.ogg", tt + .05, -8)
    js(f"tl.fromTo('#led{k}',{{scale:1,svgOrigin:'186 76'}},{{scale:1.9,duration:.22,ease:'sine.out',yoyo:true,repeat:5}},{tt+.4:.3f});")
fin("#tg4", t_scr - .1, .35, 14, 6)
fout("#s4", s(5) - .08, .3)
# S5 name
js("gsap.set('#s5',{opacity:1}); gsap.set('#mk5,#h5a,#h5b,#tg5',{opacity:0});")
fin("#mk5", s(5) + .02, .45, 30, 10, .9)
js(f"tl.to('#mk5',{{rotate:360,duration:{e(5)-s(5)+.2:.2f},ease:'sine.inOut'}},{s(5):.3f});")
fin("#h5a", s(5) + .15, .35, 24, 8); fin("#h5b", s(5) + .55, .4, 24, 8); sfx("impactsoft.ogg", s(5) + .6, -5)
fin("#tg5", s(5) + 1.1, .3, 14, 6)
fout("#s5", s(6) - .08, .3)
# S6 caveat
js("gsap.set('#s6',{opacity:1}); gsap.set('#r6a,#r6b',{opacity:0});")
fin("#r6a", s(6) + .05, .4, 36, 10, .96); sfx("tick.ogg", s(6) + .15, -7)
fin("#r6b", t_nob - .1, .4, 36, 10, .96); sfx("tick.ogg", t_nob, -7)
fout("#s6", s(7) - .08, .3)
# S7 question, then loop
js("gsap.set('#s7',{opacity:1}); gsap.set('#h7a,#h7b',{opacity:0});")
fin("#h7a", s(7) + .02, .35, 24, 8); fin("#h7b", s(7) + .3, .35, 24, 8); sfx("impactsoft.ogg", s(7) + .32, -6)
fout("#s7", e(7) + .5, .3)
js(f"tl.fromTo('#s1',{{opacity:0,filter:'blur(14px)'}},{{opacity:1,filter:'blur(0px)',duration:.4,ease:'power2.out',immediateRender:false}},{e(7)+.55:.3f});")
js(f"tl.set('#tg1',{{opacity:0}},{e(7)+.55:.3f});"); sfx("whoosh_c.ogg", e(7) + .5, -10)
JS = "\n".join(J)
json.dump(SFX, open(H_ + "/sfx96.json", "w"), indent=1)
json.dump(dict(lines=[dict(n=c["n"], text=c["line"], start=c["start"], end=c["end"]) for c in C], D=D), open(H_ + "/cues96.json", "w"), indent=1)
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
