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
Writes  hf/index.html, cues104.json, sfx103.json, out/build104.log.
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
NL = len(LINES); assert NL == 18, "ep104 is laid out for 18 lines"
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

# ---- S1 hook: three paid apps on 3D tiles, the 3D Claude mark sweeps through them
SC["S1"] = line("lead", "Claude just destroyed", 1, 0, .5, 286, 62, ready=True) + line("hv", "PAID", 1, .6, .6, 368, 215, ready=True, acc=("paid",)) + line("hv", "APPS.", 1, .85, .85, 612, 215, ready=True, acc=("apps",)) + \
  '<div class="stage" id="st1"><div class="floor" id="fl1">' + \
  '<div class="a3 fa" id="a0" style="left:90px;top:40px">' + flat_tile("slack.svg") + '</div>' + \
  '<div class="a3 fa" id="a1" style="left:420px;top:40px">' + flat_tile("calendly.svg") + '</div>' + \
  '<div class="a3 fa" id="a2" style="left:750px;top:40px">' + flat_tile("notion.png") + '</div></div>' + \
  '<div class="a3" id="cm1" style="left:370px;top:400px">' + mark3d(12, 5) + '</div></div>'
tHit = W("destroyed", "destroyed", 1, .35)
T["S1"] = dict(t0=0, hit=tHit, end=a[2])
# ---- S2 clone any app
SC["S2"] = line("lead", "You can now", 2, 0, .3, 292, 62) + line("hv", "CLONE ANY APP", 2, .3, .8, 352, 104, acc=("clone",)) + \
  '<div class="stage" id="st2"><div class="a3 orig" id="o2" style="left:150px;top:330px">' + logo_tile("notion.png") + '<span class="lbl">ORIGINAL</span></div>' + \
  '<div class="a3 clon" id="c2" style="left:150px;top:330px">' + ext('<img src="assets/logos/notion.png" class="tl">', "ghost") + '<span class="lbl on">CLONE</span></div>' + \
  '<div class="a3" id="m2" style="left:420px;top:370px;width:240px;height:240px">' + mark3d(10, 3) + '</div></div>'
T["S2"] = dict(t0=a[2], scan=W("clone", "clone", 2, .45), end=a[3])
# ---- S3 stop paying
months = "JFMAMJJASOND"
cells = "".join(f'<div class="mc"><span>{m}</span><b>$</b><i class="mk"></i></div>' for m in months)
SC["S3"] = line("lead", "so you can", 3, 0, .3, 292, 62) + line("hv", "STOP PAYING", 3, .35, .9, 352, 140, acc=("stop", "paying")) + f'<div class="wc plan" id="plan"><div class="pt2">MONTHLY PLAN</div><div class="mg">{cells}</div></div>'
T["S3"] = dict(t0=a[3], end=a[4])
# ---- S4 free (3D letters)
SC["S4"] = line("lead", "And the skill is", 4, 0, .5, 292, 62) + '<div class="free3" id="free3">FREE.</div>' + \
  '<div class="chips"><span class="chip">MIT LICENSE</span><span class="chip">NO SIGNUP</span><span class="chip">NO API KEY</span></div>'
T["S4"] = dict(t0=a[4], free=W("free", ("free",), 4, .6), end=a[5])
# ---- S5 repo page (real)
SC["S5"] = line("lead", "It's called the", 5, 0, .15, 292, 62) + line("hv", "REPLICA SKILL.", 5, .55, .75, 352, 104, acc=("replica",)) + '<div class="shot about5" id="sh5"><img src="assets/shots/about.png"></div>'
T["S5"] = dict(t0=a[5], end=a[6])
# ---- S6 eleven tiles
g = "".join(f'<div class="sk" style="left:{(i % 4) * 220}px;top:{(i // 4) * 150}px"><b>{i + 1:02d}</b><span>{n}</span></div>' for i, n in enumerate(SKILLS))
SC["S6"] = line("lead", "It's not one skill,", 6, 0, .5, 292, 62) + line("hv", "IT'S 11.", 6, .75, 1, 372, 140, acc=("11",)) + f'<div class="grid11" id="g11">{g}</div>'
T["S6"] = dict(t0=a[6], eleven=W("eleven", ("11", "eleven"), 6, .8), end=a[7])
# ---- S7 ring (3D feel): Claude mark in the middle, 11 skill cards orbiting
ABBR = ["RECON", "ARCH", "DESIGN", "BUILD", "BACK", "TEST", "DIFF", "ENTRE", "BRAND", "LAUNCH", "DEPLOY"]
def cubehtml(i):
    fr = f'<div class="cfc" style="transform:translateZ(60px)"><b>{i + 1:02d}</b><span>{ABBR[i]}</span></div>'
    oth = "".join(f'<div class="cfc side" style="transform:{tf}"></div>' for tf in ("rotateY(180deg) translateZ(60px)", "rotateY(90deg) translateZ(60px)", "rotateY(-90deg) translateZ(60px)", "rotateX(90deg) translateZ(60px)", "rotateX(-90deg) translateZ(60px)"))
    return f'<div class="orb" id="orb{i}"><div class="cb" id="cb{i}">{fr}{oth}</div></div>'
