#!/usr/bin/env python3
"""ep100 'VIRAL CLAIM, CHECKED #1' (Graphify and the "70x") scene SCAFFOLD, Miki style, HyperFrames + GSAP paused
timeline, 1080x1920. Model: video/ep99/build99.py.

Reads   voice/lines.txt (10 lines, the Revision of 15.11.2026), voice/narration-raw-cues.json and voice/words.json
        (optional: without them, or if they do not match lines.txt, an ESTIMATED timeline is used and a red
        banner is drawn on every frame).
Writes  hf/index.html, cues100.json (lines, D, sync points and where each came from, every on-screen number with
        its source), sfx100.json, out/build.log.
SHIP=1 refuses to build while the timeline is estimated or line 10 is still the placeholder.

Beats (one scene per spoken line; the claim looks true first, each test chips it down, the verdict comes last):
  1 the viral claim (stamp from frame 0)  2 "$20 does $100 work" (claim)  3 the problem: files read again, the bar drains
  4 Graphify + 148.2k stars  5 the map, the bar refills (as the claim goes)  6 "70x" gets BEST CASE
  7 other people's tests: 18% fewer, +49.5% more, issue #985  8 Max = 5x Pro, bars to scale, NOT CLOSE
  9 the saveable card  10 tomorrow line (PLACEHOLDER)

What is true on screen, and what is a scene choice:
  - Numbers: only those in NUMBERS below, each from channel/ref-graphify-verify-2026-11-15.md, each with a source line.
  - The USAGE LEFT bar and the "read x2 / x3" counters are an ILLUSTRATION (tagged on screen), not a measurement.
    From beat 7 on the bar shows "?" (how much it saves depends on the project).
  - Beat 8 bars are drawn to scale: Pro 1x, Max 5x. The hatched slice on the Pro bar is OUR ARITHMETIC from the best
    test in the verify file: 18% fewer tokens = 1 / 0.82 = about 1.22x as far (a plan-usage reading we did not measure).
  - We did not install or test Graphify: the screen says "tests by other people, not by us".
Ideas taken from the reference reel DfatglrzjiV (see channel/ref-graphify-visual-2026-11-15.md), all redrawn, other layout.
No TTS, no audio is written here.
"""
import json, os, re, math, shutil, sys, html as _html
H_ = os.path.dirname(os.path.abspath(__file__))
INK = "#0f0f0f"; PAPER = "#fbfbf8"; RED = "#D9281C"; GREEN = "#1F8A4C"; ORA = "#D97757"; ORD = "#B8502C"
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
LOG = []
def say(x): LOG.append(x); print(x)

# ---------------------------------------------------------------- assets (fonts + paper from the ep98 build; logos: hf/assets/logos/SOURCES.md)
for sub in ("fonts/InterDisplay-Black.otf", "fonts/InterDisplay-ExtraBold.otf", "fonts/InterDisplay-Medium.otf", "bg.jpg"):
    dst = f"{H_}/hf/assets/{sub}"
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(f"{H_}/../ep98/hf/assets/{sub}", dst)
for f in ("claude.svg", "graphify-icon.svg", "graphify-word.svg", "github-mark.svg", "SOURCES.md"):
    assert os.path.exists(f"{H_}/hf/assets/logos/{f}"), f"missing real logo file {f}: never redraw it, fetch it (see SOURCES.md)"

# ---------------------------------------------------------------- every number allowed on screen (verify file, read 15.11.2026)
NUMBERS = [
    dict(text="70x (as the viral claim, in quote marks)", source="the viral posts; the project's earlier worked example was 71.5x"),
    dict(text="about 52 files, compared with reading every file", source="verify file section 2 (pyshine.com, themenonlab.blog, roborhythms.com)"),
    dict(text="Pro $20 a month, Max $100 a month, Max = 5x Pro usage", source="claude.com/pricing, read 15.11.2026"),
    dict(text="148.2k stars", source="github.com/Graphify-Labs/graphify repo page, 15.11.2026"),
    dict(text="18% fewer tokens, $5.16 to $4.29, one YouTube run (The Gray Cat)", source="graphify.com/blog/reduce-claude-code-token-usage"),
    dict(text="+49.5% input tokens, FastAPI, 11 questions (Constantin Ponfick)", source="same Graphify blog post"),
    dict(text="GitHub issue #985: no savings on common queries (a user's report)", source="verify file section 5"),
    dict(text="hatched slice on the Pro bar = 1.22x", source="OUR ARITHMETIC: 1 / (1 - 0.18); not a measurement"),
]
STARS = 148.2

# ---------------------------------------------------------------- lines + cues
LINES = [l.strip() for l in open(H_ + "/voice/lines.txt") if l.strip()]
NL = len(LINES); assert NL == 10, "this build is laid out for the 10 lines of the 15.11 revision"
PH_L10 = "face a maze" in LINES[9]                              # the tomorrow line is a placeholder until it names the real next episode
try:
    C = json.load(open(H_ + "/voice/narration-raw-cues.json")); C = C if isinstance(C, list) else C["lines"]
except Exception:
    C = []
ctext = lambda c: c.get("line", c.get("text", ""))
CUE = {c["n"]: c for c in C if "n" in c}
STALE = os.environ.get("EST") == "1" or len(CUE) != NL or any(n not in CUE or norm(ctext(CUE[n])) != norm(LINES[n - 1]) for n in range(1, NL + 1))
WORDS = []
if not STALE:
    try:
        WORDS = json.load(open(H_ + "/voice/words.json"))
        if not (WORDS and norm(WORDS[0][0]) == norm(LINES[0].split()[0])): WORDS = []
    except Exception:
        WORDS = []
if STALE:
    L = {}; t = .08
    for n in range(1, NL + 1):
        d = round(.3 + .047 * len(LINES[n - 1]), 2)
        L[n] = (round(t, 2), round(t + d, 2)); t += d + .1
else:
    L = {n: (float(CUE[n]["start"]), float(CUE[n]["end"])) for n in range(1, NL + 1)}
s = lambda n: L[n][0]
e = lambda n: L[n][1]
SRC = {}
def W(name, word, n, frac, k=0):
    """time of a spoken word inside line n (words.json), else a fraction of the line (ESTIMATE)"""
    c = 0
    for w, a, b in WORDS:
        if s(n) - .12 <= a <= e(n) + .12 and norm(w) in (word if isinstance(word, tuple) else (word,)):
            if c == k: SRC[name] = "words.json"; return round(a, 3)
            c += 1
    SRC[name] = "ESTIMATE (line fraction)"
    return round(s(n) + frac * (e(n) - s(n)), 3)
D = round(e(NL) + .4, 2)
tF = D - .58                                                   # frame 0 comes back from here (loop seam)
a = {n: s(n) for n in range(1, NL + 1)}
tPlug = W("killed", "killed", 1, .42)
tNow = W("now", "now", 2, .42)
tSo = W("so", "so", 3, .46)
tAbout = W("about", "about", 4, .34)
tOnce = W("once", "once", 5, .30)
tLook = W("looks", "looks", 5, .56)
tBut = W("but", "but", 6, .66)
tR1 = W("one_saves", "one", 7, .30, 0)
tR2 = W("one_uses", "one", 7, .66, 1)
tR3 = min(e(7) + .05, tR2 + .8)
tFive = W("five", ("five", "5"), 8, .34)
t70 = W("seventy", ("seventy", "70"), 6, .2)
tFree = W("free", "free", 1, .2)
tTool = W("tool", "tool", 1, .3)
tCC = W("claude", "claude", 1, .55)
tP20 = W("twenty", ("twenty", "20", "twentydollar"), 2, .1)
tP100 = W("hundred", ("hundred", "100", "hundreddollar"), 2, .55)
tDoes = W("does", "does", 2, .42)
tGraph = W("graphify", "graphify", 4, .16)
tNo = W("nothing", "nothing", 8, .62)
tClose = W("close", "close", 8, .90)

