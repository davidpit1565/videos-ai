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
assert len(LN) == 13
s = lambda n: float(LN[n]["start"]); e = lambda n: float(LN[n]["end"])
D = float(CUES["D"])
WORDS = [[w["word"], w["start"], w["end"]] for w in json.load(open(H_ + "/voice/words-v105.json"))]
tF = round(D - .45, 3)
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

def line(cls, words, top, size, acc=(), ready=False, left=108, lh=1.12, extra=""):
    """words: list of (text, time) tuples; one mask per word"""
    out = []
    for txt, t in words:
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
SC = {}; T = {}

# ---------------------------------------------------------------- S1 frame 0 (line 1): complete on frame 0
tfree = W(1, "free", 0, .6)
SC["S1"] = (f'<img class="lg" id="spk" src="{A}claude-sparkle-site.png" style="left:108px;top:296px;width:170px;height:170px">'
            f'<img class="lg" id="gh" src="{A}github-mark.png" style="left:318px;top:338px;width:92px;height:92px">'
            f'<div class="ln hv" id="s1p" style="left:102px;top:520px;font-size:176px;line-height:190px"><span class="old">$200{STK}</span><span class="nw">$0</span></div>'
            f'<div class="ln hv" id="s1m" style="left:102px;top:742px;font-size:156px;line-height:170px">6 MONTHS</div>'
            f'<div class="ln hv acc1" id="s1f" style="left:98px;top:918px;font-size:318px;line-height:300px">FREE</div>')
T["S1"] = dict(t0=0, free=tfree, end=s(2))

# ---------------------------------------------------------------- S2 empty checklist (line 2)
cols = "".join(f'<div class="col" style="left:{108 + i * 178.5:.1f}px"><b>{i + 1}</b></div>' for i in range(5))
SC["S2"] = (line("lead", seq("Thirty seconds.", [W(2, "30", 0, 0), W(2, "seconds", 0, .2)]), 292, 62) +
            line("hv", seq("SEE IF", [W(2, "see", 0, .4), W(2, "if", 0, .45)]), 352, 130) +
            line("hv", seq("YOU GET IT.", [W(2, "you", 0, .6), W(2, "get", 0, .75), W(2, "it", 0, .9)]), 502, 130, acc=("get", "it")) + cols)
T["S2"] = dict(t0=s(2), end=s(3))

# ---------------------------------------------------------------- S3 price (line 3)
SC["S3"] = (line("lead", seq("Normally", [W(3, "normally", 0, .1)]), 430, 62) +
            line("hv", [("$200", W(3, "200", 0, .35))], 495, 330, lh=.98, extra=STK) +
            line("hv", seq("A MONTH.", [W(3, "a", 0, .7), W(3, "month", 0, .8)]), 840, 150))
T["S3"] = dict(t0=s(3), strike=W(3, "month", 0, .85), end=s(4))

# ---------------------------------------------------------------- S4a / S4b (line 4)
t4b = round(W(4, "two", 0, .5) - .06, 3)
SC["S4a"] = (line("hv", [("500+", W(4, "lots", 0, .15))], 470, 300, lh=1.0) +
             line("lead", seq("projects depend on your code", [W(4, "projects", 0, .3), W(4, "depend", 0, .4), W(4, "on", 0, .5), W(4, "your", 0, .55), W(4, "code", 0, .6)]), 800, 56))
T["S4a"] = dict(t0=s(4), end=t4b, tick1=W(4, "code", 0, .6))
marks = "".join(f'<img class="lg pm" id="pm{i}" src="{A}{f}" style="left:{108 + i * 296}px;top:610px;width:272px;height:272px">' for i, f in enumerate(["linux-tux.png", "python-logo.png", "nodejs-logo.png"]))
SC["S4b"] = (line("lead", seq("You help run a big project:", [W(4, "you", 0, .5), W(4, "help", 0, .6), W(4, "run", 0, .65), W(4, "a", 0, .7), W(4, "big", 0, .75), W(4, "project", 0, .9)]), 440, 62, ) + marks)
T["S4b"] = dict(t0=t4b, end=s(5), tick2=W(4, "project", 0, .95))