ringc = "".join(cubehtml(i) for i in range(11))
SC["S7"] = line("lead", "Each one has its own job,", 7, 0, .45, 286, 58) + line("hv", "A DEV TEAM.", 7, .55, .8, 350, 120, acc=("dev", "team"))
ORBL = f'<div class="stage" id="st7"><div class="a3 cen" id="cm7">{mark3d(8, 3)}</div>{ringc}</div>'
T["S7"] = dict(t0=a[7], end=a[8])
# ---- S8 recon
SC["S8"] = line("lead", "The first one studies the app", 8, 0, .8, 292, 54) + line("hv", "RECON", 8, .8, .95, 352, 150, acc=("recon",)) + \
  '<div class="wc recon" id="rc"><i class="sheen"></i><div class="wfwrap">' + wf("big") + '<div class="scan" id="scan"></div></div><div class="found">' + \
  "".join(f'<div class="fd"><i>✓</i>{t}</div>' for t in ("SCREENS", "FLOWS", "COMPONENTS", "DATA MODEL")) + '</div></div>'
T["S8"] = dict(t0=a[8], end=a[9])
# ---- S9 build
SC["S9"] = line("lead", "Another one", 9, 0, .2, 292, 62) + line("hv", "REBUILDS IT", 9, .25, .5, 352, 130, acc=("rebuilds",)) + \
  '<div class="trio" id="trio">' + "".join(f'<div class="ph" id="ph{i}">{wf()}<div class="sn">SCREEN {i + 1}</div></div>' for i in range(3)) + '</div>' + '<div class="cap9">BUILT FROM THE RECON MAP</div>'
T["S9"] = dict(t0=a[9], end=a[10])
# ---- S10 backend
SC["S10"] = line("lead", "One handles the", 10, 0, .3, 292, 62) + line("hv", "BACKEND", 10, .45, .6, 352, 160, acc=("backend",)) + \
  '<div class="bk" id="bk"><div class="phone">' + wf("sm") + '</div><svg class="bkl" viewBox="0 0 800 160"><path d="M400 0 V70 M130 160 V70 H670 V160" fill="none" stroke="#0f0f0f" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>' + \
  '<div class="bx" style="left:0"><b>🔒</b>AUTH</div><div class="bx" style="left:270px"><b>▤</b>DATABASE</div><div class="bx" style="left:540px"><b>▭</b>PAYMENTS</div></div>'
