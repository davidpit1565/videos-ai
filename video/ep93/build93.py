#!/usr/bin/env python3
"""ep93 'My idea has 3 flaws. I show AI.' builder. Dark navy base like the meme C.png, brand-coloured panels (ChatGPT green, Claude orange).
usage: SRC_TAG=a build93.py -> cues93.json, out/narration93.wav, sfx93.json, hf/index.html (render is a separate hyperframes call)
Voice: slices of voice/<tag>.wav joined with GAPS (SRC in voice/src.json: {"1":["a",0],...})."""
import json, os, re, sys, hashlib, subprocess
import soundfile as sf, numpy as np
H = os.path.dirname(os.path.abspath(__file__))
SR = 48000
SRC = json.load(open(H + "/voice/src.json"))
GAPS = [float(x) for x in os.environ.get("GAPS", "0.28,0.28,0.28").split(",")]
HEAD = float(os.environ.get("HEAD", "0.06"))
TAIL = float(os.environ.get("TAIL", "0.5"))
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
    ws = c[key]; m_ = []
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
    if not wf:
        words = ALL[j].split(); step = (d - .1) / len(words)
        wf = [[round(t + .05 + i * step, 3), round(t + .05 + (i + 1) * step, 3)] for i in range(len(words))]
        print("line", n, "even-spread word estimate")
    else: print("line", n, "whisper word stamps")
    lines.append(dict(n=n, text=ALL[j], start=round(t + HEAD, 3), end=round(t + d, 3), words=wf))
    parts.append((int(t * SR), x)); t += d + (GAPS[j] if j < 3 else 0)
D = round(lines[-1]["end"] + TAIL, 2)
nar = np.zeros(int((D + .3) * SR))
for i0, x in parts: nar[i0:i0 + len(x)] += x
sf.write(H + "/out/narration93.wav", nar[:int(D * SR)], SR, subtype="PCM_16")
json.dump(dict(lines=lines, D=D), open(H + "/cues93.json", "w"), indent=1)
S = lambda n: lines[n - 1]["start"]
E = lambda n: lines[n - 1]["end"]
W = lambda n, i: lines[n - 1]["words"][i][0]

J = []; SFX = []
def js(s): J.append(s)
def sfx(f, t, g=-4): SFX.append((f, round(t, 3), g))
def T(t): return f"{max(0.0, t):.3f}"

# ------------------------------------------------------------------ geometry (safe box x 65-1015, y 269-1248)
PILL = dict(g=(65, 1060, 460, 180), o=(555, 1060, 460, 180))
FULL = (65, 300, 950, 940)
COL = dict(g=(65, 300, 460, 720), o=(555, 300, 460, 720))

def mark(i, k):
    x = '<svg viewBox="0 0 40 40" width="46" height="46"><path d="M11 11L29 29M29 11L11 29" stroke="#fff" stroke-width="5.5" stroke-linecap="round"/></svg>'
    return f'<div class="mk" id="mk{k}{i}"><div class="mkh"></div><div class="mkf" id="mf{k}{i}">{x}</div></div>'

def idea_card(k, cls="card"):
    bulb = ('<svg viewBox="0 0 64 64" width="92" height="92"><path d="M32 6c-11 0-19 8-19 18 0 7 4 11 7 15 2 3 3 5 3 8h18c0-3 1-5 3-8 3-4 7-8 7-15 0-10-8-18-19-18z" fill="#FFD21F" stroke="#17130F" stroke-width="3.5"/>'
            '<path d="M24 52h16M26 58h12" stroke="#17130F" stroke-width="4" stroke-linecap="round"/></svg>')
    rows = ""
    for i, w in enumerate((64, 50, 72)):
        rows += f'<div class="row"><i class="bar" style="width:{w}%"></i>{mark(i, k)}</div>'
    return (f'<div class="{cls}" id="card{k}"><div class="ctop">{bulb}<i class="bar tb"></i></div>{rows}</div>')