# ---------------------------------------------------------------- helpers
try:
    from PIL import ImageFont
    _f = ImageFont.truetype(H_ + "/hf/assets/fonts/InterDisplay-Black.otf", 100)
    _m = ImageFont.truetype(H_ + "/hf/assets/fonts/InterDisplay-Medium.otf", 100)
    tw = lambda t: (lambda u: _f.getlength(u) - 3.0 * len(u))(_html.unescape(t))
    twm = lambda t: _m.getlength(_html.unescape(t))
except Exception:
    tw = lambda t: 62 * len(t); twm = lambda t: 52 * len(t)
J = []; SFX = []
def js(x): J.append(x)
def sfx(f, t, g=-8): SFX.append(dict(f=f, t=round(max(0, t), 3), g=g))
def fin(sel, t, d=.4, y=22, blur=8):
    js(f"tl.fromTo('{sel}',{{opacity:0,y:{y},filter:'blur({blur}px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:{d},ease:'power2.out',immediateRender:false}},{max(0, t):.3f});")
def fout(sel, t, d=.22):
    js(f"tl.to('{sel}',{{opacity:0,y:-12,filter:'blur(8px)',duration:{d},ease:'power2.inOut'}},{max(0, t):.3f});")
def pop(sel, t, d=.34, frm=.3, ease="back.out(1.8)"):
    xo = ",transformOrigin:'50% 50%'" if sel.startswith(("#dt", "#nd")) else ""
    js(f"tl.fromTo('{sel}',{{opacity:0,scale:{frm}}},{{opacity:1,scale:1{xo},duration:{d},ease:'{ease}',immediateRender:false}},{max(0, t):.3f});")
def slam(sel, t, rot):
    js(f"tl.fromTo('{sel}',{{opacity:0,scale:1.25,rotation:{rot - 9}}},{{opacity:1,scale:1,rotation:{rot},duration:.3,ease:'power3.in',immediateRender:false}},{max(0, t):.3f});")
    js(f"tl.fromTo('{sel}',{{y:0}},{{y:7,duration:.09,ease:'sine.inOut',yoyo:true,repeat:3,immediateRender:false}},{t + .3:.3f});")
def idle(sel, t0, t1, prop="y", amp=-9, per=.9):
    if t1 - t0 < per: return
    rep = max(1, int((t1 - t0) / per)) | 1
    b0 = 1 if prop in ("scale", "opacity") else 0
    xo = ",transformOrigin:'50% 50%'" if sel.startswith(("#dt", "#nd", "#grow")) else ""
    js(f"tl.fromTo('{sel}',{{{prop}:{b0}}},{{{prop}:{amp}{xo},duration:{(t1 - t0) / (rep + 1):.3f},ease:'sine.inOut',yoyo:true,repeat:{rep},immediateRender:false}},{t0:.3f});")
def srcline(txt, top, mx=950, size=26, left=65):
    fs = min(size, 100 * mx / twm(txt))
    return f'<div class="src" style="left:{left}px;top:{top}px;font-size:{fs:.1f}px;line-height:{fs * 1.25:.1f}px">{txt}</div>'
clg = lambda h, cls="": f'<img class="lg {cls}" src="assets/logos/claude.svg" style="width:{h}px;height:{h}px">'
gicon = lambda h, cls="": f'<img class="lg {cls}" src="assets/logos/graphify-icon.svg" style="height:{h}px;width:{h * 20.9347 / 24:.1f}px">'
gword = lambda h: f'<img class="lg" src="assets/logos/graphify-word.svg" style="height:{h}px;width:{h * 70.1015 / 16.5189:.1f}px">'
ghub = lambda h: f'<img class="lg" src="assets/logos/github-mark.svg" style="width:{h}px;height:{h}px">'
DOC = f'<svg class="doc" viewBox="0 0 60 72"><path d="M6 4 H38 L54 20 V68 H6Z" fill="#fff" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/><path d="M38 4 V20 H54 M16 34 H44 M16 46 H44 M16 58 H34" fill="none" stroke="{INK}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHK = f'<svg class="chk" viewBox="-20 -20 40 40"><circle r="17" fill="{GREEN}" stroke="{INK}" stroke-width="3.5"/><path d="M-9 1 L-3 7 L10 -7" fill="none" stroke="#fff" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
STAR = f'<svg class="star" viewBox="-52 -52 104 104"><path d="M0 -44 L12.6 -15.4 L43.7 -12.6 L20.2 8 L27.1 38.4 L0 22.6 L-27.1 38.4 L-20.2 8 L-43.7 -12.6 L-12.6 -15.4Z" fill="#F5B301" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/></svg>'

# ---------------------------------------------------------------- headlines: one line, plain ink, no boxes. Claims in quote marks until they are tested. ALL TEXT IS DRAFT.
HEADS = []; HLOG = []
def head(i, t_in, t_out, l1, size=100, lg=""):
    wl = 100 if lg else 0
    fs = min(size, 100 * 940 / (tw(l1) + wl))
    lgh = (gicon(round(fs * .84), "hlg") if lg == "g" else clg(round(fs * .8), "hlg")) if lg else ""
    HEADS.append(f'<div class="hd" id="h{i}" style="top:{372 + (100 - fs) / 2:.0f}px;font-size:{fs:.1f}px;line-height:{fs:.1f}px">{lgh}<span>{l1}</span></div>')
    if t_in is not None: fin(f"#h{i}", t_in)
    if t_out is not None: fout(f"#h{i}", t_out - .24)
    HLOG.append((round(t_in or 0, 2), l1))
head(0, None, a[2], "&ldquo;70x LESS USAGE&rdquo;")
head(1, a[2], a[3], "&ldquo;$20 DOES $100 WORK&rdquo;")
head(2, a[3], tSo, "NEW CHAT = FROM ZERO")
head(3, tSo, a[4], "READS YOUR FILES AGAIN")
head(4, a[4], a[5], "THE TOOL: GRAPHIFY", lg="g")
head(5, a[5], a[6], "MAPS YOUR CODE ONCE")
head(6, a[6], tBut, "&ldquo;70 TIMES LESS&rdquo;")
head(7, tBut, a[7], "ONLY IN ITS BEST CASE")
head(8, a[7], a[8], "REAL TESTS:")
head(9, a[8], tNo, "MAX = 5x PRO USAGE")
head(10, tNo, a[9], "NOTHING COMES CLOSE")
head(11, a[9], a[10], "SETUP: LINK IN BIO")
head(12, a[10], tF + .04, "TOMORROW: [PLACEHOLDER]" if PH_L10 else "TOMORROW")
fin("#h0", tF + .06, .42)

