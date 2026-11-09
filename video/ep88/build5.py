#!/usr/bin/env python3
"""ep88 round 5 builder: fast top-funnel cut. lines5.txt (7 lines) + VOICE/<n>.wav -> cues5.json, out/narration5.wav, sfx5.json, hf/index.html [--render name].
Fonts: Big Shoulders Bold (hero, condensed), Fraunces 600 (contrast serif), Inter Display (UI). All open licence (SIL OFL)."""
import json, os, re, sys, subprocess
import soundfile as sf, numpy as np
H = os.path.dirname(os.path.abspath(__file__))
VOICE = os.environ.get("VOICE", H + "/voice5/final")
GAPS = [float(x) for x in os.environ.get("GAPS", "0.22,0.2,0.22,0.2,0.85,0.3").split(",")]
TAIL = float(os.environ.get("TAIL", "0.9"))
ALL = [l.rstrip("\n") for l in open(H + "/lines5.txt") if l.strip()]
assert len(ALL) == 7 and len(GAPS) == 6
sr = 48000
src = open(H + "/build_head.py").read()
exec(src[src.index("def words_for"):src.index("lines = []; t = 0.0")])   # reuse words_for
tsrc = open(H + "/build_tail_r4a.py").read() if False else open(H + "/build_tail.py").read()
a = tsrc.index("def scene(k):"); b = tsrc.index("def feed(sfx):")
exec(tsrc[a:b])   # drawn everyday scenes

lines = []; t = 0.0; parts = []
for j in range(7):
    n = j + 1
    x, s = sf.read(f"{VOICE}/{n}.wav"); assert s == sr; x = x if x.ndim == 1 else x[:, 0]
    d = len(x) / sr
    lines.append(dict(n=n, text=ALL[j], start=round(t, 3), end=round(t + d, 3), words=words_for(x, ALL[j], t)))
    parts.append((int(t * sr), x)); t += d + (GAPS[j] if j < 6 else 0)
D = round(lines[-1]["end"] + TAIL, 2)
nar = np.zeros(int((D + 0.3) * sr))
for i0, x in parts: nar[i0:i0 + len(x)] += x
os.makedirs(H + "/out", exist_ok=True)
sf.write(H + "/out/narration5.wav", nar[:int(D * sr)], sr, subtype="PCM_16")
json.dump(dict(lines=lines, D=D), open(H + "/cues5.json", "w"), indent=1)
S = lambda n: lines[n - 1]["start"]
E = lambda n: lines[n - 1]["end"]
W = lambda n, i: lines[n - 1]["words"][i][0]

# ---- scene boundaries (all derived from the voice)
B = dict(s1=0.0, s2=S(2) - .05, s3=S(3) - .05, p1=S(4) - .05, p2=W(4, 2) - .05, p3=W(4, 5) - .05, p4=W(4, 6) - .05,
         s5=S(5) - .05, s6=S(6) - .05, s7=S(7) - .05, end=E(7) + .25, loop=E(7) + .45)
T = dict(B)
T.update(dict(tapAllow=W(2, 3), flip=S(5) + .12, slam1=W(1, 6)))
SFX = [  # (file under sfx/, time, gain_db re the -14 dBFS reference)
    ("impactpunch.ogg", 0.04, 0), ("subhit.ogg", 0.04, -3), ("whoosh_a.ogg", 0.0, -2),
    ("click_a.ogg", 0.55, -4), ("click_b.ogg", 0.85, -4), ("click_a.ogg", 1.15, -4),
    ("pop_a.ogg", W(1, 6) - .02, -1),
    ("whoosh_b.ogg", B["s2"] - .06, -2), ("select.ogg", T["tapAllow"], 0), ("pop_b.ogg", T["tapAllow"] + .06, -3),
    ("whoosh_c.ogg", B["s3"] - .05, -4), ("toggle.ogg", B["s3"] + .5, -6),
    ("whoosh_c.ogg", B["p1"] - .05, -5), ("tick.ogg", B["p1"] + .15, -2), ("whoosh_c.ogg", B["p2"] - .05, -6), ("tick.ogg", B["p2"] + .15, -2),
    ("whoosh_c.ogg", B["p3"] - .05, -6), ("tick.ogg", B["p3"] + .15, -2), ("whoosh_c.ogg", B["p4"] - .05, -6), ("tick.ogg", B["p4"] + .15, -2),
    ("whoosh_b.ogg", B["s5"] - .06, -3), ("toggle.ogg", T["flip"] + .22, 0), ("ding.ogg", T["flip"] + .32, -2), ("impactsoft.ogg", T["flip"] + .38, -5),
    ("whoosh_b.ogg", B["s6"] - .06, -3), ("pop_a.ogg", W(6, 2), -3),
    ("riser.ogg", B["s7"] - 2.2, -7), ("whoosh_b.ogg", B["s7"] - .06, -3),
    ("pop_b.ogg", W(7, 5) + .1, -3), ("pop_b.ogg", W(7, 5) + .38, -3), ("ding.ogg", E(7) - .1, -6), ("whoosh_c.ogg", B["loop"] - .1, -5),
]
json.dump([dict(f=f, t=round(tt, 3), g=g) for f, tt, g in SFX if tt < D], open(H + "/sfx5.json", "w"), indent=1)