# ---------------------------------------------------------------- S5a / S5b (line 5)
t5b = round(W(5, "four", 0, .55) - .04, 3)
SC["S5a"] = (line("hv", [("100", W(5, "hundred", 0, .25))], 460, 300, lh=1.0) +
             line("lead", seq("changes accepted", [W(5, "changes", 0, .4), W(5, "accepted", 0, .45)]), 786, 56) +
             line("lead", seq("in other people's projects", [W(5, "into", 0, .5), W(5, "other", 0, .55), W(5, "peoples", 0, .6), W(5, "projects", 0, .65)]), 850, 56))
T["S5a"] = dict(t0=s(5), end=t5b, tick3=W(5, "hundred", 0, .25))
SC["S5b"] = (line("hv", [("20", W(5, "20", 0, .6))], 460, 300, lh=1.0) +
             line("lead", seq("outsiders helped", [W(5, "outsiders", 0, .75), W(5, "helped", 0, .8)]), 786, 56) +
             line("lead", seq("build your project", [W(5, "build", 0, .85), round(W(5, "yours", 0, .9) - .1, 3), W(5, "yours", 0, .92)]), 850, 56))
T["S5b"] = dict(t0=t5b, end=s(6), tick4=W(5, "20", 0, .6))

# ---------------------------------------------------------------- S6 hidden (line 6)
SC["S6"] = (line("lead", seq("The last one, almost", [W(6, "the", 0, .02), W(6, "last", 0, .15), W(6, "one", 0, .3), W(6, "almost", 0, .5)]), 292, 62) +
            line("hv", seq("NOBODY", [W(6, "nobody", 0, .7)]), 352, 150) + line("hv", seq("KNOWS.", [W(6, "knows", 0, .9)]), 522, 150, acc=("knows",)) +
            f'<div class="hid" id="hid"><img src="{A}openssf-icon-color.png"><b id="q">?</b></div>')
T["S6"] = dict(t0=s(6), end=s(7))

# ---------------------------------------------------------------- S7 opens (line 7)
SC["S7"] = (f'<img class="lg" id="ssf" src="{A}openssf-icon-color.png" style="left:108px;top:292px;width:176px;height:176px">' +
            line("lead", seq("OpenSSF score, 0 to 1:", [W(7, "openssf", 0, .2) + d_ for d_ in (-.1, .35, .5, .62, .74)]), 850, 56) +
            line("hv", [("0.4+", W(7, "4", 0, .3))], 480, 330, lh=1.0, acc=("04",)) +
            ring("rgO", 70, 470, 780, 360) +
            line("lead", seq("how much others rely on you", [W(7, "how", 0, .5), W(7, "much", 0, .56), W(7, "other", 0, .62), round(W(7, "relies", 0, .75) - .1, 3), W(7, "relies", 0, .75), W(7, "on", 0, .85)]), 916, 56))
T["S7"] = dict(t0=s(7), open=W(7, "4", 0, .3), end=s(8))

# ---------------------------------------------------------------- S8 real page + ring (line 8)
SC["S8"] = (line("lead", seq("Not on the list?", [W(8, "not", 0, .05), W(8, "on", 0, .1), W(8, "the", 0, .12), W(8, "list", 0, .16)]), 282, 62) +
            line("hv", seq("APPLY ANYWAY.", [W(8, "apply", 0, .4), W(8, "anyway", 0, .5)]), 342, 100, acc=("apply", "anyway")) +
            f'<div class="shot" id="pg"><img src="{A}claude-for-oss-heading-criteria.png"></div>' + ring("rgP", 112, 1090, 780, 118))
T["S8"] = dict(t0=s(8), ringat=W(8, "apply", 0, .4), end=s(9))