# ---------------------------------------------------------------- scenes (page px; every scene is a full-page layer)
SC = {}
# 1 the claim: the two real marks, the free tool plugs in
SC[1] = f'''<div class="tile" id="t1a" style="left:95px;top:500px">{clg(210)}</div><div class="tn" id="tn_a" style="left:95px;top:866px">Claude Code</div>
<div id="plus" style="left:480px;top:612px">+</div>
<div class="tile" id="t1b" style="left:615px;top:500px">{gicon(220)}<div class="free" id="free">FREE TOOL</div></div><div class="tn" id="tn_b" style="left:615px;top:866px">Graphify</div>'''
# 2 the money claim: real prices, shown as a claim
def plan(i, x, name, price):
    return f'''<div class="plan" id="p{i}" style="left:{x}px;top:500px">{clg(74)}<div class="pn">{name}</div><div class="pp">{price}</div><div class="pm">a month</div></div>'''
SC[2] = plan(1, 65, "PRO", "$20") + plan(2, 577, "MAX", "$100") + '<div id="eq" style="left:481px;top:508px">=</div>' + \
        srcline("prices: claude.com/pricing, read 15.11.2026", 978)
# 3 the problem: every new chat, the files are read again
FILES = ["login", "users", "orders", "payments", "search", "emails"]
FX = [65, 392, 719]; FY = [500, 730]
SC[3] = "".join(f'<div class="fc" id="fc{c}" style="left:{FX[c % 3]}px;top:{FY[c // 3]}px">{DOC}<div class="rd" id="rd{c}">read &times;1</div><div class="fn">{FILES[c]}</div></div>' for c in range(6)) + \
        f'<div class="bdg" id="scan" style="left:{FX[0] + 222}px;top:{FY[0] + 138}px;width:74px;height:74px">{clg(46)}</div>'
# 4 the tool and its real size
SC[4] = f'''<div id="gcard">{gicon(170)}{gword(104)}</div>
<div id="gfree" style="left:65px;top:752px">{CHK}<span>free</span>{CHK}<span>open source</span></div>
<div id="grow" style="left:65px;top:820px">{ghub(120)}{STAR}<span id="stn">0.0k</span><span id="stw">stars</span></div>''' + \
        srcline("github.com/Graphify-Labs/graphify, read 15.11.2026", 978)
# 5 the map
NODE = [(150, 100), (430, 64), (770, 110), (810, 350), (500, 290), (170, 370)]
DOT = [(300, 215), (625, 200), (660, 440), (345, 452), (905, 225), (50, 235)]
P = NODE + DOT
EDGE = [(0, 1), (0, 6), (6, 4), (1, 7), (7, 2), (7, 4), (4, 3), (4, 9), (9, 5), (5, 11), (11, 0), (2, 10), (10, 3), (3, 8), (8, 9)]
PATHN = [0, 6, 4, 3]                                           # the look-up: login -> search -> payments
PATHE = [EDGE.index((0, 6)), EDGE.index((6, 4)), EDGE.index((4, 3))]
elen = lambda i: math.hypot(P[EDGE[i][0]][0] - P[EDGE[i][1]][0], P[EDGE[i][0]][1] - P[EDGE[i][1]][1])
SC[5] = f'''<svg id="gsv" viewBox="0 0 950 520" width="950" height="520" style="left:65px;top:495px">
 {"".join(f'<path class="ed" id="ed{i}" d="M{P[x][0]} {P[x][1]} L{P[y][0]} {P[y][1]}" stroke-dasharray="{elen(i) + 2:.0f}" stroke-dashoffset="{elen(i) + 2:.0f}"/>' for i, (x, y) in enumerate(EDGE))}
 {"".join(f'<circle class="dt" id="dt{i}" cx="{x}" cy="{y}" r="13"/>' for i, (x, y) in enumerate(DOT))}
 {"".join(f'<g class="nd" id="nd{i}"><circle cx="{x}" cy="{y}" r="36"/><path d="M{x - 13} {y - 17} H{x + 5} L{x + 13} {y - 9} V{y + 17} H{x - 13}Z M{x - 6} {y - 1} H{x + 6} M{x - 6} {y + 8} H{x + 6}"/></g>' for i, (x, y) in enumerate(NODE))}
</svg>''' + "".join(f'<div class="nl" style="left:{65 + x - 100}px;top:{495 + y + 40}px">{FILES[i]}</div>' for i, (x, y) in enumerate(NODE)) + \
        f'<div class="bdg" id="walk" style="left:{65 + NODE[0][0] - 42}px;top:{495 + NODE[0][1] - 42}px">{clg(52)}</div>'
# 6 the big number and where it comes from
SC[6] = f'''<div id="big70"><i>&ldquo;</i>70x<i>&rdquo;</i></div><div class="stamp big" id="bc" style="left:{round(985 - (tw("BEST CASE") * .92 + .05 * 92 * 9 + 72)) - 34}px;top:722px">BEST CASE</div>
<div class="sub1" id="s6a" style="top:893px">ONE EXAMPLE &middot; ABOUT 52 FILES</div><div class="sub2" id="s6b" style="top:949px">compared with reading every file at once</div>''' + \
        srcline("source: the project's own early example, via roborhythms.com, read 15.11.2026", 1002, size=24)
# 7 other people's tests
def row(i, y, num, word, col, d1, d2):
    return f'<div class="tr" id="tr{i}" style="top:{y}px"><span class="tnum" style="color:{col}" id="tn{i}">{num}</span><span class="tw_" style="color:{col}">{word}</span><span class="td">{d1}<br>{d2}</span></div>'
SC[7] = row(1, 495, "18%", "FEWER", GREEN, "one YouTube run", "$5.16 &rarr; $4.29") + row(2, 655, "+49.5%", "MORE", RED, "FastAPI project", "11 questions") + \
        row(3, 815, "NO", "SAVINGS", INK, "GitHub issue #985", "a user&rsquo;s report") + \
        srcline("tests by other people, not by us &middot; source: graphify.com/blog, GitHub issue #985", 978)
# 8 the money verdict: bars to scale
U = 100; BASE = 1150; PX, MX_, BW = 296, 640, 240
EXT = round(U * (1 / (1 - .18) - 1))                           # 22 px: our arithmetic, see the docstring
SC[8] = srcline("usage: claude.com/pricing (&ldquo;5x Pro usage&rdquo;), read 15.11.2026", 492) + f'''
<div id="dash" style="left:100px;top:{BASE - 5 * U - 3}px;width:{MX_ - 100}px"></div>
<div class="bar" id="bpro" style="left:{PX}px;top:{BASE - U}px;height:{U}px"></div>
<div id="bext" style="left:{PX}px;top:{BASE - U - EXT}px;height:{EXT}px"></div>
{"".join(f'<div class="bar seg" id="bm{i}" style="left:{MX_}px;top:{BASE - (i + 1) * U}px;height:{U}px"></div>' for i in range(5))}
<div class="bx" id="x1" style="left:{PX}px;top:{BASE - U - EXT - 112}px">1x</div><div class="bx" id="x5" style="left:{MX_}px;top:{BASE - 5 * U - 108}px">5x</div>
<div id="call" style="left:30px;top:{BASE - U - EXT - 60}px">best test<br>we found</div>
<svg id="carr" viewBox="0 0 60 40" style="left:232px;top:{BASE - U - EXT - 22}px"><path d="M4 8 C22 4 40 12 54 30 M54 30 L36 28 M54 30 L52 12" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>
<div class="bl" style="left:{PX - 40}px;top:{BASE + 14}px">PRO $20</div><div class="bl" style="left:{MX_ - 40}px;top:{BASE + 14}px">MAX $100</div>
<div class="stamp big nc" id="nc" style="left:82px;top:712px">NOT CLOSE</div>'''
# 9 the saveable card (stays through line 10)
ROWS = ["Free, open source, 148.2k stars", "&ldquo;70x&rdquo; = one best case", "Real tests: 18% fewer &hellip; 49.5% more", "Max is 5x Pro: no test comes near", "Measure your own project first"]
SC[9] = f'<div id="card"><div class="tape t1" data-decor></div><div class="tape t2" data-decor></div><div class="ct">{gicon(66)}<span>BEFORE YOU INSTALL</span></div>' + \
        "".join(f'<div class="cr" id="cr{i}" style="top:{112 + i * 103}px"><span class="cnm">{i + 1}</span><span class="cx">{t}</span><i class="mk"></i></div>' for i, t in enumerate(ROWS)) + \
        '<div class="cf">VIRAL CLAIM, CHECKED #1 &middot; tests by other people, not by us</div></div>'
