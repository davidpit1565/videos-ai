#!/usr/bin/env python3
"""ep90b FINAL8 - the real ghost run, redrawn, tight: light #FAFAF8 + faint grid, no typing (bubbles pop in softly), one thing at a time,
47 giant, 100 once, 'Fahhhhh' as the user's bubble, the laugh reply with STILL on a black box, end card with 'ghosts' on a black box.
Voice = the CURRENT video/ep90/voice/narration90b.wav + cues90b.json (not re-rendered, not delayed). Builds into /tmp/e8/hf8 (OUT_DIR env).
All ChatGPT text is the real run (checked against the recording frames): "47", "Wait... can I have a second chance? (pleading face)",
"100 (orange heart, shown grey)", "HAHAHAHA (loudly crying face) You gave me a second chance and I STILL chose 100 (skull)"."""
import json, os
H_ = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("OUT_DIR", "/tmp/e8/hf8")
INK = "#0f0f0f"
J = []; SFX = []
def js(s): J.append(s)
def sfx(f, t, g=-6): SFX.append((f, round(t, 3), g))
def T(t): return f"{max(0.0, t):.3f}"
EM = lambda c: f'<span class="em">{c}</span>'

CU = json.load(open("/home/user/videos-ai/video/ep90/voice/cues90b.json")); LN = {l["n"]: l for l in CU["lines"]}
Wd = lambda n, i: LN[n]["words"][i][1]; We = lambda n, i: LN[n]["words"][i][2]
S_ = lambda n: LN[n]["start"]; E_ = lambda n: LN[n]["end"]

# ---------------------------------------------------------------- markup
badge = '<div class="badge" id="bdg"><img src="assets/chatgpt.svg"></div>'
def ub(i, text, cls=""):
    return f'<div class="tag me" id="me{i}">ME</div><div class="ub {cls}" id="ub{i}">{text}</div>'
def at(i, top=700): return f'<div class="tag at" id="at{i}" style="top:{top}px">CHATGPT</div>'
dots = lambda i: f'<div class="dots" id="dots{i}"><b></b><b></b><b></b></div>'

beg = ["Wait...", "can I", "have a", "second", "chance?"]
markup = f'''
<div class="bgw" data-decor></div>
<div class="scene" id="s1" style="opacity:1">{badge}
 <div class="hk a1" id="a1"><span class="v" id="aC">I gave ChatGPT</span></div>
 <div class="hk a2" id="a2"><span class="w gh" id="aA">a</span><span class="sel" id="selA"><span id="a47">47-day</span></span></div>
 <div class="hk a3" id="a3"><span class="w gh" id="aT">timeout.</span></div>
</div>
<div class="scene" id="s2">{ub(1, "Choose a number between 0 and 100")}{at(1)}{dots(1)}
 <div class="n47" id="n47">47</div></div>
<div class="scene" id="s3">{ub(2, 'Now we won\'t be able to talk for <span class="ul" id="ul2">47 days</span>')}{at(2)}{dots(2)}
 <div class="beg" id="beg"><div class="bl" id="bl0"><span class="w" id="bw0">Wait...</span></div>
  <div class="bl" id="bl1"><span class="w" id="bw1">can</span> <span class="w" id="bw2">I</span></div>
  <div class="bl" id="bl2"><span class="w" id="bw3">have</span> <span class="w" id="bw4">a</span> <span class="w" id="bw5">second</span></div>
  <div class="bl" id="bl3"><span class="w" id="bw6">chance?</span> <span class="w" id="bw7">{EM("🥺")}</span></div></div></div>
<div class="scene" id="s4">{ub(3, "Yes", "big")}{at(3)}{dots(3)}
 <div class="n100" id="n100">100</div><div class="heart" id="heart">{EM("🧡")}</div></div>
<div class="scene" id="s5">{ub(4, "Fahhhhh", "big")}{at(4, 660)}
 <div class="lol1" id="lol1">{"".join(f'<span class="hl_" id="ha{i}">{c}</span>' for i, c in enumerate("HAHAHAHA"))}<span class="hl_ em2" id="cry">{EM("😭")}</span></div>
 <div class="lol2" id="lol2"><span class="w" id="l20">You</span> <span class="w" id="l21">gave</span> <span class="w" id="l22">me</span> <span class="w" id="l23">a</span> <span class="w" id="l24">second</span> <span class="w" id="l25">chance</span></div>
 <div class="lol3" id="lol3"><span class="w" id="l30">and</span> <span class="w" id="l31">I</span> <span class="sel" id="selE"><span class="w" id="l32">STILL</span></span></div>
 <div class="lol4" id="lol4"><span class="w" id="l33">chose</span> <span class="w" id="l34">100</span> <span class="w" id="l35">{EM("💀")}</span></div>
</div>
<div class="scene" id="s6">
 <div class="hk f1" id="f1"><span class="w" id="f10">Send</span> <span class="w" id="f11">this</span> <span class="w" id="f12">to</span></div>
 <div class="hk f2" id="f2"><span class="w" id="f20">someone</span> <span class="w" id="f21">who</span></div>
 <div class="hk f3" id="f3"><span class="sel" id="selF"><span class="w" id="f30">ghosts</span></span> <span class="w" id="f31">you.</span></div>
</div>
'''

