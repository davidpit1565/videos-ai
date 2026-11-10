#!/usr/bin/env python3
"""ep91 'Me with Claude / Me with ChatGPT' builder. The star is David's own ChatGPT artwork (assets/m2.png, 1254x1254), shown as two
stacked windows onto the same file (Claude half / ChatGPT half) that crop, push and pan; the only text we add is the headline in the gap.
usage: build91.py -> cues91.json, out/narration91.wav, sfx91.json, hf/index.html"""
import json, os, hashlib, subprocess
import soundfile as sf, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); SR = 48000
GAPS = [float(x) for x in os.environ.get("GAPS", "0.3,0.3,0.3").split(",")]
HEAD = 0.06; TAIL = float(os.environ.get("TAIL", "0.55"))
ALL = [l.rstrip("\n") for l in open(H + "/lines.txt") if l.strip()]; assert len(ALL) == 4
WAV = os.environ.get("VOICE", "a")

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
        if m_ and m_[-1][0].lower().strip('.,') in ('chat','chad') and w[0].lower().strip('.,').startswith('g'): m_[-1] = ['ChatGPT', m_[-1][1], w[2]]
        else: m_.append(list(w))
    return [[round(t0 + a, 3), round(t0 + b, 3)] for _, a, b in m_] if len(m_) == len(text.split()) else None

os.makedirs(H + "/out", exist_ok=True)
xall, s = sf.read(f"{H}/voice/{WAV}.wav"); assert s == SR; xall = xall if xall.ndim == 1 else xall[:, 0]
cus = json.load(open(f"{H}/voice/{WAV}-cues.json"))
lines = []; t = 0.0; parts = []
for j in range(4):
    cu = cus[j]
    a = max(0, int((cu["start"] - HEAD) * SR)); b = min(len(xall), int((cu["end"] + .08) * SR))
    x = xall[a:b]; d = len(x) / SR
    wf = whisper_words(x, ALL[j], t, hashlib.md5(x.tobytes()).hexdigest())
    if not wf:
        words = ALL[j].split(); step = (d - .1) / len(words)
        wf = [[round(t + .05 + i * step, 3), round(t + .05 + (i + 1) * step, 3)] for i in range(len(words))]; print("line", j + 1, "even-spread estimate")
    else: print("line", j + 1, "whisper stamps")
    lines.append(dict(n=j + 1, text=ALL[j], start=round(t + HEAD, 3), end=round(t + d, 3), words=wf))
    parts.append((int(t * SR), x)); t += d + (GAPS[j] if j < 3 else 0)
D = round(lines[-1]["end"] + TAIL, 2)
nar = np.zeros(int((D + .3) * SR))
for i0, x in parts: nar[i0:i0 + len(x)] += x
sf.write(H + "/out/narration91.wav", nar[:int(D * SR)], SR, subtype="PCM_16")
json.dump(dict(lines=lines, D=D), open(H + "/cues91.json", "w"), indent=1)
S = lambda n: lines[n - 1]["start"]; E = lambda n: lines[n - 1]["end"]; W = lambda n, i: lines[n - 1]["words"][i][0]
T = lambda v: f"{max(0.0, v):.3f}"
J = []; SFX = []
js = J.append
def sfx(f, t, g=-4): SFX.append((f, round(t, 3), g))

# layouts: (top-window height, gap, bottom-window height); the stack always starts at y=285 and ends <= 1245 (safe box 269-1248)
L0 = (380, 6, 559)      # frame 0 / loop: the whole image, uncropped
L1 = (330, 104, 520)    # "It listens."
LB = (236, 112, 600)    # ChatGPT beat
LC = (410, 120, 410)    # "Which one are you?"
LD = (330, 170, 440)    # tag line
tB = S(2) - .12; tC = S(3) - .12; tD = S(4) - .14; tL = D - .5; t1 = W(1, 3) - .52
def lay(L, t, dur=.55, ease='expo.inOut'):
    js(f"tl.to(L,{{a:{L[0]},g:{L[1]},b:{L[2]},duration:{dur},ease:'{ease}',onUpdate:R}},{T(t)});")
def view(v, cx, cy, z, t, dur, ease='sine.inOut'):
    js(f"tl.to({v},{{cx:{cx},cy:{cy},z:{z},duration:{dur:.3f},ease:'{ease}',onUpdate:R}},{T(t)});")
def words(h, n, idxs, extra=0.0):
    for k, i in enumerate(idxs):
        js(f"tl.fromTo('#{h}w{k}',{{opacity:0,y:20,scale:.9}},{{opacity:1,y:0,scale:1,duration:.3,ease:'power3.out',immediateRender:false,transformOrigin:'50% 80%'}},{T(W(n, i) - .03 + extra)});")