T["S10"] = dict(t0=a[10], end=a[11])
# ---- S11 test
rows = [("BOOK A MEETING", 1), ("SET AVAILABILITY", 1), ("RESCHEDULE", 0), ("TIME ZONES", 1)]
tr = "".join(f'<div class="tr" id="tr{i}"><i class="bx2">{"✓" if ok else "✕"}</i>{t}</div>' for i, (t, ok) in enumerate(rows))
SC["S11"] = line("lead", "And one", 11, 0, .2, 292, 62) + line("hv", "TESTS IT", 11, .3, .6, 352, 150, acc=("tests",)) + f'<div class="wc tst" id="tst"><i class="sheen"></i><span class="tg">EXAMPLE TEST RUN</span>{tr}</div>'
T["S11"] = dict(t0=a[11], bug=W("bugs", "bugs", 11, .8), end=a[12])
# ---- S12 craziest: rotating 3D cube
faces = "".join(f'<div class="cf" style="transform:{tf}">{inner}</div>' for tf, inner in (("translateZ(120px)", '<img src="assets/logos/claude.svg" style="width:150px;height:150px">'), ("rotateY(180deg) translateZ(120px)", ""), ("rotateY(90deg) translateZ(120px)", ""), ("rotateY(-90deg) translateZ(120px)", ""), ("rotateX(90deg) translateZ(120px)", ""), ("rotateX(-90deg) translateZ(120px)", "")))
SC["S12"] = line("lead", "But then there's the craziest one,", 12, 0, .6, 292, 50) + line("hv", "ENTREPRENEUR", 12, .75, .95, 352, 112, acc=("entrepreneur",)) + f'<div class="stage" id="st12"><div class="cube" id="cube">{faces}</div></div>'
T["S12"] = dict(t0=a[12], end=a[13])
# ---- S13 reviews
rv = "".join(f'<div class="rv" id="rv{i}"><div class="rh"><b>{n}</b><span class="stars">{"★" * s}{"☆" * (5 - s)}</span></div><div class="rl"></div><div class="rl s"></div></div>' for i, (n, s) in enumerate((("APP STORE", 2), ("G2", 2), ("CAPTERRA", 3), ("REDDIT", 1))))
SC["S13"] = line("lead", "It reads real user", 13, 0, .25, 292, 62) + line("hv", "REVIEWS", 13, .3, .5, 352, 150, acc=("reviews",)) + f'<div class="rvs" id="rvs">{rv}</div><div class="tag9">EXAMPLE REVIEWS</div>' + \
  '<div class="two"><span class="chip dk" id="ch1">MISSING FEATURES</span><span class="chip dk" id="ch2">WHAT PEOPLE HATE</span></div>'
T["S13"] = dict(t0=a[13], miss=W("missing", "missing", 13, .62), hate=W("hate", "hate", 13, .9), end=a[14])
# ---- S14 fixes -> app you can sell
fx = "".join(f'<div class="fx" id="fx{i}"><i class="ck">✓</i>{t}</div>' for i, t in enumerate(("SMS REMINDERS", "TIME-ZONE STEP", "FLAT PRICING")))
SC["S14"] = line("lead", "Then it fixes all of that,", 14, 0, .3, 284, 54) + line("hv", "AN APP", 14, .55, .6, 336, 112, acc=("app",)) + line("hv", "YOU CAN SELL.", 14, .7, .95, 470, 112, acc=("sell",)) + \
  f'<div class="wc fixc" id="fixc"><i class="sheen"></i><span class="tg">EXAMPLE FINDINGS</span>{fx}<div class="rts" id="rts">YOUR CLONE · READY TO SELL</div></div>'
T["S14"] = dict(t0=a[14], sell=W("sell", "sell", 14, .95), end=a[15])
# ---- S15 setup
SC["S15"] = line("lead", "And the setup?", 15, 0, .2, 292, 62) + line("hv", "2 STEPS.", 15, .45, .5, 352, 170, acc=("steps", "2")) + \
  '<div class="comp chat" id="chat"><div class="stp">1 · PASTE THE REPO LINK</div><div class="inp"><span id="u1">github.com/Jakeschincariol/replica-skill</span></div><div class="stp">2 · SAY “INSTALL SKILL”</div><div class="inp"><span id="u2">install skill</span></div><div class="ok" id="ok15">✓ Skill installed</div></div>'
T["S15"] = dict(t0=a[15], paste=W("paste", "paste", 15, .35), say=W("say", "say", 15, .72), end=a[16])
# ---- S16 rebrand
SC["S16"] = line("lead", "It even rebrands", 16, 0, .3, 292, 62) + line("hv", "YOUR OWN BRAND.", 16, .4, .8, 352, 100, acc=("own", "brand")) + \
  '<div class="rb"><div class="rbo" id="rbo"><div class="rbt">ORIGINAL</div>' + wf("grey") + '</div><div class="rby" id="rby"><div class="rbt on">YOUR BRAND</div>' + wf("brand") + '<div class="sw"><i style="background:#0f0f0f"></i><i style="background:#2f7d5b"></i><i style="background:#e9e6da"></i></div></div><div class="cpy" id="cpy">COPY<i class="stk2" id="cps"></i></div></div>'