# ---------------------------------------------------------------- S9 saveable card (line 9)
crit = ["Lots of projects use your code", "Run a big open-source project", "100+ changes accepted in 12 months", "20+ outside helpers in 12 months", "OpenSSF score 0.4+"]
rows = "".join(f'<div class="cr" id="cr{i}"><b>{i + 1}</b><span>{t}</span></div>' for i, t in enumerate(crit))
SC["S9"] = (f'<div class="sv" id="sv"><div class="sh">Any ONE of these:</div>{rows}<div class="sh pl2" id="pl2">Plus, all of:</div>'
            '<div class="ex" id="ex0">GitHub account 2+ years old</div><div class="ex" id="ex1">Active in the last 90 days</div><div class="ex" id="ex2">Open-source license</div>'
            '<div class="sp" id="sp">10,000 spots</div><i class="sheen" id="shn"></i></div>')
T["S9"] = dict(t0=s(9), plus=W(9, "github", 0, .3), act=W(9, "acted", 0, .6), lic=W(9, "open", 0, .8), spots=W(9, "10", 0, .9), end=s(10))

# ---------------------------------------------------------------- S10 value (line 10)
SC["S10"] = (line("lead", seq("6 months free is", [W(10, "six", 0, .05), W(10, "months", 0, .2), W(10, "free", 0, .3), W(10, "thats", 0, .45)]), 450, 62) +
             line("hv", [("$1,200", W(10, ["1", "12"], 0, .6))], 520, 250, lh=1.0, acc=("1200",)) +
             line("lead", seq("at list price", [round(W(10, ["1", "12"], 0, .6) + d_, 3) for d_ in (.25, .4, .55)]), 800, 62) + ring("rgV", 84, 545, 836, 250))
T["S10"] = dict(t0=s(10), val=W(10, ["1", "12"], 0, .6), end=s(11))

# ---------------------------------------------------------------- S11-S13 close
SC["S11"] = (line("lead", seq("Send this to", [W(11, "send", 0, .1), W(11, "this", 0, .25), W(11, "to", 0, .4)]), 440, 62) +
             line("hv", seq("THE FRIEND", [W(11, "the", 0, .45), W(11, "friend", 0, .6)]), 506, 128) +
             line("hv", seq("WHO CODES.", [W(11, "who", 0, .8), W(11, "codes", 0, .92)]), 640, 128, acc=("codes",)) +
             f'<img class="lg" id="m1" src="{A}claude-sparkle-site.png" style="left:108px;top:850px;width:150px;height:150px">'
             f'<img class="lg" id="m2" src="{A}github-mark.png" style="left:300px;top:872px;width:104px;height:104px">')
T["S11"] = dict(t0=s(11), end=s(12))
SC["S12"] = (line("lead", seq("The setup's in the", [W(12, "the", 0, .02), W(12, "setups", 0, .2), W(12, "in", 0, .35), W(12, "the", 1, .45)]), 520, 84) +
             line("hv", seq("LINK IN BIO.", [W(12, "link", 0, .6), W(12, "in", 1, .75), W(12, "bio", 0, .9)]), 622, 140, acc=("bio",)))
T["S12"] = dict(t0=s(12), end=s(13))
SC["S13"] = (line("lead", seq("Want the next one?", [W(13, "want", 0, .02), W(13, "the", 0, .2), W(13, "next", 0, .4), W(13, "one", 0, .6)]), 500, 84) +
             line("hv", [("FOLLOW.", W(13, "follow", 0, .85))], 600, 196, acc=("follow",)) + ring("rgF", 78, 586, 900, 250))
T["S13"] = dict(t0=s(13), acc=W(13, "follow", 0, .85), end=tF)
for k in T:
    for kk, v in list(T[k].items()):
        if isinstance(v, float): T[k][kk] = round(v, 3)
T["tF"] = tF; T["D"] = D