# ---- markup
def pcard(k, cls, style):
    return (f'<div class="pcard {cls}" style="{style}"><div class="pin">{scene(k)}</div><div class="pvig"></div>'
            f'<b class="pchip">NEVER POSTED</b></div>')

def wd(text, cls=""):
    return "".join(f'<span class="w {cls}">{w}</span> ' for w in text.split())

def stepscene(n, label, ui):
    return (f'<div class="sc" id="p{n}"><div class="cam" id="pc{n}"><div class="pnum" id="pn{n}">{n}</div><div class="plab" id="pl{n}">{label}</div>'
            f'<div class="of4">STEP {n} OF 4</div>{ui}</div></div>')

def skel(y, w=("70%", "50%")):
    return "".join(f'<u class="sk" style="top:{y+i*46}px;width:{ww}"></u>' for i, ww in enumerate(w))

UI1 = ('<div class="uic" id="ui1"><div class="fbbar"><div class="fbbadge"><img src="assets/facebook.svg"></div><div class="fbtitle"></div><div class="avt" id="avt"><i class="avh"></i><i class="avb"></i></div></div>'
       + skel(210) + '<div class="uibig"></div></div>')
UI2 = ('<div class="uic" id="ui2"><div class="row dim"><u class="sk" style="width:46%"></u></div><div class="row dim"><u class="sk" style="width:58%"></u></div>'
       '<div class="row hot" id="hot2"><b>Settings &amp; Privacy</b></div><div class="row dim"><u class="sk" style="width:52%"></u></div><div class="row dim"><u class="sk" style="width:40%"></u></div></div>')
UI3 = ('<div class="uic" id="ui3"><div class="row dim"><u class="sk" style="width:50%"></u></div>'
       '<div class="row hot" id="hot3"><i class="gear"></i><b>Settings</b></div><div class="row dim"><u class="sk" style="width:60%"></u></div><div class="row dim"><u class="sk" style="width:44%"></u></div></div>')
UI4 = ('<div class="uic" id="ui4"><div class="row dim"><u class="sk" style="width:56%"></u></div>'
       '<div class="row hot tall" id="hot4"><b>Camera roll sharing suggestions</b><div class="tg2 on" id="tg4"><i></i></div></div><div class="row dim"><u class="sk" style="width:48%"></u></div>'
       '<div class="uinote">menu names can differ by app version</div></div>')

def chat():
    return ('<div class="outb" id="outb"><div class="mini"><b>Camera roll sharing suggestions</b><div class="tg2" id="tg7"><i></i></div></div></div>'
            '<div class="mavt" id="mav">M</div><div class="dots2" id="dots2"><i></i><i></i><i></i></div>'
            '<div class="alp" id="al1">Allow</div><div class="alp" id="al2">Allow</div><div class="alp" id="al3">Allow</div>')

def hookblock(sfx):
    return (f'<div class="cam" id="hcam{sfx}"><div class="hl1" id="hl1{sfx}">{wd("FACEBOOK CAN LOOK")}</div><div class="hl1" id="hl2{sfx}" style="top:421px">{wd("THROUGH PHOTOS YOU")}</div>'
            f'<div class="hpill" id="hpill{sfx}">NEVER POSTED</div>'
            f'<div class="cards" id="cards{sfx}">{pcard(0, "c1", "")}{pcard(3, "c3", "")}{pcard(1, "c2", "")}</div>'
            f'<div class="fbb" id="fbb{sfx}"><img src="assets/facebook.svg"></div></div>')