T["S16"] = dict(t0=a[16], end=a[17])
SC["S17"] = line("lead", "The setup's in the", 17, 0, .4, 420, 84) + line("hv", "LINK IN BIO.", 17, .55, .9, 516, 140)
T["S17"] = dict(t0=a[17], end=a[18])
SC["S18"] = line("lead", "Want the next one?", 18, 0, .35, 400, 84) + line("hv", "FOLLOW.", 18, .5, .5, 500, 192, acc=("follow",)) + ring("rgG", 78, 492, 900, 250)
T["S18"] = dict(t0=a[18], acc=W("follow", "follow", 18, .5), end=tF)

for k in T:
    for kk, v in list(T[k].items()):
        if isinstance(v, float): T[k][kk] = round(v, 3)
T["tF"] = tF; T["D"] = D

SFX = []
def sfx(f, t, g=-13): SFX.append(dict(f=f, t=round(max(0, t), 3), g=g))
sfx("whoosh_b.ogg", T["S1"]["hit"] - .15, -11); sfx("select.ogg", T["S1"]["hit"] + .2, -14); sfx("select.ogg", T["S2"]["scan"], -14); sfx("click_a.ogg", a[3] + .8, -16)
sfx("select.ogg", T["S4"]["free"], -13); sfx("click_a.ogg", a[6] + .5, -16); sfx("riser.ogg", a[6] + .4, -18); sfx("whoosh_b.ogg", a[7] - .05, -17); sfx("click_a.ogg", a[8] + .8, -16); sfx("click_a.ogg", a[9] + .4, -16)
sfx("click_a.ogg", a[10] + .8, -16); sfx("select.ogg", T["S11"]["bug"], -14); sfx("riser.ogg", a[12] - .2, -17); sfx("whoosh_b.ogg", a[12] + .4, -15); sfx("click_a.ogg", a[13] + .6, -16)
sfx("select.ogg", T["S14"]["sell"], -14); sfx("click_a.ogg", T["S15"]["paste"], -16); sfx("select.ogg", T["S15"]["say"], -14); sfx("whoosh_b.ogg", a[17] - .1, -17); sfx("select.ogg", T["S18"]["acc"], -14)
SFX.sort(key=lambda x: x["t"]); json.dump(SFX, open(H_ + "/sfx104.json", "w"), indent=1)
NEWS = [(a[n], f"scene for line {n}") for n in range(1, 19)] + [(tF, "frame 0 returns")]
NEWS = sorted((round(t, 2), x) for t, x in NEWS)
FLAT = [(NEWS[i][0], NEWS[i + 1][0]) for i in range(len(NEWS) - 1) if NEWS[i + 1][0] - NEWS[i][0] > 2.5]
if os.environ.get("SHIP") == "1" and STALE: sys.exit("SHIP=1 refused: estimated timeline")
json.dump(dict(version="ep104", estimated_timeline=STALE, lines=[dict(n=n, text=LINES[n - 1], start=round(s(n), 3), end=round(e(n), 3)) for n in range(1, NL + 1)],
               D=D, frame0_returns=tF, sync=SRC, screens=T, buildup=dict(new_on_screen=[dict(t=t, what=x) for t, x in NEWS], flat_over_2_5s=FLAT),
               numbers_on_screen=[dict(text="11 skills, MIT, 9.7k stars on the real GitHub page", source="github.com/Jakeschincariol/replica-skill read 17.11.2026")]), open(H_ + "/cues104.json", "w"), indent=1)

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
'''
JS = r'''
gsap.registerPlugin(SplitText, DrawSVGPlugin, CustomEase);
const T=__T__, ORG='__ORG__', INK='__INK__';
/* house curves (motion-animation-principles): enter = ease-out, exit = ease-in and faster, move = in-out; landings use a
   critically damped spring: fast launch, long soft settle, never past its end state (motion-remotion-notes 1) */
