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
Writes  hf/index.html, cues103.json, sfxT.json, out/buildT.log.
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

LINES = [l.strip() for l in open(H_ + "/voice/linesT.txt") if l.strip()]
NL = len(LINES); assert NL == 9, "laid out for 9 lines"
try: C = json.load(open(H_ + "/voice/narrationT-cues.json"))
except Exception: C = []
CUE = {c["n"]: c for c in C if "n" in c}
STALE = os.environ.get("EST") == "1" or len(CUE) != NL or any(n not in CUE or norm(CUE[n]["line"]) != norm(LINES[n - 1]) for n in range(1, NL + 1))
WORDS = []
if not STALE:
    try: WORDS = [[w["word"], w["start"], w["end"]] for w in json.load(open(H_ + "/voice/wordsT.json"))]
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


# ---------------------------------------------------------------- A hook: whole LinkedIn tile, the Claude mark cuts it straight, corner to corner; two clean halves part. No trail, no strips.
TS = 540; TX, TY = 270, 668
def wspan(txt, n, fr0, fr1, cls=""):
    ws = txt.split(); out = []
    for i, w in enumerate(ws):
        t_ = W("", norm(w), n, fr0 + (fr1 - fr0) * (i / (len(ws) - 1) if len(ws) > 1 else 0), log=False)
        out.append(f'<span class="m"><span class="w rdy{cls}" data-t="{t_:.3f}">{w}</span></span>')
    return "".join(out)
SC["A"] = ('<div class="ln hv hrow" style="top:286px;font-size:112px;line-height:120px">' + wspan("LINKEDIN POSTS", 1, 0, .3, "") + '</div>'
           '<div class="ln lead hrow" style="top:422px;font-size:92px;line-height:100px">' + wspan("written by Claude", 1, .4, .65, "") + '</div>'
           '<div class="pst" id="pst"><i class="sheen"></i><div class="phd"><img class="plk" src="assets/logos/linkedin.svg"><div class="pnm"><b></b><u></u></div></div>'
           '<div class="pbr"><i id="pb0"></i><i id="pb1"></i><i id="pb2"></i><i id="pb3"></i></div><span class="cur" id="cur"></span></div>'
           '<img class="cmk2" id="cm2" src="assets/logos/claude.svg">'
           '<div class="ln hv hrow frw" id="frw" style="top:1000px;font-size:200px;line-height:212px">' + wspan("FREE", 1, .85, .85, " frc") + '</div>')
tFree = W("free", "free", 1, .85); tPosts = W("posts", "posts", 1, .6)
T["A"] = dict(t0=0, free=tFree, posts=tPosts, end=a[2])
# ---------------------------------------------------------------- B the promise: three big colour cards fly in as spoken
cardsB = [("1", "Posts", "#0A66C2"), ("2", "Replies", ORG), ("3", "Your profile", "#111111")]
rb = "".join(f'<div class="cd" id="cd{i}" style="top:{330 + i * 250}px;background:{c}"><i class="sheen"></i><b>{n}</b><span>{t}</span></div>' for i, (n, t, c) in enumerate(cardsB))
SC["B"] = rb
tB1 = W("b_posts", "posts", 2, .22); tB2 = W("b_replies", "replies", 2, .45); tB3 = W("b_profile", "profile", 2, .78)
T["B"] = dict(t0=a[2], r1=tB1, r2=tB2, r3=tB3, end=a[3])
# ---------------------------------------------------------------- C posts: header word + the real post typing
POSTC = [("$780", "pbig"), ("That is what five apps cost a year, if you pay the cheapest paid plan of each.", "pl"),
         ("Here is every line item, from the pricing pages, nothing rounded:", "pl pi"), ("Loom Business: $18 a month, $216 a year", "pl"), ("Notion Plus: $10 a month, $120 a year", "pl"), ("Total: $780.", "pl pt")]
