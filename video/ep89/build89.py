#!/usr/bin/env python3
"""ep89 'PROMPT #1' builder. Torn-paper collage (ep88 helpers), ONE persistent dark prompt card that changes through the 4 spoken lines, loop back to frame 0.
usage: build89.py  -> cues89.json, out/narration89.wav, sfx89.json, hf/index.html   (render is a separate hyperframes call)
Voice: slices from voice/SLICES (see SRC below), joined with GAPS."""
import json, os, re, sys, hashlib, subprocess
import soundfile as sf, numpy as np
H = os.path.dirname(os.path.abspath(__file__))
SR = 48000
# line n -> (wav, cue index in that wav's -cues.json)
SRC = json.load(open(H + "/voice/src.json"))   # {"1": ["a", 0], "2": ["b", 0], ...}
GAPS = [float(x) for x in os.environ.get("GAPS", "0.22,0.2,0.22").split(",")]
HEAD = float(os.environ.get("HEAD", "0.06"))
TAIL = float(os.environ.get("TAIL", "0.75"))
ALL = [l.rstrip("\n") for l in open(H + "/lines.txt") if l.strip()]
assert len(ALL) == 4

def whisper_words(x, text, t0, key):
    cache = H + "/voice/words-cache.json"
    c = json.load(open(cache)) if os.path.exists(cache) else {}
    if key not in c:
        tmp = H + "/out/_w.wav"; sf.write(tmp, x, SR, subtype="PCM_16")
        out = subprocess.run(["/opt/v311/bin/python", "-c", "import sys,json;from faster_whisper import WhisperModel;m=WhisperModel('small',device='cpu',compute_type='int8');seg,_=m.transcribe(sys.argv[1],language='en',word_timestamps=True);print(json.dumps([[w.word.strip(),w.start,w.end] for s in seg for w in (s.words or [])]))", tmp], capture_output=True, text=True).stdout
        try: c[key] = json.loads(out.strip().splitlines()[-1])
        except Exception: c[key] = []
        json.dump(c, open(cache, "w"))
    ws = c[key]
    m_ = []
    for w in ws:
        if m_ and (m_[-1][0] + w[0]).lower() == 'chatgpt': m_[-1] = ['ChatGPT', m_[-1][1], w[2]]
        else: m_.append(list(w))
    ws = m_
    return [[round(t0 + a, 3), round(t0 + b, 3)] for _, a, b in ws] if len(ws) == len(text.split()) else None

os.makedirs(H + "/out", exist_ok=True)
lines = []; t = 0.0; parts = []
for j in range(4):
    n = j + 1; wname, ci = SRC[str(n)]
    xall, s = sf.read(f"{H}/voice/{wname}.wav"); assert s == SR; xall = xall if xall.ndim == 1 else xall[:, 0]
    cu = json.load(open(f"{H}/voice/{wname}-cues.json"))[ci]
    a = max(0, int((cu["start"] - HEAD) * SR)); b = min(len(xall), int((cu["end"] + .08) * SR))
    x = xall[a:b]; d = len(x) / SR
    key = hashlib.md5(x.tobytes()).hexdigest()
    wf = whisper_words(x, ALL[j], t, key)
    if not wf:   # fallback: even spread over the speech
        words = ALL[j].split(); step = (d - .1) / len(words)
        wf = [[round(t + .05 + i * step, 3), round(t + .05 + (i + 1) * step, 3)] for i in range(len(words))]
        print("line", n, "even-spread word estimate")
    else: print("line", n, "whisper word stamps")
    lines.append(dict(n=n, text=ALL[j], start=round(t + HEAD, 3), end=round(t + d, 3), words=wf))
    parts.append((int(t * SR), x)); t += d + (GAPS[j] if j < 3 else 0)
