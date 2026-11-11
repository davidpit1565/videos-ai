#!/usr/bin/env python3
"""ep90b FINAL2 - the real ghost run in the ep89c Miki language: light dotted grid + grain, heavy black type built word by word, dark prompt
cards with black tags + dashed curves holding the typed user message, black selection bars, orange only for '100' (ring + digits), hand-drawn
underline, soft scrolls, NO black wipes. No voice. Music bed + sfx are mixed by mix90b2.py (ducking times in duck90b.json)."""
import json, os
H_ = os.path.dirname(os.path.abspath(__file__))
D = 20.9
INK, ORG = "#0f0f0f", "#0f0f0f"   # no orange in this version
J = []; SFX = []
def js(s): J.append(s)
def sfx(f, t, g=-6): SFX.append((f, round(t, 3), g))
def T(t): return f"{max(0.0, t):.3f}"
EM = lambda c: f'<span class="em">{c}</span>'

def typed(prefix, text, ku=()):
    out = []; ids = []; k = 0
    for wi, w in enumerate(text.split(" ")):
        ls = ""
        for j, ch in enumerate(w):
            ls += f'<span class="L" id="{prefix}{k + j}">{ch}</span>'; ids.append(f"{prefix}{k + j}")
        out.append(f'<span class="tw{" ku" if wi in ku else ""}" id="{prefix}w{wi}">{ls}</span>'); k += len(w)
    return "".join(out), ids

def comp(cid, prefix, text, top, h, ku=()):
    html, ids = typed(prefix, text, ku)
    plus = '<svg viewBox="0 0 40 40" width="52" height="52"><path d="M20 8v24M8 20h24" stroke="#d8d8dc" stroke-width="4.5" stroke-linecap="round"/></svg>'
    arrow = '<svg viewBox="0 0 40 40" width="46" height="46"><path d="M20 31V10M11 18l9-9 9 9" fill="none" stroke="#111" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return (f'<div class="comp" id="{cid}" style="top:{top}px;height:{h}px">'
            f'<div class="txt" id="{cid}t">{html}</div><div class="cbt"><div class="plus">{plus}</div><div class="send" id="{cid}s">{arrow}</div></div></div>'), ids

curve = lambda i, d: (f'<svg class="curve" id="cv{i}" viewBox="0 0 1080 1920"><mask id="m{i}"><path id="mp{i}" d="{d}" pathLength="1" stroke="#fff" stroke-width="16" fill="none" stroke-dasharray="1 1" stroke-dashoffset="1"/></mask>'
                      f'<path d="{d}" stroke="{INK}" stroke-width="5" fill="none" stroke-dasharray="4 16" stroke-linecap="round" mask="url(#m{i})"/></svg>')
CV = "M 372 340 C 470 296 600 318 650 404"
tag = lambda i, t: f'<div class="tag" id="tag{i}">{t}</div>'
atag = lambda i, top, vis=0: f'<div class="tag at" id="tagn{i}" style="top:{top}px;opacity:{vis}">CHATGPT</div>'
badge = '<div class="badge" id="bdg"><img src="assets/chatgpt.svg"></div>'

c1, ids1 = comp("c1", "p", "Choose a number between 0 and 100", 400, 400)
c2, ids2 = comp("c2", "q", "Now we won't be able to talk for 47 days", 400, 400, (8, 9))
c3, ids3 = comp("c3", "r", "Yes", 400, 290)
c4, ids4 = comp("c4", "s", "Fahhhhh", 400, 290)

beg_words = ["Wait...", "can", "I", "have", "a", "second", "chance?"]
rep_text = "".join(f'<span class="w g" id="g{i}">{w}</span>' for i, w in enumerate(beg_words)) + f'<span class="w g" id="g7">{EM("😔")}</span>'
rep = f'<div class="rep" id="rep0" style="top:895px;height:330px"><div class="rtxt">{rep_text}</div></div>'

