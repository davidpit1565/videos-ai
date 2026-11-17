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
Writes  hf/index.html, cues103.json, sfx103.json, out/build103.log.
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
NL = len(LINES); assert NL == 10, "ep103 is laid out for 10 lines"
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

# ---------------------------------------------------------------- paper-tear hook
JAG = [(0, 290), (58, 322), (112, 268), (170, 334), (232, 280), (292, 338), (352, 264), (412, 322), (470, 254), (520, 300)]
JP = " ".join(f"{x},{y}" for x, y in JAG)
top_poly = "polygon(0px 0px, 520px 0px, " + ", ".join(f"{x}px {y}px" for x, y in reversed(JAG)) + ")"
bot_poly = "polygon(" + ", ".join(f"{x}px {y}px" for x, y in JAG) + ", 520px 520px, 0px 520px)"
def half(cls, poly):
    return (f'<div class="half {cls}" style="clip-path:{poly}"><img src="assets/logos/linkedin.svg" style="width:520px;height:520px">'
            f'<svg class="edge" viewBox="0 0 520 520" style="position:absolute;left:0;top:0;width:520px;height:520px;opacity:0"><polyline points="{JP}" fill="none" stroke="#f7f4ec" stroke-width="16" stroke-linejoin="round"/></svg></div>')
mark = '<img class="cmark" src="assets/logos/claude.svg">'
SC["A"] = line("lead", "Claude Code just", 1, 0, .3, 292, 62, ready=True) + line("hv", "KILLED", 1, .55, .55, 352, 200, acc=("killed",), ready=True) + \
          f'<div class="tear" id="tear">{half("ht", top_poly)}{half("hb", bot_poly)}{mark}</div>'
tKill = W("killed", "killed", 1, .6)
T["A"] = dict(t0=0, kill=tKill, end=a[2])
SC["B"] = line("lead", "Now it writes your posts.", 2, 0, .6, 380, 70) + line("hv", "FREE.", 2, .85, .85, 470, 230, acc=("free",)) + ring("rgB", 78, 462, 560, 260)
T["B"] = dict(t0=a[2], acc=W("free", "free", 2, .85), end=a[3])
SC["C"] = line("lead", "It's twelve skills,", 3, 0, .55, 292, 66) + line("hv", "NOT ONE.", 3, .7, 1, 362, 140, acc=("not",)) + '<div class="shot about"><img src="assets/shots/about.png"></div>'
T["C"] = dict(t0=a[3], acc=W("not", "not", 3, .75), end=a[4])
SC["BP"] = line("lead", "Still not", 4, 0, .3, 420, 100) + line("hv", "THE BEST PART.", 4, .5, 1, 540, 104, acc=("best",))
T["BP"] = dict(t0=a[4], end=a[5])
POST = ["Here is every line item, from the pricing pages, nothing rounded:",
        "Loom Business: $18 a month, $216 a year", "Notion Plus: $10 a month, $120 a year", "Intercom Essential: $19 a month on the yearly rate, $228 a year",
        "Wispr Flow Pro: $12 a month on the yearly rate, $144 a year", "ElevenLabs Starter: $6 a month, $72 a year", "Total: $780."]
prow = "".join(f'<div class="pl{" pi" if i == 0 else ""}{" pt" if i == len(POST) - 1 else ""}">{t}</div>' for i, t in enumerate(POST))
SC["E"] = line("lead", "I gave it my numbers.", 5, 0, .3, 292, 62) + f'<div class="post"><div class="pbig">$780</div>{prow}</div>'
tNum = W("numbers", "numbers", 5, .22); tWrote = W("wrote", ("wrote", "rote"), 5, .85)
T["E"] = dict(t0=a[5], card=round(tNum - .05, 3), wrote=tWrote, end=a[6])
tHook = W("hook", "hook", 6, .2); tVoice = W("voice", ("voice", "boys"), 6, .55); tWith = W("without", ("without", "with"), 6, .85)
def ln3(txt, top, t, acc=False):
    ws = txt.split(); out = []
    for k, w in enumerate(ws):
        out.append(f'<span class="m"><span class="w{" acc" if acc else ""}" data-t="{t + k * .12:.3f}">{w}</span></span>')
    return f'<div class="ln hv" style="top:{top}px;font-size:104px;line-height:116px">{"".join(out)}</div>'
