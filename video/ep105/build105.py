#!/usr/bin/env python3
"""ep101 (internal 102) v4: Miki style (channel/miki-style-checklist-2026-11-16.md) built with the GSAP + motion skills
(.claude/skills/gsap-core, gsap-timeline, gsap-plugins, gsap-utils, gsap-performance, motion-animation-principles,
motion-kinetic-typography, motion-remotion-notes; model: video/demo-skills/hf/index.html).

What the skills changed against v3 (build102v3.py emitted ~180 absolute tl.fromTo lines):
  - every screen is its own function that returns a timeline with LABELS; inside a screen tweens are placed with the
    position parameter ('swap+=0.16', '<0.06'); the master timeline only places screens at the voice times (gsap-timeline)
  - one house curve: CustomEase expoOut 0.16,1,0.3,1 for enters, expoIn for exits (faster than the enter), inOut for
    moves that stay on screen, and a critically damped spring (no overshoot) for things that land (motion principles, Remotion note 1)
  - type is SET, not faded: words rise out of a mask at the moment they are spoken; the one accent word per screen is
    split into characters with SplitText masks and a 30 ms stagger; the ring is drawn along its path with DrawSVG
  - stagger and overlap: the six price tags flip to a tick one by one (90 ms, reading order), list rows 70 ms,
    attached parts settle 60-120 ms after the body (follow-through); never more than about a third of a screen moving
  - only transform / opacity / filter are animated, will-change only on what moves (gsap-performance); gsap.utils.selector
    and toArray keep selectors scoped to a screen (gsap-utils)
Still Miki: ONE idea per screen, words-only screens alternate with ONE card of real material, no counters, stamps,
totals, source lines, offset shadows, back/elastic/bounce eases.

Reads   voice/lines5.txt (11 lines), voice/narration-v5-cues.json, voice/words-v5.json (else ESTIMATED; SHIP=1 refuses).
Writes  hf/index.html, cues105.json, sfx103.json, out/build105.log.
Screens: A the cube: six real paid logos, each with a price tag that flips to a tick (line 1)   B tease (2)
         C five fast pairs on one card (3-5)   D the big one: words, card, real screenshot, "7 MONTHS OLD" (6-8)
         F the list card with "Not tested by us" (9)   G link in bio, follow (10-11)
Safe area: text inside x 108-972, y 269-1248; below y 1056 nothing to read right of x 864.
"""
import json, os, re, sys
H_ = os.path.dirname(os.path.abspath(__file__))
INK = "#0f0f0f"; ORG = "#D97757"; CARD = "#17181b"
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
LOG = []
def say(x): LOG.append(x); print(x)

LINES = [l.strip() for l in open(H_ + "/voice/lines.txt") if l.strip()]
NL = len(LINES); assert NL == 12, "ep105 is laid out for 12 lines"
try: C = json.load(open(H_ + "/voice/narration-cues.json"))
except Exception: C = []
CUE = {c["n"]: c for c in C if "n" in c}
STALE = os.environ.get("EST") == "1" or len(CUE) != NL or any(n not in CUE or norm(CUE[n]["line"]) != norm(LINES[n - 1]) for n in range(1, NL + 1))
WORDS = []
if not STALE:
    try: WORDS = [[w["word"], w["start"], w["end"]] for w in json.load(open(H_ + "/voice/words.json"))]
    except Exception: WORDS = []
if STALE:
    L = {}; t = .06
    for n in range(1, NL + 1):
        d = round(.35 + .05 * len(LINES[n - 1]), 2); L[n] = (round(t, 2), round(t + d, 2)); t += d + .1
else:
    L = {n: (float(CUE[n]["start"]), float(CUE[n]["end"])) for n in range(1, NL + 1)}
s = lambda n: L[n][0]
e = lambda n: L[n][1]
SRC = {}
def W(name, word, n, frac, k=0, log=True):
    c = 0
    for w, a_, b_ in WORDS:
        if s(n) - .12 <= a_ <= e(n) + .12 and norm(w) in (word if isinstance(word, tuple) else (word,)):
            if c == k:
                if log: SRC[name] = f"{a_:.2f}(w)"
                return round(a_, 3)
            c += 1
    t = round(s(n) + frac * (e(n) - s(n)), 3)
    if log: SRC[name] = f"{t:.2f}(EST)"
    return t
D = round(e(NL) + .78, 2)
tF = round(D - .45, 3)
a = {n: s(n) for n in range(1, NL + 1)}

# ---------------------------------------------------------------- words: masked, each with its spoken time
def line(cls, txt, n, fr0, fr1, top, size, acc=(), ready=False):
    ws = txt.split(); out = []
    for i, w in enumerate(ws):
        t = W("", norm(w), n, fr0 + (fr1 - fr0) * (i / (len(ws) - 1) if len(ws) > 1 else 0), log=False)
        ac = norm(w) in acc
        out.append(f'<span class="m"><span class="w{" acc" if ac else ""}{" rdy" if ready else ""}" data-t="{t:.3f}">{w}</span></span>')
    return f'<div class="ln {cls}" style="top:{top}px;font-size:{size}px;line-height:{round(size * 1.12)}px">{"".join(out)}</div>'
ring = lambda id_, left, top, w, h: (f'<svg class="ring" id="{id_}" viewBox="0 0 400 160" preserveAspectRatio="none" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px" data-decor>'
                                     f'<path d="M14 84 C6 30 130 8 214 10 C318 12 394 40 388 84 C382 132 270 150 190 148 C96 146 20 132 14 84 Z" fill="none" stroke="{ORG}" stroke-width="5" vector-effect="non-scaling-stroke" stroke-linecap="round"/></svg>')
lg = lambda f, h, st="": f'<img class="lg" src="assets/logos/{f}" style="width:{h}px;height:{h}px;{st}">'
TAG = f'<svg class="tag" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="{CARD}"/><path d="M30 34 H56 L74 52 L54 72 L30 48 Z" fill="none" stroke="#f2f2ee" stroke-width="7" stroke-linejoin="round"/><circle cx="41" cy="45" r="5" fill="#f2f2ee"/></svg>'
TICK = f'<svg class="tick" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="{ORG}"/><path d="M29 52 L44 67 L72 35" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARW = '<svg class="arw" viewBox="0 0 60 90"><path d="M30 6 V78 M8 54 L30 78 L52 54" fill="none" stroke="#f2f2ee" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>'

SC = {}; T = {}


# ================================================================ ep104 scenes (Replica skill)
SKILLS = ["RECON", "ARCHITECT", "DESIGN", "BUILD", "BACKEND", "TEST", "DIFF", "ENTREPRENEUR", "BRAND", "LAUNCH", "DEPLOY"]
def ext(inner, cls="", layers=9, step=3, col="#b9b6ab"):
    lay = "".join(f'<div class="lay" style="transform:translateZ({-(k + 1) * step}px);background:{col}"></div>' for k in range(layers))
    return f'<div class="t3 {cls}">{lay}<div class="face">{inner}</div></div>'
def logo_tile(f, tag=""):
    return ext(f'<img src="assets/logos/{f}" class="tl">{tag}')
def flat_tile(f):
    lay = "".join(f'<div class="lay" style="transform:translateZ({k * 4}px);background:#b9b6ab"></div>' for k in range(0, 9))
    return f'<div class="t3 flat">{lay}<div class="face" style="transform:translateZ(36px)"><img src="assets/logos/{f}" class="tl"><b class="pr"></b></div></div>'
