#!/usr/bin/env python3
"""ep102 'FREE TWINS #1' (six free, open-source alternatives to paid apps), Miki style, HyperFrames + GSAP paused
timeline, 1080x1920. Model: video/ep100/build100.py.

Reads   voice/lines.txt (15 lines), voice/narration-raw-cues.json and voice/words.json (optional: without them, or if
        they do not match lines.txt, an ESTIMATED timeline is used; SHIP=1 refuses to build then).
Writes  hf/index.html, cues102.json, sfx102.json, out/build.log.

Scenes: 1 OPENING the receipt (lines 1-2: three big logos + "$75 a month", then six rows and the total)
        2-7 one scene per pair (paid row struck out, the free twin card, a real screenshot or a tagged illustration)
        8 END the saveable card (lines 12-14)   9 follow card (line 15).   The running total ($75 down to $0) is the spine.

What is true on screen:
  - Prices: cheapest paid plan on each official pricing page, read 16.11.2026 (Loom Business $18, Notion Plus $10,
    Calendly Standard $10 billed yearly, Intercom Essential $19 with the yearly new-customer rate + $0.99 per Fin
    outcome, Wispr Flow Pro $12 billed yearly, ElevenLabs Starter $6). Sum = $75. Tagged "from".
  - Stars: read from the GitHub repo pages through Exa's fetch on 16.11.2026 and rounded DOWN to whole thousands.
  - Nothing was installed or tested by us: the end card says so.
  - Screenshots are the products' own published images (hf/assets/logos/SOURCES.md). The Cal.diy calendar and the
    OpenWhispr wave/typing are drawings, tagged ILLUSTRATION.
Safe area (CLAUDE.md 15.11): text inside x 108-972, y 269-1248; below y 1056 nothing to read right of x 864.
"""
import json, os, re, shutil, sys, html as _html
H_ = os.path.dirname(os.path.abspath(__file__))
INK = "#0f0f0f"; PAPER = "#fbfbf8"; RED = "#D9281C"; GREEN = "#1F8A4C"; GREY = "#55554f"
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
LOG = []
def say(x): LOG.append(x); print(x)

for sub in ("fonts/InterDisplay-Black.otf", "fonts/InterDisplay-ExtraBold.otf", "fonts/InterDisplay-Medium.otf", "bg.jpg"):
    dst = f"{H_}/hf/assets/{sub}"
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(f"{H_}/../ep100/hf/assets/{sub}", dst)

# ---------------------------------------------------------------- the six pairs (every number has a source; read 16.11.2026)
READ = "16.11.2026"
ITEMS = [
    dict(k=1, paid="Loom", plogo="loom.png", price=18, plan="Business", psrc="loom.com/pricing",
         free="Cap", flogo="cap.png", stars=25113, repo="CapSoftware/Cap", does="screen videos", shot="cap.jpg", shotsrc="image: Cap&rsquo;s own README on GitHub"),
    dict(k=2, paid="Notion", plogo="notion.png", price=10, plan="Plus", psrc="notion.com/pricing",
         free="AppFlowy", flogo="appflowy.svg", stars=78984, repo="AppFlowy-IO/AppFlowy", does="notes, docs, AI", shot="appflowy.jpg", shotsrc="image: appflowy.com"),
    dict(k=3, paid="Calendly", plogo="calendly.svg", price=10, plan="Standard, billed yearly", psrc="calendly.com/pricing",
         free="Cal.diy", flogo="caldiy.png", stars=50090, repo="calcom/cal.diy", does="booking page", shot=None, shotsrc=""),
    dict(k=4, paid="Intercom", plogo="intercom.svg", price=19, plan="Essential, yearly new-customer rate", psrc="intercom.com/pricing",
         free="Chatwoot", flogo="chatwoot.png", stars=39919, repo="chatwoot/chatwoot", does="customer chat", shot="chatwoot.jpg", shotsrc="image: Chatwoot&rsquo;s own README on GitHub"),
    dict(k=5, paid="Wispr Flow", plogo="wisprflow.png", price=12, plan="Pro, billed yearly (it also has a free plan)", psrc="wisprflow.ai/pricing",
         free="OpenWhispr", flogo="openwhispr.svg", stars=11623, repo="OpenWhispr/openwhispr", does="talk to type", shot=None, shotsrc=""),
    dict(k=6, paid="ElevenLabs", plogo="elevenlabs.svg", price=6, plan="Starter", psrc="elevenlabs.io/pricing",
         free="VoiceStudio", flogo="voicestudio.svg", stars=111733, repo="debpalash/VoiceStudio", does="AI voices", shot="voicestudio.jpg", shotsrc="image: VoiceStudio&rsquo;s own README on GitHub"),
]
for it in ITEMS:
    it["starsK"] = f"{it['stars'] // 1000}K+"
    for f in (f"logos/{it['plogo']}", f"logos/{it['flogo']}") + ((f"shots/{it['shot']}",) if it["shot"] else ()):
        assert os.path.exists(f"{H_}/hf/assets/{f}"), f"missing real asset {f}: never redraw it, fetch it (logos/SOURCES.md)"
TOTAL = sum(it["price"] for it in ITEMS); assert TOTAL == 75
RUN = [TOTAL]
for it in ITEMS: RUN.append(RUN[-1] - it["price"])              # 75 57 47 37 18 6 0
assert RUN == [75, 57, 47, 37, 18, 6, 0]
NUMBERS = [dict(text=f"{it['paid']} ${it['price']} a month ({it['plan']})", source=f"{it['psrc']}, read {READ}") for it in ITEMS] + \
          [dict(text=f"{it['free']} {it['starsK']} stars (page said {it['stars']:,})", source=f"github.com/{it['repo']} via Exa page fetch, read {READ}") for it in ITEMS] + \
          [dict(text="$75 a month = the sum of the six prices above", source="OUR ARITHMETIC"),
           dict(text="Intercom + $0.99 per AI answer ('per Fin outcome')", source=f"intercom.com/pricing, read {READ}"),
           dict(text="Cal.diy: personal use only", source="README of github.com/calcom/cal.diy: 'strictly recommended for personal, non-production use'"),
           dict(text="VoiceStudio: 7 months old", source="repo created 2026-04-09 (GitHub page via Exa)")]

