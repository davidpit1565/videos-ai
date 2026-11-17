#!/usr/bin/env python3
"""ep89c 'This prompt has been going viral' - Miki style (light dotted-grid page, heavy black type word by word,
typed dark prompt card, black tag, blurred answers, one hard black wipe, orange only on SCARY / GO).
Picture follows the narration: video/ep89b/voice/narration-fast.wav (do not touch). Writes hf/index.html, cues89c.json, sfx89c.json."""
import json, os, random, math
H_ = os.path.dirname(os.path.abspath(__file__))
V = "/home/user/videos-ai/video/ep89b/voice"
cues = json.load(open(V + "/cues-fast.json"))
WD = {int(k): v for k, v in json.load(open(H_ + "/voice/words.json")).items()}
# ---- new hook take (m1: exaggeration 0.60, seed 3101, rendered at 1.0 speed) replaces line 1; the rest is the original narration, shifted
import soundfile as sf_, numpy as np_
L1_RAW_ONSET, L1_END_RAW = 0.34, 2.04           # seconds in voice/m1-t1.wav (energy envelope)
L1_WORDS = [["This", .10, .34], ["prompt", .36, .60], ["has", .64, .74], ["been", .76, .90], ["going", .92, 1.20], ["viral.", 1.26, 1.80]]   # final timeline, onset moved to 0.10 s
E1 = 1.80
SHIFT = round((E1 + .05) - 1.95, 3)             # everything after original 1.95 s moves by this
S = lambda t: round(t + SHIFT, 3) if t > 1.95 else t
lines = [dict(n=c["n"], text=c["line"], start=S(c["start"]), end=S(c["end"])) for c in cues]
lines[0]["start"] = 0.07; lines[0]["end"] = E1
lines[3]["start"] = round(lines[3]["start"] + .05, 3)   # measurement window only: pyin octave-jumps on the exact start; see script file
for n_ in WD:
    if n_ == 1: WD[1] = [list(w_) for w_ in L1_WORDS]
    else:
        for w_ in WD[n_]: w_[1] = S(w_[1] + .08); w_[2] = S(w_[2] + .08)
W = lambda n, i: WD[n][i][1]
TL_ = round(WD[7][3][1] + 2.0, 3)               # GO holds >= 1.5 s with its ring after it has fully arrived, then the loop dissolve
D = round(TL_ + .75, 2)
json.dump(dict(lines=lines, D=D), open(H_ + "/cues89c.json", "w"), indent=1)
o_, sr_ = sf_.read(V + "/narration-fast.wav"); o_ = o_ if o_.ndim == 1 else o_[:, 0]
n_, _ = sf_.read(H_ + "/voice/m1-t1.wav"); n_ = n_ if n_.ndim == 1 else n_[:, 0]
a0 = int((L1_RAW_ONSET - .10) * sr_)
new1 = n_[a0:a0 + int((E1 + .05) * sr_)].copy()
act = lambda x: x[int(.10 * sr_):int(E1 * sr_)]
g_ = np_.sqrt((act(o_[:int(1.95 * sr_)]) ** 2).mean()) / np_.sqrt((act(new1) ** 2).mean())
new1 *= g_
fo = int(.02 * sr_); new1[-fo:] *= np_.linspace(1, 0, fo)
tail = o_[int(1.95 * sr_):]
sf_.write(H_ + "/out/narration89c.wav", np_.concatenate([new1, tail, np_.zeros(int(D * sr_))])[:int(D * sr_)], sr_, subtype="PCM_16")
print("line1 gain", round(float(20 * np_.log10(g_)), 2), "dB; shift", SHIFT, "D", D)

WE = lambda n, i: WD[n][i][2]
INK, ORG = "#0f0f0f", "#D97757"

J = []; SFX = []
def js(s): J.append(s)
def sfx(f, t, g=-6): SFX.append((f, round(t, 3), g))
def T(t): return f"{max(0.0, t):.3f}"

# ---------------------------------------------------------------- markup helpers
def words(prefix, items):
    """items: [(text, cls)] -> inline-block word spans with ids prefix0.."""
    return "".join(f'<span class="w {c}" id="{prefix}{i}">{t}</span>' for i, (t, c) in enumerate(items))

def typed(prefix, text, ku=()):
    out = []; k = 0
    for wi, w in enumerate(text.split(" ")):
        ls = "".join(f'<span class="L" id="{prefix}{k + j}">{ch}</span>' for j, ch in enumerate(w))
        out.append(f'<span class="tw{" ku" if wi in ku else ""}" id="{prefix}w{wi}">{ls}</span>'); k += len(w)
    return "".join(out)

def comp(cid, prefix, text, top, h, extra="", ku=()):
    logo = '<img class="chlogo" src="assets/openai.svg">'
    plus = '<svg viewBox="0 0 40 40" width="52" height="52"><path d="M20 8v24M8 20h24" stroke="#d8d8dc" stroke-width="4.5" stroke-linecap="round"/></svg>'
    arrow = '<svg viewBox="0 0 40 40" width="46" height="46"><path d="M20 31V10M11 18l9-9 9 9" fill="none" stroke="#111" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return (f'<div class="comp" id="{cid}" style="top:{top}px;height:{h}px"><div class="chd">{logo}</div>'
            f'<div class="txt" id="{cid}t">{typed(prefix, text, ku)}</div>{extra}'
            f'<div class="cbt"><div class="plus">{plus}</div><div class="send" id="{cid}s">{arrow}</div></div></div>')

