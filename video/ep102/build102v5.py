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
Writes  hf/index.html, cues102.json, sfx102.json, out/build-v5.log.
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

ITEMS = [
    dict(k=1, paid="Loom", plogo="loom.png", free="Cap", flogo="cap.png", note=""),
    dict(k=2, paid="Notion", plogo="notion.png", free="AppFlowy", flogo="appflowy.svg", note=""),
    dict(k=3, paid="Intercom", plogo="intercom.svg", free="Chatwoot", flogo="chatwoot.png", note=""),
    dict(k=4, paid="Wispr Flow", plogo="wisprflow.png", free="OpenWhispr", flogo="openwhispr.svg", note=""),
    dict(k=5, paid="ElevenLabs", plogo="elevenlabs.svg", free="VoiceStudio", flogo="voicestudio.svg", note=""),
]
for it in ITEMS:
    for f in (it["plogo"], it["flogo"]): assert os.path.exists(f"{H_}/hf/assets/logos/{f}"), f"missing real logo {f} (logos/SOURCES.md)"

LINES = [l.strip() for l in open(H_ + f"/voice/lines5{os.environ.get('VAR','')}.txt") if l.strip()]
NL = len(LINES); assert NL == 9, "v5 is laid out for 9 lines"
try: C = json.load(open(H_ + f"/voice/narration-v5{os.environ.get('VAR','')}-cues.json"))
except Exception: C = []
CUE = {c["n"]: c for c in C if "n" in c}
STALE = os.environ.get("EST") == "1" or len(CUE) != NL or any(n not in CUE or norm(CUE[n]["line"]) != norm(LINES[n - 1]) for n in range(1, NL + 1))
WORDS = []
if not STALE:
    try: WORDS = [[w["word"], w["start"], w["end"]] for w in json.load(open(H_ + f"/voice/words-v5{os.environ.get('VAR','')}.json"))]
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
# ---------------------------------------------------------------- A the cube (frame 0 is complete; then the tags flip)
def fit(txt, size, mx):
    try:
        from PIL import ImageFont
        f = ImageFont.truetype(H_ + "/hf/assets/fonts/InterDisplay-Black.otf", 100)
        return min(size, 100 * mx / (f.getlength(txt) * .955))
    except Exception: return min(size, mx / (.6 * len(txt)))
# five real paid logos: 2 + 2 + the ElevenLabs tile (the big one) centred and larger, so the bottom of the safe box is used
TPOS = [(108, 556, 417, 210), (555, 556, 417, 210), (108, 782, 417, 210), (555, 782, 417, 210), (222, 1008, 636, 240)]
tiles = ""
for i, it in enumerate(ITEMS):
    x, y, w_, h_ = TPOS[i]; big = i == 4; lh = 100
    tiles += (f'<div class="tile{" big" if big else ""}" id="t{i}" style="left:{x}px;top:{y}px;width:{w_}px;height:{h_}px"><div class="lgw" style="left:26px;top:20px;width:{lh}px;height:{lh}px">{lg(it["plogo"], lh)}</div>'
              f'<div class="bd" style="left:{w_ - 98}px;top:26px;width:72px;height:72px">{TAG}{TICK}</div>'
              f'<div class="tnm" style="left:26px;top:{h_ - 92}px;font-size:{fit(it["paid"], 58, w_ - 52):.0f}px">{it["paid"]}</div></div>')
HOOK = os.environ.get("VAR", "A")
LEAD = "Stop paying" if HOOK == "A" else "You could save"
SC["A"] = line("lead", LEAD, 1, 0, .4, 282, 62, ready=True) + line("hv", "$780 A YEAR", 1, .5, 1, 352, 118, acc=("780",), ready=True) + ring("rgA", 96, 346, 372, 150) + \
          '<div class="ln lead note" style="top:492px;font-size:34px;line-height:40px;color:#6d6c66">cheapest paid plans, per person</div>' + tiles
