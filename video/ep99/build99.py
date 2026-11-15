#!/usr/bin/env python3
"""ep99 'AI RACE: the maze', Miki style, HyperFrames + GSAP paused timeline, 1080x1920. Model: video/ep98/build98.py.

Reads   RESULTS (env) or arena/maze-race.json (the REAL run of the five answers), arena/maze.json,
        voice/lines.txt (10 lines), voice/narration-raw-cues.json, voice/words.json.
Writes  hf/index.html, cues99.json (lines, D, TARGETS for voice/stitch.py, race clock, events), sfx99.json.

LINES: 1 hook  2 premise  3 rules, last word "Go" (race starts on it)  4-7 race lines  8 the tie reveal
       9 setup line (the board)  10 tomorrow line (UNCONFIRMED: the only red PLACEHOLDER banner sits on it).

VOICE TARGETS: the race clock is fitted to the voice, and the voice is padded to the race. This build computes
where lines 4-10 must START (cues99.json "targets") from the line lengths; voice/stitch.py pads to them.
If the take on disk is more than 0.2 s off a target, the picture uses the targets (and says so).
Race clock anchors (step -> video time): Go = step 0; line 5 starts on step 29 and ends by step 44 (Claude is the
only front dot on steps 29-44); the first exit lands just before line 6; line 7: turn-back steps on the first
clause, Claude's exit on "makes it", the rest of the 500 steps under "walks in circles".

What is true on screen, and what is a scene choice:
  - Every dot position is paths[] of the results file, cell by cell; the trail is that same path.
  - The step counter is the real step. The clock is COMPRESSED and not uniform (scene choice; cues99.json lists it).
  - The number under each chip = shortest way out from the dot's cell (computed here from maze.json).
  - A ring marks the front dot ONLY when it is strictly in front: one dot, or dots standing on the same cell.
  - Every race headline is asserted against the data below (the build stops if the data does not carry it).
  - Scene choices: dots are drawn larger than a cell; they start fanned around the centre cell; dots with the
    same path are drawn side by side (they are really on the same cell); a dot that got out flies to its chip.
Safe area (15.11): text and key things inside x 108-972, y 269-1248; below y 1056 nothing important right of x 864.
No TTS, no audio is written here.
"""
import json, os, re, math, shutil, sys, bisect
from collections import deque
H_ = os.path.dirname(os.path.abspath(__file__))
INK = "#0f0f0f"; PAPER = "#fbfbf8"; RED = "#E5372B"; GREEN = "#27A35B"
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
LOG = []
def say(x): LOG.append(x); print(x)

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

# ---------------------------------------------------------------- results (real file only)
MZ = json.load(open(H_ + "/arena/maze.json"))
RPATH = os.environ.get("RESULTS") or H_ + "/arena/maze-race.json"
R = json.load(open(RPATH))
MAXS = R.get("constants", {}).get("MAX_STEPS", 500); SHORT = R.get("shortestSteps")
RES = {x["id"]: x for x in R["result"]}; PATH = {x["id"]: x["path"] for x in R["paths"]}
assert sorted(RES) == sorted(IDS), "the results file must hold exactly the five AIs"
W_, HH = MZ["width"], MZ["height"]; OPEN = [[int(ch, 16) for ch in row] for row in MZ["open"]]
START = (MZ["start"]["x"], MZ["start"]["y"]); EXIT = (MZ["exit"]["x"], MZ["exit"]["y"])
assert MZ["exit"]["side"] == "left" and W_ == HH
inside = lambda x, y: 0 <= x < W_ and 0 <= y < HH
MOVES = ((0, -1, 1), (1, 0, 2), (0, 1, 4), (-1, 0, 8))
DIST = {EXIT: 1}; dq = deque([EXIT])
while dq:
    x, y = dq.popleft()
    for dx, dy, b in MOVES:
        n = (x + dx, y + dy)
        if OPEN[y][x] & b and inside(*n) and n not in DIST: DIST[n] = DIST[(x, y)] + 1; dq.append(n)
dist = lambda c: DIST.get((c[0], c[1]), 0) if inside(c[0], c[1]) else 0
DEG = {(x, y): sum(1 for dx, dy, b in MOVES if OPEN[y][x] & b and inside(x + dx, y + dy)) for x in range(W_) for y in range(HH)}
assert DIST[START] == SHORT, "maze.json and the results file disagree on the shortest way out"
for k in IDS:                                               # every step of every path must be a legal move
    p = PATH[k]; assert tuple(p[0]) == START, k
    for i in range(1, len(p)):
        a, b = p[i - 1], p[i]
        if a == b: continue
        assert inside(*a) and abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1, f"{k}: jump at step {i}"
        assert OPEN[a[1]][a[0]] & next(bb for dx, dy, bb in MOVES if (dx, dy) == (b[0] - a[0], b[1] - a[1])), f"{k}: through a wall at step {i}"
STATUS = {k: RES[k]["status"] for k in IDS}
LAST = {k: len(PATH[k]) - 1 for k in IDS}
XSTEP = {k: RES[k]["exitStep"] for k in IDS if STATUS[k] == "exit"}
FINS = sorted(XSTEP, key=lambda k: (XSTEP[k], IDS.index(k)))
DNFS = [k for k in IDS if STATUS[k] == "dnf"]; ERRS = [k for k in IDS if STATUS[k] == "error"]
assert not ERRS, "an AI with status error needs its own beat: not laid out in this build"
ORDER = sorted(IDS, key=lambda k: RES[k]["place"])
cell = lambda k, i: PATH[k][min(i, LAST[k])]
d_at = lambda k, i: dist(cell(k, i))
F1 = XSTEP[FINS[0]]; S1 = max(XSTEP.values())               # first exit, last exit
WINS = [k for k in FINS if XSTEP[k] == F1]                   # the winner(s): a tie = more than one
TWIN = {k: next(j for j in IDS if PATH[j] == PATH[k]) for k in IDS}   # first AI in chip order with the identical path
PAIRS = [k for k in IDS if TWIN[k] != k or any(TWIN[j] == k for j in IDS if j != k)]

# ---------------------------------------------------------------- race events (data only; steps)
EV = []
for k in FINS: EV.append(dict(kind="exit", id=k, step=XSTEP[k], place=1 + sum(1 for j in FINS if XSTEP[j] < XSTEP[k])))
for k in DNFS: EV.append(dict(kind="dnf_freeze", id=k, step=LAST[k], closest=RES[k].get("closestDist"), closestAt=RES[k].get("closestAt"), closestStep=RES[k].get("closestStep")))
DEADS = {k: [] for k in IDS}; PACE = {}
for k in IDS:
    p = PATH[k]; best = dist(p[0]); bi = 0; flagged = None
    for i in range(1, LAST[k] + 1):
        c = tuple(p[i])
        if not inside(*c): break
        if c != tuple(p[i - 1]) and DEG[c] == 1 and c != START:
            DEADS[k].append([i, c[0], c[1]]); EV.append(dict(kind="dead_end", id=k, step=i, cell=list(c)))
        d = dist(c)
        if d < best: best, bi = d, i
        elif d - best >= 12 and best <= 30 and flagged != best:
            flagged = best; EV.append(dict(kind="near_miss", id=k, step=bi, closest=best, back_to=d, back_at=i, cell=list(p[bi])))
    if STATUS[k] == "dnf":                                  # from which step on the dot only paces a few cells
        for lim, nm in ((2, "paces_2_cells"), (4, "paces_4_cells")):
            sset = next((s_ for s_ in range(LAST[k]) if len(set(map(tuple, p[s_:]))) <= lim), None)
            if sset is not None and sset < LAST[k] - 20: PACE[k] = (sset, lim); EV.append(dict(kind=nm, id=k, step=sset, until=LAST[k])); break
        cs = RES[k].get("closestStep")
        if cs is not None and cs > 20: EV.append(dict(kind="circles_after_closest", id=k, step=cs, cells_after=len(set(map(tuple, p[cs:]))), steps_after=LAST[k] - cs))
# the front: FRONT[i] = the dots strictly in front at step i (one dot, or dots on the same cell), else []. Only until the first exit.
def front(i):
    alive = [k for k in IDS if not (k in XSTEP and i >= XSTEP[k])]
    m = min(d_at(k, i) for k in alive); f = [k for k in alive if d_at(k, i) == m]
    return f if len({tuple(cell(k, i)) for k in f}) == 1 and len(f) < len(alive) else []
