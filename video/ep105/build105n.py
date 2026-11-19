#!/usr/bin/env python3
"""Episode 105 (Claude Ultra free for open-source people), Miki style + GSAP skills.
Structure from the ep101 rebuild (video/ep102/build102v5.py): every screen is a function that returns a timeline,
the master timeline places screens at the voice times, one house curve set (expoOut / expoIn / inOut / critically damped spring),
words rise out of masks when spoken, DrawSVG for strokes, only transform/opacity/filter animated.
Reads  voice/narration-v105-cues.json via cues105.json (13 lines), voice/words-v105.json (Whisper word times).
Writes hf/index.html, sfx105.json, out/build105.log.  Facts: channel/episode-105-script.md "Facts used" only.
Screens: S1 frame 0 (1)  S2 empty checklist (2)  S3 price (3)  S4a/b (4)  S5a/b (5)  S6 hidden (6)  S7 opens (7)
         S8 real page + ring (8)  S9 saveable card (9)  S10 value (10)  S11 send (11)  S12 link in bio (12)  S13 follow (13) + frame 0 returns
Safe area: key text x 108-972, y 269-1248; right edge <= 864 below y 1056.
"""
import json, os, re, sys
H_ = os.path.dirname(os.path.abspath(__file__))
INK = "#0f0f0f"; ORG = "#D97757"; GREY = "#8a8982"
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
LOG = []
def say(x): LOG.append(x); print(x)

CUES = json.load(open(H_ + "/cues105.json"))
LN = {l["n"]: l for l in CUES["lines"]}
assert len(LN) == 11
s = lambda n: float(LN[n]["start"]); e = lambda n: float(LN[n]["end"])
D = float(CUES["D"])
WORDS = [[w["word"], w["start"], w["end"]] for w in json.load(open(H_ + "/voice/words-v105.json"))]
tF = round(D - .22, 3)
SRC = {}
def W(n, toks, k=0, fallback=.5):
    """time of the k-th whisper word in line n matching one of toks (normalised), else a fraction of the line"""
    toks = (toks,) if isinstance(toks, str) else toks
    c = 0
    for w, a_, b_ in WORDS:
        if s(n) - .15 <= a_ <= e(n) + .15 and any(norm(w) == t or (len(t) > 3 and norm(w).startswith(t)) for t in toks):
            if c == k: return round(a_, 3)
            c += 1
    return round(s(n) + fallback * (e(n) - s(n)), 3)

def line(cls, words, top, size, acc=(), ready=False, left=108, lh=1.12, extra="", fast=True):
    """words: list of (text, time) tuples; one mask per word"""
    out = []
    for i_, (txt, t) in enumerate(words):
        if not ready and fast: t = min(t, CUR + .14 + .1 * i_)
        ac = norm(txt) in acc
        out.append(f'<span class="m"><span class="w{" acc" if ac else ""}{" rdy" if ready else ""}" data-t="{t:.3f}">{txt}</span></span>')
    return f'<div class="ln {cls}" style="left:{left}px;top:{top}px;font-size:{size}px;line-height:{round(size * lh)}px">{"".join(out)}{extra}</div>'
def seq(txt, times):
    ws = txt.split(); assert len(ws) == len(times), (txt, times)
    return list(zip(ws, times))
ring = lambda id_, left, top, w, h: (f'<svg class="ring" id="{id_}" viewBox="0 0 400 160" preserveAspectRatio="none" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px" data-decor>'
                                     f'<path d="M14 84 C6 30 130 8 214 10 C318 12 394 40 388 84 C382 132 270 150 190 148 C96 146 20 132 14 84 Z" fill="none" stroke="{ORG}" stroke-width="5" vector-effect="non-scaling-stroke" stroke-linecap="round"/></svg>')
STK = '<i class="stk"></i>'
A = "assets/"
SC = {}; T = {}; CUR = 0

