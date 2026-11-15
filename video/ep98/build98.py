#!/usr/bin/env python3
"""ep98 'AI RACE #1' scene (T8), Miki style, HyperFrames + GSAP paused timeline, 1080x1920.
Plan: channel/episode-98-plan.md (sections 4, 6), script: channel/episode-98-script.md.

Reads  arena/race.json, arena/track.json, voice/narration-raw-cues.json (+ voice/words.json if present,
       else the speech gaps measured in voice/narration-raw.wav, else line fractions).
Writes hf/index.html, cues98.json (lines + D for the gate), sfx98.json (event times for T9).

What is true on screen, and what is a scene choice:
  - Every car position/angle is race.json, frame for frame, interpolated only between two 60 fps frames.
  - The race clock runs at 1x from the word "Go". ONE exception, labelled SLOW MOTION on screen the whole
    time it lasts: around the finish of Claude and Gemini the clock runs at 1/4 speed (all cars slow together).
  - Scene choices (not race data): the cars are drawn about 2.2x their physical size so the logos read;
    before "Go" they stand staggered behind the line (race.json starts all five on the same spot) and that
    offset fades out during the first 1.2 s of the race; after a car finishes it coasts to a parking slot
    past the line (race.json stops it on the line); at the end the cars return to the grid for the loop.
  - The close-up card shows the same cars at about their physical size (so 'touches the wall' looks right).
No TTS, no audio is written here.
"""
import json, os, re, math, shutil, wave, random
H_ = os.path.dirname(os.path.abspath(__file__))
INK = "#0f0f0f"; PAPER = "#fbfbf8"; RED = "#E5372B"; ROAD = "#d6d2c6"
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())

# ---------------------------------------------------------------- assets (fonts + paper from the ep97 build)
for sub in ("fonts/InterDisplay-Black.otf", "fonts/InterDisplay-ExtraBold.otf", "fonts/InterDisplay-Medium.otf", "bg.jpg"):
    dst = f"{H_}/hf/assets/{sub}"
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(f"{H_}/../ep97/hf/assets/{sub}", dst)

# ---------------------------------------------------------------- cues
EST = {1: (0.08, 1.80), 2: (1.86, 4.59), 3: (4.65, 6.15), 4: (6.21, 9.59), 5: (9.74, 11.33), 6: (11.39, 12.88), 7: (12.94, 14.77),
       8: (14.83, 16.28), 9: (16.43, 18.09), 10: (18.15, 20.22), 11: (20.28, 22.30), 12: (22.36, 24.17), 13: (24.23, 27.43)}
try:
    C = json.load(open(H_ + "/voice/narration-raw-cues.json")); C = C if isinstance(C, list) else C["lines"]
except Exception:
    C = []
CUE = {c["n"]: c for c in C if "n" in c}
L = {n: ((float(CUE[n]["start"]), float(CUE[n]["end"])) if n in CUE else EST[n]) for n in range(1, 14)}
TEXT = {n: (CUE[n].get("line", CUE[n].get("text", "")) if n in CUE else "") for n in range(1, 14)}
s = lambda n: L[n][0]
e = lambda n: L[n][1]
try:
    WORDS = json.load(open(H_ + "/voice/words.json"))
    if not (WORDS and WORDS[-1][1] <= e(13) + 1.0): WORDS = []
except Exception:
    WORDS = []
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
# "Go": the race starts on that word
SRC = {}
T0 = W("go", 3)
if T0 is not None: SRC["go"] = "words.json"
else:
    sg = speech(3, .15)
    if len(sg) >= 2: T0 = sg[-1][0]; SRC["go"] = "speech gap in the wav"
    else: T0 = s(3) + .8 * (e(3) - s(3)); SRC["go"] = "line fraction"
T0 = round(T0, 3)
# roll call: when each name is spoken
NAMES = ["chatgpt", "gemini", "claude", "meta", "perplexity"]
ROLL = [W(k, 4) for k in NAMES]
if all(x is not None for x in ROLL): SRC["roll"] = "words.json"
else:
    sg = speech(4, .11)
    if len(sg) == 5: ROLL = [x[0] for x in sg]; SRC["roll"] = "speech gaps in the wav"
    else:
        wts = [4.5, 3.5, 2.5, 4.5, 4.5]; acc = 0; ROLL = []
        for w_ in wts: ROLL.append(s(4) + acc / sum(wts) * (e(4) - s(4))); acc += w_
        SRC["roll"] = f"line fractions ({len(sg)} speech segments found, 5 needed)"
tF = e(13) + .15                               # everything is back in the frame-0 layout by tF + 0.9
D = round(e(13) + 1.1, 2)

# ---------------------------------------------------------------- race data
R = json.load(open(H_ + "/arena/race.json")); TR = json.load(open(H_ + "/arena/track.json"))
IDS = ["chatgpt", "gemini", "claude", "meta", "perplexity"]
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
def prog(k, i):
    if k in FIN and i >= FIN[k]: return 10 - FIN[k] / 10000
    i = min(i, STOP[k]); x, y = FR[k][i][0], FR[k][i][1]; lap = FR[k][i][4]
    j = min(range(NCL), key=lambda q: (CLN[q][0] - x) ** 2 + (CLN[q][1] - y) ** 2); fr = j / NCL
    since = i - max([0] + [q for q in LAPF[k] if q <= i])
    if fr > .8 and since < 40: fr = 0
    if fr < .1 and since > 100: fr = .999
    return lap + fr
PR = {k: [prog(k, i) for i in range(NF + 1)] for k in IDS}
raw = [sorted(range(5), key=lambda c: (-PR[IDS[c]][i], c)) for i in range(NF + 1)]
order = [raw[0]]
for i in range(1, NF + 1):
    cand = raw[i]
    order.append(cand if all(raw[min(NF, i + q)] == cand for q in range(12)) else order[-1])
RANKEV = []
for c in range(5):
    ev = [[0, order[0].index(c)]]
    for i in range(1, NF + 1):
        rk = order[i].index(c)
        if rk != ev[-1][1]: ev.append([i, rk])
    RANKEV.append(ev)
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
for c in range(5):                                          # staggered grid around the line, 88 px ahead to 88 px behind the real start point (scene choice)
    x, y, a = cl_at(-88 + 44 * c); lat = (-24 if c % 2 == 0 else 24)
    GRID.append([round(x - math.sin(a) * lat, 1), round(y + math.cos(a) * lat, 1), round(a, 3)])
PLACE = {k: RES[k]["place"] for k in IDS}
SLOT = {}
for k in FIN:                                               # parking slots past the line (scene choice)
    d = {1: 264, 2: 174, 3: 84}[PLACE[k]]; x, y, a = cl_at(-d)
    v0 = max(3.0, FR[k][FIN[k] - 1][3]) * 60
    SLOT[IDS.index(k)] = dict(f=FIN[k], x=round(x, 1), y=round(y, 1), a=round(a, 3), T=round(max(.6, 2 * d / v0), 3))
tP = STOP["perplexity"] / 60; tM = STOP["meta"] / 60        # 4.22 and 6.15 (race clock)
tC = RES["claude"]["timeS"]; tGm = RES["gemini"]["timeS"]; tCh = RES["chatgpt"]["timeS"]