def panel(k, who):
    c = "g" if who == "g" else "o"
    logo = "openai.svg" if who == "g" else "claude.svg"
    name = "ChatGPT" if who == "g" else "Claude"
    img = "dog.jpg" if who == "g" else "cat3.jpg"
    if who == "g":
        bub = '<div class="bub gb" id="bub_g"><span>Perfect idea!</span><svg class="smile" viewBox="0 0 64 64" width="78" height="78"><circle cx="32" cy="32" r="29" fill="#FFD21F" stroke="#17130F" stroke-width="3.5"/><circle cx="22" cy="26" r="4" fill="#17130F"/><circle cx="42" cy="26" r="4" fill="#17130F"/><path d="M16 38q16 18 32 0" fill="none" stroke="#17130F" stroke-width="4.5" stroke-linecap="round"/></svg></div>'
    else:
        bub = '<div class="bub ob" id="bub_o"><span>3 problems.</span><span>Fix #1 first.</span></div>'
    return (f'<div class="pan {c}" id="pan_{c}"><div class="phw"><img class="pimg" id="img_{c}" src="assets/{img}"></div>{bub}'
            f'<div class="hd" id="hd_{c}"><div class="bdg" id="bdg_{c}"><img src="assets/{logo}"></div><div class="nm" id="nm_{c}">{name}</div></div></div>')

def pill(k, who):
    c = "g" if who == "g" else "o"; logo = "openai.svg" if who == "g" else "claude.svg"
    return f'<div class="pill {c}" id="pill{k}_{c}"><div class="bdg big"><img src="assets/{logo}"></div></div>'

def sceneA(k, with_card):
    return (f'<div class="sc" id="sc{k}"><div class="cam" id="cam{k}">'
            f'<div class="head" id="head{k}"><div class="h1">My idea has <b>3 flaws.</b></div><div class="h2">I show AI.</div></div>'
            f'{idea_card(k, "card big") if with_card else ""}{pill(k, "g")}{pill(k, "o")}</div></div>')

markup = f'''
<div class="bg" data-decor><div class="glow gl1" id="gl1"></div><div class="glow gl2" id="gl2"></div></div>
{sceneA("", False)}
<div class="sc" id="scP"><div class="cam" id="camP">{panel("", "g")}{panel("", "o")}
<div class="tag" id="tag"><div class="tl"><span id="tw0">Tag</span> <span id="tw1">someone</span> <span id="tw2">who</span></div><div class="tl"><span id="tw3">needs</span> <span id="tw4">the</span> <span class="y" id="tw5">cat.</span></div></div></div></div>
<div class="sc" id="scC"><div class="cam" id="camC">{idea_card("M", "card big")}<svg class="chk" id="chk" viewBox="0 0 120 120" width="150" height="150"><circle cx="60" cy="60" r="54" fill="#1f9d55" stroke="#fff" stroke-width="7"/><path d="M34 62l17 17 36-38" fill="none" stroke="#fff" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>
{sceneA("H", True)}
'''