css = f'''
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Black.otf");font-weight:900}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-ExtraBold.otf");font-weight:800}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Medium.otf");font-weight:500}}
@font-face{{font-family:"JBM";src:url("assets/fonts/JetBrainsMono-Bold.ttf");font-weight:700}}
.bgw{{position:absolute;left:0;top:0;width:1080px;height:2000px;background:#FAFAF8 url(assets/bg8.png) repeat-y;background-size:1080px 2000px}}
.scene{{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0}}
.hk{{position:absolute;left:90px;width:900px;color:{INK};white-space:nowrap;font-weight:900;letter-spacing:-.045em}}
.w,.v{{display:inline-block}} .w{{opacity:0}} .w.gh{{opacity:.14}}
.em{{font-family:"Noto Color Emoji";font-weight:400;letter-spacing:0;display:inline-block}}
.badge{{position:absolute;left:90px;top:360px;width:128px;height:128px;border-radius:30px;background:#fff;border:4px solid {INK};display:flex;align-items:center;justify-content:center;box-shadow:7px 7px 0 {INK}}}
.badge img{{width:66%;height:66%}}
.a1{{top:530px;font-size:116px;line-height:128px}} .a2{{top:680px;font-size:206px;line-height:220px;display:flex;gap:26px;align-items:baseline}} .a3{{top:910px;font-size:206px;line-height:220px}}
.sel{{position:relative;isolation:isolate;display:inline-block;--s:0}}
.sel::before{{content:"";position:absolute;left:-16px;right:-14px;top:8px;bottom:-4px;background:#0b0b0b;transform-origin:0 50%;transform:scaleX(var(--s));z-index:-1}}
.tag{{position:absolute;left:90px;height:76px;padding:0 30px;background:#0b0b0b;color:#fff;font-family:JBM,monospace;font-weight:700;font-size:38px;letter-spacing:.04em;display:flex;align-items:center;border-radius:8px;z-index:30;opacity:0}}
.tag.me{{top:292px}}
.ub{{position:absolute;left:90px;top:388px;width:900px;background:#17181b;color:#f4f4f0;border-radius:44px;padding:48px 54px 52px;font-size:70px;line-height:84px;font-weight:500;letter-spacing:-.015em;box-shadow:0 24px 46px rgba(20,20,20,.22),0 3px 0 #000;opacity:0}}
.ub.big{{font-size:118px;line-height:130px;padding:46px 58px 52px;font-weight:800;letter-spacing:-.03em}}
.ul{{position:relative;display:inline-block;font-weight:800;white-space:nowrap}} .ul::after{{content:"";position:absolute;left:0;right:0;bottom:-6px;height:7px;border-radius:4px;background:#f4f4f0;transform-origin:0 50%;transform:scaleX(var(--u,0))}}
.dots{{position:absolute;left:90px;top:830px;display:flex;gap:30px;opacity:0}} .dots b{{display:block;width:62px;height:62px;border-radius:50%;background:{INK};opacity:.3}}
.n47{{position:absolute;left:90px;top:770px;width:900px;text-align:center;font-size:640px;line-height:440px;font-weight:900;letter-spacing:-.06em;color:{INK};opacity:0;white-space:nowrap}}
.n100{{position:absolute;left:90px;top:790px;font-size:430px;line-height:420px;font-weight:900;letter-spacing:-.06em;color:{INK};opacity:0;white-space:nowrap}}
.heart{{position:absolute;left:845px;top:790px;font-size:130px;line-height:130px;opacity:0;filter:grayscale(1)}}
.beg{{position:absolute;left:90px;top:810px;width:900px;font-weight:900;letter-spacing:-.045em;color:{INK}}}
.bl{{font-size:120px;line-height:132px;white-space:nowrap}} .bl .w{{margin-right:.2em}} .bl .em{{font-size:100px;vertical-align:.02em}}
.lol1{{position:absolute;left:90px;top:750px;font-size:132px;line-height:140px;font-weight:900;letter-spacing:-.045em;color:{INK};white-space:nowrap;display:flex;align-items:baseline}} .hl_{{display:inline-block;opacity:0}} .em2{{margin-left:22px;font-size:104px}}
.lol2{{position:absolute;left:90px;top:905px;font-size:66px;line-height:80px;font-weight:800;letter-spacing:-.025em;color:{INK};white-space:nowrap}} .lol2 .w{{margin-right:.14em}}
.lol4,.lol3{{position:absolute;left:90px;top:1000px;font-size:112px;line-height:124px;font-weight:900;letter-spacing:-.04em;color:{INK};white-space:nowrap}} .lol3 .w,.lol4 .w{{margin-right:.15em}} .lol4{{top:1124px;font-weight:900;letter-spacing:-.04em;color:{INK};white-space:nowrap}} .lol4 .em{{font-size:100px}}
.f1{{top:470px;font-size:140px;line-height:160px}} .f2{{top:650px;font-size:140px;line-height:160px}} .f3{{top:830px;font-size:156px;line-height:180px}} .f1 .w,.f2 .w,.f3 .w{{margin-right:.16em}}
'''

