#!/usr/bin/env python3
"""ep90 'My idea has 3 flaws. I show AI.' builder. Dark navy base like the meme C.png, brand-coloured panels (ChatGPT green, Claude orange).
usage: SRC_TAG=a build90.py -> cues90c.json, out/narration90c.wav, sfx90.json, hf/index.html (render is a separate hyperframes call)
Voice: slices of voice/<tag>.wav joined with GAPS (SRC in voice/src.json: {"1":["a",0],...})."""
import json, os, re, sys, hashlib, subprocess
import soundfile as sf, numpy as np
H = os.path.dirname(os.path.abspath(__file__))
SR = 48000
SRC = json.load(open(H + "/voice/src3.json"))
GAPS = [float(x) for x in os.environ.get("GAPS", "0.28,0.28,0.28").split(",")]
HEAD = float(os.environ.get("HEAD", "0.06"))
TAIL = float(os.environ.get("TAIL", "0.5"))
ALL = [l.rstrip("\n") for l in open(H + "/lines3.txt") if l.strip()]
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
sf.write(H + "/out/narration90c.wav", nar[:int(D * SR)], SR, subtype="PCM_16")
json.dump(dict(lines=lines, D=D), open(H + "/cues90c.json", "w"), indent=1)
S = lambda n: lines[n - 1]["start"]
E = lambda n: lines[n - 1]["end"]
W = lambda n, i: lines[n - 1]["words"][i][0]

J = []; SFX = []
def js(s): J.append(s)
def sfx(f, t, g=-4): SFX.append((f, round(t, 3), g))
def T(t): return f"{max(0.0, t):.3f}"

# ------------------------------------------------------------------ geometry (safe box x 65-1015, y 269-1248)
TOP0, H0 = 575, 670      # frame-0 panels
TOPF, HF = 405, 840      # focus (headline line 2 gone)
TOPD, HD = 480, 765      # end (tag text above)

def mark(i):
    x = '<svg viewBox="0 0 40 40"><path d="M11 11L29 29M29 11L11 29" stroke="#fff" stroke-width="5.5" stroke-linecap="round"/></svg>'
    return f'<div class="mk"><div class="mkh"></div><div class="mkf" id="mf{i}">{x}</div></div>'

def idea_card():
    bulb = ('<svg viewBox="0 0 64 64" width="92" height="92"><path d="M32 6c-11 0-19 8-19 18 0 7 4 11 7 15 2 3 3 5 3 8h18c0-3 1-5 3-8 3-4 7-8 7-15 0-10-8-18-19-18z" fill="#FFD21F" stroke="#17130F" stroke-width="3.5"/>'
            '<path d="M24 52h16M26 58h12" stroke="#17130F" stroke-width="4" stroke-linecap="round"/></svg>')
    rows = "".join(f'<div class="row"><i class="bar" style="width:{w}%"></i>{mark(i)}</div>' for i, w in enumerate((64, 50, 72)))
    return f'<div class="card" id="card"><div class="ctop">{bulb}<i class="bar tb"></i></div>{rows}</div>'

def panel(who):
    c = who; logo = "openai.svg" if c == "g" else "claude.svg"; img = "dog.jpg" if c == "g" else "cat3.jpg"
    if c == "g":
        bub = '<div class="bub gb" id="bub_g"><span>Perfect idea!</span><svg class="smile" viewBox="0 0 64 64" width="64" height="64"><circle cx="32" cy="32" r="29" fill="#FFD21F" stroke="#17130F" stroke-width="3.5"/><circle cx="22" cy="26" r="4" fill="#17130F"/><circle cx="42" cy="26" r="4" fill="#17130F"/><path d="M16 38q16 18 32 0" fill="none" stroke="#17130F" stroke-width="4.5" stroke-linecap="round"/></svg></div>'
    else:
        bub = '<div class="bub ob" id="bub_o"><span>3 problems.</span><span>Fix #1 first.</span></div>'
    left = 65 if c == "g" else 555
    return (f'<div class="pan {c}" id="pan_{c}" style="left:{left}px;top:{TOP0}px;width:460px;height:{H0}px"><div class="phw"><img class="pimg" id="img_{c}" src="assets/{img}"></div>'
            f'<div class="dim" id="dim_{c}"></div>{bub}<div class="hd"><div class="bdg"><img src="assets/{logo}"></div><div class="nm">{"ChatGPT" if c == "g" else "Claude"}</div></div></div>')