markup = f'''
<div class="bgl" id="bgl"></div><div class="vig"></div>
<div class="sc" id="s1" style="opacity:1;visibility:visible">{hookblock("")}</div>
<div class="sc" id="s2"><div class="cam" id="c2"><div class="ht" id="t2" style="top:292px">{wd("ONLY IF YOU TAPPED")}</div>
 <div class="dlg2" id="dlg2"><div class="stack" id="stk">{pcard(0,"d1","")}{pcard(1,"d2","")}{pcard(3,"d3","")}</div>
 <div class="bts"><div class="b1">Not now</div><div class="b2" id="b2">Allow</div></div><div class="ring" id="ring"></div><div class="fing" id="fing"></div></div>
 <div class="tiny" id="ill2">illustration</div></div></div>
<div class="sc" id="s3"><div class="cam" id="c3"><div class="ht" id="t3" style="top:292px">{wd("HERE'S HOW")}<br>{wd("TO STOP IT", "lm")}</div>
 <div class="bigtg" id="bigtg"><i></i></div><div class="tlabel" id="tlab">Camera roll sharing suggestions</div><div class="tiny" id="ill3">drawn example of the switch</div></div></div>
{stepscene(1, "Profile<br>picture", UI1)}
{stepscene(2, "Settings &amp;<br>Privacy", UI2)}
{stepscene(3, "Settings", UI3)}
{stepscene(4, "Camera roll<br>sharing<br>suggestions", UI4)}
<div class="sc" id="s5"><div class="cam" id="c5"><div class="ht" id="t5" style="top:292px">{wd("SWITCH IT OFF")}</div>
 <div class="bigtg2 on" id="bigtg2"><i></i></div><div class="offw" id="offw"><span class="scr" id="scr0">X#7</span><span class="scr" id="scr1">0F?</span><span class="scr" id="scr2">OF#</span><span class="offf" id="offf">OFF</span></div></div></div>
<div class="sc" id="s6"><div class="cam" id="c6"><div class="chip6" id="chip6">META SAYS</div><div class="big6" id="big6">OPT-IN</div><div class="sub6" id="sub6">{wd("NOT USED FOR ADS")}</div>
 <div class="src6" id="src6">Meta newsroom, April 2026 &middot; EU and UK</div></div></div>
<div class="sc" id="s7"><div class="cam" id="c7"><div class="ht" id="t7" style="top:292px;font-size:128px;line-height:122px">{wd("SEND THIS TO SOMEONE")}<br>{wd("WHO ALWAYS TAPS ALLOW", "lm")}</div>{chat()}</div></div>
<div class="sc" id="sH">{hookblock("H")}</div>
<div class="lens" id="lens1"></div><div class="lens l2" id="lens2"></div>
'''