# ---------------------------------------------------------------- helpers
def pop(sel, t, d=.4, dy=30):
    js(f"tl.fromTo('{sel}',{{opacity:0,y:{dy},scale:.95,filter:'blur(8px)'}},{{opacity:1,y:0,scale:1,filter:'blur(0px)',duration:{d},ease:'power3.out',transformOrigin:'50% 50%',immediateRender:false}},{T(t)});")
def wordin(i, t, dy=34, d=.22):
    js(f"tl.fromTo('#{i}',{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{d},ease:'power2.out',immediateRender:false}},{T(t)});")
def sel_in(selid, t, d=.3, white=True):
    js(f"tl.fromTo('#{selid}',{{'--s':0}},{{'--s':1,duration:{d},ease:'power2.inOut',immediateRender:false}},{T(t)});")
    if white: js(f"tl.to('#{selid}',{{color:'#ffffff',duration:.18}},{T(t + d * .4)});")
    sfx("select.ogg", t, -9); sfx("impactsoft.ogg", t + .08, -13)
def swap(old, new, t, d=.16):     # soft crossfade: old dissolves, new scene becomes visible (its children pop in themselves)
    js(f"tl.to('{old}',{{opacity:0,filter:'blur(10px)',duration:{d},ease:'power1.in'}},{T(t - .1)});")
    js(f"tl.set('{new}',{{opacity:1}},{T(t)});")
    sfx("whoosh_c.ogg", t - .06, -14)
def tag_in(sel, t):
    js(f"tl.fromTo('{sel}',{{opacity:0,x:-8,rotation:-4}},{{opacity:1,x:0,rotation:-1.5,duration:.3,ease:'power3.out',immediateRender:false}},{T(t)});")