hero2 = "".join(f'<span class="w" id="h{i}">{w}</span>' for i, w in enumerate(["Wait...", "can", "I"]))
markup = f'''
<div class="bgw" data-decor></div>
<div class="scene" id="sA">{badge}
 <div class="hk a1" id="a1"><span class="v" id="aC">ChatGPT</span></div>
 <div class="hk a2" id="a2"><span class="sel" id="selA"><span class="w0" id="a47">47-day</span></span> <span class="w gh" id="aT">timeout.</span></div>
 {atag(0, 795, 1)}
 {rep}
</div>
{tag(1, "ME")}{curve(1, CV)}{c1}
<div class="scene" id="sB1">{atag(1, 835)}<div class="ans47" id="a47b"><span class="sel big" id="sel47"><span id="t47">47</span></span></div>
</div>
{tag(2, "ME")}{curve(2, CV)}{c2}
<div class="scene" id="sB2">{atag(2, 835)}<div class="hk h2a" id="hb0"><span class="w" id="hb00">Wait...</span><span class="w" id="hb01">can</span><span class="w" id="hb02">I</span><span class="w" id="hb03">have</span></div>
 <div class="hk h2b" id="hb1"><span class="w" id="hb10">a</span><span class="w" id="hb11">second</span></div>
 <div class="hk h2c" id="hb2"><span class="sel" id="selB"><span class="w" id="hb20">chance?</span></span><span class="w" id="hb21">{EM("😔")}</span></div>
</div>
{tag(3, "ME")}{curve(3, CV)}{c3}
<div class="scene" id="sC">{atag(3, 735)}<div class="hk h100" id="h100"><span class="w" id="n100">100</span></div><div class="heart" id="heart">{EM("🧡")}</div>
</div>
{tag(4, "ME")}{curve(4, CV)}{c4}
{atag(4, 735)}<div class="rep dotsc" id="rep4" style="top:830px;height:400px"><div class="bigdots" id="bd"><b></b><b></b><b></b></div></div>
<div class="scene" id="sE">
 {atag(5, 296)}
 <div class="hk e1" id="e1">{"".join(f'<span class="hl_" id="ha{i}">{c}</span>' for i, c in enumerate("HAHAHAHA"))}</div>
 <div class="lol" id="lol">{EM("😆")}</div>
 <div class="hk e2" id="e2"><span class="w l2" id="e20">You</span> <span class="w l2" id="e21">gave</span> <span class="w l2" id="e22">me</span> <span class="w l2" id="e23">a</span> <span class="w l2" id="e24">second</span> <span class="w l2" id="e25">chance</span></div>
 <div class="hk e3" id="e3"><span class="w" id="e30">and</span> <span class="w" id="e31">I</span> <span class="sel" id="selE"><span class="w" id="e32">STILL</span></span></div>
 <div class="hk e4" id="e4"><span class="w l2b" id="e40">chose</span> <span class="w n100" id="e41">100</span> <span class="w" id="e42">{EM("💀")}</span></div>
 <svg class="ringE" id="ringE" viewBox="0 0 520 280" preserveAspectRatio="none"><path d="M40 150 C 20 50, 190 8, 290 12 C 450 18, 505 70, 490 150 C 475 245, 340 272, 255 268 C 115 264, 28 235, 34 140 C 38 75, 85 42, 145 30" stroke="{ORG}" stroke-width="11" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
</div>
'''