scenes = "".join(f'<div class="sc" id="sc{n}">{SC[n]}</div>' for n in sorted(SC))
PHB = ""
if STALE or PH_L10:
    what = " &middot; ".join(x for x in ("ESTIMATED TIMING" if STALE else "", "LINE 10 PLACEHOLDER" if PH_L10 else "") if x)
    PHB = f'<div class="phb" data-decor style="top:196px">SCAFFOLD &middot; {what}</div><div class="phb" data-decor style="top:1272px">SCAFFOLD &middot; {what}</div>'
markup = f'''
<div class="bgw" data-decor></div>
<div id="cam">
 <div id="fit">
 <div class="stamp" id="vc">VIRAL CLAIM</div>
 <div class="stt" id="st0">TRUE?</div><div class="stt" id="st1">CHECKING&hellip;</div><div class="stt" id="st2">NOT CLOSE</div>
 {"".join(HEADS)}
 {scenes}
 <div id="use"><div id="utag">ILLUSTRATION</div><div id="ul">YOUR CLAUDE USAGE</div><div id="up"><span id="upn">100%</span><em>left</em></div><div id="ut"><div id="uf"></div></div></div>
 </div>
</div>{PHB}'''

CSS = '''
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;color:INK}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}
.bgw{position:absolute;left:-20px;top:-20px;width:1120px;height:1960px;background:#ecebe5 url(assets/bg.jpg);background-size:1120px 1960px}
#cam{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}
#fit{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 758.5px;transform:scale(FITS)}
.lg{display:block;flex:none}
.stamp{position:absolute;border:6px solid RED;color:RED;border-radius:10px;padding:0 16px;font-weight:900;font-size:44px;line-height:56px;letter-spacing:.05em;white-space:nowrap;transform:rotate(-3deg);z-index:7}
#vc{left:72px;top:283px}
.stamp.big.nc{font-size:84px;line-height:100px}
.stamp.big{font-size:92px;line-height:110px;border-width:10px;border-radius:16px;padding:0 26px;opacity:0;background:rgba(251,251,248,.86);transform-origin:50% 50%;z-index:9}
.stt{position:absolute;right:78px;top:287px;font-weight:900;font-size:48px;line-height:56px;letter-spacing:.02em;white-space:nowrap;opacity:0;z-index:7}
#st1{color:ORD} #st2{color:RED}
.hd{position:absolute;left:65px;font-weight:900;letter-spacing:-.03em;white-space:nowrap;opacity:0;z-index:6;display:flex;align-items:center}
.hd .hlg{margin-right:.16em} #h0{opacity:1}
.sc{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0;z-index:3} #sc1{opacity:1}
.sc>*{position:absolute}
.src{position:absolute;font-weight:500;color:#3a3a36;white-space:nowrap;letter-spacing:0}
/* 1 */
.tile{width:350px;height:350px;background:#fff;border:6px solid INK;border-radius:34px;box-shadow:11px 11px 0 INK;display:flex;align-items:center;justify-content:center;transform-origin:50% 60%}
.tn{opacity:0;width:350px;text-align:center;font-weight:900;font-size:54px;line-height:62px;letter-spacing:-.03em;white-space:nowrap}
#plus{width:120px;text-align:center;font-weight:900;font-size:130px;line-height:130px}
.free{position:absolute;right:-6px;top:-12px;font-weight:900;font-size:36px;line-height:50px;letter-spacing:.04em;color:INK;background:#fff;border:5px solid INK;border-radius:30px;padding:0 18px;box-shadow:4px 4px 0 INK;white-space:nowrap;transform:rotate(5deg)}
/* 2 */
.plan{width:430px;height:456px;background:#fff;border:6px solid INK;border-radius:22px;box-shadow:8px 8px 0 INK;opacity:0;transform-origin:50% 100%}
.plan .lg{position:absolute;left:28px;top:30px} .pn{position:absolute;left:118px;top:22px;font-weight:900;font-size:88px;line-height:92px;letter-spacing:-.02em}
.pp{position:absolute;left:26px;top:150px;font-weight:900;font-size:168px;line-height:176px;letter-spacing:-.045em}
.pm{position:absolute;left:32px;top:340px;font-weight:800;font-size:54px;line-height:62px}
#eq{width:118px;height:118px;border-radius:50%;background:#fff;border:6px solid INK;box-shadow:6px 6px 0 INK;text-align:center;font-weight:900;font-size:104px;line-height:100px;opacity:0;z-index:4}
/* 3 */
.fc{width:288px;height:205px;background:#fff;border:6px solid INK;border-radius:18px;box-shadow:8px 8px 0 INK;opacity:0;transform-origin:50% 50%}
.fc .doc{position:absolute;left:20px;top:18px;width:72px;height:86px}
.fn{position:absolute;left:22px;bottom:14px;font-weight:900;font-size:46px;line-height:54px;letter-spacing:-.02em}
.rd{position:absolute;right:16px;top:20px;font-weight:900;font-size:36px;line-height:42px;color:ORD;white-space:nowrap}
.bdg{width:84px;height:84px;border-radius:50%;background:#fff;border:5px solid INK;box-shadow:5px 5px 0 INK;display:flex;align-items:center;justify-content:center;opacity:0;z-index:5}
/* 4 */
#gcard{left:65px;top:500px;width:942px;height:232px;background:#fff;border:6px solid INK;border-radius:22px;box-shadow:8px 8px 0 INK;display:flex;align-items:center;justify-content:center;gap:44px;opacity:0;transform-origin:50% 50%}
#gfree{display:flex;align-items:center;gap:14px;font-weight:900;font-size:46px;line-height:52px;white-space:nowrap;opacity:0}
#gfree .chk{width:48px;height:48px} #gfree span{margin-right:34px}
#grow{display:flex;align-items:center;gap:20px;white-space:nowrap;opacity:0}
#grow .star{width:104px;height:104px;transform-origin:50% 50%} #stn{font-weight:900;font-size:136px;line-height:140px;letter-spacing:-.04em;min-width:450px}
#stw{font-weight:900;font-size:56px;line-height:60px;align-self:flex-end;margin-bottom:16px}
/* 5 */
#gsv{overflow:visible} .ed{fill:none;stroke:INK;stroke-width:6;stroke-linecap:round}
.dt{fill:ORA;stroke:INK;stroke-width:5;opacity:0}
.nd{opacity:0} .nd circle{fill:#fff;stroke:INK;stroke-width:6} .nd path{fill:none;stroke:INK;stroke-width:4;stroke-linejoin:round;stroke-linecap:round}
.nl{width:200px;text-align:center;font-weight:900;font-size:34px;line-height:40px;opacity:0;text-shadow:2px 2px 0 PAPER,-2px 2px 0 PAPER,2px -2px 0 PAPER,-2px -2px 0 PAPER}
/* 6 */
#big70{left:110px;top:478px;width:860px;text-align:center;font-weight:900;font-size:350px;line-height:400px;letter-spacing:-.05em;color:ORA;text-shadow:9px 9px 0 INK;white-space:nowrap;transform-origin:50% 60%;opacity:0}
#big70 i{font-style:normal;font-size:200px;vertical-align:top;line-height:330px;color:INK;text-shadow:none}
.sub1{left:65px;width:950px;text-align:center;font-weight:900;font-size:50px;line-height:54px;letter-spacing:-.01em;opacity:0;white-space:nowrap}
.sub2{left:65px;width:950px;text-align:center;font-weight:800;font-size:40px;line-height:44px;opacity:0;white-space:nowrap}
/* 7 */
.tr{left:65px;width:942px;height:146px;background:#fff;border:6px solid INK;border-radius:18px;box-shadow:8px 8px 0 INK;display:flex;align-items:center;padding:0 26px;opacity:0;transform-origin:0 50%;white-space:nowrap}
.tnum{font-weight:900;font-size:96px;line-height:110px;letter-spacing:-.04em} .tw_{font-weight:900;font-size:52px;line-height:60px;margin-left:28px;align-self:flex-end;margin-bottom:26px}
.td{margin-left:auto;text-align:right;font-weight:800;font-size:35px;line-height:42px}
/* 8 */
.bar{width:BWpx;background:ORA;border:6px solid INK;transform-origin:50% 100%;transform:scaleY(0)}
.bar.seg{margin-top:0} #bpro{box-shadow:8px 8px 0 INK} .seg{box-shadow:8px 8px 0 INK}
#bext{width:BWpx;border:6px solid INK;border-bottom:none;background:repeating-linear-gradient(45deg,#fff 0 7px,ORA 7px 14px);transform-origin:50% 100%;transform:scaleY(0)}
#dash{height:0;border-top:6px dashed INK;opacity:0;transform-origin:100% 50%}
.bx{width:BWpx;text-align:center;font-weight:900;font-size:104px;line-height:104px;letter-spacing:-.03em;opacity:0}
.bl{width:320px;text-align:center;font-weight:900;font-size:47px;line-height:60px;letter-spacing:-.02em;white-space:nowrap}
#call{width:196px;text-align:right;font-weight:900;font-size:34px;line-height:38px;opacity:0}
#carr{width:60px;height:40px;opacity:0;overflow:visible}
/* 9 */
#card{left:78px;top:490px;width:916px;height:716px;background:PAPER;border:6px solid INK;border-radius:10px;box-shadow:14px 14px 0 INK;opacity:0;transform-origin:50% 0%}
.tape{position:absolute;width:130px;height:40px;background:rgba(232,221,186,.86);border:1px solid rgba(0,0,0,.14);z-index:3}
.tape.t1{right:-34px;top:-12px;transform:rotate(34deg)} .tape.t2{left:-34px;bottom:-6px;transform:rotate(34deg)}
.ct{position:absolute;left:34px;top:24px;display:flex;align-items:center;gap:18px;font-weight:900;font-size:62px;line-height:70px;letter-spacing:-.03em;white-space:nowrap}
.cr{position:absolute;left:34px;right:34px;height:100px;display:flex;align-items:center;opacity:0;border-top:4px solid rgba(15,15,15,.14);white-space:nowrap}
.mk{position:absolute;left:82px;right:0;bottom:12px;height:10px;border-radius:5px;background:ORA;transform-origin:0 50%;transform:scaleX(0);opacity:.85}
.cnm{width:62px;height:62px;border-radius:50%;border:5px solid INK;background:#fff;text-align:center;font-weight:900;font-size:40px;line-height:52px;margin-right:20px;flex:none}
.cx{font-weight:900;font-size:44px;line-height:52px;letter-spacing:-.02em}
.cf{position:absolute;left:34px;bottom:20px;font-weight:500;font-size:26px;line-height:30px;white-space:nowrap;color:#3a3a36}
/* the usage bar: the spine of the video (an illustration, tagged) */
#use{position:absolute;left:65px;top:1040px;width:950px;height:208px;z-index:5;transform-origin:50% 100%}
#utag{position:absolute;left:2px;top:-12px;font-weight:900;font-size:38px;line-height:42px;letter-spacing:.08em;color:#3a3a36;white-space:nowrap}
#ul{position:absolute;left:0;top:32px;font-weight:900;font-size:47px;line-height:54px;letter-spacing:-.01em;white-space:nowrap}
#up em{font-style:normal;font-weight:900;font-size:36px;letter-spacing:0;margin-left:8px}
#up{position:absolute;right:119px;top:0;transform-origin:100% 50%;font-weight:900;font-size:86px;line-height:86px;letter-spacing:-.04em;white-space:nowrap}
#ut{position:absolute;left:0;top:92px;width:823px;height:108px;background:#fff;border:6px solid INK;border-radius:16px;box-shadow:8px 8px 0 INK;overflow:hidden}
#uf{position:absolute;left:0;top:0;height:100%;width:100%;background:repeating-linear-gradient(115deg,ORA 0 34px,#E58D6F 34px 68px);background-size:200% 100%;border-right:6px solid INK}
.phb{position:absolute;left:0;width:1080px;text-align:center;font-weight:900;font-size:30px;line-height:40px;color:RED;letter-spacing:.02em;z-index:20;white-space:nowrap}
'''
FITS = round(864 / 950, 4)                                     # safe box x 108-972 (CLAUDE.md 15.11); in screen y 1056-1632 the right edge stays <= 864 = design x 896
for a_, b_ in (("FITS", FITS), ("BW", BW), ("GREEN", GREEN), ("INK", INK), ("PAPER", PAPER), ("RED", RED), ("ORA", ORA), ("ORD", ORD)):
    CSS = CSS.replace(a_, str(b_))