def blobs(seed, rows, widths=(70, 150)):
    r = random.Random(seed); out = []
    for ri in range(rows):
        if ri == 0:
            out.append('<div class="row"><i style="width:360px;height:34px"></i></div>'); continue
        if ri % 4 == 0: out.append('<div class="row sp"></div>'); continue
        x = 0; items = []
        limit = r.choice((780, 830, 860, 600))
        while x < limit:
            w = r.randint(*widths); items.append(f'<i style="width:{w}px"></i>'); x += w + 18
        out.append('<div class="row">' + "".join(items) + '</div>')
    return "".join(out)

def ans(aid, top, h, seed, rows):
    logo = '<img class="chlogo" src="assets/openai.svg">'
    dots = '<div class="dots"><b></b><b></b><b></b></div>'
    return (f'<div class="ans" id="{aid}" style="top:{top}px;height:{h}px"><div class="chd">{logo}{dots}</div>'
            f'<div class="rows" id="{aid}r">{blobs(seed, rows)}</div></div>')

P1 = "What do you know about me that I might not know about myself, based on our previous interactions?"
P2 = "Based on everything you know about me, create me 5 questions to my future self."
badge = '<div class="badge" id="bdg"><img src="assets/openai.svg"></div>'
tagB = '<div class="tag" id="tag1">PROMPT 1</div>'
tagE = '<div class="tag" id="tag2">PROMPT 2</div>'
curve = lambda i, d: (f'<svg class="curve" id="cv{i}" viewBox="0 0 1080 1920"><mask id="m{i}"><path id="mp{i}" d="{d}" pathLength="1" stroke="#fff" stroke-width="16" fill="none" stroke-dasharray="1 1" stroke-dashoffset="1"/></mask>'
                      f'<path d="{d}" stroke="{INK}" stroke-width="5" fill="none" stroke-dasharray="4 16" stroke-linecap="round" mask="url(#m{i})"/></svg>')

scr = lambda i, d, w=12, col=INK: (f'<svg class="scr" id="sc{i}" viewBox="0 0 1000 300" preserveAspectRatio="none"><path id="sp{i}" d="{d}" pathLength="1" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')

markup = f'''
<div class="bgw" data-decor></div>
<div class="scene" id="sA">{badge}
 <div class="hk h1" id="hA1"><span class="v" id="aT">THIS</span> <span class="v" id="aP">PROMPT</span></div>
 <div class="hk h2" id="hA2"><span class="w l" id="aL0">has</span> <span class="w l" id="aL1">been</span> <span class="w l" id="aL2">going</span> <span class="w hv" id="aV">VIRAL.</span></div>
 <svg class="ul" id="ulA" viewBox="0 0 520 60" preserveAspectRatio="none"><path id="ulAp" d="M6 36 C 90 14, 170 50, 260 28 S 430 14, 514 30" pathLength="1" stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round" stroke-dasharray="1 1" stroke-dashoffset="1"/></svg>
</div>
{tagB}{curve(1, "M 372 340 C 470 296 600 318 650 404")}
{comp("card", "a", P1, 770, 470, '<div class="blA" id="blA"></div>', (12,))}
<div class="scene" id="sC"><div class="hk c1">{words("c1_", [("When", "l"), ("the", "l"), ("response", "l"), ("comes", "l"), ("back,", "l")])}</div>
 <div class="hk c2">{words("c2_", [("IT", "hv"), ("TAKES", "hv"), ("A", "hv"), ("WHILE", "hv")])}</div>
 <div class="hk c3">{words("c3_", [("TO", "hv"), ("<span class=sel id=selC>PROCESS.</span>", "hv")])}</div></div>
{ans("ansC", 650, 590, 11, 12)}
<div class="scene" id="sD"><div class="hk d1">{words("d1_", [("But", "l"), ("here's", "l"), ("where", "l"), ("it", "l"), ("gets", "l")])}</div>
 <div class="hk d2">{words("d2_", [("EVEN", "hv"), ("MORE", "hv")])}</div>
 <div class="hk d3"><span class="w hv org" id="d3_0">SCARY.</span></div>
 {scr("D", "M 40 150 C 20 40, 300 -2, 520 6 C 800 12, 990 60, 975 170 C 960 280, 640 300, 470 296 C 220 292, 28 270, 30 140 C 32 70, 120 40, 200 30", 11, ORG)}</div>
{tagE}{curve(2, "M 372 340 C 470 296 600 318 650 404")}
{comp("card2", "b", P2, 410, 820, "", (10,))}
<div class="badge big" id="bdg2"><img src="assets/openai.svg"></div>
<div class="scene" id="sF"><div class="hk c1">{words("f1_", [("Fair", "l"), ("warning,", "l"), ("the", "l"), ("responses", "l")])}</div>
 <div class="hk c2">{words("f2_", [("CAN", "hv"), ("SHAKE", "hv"), ("YOU", "hv")])}</div>
 <div class="hk c3">{words("f3_", [("<span class=sel id=selF>A BIT.</span>", "hv")])}</div></div>
{ans("ansF", 650, 590, 29, 12)}
<div class="scene" id="sG"><div class="hk g1">{words("g1_", [("TEST", "hv"), ("IT", "hv")])}</div><div class="hk g2"><span class="w hv" id="g2_0">OUT.</span></div>
 <div class="hk g3"><span class="w hv org" id="g3_0">GO.</span></div>
 {scr("G", "M 30 170 C 10 50, 330 4, 520 8 C 790 12, 985 70, 965 170 C 945 270, 640 296, 450 292 C 200 288, 30 262, 38 150 C 44 80, 130 44, 230 34", 12, ORG)}</div>
'''