const expoOut=CustomEase.create("expoOut","0.16,1,0.3,1"), expoIn=CustomEase.create("expoIn","0.7,0,0.84,0"), inOut=CustomEase.create("mvInOut","0.65,0,0.35,1");
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
function scS1(){ const o=T.S1,t=gsap.timeline(),k=Math.max(.5,o.hit-.15);
  /* frame 0: three paid apps lie flat on the floor, the Claude mark lies below them. The mark rises, then sweeps under and flicks them away one by one. */
  gsap.set('#cm1 .m3',{rotationX:58,rotationY:0,rotationZ:0});
  document.querySelectorAll('#scS1 .hv').forEach(el=>{ const w=el.querySelector('.w'), tw=Math.max(.05,parseFloat(w.dataset.t)-.1); t.fromTo(el,{scale:1.1,transformOrigin:'0% 50%'},{scale:1,duration:.5,ease:'back.out(1.7)',immediateRender:false},tw); });
  t.to('#cm1 .m3',{rotationX:50,duration:Math.max(.3,k-.1),ease:'sine.inOut'},0)
   .to('#cm1 .m3',{rotationX:0,rotationY:-10,duration:.5,ease:'power2.out'},k-.1).to('#cm1',{y:-150,duration:.5,ease:'power2.out'},k-.1);
  const FL=[{x:-950,y:-260,z:420,rotationZ:-140,rotationX:-30},{x:60,y:140,z:1100,rotationX:-150,rotationZ:40},{x:950,y:-260,z:420,rotationZ:140,rotationX:-30}];
  [0,1,2].forEach(i=>{ const ti=k+.05+i*.2;
    t.to('#cm1',{x:(i-1)*330+(i?0:-60),y:-230,duration:.25,ease:'power2.inOut'},ti-.12)
     .to('#a'+i,Object.assign({duration:1.0,ease:'power3.out'},FL[i]),ti).to('#a'+i,{opacity:0,duration:.3,ease:'power1.in'},ti+.6)
     .fromTo('#scS1 .hv',{x:0},{x:(i%2?-9:9),duration:.07,yoyo:true,repeat:3,ease:'sine.inOut',immediateRender:false},ti+.05); });
  t.to('#cm1',{x:0,y:-40,scale:1.3,duration:.7,ease:inOut},k+.7).to('#cm1 .m3',{rotationY:'+=300',duration:Math.max(.8,o.end-k-.9),ease:'sine.inOut'},k+.7)
   .set('#a0,#a1,#a2',{opacity:1,z:0,x:0,y:0,rotationX:0,rotationY:0,rotationZ:0},T.tF).set('#cm1',{x:0,y:0,scale:1},T.tF).set('#cm1 .m3',{rotationX:58,rotationY:0},T.tF)
   .add(hide('#scS1'),o.end-.24); return t; }
function scS2(){ const o=T.S2,t=gsap.timeline(); t.add(show('#scS2'),0); type(t,'#scS2',o.t0-.04);
  t.fromTo('#o2',{autoAlpha:0,y:50,rotationY:-40},{autoAlpha:1,y:0,rotationY:0,duration:.6,ease:spring,immediateRender:false},.25)
   .fromTo('#m2',{scale:0,rotation:-90,autoAlpha:0},{scale:1,rotation:0,autoAlpha:1,duration:.5,ease:spring,immediateRender:false},Math.max(.5,o.scan-o.t0-.1))
   .fromTo('#c2',{autoAlpha:0,x:0},{autoAlpha:1,x:520,duration:.8,ease:expoOut,immediateRender:false},Math.max(.6,o.scan-o.t0))
   .to('#c2 .lbl',{opacity:1,duration:.3},Math.max(1.2,o.scan-o.t0+.7)).to('#m2 .m3',{rotationY:'+=300',duration:1.4,ease:'sine.inOut'},.6).add(hide('#scS2'),o.end-o.t0-.2); return t; }
function scS3(){ const o=T.S3,t=gsap.timeline(); t.add(show('#scS3'),0); type(t,'#scS3',o.t0-.04); card(t,'#plan',.35); sheenOnce(t,'#plan .sheen',.9);
  gsap.utils.toArray('#scS3 .mk').forEach((e,i)=>t.fromTo(e,{scaleX:0},{scaleX:1,duration:.22,ease:inOut,immediateRender:false},.7+i*.1));
  drift(t,'#plan',o.end-o.t0); t.add(hide('#scS3'),o.end-o.t0-.2); return t; }