D = round(lines[-1]["end"] + TAIL, 2)
nar = np.zeros(int((D + .3) * SR))
for i0, x in parts: nar[i0:i0 + len(x)] += x
sf.write(H + "/out/narration89.wav", nar[:int(D * SR)], SR, subtype="PCM_16")
json.dump(dict(lines=lines, D=D), open(H + "/cues89.json", "w"), indent=1)
S = lambda n: lines[n - 1]["start"]
E = lambda n: lines[n - 1]["end"]
W = lambda n, i: lines[n - 1]["words"][i][0]
WE = lambda n, i: lines[n - 1]["words"][i][1]

# ---- reuse ep88 helpers (torn pieces, strips, tape, stamps) and the ep88 styles
t7 = open(H + "/../ep88/build7_top.py").read()
st7 = open(H + "/../ep88/build7_style.py").read()
tl7 = open(H + "/../ep88/build7_tl.py").read()
from PIL import ImageFont
exec(t7[t7.index("import random as _r"):t7.index("# ---- hook block")])      # P, strip, tape, stamp, pimg, REG, js, sfx ...
exec(st7[st7.index("styles = r'''"):])                                            # styles
svgdefs = re.search(r'<svg width="0".*?</svg>', t7, re.S).group(0)
D_ = D
rnd = _r.Random(7)
def at(t): return tt(t)
exec(tl7[tl7.index("def slam"):tl7.index("def fly")])     # slam, settle, drop, tapeslap, thump
exec(tl7[tl7.index("def cam"):tl7.index("def scraps")])   # cam

def vis(sel, t):
    js(f"tl.set('{sel}',{{visibility:'visible'}},{at(t)});")

def out_(sel, t, d=.16):
    js(f"tl.to('{sel}',{{opacity:0,scale:.96,duration:{d},ease:'power1.in',transformOrigin:'50% 50%'}},{at(t)});")
    js(f"tl.set('{sel}',{{visibility:'hidden'}},{at(t + d + .01)});")

def fit(text, font, maxw, size0, minsize=40):
    s = size0
    while s > minsize and ImageFont.truetype(FONTF[font], s).getlength(text.upper()) > maxw: s -= 2
    return s

# ---------------------------------------------------------------- layout (safe box x 65-1015, y 269-1248)
STRIP_X, STRIP_Y = 70, 290
LOGO = 210
def logo(id, x, y, rot):
    return (f'<div class="gsb" id="{id}" style="left:{x}px;top:{y}px;width:{LOGO}px;height:{LOGO}px;transform:rotate({rot}deg)"><img src="assets/chatgpt.svg"></div>')

WORDS = ALL[1].replace("three", "3").split()   # on-screen: the real sentence, with the digit
WORDS_SHOW = ["Before", "you", "answer,", "ask", "me", "3", "clarifying", "questions", "you", "need."]
assert len(WORDS) == len(ALL[1].split())
WORDS_SHOW = WORDS

def card(k, typed):
    """the dark prompt card (a torn dark cardboard piece with a ChatGPT-style input box). typed=True: words are in the markup (hidden until typed)."""
    ws = ""
    for i, w in enumerate(WORDS):
        cls = " hl" if w == "3" else ""
        ws += f'<span class="pw{cls}" id="pw{k}{i}">{w}</span> <span class="cu" id="cu{k}{i}"></span>'
    inner = (f'<div class="inp"><div class="ph" id="ph{k}"><span class="cu on" id="cuS{k}"></span></div><div class="pnum2" id="pn{k}">PROMPT #1</div><div class="ptx" id="ptx{k}">{ws if typed else ""}</div></div>'
             f'<div class="plus">+</div><div class="snd" id="snd{k}"><svg viewBox="0 0 24 24" width="52" height="52"><path d="M12 19V5M5 12l7-7 7 7" stroke="#17130F" stroke-width="3.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
             f'<div class="ring2" id="rg{k}"></div>')
    return P(inner, f"card{k}", 100, 650, 880, 590, -.8, "card", (40, 36, 32), 21, 9, 6, "dkcard")