css = f'''
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Black.otf");font-weight:900}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-ExtraBold.otf");font-weight:800}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Medium.otf");font-weight:500}}
@font-face{{font-family:"JBM";src:url("assets/fonts/JetBrainsMono-Bold.ttf");font-weight:700}}
.bgw{{position:absolute;left:0;top:0;width:1080px;height:2000px;background:#ecebe5 url(assets/bg.jpg) repeat-y;background-size:1080px 1920px}}
.scene{{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0}} #sA{{opacity:1}}
.hk{{position:absolute;left:65px;width:950px;color:{INK};white-space:nowrap;font-weight:900;letter-spacing:-.045em}}
.w,.v{{display:inline-block}} .w{{opacity:0}} .w.gh{{opacity:.14}}
.em{{font-family:"Noto Color Emoji";font-weight:400;letter-spacing:0;display:inline-block}}
.org{{color:{ORG}}}
.badge{{position:absolute;left:65px;top:295px;width:128px;height:128px;border-radius:30px;background:#fff;border:4px solid {INK};display:flex;align-items:center;justify-content:center;box-shadow:7px 7px 0 {INK}}}
.badge img{{width:66%;height:66%}}
.mini{{position:absolute;left:65px;width:104px;height:104px;border-radius:26px;background:#fff;border:4px solid {INK};box-shadow:6px 6px 0 {INK};display:flex;align-items:center;justify-content:center;opacity:0}} .mini img{{width:66%;height:66%}}
.a1{{top:430px;font-size:184px;line-height:190px}} .a2{{top:622px;font-size:98px;line-height:116px;display:flex;gap:26px;align-items:baseline}}
.w0{{display:inline-block}}
.sel{{position:relative;isolation:isolate;display:inline-block;--s:0}}
.sel::before{{content:"";position:absolute;left:-14px;right:-12px;top:6px;bottom:0;background:#0b0b0b;transform-origin:0 50%;transform:scaleX(var(--s));z-index:-1}}
.rep{{position:absolute;left:80px;width:920px;background:#17181b;border-radius:40px;box-shadow:0 26px 50px rgba(20,20,20,.28),0 3px 0 #000;border:2px solid #2b2c32;z-index:20;color:#f2f2ee}}
.rtxt{{position:absolute;left:48px;right:40px;top:56px;font-size:80px;line-height:96px;font-weight:800;letter-spacing:-.03em}} .rtxt .w{{margin-right:.24em}}
.comp{{position:absolute;left:80px;width:920px;background:#17181b;border-radius:40px;box-shadow:0 26px 50px rgba(20,20,20,.28),0 3px 0 #000;border:2px solid #2b2c32;z-index:20;font-weight:500;opacity:0}}
.chd{{position:absolute;left:44px;top:36px;height:70px;display:flex;align-items:center}} .chlogo{{height:62px;width:62px;filter:invert(1)}}
.txt{{position:absolute;left:48px;right:48px;top:60px;font-size:72px;line-height:96px;color:#f2f2ee;letter-spacing:-.015em}}
.tw{{display:inline-block;white-space:nowrap;margin-right:.26em}} .L{{opacity:0;position:relative;display:inline-block}}
.L::after{{content:"";position:absolute;right:-9px;top:.14em;width:6px;height:.78em;background:#fff;opacity:var(--cur,0)}}
.ku{{position:relative}}.ku::after{{content:'';position:absolute;left:-6px;right:-12px;bottom:-16px;height:22px;transform-origin:0 50%;transform:scaleX(var(--u,0));background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 22' preserveAspectRatio='none'><path d='M4 14 C 40 4, 70 20, 110 11 S 170 6, 196 12' stroke='%23f2f2ee' stroke-width='6' fill='none' stroke-linecap='round'/></svg>") no-repeat;background-size:100% 100%}}
.cbt{{position:absolute;left:44px;right:44px;bottom:36px;height:88px;display:flex;align-items:center;justify-content:space-between}}
.plus{{width:88px;height:88px;border-radius:50%;border:3px solid #3a3b42;display:flex;align-items:center;justify-content:center}}
.send{{width:88px;height:88px;border-radius:50%;background:#5c5d63;display:flex;align-items:center;justify-content:center}}
.tag.at{{left:65px;z-index:31}}
.tag{{position:absolute;left:80px;top:296px;height:84px;padding:0 34px;background:#0b0b0b;color:#fff;font-family:JBM,monospace;font-weight:700;font-size:42px;letter-spacing:.04em;display:flex;align-items:center;border-radius:8px;z-index:30;opacity:0}}
.curve{{position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:25;opacity:0;pointer-events:none}}
.ans47{{position:absolute;left:65px;top:925px;width:950px;height:300px}} .sel.big{{display:block;width:950px;text-align:center;font-size:290px;line-height:300px;font-weight:900;letter-spacing:-.06em;color:{INK};padding:0}}
#mini1{{left:65px;top:960px}} #mini2{{left:65px;top:760px}} #mini3{{left:65px;top:760px}}
.sel.big::before{{left:0;right:0;top:0;bottom:0;border-radius:0}}
.h2a{{top:920px;font-size:96px;line-height:104px}} .h2b{{top:1024px;font-size:96px;line-height:104px}} .h2c{{top:1128px;font-size:96px;line-height:106px;display:flex;align-items:baseline}}
.h2a .w,.h2b .w{{margin-right:.22em}}
.h2c .em{{font-size:96px;margin-left:24px}}
.ast{{position:absolute;left:830px;top:880px;opacity:0}}
.h100{{top:835px;font-size:380px;line-height:380px;letter-spacing:-.06em}}
.heart{{position:absolute;left:775px;top:850px;font-size:170px;line-height:170px;opacity:0;filter:grayscale(1)}}
.bigdots{{position:absolute;left:60px;top:160px;display:flex;gap:34px}} .bigdots b{{display:block;width:78px;height:78px;border-radius:50%;background:#f2f2ee;opacity:.35}}
.rep.dotsc{{opacity:0}}
.e1{{top:445px;font-size:146px;line-height:156px;white-space:nowrap}} .hl_{{display:inline-block;opacity:0}}
.lol{{position:absolute;left:800px;top:298px;font-size:130px;line-height:130px;opacity:0;font-family:"Noto Color Emoji"}}
.e2{{top:650px;font-size:66px;line-height:80px;font-weight:500;letter-spacing:-.02em}} .e2 .w{{margin-right:.1em}}
.e3{{top:740px;font-size:150px;line-height:164px}} .e3 .w{{margin-right:.22em}}
.e4{{top:925px;font-size:96px;line-height:240px;display:flex;align-items:baseline;gap:24px}}
.e4 .l2b{{font-weight:500;letter-spacing:-.02em}} .e4 .n100{{font-size:250px;letter-spacing:-.06em;line-height:240px}} .e4 .em{{font-size:130px}}
.ringE{{position:absolute;left:290px;top:945px;width:520px;height:280px;opacity:0}}
'''