function scS4(){ const o=T.S4,t=gsap.timeline(); gsap.set('#free3,#scS4 .chip',{autoAlpha:0}); t.add(show('#scS4'),0); type(t,'#scS4',o.t0-.04);
  t.fromTo('#free3',{autoAlpha:0,scale:.6,y:60},{autoAlpha:1,scale:1,y:0,duration:.8,ease:spring,immediateRender:false},Math.max(.2,o.free-o.t0-.12))
   .fromTo('#scS4 .chip',{autoAlpha:0,y:30},{autoAlpha:1,y:0,duration:.45,stagger:.18,ease:expoOut,immediateRender:false},Math.max(.7,o.free-o.t0+.1))
   .to('#free3',{scale:1.04,duration:Math.max(1,o.end-o.t0-1),ease:'sine.inOut'},.9).add(hide('#scS4'),o.end-o.t0-.2); return t; }
function scS5(){ const o=T.S5,t=gsap.timeline(); t.add(show('#scS5'),0); type(t,'#scS5',o.t0-.04);
  t.fromTo('#sh5',{autoAlpha:0,y:50},{autoAlpha:1,y:0,duration:.6,ease:spring,immediateRender:false},.5).fromTo('#sh5',{scale:1},{scale:1.04,duration:Math.max(1,o.end-o.t0),ease:'sine.inOut',immediateRender:false},0).add(hide('#scS5'),o.end-o.t0-.2); return t; }
function scS6(){ const o=T.S6,t=gsap.timeline(); t.add(show('#scS6'),0); type(t,'#scS6',o.t0-.04);
  const e=Math.max(.9,o.eleven-o.t0);
  gsap.utils.toArray('#g11 .sk').forEach((el,i)=>t.fromTo(el,{autoAlpha:0,scale:.6,y:30},{autoAlpha:1,scale:1,y:0,duration:.4,ease:spring,immediateRender:false},.35+i*Math.max(.05,(e-.4)/11)));
  t.to('#g11 .sk b',{color:'#fff',duration:.3,stagger:.03},e).add(hide('#scS6'),o.end-o.t0-.2); return t; }
function scS7(){ const o=T.S7,t=gsap.timeline(); t.add(show('#scS7'),0); type(t,'#scS7',o.t0-.04); t.add(hide('#scS7'),o.end-o.t0-.2); return t; }
function scOrbit(){ const o=T.S7,N=11,st={a:0,p:0,f:0},ts=T.S6.eleven+.2,t=gsap.timeline();
  /* right after "it's 11" the 11 tiles flip into cubes at the same spots, fly out and ORBIT the Claude mark; cubes never spin on their own axis */
  const place=(ang,p)=>{ for(let i=0;i<N;i++){ const th=ang+i*2*Math.PI/N, z=Math.sin(th), ox=540+Math.cos(th)*400, oy=900+z*210, osc=.78+.5*(z+1)/2,
      gx=108+(i%4)*220+102, gy=640+Math.floor(i/4)*150+65, gsc=1.05, x=gx+(ox-gx)*p, y=gy+(oy-gy)*p, sc=gsc+(osc-gsc)*p;
      gsap.set('#orb'+i,{x:x-60,y:y-600-60,scale:sc,zIndex:Math.round(z*100)+200,opacity:1}); gsap.set('#cb'+i,{rotationY:-22*p,rotationX:-16*p+(1-st.f)*90}); } };
  place(0,0); gsap.set('#cm7',{x:0,y:-30,autoAlpha:0});
  t.set('#st7',{autoAlpha:1},0).to('#g11',{autoAlpha:0,duration:.08},0)
   .fromTo(st,{f:0},{f:1,duration:.42,ease:'back.out(1.5)',onUpdate:()=>place(st.a,st.p)},0)
   .fromTo(st,{p:0},{p:1,duration:.95,ease:'power3.inOut',onUpdate:()=>place(st.a,st.p)},.3)
   .fromTo(st,{a:0},{a:Math.PI*2*1.15,duration:Math.max(2,o.end-ts-.3),ease:'sine.inOut',onUpdate:()=>place(st.a,st.p)},.3)
   .fromTo('#cm7',{scale:0,autoAlpha:0},{scale:1.25,autoAlpha:1,duration:.6,ease:spring,immediateRender:false},.55)
   .to('#cm7 .m3',{rotationY:'+=360',duration:Math.max(2,o.end-ts),ease:'none'},.3)
   .to('#st7',{autoAlpha:0,duration:.22},o.end-ts-.24); t.ts=ts; return t; }