markup = f'''
<div class="bg" data-decor><div class="glow gl1" id="gl1"></div><div class="glow gl2" id="gl2"></div></div>
<div class="sc"><div class="head" id="head"><div class="hl" id="h1">My idea:</div><div class="hl" id="h2s"><b id="b3">sell ice to penguins.</b></div><div class="hl" id="h3">AI, rate this.</div></div>
<div class="tag" id="tag"><div class="tl"><span id="tw0">Tag</span> <span id="tw1">someone</span> <span id="tw2">who</span></div><div class="tl"><span id="tw3">needs</span> <span id="tw4">the</span> <span class="y" id="tw5">cat.</span></div></div>
{panel("g")}{panel("o")}{idea_card()}
<svg class="chk" id="chk" viewBox="0 0 120 120" width="120" height="120"><circle cx="60" cy="60" r="54" fill="#1f9d55" stroke="#fff" stroke-width="7"/><path d="M34 62l17 17 36-38" fill="none" stroke="#fff" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
'''

css = r'''
.bg{position:absolute;inset:0;background:#0e1422;overflow:hidden}
.glow{position:absolute;border-radius:50%;filter:blur(70px)}
.gl1{left:-300px;top:200px;width:900px;height:900px;background:radial-gradient(circle,rgba(16,163,127,.28),transparent 68%)}
.gl2{left:520px;top:900px;width:900px;height:900px;background:radial-gradient(circle,rgba(217,119,87,.26),transparent 68%)}
.sc{position:absolute;left:0;top:0;width:1080px;height:1920px}
.head{position:absolute;left:65px;top:290px;width:950px;text-align:center;color:#fff;font-weight:800;letter-spacing:-.035em}
.hl{font-size:86px;line-height:92px;white-space:nowrap;width:fit-content;margin:0 auto}.hl b{color:#ffd21f;display:inline-block}
.card{position:absolute;left:380px;top:515px;width:840px;height:440px;background:#f6f1e4;border-radius:34px;box-shadow:0 18px 40px rgba(0,0,0,.5);transform-origin:0 0;z-index:30;opacity:0}
.ctop{position:absolute;left:44px;top:34px;right:44px;height:100px;display:flex;align-items:center;gap:26px}
.bar{display:block;height:34px;border-radius:17px;background:#cfc8b6}.tb{width:46%;height:42px;background:#17130F;opacity:.85}
.row{position:absolute;left:44px;right:44px;height:90px;display:flex;align-items:center;gap:20px}
.row:nth-of-type(2){top:150px}.row:nth-of-type(3){top:250px}.row:nth-of-type(4){top:350px}
.row .bar{flex:none}
.mk{position:absolute;right:0;top:0;width:90px;height:90px}
.mkh{position:absolute;inset:0;border-radius:50%;border:8px solid rgba(229,72,77,.6)}
.mkf{position:absolute;inset:0;border-radius:50%;background:#e5484d;display:flex;align-items:center;justify-content:center;opacity:0}
.mkf svg{width:56px;height:56px}
.bdg{width:84px;height:84px;border-radius:22px;background:#fff;display:flex;align-items:center;justify-content:center;flex:none}
.bdg img{width:62%;height:62%}
.pan{position:absolute;overflow:hidden;border-radius:40px;box-shadow:0 14px 40px rgba(0,0,0,.5);z-index:10}
.pan.g{background:#10a37f}.pan.o{background:#d97757}
.hd{position:absolute;left:0;right:0;top:0;height:110px;display:flex;align-items:center;justify-content:center;gap:16px}.nm{font-size:50px;font-weight:800;color:#fff;letter-spacing:-.02em}
.phw{position:absolute;left:0;right:0;top:110px;bottom:0;overflow:hidden}
.pimg{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;will-change:transform}
#img_g{object-position:50% 58%}#img_o{object-position:62% 40%}
.dim{position:absolute;inset:0;background:#0e1422;opacity:0;pointer-events:none;z-index:5}
.bub{position:absolute;left:14px;right:14px;bottom:18px;background:#fff;border-radius:30px;border:8px solid;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#111;font-weight:800;letter-spacing:-.03em;opacity:0;z-index:20}
.gb{border-color:#10a37f;height:150px;flex-direction:row;gap:10px;font-size:58px;line-height:1}
.ob{border-color:#d97757;height:170px;font-size:56px;line-height:1.08}
.tag{position:absolute;left:65px;top:285px;width:950px;text-align:center;font-weight:800;font-size:80px;line-height:86px;letter-spacing:-.03em;color:#fff}
.tag .tl{white-space:nowrap}.tag span{display:inline-block;opacity:0;margin:0 8px}.tag .y{color:#ffd21f}
.chk{position:absolute;left:0;top:0;opacity:0;z-index:40}
'''

