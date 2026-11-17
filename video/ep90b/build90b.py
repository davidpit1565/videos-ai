#!/usr/bin/env python3
"""ep90b 'ChatGPT / 47-day timeout.' - the real ghost run redrawn in the ep89c style (light dotted grid + grain, heavy black Inter Display,
indigo user bubbles, big hero typography, ChatGPT green accent, soft scroll transitions, NO voice, NO music, sfx only).
Writes hf/index.html, sfx90b.json, cues90b.json."""
import json, os
H_ = os.path.dirname(os.path.abspath(__file__))
D = 20.2
INK, GRN, LIME, IND = "#0f0f0f", "#10A37F", "#B6F23A", "#20184E"
J = []; SFX = []
def js(s): J.append(s)
def sfx(f, t, g=-6): SFX.append((f, round(t, 3), g))
def T(t): return f"{max(0.0, t):.3f}"
EM = lambda c: f'<span class="em">{c}</span>'

def typed(prefix, text, hl=None):
    """letters as spans; hl = substring that gets the lime marker class (letters stay typed in order)"""
    out = []; k = 0; ids = []
    words = text.split(" ")
    for w in words:
        ls = ""
        for ch in w:
            ls += f'<span class="L" id="{prefix}{k}">{ch}</span>'; ids.append(f"{prefix}{k}"); k += 1
        out.append(f'<span class="tw">{ls}</span>')
    html = "".join(out)
    return html, ids

u1_html, u1_ids = typed("u", "Choose a number between 0 and 100")
u2a, u2a_ids = typed("v", "Now we won't be able to talk for")
u2b, u2b_ids = typed("w", "47 days")
u3_html, u3_ids = typed("f", "Fahhhhh")

badge = lambda i, cls="": f'<div class="badge {cls}" id="{i}"><img src="assets/chatgpt.svg"></div>'

markup = f'''
<div class="bgw" data-decor></div>
<div class="scene" id="sA">
 {badge("bdgA")}
 <div class="hk a1" id="a1">ChatGPT</div>
 <div class="hk a2" id="a2"><span class="mk" id="mkA">47-day</span> timeout.</div>
 <div class="hk beg" id="begA"><span class="bl">Wait... can I</span><span class="bl">have a second</span><span class="bl">chance? {EM("😔")}</span></div>
 <svg class="ulA" id="ulA" viewBox="0 0 560 40" preserveAspectRatio="none"><path d="M6 24 C 90 6, 170 34, 270 18 S 450 8, 554 20" stroke="{GRN}" stroke-width="10" fill="none" stroke-linecap="round"/></svg>
</div>

<div class="scene" id="sB1">
 <div class="ub" id="ub1" style="top:300px;left:215px;width:800px"><div class="ut">{u1_html}</div></div>
 {badge("bdgB1", "sm")}
 <div class="dots" id="dB1"><b></b><b></b><b></b></div>
 <div class="pill big47" id="p47"><span id="n47">47</span></div>
</div>

<div class="scene" id="sB2">
 <div class="ub" id="ub2" style="top:290px;left:150px;width:865px"><div class="ut">{u2a} <span class="hl" id="hl47">{u2b}</span></div></div>
 {badge("bdgB2", "sm")}
 <div class="dots" id="dB2"><b></b><b></b><b></b></div>
 <div class="hk beg2" id="beg2"><span class="bl" id="b2l0">Wait... can I</span><span class="bl" id="b2l1">have a second</span><span class="bl" id="b2l2">chance? {EM("😔")}</span></div>
</div>

<div class="scene" id="sC">
 <div class="ub" id="ubY" style="top:300px;right:65px;left:auto;width:auto"><div class="ut yes">Yes</div></div>
 {badge("bdgC", "sm")}
 <div class="dots" id="dC"><b></b><b></b><b></b></div>
 <div class="pill big100" id="p100"><span id="n100">100</span></div>
 <div class="heart" id="heart">{EM("🧡")}</div>
</div>

<div class="scene" id="sD">
 <div class="ub" id="ub3" style="top:420px;right:65px;left:auto;width:auto"><div class="ut fah">{u3_html}</div></div>
 {badge("bdgD", "sm")}
 <div class="dots big" id="dD"><b></b><b></b><b></b></div>
</div>

<div class="scene" id="sE">
 {badge("bdgE", "sm")}
 <div class="haha" id="haha">{"".join(f'<span class="hl_" id="ha{i}">{c}</span>' for i, c in enumerate("HAHAHAHA"))}</div>
 <div class="lol" id="lol">{EM("😆")}</div>
 <div class="hk e2" id="e2">You gave me a second chance</div>
 <div class="hk e3" id="e3">and I <b class="still">STILL</b></div>
 <div class="hk e4" id="e4"><span class="ch">chose</span> <span class="n100" id="e100">100</span> <span class="skull" id="skull">{EM("💀")}</span></div>
 <svg class="ringE" id="ringE" viewBox="0 0 560 300" preserveAspectRatio="none"><path d="M40 160 C 20 50, 200 8, 300 12 C 470 18, 545 70, 530 160 C 515 255, 360 292, 270 288 C 120 284, 28 250, 34 150 C 38 80, 90 44, 150 30" stroke="{GRN}" stroke-width="11" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
</div>
'''

