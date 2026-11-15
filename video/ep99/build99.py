#!/usr/bin/env python3
"""ep99 'AI RACE #2' (the maze) scene SCAFFOLD, Miki style, HyperFrames + GSAP paused timeline, 1080x1920.
Model: video/ep98/build98.py. Everything on the stage is driven by the results file, so it works for any outcome
(one winner, several, nobody out, a dot that never starts).

Reads   RESULTS (env) or arena/maze-race.json (the real run); if that file is missing: arena/ref-maze-race.json
        = PLACEHOLDER (our two reference bots, not AIs). arena/maze.json. voice/lines.txt,
        voice/narration-raw-cues.json, voice/words.json (all optional: without them PLACEHOLDER lines and an
        ESTIMATED timeline are used).
Writes  hf/index.html, cues99.json (lines, D, race clock, EVENTS with video times), sfx99.json.

PLACEHOLDER GUARD: if the results file does not hold exactly the five AI ids, or the script is the built-in
placeholder, a red PLACEHOLDER banner is drawn on every frame, cues99.json says so, and SHIP=1 refuses to build.

LINES (voice/lines.txt, one per line, at least 7):
  1 hook   2 premise (the request is shown going to the five AIs)   3 rules, LAST WORD "Go" (the race starts on it)
  4 .. NL-3  race lines (one or more; the race plays from "Go" to just before line NL-2)
  NL-2 result (the board lands, winner row last)   NL-1 send line   NL tomorrow line

What is true on screen, and what is a scene choice:
  - Every dot position is paths[] of the results file, cell by cell. The trail is that same path.
  - The step counter is the real step number. The race clock is COMPRESSED and not uniform (scene choice):
    the steps before the first and before the last exit play slower; after the last exit the rest of the 500
    steps runs fast (the counter shows it). cues99.json lists steps per second for each part.
  - 'steps to the exit' under each chip = shortest way out from the dot's cell (computed here from maze.json).
  - Scene choices: dots are drawn larger than a cell so the logos read; they start fanned around the centre
    cell and run a few px apart in a corridor (all five really share the same cells); a dot that got out
    flies to its chip.
No TTS, no audio is written here.
"""
import json, os, re, math, shutil, sys
from collections import deque
H_ = os.path.dirname(os.path.abspath(__file__))
INK = "#0f0f0f"; PAPER = "#fbfbf8"; RED = "#E5372B"; GREEN = "#27A35B"
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
LOG = []
def say(x): LOG.append(x); print(x)

# ---------------------------------------------------------------- assets (fonts, paper, real logos: copied from the ep98 build, unchanged)
for sub in ("fonts/InterDisplay-Black.otf", "fonts/InterDisplay-ExtraBold.otf", "fonts/InterDisplay-Medium.otf", "bg.jpg",
            "logos/chatgpt.svg", "logos/gemini.svg", "logos/claude.svg", "logos/meta-ai.svg", "logos/perplexity.svg", "logos/SOURCES.md"):
    dst = f"{H_}/hf/assets/{sub}"
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(f"{H_}/../ep98/hf/assets/{sub}", dst)

IDS = ["chatgpt", "gemini", "claude", "meta", "perplexity"]          # fixed order of the chips, never re-sorted
NAME = {"chatgpt": "ChatGPT", "gemini": "Gemini", "claude": "Claude", "meta": "Meta AI", "perplexity": "Perplexity"}
COL = {"chatgpt": "#10A37F", "gemini": "#4285F4", "claude": "#D97757", "meta": "#B44BFF", "perplexity": "#20808D"}
LOGO = {"chatgpt": "chatgpt.svg", "gemini": "gemini.svg", "claude": "claude.svg", "meta": "meta-ai.svg", "perplexity": "perplexity.svg"}

# ---------------------------------------------------------------- results
MZ = json.load(open(H_ + "/arena/maze.json"))
RPATH = os.environ.get("RESULTS") or H_ + "/arena/maze-race.json"
if not os.path.exists(RPATH): RPATH = H_ + "/arena/ref-maze-race.json"
R = json.load(open(RPATH))
MAXS = R.get("constants", {}).get("MAX_STEPS", 500); SHORT = R.get("shortestSteps")
rres = {x["id"]: x for x in R["result"]}; rpath = {x["id"]: x["path"] for x in R["paths"]}
PH_DATA = sorted(rres) != sorted(IDS)
if PH_DATA:                                                 # PLACEHOLDER: the bots of the file fill the five slots in turn
    src = [x["id"] for x in R["result"]]
    RES = {k: dict(rres[src[c % len(src)]]) for c, k in enumerate(IDS)}
    PATH = {k: rpath[src[c % len(src)]] for c, k in enumerate(IDS)}
    PH_MAP = {k: src[c % len(src)] for c, k in enumerate(IDS)}
else:
    RES = {k: dict(rres[k]) for k in IDS}; PATH = {k: rpath[k] for k in IDS}; PH_MAP = {}
W_, HH = MZ["width"], MZ["height"]; OPEN = [[int(ch, 16) for ch in row] for row in MZ["open"]]
START = (MZ["start"]["x"], MZ["start"]["y"]); EXIT = (MZ["exit"]["x"], MZ["exit"]["y"])
assert MZ["exit"]["side"] == "left" and W_ == HH, "the stage is laid out for a square maze with the exit on the left wall"
inside = lambda x, y: 0 <= x < W_ and 0 <= y < HH
MOVES = ((0, -1, 1), (1, 0, 2), (0, 1, 4), (-1, 0, 8))
# steps to get out from every cell (breadth-first from the exit; the exit cell = 1 step)
DIST = {EXIT: 1}; dq = deque([EXIT])
while dq:
    x, y = dq.popleft()
    for dx, dy, b in MOVES:
        n = (x + dx, y + dy)
        if OPEN[y][x] & b and inside(*n) and n not in DIST: DIST[n] = DIST[(x, y)] + 1; dq.append(n)
dist = lambda c: DIST.get((c[0], c[1]), 0) if inside(c[0], c[1]) else 0
DEG = {(x, y): sum(1 for dx, dy, b in MOVES if OPEN[y][x] & b and inside(x + dx, y + dy)) for x in range(W_) for y in range(HH)}
if SHORT is not None: assert DIST[START] == SHORT, "maze.json and the results file disagree on the shortest way out"
for k in IDS:                                               # every step of every path must be a legal move
    p = PATH[k]; assert tuple(p[0]) == START, k
    for i in range(1, len(p)):
        a, b = p[i - 1], p[i]
        if a == b: continue
        assert inside(*a) and abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1, f"{k}: jump at step {i}"
        bit = next(bb for dx, dy, bb in MOVES if (dx, dy) == (b[0] - a[0], b[1] - a[1]))
        assert OPEN[a[1]][a[0]] & bit, f"{k}: through a wall at step {i}"
STATUS = {k: RES[k]["status"] for k in IDS}                # exit | dnf | error
LAST = {k: len(PATH[k]) - 1 for k in IDS}                   # last step the dot has a cell for
XSTEP = {k: RES[k]["exitStep"] for k in IDS if STATUS[k] == "exit"}
FINS = sorted(XSTEP, key=lambda k: (XSTEP[k], IDS.index(k)))
ERRS = [k for k in IDS if STATUS[k] == "error"]; DNFS = [k for k in IDS if STATUS[k] == "dnf"]
def rank(k):
    r = RES[k]
    return (0, r["exitStep"], 0, IDS.index(k)) if STATUS[k] == "exit" else (1, r.get("closestDist") or 9999, r.get("closestStep") or 9999, IDS.index(k))