D_ = D
tB = S(2) - .12; tC = S(3) - .12; tD = S(4) - .14; tL = D - .45
SC = .38
js(f"gsap.set('#card',{{left:{555 + 20},top:{TOPF + 110 + 14},scale:{SC},rotation:-3,opacity:0}});")
js(f"gsap.set('#chk',{{left:{65 + 460 - 150},top:{TOPF + 120},opacity:0}});")
js("gsap.set('#bub_g,#bub_o',{opacity:0});")
js(f"tl.fromTo('#gl1',{{x:0,y:0}},{{x:120,y:80,duration:{D_:.3f},ease:'sine.inOut'}},0);")
js(f"tl.fromTo('#gl2',{{x:0,y:0}},{{x:-140,y:-60,duration:{D_:.3f},ease:'sine.inOut'}},0);")

# ---- A: frame 0 is the meme with the idea in big words. dog tilts its head at 'penguins', words bump as they are said
wp, wa = W(1, 5), W(1, 6)
js(f"tl.fromTo('#img_g',{{scale:1,rotation:0}},{{scale:1.06,duration:{tB:.3f},ease:'sine.inOut',transformOrigin:'45% 62%'}},0);")
js(f"tl.fromTo('#img_o',{{scale:1,rotation:0}},{{scale:1.06,duration:{tB:.3f},ease:'sine.inOut',transformOrigin:'62% 50%'}},0);")
js(f"tl.to('#img_g',{{rotation:-5,duration:.45,ease:'sine.inOut',yoyo:true,repeat:1}},{T(max(.5, wp - .5))});")
js(f"tl.to('#img_o',{{rotation:2.5,duration:.6,ease:'sine.inOut',yoyo:true,repeat:1}},{T(max(.9, wp - .2))});")
js(f"tl.fromTo('#b3',{{scale:1}},{{scale:1.08,duration:.25,ease:'power2.out',yoyo:true,repeat:1,transformOrigin:'50% 70%'}},{T(wp)});")
js(f"tl.fromTo('#h3',{{scale:1}},{{scale:1.12,duration:.25,ease:'power2.out',yoyo:true,repeat:1,transformOrigin:'50% 70%'}},{T(wa)});")
js(f"tl.fromTo('#h1',{{scale:1}},{{scale:1.06,duration:.25,ease:'power2.out',yoyo:true,repeat:1,transformOrigin:'50% 70%'}},{T(W(1, 1))});")
sfx("impactpunch.ogg", 0.02, -5); sfx("pop_a.ogg", wp, -6); sfx("tick.ogg", wa, -4)

# ---- B: ChatGPT. headline line 2 leaves, panels grow upward, dog punches in (zoom ~1.15+), cat dims
js(f"tl.to('#h1,#h3',{{opacity:0,y:-14,duration:.25,ease:'power2.in'}},{T(tB)});")
js(f"tl.to('#h2s',{{y:-92,duration:.55,ease:'expo.inOut'}},{T(tB)});")
for w in ("g", "o"):
    js(f"tl.to('#pan_{w}',{{top:{TOPF},height:{HF},duration:.55,ease:'expo.inOut'}},{T(tB)});")