styles = r'''
@font-face{font-family:"BS";src:url("assets/fonts/BigShoulders-Bold.ttf");font-weight:700}
@font-face{font-family:"FR";src:url("assets/fonts/fraunces-latin-600-normal.woff2");font-weight:600}
:root{--paper:#F4F5F8;--ink:#0E0E0E;--fb:#1877F2;--lime:#B6F23A;--lime2:#86D93F;--sh1:0 2px 3px rgba(14,14,14,.10),0 14px 26px -6px rgba(14,14,14,.18),0 50px 80px -22px rgba(14,14,14,.34)}
html,body,#root{background:#EEF1F6}
.bgl{position:absolute;left:0;top:0;width:1080px;height:1920px;background:radial-gradient(900px 820px at 50% 40%,#fff 0%,#F3F5F9 55%,#E5EAF3 100%)}
.bgl:before{content:"";position:absolute;left:-200px;top:900px;width:900px;height:900px;border-radius:50%;background:rgba(24,119,242,.14);filter:blur(120px)}
.bgl:after{content:"";position:absolute;left:520px;top:-200px;width:760px;height:760px;border-radius:50%;background:rgba(182,242,58,.20);filter:blur(120px)}
.vig{position:absolute;left:0;top:0;width:1080px;height:1920px;background:radial-gradient(ellipse 80% 62% at 50% 45%,transparent 58%,rgba(14,14,14,.10) 100%);pointer-events:none;z-index:50}
.sc{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0;visibility:hidden}
.cam{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 700px}
.w{display:inline-block;margin:0 9px;opacity:1;letter-spacing:inherit;font-weight:inherit;line-height:inherit}
.hl1,.ht{position:absolute;left:45px;width:990px;text-align:center;font-family:BS;font-weight:700;color:var(--ink);text-transform:uppercase;letter-spacing:-.005em}
.hl1{top:290px;font-size:136px;line-height:126px}
.ht{font-size:170px;line-height:160px}
.lm{background:var(--lime);padding:0 16px;border-radius:14px;color:var(--ink)}
.hpill{position:absolute;left:150px;top:550px;width:780px;height:150px;border-radius:30px;background:var(--fb);color:#fff;font-family:FR;font-weight:600;font-size:116px;line-height:150px;text-align:center;letter-spacing:-.02em;box-shadow:0 18px 40px -10px rgba(24,119,242,.6)}
.cards{position:absolute;left:0;top:0;width:1080px;height:1920px}
.pcard{position:absolute;overflow:hidden;border-radius:34px;background:#fff;box-shadow:var(--sh1);border:2px solid rgba(255,255,255,.9)}
.pin{position:absolute;inset:0}
.pvig{position:absolute;inset:0;background:radial-gradient(120% 90% at 50% 40%,transparent 55%,rgba(0,0,0,.30))}
.pchip{position:absolute;left:14px;bottom:14px;background:rgba(14,14,14,.82);color:#fff;font:800 24px IDisp;letter-spacing:.05em;padding:7px 14px 9px;border-radius:12px}
.pcard.c1{left:60px;top:772px;width:380px;height:470px;transform:rotate(-7deg)}
.pcard.c3{left:640px;top:772px;width:380px;height:470px;transform:rotate(7deg)}
.pcard.c2{left:350px;top:742px;width:390px;height:500px;transform:rotate(1.5deg);z-index:2}
.fbb{position:absolute;left:390px;top:716px;width:150px;height:150px;border-radius:40px;background:#fff;box-shadow:0 0 70px rgba(24,119,242,.65),var(--sh1);display:flex;align-items:center;justify-content:center;z-index:5}
.fbb img{width:100%;height:100%;padding:12px}
.dlg2{position:absolute;left:65px;top:520px;width:950px;height:700px;border-radius:56px;background:#fff;box-shadow:var(--sh1);overflow:visible}
.stack{position:absolute;left:0;top:0;width:100%;height:410px}
.stack .pcard{width:290px;height:340px;top:50px}
.stack .d1{left:110px;transform:rotate(-8deg)}.stack .d2{left:330px;top:34px;transform:rotate(2deg);z-index:2}.stack .d3{left:550px;transform:rotate(9deg)}
.bts{position:absolute;left:44px;right:44px;bottom:44px;height:210px;display:flex;gap:30px}
.b1{flex:1;border-radius:44px;background:#EEF0F4;color:#6a6f7a;font:800 56px IDisp;display:flex;align-items:center;justify-content:center}
.b2{flex:1.5;border-radius:44px;background:var(--lime);color:var(--ink);font:900 110px IDisp;letter-spacing:-.04em;display:flex;align-items:center;justify-content:center;box-shadow:0 16px 36px -8px rgba(110,170,20,.7),inset 0 -8px 0 rgba(0,0,0,.08)}
.ring{position:absolute;right:210px;bottom:90px;width:110px;height:110px;border-radius:50%;border:10px solid var(--fb);opacity:0}
.fing{position:absolute;right:190px;bottom:20px;width:100px;height:100px;border-radius:50%;background:rgba(14,14,14,.78);opacity:0}
.tiny{position:absolute;left:65px;width:950px;text-align:center;font:700 26px IDisp;letter-spacing:.06em;color:#6a6f7a;text-transform:uppercase}
#ill2{top:1228px}#ill3{top:1210px}
.bigtg{position:absolute;left:190px;top:690px;width:700px;height:330px;border-radius:165px;background:var(--lime2);box-shadow:0 30px 60px -16px rgba(110,170,20,.65),inset 0 -10px 0 rgba(0,0,0,.08)}
.bigtg i{position:absolute;right:20px;top:20px;width:290px;height:290px;border-radius:50%;background:#fff;box-shadow:0 12px 28px rgba(14,14,14,.35)}
.tlabel{position:absolute;left:65px;top:1060px;width:950px;text-align:center;font:900 64px IDisp;letter-spacing:-.04em;line-height:68px}
.pnum{position:absolute;left:70px;top:280px;font-family:BS;font-weight:700;font-size:470px;line-height:440px;color:var(--fb);letter-spacing:-.02em;text-shadow:0 20px 50px rgba(24,119,242,.35)}
.plab{position:absolute;left:330px;top:318px;width:700px;font:900 104px IDisp;line-height:100px;letter-spacing:-.05em}
.of4{position:absolute;left:336px;top:296px;font:800 28px IDisp;letter-spacing:.12em;color:#6a6f7a}
.uic{position:absolute;left:65px;top:760px;width:950px;height:486px;border-radius:48px;background:#fff;box-shadow:var(--sh1);overflow:hidden}
.fbbar{position:absolute;left:0;top:0;width:100%;height:170px;background:#F3F6FB}
.fbbadge{position:absolute;left:36px;top:30px;width:110px;height:110px;border-radius:30px;background:#fff;box-shadow:var(--sh1)}.fbbadge img{width:100%;height:100%;padding:10px}
.avt{position:absolute;right:50px;top:10px;width:150px;height:150px;border-radius:50%;background:linear-gradient(160deg,#9ED8FF,#2D7BE0);overflow:hidden;box-shadow:0 0 0 8px var(--fb),0 0 60px rgba(24,119,242,.6)}
.avh{position:absolute;left:50px;top:28px;width:50px;height:50px;border-radius:50%;background:#fff}.avb{position:absolute;left:28px;top:90px;width:94px;height:80px;border-radius:50% 50% 0 0;background:#fff}
.sk{display:block;position:absolute;left:44px;height:24px;border-radius:12px;background:#D9DEE8;text-decoration:none}
.row{position:absolute;left:30px;right:30px;height:70px;border-radius:24px;margin:0;white-space:normal}
.uic .row:nth-child(1){top:28px}.uic .row:nth-child(2){top:122px}.uic .row:nth-child(3){top:216px}.uic .row:nth-child(4){top:310px}.uic .row:nth-child(5){top:404px}
.row.dim .sk{left:24px;top:23px}
.row.hot{background:#EAF2FE;box-shadow:0 0 0 7px var(--fb),0 0 50px rgba(24,119,242,.5);display:flex;align-items:center;padding:0 30px;gap:20px;height:90px}
.row.hot b{font:900 54px IDisp;letter-spacing:-.04em}
.row.hot.tall{height:150px;top:150px!important}
#ui4 .row:nth-child(3){top:150px}#ui4 .row:nth-child(4){top:330px}
.row.hot.tall b{font-size:50px;line-height:54px;flex:1}
.gear{display:block;width:56px;height:56px;border-radius:50%;border:12px solid #6a6f7a;box-sizing:border-box}
.tg2{position:relative;width:150px;height:84px;border-radius:42px;background:#C9CED8;flex:none}
.tg2 i{position:absolute;left:5px;top:5px;width:74px;height:74px;border-radius:50%;background:#fff;box-shadow:0 4px 10px rgba(14,14,14,.35)}
.tg2.on{background:var(--lime2)}.tg2.on i{left:auto;right:5px}
.uinote{position:absolute;left:0;width:100%;bottom:14px;text-align:center;font:700 26px IDisp;color:#6a6f7a}
.bigtg2{position:absolute;left:100px;top:640px;width:880px;height:420px;border-radius:210px;background:#C9CED8;box-shadow:0 30px 60px -16px rgba(14,14,14,.35),inset 0 -10px 0 rgba(0,0,0,.08)}
.bigtg2 i{position:absolute;left:24px;top:24px;width:372px;height:372px;border-radius:50%;background:#fff;box-shadow:0 14px 34px rgba(14,14,14,.4)}
.bigtg2.on{background:var(--lime2)}.bigtg2.on i{left:auto;right:24px}
.offw{position:absolute;left:65px;top:1090px;width:950px;height:150px;text-align:center;font-family:BS;font-weight:700;font-size:210px;line-height:150px}
.offw span{position:absolute;left:0;width:100%;top:0;opacity:0}
.offf{color:#fff;background:#0E0E0E;border-radius:30px;padding:0 60px;width:auto!important;left:50%!important;transform:translateX(-50%)}
.offw .scr{color:#6a6f7a}
.chip6{position:absolute;left:300px;top:292px;width:480px;text-align:center;background:var(--ink);color:#fff;font:800 50px IDisp;letter-spacing:.1em;padding:10px 0 16px;border-radius:24px;box-shadow:var(--sh1)}
.big6{position:absolute;left:45px;top:430px;width:990px;text-align:center;font-family:BS;font-weight:700;font-size:430px;line-height:400px;color:var(--fb);text-shadow:0 30px 70px rgba(24,119,242,.4)}
.sub6{position:absolute;left:45px;top:850px;width:990px;text-align:center;font-family:BS;font-weight:700;font-size:150px;line-height:150px;color:var(--ink)}
.src6{position:absolute;left:65px;top:1090px;width:950px;text-align:center;font:600 32px IDisp;color:#6a6f7a;letter-spacing:.01em}
.outb{position:absolute;left:105px;top:640px;width:870px;background:var(--ink);border-radius:56px 56px 14px 56px;padding:30px;box-shadow:var(--sh1)}
.mini{background:#fff;border-radius:38px;padding:34px 34px;display:flex;align-items:center;gap:20px;justify-content:space-between}
.mini b{font:900 58px IDisp;letter-spacing:-.04em;line-height:62px}
.mavt{position:absolute;left:65px;top:1086px;width:130px;height:130px;border-radius:50%;background:#FFD84D;font:900 74px IDisp;display:flex;align-items:center;justify-content:center;box-shadow:var(--sh1);opacity:0}
.dots2{position:absolute;left:225px;top:1096px;width:230px;height:112px;background:#fff;border-radius:50px 50px 50px 12px;box-shadow:var(--sh1);display:flex;align-items:center;justify-content:center;gap:18px;opacity:0}
.dots2 i{display:block;width:26px;height:26px;border-radius:50%;background:var(--ink)}
.alp{position:absolute;top:1086px;background:var(--lime);border-radius:44px 44px 44px 12px;box-shadow:0 14px 28px -6px rgba(110,170,20,.65);font:900 68px IDisp;letter-spacing:-.03em;line-height:78px;padding:8px 30px 16px;opacity:0}
#al1{left:212px}#al2{left:478px}#al3{left:744px}
.lens{position:absolute;left:-600px;top:560px;width:620px;height:620px;border-radius:50%;background:radial-gradient(circle at 40% 40%,rgba(24,119,242,.55),rgba(24,119,242,.12));filter:blur(46px);opacity:0;z-index:60;pointer-events:none}
.lens.l2{background:radial-gradient(circle at 40% 40%,rgba(182,242,58,.6),rgba(182,242,58,.1));top:760px;width:520px;height:520px}
.pcard .pchip{font-size:22px}
.stack .pchip{display:none}
'''

