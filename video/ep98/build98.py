#!/usr/bin/env python3
"""ep98 'AI RACE #1' scene, v4 (T8c), Miki style, HyperFrames + GSAP paused timeline, 1080x1920.
Script: voice/lines.txt (12 lines). v4 (David, 15.11): (A) the stage is full-bleed under the headline band and fills the
safe box (track turned 90 degrees so the cars leave upward, cars big); (B) the first seconds SHOW the process on a
line-up: the request goes to the five logo chips, each answers (dots, check), each car gets its colour and logo.
TIMELINE: lines 1-4 always come from the voice cues. If the event lines (5-9) of the take are more than 0.45 s
away from their race targets (a stitch without padding), lines 5-12 are placed on the TARGETS (real durations),
so the picture matches the re-stitched voice; cues98.json says which (timeline). PLACE=cues forces the cue times.

Reads  arena/race.json, arena/track.json, voice/lines.txt, voice/narration-raw-cues.json, voice/words.json.
Writes hf/index.html, cues98.json (lines + D + targets for the voice), sfx98.json (event times).

STALE VOICE: the cue line texts are compared with voice/lines.txt. If they differ (old take still on disk)
the build uses an ESTIMATED timeline (durations of unchanged lines are taken from the old take, the rest
from the line length) and says so in the log and in cues98.json (stale_cues: true). EST=1 forces it.

What is true on screen, and what is a scene choice:
  - Every car position/angle is race.json, frame for frame, interpolated only between two 60 fps frames.
  - The race clock runs at 1x from the spoken "Go" until the replay. ONE exception, labelled
    SLOW MOTION REPLAY on screen the whole time it lasts: the finish of Claude and Gemini is shown again
    at 1/4 speed (same race.json frames).
  - No live ranking: the strip shows the five logos in a fixed order with status only (lap dots, ? stuck,
    X wall). The winner is named only on the replay.
  - Scene choices (not race data): the camera (zoom/position); the cars are drawn about 2.2-2.6x their physical
    size so the logos read, and shrink toward their physical size when the camera zooms into the hairpin
    (so 'touches the wall' looks right); before "Go" they stand staggered around the line (race.json starts
    all five on the same spot) and that offset fades out during the first 1.2 s of the race; before the race the
    five cars are shown side by side on a drawn line-up (not race data), where the request/answer picture plays;
    the whole track is drawn turned 90 degrees; after a car
    finishes it coasts to a parking slot past the line (race.json stops it on the line); at the end the cars
    are back on the grid for the loop.
No TTS, no audio is written here.
"""
import json, os, re, math, shutil, wave, random
H_ = os.path.dirname(os.path.abspath(__file__))
INK = "#0f0f0f"; PAPER = "#fbfbf8"; RED = "#E5372B"; ROAD = "#d6d2c6"
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
LOG = []
def say(x): LOG.append(x); print(x)

# ---------------------------------------------------------------- assets (fonts + paper from the ep97 build)
for sub in ("fonts/InterDisplay-Black.otf", "fonts/InterDisplay-ExtraBold.otf", "fonts/InterDisplay-Medium.otf", "bg.jpg"):
    dst = f"{H_}/hf/assets/{sub}"
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(f"{H_}/../ep97/hf/assets/{sub}", dst)

# ---------------------------------------------------------------- race data
R = json.load(open(H_ + "/arena/race.json")); TR = json.load(open(H_ + "/arena/track.json"))
IDS = ["chatgpt", "gemini", "claude", "meta", "perplexity"]          # fixed order of the strip, never re-sorted
NAME = {"chatgpt": "ChatGPT", "gemini": "Gemini", "claude": "Claude", "meta": "Meta AI", "perplexity": "Perplexity"}
COL = {"chatgpt": "#10A37F", "gemini": "#4285F4", "claude": "#D97757", "meta": "#B44BFF", "perplexity": "#20808D"}
LOGO = {"chatgpt": "chatgpt.svg", "gemini": "gemini.svg", "claude": "claude.svg", "meta": "meta-ai.svg", "perplexity": "perplexity.svg"}
FR = {c["id"]: c["frames"] for c in R["cars"]}
RES = {x["id"]: x for x in R["result"]}
FPS = R["fps"]; assert FPS == 60
FIN = {k: RES[k]["finishFrame"] for k in IDS if RES[k]["status"] == "finish"}
NF = max(FIN.values()) + 6
CLN = TR["centerline"]; NCL = len(CLN)
def stopframe(k):
    f = FR[k]
    if RES[k]["status"] == "wall": return next(i for i in range(len(f)) if f[i][5] == "wall")
    if k in FIN: return FIN[k]
    return next(i for i in range(1, len(f)) if f[i][3] == 0 and all(f[j][3] == 0 for j in range(i, min(i + 120, len(f)))))
STOP = {k: stopframe(k) for k in IDS}                       # frame where the car stops for good (finish, wall, stuck)
LAPF = {k: [i for i in range(1, NF + 1) if FR[k][i][4] != FR[k][i - 1][4]] for k in IDS}
X = [[round(FR[k][min(i, STOP[k])][0], 1) for i in range(NF + 1)] for k in IDS]
Y = [[round(FR[k][min(i, STOP[k])][1], 1) for i in range(NF + 1)] for k in IDS]
A = [[round(FR[k][min(i, STOP[k])][2], 3) for i in range(NF + 1)] for k in IDS]
CLEN = []; TRD = []
for c, k in enumerate(IDS):
    acc = [0.0]
    for i in range(1, NF + 1): acc.append(acc[-1] + math.hypot(X[c][i] - X[c][i - 1], Y[c][i] - Y[c][i - 1]))
    CLEN.append([round(v, 1) for v in acc])
    TRD.append("M" + " L".join(f"{X[c][i]} {Y[c][i]}" for i in range(0, STOP[k] + 1)))
def cl_at(back_px):
    """centreline point `back_px` before (+) or after (-) the line: x, y, heading."""
    j = (-round(back_px / 6)) % NCL; p = CLN[j]; q = CLN[(j + 1) % NCL]
    return p[0], p[1], math.atan2(q[1] - p[1], q[0] - p[0])
GRID = []
for c in range(5):                                          # staggered grid around the line (scene choice)
    x, y, a = cl_at(-116 + 58 * c); lat = (-30 if c % 2 == 0 else 30)
    GRID.append([round(x - math.sin(a) * lat, 1), round(y + math.cos(a) * lat, 1), round(a, 3)])
PLACE = {k: RES[k]["place"] for k in IDS}
SLOT = {}
for k in FIN:                                               # parking slots past the line (scene choice)
    d = {1: 264, 2: 174, 3: 84}[PLACE[k]]; x, y, a = cl_at(-d)
    v0 = max(3.0, FR[k][FIN[k] - 1][3]) * 60
    SLOT[IDS.index(k)] = dict(f=FIN[k], x=round(x, 1), y=round(y, 1), a=round(a, 3), T=round(max(.6, 2 * d / v0), 3))
tP = STOP["perplexity"] / 60; tM = STOP["meta"] / 60        # 4.22 and 6.15 (race clock)
tC = RES["claude"]["timeS"]; tGm = RES["gemini"]["timeS"]; tCh = RES["chatgpt"]["timeS"]
GAP = round(tGm - tC, 1)                                    # 0.2 s
rEND = NF / 60

# ---------------------------------------------------------------- cues: fresh take, or an estimated timeline
LINES = [l.strip() for l in open(H_ + "/voice/lines.txt") if l.strip()]; NL = len(LINES)
try:
    C = json.load(open(H_ + "/voice/narration-raw-cues.json")); C = C if isinstance(C, list) else C["lines"]
except Exception:
    C = []
ctext = lambda c: c.get("line", c.get("text", ""))
CUE = {c["n"]: c for c in C if "n" in c}
FORCE_EST = os.environ.get("EST") == "1"
STALE = FORCE_EST or len(CUE) != NL or any(n not in CUE or norm(ctext(CUE[n])) != norm(LINES[n - 1]) for n in range(1, NL + 1))
OLD = {norm(ctext(c)): float(c["end"]) - float(c["start"]) for c in C if "start" in c}
DUR = {}
for n in range(1, NL + 1):
    t = LINES[n - 1]
    if not STALE: DUR[n] = float(CUE[n]["end"]) - float(CUE[n]["start"])
    elif norm(t) in OLD: DUR[n] = round(OLD[norm(t)], 2)                 # same words in the old take: its real length
    elif n == 4: DUR[n] = 1.25                                          # "Pick one. Go!"
    else: DUR[n] = round(.3 + .045 * len(t), 2)
WORDS = []
if not STALE:
    try:
        WORDS = json.load(open(H_ + "/voice/words.json"))
        if not (WORDS and norm(WORDS[0][0]) == norm(LINES[0].split()[0]) and abs(WORDS[-1][2] - float(CUE[NL]["end"])) < 1.2): WORDS = []
    except Exception:
        WORDS = []
SRC = {}
# lines 1-4 and the word "Go" (the race starts on it)
SHIFT = {}
if STALE:
    L = {1: (.08, round(.08 + DUR[1], 2))}
    for n in (2, 3, 4): L[n] = (round(L[n - 1][1] + .1, 2), round(L[n - 1][1] + .1 + DUR[n], 2))
else:
    L = {n: (float(CUE[n]["start"]), float(CUE[n]["end"])) for n in range(1, NL + 1)}
s = lambda n: L[n][0]
e = lambda n: L[n][1]
def W(word, n, k=0):
    c = 0
    for w, a, b in WORDS:
        a = a + SHIFT.get(n, 0)
        if s(n) - .12 <= a <= e(n) + .12 and norm(w) == word:
            if c == k: return a
            c += 1
    return None
def speech(n, gap):
    """speech segments (start, end) inside line n, measured on the wav; [] if it cannot be read."""
    try:
        import numpy as np
        w = wave.open(H_ + "/voice/narration-raw.wav"); sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
        if w.getnchannels() > 1: a = a.reshape(-1, w.getnchannels()).mean(1)
        hop = int(sr * .01); t0 = s(n) - .05; t1 = e(n) + .05
        env = [math.sqrt(float((a[int(t * sr):int(t * sr) + hop] ** 2).mean() or 0)) for t in [t0 + i * .01 for i in range(int((t1 - t0) / .01))]]
        m = max(env); on = [x > .08 * m for x in env]; seg = []; i = 0
        while i < len(on):
            if on[i]:
                j = i
                while j < len(on) and on[j]: j += 1
                seg.append([t0 + i * .01, t0 + j * .01]); i = j
            else: i += 1
        out = []
        for a_, b_ in seg:
            if out and a_ - out[-1][1] < gap: out[-1][1] = b_
            else: out.append([a_, b_])
        return [x for x in out if x[1] - x[0] >= .05]
    except Exception:
        return []