css = r'''
.bg{position:absolute;inset:0;background:#0e1422;overflow:hidden}
.glow{position:absolute;border-radius:50%;filter:blur(70px)}
.gl1{left:-300px;top:200px;width:900px;height:900px;background:radial-gradient(circle,rgba(16,163,127,.28),transparent 68%)}
.gl2{left:520px;top:900px;width:900px;height:900px;background:radial-gradient(circle,rgba(217,119,87,.26),transparent 68%)}
.sc{position:absolute;left:0;top:0;width:1080px;height:1920px}
#scH{opacity:0;visibility:hidden}
.head{position:absolute;left:65px;top:290px;width:950px;text-align:center;color:#fff;font-weight:800;letter-spacing:-.035em}
.h1{font-size:98px;line-height:108px;white-space:nowrap}.h1 b{color:#ffd21f}.h2{font-size:112px;line-height:118px;margin-top:2px}
.card{position:absolute;background:#f6f1e4;border-radius:34px;box-shadow:0 18px 40px rgba(0,0,0,.5);transform-origin:0 0}
.card.big{left:120px;top:575px;width:840px;height:440px;transform:rotate(-1.4deg)}
.ctop{position:absolute;left:44px;top:34px;right:44px;height:100px;display:flex;align-items:center;gap:26px}
.bar{display:block;height:34px;border-radius:17px;background:#cfc8b6}.tb{width:46%;height:42px;background:#17130F;opacity:.85}
.row{position:absolute;left:44px;right:44px;height:90px;display:flex;align-items:center;gap:20px}
.row:nth-of-type(2){top:150px}.row:nth-of-type(3){top:250px}.row:nth-of-type(4){top:350px}
.row .bar{flex:none}
.mk{position:absolute;right:0;top:0;width:90px;height:90px}
.mkh{position:absolute;inset:0;border-radius:50%;border:8px solid rgba(229,72,77,.6)}
.mkf{position:absolute;inset:0;border-radius:50%;background:#e5484d;display:flex;align-items:center;justify-content:center;opacity:0;box-shadow:0 0 0 0 rgba(229,72,77,0)}
.mkf svg{width:56px;height:56px}
.pill{position:absolute;top:1060px;width:460px;height:180px;border-radius:40px;display:flex;align-items:center;justify-content:center;box-shadow:0 12px 30px rgba(0,0,0,.45)}
.pill.g{left:65px;background:#10a37f}.pill.o{left:555px;background:#d97757}
.bdg{width:76px;height:76px;border-radius:20px;background:#fff;display:flex;align-items:center;justify-content:center;flex:none}
.bdg img{width:62%;height:62%}.bdg.big{width:118px;height:118px;border-radius:30px}
.pan{position:absolute;overflow:hidden;border-radius:40px;box-shadow:0 14px 40px rgba(0,0,0,.5)}
.pan.g{background:#10a37f}.pan.o{background:#d97757}
.hd{position:absolute;left:0;right:0;top:0;height:180px;display:flex;align-items:center;justify-content:center;gap:0}
.nm{font-size:62px;font-weight:800;color:#fff;letter-spacing:-.02em;max-width:0;overflow:hidden;white-space:nowrap;opacity:0}
.phw{position:absolute;left:0;right:0;top:120px;bottom:0;overflow:hidden}
.pimg{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;will-change:transform}
#img_g{object-position:50% 58%}#img_o{object-position:60% 40%}
.bub{position:absolute;left:24px;right:24px;bottom:24px;background:#fff;border-radius:36px;border:9px solid;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#111;font-weight:800;letter-spacing:-.03em;opacity:0}
.gb{border-color:#10a37f;height:200px;flex-direction:row;gap:20px;font-size:90px;line-height:1}
.ob{border-color:#d97757;height:236px;font-size:82px;line-height:1.08}
.tag{position:absolute;left:65px;top:1048px;width:950px;text-align:center;font-weight:800;font-size:92px;line-height:96px;letter-spacing:-.03em;color:#fff}
.tag .tl{white-space:nowrap}.tag span{display:inline-block;opacity:0;margin:0 8px}.tag .y{color:#ffd21f}
.chk{position:absolute;left:380px;top:540px;opacity:0}
'''

# ------------------------------------------------------------------ timeline
s2, s3, s4 = S(2), S(3), S(4)
tB = s2 - .14           # B starts: green pill grows
tC = s3 - .12           # C starts: green out, orange in
tD = s4 - .14           # D starts
tL = D - .42            # loop crossfade
P0 = lambda who: PILL[who]

js(f"tl.set('#scP,#scC',{{opacity:1,visibility:'visible'}},0);")
js(f"tl.set('#scH',{{autoAlpha:0}},0);")
# panels in pill state at frame 0 (hidden: the pills of scene A are on screen instead)
for w in ("g", "o"):
    x, y, wd, h = PILL[w]
    js(f"gsap.set('#pan_{w}',{{left:{x},top:{y},width:{wd},height:{h},autoAlpha:0}});")
    js(f"gsap.set('#hd_{w}',{{height:180}});gsap.set('#bdg_{w}',{{width:118,height:118,borderRadius:30}});")
# background glow drift (always moving)
js(f"tl.fromTo('#gl1',{{x:0,y:0}},{{x:120,y:80,duration:{D:.3f},ease:'sine.inOut'}},0);")
js(f"tl.fromTo('#gl2',{{x:0,y:0}},{{x:-140,y:-60,duration:{D:.3f},ease:'sine.inOut'}},0);")