function scS8(){ const o=T.S8,t=gsap.timeline(); t.add(show('#scS8'),0); type(t,'#scS8',o.t0-.04); card(t,'#rc',.35);
  t.fromTo('#scan',{y:0,opacity:1},{y:560,duration:.9,ease:'sine.inOut',immediateRender:false},.6).to('#scan',{opacity:0,duration:.2},1.5)
   .fromTo('#scS8 .fd',{autoAlpha:0,x:-20},{autoAlpha:1,x:0,duration:.35,stagger:.16,immediateRender:false},.75).add(hide('#scS8'),o.end-o.t0-.2); return t; }
function scS9(){ const o=T.S9,t=gsap.timeline(); t.add(show('#scS9'),0); type(t,'#scS9',o.t0-.04);
  [0,1,2].forEach(i=>{ t.fromTo('#ph'+i,{autoAlpha:0,y:50},{autoAlpha:1,y:0,duration:.5,ease:expoOut,immediateRender:false},.3+i*.3)
     .fromTo('#ph'+i+' .wf>*',{opacity:0,y:10},{opacity:1,y:0,duration:.25,stagger:.1,immediateRender:false},.5+i*.3); });
  t.fromTo('#scS9 .cap9',{autoAlpha:0},{autoAlpha:1,duration:.4},1.3).add(hide('#scS9'),o.end-o.t0-.2); return t; }
function scS10(){ const o=T.S10,t=gsap.timeline(); t.add(show('#scS10'),0); type(t,'#scS10',o.t0-.04);
  gsap.set('#bk path',{drawSVG:'0%'});
  t.fromTo('#bk .phone',{autoAlpha:0,y:30},{autoAlpha:1,y:0,duration:.45,ease:expoOut,immediateRender:false},.3).to('#bk path',{drawSVG:'100%',duration:.5,ease:inOut},.6)
   .fromTo('#bk .bx',{autoAlpha:0,y:30,scale:.8},{autoAlpha:1,y:0,scale:1,duration:.45,stagger:.12,ease:spring,immediateRender:false},.8).add(hide('#scS10'),o.end-o.t0-.2); return t; }
function scS11(){ const o=T.S11,t=gsap.timeline(); t.add(show('#scS11'),0); type(t,'#scS11',o.t0-.04); card(t,'#tst',.3);
  t.fromTo('#scS11 .tr',{autoAlpha:0,x:-20},{autoAlpha:1,x:0,duration:.35,stagger:.2,immediateRender:false},.55).fromTo('#tr2 .bx2',{scale:1},{scale:1.35,duration:.22,yoyo:true,repeat:1,ease:'power2.out'},Math.max(1.2,o.bug-o.t0)).add(hide('#scS11'),o.end-o.t0-.2); return t; }
function scS12(){ const o=T.S12,t=gsap.timeline(); t.add(show('#scS12'),0); type(t,'#scS12',o.t0-.04);
  gsap.set('#cube',{rotationX:-20,rotationY:0,transformPerspective:900});
  t.fromTo('#cube',{scale:.3,autoAlpha:0},{scale:1.7,autoAlpha:1,duration:.7,ease:spring,immediateRender:false},.5)
   .to('#cube',{rotationY:560,rotationX:-34,duration:Math.max(2,o.end-o.t0-.4),ease:'sine.inOut'},.5).add(hide('#scS12'),o.end-o.t0-.2); return t; }
function scS13(){ const o=T.S13,t=gsap.timeline(); t.add(show('#scS13'),0); type(t,'#scS13',o.t0-.04);
  t.fromTo('#scS13 .rv',{autoAlpha:0,y:40,scale:.9},{autoAlpha:1,y:0,scale:1,duration:.45,stagger:.16,ease:spring,immediateRender:false},.5)
   .to('#scS13 .tag9',{opacity:1},.8)
   .to('#ch1',{opacity:1,borderColor:ORG,duration:.3},Math.max(1,o.miss-o.t0)).to('#ch2',{opacity:1,borderColor:ORG,duration:.3},Math.max(1.4,o.hate-o.t0));
  drift(t,'#rvs',o.end-o.t0); t.add(hide('#scS13'),o.end-o.t0-.2); return t; }