# ---------------------------------------------------------------- timeline
js(f"tl.fromTo('#cam',{{scale:1,rotation:0}},{{scale:1.012,rotation:.2,duration:{D / 6:.3f},ease:'sine.inOut',yoyo:true,repeat:5}},0);")
js(f"tl.fromTo('.bgw',{{x:0,y:0}},{{x:-14,y:-12,duration:{D / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},0);")
idle("#vc", 0, a[9], "rotation", 2.2, 1.1)
def scene(n, t_in, t_out):
    if t_in is not None: fin(f"#sc{n}", t_in)
    fout(f"#sc{n}", t_out - .24)
status = lambda i, t: (fout(f"#st{i - 1}", t - .2, .18), pop(f"#st{i}", t, .3, .6))
# --- 1 the claim. The bar drains (the "token problem"), the free tool plugs in, the bar is full again: the claim looks true
scene(1, None, a[2])
idle("#t1a", 0, a[2], "y", -10, .7)
js(f"tl.fromTo('#t1b',{{x:0,rotation:0}},{{x:30,rotation:6,duration:{max(.2, tPlug - .34 - tFree - .1):.3f},ease:'sine.inOut',immediateRender:false}},{tFree + .1:.3f});")
js(f"tl.to('#t1b',{{x:0,rotation:-3,duration:.34,ease:'power3.in'}},{tPlug - .34:.3f});")
js(f"tl.fromTo('#t1a',{{scale:1}},{{scale:1.07,duration:.16,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tPlug:.3f});")
js(f"tl.fromTo('#plus',{{scale:1,rotation:0}},{{scale:1.35,rotation:90,duration:.22,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tPlug:.3f});")
js(f"tl.fromTo('#free',{{scale:1}},{{scale:1.3,duration:.18,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tFree:.3f});"); idle("#free", tFree + .4, a[2], "rotation", 9, .5); sfx("pop_b.ogg", tFree, -11)
fin("#tn_b", tTool, .3, 12, 4); fin("#tn_a", tCC, .3, 12, 4)
pop("#st0", a[2] + .1, .3, .6)
idle("#t1b", tPlug + .4, a[2], "y", -10, .7)
sfx("subhit.ogg", .05, -6); sfx("whoosh_a.ogg", tPlug - .3, -10); sfx("impactsoft.ogg", tPlug, -8); sfx("riser.ogg", tPlug + .05, -14)
# --- 2 the money claim
scene(2, a[2], a[3])
for i, dl in ((1, tP20 - .12 - a[2] - .04), (2, tP100 - .12 - a[2] - .04)):
    js(f"tl.fromTo('#p{i}',{{opacity:0,y:70,rotation:{4 if i == 1 else -4}}},{{opacity:1,y:0,rotation:{-1.5 if i == 1 else 1.5},duration:.42,ease:'back.out(1.4)',immediateRender:false}},{a[2] + .04 + dl:.3f});")
    sfx("pop_a.ogg" if i == 1 else "pop_b.ogg", a[2] + .04 + dl, -10)