# zig-zag band path for the one hard wipe (spiky leading + trailing edge)
def band():
    pts = []; Hh = 2800; n = 30; step = Hh / n
    for i in range(n + 1):  # leading edge (left), spikes
        pts.append((0 if i % 2 else 170, i * step))
    for i in range(n, -1, -1):  # trailing edge (right)
        pts.append((3200 if i % 2 else 3030, i * step))
    return "M " + " L ".join(f"{x:.0f} {y:.0f}" for x, y in pts) + " Z"
markup = markup.replace("{WP}", band())

css = f'''
.bgw{{position:absolute;left:0;top:0;width:1080px;height:2000px;background-repeat:repeat-y;background:#ecebe5 url(assets/bg.jpg);background-size:1080px 1920px}}
.scene{{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0}}
#sA{{opacity:1}}
.hk{{position:absolute;left:65px;width:950px;color:{INK};white-space:nowrap}}
.w,.v{{display:inline-block}} .w{{opacity:0}} #hA2 .w{{opacity:.14}}
.hv,.h1,.h2 .hv,.d2,.d3,.g1,.g2,.g3{{font-weight:900;letter-spacing:-.045em}}
.l{{font-weight:500;letter-spacing:-.02em}}
.h1{{top:440px;font-size:148px;line-height:164px;font-weight:900;letter-spacing:-.045em}}
.h2{{top:602px;font-size:56px;line-height:170px;display:flex;align-items:baseline;gap:16px}} #aV{{margin-left:14px}}
.h2 .hv{{font-size:140px;letter-spacing:-.045em}}
.org{{color:{ORG}}}
.badge{{position:absolute;left:65px;top:300px;width:128px;height:128px;border-radius:30px;background:#fff;border:4px solid {INK};display:flex;align-items:center;justify-content:center;box-shadow:7px 7px 0 {INK}}}
.badge img{{width:66%;height:66%}}
.badge.big{{left:370px;top:560px;width:340px;height:340px;border-radius:70px;box-shadow:14px 14px 0 {INK};border-width:7px;opacity:0;z-index:50}}
.ul{{position:absolute;left:480px;top:722px;width:520px;height:44px}}
.comp{{position:absolute;left:80px;width:920px;background:#17181b;border-radius:40px;box-shadow:0 26px 50px rgba(20,20,20,.28),0 3px 0 #000;border:2px solid #2b2c32;z-index:20;font-weight:500}}
.chd{{position:absolute;left:44px;top:36px;height:70px;display:flex;align-items:center;gap:22px}}
.chlogo{{height:62px;width:62px;filter:invert(1)}}
.txt{{position:absolute;left:48px;right:48px;top:136px;font-size:72px;line-height:96px;color:#f2f2ee;letter-spacing:-.015em}}
.tw{{display:inline-block;white-space:nowrap;margin-right:.26em}}
.ku{{position:relative}}.ku::after{{content:'';position:absolute;left:-6px;right:-12px;bottom:-16px;height:22px;transform-origin:0 50%;transform:scaleX(var(--u,0));background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 22' preserveAspectRatio='none'><path d='M4 14 C 40 4, 70 20, 110 11 S 170 6, 196 12' stroke='%23f2f2ee' stroke-width='6' fill='none' stroke-linecap='round'/></svg>") no-repeat;background-size:100% 100%}}.L{{opacity:0;position:relative;display:inline-block}}
.L::after{{content:"";position:absolute;right:-9px;top:.14em;width:6px;height:.78em;background:#fff;opacity:var(--cur,0)}}
.blA{{position:absolute;left:48px;top:150px;width:6px;height:70px;background:#fff}}
.cbt{{position:absolute;left:44px;right:44px;bottom:36px;height:88px;display:flex;align-items:center;justify-content:space-between}}
.plus{{width:88px;height:88px;border-radius:50%;border:3px solid #3a3b42;display:flex;align-items:center;justify-content:center}}
.send{{width:88px;height:88px;border-radius:50%;background:#5c5d63;display:flex;align-items:center;justify-content:center}}
.tag{{position:absolute;left:80px;top:296px;height:84px;padding:0 34px;background:#0b0b0b;color:#fff;font-family:JBM,monospace;font-weight:700;font-size:42px;letter-spacing:.04em;display:flex;align-items:center;border-radius:8px;z-index:30;opacity:0}}
.curve{{position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:25;opacity:0;pointer-events:none}}
.ans{{position:absolute;left:80px;width:920px;background:#17181b;border-radius:40px;box-shadow:0 26px 50px rgba(20,20,20,.28),0 3px 0 #000;border:2px solid #2b2c32;z-index:20;opacity:0;overflow:hidden}}
.dots{{display:flex;gap:14px;align-items:center;margin-left:8px}}.dots b{{display:block;width:20px;height:20px;border-radius:50%;background:#f2f2ee;opacity:.35}}
.rows{{position:absolute;left:48px;right:48px;top:136px;filter:blur(9px);}}
.row{{display:flex;gap:18px;height:38px;margin-bottom:20px;opacity:0}}.row i{{display:block;height:26px;margin-top:6px;border-radius:13px;background:#dcdce0}}.row.sp{{height:20px;margin-bottom:0}}
.c1{{top:300px;font-size:60px;line-height:76px}} .c2{{top:376px;font-size:104px;line-height:116px}} .c3{{top:492px;font-size:104px;line-height:116px}}
.c1 .w{{font-weight:500;letter-spacing:-.02em;margin-right:16px}} .c2 .w,.c3 .w{{margin-right:24px;letter-spacing:-.045em}}
.sel{{position:relative;isolation:isolate;display:inline-block}}
.sel::before{{content:"";position:absolute;left:-14px;right:-10px;top:6px;bottom:2px;background:#0b0b0b;transform-origin:0 50%;transform:scaleX(var(--s,0));z-index:-1}}
.d1{{top:420px;font-size:78px;line-height:96px}} .d1 .w{{font-weight:500;letter-spacing:-.02em;margin-right:16px}}
.d2{{top:530px;font-size:162px;line-height:172px}} .d2 .w{{margin-right:30px}}
.d3{{top:720px;font-size:226px;line-height:250px}}
.scr{{position:absolute;left:40px;width:1000px;height:300px;pointer-events:none;opacity:0}}
#scD{{top:700px;left:60px;width:960px;height:320px}} #scG{{top:880px}}
.g1{{top:330px;font-size:180px;line-height:196px}} .g1 .w{{margin-right:34px}} .g2{{top:535px;font-size:180px;line-height:196px}} .g3{{top:760px;font-size:430px;line-height:440px}}
'''