# ---------------------------------------------------------------- lines + cues
LINES = [l.strip() for l in open(H_ + "/voice/lines.txt") if l.strip()]
NL = len(LINES); assert NL == 15, "this build is laid out for 15 lines"
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
        WORDS = [[w["word"], w["start"], w["end"]] if isinstance(w, dict) else w for w in WORDS]
    except Exception:
        WORDS = []
if STALE:
    L = {}; t = .08
    for n in range(1, NL + 1):
        d = round(.3 + .05 * len(LINES[n - 1]), 2)
        L[n] = (round(t, 2), round(t + d, 2)); t += d + .1
else:
    L = {n: (float(CUE[n]["start"]), float(CUE[n]["end"])) for n in range(1, NL + 1)}
s = lambda n: L[n][0]
e = lambda n: L[n][1]
SRC = {}; SYNCT = {}
def W(name, word, n, frac, k=0):
    """time of a spoken word inside line n (words.json), else a fraction of the line (ESTIMATE)"""
    c = 0
    for w, a_, b_ in WORDS:
        if s(n) - .12 <= a_ <= e(n) + .12 and norm(w) in (word if isinstance(word, tuple) else (word,)):
            if c == k: SRC[name] = "words.json"; SYNCT[name] = round(a_, 3); return round(a_, 3)
            c += 1
    SRC[name] = "ESTIMATE (line fraction)"; SYNCT[name] = round(s(n) + frac * (e(n) - s(n)), 3)
    return SYNCT[name]
D = round(e(NL) + .6, 2)
tF = D - .58
a = {n: s(n) for n in range(1, NL + 1)}
tTwins = W("twins", ("free", "three"), 1, .62)
tSix = a[2]
tZero = W("zero", ("zero", "0"), 2, .82)
tCap = W("cap", ("cap", "capp", "kap"), 3, .55)
tFree3 = W("free3", "free", 3, .85)
tApp = W("appflowy", ("appflowy", "app", "appflow", "apflowy"), 4, .26)
tAI = W("ai", ("ai", "ais"), 4, .86)
tCal = W("cal", ("cal", "kal", "caldiy", "call"), 5, .32)
tPers = W("personal", "personal", 5, .62)
tSeat = W("seat", ("seat", "seats", "seed"), 6, .42)
tReply = W("reply", "reply", 6, .86)
tChat = a[7]
tHost = W("host", "host", 7, .7)
tOW = W("openwhispr", ("openwhispr", "openwhisper", "open", "openwhisp"), 8, .34)
tTalk = W("talk", "talk", 8, .66)
tBig = W("big", "big", 9, .2)
tEL = W("elevenlabs", ("elevenlabs", "eleven", "11labs", "11"), 9, .5)
tVS = a[10]
tMach = W("machine", "machine", 10, .85)
tNew = W("new", "new", 11, .15)
tTest = W("test", "test", 12, .3)
tSave = a[13]
tSend = W("send", "send", 13, .3)
tFollow = W("follow", "follow", 15, .5)

# ---------------------------------------------------------------- helpers
try:
    from PIL import ImageFont
    _f = ImageFont.truetype(H_ + "/hf/assets/fonts/InterDisplay-Black.otf", 100)
    _m = ImageFont.truetype(H_ + "/hf/assets/fonts/InterDisplay-Medium.otf", 100)
    tw = lambda t: (lambda u: _f.getlength(u) - 3.0 * len(u))(_html.unescape(t))
    twm = lambda t: _m.getlength(_html.unescape(t))
except Exception:
    tw = lambda t: 62 * len(t); twm = lambda t: 52 * len(t)
fit = lambda t, size, mx: min(size, 100 * mx / tw(t))
J = []; SFX = []
def js(x): J.append(x)
def sfx(f, t, g=-8): SFX.append(dict(f=f, t=round(max(0, t), 3), g=g))
def fin(sel, t, d=.4, y=22, blur=8):
    js(f"tl.fromTo('{sel}',{{opacity:0,y:{y},filter:'blur({blur}px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:{d},ease:'power2.out',immediateRender:false}},{max(0, t):.3f});")
def fout(sel, t, d=.24):
    js(f"tl.to('{sel}',{{opacity:0,y:-12,filter:'blur(8px)',duration:{d},ease:'power2.inOut'}},{max(0, t):.3f});")
def pop(sel, t, d=.36, frm=.4, ease="back.out(1.6)"):
    js(f"tl.fromTo('{sel}',{{opacity:0,scale:{frm}}},{{opacity:1,scale:1,duration:{d},ease:'{ease}',immediateRender:false}},{max(0, t):.3f});")
def slam(sel, t, rot):
    js(f"tl.fromTo('{sel}',{{opacity:0,scale:1.7,rotation:{rot - 8}}},{{opacity:1,scale:1,rotation:{rot},duration:.3,ease:'power3.in',immediateRender:false}},{max(0, t):.3f});")
    js(f"tl.fromTo('{sel}',{{y:0}},{{y:6,duration:.09,ease:'sine.inOut',yoyo:true,repeat:3,immediateRender:false}},{t + .3:.3f});")
def idle(sel, t0, t1, prop="y", amp=-9, per=.9):
    if t1 - t0 < per: return
    rep = max(1, int((t1 - t0) / per)) | 1
    b0 = 1 if prop in ("scale", "opacity") else 0
    js(f"tl.fromTo('{sel}',{{{prop}:{b0}}},{{{prop}:{amp},duration:{(t1 - t0) / (rep + 1):.3f},ease:'sine.inOut',yoyo:true,repeat:{rep},immediateRender:false}},{t0:.3f});")
def srcline(txt, top, mx=750, size=25, left=108, id_=""):
    fs = min(size, 100 * mx / twm(txt))
    return f'<div class="src" {f"id={id_}" if id_ else ""} style="left:{left}px;top:{top}px;font-size:{fs:.1f}px;line-height:{fs * 1.25:.1f}px">{txt}</div>'