T["A"] = dict(t0=0, free=W("price", "780", 1, .55), end=a[2])
# ---------------------------------------------------------------- B tease
SC["B"] = line("lead", "The last one is", 2, 0, .36, 380, 84) + line("hv", "INSANE.", 2, .5, .5, 476, 214, acc=("insane",)) + ring("rgB", 78, 468, 890, 250) + line("hv", "STAY FOR IT.", 2, .72, .95, 760, 128)
T["B"] = dict(t0=a[2], acc=W("insane", "insane", 2, .5), end=a[3])
# ---------------------------------------------------------------- pair card
def group(it, k):
    ps = fit(it["paid"], 96, 520); fs = fit(it["free"], 132, 560)
    return f'''<div class="grp" id="g{k}">
 <div class="prow"><div class="lt">{lg(it["plogo"], 116)}</div><div class="pn" style="font-size:{ps:.0f}px">{it["paid"]}<i class="sk"></i></div></div>
 {ARW}
 <div class="frow"><div class="lt big">{lg(it["flogo"], 150)}</div><div class="fn" style="font-size:{fs:.0f}px;line-height:{fs:.0f}px">{it["free"]}</div></div>
 <div class="free"><span class="fx">FREE</span></div></div>'''
SC["C1"] = '<div class="comp">' + "".join(group(it, it["k"]) for it in ITEMS[:2]) + "</div>"
SC["L"] = line("lead", "Still not", 4, 0, .3, 420, 100) + line("hv", "THE BIG ONE.", 4, .55, 1, 540, 124, acc=("big",))
SC["C2"] = '<div class="comp">' + "".join(group(it, it["k"]) for it in ITEMS[2:4]) + "</div>"
tNotion = W("notion", ("notion", "motion"), 3, .52); tInter = W("intercom", ("intercom", "inter"), 5, .08); tWispr = W("wispr", ("wispr", "whisper", "wisper", "wisp", "flow"), 5, .6)
PST = {1: a[3], 2: tNotion - .06, 3: tInter - .06, 4: tWispr - .06}
PFR = {1: W("cap", ("cap", "capp", "kap", "cab"), 3, .3), 2: W("appflowy", ("appflowy", "app", "apflowy", "appflow"), 3, .8),
       3: W("chatwoot", ("chatwoot", "chat", "chatwoo"), 5, .3), 4: W("openwhispr", ("openwhispr", "open", "openwhisper"), 5, .9)}
PEN = {1: PST[2], 2: a[4], 3: PST[4], 4: a[6]}
mk = lambda k: dict(k=k, t0=round(PST[k], 3), free=round(max(PFR[k], PST[k] + .34), 3), end=round(PEN[k], 3))
T["C1"] = dict(t0=a[3], end=a[4], pairs=[mk(1), mk(2)])
T["L"] = dict(t0=a[4], acc=W("bigL", "big", 4, .7), end=a[5])
T["C2"] = dict(t0=a[5], end=a[6], pairs=[mk(3), mk(4)])
# ---------------------------------------------------------------- D the big one
tBig = W("big", "big", 6, .3); tEL = W("eleven", ("elevenlabs", "eleven", "11"), 6, .62)
tVS = max(a[7] + .08, W("vs", ("voicestudio", "voice"), 7, .02)); tClone = W("clones", ("clones", "clone"), 7, .3)
SC["D1"] = line("lead", "And the", 6, 0, .12, 420, 84) + line("hv", "BIG ONE.", 6, .3, .42, 516, 206, acc=("big", "one")) + ring("rgD", 78, 508, 900, 244)
tCard5 = round(max(tEL - .14, a[6] + .75), 3)
T["D1"] = dict(t0=a[6], acc=tBig, end=tCard5)
SC["D2"] = '<div class="comp">' + group(ITEMS[4], 5) + "</div>"
tShot = round(max(tClone - .06, tVS + .95), 3)
T["D2"] = dict(t0=tCard5, end=tShot, pairs=[dict(k=5, t0=tCard5, free=round(tVS, 3), end=tShot + .3)])
SC["D3"] = line("lead", "clones your own voice,", 7, .3, .55, 300, 64) + line("hv", "ON YOUR OWN", 7, .62, .8, 376, 104) + line("hv", "MACHINE.", 7, .9, .9, 490, 104) + \
           '<div class="shot"><img src="assets/shots/voicestudio.jpg"></div>'