def phase1(k):
    """frame-0 state: strips + logo + dark card with an empty input. k = suffix ('' main, 'H' loop copy)."""
    sa = fit("OPENAI SAYS:", "BS", 860, 190); sb = fit("PASTE THIS FIRST", "BS", 600, 170)
    return (strip(f"sa{k}", "OPENAI SAYS:", STRIP_X, STRIP_Y, 940, 160, -1.3, ("card", YEL), size=sa, seed=81, z=8)
            + strip(f"sb{k}", "PASTE THIS FIRST", STRIP_X, STRIP_Y + 175, 700, 160, 1.2, ("card", BLK), "#f1e8d2", "BS", sb, 82, z=9)
            + logo(f"lg{k}", 790, 450, 8) + card(k, typed=(k == "")) )

# ---------------------------------------------------------------- scene markup
def scraps_markup():
    spec = [("news", 520, 330, -6, -150, -90), ("orange", 480, 240, 5, 650, -60), ("red", 340, 420, 8, 860, 120), ("blue", 460, 300, -4, -170, 1290),
            ("ticket", 520, 340, 4, 560, 1330), ("map", 640, 380, -5, -120, 1560), ("news2", 420, 300, 7, 740, 1640), ("card", 400, 260, -3, 80, 1760),
            ("orange", 300, 420, -7, 900, 1250), ("chart", 460, 300, 5, 250, 1500)]
    out = ""
    for i, (kind, w, h, rot, x, y) in enumerate(spec):
        out += P("", f"sc{i}", x, y, w, h, rot, kind, CRM, 300 + i, 11, 1, "scrap")
    return out, spec

SCR, SPEC = scraps_markup()
# phase 2: source strip; phase 3: ask not guess; phase 4: save / send
S2X, S2Y = 90, 322
src_strip = strip("s2", "OPENAI ACADEMY", S2X, S2Y, 700, 150, -1.0, ("news", None), "#17130F", "BS", fit("OPENAI ACADEMY", "BS", 640, 150), 83, z=9)
ask_strip = strip("s3", "ASK. NOT GUESS.", S2X, S2Y, 700, 150, 1.0, ("card", YEL), size=fit("ASK. NOT GUESS.", "BS", 640, 150), seed=84, z=9)
save_strip = strip("s4a", "SAVE IT", S2X, S2Y, 900, 170, -1.2, ("card", YEL), size=fit("SAVE IT", "BS", 840, 210), seed=85, z=9)
send_strip = strip("s4b", "SEND IT", S2X, S2Y, 900, 170, 1.1, ("card", BLK), "#f1e8d2", "BS", fit("SEND IT", "BS", 840, 210), 86, z=10)

def qbubble(i, y, rot, seed):
    inner = ('<div class="qm">?</div><div class="qb"><i style="width:78%"></i><i style="width:52%"></i></div>')
    return P(inner, f"qb{i}", 150, y, 780, 150, rot, "news" if i != 1 else "card", CRM if i != 1 else WHT, seed, 8, 14, "qbub")

bubbles = qbubble(0, 690, -1.5, 91) + qbubble(1, 880, 1.2, 92) + qbubble(2, 1070, -.8, 93)
stampSaved = stamp("saved", "SAVED", 330, 1090, -6, 84, "#9BE22E", "A", .95, "BS", True, 30)
# chat for phase 4
chat4 = ('<div class="mavt" id="fav">?</div>'
         + P('<div class="shortmsg" id="shm"><span id="shmt">write email</span></div>', "fbub", 250, 1040, 600, 150, -.8, "card", WHT, 95, 8, 15, "chb")
         + '<div class="dots2" id="fdots"><i></i><i></i><i></i></div>')

markup = f'''{svgdefs}
<div id="world">
<div class="bgl" id="bgl" data-decor><img class="bgimg" id="bgimg" src="assets/p7/bg_card.jpg"></div>
<div id="scr" data-decor>{SCR}</div>
<div class="sc" id="sA" style="opacity:1;visibility:visible"><div class="cam" id="cA">
{phase1("")}{src_strip}{ask_strip}{save_strip}{send_strip}{bubbles}{stampSaved}{chat4}</div></div>
<div class="sc" id="sH"><div class="cam" id="cH">{phase1("H")}</div></div>
</div>
<img class="sheet" id="sheetA" data-decor src="assets/p6/sheet0.png"><img class="sheet" id="sheetB" data-decor src="assets/p6/sheet1.png">
<div class="grainw" data-decor><img class="grain" id="grain" data-decor src="assets/p6/grain.jpg"></div>
'''