# ---------------------------------------------------------------- timeline
SIDE = lambda sel, t, d=.28: js(f"tl.to('{sel}',{{opacity:0,filter:'blur(16px)',duration:{d},ease:'power1.in'}},{T(t)});")
SIDEIN = lambda sel, t, d=.3: js(f"tl.fromTo('{sel}',{{opacity:0,filter:'blur(16px)'}},{{opacity:1,filter:'blur(0px)',duration:{d},ease:'power2.out',immediateRender:false}},{T(t)});")
def wordin(i, t, dy=46, d=.2):
    js(f"tl.fromTo('#{i}',{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{d},ease:'power2.out',immediateRender:false}},{T(t)});")
def draw(mid, t, d=.45, ease='power2.inOut'):
    js(f"tl.to('#{mid}',{{strokeDashoffset:0,duration:{d},ease:'{ease}'}},{T(t)});")
def typeline(prefix, text, line, w0, clickg=-11):
    """letters appear spread over each spoken word; cursor follows; returns letter times"""
    words_ = text.split(" "); k = 0; prev = None; tt = []
    for wi, w in enumerate(words_):
        ws, we = WD[line][w0 + wi][1], WD[line][w0 + wi][2]
        n = len(w)
        for j in range(n):
            t = ws + (we - ws) * 0.9 * j / max(1, n)
            tt.append((f"{prefix}{k + j}", round(t, 3)))
        k += n
    for idx, (i, t) in enumerate(tt):
        cur = f"'--cur':0" if False else ""
        js(f"tl.fromTo('#{i}',{{opacity:0,y:10,scale:.8}},{{opacity:1,y:0,scale:1,duration:.09,ease:'power2.out',immediateRender:false}},{T(t)});")
        js(f"tl.set('#{i}',{{'--cur':1}},{T(t)});")
        if idx: js(f"tl.set('#{tt[idx - 1][0]}',{{'--cur':0}},{T(t)});")
        sfx("click_a.ogg" if idx % 2 == 0 else "click_b.ogg", t, clickg if idx % 3 else clickg + 3)
    return tt