# ---------------------------------------------------------------- S1 frame 0 (line 1): complete on frame 0
tfree = W(1, "free", 0, .6)
SC["S1"] = (f'<div class="wm" id="wm"><img src="{A}claude-logo-wordmark.png"></div>'
            f'<div class="ln hv" id="s1u" style="left:102px;top:424px;font-size:150px;line-height:150px">ULTRA</div>'
            f'<img class="lg" id="gh" src="{A}github-mark.png" style="left:862px;top:294px;width:108px;height:108px">'
            f'<div class="ln hv" id="s1p" style="left:100px;top:588px;font-size:190px;line-height:204px"><span class="old">$200{STK}</span><span class="nw">$0</span></div>'
            f'<div class="ln hv" id="s1m" style="left:102px;top:790px;font-size:156px;line-height:160px">6 MONTHS</div>'
            f'<div class="ln hv acc1" id="s1f" style="left:98px;top:952px;font-size:300px;line-height:288px">FREE</div>')
T["S1"] = dict(t0=0, free=tfree, end=s(2))
CUR = s(2)

# ---------------------------------------------------------------- S2 price (line 2): the strike is drawn ONCE, when "two hundred dollars" is said
T["S1"]["end"] = s(2)
CUR = s(2)
SC["S2"] = (line("lead", seq("Normally", [W(2, "normally", 0, .02)]), 380, 70) +
            line("hv", [("$200", W(2, "200", 0, .55))], 470, 350, lh=1.0, extra=STK) +
            line("hv", seq("A MONTH.", [W(2, "a", 0, .8), W(2, "month", 0, .9)]), 850, 176))
T["S2"] = dict(t0=s(2), strike=W(2, "200", 0, .55), end=s(3))
CUR = s(3)

# ---------------------------------------------------------------- S3 the offer: both marks, OPEN SOURCE, 6 MONTHS (line 3)
SC["S3"] = (f'<img class="lg" id="m3a" src="{A}claude-sparkle-site.png" style="left:108px;top:400px;width:270px;height:270px">'
            f'<img class="lg" id="m3b" src="{A}github-mark.png" style="left:470px;top:424px;width:224px;height:224px">' +
            line("hv", seq("OPEN SOURCE", [W(3, "open", 0, .3), W(3, "source", 0, .4)]), 720, 118, lh=1.0) +
            line("hv", seq("6 MONTHS", [W(3, "for", 0, .8), W(3, "6", 0, .9)]), 850, 158, lh=1.0, acc=("months",)))
T["S3"] = dict(t0=s(3), end=s(4))
CUR = s(4)

# ---------------------------------------------------------------- S4 who it is for (line 4)
marks = "".join(f'<img class="lg pm" id="pm{i}" src="{A}{f}" style="left:{108 + i * 292}px;top:470px;width:280px;height:280px">' for i, f in enumerate(["linux-tux.png", "python-logo.png", "nodejs-logo.png"]))
SC["S4"] = (marks + line("hv", seq("LOTS OF PEOPLE", [W(4, "lots", 0, .5), W(4, "of", 0, .55), W(4, "people", 0, .6)]), 800, 96, lh=1.0) +
            line("hv", seq("USE YOUR WORK", [W(4, "use", 0, .7), W(4, "you", 0, .8), W(4, "can", 0, .9)]), 910, 96, lh=1.0, acc=("work",)))
T["S4"] = dict(t0=s(4), end=s(5))
CUR = s(5)

# ---------------------------------------------------------------- S5 real page + ring (line 5)
SC["S5"] = (line("lead", seq("Not sure you fit?", [W(5, "not", 0, .05), W(5, "sure", 0, .1), W(5, "you", 0, .15), W(5, "fit", 0, .2)]), 270, 62) +
            line("hv", seq("APPLY ANYWAY.", [W(5, "apply", 0, .6), W(5, "anyway", 0, .7)]), 346, 100, acc=("apply", "anyway")) +
            f'<div class="shot" id="pg"><img src="{A}claude-for-oss-heading-criteria.png"></div>' + ring("rgP", 112, 1137, 752, 110))
T["S5"] = dict(t0=s(5), ringat=W(5, "apply", 0, .6), end=s(6))
CUR = s(6)

# ---------------------------------------------------------------- S6 the card to save: three simple steps (line 6)
steps = [("Sign in with", "GitHub"), ("Tell them about", "your project"), ("Wait for", "the email")]
stp = "".join(f'<div class="stp" id="st{i}"><b>{i + 1}</b><span>{a_}<br>{b_}</span></div>' for i, (a_, b_) in enumerate(steps))
SC["S6"] = f'<div class="sv6" id="sv">{stp}<i class="sheen" id="shn"></i></div>'
T["S6"] = dict(t0=s(6), tell=W(6, "tell", 0, .4), wait=W(6, "wait", 0, .8), end=s(7))
CUR = s(7)