def wf(cls=""):
    cells = "".join('<i></i>' for _ in range(20))
    return f'<div class="wf {cls}"><div class="wfh"></div><div class="wfg">{cells}</div><div class="wfb"></div><div class="wfb s"></div><div class="wfk">BOOK</div></div>'
def mark3d(n=14, step=4):
    back = "".join(f'<img class="m3b" src="assets/logos/claude.svg" style="transform:translateZ({-(k + 1) * step}px)">' for k in range(n))
    return f'<div class="m3">{back}<img class="m3f" src="assets/logos/claude.svg"></div>'

# ---- ep105 scenes (Agency Agents)
import math
RINGS = [(210, 11), (300, 17), (390, 23), (480, 29), (570, 35)]
KY = .40; CX, CY = 540, 1130
bands = "".join(f'<i class="bd" style="left:{CX - R_ - 40:.0f}px;top:{CY - (R_ + 40) * KY:.0f}px;width:{2 * (R_ + 40):.0f}px;height:{2 * (R_ + 40) * KY:.0f}px;background:{"#f7f6f1" if k % 2 == 0 else "#e8e6dd"}"></i>' for k, (R_, n_) in reversed(list(enumerate(RINGS))))
figs = []
for ri, (r_, n_) in enumerate(RINGS):
    for j in range(n_):
        th = 2 * math.pi * (j + .5 * (ri % 2)) / n_
        figs.append((CX + r_ * math.cos(th), CY + r_ * math.sin(th) * KY, .72 + .26 * (math.sin(th) + 1) / 2))
figs.sort(key=lambda f: f[1])
CROWD = ('<div id="crowd"><div id="cworld">' + bands + '<div class="ped"></div>' +
         "".join(f'<i class="fg" style="left:{x - 15:.0f}px;top:{y - 58:.0f}px;transform:scale({sc:.2f})"></i>' for x, y, sc in figs) +
         '<img class="clawd" id="clawd" src="assets/logos/clawd.png"></div><div class="freeb" id="freeb">FREE</div></div>')
ORBL = CROWD
def agent_badge(role, div):
    return f'<div class="ab"><img class="abl" src="assets/logos/clawd.png"><div><b>{role}</b><span>{div}</span></div></div>'
# S1 hook
SC["S1"] = line("lead", "Claude just got", 1, 0, .3, 286, 62, ready=True) + line("hv", "280 AI", 1, .35, .55, 364, 180, ready=True, acc=("280",)) + \
  line("hv", "SPECIALISTS.", 1, .6, .9, 574, 118, ready=True, acc=("specialists",))
T["S1"] = dict(t0=0, hit=W("free", "free", 1, .95), end=a[2])
# S2 company
SC["S2"] = line("lead", "It's like a", 2, 0, .15, 292, 62) + line("hv", "WHOLE COMPANY", 2, .3, .7, 352, 98, acc=("whole", "company")) + line("lead", "living inside Claude.", 2, .75, 1, 492, 62)
T["S2"] = dict(t0=a[2], end=a[3])
# S3 the real repo page
SC["S3"] = line("lead", "It's called", 3, 0, .2, 292, 62) + line("hv", "AGENCY AGENTS.", 3, .25, .5, 352, 100, acc=("agency", "agents")) + \
  '<div class="shot rh3" id="rh"><img src="assets/shots/repohead.png"></div>' + ring("rgS", 800, 520, 176, 80) + '<div class="shot ab3" id="ab"><img src="assets/shots/about.png"></div>'
T["S3"] = dict(t0=a[3], stars=W("stars", "stars", 3, .85), end=a[4])
# S4 cold emails
SC["S4"] = line("lead", "One writes your", 4, 0, .3, 292, 62) + line("hv", "COLD EMAILS.", 4, .5, .8, 352, 130, acc=("cold", "emails")) + \
  '<div class="wc card4" id="em"><div class="tg">EXAMPLE</div>' + agent_badge("OUTBOUND STRATEGIST", "SALES") + \
  '<div class="mail"><div class="mrow"><i>TO</i><u id="m1">alex@acme.com</u></div><div class="mrow"><i>SUBJECT</i><u id="m2">Quick idea for Acme</u></div><div class="mb"><span></span><span></span><span class="s"></span></div><div class="send" id="snd">SEND</div></div></div>'
T["S4"] = dict(t0=a[4], end=a[5])
# S5 calls and proposals
SC["S5"] = line("lead", "A sales team preps", 5, 0, .5, 292, 62) + line("hv", "YOUR CALLS.", 5, .6, 1, 352, 140, acc=("calls",)) + \
  '<div class="two5"><div class="wc card5" id="cp1"><div class="tg">EXAMPLE</div>' + agent_badge("DISCOVERY COACH", "SALES") + \
  '<div class="ck5">CALL PREP</div><div class="ckr"><i></i><b></b></div><div class="ckr"><i></i><b></b></div><div class="ckr"><i></i><b></b></div><div class="ckr"><i></i><b></b></div><div class="ckr"><i></i><b class="s"></b></div></div>' + \
  '<div class="wc card5" id="cp2"><div class="tg">EXAMPLE</div>' + agent_badge("PROPOSAL STRATEGIST", "SALES") + \
  '<div class="ck5">PROPOSAL</div><div class="doc"><span></span><span></span><span class="s"></span><span></span><span></span><span class="s"></span><span></span></div></div></div>'
T["S5"] = dict(t0=a[5], end=a[6])
# S6 dev team
SC["S6"] = line("lead", "A dev team builds", 6, 0, .4, 292, 62) + line("hv", "THE PRODUCT.", 6, .55, 1, 352, 112, acc=("product",)) + \
  '<div class="dev6" id="dv"><div class="dr" id="d0">' + agent_badge("FRONTEND DEVELOPER", "ENGINEERING") + '<i class="dk"></i></div><div class="dr" id="d1">' + agent_badge("BACKEND ARCHITECT", "ENGINEERING") + '<i class="dk"></i></div><div class="dr" id="d2">' + agent_badge("DEVOPS AUTOMATOR", "ENGINEERING") + '<i class="dk"></i></div><div class="live6" id="lv"><span>YOUR PRODUCT</span><b>LIVE</b></div><div class="tg" style="top:-70px;right:0">EXAMPLE</div></div>'
T["S6"] = dict(t0=a[6], end=a[7])
# S7 social and support
SC["S7"] = line("lead", "More agents run your", 7, 0, .4, 292, 62) + line("hv", "SOCIAL MEDIA", 7, .5, .7, 352, 100, acc=("social", "media")) + line("hv", "AND SUPPORT.", 7, .8, 1, 462, 100, acc=("support",)) + \
  '<div class="two5" style="top:640px"><div class="wc card5" id="sp1"><div class="tg">EXAMPLE</div>' + agent_badge("INSTAGRAM CURATOR", "MARKETING") + '<div class="post"><div class="pimg"></div><div class="pl"></div><div class="pl s"></div><div class="pl"></div></div></div>' + \
  '<div class="wc card5" id="sp2"><div class="tg">EXAMPLE</div>' + agent_badge("SUPPORT RESPONDER", "SUPPORT") + '<div class="tk"><div class="tkq">Order late?</div><div class="tkr"><span></span><span></span><span class="s"></span></div></div></div></div>'