if STALE: T0 = s(4) + .63 * DUR[4]; SRC["go"] = "ESTIMATE (stale cues)"
else:
    T0 = W("go", 4)
    if T0 is not None: SRC["go"] = "words.json"
    else:
        sg = speech(4, .15)
        if len(sg) >= 2: T0 = sg[-1][0]; SRC["go"] = "speech gap in the wav"
        else: T0 = s(4) + .63 * (e(4) - s(4)); SRC["go"] = "line fraction"
T0 = round(T0, 3)
V = lambda r: T0 + r                                         # video time of a race time, live part (1x)
vP, vM, vC, vGm, vCh = V(tP), V(tM), V(tC), V(tGm), V(tCh)
# where each line should start so the words land on the race (targets for the voice; also the estimated timeline)
TG = {1: L[1][0], 2: L[2][0], 3: L[3][0], 4: L[4][0]}
TG[5] = round(vP - .45, 2)                                   # "stops" lands as Perplexity stops
TG[6] = round(max(TG[5] + DUR[5] + .06, vM - .5), 2)         # "hits" lands on the wall
TG[7] = round(max(TG[6] + DUR[6] + .08, vC - DUR[7] - .15), 2)   # ends as the two cross the line
TG[8] = round(max(TG[7] + DUR[7] + .08, vGm + .45), 2)
TG[9] = round(max(TG[8] + DUR[8] + .1, vCh + .2), 2)         # the replay
for n in range(10, NL + 1): TG[n] = round(TG[n - 1] + DUR[n - 1] + .12, 2)
DRIFT = {n: round(L[n][0] - TG[n], 2) for n in range(5, 10)} if not STALE else {}
ONTG = STALE or (os.environ.get("PLACE") != "cues" and any(abs(v) > .45 for v in DRIFT.values()))
if ONTG:
    for n in range(5, NL + 1):
        if not STALE: SHIFT[n] = TG[n] - L[n][0]
        L[n] = (TG[n], round(TG[n] + DUR[n], 2))
D = round(e(NL) + .45, 2)
tF = D - .58                                                 # the frame-0 layout comes back from here

# ---------------------------------------------------------------- race clock r(v): 1x live, then the 1/4-speed replay
SLOW = .25
vR0 = max(s(9) - .35, vGm + .9)                              # replay: the dip starts
vRm = vR0 + .14                                              # the clock jumps here, under the dip
tw7 = W("wins", 9)
vX = max(vRm + .62, tw7 if tw7 is not None else s(9) + .32 * (e(9) - s(9)))   # Claude's nose crosses the line in the replay
vXg = vX + (tGm - tC) / SLOW                                 # Gemini crosses in the replay
tK = max(s(10) - .05, vXg + .45)                              # result card
vJ = tK + .55                                                # card covers the stage: the clock goes to the end state
rA = tC - SLOW * (vX - vRm)
def r_of(v):
    if v < T0: return 0.0
    if v < vRm: return min(v - T0, rEND)
    if v < vJ: return min(rEND, tC + SLOW * (v - vX))
    return rEND
RT = [round(r_of(n / 60), 4) for n in range(int(D * 60) + 4)]
assert vGm + .3 < vRm, "replay would start before the live finish"
LIVE_END = round(vRm - T0, 2)


# ---------------------------------------------------------------- page geometry (v4): headline band on top, full-bleed stage below it
BAND = 470                                                  # the stage starts here (page y); above it: paper + the headline
VPL, VPT, VPW, VPH = -20, BAND, 1120, 1920 - BAND + 20      # the stage: full width, down to the bottom of the page
PCX, PCY = 495 - VPL, 860 - VPT                             # where the camera centre sits (page 495, 860: middle of the action area)
AW, AH = 770, 700                                           # action area the camera keeps the cars in (page x 110-880, y 510-1210)
CXS = [160, 350, 540, 730, 920]                             # the five columns: line-up cars and their chips
CARY, CHY, CHD = 657, 892, 100                              # line-up car centre y, chip centre y, chip diameter
STRIPX, STRIPY0, STRIPDY, STRIPS = 962, 560, 124, .86       # chips as the status strip during the race: a column on the right edge of the safe box
GRASS = "#c5d3aa"; ROAD = "#cdc9bc"

# ---------------------------------------------------------------- camera (scene choice): centre x, y, zoom and car draw scale per race frame
# the world is drawn turned 90 degrees (world +x = up the page), so world x-extent uses the height, world y-extent the width
ZG = 1.9
GC = [300.0, 694.0]                                         # grid camera centre
FC = [282.0, 690.0]                                         # finish-line camera centre (replay)
kz = lambda z: max(.72, min(1.3, 1.78 / z))
def box(pts, m, zmax, zmin=1.3):
    x0 = min(p[0] for p in pts); x1 = max(p[0] for p in pts); y0 = min(p[1] for p in pts); y1 = max(p[1] for p in pts)
    z = max(zmin, min(zmax, AH / (x1 - x0 + 2 * m), AW / (y1 - y0 + 2 * m)))
    return (x0 + x1) / 2, (y0 + y1) / 2, z, kz(z)
def cam_target(i):
    r = i / 60; pos = lambda k: (FR[k][min(i, STOP[k])][0], FR[k][min(i, STOP[k])][1]); line = (300, 700)
    if r < 2.6: return box([pos(k) for k in IDS], 100, 2.1)
    if r < 3.7: return box([pos(k) for k in IDS if k != "meta"], 100, 2.1)
    if r < 4.8: return (182, 628, 2.5, .72)                  # hairpin: Perplexity stops
    if r < 5.6: return (250, 625, 1.6, .95)                  # hairpin + line: ChatGPT passes, Meta AI arrives
    if r < 6.9: return (190, 616, 2.8, .7)                   # hairpin: Meta AI and the wall
    if r < 8.0: return box([pos("claude"), pos("gemini"), (181, 608)], 110, 1.9)   # the two leaders come back to the hairpin; the stopped cars stay in view
    if r < 8.95: return box([pos("claude"), pos("gemini"), line], 100, 1.9)
    return box([pos("chatgpt"), line], 110, 1.8)
raw = [cam_target(i) for i in range(NF + 1)]
def smooth(vals, sg=20):
    n = len(vals); ker = [math.exp(-.5 * (q / sg) ** 2) for q in range(-3 * sg, 3 * sg + 1)]; ks = sum(ker)
    return [sum(ker[q + 3 * sg] * vals[min(n - 1, max(0, i + q))] for q in range(-3 * sg, 3 * sg + 1)) / ks for i in range(n)]
CX = [round(v, 1) for v in smooth([t[0] for t in raw])]; CY = [round(v, 1) for v in smooth([t[1] for t in raw])]
CZ = [round(math.exp(v), 4) for v in smooth([math.log(t[2]) for t in raw])]; CK = [round(v, 3) for v in smooth([t[3] for t in raw])]
MINCAR = min(80 * CZ[i] * CK[i] for i in range(NF + 1))     # smallest car length on screen (px) in the race

# ---------------------------------------------------------------- text helpers
try:
    from PIL import ImageFont
    _f = ImageFont.truetype(H_ + "/hf/assets/fonts/InterDisplay-Black.otf", 100)
    _f8 = ImageFont.truetype(H_ + "/hf/assets/fonts/InterDisplay-ExtraBold.otf", 100)
    tw = lambda t: _f.getlength(t) - 3.0 * len(t)           # letter-spacing -.03em
    tw8 = lambda t: _f8.getlength(t) - 1.0 * len(t)
except Exception:
    tw = lambda t: 62 * len(t); tw8 = lambda t: 56 * len(t)
def logo(k, h, cls=""):
    if k == "perplexity":                                   # raw file, icon part only (x 0-28.14 of 149.82)
        return f'<span class="pxl {cls}" style="width:{h * 28.14 / 36:.1f}px;height:{h}px"><img src="assets/logos/perplexity.svg" style="height:{h}px;width:{h * 149.82 / 36:.1f}px"></span>'
    return f'<img class="lg {cls}" src="assets/logos/{LOGO[k]}" style="width:{h}px;height:{h}px">'
def badge(k, d, cls=""):
    return f'<div class="bdg {cls}" style="width:{d}px;height:{d}px">{logo(k, round(d * .64))}</div>'

J = []; SFX = []
def js(x): J.append(x)
def sfx(f, t, g=-8): SFX.append(dict(f=f, t=round(max(0, t), 3), g=g))
def fin(sel, t, d=.36, y=20, blur=8):
    js(f"tl.fromTo('{sel}',{{opacity:0,y:{y},filter:'blur({blur}px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:{d},ease:'power2.out',immediateRender:false}},{max(0, t):.3f});")
def fout(sel, t, d=.22):
    js(f"tl.to('{sel}',{{opacity:0,y:-12,filter:'blur(8px)',duration:{d},ease:'power2.inOut'}},{max(0, t):.3f});")
clamp = lambda x, lo, hi: max(lo, min(hi, x))

# ---------------------------------------------------------------- headlines (top band; at most 2 lines, plain ink, no boxes, no code words)
HEADS = []
def head(i, t_in, t_out, l1, l2="", logos=(), t2=None, size=92, extra=""):
    wl = len(logos) * 86
    fs = min(size, 900 / max((tw(l1) + wl * 100 / 84) / 100, tw(l2) / 100 if l2 else 0.01))
    lg = "".join(logo(k, round(fs * .86), "hlg") for k in logos)
    l2h = f'<div class="hl2" id="h{i}b">{l2}</div>' if l2 else ""
    top = 283 if l2 else 283 + max(0, (176 - fs) / 2 - 10)
    HEADS.append(f'<div class="hd" id="h{i}" style="top:{top:.0f}px;font-size:{fs:.1f}px;line-height:{fs * .98:.1f}px"><div class="hl1">{lg}<span>{l1}</span></div>{l2h}{extra}</div>')
    if t_in is not None:
        fin(f"#h{i}", t_in)
        if l2 and t2 is not None:
            js(f"tl.fromTo('#h{i}b',{{opacity:0,x:34}},{{opacity:1,x:0,duration:.3,ease:'power3.out',immediateRender:false}},{t2:.3f});")
    if t_out is not None: fout(f"#h{i}", t_out - .24)