FRONT = [front(i) if i < F1 else [] for i in range(MAXS + 1)]
runs = []; i = 0
while i < F1:
    j = i
    while j + 1 < F1 and FRONT[j + 1] == FRONT[i]: j += 1
    if FRONT[i]: runs.append((i, j, FRONT[i]))
    i = j + 1
for a, b, f in runs:
    if b - a >= 2: EV.append(dict(kind="front", ids=f, id=f[0], step=a, until=b, steps_to_exit=d_at(f[0], a)))
EV.sort(key=lambda x: (x["step"], x["kind"]))
def sole(k, a, b): return all(FRONT[i] == [k] for i in range(a, b + 1))

# ---------------------------------------------------------------- lines, cues, words
LINES = [l.strip() for l in open(H_ + "/voice/lines.txt") if l.strip()]; NL = len(LINES)
assert NL == 10, "this build is laid out for the 10 lines of channel/episode-99-script.md"
C = json.load(open(H_ + "/voice/narration-raw-cues.json")); C = C if isinstance(C, list) else C["lines"]
ctext = lambda c: c.get("line", c.get("text", ""))
CUE = {c["n"]: c for c in C}
assert len(CUE) == NL and all(norm(ctext(CUE[n])) == norm(LINES[n - 1]) for n in range(1, NL + 1)), "voice/narration-raw-cues.json does not hold the lines of voice/lines.txt"
L = {n: (float(CUE[n]["start"]), float(CUE[n]["end"])) for n in range(1, NL + 1)}
DUR = {n: L[n][1] - L[n][0] for n in L}
try:
    WORDS = [(w["word"], w["start"], w["end"]) if isinstance(w, dict) else tuple(w) for w in json.load(open(H_ + "/voice/words.json"))]
except Exception:
    WORDS = []
SRC = {}
def woff(word, n, frac, k=0, name=None):
    """offset of a spoken word inside line n (words.json, relative to the line start), else a fraction of the line (ESTIMATE)"""
    c = 0
    for w, a, b in WORDS:
        if L[n][0] - .15 <= a <= L[n][1] + .1 and word in norm(w):
            if c == k: SRC[name or word] = "words.json"; return max(0.0, a - L[n][0])
            c += 1
    SRC[name or word] = "ESTIMATE (line fraction)"; return frac * DUR[n]
oGO = woff("go", 3, .86); oCL5 = woff("claude", 5, .72, name="claude(5)"); oSHORT = woff("short", 7, .32); oMAKES = woff("makes", 7, .49)
oCG7 = woff("chat", 7, .66, name="chatgpt(7)"); oPICK = woff("see", 3, .3)
T0 = round(L[3][0] + oGO, 3)
# targets: where each line must start so its words land on the race
RACEONLY = float(os.environ.get("RACEONLY", "2.9"))          # the stretch with no voice (steps 44 -> first exit)
TG = {1: L[1][0], 2: L[2][0], 3: L[3][0]}
TG[4] = round(T0 + .6, 2)
TG[5] = round(TG[4] + DUR[4] + .12, 2)
vA44 = TG[5] + DUR[5] + .2
vX = round(vA44 + RACEONLY, 3)                               # the first exit
TG[6] = round(vX + .12, 2)
TG[7] = round(TG[6] + DUR[6] + .15, 2)
TG[8] = round(TG[7] + DUR[7] + .25, 2)
TG[9] = round(TG[8] + DUR[8] + .15, 2)
TG[10] = round(TG[9] + DUR[9] + .19, 2)
DRIFT = {n: round(L[n][0] - TG[n], 2) for n in range(4, NL + 1)}
ONTG = any(abs(v) > .2 for v in DRIFT.values())
if ONTG: L = {n: ((TG[n], TG[n] + DUR[n]) if n >= 4 else L[n]) for n in L}
s = lambda n: L[n][0]
e = lambda n: L[n][1]
D = round(e(NL) + .4, 2)
tF = D - .58                                                 # the frame-0 layout comes back from here
tRV = s(8); tK = s(9)
tSAME = tRV + woff("same", 8, .52); tFOL = s(10) + woff("follow", 10, .66)                                        # the tie reveal on the maze; the board
# anchors of the race clock: (video time, step)
near = next((x for x in EV if x["kind"] == "near_miss" and x["id"] not in WINS and x["step"] >= F1 - 3), None)
assert near and near["id"] == "claude" and "claude" in XSTEP, "line 7 needs Claude's turn-back after the first exit and Claude's exit"
ANCH = [(T0 + .15, 0), (s(5), 29), (s(5) + DUR[5] + .2, 44), (s(6) - .12, F1), (s(7), F1 + 1), (s(7) + oSHORT, near["back_at"]),
        (s(7) + oMAKES + .2, XSTEP["claude"]), (e(7) - .05, MAXS)]
assert all(ANCH[i][0] < ANCH[i + 1][0] and ANCH[i][1] < ANCH[i + 1][1] for i in range(len(ANCH) - 1)), ANCH
wt = [1.0] * (MAXS + 1)                                      # screen-time weight of step i-1 -> i inside its anchor segment
for i in range(1, 9): wt[i] = 2.6 - .2 * i                   # soft start
for i in range(F1 - 11, F1 + 1): wt[i] = 3.0                 # the last steps before the first exit play slower
VT = [0.0] * (MAXS + 1)
for (va, sa), (vb, sb) in zip(ANCH, ANCH[1:]):
    tot = sum(wt[sa + 1:sb + 1]); acc = 0.0
    for i in range(sa, sb + 1):
        VT[i] = va + (vb - va) * acc / tot
        if i < sb: acc += wt[i + 1]
vEND = VT[MAXS]
v_of = lambda st: VT[int(st)]
def step_of(v):
    if v <= VT[0]: return 0.0
    if v >= VT[MAXS]: return float(MAXS)
    i = bisect.bisect_right(VT, v) - 1
    return i + (v - VT[i]) / max(1e-6, VT[i + 1] - VT[i])
ST = [round(step_of(n / 60), 3) for n in range(int(D * 60) + 4)]
for x in EV: x["v"] = round(vEND if x["kind"] == "dnf_freeze" else v_of(x["step"]), 3)
VXT = {k: round(v_of(XSTEP[k]), 3) for k in FINS}

# ---------------------------------------------------------------- facts the words and headlines rest on (the build stops if one is not in the data)
FACTS = []
def fact(ok, txt): FACTS.append(("OK  " if ok else "FAIL") + " " + txt); assert ok, "not carried by the data: " + txt
st5a, st5c, st5e = int(step_of(s(5))), int(step_of(s(5) + oCL5)), int(math.ceil(step_of(e(5))))
fact("perplexity" in PACE and PACE["perplexity"][0] <= 5, f"line 4 'Perplexity is stuck at the start': it only paces {PACE.get('perplexity', (0, 0))[1]} cells from step {PACE.get('perplexity', (0, 0))[0]} to step {MAXS}")
fact(all(d_at("chatgpt", i) >= d_at("chatgpt", st5a) for i in range(st5a, 62)) and d_at("chatgpt", st5e) > d_at("chatgpt", st5c) > d_at("chatgpt", st5a) > DIST[START] - 15 and d_at("chatgpt", 61) > DIST[START],
     f"line 5 'ChatGPT goes the wrong way': its way out grows from {d_at('chatgpt', st5a)} steps (step {st5a}) to {d_at('chatgpt', st5c)} (step {st5c}); it is {d_at('chatgpt', 61)} at step 61")
fact(sole("claude", st5c, st5e), f"line 5 'Claude leads': Claude is the only front dot on steps {st5c}-{st5e} (spoken there); data: alone in front on steps " +
     ", ".join(f"{a}-{b}" for a, b, f in runs if f == ["claude"]))