lg = lambda f, h, cls="", st="": f'<img class="lg {cls}" src="assets/logos/{f}" style="width:{h}px;height:{h}px;{st}">'
ghub = lambda h: f'<img class="lg" src="assets/logos/github-mark.svg" style="width:{h}px;height:{h}px">'
CHK = f'<svg class="chk" viewBox="-20 -20 40 40"><circle r="17" fill="{GREEN}" stroke="{INK}" stroke-width="3.5"/><path d="M-9 1 L-3 7 L10 -7" fill="none" stroke="#fff" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ZIG = "polygon(0 0,100% 0,100% calc(100% - 14px)," + ",".join(f"{100 - i * 2.5:.1f}% {'100%' if i % 2 else 'calc(100% - 14px)'}" for i in range(1, 40)) + ",0 calc(100% - 14px))"

# ---------------------------------------------------------------- scene 1: the receipt (opening)
SC = {}
RX0, RX1 = 150, 930
rows1 = "".join(
    f'<div class="rr" id="rr{it["k"]}" style="top:{306 + i * 100}px">{lg(it["plogo"], 76)}<span class="rn">{it["paid"]}</span><span class="rp">${it["price"]}</span></div>'
    for i, it in enumerate(ITEMS))
SC[1] = f'''<div id="rcp" data-decor></div>
<div id="big3">{lg("loom.png", 210)}{lg("notion.png", 210)}{lg("calendly.svg", 210)}</div>
<div id="b75">$75</div><div id="bmo">A MONTH</div>
<div class="stamp" id="ft">FREE TWINS</div>
{rows1}
<div id="rdash" data-decor></div>
<div id="rtot"><span>TOTAL / MONTH</span><b id="rtn">$75</b></div>
{srcline("from: cheapest paid plan, per person, Nov 2026", 1066, mx=640, size=27, left=184, id_="rsm")}'''

# ---------------------------------------------------------------- scenes 2-7: one pair each
def cal_ill():
    cells = "".join(f'<i class="cc" id="cc{i}" style="left:{26 + (i % 7) * 52}px;top:{62 + (i // 7) * 52}px"></i>' for i in range(21))
    return f'''<div class="ill" id="il3"><div class="itag">ILLUSTRATION</div><div class="calg">{cells}</div>
<div class="ibig" style="left:412px;top:58px">YOU HOST<br>IT YOURSELF</div><div class="isml" style="left:414px;top:170px">needs your own server</div></div>'''
def ow_ill():
    bars = "".join(f'<i class="wb" id="wb{i}" style="left:{30 + i * 22}px"></i>' for i in range(13))
    return f'''<div class="ill" id="il5"><div class="itag">ILLUSTRATION</div><div class="wav">{bars}</div>
<svg class="iarr" viewBox="0 0 70 40"><path d="M4 20 H60 M60 20 L44 6 M60 20 L44 34" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>
<div class="typ" id="typ"></div></div>'''
def pair(it):
    k = it["k"]
    nfs = fit(it["paid"], 76, 430); ffs = fit(it["free"], 104, 560)
    stage = f'<div class="shot" id="sh{k}"><img src="assets/shots/{it["shot"]}"></div>' + srcline(it["shotsrc"], 1210, mx=740, id_=f"ss{k}") if it["shot"] else (cal_ill() if k == 3 else ow_ill())
    extra = ""
    if k == 3: extra = '<div class="stamp tg" id="tg3" style="left:150px;top:1082px">PERSONAL USE ONLY</div>'
    if k == 4: extra = f'''<div class="fee" id="fee1" style="top:640px"><b>$19</b><span>PER SEAT</span></div><div class="fee" id="fee2" style="top:800px"><b>+$0.99</b><span>PER AI ANSWER</span></div>
{srcline(f"intercom.com/pricing, read {READ}", 968, id_="fsrc")}<div class="stamp tg" id="tg4" style="left:270px;top:824px;color:{GREEN};border-color:{GREEN}">FREE IF YOU HOST IT</div>'''
    if k == 6: extra = f'<div id="bigone">THE BIG ONE</div><img id="bigel" class="lg" src="assets/logos/elevenlabs.svg"><div class="stamp tg" id="tg6" style="left:250px;top:824px">NEW: 7 MONTHS OLD</div>'
    return f'''<div class="pd" id="pd{k}">{lg(it["plogo"], 120)}<div class="pn" style="font-size:{nfs:.0f}px">{it["paid"]}</div><div class="pw">{it["does"]}</div>
 <div class="pp" id="pp{k}">${it["price"]}<em>/mo</em></div><div class="sk" id="sk{k}"></div></div>
<div class="tw" id="tw{k}">{lg(it["flogo"], 150)}<div class="tn" style="font-size:{ffs:.0f}px;line-height:{ffs:.0f}px">{it["free"]}</div>
 <div class="ts">{ghub(42)}<span>{it["starsK"]} stars</span><span class="tf">FREE</span></div></div>
{stage}{extra}'''
for it in ITEMS: SC[it["k"] + 1] = pair(it)

# ---------------------------------------------------------------- scene 8: the saveable card, scene 9: follow
crow = lambda i, it: f'''<div class="cr" id="cr{i}" style="top:{118 + i * 98}px">{lg(it["plogo"], 62)}<svg class="carw" viewBox="0 0 50 30"><path d="M3 15 H44 M44 15 L32 5 M44 15 L32 25" fill="none" stroke="{INK}" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/></svg>{lg(it["flogo"], 72)}<span class="cx">{it["free"]}</span><span class="cs">{it["starsK"]}</span></div>'''
SC[8] = f'''<div id="card"><div class="tape t1" data-decor></div><div class="ct">6 FREE TWINS</div><div class="cnote">stars on GitHub,<br>read {READ}</div>
{"".join(crow(i, it) for i, it in enumerate(ITEMS))}
<div class="cf" id="cf1">NOT TESTED BY US. CHECK EACH ONE FIRST.</div></div>
<div id="bio">SETUP: LINK IN BIO</div>'''
SC[9] = '<div id="fcard"><div class="f1">WANT THE NEXT ONE?</div><div class="f2">FOLLOW</div></div>'
scenes = "".join(f'<div class="sc" id="sc{n}">{SC[n]}</div>' for n in sorted(SC))
chips = "".join(f'<div class="chip" id="ch{it["k"]}">{lg(it["plogo"], 58)}<span class="ck" id="ck{it["k"]}">{CHK}</span></div>' for it in ITEMS)
markup = f'''
<div class="bgw" data-decor></div>
<div id="cam">
 {scenes}
 <div id="spine"><div id="spp" data-decor></div><div id="spl">EVERY MONTH</div><div id="spn">$75</div><div id="chips">{chips}</div></div>
</div>'''