# ---------------------------------------------------------------- race clock: r(v), 1x, 1/4 speed around the finish
SLOW = .25; rB = tGm + .08
target = s(8) + .32 * (e(8) - s(8))                          # Claude crosses the line on "crosses"
def clock(rA):
    dt = 1 / 240; r = 0.0; rate = 1.0; tab = []; v = 0.0; n = 0; vs = ve = None
    while v <= D + .05:
        if n % 4 == 0: tab.append(r)
        if v >= T0:
            tg = SLOW if rA <= r < rB else 1.0
            step = dt / .22 * (1 - SLOW)
            rate += max(-step, min(step, tg - rate))
            if rate < .9 and vs is None: vs = v
            if vs is not None and ve is None and rate >= .9 and r >= rB: ve = v
            r += rate * dt
        v += dt; n += 1
    return tab, vs, ve
def v_of(tab, r): return next((i / 60 for i, x in enumerate(tab) if x >= r), D)
lo, hi = 7.2, tC - .05
for _ in range(30):
    mid = (lo + hi) / 2
    if v_of(clock(mid)[0], tC) > target: lo = mid
    else: hi = mid
rA = round((lo + hi) / 2, 3)
RT, vS0, vS1 = clock(rA)
V = lambda r: v_of(RT, r)                                    # video time of a race time
vP, vM, vC, vGm, vCh = V(tP), V(tM), V(tC), V(tGm), V(tCh)

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

# ---------------------------------------------------------------- headlines (at most 2 lines, plain ink, no boxes)
HEADS = []
def head(i, t_in, t_out, l1, l2="", logos=(), t2=None, size=None):
    wl = len(logos) * 86
    fs = min(84, 940 / max((tw(l1) + wl * 100 / 84) / 100, tw(l2) / 100 if l2 else 0.01))
    if size: fs = min(fs, size)
    lg = "".join(logo(k, round(fs * .86), "hlg") for k in logos)
    l2h = f'<div class="hl2" id="h{i}b">{l2}</div>' if l2 else ""
    HEADS.append(f'<div class="hd" id="h{i}" style="font-size:{fs:.1f}px;line-height:{fs * .98:.1f}px"><div class="hl1">{lg}<span>{l1}</span></div>{l2h}</div>')
    if t_in is not None:
        fin(f"#h{i}", t_in)
        if l2 and t2 is not None:
            js(f"tl.fromTo('#h{i}b',{{opacity:0,x:34}},{{opacity:1,x:0,duration:.3,ease:'power3.out',immediateRender:false}},{t2:.3f});")
    if t_out is not None: fout(f"#h{i}", t_out - .24)
head(0, None, s(2) - .08, "FIVE AIs RACE,", "ONE HITS THE WALL.")
head(1, s(2), s(3) - .06, "SAME JOB FOR EACH AI")
head(2, s(3), T0 - .04, "HANDS OFF.")
HEADS.append('<div class="hd go" id="hgo"><div class="hl1"><span>GO!</span></div></div>')
js(f"tl.fromTo('#hgo',{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.3,ease:'power3.out',immediateRender:false}},{T0:.3f});")
js(f"tl.to('#hgo',{{opacity:0,scale:1.25,duration:.26,ease:'power2.in'}},{ROLL[0] - .34:.3f});")
for c, k in enumerate(NAMES):                                # roll call, one name at a time
    kk = IDS[c]; t1 = ROLL[c + 1] if c < 4 else min(e(4) + .1, vP - .3)
    head(10 + c, ROLL[c] - .06, t1 - .02, NAME[kk].upper(), logos=(kk,))
head(5, max(vP + .05, s(5) - .05), s(6) - .02, "PERPLEXITY", "STOPS DEAD", logos=("perplexity",))
head(6, s(6) + .02, s(7) - .02, "META AI", "HITS THE WALL", logos=("meta",), t2=max(s(6) + .25, vM - .05))
head(7, s(7) + .02, s(8) - .02, "NECK AND NECK", logos=("claude", "gemini"))
head(8, s(8) + .02, s(9) - .02, "CLAUDE", "PULLS AHEAD", logos=("claude",), t2=vC)
head(9, s(9) + .02, max(s(10), vCh + .1), "CHATGPT", "TAKES ITS TIME", logos=("chatgpt",))
tW = max(s(10), vCh + .1) + .04                              # winner moment
head(20, tW, s(11) - .04, "CLAUDE WINS", "GEMINI: 2 TENTHS BEHIND", logos=("claude",), t2=tW + .9)
head(21, s(11) + .02, s(13) - .04, "SEND IT TO A FRIEND", "SEE WHO THEY PICK")
head(22, s(13) + .02, tF + .1, "NEXT: A MAZE")
fin("#h0", tF + .35, .45)

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
 <path d="{outer} {inner}" class="shd" fill="{INK}" fill-rule="evenodd" transform="translate(9 9)"/>
 <path d="{outer} {inner}" fill="{ROAD}" fill-rule="evenodd"/>
 <polyline points="{pts(CLN)} {CLN[0][0]},{CLN[0][1]}" fill="none" stroke="{INK}" stroke-opacity=".2" stroke-width="3" stroke-dasharray="16 18"/>
 <rect x="{fl[0] - 7:.1f}" y="{fl[1]:.1f}" width="14" height="{fr_[1] - fl[1]:.1f}" fill="#fff"/>{cheq}
 <g filter="url(#wob)" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"><path d="{outer}"/><path d="{inner}"/></g>
</svg>'''
trails = '<svg class="trs" viewBox="0 0 950 808" width="950" height="808">' + "".join(
    f'<path class="trl" d="{TRD[c]}" stroke="{COL[k]}" stroke-dasharray="{CLEN[c][STOP[k]] + 2:.1f}" stroke-dashoffset="{CLEN[c][STOP[k]] + 2:.1f}"/>' for c, k in enumerate(IDS)) + "</svg>"
def car(c, k):
    return f'''<div class="car" data-c="{c}"><div class="cs"><div class="cb"><svg viewBox="-40 -24 80 48" width="80" height="48">
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
for i in range(7):                                          # Meta AI touches the wall: a small bump
    an = ma + math.pi + random.uniform(-1.3, 1.3)
    PUFF.append([round(tM + .02 * i, 3), NOSE[0], NOSE[1], round(math.cos(an) * random.uniform(14, 30), 1), round(math.sin(an) * random.uniform(14, 30), 1), round(random.uniform(10, 17), 1)])
px_, py_ = FR["perplexity"][STOP["perplexity"]][:2]
fx = "".join('<div class="pf"></div>' for _ in range(len(PUFF) + 10))
star = "M0 -30 L7 -9 L27 -15 L13 2 L30 16 L8 12 L3 32 L-7 13 L-27 20 L-14 2 L-30 -12 L-9 -10Z"
qmark = '<svg class="mk qm" viewBox="-20 -30 40 60"><path d="M-10 -12 C-10 -28 12 -28 12 -12 C12 -2 1 -3 1 9" pathLength="1"/><circle cx="1" cy="21" r="3.6"/></svg>'
xmark = '<svg class="mk xm" viewBox="-20 -20 40 40"><path d="M-14 -14 L14 14 M14 -14 L-14 14" pathLength="1"/></svg>'
world = f'''{road}{trails}
<svg class="lens" viewBox="0 0 950 808" width="950" height="808"><rect class="lr" x="0" y="0" width="10" height="10" rx="6"/></svg>
<div class="fx">{fx}<svg class="star" viewBox="-34 -34 68 68"><path d="{star}"/></svg></div>
<div class="cars">{"".join(car(c, k) for c, k in enumerate(IDS))}</div>
<div class="mks">{qmark}{xmark}</div>'''