pc = "".join(f'<div class="{c} ty">{t}</div>' for t, c in POSTC)
SC["C"] = line("hv", "POSTS", 3, .0, .0, 292, 120, acc=("posts",)) + f'<div class="wc post" id="wcC"><i class="sheen"></i><span class="tg">DRAFT</span>{pc}<div class="wait">Waits for your OK.</div></div>'
T["C"] = dict(t0=a[3], hook=W("c_hook", "hook", 3, .22), live=W("c_live", ("live", "love"), 3, .7), end=a[4])
# ---------------------------------------------------------------- D replies: an example post, the reply typing
SC["RP"] = line("hv", "REPLIES", 4, .0, .0, 292, 120, acc=("replies",)) + \
          '<div class="wc ex"><i class="sheen"></i><span class="tg">EXAMPLE POST</span><div class="exp">My first freelance client did not come from a post. It came from a comment I left under someone else\'s post.</div></div>' + \
          '<div class="wc rp" id="wcD"><i class="sheen"></i><span class="tg">DRAFT REPLY</span><div class="rpt ty">Same here, and I think the reason is simple: a useful comment under a big post is read by that author\'s whole audience, while your own post only reaches your followers. What did your comment say that made them reach out?</div></div>'
T["RP"] = dict(t0=a[4], end=a[5])
# ---------------------------------------------------------------- E+F profile: before, strike, after
tAfter = W("after", "after", 6, .3); tBrand = W("brand", "brand", 6, .45)
SC["E"] = line("lead", "But the", 5, 0, .3, 292, 62) + line("hv", "PROFILE?", 5, .45, .45, 352, 150, acc=("profile",)) + \
          '<div class="wc pf" id="wcE"><i class="sheen"></i><span class="tg">EXAMPLE PROFILE</span><div class="av"></div><div class="lab">BEFORE</div><div class="hd bef" id="hbef">Freelance designer<i class="stk2" id="hstk"></i></div>' + \
          '<div class="lab aft" id="laft">AFTER</div><div class="hd afr ty" id="haft">Brand designer | I help local cafes turn menus into packaging people photograph</div></div>'
T["E"] = dict(t0=a[5], acc=W("e_profile", "profile", 5, .4), after=tAfter, brand=tBrand, end=a[7])
# ---------------------------------------------------------------- G setup
steps = ["Open Claude Code", "Add the skills", "Install"]
srow = "".join(f'<div class="st" style="top:{40 + i * 168}px"><b>{i + 1}</b><span>{t}</span></div>' for i, t in enumerate(steps))
SC["H"] = line("lead", "Free. Open source.", 7, 0, .5, 292, 62) + line("hv", "3 STEPS.", 7, .6, 1, 360, 150, acc=("steps", "3")) + f'<div class="comp steps">{srow}</div>'
T["H"] = dict(t0=a[7], end=a[8])
SC["I"] = line("lead", "The setup's in the", 8, 0, .4, 420, 84) + line("hv", "LINK IN BIO.", 8, .55, .9, 516, 140)
T["I"] = dict(t0=a[8], end=a[9])
SC["J"] = line("lead", "Want the next one?", 9, 0, .35, 400, 84) + line("hv", "FOLLOW.", 9, .5, .5, 500, 192, acc=("follow",)) + ring("rgG", 78, 492, 900, 250)
T["J"] = dict(t0=a[9], acc=W("follow", "follow", 9, .5), end=tF)
for k in T:
    for kk, v in list(T[k].items()):
        if isinstance(v, float): T[k][kk] = round(v, 3)
T["tF"] = tF; T["D"] = D

SFX = []
def sfx(f, t, g=-13): SFX.append(dict(f=f, t=round(max(0, t), 3), g=g))
sfx("whoosh_b.ogg", .02, -13); sfx("select.ogg", T["A"]["free"], -14)
for k in ("r1", "r2", "r3"): sfx("click_a.ogg", T["B"][k], -15)
sfx("click_a.ogg", T["C"]["hook"], -16); sfx("select.ogg", T["C"]["live"], -15)
sfx("click_a.ogg", a[4] + .3, -16); sfx("select.ogg", T["E"]["acc"], -15); sfx("select.ogg", tAfter + .1, -14)
sfx("riser.ogg", a[5] - .2, -17); sfx("whoosh_b.ogg", a[8] - .1, -17); sfx("select.ogg", T["J"]["acc"], -14)
SFX.sort(key=lambda x: x["t"]); json.dump(SFX, open(H_ + "/sfxT.json", "w"), indent=1)
NEWS = [(0, "A hook: Claude writes LinkedIn posts, FREE: real marks, a post being written"), (a[2], "B three rows light up: posts, replies, your profile"),
        (a[3], "C the real post types ($780 first), DRAFT, waits for your OK"), (a[4], "D example post + our reply types"), (a[5], "E profile card: before"),
        (tAfter, "F before struck, after types"), (a[7], "G free, open source, 3 steps"), (a[8], "I link in bio"), (a[9], "J follow"), (tF, "frame 0 returns")]