# ---- A: frame 0 is fully readable; small continuous motion, marks go red on 'three flaws'
for k in ("", "H"):
    js(f"tl.fromTo('#head{k}',{{scale:1,y:0}},{{scale:1.01,y:-3,duration:{tB:.3f},ease:'sine.inOut',transformOrigin:'50% 0%'}},0);" if k == '' else f"tl.fromTo('#head{k}',{{scale:1.012}},{{scale:1,duration:{D - tL:.3f},ease:'sine.out',transformOrigin:'50% 0%'}},{T(tL)});")
js(f"tl.fromTo('#cardM',{{rotation:-1.4}},{{rotation:-.3,duration:{tB:.3f},ease:'sine.inOut'}},0);")
js(f"tl.fromTo('#pill_g',{{y:0}},{{y:-8,duration:.7,ease:'sine.inOut',yoyo:true,repeat:{max(0, int(tB / .7) - 1)}}},0);")
js(f"tl.fromTo('#pill_o',{{y:-8}},{{y:0,duration:.7,ease:'sine.inOut',yoyo:true,repeat:{max(0, int(tB / .7) - 1)}}},0);")
w3 = W(1, 3)
mt = [max(.25, w3 - .1), max(.55, w3 + .2), max(.85, w3 + .5)]
for i, t0 in enumerate(mt):
    js(f"tl.fromTo('#mfM{i}',{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.32,ease:'back.out(1.7)',transformOrigin:'50% 50%'}},{T(t0)});")
    sfx("tick.ogg", t0 + .02, -3)
sfx("impactpunch.ogg", 0.02, -5)

# ---- B: ChatGPT. Green pill grows into the panel, orange pill drops, headline + card leave, dog zooms in
x, y, wd, h = FULL
js(f"tl.set('#pan_g',{{autoAlpha:1}},{T(tB)});")
js(f"tl.set('#pill_g',{{autoAlpha:0}},{T(tB)});")
js(f"tl.to('#pan_g',{{left:{x},top:{y},width:{wd},height:{h},duration:.62,ease:'expo.inOut'}},{T(tB)});")
js(f"tl.to('#hd_g',{{height:120,duration:.62,ease:'expo.inOut'}},{T(tB)});")
js(f"tl.to('#bdg_g',{{width:76,height:76,borderRadius:20,duration:.5,ease:'power3.inOut'}},{T(tB)});")
js(f"tl.to('#nm_g',{{maxWidth:380,opacity:1,marginLeft:22,duration:.45,ease:'power2.out'}},{T(tB + .3)});")
js(f"tl.to('#pill_o',{{y:240,opacity:0,duration:.4,ease:'power2.in'}},{T(tB)});")
js(f"tl.to('#head',{{y:-18,opacity:0,duration:.3,ease:'power2.in'}},{T(tB)});")
# the idea card (top layer, persistent) shrinks to a mini card top-right
js(f"tl.to('#cardM',{{x:570,y:-125,scale:.36,rotation:4,duration:.6,ease:'expo.inOut'}},{T(tB)});")
js(f"tl.set('#sc',{{visibility:'hidden'}},{T(tB + .75)});")
js(f"tl.fromTo('#img_g',{{scale:1.0}},{{scale:1.22,duration:{tC - tB + .2:.3f},ease:'sine.inOut',transformOrigin:'45% 62%'}},{T(tB)});")
js("gsap.set('#bub_g',{scale:.6,opacity:0});")
tp = max(W(2, 2) - .06, tB + .7)
js(f"tl.fromTo('#bub_g',{{scale:.6,opacity:0,y:30}},{{scale:1,opacity:1,y:0,duration:.42,ease:'back.out(1.5)',transformOrigin:'50% 100%'}},{T(tp)});")
js(f"tl.fromTo('.smile',{{rotation:-14,scale:.5}},{{rotation:8,scale:1,duration:.5,ease:'back.out(2)',transformOrigin:'50% 50%'}},{T(tp + .12)});")
js(f"tl.to('.smile',{{rotation:-6,duration:.6,ease:'sine.inOut',yoyo:true,repeat:{max(1, int((tC - tp) / .6))}}},{T(tp + .7)});")
js(f"tl.fromTo('#chk',{{opacity:0,scale:.2,rotation:-30}},{{opacity:1,scale:1,rotation:0,duration:.4,ease:'back.out(1.8)',transformOrigin:'50% 50%'}},{T(W(2, 3) - .05)});")
js(f"gsap.set('#chk',{{left:766,top:450}});")
sfx("whoosh_a.ogg", tB, -4); sfx("pop_a.ogg", tp + .1, -3); sfx("ding.ogg", W(2, 3) - .02, -4); sfx("pop_b.ogg", tB + .62, -6)