fact(sorted(WINS) == ["gemini", "meta"] and XSTEP["claude"] > F1, f"line 1 'Meta AI and Gemini just killed Claude' (= beat it clearly; Claude DOES finish, third): out in {F1} steps against Claude's {XSTEP['claude']}")
fact(len(WINS) == 2 and PATH[WINS[0]] == PATH[WINS[1]], f"lines 6 and 8: {NAME[WINS[0]]} and {NAME[WINS[1]]} leave on the same step ({F1}) with the identical path")
pair_run = next(((a, b) for a, b, f in runs if sorted(f) == sorted(WINS) and b == F1 - 1), None)
fact(pair_run is not None, f"headline 'two dots take the lead': {NAME[WINS[0]]} and {NAME[WINS[1]]} are the front (same cell) on steps {pair_run[0] if pair_run else '?'}-{F1 - 1}")
fact(near["closest"] == 10 and near["step"] == F1, f"line 7 'Claude turns back ten steps short': {near['closest']} steps from the exit at step {near['step']}, back to {near['back_to']} by step {near['back_at']}, out at step {XSTEP['claude']}")
cgc = next(x for x in EV if x["kind"] == "circles_after_closest" and x["id"] == "chatgpt")
fact(STATUS["chatgpt"] == "dnf" and cgc["cells_after"] <= 40, f"line 7 'ChatGPT walks in circles': after its closest point (step {cgc['step']}, {RES['chatgpt']['closestDist']} away) it walks {cgc['cells_after']} cells for {cgc['steps_after']} steps" +
     (f", and only {PACE['chatgpt'][1]} cells from step {PACE['chatgpt'][0]}" if "chatgpt" in PACE else ""))

# ---------------------------------------------------------------- page geometry (safe: x 108-972, y 269-1248; below y 1056 nothing important right of x 864)
CELL = 33; MW = CELL * W_                                    # maze 693 px: x 279-972, y 555-1248 (no dot ever enters the cells right of x 864 below y 1056: asserted)
MX, MY = 972 - MW, 1248 - MW
assert not any(MX + p[0] * CELL + CELL > 864 and MY + p[1] * CELL + CELL > 1056 for k in IDS for p in PATH[k]), "a dot walks under the right-hand buttons: move the maze"
CHX, CHD = 172, 127; CHYS = [563 + 127 * c for c in range(5)]  # the five chips: a column LEFT of the maze, y 506-1056 (above the EXIT marker)
FANR, FANS = 104, 1.85                                        # before Go: the dots fanned around the centre cell, drawn larger
FAN = [[round(FANR * math.cos(math.radians(-90 + 72 * c)), 1), round(FANR * math.sin(math.radians(-90 + 72 * c)), 1)] for c in range(5)]
OFF = []; TOFF = []                                          # dot offset in the corridor; trail offset (stays inside the corridor)
for c, k in enumerate(IDS):
    if k in PAIRS: sgn = -1 if TWIN[k] == k else 1; OFF.append([17 * sgn, 0]); TOFF.append([3.5 * sgn, 3.5 * sgn])
    else: a_ = math.radians(-90 + 120 * [j for j in IDS if j not in PAIRS].index(k)); OFF.append([round(5 * math.cos(a_), 1), round(5 * math.sin(a_), 1)]); TOFF.append([round(6 * math.cos(a_), 1), round(6 * math.sin(a_), 1)])
lx = lambda x: (x + .5) * CELL
try:
    from PIL import ImageFont
    _f = ImageFont.truetype(H_ + "/hf/assets/fonts/InterDisplay-Black.otf", 100)
    _f8 = ImageFont.truetype(H_ + "/hf/assets/fonts/InterDisplay-ExtraBold.otf", 100)
    tw = lambda t: _f.getlength(t) - 3.0 * len(t)
    tw8 = lambda t: _f8.getlength(t) - 1.0 * len(t)
except Exception:
    tw = lambda t: 62 * len(t); tw8 = lambda t: 56 * len(t)
def logo(k, h, cls=""):
    if k == "perplexity":                                   # raw file, icon part only (x 0-28.14 of 149.82)
        return f'<span class="pxl {cls}" style="width:{h * 28.14 / 36:.1f}px;height:{h}px"><img src="assets/logos/perplexity.svg" style="height:{h}px;width:{h * 149.82 / 36:.1f}px"></span>'
    return f'<img class="lg {cls}" src="assets/logos/{LOGO[k]}" style="width:{h}px;height:{h}px">'
def badge(k, d, cls="", st=""):
    return f'<div class="bdg {cls}" style="width:{d}px;height:{d}px;{st}">{logo(k, round(d * .62))}</div>'
J = []; SFX = []
def js(x): J.append(x)
def sfx(f, t, g=-8): SFX.append(dict(f=f, t=round(max(0, t), 3), g=g))
def fin(sel, t, d=.34, y=20, blur=8):
    js(f"tl.fromTo('{sel}',{{opacity:0,y:{y},filter:'blur({blur}px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:{d},ease:'power2.out',immediateRender:false}},{max(0, t):.3f});")
def fout(sel, t, d=.22):
    js(f"tl.to('{sel}',{{opacity:0,y:-12,filter:'blur(8px)',duration:{d},ease:'power2.inOut'}},{max(0, t):.3f});")

# ---------------------------------------------------------------- headlines (x 108-972; plain ink, no boxes, no code words)
HEADS = []; HLOG = []; HW = 864
def head(i, t_in, t_out, l1, logos=(), size=96, top=None, l2="", t2=None, l2s=.62):
    wl = len(logos) * 86
    fs = min(size, HW / max((tw(l1) + wl * 100 / 84) / 100, tw(l2) * l2s / 100 if l2 else .01))
    lg = "".join(logo(k, round(fs * .86), "hlg") for k in logos)
    tp = top if top is not None else (354 if l2 else 352 + max(0, (110 - fs) / 2))
    l2h = f'<div class="hl2" id="h{i}b" style="{"opacity:0;" if t2 is not None else ""}font-size:{fs * l2s:.1f}px;line-height:{fs * l2s * 1.12:.1f}px">{l2}</div>' if l2 else ""
    HEADS.append(f'<div class="hd" id="h{i}" style="top:{tp:.0f}px;font-size:{fs:.1f}px;line-height:{fs * .98:.1f}px"><div class="hl1">{lg}<span>{l1}</span></div>{l2h}</div>')
    if t_in is not None: fin(f"#h{i}", t_in)
    if l2 and t2 is not None: js(f"tl.fromTo('#h{i}b',{{opacity:0,x:34}},{{opacity:1,x:0,duration:.3,ease:'power3.out',immediateRender:false}},{t2:.3f});")
    if t_out is not None: fout(f"#h{i}", t_out - .24)
    HLOG.append((round(t_in or 0, 2), l1 + (" / " + l2 if l2 else "")))
a2, d2, a3 = s(2), DUR[2], s(3)
vCL = s(5) + oCL5; v45 = v_of(st5e + 1) if st5e + 1 <= 45 else v_of(45)
vPAIR = v_of(pair_run[0]); vCLX = VXT["claude"]; vCG = max(s(7) + oCG7, vCLX + .6)
head(0, None, a2 - .02, "AI MAZE RACE", size=118, top=296)
head(1, a2, a3, "FIVE AIs. SAME REQUEST.", size=96, top=318)
head(2, a3, T0 - .04, "THEY CAN&rsquo;T SEE THE MAZE", l2="pick one before it starts", t2=a3 + oPICK, l2s=.66, top=300)
HEADS.append('<div class="hd go" id="hgo"><div class="hl1"><span>GO!</span></div></div>')
js(f"tl.fromTo('#hgo',{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.3,ease:'power3.out',immediateRender:false}},{T0:.3f});")
js(f"tl.to('#hgo',{{opacity:0,scale:1.2,duration:.26,ease:'power2.in'}},{s(4) - .28:.3f});")
head(3, s(4), s(5), "PERPLEXITY: STUCK", logos=("perplexity",))
head(4, s(5), vCL, "CHATGPT: WRONG WAY", logos=("chatgpt",))
head(5, vCL, min(v45, vPAIR - .3), "CLAUDE LEADS", logos=("claude",))
head(6, vPAIR, vX, "TWO DOTS TAKE THE LEAD")
head(7, vX, s(7), "TWO OUT. SAME STEP.")
head(8, s(7), vCG, f"CLAUDE: {near['closest']} STEPS SHORT...", logos=("claude",), l2=f"...OUT IN {XSTEP['claude']}", t2=vCLX, l2s=.86)
head(9, vCG, tRV, "CHATGPT: IN CIRCLES", logos=("chatgpt",))
head(13, tRV, tSAME, f"{NAME[WINS[0]].upper()} + {NAME[WINS[1]].upper()} TIE", logos=tuple(WINS))
head(10, tSAME, tK - .1, "SAME PATH. EVERY STEP.", size=84)
head(11, tK + .1, s(10), "THE REQUEST: LINK IN BIO")
head(12, s(10), tFOL, "WANT THE NEXT ONE?")
head(14, tFOL, tF - .1, "FOLLOW, AND YOU&rsquo;LL SEE IT")
fin("#h0", tF + .12, .4)