ORDER = sorted(IDS, key=(rank if PH_DATA else lambda k: RES[k]["place"]))
PLACE = {k: i + 1 for i, k in enumerate(ORDER)}
WINNER = FINS[0] if FINS else None
cell = lambda k, i: PATH[k][min(i, LAST[k])]
S1 = max(XSTEP.values()) if FINS else MAXS                  # the main part of the race clock ends here
S1 = max(S1, 1)
TAIL = bool(FINS) and S1 < MAXS and any(LAST[k] > S1 for k in IDS if k not in XSTEP)

# ---------------------------------------------------------------- race events (data only; steps)
EV = []                                                     # dict(kind, id, step, ...)
for k in FINS: EV.append(dict(kind="exit", id=k, step=XSTEP[k], place=FINS.index(k) + 1))
for k in ERRS: EV.append(dict(kind="error_stop", id=k, step=LAST[k]))
for k in DNFS: EV.append(dict(kind="dnf_freeze", id=k, step=LAST[k], closest=RES[k].get("closestDist"), closestAt=RES[k].get("closestAt")))
DEADS = {k: [] for k in IDS}
for k in IDS:
    p = PATH[k]; best = dist(p[0]); bi = 0; flagged = None; nm = 0
    for i in range(1, LAST[k] + 1):
        c = tuple(p[i])
        if not inside(*c): break
        if c != tuple(p[i - 1]) and DEG[c] == 1 and c != START:
            DEADS[k].append([i, c[0], c[1]]); EV.append(dict(kind="dead_end", id=k, step=i, cell=list(c)))
        d = dist(c)
        if d < best: best, bi = d, i
        elif d - best >= 12 and best <= 30 and flagged != best and nm < 2 and (STATUS[k] != "exit" or i < XSTEP[k]):
            flagged = best; nm += 1; EV.append(dict(kind="near_miss", id=k, step=bi, closest=best, cell=list(p[bi])))
D0 = DIST[START]; half = None
for i in range(S1 + 1):                                     # milestones of the front dot
    m = min(dist(cell(k, i)) for k in IDS if inside(*cell(k, i))) if any(inside(*cell(k, i)) for k in IDS) else 0
    if half is None and m <= D0 // 2 and not (FINS and i >= XSTEP[FINS[0]]):
        half = i; EV.append(dict(kind="halfway", id=min(IDS, key=lambda k: dist(cell(k, i)) if inside(*cell(k, i)) else 999), step=i, steps_to_exit=m))
if FINS and XSTEP[FINS[0]] > 14: EV.append(dict(kind="final_stretch", id=FINS[0], step=XSTEP[FINS[0]] - 12, steps_to_exit=12))
# leader = the dot still running with the fewest steps to the exit; a change counts once it has held 8 steps
LEADRAW = []
for i in range(S1 + 1):
    alive = [k for k in IDS if not (k in XSTEP and i >= XSTEP[k]) and not (k in ERRS and i >= LAST[k])]
    if FINS and i >= XSTEP[FINS[0]] or not alive or i < 6: LEADRAW.append(-1); continue
    LEADRAW.append(IDS.index(min(alive, key=lambda k: (dist(cell(k, i)), IDS.index(k)))))
LEAD = [-1] * (S1 + 1); cur = -1
for i in range(S1 + 1):
    if LEADRAW[i] == -1: cur = -1
    elif LEADRAW[i] != cur and all(LEADRAW[min(S1, j)] == LEADRAW[i] for j in range(i, i + 8)):
        if cur != -1: EV.append(dict(kind="lead_change", id=IDS[LEADRAW[i]], step=i, was=IDS[cur], steps_to_exit=dist(cell(IDS[LEADRAW[i]], i))))
        else: EV.append(dict(kind="first_leader", id=IDS[LEADRAW[i]], step=i))
        cur = LEADRAW[i]
    LEAD[i] = cur
EV.sort(key=lambda x: (x["step"], x["kind"]))

# ---------------------------------------------------------------- script lines + cues (placeholder lines and an estimated timeline until the voice exists)
PH_LINES = ["PLACEHOLDER HOOK: five AIs, one maze, not all get out.",
            "PLACEHOLDER: same job for all five, get the dot out of the maze.",
            "PLACEHOLDER: no map, five hundred steps. Go!",
            "PLACEHOLDER race line one, on a real event.", "PLACEHOLDER race line two, on a real event.", "PLACEHOLDER race line three, on a real event.",
            "PLACEHOLDER result line, the winner is named here.",
            "PLACEHOLDER: send it to a friend.",
            "PLACEHOLDER tomorrow line."]
LP = H_ + "/voice/lines.txt"
PH_SCRIPT = not os.path.exists(LP)
LINES = PH_LINES if PH_SCRIPT else [l.strip() for l in open(LP) if l.strip()]
NL = len(LINES); assert NL >= 7, "need at least 7 lines: hook, premise, rules+Go, 1+ race lines, result, send, tomorrow"
nRES, nSEND, nTOM = NL - 2, NL - 1, NL; RACE_LINES = list(range(4, NL - 2))
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
        d = 2.9 if (PH_SCRIPT and n in RACE_LINES) else 2.2 if (PH_SCRIPT and n in (1, 3)) else round(.3 + .045 * len(LINES[n - 1]), 2)
        L[n] = (round(t, 2), round(t + d, 2)); t += d + .12
else:
    L = {n: (float(CUE[n]["start"]), float(CUE[n]["end"])) for n in range(1, NL + 1)}
s = lambda n: L[n][0]
e = lambda n: L[n][1]
def W(word, n, k=0):
    c = 0
    for w, a, b in WORDS:
        if s(n) - .12 <= a <= e(n) + .12 and norm(w) == word:
            if c == k: return a
            c += 1
    return None
SRC = {}
T0 = W("go", 3)
if T0 is None: T0 = s(3) + .86 * (e(3) - s(3)); SRC["go"] = "ESTIMATE (line fraction)"
else: SRC["go"] = "words.json"
T0 = round(T0, 3)
D = round(e(NL) + .4, 2)
tF = D - .58                                                 # the frame-0 layout comes back from here
tK = s(nRES)                                                 # the board
vEND = tK - .35                                              # the race clock has reached its last step
TAILD = 1.1 if TAIL else 0.0
vM0 = T0 + .25; vM1 = vEND - TAILD                           # main part: steps 0..S1
assert vM1 - vM0 > 2.0, "the race lines leave under 2 s for the race"

# ---------------------------------------------------------------- race clock: step for every video frame (compressed, slower before the first and the last exit)
wt = [1.0] * (S1 + 1)                                        # wt[i] = screen-time weight of step i-1 -> i
if FINS:
    f1 = XSTEP[FINS[0]]
    for i in range(max(1, f1 - 12), f1 + 1): wt[i] = 3.2
    if len(FINS) > 1:
        for i in range(max(1, S1 - 8), S1 + 1): wt[i] = max(wt[i], 2.4)
else:
    for i in range(max(1, S1 - 25), S1 + 1): wt[i] = 2.0     # nobody gets out: the last steps play slower (will anyone make it?)
for i in range(1, min(8, S1) + 1): wt[i] = max(wt[i], 2.5 - .2 * i)   # soft start
cumw = [0.0]
for i in range(1, S1 + 1): cumw.append(cumw[-1] + wt[i])
def v_of(step):                                              # video time of a (fractional) step
    if step <= S1:
        i = int(step); f = step - i
        w_ = cumw[i] + (f * wt[i + 1] if i < S1 else 0)
        return vM0 + (vM1 - vM0) * w_ / cumw[S1]
    return vM1 + TAILD * (step - S1) / max(1, MAXS - S1)