# ---- C: Claude. green panel swipes out left, orange comes in from the right, check goes, marks light up one by one
js(f"tl.to('#pan_g',{{opacity:0,scale:.94,duration:.32,ease:'power2.in',transformOrigin:'50% 50%'}},{T(tC)});")
js(f"tl.set('#pan_g',{{autoAlpha:0}},{T(tC + .34)});")
js(f"gsap.set('#pan_o',{{left:{FULL[0]},top:{FULL[1]},width:{FULL[2]},height:{FULL[3]}}});")
js("gsap.set('#hd_o',{height:120});gsap.set('#bdg_o',{width:76,height:76,borderRadius:20});gsap.set('#nm_o',{maxWidth:380,opacity:1,marginLeft:22});")
js(f"tl.fromTo('#pan_o',{{scale:1.07,opacity:0}},{{scale:1,opacity:1,duration:.5,ease:'expo.out',transformOrigin:'50% 50%'}},{T(tC + .1)});")
js("gsap.set('#pan_o',{autoAlpha:0});")
js(f"tl.set('#pan_o',{{autoAlpha:1}},{T(tC + .1)});")
js(f"tl.fromTo('#img_o',{{scale:1.0}},{{scale:1.2,duration:{tD - tC - .05:.3f},ease:'sine.inOut',transformOrigin:'62% 55%'}},{T(tC + .05)});")
js(f"tl.to('#chk',{{opacity:0,scale:.2,duration:.25,ease:'power2.in'}},{T(tC)});")
js(f"tl.to('#cardM',{{x:-30,y:-135,scale:.5,rotation:-3,duration:.55,ease:'expo.inOut'}},{T(tC + .02)});")
tm = [W(3, 2) - .08, W(3, 2) + .26, W(3, 2) + .6]
for i, t0 in enumerate(tm):
    js(f"tl.fromTo('#mfM{i}',{{scale:1}},{{scale:1.45,duration:.18,ease:'power2.out',yoyo:true,repeat:1,transformOrigin:'50% 50%'}},{T(t0)});")
    js(f"tl.fromTo('#mfM{i} svg',{{rotate:-40}},{{rotate:0,duration:.3,ease:'back.out(2)'}},{T(t0)});")
    sfx("tick.ogg", t0 + .02, -2); sfx("click_a.ogg", t0 + .04, -6)
js(f"tl.set('#mfM0,#mfM1,#mfM2',{{opacity:0}},{T(tC + .1)});")
for i, t0 in enumerate(tm):
    js(f"tl.set('#mfM{i}',{{opacity:1}},{T(t0)});")
tb = max(W(3, 3) - .1, tC + .6)
js(f"tl.fromTo('#bub_o',{{scale:.6,opacity:0,y:30}},{{scale:1,opacity:1,y:0,duration:.42,ease:'back.out(1.4)',transformOrigin:'50% 100%'}},{T(tb)});")
js(f"tl.to('#bub_o',{{scale:1.04,duration:.2,ease:'power2.out',yoyo:true,repeat:1,transformOrigin:'50% 100%'}},{T(W(3, 6) - .05)});")
sfx("whoosh_b.ogg", tC, -4); sfx("impactsoft.ogg", tm[0] - .04, -3); sfx("pop_a.ogg", tb + .1, -4); sfx("subhit.ogg", W(3, 6) - .02, -5)