# ---------------------------------------------------------------- S7 value (line 7)
SC["S7"] = (line("lead", seq("6 months free is", [W(7, "6", 0, .05), W(7, "months", 0, .15), W(7, "free", 0, .25), W(7, "thats", 0, .4)]), 470, 80) +
            line("hv", [("$1,200", W(7, "1200", 0, .6))], 560, 272, lh=1.0, acc=("1200",)) +
            line("lead", seq("at list price", [.2, .3, .4]), 860, 80) + ring("rgV", 84, 545, 860, 300))
T["S7"] = dict(t0=s(7), val=W(7, "1200", 0, .6), end=s(8))
CUR = s(8)

# ---------------------------------------------------------------- S8 scarcity (line 8)
SC["S8"] = (line("hv", seq("10,000", [W(8, "10", 0, .45)]), 420, 244, lh=1.0, acc=("10000",)) +
            line("hv", seq("SPOTS", [W(8, "spots", 0, .8)]), 680, 244, lh=1.0) +
            line("lead", seq("GitHub account 2+ years old", [.2, .3, .4, .5, .6]), 960, 62))
T["S8"] = dict(t0=s(8), end=s(9))
CUR = s(9)

# ---------------------------------------------------------------- S9 send (line 9)
SC["S9"] = (line("lead", seq("Send this to a", [W(9, "send", 0, .05), W(9, "this", 0, .2), W(9, "to", 0, .3), W(9, "a", 0, .4)]), 470, 88) +
            line("hv", seq("FRIEND", [W(9, "friend", 0, .55)]), 585, 210, lh=1.0, acc=("friend",)) +
            line("lead", seq("who builds things.", [W(9, "who", 0, .7), W(9, "builds", 0, .8), W(9, "things", 0, .92)]), 810, 88, acc=("builds",)))
T["S9"] = dict(t0=s(9), end=s(10))
CUR = s(10)

# ---------------------------------------------------------------- S10 link in bio (line 10)
SC["S10"] = (line("lead", seq("The setup's in the", [W(10, "the", 0, .02), W(10, "setups", 0, .2), W(10, "in", 0, .35), W(10, "the", 1, .45)]), 450, 90) +
             line("hv", seq("LINK", [W(10, "link", 0, .6)]), 560, 200, lh=1.0) + line("hv", seq("IN BIO.", [W(10, "in", 1, .75), W(10, "bio", 0, .9)]), 760, 200, acc=("bio",), lh=1.0))
T["S10"] = dict(t0=s(10), end=s(11))
CUR = s(11)

# ---------------------------------------------------------------- S11 follow (line 11, ep104 take)
SC["S11"] = (line("lead", seq("Want the next one?", [W(11, "want", 0, .02), W(11, "the", 0, .2), W(11, "next", 0, .4), W(11, "one", 0, .6)]), 470, 90) +
             line("hv", [("FOLLOW.", W(11, "follow", 0, .6))], 590, 200, acc=("follow",), fast=False) + ring("rgF", 78, 574, 900, 250) +
             line("lead", seq("and you'll see it.", [W(11, "and", 0, .75), W(11, "youll", 0, .85), W(11, "see", 0, .92), W(11, "it", 0, .97)]), 840, 80, fast=False))
T["S11"] = dict(t0=s(11), acc=W(11, "follow", 0, .6), end=tF)

for k in T:
    for kk, v in list(T[k].items()):
        if isinstance(v, float): T[k][kk] = round(v, 3)
T["tF"] = tF; T["D"] = D

# ---------------------------------------------------------------- sfx (soft, real library clips from ep89c/sfx)
SFX = []
def sfx(f, t, g=-13): SFX.append(dict(f=f, t=round(max(0, t), 3), g=g))
sfx("whoosh_b.ogg", .08, -15); sfx("select.ogg", T["S1"]["free"] - .04, -13); sfx("select.ogg", T["S2"]["strike"], -14)
sfx("click_a.ogg", s(3) + .25, -17); sfx("click_a.ogg", s(4) + .3, -17); sfx("click_a.ogg", T["S5"]["ringat"] + .3, -17)
sfx("click_a.ogg", s(6) + .3, -15); sfx("click_a.ogg", T["S6"]["tell"], -15); sfx("click_a.ogg", T["S6"]["wait"], -15)
sfx("select.ogg", T["S7"]["val"], -13); sfx("select.ogg", s(8) + .4, -14); sfx("whoosh_b.ogg", s(9) - .05, -17); sfx("select.ogg", T["S11"]["acc"], -14)
SFX.sort(key=lambda x: x["t"]); json.dump(SFX, open(H_ + "/sfx105.json", "w"), indent=1)