tA2 = T0 + .82
tA3 = clamp(s(5), vP - .6, vP - .12)                        # the event headlines follow the race, the voice is told where to land (targets)
tA4 = clamp(s(6), vM - .7, vM - .12)
tA5 = clamp(s(7), vM + 1.0, vC - .9)
tA6 = clamp(s(8), vGm + .5, max(vGm + .5, vR0 - 1.2))
tS8 = W("send", 10); tS8 = tS8 if tS8 is not None else s(10) + .52 * (e(10) - s(10))
head(0, None, s(2) - .02, "EACH AI TAUGHT A CAR.", "ONE HITS THE WALL.")
head(11, s(2), s(3) - .02, "SAME JOB FOR ALL FIVE")
head(12, s(3), s(4) - .02, "EACH SETS ITS OWN RULES")
head(1, s(4), T0 - .04, "PICK ONE.", size=132)
HEADS.append('<div class="hd go" id="hgo"><div class="hl1"><span>GO!</span></div></div>')
js(f"tl.fromTo('#hgo',{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.3,ease:'power3.out',immediateRender:false}},{T0:.3f});")
js(f"tl.to('#hgo',{{opacity:0,scale:1.2,duration:.26,ease:'power2.in'}},{tA2 - .3:.3f});")
head(2, tA2, tA3, "TWO LAPS.", "HANDS OFF.")
head(3, tA3, tA4, "PERPLEXITY", "STOPS DEAD", logos=("perplexity",), t2=vP)
head(4, tA4, tA5, "META AI", "HITS THE WALL", logos=("meta",), t2=vM)
head(5, tA5, tA6, "NECK AND NECK", logos=("claude", "gemini"))
head(6, tA6, vR0 + .1, "CHATGPT", "ROLLS IN NEXT", logos=("chatgpt",))
head(7, vR0 + .12, vX, "WHO WON?", size=120)
head(8, vX, tK, "CLAUDE WINS", f"{GAP} s AHEAD OF GEMINI", logos=("claude",), t2=vXg)
head(9, tK, s(12) - .04, "SEND IT TO A FRIEND", "SEE WHO THEY PICK", t2=tS8)
head(10, s(12), tF + .04, "NEXT: A MAZE", size=120)
fin("#h0", tF + .06, .42)

# ---------------------------------------------------------------- markup: the world (ground, road, trails, cars, effects), drawn turned 90 degrees by render()
pts = lambda P: " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in P)
outer = "M" + " L".join(f"{p[0]:.1f} {p[1]:.1f}" for p in TR["rightEdge"]) + "Z"
inner = "M" + " L".join(f"{p[0]:.1f} {p[1]:.1f}" for p in TR["leftEdge"]) + "Z"
fl = TR["leftEdge"][0]; fr_ = TR["rightEdge"][0]            # the finish line runs between these two edge points
cheq = ""
for i in range(20):
    y0 = fl[1] + (fr_[1] - fl[1]) * i / 20; hh = (fr_[1] - fl[1]) / 20
    for q in range(2):
        if (i + q) % 2 == 0: cheq += f'<rect x="{fl[0] - 7 + 7 * q:.1f}" y="{y0:.1f}" width="7" height="{hh:.2f}" fill="{INK}"/>'
random.seed(5); tuft = ""
for _ in range(26):                                         # pencil tufts for the ground pattern (hand-drawn, not a flat fill)
    x, y = random.uniform(6, 150), random.uniform(6, 150); a_ = random.uniform(-.5, .5); l_ = random.uniform(7, 13)
    tuft += f'<path d="M{x:.1f} {y:.1f} l{math.sin(a_) * l_:.1f} {-math.cos(a_) * l_:.1f} M{x + 5:.1f} {y:.1f} l{math.sin(a_ + .5) * l_ * .8:.1f} {-math.cos(a_ + .5) * l_ * .8:.1f}"/>'
GDEF = f'<pattern id="PID" width="160" height="160" patternUnits="userSpaceOnUse" PT><rect width="160" height="160" fill="{GRASS}"/><g fill="none" stroke="#5d7a3c" stroke-opacity=".5" stroke-width="2.2" stroke-linecap="round">{tuft}</g></pattern>'
road = f'''<svg class="road" viewBox="0 0 950 808" width="950" height="808">
 <defs>{GDEF.replace("PID", "gr").replace("PT", 'patternTransform="rotate(90) scale(.62)"')}<filter id="wob" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="3.2"/></filter></defs>
 <rect x="-1400" y="-1400" width="3800" height="3800" fill="url(#gr)"/>
 <path d="{outer} {inner}" fill="{INK}" fill-rule="evenodd" transform="translate(-7 7)"/>
 <path d="{outer} {inner}" fill="{ROAD}" fill-rule="evenodd"/>
 <polyline points="{pts(CLN)} {CLN[0][0]},{CLN[0][1]}" fill="none" stroke="{INK}" stroke-opacity=".2" stroke-width="3" stroke-dasharray="16 18"/>
 <rect x="{fl[0] - 7:.1f}" y="{fl[1]:.1f}" width="14" height="{fr_[1] - fl[1]:.1f}" fill="#fff"/>{cheq}
 <g filter="url(#wob)" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"><path d="{outer}"/><path d="{inner}"/></g>
</svg>'''
trails = '<svg class="trs" viewBox="0 0 950 808" width="950" height="808">' + "".join(
    f'<path class="trl" d="{TRD[c]}" stroke="{COL[k]}" stroke-dasharray="{CLEN[c][STOP[k]] + 2:.1f}" stroke-dashoffset="{CLEN[c][STOP[k]] + 2:.1f}"/>' for c, k in enumerate(IDS)) + "</svg>"
rays = "".join(f'<path d="M{math.cos(i * math.pi / 8) * 62:.1f} {math.sin(i * math.pi / 8) * 62:.1f} L{math.cos(i * math.pi / 8) * (92 if i % 2 else 80):.1f} {math.sin(i * math.pi / 8) * (92 if i % 2 else 80):.1f}"/>' for i in range(16))
def bodyparts(fill):
    return f'''<rect x="-28" y="-23" width="15" height="9" rx="3" fill="{INK}"/><rect x="13" y="-23" width="15" height="9" rx="3" fill="{INK}"/>
 <rect x="-28" y="14" width="15" height="9" rx="3" fill="{INK}"/><rect x="13" y="14" width="15" height="9" rx="3" fill="{INK}"/>
 <rect x="-36" y="-17" width="72" height="34" rx="13" fill="{fill}" stroke="{INK}" stroke-width="3.5"/>
 <rect x="-39" y="-15" width="7" height="30" rx="2" fill="{INK}"/><path d="M30 -9 Q37 0 30 9" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'''
def car(c, k):
    ry = f'<svg class="rays" viewBox="-100 -100 200 200">{rays}</svg>' if k == "claude" else ""
    return f'''<div class="car" data-c="{c}" style="z-index:{10 - c}"><div class="cs">{ry}<div class="cb"><svg viewBox="-40 -24 80 48" width="80" height="48">
 {bodyparts(COL[k])}
</svg></div>{badge(k, 50, "bd")}</div></div>'''
random.seed(98)
PUFF = []                                                   # race dust: [race time, x, y, dx, dy, size]
for i in range(STOP["perplexity"] - 21, STOP["perplexity"] + 1, 3):       # Perplexity brakes to a stop
    x, y, a = FR["perplexity"][i][:3]
    PUFF.append([round(i / 60, 3), round(x - math.cos(a) * 16 + random.uniform(-6, 6), 1), round(y - math.sin(a) * 16 + random.uniform(-6, 6), 1),
                 round(-math.cos(a) * 14 + random.uniform(-8, 8), 1), round(-math.sin(a) * 14 + random.uniform(-8, 8), 1), round(random.uniform(13, 20), 1)])
mx, my, ma = FR["meta"][STOP["meta"]][:3]
NOSE = [round(mx + math.cos(ma) * 17, 1), round(my + math.sin(ma) * 17, 1)]
for i in range(9):                                          # Meta AI touches the wall: a bump
    an = ma + math.pi + random.uniform(-1.4, 1.4)
    PUFF.append([round(tM + .02 * i, 3), NOSE[0], NOSE[1], round(math.cos(an) * random.uniform(16, 34), 1), round(math.sin(an) * random.uniform(16, 34), 1), round(random.uniform(9, 15), 1)])
px_, py_ = FR["perplexity"][STOP["perplexity"]][:2]
fx = "".join('<div class="pf"></div>' for _ in range(len(PUFF) + 10))
star = "M0 -30 L7 -9 L27 -15 L13 2 L30 16 L8 12 L3 32 L-7 13 L-27 20 L-14 2 L-30 -12 L-9 -10Z"
qmark = '<svg class="mk qm" viewBox="-20 -30 40 60"><path d="M-10 -12 C-10 -28 12 -28 12 -12 C12 -2 1 -3 1 9" pathLength="1"/><circle cx="1" cy="21" r="3.6"/></svg>'
xmark = '<svg class="mk xm" viewBox="-20 -20 40 40"><path d="M-14 -14 L14 14 M14 -14 L-14 14" pathLength="1"/></svg>'
world = f'''{road}{trails}
<div class="fx">{fx}<svg class="star" viewBox="-34 -34 68 68"><path d="{star}"/></svg></div>
<div class="cars">{"".join(car(c, k) for c, k in enumerate(IDS))}</div>
<div class="mks">{qmark}{xmark}</div>'''

# ---------------------------------------------------------------- markup: the line-up scene (frame 0, premise, pick). Page coordinates.
REQ = "Teach this car to drive."
BFS = min(64, 100 * 590 / tw8(REQ))
lane = "".join(f'<path d="M{x} {BAND + 60} V1930"/>' for x in (255, 445, 635, 825))
sq = 18; lch = ""
for i in range(round(1000 / sq) + 1):
    for q in range(2):
        if (i + q) % 2 == 0: lch += f'<rect x="{40 + i * sq}" y="{BAND + 10 + q * sq}" width="{sq}" height="{sq}" fill="{INK}"/>'