T["S7"] = dict(t0=a[7], end=a[8])
# S8 boss agent
SC["S8"] = line("lead", "But the craziest one is the", 8, 0, .6, 292, 62) + line("hv", "BOSS AGENT.", 8, .7, 1, 352, 130, acc=("boss", "agent")) + \
  '<div class="hub8" id="hub"><svg class="hsv" viewBox="0 0 864 640" data-decor><path id="hp0" d="M432 320 L432 95"/><path id="hp1" d="M432 320 L565 320"/><path id="hp2" d="M432 320 L432 545"/><path id="hp3" d="M432 320 L165 320"/></svg>' + \
  '<div class="hn" style="left:432px;top:60px">PROJECT MANAGER</div><div class="hn" style="left:700px;top:320px">UX ARCHITECT</div><div class="hn" style="left:432px;top:580px">DEVELOPER</div><div class="hn" style="left:110px;top:320px">QA</div>' + \
  '<div class="hc" id="hc"><img src="assets/logos/clawd.png"><span>ORCHESTRATOR</span></div></div>'
T["S8"] = dict(t0=a[8], end=a[9])
# S9 checks every step
SC["S9"] = line("lead", "It hands the work to the right", 9, 0, .5, 292, 62) + line("hv", "SPECIALIST,", 9, .55, .7, 352, 130, acc=("specialist",)) + line("lead", "and checks every step.", 9, .75, 1, 506, 62) + \
  '<div class="wc card9" id="ck"><div class="tg">FROM THE REPO</div><div class="st9" id="s90"><b>1</b>PLANNING<i></i></div><div class="st9" id="s91"><b>2</b>ARCHITECTURE<i></i></div><div class="st9" id="s92"><b>3</b>DEV ↔ QA LOOP<i></i></div><div class="st9" id="s93"><b>4</b>FINAL CHECK<i></i></div><div class="q9">“Each implementation task must pass QA before proceeding.”</div></div>'
T["S9"] = dict(t0=a[9], checks=W("checks", "checks", 9, .8), end=a[10])
# S10 all or one
dots = "".join(f'<i class="dt" id="dt{i}"></i>' for i in range(283))
SC["S10"] = line("lead", "You can install", 10, 0, .3, 292, 62) + line("hv", "ALL OF THEM,", 10, .35, .7, 352, 118, acc=("all", "them")) + line("lead", "or just one.", 10, .75, 1, 500, 62) + \
  f'<div class="dots10" id="dots">{dots}</div><div class="one10" id="one">JUST ONE</div><div class="cnt10" id="cnt">283 AGENTS</div>'
T["S10"] = dict(t0=a[10], one=W("one", "one", 10, .95), end=a[11])
SC["S11"] = line("lead", "The setup's in the", 11, 0, .4, 420, 84) + line("hv", "LINK IN BIO.", 11, .55, .9, 516, 140)
T["S11"] = dict(t0=a[11], end=a[12])
SC["S12"] = line("lead", "Want the next one?", 12, 0, .35, 400, 84) + line("hv", "FOLLOW.", 12, .5, .5, 500, 192, acc=("follow",)) + ring("rgG", 78, 492, 900, 250)
T["S12"] = dict(t0=a[12], acc=W("follow", "follow", 12, .5), end=tF)

for k in T:
    for kk, v in list(T[k].items()):
        if isinstance(v, float): T[k][kk] = round(v, 3)
T["tF"] = tF; T["D"] = D

SFX = []
def sfx(f, t, g=-13): SFX.append(dict(f=f, t=round(max(0, t), 3), g=g))
sfx("whoosh_b.ogg", .1, -14); sfx("select.ogg", T["S1"]["hit"] - .05, -12); sfx("riser.ogg", a[2] - .3, -18); sfx("select.ogg", T["S3"]["stars"], -14)
sfx("click_a.ogg", a[4] + .5, -16); sfx("click_a.ogg", a[5] + .5, -16); sfx("click_a.ogg", a[6] + .5, -16); sfx("click_a.ogg", a[7] + .6, -16)
sfx("riser.ogg", a[8] + .3, -17); sfx("select.ogg", a[8] + 1.0, -14); sfx("click_a.ogg", T["S9"]["checks"], -16); sfx("whoosh_b.ogg", a[10] - .05, -16); sfx("select.ogg", T["S10"]["one"], -14); sfx("select.ogg", T["S12"]["acc"], -14)
SFX.sort(key=lambda x: x["t"]); json.dump(SFX, open(H_ + "/sfx105.json", "w"), indent=1)
NEWS = [(a[n], f"scene for line {n}") for n in range(1, NL + 1)] + [(tF, "frame 0 returns")]
NEWS = sorted((round(t, 2), x) for t, x in NEWS)
FLAT = [(NEWS[i][0], NEWS[i + 1][0]) for i in range(len(NEWS) - 1) if NEWS[i + 1][0] - NEWS[i][0] > 2.5]
if os.environ.get("SHIP") == "1" and STALE: sys.exit("SHIP=1 refused: estimated timeline")
json.dump(dict(version="ep105", estimated_timeline=STALE, lines=[dict(n=n, text=LINES[n - 1], start=round(s(n), 3), end=round(e(n), 3)) for n in range(1, NL + 1)],
               D=D, frame0_returns=tF, sync=SRC, screens=T, buildup=dict(new_on_screen=[dict(t=t, what=x) for t, x in NEWS], flat_over_2_5s=FLAT),
               numbers_on_screen=[dict(text="169k stars, 27.4k forks, MIT on the real GitHub page", source="github.com/msitarzewski/agency-agents read 17.11.2026"), dict(text="283 agent dots", source="README tables link 283 agent files (verify note 15.11.2026)")]), open(H_ + "/cues105.json", "w"), indent=1)