T["D3"] = dict(t0=tShot, end=a[8])
# ---------------------------------------------------------------- F the list card (line 8, "The setup's in the link in bio."): the saveable list, no claim about testing
rows = "".join(f'<div class="lr" style="top:{128 + i * 112}px"><div class="lt sm">{lg(it["plogo"], 50)}</div><svg class="la" viewBox="0 0 50 30"><path d="M3 15 H44 M44 15 L32 5 M44 15 L32 25" fill="none" stroke="#8d8c86" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg><div class="lt sm">{lg(it["flogo"], 60)}</div><span class="lx">{it["free"]}</span><span class="lf">FREE</span></div>' for i, it in enumerate(ITEMS))
SC["F"] = f'<div class="comp list"><div class="ltit">Save this list</div>{rows}</div>'
T["F"] = dict(t0=a[8], end=a[9])
# ---------------------------------------------------------------- G
SC["G2"] = line("lead", "Want the next one?", 9, 0, .35, 400, 84) + line("hv", "FOLLOW.", 9, .5, .5, 500, 192, acc=("follow",)) + ring("rgG", 78, 492, 900, 250)
T["G2"] = dict(t0=a[9], acc=W("follow", "follow", 9, .5), end=tF)
for k in T:
    for kk, v in list(T[k].items()):
        if isinstance(v, float): T[k][kk] = round(v, 3)
T["tF"] = tF; T["D"] = D

SFX = []
def sfx(f, t, g=-13): SFX.append(dict(f=f, t=round(max(0, t), 3), g=g))
for i in range(5): sfx("tick.ogg", .2 + i * .09, -17)
sfx("select.ogg", T["B"]["acc"], -15); sfx("select.ogg", T["L"]["acc"], -15)
for p in T["C1"]["pairs"] + T["C2"]["pairs"] + T["D2"]["pairs"]: sfx("click_a.ogg", p["free"] - .15, -16); sfx("select.ogg", p["free"] + .1, -14)
sfx("riser.ogg", a[6] - .2, -16); sfx("whoosh_b.ogg", a[8] - .1, -17); sfx("select.ogg", T["G2"]["acc"], -14)
SFX.sort(key=lambda x: x["t"]); json.dump(SFX, open(H_ + "/sfx102.json", "w"), indent=1)

pn = lambda p: ITEMS[p['k'] - 1]
NEWS = [(0, "A the cube: five real paid logos + 'Five apps you pay for. FREE TWINS EXIST!', price tags flip to ticks"),
        (a[2], "B words only: 'The last one is INSANE. STAY FOR IT.'")] + \
       [(p["t0"], f"card: {pn(p)['paid']} struck, arrow, {pn(p)['free']} at {p['free']:.2f}, FREE") for p in T["C1"]["pairs"] + T["C2"]["pairs"]] + \
       [(a[4], "words only: 'Still not THE BIG ONE.' (true: ElevenLabs/VoiceStudio comes later)"), (a[6], "D words only: 'And the BIG ONE.'"),
        (tCard5, f"card: ElevenLabs struck, arrow, VoiceStudio at {tVS:.2f}, FREE"), (tShot, "the real VoiceStudio screenshot: 'clones your own voice, ON YOUR OWN MACHINE.'"),
        (a[8], "F one card: the saveable list of five pairs ('The setup's in the link in bio')"), (a[9], "words only: 'Want the next one? FOLLOW.'"), (tF, "frame 0 returns (loop)")]