check = '<path d="M-10 1 L-3 8 L11 -8" pathLength="1"/>'
sa = f'''<svg class="sag" viewBox="0 0 1080 1920" width="1080" height="1920">
 <defs>{GDEF.replace("PID", "gr2").replace("PT", "")}<filter id="wob2" x="-20%" y="-2%" width="140%" height="104%"><feTurbulence type="fractalNoise" baseFrequency=".02" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="5"/></filter></defs>
 <rect x="-40" y="{BAND - 10}" width="1160" height="1480" fill="url(#gr2)"/>
 <rect x="47" y="{BAND - 10}" width="1000" height="1480" fill="{INK}"/><rect x="40" y="{BAND - 10}" width="1000" height="1480" fill="{ROAD}"/>
 <g fill="none" stroke="{INK}" stroke-opacity=".2" stroke-width="5" stroke-dasharray="26 28">{lane}</g>
 <rect x="40" y="{BAND + 10}" width="1000" height="{2 * sq}" fill="#fff"/>{lch}
 <g filter="url(#wob2)" fill="none" stroke="{INK}" stroke-width="8"><path d="M40 {BAND - 10} V1940"/><path d="M1040 {BAND - 10} V1940"/></g>
</svg>'''
for c, k in enumerate(IDS):
    cx = CXS[c]
    sa += f'<div class="lpw" id="lpw{c}">' + "".join(f'<div class="lp" id="lp{c}{q}" style="left:{cx - 36 + 72 * q}px;top:{CARY + 128}px"></div>' for q in range(2)) + "</div>"
    sa += f'<svg class="lk" id="lk{c}" style="left:{cx - 20}px;top:{CARY + 136}px" viewBox="-20 0 40 44"><path d="M0 44 V8 M-9 18 L0 6 L9 18"/></svg>'
for c, k in enumerate(IDS):
    cx = CXS[c]
    sa += f'''<div class="lc" id="lc{c}" style="left:{cx}px;top:{CARY}px"><div class="lcb"><svg class="lb0" viewBox="-24 -40 48 80"><g transform="rotate(-90)">{bodyparts("#fbfbf8")}</g></svg><svg class="lb1" id="lb{c}" viewBox="-24 -40 48 80"><g transform="rotate(-90)">{bodyparts(COL[k])}</g></svg>{badge(k, 112, "lbd")}</div></div>'''
sa += f'''<div id="bub"><svg class="bcar" viewBox="-42 -26 84 52">{bodyparts("#fbfbf8")}</svg><div id="btx" style="font-size:{BFS:.1f}px;line-height:{BFS * 1.2:.1f}px">{REQ}</div>
 <svg class="btail" data-decor viewBox="0 0 60 44"><path d="M4 0 C10 22 30 36 56 40 C36 40 18 30 4 0Z" fill="#fff" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/><rect x="0" y="-6" width="40" height="9" fill="#fff"/></svg></div>'''
sa += "".join(f'<div class="nt" id="nt{c}"><i></i><i></i></div>' for c in range(5))

RULES3 = ["Stay in the middle of the road", "Slow down for bends", "Steer away from walls"]   # plain-words summary of what all five answers do (coordinator's reading of the answers)
sa += '<div id="rules"><div class="rt">RULES</div><div class="rs">plain-words summary</div>' + "".join(f'<div class="rl" id="rl{q}"><b></b>{x}</div>' for q, x in enumerate(RULES3)) + "</div>"
sa += "".join(f'<div class="mr" id="mr{c}" style="left:{CXS[c] - 62}px;top:{CHY - 112}px"><span>RULES</span><i></i><i></i><i></i></div>' for c in range(5))

# ---------------------------------------------------------------- markup: chips (the AIs; later the status strip: fixed order, status only), maze, result card
strip = '<div id="strip">'
for c, k in enumerate(IDS):
    mark = '<path d="M-9 -9 C-9 -22 11 -22 11 -9 C11 0 1 0 1 8 M1 17 V17.5" pathLength="1"/>' if k == "perplexity" else '<path d="M-13 -13 L13 13 M13 -13 L-13 13" pathLength="1"/>' if k == "meta" else ""
    strip += f'''<div class="sl" id="sl{c}" style="left:{CXS[c] - CHD / 2:.0f}px;top:{CHY - CHD / 2:.0f}px"><i class="ring" style="border-color:{COL[k]}"></i>{badge(k, CHD, "tb")}{f'<svg class="tm" viewBox="-22 -24 44 48">{mark}</svg>' if mark else ""}
 <div class="dots"><i class="d1"></i><i class="d2"></i></div><div class="tk" id="tk{c}"><i></i><i></i><i></i></div><svg class="ck" id="ck{c}" viewBox="-20 -20 40 40"><circle r="17"/>{check}</svg></div>'''