# ---------------------------------------------------------------- markup: HUD, infield items, result card
TX, TY0, TP = 65, 520, 68                                    # tower: left, first row top, row pitch
tower = '<div class="lap" id="lap"><span id="lapt">LAP 1 OF 2</span><i></i></div>'
for i in range(5): tower += f'<div class="tn" style="top:{TY0 + i * TP + 4}px">{i + 1}</div>'
for c, k in enumerate(IDS):
    tower += f'''<div class="trw" id="tr{c}">{badge(k, 58, "tb")}<div class="dots"><i class="d1"></i><i class="d2"></i></div>
 <svg class="tm" viewBox="-20 -20 40 40">{'<path d="M-13 1 L-4 11 L14 -12" pathLength="1"/>' if k in FIN else '<path d="M-9 -7 C-9 -19 10 -19 10 -7 C10 1 1 0 1 8 M1 16 V16.5" pathLength="1"/>' if k == "perplexity" else '<path d="M-12 -12 L12 12 M12 -12 L-12 12" pathLength="1"/>'}</svg></div>'''
# infield: world x 460-740, y 290-600 is clear of the road (measured on track.json)
IX, IY, IW, IH = 65 + 460, 440 + 290, 280, 310
note = f'''<div id="note"><div class="tape t1" data-decor></div><div class="tape t2" data-decor></div>
 <div class="nt">Teach this car<br>to race.</div>
 <svg class="ncar" viewBox="-44 -26 88 52"><rect x="-28" y="-23" width="15" height="9" rx="3"/><rect x="13" y="-23" width="15" height="9" rx="3"/><rect x="-28" y="14" width="15" height="9" rx="3"/><rect x="13" y="14" width="15" height="9" rx="3"/><rect class="nb" x="-36" y="-17" width="72" height="34" rx="13"/></svg>
 <div class="nrow">{"".join(f'<div class="nl" id="nl{c}"><svg viewBox="0 0 40 46"><path d="M20 2 V36 M8 24 L20 38 L32 24" pathLength="1"/></svg>{badge(k, 84)}</div>' for c, k in enumerate(IDS))}</div></div>'''