NEWS = sorted((round(t, 2), x) for t, x in NEWS)
FLAT = [(NEWS[i][0], NEWS[i + 1][0]) for i in range(len(NEWS) - 1) if NEWS[i + 1][0] - NEWS[i][0] > 2.5]
if os.environ.get("SHIP") == "1" and STALE: sys.exit("SHIP=1 refused: estimated timeline")
json.dump(dict(version="v5", estimated_timeline=STALE, lines=[dict(n=n, text=LINES[n - 1], start=round(s(n), 3), end=round(e(n), 3)) for n in range(1, NL + 1)],
               D=D, frame0_returns=tF, sync=SRC, screens=T, buildup=dict(new_on_screen=[dict(t=t, what=x) for t, x in NEWS], flat_over_2_5s=FLAT),
               numbers_on_screen=[]), open(H_ + "/cues102.json", "w"), indent=1)

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
.w.acc.rdy{{color:{ORG}}}
.ring{{overflow:visible}}
.tile{{width:417px;height:228px;background:#fff;border-radius:44px;box-shadow:0 18px 36px rgba(20,20,20,.16);will-change:transform}}
.tile>*{{position:absolute}} .lgw .lg{{border-radius:22px}}
.lgw.cal{{display:flex;flex-direction:column;align-items:center;justify-content:center}} .cwm{{display:block;width:150px;height:36px;margin-top:8px}}
.bd{{left:252px;top:62px;width:104px;height:104px;will-change:transform}} .bd svg{{position:absolute;left:0;top:0;width:100%;height:100%}} .tnm{{position:absolute;font-weight:900;letter-spacing:-.04em;color:#0f0f0f;white-space:nowrap;line-height:1.1}} .tick{{opacity:0}}
.comp{{left:108px;top:300px;width:864px;height:744px;background:{CARD};border-radius:44px;box-shadow:0 26px 50px rgba(20,20,20,.28);border:2px solid #2b2c32}}
.grp{{position:absolute;left:0;top:0;width:864px;height:744px;opacity:0;visibility:hidden}} .grp>*{{position:absolute}}
.lt{{width:150px;height:150px;border-radius:34px;background:#fff;display:flex;align-items:center;justify-content:center;flex:none}} .lt .lg{{border-radius:22px}}
.lt.big{{width:190px;height:190px;border-radius:42px}} .lt.sm{{width:72px;height:72px;border-radius:17px}} .lt.sm .lg{{border-radius:10px}}
.prow{{left:56px;top:56px;width:760px;height:150px;display:flex;align-items:center;gap:34px}}
.pn{{position:relative;font-weight:900;letter-spacing:-.04em;color:#f2f2ee;white-space:nowrap;line-height:1.1}}
.sk{{position:absolute;left:-10px;right:-10px;top:52%;height:9px;border-radius:5px;background:#f2f2ee;transform-origin:0 50%;transform:scaleX(0)}}
.arw{{left:101px;top:226px;width:60px;height:90px}}
.frow{{left:36px;top:338px;width:800px;height:190px;display:flex;align-items:center;gap:34px;opacity:0;visibility:hidden}}
.fn{{font-weight:900;letter-spacing:-.045em;color:#fff;white-space:nowrap}}
.free{{left:258px;top:540px;font-weight:900;font-size:124px;line-height:134px;letter-spacing:-.03em;color:{ORG};white-space:nowrap}}
.nt{{left:262px;top:676px;font-weight:500;font-size:44px;line-height:50px;letter-spacing:-.01em;color:#b9b8b2;white-space:nowrap;opacity:0;visibility:hidden}}
.shot{{left:108px;top:628px;width:756px;height:525px;border-radius:30px;box-shadow:0 26px 50px rgba(20,20,20,.28);overflow:hidden;background:{CARD};will-change:transform}}
.shot img{{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;transform-origin:30% 40%}}
.ltit{{position:absolute;left:44px;top:28px;font-weight:900;font-size:58px;line-height:66px;letter-spacing:-.03em;color:#fff;white-space:nowrap}}
.lr{{position:absolute;left:44px;right:44px;height:84px;display:flex;align-items:center;gap:16px;white-space:nowrap;opacity:0;visibility:hidden}}
.la{{width:46px;height:28px;flex:none}} .lx{{margin-left:10px;font-weight:900;font-size:58px;line-height:64px;letter-spacing:-.035em;color:#fff}}
.lf{{margin-left:auto;font-weight:900;font-size:42px;line-height:48px;letter-spacing:.01em;color:{ORG}}}
.lnote{{position:absolute;left:44px;bottom:26px;font-weight:500;font-size:42px;line-height:48px;letter-spacing:-.01em;color:#b9b8b2;white-space:nowrap;opacity:0;visibility:hidden}}
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
      t.fromTo(sp.chars,{yPercent:112},{yPercent:0,duration:.5,ease:expoOut,stagger:.03},at).to(sp.chars,{color:ORG,duration:.3,ease:'power1.out',stagger:.03},at+.12); }
    else t.fromTo(w,{yPercent:112,y:0},{yPercent:0,y:0,duration:.46,ease:expoOut,immediateRender:false},at); });
}
function ringDraw(t,id,at){ t.fromTo(id+' path',{drawSVG:'0%'},{drawSVG:'100%',duration:.8,ease:'power2.inOut',immediateRender:false},at) }
gsap.set('.ring:not(#rgA) path, .arw path',{drawSVG:'0%'});

/* A: the cube. Frame 0 is complete; then the six price tags flip to ticks one by one, each tile nudges (follow-through) */
function scA(){ const t=gsap.timeline({defaults:{ease:expoOut}}), bd=gsap.utils.toArray('#scA .bd');
  t.addLabel('flip',.2);
  bd.forEach((b,i)=>{ const at='flip+='+(i*.09).toFixed(2), q=gsap.utils.selector(b);
    t.to(b,{scaleX:0,duration:.14,ease:'power2.in'},at).set(q('.tag'),{autoAlpha:0},'>').set(q('.tick'),{autoAlpha:1},'<')
     .to(b,{scaleX:1,duration:.34,ease:spring},'>').fromTo('#t'+i,{y:0},{y:-9,duration:.16,ease:'power2.out',immediateRender:false},at+'+=0.06').to('#t'+i,{y:0,duration:.5,ease:spring},'>'); });
  t.fromTo('#rgA path',{drawSVG:'100%'},{drawSVG:'100%',duration:.01,immediateRender:false},0)
   .to('#scA .lead',{x:6,duration:1.6,ease:'sine.inOut'},.9)                      // slow drift while it is read
   .add(hide('#scA'),T.A.end-.24);
  return t; }
/* words-only screens: lead-in + heavy line(s), one accent, one ring */
function scWords(id,o,ringId){ const t=gsap.timeline(); t.add(show(id),0); type(t,id,o.t0-.04);
  if(ringId) ringDraw(t,'#'+ringId,(o.acc-o.t0)+.16);
  t.to(id+' .ln',{x:8,duration:Math.max(.6,o.end-o.t0-.5),ease:'sine.inOut',stagger:.06},.4)
   .add(hide(id),o.end-o.t0-.2);
  return t; }
/* one pair: same place, same motion every time. Labels: in -> swap (strike, grey, arrow, free row lands) -> free (the word FREE on the free row) */
function pair(p,first){ const g='#g'+p.k, q=gsap.utils.selector(g), t=gsap.timeline({defaults:{ease:expoOut}});
  const fx=SplitText.create(q('.fx'),{type:'chars',mask:'chars',aria:'none'});
  t.addLabel('in',0).set(g,{autoAlpha:1},'in')
   .fromTo(q('.prow'),{autoAlpha:0,x:first?0:-22},{autoAlpha:1,x:0,duration:.36,immediateRender:false},'in')
   .addLabel('swap',Math.max(.18,p.free-p.t0-.2))
   .to(q('.sk'),{scaleX:1,duration:.2,ease:inOut},'swap')
   .to(q('.prow'),{opacity:.36,duration:.26,ease:'power1.out'},'swap+=0.08')
   .to(q('.arw path'),{drawSVG:'100%',duration:.24,ease:inOut},'swap+=0.05')
   .fromTo(q('.frow'),{autoAlpha:0,y:28},{autoAlpha:1,y:0,duration:.46,ease:spring,immediateRender:false},'swap+=0.1')
   .addLabel('free','swap+=0.3')
   .fromTo(fx.chars,{yPercent:112},{yPercent:0,duration:.42,stagger:.03},'free');
  if(q('.nt').length) t.fromTo(q('.nt'),{autoAlpha:0,y:8},{autoAlpha:1,y:0,duration:.3,immediateRender:false},'free+=0.14');
  t.to(g,{autoAlpha:0,y:-12,duration:.16,ease:expoIn},p.end-p.t0-.16);
  return t; }
function scCard(id,o){ const t=gsap.timeline(); t.add(show(id),0);
  o.pairs.forEach((p,i)=>t.add(pair(p,i===0),p.t0-o.t0+(i===0?.04:0)));
  t.add(hide(id),o.end-o.t0-.2); return t; }
function scShot(){ const o=T.D3, t=gsap.timeline(); t.add(show('#scD3'),0); type(t,'#scD3',o.t0-.04);
  t.fromTo('#scD3 .shot',{y:40,autoAlpha:0},{y:0,autoAlpha:1,duration:.6,ease:spring,immediateRender:false},.05)
   .fromTo('#scD3 .shot img',{scale:1},{scale:1.07,duration:Math.max(1,o.end-o.t0),ease:'sine.inOut',immediateRender:false},0)
   .add(hide('#scD3'),o.end-o.t0-.2); return t; }
function scList(){ const o=T.F, t=gsap.timeline({defaults:{ease:expoOut}}); t.add(show('#scF'),0)
   .fromTo('#scF .lr',{autoAlpha:0,x:-20},{autoAlpha:1,x:0,duration:.4,stagger:.07,immediateRender:false},.12)
   .to('#scF .comp',{y:-8,duration:Math.max(.8,o.end-o.t0-.6),ease:'sine.inOut'},.5)
   .add(hide('#scF'),o.end-o.t0-.2); return t; }

const tl=gsap.timeline({paused:true});
tl.fromTo('#cam',{scale:1},{scale:1.012,duration:T.D/4,ease:'sine.inOut',yoyo:true,repeat:3},0)       // ambient layer only
  .fromTo('.bgw',{x:0,y:0},{x:-14,y:-12,duration:T.D/2,ease:'sine.inOut',yoyo:true,repeat:1},0)
  .add(scA(),0)
  .add(scWords('#scB',T.B,'rgB'),T.B.t0-.04)
  .add(scCard('#scC1',T.C1),T.C1.t0-.04)
  .add(scWords('#scL',T.L,null),T.L.t0-.04)
  .add(scCard('#scC2',T.C2),T.C2.t0-.04)
  .add(scWords('#scD1',T.D1,'rgD'),T.D1.t0-.04)
  .add(scCard('#scD2',T.D2),T.D2.t0)
  .add(scShot(),T.D3.t0)
  .add(scList(),T.F.t0-.04)
  .add(scWords('#scG2',T.G2,'rgG'),T.G2.t0-.04);
/* loop seam: frame 0 comes back exactly (tags, not ticks) */
tl.set('#scA .tag',{autoAlpha:1},T.tF).set('#scA .tick',{autoAlpha:0},T.tF).set('#scA .lead',{x:0},T.tF)
  .fromTo('#scA',{autoAlpha:0,y:0,filter:'blur(6px)'},{autoAlpha:1,y:0,filter:'blur(0px)',duration:.36,ease:'power2.out',immediateRender:false},T.tF+.02)
  .to({},{duration:.001},T.D-.001);
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
say(f"v5 estimated timeline={STALE}  D={D}  sfx={len(SFX)}")
say("lines: " + "  ".join(f"{n}:{s(n):.2f}-{e(n):.2f}" for n in range(1, NL + 1)))
say("sync: " + "  ".join(f"{k}={v}" for k, v in SRC.items() if k))
for t, x in NEWS: say(f"  new {t:6.2f}  {x}")
say("FLAT stretches over 2.5 s with nothing new: " + (str(FLAT) if FLAT else "none"))
open(H_ + "/out/build-v5.log", "w").write("\n".join(LOG) + "\n")