def dots_run(i, t0, t1):
    js(f"tl.fromTo('#dots{i}',{{opacity:0,y:14}},{{opacity:1,y:0,duration:.25,ease:'power2.out',immediateRender:false}},{T(t0)});")
    n = max(1, int((t1 - t0 - .15) / .5))
    js(f"tl.fromTo('#dots{i} b',{{y:0,opacity:.3}},{{y:-14,opacity:1,duration:.25,ease:'sine.inOut',yoyo:true,repeat:{2 * n - 1},stagger:.1,immediateRender:false}},{T(t0 + .1)});")
    js(f"tl.to('#dots{i}',{{opacity:0,duration:.12}},{T(t1)});")
    sfx("tick.ogg", t0 + .1, -12)

# ---------------------------------------------------------------- timing from the voice
T2 = 2.52; T3 = 5.22; T4 = 9.95; T5 = 11.15; T6 = 14.2
HOLD_END = round(E_(7) + 1.0, 2)           # static end card ~1 s after the last word
tL = HOLD_END
D = round(tL + .45, 2)

# ============================== S1 hook (line 1) - frame 0 already shows 'I gave ChatGPT' + badge; rest ghosted and building with the voice
js("tl.fromTo('.bgw',{y:0},{y:-60,duration:%.2f,ease:'sine.inOut',yoyo:true,repeat:1},0);" % (D / 2))
js("tl.fromTo('#bdg',{rotation:-14,scale:.86,y:10},{rotation:-3,scale:1,y:0,duration:.4,ease:'power3.out'},0);")
js("tl.to('#bdg',{rotation:3,duration:2.2,ease:'sine.inOut'},.4);")
js("tl.fromTo('#aC',{scale:1},{scale:1.02,duration:.2,ease:'power2.out',yoyo:true,repeat:1,transformOrigin:'0% 70%'},0.04);")
js(f"tl.fromTo('#aA',{{opacity:.14,y:26}},{{opacity:1,y:0,duration:.22,ease:'power2.out',immediateRender:false}},{T(Wd(1, 3) - .04)});")
sel_in("selA", Wd(1, 4) - .08, .3)
js(f"tl.fromTo('#aT',{{opacity:.14,y:30}},{{opacity:1,y:0,duration:.28,ease:'power2.out',immediateRender:false}},{T(Wd(1, 6) - .06)});")
js("tl.fromTo('#s1',{scale:1},{scale:1.012,duration:2.4,ease:'sine.inOut',transformOrigin:'50% 40%'},0);")
sfx("impactsoft.ogg", 0.04, -8); sfx("pop_a.ogg", Wd(1, 3), -9); sfx("tick.ogg", Wd(1, 6), -12)

# ============================== S2 line 2: bubble, dots, 47 giant
swap("#s1", "#s2", T2)
pop("#ub1", T2 + .08); tag_in("#me1", T2 + .1); sfx("pop_a.ogg", T2 + .1, -9)
dots_run(1, 3.3, Wd(2, 9) - .3); tag_in("#at1", 3.3)
t47 = Wd(2, 9) - .1
js(f"tl.set('#n47',{{opacity:1}},{T(t47)});")
js(f"tl.fromTo('#n47',{{scale:.82,y:30,filter:'blur(8px)'}},{{scale:1,y:0,filter:'blur(0px)',duration:.45,ease:'expo.out',transformOrigin:'50% 55%',immediateRender:false}},{T(t47)});")
js(f"tl.to('#n47',{{scale:1.03,duration:1.1,ease:'sine.inOut'}},{T(t47 + .5)});")
sfx("pop_b.ogg", t47, -8); sfx("impactsoft.ogg", t47 + .04, -9); sfx("ding.ogg", t47 + .05, -11)