js("gsap.set('#bdg2',{opacity:0});")
js(f"tl.fromTo('.bgw',{{y:0}},{{y:-70,duration:{D/2},ease:'sine.inOut',yoyo:true,repeat:1}},0);")
# --- A: frame 0 = logo + THIS PROMPT + card with fast cursor; ghost words of the rest; punch-ins every ~0.4 s
js(f"tl.fromTo('#blA',{{opacity:1}},{{opacity:0,duration:.2,ease:'sine.inOut',repeat:{int((tB_ := S(2.0) - .12) / .2)},yoyo:True}},0);".replace("True","true"))
js(f"tl.fromTo('#aT',{{scale:1}},{{scale:1.04,duration:.16,ease:'power2.out',yoyo:true,repeat:1,transformOrigin:'50% 70%'}},0.10);")
js(f"tl.fromTo('#aP',{{scale:1}},{{scale:1.04,duration:.16,ease:'power2.out',yoyo:true,repeat:1,transformOrigin:'50% 70%'}},{T(W(1, 1))});")
js("tl.fromTo('#bdg',{rotation:-14,scale:.86,y:10},{rotation:-3,scale:1,y:0,duration:.4,ease:'power3.out'},0);")
js("tl.to('#bdg',{rotation:3,duration:1.5,ease:'sine.inOut'},.4);")
js("tl.fromTo('#card',{scale:.95,y:26},{scale:1,y:-10,duration:.45,ease:'expo.out',transformOrigin:'50% 50%'},0);")
js(f"tl.fromTo('#sA',{{scale:1}},{{scale:1.02,duration:{tB_:.2f},ease:'sine.inOut',transformOrigin:'50% 40%'}},0);")
def gword(i, t, dy):
    js(f"tl.fromTo('#{i}',{{opacity:.14,y:{dy}}},{{opacity:1,y:0,duration:.2,ease:'power2.out',immediateRender:false}},{T(t)});")
for i, k in enumerate((2, 3, 4)): gword(f"aL{i}", W(1, k) - .03, 24)
js(f"tl.fromTo('#aV',{{opacity:.14,y:12}},{{opacity:1,y:0,duration:.5,ease:'sine.inOut',immediateRender:false}},{T(W(1, 5) - .24)});")
draw("ulAp", W(1, 5) + .1, .55, 'sine.inOut')
sfx("impactpunch.ogg", 0.10, -6); sfx("pop_a.ogg", W(1, 1), -6); sfx("tick.ogg", W(1, 2), -8); sfx("tick.ogg", W(1, 3), -8); sfx("tick.ogg", W(1, 4), -8)
sfx("tick.ogg", W(1, 5) - .02, -13); sfx("whoosh_c.ogg", 0.0, -12)

# --- B: prompt 1 typed live into the card (card grows from the frame-0 size to the big one)
tB = S(2.0) - .12
SIDE("#sA", tB, .26)
js(f"tl.to('#card',{{top:410,height:830,duration:.55,ease:'expo.inOut'}},{T(tB)});")
js(f"tl.set('#blA',{{opacity:0}},{T(tB + .2)});")
js(f"tl.fromTo('#tag1',{{opacity:0,x:-12,rotation:-4}},{{opacity:1,x:0,rotation:-1.5,duration:.3,ease:'power3.out',immediateRender:false}},{T(tB + .12)});")
js(f"tl.set('#cv1',{{opacity:1}},{T(tB + .15)});"); draw("mp1", tB + .18, .5)
sfx("whoosh_b.ogg", tB - .02, -13); sfx("pop_b.ogg", tB + .14, -5); sfx("select.ogg", tB + .22, -9); sfx("tick.ogg", tB + .6, -8)
tt = typeline("a", P1, 2, 0)
js(f"tl.fromTo('#aw12',{{'--u':0}},{{'--u':1,duration:.4,ease:'power2.inOut',immediateRender:false}},{T(WE(2, 12) - .05)});"); sfx("select.ogg", WE(2, 12), -8)
for kk in (12,): js(f"tl.fromTo('#card',{{scale:1.03}},{{scale:1.045,duration:.2,ease:'power2.out',yoyo:true,repeat:1,transformOrigin:'50% 40%'}},{T(WE(2, kk))});")
tsend = S(6.12)
js(f"tl.to('#card',{{y:-22,scale:1.035,duration:4.4,ease:'sine.inOut',transformOrigin:'50% 40%'}},{T(tB + .5)});")
# a hand-drawn bar under 'might not know about myself' (black selection bar behind it is too heavy on a dark card): white underline
js(f"tl.to('#cards',{{background:'#f4f4f0',duration:.18,ease:'power2.out'}},{T(tsend - .2)});")
js(f"tl.fromTo('#cards',{{scale:1}},{{scale:1.18,duration:.16,ease:'power2.out',yoyo:true,repeat:1}},{T(tsend)});")
sfx("ding.ogg", tsend, -8); sfx("pop_a.ogg", tsend + .02, -5)