js(f"tl.to('#dim_o',{{opacity:.55,duration:.35,ease:'power2.out'}},{T(tB)});")
js(f"tl.to('#img_g',{{scale:1.27,rotation:0,duration:.55,ease:'expo.out',transformOrigin:'45% 62%'}},{T(tB + .02)});")
js(f"tl.to('#img_g',{{scale:1.36,duration:{tC - tB - .5:.3f},ease:'sine.inOut'}},{T(tB + .57)});")
js(f"tl.to('#pan_g',{{scale:1.03,duration:.3,ease:'power2.out',transformOrigin:'50% 50%'}},{T(tB)});")
tp = max(W(2, 1) - .05, tB + .35)
js(f"tl.fromTo('#bub_g',{{scale:.6,opacity:0,y:30}},{{scale:1,opacity:1,y:0,duration:.4,ease:'back.out(1.5)',transformOrigin:'50% 100%'}},{T(tp)});")
js(f"tl.fromTo('.smile',{{rotation:-14,scale:.5}},{{rotation:8,scale:1,duration:.5,ease:'back.out(2)',transformOrigin:'50% 50%'}},{T(tp + .12)});")
tk = W(2, 2) - .02
js(f"tl.to('#img_g',{{rotation:7,duration:.18,ease:'sine.inOut',yoyo:true,repeat:3}},{T(tp + .05)});")
js(f"tl.to('#pan_g',{{y:-14,duration:.16,ease:'power2.out',yoyo:true,repeat:3}},{T(tp + .05)});")
js(f"tl.fromTo('#chk',{{opacity:0,scale:.2,rotation:-30}},{{opacity:1,scale:1,rotation:0,duration:.35,ease:'back.out(1.8)',transformOrigin:'50% 50%'}},{T(tk)});")
sfx("whoosh_a.ogg", tB, -4); sfx("pop_a.ogg", tp + .08, -3); sfx("ding.ogg", tk, -4)

# ---- C: Claude. dog dims, cat punches in, check leaves, marks light again one by one, bubble pops
js(f"tl.to('#bub_g',{{opacity:0,y:20,duration:.2,ease:'power2.in'}},{T(tC)});")
js(f"tl.to('#dim_g',{{opacity:.55,duration:.35,ease:'power2.out'}},{T(tC)});")
js(f"tl.to('#dim_o',{{opacity:0,duration:.3,ease:'power2.out'}},{T(tC)});")
js(f"tl.to('#pan_g',{{scale:1,duration:.3,ease:'power2.out'}},{T(tC)});")
js(f"tl.to('#pan_o',{{scale:1.03,duration:.3,ease:'power2.out',transformOrigin:'50% 50%'}},{T(tC)});")
js(f"tl.to('#img_o',{{scale:1.25,rotation:0,duration:.55,ease:'expo.out',transformOrigin:'62% 50%'}},{T(tC + .02)});")
tq = W(3, 3)
js(f"tl.to('#img_o',{{scale:1.3,duration:{max(.1, tq - .15 - tC - .57):.3f},ease:'sine.inOut'}},{T(tC + .57)});")
js(f"tl.to('#img_o',{{scale:1.55,rotation:-3,duration:.22,ease:'power3.out'}},{T(tq - .15)});")
js(f"tl.to('#img_o',{{scale:1.4,rotation:0,duration:.7,ease:'sine.inOut'}},{T(tq + .1)});")
js(f"tl.to('#img_o',{{scale:1.48,duration:{max(.2, tD - W(3, 6) - .1):.3f},ease:'sine.inOut'}},{T(W(3, 6) - .05)});")
js(f"tl.fromTo('#card',{{opacity:0,scale:.1,transformOrigin:'0 0'}},{{opacity:1,scale:{SC},duration:.4,ease:'back.out(1.6)',transformOrigin:'0 0',immediateRender:false}},{T(tC + .3)});")
js(f"tl.to('#chk',{{opacity:0,scale:.2,duration:.2,ease:'power2.in'}},{T(tC)});")
js(f"tl.set('#mf0,#mf1,#mf2',{{opacity:0}},{T(tC + .1)});")
tm = [W(3, 2) - .06, W(3, 2) + .28, W(3, 2) + .6]
for i, t0 in enumerate(tm):
    js(f"tl.fromTo('#mf{i}',{{opacity:0,scale:1.5}},{{opacity:1,scale:1,duration:.22,ease:'back.out(2)',transformOrigin:'50% 50%'}},{T(t0)});")
    sfx("tick.ogg", t0 + .02, -2); sfx("click_a.ogg", t0 + .04, -6)
tb = max(W(3, 3) - .1, tC + .5)
js(f"tl.fromTo('#bub_o',{{scale:.6,opacity:0,y:30}},{{scale:1,opacity:1,y:0,duration:.4,ease:'back.out(1.4)',transformOrigin:'50% 100%'}},{T(tb)});")
js(f"tl.to('#bub_o',{{scale:1.05,duration:.2,ease:'power2.out',yoyo:true,repeat:1,transformOrigin:'50% 100%'}},{T(W(3, 6) - .05)});")
sfx("whoosh_b.ogg", tC, -4); sfx("impactsoft.ogg", tm[0], -3); sfx("pop_a.ogg", tb + .1, -4); sfx("subhit.ogg", W(3, 6) - .02, -5)