scenes = "".join(f'<div class="sc" id="sc{n[1:]}">{SC[n]}</div>' for n in SC)
CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;font-weight:500;color:{INK};font-kerning:none}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}}
.bgw{{position:absolute;left:-20px;top:-20px;width:1120px;height:1960px;background:#ecebe5 url(assets/bg.jpg);background-size:1120px 1960px;will-change:transform}}
#cam{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}}
.sc{{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0;visibility:hidden;will-change:transform,opacity}} #sc1{{opacity:1;visibility:visible}}
.sc>*{{position:absolute}}
.lg{{display:block;flex:none;object-fit:contain}}
.ln{{white-space:nowrap}}
.m{{display:inline-block;overflow:hidden;vertical-align:top;padding:0 .05em .08em 0;margin-right:.2em}} .lead .m{{margin-right:.24em}}
.w{{display:inline-block;transform:translateY(112%);will-change:transform}} .w.rdy{{transform:none}}
.lead .w{{font-weight:500;letter-spacing:-.02em;color:#33322f}} .hv .w{{font-weight:900;letter-spacing:-.045em}}
.w.acc{{color:{INK}}}
.ring{{overflow:visible}}
.hv{{font-weight:900;letter-spacing:-.045em}}
.old{{position:relative;display:inline-block;color:#4f4e49;margin-right:.34em}} .nw{{display:inline-block;color:{INK}}}
.wm{{position:absolute;left:104px;top:292px;width:600px;height:131px;overflow:hidden}} .wm img{{position:absolute;left:0;top:-234.4px;width:600px;height:600px;max-width:none}}
.stk{{position:absolute;left:-.03em;right:-.03em;top:53%;height:.09em;border-radius:.04em;background:{ORG};transform-origin:0 50%;transform:scaleX(0)}} .old .wm{{position:absolute;left:104px;top:292px;width:600px;height:131px;overflow:hidden}} .wm img{{position:absolute;left:0;top:-234.4px;width:600px;height:600px;max-width:none}}
.stk{{transform:scaleX(1)}}
#s1f{{color:{ORG}}}
.col{{position:absolute;top:800px;width:150px;height:440px;border:6px solid #cfcdc4;border-radius:36px;background:rgba(255,255,255,.55);opacity:0;visibility:hidden}} .col b{{position:absolute;left:0;right:0;top:26px;text-align:center;font-weight:900;font-size:70px;line-height:76px;color:#b4b2a8}}
.pm{{opacity:0;visibility:hidden}}
.hid{{left:410px;top:810px;width:260px;height:260px;border-radius:60px;background:#fff;box-shadow:0 30px 60px rgba(20,20,20,.16);overflow:hidden;opacity:0;visibility:hidden}} .hid img{{position:absolute;left:50px;top:50px;width:160px;height:160px;filter:blur(20px);opacity:.9}} .hid b{{position:absolute;left:0;right:0;top:20px;text-align:center;font-weight:900;font-size:170px;line-height:220px;color:{INK}}}
.shot{{left:108px;top:468px;width:864px;height:772px;overflow:hidden;background:#fbfaf7;border-radius:40px;box-shadow:0 30px 60px rgba(20,20,20,.18);opacity:0;visibility:hidden}} .shot img{{position:absolute;left:-228px;top:-538.8px;width:1296px;height:1308px;max-width:none}}
.sv{{left:108px;top:272px;width:864px;height:976px;border-radius:44px;background:#fff;box-shadow:0 30px 60px rgba(20,20,20,.16);padding:40px 0 0 44px;opacity:0;visibility:hidden;overflow:hidden}} .sheen{{position:absolute;top:-20%;left:0;width:200px;height:150%;background:linear-gradient(100deg,rgba(255,255,255,0),rgba(217,119,87,.16),rgba(255,255,255,0));transform:translateX(-300px) skewX(-12deg);pointer-events:none}}
.sh{{font-weight:900;font-size:32px;letter-spacing:.06em;text-transform:uppercase;color:{GREY};height:52px;line-height:52px;opacity:0}} .sh.pl2{{margin-top:26px}}
.cr{{display:flex;align-items:center;gap:22px;height:92px;opacity:0;width:716px;border-bottom:2px solid #eeede7}} .cr b{{flex:none;width:54px;height:54px;border-radius:27px;background:{ORG};color:#fff;text-align:center;line-height:54px;font-weight:900;font-size:30px}} .cr span{{font-weight:900;font-size:35px;letter-spacing:-.02em;white-space:nowrap}}
.ex{{height:62px;line-height:62px;font-weight:800;font-size:37px;letter-spacing:-.015em;white-space:nowrap;opacity:0;padding-left:76px}}
.sp{{margin-top:20px;font-weight:900;font-size:86px;line-height:90px;letter-spacing:-.045em;color:{ORG};opacity:0}}
.sv6{{left:108px;top:360px;width:864px;height:760px;border-radius:44px;background:#fff;box-shadow:0 30px 60px rgba(20,20,20,.16);overflow:hidden;opacity:0;visibility:hidden;padding:40px 0 0 44px}}
.stp{{display:flex;align-items:center;gap:30px;height:226px;opacity:0;border-bottom:2px solid #eeede7;width:760px}} .stp:nth-of-type(3){{border-bottom:0}} .stp b{{flex:none;width:96px;height:96px;border-radius:48px;background:{ORG};color:#fff;text-align:center;line-height:96px;font-weight:900;font-size:56px}} .stp span{{font-weight:900;font-size:56px;line-height:64px;letter-spacing:-.02em;white-space:nowrap}}
.bx{{position:absolute;top:1090px;width:132px;height:132px;border:6px solid #cfcdc4;border-radius:34px;background:rgba(255,255,255,.7);opacity:0;visibility:hidden}} .bx b{{position:absolute;left:0;right:0;top:0;text-align:center;font-weight:900;font-size:68px;line-height:120px;color:#a9a79d}} .bx svg{{position:absolute;left:23px;top:23px;width:74px;height:74px}}
#rowB{{position:absolute;left:0;top:0;width:1080px;height:1920px;pointer-events:none}}
'''
JS = r'''
gsap.registerPlugin(SplitText, DrawSVGPlugin, CustomEase);
const T=__T__, ORG='__ORG__', INK='__INK__';
const expoOut=CustomEase.create("expoOut","0.16,1,0.3,1"), expoIn=CustomEase.create("expoIn","0.7,0,0.84,0"), inOut=CustomEase.create("mvInOut","0.65,0,0.35,1");
const spring=(w=>{const f=t=>1-(1+w*t)*Math.exp(-w*t), n=f(1); return t=>f(t)/n})(9);
const show=id=>gsap.fromTo(id,{autoAlpha:0,y:10,filter:'blur(6px)'},{autoAlpha:1,y:0,filter:'blur(0px)',duration:.3,ease:'power2.out',immediateRender:false});
const hide=id=>gsap.to(id,{autoAlpha:0,y:-12,filter:'blur(8px)',duration:.22,ease:expoIn});
function type(t,id,S){
  gsap.utils.toArray(id+' .w:not(.rdy)').forEach(w=>{
    const at=Math.max(0,+w.dataset.t-S-.07);
    if(w.classList.contains('acc')){ gsap.set(w,{y:0,yPercent:0}); const sp=SplitText.create(w,{type:'chars',mask:'chars',aria:'none'});
      t.fromTo(sp.chars,{yPercent:112},{yPercent:0,duration:.5,ease:expoOut,stagger:.03},at).to(sp.chars,{color:ORG,duration:.3,ease:'power1.out',stagger:.03},at+.12); }
    else t.fromTo(w,{yPercent:112,y:0},{yPercent:0,y:0,duration:.46,ease:expoOut,immediateRender:false},at); });
}
function ringDraw(t,id,at){ t.fromTo(id+' path',{drawSVG:'0%'},{drawSVG:'100%',duration:.8,ease:'power2.inOut',immediateRender:false},at) }
gsap.set('.ring path, .bx svg path',{drawSVG:'0%'});
const card=(t,sel,at,y)=>t.fromTo(sel,{autoAlpha:0,y:y||40},{autoAlpha:1,y:0,duration:.55,ease:spring,immediateRender:false},at);
/* a screen: shows 0.04 s before its first word, builds its words, drifts its lines, hides 0.2 s before the next screen */
function scr(id,o,fn,opt){ opt=opt||{}; const S=o.t0-.04, t=gsap.timeline(); t.add(show(id),0); type(t,id,S);
  t.to(id+' .ln',{x:8,duration:Math.max(.6,o.end-o.t0-.5),ease:'sine.inOut',stagger:.05},.4);
  if(fn) fn(t,a=>a-S,S); if(!opt.keep) t.add(hide(id),Math.max(.3,o.end-S-.22)); return t; }
const pops=(t,sel,at,each)=>t.fromTo(sel,{autoAlpha:0,y:36,scale:.9},{autoAlpha:1,y:0,scale:1,duration:.55,ease:spring,stagger:each,immediateRender:false},at);
const tl=gsap.timeline({paused:true});
tl.fromTo('#cam',{scale:1},{scale:1.014,duration:T.D/4,ease:'sine.inOut',yoyo:true,repeat:3},0)
  .fromTo('.bgw',{x:0,y:0},{x:-14,y:-12,duration:T.D/2,ease:'sine.inOut',yoyo:true,repeat:1},0);
/* S1 frame 0: complete from the first frame (the strike on $200 is part of it, never redrawn) */
tl.add((()=>{ const o=T.S1,t=gsap.timeline();
  t.fromTo('#s1f',{scale:1.07,transformOrigin:'0% 50%'},{scale:1,duration:.9,ease:spring,immediateRender:false},Math.max(.12,o.free-.2))
   .fromTo('#gh',{y:0},{y:-8,duration:1.0,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false},0)
   .fromTo('#s1p .nw',{scale:1.05,transformOrigin:'0% 50%'},{scale:1,duration:.8,ease:spring,immediateRender:false},.1)
   .to('#s1u',{x:8,duration:1.9,ease:'sine.inOut'},.1).to('#wm',{x:8,duration:1.9,ease:'sine.inOut'},.1).to('#s1m',{x:8,duration:1.9,ease:'sine.inOut'},.1).to('#s1f',{x:8,duration:1.9,ease:'sine.inOut'},.1).to('#s1p',{x:8,duration:1.9,ease:'sine.inOut'},.1);
  t.add(hide('#sc1'),o.end-.24); return t; })(),0);
/* S2: the strike is ONE tween: scaleX is set to 0 here and drawn once at the spoken "two hundred" */
gsap.set('#sc2 .stk',{scaleX:0});
tl.add(scr('#sc2',T.S2,(t,r)=>{ t.to('#sc2 .stk',{scaleX:1,duration:.5,ease:'power3.inOut'},Math.max(.3,r(T.S2.strike)-.05)); }),T.S2.t0-.04);
const pulse=(t,sel,at,k,each)=>t.fromTo(sel,{scale:1,transformOrigin:'50% 50%'},{scale:k,duration:.5,yoyo:true,repeat:1,ease:'sine.inOut',stagger:each||0,immediateRender:false},at);
tl.add(scr('#sc3',T.S3,(t,r)=>{ pops(t,'#m3a',.1,0); pops(t,'#m3b',.25,0);
  [.9,1.9,2.9].forEach(a=>{ pulse(t,'#m3a',a,1.12); pulse(t,'#m3b',a+.12,1.12); });
  t.fromTo('#sc3 .hv',{x:0},{x:0},0); [1.4,2.6].forEach(a=>t.fromTo('#sc3 .hv',{scale:1,transformOrigin:'0% 50%'},{scale:1.05,duration:.5,yoyo:true,repeat:1,ease:'sine.inOut',stagger:.15,immediateRender:false},a)); }),T.S3.t0-.04);
tl.add(scr('#sc4',T.S4,(t,r)=>{ pops(t,'#sc4 .pm',.1,.14); [.9,1.9,2.9].forEach(a=>pulse(t,'#sc4 .pm',a,1.1,.22)); [1.2,2.4].forEach(a=>t.fromTo('#sc4 .hv',{scale:1,transformOrigin:'0% 50%'},{scale:1.05,duration:.5,yoyo:true,repeat:1,ease:'sine.inOut',stagger:.15,immediateRender:false},a)); }),T.S4.t0-.04);
tl.add(scr('#sc5',T.S5,(t,r)=>{ card(t,'#pg',.35); t.fromTo('#pg img',{scale:1,transformOrigin:'0% 100%'},{scale:1.035,duration:Math.max(1.5,T.S5.end-T.S5.t0-.4),ease:'sine.inOut',immediateRender:false},.5);
  ringDraw(t,'#rgP',Math.max(1.3,r(T.S5.ringat)+.4)); }),T.S5.t0-.04);
tl.add(scr('#sc6',T.S6,(t,r)=>{ card(t,'#sv',.05,30); t.fromTo('#st0',{autoAlpha:0,y:24},{autoAlpha:1,y:0,duration:.5,ease:expoOut,immediateRender:false},.25);
  t.fromTo('#st1',{autoAlpha:0,y:24},{autoAlpha:1,y:0,duration:.5,ease:expoOut,immediateRender:false},Math.max(.7,r(T.S6.tell)-.25));
  t.fromTo('#st2',{autoAlpha:0,y:24},{autoAlpha:1,y:0,duration:.5,ease:expoOut,immediateRender:false},Math.max(1.2,r(T.S6.wait)-.25));
  t.fromTo('#sv',{scale:1,transformOrigin:'50% 40%'},{scale:1.04,duration:Math.max(1.5,T.S6.end-T.S6.t0-.2),ease:'sine.inOut',immediateRender:false},.4);
  [1.3,2.4].forEach(a=>t.fromTo('#shn',{x:-300},{x:1100,duration:1.1,ease:'sine.inOut',immediateRender:false},a));
  t.fromTo('#sc6 .stp b',{scale:1},{scale:1.12,duration:.35,yoyo:true,repeat:1,ease:'sine.inOut',stagger:.3,immediateRender:false},1.6); }),T.S6.t0-.04);
tl.add(scr('#sc7',T.S7,(t,r)=>{ ringDraw(t,'#rgV',r(T.S7.val)+.2); }),T.S7.t0-.04);
tl.add(scr('#sc8',T.S8,(t,r)=>{ t.fromTo('#sc8 .hv',{scale:1,transformOrigin:'0% 50%'},{scale:1.05,duration:.5,yoyo:true,repeat:1,ease:'sine.inOut',stagger:.2,immediateRender:false},.9); }),T.S8.t0-.04);
tl.add(scr('#sc9',T.S9,null),T.S9.t0-.04);
tl.add(scr('#sc10',T.S10,null),T.S10.t0-.04);
tl.add(scr('#sc11',T.S11,(t,r)=>{ ringDraw(t,'#rgF',r(T.S11.acc)+.1); },{keep:true}),T.S11.t0-.04);
tl.to('#sc11',{autoAlpha:0,filter:'blur(6px)',duration:.12,ease:'power1.in'},T.tF-.12).set('#sc1',{autoAlpha:0},T.tF-.3).fromTo('#sc1',{autoAlpha:0,filter:'blur(6px)'},{autoAlpha:1,filter:'blur(0px)',duration:.2,ease:'power2.out',immediateRender:false},T.tF).to({},{duration:.001},T.D-.001);
window.__timelines=window.__timelines||{}; window.__timelines["main"]=tl; tl.seek(0);
window.__reel={duration:T.D,seek:t=>{tl.seek(t)}};
'''.replace("__T__", json.dumps(T, separators=(",", ":"))).replace("__ORG__", ORG).replace("__INK__", INK)
CDN = "https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/"
html = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="{CDN}gsap.min.js"></script>
<script src="{CDN}SplitText.min.js"></script>
<script src="{CDN}DrawSVGPlugin.min.js"></script>
<script src="{CDN}CustomEase.min.js"></script>
<style>
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Black.otf");font-weight:900}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-ExtraBold.otf");font-weight:800}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Medium.otf");font-weight:500}}
{CSS}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
<div class="bgw" data-decor></div><div id="cam">{scenes}</div>
</div>
<script>
{JS}
</script></body></html>'''
os.makedirs(H_ + "/out", exist_ok=True)
open(H_ + "/hf/index.html", "w").write(html)
say(f"ep105 build D={D} sfx={len(SFX)}")
say("screens: " + "  ".join(f"{k}:{v['t0']:.2f}-{v['end']:.2f}" for k, v in T.items() if isinstance(v, dict) and 't0' in v))
open(H_ + "/out/build105.log", "w").write("\n".join(LOG) + "\n")