def step_of(v):
    if v <= vM0: return 0.0
    if v >= vEND: return float(MAXS if (TAIL or not FINS) else S1)
    if v >= vM1: return S1 + (MAXS - S1) * (v - vM1) / TAILD
    tgt = (v - vM0) / (vM1 - vM0) * cumw[S1]; lo, hi = 0, S1
    while lo < hi:
        m = (lo + hi + 1) // 2
        if cumw[m] <= tgt: lo = m
        else: hi = m - 1
    return lo + ((tgt - cumw[lo]) / wt[lo + 1] if lo < S1 else 0)
ST = [round(step_of(n / 60), 3) for n in range(int(D * 60) + 4)]
for x in EV: x["v"] = round(v_of(x["step"]) if x["kind"] != "dnf_freeze" else vEND, 3)
VX = {k: round(v_of(XSTEP[k]), 3) for k in FINS}
VE = {k: round(v_of(LAST[k]), 3) for k in ERRS}

# ---------------------------------------------------------------- page geometry
CELL = 38; MW = CELL * W_                                    # maze 798 px at race scale
MXR, MYR = (1080 - MW) // 2, 1248 - MW                       # race: x 141-939, y 450-1248 (down to the edge of the safe box)
CXS = [160, 350, 540, 730, 920]; CHD = 100                   # frame 0: the five chips in a row
try:
    from PIL import ImageFont
    _f = ImageFont.truetype(H_ + "/hf/assets/fonts/InterDisplay-Black.otf", 100)
    _f8 = ImageFont.truetype(H_ + "/hf/assets/fonts/InterDisplay-ExtraBold.otf", 100)
    tw = lambda t: _f.getlength(t) - 3.0 * len(t)
    tw8 = lambda t: _f8.getlength(t) - 1.0 * len(t)
except Exception:
    tw = lambda t: 62 * len(t); tw8 = lambda t: 56 * len(t)
HOOK = ["FIVE AIs. ONE MAZE.", "[HOOK PLACEHOLDER]"] if PH_SCRIPT else [x.strip() for x in open(H_ + "/voice/hook-display.txt") if x.strip()][:2] if os.path.exists(H_ + "/voice/hook-display.txt") else ["FIVE AIs. ONE MAZE."]
HFS = min(104, 900 / max(tw(x) / 100 for x in HOOK))
HBOT = 338 + len(HOOK) * HFS * .98
CHY = round(HBOT + 26 + CHD / 2)                             # chips row centre (frame 0)
MY0 = CHY + CHD // 2 + 30; S0 = round((1248 - MY0) / MW, 4); MX0 = round(540 - MW * S0 / 2, 1)   # frame-0 maze: under the chips, down to y 1248
RXS = [93 + 128 * c for c in range(5)]; RY, RS = 309, .56     # each chip is followed by its steps-to-the-exit number     # race: the chips as a status row at the top of the safe box
FAN = [[round(46 * math.cos(math.radians(-90 + 72 * c)), 1), round(46 * math.sin(math.radians(-90 + 72 * c)), 1)] for c in range(5)]
OFF = [[round(6.5 * math.cos(math.radians(-90 + 72 * c)), 1), round(6.5 * math.sin(math.radians(-90 + 72 * c)), 1)] for c in range(5)]
lx = lambda x: (x + .5) * CELL
def logo(k, h, cls=""):
    if k == "perplexity":                                   # raw file, icon part only (x 0-28.14 of 149.82)
        return f'<span class="pxl {cls}" style="width:{h * 28.14 / 36:.1f}px;height:{h}px"><img src="assets/logos/perplexity.svg" style="height:{h}px;width:{h * 149.82 / 36:.1f}px"></span>'
    return f'<img class="lg {cls}" src="assets/logos/{LOGO[k]}" style="width:{h}px;height:{h}px">'
def badge(k, d, cls="", st=""):
    return f'<div class="bdg {cls}" style="width:{d}px;height:{d}px;{st}">{logo(k, round(d * .62))}</div>'
J = []; SFX = []
def js(x): J.append(x)
def sfx(f, t, g=-8): SFX.append(dict(f=f, t=round(max(0, t), 3), g=g))
def fin(sel, t, d=.36, y=20, blur=8):
    js(f"tl.fromTo('{sel}',{{opacity:0,y:{y},filter:'blur({blur}px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:{d},ease:'power2.out',immediateRender:false}},{max(0, t):.3f});")
def fout(sel, t, d=.22):
    js(f"tl.to('{sel}',{{opacity:0,y:-12,filter:'blur(8px)',duration:{d},ease:'power2.inOut'}},{max(0, t):.3f});")

# ---------------------------------------------------------------- headlines (one line under the status row; plain ink, no boxes, no code words). ALL TEXT IS DRAFT.
HEADS = []; HLOG = []
def head(i, t_in, t_out, l1, logos=(), size=96, top=None, l2=""):
    wl = len(logos) * 86
    fs = min(size, 900 / max((tw(l1) + wl * 100 / 84) / 100, tw(l2) / 100 if l2 else .01))
    lg = "".join(logo(k, round(fs * .86), "hlg") for k in logos)
    tp = top if top is not None else 342 + max(0, (100 - fs) / 2)
    l2h = f'<div class="hl2">{l2}</div>' if l2 else ""
    HEADS.append(f'<div class="hd" id="h{i}" style="top:{tp:.0f}px;font-size:{fs:.1f}px;line-height:{fs * .98:.1f}px"><div class="hl1">{lg}<span>{l1}</span></div>{l2h}</div>')
    if t_in is not None: fin(f"#h{i}", t_in)
    if t_out is not None: fout(f"#h{i}", t_out - .24)
    HLOG.append((round(t_in or 0, 2), l1))
a2, d2, a3, d3 = s(2), e(2) - s(2), s(3), e(3) - s(3)
t500 = W("five", 3); t500 = t500 if t500 is not None else a3 + .42 * d3
t500 = min(max(t500, a3 + .5), T0 - .5)
head(0, None, a2 - .02, HOOK[0], size=104, top=338, l2=HOOK[1] if len(HOOK) > 1 else "")
head(1, a2, a3, "ONE JOB: GET OUT.")
head(2, a3, t500, "NO MAP.", size=110)
head(3, t500, T0 - .04, f"{MAXS} STEPS.", size=110)
HEADS.append('<div class="hd go" id="hgo"><div class="hl1"><span>GO!</span></div></div>')
js(f"tl.fromTo('#hgo',{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.3,ease:'power3.out',immediateRender:false}},{T0:.3f});")
js(f"tl.to('#hgo',{{opacity:0,scale:1.2,duration:.26,ease:'power2.in'}},{T0 + .55:.3f});")
# race headlines: picked from the events. exit > near miss > lead change > first dead end; at least 1.25 s apart (an exit always shows)
PRI = dict(exit=4, error_stop=3, near_miss=3, final_stretch=3, lead_change=2, halfway=2, dead_end=1, first_leader=0)
DEADTX = ["DEAD END!", "WRONG WAY!", "BACK AGAIN!"]
def htext(x):
    n = NAME[x["id"]].upper()
    if x["kind"] == "exit": return (f"{n} IS OUT!" if x["place"] == 1 else f"{n} IS OUT TOO")
    if x["kind"] == "error_stop": return f"{n} STOPS"
    if x["kind"] == "near_miss": return f"SO CLOSE! {x['closest']} TO GO"
    if x["kind"] == "lead_change": return f"{n} LEADS NOW"
    if x["kind"] == "halfway": return "HALFWAY THERE"
    if x["kind"] == "final_stretch": return "12 STEPS TO GO..."
    if x["kind"] == "dead_end": return DEADTX[x.get("_n", 0) % 3]