# ---- D: both panels side by side, text 'Tag someone who needs the cat.' word by word; names off, bubbles off
gx, gy, gw, gh = COL["g"]; ox, oy, ow, oh = COL["o"]
js(f"tl.to('#bub_o',{{opacity:0,y:20,duration:.2,ease:'power2.in'}},{T(tD - .02)});")
js(f"tl.to('#cardM',{{opacity:0,scale:.3,duration:.25,ease:'power2.in'}},{T(tD - .02)});")
js(f"tl.to('#nm_o',{{maxWidth:0,opacity:0,marginLeft:0,duration:.3,ease:'power2.in'}},{T(tD)});")
js(f"tl.to('#pan_o',{{left:{ox},top:{oy},width:{ow},height:{oh},duration:.6,ease:'expo.inOut'}},{T(tD)});")
js(f"tl.set('#pan_g',{{x:0,scale:1,left:{gx},top:{gy},width:{gw},height:{gh},autoAlpha:1,opacity:0}},{T(tD)});")
js(f"gsap.set('#bub_g',{{opacity:0}});")
js(f"tl.set('#bub_g',{{opacity:0,scale:.6}},{T(tD)});")
js(f"tl.set('#nm_g',{{maxWidth:0,opacity:0,marginLeft:0}},{T(tD)});")
js(f"tl.set('#hd_g',{{height:120}},{T(tD)});")
js(f"tl.fromTo('#pan_g',{{opacity:0,scale:.92}},{{opacity:1,scale:1,duration:.5,ease:'expo.out',transformOrigin:'50% 50%'}},{T(tD + .05)});")
js(f"tl.fromTo('#img_g',{{scale:1.05}},{{scale:1.22,duration:{tL - tD:.3f},ease:'sine.inOut',transformOrigin:'45% 62%'}},{T(tD)});")
js(f"tl.fromTo('#img_o',{{scale:1.2}},{{scale:1.1,duration:{tL - tD:.3f},ease:'sine.inOut',transformOrigin:'62% 55%'}},{T(tD)});")
for i in range(6):
    t0 = W(4, i) - .03
    js(f"tl.fromTo('#tw{i}',{{opacity:0,y:22,scale:.9}},{{opacity:1,y:0,scale:1,duration:.3,ease:'power3.out',transformOrigin:'50% 80%'}},{T(max(t0, tD + .3))});")
js(f"tl.to('#pan_o',{{scale:1.05,duration:.22,ease:'power2.out',yoyo:true,repeat:1,transformOrigin:'50% 50%'}},{T(W(4, 5) - .02)});")
js(f"tl.to('#pan_g',{{y:-10,duration:.5,ease:'sine.inOut',yoyo:true,repeat:{max(1, int((tL - tD) / .5))}}},{T(tD + .7)});")
sfx("whoosh_c.ogg", tD, -4); sfx("pop_b.ogg", W(4, 0), -5); sfx("impactsoft.ogg", W(4, 5) - .02, -4); sfx("ding.ogg", E(4) - .02, -8)

# ---- loop: soft crossfade (no wipe) back to the frame-0 copy
js(f"tl.to('#scP',{{opacity:0,duration:.34,ease:'sine.inOut'}},{T(tL)});")
js(f"tl.to('#scC',{{opacity:0,duration:.2}},{T(tL)});")
js(f"tl.fromTo('#scH',{{autoAlpha:0}},{{autoAlpha:1,duration:.34,ease:'sine.inOut'}},{T(tL)});")
sfx("whoosh_b.ogg", tL - .05, -8)

JS = "\n".join(J)
json.dump([dict(f=f, t=t, g=g) for f, t, g in SFX if 0 <= t < D], open(H + "/sfx93.json", "w"), indent=1)
html = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Black.otf");font-weight:900}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-ExtraBold.otf");font-weight:800}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Medium.otf");font-weight:500}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#0e1422;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;font-weight:800;color:#fff}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#0e1422}}
.cam{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
{css}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
{markup}
</div>
<script>
const C={json.dumps(dict(lines=lines, D=D))}; const D={D}; window.__cues=C; window.__CUES=C;
const tl=gsap.timeline({{paused:true}});
{JS}
tl.to({{}},{{duration:.001}},D-.001);
window.__timelines=window.__timelines||{{}}; window.__timelines["main"]=tl; tl.seek(0);
window.__reel={{duration:D,seek:t=>tl.seek(t)}};
</script></body></html>'''
os.makedirs(H + "/hf", exist_ok=True)
open(H + "/hf/index.html", "w").write(html)
print("D=", D, [(l["n"], l["start"], l["end"]) for l in lines], "B,C,D", round(tB, 2), round(tC, 2), round(tD, 2), "sfx", len(SFX))