# --- C: answer arrives blurred, headline words in the voice rhythm
tC = S(6.34)
js(f"tl.to('#card,#tag1,#cv1',{{opacity:0,filter:'blur(16px)',y:-30,duration:.26,ease:'power1.in'}},{T(tC)});")
js(f"tl.set('#card',{{top:770,height:470}},{T(tC + .35)});")
for i in range(len(tt)): pass
js("tl.set('.comp .L',{opacity:0,'--cur':0},%s);" % T(tC + .3))
js("tl.set('#aw12,#bw10',{'--u':0},%s);" % T(tC + .3))
js(f"tl.set('#blA',{{opacity:1}},{T(tC + .31)});")
js(f"tl.fromTo('#sC',{{opacity:0}},{{opacity:1,duration:.2,ease:'power2.out',immediateRender:false}},{T(tC + .1)});")
js(f"tl.fromTo('#ansC',{{opacity:0,y:60,filter:'blur(14px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:.4,ease:'power3.out',immediateRender:false}},{T(tC + .12)});")
for i, k in enumerate(range(0, 5)): wordin(f"c1_{i}", W(3, k) - .03, 30, .18)
for i, k in enumerate((5, 6, 7, 8)): wordin(f"c2_{i}", W(3, k) - .03, 50, .2)
wordin("c3_0", W(3, 9) - .03, 50, .2); wordin("c3_1", W(3, 10) - .03, 50, .2)
# typing dots, then blurred rows load line by line
dots = S(6.5)
js(f"tl.fromTo('#ansC .dots b',{{opacity:.3,y:0}},{{opacity:1,y:-8,duration:.22,ease:'sine.inOut',yoyo:true,repeat:5,stagger:.12}},{T(dots)});")
rows_t = S(7.12)
for r in range(12):
    t = rows_t + r * 0.14
    js(f"tl.fromTo('#ansCr .row:nth-child({r + 1})',{{opacity:0,x:-24}},{{opacity:.92,x:0,duration:.25,ease:'power2.out',immediateRender:false}},{T(t)});")
    if r % 2 == 0: sfx("tick.ogg", t, -12)
js(f"tl.to('#ansC .dots',{{opacity:0,duration:.2}},{T(rows_t)});")
js(f"tl.fromTo('#ansC',{{scale:1}},{{scale:1.02,duration:2.7,ease:'sine.inOut',transformOrigin:'50% 50%'}},{T(tC + .5)});")
js(f"tl.fromTo('#selC',{{'--s':0}},{{'--s':1,duration:.3,ease:'power2.inOut',immediateRender:false}},{T(W(3, 10) - .02)});")
js(f"tl.to('#selC',{{color:'#ffffff',duration:.2}},{T(W(3, 10) + .08)});")
for k in range(0, 5): sfx("tick.ogg", W(3, k), -10)
sfx("whoosh_c.ogg", tC - .02, -8); sfx("pop_a.ogg", tC + .2, -6); sfx("tick.ogg", dots, -8); sfx("tick.ogg", dots + .12, -8); sfx("tick.ogg", dots + .24, -8)
sfx("select.ogg", W(3, 10) - .02, -6); sfx("impactsoft.ogg", W(3, 10) + .1, -9)

# --- C -> D: quick vertical scroll (page scrolls up), no black
tW = W(4, 0) - .30; SD = .22
js(f"tl.fromTo('#sD',{{opacity:1,y:520,filter:'blur(8px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:{SD},ease:'power2.inOut',immediateRender:false}},{T(tW)});")
js(f"tl.to('#sC,#ansC',{{y:-1250,filter:'blur(10px)',duration:{SD},ease:'power2.in'}},{T(tW)});")
js(f"tl.to('#sC,#ansC',{{opacity:0,duration:{SD * .6:.3f},ease:'power1.in'}},{T(tW)});")
sfx("whoosh_c.ogg", tW - .02, -4); sfx("whoosh_b.ogg", tW, -9); sfx("impactsoft.ogg", tW + SD, -6)

# --- D: 'But here's where it gets even more SCARY.' orange on SCARY only
for i, k in enumerate(range(0, 5)): wordin(f"d1_{i}", W(4, k) - .03, 30, .18)
wordin("d2_0", W(4, 5) - .03, 60, .22); wordin("d2_1", W(4, 6) - .03, 60, .22)
tS = W(4, 7) - .06
js(f"tl.fromTo('#d3_0',{{opacity:0,scale:.82,y:16}},{{opacity:1,scale:1,y:0,duration:.34,ease:'expo.out',transformOrigin:'50% 60%',immediateRender:false}},{T(tS)});")
RA = .6   # ring: soft arrival (fade + scale .96 -> 1), then slow breathing; no stroke drawing
js(f"tl.fromTo('#scD',{{opacity:0,scale:.96}},{{opacity:1,scale:1,duration:{RA},ease:'sine.inOut',transformOrigin:'50% 50%',immediateRender:false}},{T(tS - .12)});")
js(f"tl.fromTo('#scD',{{rotation:-.5,y:0}},{{rotation:.6,y:-5,duration:1.42,ease:'sine.inOut',immediateRender:false}},{T(tS - .12)});")
js(f"tl.fromTo('#sD',{{scale:1.0}},{{scale:1.0,duration:2.6,ease:'sine.inOut'}},{T(tW + .5)});")
js(f"tl.to('#d3_0',{{rotation:-2,duration:.7,ease:'sine.inOut',yoyo:true,repeat:1}},{T(tS + .4)});")
sfx("impactpunch.ogg", tS + .02, -3); sfx("subhit.ogg", tS + .04, -5); sfx("select.ogg", tS + .16, -7)
for i, k in enumerate((0, 1, 2, 3, 4)): sfx("tick.ogg", W(4, k), -10)
sfx("pop_b.ogg", W(4, 5), -8); sfx("pop_b.ogg", W(4, 6), -8)