css = f'''
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Black.otf");font-weight:900}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-ExtraBold.otf");font-weight:800}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Medium.otf");font-weight:500}}
.bgw{{position:absolute;left:0;top:0;width:1080px;height:2000px;background:#ecebe5 url(assets/bg.jpg) repeat-y;background-size:1080px 1920px}}
.scene{{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0}} #sA{{opacity:1}}
.hk{{position:absolute;left:65px;width:950px;color:{INK};white-space:nowrap;font-weight:900;letter-spacing:-.045em}}
.em{{font-family:"Noto Color Emoji";font-weight:400;letter-spacing:0;display:inline-block}}
.badge{{position:absolute;left:65px;top:295px;width:128px;height:128px;border-radius:30px;background:#fff;border:4px solid {INK};display:flex;align-items:center;justify-content:center;box-shadow:7px 7px 0 {INK}}}
.badge img{{width:66%;height:66%}} .badge.sm{{width:104px;height:104px;border-radius:26px;box-shadow:6px 6px 0 {INK}}}
.a1{{top:430px;font-size:184px;line-height:190px}}
.a2{{top:624px;font-size:98px;line-height:116px}}
.mk{{position:relative;isolation:isolate;display:inline-block}}
.mk::before{{content:"";position:absolute;left:-14px;right:-10px;top:8px;bottom:-4px;background:{LIME};transform-origin:0 50%;transform:scaleX(var(--m,1));z-index:-1}}
.beg{{top:785px;font-size:122px;line-height:132px;font-weight:800;letter-spacing:-.035em}}
.bl{{display:block}}
.ulA{{position:absolute;left:70px;top:1168px;width:640px;height:40px}}
.ub{{position:absolute;background:{IND};border-radius:48px 48px 14px 48px;padding:34px 46px;color:#fff;font-weight:500;opacity:0}}
.ut{{font-size:64px;line-height:78px;letter-spacing:-.015em}}
.ut.yes{{font-size:96px;line-height:110px;font-weight:800}} .ut.fah{{font-size:132px;line-height:150px;font-weight:800}}
.tw{{display:inline-block;white-space:nowrap;margin-right:.26em}} .L{{opacity:0;display:inline-block}}
.hl{{display:inline-block;background:rgba(182,242,58,0);color:#fff;border-radius:12px;padding:0 14px;margin:0 -6px}}
.dots{{position:absolute;left:215px;top:780px;display:flex;gap:22px;opacity:0}} .dots b{{display:block;width:46px;height:46px;border-radius:50%;background:{INK}}}
.dots.big{{top:700px}} .dots.big b{{width:80px;height:80px}}
#bdgB1{{top:560px}} #bdgB2{{top:660px}} #bdgC{{top:540px}} #bdgD{{top:580px}}
#dB1,#dC{{left:215px;top:700px}} #dB2{{left:215px;top:700px}} #dD{{left:215px;top:620px}} #dB1,#dB2,#dC{{top:690px}}
.pill{{position:absolute;left:150px;background:{LIME};border:8px solid {INK};border-radius:64px;box-shadow:16px 16px 0 {INK};text-align:center;font-weight:900;letter-spacing:-.06em;color:{INK};opacity:0}}
.big47{{top:690px;width:780px;height:500px;font-size:480px;line-height:500px}} .big100{{top:700px;width:800px;height:480px;font-size:420px;line-height:480px;left:110px}}
.heart{{position:absolute;left:735px;top:470px;font-size:170px;line-height:170px;opacity:0}}
.beg2{{top:830px;font-size:122px;line-height:132px;font-weight:800;letter-spacing:-.035em}} .beg2 .bl{{opacity:0}}
.haha{{position:absolute;left:65px;top:470px;font-size:150px;line-height:170px;font-weight:900;letter-spacing:-.04em;color:{INK};white-space:nowrap}} .hl_{{display:inline-block;opacity:0}}
.lol{{position:absolute;left:800px;top:285px;font-size:150px;line-height:150px;opacity:0;font-family:"Noto Color Emoji"}}
.e2{{top:672px;font-size:66px;line-height:78px;font-weight:500;letter-spacing:-.02em;opacity:0}}
.e3{{top:762px;font-size:150px;line-height:160px;opacity:0}} .e3 .still{{font-weight:900}}
.e4{{top:925px;font-size:96px;line-height:260px;opacity:0;display:flex;align-items:baseline;gap:26px}}
.e4 .ch{{font-weight:500;letter-spacing:-.02em}} .n100{{font-size:250px;font-weight:900;letter-spacing:-.06em;color:{GRN};line-height:260px}} .skull{{font-size:130px}}
.ringE{{position:absolute;left:280px;top:925px;width:520px;height:280px;opacity:0}}
'''