# ---------------------------------------------------------------- sfx (soft, real library clips from ep89c/sfx)
SFX = []
def sfx(f, t, g=-13): SFX.append(dict(f=f, t=round(max(0, t), 3), g=g))
sfx("whoosh_b.ogg", .08, -15); sfx("select.ogg", T["S1"]["free"] - .04, -13); sfx("click_a.ogg", s(2) + .2, -17)
sfx("select.ogg", T["S3"]["strike"], -14)
for k in ("tick1", "tick2"): sfx("click_a.ogg", T["S4a" if k == "tick1" else "S4b"][k], -14)
sfx("click_a.ogg", T["S5a"]["tick3"], -14); sfx("click_a.ogg", T["S5b"]["tick4"], -14)
sfx("riser.ogg", s(6) + .5, -19); sfx("select.ogg", T["S7"]["open"], -13); sfx("click_a.ogg", T["S8"]["ringat"] + .3, -17)
sfx("select.ogg", T["S9"]["spots"], -14); sfx("whoosh_b.ogg", s(10) - .05, -17); sfx("select.ogg", T["S10"]["val"], -13); sfx("select.ogg", T["S13"]["acc"], -14)
SFX.sort(key=lambda x: x["t"]); json.dump(SFX, open(H_ + "/sfx105.json", "w"), indent=1)

