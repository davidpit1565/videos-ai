#!/usr/bin/env python3
"""ep94 'Flagged as AI. Your own essay.' full reel, Miki style, script v3 (card early, facts, card again, loop).
Reads voice/narration-v5-raw-cues.json (line start/end) -> hf/index.html, sfx94.json, cues94.json. Word times inside a line are FRACTIONS of the line (refine with whisper words later)."""
import json, os, re
H_ = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(H_ + "/voice/narration-v5-raw-cues.json"))
C = C if isinstance(C, list) else C["lines"]
L = {c["n"]: (c["start"], c["end"]) for c in C}
s = lambda n: L[n][0]
e = lambda n: L[n][1]
wt = lambda n, f: round(L[n][0] + f * (L[n][1] - L[n][0]), 3)
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
    WORDS = json.load(open(H_ + "/voice/words-v5.json"))
except Exception:
    WORDS = []
def W(word, k=0, after=0.0, default=None):
    n = 0
    for w, a, b in WORDS:
        if a >= after and re.sub(r"[^a-z0-9]", "", w.lower()) == word:
            if n == k: return a
            n += 1
    return default
# ------------------------------------------------------------------ markup
ROWS = [("1", "VERSION HISTORY", "GOOGLE DOCS"), ("2", "YOUR NOTES", "AND DRAFTS"), ("3", "ASK THE TOOL", "HOW OFTEN IT IS WRONG")]
def letters(rid, i, text):
    return "".join(f'<span class="L" id="{rid}{i}L{j}">{"&nbsp;" if ch == " " else ch}</span>' for j, ch in enumerate(text))
def card(cid, rid):
    rows = "".join(f'<div class="row" id="{rid}{i}"><b class="num">{n}</b><div class="rt"><span class="r1">{letters(rid, i, a)}</span><span class="r2">{b}</span></div></div>' for i, (n, a, b) in enumerate(ROWS))
    return f'<div class="card" id="{cid}"><div class="ct" id="{cid}t">BRING PROOF</div>{rows}</div>'