# ------------------------------------------------------------ timeline
def fadeup(sel, t, d=.3, dy=40, ease='power2.out'):
    js(f"tl.fromTo('{sel}',{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{d},ease:'{ease}',immediateRender:false}},{T(t)});")
def type_in(ids, t0, dur, clickg=-17):
    n = len(ids)
    for k, i in enumerate(ids):
        t = t0 + dur * k / n
        js(f"tl.fromTo('#{i}',{{opacity:0,y:8,scale:.85}},{{opacity:1,y:0,scale:1,duration:.09,ease:'power2.out',immediateRender:false}},{T(t)});")
        if k % 2 == 0: sfx("click_a.ogg" if (k // 2) % 2 == 0 else "click_b.ogg", t, clickg)
def scroll(out_sels, in_sel, t, d=.28):
    js(f"tl.fromTo('{in_sel}',{{opacity:1,y:560,filter:'blur(8px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:{d},ease:'power2.inOut',immediateRender:false}},{T(t)});")
    js(f"tl.to('{out_sels}',{{y:-1250,filter:'blur(10px)',duration:{d},ease:'power2.in'}},{T(t)});")
    js(f"tl.to('{out_sels}',{{opacity:0,duration:{d * .4:.3f},ease:'power3.out'}},{T(t)});")
    sfx("whoosh_c.ogg", t - .02, -12)
def bubble(sel, t, d=.32):
    js(f"tl.fromTo('{sel}',{{opacity:0,scale:.9,y:24}},{{opacity:1,scale:1,y:0,duration:{d},ease:'power3.out',transformOrigin:'100% 100%',immediateRender:false}},{T(t)});")
def dots(sel, t0, t1):
    js(f"tl.fromTo('{sel}',{{opacity:0}},{{opacity:1,duration:.2,ease:'sine.out',immediateRender:false}},{T(t0)});")
    js(f"tl.fromTo('{sel} b',{{y:0,opacity:.35}},{{y:-12,opacity:1,duration:.24,ease:'sine.inOut',yoyo:true,repeat:{int((t1 - t0) / .24)},stagger:.12,immediateRender:false}},{T(t0)});")
    js(f"tl.to('{sel}',{{opacity:0,duration:.15}},{T(t1)});")

# --- frame 0 = the hook: all text visible, nothing covers anything
js("tl.fromTo('.bgw',{y:0},{y:-70,duration:%.2f,ease:'sine.inOut',yoyo:true,repeat:1},0);" % (D / 2))
js("tl.fromTo('#bdgA',{rotation:-14,scale:.86,y:10},{rotation:-3,scale:1,y:0,duration:.45,ease:'power3.out'},0);")
js("tl.to('#bdgA',{rotation:3,duration:3,ease:'sine.inOut'},.45);")
js("tl.fromTo('#mkA',{'--m':1},{'--m':1,duration:.01},0);")
js("tl.fromTo('#begA',{y:14},{y:-10,duration:3.6,ease:'sine.inOut'},0);")
js("tl.fromTo('#begA .em',{rotation:-8},{rotation:8,duration:.5,ease:'sine.inOut',yoyo:true,repeat:6,transformOrigin:'50% 60%'},0);")
js("tl.fromTo('#ulA',{opacity:0},{opacity:1,duration:.5,ease:'sine.inOut'},0.9);")
js("tl.fromTo('#sA',{scale:1},{scale:1.01,duration:3.6,ease:'sine.inOut',transformOrigin:'50% 40%'},0);")
sfx("impactsoft.ogg", 0.04, -9); sfx("ding.ogg", 0.32, -9); sfx("pop_a.ogg", 0.62, -12); sfx("tick.ogg", 1.0, -14)

# --- A -> B1
tB1 = 3.4
scroll("#sA", "#sB1", tB1)
js("tl.set('#sA',{opacity:0},%s);" % T(tB1 + .3))
bubble("#ub1", tB1 + .35); sfx("pop_b.ogg", tB1 + .38, -10)
type_in(u1_ids, tB1 + .5, .7)
dots("#dB1", tB1 + 1.3, tB1 + 1.65)
js(f"tl.fromTo('#bdgB1',{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.3,ease:'power3.out',immediateRender:false}},{T(tB1 + 1.25)});")
t47 = tB1 + 1.7
js(f"tl.fromTo('#p47',{{opacity:0,scale:.82,rotation:-4}},{{opacity:1,scale:1,rotation:-2,duration:.42,ease:'expo.out',transformOrigin:'50% 55%',immediateRender:false}},{T(t47)});")
js(f"tl.fromTo('#p47',{{y:0}},{{y:-14,duration:1.0,ease:'sine.inOut'}},{T(t47 + .3)});")
sfx("pop_a.ogg", t47, -6); sfx("impactsoft.ogg", t47 + .05, -12)

# --- B1 -> B2
tB2 = t47 + .9
scroll("#sB1", "#sB2", tB2)
js("tl.set('#sB1',{opacity:0},%s);" % T(tB2 + .3))
bubble("#ub2", tB2 + .35); sfx("pop_b.ogg", tB2 + .38, -10)
type_in(u2a_ids, tB2 + .5, .7)
type_in(u2b_ids, tB2 + 1.25, .3)
js(f"tl.to('#hl47',{{backgroundColor:'{LIME}',color:'{INK}',duration:.3,ease:'power2.inOut'}},{T(tB2 + 1.6)});")
sfx("select.ogg", tB2 + 1.62, -10)
dots("#dB2", tB2 + 1.75, tB2 + 2.15)
js(f"tl.fromTo('#bdgB2',{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.3,ease:'power3.out',immediateRender:false}},{T(tB2 + 1.7)});")
tBeg = tB2 + 2.2
for i in range(3): fadeup(f"#b2l{i}", tBeg + i * .16, .32, 36)
js(f"tl.fromTo('#beg2 .em',{{rotation:-10,scale:.7}},{{rotation:6,scale:1,duration:.5,ease:'back.out(1.4)',transformOrigin:'50% 60%',immediateRender:false}},{T(tBeg + .5)});")
js(f"tl.fromTo('#beg2',{{y:12}},{{y:-8,duration:2.2,ease:'sine.inOut'}},{T(tBeg)});")
sfx("ding.ogg", tBeg, -8); sfx("pop_a.ogg", tBeg + .5, -11)

# --- B2 -> C  (begging line holds >= 2 s)
tC = tBeg + 2.2
scroll("#sB2", "#sC", tC)
js("tl.set('#sB2',{opacity:0},%s);" % T(tC + .3))
bubble("#ubY", tC + .35); sfx("pop_b.ogg", tC + .38, -8); sfx("click_a.ogg", tC + .4, -12)
dots("#dC", tC + .85, tC + 1.2)
js(f"tl.fromTo('#bdgC',{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.3,ease:'power3.out',immediateRender:false}},{T(tC + .8)});")
t100 = tC + 1.25
js(f"tl.fromTo('#p100',{{opacity:0,scale:.82,rotation:3}},{{opacity:1,scale:1,rotation:2,duration:.42,ease:'expo.out',transformOrigin:'50% 55%',immediateRender:false}},{T(t100)});")
js(f"tl.fromTo('#heart',{{opacity:0,scale:.4,rotation:-20}},{{opacity:1,scale:1,rotation:12,duration:.55,ease:'back.out(1.5)',transformOrigin:'50% 60%',immediateRender:false}},{T(t100 + .25)});")
js(f"tl.to('#heart',{{y:-16,duration:.9,ease:'sine.inOut',yoyo:true,repeat:1}},{T(t100 + .8)});")
sfx("pop_a.ogg", t100, -6); sfx("ding.ogg", t100 + .3, -10)

# --- C -> D (tension: near silence before the punchline)
tD = t100 + 1.3
scroll("#sC", "#sD", tD)
js("tl.set('#sC',{opacity:0},%s);" % T(tD + .3))
bubble("#ub3", tD + .35); sfx("pop_b.ogg", tD + .38, -10)
type_in(u3_ids, tD + .5, .5, -15)
tdots = tD + 1.1
js(f"tl.fromTo('#bdgD',{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.3,ease:'power3.out',immediateRender:false}},{T(tdots - .05)});")
dots("#dD", tdots, tdots + .95)
# --- D -> E: the punchline
tE = tdots + 1.0
scroll("#sD", "#sE", tE, .26)
js("tl.set('#sD',{opacity:0},%s);" % T(tE + .3))
js(f"tl.fromTo('#bdgE',{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.3,ease:'power3.out',immediateRender:false}},{T(tE + .2)});")
for i in range(8):
    js(f"tl.fromTo('#ha{i}',{{opacity:0,y:60,scale:.8}},{{opacity:1,y:0,scale:1,duration:.26,ease:'power3.out',immediateRender:false}},{T(tE + .3 + i * .055)});")
    if i % 2 == 0: sfx("pop_a.ogg", tE + .3 + i * .055, -11)
js(f"tl.fromTo('#lol',{{opacity:0,scale:.3,rotation:-30}},{{opacity:1,scale:1,rotation:10,duration:.5,ease:'back.out(1.6)',transformOrigin:'50% 60%',immediateRender:false}},{T(tE + .35)});")
js(f"tl.to('#lol',{{rotation:-8,duration:.35,ease:'sine.inOut',yoyo:true,repeat:5}},{T(tE + .9)});")
sfx("impactsoft.ogg", tE + .3, -3); sfx("subhit.ogg", tE + .32, -10)
fadeup("#e2", tE + 1.15, .4, 30); fadeup("#e3", tE + 1.55, .4, 40)
fadeup("#e4", tE + 1.95, .4, 40)
js(f"tl.fromTo('#e100',{{scale:.82}},{{scale:1,duration:.4,ease:'expo.out',transformOrigin:'50% 70%',immediateRender:false}},{T(tE + 1.95)});")
js(f"tl.fromTo('#skull',{{rotation:-25,scale:.5}},{{rotation:6,scale:1,duration:.5,ease:'back.out(1.5)',transformOrigin:'50% 60%',immediateRender:false}},{T(tE + 2.2)});")
RA = .6; tR = tE + 1.9
js(f"tl.fromTo('#ringE',{{opacity:0,scale:.96}},{{opacity:1,scale:1,duration:{RA},ease:'sine.inOut',transformOrigin:'50% 50%',immediateRender:false}},{T(tR - .1)});")
js(f"tl.fromTo('#ringE',{{rotation:-.5,y:0}},{{rotation:.6,y:-5,duration:2.5,ease:'sine.inOut',immediateRender:false}},{T(tR - .1)});")
js(f"tl.fromTo('#sE',{{y:0}},{{y:-10,duration:3.2,ease:'sine.inOut'}},{T(tE + .4)});")
sfx("pop_b.ogg", tE + 1.2, -12); sfx("pop_a.ogg", tE + 1.97, -9); sfx("pop_b.ogg", tE + 2.25, -9); sfx("ding.ogg", tR + .35, -14)

# --- loop: punchline holds >= 2 s clean, soft dissolve back to frame 0
tL = tR + 2.3
js(f"tl.to('#sE',{{opacity:0,filter:'blur(14px)',duration:.4,ease:'power1.in'}},{T(tL)});")
js(f"tl.set('#sA',{{opacity:0,y:0,scale:1}},{T(tL - .02)});")
js(f"tl.set('#bdgA',{{rotation:-14,scale:.86,y:10}},{T(tL - .02)});")
js(f"tl.set('#begA',{{y:14}},{T(tL - .02)});")
js(f"tl.set('#ulA',{{opacity:0}},{T(tL - .02)});")
js(f"tl.fromTo('#sA',{{opacity:0,filter:'blur(14px)'}},{{opacity:1,filter:'blur(0px)',duration:.5,ease:'power2.out',immediateRender:false}},{T(tL + .35)});")
sfx("whoosh_b.ogg", tL + .1, -14); sfx("pop_a.ogg", tL + .45, -14)
assert tL + .85 <= D + .01, (tL, D)
print("tL", round(tL, 2), "tE", round(tE, 2), "D", D)

JS = "\n".join(J)
json.dump([dict(f=f, t=t, g=g) for f, t, g in SFX if 0 <= t < D], open(H_ + "/sfx90b.json", "w"), indent=1)
json.dump(dict(lines=[dict(n=1, text="(no voice-over)", start=0, end=D)], D=D), open(H_ + "/cues90b.json", "w"))
html = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;font-weight:500;color:{INK}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}}
{css}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
{markup}
</div>
<script>
const D={D};
const tl=gsap.timeline({{paused:true}});
{JS}
tl.to({{}},{{duration:.001}},D-.001);
window.__timelines=window.__timelines||{{}}; window.__timelines["main"]=tl; tl.seek(0);
window.__reel={{duration:D,seek:t=>tl.seek(t)}};
</script></body></html>'''
open(H_ + "/hf/index.html", "w").write(html)
print("sfx", len(SFX), "js", len(J))