def hide(h, t): js(f"tl.to('#{h}',{{opacity:0,duration:.12,ease:'sine.in'}},{T(t - .14)});")
def show(h, t): js(f"tl.set('#{h}',{{opacity:1}},{T(t)});")
def bump(p, t, sc=1.035): js(f"tl.to('#{p}',{{scale:{sc},duration:.2,ease:'power2.out',yoyo:true,repeat:1,transformOrigin:'50% 50%'}},{T(t)});")

# A: frame 0 = the whole artwork, then a slow push; the headline strip opens at "It listens"
js(f"tl.to(V1,{{z:1.06,duration:{t1:.3f},ease:'sine.inOut',onUpdate:R}},0);")
js(f"tl.to(V2,{{z:1.05,duration:{t1:.3f},ease:'sine.inOut',onUpdate:R}},0);")
sfx("impactpunch.ogg", .02, -6)
lay(L1, t1, .6)
view("V1", 650, 250, 1.4, t1, .7, 'expo.out')
view("V2", 627, 880, 1.04, t1, .7, 'expo.out')
show("h1", t1 + .3); words("h1", 1, [3, 4])
view("V1", 760, 235, 1.52, t1 + .75, tB - t1 - .75)
sfx("whoosh_a.ogg", t1, -5); sfx("pop_a.ogg", W(1, 3), -6); sfx("tick.ogg", W(1, 4), -5)
# B: ChatGPT, the bottom window takes over, bubble, then punch in on the Step 1..8 board and scroll down it
hide("h1", tB - .02); show("h2", tB + .12)
lay(LB, tB, .6)
js(f"tl.to('#dim1',{{opacity:.5,duration:.4,ease:'power2.out'}},{T(tB)});")
view("V1", 760, 240, 1.6, tB, .8)
view("V2", 640, 800, 1.12, tB, .65, 'expo.out')
tg = W(2, 2)
view("V2", 560, 790, 1.4, tg - .05, .5, 'power3.out')
bump("pan2", tg, 1.02)
words("h2", 2, [3, 4, 5, 6])
tbd = W(2, 4) - .1
view("V2", 960, 700, 2.0, tbd, .6, 'expo.inOut')
view("V2", 960, 940, 2.0, tbd + .62, max(.5, E(2) - tbd - .7), 'sine.inOut')
sfx("whoosh_b.ogg", tB, -4); sfx("pop_a.ogg", tg, -4); sfx("pop_b.ogg", W(2, 3), -6); sfx("whoosh_a.ogg", tbd, -6); sfx("subhit.ogg", W(2, 6) - .02, -5); sfx("tick.ogg", W(2, 4), -6)
# C: both faces, one window each; the windows pop on 'Which' / 'one'
hide("h2", tC - .02); show("h3", tC + .1)
lay(LC, tC, .55)
js(f"tl.to('#dim1',{{opacity:0,duration:.3}},{T(tC)});")
view("V1", 470, 300, 1.55, tC, .6, 'expo.out')
view("V2", 520, 1015, 1.5, tC, .6, 'expo.out')
words("h3", 3, [0, 1, 2, 3])
bump("pan1", W(3, 0), 1.03); bump("pan2", W(3, 1), 1.03)
view("V1", 520, 310, 1.62, tC + .65, tD - tC - .65)
view("V2", 560, 1020, 1.6, tC + .65, tD - tC - .65)
sfx("whoosh_c.ogg", tC, -4); sfx("pop_a.ogg", W(3, 0), -5); sfx("pop_b.ogg", W(3, 1), -5); sfx("ding.ogg", W(3, 3), -6)
# D: tag line
hide("h3", tD - .02); show("h4", tD + .1)
lay(LD, tD, .55)
view("V1", 700, 300, 1.3, tD, .6, 'expo.out')
view("V2", 627, 800, 1.05, tD, .6, 'expo.out')
words("h4", 4, [0, 1, 2], 0); words("h4", 4, [3, 4, 5, 6], 0)
view("V1", 640, 305, 1.1, tD + .65, tL - tD - .65)
bump("pan1", W(4, 5), 1.04)
sfx("whoosh_b.ogg", tD, -4); sfx("pop_b.ogg", W(4, 0), -6); sfx("impactsoft.ogg", W(4, 5) - .02, -4); sfx("ding.ogg", E(4) - .02, -8)
# loop: the same scene eases back to the whole artwork of frame 0
hide("h4", tL)
lay(L0, tL, D - tL - .02, 'sine.inOut')
view("V1", 627, 251, 1.0, tL, D - tL - .02)
view("V2", 627, 886, 1.0, tL, D - tL - .02)
sfx("whoosh_c.ogg", tL - .03, -9)