scenes = "".join(f'<div class="sc" id="sc{n[1:]}">{SC[n]}</div>' for n in SC)
rowB = "".join(f'<div class="bx" id="b{i}" style="left:{108 + i * 154}px"><b>{"?" if i == 4 else i + 1}</b><svg viewBox="0 0 100 100"><path d="M24 52 L43 71 L77 32" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg></div>' for i in range(5))
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
.old{{position:relative;display:inline-block;color:{GREY};margin-right:.34em}} .nw{{display:inline-block;color:{INK}}}
.stk{{position:absolute;left:-.03em;right:-.03em;top:53%;height:.075em;border-radius:.04em;background:{ORG};transform-origin:0 50%;transform:scaleX(0)}} .old .stk{{transform:scaleX(1)}}
#s1f{{color:{ORG}}}
.col{{position:absolute;top:700px;width:150px;height:430px;border:6px solid #cfcdc4;border-radius:36px;background:rgba(255,255,255,.55);opacity:0;visibility:hidden}} .col b{{position:absolute;left:0;right:0;top:26px;text-align:center;font-weight:900;font-size:70px;line-height:76px;color:#b4b2a8}}
.pm{{opacity:0;visibility:hidden}}
.hid{{left:380px;top:728px;width:320px;height:320px;border-radius:72px;background:#fff;box-shadow:0 30px 60px rgba(20,20,20,.16);overflow:hidden;opacity:0;visibility:hidden}} .hid img{{position:absolute;left:60px;top:60px;width:200px;height:200px;filter:blur(20px);opacity:.9}} .hid b{{position:absolute;left:0;right:0;top:36px;text-align:center;font-weight:900;font-size:200px;line-height:240px;color:{INK}}}
.shot{{left:108px;top:520px;width:864px;height:680px;overflow:hidden;background:#fbfaf7;border-radius:40px;box-shadow:0 30px 60px rgba(20,20,20,.18);opacity:0;visibility:hidden}} .shot img{{position:absolute;left:-218.5px;top:-573.85px;width:1242px;height:1253.5px;max-width:none}}
.sv{{left:108px;top:292px;width:864px;height:904px;border-radius:44px;background:#fff;box-shadow:0 30px 60px rgba(20,20,20,.16);padding:44px 0 0 44px;opacity:0;visibility:hidden;overflow:hidden}} .sheen{{position:absolute;top:-20%;left:0;width:200px;height:150%;background:linear-gradient(100deg,rgba(255,255,255,0),rgba(217,119,87,.16),rgba(255,255,255,0));transform:translateX(-300px) skewX(-12deg);pointer-events:none}}
.sh{{font-weight:900;font-size:32px;letter-spacing:.06em;text-transform:uppercase;color:{GREY};height:52px;line-height:52px;opacity:0}} .sh.pl2{{margin-top:22px}}
.cr{{display:flex;align-items:center;gap:22px;height:86px;opacity:0;width:716px;border-bottom:2px solid #eeede7}} .cr b{{flex:none;width:54px;height:54px;border-radius:27px;background:{ORG};color:#fff;text-align:center;line-height:54px;font-weight:900;font-size:30px}} .cr span{{font-weight:900;font-size:35px;letter-spacing:-.02em;white-space:nowrap}}
.ex{{height:60px;line-height:60px;font-weight:800;font-size:37px;letter-spacing:-.015em;white-space:nowrap;opacity:0;padding-left:76px}}
.sp{{margin-top:20px;font-weight:900;font-size:78px;line-height:84px;letter-spacing:-.045em;color:{ORG};opacity:0}}
.bx{{position:absolute;top:1070px;width:128px;height:128px;border:6px solid #cfcdc4;border-radius:34px;background:rgba(255,255,255,.7);opacity:0;visibility:hidden}} .bx b{{position:absolute;left:0;right:0;top:0;text-align:center;font-weight:900;font-size:66px;line-height:116px;color:#a9a79d}} .bx svg{{position:absolute;left:22px;top:22px;width:72px;height:72px}}
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
/* world: slow camera and paper drift, always moving a little */
tl.fromTo('#cam',{scale:1},{scale:1.014,duration:T.D/4,ease:'sine.inOut',yoyo:true,repeat:3},0)
  .fromTo('.bgw',{x:0,y:0},{x:-14,y:-12,duration:T.D/2,ease:'sine.inOut',yoyo:true,repeat:1},0);
/* S1: frame 0 is complete; then a soft settle of FREE and a slow turn of the logo */
tl.add((()=>{ const o=T.S1,t=gsap.timeline();
  t.fromTo('#s1f',{scale:1.07,transformOrigin:'0% 50%'},{scale:1,duration:.9,ease:spring,immediateRender:false},Math.max(.12,o.free-.2))
   .fromTo('#spk',{rotation:-5,transformOrigin:'50% 50%'},{rotation:5,duration:2.1,ease:'sine.inOut',immediateRender:false},0)
   .fromTo('#gh',{y:0},{y:-8,duration:1.1,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false},0)
   .fromTo('#s1p .nw',{scale:1.05,transformOrigin:'0% 50%'},{scale:1,duration:.8,ease:spring,immediateRender:false},.1)
   .to('#s1m',{x:8,duration:1.9,ease:'sine.inOut'},.1).to('#s1f',{x:8,duration:1.9,ease:'sine.inOut'},.1).to('#s1p',{x:8,duration:1.9,ease:'sine.inOut'},.1);
  t.add(hide('#sc1'),o.end-.24); return t; })(),0);
/* S2: five empty slots rise one after another */
tl.add(scr('#sc2',T.S2,(t,r)=>{ pops(t,'#sc2 .col',.35,.1); t.fromTo('#sc2 .col',{backgroundColor:'rgba(255,255,255,.55)'},{backgroundColor:'rgba(255,255,255,.9)',duration:.8,stagger:.1,immediateRender:false},.9); }),T.S2.t0-.04);
/* S3: price, then the strike is drawn across it */
tl.add(scr('#sc3',T.S3,(t,r)=>{ t.fromTo('#sc3 .stk',{scaleX:0},{scaleX:1,duration:.5,ease:'power3.inOut',immediateRender:false},r(T.S3.strike)-.1); }),T.S3.t0-.04);
/* S4a: 500+ ; S4b: three real project marks */
tl.add(scr('#sc4a',T.S4a,null),T.S4a.t0-.04);
tl.add(scr('#sc4b',T.S4b,(t,r)=>{ pops(t,'#sc4b .pm',.3,.14); t.fromTo('#sc4b .pm',{y:0},{y:-10,duration:1.4,ease:'sine.inOut',stagger:.12,yoyo:true,repeat:1,immediateRender:false},1.0); }),T.S4b.t0-.04);
tl.add(scr('#sc5a',T.S5a,null),T.S5a.t0-.04);
tl.add(scr('#sc5b',T.S5b,null),T.S5b.t0-.04);
/* S6: box five hidden behind a soft blur */
tl.add(scr('#sc6',T.S6,(t,r)=>{ t.fromTo('#hid',{autoAlpha:0,y:50,scale:.92},{autoAlpha:1,y:0,scale:1,duration:.7,ease:spring,immediateRender:false},.7)
  .fromTo('#hid',{scale:1},{scale:1.04,duration:Math.max(.8,T.S6.end-T.S6.t0-1.3),ease:'sine.inOut',immediateRender:false},1.3)
  .fromTo('#hid img',{rotation:-8,scale:1},{rotation:8,scale:1.08,duration:2,ease:'sine.inOut',immediateRender:false},.7); }),T.S6.t0-.04);
/* S7: it opens */
tl.add(scr('#sc7',T.S7,(t,r)=>{ t.fromTo('#ssf',{autoAlpha:0,scale:.7,rotation:-14},{autoAlpha:1,scale:1,rotation:0,duration:.7,ease:spring,immediateRender:false},r(T.S7.open)-1.2)
  .fromTo('#ssf',{y:0},{y:-8,duration:1.4,ease:'sine.inOut',yoyo:true,repeat:2,immediateRender:false},r(T.S7.open)-.4);
  ringDraw(t,'#rgO',r(T.S7.open)+.7); [.9,1.9,2.6].forEach(a=>{ t.fromTo('#sc7 .hv',{scale:1,transformOrigin:'0% 50%'},{scale:1.1,duration:.5,yoyo:true,repeat:1,ease:'sine.inOut',immediateRender:false},r(T.S7.open)+a); t.fromTo('#ssf',{scale:1},{scale:1.22,duration:.5,yoyo:true,repeat:1,ease:'sine.inOut',immediateRender:false},r(T.S7.open)+a+.1); }); }),T.S7.t0-.04);
/* S8: the real page, a hand-drawn ring around the sentence */
tl.add(scr('#sc8',T.S8,(t,r)=>{ card(t,'#pg',.55); t.fromTo('#pg img',{scale:1,transformOrigin:'0% 100%'},{scale:1.035,duration:Math.max(1.5,T.S8.end-T.S8.t0-.4),ease:'sine.inOut',immediateRender:false},.7);
  ringDraw(t,'#rgP',Math.max(1.5,r(T.S8.ringat)+.5)); }),T.S8.t0-.04);
/* S9: the card to save, built row by row, then a slow drift */
tl.add(scr('#sc9',T.S9,(t,r)=>{ card(t,'#sv',.1,30);
  t.fromTo('#sc9 .sh:not(.pl2)',{autoAlpha:0},{autoAlpha:1,duration:.3,immediateRender:false},.35);
  t.fromTo('#sc9 .cr',{autoAlpha:0,y:20},{autoAlpha:1,y:0,duration:.45,ease:expoOut,stagger:.22,immediateRender:false},.5);
  t.fromTo('#pl2',{autoAlpha:0},{autoAlpha:1,duration:.3,immediateRender:false},Math.max(1.6,r(T.S9.plus)-.35));
  ['#ex0','#ex1','#ex2'].forEach((id,i)=>t.fromTo(id,{autoAlpha:0,y:16},{autoAlpha:1,y:0,duration:.4,ease:expoOut,immediateRender:false},Math.max(1.7,r([T.S9.plus,T.S9.act,T.S9.lic][i])-.1)));
  t.fromTo('#sp',{autoAlpha:0,scale:.8,transformOrigin:'0% 50%'},{autoAlpha:1,scale:1,duration:.6,ease:spring,immediateRender:false},r(T.S9.spots)-.1);
  t.fromTo('#sv',{scale:1,transformOrigin:'50% 40%'},{scale:1.04,duration:Math.max(1.5,T.S9.end-T.S9.t0-.2),ease:'sine.inOut',immediateRender:false},.5);
  [1.9,3.3].forEach(a=>t.fromTo('#shn',{x:-300},{x:1100,duration:1.2,ease:'sine.inOut',immediateRender:false},a));
  t.fromTo('#sc9 .cr b',{scale:1},{scale:1.14,duration:.35,yoyo:true,repeat:1,ease:'sine.inOut',stagger:.28,immediateRender:false},2.4); }),T.S9.t0-.04);
/* S10 */
tl.add(scr('#sc10',T.S10,(t,r)=>{ ringDraw(t,'#rgV',r(T.S10.val)+.25); }),T.S10.t0-.04);
/* S11-S13 */
tl.add(scr('#sc11',T.S11,(t,r)=>{ pops(t,'#m1',r(T.S11.t0)+.85,0); pops(t,'#m2',r(T.S11.t0)+1.0,0); }),T.S11.t0-.04);
tl.add(scr('#sc12',T.S12,null),T.S12.t0-.04);
tl.add(scr('#sc13',T.S13,(t,r)=>{ ringDraw(t,'#rgF',r(T.S13.acc)+.1); },{keep:true}),T.S13.t0-.04);
/* the checklist row under S4-S7: stays across the four screens, ticks at the spoken words */
tl.fromTo('.bx',{autoAlpha:0,y:24,scale:.92},{autoAlpha:1,y:0,scale:1,duration:.6,ease:spring,stagger:.06,immediateRender:false},T.S4a.t0-.04)
  .to('.bx',{autoAlpha:0,y:-10,duration:.22,ease:expoIn},T.S8.t0-.22);
function tick(i,at){ tl.to('#b'+i,{backgroundColor:ORG,borderColor:ORG,duration:.3,ease:'power2.out'},at).to('#b'+i+' b',{autoAlpha:0,duration:.2},at)
  .fromTo('#b'+i+' svg path',{drawSVG:'0%'},{drawSVG:'100%',duration:.35,ease:'power2.out',immediateRender:false},at+.06)
  .fromTo('#b'+i,{scale:.9},{scale:1,duration:.5,ease:spring,immediateRender:false},at); }
tick(0,T.S4a.tick1-.1); tick(1,T.S4b.tick2-.1); tick(2,T.S5a.tick3-.1); tick(3,T.S5b.tick4-.1); tick(4,T.S7.open+.1);
tl.fromTo('#b4 b',{y:0},{y:-6,duration:.5,yoyo:true,repeat:Math.floor((T.S7.t0-T.S6.t0)/.5)-1,ease:'sine.inOut'},T.S6.t0);
/* the frame-0 look returns for the loop */
tl.add(hide('#sc13'),T.tF-.24).set('#sc1',{autoAlpha:0},T.tF-.3).fromTo('#sc1',{autoAlpha:0,filter:'blur(6px)'},{autoAlpha:1,filter:'blur(0px)',duration:.36,ease:'power2.out',immediateRender:false},T.tF-.02).to({},{duration:.001},T.D-.001);
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
<div class="bgw" data-decor></div><div id="cam">{scenes}<div id="rowB">{rowB}</div></div>
</div>
<script>
{JS}
</script></body></html>'''
os.makedirs(H_ + "/out", exist_ok=True)
open(H_ + "/hf/index.html", "w").write(html)
say(f"ep105 build D={D} sfx={len(SFX)}")
say("screens: " + "  ".join(f"{k}:{v['t0']:.2f}-{v['end']:.2f}" for k, v in T.items() if isinstance(v, dict) and 't0' in v))
open(H_ + "/out/build105.log", "w").write("\n".join(LOG) + "\n")