# --- E: prompt 2. big logo pops in, card rises, then typing
tE = tS + 1.3
SIDE("#sD", tE, .24)
js(f"tl.set('#sD',{{opacity:0}},{T(tE + .3)});")
js(f"tl.fromTo('#card2',{{top:1420,opacity:0,filter:'blur(12px)'}},{{top:410,opacity:1,filter:'blur(0px)',duration:.6,ease:'expo.out',immediateRender:false}},{T(tE + .12)});")
js("gsap.set('#card2',{opacity:0});")
js(f"tl.fromTo('#tag2',{{opacity:0,x:-12,rotation:-4}},{{opacity:1,x:0,rotation:-1.5,duration:.3,ease:'power3.out',immediateRender:false}},{T(tE + .34)});")
js(f"tl.set('#cv2',{{opacity:1}},{T(tE + .38)});"); draw("mp2", tE + .4, .5)
js(f"tl.fromTo('#bdg2',{{opacity:0,scale:.3,rotation:-14}},{{opacity:1,scale:1,rotation:2,duration:.42,ease:'back.out(1.4)',transformOrigin:'50% 50%',immediateRender:false}},{T(tE + .3)});")
t_in = W(5, 5) - .22
js(f"tl.to('#bdg2',{{scale:.18,x:-300,y:-230,opacity:0,duration:.4,ease:'power2.in'}},{T(t_in)});")
js(f"tl.to('#card2',{{y:-14,duration:5.0,ease:'sine.inOut'}},{T(tE + .7)});")
js(f"tl.fromTo('#bdg2 img',{{y:0}},{{y:-10,duration:.5,ease:'sine.inOut',yoyo:true,repeat:1}},{T(tE + .8)});")
sfx("whoosh_a.ogg", tE + .06, -6); sfx("pop_a.ogg", tE + .3, -4); sfx("pop_b.ogg", tE + .36, -6); sfx("select.ogg", tE + .5, -8); sfx("subhit.ogg", tE + .34, -9)
sfx("whoosh_c.ogg", t_in, -9)
tt2 = typeline("b", P2, 5, 5)
js(f"tl.fromTo('#bw10',{{'--u':0}},{{'--u':1,duration:.4,ease:'power2.inOut',immediateRender:false}},{T(WE(5, 15) - .05)});"); sfx("select.ogg", WE(5, 15), -8)
tsend2 = S(17.12)
js(f"tl.to('#card2s',{{background:'#f4f4f0',duration:.18,ease:'power2.out'}},{T(tsend2 - .2)});")
js(f"tl.fromTo('#card2s',{{scale:1}},{{scale:1.18,duration:.16,ease:'power2.out',yoyo:true,repeat:1}},{T(tsend2)});")
sfx("ding.ogg", tsend2, -8); sfx("pop_a.ogg", tsend2 + .02, -5)

# --- F: blurred answer again + 'Fair warning ...'
tF = S(17.14)
js(f"tl.to('#card2,#tag2,#cv2',{{opacity:0,filter:'blur(16px)',y:-30,duration:.26,ease:'power1.in'}},{T(tF)});")
js(f"tl.fromTo('#sF',{{opacity:0}},{{opacity:1,duration:.2,ease:'power2.out',immediateRender:false}},{T(tF + .1)});")
js(f"tl.fromTo('#ansF',{{opacity:0,y:60,filter:'blur(14px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:.4,ease:'power3.out',immediateRender:false}},{T(tF + .12)});")
for i in range(4): wordin(f"f1_{i}", W(6, i) - .03, 30, .18)
for i, k in enumerate((4, 5, 6)): wordin(f"f2_{i}", W(6, k) - .03, 50, .2)
wordin("f3_0", W(6, 7) - .03, 50, .2)
js(f"tl.fromTo('#ansF .dots b',{{opacity:.3,y:0}},{{opacity:1,y:-8,duration:.22,ease:'sine.inOut',yoyo:true,repeat:3,stagger:.12}},{T(tF + .35)});")
rows_f = tF + .85
for r in range(12):
    t = rows_f + r * 0.1
    js(f"tl.fromTo('#ansFr .row:nth-child({r + 1})',{{opacity:0,x:-24}},{{opacity:.92,x:0,duration:.22,ease:'power2.out',immediateRender:false}},{T(t)});")
    if r % 2 == 0: sfx("tick.ogg", t, -12)
js(f"tl.to('#ansF .dots',{{opacity:0,duration:.2}},{T(rows_f)});")
js(f"tl.fromTo('#ansF',{{scale:1}},{{scale:1.02,duration:2.3,ease:'sine.inOut',transformOrigin:'50% 50%'}},{T(tF + .5)});")
js(f"tl.fromTo('#selF',{{'--s':0}},{{'--s':1,duration:.28,ease:'power2.inOut',immediateRender:false}},{T(W(6, 7) - .02)});")
js(f"tl.to('#selF',{{color:'#ffffff',duration:.2}},{T(W(6, 7) + .06)});")
for i in range(4): sfx("tick.ogg", W(6, i), -10)
sfx("whoosh_c.ogg", tF - .02, -8); sfx("pop_a.ogg", tF + .2, -6); sfx("select.ogg", W(6, 7) - .02, -6); sfx("impactsoft.ogg", W(6, 7) + .08, -9)
sfx("riser.ogg", S(17.95), -9)