scenes = "".join(f'<div class="sc" id="sc{n}">{SC[n]}</div>' for n in SC)
CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;font-weight:500;color:{INK}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}}
.bgw{{position:absolute;left:-20px;top:-20px;width:1120px;height:1960px;background:#ecebe5 url(assets/bg.jpg);background-size:1120px 1960px;will-change:transform}}
#cam{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}}
.sc{{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0;visibility:hidden;will-change:transform,opacity}} #scA{{opacity:1;visibility:visible}}
.sc>*{{position:absolute}}
.lg{{display:block;flex:none;object-fit:contain}}
.ln{{left:108px;white-space:nowrap}}
.m{{display:inline-block;overflow:hidden;vertical-align:top;padding:0 .04em .06em 0;margin-right:.2em}} .lead .m{{margin-right:.24em}}
.w{{display:inline-block;transform:translateY(112%);will-change:transform}} .w.rdy{{transform:none}}
.lead .w{{font-weight:500;letter-spacing:-.02em}} .hv .w{{font-weight:900;letter-spacing:-.045em}}
.w.acc.rdy{{color:{INK}}}
.ring{{overflow:visible}}
#scS1{{opacity:1;visibility:visible}}
.stage{{position:absolute;left:0;top:600px;width:1080px;height:660px;perspective:1300px;transform-style:preserve-3d}}
.a3{{position:absolute;transform-style:preserve-3d}} #st1{{top:790px}} #st7{{visibility:hidden;opacity:0;z-index:40}} .clon,.free3,#scS4 .chip{{opacity:0;visibility:hidden}}
.floor{{position:absolute;left:0;top:90px;width:1080px;height:420px;transform-style:preserve-3d;transform:rotateX(44deg)}} .fa{{transform-style:preserve-3d}} .t3.flat{{zoom:1;transform:none}}
.orb{{position:absolute;left:0;top:0;width:120px;height:120px;perspective:600px;opacity:0}} .cb{{position:absolute;left:0;top:0;width:120px;height:120px;transform-style:preserve-3d}}
.cfc{{position:absolute;left:0;top:0;width:120px;height:120px;background:#fff;border:3px solid #b9b5a6;border-radius:12px;display:flex;flex-direction:column;align-items:center;justify-content:center;backface-visibility:hidden}} .cfc.side{{background:#e4e1d6}} .orb{{filter:drop-shadow(0 14px 16px rgba(20,20,20,.28))}}
.cfc b{{font-weight:900;font-size:40px;color:#111;line-height:1}} .cfc span{{font-weight:900;font-size:19px;letter-spacing:.04em;color:#6d6c66;margin-top:6px}}
.t3{{zoom:1.18;position:relative;width:240px;height:240px;transform-style:preserve-3d;transform:rotateX(8deg) rotateY(-18deg)}}
.t3 .lay{{position:absolute;left:0;top:0;width:240px;height:240px;border-radius:54px}}
.t3 .face{{position:absolute;left:0;top:0;width:240px;height:240px;border-radius:54px;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:inset 0 0 0 2px #e4e1d8}}
.tl{{width:140px;height:140px;object-fit:contain;border-radius:22px}}
.pr{{position:absolute;right:12px;top:10px;width:52px;height:52px;border-radius:26px;background:#111}} .pr:after{{content:'';position:absolute;left:12px;top:12px;width:22px;height:22px;border-radius:11px;border:5px solid #fff}}
.m3{{position:relative;width:260px;height:260px;transform-style:preserve-3d;transform:rotateY(-24deg) rotateX(8deg)}}
.m3 img{{position:absolute;left:0;top:0;width:260px;height:260px}} .m3b{{filter:brightness(.8) saturate(.95)}}
.lbl{{position:absolute;left:0;top:-52px;font-weight:900;font-size:30px;letter-spacing:.08em;color:#8a8982;white-space:nowrap}} .lbl.on{{color:#111;opacity:0}}
.ghost .face{{border:4px dashed #b9b6ab;background:#fafaf6}}
.plan{{top:560px;height:640px}} .pt2{{font-weight:900;font-size:44px;letter-spacing:-.02em;margin:6px 0 26px}}
.mg{{display:grid;grid-template-columns:repeat(6,1fr);gap:16px}} .mc{{position:relative;height:210px;border:3px solid #cfcdc4;border-radius:20px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px}}
.mc span{{font-weight:900;font-size:36px;color:#8a8982}} .mc b{{font-weight:900;font-size:76px;color:#111}} .mk{{position:absolute;left:-6px;right:-6px;top:56%;height:10px;border-radius:5px;background:{ORG};transform-origin:0 50%;transform:scaleX(0)}}
.free3{{position:absolute;left:108px;top:380px;font-weight:900;font-size:290px;line-height:300px;letter-spacing:-.05em;color:#111;white-space:nowrap;text-shadow:1px 1px 0 rgb(205,202,191), 2px 2px 0 rgb(200,197,186), 3px 3px 0 rgb(195,192,181), 4px 4px 0 rgb(190,187,176), 5px 5px 0 rgb(185,182,171), 6px 6px 0 rgb(180,177,166), 7px 7px 0 rgb(175,172,161), 8px 8px 0 rgb(170,167,156), 9px 9px 0 rgb(165,162,151), 10px 10px 0 rgb(160,157,146), 11px 11px 0 rgb(155,152,141), 12px 12px 0 rgb(150,147,136), 13px 13px 0 rgb(145,142,131), 14px 14px 0 rgb(140,137,126), 26px 34px 40px rgba(0,0,0,.28)}}
.chips{{position:absolute;left:108px;top:760px;display:flex;gap:14px}} .chip{{font-weight:900;font-size:32px;letter-spacing:.03em;border:4px solid #111;border-radius:60px;padding:10px 22px;color:#111;white-space:nowrap;background:rgba(255,255,255,.7)}}
.shot img{{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover}} .shot{{overflow:hidden;background:#fff;border-radius:30px;box-shadow:0 26px 50px rgba(20,20,20,.28)}}
.about5{{left:140px;top:560px;width:800px;height:381px}}
.grid11{{position:absolute;left:108px;top:640px;width:864px;height:470px}} .sk{{position:absolute;width:204px;height:130px;border-radius:28px;background:{CARD};box-shadow:0 14px 28px rgba(20,20,20,.22);padding:16px 18px;opacity:0}}
.sk b{{display:block;font-weight:900;font-size:26px;color:{ORG};letter-spacing:.04em}} .sk span{{display:block;font-weight:900;font-size:22px;color:#f2f2ee;margin-top:16px;letter-spacing:-.02em;white-space:nowrap}}
.cen{{left:410px;top:170px}}
.wc{{position:absolute;left:108px;width:864px;background:#fff;border-radius:34px;box-shadow:0 26px 50px rgba(20,20,20,.22);padding:34px 40px;opacity:0;visibility:hidden;overflow:hidden}}
.sheen{{position:absolute;top:-20%;left:0;width:160px;height:140%;background:linear-gradient(100deg,rgba(255,255,255,0),rgba(255,255,255,.75),rgba(255,255,255,0));transform:translateX(-320px) skewX(-12deg);pointer-events:none}}
.tg{{position:absolute;right:30px;top:22px;font-weight:500;font-size:24px;letter-spacing:.06em;color:#8a8982;border:2px solid #cfcdc4;border-radius:8px;padding:2px 10px}}
.wf{{position:relative;width:300px;height:480px;background:#fff;border:3px solid #111;border-radius:24px;padding:18px;box-shadow:0 12px 24px rgba(20,20,20,.14)}} .wf.big{{transform:scale(1.22);transform-origin:0 0}} .wf.sm{{transform:scale(.62);transform-origin:50% 0}}
.wfh{{height:48px;background:#111;border-radius:10px;margin-bottom:14px}} .wfg{{display:grid;grid-template-columns:repeat(5,1fr);gap:8px}} .wfg i{{display:block;height:44px;border:2px solid #cfcdc4;border-radius:8px}} .wfg i:nth-child(8){{background:#111;border-color:#111}}
.wfb{{height:30px;border-radius:8px;background:#e7e5dd;margin-top:16px}} .wfb.s{{width:70%}} .wfk{{position:absolute;left:18px;right:18px;bottom:18px;height:56px;border-radius:12px;background:#111;color:#fff;font-weight:900;font-size:26px;line-height:56px;text-align:center;letter-spacing:.06em}}
.wf.grey{{filter:grayscale(1);opacity:.75}} .wf.brand .wfh{{background:#2f7d5b}} .wf.brand .wfk{{background:#2f7d5b}} .wf.brand .wfg i:nth-child(8){{background:#2f7d5b;border-color:#2f7d5b}}
.recon{{top:560px;height:700px;padding:0}} .wfwrap{{position:absolute;left:40px;top:40px;width:370px;height:600px;overflow:hidden}} .scan{{position:absolute;left:0;top:0;width:370px;height:10px;background:{ORG};box-shadow:0 0 22px 6px rgba(217,119,87,.7);border-radius:5px;opacity:0}}
.found{{position:absolute;left:450px;top:60px;width:380px}} .fd{{height:130px;display:flex;align-items:center;gap:18px;font-weight:900;font-size:40px;letter-spacing:-.02em;color:#111;opacity:0}} .fd i{{font-style:normal;width:54px;height:54px;border-radius:27px;background:#111;color:#fff;font-size:34px;line-height:54px;text-align:center;flex:none}}
.trio{{position:absolute;left:108px;top:560px;width:864px;height:560px}} .ph{{position:absolute;top:0;width:260px;height:520px}} #ph1{{left:300px}} #ph2{{left:600px}} .ph .wf{{transform:scale(.86);transform-origin:0 0}} .ph .wf>*{{opacity:0}} .sn{{position:absolute;left:0;bottom:-6px;width:258px;text-align:center;font-weight:900;font-size:30px;letter-spacing:.06em;color:#8a8982}}
.cap9{{position:absolute;left:108px;width:864px;top:1160px;text-align:center;font-weight:900;font-size:32px;letter-spacing:.08em;color:#111;opacity:0}}
.bk{{position:absolute;left:108px;top:540px;width:864px;height:660px}} .phone{{position:absolute;left:332px;top:0;width:200px;height:300px}} .bkl{{position:absolute;left:32px;top:300px;width:800px;height:160px;overflow:visible}}
.bx{{position:absolute;top:470px;width:250px;height:160px;border:4px solid #111;border-radius:26px;background:#fff;font-weight:900;font-size:36px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;opacity:0;box-shadow:0 14px 28px rgba(20,20,20,.14)}} .bx b{{font-size:48px}}
.tst{{top:560px;height:660px;padding-top:96px}} .tr{{height:128px;display:flex;align-items:center;gap:26px;font-weight:900;font-size:44px;letter-spacing:-.02em;color:#111;opacity:0;border-bottom:2px solid #eee}} .bx2{{font-style:normal;width:64px;height:64px;border-radius:32px;background:#111;color:#fff;text-align:center;line-height:64px;font-size:40px;flex:none}} #tr2 .bx2{{background:{ORG}}}
.cube{{position:absolute;left:420px;top:210px;width:240px;height:240px;transform-style:preserve-3d}} .cf{{position:absolute;left:0;top:0;width:240px;height:240px;background:{CARD};border:4px solid {ORG};display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:40px;text-align:center;line-height:1}}
.rvs{{position:absolute;left:108px;top:560px;width:864px;height:520px;display:grid;grid-template-columns:1fr 1fr;gap:24px}} .rv{{background:#fff;border-radius:26px;box-shadow:0 18px 36px rgba(20,20,20,.16);padding:22px 26px;height:240px;opacity:0}} .rh{{display:flex;justify-content:space-between;align-items:center}} .rh b{{font-weight:900;font-size:30px}} .stars{{font-size:34px;color:{ORG};letter-spacing:2px}}
.rl{{height:20px;border-radius:10px;background:#e7e5dd;margin-top:22px}} .rl.s{{width:64%}} .tag9{{position:absolute;left:108px;top:1090px;font-weight:500;font-size:26px;letter-spacing:.08em;color:#8a8982}}
.two{{position:absolute;left:108px;top:1140px;display:flex;gap:18px}} .chip.dk{{font-size:34px;padding:10px 24px;opacity:.35}}
.fixc{{top:620px;height:640px;padding-top:96px}} .fx{{height:120px;display:flex;align-items:center;gap:26px;font-weight:900;font-size:46px;letter-spacing:-.02em;color:#111;opacity:0;border-bottom:2px solid #eee}} .ck{{font-style:normal;width:60px;height:60px;border-radius:30px;border:4px solid #cfcdc4;color:transparent;text-align:center;line-height:52px;font-size:36px;flex:none}} .fx.on .ck{{background:#111;border-color:#111;color:#fff}}
.rts{{position:absolute;left:40px;right:40px;bottom:30px;height:96px;border:5px solid #111;border-radius:20px;font-weight:900;font-size:40px;line-height:86px;text-align:center;letter-spacing:.02em;color:#111;opacity:0}}
.chat{{top:600px;height:600px;padding:40px 44px}} .stp{{font-weight:900;font-size:34px;letter-spacing:.06em;color:#b9b8b2;margin:0 0 14px}} .inp{{background:#26272c;border-radius:22px;padding:26px 30px;font-size:34px;color:#f2f2ee;margin-bottom:36px;min-height:96px;font-family:'Courier New',monospace;white-space:nowrap;overflow:hidden}} .ok{{font-weight:900;font-size:42px;color:#f2f2ee;opacity:0}}
.rb{{position:absolute;left:108px;top:560px;width:864px;height:640px}} .rbo,.rby{{position:absolute;top:0;width:330px;opacity:0}} .rbo{{left:20px}} .rby{{left:500px}} .rbt{{font-weight:900;font-size:34px;letter-spacing:.08em;margin-bottom:16px;color:#8a8982}} .rbt.on{{color:#111}} .sw{{display:flex;gap:12px;margin-top:20px}} .sw i{{display:block;width:60px;height:60px;border-radius:14px;border:3px solid #111}}
.cpy{{position:absolute;left:372px;top:260px;font-weight:900;font-size:50px;color:#111;opacity:0}} .stk2{{position:absolute;left:-8px;right:-8px;top:52%;height:9px;border-radius:5px;background:{ORG};transform-origin:0 50%;transform:scaleX(0)}}
.comp{{position:absolute;left:108px;width:864px;background:{CARD};border-radius:44px;box-shadow:0 26px 50px rgba(20,20,20,.28);opacity:0;visibility:hidden}}
.sc{{z-index:2}}
#crowd{{position:absolute;left:0;top:0;width:1080px;height:1920px;clip-path:inset(740px 0 0 0);z-index:1}} #cworld{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 1130px}}
.bd{{position:absolute;border-radius:50%;box-shadow:0 10px 18px rgba(20,20,20,.10)}}
.fg{{position:absolute;width:30px;height:58px;transform-origin:50% 100%;filter:drop-shadow(0 6px 4px rgba(20,20,20,.18))}} .fg:before{{content:'';position:absolute;left:5px;top:0;width:20px;height:20px;border-radius:10px;background:linear-gradient(#34343a,#0f0f10)}} .fg:after{{content:'';position:absolute;left:0;top:23px;width:30px;height:35px;border-radius:15px 15px 6px 6px;background:linear-gradient(#2a2a2f,#0f0f10)}}
.ped{{position:absolute;left:300px;top:1062px;width:480px;height:150px;border-radius:50%;background:#fff;box-shadow:0 18px 34px rgba(20,20,20,.22),inset 0 -8px 0 #ecebe5}} .clawd{{position:absolute;left:350px;top:800px;width:380px;height:380px;object-fit:contain;filter:drop-shadow(0 14px 10px rgba(20,20,20,.20))}}
.freeb{{position:absolute;left:770px;top:748px;width:220px;height:220px;border-radius:50%;background:{ORG};color:#fff;font-weight:900;font-size:76px;letter-spacing:-.03em;display:flex;align-items:center;justify-content:center;box-shadow:0 20px 34px rgba(20,20,20,.28);opacity:0;visibility:hidden}}
.rh3{{left:108px;top:536px;width:864px;height:65px;opacity:0;visibility:hidden}} .ab3{{left:160px;top:634px;width:760px;height:631px;opacity:0;visibility:hidden}}
.ab{{display:flex;align-items:center;gap:18px}} .abl{{width:64px;height:64px;object-fit:contain}} .ab b{{font-weight:900;font-size:34px;letter-spacing:-.01em;display:block;white-space:nowrap}} .ab span{{font-weight:500;font-size:24px;letter-spacing:.08em;color:#8a8982}}
.card4{{top:580px;height:620px}} .mail{{margin-top:34px}} .mrow{{display:flex;gap:20px;font-weight:500;font-size:36px;padding:20px 0;border-bottom:2px solid #eee}} .mrow i{{font-style:normal;font-weight:900;font-size:24px;color:#8a8982;width:150px;letter-spacing:.06em;padding-top:8px}} .mrow u{{text-decoration:none}} .mrow .c{{opacity:0}}
.mb span{{display:block;height:24px;border-radius:12px;background:#e7e5dd;margin-top:30px}} .mb span.s{{width:60%}} .send{{margin-top:44px;display:inline-block;background:#111;color:#fff;font-weight:900;font-size:36px;padding:18px 50px;border-radius:18px;letter-spacing:.06em;opacity:0}}
.two5{{position:absolute;left:108px;top:580px;width:864px;height:620px}} .two5 .wc{{width:420px;height:600px;top:0}} #cp1,#sp1{{left:0}} #cp2,#sp2{{left:444px}} .card5 .ab b{{font-size:22px}} .card5 .abl{{width:48px;height:48px}} .card5 .ab span{{font-size:20px}} .card5 .tg,.card9 .tg{{top:auto;bottom:20px;right:24px}} .card9{{padding-bottom:60px}}
.ck5{{font-weight:900;font-size:34px;letter-spacing:.06em;margin:30px 0 8px}} .ckr{{display:flex;align-items:center;gap:16px;margin-top:26px}} .ckr i{{width:38px;height:38px;border:4px solid #111;border-radius:10px;flex:none}} .ckr i.on{{background:{ORG};border-color:{ORG}}} .ckr b{{display:block;flex:1;height:22px;border-radius:11px;background:#e7e5dd}} .ckr b.s{{flex:.6}}
.doc span{{display:block;height:22px;border-radius:11px;background:#e7e5dd;margin-top:26px;transform-origin:0 50%}} .doc span.s{{width:55%}}
.dev6{{position:absolute;left:108px;top:600px;width:864px;height:620px}} .dr{{position:absolute;left:0;width:560px;height:170px;background:#fff;border-radius:26px;box-shadow:0 18px 36px rgba(20,20,20,.16);padding:0 28px;display:flex;align-items:center;justify-content:space-between;opacity:0}} .dr .ab b{{font-size:27px}} .dr .abl{{width:56px;height:56px}} #d0{{top:0}} #d1{{top:195px}} #d2{{top:390px}}
.dk{{font-style:normal;width:46px;height:46px;border-radius:23px;background:#d8d6cd;color:#fff;text-align:center;line-height:46px;font-weight:900;font-size:28px;flex:none}} .dk.on{{background:{ORG}}}
.live6{{position:absolute;left:600px;top:150px;width:264px;height:290px;background:{CARD};border-radius:34px;box-shadow:0 26px 50px rgba(20,20,20,.28);color:#f2f2ee;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;opacity:0}} .live6 span{{font-weight:500;font-size:22px;letter-spacing:.1em;color:#b9b8b2}} .live6 b{{font-weight:900;font-size:84px;letter-spacing:-.03em;color:{ORG}}}
.post .pimg{{height:240px;border-radius:18px;background:linear-gradient(135deg,#e7e5dd,#d9d6c9);margin-top:24px;position:relative}} .post .pimg:after{{content:'';position:absolute;left:50%;top:50%;margin:-50px 0 0 -50px;width:100px;height:100px;border-radius:50%;background:{ORG}}} .pl{{height:20px;border-radius:10px;background:#e7e5dd;margin-top:22px}} .pl.s{{width:60%}}
.tk{{margin-top:26px}} .tkq{{background:#111;color:#fff;font-weight:700;font-size:32px;padding:16px 24px;border-radius:18px;display:inline-block}} .tkr{{margin-top:26px;border:3px solid #cfcdc4;border-radius:18px;padding:24px}} .tkr span{{display:block;height:20px;border-radius:10px;background:#e7e5dd;margin-bottom:16px}} .tkr span.s{{width:60%;margin-bottom:0}}
.hub8{{position:absolute;left:108px;top:570px;width:864px;height:640px;transform:scale(1.15);transform-origin:50% 45%}} .hsv{{position:absolute;left:0;top:0;width:864px;height:640px;overflow:visible}} .hsv path{{fill:none;stroke:#111;stroke-width:5;stroke-linecap:round}}
.hn{{position:absolute;font-weight:900;font-size:26px;letter-spacing:.04em;background:#fff;border:4px solid #111;border-radius:60px;padding:10px 24px;white-space:nowrap;opacity:0}} .hc{{position:absolute;left:432px;top:320px;width:250px;height:250px;border-radius:50%;background:#fff;border:7px solid {ORG};box-shadow:0 26px 50px rgba(20,20,20,.22);display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0}} .hc img{{width:120px;height:120px;object-fit:contain}} .hc span{{font-weight:900;font-size:23px;letter-spacing:.06em;margin-top:6px}}
.card9{{top:650px;height:580px}} .st9{{display:flex;align-items:center;gap:22px;font-weight:900;font-size:40px;height:92px;border-bottom:2px solid #eee;letter-spacing:-.01em}} .st9 b{{width:56px;height:56px;border-radius:28px;background:#111;color:#fff;text-align:center;line-height:56px;font-size:30px;flex:none}} .st9 i{{margin-left:auto;font-style:normal;width:50px;height:50px;border-radius:25px;border:4px solid #cfcdc4;text-align:center;line-height:42px;color:#fff;font-size:28px}} .st9.on i{{background:{ORG};border-color:{ORG}}} .q9{{margin-top:24px;font-weight:500;font-size:32px;line-height:1.3;color:#444}}
.dots10{{position:absolute;left:108px;top:660px;width:864px;display:grid;grid-template-columns:repeat(23,1fr);gap:7px}} .dt{{display:block;aspect-ratio:1;border-radius:7px;background:#111;opacity:0}} .cnt10{{position:absolute;left:108px;top:1150px;font-weight:900;font-size:44px;letter-spacing:.04em}} .one10{{position:absolute;left:600px;top:1150px;font-weight:900;font-size:44px;letter-spacing:.04em;color:{ORG};opacity:0}}
'''
JS = r'''
gsap.registerPlugin(SplitText, DrawSVGPlugin, CustomEase);
const T=__T__, ORG='__ORG__', INK='__INK__';
/* house curves (motion-animation-principles): enter = ease-out, exit = ease-in and faster, move = in-out; landings use a
   critically damped spring: fast launch, long soft settle, never past its end state (motion-remotion-notes 1) */
const expoOut=CustomEase.create("expoOut","0.16,1,0.3,1"), expoIn=CustomEase.create("expoIn","0.7,0,0.84,0"), inOut=CustomEase.create("mvInOut","0.65,0,0.35,1");
const expoInOutZ=CustomEase.create('expoInOutZ','0.76,0,0.24,1');
const spring=(w=>{const f=t=>1-(1+w*t)*Math.exp(-w*t), n=f(1); return t=>f(t)/n})(9);
const show=id=>gsap.fromTo(id,{autoAlpha:0,y:10,filter:'blur(6px)'},{autoAlpha:1,y:0,filter:'blur(0px)',duration:.3,ease:'power2.out',immediateRender:false});
const hide=id=>gsap.to(id,{autoAlpha:0,y:-12,filter:'blur(8px)',duration:.22,ease:expoIn});
/* kinetic type: each word rises out of its mask when it is spoken; the accent word is split into characters (SplitText masks) */
function type(t,id,t0){
  gsap.utils.toArray(id+' .w:not(.rdy)').forEach(w=>{
    const at=Math.max(0,+w.dataset.t-t0-.07);
    if(w.classList.contains('acc')){ gsap.set(w,{y:0,yPercent:0}); const sp=SplitText.create(w,{type:'chars',mask:'chars',aria:'none'});
      t.fromTo(sp.chars,{yPercent:112},{yPercent:0,duration:.5,ease:expoOut,stagger:.03},at).to(sp.chars,{color:INK,duration:.3,ease:'power1.out',stagger:.03},at+.12); }
    else t.fromTo(w,{yPercent:112,y:0},{yPercent:0,y:0,duration:.46,ease:expoOut,immediateRender:false},at); });
}
function ringDraw(t,id,at){ t.fromTo(id+' path',{drawSVG:'0%'},{drawSVG:'100%',duration:.8,ease:'power2.inOut',immediateRender:false},at) }
gsap.set('.ring path, .arw path',{drawSVG:'0%'});

/* A: the cube. Frame 0 is complete; then the six price tags flip to ticks one by one, each tile nudges (follow-through) */
/* typed text: each character appears at a slightly varying pace (never a fixed tick) */
function typeChars(t,sel,at,dur){ const el=document.querySelector(sel); if(!el) return; const sp=SplitText.create(el,{type:'words,chars',charsClass:'c',wordsClass:'wd'}); const n=sp.chars.length; let w=[],tot=0;
  for(let i=0;i<n;i++){ const v=.7+.6*Math.abs(Math.sin(i*2.3+1)); w.push(v); tot+=v; } let c=at;
  sp.chars.forEach((ch,i)=>{ t.set(ch,{opacity:1},c); c+=dur*w[i]/tot; }); }
function typeChars(t,sel,at,dur){ const el=document.querySelector(sel); if(!el) return; const sp=SplitText.create(el,{type:'words,chars',charsClass:'c',wordsClass:'wd'}); const n=sp.chars.length; let w=[],tot=0;
  for(let i=0;i<n;i++){ const v=.7+.6*Math.abs(Math.sin(i*2.3+1)); w.push(v); tot+=v; } let c=at; sp.chars.forEach((ch,i)=>{ t.set(ch,{opacity:1},c); c+=dur*w[i]/tot; }); }
function scWords(id,o,ringId){ const t=gsap.timeline(); t.add(show(id),0); type(t,id,o.t0-.04);
  if(ringId) ringDraw(t,'#'+ringId,(o.acc-o.t0)+.16);
  t.to(id+' .ln',{x:8,duration:Math.max(.6,o.end-o.t0-.5),ease:'sine.inOut',stagger:.06},.4).add(hide(id),o.end-o.t0-.2); return t; }
const card=(t,sel,at,y)=>t.fromTo(sel,{autoAlpha:0,y:y||40},{autoAlpha:1,y:0,duration:.55,ease:spring,immediateRender:false},at);
const sheenOnce=(t,sel,at)=>t.fromTo(sel,{x:-320},{x:1100,duration:.9,ease:'sine.inOut',immediateRender:false},at);
const drift=(t,sel,dur,s)=>t.fromTo(sel,{scale:1},{scale:s||1.035,duration:Math.max(1,dur),ease:'sine.inOut',immediateRender:false},.3);
function scS1(){ const o=T.S1,t=gsap.timeline();
  document.querySelectorAll('#scS1 .hv').forEach(el=>{ const w=el.querySelector('.w'), tw=Math.max(.05,parseFloat(w.dataset.t)-.1); t.fromTo(el,{scale:1.1,transformOrigin:'0% 50%'},{scale:1,duration:.5,ease:'back.out(1.7)',immediateRender:false},tw); });
  t.fromTo('#freeb',{autoAlpha:0,scale:.3,rotation:-40},{autoAlpha:1,scale:1,rotation:-8,duration:.55,ease:spring,immediateRender:false},Math.max(.3,o.hit-.12)).fromTo('#freeb',{y:0},{y:-10,duration:1.2,yoyo:true,repeat:1,ease:'sine.inOut',immediateRender:false},Math.max(.9,o.hit+.4));
  t.add(hide('#scS1'),o.end-.24); return t; }
function scS2(){ const o=T.S2,t=gsap.timeline(); t.add(show('#scS2'),0); type(t,'#scS2',o.t0-.04); t.add(hide('#scS2'),o.end-o.t0-.2); return t; }
function scS3(){ const o=T.S3,t=gsap.timeline(); t.add(show('#scS3'),0); type(t,'#scS3',o.t0-.04);
  t.fromTo('#rh',{autoAlpha:0,y:40},{autoAlpha:1,y:0,duration:.55,ease:spring,immediateRender:false},.55).fromTo('#ab',{autoAlpha:0,y:50},{autoAlpha:1,y:0,duration:.6,ease:spring,immediateRender:false},.9);
  ringDraw(t,'#rgS',Math.max(1.4,o.stars-o.t0-.5)); t.fromTo('#ab',{scale:1},{scale:1.035,duration:Math.max(1,o.end-o.t0),ease:'sine.inOut',immediateRender:false},.9).add(hide('#scS3'),o.end-o.t0-.2); return t; }
function scS4(){ const o=T.S4,t=gsap.timeline(); t.add(show('#scS4'),0); type(t,'#scS4',o.t0-.04); card(t,'#em',.25);
  typeChars(t,'#m1',.45,.35); typeChars(t,'#m2',.8,.45);
  t.fromTo('#em .mb span',{scaleX:0,transformOrigin:'0 50%'},{scaleX:1,duration:.3,stagger:.1,ease:'power2.out',immediateRender:false},1.1).fromTo('#snd',{autoAlpha:0,scale:.8},{autoAlpha:1,scale:1,duration:.3,ease:spring,immediateRender:false},1.4).add(hide('#scS4'),o.end-o.t0-.2); return t; }
function scS5(){ const o=T.S5,t=gsap.timeline(); t.add(show('#scS5'),0); type(t,'#scS5',o.t0-.04); card(t,'#cp1',.25); card(t,'#cp2',.4);
  t.fromTo('#cp1 .ckr i',{background:'#fff'},{background:ORG,borderColor:ORG,duration:.2,stagger:.2,immediateRender:false},.75)
   .fromTo('#cp2 .doc span',{scaleX:0},{scaleX:1,duration:.3,stagger:.12,ease:'power2.out',immediateRender:false},.7).add(hide('#scS5'),o.end-o.t0-.2); return t; }
function scS6(){ const o=T.S6,t=gsap.timeline(); t.add(show('#scS6'),0); type(t,'#scS6',o.t0-.04);
  [0,1,2].forEach(i=>{ t.fromTo('#d'+i,{autoAlpha:0,x:-40},{autoAlpha:1,x:0,duration:.4,ease:expoOut,immediateRender:false},.25+i*.2).add(()=>document.querySelector('#d'+i+' .dk').classList.add('on'),.75+i*.2).add(()=>{document.querySelector('#d'+i+' .dk').classList.remove('on')},0); });
  t.fromTo('#lv',{autoAlpha:0,scale:.8},{autoAlpha:1,scale:1,duration:.45,ease:spring,immediateRender:false},1.1).add(hide('#scS6'),o.end-o.t0-.2); return t; }
function scS7(){ const o=T.S7,t=gsap.timeline(); t.add(show('#scS7'),0); type(t,'#scS7',o.t0-.04); card(t,'#sp1',.45); card(t,'#sp2',.65);
  t.fromTo('#sp1 .pimg',{scale:.9},{scale:1,duration:.5,ease:spring,immediateRender:false},.8).fromTo('#sp2 .tkr span',{scaleX:0,transformOrigin:'0 50%'},{scaleX:1,duration:.3,stagger:.15,immediateRender:false},1.2).add(hide('#scS7'),o.end-o.t0-.2); return t; }
function scS8(){ const o=T.S8,t=gsap.timeline(); t.add(show('#scS8'),0); type(t,'#scS8',o.t0-.04);
  gsap.set('.hn,.hc',{xPercent:-50,yPercent:-50}); gsap.set('.hsv path',{drawSVG:'0%'});
  t.fromTo('#hc',{autoAlpha:0,scale:.6},{autoAlpha:1,scale:1,duration:.55,ease:spring,immediateRender:false},.6);
  [0,1,2,3].forEach(i=>{ t.fromTo('#hp'+i,{drawSVG:'0%'},{drawSVG:'100%',duration:.45,ease:'power2.inOut',immediateRender:false},.95+i*.12).fromTo('#hub .hn:nth-of-type('+(i+1)+')',{autoAlpha:0,scale:.7},{autoAlpha:1,scale:1,duration:.4,ease:spring,immediateRender:false},1.1+i*.12); });
  t.fromTo('#hc',{rotation:-3},{rotation:3,duration:Math.max(1,o.end-o.t0-1),ease:'sine.inOut',immediateRender:false},1.3).add(hide('#scS8'),o.end-o.t0-.2); return t; }
function scS9(){ const o=T.S9,t=gsap.timeline(); t.add(show('#scS9'),0); type(t,'#scS9',o.t0-.04); card(t,'#ck',.5);
  [0,1,2,3].forEach(i=>{ const at=Math.max(.9,o.checks-o.t0)+i*.3; t.add(()=>{const e=document.querySelector('#s9'+i); e.classList.add('on'); e.querySelector('i').textContent='✓'},at).add(()=>{const e=document.querySelector('#s9'+i); e.classList.remove('on'); e.querySelector('i').textContent=''},0); });
  t.fromTo('#ck .q9',{autoAlpha:0},{autoAlpha:1,duration:.4,immediateRender:false},Math.max(1.4,o.checks-o.t0+.6)).add(hide('#scS9'),o.end-o.t0-.2); return t; }
function scS10(){ const o=T.S10,t=gsap.timeline(); t.add(show('#scS10'),0); type(t,'#scS10',o.t0-.04);
  t.fromTo('#dots .dt',{opacity:0,scale:.3},{opacity:1,scale:1,duration:.25,stagger:{each:.0022,from:'random'},ease:'power2.out',immediateRender:false},.35).fromTo('#cnt',{autoAlpha:0},{autoAlpha:1,duration:.3,immediateRender:false},.8);
  const one=Math.max(1.2,o.one-o.t0-.1);
  t.to('#dots .dt',{opacity:.22,duration:.4},one).to('#dt137',{opacity:1,scale:2.6,backgroundColor:ORG,duration:.5,ease:spring,zIndex:5},one+.05).to('#one',{opacity:1,duration:.4},one+.1).add(hide('#scS10'),o.end-o.t0-.2); return t; }
const tl=gsap.timeline({paused:true});
tl.fromTo('#cam',{scale:1},{scale:1.012,duration:T.D/4,ease:'sine.inOut',yoyo:true,repeat:3},0)
  .fromTo('.bgw',{x:0,y:0},{x:-14,y:-12,duration:T.D/2,ease:'sine.inOut',yoyo:true,repeat:1},0)
  .fromTo('#cworld',{scale:1.25},{scale:1.4,duration:T.S2.t0,ease:'sine.inOut'},0).to('#cworld',{scale:.74,duration:1.5,ease:expoInOutZ},T.S2.t0-.15).to('#cworld',{scale:.7,duration:Math.max(.5,T.S3.t0-T.S2.t0-1.2),ease:'sine.inOut'},T.S2.t0+1.35)
  .fromTo('#clawd',{y:0},{y:-12,duration:1.1,yoyo:true,repeat:Math.ceil(T.S3.t0/1.1),ease:'sine.inOut'},0)
  .to('#crowd',{autoAlpha:0,duration:.3,ease:'power1.in'},T.S3.t0-.05)
  .add(scS1(),0).add(scS2(),T.S2.t0-.04).add(scS3(),T.S3.t0-.04).add(scS4(),T.S4.t0-.04).add(scS5(),T.S5.t0-.04).add(scS6(),T.S6.t0-.04).add(scS7(),T.S7.t0-.04)
  .add(scS8(),T.S8.t0-.04).add(scS9(),T.S9.t0-.04).add(scS10(),T.S10.t0-.04).add(scWords('#scS11',T.S11),T.S11.t0-.04).add(scWords('#scS12',T.S12,'rgG'),T.S12.t0-.04);
tl.set('#freeb',{autoAlpha:0},T.tF).set('#crowd',{autoAlpha:1},T.tF).set('#cworld',{scale:1.38},T.tF).set('#clawd',{y:0},T.tF).fromTo('#scS1',{autoAlpha:0,filter:'blur(6px)'},{autoAlpha:1,filter:'blur(0px)',duration:.36,ease:'power2.out',immediateRender:false},T.tF+.02).to({},{duration:.001},T.D-.001);
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
<div class="bgw" data-decor></div><div id="cam">{scenes}{ORBL}</div>
</div>
<script>
{JS}
</script></body></html>'''
os.makedirs(H_ + "/out", exist_ok=True)
open(H_ + "/hf/index.html", "w").write(html)
say(f"v5 estimated timeline={STALE}  D={D}  sfx={len(SFX)}")
say("lines: " + "  ".join(f"{n}:{s(n):.2f}-{e(n):.2f}" for n in range(1, NL + 1)))
say("sync: " + "  ".join(f"{k}={v}" for k, v in SRC.items() if k))
for t, x in NEWS: say(f"  new {t:6.2f}  {x}")
say("FLAT stretches over 2.5 s with nothing new: " + (str(FLAT) if FLAT else "none"))
open(H_ + "/out/build105.log", "w").write("\n".join(LOG) + "\n")