picked = []; seen_dead = False
for x in sorted((x for x in EV if x["kind"] in PRI and PRI[x["kind"]] > 0 and T0 + 1.3 < x["v"] < vEND - .2 or x["kind"] == "exit"), key=lambda x: x["v"]):
    if x["kind"] == "dead_end":
        if seen_dead: continue
    if picked and x["v"] - picked[-1]["v"] < 1.25:
        if PRI[x["kind"]] > PRI[picked[-1]["kind"]] and x["v"] - picked[-1]["v"] < .5: picked[-1] = x
        elif x["kind"] == "exit": picked.append(x)
        continue
    picked.append(x); seen_dead = seen_dead or x["kind"] == "dead_end"
RH = [(T0 + .62, "FIND THE EXIT", ())] + [(x["v"], htext(x), (x["id"],)) for x in picked]
# no flat stretch: a hold longer than 2.5 s gets a dead-end beat of some dot from the data (if there is one in it)
nfill = 1
for _ in range(12):
    RH.sort(); ts = [x[0] for x in RH] + [vEND]
    g = next((i for i in range(len(RH)) if ts[i + 1] - ts[i] > 2.5), None)
    if g is None: break
    mid = (ts[g] + ts[g + 1]) / 2
    cand = [x for x in EV if x["kind"] == "dead_end" and ts[g] + 1.1 < x["v"] < ts[g + 1] - 1.1]
    if not cand: break
    x = min(cand, key=lambda x: abs(x["v"] - mid)); x["_n"] = nfill; nfill += 1
    RH.append((x["v"], htext(x), (x["id"],)))
RH.sort()
nd = len(DNFS) + len(ERRS)
if not FINS: RH.append((vEND, "NOBODY GETS OUT", ()))
elif nd and TAIL: RH.append((vM1 + .1, (f"{NAME[DNFS[0]].upper()} IS STILL LOST" if nd == 1 and DNFS else f"{nd} STILL INSIDE"), tuple(DNFS[:1]) if nd == 1 else ()))
RH = [x for i, x in enumerate(RH) if i == 0 or x[0] - RH[i - 1][0] > .35]
tS8 = s(nSEND)
for i, (t, txt, lg) in enumerate(RH):
    head(10 + i, t, RH[i + 1][0] if i + 1 < len(RH) else tK, txt, logos=lg)
head(40, tK, tS8, (f"{NAME[WINNER].upper()} WINS" if WINNER else "NOBODY WINS"), logos=(WINNER,) if WINNER else ())
head(41, tS8, s(nTOM), "SEND IT TO A FRIEND")
head(42, s(nTOM), tF + .04, "NEXT: [PLACEHOLDER]" if PH_SCRIPT else "NEXT RACE", size=100)
fin("#h0", tF + .06, .42)

# ---------------------------------------------------------------- markup: the maze (local px, scaled by render()), trails, exit, start, marks
hw = []; vw = []
for gy in range(HH + 1):                                    # horizontal wall runs
    run = None
    for x in range(W_ + 1):
        wall = x < W_ and (not OPEN[gy][x] & 1 if gy < HH else not OPEN[gy - 1][x] & 4)
        if wall and run is None: run = x
        if not wall and run is not None: hw.append(f"M{run * CELL} {gy * CELL} H{x * CELL}"); run = None
for gx in range(W_ + 1):
    run = None
    for y in range(HH + 1):
        wall = y < HH and (not OPEN[y][gx] & 8 if gx < W_ else not OPEN[y][gx - 1] & 2)
        if wall and run is None: run = y
        if not wall and run is not None: vw.append(f"M{gx * CELL} {run * CELL} V{y * CELL}"); run = None