pop("#eq", tDoes, .32); sfx("select.ogg", tDoes, -9)
js(f"tl.fromTo('#p1',{{scale:1}},{{scale:1.06,duration:.4,ease:'sine.inOut',yoyo:true,repeat:{max(1, int((a[3] - tDoes - .4) / .4)) | 1},immediateRender:false}},{tDoes + .1:.3f});")
idle("#eq", tDoes + .35, a[3], "rotation", 14, .5)
idle("#p2", tP100 + .4, a[3], "y", -8, .4)
# --- 3 the problem: the files are read again, the bar drains
scene(3, a[3], a[4])
for c in range(6):
    js(f"tl.fromTo('#fc{c}',{{opacity:0,y:40,scale:.9}},{{opacity:1,y:0,scale:1,duration:.32,ease:'back.out(1.5)',immediateRender:false}},{a[3] + .05 + .06 * c:.3f});")
    sfx("pop_a.ogg" if c % 2 == 0 else "pop_b.ogg", a[3] + .05 + .06 * c, -13)
for c in range(6):                                              # while "from zero" is said the cards breathe in a wave
    js(f"tl.fromTo('#fc{c}',{{rotation:0}},{{rotation:{2.5 if c % 2 else -2.5},duration:.3,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{a[3] + .7 + .1 * c:.3f});")
h0 = tSo - .1; NH = max(6, min(12, int((a[4] - .3 - h0) / .2))); hstep = (a[4] - .3 - h0) / NH
HOPS = []
pop("#scan", h0 - .28, .26)
for k in range(NH):
    c = k % 6; t = h0 + k * hstep
    js(f"tl.to('#scan',{{x:{FX[c % 3] - FX[0]},y:{FY[c // 3] - FY[0]},duration:{min(.22, hstep * .8):.3f},ease:'power2.inOut'}},{t - min(.22, hstep * .8):.3f});")
    js(f"tl.fromTo('#fc{c}',{{scale:1}},{{scale:1.07,duration:{hstep * .45:.3f},ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{t:.3f});")
    js(f"tl.fromTo('#rd{c}',{{scale:1}},{{scale:1.28,transformOrigin:'100% 50%',duration:{hstep * .45:.3f},ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{t:.3f});")
    HOPS.append([round(t, 3), c]); sfx("tick.ogg", t, -12)
# --- 4 the tool + the stars
scene(4, a[4], a[5])
js(f"tl.fromTo('#gcard',{{opacity:0,scale:.8,rotation:-4}},{{opacity:1,scale:1,rotation:-1,duration:.42,ease:'back.out(1.6)',immediateRender:false}},{tGraph - .1:.3f});")
sfx("whoosh_b.ogg", tGraph - .1, -10)
fin("#gfree", tGraph + .4, .3, 14, 4)
fin("#grow", tAbout - .1, .3, 14, 4)
STAR_D = max(.8, min(1.5, a[5] - tAbout - .5))
js(f"tl.fromTo('#grow .star',{{rotation:-30,scale:.6}},{{rotation:360,scale:1,duration:{STAR_D:.3f},ease:'power2.out',immediateRender:false}},{tAbout:.3f});")
idle("#grow .star", tAbout + STAR_D, a[5], "scale", 1.14, .45)
idle("#gcard", a[4] + .5, a[5], "y", -8, .8)
sfx("riser.ogg", tAbout, -13); sfx("ding.ogg", tAbout + STAR_D, -8)
# --- 5 the map: nodes, links, then one look-up along the links; the bar refills (as the claim goes)
scene(5, a[5], a[6])
for i in range(6):
    pop(f"#nd{i}", a[5] + .06 + .06 * i, .28); fin(f".sc .nl:nth-of-type({i + 1})", a[5] + .2 + .06 * i, .25, 8, 3)
for i in range(6): pop(f"#dt{i}", a[5] + .3 + .05 * i, .24)
e0 = a[5] + .45; estep = min(.11, max(.05, (tLook - .2 - e0) / len(EDGE)))
for i in range(len(EDGE)):
    js(f"tl.to('#ed{i}',{{strokeDashoffset:0,duration:.3,ease:'power2.inOut'}},{e0 + i * estep:.3f});")
    if i % 3 == 0: sfx("click_a.ogg", e0 + i * estep, -14)
pop("#walk", tLook - .3, .26)
wstep = max(.25, min(.5, (a[6] - .5 - tLook) / 3))
for k in range(1, 4):
    x0, y0 = P[PATHN[0]]; x1, y1 = P[PATHN[k]]; t = tLook + (k - 1) * wstep
    js(f"tl.to('#walk',{{x:{x1 - x0},y:{y1 - y0},duration:{wstep * .8:.3f},ease:'power2.inOut'}},{t:.3f});")
    js(f"tl.to('#ed{PATHE[k - 1]}',{{stroke:'{ORA}',strokeWidth:13,duration:{wstep * .8:.3f},ease:'power2.inOut'}},{t:.3f});")
    sfx("select.ogg", t + wstep * .8, -12)
