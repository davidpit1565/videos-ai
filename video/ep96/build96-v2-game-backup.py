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
markup = f'''
<div class="bgw" data-decor></div>
<div id="cam">
 <div id="s1">
  <div class="h1a" id="h1a">AI SOLVES</div><div class="h1b" id="h1b">BLACK HOLE MATH</div>
  <div class="card1" id="card1">{HOLE}</div>
  <div class="tag" id="tg1" style="top:1180px;left:100px">ANTHROPIC'S CLAIM · NOT CHECKED YET</div>
 </div>
 <div id="s2"><div class="h2" id="h2">ONE SENTENCE</div><div class="ui" id="ui"><div class="uih"><span class="chip dark" id="chip">Claude Fable 5.2</span></div><div class="typed" id="typed"></div></div></div>
 <div id="s3"><div class="n3" id="n3">75 SECONDS</div><div class="n3 n5" id="n5">CLAUDE FABLE 5.2</div><div class="gcard" id="gcard"><canvas id="gc" width="880" height="760"></canvas></div>
  <div class="tag" id="tg3" style="top:1184px;left:100px">THE REAL GAME · PLAYED BY ITS BOT</div></div>
 <div id="s5"><img class="mkbig" id="mk5" src="assets/claude-mark.svg"><div class="h5a" id="h5a">CLAUDE</div><div class="h5b" id="h5b">FABLE 5.2</div>
  <div class="tag" id="tg5" style="top:1090px;left:100px">NEW · PAID PLANS</div></div>
 <div id="s6"><div class="row6" id="r6a"><b class="yes">?</b><span>ANTHROPIC'S CLAIM</span></div><div class="row6" id="r6b"><b class="no">✕</b><span>NOT CHECKED YET</span></div></div>
 <div id="s7"><div class="h7a" id="h7a">WHAT</div><div class="h7b" id="h7b">NEXT?</div><div class="tag" id="tg7" style="top:760px;left:100px">COMMENT ONE SENTENCE</div></div>
</div>
'''
css = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;font-weight:500;color:{INK}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}}
.bgw{{position:absolute;left:0;top:0;width:1080px;height:1920px;background:#ecebe5 url(assets/bg.jpg);background-size:1080px 1920px}}
#cam{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}}
#s1,#s2,#s3,#s5,#s6,#s7{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
#s2,#s3,#s5,#s6,#s7{{opacity:0}}
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
.row6 span{{font-size:58px;line-height:62px;font-weight:900;letter-spacing:-.04em}}
.h7a{{position:absolute;left:88px;top:300px;font-size:230px;line-height:210px;font-weight:900;letter-spacing:-.055em;opacity:0}}
.h7b{{position:absolute;left:88px;top:510px;font-size:230px;line-height:210px;font-weight:900;letter-spacing:-.055em;opacity:0}}
'''
t_hole = W("black", 0, default=.6)
t_one = W("one", 0, after=s(2), default=s(2) + .8)
t_sev = s(4); t_play = W("playing", 0, after=s(4), default=s(4) + 1.4)
t_fable = W("fable", 0, after=s(5), default=s(5) + .9)
t_claim = W("claim", 0, after=s(6), default=s(6) + 1.6); t_nob = W("nobody", 0, after=s(6), default=s(6) + 2.2)
js(f"tl.fromTo('#cam',{{scale:1.0,y:0}},{{scale:1.03,y:-12,duration:{D},ease:'sine.inOut'}},0);")
# S1 hook: the black hole, already on screen at frame 0 and turning
js("gsap.set('#tg1',{opacity:0});")
js(f"tl.fromTo('#ring1',{{strokeDashoffset:0}},{{strokeDashoffset:-960,duration:{s(2)+1:.2f},ease:'none'}},0);")
js(f"tl.fromTo('#disc',{{scale:.9,transformOrigin:'440px 250px'}},{{scale:1.06,duration:{s(2):.2f},ease:'sine.inOut'}},0);")
js("tl.fromTo('#h1a',{x:-20},{x:0,duration:.5,ease:'power2.out',immediateRender:false},0);")
js(f"tl.fromTo('#h1b',{{scale:1}},{{scale:1.04,duration:.2,ease:'sine.out',yoyo:true,repeat:1,transformOrigin:'0% 50%'}},{max(.1,t_hole):.3f});")
sfx("subhit.ogg", .05, -6); sfx("impactsoft.ogg", max(.1, t_hole), -6)
fin("#tg1", .8, .35, 14, 6)
fout("#s1", s(2) - .08, .3)
# S2 one sentence typed
js("gsap.set('#s2',{opacity:1}); gsap.set('#h2,#ui',{opacity:0});")
fin("#h2", s(2) + .02, .35, 24, 8); fin("#ui", s(2) + .15, .45, 40, 12, .97); sfx("whoosh_b.ogg", s(2) - .04, -9)
js(f"(function(){{var el=document.getElementById('typed');el.innerHTML='';var sp=[];for(var i=0;i<{len(PROMPT)};i++){{var q=document.createElement('span');q.textContent={json.dumps(PROMPT)}[i];q.style.opacity=0;el.appendChild(q);sp.push(q);}}window.__sp=sp;}})();")
t0 = s(2) + .55; tn = max(1.6, (e(3) - t0) - .25)
js(f"tl.to(window.__sp,{{opacity:1,duration:.02,stagger:{tn/len(PROMPT):.4f}}},{t0:.3f});")
for k in range(0, 12, 2): sfx("click_a.ogg" if k % 4 == 0 else "click_b.ogg", t0 + k * tn / 12, -14)
fout("#s2", s(4) - .08, .3)
# S3 the real game, re-simulated per frame by its own bot
G0 = s(4) - .05; G1 = s(6) - .1
js("gsap.set('#s3',{opacity:1}); gsap.set('#n3,#n5,#gcard,#tg3',{opacity:0});")
js("window.__g=CatGame.make(document.getElementById('gc')); window.__g.simulateTo(1.5);")
js(f"(function(){{var o={{t:1.5}};tl.to(o,{{t:{1.5+(G1-G0):.3f},duration:{G1-G0:.3f},ease:'none',onUpdate:function(){{window.__g.simulateTo(o.t)}}}},{G0:.3f});}})();")
fin("#gcard", G0, .4, 40, 12, .97); fin("#n3", t_sev, .35, 24, 8); sfx("impactpunch.ogg", t_sev + .05, -6); sfx("whoosh_a.ogg", G0 - .03, -9)
fin("#tg3", t_play, .35, 14, 6)
fout('#n3', s(5) - .15, .25, 8, -10); fin('#n5', s(5) + .05, .35, 20, 8); sfx('pop_a.ogg', s(5) + .1, -8)
# line 5 over the game: name badge slides over, then S5 full
fout("#s3", G1, .3)
js("gsap.set('#s5',{opacity:0});")
# S5 name (short, inside line 5): shown as an overlay scene between game and caveat
# S6 caveat
js("gsap.set('#s6',{opacity:1}); gsap.set('#r6a,#r6b',{opacity:0});")
fin("#r6a", s(6) + .05, .4, 36, 10, .96); sfx("tick.ogg", s(6) + .15, -7)
fin("#r6b", t_nob - .1, .4, 36, 10, .96); sfx("tick.ogg", t_nob, -7)
fout("#s6", s(7) - .08, .3)
# S7 question, then loop to the hook frame
js("gsap.set('#s7',{opacity:1}); gsap.set('#h7a,#h7b,#tg7',{opacity:0});")
fin("#h7a", s(7) + .02, .35, 24, 8); fin("#h7b", s(7) + .3, .35, 24, 8); sfx("impactsoft.ogg", s(7) + .32, -6)
fin("#tg7", s(7) + .8, .35, 14, 6)
fout("#s7", e(7) + .5, .3)
js(f"tl.fromTo('#s1',{{opacity:0,filter:'blur(14px)'}},{{opacity:1,filter:'blur(0px)',duration:.4,ease:'power2.out',immediateRender:false}},{e(7)+.55:.3f});")
js(f"tl.set('#tg1',{{opacity:0}},{e(7)+.55:.3f});"); sfx("whoosh_c.ogg", e(7) + .5, -10)
JS = "\n".join(J)
json.dump(SFX, open(H_ + "/sfx96.json", "w"), indent=1)
json.dump(dict(lines=[dict(n=c["n"], text=c["line"], start=c["start"], end=c["end"]) for c in C], D=D), open(H_ + "/cues96.json", "w"), indent=1)
html = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script><script src="assets/game.js"></script>
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