extra_css = r'''
#s2,#s3,#s4a,#s4b{visibility:hidden}
#saved{mix-blend-mode:normal!important}
#scr{position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:0}
.sc{z-index:2}

.gsb{position:absolute;z-index:20;border-radius:50%;background:#fff;box-shadow:0 0 0 7px #fff,0 10px 26px rgba(30,18,6,.5);display:flex;align-items:center;justify-content:center}
.gsb img{width:66%;height:66%}
.dkcard .inp{position:absolute;left:34px;top:34px;width:812px;height:446px;border-radius:46px;background:#33302c;box-shadow:inset 0 3px 10px rgba(0,0,0,.45);overflow:hidden}
.ph{position:absolute;left:44px;top:46px;font:500 50px IDisp;height:70px;color:rgba(241,232,210,.42);white-space:nowrap}
.pnum2{position:absolute;left:0;top:70px;width:100%;text-align:center;font:700 168px BS;line-height:240px;white-space:nowrap;color:#E0553B;transform:rotate(-5deg);opacity:1;filter:url(#ink);letter-spacing:.01em}
.ptx{position:absolute;left:44px;top:26px;right:36px;font:800 76px IDisp;line-height:102px;color:#f1e8d2;letter-spacing:-.02em;filter:url(#ink)}
.pw{opacity:0;display:inline}
.pw.hl{background:linear-gradient(0deg,transparent 6%,var(--lime) 6%,var(--lime) 92%,transparent 92%);color:#17130F;padding:0 12px;border-radius:6px;margin:0 2px}
.cu{display:inline-block;width:6px;height:60px;margin-left:2px;margin-right:6px;vertical-align:-6px;background:#f1e8d2;opacity:0}
.cu.on{opacity:1;margin-left:14px;vertical-align:-10px}
.plus{position:absolute;left:44px;top:486px;width:78px;height:78px;border-radius:50%;border:5px solid rgba(241,232,210,.5);color:rgba(241,232,210,.7);font:500 58px IDisp;line-height:64px;text-align:center}
.snd{position:absolute;left:748px;top:476px;width:98px;height:98px;border-radius:50%;background:#f1e8d2;display:flex;align-items:center;justify-content:center}
.ring2{position:absolute;left:718px;top:446px;width:158px;height:158px;border-radius:50%;border:10px solid var(--red);opacity:0}
.qbub .qm{position:absolute;left:36px;top:0;font:700 150px BS;line-height:150px;color:var(--red);filter:url(#ink);mix-blend-mode:multiply}
.qbub .qb{position:absolute;left:150px;top:36px;right:40px;bottom:36px;display:flex;flex-direction:column;justify-content:center;gap:22px}
.qbub .qb i{display:block;height:26px;border-radius:13px;background:rgba(40,34,26,.55)}
.shortmsg{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font:800 76px IDisp;color:#17130F;letter-spacing:-.02em;filter:url(#ink)}
'''

# ---------------------------------------------------------------- timeline
T = dict(s2=S(2) - .12, s3=S(3) - .12, s4=S(4) - .1, send=W(4, 2) - .1, short=W(4, 5) - .05, loop=E(4) + .22)
js(f"tl.fromTo('#world',{{scale:1,rotation:-.25}},{{scale:1.02,rotation:.25,duration:{D_:.3f},ease:'sine.inOut'}},0);")
js(f"tl.fromTo('#bgimg',{{x:0}},{{x:-320,duration:{D_:.3f},ease:'sine.inOut'}},0);")
g_t = 0.0
while g_t < D_:
    js(f"tl.set('#grain',{{x:{rnd.randint(-30, 30)},y:{rnd.randint(-30, 30)}}},{at(g_t)});"); g_t += 1 / 12