# --- G: TEST IT OUT. GO.
tG = S(19.34)
SIDE("#sF", tG, .22); SIDE("#ansF", tG, .22)
js(f"tl.set('#sF,#ansF',{{opacity:0}},{T(tG + .3)});")
js(f"tl.set('#sG',{{opacity:1}},{T(tG + .02)});")
wordin("g1_0", W(7, 0) - .03, 70, .22); wordin("g1_1", W(7, 1) - .03, 70, .22); wordin("g2_0", W(7, 2) - .03, 70, .22)
tGO = W(7, 3) - .04
js(f"tl.fromTo('#g3_0',{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.34,ease:'expo.out',transformOrigin:'50% 60%',immediateRender:false}},{T(tGO)});")
js(f"tl.fromTo('#scG',{{opacity:0,scale:.96}},{{opacity:1,scale:1,duration:{RA},ease:'sine.inOut',transformOrigin:'50% 50%',immediateRender:false}},{T(tGO - .12)});")
js(f"tl.fromTo('#scG',{{rotation:-.5,y:0}},{{rotation:.6,y:-5,duration:{TL_ - tGO:.3f},ease:'sine.inOut',immediateRender:false}},{T(tGO - .12)});")
js(f"tl.fromTo('#sG',{{scale:1}},{{scale:1.0,y:-16,duration:{TL_ - tG - .3:.3f},ease:'sine.inOut',transformOrigin:'50% 50%'}},{T(tG + .2)});")
sfx("whoosh_a.ogg", tG - .02, -7)
for i, k in enumerate((0, 1, 2)): sfx("pop_b.ogg", W(7, k), -6)
sfx("impactpunch.ogg", tGO + .02, -2); sfx("subhit.ogg", tGO + .04, -4); sfx("ding.ogg", tGO + .2, -8); sfx("select.ogg", tGO + .14, -7)

# --- loop: G dissolves and frame 0 (logo, THIS PROMPT, card with cursor) comes back
tL = TL_
sfx("ding.ogg", tGO + 1.1, -12); sfx("subhit.ogg", tGO + 1.25, -13)
SIDE("#sG", tL, .3)
js(f"tl.set('#card',{{opacity:0,filter:'blur(0px)',y:26,scale:.95,top:770,height:470}},{T(tL - .02)});")
js(f"tl.set('#tag1,#cv1',{{opacity:0}},{T(tL - .02)});")
js(f"tl.set('#bdg',{{rotation:-14,scale:.86,y:10}},{T(tL - .02)});")
js(f"tl.set('#sA',{{scale:1}},{T(tL - .02)});")
js(f"tl.set('#sA',{{opacity:0}},{T(tL - .02)});")
js(f"tl.set('#hA2 .w',{{opacity:.14}},{T(tL - .02)});")
js(f"tl.set('#aL0,#aL1,#aL2,#aV',{{opacity:.14,y:0}},{T(tL - .02)});")
js(f"tl.set('#ulAp',{{strokeDashoffset:1}},{T(tL - .02)});")
js(f"tl.fromTo('#sA',{{opacity:0,filter:'blur(16px)'}},{{opacity:1,filter:'blur(0px)',duration:.5,ease:'power2.out',immediateRender:false}},{T(tL + .26)});")
js(f"tl.fromTo('#card',{{opacity:0,filter:'blur(14px)'}},{{opacity:1,filter:'blur(0px)',duration:.4,ease:'power2.out',immediateRender:false}},{T(tL + .32)});")
js(f"tl.set('#blA',{{opacity:1}},{T(tL + .5)});")
sfx("whoosh_b.ogg", tL + .2, -12); sfx("pop_a.ogg", tL + .36, -10)

JS = "\n".join(J)
json.dump([dict(f=f, t=t, g=g) for f, t, g in SFX if 0 <= t < D], open(H_ + "/sfx89c.json", "w"), indent=1)
html = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Black.otf");font-weight:900}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-ExtraBold.otf");font-weight:800}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Medium.otf");font-weight:500}}
@font-face{{font-family:"JBM";src:url("assets/fonts/JetBrainsMono-Bold.ttf");font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;font-weight:500;color:{INK}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}}
{css}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
{markup}
</div>
<script>
const C={json.dumps(dict(lines=lines, D=D))}; const D={D}; window.__cues=C; window.__CUES=C;
const tl=gsap.timeline({{paused:true}});
{JS}
tl.to({{}},{{duration:.001}},D-.001);
window.__timelines=window.__timelines||{{}}; window.__timelines["main"]=tl; tl.seek(0);
window.__reel={{duration:D,seek:t=>tl.seek(t)}};
</script></body></html>'''
open(H_ + "/hf/index.html", "w").write(html)
print("D=", D, "sfx", len(SFX), "js", len(J))