CSS = '''
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;color:INK}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}
.bgw{position:absolute;left:-20px;top:-20px;width:1120px;height:1960px;background:#ecebe5 url(assets/bg.jpg);background-size:1120px 1960px}
#cam{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}
.lg{display:block;flex:none;object-fit:contain}
.sc{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0;z-index:3} #sc1{opacity:1}
.sc>*{position:absolute}
.src{position:absolute;font-weight:500;color:#3a3a36;white-space:nowrap;letter-spacing:0}
.stamp{position:absolute;border:8px solid RED;color:RED;border-radius:14px;padding:0 22px;font-weight:900;font-size:64px;line-height:84px;letter-spacing:.04em;white-space:nowrap;transform:rotate(-4deg);z-index:7}
/* 1 the receipt */
#rcp{left:150px;top:240px;width:780px;height:960px;background:#fff;box-shadow:10px 12px 0 rgba(15,15,15,.16);clip-path:ZIG;filter:none}
#big3{left:180px;top:316px;width:720px;display:flex;justify-content:space-between}
#big3 .lg{border-radius:46px;filter:drop-shadow(6px 7px 0 rgba(15,15,15,.9))}
#b75{left:150px;top:560px;width:780px;text-align:center;font-weight:900;font-size:310px;line-height:280px;letter-spacing:-.05em;transform-origin:50% 60%}
#bmo{left:150px;top:842px;width:780px;text-align:center;font-weight:900;font-size:96px;line-height:100px;letter-spacing:-.01em}
#ft{left:262px;top:962px;color:GREEN;border-color:GREEN;font-size:78px;line-height:100px;border-width:10px;transform:rotate(-5deg);transform-origin:50% 50%}
.rr{left:184px;width:712px;height:92px;display:flex;align-items:center;opacity:0;border-bottom:3px dashed rgba(15,15,15,.22)}
.rr .lg{border-radius:18px;box-shadow:0 0 0 3px INK} .rn{margin-left:24px;font-weight:900;font-size:58px;line-height:64px;letter-spacing:-.02em;white-space:nowrap}
.rp{margin-left:auto;font-weight:900;font-size:62px;line-height:64px;letter-spacing:-.03em}
#rdash{left:184px;top:914px;width:712px;height:0;border-top:7px solid INK;opacity:0}
#rtot{left:184px;top:930px;width:712px;height:112px;display:flex;align-items:center;opacity:0;white-space:nowrap}
#rtot span{font-weight:900;font-size:46px;line-height:50px;letter-spacing:.01em} #rtot b{margin-left:auto;font-weight:900;font-size:118px;line-height:112px;letter-spacing:-.04em;transform-origin:100% 60%}
#rsm{opacity:0}
/* the spine: the running total */
#spine{position:absolute;left:0;top:0;width:1080px;height:420px;z-index:6;opacity:0}
#spp{position:absolute;left:84px;top:256px;width:912px;height:166px;background:#fff;box-shadow:8px 9px 0 rgba(15,15,15,.16);clip-path:ZIG}
#spl{position:absolute;left:116px;top:276px;font-weight:900;font-size:30px;line-height:34px;letter-spacing:.08em;color:GREY;white-space:nowrap}
#spn{position:absolute;left:112px;top:306px;font-weight:900;font-size:104px;line-height:104px;letter-spacing:-.04em;white-space:nowrap;transform-origin:0 60%}
#chips{position:absolute;left:478px;top:310px;width:486px;display:flex;justify-content:space-between}
.chip{position:relative;width:66px;height:66px} .chip .lg{border-radius:14px;margin:4px;box-shadow:0 0 0 3px INK}
.ck{position:absolute;right:-12px;bottom:-12px;width:40px;height:40px;opacity:0} .ck svg{width:40px;height:40px;display:block}
/* 2-7 the pairs */
.pd{left:108px;top:446px;width:864px;height:140px}
.pd>*{position:absolute} .pd .lg{left:0;top:10px;border-radius:26px;box-shadow:0 0 0 4px INK}
.pn{left:146px;top:8px;font-weight:900;line-height:84px;letter-spacing:-.03em;white-space:nowrap}
.pw{left:150px;top:92px;font-weight:800;font-size:36px;line-height:40px;color:GREY;white-space:nowrap}
.pp{right:0;top:14px;font-weight:900;font-size:92px;line-height:96px;letter-spacing:-.04em;white-space:nowrap;transform-origin:100% 50%}
.pp em{font-style:normal;font-size:40px;letter-spacing:0;margin-left:4px}
.sk{left:140px;right:-8px;top:52px;height:12px;border-radius:6px;background:RED;transform-origin:0 50%;transform:scaleX(0) rotate(-2deg)}
.tw{left:108px;top:606px;width:856px;height:206px;background:#fff;border:6px solid INK;border-radius:24px;box-shadow:8px 8px 0 INK;opacity:0;transform-origin:50% 50%}
.tw>*{position:absolute} .tw .lg{left:22px;top:22px;border-radius:30px}
.tn{left:198px;top:16px;font-weight:900;letter-spacing:-.035em;white-space:nowrap;height:108px;display:flex;align-items:center}
.ts{left:200px;top:132px;display:flex;align-items:center;gap:14px;font-weight:900;font-size:44px;line-height:50px;white-space:nowrap}
.tf{margin-left:26px;color:GREEN;font-size:54px;letter-spacing:.03em}
.shot{left:108px;top:850px;width:744px;height:344px;border:6px solid INK;border-radius:18px;box-shadow:8px 8px 0 INK;overflow:hidden;background:#fff;opacity:0;transform-origin:50% 50%}
.shot img{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;object-position:50% 0;transform-origin:50% 30%}
.ill{left:108px;top:850px;width:744px;height:344px;border:6px solid INK;border-radius:18px;box-shadow:8px 8px 0 INK;background:#fff;opacity:0;transform-origin:50% 50%}
.ill>*{position:absolute}
.itag{left:24px;top:14px;font-weight:900;font-size:28px;line-height:32px;letter-spacing:.08em;color:GREY}
.calg{left:0;top:0;width:470px;height:300px} .cc{position:absolute;width:42px;height:42px;border:4px solid INK;border-radius:9px;background:#fff}
.ibig{font-weight:900;font-size:46px;line-height:52px;letter-spacing:-.02em;white-space:nowrap} .isml{font-weight:800;font-size:28px;line-height:34px;color:GREY;white-space:nowrap}
.wav{left:0;top:70px;width:330px;height:240px} .wb{position:absolute;top:50%;width:13px;height:200px;margin-top:-100px;border-radius:7px;background:INK;transform:scaleY(.1)}
.iarr{left:322px;top:166px;width:70px;height:40px}
.typ{left:408px;top:112px;width:320px;font-weight:900;font-size:56px;line-height:66px;letter-spacing:-.02em;white-space:pre-line}
.tg{opacity:0;background:rgba(251,251,248,.9);z-index:9;font-size:56px;line-height:76px;transform-origin:50% 50%}
.fee{left:108px;width:864px;display:flex;align-items:baseline;gap:22px;opacity:0;white-space:nowrap;transform-origin:0 50%}
.fee b{font-weight:900;font-size:122px;line-height:130px;letter-spacing:-.05em;color:RED} .fee span{font-weight:900;font-size:47px;line-height:52px;letter-spacing:-.01em}
#fsrc,[id^=ss]{opacity:0}
#bigel{left:390px;top:830px;width:300px;height:300px;border-radius:60px;box-shadow:0 0 0 6px INK,12px 12px 0 INK;opacity:0;transform-origin:50% 50%}
#bigone{left:108px;top:640px;width:864px;text-align:center;font-weight:900;font-size:128px;line-height:150px;letter-spacing:-.04em;white-space:nowrap;opacity:0;transform-origin:50% 50%}
/* 8 the card */
#card{left:108px;top:280px;width:856px;height:796px;background:PAPER;border:6px solid INK;border-radius:12px;box-shadow:12px 12px 0 INK;opacity:0;transform-origin:50% 0%}
.tape{position:absolute;width:130px;height:40px;background:rgba(232,221,186,.86);border:1px solid rgba(0,0,0,.14);z-index:3}
.tape.t1{right:-30px;top:-14px;transform:rotate(30deg)}
.ct{position:absolute;left:28px;top:18px;font-weight:900;font-size:76px;line-height:84px;letter-spacing:-.03em;white-space:nowrap}
.cnote{position:absolute;right:60px;top:26px;text-align:right;font-weight:800;font-size:25px;line-height:30px;color:#3a3a36;white-space:nowrap}
.cr{position:absolute;left:28px;right:28px;height:98px;display:flex;align-items:center;opacity:0;border-top:4px solid rgba(15,15,15,.14);white-space:nowrap}
.cr .lg{border-radius:14px;box-shadow:0 0 0 3px INK} .carw{width:50px;height:30px;margin:0 14px;flex:none}
.cx{margin-left:20px;font-weight:900;font-size:56px;line-height:62px;letter-spacing:-.03em}
.cs{margin-left:auto;font-weight:900;font-size:44px;line-height:50px;color:GREY}
.cf{position:absolute;left:28px;bottom:18px;font-weight:900;font-size:35px;line-height:42px;letter-spacing:-.01em;white-space:nowrap;color:RED;opacity:0}
#bio{left:108px;top:1106px;font-weight:900;font-size:76px;line-height:84px;letter-spacing:-.03em;white-space:nowrap;opacity:0;transform-origin:0 50%}
#fcard{left:120px;top:560px;width:840px;height:420px;background:PAPER;border:6px solid INK;border-radius:12px;box-shadow:14px 14px 0 INK;opacity:0;display:flex;flex-direction:column;align-items:center;justify-content:center;transform-origin:50% 50%}
.f1{font-weight:900;font-size:62px;line-height:70px;letter-spacing:-.02em;white-space:nowrap}
.f2{margin-top:26px;font-weight:900;font-size:176px;line-height:160px;letter-spacing:-.04em;white-space:nowrap;transform-origin:50% 60%}
'''
for a_, b_ in (("ZIG", ZIG), ("GREEN", GREEN), ("GREY", GREY), ("INK", INK), ("PAPER", PAPER), ("RED", RED)):
    CSS = CSS.replace(a_, str(b_))