# ---------------------------------------------------------------- markup
def hl(i, rows):  # rows: list of list of (text, cls)
    inner = "".join('<div class="row">' + "".join(f'<span class="w {c}" id="h{i}w{sum(len(r) for r in rows[:ri]) + k}">{tx}</span>' for k, (tx, c) in enumerate(r)) + '</div>' for ri, r in enumerate(rows))
    return f'<div class="hl s{i}" id="h{i}">{inner}</div>'
markup = f'''
<div class="sc">
<div class="pan" id="pan1"><div class="win" id="win1"><img id="im1" src="assets/m2.png"></div><div class="dim" id="dim1"></div></div>
<div class="pan" id="pan2"><div class="win" id="win2"><img id="im2" src="assets/m2.png"></div></div>
<div class="hw" id="hw">
{hl(1, [[("It", ""), ("listens.", "o")]])}
{hl(2, [[("It's", ""), ("way", ""), ("more", ""), ("complex.", "t")]])}
{hl(3, [[("Which", ""), ("one", ""), ("are", ""), ("you?", "")]])}
{hl(4, [[("Tag", ""), ("someone", ""), ("who", "")], [("needs", ""), ("the", ""), ("Claude", "o"), ("one.", "o")]])}
</div></div>'''
css = r'''
.sc{position:absolute;left:0;top:0;width:1080px;height:1920px}
.pan{position:absolute;left:65px;width:950px;overflow:hidden;border-radius:26px;background:#0b0f1a;z-index:5;transform-origin:50% 50%}
.win{position:absolute;inset:0;overflow:hidden}
#im1,#im2{position:absolute;left:0;top:0;width:1254px;height:1254px;max-width:none;transform-origin:0 0;will-change:transform}
.dim{position:absolute;inset:0;background:#0b0f1a;opacity:0}
.hw{position:absolute;left:65px;width:950px;z-index:8}
.hl{position:absolute;left:0;right:0;top:0;bottom:0;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;font-weight:800;letter-spacing:-.035em;opacity:0}
.row{display:flex;gap:.26em;white-space:nowrap;line-height:1.02}
.w{display:inline-block;opacity:0}
.s1,.s3{font-size:100px}.s2{font-size:84px}.s4{font-size:74px}
.o{color:#ff8a4c}.t{color:#3de8c8}
'''
JS = "\n".join(J)
json.dump([dict(f=f, t=t, g=g) for f, t, g in SFX if 0 <= t < D], open(H + "/sfx91.json", "w"), indent=1)
a0, g0, b0 = L0
html = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Black.otf");font-weight:900}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-ExtraBold.otf");font-weight:800}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Medium.otf");font-weight:500}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#0b0f1a;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;font-weight:800;color:#fff}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#0b0f1a}}
{css}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
{markup}
</div>
<script>
const C={json.dumps(dict(lines=lines, D=D))}; const D={D}; window.__cues=C; window.__CUES=C;
const TOP=285, WW=950, SW=1254, K=WW/SW;
const L={{a:{a0},g:{g0},b:{b0}}};
const V1={{cx:627,cy:251,z:1.0}}, V2={{cx:627,cy:886,z:1.0}};
const R1=[0,503], R2=[519,1254];
function place(id,V,h,R){{
  let sc=Math.max(K*V.z, h/(R[1]-R[0]), WW/SW);
  const hw=WW/2/sc, hh=h/2/sc;
  const cx=Math.min(Math.max(V.cx,hw),SW-hw), cy=Math.min(Math.max(V.cy,R[0]+hh),R[1]-hh);
  document.getElementById('im'+id).style.transform='translate('+(WW/2-cx*sc).toFixed(2)+'px,'+(h/2-cy*sc).toFixed(2)+'px) scale('+sc.toFixed(5)+')';
}}
function R(){{
  const p1=document.getElementById('pan1'),p2=document.getElementById('pan2'),hw=document.getElementById('hw');
  const t2=TOP+L.a+L.g;
  p1.style.top=TOP+'px';p1.style.height=L.a+'px';p2.style.top=t2+'px';p2.style.height=L.b+'px';
  hw.style.top=(TOP+L.a)+'px';hw.style.height=L.g+'px';
  place(1,V1,L.a,R1);place(2,V2,L.b,R2);
}}
R();
const tl=gsap.timeline({{paused:true}});
tl.to({{}},{{duration:D,onUpdate:R}},0);
{JS}
tl.to({{}},{{duration:.001}},D-.001);
window.__timelines=window.__timelines||{{}}; window.__timelines["main"]=tl; tl.seek(0);
window.__reel={{duration:D,seek:t=>tl.seek(t)}};
</script></body></html>'''
open(H + "/hf/index.html", "w").write(html)
print("D=", D, [(l["n"], l["start"], l["end"]) for l in lines], "B,C,D,L", round(tB, 2), round(tC, 2), round(tD, 2), round(tL, 2), "sfx", len(SFX))