# ============================== S3 lines 3-4: bubble, 47 days underline, dots, begging reply
swap("#s2", "#s3", T3)
pop("#ub2", T3 + .08); tag_in("#me2", T3 + .1); sfx("pop_a.ogg", T3 + .1, -9)
js(f"tl.fromTo('#ul2',{{'--u':0}},{{'--u':1,duration:.4,ease:'power2.inOut',immediateRender:false}},{T(Wd(3, 6) - .05)});"); sfx("select.ogg", Wd(3, 6), -10)
tb = Wd(4, 0) - .05
dots_run(2, 7.4, tb - .2); tag_in("#at2", 7.4)
wordin("bw0", tb, 34, .26); sfx("ding.ogg", tb, -10); sfx("pop_b.ogg", tb + .05, -10)
for idn, (n, i) in [("bw1", (4, 2)), ("bw2", (4, 3)), ("bw3", (4, 4)), ("bw4", (4, 5)), ("bw5", (4, 6)), ("bw6", (4, 7))]:
    wordin(idn, Wd(n, i) - .06, 34, .22); sfx("tick.ogg", Wd(n, i) - .06, -12)
js(f"tl.fromTo('#bw7',{{opacity:0,scale:.5,rotation:-14}},{{opacity:1,scale:1,rotation:0,duration:.45,ease:'back.out(1.4)',transformOrigin:'50% 60%',immediateRender:false}},{T(We(4, 7) + .02)});")
js(f"tl.to('#bw7',{{rotation:8,duration:.5,ease:'sine.inOut',yoyo:true,repeat:1,transformOrigin:'50% 60%'}},{T(We(4, 7) + .5)});")
sfx("pop_a.ogg", We(4, 7) + .05, -11)

# ============================== S4 line 5: Yes, then 100 (once)
swap("#s3", "#s4", T4)
pop("#ub3", T4 + .08); tag_in("#me3", T4 + .1); sfx("pop_a.ogg", T4 + .1, -9)
t100 = Wd(5, 2) - .05
tag_in("#at3", t100 - .12)
js(f"tl.set('#n100',{{opacity:1}},{T(t100)});")
js(f"tl.fromTo('#n100',{{scale:.86,y:30,filter:'blur(8px)'}},{{scale:1,y:0,filter:'blur(0px)',duration:.42,ease:'expo.out',transformOrigin:'0% 55%',immediateRender:false}},{T(t100)});")
js(f"tl.fromTo('#heart',{{opacity:0,scale:.4,rotation:-20}},{{opacity:1,scale:1,rotation:8,duration:.5,ease:'back.out(1.5)',transformOrigin:'50% 60%',immediateRender:false}},{T(t100 + .2)});")
sfx("pop_b.ogg", t100, -8); sfx("ding.ogg", t100 + .05, -11); sfx("pop_a.ogg", t100 + .22, -12)

# ============================== S5 line 6: Fahhhhh bubble, then the laugh reply (STILL on black box)
swap("#s4", "#s5", T5)
pop("#ub4", T5 + .08); tag_in("#me4", T5 + .1); sfx("pop_a.ogg", T5 + .1, -9)
tl_ = S_(6) - .4          # 'And it still ...' starts; laugh reply lands with it
tag_in("#at4", tl_)
for i in range(8):
    js(f"tl.fromTo('#ha{i}',{{opacity:0,y:50,scale:.85}},{{opacity:1,y:0,scale:1,duration:.24,ease:'power3.out',immediateRender:false}},{T(tl_ + .06 + i * .035)});")
    if i % 3 == 0: sfx("pop_a.ogg", tl_ + .06 + i * .035, -11)