# decorative scraps: slow drift all the time (3 speeds)
for i, (kind, w, h, rot, x, y) in enumerate(SPEC):
    dx = (-1) ** i * (16 + 12 * (i % 3)); dy = (-1) ** (i // 2) * (10 + 8 * (i % 2)); dr = (-1) ** i * 1.4
    js(f"tl.fromTo('#sc{i}',{{x:{-dx},y:{-dy},rotation:{rot - dr}}},{{x:{dx},y:{dy},rotation:{rot + dr},duration:{D_:.3f},ease:'sine.inOut'}},0);")
# camera: continuous slow push, different per phase (no jumps: the end of one is the start of the next)
cam("cA", 0, T["s2"], 1.0, 1.012, -.3, .2, 0, 0, 0, 0)
cam("cA", T["s2"], T["s3"], 1.012, 1.03, .2, -.2, 0, 0, 0, -8)
cam("cA", T["s3"], T["s4"], 1.03, 1.02, -.2, .3, 0, 0, -8, 0)
cam("cA", T["s4"], T["loop"], 1.02, 1.0, .3, 0, 0, 0, 0, 0)

js("tl.set('#s2,#s3,#s4a,#s4b',{visibility:'hidden'},0);")
# --- phase 1 (frame 0 is settled and readable; only small continuous motion)
js(f"tl.fromTo('#lg',{{rotation:8,scale:1}},{{rotation:2,scale:1.07,duration:.9,ease:'sine.inOut',yoyo:true,repeat:1,transformOrigin:'50% 50%'}},{at(.05)});")
js(f"tl.fromTo('#sa',{{x:-10,rotation:-1.5}},{{x:8,rotation:-1.1,duration:{T['s2']:.3f},ease:'sine.inOut',transformOrigin:'50% 50%'}},0);")
js(f"tl.fromTo('#sb',{{x:10}},{{x:-8,duration:{T['s2']:.3f},ease:'sine.inOut'}},0);")
js(f"tl.fromTo('#card',{{y:6}},{{y:-6,duration:{T['s2']:.3f},ease:'sine.inOut'}},0);")
# blinking cursor in the empty input
js(f"tl.fromTo('#cuS',{{opacity:1}},{{opacity:0,duration:.34,ease:'steps(1)',yoyo:true,repeat:{int(T['s2'] / .34)}}},0);")
sfx("impactpunch.ogg", 0.02, -3)

# --- phase 2: strips out, source strip in, the prompt is typed word by word as it is read
s = T["s2"]
for sel in ("#sa", "#sb"):
    out_(sel, s - .06)
vis("#s2", s + .13); slam("#s2", s + .14, dx=-280, rot=-1, s0=1.08, dur=.34)
js(f"tl.fromTo('#lg',{{y:0}},{{y:-160,rotation:-6,duration:.55,ease:'back.out(1.4)'}},{at(s + .12)});")
sfx("whoosh_a.ogg", s, -3); sfx("pop_a.ogg", s + .3, -4)
js(f"tl.to('#pn',{{opacity:0,scale:1.1,duration:.2,ease:'power2.in',transformOrigin:'50% 50%'}},{at(s - .1)});")
js(f"tl.set('#ph',{{opacity:0}},{at(W(2, 0) - .05)});")
for i, w in enumerate(WORDS):
    t0 = W(2, i) - .04
    js(f"tl.set('#pw{i}',{{opacity:1}},{at(t0)});")
    if i == 5: js(f"tl.fromTo('#pw{i}',{{scale:1.5}},{{scale:1,duration:.3,ease:'back.out(2)',transformOrigin:'50% 70%'}},{at(t0)});"); sfx("click_a.ogg", t0, -5)
    js(f"tl.set('#cu{i}',{{opacity:1}},{at(t0)});")
    js(f"tl.set('#cu{i}',{{opacity:0}},{at(W(2, i + 1) - .04 if i + 1 < len(WORDS) else E(2))});")
    sfx("tick.ogg", t0, -13)
js(f"tl.fromTo('#ptx',{{x:-8}},{{x:6,duration:{E(2) - S(2):.3f},ease:'sine.inOut'}},{at(S(2))});")
js(f"tl.fromTo('#card',{{scale:1,rotation:-.8}},{{scale:1.045,rotation:.2,duration:{T['s3'] - s:.3f},ease:'sine.inOut',transformOrigin:'50% 40%'}},{at(s)});")
# press send right at the end of the read
js(f"tl.to('#rg',{{opacity:1,scale:1.0,duration:.1}},{at(E(2) + .02)});")
js(f"tl.fromTo('#rg',{{scale:1.5}},{{scale:1,duration:.22,ease:'power3.out',transformOrigin:'50% 50%'}},{at(E(2) + .02)});")
js(f"tl.to('#snd',{{scale:.86,duration:.08,yoyo:true,repeat:1}},{at(E(2) + .06)});")
js(f"tl.to('#rg',{{opacity:0,duration:.2}},{at(E(2) + .4)});")
sfx("select.ogg", E(2) + .05, -4)

# --- phase 3: "It makes ChatGPT ask, not guess." three question bubbles pop (placeholders, no invented answers)
s = T["s3"]
out_("#s2", s - .04)
vis("#s3", s + .13); slam("#s3", s + .14, dx=280, rot=1, s0=1.08, dur=.34)
sfx("whoosh_b.ogg", s, -3)
js(f"tl.to('#ptx',{{opacity:0,duration:.2}},{at(s + .05)});")
js(f"tl.to('#card',{{scale:1.0,rotation:-.6,duration:.6,ease:'sine.inOut'}},{at(s + .1)});")
js(f"tl.to('.dkcard .plus,#snd',{{opacity:0,duration:.15}},{at(s + .15)});")
bt = [W(3, 3) - .35, W(3, 3) - .05, W(3, 3) + .22]   # around "ChatGPT ask"
for i in range(3):
    t0 = max(s + .2, bt[i])
    js(f"tl.fromTo('#qb{i}',{{scale:.55,opacity:0,rotation:{(-8, 6, -5)[i]}}},{{scale:1,opacity:1,rotation:0,duration:.4,ease:'back.out(1.6)',transformOrigin:'50% 50%'}},{at(t0)});")
    sfx("pop_a.ogg", t0 + .12, -3)
js("tl.set('#qb0,#qb1,#qb2',{opacity:0},0);")
for i in range(3):
    js(f"tl.to('#qb{i}',{{y:{(-1) ** i * 6},duration:{T['s4'] - s:.3f},ease:'sine.inOut'}},{at(s + .6)});")

# --- phase 4: save it / send it to someone who types short prompts
s = T["s4"]
for i in range(3):
    js(f"tl.to('#qb{i}',{{scale:.7,opacity:0,rotation:{(-9, 7, -6)[i]},duration:.25,ease:'power2.in',transformOrigin:'50% 50%'}},{at(s - .02 + i * .05)});")
out_("#s3", s - .04)
js(f"tl.to('.dkcard .plus,#snd',{{opacity:1,duration:.2}},{at(s + .4)});")
vis("#s4a", s + .13); slam("#s4a", s + .14, dx=-280, rot=-1, s0=1.08, dur=.34)
js(f"tl.to('#lg',{{scale:0,opacity:0,rotation:-60,duration:.35,ease:'back.in(1.5)'}},{at(s)});")
js(f"tl.to('#ptx',{{opacity:1,duration:.3}},{at(s + .25)});")
js(f"tl.fromTo('#saved',{{scale:2.2,opacity:0}},{{scale:1,opacity:.9,duration:.16,ease:'power4.in',transformOrigin:'50% 50%'}},{at(W(4, 0) + .1)});")
sfx("whoosh_c.ogg", s, -4); sfx("impactsoft.ogg", W(4, 0) + .22, -4); sfx("click_a.ogg", W(4, 0) + .24, -4)
# send: the card shrinks into a sent message (right), strip changes, friend asks with a short prompt
t0 = T["send"]
out_("#s4a", t0 - .2)
vis("#s4b", t0 - .01); slam("#s4b", t0 + .0, dx=280, rot=1, s0=1.08, dur=.34)
js(f"tl.to('#saved',{{opacity:0,duration:.2}},{at(t0)});")
js(f"tl.to('#card',{{x:70,y:-200,scale:.8,rotation:3,duration:.7,ease:'expo.inOut',transformOrigin:'50% 50%'}},{at(t0)});")
sfx("whoosh_a.ogg", t0, -3); sfx("pop_b.ogg", t0 + .72, -3)
js("tl.set('#fav,#fbub,#fdots',{opacity:0},0);")
js(f"tl.fromTo('#fav',{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.38,ease:'back.out(2)'}},{at(t0 + .5)});")
js(f"tl.fromTo('#fdots',{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.3,ease:'power2.out'}},{at(t0 + .6)});")
js(f"tl.to('#fdots i',{{y:-10,duration:.24,ease:'sine.inOut',yoyo:true,repeat:3,stagger:.08}},{at(t0 + .7)});")
js(f"tl.to('#fdots',{{opacity:0,duration:.16}},{at(T['short'] - .05)});")
js(f"tl.fromTo('#fbub',{{scale:.6,opacity:0,rotation:-5}},{{scale:1,opacity:1,rotation:0,duration:.4,ease:'back.out(1.6)',transformOrigin:'0% 50%'}},{at(T['short'])});")
sfx("pop_a.ogg", T["short"] + .12, -3); sfx("ding.ogg", E(4) - .05, -7)

# --- loop: a paper sweep covers the frame, scene swaps to the frame-0 copy
tl_ = T["loop"]
js(f"tl.fromTo('#sheetA',{{x:1160,y:-100,rotation:-2.5,opacity:1}},{{x:-1560,y:-120,rotation:2.5,duration:.24,ease:'power2.inOut'}},{at(tl_ - .12)});")
js(f"tl.set('#sheetA',{{opacity:0}},{at(tl_ + .14)});")
js(f"tl.set('#sA',{{autoAlpha:0}},{at(tl_ - .01)});"); js(f"tl.set('#sH',{{autoAlpha:1}},{at(tl_ - .01)});")
js("tl.set('#sH',{autoAlpha:0},0);")
js(f"tl.fromTo('#cH',{{scale:1.012,rotation:.2}},{{scale:1,rotation:0,duration:{D_ - tl_:.3f},ease:'sine.out',transformOrigin:'540px 760px'}},{at(tl_)});")
js(f"tl.fromTo('#lgH',{{rotation:8}},{{rotation:3,scale:1.05,duration:{D_ - tl_:.3f},ease:'sine.inOut',transformOrigin:'50% 50%'}},{at(tl_)});")
js("tl.set('#sheetA,#sheetB',{opacity:0},0);")
sfx("whoosh_c.ogg", tl_ - .13, -4)

JS = "const D2=" + str(D_) + ";\n" + "\n".join(J)
json.dump([dict(f=f, t=t, g=g) for f, t, g in SFX if 0 <= t < D_], open(H + "/sfx89.json", "w"), indent=1)
html = open(H + "/shell8.html").read()
html = (html.replace("__STYLES__", styles + extra_css).replace("__MARKUP__", markup).replace("__CHROME__", "").replace("__SCRIPTS__", "")
        .replace("__D__", str(D_)).replace("__CUES__", json.dumps(dict(lines=lines, D=D_)))
        .replace("__CALLS__", JS).replace("__NSC__", "1"))
html = re.sub(r'<div class="abs clip" id="gd".*?</div>', '', html, flags=re.S)
os.makedirs(H + "/hf", exist_ok=True)
open(H + "/hf/index.html", "w").write(html)
print("D=", D_, [(l["n"], l["start"], l["end"]) for l in lines], "T", {k: round(v, 2) for k, v in T.items()}, "js", len(J), "sfx", len(SFX))