SC["F"] = ln3("PICKS THE HOOK.", 380, tHook - .5) + ln3("FIXES THE VOICE.", 520, tVoice - .5) + ln3("YOU APPROVE.", 660, tWith - .1, acc=True)
T["F"] = dict(t0=a[6], end=a[7])
tCraz = W("craziest", ("craziest", "crazy", "craziest"), 7, .05); tRead = W("reads", ("reads", "read", "reeds"), 7, .4)
SC["G"] = line("lead", "But the craziest one?", 7, 0, .3, 292, 62) + line("hv", "HOOK", 7, .35, .35, 360, 150, acc=("hook",)) + line("hv", "EXTRACTOR", 7, .4, .4, 534, 150) + \
          '<div class="xcard"><div class="xin"><i></i><i></i><i></i><i></i></div><svg class="xar" viewBox="0 0 60 90"><path d="M30 6 V78 M8 54 L30 78 L52 54" fill="none" stroke="#f2f2ee" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg><div class="xout"><span>F7</span> Odd-Precision Money Ledger</div></div>'
T["G"] = dict(t0=a[7], acc=W("hook7", "hook", 7, .35), card=round(max(tRead - .1, a[7] + 2.0), 3), end=a[8])
steps = ["Open Claude Code", "Add the skills", "Install"]
srow = "".join(f'<div class="st" style="top:{40 + i * 168}px"><b>{i + 1}</b><span>{t}</span></div>' for i, t in enumerate(steps))
SC["H"] = line("lead", "Setup takes", 8, 0, .3, 292, 62) + line("hv", "THREE STEPS.", 8, .5, 1, 360, 120, acc=("three",)) + f'<div class="comp steps">{srow}</div>'
T["H"] = dict(t0=a[8], end=a[9])
SC["I"] = line("lead", "The setup's in the", 9, 0, .4, 420, 84) + line("hv", "LINK IN BIO.", 9, .55, .9, 516, 140)
T["I"] = dict(t0=a[9], end=a[10])
SC["J"] = line("lead", "Want the next one?", 10, 0, .35, 400, 84) + line("hv", "FOLLOW.", 10, .5, .5, 500, 192, acc=("follow",)) + ring("rgG", 78, 492, 900, 250)
T["J"] = dict(t0=a[10], acc=W("follow", "follow", 10, .5), end=tF)
for k in T:
    for kk, v in list(T[k].items()):
        if isinstance(v, float): T[k][kk] = round(v, 3)
T["tF"] = tF; T["D"] = D

SFX = []
def sfx(f, t, g=-13): SFX.append(dict(f=f, t=round(max(0, t), 3), g=g))
sfx("whoosh_b.ogg", T["A"]["kill"] - .05, -11); sfx("select.ogg", T["A"]["kill"] + .25, -14)
sfx("select.ogg", T["B"]["acc"], -15); sfx("select.ogg", T["C"]["acc"], -15)
sfx("click_a.ogg", T["E"]["card"], -16); sfx("select.ogg", T["E"]["wrote"], -14)
for t in (tHook, tVoice, tWith): sfx("click_a.ogg", t, -16)
sfx("riser.ogg", a[7] - .2, -16); sfx("select.ogg", T["G"]["card"], -14); sfx("whoosh_b.ogg", a[9] - .1, -17); sfx("select.ogg", T["J"]["acc"], -14)
SFX.sort(key=lambda x: x["t"]); json.dump(SFX, open(H_ + "/sfx103.json", "w"), indent=1)
NEWS = [(0, "A hook: 'Claude Code just KILLED' + the LinkedIn tile, torn like paper on the verb, Claude mark appears"), (a[2], "B words: 'Now it writes your posts. FREE.'"),
        (a[3], "C real GitHub About text: '12 Claude Code and Codex skills ... MIT'"), (a[4], "D words: 'Still not THE BEST PART.' (true: the test post and the Hook Extractor come next)"),
        (a[5], "E the real test post from our run, '$780' first, ledger lines"), (a[6], "F three beats: picks the hook / fixes the voice / you approve"),
        (a[7], "G Hook Extractor: viral post -> formula F7 (a real formula name from the project's own reference)"), (a[8], "H three setup steps"), (a[9], "I link in bio"), (a[10], "J follow"), (tF, "frame 0 returns")]