strip += "</div>"
# maze teaser: seeded depth-first maze, drawn as one stroke
random.seed(99); MN, MC = 5, 44
seen = {(0, 0)}; open_ = set(); stack = [(0, 0)]
while stack:
    cx_, cy_ = stack[-1]
    nb = [(cx_ + dx, cy_ + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= cx_ + dx < MN and 0 <= cy_ + dy < MN and (cx_ + dx, cy_ + dy) not in seen]
    if nb:
        n_ = random.choice(nb); open_.add(frozenset(((cx_, cy_), n_))); seen.add(n_); stack.append(n_)
    else: stack.pop()
md = f"M0 0 H{MN * MC} V{MN * MC} H{MC} M0 {MN * MC} V0"       # outer wall, entrance bottom-left
for x in range(MN):
    for y in range(MN):
        if x + 1 < MN and frozenset(((x, y), (x + 1, y))) not in open_: md += f" M{(x + 1) * MC} {y * MC} V{(y + 1) * MC}"
        if y + 1 < MN and frozenset(((x, y), (x, y + 1))) not in open_: md += f" M{x * MC} {(y + 1) * MC} H{(x + 1) * MC}"
# a wandering line from the entrance (bottom-left cell) along the longest branch found: "who gets lost"
seen = {(0, MN - 1)}; stack = [(0, MN - 1)]; best = [(0, MN - 1)]
adj = lambda a_, b_: frozenset((a_, b_)) in open_
while stack:
    c_ = stack[-1]
    nb = [(c_[0] + dx, c_[1] + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (c_[0] + dx, c_[1] + dy) not in seen and adj(c_, (c_[0] + dx, c_[1] + dy))]
    if nb:
        stack.append(nb[0]); seen.add(nb[0])
        if len(stack) > len(best): best = list(stack)
    else: stack.pop()
wd = f"M{MC / 2} {MN * MC + 26} " + " ".join(f"L{x * MC + MC / 2} {y * MC + MC / 2}" for x, y in best[:12])
maze = f'<div id="msheet"><svg viewBox="-8 -8 {MN * MC + 16} {MN * MC + 44}"><path id="mzw" d="{md}" pathLength="1"/><path id="mzp" d="{wd}" pathLength="1"/></svg><div id="mzq">?</div></div>'
ROWS = [("claude", "1", f"{RES['claude']['timeS']:.2f} s"), ("gemini", "2", f"{RES['gemini']['timeS']:.2f} s"), ("chatgpt", "3", f"{RES['chatgpt']['timeS']:.2f} s"),
        ("meta", "&ndash;", "touched the wall"), ("perplexity", "&ndash;", "stuck in the bend")]
card = '<div id="card"><div class="tape t1" data-decor></div><div class="tape t2" data-decor></div><div class="ct">AI RACE #1 &middot; 2 LAPS</div>'
for i, (k, pl, res) in enumerate(ROWS):
    card += f'<div class="cr" id="cr{i}" style="top:{112 + i * 100}px"><span class="cp">{pl}</span>{badge(k, 78)}<span class="cn">{NAME[k]}</span><span class="cv">{res}</span>{"<i></i>" if i == 0 else ""}</div>'
card += '<div class="cl" id="cl">rules locked first, one try each</div></div>'
markup = f'''
<div class="bgw" data-decor></div>
<div id="cam">
 <div id="vp"><div id="world" class="world">{world}</div><div id="flash"></div><div id="dip"></div>{maze}</div>
 <div id="saw"><div id="sa">{sa}</div></div>
 <svg id="edge" data-decor viewBox="0 0 1120 20" width="1120" height="20"><path d="M0 10 H1120" fill="none" stroke="{INK}" stroke-width="7" filter="url(#wob)"/></svg>
 <div id="slow"><b></b>SLOW MOTION REPLAY</div>
 {strip}
 {"".join(HEADS)}
 {card}
</div>'''

CSS = '''
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;color:INK}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}
.bgw{position:absolute;left:-20px;top:-20px;width:1120px;height:1960px;background:#ecebe5 url(assets/bg.jpg);background-size:1120px 1960px}
#cam{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 844px}
#vp,#saw{position:absolute;left:VPLpx;top:VPTpx;width:VPWpx;height:VPHpx;overflow:hidden}
#vp{background:GRASS;z-index:1} #saw{z-index:2}
#sa{position:absolute;left:20px;top:-BANDpx;width:1080px;height:1920px;transform-origin:540px 760px}
#edge{position:absolute;left:-20px;top:460px;z-index:3;overflow:visible}
.world{position:absolute;left:0;top:0;width:950px;height:808px;transform-origin:0 0;will-change:transform}
#strip{position:absolute;left:0;top:0;width:0;height:0;z-index:4}
.hd{z-index:5} #card{z-index:6} #slow{z-index:3}
.world svg.road,.world svg.trs{position:absolute;left:0;top:0;overflow:visible}
.trl{fill:none;stroke-width:6;stroke-linecap:round;stroke-linejoin:round;opacity:0}
.cars,.fx,.mks{position:absolute;left:0;top:0;width:0;height:0}
.car{position:absolute;left:0;top:0;width:0;height:0;will-change:transform}
.cs{position:absolute;left:0;top:0;width:0;height:0}
.cb{position:absolute;left:-40px;top:-24px;width:80px;height:48px}
.cb svg{display:block}
.bdg{position:relative;border-radius:50%;background:#fff;border:3.5px solid INK;display:flex;align-items:center;justify-content:center;flex:none}
.bdg .lg{display:block}
.pxl{display:block;overflow:hidden;flex:none} .pxl img{display:block;max-width:none}
.car .bd{position:absolute;left:-25px;top:-25px}
.rays{position:absolute;left:-100px;top:-100px;width:200px;height:200px;overflow:visible;opacity:0} .rays path{stroke:#D97757;stroke-width:8;stroke-linecap:round}
.pf{position:absolute;left:0;top:0;width:20px;height:20px;margin:-10px 0 0 -10px;border-radius:50%;background:#fbf8ee;border:2px solid INK;opacity:0}
.star{position:absolute;left:0;top:0;width:68px;height:68px;margin:-34px 0 0 -34px;overflow:visible;opacity:0}
.star path{fill:#FFD23F;stroke:INK;stroke-width:4;stroke-linejoin:round}
.mk{position:absolute;left:0;top:0;overflow:visible;opacity:0}
.mk path{fill:none;stroke:RED;stroke-width:7;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1}
.mk circle{fill:RED}
.qm{width:40px;height:60px;margin:-30px 0 0 -20px} .xm{width:40px;height:40px;margin:-20px 0 0 -20px}
#flash,#dip{position:absolute;left:0;top:0;width:VPWpx;height:VPHpx;opacity:0;pointer-events:none}
#flash{background:#fff} #dip{background:#ecebe5 url(assets/bg.jpg);background-size:1120px 1960px;background-position:0 -BANDpx}
#slow{position:absolute;left:84px;top:492px;font-weight:900;font-size:30px;line-height:36px;letter-spacing:-.01em;color:RED;white-space:nowrap;opacity:0;display:flex;align-items:center;gap:9px;
 text-shadow:2px 2px 0 #fbfbf8,-2px 2px 0 #fbfbf8,2px -2px 0 #fbfbf8,-2px -2px 0 #fbfbf8,0 3px 0 #fbfbf8,3px 0 0 #fbfbf8,-3px 0 0 #fbfbf8,0 -3px 0 #fbfbf8}
#slow b{display:block;width:17px;height:17px;border-radius:50%;background:RED;border:2px solid #fbfbf8}
.sag{position:absolute;left:0;top:0;overflow:visible}
.lc{position:absolute;width:0;height:0}
.lcb{position:absolute;left:-75px;top:-125px;width:150px;height:250px}
.lcb svg{position:absolute;left:0;top:0;width:150px;height:250px;overflow:visible}
.lcb .lbd{position:absolute;left:19px;top:69px;border-width:5px}
.lp{position:absolute;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;background:#fbf8ee;border:3px solid INK;opacity:0}
.lk{position:absolute;width:40px;height:44px;overflow:visible} .lk path{fill:none;stroke:INK;stroke-width:5;stroke-linecap:round;stroke-linejoin:round}
#bub{position:absolute;left:120px;top:1052px;width:840px;height:172px;background:#fff;border:6px solid INK;border-radius:50px;box-shadow:9px 9px 0 INK;display:flex;align-items:center;justify-content:center;gap:26px;transform-origin:50% 60%}
.bcar{width:132px;height:82px;flex:none;overflow:visible}
#btx{font-weight:800;letter-spacing:-.01em;white-space:nowrap}
.btail{position:absolute;right:46px;bottom:-42px;width:60px;height:44px;overflow:visible}
.nt{position:absolute;left:506px;top:1010px;width:68px;height:50px;background:#fff;border:4px solid INK;border-radius:14px;opacity:0;padding:10px 10px 0}
.nt i{display:block;height:5px;border-radius:3px;background:INK;margin-bottom:8px} .nt i+i{width:60%}
#rules{position:absolute;left:120px;top:1000px;width:840px;height:232px;background:PAPER;border:6px solid INK;border-radius:10px;box-shadow:9px 9px 0 INK;opacity:0;padding:16px 34px 0;transform-origin:50% 0}
.rt{display:inline-block;font-weight:900;font-size:46px;line-height:50px;letter-spacing:-.02em}
.rs{position:absolute;right:30px;top:28px;font-weight:500;font-size:24px;line-height:28px;opacity:.7}
.rl{opacity:0;font-weight:800;font-size:40px;line-height:50px;letter-spacing:-.01em;white-space:nowrap;display:flex;align-items:center;gap:16px}
.rl b{display:block;width:16px;height:16px;border-radius:50%;background:INK;flex:none}
.mr{position:absolute;width:124px;height:104px;background:PAPER;border:4px solid INK;border-radius:8px;box-shadow:5px 5px 0 INK;opacity:0;padding:8px 12px 0;transform-origin:50% 100%;z-index:3}
.mr span{display:block;font-weight:900;font-size:22px;line-height:24px;letter-spacing:-.01em;margin-bottom:7px}
.mr i{display:block;height:6px;border-radius:3px;background:INK;margin-bottom:9px} .mr i:nth-child(3){width:72%} .mr i:nth-child(4){width:86%}
.sl{position:absolute;width:100px;height:100px;will-change:transform}
.sl .tb{position:absolute;left:0;top:0;border-width:5px;box-shadow:5px 5px 0 INK}
.ring{position:absolute;left:-13px;top:-13px;width:126px;height:126px;border-radius:50%;border:8px solid INK;opacity:0}
.dots{position:absolute;left:23px;top:108px;display:flex;gap:10px;opacity:0} .dots i{display:block;width:21px;height:21px;border-radius:50%;border:4px solid INK;background:PAPER}
.tm{position:absolute;left:4px;top:0;width:92px;height:100px;overflow:visible;opacity:0}
.tm path{fill:none;stroke:RED;stroke-width:8;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1}
.tk{position:absolute;left:52px;top:-34px;width:74px;height:40px;border-radius:20px;background:#fff;border:4px solid INK;display:flex;align-items:center;justify-content:center;gap:7px;opacity:0;transform-origin:20% 100%}
.tk i{display:block;width:10px;height:10px;border-radius:50%;background:INK}
.ck{position:absolute;left:62px;top:-22px;width:52px;height:52px;overflow:visible;transform-origin:50% 50%}
.ck circle{fill:#27A35B;stroke:INK;stroke-width:3.5} .ck path{fill:none;stroke:#fff;stroke-width:5.5;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:0}
.hd{position:absolute;left:65px;top:283px;font-weight:900;letter-spacing:-.03em;white-space:nowrap;opacity:0;transform-origin:0 50%}
#h0{opacity:1}
.hl1{display:flex;align-items:center} .hlg{margin-right:.16em;flex:none} .hl2{display:block}
.hd.go{font-size:170px;line-height:170px;top:286px}
#h8 .hl2{font-size:.62em;line-height:1.3em;letter-spacing:-.02em}
.tape{position:absolute;width:130px;height:40px;background:rgba(232,221,186,.86);border:1px solid rgba(0,0,0,.14);z-index:3}
.tape.t1{right:-34px;top:-12px;transform:rotate(34deg)} .tape.t2{left:-34px;bottom:-6px;transform:rotate(34deg)}
#msheet{position:absolute;left:0;top:0;width:VPWpx;height:VPHpx;opacity:0;background:#ecebe5 url(assets/bg.jpg);background-size:1120px 1960px;background-position:0 -BANDpx}
#msheet svg{position:absolute;left:150px;top:34px;width:640px;height:716px;overflow:visible}
#mzw{fill:none;stroke:INK;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1}
#mzp{fill:none;stroke:RED;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1}
#mzq{position:absolute;left:806px;top:60px;font-weight:900;font-size:280px;line-height:290px;color:RED;opacity:0;transform-origin:50% 60%}
#card{position:absolute;left:78px;top:490px;width:916px;height:738px;background:PAPER;border:6px solid INK;border-radius:10px;box-shadow:14px 14px 0 INK;opacity:0;transform-origin:50% 0%}
.ct{position:absolute;left:38px;top:28px;font-weight:900;font-size:56px;line-height:64px;letter-spacing:-.03em;white-space:nowrap}
.cr{position:absolute;left:38px;right:38px;height:94px;display:flex;align-items:center;opacity:0;border-top:4px solid rgba(15,15,15,.14)}
.cp{width:56px;font-weight:900;font-size:54px;line-height:60px;text-align:center;margin-right:14px}
.cn{font-weight:900;font-size:52px;line-height:60px;letter-spacing:-.03em;margin-left:20px;white-space:nowrap}
.cv{margin-left:auto;font-weight:800;font-size:39px;line-height:60px;letter-spacing:-.01em;white-space:nowrap}
.cr i{position:absolute;left:0;right:0;bottom:2px;height:9px;border-radius:5px;background:#D97757;transform-origin:0 50%;transform:scaleX(0)}
.cl{position:absolute;left:40px;top:640px;font-weight:800;font-size:38px;line-height:46px;letter-spacing:-.01em;white-space:nowrap;opacity:0}
.cf{position:absolute;left:40px;top:672px;font-weight:800;font-size:36px;line-height:42px;white-space:nowrap;opacity:0}
.cf i{position:absolute;left:0;right:0;bottom:-7px;height:6px;border-radius:3px;background:INK;transform-origin:0 50%;transform:scaleX(0)}
'''
for a_, b_ in (("VPL", VPL), ("VPT", VPT), ("VPW", VPW), ("VPH", VPH), ("BAND", BAND), ("GRASS", GRASS), ("INK", INK), ("PAPER", PAPER), ("RED", RED)):
    CSS = CSS.replace(a_, str(b_))

# ---------------------------------------------------------------- timeline (GSAP: text, line-up, chips, cards; cars and camera are driven by render())
js(f"tl.fromTo('#cam',{{scale:1,rotation:0}},{{scale:1.012,rotation:.2,duration:{D / 4:.3f},ease:'sine.inOut',yoyo:true,repeat:3}},0);")
js(f"tl.fromTo('.bgw',{{x:0,y:0}},{{x:-14,y:-12,duration:{D / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},0);")
# beat 1: the hook over the finished picture (request, five AIs, five cars). "ONE HITS THE WALL" breathes on the word
tw_ = W("wall", 1); tw_ = tw_ if tw_ is not None else s(1) + .82 * (e(1) - s(1))
js(f"tl.fromTo('#h0 .hl2',{{scale:1}},{{scale:1.03,transformOrigin:'0 50%',duration:.22,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tw_:.3f});")
for c in range(5):                                           # engines idle: exhaust puffs and a small rock, the whole time the line-up is on
    for q in range(2):
        js(f"tl.fromTo('#lp{c}{q}',{{y:0,x:0,scale:.3,opacity:.9}},{{y:64,x:{-8 + 16 * q},scale:1.15,opacity:0,duration:.6,ease:'sine.out',repeat:{int(D / .6) + 1},immediateRender:false}},{.02 + .11 * c + .3 * q:.3f});")
    js(f"tl.fromTo('#lc{c} .lcb',{{y:0}},{{y:-7,duration:{.34 + .03 * c:.2f},ease:'sine.inOut',yoyo:true,repeat:{int(D / .36) + 1}}},{.05 * c:.2f});")
js(f"tl.fromTo('#bub',{{y:0,rotation:0}},{{y:-8,rotation:-.6,duration:{max(.5, (s(2) - .1) / 2):.3f},ease:'sine.inOut',yoyo:true,repeat:1}},0);")
sfx("subhit.ogg", .05, -6); sfx("impactsoft.ogg", tw_, -9)
# beat 2: the PROCESS, in pictures. The cars go blank; the request is typed; one note flies to each AI; each thinks, ticks; its car gets colour and logo
a2 = s(2); f2 = clamp((e(2) - s(2)) / 2.5, .75, 1.3)
js(f"tl.to('.lb1',{{opacity:0,duration:.2,ease:'sine.inOut'}},{a2 - .1:.3f});")
js(f"tl.to('.lbd',{{scale:0,duration:.2,ease:'power2.in'}},{a2 - .1:.3f});")
js(f"tl.to('.lpw',{{opacity:0,duration:.2}},{a2 - .1:.3f});")
js(f"tl.to('.lk',{{opacity:0,duration:.2}},{a2 - .1:.3f});")
js(f"tl.to('.ck',{{scale:0,duration:.2,ease:'power2.in'}},{a2 - .1:.3f});")
js(f"tl.fromTo('#bub',{{scale:.82}},{{scale:1,duration:.4,ease:'power3.out',immediateRender:false}},{a2:.3f});")
js(f"tl.fromTo('#btx',{{clipPath:'inset(0 100% 0 0)'}},{{clipPath:'inset(0 0% 0 0)',duration:{.5 * f2:.3f},ease:'sine.inOut',immediateRender:false}},{a2:.3f});")
sfx("pop_a.ogg", a2, -9)
tN = a2 + .52 * f2; ALIVE = []
for c in range(5):
    t0_ = tN + .055 * c; dx = CXS[c] - 540; dy = (CHY + 30) - 1035
    js(f"tl.fromTo('#nt{c}',{{opacity:0,x:0,y:0,scale:.6,rotation:0}},{{opacity:1,scale:1,duration:.1,ease:'sine.out',immediateRender:false}},{t0_:.3f});")
    js(f"tl.to('#nt{c}',{{x:{dx},duration:.4,ease:'sine.inOut'}},{t0_:.3f});")
    js(f"tl.to('#nt{c}',{{y:{dy},rotation:{dx / 30:.1f},duration:.4,ease:'power2.out'}},{t0_:.3f});")
    ta = t0_ + .38
    js(f"tl.to('#nt{c}',{{opacity:0,scale:.3,y:{dy - 40},duration:.14,ease:'sine.in'}},{ta:.3f});")
    js(f"tl.fromTo('#sl{c}',{{y:0}},{{y:-10,duration:.15,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{ta + .05:.3f});")
    js(f"tl.fromTo('#tk{c}',{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.18,ease:'power3.out',immediateRender:false}},{ta + .06:.3f});")
    th = .62 * f2 + .06 * c                                   # each AI takes its own time
    for q in range(3):
        js(f"tl.fromTo('#tk{c} i:nth-child({q + 1})',{{y:0}},{{y:-9,duration:.14,ease:'sine.inOut',yoyo:true,repeat:{max(1, 2 * round(th / .3)) - 1},immediateRender:false}},{ta + .1 + .07 * q:.3f});")
    tc = ta + .06 + th
    js(f"tl.to('#tk{c}',{{opacity:0,scale:.5,duration:.14,ease:'sine.in'}},{tc:.3f});")
    js(f"tl.to('#ck{c}',{{scale:1,duration:.28,ease:'back.out(2)'}},{tc + .06:.3f});")
    js(f"tl.fromTo('#ck{c} path',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.22,ease:'power2.out',immediateRender:false}},{tc + .12:.3f});")
    sfx("tick.ogg", tc + .06, -11)
sfx("whoosh_b.ogg", tN, -11)
# beat 3: WHAT each AI wrote. The request leaves; one big card shows the rules in plain words; a small copy pops out of
# every AI and slides into its car, which gets its colour and logo
a3 = s(3); f3 = clamp((e(3) - s(3)) / 2.0, .8, 1.3)
js(f"tl.to('#bub',{{opacity:0,y:40,scale:.9,duration:.24,ease:'power2.in'}},{a3 - .3:.3f});")
js(f"tl.fromTo('#rules',{{opacity:0,y:60,rotation:2}},{{opacity:1,y:0,rotation:-.6,duration:.42,ease:'power3.out',immediateRender:false}},{a3 - .04:.3f});")
for q in range(3):
    js(f"tl.fromTo('#rl{q}',{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.3,ease:'power3.out',immediateRender:false}},{a3 + .16 + .17 * q * f3:.3f});")
    sfx("pop_a.ogg" if q % 2 == 0 else "pop_b.ogg", a3 + .16 + .17 * q * f3, -11)
js(f"tl.to('#rules',{{rotation:.5,y:-6,duration:{max(.4, (s(4) - a3 - .6) / 2):.3f},ease:'sine.inOut',yoyo:true,repeat:1}},{a3 + .44:.3f});")
sfx("whoosh_b.ogg", a3, -11)
for c in range(5):
    tm = a3 + .14 + .06 * c
    js(f"tl.fromTo('#mr{c}',{{opacity:0,scale:.2,y:60,rotation:0}},{{opacity:1,scale:1,y:0,rotation:{(-3, 2, -2, 3, -1)[c]},duration:.34,ease:'back.out(1.5)',immediateRender:false}},{tm:.3f});")
    ts = a3 + (.92 + .08 * c) * f3
    js(f"tl.to('#mr{c}',{{y:{CARY - (CHY - 60)},scale:.5,rotation:0,duration:.32,ease:'power2.inOut'}},{ts:.3f});")
    js(f"tl.to('#mr{c}',{{opacity:0,duration:.12,ease:'sine.in'}},{ts + .24:.3f});")
    tv = ts + .26; ALIVE.append(round(tv, 3))
    js(f"tl.to('#lk{c}',{{opacity:1,duration:.2}},{tv - .08:.3f});")
    js(f"tl.to('#lb{c}',{{opacity:1,duration:.26,ease:'sine.out'}},{tv:.3f});")
    js(f"tl.to('#lc{c} .lbd',{{scale:1,duration:.34,ease:'back.out(1.7)'}},{tv:.3f});")
    js(f"tl.fromTo('#lc{c}',{{y:0,scale:1}},{{y:-20,scale:1.07,duration:.2,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tv:.3f});")
    js(f"tl.to('#lpw{c}',{{opacity:1,duration:.2}},{tv + .05:.3f});")
    sfx("pop_a.ogg" if c % 2 == 0 else "pop_b.ogg", tv, -10)
# beat 4: "Pick one": the rules card leaves, the five logos light up as choices, one after another, and stay lit until Go
js(f"tl.to('#rules',{{opacity:0,y:40,scale:.94,duration:.28,ease:'power2.in'}},{s(4) - .16:.3f});")
tPk = s(4) - .08; stepk = min(.13, max(.06, (T0 - .3 - tPk) / 5))
PICK = [round(tPk + c * stepk, 3) for c in range(5)]
for c in range(5):
    js(f"tl.fromTo('#sl{c}',{{y:0}},{{y:-18,duration:.2,ease:'power2.out',yoyo:true,repeat:1,immediateRender:false}},{PICK[c]:.3f});")
    js(f"tl.fromTo('#sl{c} .ring',{{opacity:0,scale:.7}},{{opacity:1,scale:1,duration:.26,ease:'power3.out',immediateRender:false}},{PICK[c]:.3f});")
    js(f"tl.fromTo('#lc{c}',{{y:0}},{{y:-16,duration:.2,ease:'power2.out',yoyo:true,repeat:1,immediateRender:false}},{PICK[c] + .04:.3f});")
    sfx("pop_a.ogg" if c % 2 == 0 else "pop_b.ogg", PICK[c], -10)
tPe = PICK[4] + .3
if T0 - tPe > .3:
    js(f"tl.to('.ring',{{scale:1.1,duration:{(T0 - tPe) / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},{tPe:.3f});")
js(f"tl.to('.ring',{{opacity:0,scale:1.25,duration:.4,ease:'power2.out'}},{T0 + .05:.3f});")
# Go: the camera dives through the line-up into the real track; the chips slide down and become the status strip
js(f"tl.to('.lc',{{y:-150,duration:.36,ease:'power2.in'}},{T0 - .05:.3f});")
js(f"tl.to('#sa',{{opacity:0,scale:1.45,filter:'blur(9px)',duration:.38,ease:'power2.in'}},{T0 - .05:.3f});")
for c in range(5): js(f"tl.to('#sl{c}',{{x:{STRIPX - CXS[c]},y:{STRIPY0 + STRIPDY * c - CHY},scale:{STRIPS},duration:.62,ease:'power3.inOut'}},{T0 - .05 + .03 * c:.3f});")
js(f"tl.to('.ck',{{opacity:0,scale:.4,duration:.25,ease:'sine.in'}},{T0 - .05:.3f});")
js(f"tl.to('.dots',{{opacity:1,duration:.3,ease:'sine.out'}},{T0 + .3:.3f});")
js(f"tl.set('.lc',{{y:0}},{T0 + .8:.3f});"); js(f"tl.set('#bub',{{opacity:1,y:0,scale:1}},{T0 + .8:.3f});")
sfx("whoosh_a.ogg", T0 - .03, -6)
# race events (live, 1x)
sfx("toggle.ogg", vP - .25, -9); sfx("impactpunch.ogg", vM, -4); sfx("click_a.ogg", vC, -10); sfx("click_a.ogg", vGm, -10)
if vCh < vRm: sfx("click_b.ogg", vCh, -9)
# replay: a soft dip hides the jump of the clock; the label is small and short (the replay itself runs on)
js(f"tl.fromTo('#dip',{{opacity:0}},{{opacity:1,duration:.14,ease:'sine.in',immediateRender:false}},{vR0:.3f});")
js(f"tl.to('#dip',{{opacity:0,duration:.24,ease:'sine.out'}},{vRm + .03:.3f});")
js(f"tl.fromTo('#slow',{{opacity:0,x:-16}},{{opacity:1,x:0,duration:.2,ease:'power2.out',immediateRender:false}},{vRm:.3f});")
js(f"tl.fromTo('#slow b',{{opacity:1}},{{opacity:.25,duration:.3,ease:'sine.inOut',yoyo:true,repeat:3,immediateRender:false}},{vRm:.3f});")
tSO = min(vRm + 1.5, tK - .14)
js(f"tl.to('#slow',{{opacity:0,duration:.2,ease:'sine.in'}},{tSO:.3f});")
sfx("whoosh_c.ogg", vR0, -11); sfx("riser.ogg", vRm, -12); sfx("ding.ogg", vX, -6); sfx("impactsoft.ogg", vX, -8); sfx("click_a.ogg", vXg, -9)
# winner: only now. Claude's logo in the strip gets its ring
ci = IDS.index("claude")
js(f"tl.fromTo('#sl{ci} .ring',{{opacity:0,scale:.6}},{{opacity:1,scale:1.06,duration:.35,ease:'power3.out',immediateRender:false}},{vX:.3f});")
js(f"tl.fromTo('#h8 .hl1',{{scale:1}},{{scale:1.06,transformOrigin:'0 50%',duration:.24,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{vX + .36:.3f});")
# result card (the saveable card): rows land slowest result first, the winner last
js(f"tl.fromTo('#card',{{opacity:0,y:90,rotation:3,scale:1}},{{opacity:1,y:0,rotation:-1,duration:.5,ease:'power3.out',immediateRender:false}},{tK + .03:.3f});")
sfx("whoosh_b.ogg", tK, -10)
for q, i in enumerate((4, 3, 2, 1, 0)):
    t = tK + .28 + q * .16 + (.12 if i == 0 else 0)
    js(f"tl.fromTo('#cr{i}',{{opacity:0,x:-46}},{{opacity:1,x:0,duration:.36,ease:'power3.out',immediateRender:false}},{t:.3f});")
    sfx("pop_a.ogg" if q % 2 == 0 else "pop_b.ogg", t, -10)
tU = tK + 1.25
js(f"tl.to('#cr0 i',{{scaleX:1,duration:.5,ease:'power2.inOut'}},{tU:.3f});")
js(f"tl.fromTo('#cr0 .bdg',{{scale:1}},{{scale:1.14,duration:.3,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tU:.3f});")
fin("#cl", tU + .25, .4, 14, 6)
hold = max(.8, s(12) - tK - .7)
js(f"tl.to('#card',{{rotation:.6,y:-8,duration:{hold / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},{tK + .55:.3f});")
for q, i in enumerate((3, 4, 2, 1)):                         # a slow wave keeps the list alive while it is read
    js(f"tl.fromTo('#cr{i} .bdg',{{rotation:0}},{{rotation:{-10 if q % 2 else 10},duration:.28,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tU + .7 + q * .3:.3f});")
for q, i in enumerate((0, 1, 2)):
    js(f"tl.fromTo('#cr{i} .cv',{{scale:1}},{{scale:1.1,transformOrigin:'100% 50%',duration:.24,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{s(11) + .95 + q * .2:.3f});")
# last line: the maze sheet covers the road, then the frame-0 picture (the line-up) returns
tG = s(12) + .15
js(f"tl.fromTo('#msheet',{{opacity:0}},{{opacity:1,duration:.22,ease:'sine.inOut',immediateRender:false}},{s(12) - .36:.3f});")
js(f"tl.to('#sl{ci} .ring',{{opacity:0,duration:.2,ease:'sine.inOut'}},{s(12) - .36:.3f});")
js(f"tl.to('.sl',{{opacity:0,duration:.22,ease:'sine.inOut'}},{s(12) - .36:.3f});")
js(f"tl.set('.sl',{{x:0,y:0,scale:1}},{s(12) + .2:.3f});"); js(f"tl.set('.dots',{{opacity:0}},{s(12) + .2:.3f});"); js(f"tl.set('.ck',{{opacity:1,scale:1}},{s(12) + .2:.3f});")
js(f"tl.to('#card',{{opacity:0,scale:.82,y:-50,rotation:-4,duration:.36,ease:'power2.in'}},{s(12) - .12:.3f});")
sfx("whoosh_c.ogg", s(12) - .12, -10)
mzD = tF - s(12)
js(f"tl.to('#mzw',{{strokeDashoffset:0,duration:{min(1.2, mzD * .45):.3f},ease:'power2.inOut'}},{s(12) - .2:.3f});")
js(f"tl.to('#mzp',{{strokeDashoffset:0,duration:{max(.5, mzD * .5):.3f},ease:'sine.inOut'}},{s(12) + min(1.2, mzD * .45):.3f});")
js(f"tl.fromTo('#msheet svg',{{rotation:-2,scale:.96}},{{rotation:1.5,scale:1,duration:{mzD:.3f},ease:'sine.inOut',immediateRender:false}},{s(12) - .1:.3f});")
tq = W("lost", 12); tq = tq if tq is not None else s(12) + .86 * (e(12) - s(12))
tq = min(tq, tF - .45)
js(f"tl.fromTo('#mzq',{{opacity:0,scale:.5,rotation:-14}},{{opacity:1,scale:1,rotation:8,duration:.35,ease:'power3.out',immediateRender:false}},{tq:.3f});")
js(f"tl.fromTo('#sa',{{opacity:0,scale:1.06,filter:'blur(8px)'}},{{opacity:1,scale:1,filter:'blur(0px)',duration:.42,ease:'power2.out',immediateRender:false}},{tF:.3f});")
js(f"tl.fromTo('.sl',{{opacity:0}},{{opacity:1,duration:.42,ease:'power2.out',immediateRender:false}},{tF:.3f});")
sfx("tick.ogg", s(12) + .1, -10); sfx("whoosh_c.ogg", tF, -12)

# ---------------------------------------------------------------- render(): the race and the camera, driven by the timeline clock
DATA = dict(T0=T0, D=D, NF=NF, RT=RT, X=X, Y=Y, A=A, CL=CLEN, TL=[CLEN[c][STOP[k]] + 2 for c, k in enumerate(IDS)],
            GRID=GRID, SLOT={str(k): v for k, v in SLOT.items()}, LAPF=[LAPF[k] for k in IDS], STOP=[STOP[k] for k in IDS],
            PUFF=PUFF, NOSE=NOSE, tP=tP, tM=tM, iP=IDS.index("perplexity"), iM=IDS.index("meta"), iC=ci,
            vRm=round(vRm, 3), vJ=round(vJ, 3), vX=round(vX, 3), tG=round(tG, 3), PCX=PCX, PCY=PCY, ZG=ZG,
            CX=CX, CY=CY, CZ=CZ, CK=CK, GC=GC, FC=FC, QM=[round(px_ + 6, 1), round(py_ + 62, 1)], XM=[round(NOSE[0] + 4, 1), round(NOSE[1] - 50, 1)])
RJS = r'''
const Dt=__DATA__;
const ez=p=>{p=p<0?0:p>1?1:p;return p*p*(3-2*p)}, lerp=(a,b,t)=>a+(b-a)*t, bump=p=>p>0&&p<1?Math.sin(Math.PI*p):0;
const angd=(to,from)=>{let d=(to-from)%(2*Math.PI);if(d>Math.PI)d-=2*Math.PI;if(d<-Math.PI)d+=2*Math.PI;return d};
function Rv(v){const i=Math.max(0,v*60),k=Math.min(Dt.RT.length-2,Math.floor(i)),a=Dt.RT[k],b=Dt.RT[k+1];return Math.abs(b-a)>.1?a:a+(b-a)*Math.min(1,i-k)}
const world=document.querySelector('#world');
const cars=[...world.querySelectorAll('.car')].map(el=>({el,cs:el.querySelector('.cs'),cb:el.querySelector('.cb'),bd:el.querySelector('.bd'),ry:el.querySelector('.rays')}));
const trs=[...world.querySelectorAll('.trl')], pfs=[...world.querySelectorAll('.pf')], star=world.querySelector('.star');
const qm=world.querySelector('.qm'), xm=world.querySelector('.xm'), qp=world.querySelector('.qm path'), xp=world.querySelector('.xm path'), qc=world.querySelector('.qm circle');
const rows=[0,1,2,3,4].map(c=>{const el=document.querySelector('#sl'+c);return {tb:el.querySelector('.tb'),d1:el.querySelector('.d1'),d2:el.querySelector('.d2'),tm:el.querySelector('.tm'),tp:el.querySelector('.tm path')}});
const flash=document.querySelector('#flash');
const NP=Dt.PUFF.length;
function render(v){
  const r=Rv(v), fr=r*60, rp=v>=Dt.vRm&&v<Dt.vJ, wEnd=ez((v-Dt.tG)/.6), wg=v<Dt.T0?1:1-ez(r/1.2), w=Math.max(wg,wEnd), idle=v<Dt.T0?1:wEnd;
  const i=Math.min(Math.floor(fr),Dt.NF-1), f=Math.min(1,fr-i);
  // camera (scene choice): grid before Go, a smoothed follow during the race, the finish line in the replay, the grid again at the end
  const g=v<Dt.T0?0:ez(r/1.3);
  let cx=lerp(Dt.GC[0],lerp(Dt.CX[i],Dt.CX[i+1],f),g), cy=lerp(Dt.GC[1],lerp(Dt.CY[i],Dt.CY[i+1],f),g);
  let z=lerp(Dt.ZG,lerp(Dt.CZ[i],Dt.CZ[i+1],f),g), k=lerp(1.05,lerp(Dt.CK[i],Dt.CK[i+1],f),g);
  if(rp){const p=(v-Dt.vRm)/(Dt.vJ-Dt.vRm); cx=Dt.FC[0]+14*p; cy=Dt.FC[1]; z=2.2+.3*p; k=.8}
  cx=lerp(cx,Dt.GC[0],wEnd); cy=lerp(cy,Dt.GC[1],wEnd); z=lerp(z,Dt.ZG,wEnd); k=lerp(k,1.05,wEnd);
  const qM=r-Dt.tM, live=!rp&&v<Dt.vRm&&v>=Dt.T0;
  if(live&&qM>0&&qM<1.2){const s_=Math.exp(-5*qM); cx+=4*s_*Math.cos(37*qM); cy+=6*s_*Math.sin(44*qM)}
  // the world is drawn turned 90 degrees: world +x is up the page (page x = world y, page y = -world x)
  world.style.transform='translate('+(Dt.PCX-cy*z).toFixed(2)+'px,'+(Dt.PCY+cx*z).toFixed(2)+'px) rotate(-90deg) scale('+z.toFixed(4)+')';
  flash.style.opacity=(live&&qM>0&&qM<.36?(qM<.035?qM/.035:1-ez((qM-.035)/.325))*.82:0).toFixed(3);
  const P=[];
  for(let c=0;c<5;c++){
    let x=lerp(Dt.X[c][i],Dt.X[c][i+1],f), y=lerp(Dt.Y[c][i],Dt.Y[c][i+1],f), a=lerp(Dt.A[c][i],Dt.A[c][i+1],f);
    const S=Dt.SLOT[c];
    if(S&&fr>S.f){const p=Math.min(1,(r-S.f/60)/S.T), q=1-(1-p)*(1-p); x=lerp(x,S.x,q); y=lerp(y,S.y,q); a=a+angd(S.a,a)*q}
    if(c===Dt.iM&&r>Dt.tM){const q=r-Dt.tM; a+=.26*Math.exp(-3*q)*Math.sin(19*q)}
    const G=Dt.GRID[c]; x=lerp(x,G[0],w); y=lerp(y,G[1],w); a=a+angd(G[2],a)*w;
    x+=Math.sin(v*41+c*1.7)*.8*idle; y+=Math.cos(v*35+c*2.3)*.8*idle;
    let pu=1;
    if(c===Dt.iC&&rp) pu+=.45*bump((v-Dt.vX)/.7);
    if(c===Dt.iP&&r>Dt.tP) pu+=.06*Math.sin((r-Dt.tP)*7)*(1-wEnd);
    P.push({x,y,a});
    const off=Dt.TL[c]-lerp(Dt.CL[c][i],Dt.CL[c][i+1],f), to=ez((r-.5)/.6)*(1-wEnd)*.9;
    const e=cars[c];
    e.el.style.transform='translate('+x.toFixed(2)+'px,'+y.toFixed(2)+'px)'; e.cs.style.transform='scale('+k.toFixed(3)+')';
    e.cb.style.transform='rotate('+a.toFixed(4)+'rad)'; e.bd.style.transform='rotate(90deg) scale('+pu.toFixed(3)+')';
    if(e.ry){const o=rp?ez((v-Dt.vX)/.25):0; e.ry.style.opacity=o.toFixed(3); e.ry.style.transform='rotate('+((v-Dt.vX)*38).toFixed(1)+'deg) scale('+(.7+.3*o).toFixed(3)+')'}
    trs[c].style.strokeDashoffset=off.toFixed(1); trs[c].style.opacity=to.toFixed(3);
    // chips: status only, fixed order
    const R=rows[c], out=(c===Dt.iP&&r>Dt.tP)||(c===Dt.iM&&r>Dt.tM), tS=c===Dt.iP?Dt.tP:Dt.tM, mo=out?ez((r-tS-.1)/.35)*(1-wEnd):0;
    R.tb.style.transform='scale('+(1+(c===Dt.iC&&rp?.24*bump((v-Dt.vX)/.7):0)).toFixed(3)+')';
    R.tb.style.opacity=(1-.6*mo).toFixed(3);
    const L=Dt.LAPF[c], on1=L[0]!==undefined&&fr>=L[0]&&wEnd<.5, on2=L[1]!==undefined&&fr>=L[1]&&wEnd<.5;
    R.d1.style.background=on1?'#0f0f0f':'#fbfbf8'; R.d2.style.background=on2?'#0f0f0f':'#fbfbf8';
    R.d1.style.transform='scale('+(1+.5*bump(L[0]!==undefined?(fr-L[0])/20:-1)).toFixed(3)+')';
    R.d2.style.transform='scale('+(1+.5*bump(L[1]!==undefined?(fr-L[1])/20:-1)).toFixed(3)+')';
    if(R.tm){R.tm.style.opacity=mo>0?1:0; R.tp.style.strokeDashoffset=(1-mo).toFixed(3); R.tm.style.transform='scale('+(1+.25*bump((r-tS-.1)/.5)).toFixed(3)+')'}
  }
  // effects (world units; sized with the car draw scale)
  for(let n=0;n<NP;n++){
    const U=Dt.PUFF[n], p=(r-U[0])/.75, el=pfs[n];
    if(p>0&&p<1&&live){el.style.opacity=((1-p)*.92).toFixed(3); el.style.transform='translate('+(U[1]+U[3]*p*k).toFixed(1)+'px,'+(U[2]+U[4]*p*k).toFixed(1)+'px) scale('+(U[5]/20*(.45+p)*1.5*k).toFixed(3)+')'}
    else el.style.opacity=0;
  }
  for(let n=0;n<10;n++){            // exhaust on the grid (under the line-up; seen for a moment at Go)
    const c=n%5, el=pfs[NP+n], ph=((v*2.1+n*.37)%1+1)%1, C=P[c], d=48+30*ph;
    el.style.opacity=(idle*(1-ph)*.8).toFixed(3);
    el.style.transform='translate('+(C.x-Math.cos(C.a)*d).toFixed(1)+'px,'+(C.y-Math.sin(C.a)*d+(n<5?-5:5)).toFixed(1)+'px) scale('+((.35+ph*.7)*1.2).toFixed(3)+')';
  }
  const so=live&&qM>0&&qM<.9?(qM<.08?qM/.08:1-ez((qM-.3)/.6)):0;
  star.style.opacity=so.toFixed(3);
  star.style.transform='translate('+Dt.NOSE[0]+'px,'+Dt.NOSE[1]+'px) scale('+((.45+.75*ez(qM/.18))).toFixed(3)+') rotate('+(qM*40).toFixed(1)+'deg)';
  const qo=ez((r-Dt.tP-.15)/.4)*(1-wEnd), xo=ez((r-Dt.tM-.12)/.35)*(1-wEnd);
  qm.style.opacity=qo>0?1:0; qp.style.strokeDashoffset=(1-qo).toFixed(3); qc.style.opacity=qo>.9?1:0;
  qm.style.transform='translate('+(Dt.QM[0]+Math.sin(v*4)*1.2).toFixed(1)+'px,'+Dt.QM[1]+'px) rotate(90deg) scale(.8)';
  xm.style.opacity=xo>0?1:0; xp.style.strokeDashoffset=(1-xo).toFixed(3);
  xm.style.transform='translate('+Dt.XM[0]+'px,'+Dt.XM[1]+'px) rotate('+(90+Math.sin(v*3)*5).toFixed(1)+'deg) scale('+(.95+.3*bump((r-Dt.tM-.12)/.5)).toFixed(3)+')';
}
'''.replace("__DATA__", json.dumps(DATA, separators=(",", ":")))

JS = re.sub(r"tl\.set\(([^,]+),\{", r"tl.set(\1,{immediateRender:false,", "\n".join(J))
SFX.sort(key=lambda x: x["t"])
json.dump(SFX, open(H_ + "/sfx98.json", "w"), indent=1)
TLN = "ESTIMATED (cue texts do not match voice/lines.txt)" if STALE else ("lines 1-4 from the voice cues, lines 5-12 on the TARGETS (the take is not padded yet: re-stitch on the targets)" if ONTG else "voice cues")
json.dump(dict(lines=[dict(n=n, text=LINES[n - 1], start=round(s(n), 3), end=round(e(n), 3)) for n in range(1, NL + 1)], D=D, go=T0,
               stale_cues=STALE, lines_on_targets=ONTG, timeline=TLN,
               targets={str(n): round(TG[n], 2) for n in range(1, NL + 1)}, drift_vs_targets=DRIFT,
               race=dict(start=T0, live_until_race_s=LIVE_END, perplexity_stops=round(vP, 3), meta_wall=round(vM, 3), claude=round(vC, 3), gemini=round(vGm, 3),
                         chatgpt=round(vCh, 3) if vCh < vRm else None,
                         replay_from=round(vRm, 3), replay_to=round(vJ, 3), replay_rate=SLOW, replay_race_from=round(rA, 3), replay_claude=round(vX, 3), replay_gemini=round(vXg, 3)),
               premise=dict(start=round(a2, 3), notes=round(tN, 3), rules=round(a3, 3), cars_alive=ALIVE, pick=PICK),
               sources=SRC), open(H_ + "/cues98.json", "w"), indent=1)
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
// a clock, not a motion: GSAP writes the time into clk.v and the setter draws the race for that time
// (a setter, not onUpdate: seek() suppresses callbacks by default, a property write always happens)
let _v=0; const clk={{get v(){{return _v}},set v(x){{_v=x;render(x)}}}};
tl.fromTo(clk,{{v:0}},{{v:D,duration:D,ease:'none',immediateRender:false}},0);
{JS}
tl.to({{}},{{duration:.001}},D-.001);
window.__timelines=window.__timelines||{{}}; window.__timelines["main"]=tl; tl.seek(0); render(0);
window.__reel={{duration:D,seek:t=>{{tl.seek(t)}}}};
</script></body></html>'''
os.makedirs(H_ + "/hf", exist_ok=True); os.makedirs(H_ + "/out", exist_ok=True)
open(H_ + "/hf/index.html", "w").write(html)
say(f"D={D} go={T0} ({SRC['go']}) stale_cues={STALE} lines_on_targets={ONTG} js={len(J)} sfx={len(SFX)}")
say("timeline: " + TLN)
if STALE:
    say("WARNING stale cues: voice/narration-raw-cues.json does not hold the lines of voice/lines.txt (old take" + (", or EST=1" if FORCE_EST else "") +
        "). ESTIMATED timeline in use; rebuild when the new take is in place.")
say("lines: " + "  ".join(f"{n}:{s(n):.2f}-{e(n):.2f}" for n in range(1, NL + 1)))
say("voice targets (line start so the words land on the race): " + "  ".join(f"{n}:{TG[n]:.2f}" for n in range(1, NL + 1)) +
    ("" if STALE else "   drift of the take on disk: " + "  ".join(f"{n}:{DRIFT[n]:+.2f}" for n in DRIFT)))
say(f"premise: reset {a2 - .1:.2f}, notes fly {tN:.2f}, rules {a3:.2f}, cars alive {ALIVE[0]:.2f}-{ALIVE[-1]:.2f}, pick {PICK[0]:.2f}-{PICK[-1]:.2f}, go {T0}")
say(f"race clock: 1x from {T0} to {vRm:.2f} (race {LIVE_END}); video times: Perplexity stops {vP:.2f}, Meta AI wall {vM:.2f}, Claude {vC:.2f}, Gemini {vGm:.2f}, "
    f"ChatGPT {vCh:.2f}{'' if vCh < vRm else ' (NOT SHOWN live: the replay starts first)'}")
say(f"SLOW MOTION REPLAY {SLOW}x video {vRm:.2f}-{vJ:.2f} (race from {rA:.2f}), label until {tSO:.2f}; Claude crosses {vX:.2f}, Gemini {vXg:.2f}; card {tK:.2f}; maze {s(12):.2f}; frame-0 layout from {tF:.2f}")
say(f"headlines in: two-laps {tA2:.2f}, Perplexity {tA3:.2f}, Meta AI {tA4:.2f}, neck {tA5:.2f}, ChatGPT {tA6:.2f}, who-won {vR0 + .12:.2f}, wins {vX:.2f}, send {tK:.2f}/{tS8:.2f}")
say(f"camera: zoom {min(CZ):.2f}-{max(CZ):.2f}; smallest car on screen in the race {MINCAR:.0f} px long, {MINCAR * .6:.0f} px wide")
if not WORDS: say("NOTE: no usable voice/words.json for this take: word-timed beats use line fractions.")
open(H_ + "/out/build-v6.log", "w").write("\n".join(LOG) + "\n")