js = r'''
const T=%s;
const EA="sine.inOut",EO="power2.out",EX="expo.out";
const Q=s=>document.querySelector(s), QA=s=>[...document.querySelectorAll(s)];
const sceneIn=(id,t,cam)=>{ tl.fromTo('#'+id,{autoAlpha:0},{autoAlpha:1,duration:.2,ease:EA},t); };
const sceneOut=(id,t)=>tl.to('#'+id,{autoAlpha:0,duration:.14,ease:EA},t);
const push=(cam,t0,t1,s0,s1)=>tl.fromTo('#'+cam,{scale:s0||1},{scale:s1||1.06,duration:t1-t0,ease:EA},t0);
const slam=(sel,t0,st,blur)=>tl.fromTo(sel,{scale:1.35,opacity:0,filter:"blur("+(blur||12)+"px)"},{scale:1,opacity:1,filter:"blur(0px)",duration:.4,ease:EX,stagger:st||.07,transformOrigin:"50% 55%"},t0);
const lensCross=(id,t,dur)=>{ tl.fromTo('#'+id,{x:0,opacity:0},{opacity:.9,duration:dur*.3,ease:EA},t); tl.to('#'+id,{x:1900,duration:dur,ease:"power1.inOut"},t); tl.to('#'+id,{opacity:0,duration:dur*.25,ease:EA},t+dur*.75); };
// ---------- S1 hook (frame 0 already composed)
function hook(sfx,t0,t1){
  const h='hcam'+sfx;
  tl.fromTo('#cards'+sfx+' .pcard.c1',{y:90,rotate:-12},{y:0,rotate:-7,duration:.6,ease:EX},t0);
  tl.fromTo('#cards'+sfx+' .pcard.c3',{y:110,rotate:12},{y:0,rotate:7,duration:.6,ease:EX},t0+.05);
  tl.fromTo('#cards'+sfx+' .pcard.c2',{y:70,scale:.94},{y:0,scale:1,duration:.6,ease:EX},t0+.1);
  tl.fromTo('#fbb'+sfx,{scale:.7,rotate:-12},{scale:1,rotate:0,duration:.55,ease:"back.out(2.2)"},t0+.15);
  tl.fromTo('#hl1'+sfx+' .w,#hl2'+sfx+' .w',{scale:1.14,filter:"blur(3px)"},{scale:1,filter:"blur(0px)",duration:.35,ease:EX,stagger:.04,transformOrigin:"50%% 55%%"},t0);
  tl.fromTo('#hpill'+sfx,{scale:1.0},{scale:1.0,duration:.01},t0);
  push(h,t0,t1,1,1.06);
  // slam on the word 'never'
  tl.fromTo('#hpill'+sfx,{scale:1.22,boxShadow:"0 0 0 0 rgba(24,119,242,0.9)"},{scale:1,boxShadow:"0 0 0 40px rgba(24,119,242,0)",duration:.5,ease:EX,immediateRender:false},T.slam1);
  tl.fromTo('#cards'+sfx,{x:0},{x:-30,duration:t1-t0,ease:EA},t0);
}
hook('',0,T.s2+.1);
lensCross('lens1',T.s2-.45,.55);
sceneOut('s1',T.s2-.02);
// ---------- S2 Only if you tapped Allow
sceneIn('s2',T.s2); push('c2',T.s2,T.s3,1,1.06);
slam('#t2 .w',T.s2+.02,.09);
tl.fromTo('#dlg2',{y:110,scale:.94,opacity:0},{y:0,scale:1,opacity:1,duration:.5,ease:EX},T.s2+.1);
tl.fromTo('#stk .pcard',{y:60,opacity:0},{y:0,opacity:1,duration:.45,ease:EX,stagger:.07},T.s2+.25);
tl.fromTo('#fing',{opacity:0,y:60},{opacity:1,y:0,duration:.4,ease:EO},T.tapAllow-.4);
tl.to('#b2',{scale:.94,duration:.14,ease:EA,transformOrigin:"50%% 50%%"},T.tapAllow);
tl.fromTo('#ring',{opacity:.95,scale:.5},{opacity:0,scale:2.6,duration:.7,ease:EO},T.tapAllow+.02);
tl.to('#b2',{scale:1.0,duration:.3,ease:EA},T.tapAllow+.14);
tl.to('#fing',{opacity:0,duration:.3,ease:EA},T.tapAllow+.45);
tl.fromTo('#ill2',{opacity:0},{opacity:1,duration:.3},T.s2+.5);
sceneOut('s2',T.s3-.02);
// ---------- S3 Here's how to stop it
sceneIn('s3',T.s3); push('c3',T.s3,T.p1,1,1.06);
slam('#t3 .w',T.s3+.02,.1);
tl.fromTo('#bigtg',{scale:.86,opacity:0,y:60},{scale:1,opacity:1,y:0,duration:.55,ease:EX},T.s3+.15);
tl.fromTo('#tlab',{opacity:0,y:20},{opacity:1,y:0,duration:.4,ease:EO},T.s3+.4);
tl.fromTo('#ill3',{opacity:0},{opacity:1,duration:.3},T.s3+.6);
tl.to('#bigtg',{y:-10,duration:T.p1-T.s3,ease:EA},T.s3+.7);
sceneOut('s3',T.p1-.02);
// ---------- steps
const steps=[['p1','p2','pc1','pn1','pl1','ui1','avt'],['p2','p3','pc2','pn2','pl2','ui2','hot2'],['p3','p4','pc3','pn3','pl3','ui3','hot3'],['p4','s5','pc4','pn4','pl4','ui4','hot4']];
steps.forEach((s,i)=>{
  const t0=T[s[0]], t1=(s[1]=='s5'?T.s5:T[s[1]]);
  sceneIn(s[0],t0); push(s[2],t0,t1+.1,1,1.07);
  tl.fromTo('#'+s[3],{scale:1.35,opacity:0,filter:"blur(14px)"},{scale:1,opacity:1,filter:"blur(0px)",duration:.38,ease:EX,transformOrigin:"30%% 50%%"},t0+.02);
  tl.fromTo('#'+s[4],{x:60,opacity:0},{x:0,opacity:1,duration:.4,ease:EX},t0+.08);
  tl.fromTo('#'+s[5],{y:90,opacity:0,scale:.95},{y:0,opacity:1,scale:1,duration:.45,ease:EX},t0+.1);
  tl.fromTo('#'+s[6],{scale:1},{scale:1.06,duration:.5,ease:EA,yoyo:true,repeat:2,transformOrigin:"50%% 50%%"},t0+.4);
  if(s[1]!='s5') sceneOut(s[0],t1-.02);
});
sceneOut('p4',T.s5-.02);
// ---------- S5 switch OFF: the proof
sceneIn('s5',T.s5); push('c5',T.s5,T.s6,1,1.07);
slam('#t5 .w',T.s5+.02,.09);
tl.fromTo('#bigtg2',{scale:.9,opacity:0},{scale:1,opacity:1,duration:.4,ease:EX},T.s5+.05);
tl.to('#bigtg2 i',{right:476,duration:.34,ease:"power3.inOut"},T.flip);
tl.to('#bigtg2',{backgroundColor:"#C9CED8",duration:.34,ease:"power3.inOut"},T.flip);
tl.fromTo('#bigtg2',{boxShadow:"0 30px 60px -16px rgba(14,14,14,.35),0 0 0 0 rgba(182,242,58,.9)"},{boxShadow:"0 30px 60px -16px rgba(14,14,14,.35),0 0 0 50px rgba(182,242,58,0)",duration:.6,ease:EO,immediateRender:false},T.flip+.3);
[0,1,2].forEach(i=>{ tl.set('#scr'+i,{opacity:1},T.flip+.34+i*.07); tl.set('#scr'+i,{opacity:0},T.flip+.34+i*.07+.07); });
tl.fromTo('#offf',{scale:1.4,opacity:0,filter:"blur(14px)"},{scale:1,opacity:1,filter:"blur(0px)",duration:.4,ease:EX,transformOrigin:"50%% 50%%"},T.flip+.55);
tl.to('#bigtg2',{y:-8,duration:T.s6-T.s5,ease:EA},T.s5+.5);
sceneOut('s5',T.s6-.02);
// ---------- S6 Meta
sceneIn('s6',T.s6); push('c6',T.s6,T.s7,1,1.06);
tl.fromTo('#chip6',{y:-30,opacity:0},{y:0,opacity:1,duration:.4,ease:EX},T.s6+.02);
tl.fromTo('#big6',{scale:1.4,opacity:0,filter:"blur(16px)"},{scale:1,opacity:1,filter:"blur(0px)",duration:.45,ease:EX,transformOrigin:"50%% 55%%"},T.s6+.1);
slam('#sub6 .w',T.s6+.55,.1);
tl.fromTo('#src6',{opacity:0},{opacity:1,duration:.4},T.s6+1.0);
lensCross('lens2',T.s7-.5,.55);
sceneOut('s6',T.s7-.02);
// ---------- S7 send
sceneIn('s7',T.s7); push('c7',T.s7,T.end,1,1.05);
slam('#t7 .w',T.s7+.02,.07,8);
tl.fromTo('#outb',{x:90,y:30,opacity:0,scale:.94},{x:0,y:0,opacity:1,scale:1,duration:.55,ease:EX},T.s7+.2);
tl.fromTo('#mav',{opacity:0,scale:.6},{opacity:1,scale:1,duration:.4,ease:"back.out(2)"},T.s7+1.0);
tl.fromTo('#dots2',{opacity:0,scale:.8},{opacity:1,scale:1,duration:.35,ease:EO},T.s7+1.1);
tl.to('#dots2 i',{y:-10,duration:.28,ease:EA,yoyo:true,repeat:3,stagger:.09},T.s7+1.2);
tl.to('#dots2',{opacity:0,duration:.18},T.s7+1.75);
[1,2,3].forEach((k,i)=>tl.fromTo('#al'+k,{opacity:0,scale:.6,y:20},{opacity:1,scale:1,y:0,duration:.4,ease:"back.out(2)"},T.s7+1.8+i*.28));
tl.to('#tg7 i',{left:5,duration:.01},T.s7);
sceneOut('s7',T.loop-.1);
// ---------- loop back to frame 0
tl.set('#sH',{autoAlpha:0},0);
tl.fromTo('#sH',{autoAlpha:0},{autoAlpha:1,duration:.3,ease:EA},T.loop-.1);
hook('H',T.loop,D);
'''