NEWS = sorted((round(t, 2), x) for t, x in NEWS)
FLAT = [(NEWS[i][0], NEWS[i + 1][0]) for i in range(len(NEWS) - 1) if NEWS[i + 1][0] - NEWS[i][0] > 2.5]
if os.environ.get("SHIP") == "1" and STALE: sys.exit("SHIP=1 refused: estimated timeline")
json.dump(dict(version="ep103", estimated_timeline=STALE, lines=[dict(n=n, text=LINES[n - 1], start=round(s(n), 3), end=round(e(n), 3)) for n in range(1, NL + 1)],
               D=D, frame0_returns=tF, sync=SRC, screens=T, buildup=dict(new_on_screen=[dict(t=t, what=x) for t, x in NEWS], flat_over_2_5s=FLAT),
               numbers_on_screen=[dict(text="$780 etc (test post)", source="channel/episode-102-linkedin-test-post.txt; prices from official pricing pages read 16.11.2026")]), open(H_ + "/cues103.json", "w"), indent=1)

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
.bd{{left:252px;top:62px;width:104px;height:104px;will-change:transform}} .bd svg{{position:absolute;left:0;top:0;width:100%;height:100%}} .tpr{{position:absolute;font-weight:900;font-size:52px;line-height:56px;letter-spacing:-.04em;color:#0f0f0f;white-space:nowrap}} .tpr span{{font-size:30px;font-weight:500;letter-spacing:0;color:#6d6c66;margin-left:4px}} .stk{{position:absolute;left:-8px;top:50%;height:9px;width:calc(100% + 16px);border-radius:5px;background:{ORG};transform-origin:0 50%}} .stk.big{{left:104px;top:486px;width:610px;height:20px}} .tpr .stk{{width:calc(100% + 12px)}} .tnm{{position:absolute;font-weight:900;letter-spacing:-.04em;color:#0f0f0f;white-space:nowrap;line-height:1.1}} .tick{{opacity:0}}
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

.tear{{left:280px;top:640px;width:520px;height:520px}} .tear>*{{position:absolute;left:0;top:0}} .half{{width:520px;height:520px;will-change:transform,opacity}}
.half img{{position:absolute;left:0;top:0}} .cmark{{width:240px;height:240px;left:140px!important;top:140px!important;opacity:0}}
.about{{left:150px;top:560px;width:780px;height:627px}}
.post{{left:108px;top:372px;width:864px;height:830px;background:#fff;border-radius:34px;box-shadow:0 26px 50px rgba(20,20,20,.22);padding:34px 40px;opacity:0;visibility:hidden}}
.pbig{{font-weight:900;font-size:168px;line-height:176px;letter-spacing:-.05em;color:{INK}}}
.pl{{font-weight:500;font-size:34px;line-height:44px;color:#222;margin-top:20px;letter-spacing:-.005em;opacity:0}} .pl.pi{{color:#666;margin-top:12px}} .pl.pt{{font-weight:900;font-size:44px;margin-top:26px;color:{INK}}}
.xcard{{left:108px;top:760px;width:864px;height:430px;background:{CARD};border-radius:44px;box-shadow:0 26px 50px rgba(20,20,20,.28);opacity:0;visibility:hidden}}
.xin{{position:absolute;left:60px;top:44px;width:744px}} .xin i{{display:block;height:20px;border-radius:10px;background:#3a3b42;margin-bottom:18px}} .xin i:nth-child(2){{width:84%}} .xin i:nth-child(3){{width:92%}} .xin i:nth-child(4){{width:55%}}
.xar{{position:absolute;left:402px;top:190px;width:56px;height:84px}}
.xout{{position:absolute;left:60px;top:296px;width:744px;font-weight:900;font-size:46px;line-height:70px;letter-spacing:-.04em;color:#fff;white-space:nowrap}} .xout span{{color:{ORG};margin-right:14px}}
.steps{{left:108px;top:560px;width:864px;height:560px}} .st{{position:absolute;left:44px;right:44px;height:140px;display:flex;align-items:center;gap:34px;opacity:0}}
.st b{{width:96px;height:96px;border-radius:48px;background:{ORG};color:#fff;font-weight:900;font-size:60px;line-height:96px;text-align:center;flex:none}} .st span{{font-weight:900;font-size:68px;letter-spacing:-.04em;color:#fff;white-space:nowrap}}
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
gsap.set('.ring path, .arw path',{drawSVG:'0%'}); gsap.set('.stk',{scaleX:0,rotation:-3}); gsap.set('#bigstk',{rotation:-4});

/* A: the cube. Frame 0 is complete; then the six price tags flip to ticks one by one, each tile nudges (follow-through) */
function scA(){ const t=gsap.timeline(), k=T.A.kill;
  gsap.set('.cmark',{scale:.2});
  t.fromTo('#tear',{scale:1},{scale:1.04,duration:Math.max(.3,k-.1),ease:'sine.inOut',immediateRender:false},0)
   .set('.edge',{opacity:1},k).to('.ht',{x:210,y:-70,rotation:13,duration:.95,ease:expoOut},k)
   .to('.hb',{x:-210,y:170,rotation:-12,duration:.95,ease:expoOut},k)
   .to('.half',{opacity:0,duration:.3,ease:'power1.in'},k+.5)
   .to('.cmark',{opacity:1,scale:1,duration:.7,ease:spring},k+.25)
   .to('.cmark',{rotation:90,duration:T.A.end-k,ease:'sine.inOut'},k+.3)
   .add(hide('#scA'),T.A.end-.24);
  return t; }
function scWords(id,o,ringId){ const t=gsap.timeline(); t.add(show(id),0); type(t,id,o.t0-.04);
  if(ringId) ringDraw(t,'#'+ringId,(o.acc-o.t0)+.16);
  t.to(id+' .ln',{x:8,duration:Math.max(.6,o.end-o.t0-.5),ease:'sine.inOut',stagger:.06},.4)
   .add(hide(id),o.end-o.t0-.2);
  return t; }
function scAbout(){ const o=T.C, t=gsap.timeline(); t.add(show('#scC'),0); type(t,'#scC',o.t0-.04);
  t.fromTo('#scC .shot',{y:40,autoAlpha:0},{y:0,autoAlpha:1,duration:.6,ease:spring,immediateRender:false},.5)
   .fromTo('#scC .shot img',{scale:1},{scale:1.05,duration:Math.max(1,o.end-o.t0),ease:'sine.inOut',immediateRender:false},0)
   .add(hide('#scC'),o.end-o.t0-.2); return t; }
function scPost(){ const o=T.E, t=gsap.timeline({defaults:{ease:expoOut}}); t.add(show('#scE'),0); type(t,'#scE',o.t0-.04);
  const c=Math.max(.15,o.card-o.t0);
  t.fromTo('#scE .post',{autoAlpha:0,y:40},{autoAlpha:1,y:0,duration:.55,ease:spring,immediateRender:false},c);
  const n=document.querySelectorAll('#scE .pl').length, span=Math.max(2,o.end-o.t0-c-1.2);
  gsap.utils.toArray('#scE .pl').forEach((el,i)=>t.fromTo(el,{autoAlpha:0,y:14},{autoAlpha:1,y:0,duration:.4,immediateRender:false},c+.5+i*(span/n)));
  t.to('#scE .post',{y:-10,duration:Math.max(.8,o.end-o.t0-c),ease:'sine.inOut'},c+.3)
   .add(hide('#scE'),o.end-o.t0-.2); return t; }
function scThree(){ const o=T.F, t=gsap.timeline(); t.add(show('#scF'),0); type(t,'#scF',o.t0-.04);
  t.to('#scF .ln',{x:8,duration:Math.max(.6,o.end-o.t0-.5),ease:'sine.inOut',stagger:.08},.4).add(hide('#scF'),o.end-o.t0-.2); return t; }
function scExtract(){ const o=T.G, t=gsap.timeline(); t.add(show('#scG'),0); type(t,'#scG',o.t0-.04);
  t.fromTo('#scG .xcard',{autoAlpha:0,y:40},{autoAlpha:1,y:0,duration:.6,ease:spring,immediateRender:false},Math.max(.9,o.card-o.t0))
   .fromTo('#scG .xin i',{scaleX:0},{scaleX:1,transformOrigin:'0 50%',duration:.5,stagger:.09,ease:inOut,immediateRender:false},Math.max(1.1,o.card-o.t0+.1))
   .fromTo('#scG .xar',{autoAlpha:0,y:-10},{autoAlpha:1,y:0,duration:.35,immediateRender:false},Math.max(1.6,o.card-o.t0+.5))
   .fromTo('#scG .xout',{autoAlpha:0,y:16},{autoAlpha:1,y:0,duration:.5,immediateRender:false},Math.max(1.9,o.card-o.t0+.8))
   .add(hide('#scG'),o.end-o.t0-.2); return t; }
function scSteps(){ const o=T.H, t=gsap.timeline({defaults:{ease:expoOut}}); t.add(show('#scH'),0); type(t,'#scH',o.t0-.04);
  t.fromTo('#scH .st',{autoAlpha:0,x:-26},{autoAlpha:1,x:0,duration:.45,stagger:.16,immediateRender:false},.35).add(hide('#scH'),o.end-o.t0-.2); return t; }

const tl=gsap.timeline({paused:true});
tl.fromTo('#cam',{scale:1},{scale:1.012,duration:T.D/4,ease:'sine.inOut',yoyo:true,repeat:3},0)
  .fromTo('.bgw',{x:0,y:0},{x:-14,y:-12,duration:T.D/2,ease:'sine.inOut',yoyo:true,repeat:1},0)
  .add(scA(),0)
  .add(scWords('#scB',T.B,'rgB'),T.B.t0-.04)
  .add(scAbout(),T.C.t0-.04)
  .add(scWords('#scBP',T.BP),T.BP.t0-.04)
  .add(scPost(),T.E.t0-.04)
  .add(scThree(),T.F.t0-.04)
  .add(scExtract(),T.G.t0-.04)
  .add(scSteps(),T.H.t0-.04)
  .add(scWords('#scI',T.I),T.I.t0-.04)
  .add(scWords('#scJ',T.J,'rgG'),T.J.t0-.04);
tl.set('.half',{x:0,y:0,rotation:0,opacity:1},T.tF).set('.edge',{opacity:0},T.tF).set('.cmark',{opacity:0,scale:.2,rotation:0},T.tF)
  .fromTo('#scA',{autoAlpha:0,filter:'blur(6px)'},{autoAlpha:1,filter:'blur(0px)',duration:.36,ease:'power2.out',immediateRender:false},T.tF+.02)
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
open(H_ + "/out/build103.log", "w").write("\n".join(LOG) + "\n")