# ---------------------------------------------------------------- timeline
js(f"tl.fromTo('#cam',{{scale:1,rotation:0}},{{scale:1.012,rotation:.2,duration:{D / 6:.3f},ease:'sine.inOut',yoyo:true,repeat:5}},0);")
js(f"tl.fromTo('.bgw',{{x:0,y:0}},{{x:-14,y:-12,duration:{D / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},0);")
NEWS = [(0, "OPENING: the receipt: Loom, Notion, Calendly logos, $75 A MONTH, FREE TWINS stamp")]
# --- 1 opening. Frame 0 is complete (nothing fades in); it breathes, the stamp lands again on 'free twins'
js(f"tl.fromTo('#b75',{{scale:1}},{{scale:1.05,duration:.42,ease:'sine.inOut',yoyo:true,repeat:{max(1, int((tSix - .3) / .42)) | 1},immediateRender:false}},0.02);")
for i in range(3):
    js(f"tl.fromTo('#big3 .lg:nth-child({i + 1})',{{y:0,rotation:0}},{{y:-16,rotation:{(-4, 3, -3)[i]},duration:.3,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{.06 + i * (max(.25, (tTwins - .1) / 3)):.3f});")
    sfx("pop_a.ogg" if i != 1 else "pop_b.ogg", .06 + i * (max(.25, (tTwins - .1) / 3)), -11)