TRD = []; CLEN = []
for c, k in enumerate(IDS):
    pts_ = [(lx(p[0]) + OFF[c][0], lx(p[1]) + OFF[c][1]) for p in PATH[k]]
    acc = [0.0]
    for i in range(1, len(pts_)): acc.append(acc[-1] + math.hypot(pts_[i][0] - pts_[i - 1][0], pts_[i][1] - pts_[i - 1][1]))
    CLEN.append([round(v, 1) for v in acc]); TRD.append("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts_))
ey = lx(EXIT[1])
dead_marks = "".join(f'<path class="dm" data-c="{c}" data-s="{i}" d="M{lx(x) - 8:.0f} {lx(y) - 8:.0f} l16 16 m0 -16 l-16 16"/>' for c, k in enumerate(IDS) for i, x, y in DEADS[k][:14])
close_marks = "".join(f'<circle class="cm" data-c="{c}" cx="{lx(RES[k]["closestAt"][0]):.0f}" cy="{lx(RES[k]["closestAt"][1]):.0f}" r="15" stroke="{COL[k]}"/>'
                      for c, k in enumerate(IDS) if STATUS[k] != "exit" and RES[k].get("closestAt"))
maze = f'''<div id="maze"><div class="floor" data-decor></div>
 <svg class="msv" viewBox="0 0 {MW} {MW}" width="{MW}" height="{MW}">
  <defs><filter id="wob" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".03" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="2.6"/></filter></defs>
  <rect id="stc" x="{START[0] * CELL + 3}" y="{START[1] * CELL + 3}" width="{CELL - 6}" height="{CELL - 6}" rx="6" fill="#FFE28A"/>
  <rect id="exc" x="{EXIT[0] * CELL + 3}" y="{EXIT[1] * CELL + 3}" width="{CELL - 6}" height="{CELL - 6}" rx="6" fill="{GREEN}" opacity=".3"/>
  <g id="trs">{"".join(f'<path class="trl" d="{TRD[c]}" stroke="{COL[k]}" stroke-dasharray="{CLEN[c][-1] + 2:.1f}" stroke-dashoffset="{CLEN[c][-1] + 2:.1f}"/>' for c, k in enumerate(IDS))}</g>
  <g id="walls" filter="url(#wob)" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"><path d="{" ".join(hw)} {" ".join(vw)}"/></g>
  <g id="dms">{dead_marks}</g><g id="cms">{close_marks}</g>
  <g id="exm"><path d="M-12 {ey} H-62 M-40 {ey - 20} L-64 {ey} L-40 {ey + 20}" fill="none" stroke="{GREEN}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>
 </svg>
 <div id="ext" style="top:{ey - 66:.0f}px">EXIT</div><div id="dot0" style="left:{lx(START[0]):.0f}px;top:{lx(START[1]):.0f}px"></div></div>'''
dots = '<div id="dots">' + "".join(f'<div class="dot" data-c="{c}">{badge(k, 52, "db", f"border-color:{COL[k]}")}</div>' for c, k in enumerate(IDS)) + "</div>"
check = '<path d="M-10 1 L-3 8 L11 -8" pathLength="1"/>'
chips = '<div id="chips">'
for c, k in enumerate(IDS):
    chips += f'''<div class="sl" id="sl{c}"><i class="ring" style="border-color:{COL[k]}"></i>{badge(k, CHD, "tb")}
 <div class="tk" id="tk{c}"><i></i><i></i><i></i></div><svg class="ck" id="ck{c}" viewBox="-20 -20 40 40"><circle r="17"/>{check}</svg>
 <svg class="ok" viewBox="-20 -20 40 40"><circle r="17"/>{check}</svg>
 <svg class="tm qm" viewBox="-22 -24 44 48"><path d="M-9 -9 C-9 -22 11 -22 11 -9 C11 0 1 0 1 8 M1 17 V17.5"/></svg>
 <svg class="tm xm" viewBox="-22 -24 44 48"><path d="M-13 -13 L13 13 M13 -13 L-13 13"/></svg>
 <div class="dn"></div></div>'''
chips += "</div>"
REQ = "Get the dot out of the maze."
BFS = min(62, 100 * 640 / tw8(REQ)); BUBY = round(MY0 + MW * S0 * .5 - 190)
bub = f'<div id="bub" style="top:{BUBY}px"><i class="bdot"></i><div id="btx" style="font-size:{BFS:.1f}px;line-height:{BFS * 1.2:.1f}px">{REQ}</div></div>' + \
      "".join(f'<div class="nt" id="nt{c}" style="top:{BUBY + 50}px"><i></i><i></i></div>' for c in range(5))
def rowtext(k):
    r = RES[k]
    if STATUS[k] == "exit": return f"{r['exitStep']} steps"
    if STATUS[k] == "dnf": return f"lost, {r['closestDist']} steps away"
    return "did not start" if r.get("loadError") or LAST[k] == 0 else f"stopped at step {LAST[k]}"
card = f'<div id="card"><div class="tape t1" data-decor></div><div class="tape t2" data-decor></div><div class="ct">AI MAZE CONTEST</div>'
for i, k in enumerate(ORDER):
    pl = str(i + 1) if STATUS[k] == "exit" else "&ndash;"
    card += f'<div class="cr" id="cr{i}" style="top:{108 + i * 108}px"><span class="cp">{pl}</span>{badge(k, 74)}<span class="cn">{NAME[k]}</span><span class="cv">{rowtext(k)}</span>{f"""<i style="background:{COL[k]}"></i>""" if i == 0 and WINNER else ""}</div>'
card += (f'<div class="cf">Shortest way out: {SHORT} steps</div>' if SHORT else "") + "</div>"
PHB = ""
if PH_DATA or PH_SCRIPT:
    what = " + ".join(x for x in ("DATA" if PH_DATA else "", "SCRIPT" if PH_SCRIPT else "") if x)
    PHB = f'<div class="phb" data-decor style="top:196px">PLACEHOLDER {what} &middot; NOT REAL AI RESULTS</div><div class="phb" data-decor style="top:1272px">PLACEHOLDER {what} &middot; NOT REAL AI RESULTS</div>'
flag = '<svg viewBox="0 0 40 40"><path d="M6 38 V3" stroke="#0f0f0f" stroke-width="5" stroke-linecap="round"/><path d="M6 4 H36 V24 H6Z" fill="#fff" stroke="#0f0f0f" stroke-width="3"/><path d="M6 4 h10 v10 h-10z M26 4 h10 v10 h-10z M16 14 h10 v10 h-10z" fill="#0f0f0f"/></svg>'
markup = f'''
<div class="bgw" data-decor></div>
<div id="cam">
 {maze}{dots}{bub}{chips}
 <div id="lab">{flag}AI MAZE CONTEST</div>
 <div id="cnt"><em>STEP</em><span id="cnn">0</span><em>/ {MAXS}</em></div>
 {"".join(HEADS)}
 {card}
</div>{PHB}'''

CSS = '''
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;color:INK}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}
.bgw{position:absolute;left:-20px;top:-20px;width:1120px;height:1960px;background:#ecebe5 url(assets/bg.jpg);background-size:1120px 1960px}
#cam{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 844px}
#maze{position:absolute;left:0;top:0;width:MWpx;height:MWpx;transform-origin:0 0;will-change:transform;z-index:1}
.floor{position:absolute;left:-14px;top:-14px;right:-14px;bottom:-14px;background:PAPER;border:5px solid INK;border-radius:10px;box-shadow:12px 12px 0 INK}
.msv{position:absolute;left:0;top:0;overflow:visible}
.trl{fill:none;stroke-width:6;stroke-linecap:round;stroke-linejoin:round;opacity:0}
.dm{fill:none;stroke:RED;stroke-width:5;stroke-linecap:round;opacity:0}
.cm{fill:none;stroke-width:6;stroke-dasharray:7 6;opacity:0;transform-box:fill-box;transform-origin:50% 50%}
#ext{position:absolute;left:-84px;width:84px;text-align:center;font-weight:900;font-size:27px;line-height:30px;letter-spacing:.02em;color:GREEN;
 text-shadow:2px 2px 0 PAPER,-2px 2px 0 PAPER,2px -2px 0 PAPER,-2px -2px 0 PAPER}
#dot0{position:absolute;width:26px;height:26px;margin:-13px 0 0 -13px;border-radius:50%;background:#fff;border:5px solid INK}
#dots,#chips{position:absolute;left:0;top:0;width:0;height:0}
#dots{z-index:3} #chips{z-index:4} #bub,.nt{z-index:4}
.dot{position:absolute;left:0;top:0;width:0;height:0;opacity:0;will-change:transform}
.bdg{position:relative;border-radius:50%;background:#fff;border:3.5px solid INK;display:flex;align-items:center;justify-content:center;flex:none}
.bdg .lg{display:block}
.pxl{display:block;overflow:hidden;flex:none} .pxl img{display:block;max-width:none}
.dot .db{position:absolute;left:-26px;top:-26px;border-width:6px;box-shadow:0 0 0 2.5px INK}
.sl{position:absolute;left:0;top:0;width:0;height:0;will-change:transform}
.sl .tb{position:absolute;left:-50px;top:-50px;border-width:5px;box-shadow:5px 5px 0 INK}
.ring{position:absolute;left:-63px;top:-63px;width:126px;height:126px;border-radius:50%;border:9px solid INK;opacity:0}
.tk{position:absolute;left:2px;top:-84px;width:74px;height:40px;border-radius:20px;background:#fff;border:4px solid INK;display:flex;align-items:center;justify-content:center;gap:7px;opacity:0;transform-origin:20% 100%}
.tk i{display:block;width:10px;height:10px;border-radius:50%;background:INK}
.ck,.ok{position:absolute;left:12px;top:-72px;width:52px;height:52px;overflow:visible;transform-origin:50% 50%;opacity:0}
.ok{left:8px;top:-76px;width:68px;height:68px}
.ck circle,.ok circle{fill:GREEN;stroke:INK;stroke-width:3.5} .ck path,.ok path{fill:none;stroke:#fff;stroke-width:5.5;stroke-linecap:round;stroke-linejoin:round}
.tm{position:absolute;left:-46px;top:-50px;width:92px;height:100px;overflow:visible;opacity:0}
.tm path{fill:none;stroke:RED;stroke-width:9;stroke-linecap:round;stroke-linejoin:round}
.dn{position:absolute;left:64px;top:-34px;width:130px;text-align:left;font-weight:900;font-size:62px;line-height:68px;letter-spacing:-.02em;opacity:0;white-space:nowrap}
#bub{position:absolute;left:130px;width:820px;height:150px;background:#fff;border:6px solid INK;border-radius:50px;box-shadow:9px 9px 0 INK;display:flex;align-items:center;justify-content:center;gap:24px;opacity:0;transform-origin:50% 60%}
.bdot{display:block;width:44px;height:44px;border-radius:50%;background:#fff;border:7px solid INK;flex:none}
#btx{font-weight:800;letter-spacing:-.01em;white-space:nowrap}
.nt{position:absolute;left:506px;width:68px;height:50px;background:#fff;border:4px solid INK;border-radius:14px;opacity:0;padding:10px 10px 0}
.nt i{display:block;height:5px;border-radius:3px;background:INK;margin-bottom:8px} .nt i+i{width:60%}
#lab{position:absolute;left:65px;top:279px;z-index:5;font-weight:900;font-size:44px;line-height:48px;letter-spacing:.04em;white-space:nowrap;display:flex;align-items:center;gap:14px;transform-origin:0 0}
#lab svg{width:42px;height:42px;flex:none}
#cnt{position:absolute;right:65px;top:281px;z-index:5;font-weight:900;font-size:56px;line-height:60px;letter-spacing:-.03em;white-space:nowrap;opacity:0;display:flex;align-items:baseline;gap:10px}
#cnt em{font-style:normal;font-size:26px;letter-spacing:0}
.hd{position:absolute;left:65px;top:342px;font-weight:900;letter-spacing:-.03em;white-space:nowrap;opacity:0;transform-origin:0 50%;z-index:5}
#h0{opacity:1}
.hl1{display:flex;align-items:center} .hlg{margin-right:.16em;flex:none} .hl2{display:block}
.hd.go{font-size:150px;line-height:150px;top:318px;left:auto;right:80px;transform-origin:100% 50%}
#card{position:absolute;left:78px;top:462px;width:916px;height:HCARDpx;background:PAPER;border:6px solid INK;border-radius:10px;box-shadow:14px 14px 0 INK;opacity:0;transform-origin:50% 0%;z-index:6}
.tape{position:absolute;width:130px;height:40px;background:rgba(232,221,186,.86);border:1px solid rgba(0,0,0,.14);z-index:3}
.tape.t1{right:-34px;top:-12px;transform:rotate(34deg)} .tape.t2{left:-34px;bottom:-6px;transform:rotate(34deg)}
.ct{position:absolute;left:38px;top:24px;font-weight:900;font-size:56px;line-height:64px;letter-spacing:-.03em;white-space:nowrap}
.cr{position:absolute;left:38px;right:38px;height:104px;display:flex;align-items:center;opacity:0;border-top:4px solid rgba(15,15,15,.14)}
.cp{width:56px;font-weight:900;font-size:54px;line-height:60px;text-align:center;margin-right:14px}
.cn{font-weight:900;font-size:52px;line-height:60px;letter-spacing:-.03em;margin-left:18px;white-space:nowrap}
.cv{margin-left:auto;font-weight:800;font-size:38px;line-height:60px;letter-spacing:-.01em;white-space:nowrap}
.cr i{position:absolute;left:0;right:0;bottom:2px;height:9px;border-radius:5px;transform-origin:0 50%;transform:scaleX(0)}
.cf{position:absolute;left:38px;bottom:22px;font-weight:800;font-size:36px;line-height:42px;white-space:nowrap;opacity:0}
.phb{position:absolute;left:0;width:1080px;text-align:center;font-weight:900;font-size:34px;line-height:40px;color:RED;letter-spacing:.02em;z-index:20;white-space:nowrap}
'''
for a_, b_ in (("HCARD", 108 + 5 * 108 + (70 if SHORT else 14)), ("MW", MW), ("GREEN", GREEN), ("INK", INK), ("PAPER", PAPER), ("RED", RED)):
    CSS = CSS.replace(a_, str(b_))

# ---------------------------------------------------------------- timeline (GSAP: text, premise, card; maze, dots, chips, marks are driven by render())
js(f"tl.fromTo('#cam',{{scale:1,rotation:0}},{{scale:1.012,rotation:.2,duration:{D / 4:.3f},ease:'sine.inOut',yoyo:true,repeat:3}},0);")
js(f"tl.fromTo('.bgw',{{x:0,y:0}},{{x:-14,y:-12,duration:{D / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},0);")
# beat 1: hook over the whole picture (five logos, the maze, the dot in the middle, the exit). The chips ripple so nothing sits still
for c in range(5):
    js(f"tl.fromTo('#sl{c} .tb',{{y:0}},{{y:-10,duration:.34,ease:'sine.inOut',yoyo:true,repeat:{max(1, int(a2 / .34) | 1)},immediateRender:false}},{.06 * c:.2f});")
sfx("subhit.ogg", .05, -6)
# beat 2: the premise as a process: the request -> a note to each AI -> each thinks -> each answers -> each gets its own dot in the middle
js(f"tl.fromTo('#bub',{{opacity:0,y:50,scale:.9}},{{opacity:1,y:0,scale:1,duration:.36,ease:'back.out(1.6)',immediateRender:false}},{a2:.3f});")
sfx("whoosh_b.ogg", a2, -11)
tN = a2 + min(.5, .2 * d2); tC = a2 + .56 * d2; SPAWN = []
for c in range(5):
    t = tN + .06 * c
    js(f"tl.fromTo('#nt{c}',{{opacity:0,x:0,y:0,scale:.5}},{{opacity:1,scale:1,duration:.12,ease:'power2.out',immediateRender:false}},{t:.3f});")
    js(f"tl.to('#nt{c}',{{x:{CXS[c] - 540},y:{CHY - (BUBY + 75)},rotation:{(c - 2) * 9},duration:.38,ease:'power2.inOut'}},{t + .06:.3f});")
    js(f"tl.to('#nt{c}',{{opacity:0,scale:.4,duration:.12,ease:'power2.in'}},{t + .4:.3f});")
    js(f"tl.fromTo('#tk{c}',{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.2,ease:'back.out(2)',immediateRender:false}},{t + .46:.3f});")
    js(f"tl.fromTo('#tk{c} i',{{y:0}},{{y:-7,duration:.16,ease:'sine.inOut',yoyo:true,repeat:5,stagger:.07,immediateRender:false}},{t + .5:.3f});")
    tc = max(tC + .07 * c, t + .9)
    js(f"tl.to('#tk{c}',{{opacity:0,scale:.5,duration:.14,ease:'power2.in'}},{tc - .1:.3f});")
    js(f"tl.fromTo('#ck{c}',{{opacity:0,scale:.2}},{{opacity:1,scale:1,duration:.28,ease:'back.out(2)',immediateRender:false}},{tc:.3f});")
    sfx("pop_a.ogg" if c % 2 == 0 else "pop_b.ogg", t, -11); sfx("tick.ogg", tc, -11)
    SPAWN.append(round(tc + .14, 3))
js(f"tl.to('#bub',{{opacity:0,y:30,scale:.92,duration:.24,ease:'power2.in'}},{min(tC - .1, a3 - .4):.3f});")
# beat 3: the rule the viewer must feel: the AIs never see the maze (the walls fade for a moment), and the step limit
js(f"tl.to('#walls',{{opacity:.13,duration:.4,ease:'sine.inOut'}},{a3 + .08:.3f});")
js(f"tl.to('#walls',{{opacity:1,duration:.4,ease:'sine.inOut'}},{T0 - .3:.3f});")
js(f"tl.to('.ck',{{opacity:0,scale:.4,duration:.25,ease:'sine.in'}},{T0 - .1:.3f});")
js(f"tl.to('#lab',{{opacity:0,duration:.2,ease:'sine.in'}},{T0 - .16:.3f});")
js(f"tl.to('#lab',{{opacity:1,duration:.4,ease:'sine.out'}},{tF + .06:.3f});")
sfx("toggle.ogg", a3 + .08, -10); sfx("tick.ogg", t500, -9); sfx("whoosh_a.ogg", T0 - .03, -6)
# race sounds, from the events
nde = 0
for x in EV:
    if not (T0 < x["v"] <= vEND + .01): continue
    if x["kind"] == "exit": sfx("ding.ogg" if x["place"] == 1 else "click_a.ogg", x["v"], -6 if x["place"] == 1 else -9)
    elif x["kind"] == "error_stop": sfx("toggle.ogg", x["v"], -9)
    elif x["kind"] == "lead_change": sfx("select.ogg", x["v"], -12)
    elif x["kind"] == "near_miss": sfx("impactsoft.ogg", x["v"], -10)
    elif x["kind"] == "dead_end" and nde < 8 and (not SFX or x["v"] - SFX[-1]["t"] > .35): sfx("tick.ogg", x["v"], -13); nde += 1
if FINS: sfx("riser.ogg", max(T0, VX[FINS[0]] - 1.6), -13)
if TAIL: sfx("whoosh_c.ogg", vM1, -11)
if DNFS: sfx("impactsoft.ogg", vEND, -8)
# the board: rows land from the last place up, the winner last (its line is drawn under it after a beat)
js(f"tl.fromTo('#card',{{opacity:0,y:90,rotation:3,scale:1}},{{opacity:1,y:0,rotation:-1,duration:.5,ease:'power3.out',immediateRender:false}},{tK + .03:.3f});")
sfx("whoosh_b.ogg", tK, -10)
dres = max(1.2, s(nSEND) - tK); stp = min(.3, (dres - .9) / 4)
for q, i in enumerate((4, 3, 2, 1, 0)):
    t = tK + .3 + q * stp + (.3 if i == 0 else 0)
    js(f"tl.fromTo('#cr{i}',{{opacity:0,x:-46}},{{opacity:1,x:0,duration:.36,ease:'power3.out',immediateRender:false}},{t:.3f});")
    sfx("pop_a.ogg" if q % 2 == 0 else "pop_b.ogg", t, -10)
tU = tK + .3 + 4 * stp + .6
js(f"tl.to('#cr0 i',{{scaleX:1,duration:.5,ease:'power2.inOut'}},{tU:.3f});")
js(f"tl.fromTo('#cr0 .bdg',{{scale:1}},{{scale:1.16,duration:.3,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tU:.3f});")
js(f"tl.fromTo('.cf',{{opacity:0}},{{opacity:1,duration:.3,ease:'sine.out',immediateRender:false}},{tU + .3:.3f});")
hold = max(.8, (tF - tK - .8) / 2)
js(f"tl.to('#card',{{rotation:.6,y:-8,duration:{hold / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:3}},{tK + .55:.3f});")
t = tU + .9; q = 0
while t < tF - .5:                                           # a slow wave keeps the board alive while it is read
    js(f"tl.fromTo('#cr{q % 5} .bdg',{{rotation:0}},{{rotation:{-10 if q % 2 else 10},duration:.28,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{t:.3f});"); t += .45; q += 1
js(f"tl.to('#card',{{opacity:0,scale:.9,y:-40,rotation:-3,duration:.32,ease:'power2.in'}},{tF - .26:.3f});")
sfx("whoosh_c.ogg", tF - .2, -12)

# ---------------------------------------------------------------- render(): maze layout, dots, trails, chips, marks, counter: all from the clock
DATA = dict(T0=T0, D=D, tF=round(tF, 3), tK=round(tK, 3), vEND=round(vEND, 3), ST=ST, MAXS=MAXS, CELL=CELL,
            MXR=MXR, MYR=MYR, MX0=MX0, MY0=MY0, S0=S0, CXS=CXS, CHY=CHY, RXS=RXS, RY=RY, RS=RS, FAN=FAN, OFF=OFF,
            P=[[v for p in PATH[k] for v in p] for k in IDS], LAST=[LAST[k] for k in IDS], CL=CLEN,
            DS=[[dist(p) for p in PATH[k]] for k in IDS], LEAD=LEAD, S1=S1,
            VX=[VX.get(k) for k in IDS], VE=[VE.get(k) for k in IDS], DNF=[k in DNFS for k in IDS], SP=SPAWN,
            DEAD=[[i for i, _, _ in DEADS[k][:14]] for k in IDS], START=list(START), WIN=IDS.index(WINNER) if WINNER else -1)
RJS = r'''
const Dt=__DATA__;
const ez=p=>{p=p<0?0:p>1?1:p;return p*p*(3-2*p)}, lerp=(a,b,t)=>a+(b-a)*t, bump=p=>p>0&&p<1?Math.sin(Math.PI*p):0, $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
function St(v){const i=Math.max(0,v*60),k=Math.min(Dt.ST.length-2,Math.floor(i));return lerp(Dt.ST[k],Dt.ST[k+1],Math.min(1,i-k))}
const maze=$('#maze'), dots=$$('.dot'), trs=$$('.trl'), cnt=$('#cnt'), cnn=$('#cnn'), dot0=$('#dot0'), exm=$('#exm'), exc=$('#exc'), stc=$('#stc');
const chips=[0,1,2,3,4].map(c=>{const el=$('#sl'+c);return {el,tb:el.querySelector('.tb'),ring:el.querySelector('.ring'),ok:el.querySelector('.ok'),qm:el.querySelector('.qm'),xm:el.querySelector('.xm'),dn:el.querySelector('.dn')}});
const dms=$$('.dm').map(el=>({el,c:+el.dataset.c,s:+el.dataset.s})), cms=$$('.cm').map(el=>({el,c:+el.dataset.c}));
const C=Dt.CELL, sx=(Dt.START[0]+.5)*C, sy=(Dt.START[1]+.5)*C;
function render(v){
  const st=St(v), pOut=ez((v-Dt.tF)/.5), p=Math.max(1-ez((v-(Dt.T0-.05))/.65),pOut), on=v<Dt.tF?1:1-pOut;   // p: 1 = frame-0 layout, 0 = race layout
  const s=lerp(1,Dt.S0,p), ox=lerp(Dt.MXR,Dt.MX0,p), oy=lerp(Dt.MYR,Dt.MY0,p), race=v>=Dt.T0&&v<Dt.tF;
  maze.style.transform='translate('+ox.toFixed(2)+'px,'+oy.toFixed(2)+'px) scale('+s.toFixed(4)+')';
  exm.style.transform='translate('+(Math.sin(v*5.2)*7).toFixed(1)+'px,0)'; exc.style.opacity=(.22+.16*Math.sin(v*5.2)).toFixed(3);
  stc.style.opacity=(.75+.25*Math.sin(v*3.1)).toFixed(3);
  dot0.style.opacity=v<Dt.SP[0]?1:v<Dt.SP[4]?.5:pOut; dot0.style.transform='scale('+(1+.18*Math.sin(v*6)).toFixed(3)+')';
  const si=Math.min(Math.floor(st),Dt.S1), lead=race&&v<Dt.vEND?Dt.LEAD[si]:-1, fanw=v<Dt.T0?1:1-ez(st/5);
  for(let c=0;c<5;c++){
    // chip: frame-0 row <-> status row
    const cx=lerp(Dt.RXS[c],Dt.CXS[c],p), cy=lerp(Dt.RY,Dt.CHY,p), cs=lerp(Dt.RS,1,p), ch=chips[c];
    const vx=Dt.VX[c], ve=Dt.VE[c], out=vx!==null&&v>=vx, okp=out?(v-vx-.45)/.4:-1;
    ch.el.style.transform='translate('+cx.toFixed(2)+'px,'+cy.toFixed(2)+'px) scale('+(cs*(1+.3*bump(okp))).toFixed(4)+')';
    ch.ring.style.opacity=((lead===c?1:0)*on+(c===Dt.WIN&&v>=Dt.tK?on:0)).toFixed(2); ch.ring.style.transform='scale('+(1+.06*Math.sin(v*7)).toFixed(3)+')';
    ch.ok.style.opacity=(okp>0?on:0); ch.ok.style.transform='scale('+(.4+.6*ez(okp/.5)).toFixed(3)+')';
    const stuck=Dt.DNF[c]&&v>=Dt.vEND, err=ve!==null&&v>=ve;
    ch.qm.style.opacity=stuck?on:0; ch.qm.style.transform='scale('+(stuck?.6+.4*ez((v-Dt.vEND)/.3)+.1*Math.sin(v*5):1).toFixed(3)+')';
    ch.xm.style.opacity=err?on:0; ch.tb.style.opacity=(1-.55*((stuck||err)?on:0)).toFixed(2);
    // dot
    const n=Dt.LAST[c], k=Math.min(Math.floor(st),Math.max(0,n-1)), f=n===0?0:Math.min(1,Math.max(0,st-k)), P=Dt.P[c];
    const gx=n===0?P[0]:lerp(P[2*k],P[2*k+2],f), gy=n===0?P[1]:lerp(P[2*k+1],P[2*k+3],f);
    let x=ox+((gx+.5)*C+lerp(Dt.OFF[c][0],Dt.FAN[c][0],fanw))*s, y=oy+((gy+.5)*C+lerp(Dt.OFF[c][1],Dt.FAN[c][1],fanw))*s, o=v>=Dt.SP[c]?1:0, k_=s;
    const q0=ez((v-Dt.SP[c])/.45); x=lerp(cx,x,q0); y=lerp(cy,y,q0)-70*bump(q0)*s; k_*=lerp(.5,1,q0);
    if(out){const q=ez((v-vx)/.6); x=lerp(x,cx,q); y=lerp(y,cy,q)-90*bump(q); o=1-ez((q-.75)/.25); k_*=lerp(1,.7,q)*(1+.5*bump((v-vx)/.3))}
    else if(lead===c) k_*=1.12+.05*Math.sin(v*9);
    if(race&&!out&&!err&&!stuck) k_*=1+.04*Math.sin(v*11+c*1.3);
    const d=dots[c]; d.style.opacity=(o*on*(v>=Dt.tF?0:1)).toFixed(3); d.style.zIndex=lead===c?9:5-c;
    d.style.transform='translate('+x.toFixed(2)+'px,'+y.toFixed(2)+'px) scale('+k_.toFixed(4)+')';
    // trail
    const cl=Dt.CL[c], len=n===0?0:lerp(cl[k],cl[k+1],f);
    trs[c].style.strokeDashoffset=(cl[cl.length-1]+2-len).toFixed(1); trs[c].style.opacity=(ez((v-Dt.T0-.2)/.5)*on*(v>=Dt.tF?0:1)*.8).toFixed(3);
    // steps to the exit, under the chip (race only)
    const ds=Dt.DS[c][Math.min(Math.round(st),n)];
    ch.dn.textContent=out?'':ds; ch.dn.style.opacity=(race&&!out?(1-p)*on:0).toFixed(2); ch.dn.style.color=lead===c?'#E5372B':'#0f0f0f';
  }
  for(const m of dms){const q=(st-m.s)/6; m.el.style.opacity=(race&&st>=m.s?(.35+.65*(1-ez(q)))*on:0).toFixed(2)}
  for(const m of cms){const a=v>=Dt.vEND&&v<Dt.tF; m.el.style.opacity=a?1:0; m.el.style.transform='scale('+(1+.22*Math.sin(v*6)).toFixed(3)+')'}
  cnt.style.opacity=(race?(1-p)*on:0).toFixed(2); cnn.textContent=Math.min(Dt.MAXS,Math.round(st));
}
'''.replace("__DATA__", json.dumps(DATA, separators=(",", ":")))

JS = re.sub(r"tl\.set\(([^,]+),\{", r"tl.set(\1,{immediateRender:false,", "\n".join(J))
SFX.sort(key=lambda x: x["t"])
json.dump(SFX, open(H_ + "/sfx99.json", "w"), indent=1)
PLACEHOLDER = dict(data=PH_DATA, script=PH_SCRIPT, data_map=PH_MAP, results_file=os.path.relpath(RPATH, H_))
if os.environ.get("SHIP") == "1" and (PH_DATA or PH_SCRIPT or STALE):
    sys.exit(f"SHIP=1 refused: placeholder data={PH_DATA}, placeholder script={PH_SCRIPT}, estimated timeline={STALE}")
sps = lambda a, b: round((b - a) / max(.001, v_of(b) - v_of(a)), 1) if b > a else None
json.dump(dict(placeholder=PLACEHOLDER, estimated_timeline=STALE,
               lines=[dict(n=n, text=LINES[n - 1], start=round(s(n), 3), end=round(e(n), 3),
                           role=("hook" if n == 1 else "premise" if n == 2 else "rules+Go" if n == 3 else "result" if n == nRES else "send" if n == nSEND else "tomorrow" if n == nTOM else "race")) for n in range(1, NL + 1)],
               D=D, go=T0, sources=SRC,
               race=dict(start=T0, main_from=round(vM0, 3), main_to=round(vM1, 3), tail_to=round(vEND, 3), main_last_step=S1, max_steps=MAXS,
                         steps_per_second=dict(normal=sps(min(20, S1), max(min(20, S1) + 1, (XSTEP[FINS[0]] - 13) if FINS else S1 - 26)),
                                               before_first_exit=sps(max(0, XSTEP[FINS[0]] - 12), XSTEP[FINS[0]]) if FINS else None,
                                               tail=round((MAXS - S1) / TAILD, 1) if TAIL else None),
                         board=round(tK, 3), frame0_returns=round(tF, 3),
                         order=[dict(place=PLACE[k], id=k, status=STATUS[k], steps=RES[k].get("exitStep"), closest=RES[k].get("closestDist"), board_text=rowtext(k)) for k in ORDER],
                         events=[x for x in EV if x["kind"] != "dead_end"] , dead_ends={k: [dict(step=i, v=round(v_of(i), 3)) for i, _, _ in DEADS[k]] for k in IDS}),
               headlines_draft=[dict(t=t, text=x) for t, x in sorted(HLOG)]), open(H_ + "/cues99.json", "w"), indent=1)
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
// a clock, not a motion: GSAP writes the time into clk.v and the setter draws the stage for that time
let _v=0; const clk={{get v(){{return _v}},set v(x){{_v=x;render(x)}}}};
tl.fromTo(clk,{{v:0}},{{v:D,duration:D,ease:'none',immediateRender:false}},0);
{JS}
tl.to({{}},{{duration:.001}},D-.001);
window.__timelines=window.__timelines||{{}}; window.__timelines["main"]=tl; tl.seek(0); render(0);
window.__reel={{duration:D,seek:t=>{{tl.seek(t)}}}};
</script></body></html>'''
os.makedirs(H_ + "/out", exist_ok=True)
open(H_ + "/hf/index.html", "w").write(html)
say(f"results: {os.path.relpath(RPATH, H_)}  PLACEHOLDER data={PH_DATA} script={PH_SCRIPT}  estimated timeline={STALE}" + (f"  slots: {PH_MAP}" if PH_DATA else ""))
say(f"D={D} go={T0} ({SRC['go']}) lines={NL} (race lines {RACE_LINES}) js={len(J)} sfx={len(SFX)}")
say("lines: " + "  ".join(f"{n}:{s(n):.2f}-{e(n):.2f}" for n in range(1, NL + 1)))
say(f"race clock: steps 0-{S1} over video {vM0:.2f}-{vM1:.2f}" + (f", then steps {S1}-{MAXS} fast until {vEND:.2f}" if TAIL else "") + f"; board {tK:.2f}; frame 0 back {tF:.2f}")
say("order: " + "  ".join(f"{PLACE[k]}.{k}({rowtext(k)})" for k in ORDER))
cnt_ = {}
for x in EV: cnt_[x["kind"]] = cnt_.get(x["kind"], 0) + 1
say("events: " + ", ".join(f"{k} x{v}" for k, v in sorted(cnt_.items())))
for x in EV:
    if x["kind"] != "dead_end": say(f"  {x['v']:6.2f}s step {x['step']:3d} {x['kind']:12s} {x['id']}" + (f" closest {x['closest']}" if x.get("closest") else ""))
hs = sorted(HLOG); gaps = [(round(hs[i + 1][0] - hs[i][0], 2), hs[i][1]) for i in range(len(hs) - 1) if hs[i + 1][0] - hs[i][0] > 2.5 and hs[i][0] >= T0]
say("headlines (draft): " + " | ".join(f"{t:.2f} {x}" for t, x in hs))
if gaps: say("NOTE headline holds over 2.5 s (the stage still moves; hang a spoken line or pick another event here): " + str(gaps))
if vM1 - vM0 < 6: say("NOTE: the race lines leave under 6 s for the race; the dots will move very fast.")
open(H_ + "/out/build.log", "w").write("\n".join(LOG) + "\n")