lights = '<div id="lights">' + "".join(f'<i id="lt{i}"></i>' for i in range(5)) + '</div><div id="pick">PICK ONE,<br>COMMENT IT</div>'
stamp = '''<div id="stamp"><svg viewBox="0 0 120 90"><path d="M14 86 V8" stroke-width="7"/><path d="M14 10 Q40 0 62 12 T110 10 V54 Q86 64 62 54 T14 54Z" stroke-width="5" fill="#fbfbf8"/><path d="M14 32 Q40 22 62 33 T110 32 M46 5 V52 M78 16 V58" stroke-width="4"/></svg><span>RACE #1</span><i></i></div>'''
inset = f'<div id="inset"><div class="tape t2" data-decor></div><div id="ivw"></div><div id="slow"><b></b>SLOW MOTION</div></div>'
rays = "".join(f'<path d="M{math.cos(i * math.pi / 8) * 112:.1f} {math.sin(i * math.pi / 8) * 112:.1f} L{math.cos(i * math.pi / 8) * (140 if i % 2 else 128):.1f} {math.sin(i * math.pi / 8) * (140 if i % 2 else 128):.1f}"/>' for i in range(16))
winner = f'<div id="win"><svg class="rays" viewBox="-145 -145 290 290">{rays}</svg>{badge("claude", 196)}</div>'
# maze teaser: seeded depth-first maze, drawn as one stroke
random.seed(99); MN, MC = 5, 44
seen = {(0, 0)}; open_ = set(); stack = [(0, 0)]; first_dead = None; path_ = [(0, 0)]; best = []
while stack:
    cx_, cy_ = stack[-1]
    nb = [(cx_ + dx, cy_ + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= cx_ + dx < MN and 0 <= cy_ + dy < MN and (cx_ + dx, cy_ + dy) not in seen]
    if nb:
        n_ = random.choice(nb); open_.add(frozenset(((cx_, cy_), n_))); seen.add(n_); stack.append(n_)
        if len(stack) > len(best): best = list(stack)
    else: stack.pop()
md = f"M0 0 H{MN * MC} V{MN * MC} H{MC} M0 {MN * MC} V0"       # outer wall, entrance bottom-left
for x in range(MN):
    for y in range(MN):
        if x + 1 < MN and frozenset(((x, y), (x + 1, y))) not in open_: md += f" M{(x + 1) * MC} {y * MC} V{(y + 1) * MC}"
        if y + 1 < MN and frozenset(((x, y), (x, y + 1))) not in open_: md += f" M{x * MC} {(y + 1) * MC} H{(x + 1) * MC}"
# a wandering line from the entrance (bottom-left cell) along the longest branch found: "who gets lost"
random.seed(99); seen = {(0, MN - 1)}; stack = [(0, MN - 1)]; best = [(0, MN - 1)]
adj = lambda a_, b_: frozenset((a_, b_)) in open_
while stack:
    c_ = stack[-1]
    nb = [(c_[0] + dx, c_[1] + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (c_[0] + dx, c_[1] + dy) not in seen and adj(c_, (c_[0] + dx, c_[1] + dy))]
    if nb:
        stack.append(nb[0]); seen.add(nb[0])
        if len(stack) > len(best): best = list(stack)
    else: stack.pop()
wd = f"M{MC / 2} {MN * MC + 26} " + " ".join(f"L{x * MC + MC / 2} {y * MC + MC / 2}" for x, y in best[:12])
maze = f'''<div id="maze"><svg viewBox="-8 -8 {MN * MC + 16} {MN * MC + 44}"><path id="mzw" d="{md}" pathLength="1"/><path id="mzp" d="{wd}" pathLength="1"/></svg>
 <div class="mzl">{"".join(f'<span id="mz{c}">{badge(k, 40)}</span>' for c, k in enumerate(IDS))}</div></div>'''
ROWS = [("claude", "1", f"{RES['claude']['timeS']:.2f} s"), ("gemini", "2", f"{RES['gemini']['timeS']:.2f} s"), ("chatgpt", "3", f"{RES['chatgpt']['timeS']:.2f} s"),
        ("meta", "&ndash;", "touched the wall"), ("perplexity", "&ndash;", "stuck in the bend")]
card = '<div id="card"><div class="tape t1" data-decor></div><div class="tape t2" data-decor></div><div class="ct">AI RACE #1 &middot; 2 LAPS</div>'
for i, (k, pl, res) in enumerate(ROWS):
    card += f'<div class="cr" id="cr{i}" style="top:{118 + i * 104}px"><span class="cp">{pl}</span>{badge(k, 78)}<span class="cn">{NAME[k]}</span><span class="cv">{res}</span>{"<i></i>" if i == 0 else ""}</div>'
card += '<div class="cf" id="cf">race your own AI: link in bio<i></i></div></div>'
arrow = '<svg id="arrow" viewBox="0 0 160 130" data-decor><path d="M10 10 C30 70 70 96 128 104" pathLength="1"/><path d="M104 82 L132 105 L98 118" pathLength="1"/></svg>'
markup = f'''
<div class="bgw" data-decor></div>
<div id="cam">
 <div id="world" class="world">{world}</div>
 {arrow}{stamp}{note}{lights}{inset}{winner}{maze}
 <div id="tower">{tower}</div>
 {"".join(HEADS)}
 {card}
</div>'''

CSS = '''
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;color:INK}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}
.bgw{position:absolute;left:-20px;top:-20px;width:1120px;height:1960px;background:#ecebe5 url(assets/bg.jpg);background-size:1120px 1960px}
#cam{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 844px}
.world{position:absolute;left:65px;top:440px;width:950px;height:808px;transform-origin:0 0;z-index:0}
#arrow,#stamp,#note,#lights,#pick,#inset,#win,#maze{z-index:2} #tower,.hd{z-index:3} #card{z-index:5}
.world svg.road,.world svg.trs,.world svg.lens{position:absolute;left:0;top:0;overflow:visible}
.trl{fill:none;stroke-width:6;stroke-linecap:round;stroke-linejoin:round;opacity:0}
.lr{fill:none;stroke:RED;stroke-width:4;stroke-dasharray:9 8;opacity:0}
.cars,.fx,.mks{position:absolute;left:0;top:0;width:0;height:0}
.car{position:absolute;left:0;top:0;width:0;height:0;will-change:transform}
.cs{position:absolute;left:0;top:0;width:0;height:0}
.cb{position:absolute;left:-40px;top:-24px;width:80px;height:48px}
.cb svg{display:block}
.bdg{position:relative;border-radius:50%;background:#fff;border:3.5px solid INK;display:flex;align-items:center;justify-content:center;flex:none}
.bdg .lg{display:block}
.pxl{display:block;overflow:hidden;flex:none} .pxl img{display:block;max-width:none}
.car .bd{position:absolute;left:-25px;top:-25px}
.pf{position:absolute;left:0;top:0;width:20px;height:20px;margin:-10px 0 0 -10px;border-radius:50%;background:#fbf8ee;border:2px solid INK;opacity:0}
.star{position:absolute;left:0;top:0;width:68px;height:68px;margin:-34px 0 0 -34px;overflow:visible;opacity:0}
.star path{fill:#FFD23F;stroke:INK;stroke-width:4;stroke-linejoin:round}
.mk{position:absolute;left:0;top:0;overflow:visible;opacity:0}
.mk path{fill:none;stroke:RED;stroke-width:7;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1}
.mk circle{fill:RED}
.qm{width:40px;height:60px;margin:-30px 0 0 -20px} .xm{width:40px;height:40px;margin:-20px 0 0 -20px}
.w2 .lens,.w2 .shd{display:none} .w2 .trl{stroke-width:2.6}
#arrow{position:absolute;left:92px;top:884px;width:150px;height:122px;overflow:visible}
#arrow path{fill:none;stroke:RED;stroke-width:9;stroke-linecap:round;stroke-linejoin:round}
.hd{position:absolute;left:65px;top:283px;font-weight:900;letter-spacing:-.03em;white-space:nowrap;opacity:0;transform-origin:0 50%}
#h0{opacity:1}
.hl1{display:flex;align-items:center} .hlg{margin-right:.16em;flex:none} .hl2{display:block}
.hd.go{font-size:150px;line-height:150px;top:286px}
#h20 .hl2{font-size:.56em;line-height:1.25em;letter-spacing:-.02em}
#tower{position:absolute;left:0;top:0;width:1080px;height:1920px}
.lap{position:absolute;left:67px;top:466px;font-weight:800;font-size:31px;line-height:36px;letter-spacing:-.01em;white-space:nowrap;opacity:0}
.lap i{position:absolute;left:0;right:0;bottom:-7px;height:5px;border-radius:3px;background:INK}
.tn{position:absolute;left:65px;width:34px;height:50px;font-weight:900;font-size:42px;line-height:50px;text-align:center}
.trw{position:absolute;left:112px;top:520px;height:58px;display:flex;align-items:center;gap:12px;will-change:transform}
.dots{display:flex;gap:7px} .dots i{display:block;width:17px;height:17px;border-radius:50%;border:3.5px solid INK;background:PAPER}
.tm{width:38px;height:38px;overflow:visible;opacity:0}
.tm path{fill:none;stroke:INK;stroke-width:7;stroke-linecap:round;stroke-linejoin:round}
.tape{position:absolute;width:130px;height:40px;background:rgba(232,221,186,.86);border:1px solid rgba(0,0,0,.14);z-index:3}
.tape.t1{right:-34px;top:-12px;transform:rotate(34deg)} .tape.t2{left:-34px;bottom:-6px;transform:rotate(34deg)}
#stamp{position:absolute;left:IXpx;top:IYpx;width:IWpx;height:IHpx;display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(-5deg)}
#stamp svg{width:132px;height:99px;overflow:visible;margin-bottom:10px;transform-origin:12% 100%} #stamp svg path{fill:none;stroke:INK;stroke-linecap:round;stroke-linejoin:round}
#stamp span{font-weight:900;font-size:62px;line-height:64px;letter-spacing:-.03em;white-space:nowrap}
#stamp i{display:block;width:230px;height:8px;border-radius:4px;background:RED;margin-top:8px;transform-origin:0 50%}
#note{position:absolute;left:372px;top:560px;width:600px;height:430px;background:PAPER;border:6px solid INK;border-radius:8px;box-shadow:12px 12px 0 INK;opacity:0;transform-origin:50% 50%}
.nt{position:absolute;left:34px;top:26px;font-weight:900;font-size:66px;line-height:68px;letter-spacing:-.03em;white-space:nowrap}
.ncar{position:absolute;right:26px;top:150px;width:132px;height:78px;overflow:visible;transform:rotate(-8deg)} .ncar rect{fill:INK} .ncar .nb{fill:#FFD23F;stroke:INK;stroke-width:3.5}
.nrow{position:absolute;left:30px;right:30px;bottom:22px;display:flex;justify-content:space-between}
.nl{display:flex;flex-direction:column;align-items:center;opacity:0} .nl svg{width:40px;height:46px;overflow:visible;margin-bottom:6px}
.nl path{fill:none;stroke:INK;stroke-width:6;stroke-linecap:round;stroke-linejoin:round}
#lights{position:absolute;left:IXpx;top:LYpx;width:IWpx;display:flex;justify-content:space-between;opacity:0}
#lights i{display:block;width:46px;height:46px;border-radius:50%;border:5px solid INK;background:PAPER;box-shadow:4px 4px 0 INK}
#pick{position:absolute;left:IXpx;top:PYpx;width:IWpx;text-align:center;font-weight:900;font-size:38px;line-height:42px;letter-spacing:-.02em;opacity:0}
#inset{position:absolute;left:IXpx;top:IYpx;width:IWpx;height:IHpx;background:PAPER;border:6px solid INK;border-radius:10px;box-shadow:10px 10px 0 INK;opacity:0;transform-origin:20% 90%}
#ivw{position:absolute;inset:0;overflow:hidden;border-radius:4px;background:#ecebe5}
#ivw .world{left:0;top:0}
#slow{position:absolute;left:12px;top:8px;font-weight:900;font-size:30px;line-height:36px;letter-spacing:-.01em;color:RED;white-space:nowrap;opacity:0;display:flex;align-items:center;gap:8px;
 text-shadow:0 0 0 #fff,2px 2px 0 #fbfbf8,-2px 2px 0 #fbfbf8,2px -2px 0 #fbfbf8,-2px -2px 0 #fbfbf8,0 3px 0 #fbfbf8,3px 0 0 #fbfbf8,-3px 0 0 #fbfbf8,0 -3px 0 #fbfbf8}
#slow b{display:block;width:16px;height:16px;border-radius:50%;background:RED;border:2px solid #fbfbf8}
#win{position:absolute;left:WXpx;top:WYpx;width:196px;height:196px;opacity:0}
#win .bdg{border-width:7px;box-shadow:9px 9px 0 INK}
.rays{position:absolute;left:-47px;top:-47px;width:290px;height:290px;overflow:visible} .rays path{stroke:#D97757;stroke-width:9;stroke-linecap:round}
#maze{position:absolute;left:IXpx;top:IYpx;width:IWpx;height:IHpx;opacity:0}
#maze svg{position:absolute;left:22px;top:0;width:236px;height:264px;overflow:visible}
#mzw{fill:none;stroke:INK;stroke-width:6;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1}
#mzp{fill:none;stroke:RED;stroke-width:6;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1}
.mzl{position:absolute;left:0;right:0;bottom:-4px;display:flex;justify-content:center;gap:6px} .mzl>span{display:block;opacity:0} .mzl .bdg{border-width:3px}
#card{position:absolute;left:100px;top:468px;width:880px;height:762px;background:PAPER;border:6px solid INK;border-radius:10px;box-shadow:14px 14px 0 INK;opacity:0;transform-origin:50% 0%}
.ct{position:absolute;left:38px;top:30px;font-weight:900;font-size:52px;line-height:60px;letter-spacing:-.03em;white-space:nowrap}
.cr{position:absolute;left:38px;right:38px;height:92px;display:flex;align-items:center;opacity:0;border-top:4px solid rgba(15,15,15,.14)}
.cp{width:56px;font-weight:900;font-size:52px;line-height:60px;text-align:center;margin-right:14px}
.cn{font-weight:900;font-size:50px;line-height:60px;letter-spacing:-.03em;margin-left:20px;white-space:nowrap}
.cv{margin-left:auto;font-weight:800;font-size:38px;line-height:60px;letter-spacing:-.01em;white-space:nowrap}
.cr i{position:absolute;left:0;right:0;bottom:2px;height:9px;border-radius:5px;background:#D97757;transform-origin:0 50%;transform:scaleX(0)}
.cf{position:absolute;left:40px;top:664px;font-weight:800;font-size:38px;line-height:48px;white-space:nowrap;opacity:0}
.cf i{position:absolute;left:0;right:0;bottom:-8px;height:6px;border-radius:3px;background:INK;transform-origin:0 50%;transform:scaleX(0)}
'''
LY = IY + 78; PY = IY + 160
for a_, b_ in (("IX", IX), ("IY", IY), ("IW", IW), ("IH", IH), ("LY", LY), ("PY", PY), ("WX", IX + 42), ("WY", IY + 57), ("INK", INK), ("PAPER", PAPER), ("RED", RED)):
    CSS = CSS.replace(a_, str(b_))

# ---------------------------------------------------------------- timeline (GSAP: text, cards, camera; cars are driven by render())
vI0 = V(3.7); vI1 = vS1 + .45                               # close-up card: opens before the hairpin stops, closes after the slow motion
vPan = max(vM + 1.0, s(7) + .1)                             # the close-up slides from the hairpin to the finish line
tG = s(13) + .15                                            # the cars roll back to the grid (1.3 s)
js(f"tl.fromTo('#cam',{{scale:1,rotation:0}},{{scale:1.014,rotation:.22,duration:{D / 4:.3f},ease:'sine.inOut',yoyo:true,repeat:3}},0);")
js(f"tl.fromTo('.bgw',{{x:0,y:0}},{{x:-14,y:-12,duration:{D / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},0);")
# beat 1: hook. The arrow points at the hairpin wall, the flag waves, the headline breathes
js(f"tl.fromTo('#arrow',{{x:0,y:0}},{{x:10,y:8,duration:.38,ease:'sine.inOut',yoyo:true,repeat:{2 * max(1, round((s(3) - .2) / .76)) - 1}}},0);")
js(f"tl.to('#arrow',{{opacity:0,duration:.3,ease:'sine.inOut'}},{s(3) - .1:.3f});")
js(f"tl.fromTo('#stamp svg',{{rotation:-5}},{{rotation:7,duration:.5,ease:'sine.inOut',yoyo:true,repeat:{2 * max(1, round(s(2) / 1.0)) - 1}}},0);")
tw_ = W("wall", 1); tw_ = tw_ if tw_ is not None else s(1) + .72 * (e(1) - s(1))
js(f"tl.fromTo('#h0 .hl2',{{scale:1}},{{scale:1.05,transformOrigin:'0 50%',duration:.22,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tw_:.3f});")
sfx("subhit.ogg", .05, -6); sfx("impactsoft.ogg", tw_, -9)
# beat 2: the same job goes to each AI (note over the far side of the road; the cars on the grid stay clear)
fout("#stamp", s(2) - .1)
js(f"tl.fromTo('#note',{{opacity:0,y:90,scale:.6,rotation:7}},{{opacity:1,y:0,scale:1,rotation:-2,duration:.55,ease:'power3.out',immediateRender:false}},{s(2) - .05:.3f});")
js(f"tl.fromTo('.ncar',{{x:-30}},{{x:16,duration:{(s(3) - s(2)) / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{s(2):.3f});")
te = W("each", 2); te = te if te is not None else s(2) + .12 * (e(2) - s(2))
t0n = max(s(2) + .45, te + .3); stepn = min(.22, (e(2) - .3 - t0n) / 5)
for c in range(5):
    t = t0n + c * stepn
    js(f"tl.fromTo('#nl{c}',{{opacity:0,y:-26,scale:.7}},{{opacity:1,y:0,scale:1,duration:.34,ease:'power3.out',immediateRender:false}},{t:.3f});")
    sfx("pop_a.ogg" if c % 2 == 0 else "pop_b.ogg", t, -10)
js(f"tl.to('#note',{{rotation:-.6,y:-8,duration:{max(.4, s(3) - .4 - (t0n + 5 * stepn)):.3f},ease:'sine.inOut'}},{t0n + 5 * stepn:.3f});")
js(f"tl.to('#note',{{opacity:0,y:-70,scale:.7,rotation:5,duration:.4,ease:'power3.in'}},{s(3) - .42:.3f});")
sfx("whoosh_b.ogg", s(2) - .05, -10); sfx("whoosh_c.ogg", s(3) - .42, -11)
# beat 3: start lights, then Go
js(f"tl.fromTo('#lights',{{opacity:0,y:18}},{{opacity:1,y:0,duration:.3,ease:'power2.out',immediateRender:false}},{s(3) - .05:.3f});")
fin("#pick", s(3) + .12)
stepl = max(.12, (T0 - .16 - s(3) - .1) / 5)
for i in range(5):
    t = s(3) + .1 + i * stepl
    js(f"tl.to('#lt{i}',{{backgroundColor:'{RED}',scale:1.16,duration:.14,ease:'power2.out'}},{t:.3f});")
    js(f"tl.to('#lt{i}',{{scale:1,duration:.2,ease:'sine.inOut'}},{t + .14:.3f});")
    sfx("tick.ogg", t, -8)
js(f"tl.to('#lights i',{{backgroundColor:'#19B35A',scale:1.12,duration:.12,ease:'power2.out'}},{T0 - .02:.3f});")
js(f"tl.to('#lights',{{opacity:0,y:-16,duration:.35,ease:'power2.inOut'}},{T0 + .55:.3f});")
fout("#pick", T0 + .5); sfx("whoosh_a.ogg", T0 - .03, -6)
js(f"tl.fromTo('#lap',{{opacity:0,x:24}},{{opacity:1,x:0,duration:.35,ease:'power2.out',immediateRender:false}},{T0 + .85:.3f});")
fin("#stamp", T0 + 1.0); fout("#stamp", vI0 - .15)
js(f"tl.fromTo('#stamp svg',{{rotation:-5}},{{rotation:7,duration:.5,ease:'sine.inOut',yoyo:true,repeat:{2 * max(1, round((vI0 - T0 - 1) / 1.0)) - 1},immediateRender:false}},{T0 + 1.0:.3f});")
for c in range(5): sfx("select.ogg", ROLL[c], -12)
# race: close-up card on the hairpin, then on the finish line
js(f"tl.fromTo('#inset',{{opacity:0,scale:.5,rotation:-6}},{{opacity:1,scale:1,rotation:-1.2,duration:.45,ease:'power3.out',immediateRender:false}},{vI0:.3f});")
js(f"tl.fromTo('.lr',{{opacity:0}},{{opacity:1,duration:.3,ease:'sine.inOut',immediateRender:false}},{vI0:.3f});")
js(f"tl.to('#inset',{{rotation:1,duration:{(vI1 - vI0 - .5) / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},{vI0 + .45:.3f});")
js(f"tl.to('#inset',{{opacity:0,scale:.6,duration:.35,ease:'power2.in'}},{vI1:.3f});")
js(f"tl.to('.lr',{{opacity:0,duration:.3,ease:'sine.inOut'}},{vI1:.3f});")
sfx("whoosh_c.ogg", vI0, -12); sfx("toggle.ogg", vP - .25, -9); sfx("impactsoft.ogg", vM, -4); sfx("whoosh_c.ogg", vPan, -13)
# slow motion label: on screen for the whole slowed stretch
js(f"tl.fromTo('#slow',{{opacity:0}},{{opacity:1,duration:.15,ease:'sine.out',immediateRender:false}},{vS0 - .05:.3f});")
js(f"tl.fromTo('#slow b',{{opacity:1}},{{opacity:.25,duration:.3,ease:'sine.inOut',yoyo:true,repeat:{2 * max(1, round((vS1 - vS0) / .6)) - 1},immediateRender:false}},{vS0:.3f});")
js(f"tl.to('#slow',{{opacity:0,duration:.15,ease:'sine.in'}},{vS1 + .02:.3f});")
js(f"tl.to('#inset',{{borderColor:'{RED}',duration:.2,ease:'sine.inOut'}},{vS0 - .05:.3f});")
js(f"tl.to('#inset',{{borderColor:'{INK}',duration:.2,ease:'sine.inOut'}},{vS1:.3f});")
sfx("riser.ogg", vS0 - .3, -12); sfx("ding.ogg", vC, -7); sfx("click_a.ogg", vGm, -9); sfx("click_b.ogg", vCh, -9)
js(f"tl.to('#lap',{{opacity:0,duration:.3,ease:'sine.inOut'}},{vCh + .1:.3f});")
# winner
js(f"tl.fromTo('#win',{{opacity:0,scale:.4,rotation:-14}},{{opacity:1,scale:1,rotation:0,duration:.5,ease:'power3.out',immediateRender:false}},{tW:.3f});")
js(f"tl.fromTo('.rays',{{rotation:0}},{{rotation:50,duration:{s(11) - tW + .3:.3f},ease:'sine.inOut',immediateRender:false}},{tW:.3f});")
js(f"tl.fromTo('#win .bdg',{{scale:1}},{{scale:1.07,duration:.4,ease:'sine.inOut',yoyo:true,repeat:{2 * max(1, round((s(11) - tW - .5) / .8)) - 1},immediateRender:false}},{tW + .5:.3f});")
js(f"tl.to('#win',{{opacity:0,scale:.7,duration:.3,ease:'power2.in'}},{s(11) - .3:.3f});")
sfx("impactpunch.ogg", tW, -6)
# result card (the saveable card): rows land slowest result first, the winner last
tK = s(11) - .05
js(f"tl.to('#tower',{{opacity:0,duration:.3,ease:'sine.inOut'}},{tK - .1:.3f});")
js(f"tl.fromTo('#card',{{opacity:0,y:90,rotation:3,scale:1}},{{opacity:1,y:0,rotation:-1,duration:.5,ease:'power3.out',immediateRender:false}},{tK:.3f});")
sfx("whoosh_b.ogg", tK, -10)
for q, i in enumerate((4, 3, 2, 1, 0)):
    t = tK + .3 + q * .18 + (.14 if i == 0 else 0)
    js(f"tl.fromTo('#cr{i}',{{opacity:0,x:-46}},{{opacity:1,x:0,duration:.36,ease:'power3.out',immediateRender:false}},{t:.3f});")
    sfx("pop_a.ogg" if q % 2 == 0 else "pop_b.ogg", t, -10)
js(f"tl.to('#cr0 i',{{scaleX:1,duration:.5,ease:'power2.inOut'}},{tK + 1.4:.3f});")
js(f"tl.fromTo('#cr0 .bdg',{{scale:1}},{{scale:1.14,duration:.3,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tK + 1.4:.3f});")
hold = max(.8, s(13) - tK - .6)
js(f"tl.to('#card',{{rotation:.6,y:-8,duration:{hold / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},{tK + .55:.3f});")
for q, i in enumerate((3, 4, 2, 1)):                         # a slow wave keeps the list alive while it is read
    js(f"tl.fromTo('#cr{i} .bdg',{{rotation:0}},{{rotation:{-10 if q % 2 else 10},duration:.28,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tK + 2.0 + q * .34:.3f});")
fin("#cf", s(12) + .05)
js(f"tl.to('#cf i',{{scaleX:1,duration:.6,ease:'power2.inOut'}},{s(12) + .3:.3f});")
sfx("tick.ogg", s(12) + .05, -9)
for q, i in enumerate((0, 1, 2)):
    js(f"tl.fromTo('#cr{i} .cv',{{scale:1}},{{scale:1.1,transformOrigin:'100% 50%',duration:.24,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{s(12) + 1.0 + q * .22:.3f});")
js(f"tl.to('#card',{{opacity:0,scale:.82,y:-50,rotation:-4,duration:.36,ease:'power2.in'}},{s(13) - .12:.3f});")
sfx("whoosh_c.ogg", s(13) - .12, -10)
# beat 13: cars roll back to the grid (render()), the maze sketch draws itself, then the frame-0 layout returns
js(f"tl.to('#tower',{{opacity:1,duration:.4,ease:'sine.inOut'}},{tG + .3:.3f});")
js(f"tl.fromTo('#maze',{{opacity:0,rotation:-4}},{{opacity:1,rotation:2,duration:.4,ease:'power2.out',immediateRender:false}},{s(13) + .35:.3f});")
js(f"tl.to('#mzw',{{strokeDashoffset:0,duration:1.2,ease:'power2.inOut'}},{s(13) + .4:.3f});")
for c in range(5):
    js(f"tl.fromTo('#mz{c}',{{opacity:0,y:24}},{{opacity:1,y:0,duration:.3,ease:'power3.out',immediateRender:false}},{s(13) + 1.45 + c * .13:.3f});")
js(f"tl.to('#mzp',{{strokeDashoffset:0,duration:{max(.6, tF - s(13) - 2.1):.3f},ease:'sine.inOut'}},{s(13) + 2.0:.3f});")
js(f"tl.to('#maze',{{rotation:-2,duration:{max(.5, tF - s(13) - .8):.3f},ease:'sine.inOut'}},{s(13) + .75:.3f});")
js(f"tl.to('#maze',{{opacity:0,scale:.8,duration:.3,ease:'power2.in'}},{tF:.3f});")
fin("#stamp", tF + .35, .45)
js(f"tl.set('#stamp svg',{{rotation:-5}},{tF:.3f});")
js(f"tl.fromTo('#arrow',{{opacity:0,x:-20,y:-20}},{{opacity:1,x:0,y:0,duration:.45,ease:'power2.out',immediateRender:false}},{tF + .35:.3f});")
sfx("whoosh_c.ogg", tG, -11)

# ---------------------------------------------------------------- render(): the race, driven by the timeline clock
DATA = dict(T0=T0, D=D, NF=NF, RT=[round(x, 4) for x in RT], X=X, Y=Y, A=A, CL=CLEN, TL=[CLEN[c][STOP[k]] + 2 for c, k in enumerate(IDS)],
            RK=RANKEV, GRID=GRID, SLOT={str(k): v for k, v in SLOT.items()}, LAPF=[LAPF[k] for k in IDS], STOP=[STOP[k] for k in IDS],
            FINC=[1 if k in FIN else 0 for k in IDS], PUFF=PUFF, NOSE=NOSE, tP=tP, tM=tM, iP=IDS.index("perplexity"), iM=IDS.index("meta"), iC=IDS.index("claude"),
            ROLL=[round(x, 3) for x in ROLL], tW=round(tW, 3), tG=round(tG, 3), vPan=round(vPan, 3), TP=TP, IW=IW, IH=IH,
            HAIR=[173, 626], FINL=[292, 700], Z=2.2,
            MK=[dict(q=[62, round(py_, 1), 1], x=[237, 626, .85]), dict(q=[round(px_ - 30, 1), round(py_ - 4, 1), .42], x=[222, 628, .42])])
RJS = r'''
const Dt=__DATA__;
const ez=p=>{p=p<0?0:p>1?1:p;return p*p*(3-2*p)}, lerp=(a,b,t)=>a+(b-a)*t, bump=p=>p>0&&p<1?Math.sin(Math.PI*p):0;
const angd=(to,from)=>{let d=(to-from)%(2*Math.PI);if(d>Math.PI)d-=2*Math.PI;if(d<-Math.PI)d+=2*Math.PI;return d};
function Rv(v){const i=Math.max(0,v*60),k=Math.min(Dt.RT.length-2,Math.floor(i));return Dt.RT[k]+(Dt.RT[k+1]-Dt.RT[k])*Math.min(1,i-k)}
const main=document.querySelector('#world'), cl=main.cloneNode(true); cl.removeAttribute('id'); cl.classList.add('w2'); document.querySelector('#ivw').appendChild(cl);
const mk=(root,k,vi)=>({root,k,vi,cars:[...root.querySelectorAll('.car')].map(el=>({el,cb:el.querySelector('.cb'),bd:el.querySelector('.bd')})),
  tr:[...root.querySelectorAll('.trl')],pf:[...root.querySelectorAll('.pf')],star:root.querySelector('.star'),qm:root.querySelector('.qm'),xm:root.querySelector('.xm'),
  qp:root.querySelector('.qm path'),xp:root.querySelector('.xm path')});
const views=[mk(main,1,0),mk(cl,.5,1)];
views.forEach(vw=>vw.root.querySelectorAll('.cs').forEach(el=>{el.style.transform='scale('+vw.k+')'}));
const rows=[0,1,2,3,4].map(c=>{const el=document.querySelector('#tr'+c);return {el,tb:el.querySelector('.tb'),d1:el.querySelector('.d1'),d2:el.querySelector('.d2'),tm:el.querySelector('.tm'),tp:el.querySelector('.tm path')}});
const lapt=document.querySelector('#lapt'), lr=document.querySelector('#world .lr'); let lapNow='';
const NP=Dt.PUFF.length;
function rankAt(c,fr){const E=Dt.RK[c];let k=0;while(k+1<E.length&&E[k+1][0]<=fr)k++;const prev=k>0?E[k-1][1]:E[k][1];return prev+(E[k][1]-prev)*ez((fr-E[k][0])/22)}
function render(v){
  const r=Rv(v), fr=r*60, wEnd=ez((v-Dt.tG)/1.3), wg=v<Dt.T0?1:1-ez(r/1.2), w=Math.max(wg,wEnd), idle=v<Dt.T0?1:wEnd;
  const P=[];
  for(let c=0;c<5;c++){
    const i=Math.min(Math.floor(fr),Dt.NF-1), f=Math.min(1,fr-i);
    let x=lerp(Dt.X[c][i],Dt.X[c][i+1],f), y=lerp(Dt.Y[c][i],Dt.Y[c][i+1],f), a=lerp(Dt.A[c][i],Dt.A[c][i+1],f);
    const S=Dt.SLOT[c];
    if(S&&fr>S.f){const p=Math.min(1,(r-S.f/60)/S.T), q=1-(1-p)*(1-p); x=lerp(x,S.x,q); y=lerp(y,S.y,q); a=a+angd(S.a,a)*q}
    if(c===Dt.iM&&r>Dt.tM){const q=r-Dt.tM; a+=.2*Math.exp(-3.2*q)*Math.sin(17*q)}
    const G=Dt.GRID[c]; x=lerp(x,G[0],w); y=lerp(y,G[1],w); a=a+angd(G[2],a)*w;
    x+=Math.sin(v*41+c*1.7)*.9*idle; y+=Math.cos(v*35+c*2.3)*.9*idle;
    let pu=1+.38*bump((v-Dt.ROLL[c])/.5);
    if(c===Dt.iC) pu+=.5*bump((v-Dt.tW)/.7);
    if(c===Dt.iP&&r>Dt.tP) pu+=.06*Math.sin((r-Dt.tP)*7)*(1-wEnd);
    const rk=rankAt(c,fr)*(1-wEnd)+c*wEnd;
    P.push({x,y,a,pu,rk});
    const off=Dt.TL[c]-lerp(Dt.CL[c][i],Dt.CL[c][i+1],f), to=ez((r-.5)/.6)*(1-wEnd)*.9;
    for(const vw of views){
      const e=vw.cars[c];
      e.el.style.transform='translate('+x.toFixed(2)+'px,'+y.toFixed(2)+'px)'; e.el.style.zIndex=10-Math.round(rk);
      e.cb.style.transform='rotate('+a.toFixed(4)+'rad)'; e.bd.style.transform='scale('+pu.toFixed(3)+')';
      vw.tr[c].style.strokeDashoffset=off.toFixed(1); vw.tr[c].style.opacity=to.toFixed(3);
    }
    // tower row
    const R=rows[c], out=(c===Dt.iP&&r>Dt.tP)||(c===Dt.iM&&r>Dt.tM), tS=c===Dt.iP?Dt.tP:c===Dt.iM?Dt.tM:Dt.STOP[c]/60;
    const done=Dt.FINC[c]?fr>=Dt.STOP[c]:out, mo=done?ez((r-tS)/.3)*(1-wEnd):0;
    R.el.style.transform='translateY('+(rk*Dt.TP).toFixed(2)+'px)'; R.el.style.zIndex=10-Math.round(rk);
    R.tb.style.transform='scale('+(1+.3*bump((v-Dt.ROLL[c])/.5)+(c===Dt.iC?.3*bump((v-Dt.tW)/.7):0)).toFixed(3)+')';
    R.tb.style.opacity=(out?1-.5*ez((r-tS)/.4)*(1-wEnd):1).toFixed(3);
    const L=Dt.LAPF[c];
    R.d1.style.background=(L[0]!==undefined&&fr>=L[0]&&wEnd<.5)?'#0f0f0f':'#fbfbf8';
    R.d2.style.background=(L[1]!==undefined&&fr>=L[1]&&wEnd<.5)?'#0f0f0f':'#fbfbf8';
    R.d1.style.transform='scale('+(1+.5*bump(L[0]!==undefined?(fr-L[0])/20:-1)).toFixed(3)+')';
    R.d2.style.transform='scale('+(1+.5*bump(L[1]!==undefined?(fr-L[1])/20:-1)).toFixed(3)+')';
    R.tm.style.opacity=mo.toFixed(3); R.tp.style.strokeDasharray='1'; R.tp.style.strokeDashoffset=(1-mo).toFixed(3);
  }
  // lap counter: the leader's lap
  let lap=1; for(let c=0;c<5;c++){if(Dt.LAPF[c][0]!==undefined&&fr>=Dt.LAPF[c][0])lap=2}
  const lt='LAP '+lap+' OF 2'; if(lt!==lapNow){lapt.textContent=lt;lapNow=lt}
  // close-up: where it looks
  const pp=ez((v-Dt.vPan)/.8), cx=lerp(Dt.HAIR[0],Dt.FINL[0],pp), cy=lerp(Dt.HAIR[1],Dt.FINL[1],pp), vw_=Dt.IW/Dt.Z, vh_=Dt.IH/Dt.Z;
  cl.style.transform='translate('+(Dt.IW/2-cx*Dt.Z).toFixed(2)+'px,'+(Dt.IH/2-cy*Dt.Z).toFixed(2)+'px) scale('+Dt.Z+')';
  lr.setAttribute('x',(cx-vw_/2).toFixed(1)); lr.setAttribute('y',(cy-vh_/2).toFixed(1)); lr.setAttribute('width',vw_.toFixed(1)); lr.setAttribute('height',vh_.toFixed(1));
  // effects
  for(const vw of views){
    const k=vw.k;
    for(let n=0;n<NP;n++){
      const U=Dt.PUFF[n], p=(r-U[0])/.75, el=vw.pf[n];
      if(p>0&&p<1&&v>=Dt.T0){el.style.opacity=((1-p)*.92).toFixed(3); el.style.transform='translate('+(U[1]+U[3]*p*(k<1?.6:1)).toFixed(1)+'px,'+(U[2]+U[4]*p*(k<1?.6:1)).toFixed(1)+'px) scale('+(U[5]/20*(.45+p)*(k<1?.55:1.5)).toFixed(3)+')'}
      else el.style.opacity=0;
    }
    for(let n=0;n<10;n++){            // exhaust on the grid (before Go, and again in the loop tail)
      const c=n%5, el=vw.pf[NP+n], ph=((v*2.1+n*.37)%1+1)%1, C=P[c], d=(48+30*ph)*k;
      el.style.opacity=(idle*(1-ph)*.8).toFixed(3);
      el.style.transform='translate('+(C.x-Math.cos(C.a)*d).toFixed(1)+'px,'+(C.y-Math.sin(C.a)*d+(n<5?-5:5)*k).toFixed(1)+'px) scale('+((.35+ph*.7)*k*1.2).toFixed(3)+')';
    }
    const q=r-Dt.tM, so=q>0&&q<.9?(q<.12?q/.12:1-ez((q-.25)/.65)):0;
    vw.star.style.opacity=(so*(v>=Dt.T0?1:0)).toFixed(3);
    vw.star.style.transform='translate('+Dt.NOSE[0]+'px,'+Dt.NOSE[1]+'px) scale('+((.5+.7*ez(q/.2))*(k<1?.5:1.15)).toFixed(3)+') rotate('+(q*40).toFixed(1)+'deg)';
    const M=Dt.MK[vw.vi], qo=ez((r-Dt.tP-.15)/.4)*(1-wEnd), xo=ez((r-Dt.tM-.2)/.4)*(1-wEnd);
    vw.qm.style.opacity=qo>0?1:0; vw.qp.style.strokeDashoffset=(1-qo).toFixed(3); vw.qm.querySelector('circle').style.opacity=qo>.9?1:0;
    vw.qm.style.transform='translate('+M.q[0]+'px,'+(M.q[1]+Math.sin(v*4)*3*M.q[2]).toFixed(1)+'px) scale('+M.q[2]+')';
    vw.xm.style.opacity=xo>0?1:0; vw.xp.style.strokeDashoffset=(1-xo).toFixed(3);
    vw.xm.style.transform='translate('+M.x[0]+'px,'+M.x[1]+'px) scale('+M.x[2]+') rotate('+(Math.sin(v*3)*5).toFixed(1)+'deg)';
  }
}
'''.replace("__DATA__", json.dumps(DATA, separators=(",", ":")))

JS = re.sub(r"tl\.set\(([^,]+),\{", r"tl.set(\1,{immediateRender:false,", "\n".join(J))
json.dump(SFX, open(H_ + "/sfx98.json", "w"), indent=1)
json.dump(dict(lines=[dict(n=n, text=TEXT[n], start=s(n), end=e(n)) for n in range(1, 14)], D=D, go=T0,
               race=dict(start=T0, slow_from=round(vS0, 3), slow_to=round(vS1, 3), slow_rate=SLOW, slow_race_from=rA, slow_race_to=round(rB, 3),
                         perplexity_stops=round(vP, 3), meta_wall=round(vM, 3), claude=round(vC, 3), gemini=round(vGm, 3), chatgpt=round(vCh, 3)),
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
print(f"D={D} go={T0} ({SRC['go']}) roll={[round(x, 2) for x in ROLL]} ({SRC['roll']}) js={len(J)} sfx={len(SFX)}")
print(f"race clock: 1x from {T0}; SLOW MOTION {SLOW}x video {vS0:.2f}-{vS1:.2f} (race {rA}-{rB:.2f}); video times: Perplexity stops {vP:.2f}, Meta AI wall {vM:.2f}, "
      f"Claude {vC:.2f}, Gemini {vGm:.2f}, ChatGPT {vCh:.2f}; close-up {vI0:.2f}-{vI1:.2f}, pan {vPan:.2f}; winner {tW:.2f}; grid return {tG:.2f}; loop reset {tF:.2f}")
print("rank changes:", {IDS[c]: RANKEV[c] for c in range(5)})
if not WORDS: print("NOTE: voice/words.json not found: 'Go' and the roll call are timed from", SRC)