js(f"tl.fromTo('#cry',{{opacity:0,scale:.3,rotation:-30}},{{opacity:1,scale:1,rotation:8,duration:.45,ease:'back.out(1.6)',transformOrigin:'50% 60%',immediateRender:false}},{T(tl_ + .34)});")
js(f"tl.to('#cry',{{rotation:-8,duration:.35,ease:'sine.inOut',yoyo:true,repeat:3,transformOrigin:'50% 60%'}},{T(tl_ + .8)});")
sfx("impactsoft.ogg", tl_ + .06, -3); sfx("subhit.ogg", tl_ + .08, -10)
for i in range(6): wordin(f"l2{i}", tl_ + .28 + i * .05, 24, .2)
wordin("l30", Wd(6, 2) - .32, 34, .2); wordin("l31", Wd(6, 2) - .2, 34, .2)
tS = Wd(6, 2) - .1
wordin("l32", tS, 34, .22); sel_in("selE", tS, .28)
wordin("l33", Wd(6, 3) - .1, 34, .22); wordin("l34", Wd(6, 4) - .12, 34, .22); wordin("l35", Wd(6, 4) + .1, 34, .22)
js(f"tl.fromTo('#l35 .em',{{rotation:-25,scale:.5}},{{rotation:6,scale:1,duration:.5,ease:'back.out(1.5)',transformOrigin:'50% 60%',immediateRender:false}},{T(Wd(6, 4) + .12)});")
sfx("pop_b.ogg", Wd(6, 3) - .08, -10); sfx("pop_a.ogg", Wd(6, 4) - .1, -9); sfx("ding.ogg", Wd(6, 4) + .3, -14)

# ============================== S6 end card with line 7
swap("#s5", "#s6", T6)
for idn, k in [("f10", 0), ("f11", 1), ("f12", 2), ("f20", 3), ("f21", 4)]:
    wordin(idn, Wd(7, k) - .05, 34, .22); sfx("tick.ogg", Wd(7, k) - .05, -12)
wordin("f30", Wd(7, 5) - .06, 34, .22); sel_in("selF", Wd(7, 5) - .06, .3)
wordin("f31", Wd(7, 6) - .05, 34, .22)
sfx("pop_a.ogg", Wd(7, 5) - .05, -9); sfx("ding.ogg", Wd(7, 6) + .1, -12)

# ============================== soft ending: dissolve back to frame 0 (loop); the end card holds still before it
js(f"tl.to('#s6',{{opacity:0,filter:'blur(12px)',duration:.25,ease:'power1.in'}},{T(tL - .1)});")
reset = f"""
tl.set('#s1',{{opacity:0,y:0,scale:1}},{T(tL + .1)});
tl.set('#bdg',{{rotation:-14,scale:.86,y:10}},{T(tL + .1)});
tl.set('#selA',{{'--s':0,color:'{INK}'}},{T(tL + .1)});
tl.set('#aT,#aA',{{opacity:.14,y:0}},{T(tL + .1)});
"""
for ln in reset.strip().splitlines(): js(ln)
js(f"tl.fromTo('#s1',{{opacity:0,filter:'blur(12px)'}},{{opacity:1,filter:'blur(0px)',duration:.32,ease:'power2.out',immediateRender:false}},{T(D - .34)});")
sfx("whoosh_b.ogg", tL - .05, -15)
print("T2..T6", T2, T3, T4, T5, T6, "tL", tL, "D", D)

# ---------------------------------------------------------------- narration (current voice, padded, NOT delayed), cues, duck, sfx
import soundfile as _sf, numpy as _np
_x, _sr = _sf.read("/home/user/videos-ai/video/ep90/voice/narration90b.wav"); _x = _x if _x.ndim == 1 else _x[:, 0]
_n = _np.concatenate([_x, _np.zeros(int(D * _sr))])[:int(D * _sr)]
os.makedirs(H_ + "/out", exist_ok=True)
_sf.write(H_ + "/out/narration90b8.wav", _n, _sr, subtype="PCM_16")
json.dump(dict(lines=CU["lines"], D=D), open(H_ + "/cues90b8.json", "w"), indent=1)
json.dump(dict(D=D, tender=[round(tb - .1, 2), round(T4 + .1, 2)], silence=[round(T5 + .05, 2), round(tl_ - .05, 2)], punch=round(tl_, 2)), open(H_ + "/duck90b8.json", "w"))
json.dump([dict(f=f, t=t, g=g) for f, t, g in SFX if 0 <= t < D], open(H_ + "/sfx90b8.json", "w"), indent=1)
JS = "\n".join(J)
html = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#FAFAF8;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;font-weight:500;color:{INK}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#FAFAF8}}
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
os.makedirs(OUT, exist_ok=True)
open(OUT + "/index.html", "w").write(html)
print("sfx", len(SFX), "js", len(J))
