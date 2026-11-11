#!/usr/bin/env python3
"""ep94 'Flagged as AI. Your own essay.' full reel, Miki style, script v3 (card early, facts, card again, loop).
Reads voice/narration-v3-raw-cues.json (line start/end) -> hf/index.html, sfx94.json, cues94.json. Word times inside a line are FRACTIONS of the line (refine with whisper words later)."""
import json, os
H_ = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(H_ + "/voice/narration-v3-raw-cues.json"))
C = C if isinstance(C, list) else C["lines"]
L = {c["n"]: (c["start"], c["end"]) for c in C}
s = lambda n: L[n][0]
e = lambda n: L[n][1]
wt = lambda n, f: round(L[n][0] + f * (L[n][1] - L[n][0]), 3)
D = round(e(9) + 1.0, 2)
INK = "#0f0f0f"
J = []; SFX = []
def js(x): J.append(x)
def sfx(f, t, g=-6): SFX.append(dict(f=f, t=round(t, 3), g=g))
def fin(sel, t, d=.4, y=30, blur=14, sc=None):
    sc_ = f",scale:{sc}" if sc else ""
    js(f"tl.fromTo('{sel}',{{opacity:0,y:{y},filter:'blur({blur}px)'{sc_}}},{{opacity:1,y:0,scale:1,filter:'blur(0px)',duration:{d},ease:'power2.out',immediateRender:false}},{max(0,t):.3f});")
def fout(sel, t, d=.3, blur=14, y=-20):
    js(f"tl.to('{sel}',{{opacity:0,y:{y},filter:'blur({blur}px)',duration:{d},ease:'power1.in'}},{max(0,t):.3f});")

# ------------------------------------------------------------------ markup
ROWS = [("1", "VERSION HISTORY", "GOOGLE DOCS"), ("2", "YOUR DRAFTS", "AND NOTES"), ("3", "ASK THE TOOL", "WHICH ONE? ERROR RATE?")]
def card(cid, rid):
    rows = "".join(f'<div class="row" id="{rid}{i}"><b class="num">{n}</b><div class="rt"><span class="r1">{a}</span><span class="r2">{b}</span></div></div>' for i, (n, a, b) in enumerate(ROWS))
    return f'<div class="card" id="{cid}"><div class="ct" id="{cid}t">BRING PROOF</div>{rows}</div>'