NEWS = sorted((round(t, 2), x) for t, x in NEWS)
FLAT = [(NEWS[i][0], NEWS[i + 1][0]) for i in range(len(NEWS) - 1) if NEWS[i + 1][0] - NEWS[i][0] > 2.5]
if os.environ.get("SHIP") == "1" and STALE: sys.exit("SHIP=1 refused: estimated timeline")
json.dump(dict(version="ep103t", estimated_timeline=STALE, lines=[dict(n=n, text=LINES[n - 1], start=round(s(n), 3), end=round(e(n), 3)) for n in range(1, NL + 1)],
               D=D, frame0_returns=tF, sync=SRC, screens=T, buildup=dict(new_on_screen=[dict(t=t, what=x) for t, x in NEWS], flat_over_2_5s=FLAT),
               numbers_on_screen=[dict(text="$780 etc (test post)", source="channel/episode-102-linkedin-test-post.txt; prices from official pricing pages read 16.11.2026")]), open(H_ + "/cuesT.json", "w"), indent=1)

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
#scA .frc.w.rdy{{color:{ORG}}}
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

.cc{{position:absolute;left:108px;top:286px;width:58px;height:58px}}
#scA{{overflow:visible}} .hrow{{left:0px!important;width:1080px;text-align:center;display:flex;justify-content:center;align-items:center;gap:26px}} .hrow .m{{margin-right:0}} .cc2{{width:96px;height:96px;flex:none}}
.lkw{{left:270px;top:668px;width:540px;height:540px;filter:drop-shadow(0 20px 30px rgba(20,20,20,.3))}} .whole{{position:absolute;left:0;top:0;width:540px;height:540px}}
.hl{{position:absolute;left:0;top:0;width:540px;height:540px;opacity:0;will-change:transform,opacity}} .hul{{clip-path:polygon(0px 0px,542px 0px,0px 542px)}} .hlr{{clip-path:polygon(542px 0px,542px 542px,0px 542px)}} .lk{{position:absolute;left:0;top:0;width:540px;height:540px}}
.pst{{left:108px;top:610px;width:864px;height:370px;background:#fff;border-radius:34px;box-shadow:0 26px 50px rgba(20,20,20,.22);overflow:hidden;will-change:transform}}
.phd{{position:absolute;left:40px;top:34px;width:780px;height:92px;display:flex;align-items:center;gap:26px}} .plk{{width:92px;height:92px;border-radius:18px;flex:none}}
.pnm b{{display:block;width:300px;height:22px;border-radius:11px;background:#2a2a2a}} .pnm u{{display:block;width:190px;height:16px;border-radius:8px;background:#c9c7bf;margin-top:14px}}
.pbr{{position:absolute;left:40px;top:160px;width:784px}} .pbr i{{display:block;height:24px;border-radius:12px;background:#d9d7cf;margin-bottom:24px;transform-origin:0 50%;will-change:transform}} .pbr i:nth-child(1){{width:784px}} .pbr i:nth-child(2){{width:740px}} .pbr i:nth-child(3){{width:660px}} .pbr i:nth-child(4){{width:420px;background:#0A66C2}}
.cur{{position:absolute;left:40px;top:262px;width:6px;height:36px;border-radius:3px;background:#0A66C2}}
.cmk2{{left:760px;top:540px;width:190px;height:190px;will-change:transform;filter:drop-shadow(0 12px 18px rgba(20,20,20,.25))}}
.frw .frc{{color:{ORG}}}
.cmk{{left:60px;top:1000px;width:300px;height:300px;will-change:transform}}
.cd{{position:absolute;left:108px;width:864px;height:210px;border-radius:44px;box-shadow:0 26px 50px rgba(20,20,20,.3);display:flex;align-items:center;gap:36px;padding-left:44px;overflow:hidden;opacity:0;visibility:hidden}}
.cd b{{width:110px;height:110px;border-radius:55px;background:rgba(255,255,255,.22);color:#fff;font-weight:900;font-size:68px;line-height:110px;text-align:center;flex:none}} .cd span{{font-weight:900;font-size:104px;letter-spacing:-.045em;color:#fff;white-space:nowrap}}
.pcard{{left:108px;top:640px;width:864px;height:300px;background:{CARD};border-radius:44px;box-shadow:0 26px 50px rgba(20,20,20,.28);padding:48px 52px;opacity:0;visibility:hidden}}
.pt{{font-weight:500;font-size:50px;line-height:64px;color:#f2f2ee;letter-spacing:-.01em}} .ty .c{{opacity:0}}
.rows{{left:108px;top:330px;width:864px;height:640px}} .rw{{position:absolute;left:44px;right:44px;height:140px;display:flex;align-items:center;gap:34px;opacity:.28}}
.rw b{{width:96px;height:96px;border-radius:48px;background:#3a3b42;color:#fff;font-weight:900;font-size:56px;line-height:96px;text-align:center;flex:none}} .rw span{{font-weight:900;font-size:84px;letter-spacing:-.045em;color:#fff;white-space:nowrap}}
.wc{{position:absolute;left:108px;width:864px;background:#fff;border-radius:34px;box-shadow:0 26px 50px rgba(20,20,20,.22);padding:34px 40px;opacity:0;visibility:hidden}}
.wc{{overflow:hidden}} .sheen{{position:absolute;top:-20%;left:0;width:160px;height:140%;background:linear-gradient(100deg,rgba(255,255,255,0),rgba(255,255,255,.75),rgba(255,255,255,0));transform:translateX(-300px) skewX(-12deg);opacity:.9;pointer-events:none}} .ex .sheen{{background:linear-gradient(100deg,rgba(255,255,255,0),rgba(255,255,255,.5),rgba(255,255,255,0))}} .tg{{position:absolute;right:30px;top:22px;font-weight:500;font-size:24px;letter-spacing:.06em;color:#8a8982;border:2px solid #cfcdc4;border-radius:8px;padding:2px 10px}}
.post{{top:450px;height:790px}} .pbig{{font-weight:900;font-size:150px;line-height:160px;letter-spacing:-.05em;color:{INK}}}
.pl{{font-weight:500;font-size:36px;line-height:46px;color:#222;margin-top:18px}} .pl.pi{{color:#666}} .pl.pt{{font-weight:900;font-size:46px;margin-top:24px;color:{INK}}} .wait{{position:absolute;left:40px;bottom:26px;font-size:30px;color:#8a8982;opacity:0}}
.ex{{top:440px;height:230px;background:#e7e5dd;box-shadow:none}} .exp{{font-weight:500;font-size:34px;line-height:44px;color:#444;margin-top:34px}}
.rp{{top:700px;height:520px}} .rpt{{font-weight:500;font-size:37px;line-height:48px;color:#111;margin-top:36px}}
.pf{{top:560px;height:660px}} .av{{width:130px;height:130px;border-radius:65px;background:#d8d6cd;margin-top:30px}}
.lab{{font-weight:900;font-size:30px;letter-spacing:.08em;color:#8a8982;margin-top:34px}} .hd{{position:relative;font-weight:900;font-size:62px;line-height:72px;letter-spacing:-.04em;color:{INK};margin-top:8px;display:inline-block}}
.stk2{{position:absolute;left:-6px;right:-6px;top:52%;height:9px;border-radius:5px;background:{ORG};transform-origin:0 50%}} .lab.aft{{color:{ORG};opacity:0}} .hd.afr{{font-size:54px;line-height:64px}}
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
function scA(){ const t=gsap.timeline(), A=T.A;
  /* frame 0 is complete and already moving: the Claude mark turns, the post lines are being written, a cursor blinks, a sheen runs over the card */
  const st0=()=>{ gsap.set('#pb0,#pb1',{scaleX:1}); gsap.set('#pb2',{scaleX:.45}); gsap.set('#pb3',{scaleX:0}); gsap.set('#cm2',{rotation:0,scale:1}); gsap.set('#pst',{y:0,scale:1}); gsap.set('#frw',{scale:1}); };
  st0();
  t.to('#cm2',{rotation:330,duration:A.end,ease:'sine.inOut'},0)
   .to('#pb2',{scaleX:1,duration:.7,ease:'power2.inOut'},0).to('#pb3',{scaleX:1,duration:.8,ease:'power2.inOut'},.55)
   .to('#cur',{x:425,duration:.8,ease:'power2.inOut'},.55)
   .fromTo('#cur',{opacity:1},{opacity:0,duration:.2,repeat:5,yoyo:true,ease:'none'},1.3)
   .fromTo('#pst .sheen',{x:-320},{x:1100,duration:1.3,ease:'sine.inOut',immediateRender:false},.1)
   .fromTo('#pst',{y:0},{y:-10,duration:A.end,ease:'sine.inOut'},0)
   .fromTo('#frw',{scale:1},{scale:1.07,duration:.28,ease:'power2.out',transformOrigin:'540px 130px',immediateRender:false},Math.max(0,A.free-.1)).to('#frw',{scale:1,duration:.5,ease:spring},Math.max(0,A.free-.1)+.28)
   .fromTo('#cm2',{scale:1},{scale:1.12,duration:.25,ease:'power2.out',immediateRender:false},Math.max(0,A.posts-.1)).to('#cm2',{scale:1,duration:.45,ease:spring},Math.max(0,A.posts-.1)+.25)
   .set('#pb0,#pb1',{scaleX:1},T.tF).set('#pb2',{scaleX:.45},T.tF).set('#pb3',{scaleX:0},T.tF).set('#cm2',{rotation:0,scale:1},T.tF).set('#pst',{y:0},T.tF).set('#cur',{x:0,opacity:1},T.tF)
   .add(hide('#scA'),T.A.end-.24); return t; }
function scWords(id,o,ringId){ const t=gsap.timeline(); t.add(show(id),0); type(t,id,o.t0-.04);
  if(ringId) ringDraw(t,'#'+ringId,(o.acc-o.t0)+.16);
  t.to(id+' .ln',{x:8,duration:Math.max(.6,o.end-o.t0-.5),ease:'sine.inOut',stagger:.06},.4)
   .add(hide(id),o.end-o.t0-.2); return t; }
function scRows(){ const o=T.B, t=gsap.timeline(); t.add(show('#scB'),0);
  [['#cd0',o.r1],['#cd1',o.r2],['#cd2',o.r3]].forEach(([id,at],i)=>{ const q=Math.max(.05,at-o.t0-.3);
    t.fromTo(id,{autoAlpha:0,x:150},{autoAlpha:1,x:0,duration:.5,ease:expoOut,immediateRender:false},q)
     .fromTo(id,{scale:1.06},{scale:1,duration:.5,ease:spring,immediateRender:false},q+.35)
     .fromTo(id+' .sheen',{x:-320},{x:1100,duration:.9,ease:'sine.inOut',immediateRender:false},q+.5); });
  t.fromTo('#scB',{scale:1},{scale:1.035,duration:Math.max(1,o.end-o.t0),ease:'sine.inOut',transformOrigin:'540px 700px',immediateRender:false},0).add(hide('#scB'),o.end-o.t0-.2); return t; }
function sheen(t,sel,t0,dur){ const n=Math.max(1,Math.ceil(dur/2.6)); for(let i=0;i<n;i++) t.fromTo(sel,{x:-320},{x:1100,duration:1.9,ease:'sine.inOut',immediateRender:false},t0+i*2.6); }
function scPost(){ const o=T.C, t=gsap.timeline(); t.add(show('#scC'),0); type(t,'#scC',o.t0-.04);
  t.fromTo('#wcC',{autoAlpha:0,y:40},{autoAlpha:1,y:0,duration:.55,ease:spring,immediateRender:false},.3);
  const els=['#scC .pbig','#scC .pl:nth-of-type(2)']; const all=Array.from(document.querySelectorAll('#scC .ty')); const tot=all.reduce((a,e)=>a+e.textContent.length,0); let c=.7; const span=Math.max(2,o.end-o.t0-1.2);
  all.forEach((e,i)=>{ const id='cty'+i; e.id=id; const d=span*e.textContent.length/tot; typeChars(t,'#'+id,c,d); c+=d; });
  sheen(t,'#wcC .sheen',.9,o.end-o.t0-.9); t.to('#scC .wait',{opacity:1,duration:.4},Math.max(.8,o.live-o.t0)).fromTo('#wcC',{scale:1},{scale:1.035,duration:Math.max(1,o.end-o.t0),ease:'sine.inOut',immediateRender:false},.3).add(hide('#scC'),o.end-o.t0-.2); return t; }
function scReplies(){ const o=T.RP, t=gsap.timeline(); t.add(show('#scRP'),0); type(t,'#scRP',o.t0-.04);
  t.fromTo('#scRP .ex',{autoAlpha:0,y:30},{autoAlpha:1,y:0,duration:.5,ease:expoOut,immediateRender:false},.25)
   .fromTo('#wcD',{autoAlpha:0,y:40},{autoAlpha:1,y:0,duration:.55,ease:spring,immediateRender:false},.85);
  typeChars(t,'#scRP .rpt',1.3,Math.max(1.2,o.end-o.t0-1.7)); sheen(t,'#wcD .sheen',1.2,o.end-o.t0-1.2); t.fromTo('#scRP .ex, #wcD',{scale:1},{scale:1.03,duration:Math.max(1,o.end-o.t0),ease:'sine.inOut',immediateRender:false},.3).add(hide('#scRP'),o.end-o.t0-.2); return t; }
function scProfile(){ const o=T.E, t=gsap.timeline(); t.add(show('#scE'),0); type(t,'#scE',o.t0-.04);
  t.fromTo('#wcE',{autoAlpha:0,y:40},{autoAlpha:1,y:0,duration:.55,ease:spring,immediateRender:false},.45);
  gsap.set('#hstk',{scaleX:0,rotation:-2});
  const ta=Math.max(1.4,o.after-o.t0);
  t.to('#hstk',{scaleX:1,duration:.3,ease:inOut},ta).to('#hbef',{opacity:.45,duration:.4},ta+.15).to('#laft',{opacity:1,duration:.3},ta+.3);
  sheen(t,'#wcE .sheen',.9,ta-.9); typeChars(t,'#haft',ta+.45,Math.max(1.6,o.end-o.t0-ta-1.0)); t.to('#wcE',{backgroundColor:'#17181b',duration:.6,ease:'power2.inOut'},ta+.25).to('#wcE .hd,#wcE .hd.bef',{color:'#f2f2ee',duration:.6},ta+.25).to('#wcE .lab:not(.aft)',{color:'#b9b8b2',duration:.5},ta+.25).to('#wcE .av',{backgroundColor:'#3a3b42',duration:.5},ta+.25).fromTo('#wcE',{scale:1},{scale:1.04,duration:Math.max(1,o.end-o.t0),ease:'sine.inOut',immediateRender:false},.3).fromTo('#hstk',{backgroundColor:ORG},{backgroundColor:ORG,duration:.01},0).add(hide('#scE'),o.end-o.t0-.2); return t; }
function scSteps(){ const o=T.H, t=gsap.timeline({defaults:{ease:expoOut}}); t.add(show('#scH'),0); type(t,'#scH',o.t0-.04);
  t.fromTo('#scH .st',{autoAlpha:0,x:-26},{autoAlpha:1,x:0,duration:.45,stagger:.16,immediateRender:false},.35).add(hide('#scH'),o.end-o.t0-.2); return t; }

const tl=gsap.timeline({paused:true});
tl.fromTo('#cam',{scale:1},{scale:1.012,duration:T.D/4,ease:'sine.inOut',yoyo:true,repeat:3},0)
  .fromTo('.bgw',{x:0,y:0},{x:-14,y:-12,duration:T.D/2,ease:'sine.inOut',yoyo:true,repeat:1},0)
  .add(scA(),0)
  .add(scRows(),T.B.t0-.04)
  .add(scPost(),T.C.t0-.04)
  .add(scReplies(),T.RP.t0-.04)
  .add(scProfile(),T.E.t0-.04)
  .add(scSteps(),T.H.t0-.04)
  .add(scWords('#scI',T.I),T.I.t0-.04)
  .add(scWords('#scJ',T.J,'rgG'),T.J.t0-.04);
tl.set({},{},T.tF)
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
open(H_ + "/out/buildT.log", "w").write("\n".join(LOG) + "\n")