# ------------------------------------------------------------- timeline helpers
def type_in(ids, t0, dur, cur_id=None, clickg=-17):
    n = len(ids)
    for k, i in enumerate(ids):
        t = t0 + dur * k / n
        js(f"tl.fromTo('#{i}',{{opacity:0,y:10,scale:.8}},{{opacity:1,y:0,scale:1,duration:.09,ease:'power2.out',immediateRender:false}},{T(t)});")
        js(f"tl.set('#{i}',{{'--cur':1}},{T(t)});")
        if k: js(f"tl.set('#{ids[k - 1]}',{{'--cur':0}},{T(t)});")
        if k % 2 == 0: sfx("click_a.ogg" if (k // 2) % 2 == 0 else "click_b.ogg", t, clickg)
def wordin(i, t, dy=40, d=.22):
    js(f"tl.fromTo('#{i}',{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{d},ease:'power2.out',immediateRender:false}},{T(t)});")
def scroll(outs, t, d=.28, nxt=None):
    js(f"tl.to('{outs}',{{y:-1250,filter:'blur(10px)',duration:{d},ease:'power2.in'}},{T(t)});")
    js(f"tl.to('{outs}',{{opacity:0,duration:{d * .45:.3f},ease:'power3.out'}},{T(t)});")
    sfx("whoosh_c.ogg", t - .02, -12)
def scroll_in(sel, t, d=.28):
    js(f"tl.fromTo('{sel}',{{opacity:1,y:560,filter:'blur(8px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:{d},ease:'power2.inOut',immediateRender:false}},{T(t)});")
def card_in(card, tagid, cvid, t):
    js(f"tl.fromTo('#{card}',{{opacity:0,y:70,filter:'blur(10px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:.4,ease:'power3.out',immediateRender:false}},{T(t)});")
    js(f"tl.fromTo('#tag{tagid}',{{opacity:0,x:-12,rotation:-4}},{{opacity:1,x:0,rotation:-1.5,duration:.3,ease:'power3.out',immediateRender:false}},{T(t + .08)});")
    js(f"tl.set('#cv{cvid}',{{opacity:1}},{T(t + .1)});"); js(f"tl.to('#mp{cvid}',{{strokeDashoffset:0,duration:.45,ease:'power2.inOut'}},{T(t + .12)});")
    sfx("pop_b.ogg", t + .05, -9); sfx("select.ogg", t + .2, -12)
def sendpulse(card, t):
    js(f"tl.to('#{card}s',{{background:'#f4f4f0',duration:.15,ease:'power2.out'}},{T(t - .1)});")
    js(f"tl.fromTo('#{card}s',{{scale:1}},{{scale:1.18,duration:.15,ease:'power2.out',yoyo:true,repeat:1}},{T(t)});")
    sfx("ding.ogg", t, -12); sfx("pop_a.ogg", t + .02, -9)
def card_out(card, tagid, cvid, t):
    js(f"tl.to('#{card},#tag{tagid},#cv{cvid}',{{opacity:0,filter:'blur(14px)',y:-30,duration:.26,ease:'power1.in'}},{T(t)});")
def sel_in(selid, t, d=.32, white=True):
    js(f"tl.fromTo('#{selid}',{{'--s':0}},{{'--s':1,duration:{d},ease:'power2.inOut',immediateRender:false}},{T(t)});")
    if white: js(f"tl.to('#{selid}',{{color:'#ffffff',duration:.2}},{T(t + d * .4)});")
    sfx("select.ogg", t, -9); sfx("impactsoft.ogg", t + .1, -13)

# ============================== A: hook
js("tl.fromTo('.bgw',{y:0},{y:-70,duration:%.2f,ease:'sine.inOut',yoyo:true,repeat:1},0);" % (D / 2))
js("tl.fromTo('#bdg',{rotation:-14,scale:.86,y:10},{rotation:-3,scale:1,y:0,duration:.4,ease:'power3.out'},0);")
js("tl.to('#bdg',{rotation:3,duration:3,ease:'sine.inOut'},.4);")
js("tl.fromTo('#aC',{scale:1},{scale:1.02,duration:.2,ease:'power2.out',yoyo:true,repeat:1,transformOrigin:'0% 70%'},0.04);")
sel_in("selA", .18, .3)
js("tl.fromTo('#aT',{opacity:.14,y:26},{opacity:1,y:0,duration:.25,ease:'power2.out',immediateRender:false},.32);")
js("tl.fromTo('#rep0',{scale:.97,y:20},{scale:1,y:0,duration:.4,ease:'expo.out',transformOrigin:'50% 50%'},0);")
js("tl.to('#rep0',{y:-12,duration:3.2,ease:'sine.inOut'},.4);")
for i, t in enumerate([0.0, .22, .34, .46, .56, .68, .82]):
    if i == 0: continue
    js(f"tl.fromTo('#g{i}',{{opacity:.14,y:20}},{{opacity:1,y:0,duration:.2,ease:'power2.out',immediateRender:false}},{T(t)});")
js("tl.set('#g0',{opacity:1},0);")
js("tl.fromTo('#g7',{opacity:.14,scale:.6,rotation:-12},{opacity:1,scale:1,rotation:0,duration:.4,ease:'back.out(1.5)',transformOrigin:'50% 60%',immediateRender:false},.98);")
js("tl.to('#g7',{rotation:9,duration:.5,ease:'sine.inOut',yoyo:true,repeat:5,transformOrigin:'50% 60%'},1.4);")
js("tl.fromTo('#sA',{scale:1},{scale:1.01,duration:3.2,ease:'sine.inOut',transformOrigin:'50% 40%'},0);")
sfx("impactsoft.ogg", 0.04, -8); sfx("pop_a.ogg", .22, -9); sfx("tick.ogg", .46, -12); sfx("tick.ogg", .68, -12); sfx("ding.ogg", .98, -9); sfx("pop_b.ogg", 1.0, -12)

# ============================== B1: Card 1 -> 47
tB1 = 3.3
scroll("#sA", tB1); js(f"tl.set('#sA',{{opacity:0}},{T(tB1 + .3)});")
card_in("c1", 1, 1, tB1 + .3)
type_in(ids1, tB1 + .55, .75)
sendpulse("c1", tB1 + 1.45)
js(f"tl.fromTo('#a47b',{{opacity:0,y:40}},{{opacity:1,y:0,duration:.01,immediateRender:false}},{T(tB1 + 1.7)});")
js(f"tl.set('#sB1',{{opacity:1}},{T(tB1 + 1.69)});")
js(f"tl.fromTo('#tagn1',{{opacity:0,x:-12,rotation:-4}},{{opacity:1,x:0,rotation:-1.5,duration:.3,ease:'power3.out',immediateRender:false}},{T(tB1 + 1.6)});")
sel_in("sel47", tB1 + 1.75, .4)
js(f"tl.fromTo('#t47',{{scale:.9}},{{scale:1,duration:.35,ease:'expo.out',transformOrigin:'50% 60%',immediateRender:false}},{T(tB1 + 1.8)});")
js(f"tl.fromTo('#a47b',{{y:0}},{{y:-10,duration:1.0,ease:'sine.inOut'}},{T(tB1 + 2.0)});")

# ============================== B2: Card 2 -> begging hero
tB2 = tB1 + 2.4
card_out("c1", 1, 1, tB2); js(f"tl.to('#sB1',{{y:-900,opacity:0,filter:'blur(10px)',duration:.3,ease:'power2.in'}},{T(tB2)});"); sfx("whoosh_c.ogg", tB2 - .02, -12)
card_in("c2", 2, 2, tB2 + .3)
type_in(ids2, tB2 + .55, .95)
js(f"tl.fromTo('#qw8,#qw9',{{'--u':0}},{{'--u':1,duration:.4,ease:'power2.inOut',immediateRender:false}},{T(tB2 + 1.65)});"); sfx("select.ogg", tB2 + 1.68, -10)
sendpulse("c2", tB2 + 1.9)
tH = tB2 + 2.2
js(f"tl.set('#sB2',{{opacity:1}},{T(tH - .01)});")
js(f"tl.fromTo('#tagn2',{{opacity:0,x:-12,rotation:-4}},{{opacity:1,x:0,rotation:-1.5,duration:.3,ease:'power3.out',immediateRender:false}},{T(tH - .05)});")
for i, (idn, dt) in enumerate([("hb00", 0), ("hb01", .12), ("hb02", .22), ("hb03", .32), ("hb10", .44), ("hb11", .54), ("hb20", .7)]):
    wordin(idn, tH + dt, 40, .24); sfx("tick.ogg", tH + dt, -12)
js(f"tl.fromTo('#hb21',{{opacity:0,scale:.5,rotation:-14}},{{opacity:1,scale:1,rotation:0,duration:.45,ease:'back.out(1.4)',transformOrigin:'50% 60%',immediateRender:false}},{T(tH + .95)});")
js(f"tl.to('#hb21',{{rotation:8,duration:.5,ease:'sine.inOut',yoyo:true,repeat:3,transformOrigin:'50% 60%'}},{T(tH + 1.4)});")
sfx("ding.ogg", tH, -8); sfx("pop_a.ogg", tH + .95, -11)
sel_in("selB", tH + 1.25, .4)

# ============================== C: Yes -> 100
tC = tH + 2.8      # begging hero visible >= 2.4 s
js(f"tl.to('#c2,#tag2,#cv2',{{opacity:0,filter:'blur(14px)',y:-30,duration:.26,ease:'power1.in'}},{T(tC)});")
js(f"tl.to('#sB2',{{y:-1000,opacity:0,filter:'blur(10px)',duration:.3,ease:'power2.in'}},{T(tC)});"); sfx("whoosh_c.ogg", tC - .02, -12)
card_in("c3", 3, 3, tC + .3)
type_in(ids3, tC + .55, .3, clickg=-14)
sendpulse("c3", tC + 1.05)
t100 = tC + 1.35
js(f"tl.set('#sC',{{opacity:1}},{T(t100 - .01)});")
js(f"tl.fromTo('#tagn3',{{opacity:0,x:-12,rotation:-4}},{{opacity:1,x:0,rotation:-1.5,duration:.3,ease:'power3.out',immediateRender:false}},{T(t100 - .1)});")
js(f"tl.fromTo('#n100',{{opacity:0,y:50,scale:.9}},{{opacity:1,y:0,scale:1,duration:.6,ease:'sine.inOut',transformOrigin:'0% 60%',immediateRender:false}},{T(t100)});")
js(f"tl.fromTo('#heart',{{opacity:0,scale:.4,rotation:-20}},{{opacity:1,scale:1,rotation:10,duration:.55,ease:'back.out(1.5)',transformOrigin:'50% 60%',immediateRender:false}},{T(t100 + .3)});")
js(f"tl.to('#heart',{{y:-14,duration:.9,ease:'sine.inOut',yoyo:true,repeat:1}},{T(t100 + .9)});")
sfx("pop_a.ogg", t100, -7); sfx("ding.ogg", t100 + .3, -10)

# ============================== D: Fahhhhh -> typing dots (near-silence)
tD = t100 + 1.3
js(f"tl.to('#c3,#tag3,#cv3',{{opacity:0,filter:'blur(14px)',y:-30,duration:.26,ease:'power1.in'}},{T(tD)});")
js(f"tl.to('#sC',{{y:-1000,opacity:0,filter:'blur(10px)',duration:.3,ease:'power2.in'}},{T(tD)});"); sfx("whoosh_c.ogg", tD - .02, -12)
card_in("c4", 4, 4, tD + .3)
type_in(ids4, tD + .55, .55, clickg=-14)
sendpulse("c4", tD + 1.2)
tdot = tD + 1.3
js(f"tl.fromTo('#tagn4',{{opacity:0,x:-12,rotation:-4}},{{opacity:1,x:0,rotation:-1.5,duration:.3,ease:'power3.out',immediateRender:false}},{T(tdot - .05)});")
js(f"tl.fromTo('#rep4',{{opacity:0,y:60,filter:'blur(10px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:.4,ease:'power3.out',immediateRender:false}},{T(tdot)});")
js(f"tl.fromTo('#bd b',{{y:0,opacity:.35}},{{y:-18,opacity:1,duration:.26,ease:'sine.inOut',yoyo:true,repeat:6,stagger:.13,immediateRender:false}},{T(tdot + .3)});")

# ============================== E: the punchline
tE = tdot + 1.3
js(f"tl.to('#c4,#tag4,#cv4,#rep4,#tagn4',{{opacity:0,filter:'blur(14px)',y:-40,duration:.3,ease:'power1.in'}},{T(tE)});"); sfx("whoosh_c.ogg", tE - .02, -11)
js(f"tl.set('#sE',{{opacity:1}},{T(tE + .15)});")
js(f"tl.fromTo('#tagn5',{{opacity:0,x:-12,rotation:-4}},{{opacity:1,x:0,rotation:-1.5,duration:.3,ease:'power3.out',immediateRender:false}},{T(tE + .15)});")
for i in range(8):
    js(f"tl.fromTo('#ha{i}',{{opacity:0,y:60,scale:.8}},{{opacity:1,y:0,scale:1,duration:.26,ease:'power3.out',immediateRender:false}},{T(tE + .3 + i * .055)});")
    if i % 2 == 0: sfx("pop_a.ogg", tE + .3 + i * .055, -11)
js(f"tl.fromTo('#lol',{{opacity:0,scale:.3,rotation:-30}},{{opacity:1,scale:1,rotation:10,duration:.5,ease:'back.out(1.6)',transformOrigin:'50% 60%',immediateRender:false}},{T(tE + .35)});")
js(f"tl.to('#lol',{{rotation:-8,duration:.35,ease:'sine.inOut',yoyo:true,repeat:5}},{T(tE + .9)});")
sfx("impactsoft.ogg", tE + .3, -3); sfx("subhit.ogg", tE + .32, -10)
for i in range(6): wordin(f"e2{i}", tE + 1.0 + i * .07, 28, .22)
wordin("e30", tE + 1.45, 40, .24); wordin("e31", tE + 1.55, 40, .24); wordin("e32", tE + 1.65, 40, .24)
sel_in("selE", tE + 1.8, .3)
wordin("e40", tE + 2.05, 40, .24)
js(f"tl.fromTo('#e41',{{opacity:0,scale:.82}},{{opacity:1,scale:1,duration:.5,ease:'sine.inOut',transformOrigin:'50% 70%',immediateRender:false}},{T(tE + 2.15)});")
wordin("e42", tE + 2.4, 40, .24)
js(f"tl.fromTo('#e42 .em',{{rotation:-25,scale:.5}},{{rotation:6,scale:1,duration:.5,ease:'back.out(1.5)',transformOrigin:'50% 60%',immediateRender:false}},{T(tE + 2.4)});")
tR = tE + 2.1
js(f"tl.fromTo('#ringE',{{opacity:0,scale:.96}},{{opacity:1,scale:1,duration:.6,ease:'sine.inOut',transformOrigin:'50% 50%',immediateRender:false}},{T(tR - .1)});")
js(f"tl.fromTo('#ringE',{{rotation:-.5,y:0}},{{rotation:.6,y:-5,duration:2.4,ease:'sine.inOut',immediateRender:false}},{T(tR - .1)});")
js(f"tl.fromTo('#sE',{{y:0}},{{y:-10,duration:3.4,ease:'sine.inOut'}},{T(tE + .4)});")
sfx("pop_b.ogg", tE + 1.05, -12); sfx("pop_a.ogg", tE + 2.17, -9); sfx("pop_b.ogg", tE + 2.45, -9); sfx("ding.ogg", tR + .5, -14)

# ============================== loop: soft dissolve back to frame 0
tL = tE + 4.0
assert tL + .85 <= D + .01, (tL, D)
js(f"tl.to('#sE',{{opacity:0,filter:'blur(14px)',duration:.4,ease:'power1.in'}},{T(tL)});")
reset = f'''
tl.set('#sA',{{opacity:0,y:0,scale:1}},{T(tL - .02)});
tl.set('#bdg',{{rotation:-14,scale:.86,y:10}},{T(tL - .02)});
tl.set('#rep0',{{y:20,scale:.97}},{T(tL - .02)});
tl.set('#a47',{{opacity:1}},{T(tL - .02)});
tl.set('#selA',{{'--s':0,color:'{INK}'}},{T(tL - .02)});
tl.set('#aT',{{opacity:.14,y:0}},{T(tL - .02)});
tl.set('#g1,#g2,#g3,#g4,#g5,#g6,#g7',{{opacity:.14,y:0,scale:1,rotation:0}},{T(tL - .02)});
'''
for ln in reset.strip().splitlines(): js(ln)
js(f"tl.fromTo('#sA',{{opacity:0,filter:'blur(14px)'}},{{opacity:1,filter:'blur(0px)',duration:.5,ease:'power2.out',immediateRender:false}},{T(tL + .38)});")
sfx("whoosh_b.ogg", tL + .2, -14); sfx("pop_a.ogg", tL + .5, -14)
print("tB1", round(tB1, 2), "tB2", round(tB2, 2), "tH", round(tH, 2), "tC", round(tC, 2), "t100", round(t100, 2), "tD", round(tD, 2), "tdot", round(tdot, 2), "tE", round(tE, 2), "tL", round(tL, 2), "D", D)
# music ducking plan (seconds): tender at the begging line, near-silence before the punchline, groove back after
json.dump(dict(D=D, tender=[round(tH - .1, 2), round(tC + .2, 2)], silence=[round(tdot + .1, 2), round(tE + .25, 2)]), open(H_ + "/duck90b.json", "w"))

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