html = open(H + "/shell8.html").read()
html = (html.replace("__STYLES__", styles).replace("__MARKUP__", markup).replace("__CHROME__", "").replace("__SCRIPTS__", "")
        .replace("__D__", str(D)).replace("__CUES__", json.dumps(dict(lines=lines, D=D)))
        .replace("__CALLS__", js.replace("const T=%s;", "const T=" + json.dumps(T) + ";").replace("%%", "%")).replace("__NSC__", "1"))
# remove the shell's dotted background layer; our own background replaces it
html = re.sub(r'<div class="abs clip" id="gd".*?</div>', '', html, flags=re.S)
os.makedirs(H + "/hf", exist_ok=True)
open(H + "/hf/index.html", "w").write(html)
print("D=", D, [(l["n"], l["start"], l["end"]) for l in lines])
print("scenes", {k: round(v, 2) for k, v in B.items()})
if "--render" in sys.argv:
    name = sys.argv[sys.argv.index("--render") + 1]
    env = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1", DO_NOT_TRACK="1")
    r = subprocess.run(["npx", "--no-install", "hyperframes", "render", "-o", f"{H}/out/{name}.mp4", "--format", "mp4", "--quiet"],
                       cwd=H + "/hf", env=env, capture_output=True, text=True, timeout=2400)
    print(r.stdout[-400:], r.stderr[-800:])