# ---------------------------------------------------------------- markup
hw = []; vw = []
for gy in range(HH + 1):
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
    pts_ = [(lx(p[0]) + TOFF[c][0], lx(p[1]) + TOFF[c][1]) for p in PATH[k]]
    acc = [0.0]
    for i in range(1, len(pts_)): acc.append(acc[-1] + math.hypot(pts_[i][0] - pts_[i - 1][0], pts_[i][1] - pts_[i - 1][1]))
    CLEN.append([round(v, 1) for v in acc]); TRD.append("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts_))
ey = lx(EXIT[1])
dead_marks = "".join(f'<path class="dm" data-c="{c}" data-s="{i}" d="M{lx(x) - 7:.0f} {lx(y) - 7:.0f} l14 14 m0 -14 l-14 14"/>' for c, k in enumerate(IDS) if TWIN[k] == k for i, x, y in DEADS[k][:14])
close_marks = "".join(f'<circle class="cm" data-c="{c}" cx="{lx(RES[k]["closestAt"][0]):.0f}" cy="{lx(RES[k]["closestAt"][1]):.0f}" r="14" stroke="{COL[k]}"/>' for c, k in enumerate(IDS) if STATUS[k] != "exit")
maze = f'''<div id="maze" style="left:{MX}px;top:{MY}px"><div class="floor" data-decor></div>
 <svg class="msv" viewBox="0 0 {MW} {MW}" width="{MW}" height="{MW}">
  <defs><filter id="wob" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".03" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="2.4"/></filter></defs>
  <g id="rays" stroke="#0f0f0f" stroke-width="6" stroke-linecap="round">{"".join(f'<path d="M{lx(START[0]) + 172 * math.cos(a_):.0f} {lx(START[1]) + 172 * math.sin(a_):.0f} L{lx(START[0]) + (204 if q % 2 else 190) * math.cos(a_):.0f} {lx(START[1]) + (204 if q % 2 else 190) * math.sin(a_):.0f}"/>' for q, a_ in enumerate(math.radians(18 + 36 * j) for j in range(10)))}</g>
  <rect id="stc" x="{START[0] * CELL + 3}" y="{START[1] * CELL + 3}" width="{CELL - 6}" height="{CELL - 6}" rx="6" fill="#FFE28A"/>
  <rect id="exc" x="{EXIT[0] * CELL + 3}" y="{EXIT[1] * CELL + 3}" width="{CELL - 6}" height="{CELL - 6}" rx="6" fill="{GREEN}" opacity=".3"/>
  <g id="trs">{"".join(f'<path class="trl" d="{TRD[c]}" stroke="{COL[k]}" stroke-dasharray="{CLEN[c][-1] + 2:.1f}" stroke-dashoffset="{CLEN[c][-1] + 2:.1f}"/>' for c, k in enumerate(IDS))}</g>
  <g id="walls" filter="url(#wob)" fill="none" stroke="{INK}" stroke-width="4.6" stroke-linecap="round"><path d="{" ".join(hw)} {" ".join(vw)}"/></g>
  <g id="dms">{dead_marks}</g><g id="cms">{close_marks}</g>
  <g id="exm"><path d="M-16 {ey} H-112 M-88 {ey - 21} L-116 {ey} L-88 {ey + 21}" fill="none" stroke="#15803d" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></g>
 </svg>
 <div id="ext" style="top:{ey - 88:.0f}px">EXIT</div></div>'''
dots = '<div id="dots">' + "".join(f'<div class="dot" data-c="{c}">{badge(k, 60, "db")}<i class="dr" style="border-color:{COL[k]}"></i></div>' for c, k in enumerate(IDS)) + "</div>"
check = '<path d="M-10 1 L-3 8 L11 -8" pathLength="1"/>'
chips = '<div id="chips">'
for c, k in enumerate(IDS):
    chips += f'''<div class="sl" id="sl{c}" style="left:{CHX}px;top:{CHYS[c]}px"><i class="ring" style="border-color:{COL[k]}"></i>{badge(k, CHD, "tb")}
 <div class="tk" id="tk{c}"><i></i><i></i><i></i></div><svg class="ck" id="ck{c}" viewBox="-20 -20 40 40"><circle r="17"/>{check}</svg>
 <svg class="ok" viewBox="-20 -20 40 40"><circle r="17"/>{check}</svg>
 <svg class="tm qm" viewBox="-22 -24 44 48"><path d="M-9 -9 C-9 -22 11 -22 11 -9 C11 0 1 0 1 8 M1 17 V17.5"/></svg>
 <div class="dn"></div>{'<div class="kos">K.O.</div>' if k == near["id"] else ""}</div>'''
chips += "</div>"
REQ = "Get this dot out of the maze."
BFS = min(50, 100 * 500 / tw8(REQ)); BUBY = MY + 40
bub = f'<div id="bub" style="top:{BUBY}px"><i class="bdot"></i><div id="btx" style="font-size:{BFS:.1f}px;line-height:{BFS * 1.2:.1f}px">{REQ}</div></div>' + \
      "".join(f'<div class="nt" id="nt{c}" style="top:{BUBY + 40}px"><i></i><i></i></div>' for c in range(5))
def rowtext(k):
    r = RES[k]
    if STATUS[k] == "exit": return f"out in {r['exitStep']} steps" + (", same path" if TWIN[k] != k else "")
    return "stuck by the start" if r.get("cellsVisited", 99) <= 6 else f"lost, closest {r['closestDist']} steps away"
RH = 100
card = f'<div id="card"><div class="tape t1" data-decor></div><div class="tape t2" data-decor></div><div class="ct">AI RACE &middot; THE MAZE</div>'
for i, k in enumerate(ORDER):
    pl = str(1 + sum(1 for j in FINS if XSTEP[j] < XSTEP[k])) if STATUS[k] == "exit" else "&ndash;"
    card += f'<div class="cr" id="cr{i}" style="top:{92 + i * RH}px"><span class="cp">{pl}</span>{badge(k, 72)}<div class="cx"><span class="cn">{NAME[k]}</span><span class="cv">{rowtext(k)}</span></div>{f"""<i style="background:{COL[k]}"></i>""" if k in WINS else ""}</div>'
card += f'<div class="cf">best possible: {SHORT} steps</div></div>'
KW = [(WINS[1] if WINS[1] == "meta" else WINS[0]), (WINS[0] if WINS[1] == "meta" else WINS[1])]      # spoken order: Meta AI, Gemini
KWX, KWY, KCX, KCY = [MX + MW // 2 - 112, MX + MW // 2 + 112], MY + 190, MX + MW // 2 - 40, MY + 450
KFS = 100; KSW = tw("K.O.") * KFS / 100 + 6; KHALF = (KSW * .982 + KFS * .191) / 2 * 1.37 + 12     # half width of the stamp at its largest (scale 1.365, rotated 11 degrees, shadow)
KSX = min(KCX + 26 + 84 + 90, 968 - KHALF); KSL, KST = round(KSX - KSW / 2), KCY - 62
STAR = '<svg class="star" viewBox="-34 -34 68 68"><path d="M0 -30 L7 -9 L27 -15 L13 2 L30 16 L8 12 L3 32 L-7 13 L-27 20 L-14 2 L-30 -12 L-9 -10Z"/></svg>'
kcol = COL[near["id"]]
ko = '<div id="ko">' + "".join(f'<div class="kb kw" style="left:{KWX[i]}px;top:{KWY}px">{badge(k, 184, "kg", f"border-color:{COL[k]}")}<svg class="crown" viewBox="-46 -34 92 62"><path d="M-36 22 L-42 -16 L-19 2 L0 -28 L19 2 L42 -16 L36 22Z"/></svg></div>' for i, k in enumerate(KW)) + \
     f'<div class="kb" id="kcl" style="left:{KCX}px;top:{KCY}px">{badge(near["id"], 168, "kg", f"border-color:{kcol}")}</div><div id="kst" style="left:{KSL}px;top:{KST}px;width:{KSW:.0f}px">K.O.</div></div><div id="stars">{STAR * 4}</div>'
markup = f'''
<div class="bgw" data-decor></div>
<div id="cam"><div id="pn">
 {maze}{dots}{ko}{bub}{chips}
 <div id="cnt"><em>STEP</em><span id="cnn">0</span><em>/ {MAXS}</em></div>
 {"".join(HEADS)}
 {card}
</div></div>'''

CSS = '''
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;color:INK}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}
.bgw{position:absolute;left:-20px;top:-20px;width:1120px;height:1960px;background:#ecebe5 url(assets/bg.jpg);background-size:1120px 1960px}
#cam,#pn{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 780px}
#maze{position:absolute;width:MWpx;height:MWpx;z-index:1}
.floor{position:absolute;left:-12px;top:-12px;right:-12px;bottom:-12px;background:PAPER;border:5px solid INK;border-radius:10px;box-shadow:-10px 10px 0 INK}
.msv{position:absolute;left:0;top:0;overflow:visible}
.trl{fill:none;stroke-width:5.5;stroke-linecap:round;stroke-linejoin:round;opacity:0}
.dm{fill:none;stroke:RED;stroke-width:4.5;stroke-linecap:round;opacity:0}
.cm{fill:none;stroke-width:6;stroke-dasharray:7 6;opacity:0;transform-box:fill-box;transform-origin:50% 50%}
#ext{position:absolute;left:-171px;width:150px;text-align:left;font-weight:900;font-size:54px;line-height:54px;letter-spacing:.01em;color:#15803d}
#rays{transform-box:fill-box;transform-origin:50% 50%}
#dots,#chips{position:absolute;left:0;top:0;width:0;height:0}
#dots{z-index:3} #chips{z-index:4} #bub,.nt{z-index:4}
.dot{position:absolute;left:0;top:0;width:0;height:0;will-change:transform}
.bdg{position:relative;border-radius:50%;background:#fff;border:3.5px solid INK;display:flex;align-items:center;justify-content:center;flex:none}
.bdg .lg{display:block}
.pxl{display:block;overflow:hidden;flex:none} .pxl img{display:block;max-width:none}
.dot .db{position:absolute;left:-30px;top:-30px;border-width:3.5px}
.dr{position:absolute;left:-30px;top:-30px;width:60px;height:60px;border-radius:50%;border:7px solid INK;box-shadow:0 0 0 2.5px INK;opacity:0}
.sl{position:absolute;width:0;height:0;will-change:transform}
.sl .tb{position:absolute;left:-63.5px;top:-63.5px;border-width:5.5px}
.ring{position:absolute;left:-63.5px;top:-63.5px;width:127px;height:127px;border-radius:50%;border:12px solid INK;opacity:0}
.tk{position:absolute;left:30px;top:-76px;width:68px;height:36px;border-radius:18px;background:#fff;border:4px solid INK;display:flex;align-items:center;justify-content:center;gap:6px;opacity:0;transform-origin:20% 100%}
.tk i{display:block;width:9px;height:9px;border-radius:50%;background:INK}
.ck,.ok{position:absolute;left:26px;top:-68px;width:54px;height:54px;overflow:visible;transform-origin:50% 50%;opacity:0}
.ck circle,.ok circle{fill:GREEN;stroke:INK;stroke-width:3.5} .ck path,.ok path{fill:none;stroke:#fff;stroke-width:5.5;stroke-linecap:round;stroke-linejoin:round}
.tm{position:absolute;left:-46px;top:-52px;width:92px;height:104px;overflow:visible;opacity:0}
.tm path{fill:none;stroke:RED;stroke-width:9;stroke-linecap:round;stroke-linejoin:round}
.dn{position:absolute;left:-10px;top:18px;width:78px;text-align:right;font-weight:900;font-size:44px;line-height:44px;letter-spacing:-.03em;opacity:0;white-space:nowrap;transform-origin:100% 50%;
 text-shadow:3px 3px 0 PAPER,-3px 3px 0 PAPER,3px -3px 0 PAPER,-3px -3px 0 PAPER,0 4px 0 PAPER,4px 0 0 PAPER,-4px 0 0 PAPER,0 -4px 0 PAPER}
#ko,#stars{position:absolute;left:0;top:0;width:0;height:0;z-index:3} #stars{z-index:5}
.kb{position:absolute;width:0;height:0}
.kb .kg{position:absolute;left:-92px;top:-92px;border-width:13px;box-shadow:0 0 0 4px INK,-9px 11px 0 4px INK}
#kcl .kg{left:-84px;top:-84px}
#kst,.kos{font-weight:900;color:RED;letter-spacing:-.02em;white-space:nowrap;transform-origin:50% 50%;
 text-shadow:4px 4px 0 PAPER,-4px 4px 0 PAPER,4px -4px 0 PAPER,-4px -4px 0 PAPER,0 5px 0 PAPER,5px 0 0 PAPER,-5px 0 0 PAPER,0 -5px 0 PAPER,7px 9px 0 INK}
#kst{position:absolute;font-size:100px;line-height:100px;text-align:center}
.crown{position:absolute;left:-46px;top:-158px;width:92px;height:62px;overflow:visible;transform-origin:50% 100%}
.crown path{fill:#FFD23F;stroke:INK;stroke-width:6;stroke-linejoin:round}
.kos{position:absolute;left:-60px;top:-66px;font-size:48px;line-height:50px;opacity:0;text-shadow:3px 3px 0 PAPER,-3px 3px 0 PAPER,3px -3px 0 PAPER,-3px -3px 0 PAPER,0 4px 0 PAPER,4px 0 0 PAPER,-4px 0 0 PAPER,0 -4px 0 PAPER}
.star{position:absolute;left:0;top:0;width:52px;height:52px;margin:-26px 0 0 -26px;opacity:0;overflow:visible}
.star path{fill:#FFD23F;stroke:INK;stroke-width:5;stroke-linejoin:round}
#bub{position:absolute;left:306px;width:640px;height:116px;background:#fff;border:6px solid INK;border-radius:44px;box-shadow:-8px 8px 0 INK;display:flex;align-items:center;justify-content:center;gap:20px;opacity:0;transform-origin:50% 60%}
.bdot{display:block;width:38px;height:38px;border-radius:50%;background:#fff;border:7px solid INK;flex:none}
#btx{font-weight:800;letter-spacing:-.01em;white-space:nowrap}
.nt{position:absolute;left:600px;width:64px;height:46px;background:#fff;border:4px solid INK;border-radius:13px;opacity:0;padding:9px 9px 0}
.nt i{display:block;height:5px;border-radius:3px;background:INK;margin-bottom:7px} .nt i+i{width:60%}
#cnt{position:absolute;right:108px;top:292px;z-index:5;font-weight:900;font-size:50px;line-height:50px;letter-spacing:-.03em;white-space:nowrap;opacity:0;display:flex;align-items:baseline;gap:9px}
#cnt em{font-style:normal;font-size:24px;letter-spacing:0}
.hd{position:absolute;left:108px;top:336px;font-weight:900;letter-spacing:-.03em;white-space:nowrap;opacity:0;transform-origin:0 50%;z-index:5}
#h0{opacity:1}
.hl1{display:flex;align-items:center} .hlg{margin-right:.16em;flex:none} .hl2{display:block}
#h2b{font-weight:800;letter-spacing:-.01em;border-bottom:5px solid INK;display:inline-block;padding-bottom:2px;margin-top:8px}
.hd.go{font-size:140px;line-height:140px;top:340px;left:108px}
#card{position:absolute;left:258px;top:560px;width:606px;height:HCARDpx;background:PAPER;border:6px solid INK;border-radius:10px;box-shadow:-12px 12px 0 INK;opacity:0;transform-origin:50% 0%;z-index:6}
.tape{position:absolute;width:120px;height:38px;background:rgba(232,221,186,.86);border:1px solid rgba(0,0,0,.14);z-index:3}
.tape.t1{right:-30px;top:-12px;transform:rotate(34deg)} .tape.t2{left:-30px;bottom:-6px;transform:rotate(34deg)}
.ct{position:absolute;left:34px;top:20px;font-weight:900;font-size:48px;line-height:60px;letter-spacing:-.03em;white-space:nowrap}
.cr{position:absolute;left:34px;right:34px;height:RHpx;display:flex;align-items:center;opacity:0;border-top:4px solid rgba(15,15,15,.14)}
.cp{width:48px;font-weight:900;font-size:52px;line-height:60px;text-align:center;margin-right:14px}
.cx{margin-left:18px;display:flex;flex-direction:column}
.cn{font-weight:900;font-size:44px;line-height:46px;letter-spacing:-.03em;white-space:nowrap}
.cv{font-weight:800;font-size:31px;line-height:38px;letter-spacing:-.01em;white-space:nowrap}
.cr i{position:absolute;left:0;right:0;bottom:1px;height:8px;border-radius:4px;transform-origin:0 50%;transform:scaleX(0)}
.cf{position:absolute;left:34px;bottom:18px;font-weight:800;font-size:33px;line-height:40px;white-space:nowrap;opacity:0}
'''
for a_, b_ in (("HCARD", 92 + 5 * RH + 62), ("RH", RH), ("MW", MW), ("GREEN", GREEN), ("INK", INK), ("PAPER", PAPER), ("RED", RED)):
    CSS = CSS.replace(a_, str(b_))

# ---------------------------------------------------------------- timeline (GSAP: text, premise, board; maze, dots, chips, marks are driven by render())
js(f"tl.fromTo('#cam',{{scale:1,rotation:0}},{{scale:1.012,rotation:.2,duration:{D / 4:.3f},ease:'sine.inOut',yoyo:true,repeat:3}},0);")
js(f"tl.fromTo('.bgw',{{x:0,y:0}},{{x:-14,y:-12,duration:{D / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},0);")
# beat 1: hook over the whole picture. The chips ripple so nothing sits still
for c in range(5):
    js(f"tl.fromTo('#sl{c} .tb',{{x:0}},{{x:-9,duration:.34,ease:'sine.inOut',yoyo:true,repeat:{max(1, int(a2 / .34) | 1)},immediateRender:false}},{.06 * c:.2f});")
sfx("subhit.ogg", .05, -6)
# beat 2: the premise as a process: the request -> a note to each AI -> each thinks -> each answers -> its dot lights up
js(f"tl.fromTo('#bub',{{opacity:0,y:50,scale:.9}},{{opacity:1,y:0,scale:1,duration:.36,ease:'back.out(1.6)',immediateRender:false}},{a2:.3f});")
sfx("whoosh_b.ogg", a2, -11)
tN = a2 + min(.42, .2 * d2); tC = a2 + .56 * d2; SPAWN = []
for c in range(5):
    t = tN + .06 * c
    js(f"tl.fromTo('#nt{c}',{{opacity:0,x:0,y:0,scale:.5}},{{opacity:1,scale:1,duration:.12,ease:'power2.out',immediateRender:false}},{t:.3f});")
    js(f"tl.to('#nt{c}',{{x:{CHX - 32 - 600},y:{CHYS[c] - 23 - (BUBY + 40)},rotation:{(c - 2) * 9},duration:.38,ease:'power2.inOut'}},{t + .06:.3f});")
    js(f"tl.to('#nt{c}',{{opacity:0,scale:.4,duration:.12,ease:'power2.in'}},{t + .4:.3f});")
    js(f"tl.fromTo('#tk{c}',{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.2,ease:'back.out(2)',immediateRender:false}},{t + .46:.3f});")
    js(f"tl.fromTo('#tk{c} i',{{y:0}},{{y:-6,duration:.16,ease:'sine.inOut',yoyo:true,repeat:5,stagger:.07,immediateRender:false}},{t + .5:.3f});")
    tc = max(tC + .07 * c, t + .86)
    js(f"tl.to('#tk{c}',{{opacity:0,scale:.5,duration:.14,ease:'power2.in'}},{tc - .1:.3f});")
    js(f"tl.fromTo('#ck{c}',{{opacity:0,scale:.2}},{{opacity:1,scale:1,duration:.28,ease:'back.out(2)',immediateRender:false}},{tc:.3f});")
    sfx("pop_a.ogg" if c % 2 == 0 else "pop_b.ogg", t, -11); sfx("tick.ogg", tc, -11)
    SPAWN.append(round(tc + .12, 3))
js(f"tl.to('#bub',{{opacity:0,y:30,scale:.92,duration:.24,ease:'power2.in'}},{min(tC - .1, a3 - .4):.3f});")
# beat 3: the AIs never see the maze: the walls fade for a moment
js(f"tl.to('#walls',{{opacity:.13,duration:.4,ease:'sine.inOut'}},{a3 + .08:.3f});")
js(f"tl.to('#walls',{{opacity:1,duration:.4,ease:'sine.inOut'}},{T0 - .3:.3f});")
js(f"tl.to('.ck',{{opacity:0,scale:.4,duration:.25,ease:'sine.in'}},{T0 - .1:.3f});")
sfx("toggle.ogg", a3 + .08, -10); sfx("whoosh_a.ogg", T0 - .03, -6)
# race sounds, from the events
nde = 0
for x in EV:
    if not (T0 < x["v"] <= vEND + .01): continue
    if x["kind"] == "exit": sfx("ding.ogg" if x["id"] == WINS[0] else "click_a.ogg", x["v"] + (.07 if x["id"] in WINS[1:] else 0), -6 if x["id"] == WINS[0] else -8)
    elif x["kind"] == "front" and x["step"] in (st5a, pair_run[0], 29): sfx("select.ogg", x["v"], -11)
    elif x["kind"] == "near_miss": sfx("impactsoft.ogg", x["v"] + .3, -10)
    elif x["kind"] == "dead_end" and nde < 8 and TWIN[x["id"]] == x["id"] and x["v"] - SFX[-1]["t"] > .3: sfx("tick.ogg", x["v"], -13); nde += 1
sfx("riser.ogg", max(T0, vX - 1.6), -13); sfx("whoosh_c.ogg", vCG, -11); sfx("impactsoft.ogg", vEND, -9)
# the tie reveal (line 8): on the maze, the two winning trails are drawn again and close into one line
sfx("whoosh_b.ogg", tSAME, -10); sfx("ding.ogg", tSAME + .8, -8)
# the board (line 9): rows land from the last place up, the tie last (both together), then their lines
js(f"tl.fromTo('#card',{{opacity:0}},{{opacity:1,duration:.12,ease:'none',immediateRender:false}},{tK + .03:.3f});")
js(f"tl.fromTo('#card',{{y:110,rotation:3,scale:1}},{{y:0,rotation:-1,duration:.5,ease:'power3.out',immediateRender:false}},{tK + .03:.3f});")
sfx("whoosh_b.ogg", tK, -10)
nw = len(WINS); t = tK + .3; RT_ = {}
for i in range(4, -1, -1):
    k = ORDER[i]
    if k in WINS and k != ORDER[nw - 1]: RT_[i] = RT_[nw - 1]; continue
    if k in WINS: t += .22
    RT_[i] = t; sfx("pop_a.ogg" if i % 2 == 0 else "pop_b.ogg", t, -10); t += .2
for i in range(5):
    js(f"tl.fromTo('#cr{i}',{{opacity:0,x:-46}},{{opacity:1,x:0,duration:.36,ease:'power3.out',immediateRender:false}},{RT_[i]:.3f});")
tU = RT_[0] + .5
for i in range(nw):
    js(f"tl.to('#cr{i} i',{{scaleX:1,duration:.5,ease:'power2.inOut'}},{tU:.3f});")
    js(f"tl.fromTo('#cr{i} .bdg',{{scale:1}},{{scale:1.16,duration:.3,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tU + .1 * i:.3f});")
js(f"tl.fromTo('.cf',{{opacity:0}},{{opacity:1,duration:.3,ease:'sine.out',immediateRender:false}},{tU + .3:.3f});")
js(f"tl.to('#card',{{rotation:.6,y:-8,duration:{max(.8, (tF - tK - .8) / 6):.3f},ease:'sine.inOut',yoyo:true,repeat:5}},{tK + .55:.3f});")
t = tU + .9; q = 0
while t < tF - .5:                                           # a slow wave keeps the board alive while it is read
    js(f"tl.fromTo('#cr{q % 5} .bdg',{{rotation:0}},{{rotation:{-10 if q % 2 else 10},duration:.28,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{t:.3f});"); t += .45; q += 1
js(f"tl.to('#card',{{y:50,duration:.24,ease:'power2.in'}},{tF - .4:.3f});")
js(f"tl.to('#card',{{opacity:0,duration:.1,ease:'none'}},{tF - .26:.3f});")
sfx("tick.ogg", s(10) + .1, -10); sfx("whoosh_c.ogg", tF - .2, -12)

# no flat stretch: a soft camera push on every beat, and on a data event (dead end) wherever two beats are more than 2.2 s apart
PUN = sorted({round(t, 2) for t in (.9, a2, a3 + .1, T0, s(4), s(5), vCL, vPAIR, vX, s(7), vCLX, vCG, vEND, tRV, tSAME, tSAME + .8, tK + .05, tU, s(10), tFOL)})
for _ in range(20):
    g = next((i for i in range(len(PUN) - 1) if PUN[i + 1] - PUN[i] > 2.2), None)
    if g is None: break
    mid = (PUN[g] + PUN[g + 1]) / 2
    cand = [x["v"] for x in EV if x["kind"] == "dead_end" and PUN[g] + .9 < x["v"] < PUN[g + 1] - .9]
    PUN = sorted(PUN + [round(min(cand, key=lambda v: abs(v - mid)) if cand else mid, 2)])
for t in PUN: js(f"tl.fromTo('#pn',{{scale:1}},{{scale:1.035,duration:.17,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{t:.3f});")
# ---------------------------------------------------------------- render(): dots, trails, chips, marks, counter: all from the clock
ci = lambda ks: [IDS.index(k) for k in ks]
DATA = dict(a2=round(a2, 3), KC=[KCX, KCY], KO=[IDS.index(near['id']), round(vX + .3, 3), round(s(7) + .15, 3)], T0=T0, D=D, tF=round(tF, 3), tK=round(tK, 3), tRV=round(tRV, 3), tS=round(tSAME, 3), vEND=round(vEND, 3), ST=ST, MAXS=MAXS, CELL=CELL, MX=MX, MY=MY,
            CHX=CHX, CHYS=CHYS, FAN=FAN, FANS=FANS, OFF=OFF, TOFF=TOFF,
            P=[[v for p in PATH[k] for v in p] for k in IDS], LAST=[LAST[k] for k in IDS], CL=CLEN,
            DS=[[dist(p) for p in PATH[k]] for k in IDS], FR=[sum(1 << IDS.index(k) for k in f) for f in FRONT[:F1 + 1]], F1=F1,
            VX=[VXT.get(k) for k in IDS], DNF=[k in DNFS for k in IDS], SP=SPAWN, WIN=ci(WINS), TW=[IDS.index(TWIN[k]) for k in IDS],
            NM=[IDS.index(near["id"]), round(v_of(near["step"]), 3), round(v_of(near["back_at"]), 3)])
RJS = r'''
const Dt=__DATA__;
const ez=p=>{p=p<0?0:p>1?1:p;return p*p*(3-2*p)}, lerp=(a,b,t)=>a+(b-a)*t, bump=p=>p>0&&p<1?Math.sin(Math.PI*p):0, $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
function St(v){const i=Math.max(0,v*60),k=Math.min(Dt.ST.length-2,Math.floor(i));return lerp(Dt.ST[k],Dt.ST[k+1],Math.min(1,i-k))}
const dots=$$('.dot').map(el=>({el,dr:el.querySelector('.dr')})), trs=$$('.trl'), cnt=$('#cnt'), cnn=$('#cnn'), exm=$('#exm'), exc=$('#exc'), stc=$('#stc');
const chips=[0,1,2,3,4].map(c=>{const el=$('#sl'+c);return {el,tb:el.querySelector('.tb'),ring:el.querySelector('.ring'),ok:el.querySelector('.ok'),qm:el.querySelector('.qm'),dn:el.querySelector('.dn')}});
const rays=$('#rays'), ko=$('#ko'), kws=$$('.kw'), kcl=$('#kcl'), kst=$('#kst'), stars=$$('.star'), kos=$('.kos'), eo=p=>1-Math.pow(1-Math.max(0,Math.min(1,p)),3);
const dms=$$('.dm').map(el=>({el,c:+el.dataset.c,s:+el.dataset.s})), cms=$$('.cm').map(el=>({el,c:+el.dataset.c}));
const C=Dt.CELL;
function render(v){
  const st=St(v), pOut=ez((v-Dt.tF)/.5), on=1-pOut, race=v>=Dt.T0&&v<Dt.tF, pre=v<Dt.T0?1:Math.max(1-ez(st/5),pOut);   // pre: 1 = the dots fanned and large in the centre
  exm.style.transform='translate('+(Math.sin(v*5.2)*4).toFixed(1)+'px,0)'; exc.style.opacity=(.22+.16*Math.sin(v*5.2)).toFixed(3);
  rays.style.opacity=(v<Dt.a2?0:v<Dt.T0?1-ez((v-Dt.T0+.4)/.4):0).toFixed(2); rays.style.transform='rotate('+(v*14).toFixed(1)+'deg) scale('+(1+.05*Math.sin(v*6)).toFixed(3)+')';
  // the hook picture (frame 0 and the loop end): the two winners on top, Claude knocked back, stars, a K.O. stamp. Cartoon only.
  const kq=v<Dt.a2?1-ez((v-Dt.a2+.32)/.26):ez((v-Dt.tF-.08)/.4), kt=v<Dt.a2?v:9;
  ko.style.opacity=kq.toFixed(3); ko.style.transform='scale('+(.9+.1*kq).toFixed(3)+')'; ko.style.transformOrigin=Dt.KC[0]+'px '+(Dt.KC[1]-120)+'px';
  kws.forEach((el,i)=>{el.style.transform='translate(0,'+(Math.sin(v*6.5+i*1.9)*9-30*(1-eo(kt/.4))).toFixed(1)+'px) scale('+(.86+.14*eo(kt/.4)+.03*Math.sin(v*6.5+i*1.9)).toFixed(3)+')'});
  kcl.style.transform='translate('+(26*eo(kt/.32)).toFixed(1)+'px,'+(18*eo(kt/.32)).toFixed(1)+'px) rotate('+(8+18*eo(kt/.32)+3*Math.sin(v*4.4)).toFixed(1)+'deg)';
  kst.style.transform='rotate(-11deg) scale('+(1+.32*(1-eo(kt/.3))+.045*Math.sin(v*8)).toFixed(3)+')';
  let scx=Dt.KC[0]+26, scy=Dt.KC[1]-96, srx=96, sry=26, so=kq, ss=1; const kow=v>=Dt.KO[1]&&v<Dt.KO[2];
  stc.style.opacity=(.75+.25*Math.sin(v*3.1)).toFixed(3);
  const si=Math.min(Math.floor(st),Dt.F1), fr=race&&v<Dt.vEND?Dt.FR[si]:0, rv=v>=Dt.tRV&&v<Dt.tF, rp=ez((v-Dt.tS)/.75), rm=ez((v-Dt.tS-.75)/.3);
  for(let c=0;c<5;c++){
    const ch=chips[c], lead=(fr>>c)&1, win=Dt.WIN.includes(c), cx=Dt.CHX, cy=Dt.CHYS[c];
    const vx=Dt.VX[c], out=vx!==null&&v>=vx&&v<Dt.tF, okp=out?(v-vx-.45)/.4:-1, stuck=Dt.DNF[c]&&v>=Dt.vEND&&v<Dt.tF;
    ch.el.style.transform='scale('+(1+.25*bump(okp)+(win&&rv?.12*bump((v-Dt.tS-.75)/.5):0)).toFixed(4)+')';
    ch.ring.style.opacity=((lead?1:0)+(win&&v>=Dt.tS+.75&&v<Dt.tF?1:0)).toFixed(2); ch.ring.style.transform='scale('+(1+.06*Math.sin(v*7)).toFixed(3)+')';
    ch.ok.style.opacity=(okp>0?on:0); ch.ok.style.transform='scale('+(.4+.6*ez(okp/.5)).toFixed(3)+')';
    ch.qm.style.opacity=stuck?on:0; ch.qm.style.transform='scale('+(stuck?.6+.4*ez((v-Dt.vEND)/.3)+.08*Math.sin(v*5):1).toFixed(3)+')';
    ch.tb.style.opacity=(1-.55*(stuck?on:0)).toFixed(2);
    // dot
    const n=Dt.LAST[c], k=Math.min(Math.floor(st),n-1), f=Math.min(1,Math.max(0,st-k)), P=Dt.P[c];
    const gx=lerp(P[2*k],P[2*k+2],f), gy=lerp(P[2*k+1],P[2*k+3],f);
    const br=v<Dt.T0?(.6+.4*eo((v-Dt.a2)/.7)+.03*Math.sin(v*3.3+c)):1;
    let x=Dt.MX+(gx+.5)*C+lerp(Dt.OFF[c][0],Dt.FAN[c][0]*br,pre), y=Dt.MY+(gy+.5)*C+lerp(Dt.OFF[c][1],Dt.FAN[c][1]*br,pre), o=ez((v-Dt.a2+.06)/.2), k_=lerp(1,Dt.FANS,pre);
    const lit=1; k_*=1+.3*bump((v-Dt.SP[c])/.4);
    if(out){const q=ez((v-vx)/.6); x=lerp(x,cx,q); y=lerp(y,cy,q)-90*bump(q); o=1-ez((q-.75)/.25); k_*=lerp(1,.7,q)*(1+.5*bump((v-vx)/.3))}
    else if(lead) k_*=1.14+.05*Math.sin(v*9);
    if(c===Dt.NM[0]&&v>=Dt.NM[1]&&v<Dt.NM[2]) k_*=1.16+.08*Math.sin(v*10);
    if(race&&!out&&!stuck) k_*=1+.04*Math.sin(v*11+c*1.3);
    if(v>=Dt.tF) o=Math.min(o,1-ez((v-Dt.tF)/.15));
    if(c===Dt.KO[0]&&kow){scx=x; scy=y-34; srx=40; sry=12; so=1; ss=.55}
    const d=dots[c]; d.el.style.opacity=o.toFixed(3); d.el.style.zIndex=lead?9:5-c; d.dr.style.opacity=lit.toFixed(3);
    d.el.style.transform='translate('+x.toFixed(2)+'px,'+y.toFixed(2)+'px) scale('+k_.toFixed(4)+')';
    // trail: live during the race; in the reveal the winners' trails are drawn again and close into one line
    const cl=Dt.CL[c], tot=cl[cl.length-1]+2, len=lerp(cl[k],cl[k+1],f), t_=trs[c];
    let off=tot-len, op=ez((v-Dt.T0-.2)/.5)*on*.8, tx=0, ty=0, sw=5.5;
    if(rv){ if(win){off=v<Dt.tS?0:tot*(1-rp); op=on; sw=5.5+3*rp-1.5*rm; tx=-Dt.TOFF[c][0]*rm; ty=-Dt.TOFF[c][1]*rm} else op=lerp(.8,.13,ez((v-Dt.tRV)/.3))*on }
    t_.style.strokeDashoffset=off.toFixed(1); t_.style.opacity=op.toFixed(3); t_.style.strokeWidth=sw.toFixed(2); t_.style.transform='translate('+tx.toFixed(2)+'px,'+ty.toFixed(2)+'px)';
    // steps to the exit, under the chip (race only)
    const ds=Dt.DS[c][Math.min(Math.round(st),n)], nm=c===Dt.NM[0]&&v>=Dt.NM[1]-.3&&v<Dt.NM[2]+.4;
    ch.dn.textContent=out?'':ds; ch.dn.style.opacity=(race&&!out&&v<Dt.vEND?ez((v-Dt.T0)/.4):0).toFixed(2); ch.dn.style.color=(lead||nm)?'#E5372B':'#0f0f0f';
    ch.dn.style.transform='scale('+(nm?1.25+.1*Math.sin(v*10):1).toFixed(3)+')';
  }
  for(const m of dms){const q=(st-m.s)/6; m.el.style.opacity=(race&&st>=m.s&&!rv?(.35+.65*(1-ez(q))):0).toFixed(2)}
  stars.forEach((el,i)=>{const a=v*5.2+i*Math.PI/2, z=Math.sin(a); el.style.opacity=(so*(.75+.25*z)).toFixed(2); el.style.zIndex=z>0?2:1;
    el.style.transform='translate('+(scx+Math.cos(a)*srx).toFixed(1)+'px,'+(scy+z*sry).toFixed(1)+'px) scale('+(ss*(.8+.25*z)).toFixed(3)+') rotate('+(v*90+i*40).toFixed(0)+'deg)'});
  kos.style.opacity=kow?1:0; kos.style.transform='rotate(-10deg) scale('+(1+.5*(1-eo((v-Dt.KO[1])/.25))+.05*Math.sin(v*8)).toFixed(3)+')';
  for(const m of cms){const a=v>=Dt.vEND&&v<Dt.tRV; m.el.style.opacity=a?1:0; m.el.style.transform='scale('+(1+.22*Math.sin(v*6)).toFixed(3)+')'}
  cnt.style.opacity=(race&&v<Dt.tK?ez((v-Dt.T0-.2)/.4):0).toFixed(2); cnn.textContent=Math.min(Dt.MAXS,Math.round(st));
}
'''.replace("__DATA__", json.dumps(DATA, separators=(",", ":")))

JS = re.sub(r"tl\.set\(([^,]+),\{", r"tl.set(\1,{immediateRender:false,", "\n".join(J))
SFX.sort(key=lambda x: x["t"])
json.dump(SFX, open(H_ + "/sfx99.json", "w"), indent=1)
sps = lambda a, b: round((b - a) / max(.001, VT[b] - VT[a]), 1)
ROLE = {1: "hook", 2: "premise", 3: "rules+Go", 8: "tie reveal", 9: "setup (board)", 10: "follow line"}
json.dump(dict(placeholder=dict(data=False, script=False, results_file=os.path.relpath(RPATH, H_)),
               lines=[dict(n=n, text=LINES[n - 1], start=round(s(n), 3), end=round(e(n), 3), role=ROLE.get(n, "race")) for n in range(1, NL + 1)],
               D=D, go=T0, sources=SRC, targets={str(n): TG[n] for n in range(4, NL + 1)}, drift_vs_targets=DRIFT, lines_on_targets=ONTG,
               race=dict(anchors=[dict(v=round(v, 3), step=st_) for v, st_ in ANCH], race_only_s=RACEONLY,
                         steps_per_second={f"{a}-{b}": sps(a, b) for (_, a), (_, b) in zip(ANCH, ANCH[1:])},
                         first_exit=round(vX, 3), end=round(vEND, 3), reveal=round(tRV, 3), board=round(tK, 3), frame0_returns=round(tF, 3),
                         order=[dict(place=RES[k]["place"], id=k, status=STATUS[k], steps=RES[k].get("exitStep"), closest=RES[k].get("closestDist"), board_text=rowtext(k)) for k in ORDER],
                         events=[x for x in EV if x["kind"] != "dead_end"], dead_ends={k: [dict(step=i, v=round(v_of(i), 3)) for i, _, _ in DEADS[k]] for k in IDS}),
               facts=FACTS, headlines=[dict(t=t, text=x) for t, x in sorted(HLOG)]), open(H_ + "/cues99.json", "w"), indent=1)
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
say(f"results: {os.path.relpath(RPATH, H_)} (real)  D={D} go={T0}  lines on targets (take not padded)={ONTG}  js={len(J)} sfx={len(SFX)}")
say("lines: " + "  ".join(f"{n}:{s(n):.2f}-{e(n):.2f}" for n in range(1, NL + 1)))
say("targets (line starts for voice/stitch.py): " + "  ".join(f"{n}:{TG[n]:.2f}" for n in range(4, NL + 1)) + "   drift of the take on disk: " + "  ".join(f"{n}:{DRIFT[n]:+.2f}" for n in DRIFT))
say("race clock anchors: " + "  ".join(f"step {st_}@{v:.2f}" for v, st_ in ANCH) + "   steps/s: " + ", ".join(f"{a}-{b}: {sps(a, b)}" for (_, a), (_, b) in zip(ANCH, ANCH[1:])))
say("word sources: " + ", ".join(f"{k}={v}" for k, v in SRC.items()))
for f in FACTS: say("  " + f)
say("front runs (strict): " + "  ".join(f"{a}-{b}:{'+'.join(f)}" for a, b, f in runs))
for x in EV:
    if x["kind"] not in ("dead_end", "front"): say(f"  {x['v']:6.2f}s step {x['step']:3d} {x['kind']:22s} {x['id']}" + (f" closest {x['closest']}" if x.get("closest") else ""))
hs = sorted(HLOG); say("headlines: " + " | ".join(f"{t:.2f} {x}" for t, x in hs))
gaps = [(round(hs[i + 1][0] - hs[i][0], 2), hs[i][1]) for i in range(len(hs) - 1) if hs[i + 1][0] - hs[i][0] > 2.5]
if gaps: say("NOTE headline holds over 2.5 s (the stage moves under them): " + str(gaps))
open(H_ + "/out/build.log", "w").write("\n".join(LOG) + "\n")
