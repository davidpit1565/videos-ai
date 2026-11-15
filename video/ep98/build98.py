#!/usr/bin/env python3
"""ep98 'AI RACE #1' scene, v2 (T8b), Miki style, HyperFrames + GSAP paused timeline, 1080x1920.
Script: 'v2 script' in channel/episode-98-script.md (10 lines, voice/lines.txt). Fixes: channel/episode-98-redteam.md.

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
    all five on the same spot) and that offset fades out during the first 1.2 s of the race; after a car
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
    elif n == 2: DUR[n] = 1.25                                          # "Pick one. Go!"
    else: DUR[n] = round(.3 + .045 * len(t), 2)
WORDS = []
if not STALE:
    try:
        WORDS = json.load(open(H_ + "/voice/words.json"))
        if not (WORDS and norm(WORDS[0][0]) == norm(LINES[0].split()[0]) and abs(WORDS[-1][2] - float(CUE[NL]["end"])) < 1.2): WORDS = []
    except Exception:
        WORDS = []
SRC = {}
# lines 1-2 and the word "Go" (the race starts on it)
if STALE:
    L = {1: (.08, round(.08 + DUR[1], 2))}; L[2] = (round(L[1][1] + .06, 2), round(L[1][1] + .06 + DUR[2], 2))
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
if STALE: T0 = s(2) + .76 * DUR[2]; SRC["go"] = "ESTIMATE (stale cues)"
else:
    T0 = W("go", 2)
    if T0 is not None: SRC["go"] = "words.json"
    else:
        sg = speech(2, .15)
        if len(sg) >= 2: T0 = sg[-1][0]; SRC["go"] = "speech gap in the wav"
        else: T0 = s(2) + .76 * (e(2) - s(2)); SRC["go"] = "line fraction"
T0 = round(T0, 3)
V = lambda r: T0 + r                                         # video time of a race time, live part (1x)
vP, vM, vC, vGm, vCh = V(tP), V(tM), V(tC), V(tGm), V(tCh)
# where each line should start so the words land on the race (targets for the voice; also the estimated timeline)
TG = {1: L[1][0] if not STALE else .08, 2: L[2][0]}
TG[3] = round(vP - .45, 2)                                   # "stops" lands as Perplexity stops
TG[4] = round(max(TG[3] + DUR[3] + .06, vM - .5), 2)         # "hits" lands on the wall
TG[5] = round(max(TG[4] + DUR[4] + .08, vC - DUR[5] - .15), 2)   # ends as the two cross the line
TG[6] = round(max(TG[5] + DUR[5] + .08, vGm + .45), 2)
TG[7] = round(max(TG[6] + DUR[6] + .1, vCh + .2), 2)         # the replay
for n in range(8, NL + 1): TG[n] = round(TG[n - 1] + DUR[n - 1] + .06, 2)
if STALE:
    for n in range(3, NL + 1): L[n] = (TG[n], round(TG[n] + DUR[n], 2))
DRIFT = {n: round(s(n) - TG[n], 2) for n in range(3, 8)}
D = round(e(NL) + .45, 2)
tF = D - .58                                                 # the frame-0 layout comes back from here

# ---------------------------------------------------------------- race clock r(v): 1x live, then the 1/4-speed replay
SLOW = .25
vR0 = max(s(7) - .35, vGm + .9)                              # replay: the dip starts
vRm = vR0 + .14                                              # the clock jumps here, under the dip
tw7 = W("wins", 7)
vX = max(vRm + .62, tw7 if tw7 is not None else s(7) + .32 * (e(7) - s(7)))   # Claude's nose crosses the line in the replay
vXg = vX + (tGm - tC) / SLOW                                 # Gemini crosses in the replay
tK = max(s(8) - .05, vXg + .45)                              # result card
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

# ---------------------------------------------------------------- camera (scene choice): centre x, y, zoom and car draw scale per race frame
SX, SY, SW, SH, BW = 65, 508, 950, 736, 6                   # stage box on the page (inside the safe box), ink border
VW, VH = SW - 2 * BW, SH - 2 * BW - 118                     # road viewport inside the stage (the strip takes the bottom 118 px)
GC = [300.0, 694.0]                                         # grid camera centre
FC = [278.0, 688.0]                                         # finish-line camera centre (replay)
def box(pts, m, zmax, zmin=.78):
    x0 = min(p[0] for p in pts); x1 = max(p[0] for p in pts); y0 = min(p[1] for p in pts); y1 = max(p[1] for p in pts)
    z = max(zmin, min(zmax, VW / (x1 - x0 + 2 * m), VH / (y1 - y0 + 2 * m)))
    return (x0 + x1) / 2, (y0 + y1) / 2, z
def cam_target(i):
    r = i / 60; pos = lambda k: (FR[k][min(i, STOP[k])][0], FR[k][min(i, STOP[k])][1]); line = (300, 700)
    if r < 3.7: return (*box([pos(k) for k in IDS], 100, 1.8), 1.2)
    if r < 4.8: return (178, 632, 2.4, .72)                  # hairpin: Perplexity stops
    if r < 5.6: return (240, 600, 1.8, .72)                  # hairpin + line: ChatGPT passes, Meta AI arrives
    if r < 6.9: return (190, 616, 2.8, .7)                   # hairpin: Meta AI and the wall
    if r < 7.5: return (*box([pos(k) for k in FIN], 110, 1.2), 1.2)
    if r < 8.95: return (*box([pos("claude"), pos("gemini"), line], 100, 1.6), 1.15)
    return (*box([pos("chatgpt"), line], 110, 1.6), 1.15)
raw = [cam_target(i) for i in range(NF + 1)]
def smooth(vals, sg=16):
    n = len(vals); ker = [math.exp(-.5 * (q / sg) ** 2) for q in range(-3 * sg, 3 * sg + 1)]; ks = sum(ker)
    return [sum(ker[q + 3 * sg] * vals[min(n - 1, max(0, i + q))] for q in range(-3 * sg, 3 * sg + 1)) / ks for i in range(n)]
CX = [round(v, 1) for v in smooth([t[0] for t in raw])]; CY = [round(v, 1) for v in smooth([t[1] for t in raw])]
CZ = [round(math.exp(v), 4) for v in smooth([math.log(t[2]) for t in raw])]; CK = [round(v, 3) for v in smooth([t[3] for t in raw])]

# ---------------------------------------------------------------- text helpers
try:
    from PIL import ImageFont
    _f = ImageFont.truetype(H_ + "/hf/assets/fonts/InterDisplay-Black.otf", 100)
    tw = lambda t: _f.getlength(t) - 3.0 * len(t)           # letter-spacing -.03em
except Exception:
    tw = lambda t: 62 * len(t)
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

# ---------------------------------------------------------------- headlines (at most 2 lines + one small line, plain ink, no boxes, no code words)
HEADS = []
def head(i, t_in, t_out, l1, l2="", logos=(), t2=None, size=96, extra=""):
    wl = len(logos) * 86
    fs = min(size, 900 / max((tw(l1) + wl * 100 / 84) / 100, tw(l2) / 100 if l2 else 0.01))
    lg = "".join(logo(k, round(fs * .86), "hlg") for k in logos)
    l2h = f'<div class="hl2" id="h{i}b">{l2}</div>' if l2 else ""
    HEADS.append(f'<div class="hd" id="h{i}" style="font-size:{fs:.1f}px;line-height:{fs * .98:.1f}px"><div class="hl1">{lg}<span>{l1}</span></div>{l2h}{extra}</div>')
    if t_in is not None:
        fin(f"#h{i}", t_in)
        if l2 and t2 is not None:
            js(f"tl.fromTo('#h{i}b',{{opacity:0,x:34}},{{opacity:1,x:0,duration:.3,ease:'power3.out',immediateRender:false}},{t2:.3f});")
    if t_out is not None: fout(f"#h{i}", t_out - .24)
tA2 = T0 + .82
tA3 = clamp(s(3), vP - .6, vP - .12)                        # the event headlines follow the race, the voice is told where to land (targets)
tA4 = clamp(s(4), vM - .7, vM - .12)
tA5 = clamp(s(5), vM + 1.0, vC - .9)
tA6 = clamp(s(6), vGm + .5, max(vGm + .5, vR0 - 1.2))
tS8 = W("send", 8); tS8 = tS8 if tS8 is not None else s(8) + .52 * (e(8) - s(8))
head(0, None, s(2) - .05, "EACH AI TAUGHT A CAR.", "ONE HITS THE WALL.", size=88, extra='<div class="hs" id="h0s">same request to every AI</div>')
head(1, s(2), T0 - .04, "PICK ONE.", size=132)
HEADS.append('<div class="hd go" id="hgo"><div class="hl1"><span>GO!</span></div></div>')
js(f"tl.fromTo('#hgo',{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.3,ease:'power3.out',immediateRender:false}},{T0:.3f});")
js(f"tl.to('#hgo',{{opacity:0,scale:1.2,duration:.26,ease:'power2.in'}},{tA2 - .3:.3f});")
head(2, tA2, tA3, "TWO LAPS.", "HANDS OFF.")
head(3, tA3, tA4, "PERPLEXITY", "STOPS DEAD", logos=("perplexity",), t2=vP)
head(4, tA4, tA5, "META AI", "HITS THE WALL", logos=("meta",), t2=vM)
head(5, tA5, tA6, "NECK AND NECK", logos=("claude", "gemini"))
head(6, tA6, vR0 + .1, "CHATGPT", "TAKES ITS TIME", logos=("chatgpt",))
head(7, vR0 + .12, vX, "WHO WON?", size=120)
head(8, vX, tK, "CLAUDE WINS", f"{GAP} s AHEAD OF GEMINI", logos=("claude",), t2=vXg)
head(9, tK, s(10) - .04, "SEND IT TO A FRIEND", "SEE WHO THEY PICK", t2=tS8)
head(10, s(10), tF + .04, "NEXT: A MAZE", size=120)
fin("#h0", tF + .06, .42)

# ---------------------------------------------------------------- markup: the world (road, trails, cars, effects)
pts = lambda P: " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in P)
outer = "M" + " L".join(f"{p[0]:.1f} {p[1]:.1f}" for p in TR["rightEdge"]) + "Z"
inner = "M" + " L".join(f"{p[0]:.1f} {p[1]:.1f}" for p in TR["leftEdge"]) + "Z"
fl = TR["leftEdge"][0]; fr_ = TR["rightEdge"][0]            # the finish line runs between these two edge points
cheq = ""
for i in range(20):
    y0 = fl[1] + (fr_[1] - fl[1]) * i / 20; hh = (fr_[1] - fl[1]) / 20
    for q in range(2):
        if (i + q) % 2 == 0: cheq += f'<rect x="{fl[0] - 7 + 7 * q:.1f}" y="{y0:.1f}" width="7" height="{hh:.2f}" fill="{INK}"/>'
road = f'''<svg class="road" viewBox="0 0 950 808" width="950" height="808">
 <defs><filter id="wob" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="3.2"/></filter></defs>
 <path d="{outer} {inner}" fill="{INK}" fill-rule="evenodd" transform="translate(7 7)"/>
 <path d="{outer} {inner}" fill="{ROAD}" fill-rule="evenodd"/>
 <polyline points="{pts(CLN)} {CLN[0][0]},{CLN[0][1]}" fill="none" stroke="{INK}" stroke-opacity=".2" stroke-width="3" stroke-dasharray="16 18"/>
 <rect x="{fl[0] - 7:.1f}" y="{fl[1]:.1f}" width="14" height="{fr_[1] - fl[1]:.1f}" fill="#fff"/>{cheq}
 <g filter="url(#wob)" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"><path d="{outer}"/><path d="{inner}"/></g>
</svg>'''
trails = '<svg class="trs" viewBox="0 0 950 808" width="950" height="808">' + "".join(
    f'<path class="trl" d="{TRD[c]}" stroke="{COL[k]}" stroke-dasharray="{CLEN[c][STOP[k]] + 2:.1f}" stroke-dashoffset="{CLEN[c][STOP[k]] + 2:.1f}"/>' for c, k in enumerate(IDS)) + "</svg>"
rays = "".join(f'<path d="M{math.cos(i * math.pi / 8) * 62:.1f} {math.sin(i * math.pi / 8) * 62:.1f} L{math.cos(i * math.pi / 8) * (92 if i % 2 else 80):.1f} {math.sin(i * math.pi / 8) * (92 if i % 2 else 80):.1f}"/>' for i in range(16))
def car(c, k):
    ry = f'<svg class="rays" viewBox="-100 -100 200 200">{rays}</svg>' if k == "claude" else ""
    return f'''<div class="car" data-c="{c}" style="z-index:{10 - c}"><div class="cs">{ry}<div class="cb"><svg viewBox="-40 -24 80 48" width="80" height="48">
 <rect x="-28" y="-23" width="15" height="9" rx="3" fill="{INK}"/><rect x="13" y="-23" width="15" height="9" rx="3" fill="{INK}"/>
 <rect x="-28" y="14" width="15" height="9" rx="3" fill="{INK}"/><rect x="13" y="14" width="15" height="9" rx="3" fill="{INK}"/>
 <rect x="-36" y="-17" width="72" height="34" rx="13" fill="{COL[k]}" stroke="{INK}" stroke-width="3.5"/>
 <rect x="-39" y="-15" width="7" height="30" rx="2" fill="{INK}"/><path d="M30 -9 Q37 0 30 9" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
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

# ---------------------------------------------------------------- markup: strip (fixed order, status only), maze, result card
strip = '<div id="strip">'
for c, k in enumerate(IDS):
    mark = '<path d="M-9 -9 C-9 -22 11 -22 11 -9 C11 0 1 0 1 8 M1 17 V17.5" pathLength="1"/>' if k == "perplexity" else '<path d="M-13 -13 L13 13 M13 -13 L-13 13" pathLength="1"/>' if k == "meta" else ""
    strip += f'''<div class="sl" id="sl{c}"><div class="sb"><i class="ring" style="border-color:{COL[k]}"></i>{badge(k, 80, "tb")}{f'<svg class="tm" viewBox="-22 -24 44 48">{mark}</svg>' if mark else ""}</div><div class="dots"><i class="d1"></i><i class="d2"></i></div></div>'''
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
    card += f'<div class="cr" id="cr{i}" style="top:{104 + i * 98}px"><span class="cp">{pl}</span>{badge(k, 74)}<span class="cn">{NAME[k]}</span><span class="cv">{res}</span>{"<i></i>" if i == 0 else ""}</div>'
card += '<div class="cl" id="cl">rules locked first, one try each</div><div class="cf" id="cf">race your own AI: link in bio<i></i></div></div>'
markup = f'''
<div class="bgw" data-decor></div>
<div id="cam">
 <div id="stage"><div id="vp"><div id="world" class="world">{world}</div><div id="flash"></div><div id="dip"></div>
  <div id="slow"><b></b>SLOW MOTION REPLAY</div>{maze}</div>{strip}</div>
 {"".join(HEADS)}
 {card}
</div>'''

CSS = '''
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;color:INK}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}
.bgw{position:absolute;left:-20px;top:-20px;width:1120px;height:1960px;background:#ecebe5 url(assets/bg.jpg);background-size:1120px 1960px}
#cam{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 844px}
#stage{position:absolute;left:SXpx;top:SYpx;width:SWpx;height:SHpx;border:BWpx solid INK;border-radius:12px;box-shadow:12px 12px 0 INK;background:#ecebe5;overflow:hidden;z-index:1}
#vp{position:absolute;left:0;top:0;width:VWpx;height:VHpx;overflow:hidden;background:#ecebe5 url(assets/bg.jpg);background-size:1120px 1960px;background-position:-70px -520px}
.world{position:absolute;left:0;top:0;width:950px;height:808px;transform-origin:0 0;will-change:transform}
.hd{z-index:3} #card{z-index:5}
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
#flash,#dip{position:absolute;left:0;top:0;width:VWpx;height:VHpx;opacity:0;pointer-events:none}
#flash{background:#fff} #dip{background:#ecebe5 url(assets/bg.jpg);background-size:1120px 1960px;background-position:-70px -520px}
#slow{position:absolute;left:22px;top:16px;font-weight:900;font-size:36px;line-height:42px;letter-spacing:-.01em;color:RED;white-space:nowrap;opacity:0;display:flex;align-items:center;gap:10px;
 text-shadow:2px 2px 0 #fbfbf8,-2px 2px 0 #fbfbf8,2px -2px 0 #fbfbf8,-2px -2px 0 #fbfbf8,0 3px 0 #fbfbf8,3px 0 0 #fbfbf8,-3px 0 0 #fbfbf8,0 -3px 0 #fbfbf8}
#slow b{display:block;width:20px;height:20px;border-radius:50%;background:RED;border:2px solid #fbfbf8}
#strip{position:absolute;left:0;bottom:0;width:VWpx;height:118px;background:PAPER;border-top:BWpx solid INK;display:flex}
.sl{flex:1;display:flex;align-items:center;justify-content:center;gap:10px;will-change:transform}
.sb{position:relative;width:80px;height:80px;flex:none}
.sb .tb{position:absolute;left:0;top:0}
.ring{position:absolute;left:-9px;top:-9px;width:98px;height:98px;border-radius:50%;border:7px solid INK;opacity:0}
.dots{display:flex;flex-direction:column;gap:8px} .dots i{display:block;width:19px;height:19px;border-radius:50%;border:3.5px solid INK;background:PAPER}
.tm{position:absolute;left:-2px;top:-4px;width:84px;height:92px;overflow:visible;opacity:0}
.tm path{fill:none;stroke:RED;stroke-width:8;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1}
.hd{position:absolute;left:65px;top:283px;font-weight:900;letter-spacing:-.03em;white-space:nowrap;opacity:0;transform-origin:0 50%}
#h0{opacity:1}
.hl1{display:flex;align-items:center} .hlg{margin-right:.16em;flex:none} .hl2{display:block}
.hs{font-weight:800;font-size:40px;line-height:46px;letter-spacing:-.01em;margin-top:8px}
.hd.go{font-size:170px;line-height:170px;top:286px}
#h8 .hl2{font-size:.62em;line-height:1.3em;letter-spacing:-.02em}
.tape{position:absolute;width:130px;height:40px;background:rgba(232,221,186,.86);border:1px solid rgba(0,0,0,.14);z-index:3}
.tape.t1{right:-34px;top:-12px;transform:rotate(34deg)} .tape.t2{left:-34px;bottom:-6px;transform:rotate(34deg)}
#msheet{position:absolute;left:0;top:0;width:VWpx;height:VHpx;opacity:0;background:#ecebe5 url(assets/bg.jpg);background-size:1120px 1960px;background-position:-70px -520px}
#msheet svg{position:absolute;left:214px;top:22px;width:510px;height:570px;overflow:visible}
#mzw{fill:none;stroke:INK;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1}
#mzp{fill:none;stroke:RED;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1}
#mzq{position:absolute;left:770px;top:150px;font-weight:900;font-size:230px;line-height:240px;color:RED;opacity:0;transform-origin:50% 60%}
#card{position:absolute;left:82px;top:506px;width:902px;height:736px;background:PAPER;border:6px solid INK;border-radius:10px;box-shadow:14px 14px 0 INK;opacity:0;transform-origin:50% 0%}
.ct{position:absolute;left:38px;top:26px;font-weight:900;font-size:52px;line-height:60px;letter-spacing:-.03em;white-space:nowrap}
.cr{position:absolute;left:38px;right:38px;height:90px;display:flex;align-items:center;opacity:0;border-top:4px solid rgba(15,15,15,.14)}
.cp{width:56px;font-weight:900;font-size:52px;line-height:60px;text-align:center;margin-right:14px}
.cn{font-weight:900;font-size:50px;line-height:60px;letter-spacing:-.03em;margin-left:20px;white-space:nowrap}
.cv{margin-left:auto;font-weight:800;font-size:38px;line-height:60px;letter-spacing:-.01em;white-space:nowrap}
.cr i{position:absolute;left:0;right:0;bottom:2px;height:9px;border-radius:5px;background:#D97757;transform-origin:0 50%;transform:scaleX(0)}
.cl{position:absolute;left:40px;top:602px;font-weight:800;font-size:34px;line-height:42px;letter-spacing:-.01em;white-space:nowrap;opacity:0}
.cf{position:absolute;left:40px;top:658px;font-weight:800;font-size:38px;line-height:48px;white-space:nowrap;opacity:0}
.cf i{position:absolute;left:0;right:0;bottom:-8px;height:6px;border-radius:3px;background:INK;transform-origin:0 50%;transform:scaleX(0)}
'''
for a_, b_ in (("SX", SX), ("SY", SY), ("SW", SW), ("SH", SH), ("BW", BW), ("VW", VW), ("VH", VH), ("INK", INK), ("PAPER", PAPER), ("RED", RED)):
    CSS = CSS.replace(a_, str(b_))

# ---------------------------------------------------------------- timeline (GSAP: text, strip, cards; cars and camera are driven by render())
js(f"tl.fromTo('#cam',{{scale:1,rotation:0}},{{scale:1.012,rotation:.2,duration:{D / 4:.3f},ease:'sine.inOut',yoyo:true,repeat:3}},0);")
js(f"tl.fromTo('.bgw',{{x:0,y:0}},{{x:-14,y:-12,duration:{D / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},0);")
# beat 1: the hook. "ONE HITS THE WALL" breathes on the word
tw_ = W("wall", 1); tw_ = tw_ if tw_ is not None else s(1) + .82 * (e(1) - s(1))
js(f"tl.fromTo('#h0 .hl2',{{scale:1}},{{scale:1.05,transformOrigin:'0 50%',duration:.22,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tw_:.3f});")
js(f"tl.fromTo('#h0s',{{x:0}},{{x:10,duration:{max(.4, (s(2) - .3) / 2):.3f},ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},0.1);")
sfx("subhit.ogg", .05, -6); sfx("impactsoft.ogg", tw_, -9)
# beat 2: "Pick one": the five logos light up as choices, one after another, and stay lit until Go
tPk = s(2) - .12; stepk = min(.13, max(.06, (T0 - .35 - tPk) / 5))
PICK = [round(tPk + c * stepk, 3) for c in range(5)]
for c in range(5):
    js(f"tl.fromTo('#sl{c}',{{y:0}},{{y:-16,duration:.2,ease:'power2.out',yoyo:true,repeat:1,immediateRender:false}},{PICK[c]:.3f});")
    js(f"tl.fromTo('#sl{c} .ring',{{opacity:0,scale:.7}},{{opacity:1,scale:1,duration:.26,ease:'power3.out',immediateRender:false}},{PICK[c]:.3f});")
    sfx("pop_a.ogg" if c % 2 == 0 else "pop_b.ogg", PICK[c], -10)
tPe = PICK[4] + .3
if T0 - tPe > .3:
    js(f"tl.to('.ring',{{scale:1.1,duration:{(T0 - tPe) / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},{tPe:.3f});")
js(f"tl.to('.ring',{{opacity:0,scale:1.25,duration:.4,ease:'power2.out'}},{T0 + .05:.3f});")
sfx("whoosh_a.ogg", T0 - .03, -6)
# race events (live, 1x)
sfx("toggle.ogg", vP - .25, -9); sfx("impactpunch.ogg", vM, -4); sfx("click_a.ogg", vC, -10); sfx("click_a.ogg", vGm, -10)
if vCh < vRm: sfx("click_b.ogg", vCh, -9)
# replay: a soft dip hides the jump of the clock, the label stays on for the whole slowed stretch
js(f"tl.fromTo('#dip',{{opacity:0}},{{opacity:1,duration:.14,ease:'sine.in',immediateRender:false}},{vR0:.3f});")
js(f"tl.to('#dip',{{opacity:0,duration:.24,ease:'sine.out'}},{vRm + .03:.3f});")
js(f"tl.fromTo('#slow',{{opacity:0,x:-16}},{{opacity:1,x:0,duration:.2,ease:'power2.out',immediateRender:false}},{vRm:.3f});")
js(f"tl.fromTo('#slow b',{{opacity:1}},{{opacity:.25,duration:.3,ease:'sine.inOut',yoyo:true,repeat:{2 * max(1, round((vJ - vRm) / .6)) - 1},immediateRender:false}},{vRm:.3f});")
js(f"tl.to('#slow',{{opacity:0,duration:.16,ease:'sine.in'}},{tK - .14:.3f});")
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
hold = max(.8, s(10) - tK - .7)
js(f"tl.to('#card',{{rotation:.6,y:-8,duration:{hold / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},{tK + .55:.3f});")
for q, i in enumerate((3, 4, 2, 1)):                         # a slow wave keeps the list alive while it is read
    js(f"tl.fromTo('#cr{i} .bdg',{{rotation:0}},{{rotation:{-10 if q % 2 else 10},duration:.28,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tU + .7 + q * .3:.3f});")
fin("#cf", s(9) + .05)
js(f"tl.to('#cf i',{{scaleX:1,duration:.6,ease:'power2.inOut'}},{s(9) + .3:.3f});")
sfx("tick.ogg", s(9) + .05, -9)
for q, i in enumerate((0, 1, 2)):
    js(f"tl.fromTo('#cr{i} .cv',{{scale:1}},{{scale:1.1,transformOrigin:'100% 50%',duration:.24,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{s(9) + .95 + q * .2:.3f});")
# last line: the maze sheet covers the road (the cars go back to the grid under it), then the frame-0 layout returns
tG = s(10) + .15
js(f"tl.fromTo('#msheet',{{opacity:0}},{{opacity:1,duration:.22,ease:'sine.inOut',immediateRender:false}},{s(10) - .36:.3f});")
js(f"tl.to('#sl{ci} .ring',{{opacity:0,duration:.2,ease:'sine.inOut'}},{s(10) - .36:.3f});")
js(f"tl.to('#card',{{opacity:0,scale:.82,y:-50,rotation:-4,duration:.36,ease:'power2.in'}},{s(10) - .12:.3f});")
sfx("whoosh_c.ogg", s(10) - .12, -10)
mzD = tF - s(10)
js(f"tl.to('#mzw',{{strokeDashoffset:0,duration:{min(1.2, mzD * .45):.3f},ease:'power2.inOut'}},{s(10) + .1:.3f});")
js(f"tl.to('#mzp',{{strokeDashoffset:0,duration:{max(.5, mzD * .5):.3f},ease:'sine.inOut'}},{s(10) + min(1.2, mzD * .45):.3f});")
js(f"tl.fromTo('#msheet svg',{{rotation:-2,scale:.96}},{{rotation:1.5,scale:1,duration:{mzD:.3f},ease:'sine.inOut',immediateRender:false}},{s(10) - .1:.3f});")
tq = W("lost", 10); tq = tq if tq is not None else s(10) + .86 * (e(10) - s(10))
tq = min(tq, tF - .45)
js(f"tl.fromTo('#mzq',{{opacity:0,scale:.5,rotation:-14}},{{opacity:1,scale:1,rotation:8,duration:.35,ease:'power3.out',immediateRender:false}},{tq:.3f});")
js(f"tl.to('#msheet',{{opacity:0,duration:.4,ease:'sine.inOut'}},{tF:.3f});")
sfx("tick.ogg", s(10) + .1, -10); sfx("whoosh_c.ogg", tF, -12)

# ---------------------------------------------------------------- render(): the race and the camera, driven by the timeline clock
DATA = dict(T0=T0, D=D, NF=NF, RT=RT, X=X, Y=Y, A=A, CL=CLEN, TL=[CLEN[c][STOP[k]] + 2 for c, k in enumerate(IDS)],
            GRID=GRID, SLOT={str(k): v for k, v in SLOT.items()}, LAPF=[LAPF[k] for k in IDS], STOP=[STOP[k] for k in IDS],
            PUFF=PUFF, NOSE=NOSE, tP=tP, tM=tM, iP=IDS.index("perplexity"), iM=IDS.index("meta"), iC=ci,
            PICK=PICK, vRm=round(vRm, 3), vJ=round(vJ, 3), vX=round(vX, 3), tG=round(tG, 3), VW=VW, VH=VH,
            CX=CX, CY=CY, CZ=CZ, CK=CK, GC=GC, FC=FC, QM=[round(px_ - 84, 1), round(py_ + 6, 1)], XM=[round(NOSE[0] + 62, 1), round(NOSE[1] + 8, 1)])
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
  let z=lerp(2.12+.16*ez(v/Dt.T0),lerp(Dt.CZ[i],Dt.CZ[i+1],f),g), k=lerp(1,lerp(Dt.CK[i],Dt.CK[i+1],f),g);
  if(rp){const p=(v-Dt.vRm)/(Dt.vJ-Dt.vRm); cx=Dt.FC[0]+16*p; cy=Dt.FC[1]; z=2.15+.25*p; k=.8}
  cx=lerp(cx,Dt.GC[0],wEnd); cy=lerp(cy,Dt.GC[1],wEnd); z=lerp(z,2.12,wEnd); k=lerp(k,1,wEnd);
  const qM=r-Dt.tM, live=!rp&&v<Dt.vRm&&v>=Dt.T0;
  if(live&&qM>0&&qM<1.2){const s_=Math.exp(-5*qM); cx+=6*s_*Math.sin(44*qM); cy+=4*s_*Math.cos(37*qM)}
  world.style.transform='translate('+(Dt.VW/2-cx*z).toFixed(2)+'px,'+(Dt.VH/2-cy*z).toFixed(2)+'px) scale('+z.toFixed(4)+')';
  flash.style.opacity=(live&&qM>0&&qM<.36?(qM<.035?qM/.035:1-ez((qM-.035)/.325))*.82:0).toFixed(3);
  const P=[];
  for(let c=0;c<5;c++){
    let x=lerp(Dt.X[c][i],Dt.X[c][i+1],f), y=lerp(Dt.Y[c][i],Dt.Y[c][i+1],f), a=lerp(Dt.A[c][i],Dt.A[c][i+1],f);
    const S=Dt.SLOT[c];
    if(S&&fr>S.f){const p=Math.min(1,(r-S.f/60)/S.T), q=1-(1-p)*(1-p); x=lerp(x,S.x,q); y=lerp(y,S.y,q); a=a+angd(S.a,a)*q}
    if(c===Dt.iM&&r>Dt.tM){const q=r-Dt.tM; a+=.26*Math.exp(-3*q)*Math.sin(19*q)}
    const G=Dt.GRID[c]; x=lerp(x,G[0],w); y=lerp(y,G[1],w); a=a+angd(G[2],a)*w;
    x+=Math.sin(v*41+c*1.7)*.8*idle; y+=Math.cos(v*35+c*2.3)*.8*idle;
    let pu=1+.3*bump((v-Dt.PICK[c])/.42);
    if(c===Dt.iC&&rp) pu+=.45*bump((v-Dt.vX)/.7);
    if(c===Dt.iP&&r>Dt.tP) pu+=.06*Math.sin((r-Dt.tP)*7)*(1-wEnd);
    P.push({x,y,a});
    const off=Dt.TL[c]-lerp(Dt.CL[c][i],Dt.CL[c][i+1],f), to=ez((r-.5)/.6)*(1-wEnd)*.9;
    const e=cars[c];
    e.el.style.transform='translate('+x.toFixed(2)+'px,'+y.toFixed(2)+'px)'; e.cs.style.transform='scale('+k.toFixed(3)+')';
    e.cb.style.transform='rotate('+a.toFixed(4)+'rad)'; e.bd.style.transform='scale('+pu.toFixed(3)+')';
    if(e.ry){const o=rp?ez((v-Dt.vX)/.25):0; e.ry.style.opacity=o.toFixed(3); e.ry.style.transform='rotate('+((v-Dt.vX)*38).toFixed(1)+'deg) scale('+(.7+.3*o).toFixed(3)+')'}
    trs[c].style.strokeDashoffset=off.toFixed(1); trs[c].style.opacity=to.toFixed(3);
    // strip: status only, fixed order
    const R=rows[c], out=(c===Dt.iP&&r>Dt.tP)||(c===Dt.iM&&r>Dt.tM), tS=c===Dt.iP?Dt.tP:Dt.tM, mo=out?ez((r-tS-.1)/.35)*(1-wEnd):0;
    R.tb.style.transform='scale('+(1+.22*bump((v-Dt.PICK[c])/.42)+(c===Dt.iC&&rp?.24*bump((v-Dt.vX)/.7):0)).toFixed(3)+')';
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
  for(let n=0;n<10;n++){            // exhaust on the grid (before Go, and again in the loop tail)
    const c=n%5, el=pfs[NP+n], ph=((v*2.1+n*.37)%1+1)%1, C=P[c], d=48+30*ph;
    el.style.opacity=(idle*(1-ph)*.8).toFixed(3);
    el.style.transform='translate('+(C.x-Math.cos(C.a)*d).toFixed(1)+'px,'+(C.y-Math.sin(C.a)*d+(n<5?-5:5)).toFixed(1)+'px) scale('+((.35+ph*.7)*1.2).toFixed(3)+')';
  }
  const so=live&&qM>0&&qM<.9?(qM<.08?qM/.08:1-ez((qM-.3)/.6)):0;
  star.style.opacity=so.toFixed(3);
  star.style.transform='translate('+Dt.NOSE[0]+'px,'+Dt.NOSE[1]+'px) scale('+((.45+.75*ez(qM/.18))).toFixed(3)+') rotate('+(qM*40).toFixed(1)+'deg)';
  const qo=ez((r-Dt.tP-.15)/.4)*(1-wEnd), xo=ez((r-Dt.tM-.12)/.35)*(1-wEnd);
  qm.style.opacity=qo>0?1:0; qp.style.strokeDashoffset=(1-qo).toFixed(3); qc.style.opacity=qo>.9?1:0;
  qm.style.transform='translate('+Dt.QM[0]+'px,'+(Dt.QM[1]+Math.sin(v*4)*2.5).toFixed(1)+'px) scale(.8)';
  xm.style.opacity=xo>0?1:0; xp.style.strokeDashoffset=(1-xo).toFixed(3);
  xm.style.transform='translate('+Dt.XM[0]+'px,'+Dt.XM[1]+'px) scale('+(.95+.3*bump((r-Dt.tM-.12)/.5)).toFixed(3)+') rotate('+(Math.sin(v*3)*5).toFixed(1)+'deg)';
}
'''.replace("__DATA__", json.dumps(DATA, separators=(",", ":")))

JS = re.sub(r"tl\.set\(([^,]+),\{", r"tl.set(\1,{immediateRender:false,", "\n".join(J))
SFX.sort(key=lambda x: x["t"])
json.dump(SFX, open(H_ + "/sfx98.json", "w"), indent=1)
json.dump(dict(lines=[dict(n=n, text=LINES[n - 1], start=s(n), end=e(n)) for n in range(1, NL + 1)], D=D, go=T0,
               stale_cues=STALE, timeline="ESTIMATED (cue texts do not match voice/lines.txt)" if STALE else "voice cues",
               targets={str(n): TG[n] for n in range(1, NL + 1)}, drift_vs_targets=DRIFT,
               race=dict(start=T0, live_until_race_s=LIVE_END, perplexity_stops=round(vP, 3), meta_wall=round(vM, 3), claude=round(vC, 3), gemini=round(vGm, 3),
                         chatgpt=round(vCh, 3) if vCh < vRm else None,
                         replay_from=round(vRm, 3), replay_to=round(vJ, 3), replay_rate=SLOW, replay_race_from=round(rA, 3), replay_claude=round(vX, 3), replay_gemini=round(vXg, 3)),
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
say(f"D={D} go={T0} ({SRC['go']}) stale_cues={STALE} js={len(J)} sfx={len(SFX)}")
if STALE:
    say("WARNING stale cues: voice/narration-raw-cues.json does not hold the 10 lines of voice/lines.txt (old take" + (", or EST=1" if FORCE_EST else "") +
        "). ESTIMATED timeline in use; rebuild when the new take is in place.")
say("lines: " + "  ".join(f"{n}:{s(n):.2f}-{e(n):.2f}" for n in range(1, NL + 1)))
say("voice targets (line start so the words land on the race): " + "  ".join(f"{n}:{TG[n]:.2f}" for n in range(3, 8)) +
    ("" if STALE else "   drift of the take: " + "  ".join(f"{n}:{DRIFT[n]:+.2f}" for n in DRIFT)))
if not STALE and any(abs(v) > .45 for v in DRIFT.values()): say("WARNING: a spoken line is more than 0.45 s away from its race event; place the lines on the targets above.")
say(f"race clock: 1x from {T0} to {vRm:.2f} (race {LIVE_END}); video times: Perplexity stops {vP:.2f}, Meta AI wall {vM:.2f}, Claude {vC:.2f}, Gemini {vGm:.2f}, "
    f"ChatGPT {vCh:.2f}{'' if vCh < vRm else ' (NOT SHOWN live: the replay starts first)'}")
say(f"SLOW MOTION REPLAY {SLOW}x video {vRm:.2f}-{vJ:.2f} (race from {rA:.2f}); Claude crosses {vX:.2f}, Gemini {vXg:.2f}; card {tK:.2f}; maze {s(10):.2f}; frame-0 layout from {tF:.2f}")
say(f"headlines in: two-laps {tA2:.2f}, Perplexity {tA3:.2f}, Meta AI {tA4:.2f}, neck {tA5:.2f}, ChatGPT {tA6:.2f}, who-won {vR0 + .12:.2f}, wins {vX:.2f}, send {tK:.2f}/{tS8:.2f}")
if not WORDS: say("NOTE: no usable voice/words.json for this take: word-timed beats use line fractions.")
open(H_ + "/out/build-v2.log", "w").write("\n".join(LOG) + "\n")