js(f"tl.fromTo('#ft',{{scale:1,rotation:-5}},{{scale:1.22,rotation:-9,duration:.16,ease:'power2.in',yoyo:true,repeat:1,immediateRender:false}},{tTwins - .05:.3f});")
sfx("subhit.ogg", .03, -7); sfx("impactpunch.ogg", tTwins + .1, -6)
idle("#ft", tTwins + .4, tSix - .05, "rotation", -3, .5)
# line 2: the three logos and the big number fold into six rows with a total
for sel in ("#big3", "#b75", "#bmo", "#ft"):
    js(f"tl.to('{sel}',{{opacity:0,scale:.82,y:-30,duration:.3,ease:'power2.inOut'}},{tSix - .12:.3f});")
sfx("whoosh_a.ogg", tSix - .1, -10)
rstep = min(.13, max(.07, (tZero - tSix - .9) / 6))
for i in range(6):
    t = tSix + .12 + i * rstep
    js(f"tl.fromTo('#rr{i + 1}',{{opacity:0,x:-50}},{{opacity:1,x:0,duration:.32,ease:'power3.out',immediateRender:false}},{t:.3f});"); sfx("tick.ogg", t, -11)
tTot = tSix + .12 + 6 * rstep
fin("#rdash", tTot, .25, 0, 0); fin("#rtot", tTot + .05, .3, 14, 4); fin("#rsm", tTot + .25, .3, 8, 3); sfx("ding.ogg", tTot + .1, -9)
NEWS += [(tSix, "the receipt lists six apps with prices"), (tTot, "TOTAL / MONTH $75")]
js(f"tl.fromTo('#rtn',{{scale:1,color:'{INK}'}},{{scale:1.16,color:'{RED}',duration:.22,ease:'sine.inOut',yoyo:true,repeat:3,immediateRender:false}},{tZero - .25:.3f});")
sfx("riser.ogg", tZero - .5, -12)
NEWS.append((tZero - .25, "the total flashes red: 'watch it hit zero'"))
for i in range(6): idle(f"#rr{i + 1} .lg", tTot + .3 + .08 * i, a[3] - .3, "scale", 1.1, .45)
fout("#sc1", a[3] - .26)
# --- the spine
js(f"tl.fromTo('#spine',{{opacity:0,y:-40}},{{opacity:1,y:0,duration:.4,ease:'power2.out',immediateRender:false}},{a[3] - .05:.3f});")
js(f"tl.to('#spine',{{opacity:0,y:-40,duration:.3,ease:'power2.in'}},{a[12] - .3:.3f});")
# --- the pairs
BEAT = {1: (a[3], tCap, tFree3, a[4]), 2: (a[4], tApp, tApp + .3, a[5]), 3: (a[5], tCal, tCal + .3, a[6]),
        4: (a[6], tChat, tChat + .3, a[8]), 5: (a[8], tOW, tOW + .3, a[9]), 6: (a[9], tVS, tVS + .35, a[12])}
DROPS = []
for it in ITEMS:
    k = it["k"]; t0, tT, tD, t1 = BEAT[k]; tD = min(tD, t1 - .5)
    fin(f"#sc{k + 1}", t0, .32); fout(f"#sc{k + 1}", t1 - .26)
    js(f"tl.fromTo('#pd{k}',{{x:-60,opacity:0}},{{x:0,opacity:1,duration:.34,ease:'power3.out',immediateRender:false}},{t0 + .04:.3f});")
    js(f"tl.fromTo('#pp{k}',{{scale:1}},{{scale:1.14,duration:.2,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{t0 + .36:.3f});")
    js(f"tl.fromTo('#ch{k}',{{scale:1,y:0}},{{scale:1.3,y:-6,duration:.2,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{t0 + .1:.3f});")
    sfx("pop_b.ogg", t0 + .05, -11)
    # the twin arrives
    js(f"tl.fromTo('#tw{k}',{{opacity:0,y:70,rotation:{3 if k % 2 else -3},scale:.86}},{{opacity:1,y:0,rotation:{-1 if k % 2 else 1},scale:1,duration:.42,ease:'back.out(1.5)',immediateRender:false}},{tT - .1:.3f});")
    sfx("whoosh_b.ogg" if k % 2 else "whoosh_c.ogg", tT - .12, -10)
    idle(f"#tw{k}", tT + .45, t1 - .3, "y", -8, .7)
    # the price is struck, the total drops
    js(f"tl.to('#sk{k}',{{scaleX:1,duration:.24,ease:'power2.inOut'}},{tD - .05:.3f});")
    js(f"tl.to('#pd{k} .pn, #pd{k} .pp, #pd{k} .lg',{{opacity:.38,duration:.3,ease:'power2.out'}},{tD + .1:.3f});")
    js(f"tl.fromTo('#ck{k}',{{opacity:0,scale:.2}},{{opacity:1,scale:1,duration:.3,ease:'back.out(2)',immediateRender:false}},{tD + .1:.3f});")
    js(f"tl.to('#ch{k} .lg',{{opacity:.4,duration:.3}},{tD + .1:.3f});")
    js(f"tl.fromTo('#spn',{{scale:1}},{{scale:1.2,duration:.17,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tD + .32:.3f});")
    js(f"tl.fromTo('#tw{k} .tf',{{scale:1}},{{scale:1.3,duration:.2,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false,transformOrigin:'0 50%'}},{tD + .05:.3f});")
    DROPS.append([round(tD, 3), RUN[k - 1], RUN[k]]); sfx("select.ogg", tD, -9); sfx("ding.ogg", tD + .3, -11 if k < 6 else -6)
    NEWS += [(t0, f"{it['paid']} ${it['price']}/mo ({it['does']})"), (tT, f"the free twin: {it['free']}, {it['starsK']} stars"), (tD, f"{it['paid']} struck out, total ${RUN[k - 1]} to ${RUN[k]}")]
    # the stage under the twin
    if it["shot"]:
        tS = tT + .28
        js(f"tl.fromTo('#sh{k}',{{opacity:0,y:90,rotation:{-4 if k % 2 else 4}}},{{opacity:1,y:0,rotation:{1 if k % 2 else -1},duration:.45,ease:'power3.out',immediateRender:false}},{tS:.3f});")
        js(f"tl.fromTo('#sh{k} img',{{scale:1.02}},{{scale:1.2,duration:{max(.6, t1 - tS):.3f},ease:'sine.inOut',immediateRender:false}},{tS:.3f});")
        fin(f"#ss{k}", tS + .3, .3, 8, 3)
        NEWS.append((tS, f"real screenshot of {it['free']}"))