# ---- D: headline line 1 -> tag sentence, panels settle, both bright again, bump on 'cat.'
js(f"tl.to('#bub_o',{{opacity:0,y:20,duration:.2,ease:'power2.in'}},{T(tD - .02)});")
js(f"tl.to('#card',{{opacity:0,scale:.2,duration:.25,ease:'power2.in',transformOrigin:'0 0'}},{T(tD - .02)});")
js(f"tl.to('#h2s',{{opacity:0,y:-106,duration:.25,ease:'power2.in'}},{T(tD)});")
js(f"tl.to('#dim_g',{{opacity:0,duration:.3}},{T(tD)});")
js(f"tl.to('#pan_o',{{scale:1,duration:.3}},{T(tD)});")
for w in ("g", "o"):
    js(f"tl.to('#pan_{w}',{{top:{TOPD},height:{HD},duration:.5,ease:'expo.inOut'}},{T(tD)});")
js(f"tl.to('#img_g',{{scale:1.18,duration:{tL - tD:.3f},ease:'sine.inOut'}},{T(tD)});")
js(f"tl.to('#img_o',{{scale:1.15,duration:{tL - tD:.3f},ease:'sine.inOut'}},{T(tD)});")
for i in range(6):
    t0 = max(W(4, i) - .03, tD + .3)
    js(f"tl.fromTo('#tw{i}',{{opacity:0,y:22,scale:.9}},{{opacity:1,y:0,scale:1,duration:.3,ease:'power3.out',transformOrigin:'50% 80%'}},{T(t0)});")
js(f"tl.to('#pan_o',{{scale:1.05,duration:.22,ease:'power2.out',yoyo:true,repeat:1,transformOrigin:'50% 50%'}},{T(W(4, 5) - .02)});")
js(f"tl.to('#pan_g',{{y:-10,duration:.5,ease:'sine.inOut',yoyo:true,repeat:{max(1, int((tL - tD - .6) / .5))}}},{T(tD + .5)});")
sfx("whoosh_c.ogg", tD, -4); sfx("pop_b.ogg", W(4, 0), -5); sfx("impactsoft.ogg", W(4, 5) - .02, -4); sfx("ding.ogg", E(4) - .02, -8)

# ---- loop: the same scene eases back to the frame-0 pose (no copy, no wipe)
js(f"tl.to('#tag',{{opacity:0,duration:.15,ease:'sine.inOut'}},{T(tL)});")
js(f"tl.set('#h2s',{{y:0}},{T(tL + .14)});")
js(f"tl.fromTo('#h2s',{{opacity:0,y:-14}},{{opacity:1,y:0,duration:.25,ease:'sine.out',immediateRender:false}},{T(tL + .17)});")
js(f"tl.fromTo('#h1',{{opacity:0,y:-14}},{{opacity:1,y:0,duration:.25,ease:'sine.out',immediateRender:false}},{T(tL + .2)});")
js(f"tl.fromTo('#h3',{{opacity:0,y:-14}},{{opacity:1,y:0,duration:.25,ease:'sine.out',immediateRender:false}},{T(tL + .23)});")
for w in ("g", "o"):
    js(f"tl.to('#pan_{w}',{{top:{TOP0},height:{H0},duration:{D_ - tL - .02:.3f},ease:'sine.inOut'}},{T(tL)});")
    js(f"tl.to('#img_{w}',{{scale:1,rotation:0,duration:{D_ - tL - .02:.3f},ease:'sine.inOut'}},{T(tL)});")
js(f"tl.to('#pan_g',{{y:0,duration:.01}},{T(tL)});")
sfx("whoosh_b.ogg", tL - .03, -8)

JS = "\n".join(J)
json.dump([dict(f=f, t=t, g=g) for f, t, g in SFX if 0 <= t < D], open(H + "/sfx90c.json", "w"), indent=1)
html = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Black.otf");font-weight:900}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-ExtraBold.otf");font-weight:800}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Medium.otf");font-weight:500}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#0e1422;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;font-weight:800;color:#fff}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#0e1422}}
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
open(H + "/hf3/index.html", "w").write(html)
print("D=", D, [(l["n"], l["start"], l["end"]) for l in lines], "B,C,D", round(tB, 2), round(tC, 2), round(tD, 2), "sfx", len(SFX))