for i in range(6): idle(f"#dt{i}", a[5] + .9 + .1 * i, a[6], "scale", 1.3, .5)
# --- 6 the big number, then where it comes from
scene(6, a[6], a[7])
status(1, a[6] + .1)
js(f"tl.fromTo('#big70',{{scale:.55,opacity:0}},{{scale:1,opacity:1,duration:.45,ease:'back.out(1.5)',immediateRender:false}},{t70 - .08:.3f});")
idle("#big70", t70 + .45, tBut, "scale", 1.05, .5)
sfx("impactpunch.ogg", t70, -8)
slam("#bc", tBut, -8); sfx("impactpunch.ogg", tBut + .28, -5)
js(f"tl.to('#big70',{{scale:.93,rotation:-2,color:'#E3B5A3',duration:.4,ease:'power2.out'}},{tBut + .3:.3f});")
fin("#s6a", tBut + .5, .3, 12, 4); fin("#s6b", tBut + .68, .3, 12, 4)
idle("#bc", tBut + .7, a[7], "rotation", -5.5, .6)
# --- 7 other people's tests chip it down
scene(7, a[7], a[8])
for i, t in ((1, tR1), (2, tR2), (3, tR3)):
    js(f"tl.fromTo('#tr{i}',{{opacity:0,x:-70,rotation:-2}},{{opacity:1,x:0,rotation:0,duration:.36,ease:'back.out(1.4)',immediateRender:false}},{t - .1:.3f});")
    js(f"tl.fromTo('#tn{i}',{{scale:1}},{{scale:1.08,duration:.22,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false,transformOrigin:'0% 60%'}},{t + .26:.3f});")
    sfx("pop_a.ogg" if i == 1 else "impactsoft.ogg" if i == 2 else "click_b.ogg", t, -8 if i == 2 else -10)
    idle(f"#tr{i}", t + .75, a[8], "x", 8, .6)
# --- 8 the money verdict: Pro 1x against Max 5x, to scale
scene(8, a[8], a[9])
js(f"tl.to('#use',{{opacity:0,y:30,duration:.25,ease:'power2.in'}},{a[8] - .26:.3f});")
grow = lambda sel, t, d=.34: js(f"tl.to('{sel}',{{scaleY:1,duration:{d},ease:'power2.out'}},{t:.3f});")
grow("#bpro", a[8] + .12); pop("#x1", a[8] + .4, .28); sfx("pop_a.ogg", a[8] + .12, -10)
seg = min(.2, max(.1, (tNo - .3 - tFive) / 5))
for i in range(5): grow(f"#bm{i}", tFive + i * seg, seg * 1.5); sfx("tick.ogg", tFive + i * seg, -10)
pop("#x5", tFive + 5 * seg, .3); sfx("ding.ogg", tFive + 5 * seg, -9)
js(f"tl.fromTo('#dash',{{opacity:0,scaleX:0}},{{opacity:1,scaleX:1,duration:.4,ease:'power2.inOut',immediateRender:false}},{tFive + 5 * seg + .1:.3f});")
grow("#bext", tNo, .3); fin("#call", tNo + .05, .28, 10, 4); fin("#carr", tNo + .15, .28, 10, 4)
status(2, tClose)
slam("#nc", tClose, -7); sfx("impactpunch.ogg", tClose + .28, -5)
idle("#x5", tFive + 5 * seg + .4, a[9], "scale", 1.1, .5)
idle("#bext", tNo + .4, a[9], "opacity", .45, .35)
idle("#nc", tClose + .7, a[9], "rotation", -4.5, .6)
# --- 9 + 10 the saveable card
js(f"tl.fromTo('#sc9',{{opacity:0}},{{opacity:1,duration:.05,immediateRender:false}},{a[9]:.3f});")
js(f"tl.fromTo('#card',{{opacity:0,y:90,rotation:3,scale:1}},{{opacity:1,y:0,rotation:-1,duration:.5,ease:'power3.out',immediateRender:false}},{a[9] + .03:.3f});")
sfx("whoosh_b.ogg", a[9], -10)
rstep = min(.3, max(.16, (a[10] - a[9] - .7) / 5))
for i in range(5):
    t = a[9] + .3 + i * rstep
    js(f"tl.fromTo('#cr{i}',{{opacity:0,x:-46}},{{opacity:1,x:0,duration:.36,ease:'power3.out',immediateRender:false}},{t:.3f});")
    sfx("pop_a.ogg" if i % 2 == 0 else "pop_b.ogg", t, -11)
idle("#card", a[9] + .6, tF - .3, "rotation", .7, 1.2)
t = a[9] + .3 + 5 * rstep + .3; q = 0
while t < tF - .5:                                              # a slow wave keeps the card alive while it is read
    js(f"tl.fromTo('#cr{q % 5} .cnm',{{scale:1,rotation:0}},{{scale:1.2,rotation:{-12 if q % 2 else 12},duration:.26,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{t:.3f});"); t += .42; q += 1
t = a[9] + .3 + 5 * rstep + .2; q = 0
while t < tF - .75:
    js(f"tl.fromTo('#cr{q % 5} .mk',{{scaleX:0,opacity:.85}},{{scaleX:1,duration:.5,ease:'power2.inOut',immediateRender:false}},{t:.3f});")
    js(f"tl.to('#cr{q % 5} .mk',{{opacity:0,duration:.25,ease:'sine.in'}},{t + .5:.3f});"); t += .62; q += 1
idle("#card", a[9] + .6, tF - .3, "y", -12, .8)
js(f"tl.to('#card',{{opacity:0,scale:.9,y:-40,rotation:-3,duration:.32,ease:'power2.in'}},{tF - .26:.3f});")
sfx("whoosh_c.ogg", tF - .2, -12)
# --- loop seam: frame 0 comes back
fin("#sc1", tF + .06, .42)
js(f"tl.set('#t1b',{{x:0,y:0,rotation:0}},{tF:.3f});"); js(f"tl.set('#tn_a,#tn_b',{{opacity:0}},{tF:.3f});")
js(f"tl.fromTo('#use',{{opacity:0,y:30}},{{opacity:1,y:0,duration:.4,ease:'power2.out',immediateRender:false}},{tF + .06:.3f});")
fout("#st2", tF - .2, .18)

# ---------------------------------------------------------------- render(): the usage bar, the read counters, the star counter (all from the clock)
KF = [(0, 88), (tPlug - .08, 31), (tPlug + .7, 100), (tSo - .1, 100), (h0 + NH * hstep, 17), (a[5] + .5, 17), (tLook + 3 * wstep, 97),
      (tBut + .28, 97), (tBut + .6, 78), (a[7], 70)]