# 3 Cal.diy: calendar illustration + the personal-use stamp
js(f"tl.fromTo('#il3',{{opacity:0,y:90,rotation:4}},{{opacity:1,y:0,rotation:-1,duration:.45,ease:'power3.out',immediateRender:false}},{tCal + .2:.3f});")
cst = max(.05, min(.12, (a[6] - tCal - .9) / 8))
for j, c in enumerate((2, 5, 9, 11, 15, 18)):
    js(f"tl.to('#cc{c}',{{backgroundColor:'{GREEN}',scale:1.15,duration:.2,ease:'back.out(2)'}},{tCal + .55 + j * cst * 1.4:.3f});")
slam("#tg3", tPers, -5); sfx("impactpunch.ogg", tPers + .28, -6); idle("#tg3", tPers + .7, a[6] - .3, "rotation", -3, .5)
NEWS.append((tPers, "stamp PERSONAL USE ONLY; you host it yourself"))
# 4 Intercom: the two fees first (line 6), then Chatwoot (line 7)
js(f"tl.fromTo('#fee1',{{opacity:0,x:-80}},{{opacity:1,x:0,duration:.34,ease:'back.out(1.4)',immediateRender:false}},{tSeat - .25:.3f});")
js(f"tl.fromTo('#fee2',{{opacity:0,x:-80}},{{opacity:1,x:0,duration:.34,ease:'back.out(1.4)',immediateRender:false}},{tReply - .45:.3f});")
sfx("impactsoft.ogg", tSeat - .2, -9); sfx("impactsoft.ogg", tReply - .4, -8); fin("#fsrc", tReply - .2, .3, 8, 3)
idle("#fee1 b", tSeat + .2, tChat - .3, "scale", 1.06, .4); idle("#fee2 b", tReply, tChat - .3, "scale", 1.08, .35)
for sel in ("#fee1", "#fee2", "#fsrc"): js(f"tl.to('{sel}',{{opacity:0,x:120,duration:.26,ease:'power2.in'}},{tChat - .3:.3f});")
slam("#tg4", tHost, 4); sfx("impactpunch.ogg", tHost + .28, -7); idle("#tg4", tHost + .7, a[8] - .3, "rotation", 6, .5)
NEWS += [(tSeat - .25, "$19 per seat"), (tReply - .45, "+ $0.99 per AI answer"), (tHost, "stamp FREE IF YOU HOST IT")]
# 5 OpenWhispr: the wave and the typed words are drawn by render()
js(f"tl.fromTo('#il5',{{opacity:0,y:90,rotation:-4}},{{opacity:1,y:0,rotation:1,duration:.45,ease:'power3.out',immediateRender:false}},{tOW + .2:.3f});")
NEWS.append((tTalk, "illustration: a voice wave turns into typed words"))
# 6 the big one
pop("#bigone", tBig - .08, .4, .5); sfx("riser.ogg", a[9], -11); sfx("impactpunch.ogg", tBig + .05, -5)
idle("#bigone", tBig + .4, tVS - .3, "scale", 1.06, .4)
pop("#bigel", tEL - .1, .4, .3); idle("#bigel", tEL + .35, tVS - .3, "rotation", 5, .35)
js(f"tl.to('#bigel',{{opacity:0,scale:.3,y:-380,x:-330,duration:.28,ease:'power2.in'}},{tVS - .3:.3f});")
js(f"tl.to('#bigone',{{opacity:0,scale:1.5,duration:.26,ease:'power2.in'}},{tVS - .3:.3f});")
slam("#tg6", tNew, -5); sfx("impactsoft.ogg", tNew + .28, -8); idle("#tg6", tNew + .7, a[12] - .3, "rotation", -3, .5)
NEWS += [(tBig, "THE BIG ONE: ElevenLabs"), (DROPS[-1][0] + .3, "the total hits $0"), (tNew, "stamp NEW: 7 MONTHS OLD")]
js(f"tl.to('#spn',{{color:'{GREEN}',duration:.3}},{DROPS[-1][0] + .3:.3f});")
# --- 8 END: the saveable card
fin("#sc8", a[12] - .02, .3)
js(f"tl.fromTo('#card',{{opacity:0,y:120,rotation:3}},{{opacity:1,y:0,rotation:-.6,duration:.5,ease:'power3.out',immediateRender:false}},{a[12]:.3f});")
sfx("whoosh_b.ogg", a[12] - .05, -10)
cstep = min(.2, max(.1, (a[13] - a[12] - .9) / 6))
for i in range(6):
    t = a[12] + .3 + i * cstep
    js(f"tl.fromTo('#cr{i}',{{opacity:0,x:-46}},{{opacity:1,x:0,duration:.32,ease:'power3.out',immediateRender:false}},{t:.3f});"); sfx("pop_a.ogg" if i % 2 == 0 else "pop_b.ogg", t, -11)
fin("#cf1", max(tTest, a[12] + .3), .3, 10, 3)
js(f"tl.fromTo('#cf1',{{scale:1}},{{scale:1.05,duration:.25,ease:'sine.inOut',yoyo:true,repeat:3,immediateRender:false,transformOrigin:'0 50%'}},{max(tTest, a[12] + .3) + .35:.3f});")
for i in range(6):
    js(f"tl.fromTo('#cr{i} .cx',{{x:0}},{{x:14,duration:.2,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tSave + .1 + i * max(.12, (a[14] - tSave - .6) / 6):.3f});")