function scS14(){ const o=T.S14,t=gsap.timeline(); t.add(show('#scS14'),0); type(t,'#scS14',o.t0-.04); card(t,'#fixc',.4); sheenOnce(t,'#fixc .sheen',1.0);
  gsap.utils.toArray('#scS14 .fx').forEach((el,i)=>{ t.fromTo(el,{autoAlpha:0,x:-20},{autoAlpha:1,x:0,duration:.35,immediateRender:false},.7+i*.35).add(()=>el.classList.add('on'),1.0+i*.35).add(()=>el.classList.remove('on'),0); });
  t.fromTo('#rts',{autoAlpha:0,y:20},{autoAlpha:1,y:0,duration:.5,ease:spring,immediateRender:false},Math.max(2.2,o.sell-o.t0)); drift(t,'#fixc',o.end-o.t0); t.add(hide('#scS14'),o.end-o.t0-.2); return t; }
function scS15(){ const o=T.S15,t=gsap.timeline(); t.add(show('#scS15'),0); type(t,'#scS15',o.t0-.04); card(t,'#chat',.35);
  typeChars(t,'#u1',Math.max(.8,o.paste-o.t0),1.5); typeChars(t,'#u2',Math.max(2.4,o.say-o.t0+.1),.7);
  t.to('#ok15',{opacity:1,duration:.4},Math.max(3.4,o.say-o.t0+1.0)).fromTo('#chat .stp',{autoAlpha:0},{autoAlpha:1,duration:.3,stagger:.6,immediateRender:false},.6).add(hide('#scS15'),o.end-o.t0-.2); return t; }
function scS16(){ const o=T.S16,t=gsap.timeline(); t.add(show('#scS16'),0); type(t,'#scS16',o.t0-.04);
  gsap.set('#cps',{scaleX:0});
  t.fromTo('#rbo',{autoAlpha:0,x:-40},{autoAlpha:1,x:0,duration:.5,ease:expoOut,immediateRender:false},.4).fromTo('#rby',{autoAlpha:0,x:40},{autoAlpha:1,x:0,duration:.5,ease:expoOut,immediateRender:false},.8)
   .fromTo('#cpy',{autoAlpha:0},{autoAlpha:1,duration:.3},1.2).to('#cps',{scaleX:1,duration:.3,ease:inOut},1.6).add(hide('#scS16'),o.end-o.t0-.2); return t; }
const tl=gsap.timeline({paused:true});
tl.fromTo('#cam',{scale:1},{scale:1.012,duration:T.D/4,ease:'sine.inOut',yoyo:true,repeat:3},0)
  .fromTo('.bgw',{x:0,y:0},{x:-14,y:-12,duration:T.D/2,ease:'sine.inOut',yoyo:true,repeat:1},0)
  .add(scS1(),0).add(scS2(),T.S2.t0-.04).add(scS3(),T.S3.t0-.04).add(scS4(),T.S4.t0-.04).add(scS5(),T.S5.t0-.04).add(scS6(),T.S6.t0-.04).add(scS7(),T.S7.t0-.04).add(scOrbit(),T.S6.eleven+.2)
  .add(scS8(),T.S8.t0-.04).add(scS9(),T.S9.t0-.04).add(scS10(),T.S10.t0-.04).add(scS11(),T.S11.t0-.04).add(scS12(),T.S12.t0-.04).add(scS13(),T.S13.t0-.04)
  .add(scS14(),T.S14.t0-.04).add(scS15(),T.S15.t0-.04).add(scS16(),T.S16.t0-.04).add(scWords('#scS17',T.S17),T.S17.t0-.04).add(scWords('#scS18',T.S18,'rgG'),T.S18.t0-.04);
tl.fromTo('#scS1',{autoAlpha:0,filter:'blur(6px)'},{autoAlpha:1,filter:'blur(0px)',duration:.36,ease:'power2.out',immediateRender:false},T.tF+.02).to({},{duration:.001},T.D-.001);
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
open(H_ + "/out/build104.log", "w").write("\n".join(LOG) + "\n")