DATA = dict(D=D, tF=round(tF, 3), KF=[[round(t, 3), p] for t, p in KF], HOPS=HOPS, tQ=round(a[7], 3), tS=tAbout, sD=round(STAR_D, 3), STARS=STARS)
RJS = r'''
const Dt=__DATA__;
const ez=p=>{p=p<0?0:p>1?1:p;return p*p*(3-2*p)}, lerp=(a,b,t)=>a+(b-a)*t, $=s=>document.querySelector(s);
const uf=$('#uf'), up=$('#upn'), upe=$('#up em'), stn=$('#stn'), rd=[0,1,2,3,4,5].map(c=>$('#rd'+c));
function pct(v){const K=Dt.KF; if(v>=Dt.tF) return 100+(K[0][1]-100)*ez((v-Dt.tF)/.5); if(v<=K[0][0]) return K[0][1];
  for(let i=1;i<K.length;i++) if(v<K[i][0]) return lerp(K[i-1][1],K[i][1],ez((v-K[i-1][0])/(K[i][0]-K[i-1][0])));
  return K[K.length-1][1]}
function render(v){
  const q=v>=Dt.tQ&&v<Dt.tF;                                  // from the tests on: nobody can say (it depends on the project)
  const p=q?52+20*Math.sin((v-Dt.tQ)*2.6):pct(v);
  uf.style.width=p.toFixed(2)+'%'; uf.style.backgroundPosition=(-(v*46)%136).toFixed(1)+'px 0';
  up.textContent=q?'?':Math.round(p)+'%'; upe.style.opacity=q?0:1; up.style.color=(!q&&p<35)?'#D9281C':'#0f0f0f';
  up.style.display='inline-block'; up.style.transform='scale('+(1+(q?.08*Math.sin(v*5):0)).toFixed(3)+')';
  const n=[1,1,1,1,1,1]; for(const h of Dt.HOPS) if(v>=h[0]) n[h[1]]++;
  for(let c=0;c<6;c++) rd[c].textContent='read ×'+n[c];
  stn.textContent=(Dt.STARS*ez((v-Dt.tS)/Dt.sD)).toFixed(1)+'k';
}
'''.replace("__DATA__", json.dumps(DATA, separators=(",", ":")))

NEWS = [(0, "the viral claim, the two marks, the usage bar"), (tFree, "FREE"), (tPlug, "the tool plugs in, the bar refills (the claim looks true)"), (tCC, "the name Claude Code"),
        (tP20, "PRO $20"), (tDoes, "the '=' (claim)"), (tP100, "MAX $100"), (a[3], "six file cards: a new chat starts from zero"), (h0, "files read again, counters rise, the bar drains (to " + f"{h0 + NH * hstep:.1f} s)"),
        (tGraph - .1, "Graphify card, free + open source"), (tAbout, f"the star count runs to 148.2k (to {tAbout + STAR_D:.1f} s)"), (a[5], "the map: nodes and links"),
        (tLook, f"one look-up along the links, the bar refills (to {tLook + 3 * wstep:.1f} s)"), (a[6], "status CHECKING, the claim headline"), (t70, "the giant 70x"),
        (tBut + .3, "BEST CASE stamp, then: one example, about 52 files"), (a[7], "REAL TESTS, the bar turns to '?'"), (tR1, "18% fewer"), (tR2, "+49.5% more"), (tR3, "issue #985: no savings"),
        (a[8] + .12, "Pro bar, 1x"), (tFive, f"Max bar grows to 5x (to {tFive + 5 * seg:.1f} s)"), (tNo, "the best test as a thin slice on the Pro bar"), (tClose + .3, "NOT CLOSE stamp"),
        (a[9], f"the saveable card, five rows (to {a[9] + .3 + 5 * rstep:.1f} s)"), (a[10], "tomorrow headline (PLACEHOLDER: no picture of the next episode yet)"), (tF, "frame 0 returns (loop)")]
NEWS = sorted((round(t, 2), x) for t, x in NEWS)
FLAT = [(NEWS[i][0], NEWS[i + 1][0], NEWS[i][1]) for i in range(len(NEWS) - 1) if NEWS[i + 1][0] - NEWS[i][0] > 2.5]
JS = re.sub(r"tl\.set\(([^,]+),\{", r"tl.set(\1,{immediateRender:false,", "\n".join(J))
SFX.sort(key=lambda x: x["t"])
json.dump(SFX, open(H_ + "/sfx100.json", "w"), indent=1)
if os.environ.get("SHIP") == "1" and (STALE or PH_L10):
    sys.exit(f"SHIP=1 refused: estimated timeline={STALE}, line 10 placeholder={PH_L10}")
ROLE = ["hook: the viral claim", "the money claim", "the problem (real)", "the tool + stars", "how it works", "reveal 1: where 70 comes from",
        "reveal 2: other people's tests", "reveal 3: the money verdict", "saveable card + link in bio", "tomorrow (PLACEHOLDER)" if PH_L10 else "tomorrow"]
json.dump(dict(placeholder=dict(estimated_timeline=STALE, line10=PH_L10, claude_code_mark="Claude symbol + the words 'Claude Code' (no Claude Code-specific mark sourced)",
                                screenshots="none: drawn cards with dated numbers instead of real repo/pricing screenshots"),
               lines=[dict(n=n, text=LINES[n - 1], start=round(s(n), 3), end=round(e(n), 3), role=ROLE[n - 1]) for n in range(1, NL + 1)],
               D=D, frame0_returns=round(tF, 3),
               sync={k: dict(t=v, source=SRC[k]) for k, v in (("killed", tPlug), ("now", tNow), ("so", tSo), ("about", tAbout), ("once", tOnce), ("looks", tLook), ("but", tBut),
                                                             ("one_saves", tR1), ("one_uses", tR2), ("five", tFive), ("nothing", tNo), ("close", tClose), ("seventy", t70), ("free", tFree), ("tool", tTool), ("claude", tCC), ("twenty", tP20), ("hundred", tP100), ("does", tDoes), ("graphify", tGraph))},
               usage_bar=dict(note="ILLUSTRATION, tagged on screen; '?' from line 7 on; hidden in line 8", keyframes=DATA["KF"]),
               buildup=dict(new_on_screen=[dict(t=t, what=x) for t, x in NEWS], flat_over_2_5s=[dict(start=a_, end=b_, after=x) for a_, b_, x in FLAT]), numbers_on_screen=NUMBERS, headlines_draft=[dict(t=t, text=x) for t, x in sorted(HLOG)]), open(H_ + "/cues100.json", "w"), indent=1)
html = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Black.otf");font-weight:900}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-ExtraBold.otf");font-weight:800}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Medium.otf");font-weight:500}}
{CSS}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
{markup}
</div>
<script>
{RJS}
const D={D}; const tl=gsap.timeline({{paused:true}});
// a clock, not a motion: GSAP writes the time into clk.v and the setter draws the clock-driven parts for that time
let _v=0; const clk={{get v(){{return _v}},set v(x){{_v=x;render(x)}}}};
tl.fromTo(clk,{{v:0}},{{v:D,duration:D,ease:'none',immediateRender:false}},0);
{JS}
tl.to({{}},{{duration:.001}},D-.001);
window.__timelines=window.__timelines||{{}}; window.__timelines["main"]=tl; tl.seek(0); render(0);
window.__reel={{duration:D,seek:t=>{{tl.seek(t)}}}};
</script></body></html>'''
os.makedirs(H_ + "/out", exist_ok=True)
open(H_ + "/hf/index.html", "w").write(html)
say(f"estimated timeline={STALE}  line 10 placeholder={PH_L10}  D={D}  js={len(J)} sfx={len(SFX)}")
say("lines: " + "  ".join(f"{n}:{s(n):.2f}-{e(n):.2f}" for n in range(1, NL + 1)))
say("sync: " + "  ".join(f"{k}={v['t']}({'w' if v['source'] == 'words.json' else 'EST'})" for k, v in json.load(open(H_ + '/cues100.json'))["sync"].items()))
for t, x in NEWS: say(f"  new {t:6.2f}  {x}")
say("FLAT stretches over 2.5 s with nothing new: " + (str(FLAT) if FLAT else "none"))
hs = sorted(HLOG)
say("headlines (draft): " + " | ".join(f"{t:.2f} {x}" for t, x in hs))
open(H_ + "/out/build.log", "w").write("\n".join(LOG) + "\n")