js(f"tl.fromTo('#card',{{scale:1}},{{scale:1.03,duration:.25,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tSend:.3f});"); sfx("select.ogg", tSave + .05, -10)
js(f"tl.fromTo('#bio',{{opacity:0,x:-60}},{{opacity:1,x:0,duration:.36,ease:'back.out(1.5)',immediateRender:false}},{a[14]:.3f});"); sfx("pop_b.ogg", a[14], -9)
idle("#bio", a[14] + .45, a[15] - .3, "scale", 1.05, .4); idle("#card", a[12] + .8, a[15] - .4, "y", -8, .8)
NEWS += [(a[12], "END: the saveable card, six pairs with stars"), (max(tTest, a[12] + .3), "NOT TESTED BY US. CHECK EACH ONE FIRST."), (a[14], "SETUP: LINK IN BIO")]
fout("#sc8", a[15] - .2)
# --- 9 follow
fin("#sc9", a[15] - .02, .25)
js(f"tl.fromTo('#fcard',{{opacity:0,x:140,rotation:4}},{{opacity:1,x:0,rotation:1,duration:.45,ease:'power3.out',immediateRender:false}},{a[15] + .04:.3f});"); sfx("whoosh_c.ogg", a[15] - .1, -11)
js(f"tl.fromTo('.f2',{{scale:1}},{{scale:1.07,duration:.24,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{tFollow:.3f});"); sfx("select.ogg", tFollow, -9)
idle("#fcard", a[15] + .6, tF - .3, "y", -10, .5)
NEWS.append((a[15], "the FOLLOW card (no promised episode)"))
fout("#sc9", tF - .24)
# --- loop seam: frame 0 comes back
for sel in ("#big3", "#b75", "#bmo"): js(f"tl.set('{sel}',{{opacity:1,scale:1,y:0}},{tF:.3f});")
js(f"tl.set('#ft',{{opacity:1,scale:1,y:0,rotation:-5}},{tF:.3f});")
js(f"tl.set('.rr, #rdash, #rtot, #rsm',{{opacity:0}},{tF:.3f});")
fin("#sc1", tF + .04, .42)
NEWS.append((tF, "frame 0 returns (loop)"))

DATA = dict(D=D, tF=round(tF, 3), DROPS=DROPS, tTalk=tTalk, e8=round(e(8), 3), a9=round(a[9], 3), TYPE="You talk,\nit types.")
RJS = r'''
const Dt=__DATA__;
const ez=p=>{p=p<0?0:p>1?1:p;return p*p*(3-2*p)}, $=s=>document.querySelector(s);
const spn=$('#spn'), typ=$('#typ'), wb=[...document.querySelectorAll('.wb')];
function total(v){let x=75; for(const d of Dt.DROPS){ if(v>=d[0]) x=d[1]+(d[2]-d[1])*ez((v-d[0])/.45) } return Math.round(x)}
function render(v){
  spn.textContent='$'+total(v);
  const talk=v>=Dt.tTalk-.5&&v<Dt.a9;
  wb.forEach((b,i)=>{const h=talk?(.18+.82*Math.abs(Math.sin(v*9+i*1.7)*Math.sin(v*3.1+i*.6))):.1+.05*Math.abs(Math.sin(v*4+i)); b.style.transform='scaleY('+h.toFixed(3)+')'});
  const n=Math.max(0,Math.min(Dt.TYPE.length,Math.floor((v-Dt.tTalk)/Math.max(.2,(Dt.e8-Dt.tTalk))*Dt.TYPE.length*1.05)));
  typ.textContent=Dt.TYPE.slice(0,n)+((v*2.5%1)<.5&&v<Dt.a9?'|':'');
}
'''.replace("__DATA__", json.dumps(DATA, separators=(",", ":")))

NEWS = sorted((round(t, 2), x) for t, x in NEWS)
FLAT = [(NEWS[i][0], NEWS[i + 1][0], NEWS[i][1]) for i in range(len(NEWS) - 1) if NEWS[i + 1][0] - NEWS[i][0] > 2.5]
JS = re.sub(r"tl\.set\(([^,]+),\{", r"tl.set(\1,{immediateRender:false,", "\n".join(J))
SFX.sort(key=lambda x: x["t"])
json.dump(SFX, open(H_ + "/sfx102.json", "w"), indent=1)
if os.environ.get("SHIP") == "1" and STALE:
    sys.exit("SHIP=1 refused: estimated timeline")
json.dump(dict(estimated_timeline=STALE,
               lines=[dict(n=n, text=LINES[n - 1], start=round(s(n), 3), end=round(e(n), 3)) for n in range(1, NL + 1)],
               D=D, frame0_returns=round(tF, 3), sync={k: dict(t=SYNCT[k], source=SRC[k]) for k in SRC}, total_drops=DROPS,
               buildup=dict(new_on_screen=[dict(t=t, what=x) for t, x in NEWS], flat_over_2_5s=[dict(start=a_, end=b_, after=x) for a_, b_, x in FLAT]),
               numbers_on_screen=NUMBERS), open(H_ + "/cues102.json", "w"), indent=1)
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
let _v=0; const clk={{get v(){{return _v}},set v(x){{_v=x;render(x)}}}};
tl.fromTo(clk,{{v:0}},{{v:D,duration:D,ease:'none',immediateRender:false}},0);
{JS}
tl.to({{}},{{duration:.001}},D-.001);
window.__timelines=window.__timelines||{{}}; window.__timelines["main"]=tl; tl.seek(0); render(0);
window.__reel={{duration:D,seek:t=>{{tl.seek(t)}}}};
</script></body></html>'''
os.makedirs(H_ + "/out", exist_ok=True)
open(H_ + "/hf/index.html", "w").write(html)
say(f"estimated timeline={STALE}  D={D}  js={len(J)} sfx={len(SFX)}")
say("lines: " + "  ".join(f"{n}:{s(n):.2f}-{e(n):.2f}" for n in range(1, NL + 1)))
say("sync: " + "  ".join(f"{k}={v['t']}({'w' if v['source'] == 'words.json' else 'EST'})" for k, v in json.load(open(H_ + '/cues102.json'))["sync"].items()))
for t, x in NEWS: say(f"  new {t:6.2f}  {x}")
say("FLAT stretches over 2.5 s with nothing new: " + (str(FLAT) if FLAT else "none"))
open(H_ + "/out/build.log", "w").write("\n".join(LOG) + "\n")