sheets = "".join(f'<div class="mini" id="m{i}"><div class="mln" style="top:26px;width:70%"></div><div class="mln" style="top:62px;width:92%"></div><div class="mln" style="top:98px;width:60%"></div><div class="mst" id="ms{i}">AI</div></div>' for i in range(10))
markup = f'''
<div class="bgw" data-decor></div>
<div id="cam">
 <div id="s1">
  <div class="hd" id="hd"><span class="w" id="w1">YOUR</span><span class="w" id="w2">OWN</span><span class="br"></span><span class="w" id="w3">ESSAY</span>
   <svg class="ul" viewBox="0 0 620 40" preserveAspectRatio="none"><path id="ulp" d="M6 24 C 100 6, 200 34, 320 18 S 520 8, 614 20" pathLength="1" stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round" stroke-dasharray="1 1" stroke-dashoffset="1"/></svg></div>
  <div class="sheet" id="sheet"><div class="ln" style="top:50px;width:420px"></div><div class="ln" style="top:110px;width:700px"></div><div class="ln" style="top:170px;width:640px"></div><div class="ln" style="top:330px;width:690px"></div><div class="ln" style="top:390px;width:520px"></div></div>
  <div class="stamp" id="stamp"><i>AI DETECTOR</i><b>FLAGGED AS AI</b></div>
 </div>
 {card("card", "q")}
 <div id="s4"><div class="why" id="why">HERE'S WHY</div><img class="tnlogo" id="tn" src="assets/turnitin.svg">
  <div class="big1" id="lt">LESS THAN</div><div class="big2" id="pc">1%</div><div class="tag" id="tg4" style="top:1110px;left:80px">FALSE POSITIVES · ITS OWN CLAIM, 2023</div></div>
 <div id="s5"><div class="num5" id="n75">75,000</div><div class="num5 n750" id="n750">~750</div>
  <div class="win" id="win"><img src="assets/vanderbilt-para.png"/>
   <svg class="rings" viewBox="0 0 880 572"><rect id="rg1" x="-6" y="237" width="177" height="44" rx="10" pathLength="1" fill="none" stroke="{INK}" stroke-width="5" stroke-dasharray="1 1" stroke-dashoffset="1"/><rect id="rg2" x="58" y="277" width="320" height="44" rx="10" pathLength="1" fill="none" stroke="{INK}" stroke-width="5" stroke-dasharray="1 1" stroke-dashoffset="1"/></svg></div>
  <div class="tag" id="tg5" style="top:1155px;left:100px">VANDERBILT'S OWN ESTIMATE</div></div>
 <div id="s6"><div class="tgl" id="tgl"><span class="onl" id="onl">ON</span><span class="ofl" id="ofl">OFF</span><div class="knob" id="knob"></div></div><div class="tag" id="tg6" style="top:850px;left:100px">VANDERBILT · AUG 2023</div></div>
 <div id="s7"><div class="h7" id="h7">7 OTHER TOOLS</div><div class="grid7">{sheets}</div><div class="tag" id="tg7" style="top:1110px;left:100px">TURNITIN NOT TESTED</div></div>
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
.hd{{position:absolute;left:75px;top:335px;width:950px;font-size:176px;line-height:176px;font-weight:900;letter-spacing:-.045em;white-space:nowrap}}
.hd .w{{display:inline-block;margin-right:34px}} .hd .br{{display:block;height:0}}
.hd .ul{{position:absolute;left:0;top:326px;width:620px;height:40px}}
.sheet{{position:absolute;left:110px;top:760px;width:860px;height:470px;background:#fbfbf8;border:4px solid {INK};border-radius:6px;box-shadow:14px 14px 0 {INK}}}
.ln{{position:absolute;left:60px;height:30px;border-radius:15px;background:#d4d4d8;filter:blur(6px)}}
.stamp{{position:absolute;left:100px;top:890px;width:880px;height:230px;border:14px solid {INK};border-radius:14px;display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(-7deg);opacity:0}}
.stamp b{{font-size:106px;line-height:110px;margin-top:10px;font-weight:900;letter-spacing:-.04em;white-space:nowrap}}
.stamp i{{position:absolute;left:-14px;top:-104px;height:56px;padding:0 24px;background:{INK};color:#fff;font:700 34px/56px JBM,monospace;letter-spacing:.06em;font-style:normal;border-radius:6px}}
.card{{position:absolute;left:100px;top:340px;width:880px;height:850px;background:#fbfbf8;border:4px solid {INK};border-radius:8px;box-shadow:14px 14px 0 {INK}}}
.ct{{position:absolute;left:50px;top:40px;font-size:128px;line-height:130px;font-weight:900;letter-spacing:-.045em;white-space:nowrap}}
.row{{position:absolute;left:50px;width:780px;height:170px;display:flex;align-items:center;gap:34px;opacity:0}}
.row:nth-of-type(2){{top:230px}} .row:nth-of-type(3){{top:430px}} .row:nth-of-type(4){{top:630px}}
.num{{flex:none;width:120px;height:120px;border-radius:14px;background:{INK};color:#fff;font-size:80px;line-height:120px;text-align:center;font-weight:900}}
.rt{{display:flex;flex-direction:column;gap:8px}} .r1{{font-size:66px;line-height:70px;font-weight:900;letter-spacing:-.03em;white-space:nowrap}} .r2{{font:700 34px/38px JBM,monospace;letter-spacing:.05em;color:#55565c;white-space:nowrap}}
.tag{{position:absolute;height:64px;padding:0 26px;background:{INK};color:#fff;font:700 34px/64px JBM,monospace;letter-spacing:.05em;border-radius:6px;white-space:nowrap;opacity:0}}
.why{{position:absolute;left:65px;top:300px;font-size:130px;line-height:130px;font-weight:900;letter-spacing:-.045em;opacity:0;white-space:nowrap}}
.tnlogo{{position:absolute;left:100px;top:310px;width:880px;opacity:0}}
.big1{{position:absolute;left:65px;top:560px;font-size:150px;line-height:150px;font-weight:900;letter-spacing:-.045em;opacity:0;white-space:nowrap}}
.big2{{position:absolute;left:85px;top:735px;font-size:380px;line-height:340px;font-weight:900;letter-spacing:-.06em;opacity:0}}
.num5{{position:absolute;left:65px;top:300px;font-size:240px;line-height:240px;font-weight:900;letter-spacing:-.05em;opacity:0;white-space:nowrap}}
.n750{{font-size:270px}}
.win{{position:absolute;left:100px;top:560px;width:880px;height:572px;background:#fff;border:4px solid {INK};border-radius:8px;box-shadow:14px 14px 0 {INK};overflow:visible;opacity:0}}
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
# ------------------------------------------------------------------ timeline
js(f"tl.fromTo('#cam',{{scale:1.0,y:0}},{{scale:1.03,y:-12,duration:{D},ease:'sine.inOut'}},0);")
js("gsap.set('#s4,#s5,#s6,#s7',{opacity:1}); gsap.set('#tn,#why,#lt,#pc,#tg4,#n75,#n750,#win,#tg5,#tgl,#tg6,#h7,#tg7,.mini',{opacity:0});")
# S1: stamp lands at once (voice starts ~0.08)
t1 = s(1) + .02
js(f"tl.fromTo('#stamp',{{opacity:0,y:-520,scale:1.25}},{{opacity:1,y:0,scale:1,duration:.34,ease:'expo.out'}},{t1:.3f});")
js(f"tl.to('#sheet',{{x:-7,duration:.06,ease:'sine.out'}},{t1+.34:.3f});tl.to('#sheet',{{x:5,duration:.1,ease:'sine.inOut'}},{t1+.40:.3f});tl.to('#sheet',{{x:0,duration:.18,ease:'sine.out'}},{t1+.50:.3f});")
js("tl.to('#ulp',{strokeDashoffset:0,duration:.5,ease:'sine.inOut'},1.45);")
sfx("impactpunch.ogg", t1 + .1, -3); sfx("subhit.ogg", t1 + .14, -6)
fout("#s1", s(2) - .08, .3)
# S2: card builds with the spoken items
js(f"gsap.set('#card',{{opacity:0}});")
fin("#card", s(2) - .02, .45, 40, 14, .96)
sfx("whoosh_b.ogg", s(2) - .05, -9); sfx("pop_a.ogg", s(2) + .35, -8)
for i, tr in enumerate((5.66, 6.98, 8.0)):
    fin(f"#q{i}", tr, .35, 34, 10)
    sfx("pop_b.ogg", tr + .05, -8)
fout("#card", s(4) - .1, .3)
# S4: Turnitin
fin("#why", s(4) + .02, .3, 20, 8); fout("#why", s(4) + .85, .28, 10, -10)
fin("#tn", 10.6, .4, 30, 10, .96); sfx("pop_a.ogg", 10.6 + .08, -8)
fin("#lt", 11.5, .3, 24, 8)
fin("#pc", 12.05, .45, 30, 10, .92); sfx("impactsoft.ogg", 12.05 + .1, -4)
fin("#tg4", 13.3, .35, 16, 6); sfx("tick.ogg", 13.3 + .05, -8)
fout("#s4", s(5) - .1, .3)
# S5: Vanderbilt real page
fin("#win", s(5) + .05, .5, 40, 12, .97); sfx("whoosh_a.ogg", s(5), -9)
fin("#n75", 17.8, .4, 30, 10); sfx("pop_b.ogg", 17.8 + .06, -6)
js(f"tl.to('#rg1',{{strokeDashoffset:0,duration:.5,ease:'sine.inOut'}},17.8);")
fout("#n75", 19.6, .25, 10, -10)
fin("#n750", 19.72, .45, 30, 10, .92); sfx("impactsoft.ogg", 19.72 + .1, -4)
js(f"tl.to('#rg2',{{strokeDashoffset:0,duration:.5,ease:'sine.inOut'}},19.72);")
fin("#tg5", 20.9, .35, 16, 6); sfx("tick.ogg", 20.9 + .05, -8)
fout("#s5", s(6) - .1, .3)
# S6: switch ON -> OFF
fin("#tgl", s(6) + .02, .4, 30, 10, .95); fin("#tg6", 22.7, .35, 16, 6)
tf = 23.3
js(f"tl.to('#knob',{{left:40,duration:.34,ease:'power3.inOut'}},{tf:.3f});tl.to('#onl',{{opacity:0,duration:.2}},{tf:.3f});tl.to('#ofl',{{opacity:1,color:'#0f0f0f',duration:.25}},{tf+.1:.3f});")
sfx("toggle.ogg", tf + .12, -4); sfx("impactsoft.ogg", tf + .3, -8)
fout("#s6", s(7) - .1, .3)
# S7: Stanford
fin("#h7", s(7) + .02, .35, 24, 8); fin("#tg7", s(7) + .35, .35, 16, 6)
for i in range(10):
    fin(f"#m{i}", s(7) + .3 + i * .05, .25, 20, 6)
for k, i in enumerate((0, 2, 3, 5, 7, 8)):
    ts = 26.45 + k * .13
    js(f"tl.fromTo('#ms{i}',{{opacity:0,scale:1.5}},{{opacity:1,scale:1,duration:.14,ease:'expo.out',immediateRender:false}},{ts:.3f});")
    sfx("tick.ogg" if k % 2 else "click_a.ogg", ts + .05, -8)
fout("#s7", s(8) - .1, .3)
# S8: card returns with SAVE THIS
js("gsap.set('#card2 .row',{opacity:1});")
fin("#card2", s(8) - .02, .45, 40, 14, .96); fin("#tgs", s(8) + .25, .3, 14, 6)
sfx("whoosh_b.ogg", s(8) - .05, -9); sfx("ding.ogg", s(8) + .45, -9)
js(f"tl.fromTo('#card2',{{y:0}},{{y:-14,duration:{s(9)-s(8)+.1:.3f},ease:'sine.inOut'}},{s(8)+.4:.3f});")
fout("#card2,#tgs", s(9) - .1, .3)
# S9: loop back to the first frame (heading + sheet, stamp removed at the very end)
js(f"tl.fromTo('#s1',{{opacity:0,filter:'blur(14px)'}},{{opacity:1,filter:'blur(0px)',duration:.4,ease:'power2.out',immediateRender:false}},{s(9)-.02:.3f});")
js(f"tl.set('#stamp',{{opacity:1,y:0,scale:1}},{s(9)-.03:.3f});")
js(f"tl.to('#stamp',{{opacity:0,duration:.25,ease:'sine.in'}},{D-.45:.3f});")
sfx("whoosh_c.ogg", s(9) - .05, -10)
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