sheets = "".join(f'<div class="mini" id="m{i}"><div class="mln" style="top:26px;width:70%"></div><div class="mln" style="top:62px;width:92%"></div><div class="mln" style="top:98px;width:60%"></div><div class="mst" id="ms{i}">AI</div></div>' for i in range(10))
markup = f'''
<div class="bgw" data-decor></div>
<div id="cam">
 <div id="s1">
  <div class="pg" id="pg"></div>
  <div class="who" id="who">TEACHER</div>
  <div class="bub" id="bub">I think <b>AI</b> wrote your <b>essay</b>.</div>
  <div class="exm" id="exm">EXAMPLE MESSAGE</div>
  <div class="yw" id="yw"><span id="yw1">YOU</span><span id="yw2">WROTE</span><span id="yw3">IT.</span></div>
  <div class="t3" id="t3">3 THINGS PROVE IT</div>
  <div class="bx" id="bx"><i id="bx1"></i><i id="bx2"></i><i id="bx3"></i></div>
 </div>
 {card("card", "q")}
 <div id="s4"><div class="why" id="why">HERE'S WHY</div><img class="tnlogo" id="tn" src="assets/turnitin.svg">
  <div class="big1" id="lt">LESS THAN</div><div class="big2" id="pc">1%</div><div class="tag" id="tg4" style="top:1110px;left:80px">THIS MISTAKE · ITS OWN CLAIM, 2023</div></div>
 <div id="s5"><div class="num5" id="n75">75,000</div><div class="num5 n750" id="n750">~750</div>
  <div class="win" id="win"><div class="wini" id="wini"><img src="assets/vanderbilt-para.png"/>
   <svg class="rings" viewBox="0 0 880 572"><rect id="rg1" x="-6" y="237" width="177" height="44" rx="10" pathLength="1" fill="none" stroke="{INK}" stroke-width="5" stroke-dasharray="1 1" stroke-dashoffset="1"/><rect id="rg2" x="58" y="277" width="320" height="44" rx="10" pathLength="1" fill="none" stroke="{INK}" stroke-width="5" stroke-dasharray="1 1" stroke-dashoffset="1"/></svg></div></div>
  <div class="tag" id="tg5" style="top:1155px;left:100px">VANDERBILT'S OWN ESTIMATE</div></div>
 <div id="s6"><div class="tgl" id="tgl"><span class="onl" id="onl">ON</span><span class="ofl" id="ofl">OFF</span><div class="knob" id="knob"></div></div><div class="tag" id="tg6" style="top:850px;left:100px">VANDERBILT · AUG 2023</div></div>
 <div id="s7"><div class="h7" id="h7">7 OTHER TOOLS</div><div class="grid7">{sheets}</div><div class="tag" id="tg7" style="top:1110px;left:100px">91 ESSAYS · TURNITIN NOT TESTED</div></div>
 {card("card2", "p")}
 <div class="tag" id="tgs" style="top:292px;left:100px;z-index:60">SAVE THIS</div>
</div>
'''
css = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;font-weight:500;color:{INK}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}}
.bgw{{position:absolute;left:0;top:0;width:1080px;height:1920px;background:#ecebe5 url(assets/bg.jpg);background-size:1080px 1920px}}
#cam{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}}
#s1,#s4,#s5,#s6,#s7{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
#s4,#s5,#s6,#s7,#card,#card2,#tgs{{opacity:0}}
.pg{{position:absolute;left:60px;top:285px;width:960px;height:960px;background:#fbfbf8 repeating-linear-gradient(0deg,transparent 0,transparent 63px,#dedcd4 63px,#dedcd4 66px);border:4px solid {INK};border-radius:6px;box-shadow:14px 14px 0 {INK}}}
.who{{position:absolute;left:90px;top:318px;height:56px;padding:0 24px;background:{INK};color:#fff;font:700 40px/56px JBM,monospace;letter-spacing:.06em;border-radius:6px}}
.bub{{position:absolute;left:90px;top:384px;width:900px;padding:22px 30px;background:#fff;border:5px solid {INK};border-radius:28px;font-size:66px;line-height:74px;font-weight:500;letter-spacing:-.02em;box-shadow:8px 8px 0 {INK}}}
.bub b{{font-weight:900}}
.exm{{position:absolute;left:96px;top:598px;font:700 30px/34px JBM,monospace;letter-spacing:.06em;color:#55565c}}
.yw{{position:absolute;left:90px;top:630px;font-size:180px;line-height:164px;font-weight:900;letter-spacing:-.05em}}
.yw span{{display:block;opacity:.14}}
.t3{{position:absolute;left:90px;top:1150px;height:60px;padding:0 24px;background:{INK};color:#fff;font:700 38px/60px JBM,monospace;letter-spacing:.05em;border-radius:6px;opacity:0}}
.bx{{position:absolute;left:560px;top:1152px;display:flex;gap:18px;opacity:0}} .bx i{{display:block;width:56px;height:56px;border:5px dashed {INK};border-radius:8px;background:#fbfbf8}}
.card{{position:absolute;left:100px;top:340px;width:880px;height:850px;background:#fbfbf8;border:4px solid {INK};border-radius:8px;box-shadow:14px 14px 0 {INK}}}
.ct{{position:absolute;left:50px;top:40px;font-size:128px;line-height:130px;font-weight:900;letter-spacing:-.045em;white-space:nowrap}}
.row{{position:absolute;left:50px;width:780px;height:170px;display:flex;align-items:center;gap:34px;opacity:0}}
.row:nth-of-type(2){{top:230px}} .row:nth-of-type(3){{top:430px}} .row:nth-of-type(4){{top:630px}}
.num{{flex:none;width:120px;height:120px;border-radius:14px;background:{INK};color:#fff;font-size:80px;line-height:120px;text-align:center;font-weight:900}}
.rt{{display:flex;flex-direction:column;gap:8px}} .r1{{font-size:66px;line-height:70px;font-weight:900;letter-spacing:-.03em;white-space:nowrap}} .r2{{font:700 34px/38px JBM,monospace;letter-spacing:.05em;color:#55565c;white-space:nowrap}}
.L{{display:inline-block;white-space:pre;opacity:0}}
.tag{{position:absolute;height:64px;padding:0 26px;background:{INK};color:#fff;font:700 34px/64px JBM,monospace;letter-spacing:.05em;border-radius:6px;white-space:nowrap;opacity:0}}
.why{{position:absolute;left:65px;top:300px;font-size:130px;line-height:130px;font-weight:900;letter-spacing:-.045em;opacity:0;white-space:nowrap}}
.tnlogo{{position:absolute;left:100px;top:310px;width:880px;opacity:0}}
.big1{{position:absolute;left:65px;top:560px;font-size:150px;line-height:150px;font-weight:900;letter-spacing:-.045em;opacity:0;white-space:nowrap}}
.big2{{position:absolute;left:85px;top:735px;font-size:380px;line-height:340px;font-weight:900;letter-spacing:-.06em;opacity:0}}
.num5{{position:absolute;left:88px;top:300px;font-size:240px;line-height:240px;font-weight:900;letter-spacing:-.05em;opacity:0;white-space:nowrap}}
.n750{{font-size:270px}}
.win{{position:absolute;left:100px;top:560px;width:880px;height:572px;background:#fff;border:4px solid {INK};border-radius:8px;box-shadow:14px 14px 0 {INK};overflow:hidden;opacity:0}}
.wini{{position:absolute;left:0;top:0;width:880px;height:572px;transform-origin:0 0}}
.win img{{position:absolute;left:0;top:0;width:880px;height:572px;display:block}}
.rings{{position:absolute;left:0;top:0;width:880px;height:572px;overflow:visible}}
.tgl{{position:absolute;left:140px;top:500px;width:800px;height:300px;border:10px solid {INK};border-radius:150px;background:#fbfbf8;box-shadow:14px 14px 0 {INK}}}
.knob{{position:absolute;left:520px;top:30px;width:230px;height:230px;border-radius:50%;background:{INK}}}
.onl,.ofl{{position:absolute;top:96px;font-size:110px;line-height:110px;font-weight:900;letter-spacing:-.03em}} .onl{{left:60px}} .ofl{{left:520px;opacity:0;color:#bbb}}
.h7{{position:absolute;left:85px;top:300px;font-size:104px;line-height:112px;font-weight:900;letter-spacing:-.045em;white-space:nowrap;opacity:0}}
.grid7{{position:absolute;left:111px;top:500px;width:860px;display:flex;flex-wrap:wrap;gap:56px 18px}}
.mini{{position:relative;width:152px;height:250px;background:#fbfbf8;border:4px solid {INK};border-radius:6px;box-shadow:6px 6px 0 {INK};opacity:0}}
.mln{{position:absolute;left:14px;height:14px;border-radius:7px;background:#d4d4d8}}
.mst{{position:absolute;left:8px;top:100px;width:130px;height:62px;border:7px solid {INK};border-radius:8px;font-size:44px;line-height:48px;font-weight:900;text-align:center;transform:rotate(-8deg);background:rgba(251,251,248,.9);opacity:0}}
'''

t_show1 = W("show", 0, default=1.0); t_show2 = W("show", 1, default=1.0); t_ask = W("ask", 0, default=1.0)
t_tn = W("turnitin", default=1.0) - .1
t_less = W("less", after=t_tn, default=1.0); t_one = W("one", after=t_less, default=1.0); t_hund = W("hundred", after=t_one, default=1.0) + .15
t_75 = W("75", after=s(5), default=1.0); t_750 = W("750", after=t_75, default=1.0); t_could = W("could", after=t_750, default=1.0)
t_mist = W("mistake", after=t_750, default=1.0); t_out = t_mist + .5
t_off = W("off", after=s(6), default=1.0) - .05
t_six = W("six", after=s(2), default=1.0) - .05
t_you = W("you", 0, default=2.4); t_wrote = W("wrote", 1, default=2.7); t_it = W("it", 0, after=t_wrote, default=3.0); t_three = W("three", 0, default=3.4); t_things = W("things", 0, after=t_three, default=3.7); t_prove = W("prove", 0, after=t_things, default=4.0)
# ------------------------------------------------------------------ timeline
js(f"tl.fromTo('#cam',{{scale:1.0,y:0}},{{scale:1.03,y:-12,duration:{D},ease:'sine.inOut'}},0);")
js("gsap.set('#s4,#s5,#s6,#s7',{opacity:1}); gsap.set('#tn,#why,#lt,#pc,#tg4,#n75,#n750,#win,#tg5,#tgl,#tg6,#h7,#tg7,.mini',{opacity:0});")
# S1: hook = teacher message over an essay page; words fill with the voice; tag + three empty boxes (open loop)
js("gsap.set('#exm,#t3,#bx',{opacity:0});")
js("tl.to('#bub',{x:-9,duration:.05,ease:'sine.inOut'},.25);tl.to('#bub',{x:8,duration:.07,ease:'sine.inOut'},.3);tl.to('#bub',{x:-5,duration:.07,ease:'sine.inOut'},.37);tl.to('#bub',{x:0,duration:.1,ease:'sine.out'},.44);")
sfx("impactsoft.ogg", .27, -6); sfx("pop_a.ogg", .32, -9)
fin("#exm", .9, .35, 10, 4)
for nm, tt in (("yw1", t_you), ("yw2", t_wrote), ("yw3", t_it)):
    js(f"tl.to('#{nm}',{{opacity:1,duration:.3,ease:'sine.out'}},{tt-.05:.3f});")
    sfx("impactsoft.ogg", tt + .02, -7)
fin("#t3", t_three, .35, 14, 6); fin("#bx", t_three + .1, .3, 10, 4)
for k, tt in enumerate((t_three + .15, t_things + .05, t_prove + .05)):
    js(f"tl.fromTo('#bx{k+1}',{{scale:1}},{{scale:1.25,duration:.18,ease:'sine.out',yoyo:true,repeat:1,transformOrigin:'50% 50%'}},{tt:.3f});")
    sfx("tick.ogg", tt, -8)
fout("#s1", s(2) - .08, .3)
# S2 (line 2): the surprising fact first: Stanford, 6 of 10 sheets called AI
fin("#h7", s(2) + .02, .35, 24, 8); fin("#tg7", s(2) + .4, .35, 16, 6)
for i in range(10):
    fin(f"#m{i}", s(2) + .35 + i * .05, .25, 20, 6)
for k, i in enumerate((0, 2, 3, 5, 7, 8)):
    ts = t_six + k * .13
    js(f"tl.fromTo('#ms{i}',{{opacity:0,scale:1.5}},{{opacity:1,scale:1,duration:.14,ease:'expo.out',immediateRender:false}},{ts:.3f});")
    sfx("tick.ogg" if k % 2 else "click_a.ogg", ts + .05, -8)
fout("#s7", s(3) - .1, .3)
# S3 (line 3): the card builds with the spoken items
js(f"gsap.set('#card',{{opacity:0}});")
fin("#card", s(3) - .02, .45, 40, 14, .96)
sfx("whoosh_b.ogg", s(3) - .05, -9); sfx("pop_a.ogg", s(3) + .35, -8)
for i, tr in enumerate((t_show1, t_show2, t_ask)):
    fin(f"#q{i}", tr - .05, .3, 24, 8)
    nl = len(ROWS[i][1]); span = 0.34 + 0.045 * nl
    for j in range(nl):
        tj = tr + .05 + j * (span / nl)
        js(f"tl.fromTo('#q{i}L{j}',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.09,ease:'power2.out',immediateRender:false}},{tj:.3f});")
        if ROWS[i][1][j] != " ": sfx("click_a.ogg" if j % 2 == 0 else "click_b.ogg", tj, -13)
fout("#card", s(4) - .1, .3)
# S4: Turnitin
fin("#why", s(4) + .02, .3, 20, 8); fout("#why", s(4) + .85, .28, 10, -10)
fin("#tn", t_tn, .4, 30, 10, .96); sfx("pop_a.ogg", t_tn + .08, -8)
fin("#lt", t_less, .3, 24, 8)
fin("#pc", t_one, .45, 30, 10, .92); sfx("impactsoft.ogg", t_one + .1, -4)
fin("#tg4", t_hund, .35, 16, 6); sfx("tick.ogg", t_hund + .05, -8)
fout("#s4", s(5) - .1, .3)
# S5: Vanderbilt real page
fin("#win", s(5) + .05, .5, 40, 12, .97); sfx("whoosh_a.ogg", s(5), -9)
k1 = 1.55; kx1, ky1 = 440 - k1 * 100, 262 - k1 * 259
js(f"tl.fromTo('#wini',{{scale:1,x:0,y:0}},{{scale:{k1},x:{kx1},y:{ky1},duration:.9,ease:'sine.inOut',immediateRender:false}},{(t_75-.2):.3f});")
k2 = 1.55; kx2, ky2 = 440 - k2 * 215, 262 - k2 * 299
js(f"tl.to('#wini',{{x:{kx2},y:{ky2},duration:.7,ease:'sine.inOut'}},{(t_750-.17):.3f});")
js(f"tl.to('#wini',{{scale:1,x:0,y:0,duration:.8,ease:'sine.inOut'}},{t_out:.3f});")
fin("#n75", t_75, .4, 30, 10); sfx("pop_b.ogg", t_75 + .06, -6)
js(f"tl.to('#rg1',{{strokeDashoffset:0,duration:.5,ease:'sine.inOut'}},{t_75:.3f});")
fout("#n75", (t_750-.12), .25, 10, -10)
fin("#n750", t_750, .45, 30, 10, .92); sfx("impactsoft.ogg", t_750 + .1, -4)
js(f"tl.to('#rg2',{{strokeDashoffset:0,duration:.5,ease:'sine.inOut'}},{t_750:.3f});")
fin("#tg5", t_could, .35, 16, 6); sfx("tick.ogg", t_could + .05, -8)
fout("#s5", s(6) - .1, .3)
# S6: switch ON -> OFF
fin("#tgl", s(6) + .02, .4, 30, 10, .95); fin("#tg6", (s(6)+.5), .35, 16, 6)
tf = t_off
js(f"tl.to('#knob',{{left:40,duration:.34,ease:'power3.inOut'}},{tf:.3f});tl.to('#onl',{{opacity:0,duration:.2}},{tf:.3f});tl.to('#ofl',{{opacity:1,color:'#0f0f0f',duration:.25}},{tf+.1:.3f});")
sfx("toggle.ogg", tf + .12, -4); sfx("impactsoft.ogg", tf + .3, -8)
fout("#s6", s(7) - .1, .3)
# S8: card returns with SAVE THIS
js("gsap.set('#card2 .row,#card2 .L',{opacity:1});")
fin("#card2", s(7) - .02, .45, 40, 14, .96); fin("#tgs", s(7) + .25, .3, 14, 6)
sfx("whoosh_b.ogg", s(7) - .05, -9); sfx("ding.ogg", s(7) + .45, -9)
js(f"tl.fromTo('#card2',{{y:0}},{{y:-14,duration:{s(8)-s(7)+.1:.3f},ease:'sine.inOut'}},{s(7)+.4:.3f});")
fout("#card2,#tgs", s(8) - .1, .3)
# S8: loop back to the hook frame while the question is asked
js(f"tl.fromTo('#s1',{{opacity:0,filter:'blur(14px)'}},{{opacity:1,filter:'blur(0px)',duration:.4,ease:'power2.out',immediateRender:false}},{s(8)-.02:.3f});")
sfx("whoosh_c.ogg", s(8) - .05, -10)
JS = "\n".join(J)
json.dump(SFX, open(H_ + "/sfx94.json", "w"), indent=1)
json.dump(dict(lines=[dict(n=c["n"], text=c["line"], start=c["start"], end=c["end"]) for c in C], D=D), open(H_ + "/cues94.json", "w"), indent=1)
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
