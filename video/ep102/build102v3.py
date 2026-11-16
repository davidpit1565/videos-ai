#!/usr/bin/env python3
"""ep102 v3 'six free alternatives' rebuilt on the episode 89 recipe (video/ep89c) and channel/miki-style-checklist-2026-11-16.md.
ONE idea per screen: either one block of words (small lead-in line + heavy black capitals, built word by word as spoken,
one terracotta accent word with one ring) or ONE card that holds real material (real logos, one real screenshot).
No counters, totals, stamps, source lines, offset shadows or bouncing.

Reads   voice/lines.txt (13 lines), voice/narration-v3-cues.json, voice/words-v3.json (without them: ESTIMATED timeline; SHIP=1 refuses).
Writes  hf/index.html, cues102.json, sfx102.json, out/build-v3.log.

Screens: A hook (line 1): headline + the six paid apps' real logos   B tease (line 2), words only
         C items 1-5 (lines 3-6; line 3 carries items 1 and 2): one dark card, same layout and same motion every time:
           paid logo + name -> the name is struck and greyed -> arrow -> free logo + name -> the word FREE lands on the free row
         D the big one (lines 7-9): words, then the same card for ElevenLabs -> VoiceStudio, then the real screenshot full stage, then "7 MONTHS OLD"
         E not tested (line 10), words only   F the list card (line 11)   G link in bio / follow (lines 12-13), words only
On screen there are no prices and no star counts: only what is spoken. Nothing was installed or tested by us (line 11 says so).
Safe area: text inside x 108-972, y 269-1248; below y 1056 nothing to read right of x 864.
"""
import json, os, re, sys, html as _html
H_ = os.path.dirname(os.path.abspath(__file__))
INK = "#0f0f0f"; ORG = "#D97757"; CARD = "#17181b"; GHOST = "#c4c3bc"; SOFT = "#8d8c86"
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
LOG = []
def say(x): LOG.append(x); print(x)

ITEMS = [
    dict(k=1, paid="Loom", plogo="loom.png", free="Cap", flogo="cap.png", note=""),
    dict(k=2, paid="Notion", plogo="notion.png", free="AppFlowy", flogo="appflowy.svg", note=""),
    dict(k=3, paid="Calendly", plogo="calendly.svg", free="Cal.diy", flogo="caldiy.png", note="personal use only"),
    dict(k=4, paid="Intercom", plogo="intercom.svg", free="Chatwoot", flogo="chatwoot.png", note="if you host it yourself"),
    dict(k=5, paid="Wispr Flow", plogo="wisprflow.png", free="OpenWhispr", flogo="openwhispr.svg", note=""),
    dict(k=6, paid="ElevenLabs", plogo="elevenlabs.svg", free="VoiceStudio", flogo="voicestudio.svg", note=""),
]
for it in ITEMS:
    for f in (it["plogo"], it["flogo"]): assert os.path.exists(f"{H_}/hf/assets/logos/{f}"), f"missing real logo {f} (logos/SOURCES.md)"
assert os.path.exists(f"{H_}/hf/assets/shots/voicestudio.jpg") and os.path.exists(f"{H_}/hf/assets/logos/calendly-wordmark.svg")

# ---------------------------------------------------------------- lines + cues + words
LINES = [l.strip() for l in open(H_ + "/voice/lines.txt") if l.strip()]
NL = len(LINES); assert NL == 13, "v3 is laid out for 13 lines (line 3 carries items 1 and 2)"
try: C = json.load(open(H_ + "/voice/narration-v3-cues.json"))
except Exception: C = []
CUE = {c["n"]: c for c in C if "n" in c}
STALE = os.environ.get("EST") == "1" or len(CUE) != NL or any(n not in CUE or norm(CUE[n]["line"]) != norm(LINES[n - 1]) for n in range(1, NL + 1))
WORDS = []
if not STALE:
    try: WORDS = [[w["word"], w["start"], w["end"]] for w in json.load(open(H_ + "/voice/words-v3.json"))]
    except Exception: WORDS = []
if STALE:
    L = {}; t = .06
    for n in range(1, NL + 1):
        d = round(.35 + .052 * len(LINES[n - 1]), 2); L[n] = (round(t, 2), round(t + d, 2)); t += d + .12
else:
    L = {n: (float(CUE[n]["start"]), float(CUE[n]["end"])) for n in range(1, NL + 1)}
s = lambda n: L[n][0]
e = lambda n: L[n][1]
SRC = {}; SYNCT = {}
def W(name, word, n, frac, k=0):
    c = 0
    for w, a_, b_ in WORDS:
        if s(n) - .12 <= a_ <= e(n) + .12 and norm(w) in (word if isinstance(word, tuple) else (word,)):
            if c == k: SRC[name] = "words"; SYNCT[name] = round(a_, 3); return round(a_, 3)
            c += 1
    SRC[name] = "ESTIMATE"; SYNCT[name] = round(s(n) + frac * (e(n) - s(n)), 3); return SYNCT[name]
D = round(e(NL) + 1.3, 2)                                       # FOLLOW holds with its ring, then frame 0 returns
tF = D - .5
a = {n: s(n) for n in range(1, NL + 1)}

J = []; SFX = []; NEWS = []
def js(x): J.append(x)
def sfx(f, t, g=-12): SFX.append(dict(f=f, t=round(max(0, t), 3), g=g))
EASE = "power2.out"
def fin(sel, t, d=.36, y=16, blur=6):
    js(f"tl.fromTo('{sel}',{{opacity:0,y:{y},filter:'blur({blur}px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:{d},ease:'{EASE}',immediateRender:false}},{max(0, t):.3f});")
def fout(sel, t, d=.24):
    js(f"tl.to('{sel}',{{opacity:0,y:-10,filter:'blur(6px)',duration:{d},ease:'power2.inOut'}},{max(0, t):.3f});")

# ---------------------------------------------------------------- words: lead-in (regular) and heavy lines, built as spoken
WID = [0]
def words(cls, txt, n, fr0, fr1, acc=(), top=None, size=None, ready=False):
    """one line of words; each word turns from ghost to ink at its spoken time (or an even spread between fr0..fr1 of line n)"""
    ws = txt.split(); out = []
    for i, w in enumerate(ws):
        WID[0] += 1; wid = f"w{WID[0]}"
        t = W(wid, norm(w), n, fr0 + (fr1 - fr0) * (i / max(1, len(ws) - 1) if len(ws) > 1 else 0))
        col = ORG if norm(w) in acc else INK
        if ready:
            out.append(f'<span class="w" id="{wid}" style="opacity:1;color:{col}">{w}</span>')
        else:
            out.append(f'<span class="w" id="{wid}">{w}</span>')
            js(f"tl.to('#{wid}',{{opacity:.16,duration:.2,ease:'{EASE}'}},{max(0, t - .32):.3f});")
            js(f"tl.to('#{wid}',{{opacity:1,color:'{col}',duration:.16,ease:'{EASE}'}},{t:.3f});")
        del SRC[wid], SYNCT[wid]
    st = (f"top:{top}px;" if top is not None else "") + (f"font-size:{size}px;line-height:{round(size * 1.1)}px;" if size else "")
    return f'<div class="ln {cls}" style="{st}">{"".join(out)}</div>'
def ring(id_, left, top, w, h):
    return (f'<svg class="ring" id="{id_}" viewBox="0 0 400 160" preserveAspectRatio="none" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px" data-decor>'
            f'<path d="M14 84 C6 30 130 8 214 10 C318 12 394 40 388 84 C382 132 270 150 190 148 C96 146 20 132 14 84 Z" fill="none" stroke="{ORG}" stroke-width="5" vector-effect="non-scaling-stroke" stroke-linecap="round"/></svg>')
def ring_in(id_, t):
    js(f"tl.fromTo('#{id_}',{{opacity:0,scale:.96}},{{opacity:1,scale:1,duration:.6,ease:'{EASE}',immediateRender:false}},{t:.3f});")
lg = lambda f, h, st="": f'<img class="lg" src="assets/logos/{f}" style="width:{h}px;height:{h}px;{st}">'
ARW = lambda id_, col: f'<svg class="arw" id="{id_}" viewBox="0 0 60 90"><path d="M30 6 V78 M30 78 L8 54 M30 78 L52 54" fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>'

SC = {}
# ---------------------------------------------------------------- A hook: headline + the six real logos (frame 0 is complete)
tFree = W("free", "free", 1, .62)
TX = [108, 371, 634]; TY = [722, 985]
tiles = ""
for i, it in enumerate(ITEMS):
    x, y = TX[i % 3], TY[i // 3]
    inner = (lg("calendly.svg", 118, "margin-top:-22px") + '<img class="cwm" src="assets/logos/calendly-wordmark.svg">') if it["paid"] == "Calendly" else lg(it["plogo"], 150)
    tiles += f'<div class="tile" id="t{i}" style="left:{x}px;top:{y}px">{inner}</div>'
SC["A"] = words("lead", "Six apps you pay for have", 1, 0, .5, top=286, size=64, ready=True) + \
          words("hv", "FREE", 1, .62, .62, acc=("free",), top=362, size=176, ready=True) + \
          words("hv", "ALTERNATIVES", 1, .75, .75, top=560, size=114, ready=True) + ring("rgA", 84, 352, 500, 196) + tiles
js(f"tl.fromTo('#rgA',{{opacity:.0,scale:.96}},{{opacity:1,scale:1,duration:.5,ease:'{EASE}',immediateRender:false}},{max(.05, tFree - .1):.3f});")
for i in range(6):                                              # one calm wave through the logos, in reading order
    js(f"tl.fromTo('#t{i}',{{y:0,scale:1}},{{y:-10,scale:1.04,duration:.3,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false}},{.1 + i * max(.2, (e(1) - .5) / 6):.3f});")
sfx("pop_a.ogg", .05, -14); sfx("select.ogg", tFree, -14)
NEWS.append((0, "A: 'Six apps you pay for have FREE ALTERNATIVES' + the six paid apps' real logos"))
fout("#scA", a[2] - .24)
# ---------------------------------------------------------------- B tease: words only
tIns = W("insane", "insane", 2, .5); tStay = W("stay", "stay", 2, .72)
SC["B"] = words("lead", "The last one is", 2, 0, .36, top=380, size=84) + words("hv", "INSANE.", 2, .5, .5, acc=("insane",), top=476, size=214) + \
          ring("rgB", 78, 468, 890, 250) + words("hv", "STAY FOR IT.", 2, .72, .95, top=760, size=128)
fin("#scB", a[2] - .04, .28); ring_in("rgB", tIns + .1); sfx("whoosh_c.ogg", a[2] - .1, -16)
NEWS.append((a[2], "B: words only: 'The last one is INSANE. STAY FOR IT.'"))
fout("#scB", a[3] - .24)
# ---------------------------------------------------------------- the transform card (one layout, one motion, for all six)
def fit(txt, size, mx):
    try:
        from PIL import ImageFont
        f = ImageFont.truetype(H_ + "/hf/assets/fonts/InterDisplay-Black.otf", 100)
        return min(size, 100 * mx / (f.getlength(txt) * .955))
    except Exception: return min(size, mx / (.6 * len(txt)))
def group(it):
    k = it["k"]; ps = fit(it["paid"], 96, 520); fs = fit(it["free"], 132, 560)
    note = f'<div class="nt" id="nt{k}">{it["note"]}</div>' if it["note"] else ""
    return f'''<div class="grp" id="g{k}">
 <div class="prow" id="pr{k}"><div class="lt">{lg(it["plogo"], 116)}</div><div class="pn" style="font-size:{ps:.0f}px">{it["paid"]}<i class="sk" id="sk{k}"></i></div></div>
 {ARW(f"ar{k}", "#f2f2ee")}
 <div class="frow" id="fr{k}"><div class="lt big">{lg(it["flogo"], 150)}</div><div class="fn" style="font-size:{fs:.0f}px;line-height:{fs:.0f}px">{it["free"]}</div></div>
 <div class="free" id="fx{k}">FREE</div>{note}</div>'''
def transform(k, t_in, t_free, t_note=None, first=False):
    """same place, same motion every item: paid row -> strike + grey -> arrow -> free row -> FREE lands on the free row"""
    if first: js(f"tl.set('#g{k}',{{opacity:1}},{t_in:.3f});")
    else: fin(f"#g{k}", t_in, .26, 14, 5)
    js(f"tl.to('#sk{k}',{{scaleX:1,duration:.2,ease:'power2.inOut'}},{t_free - .2:.3f});")
    js(f"tl.to('#pr{k}',{{opacity:.36,duration:.25,ease:'{EASE}'}},{t_free - .1:.3f});")
    js(f"tl.fromTo('#ar{k}',{{opacity:0,y:-18}},{{opacity:1,y:0,duration:.22,ease:'{EASE}',immediateRender:false}},{t_free - .08:.3f});")
    js(f"tl.fromTo('#fr{k}',{{opacity:0,y:18,filter:'blur(5px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:.3,ease:'{EASE}',immediateRender:false}},{t_free + .04:.3f});")
    tx = t_free + .3
    js(f"tl.fromTo('#fx{k}',{{opacity:0,scale:.9}},{{opacity:1,scale:1,duration:.24,ease:'{EASE}',immediateRender:false}},{tx:.3f});")
    sfx("click_a.ogg", t_free - .2, -15); sfx("select.ogg", tx, -13)
    if t_note is not None: fin(f"#nt{k}", max(t_note, tx + .1), .26, 8, 3)
    NEWS.append((round(t_in, 2), f"card: {ITEMS[k - 1]['paid']} (paid)")); NEWS.append((round(t_free, 2), f"{ITEMS[k - 1]['paid']} struck, arrow, {ITEMS[k - 1]['free']}; then FREE lands on {ITEMS[k - 1]['free']} at {tx:.2f}"))
    return tx
SC["C"] = '<div class="comp" id="comp">' + "".join(group(it) for it in ITEMS) + "</div>"
tNotion = W("notion", ("notion", "motion"), 3, .52)
START = {1: a[3], 2: tNotion + .04, 3: a[4], 4: a[5], 5: a[6]}
FREEW = {1: round(a[3] + .70, 3),   # "Cap" starts about 0.75 s into the line (Whisper joins it to "try"), measured on the take
          2: W("appflowy", ("appflowy", "app", "apflowy", "appflow"), 3, .72), 3: W("cal", ("cal", "caldiy", "kal", "cald"), 4, .34),
         4: W("chatwoot", ("chatwoot", "chat", "chatwoo"), 5, .34), 5: W("openwhispr", ("openwhispr", "open", "openwhisper"), 6, .55)}
NOTE = {3: W("personal", ("for", "personal"), 4, .6), 4: W("host", ("if", "host"), 5, .62)}
END = {1: START[2], 2: a[4], 3: a[5], 4: a[6], 5: a[7]}
fin("#scC", a[3] - .04, .28); sfx("whoosh_b.ogg", a[3] - .1, -16)
for k in range(1, 6):
    transform(k, START[k] - (.0 if k == 1 else .02), max(FREEW[k], START[k] + .38), NOTE.get(k), first=(k == 1))
    fout(f"#g{k}", END[k] - .16, .16)
fout("#scC", a[7] - .24)
# ---------------------------------------------------------------- D the big one: words -> the same card -> the real screenshot -> 7 months old
tBig = W("big", "big", 7, .3); tEL = W("eleven", ("elevenlabs", "eleven", "11"), 7, .62)
tVS = max(a[8] + .1, W("vs", ("voicestudio", "voice"), 8, .02)); tClone = W("clones", ("clones", "clone"), 8, .3); tOwn = W("own", "own", 8, .42); tMach = W("machine", "machine", 8, .9)
SC["D1"] = words("lead", "And the", 7, 0, .12, top=420, size=84) + words("hv", "BIG ONE.", 7, .3, .42, acc=("big", "one"), top=516, size=206) + ring("rgD", 78, 508, 900, 244)
fin("#scD1", a[7] - .04, .28); ring_in("rgD", tBig + .25); sfx("riser.ogg", a[7] - .2, -15)
NEWS.append((a[7], "D: words only: 'And the BIG ONE.'"))
tCard6 = max(tEL - .12, a[7] + .7)
fout("#scD1", tCard6 - .22)
SC["D2"] = '<div class="comp" id="comp6">' + group(dict(ITEMS[5], k=7)) + "</div>"
fin("#scD2", tCard6, .28); js(f"tl.set('#g7',{{opacity:1}},{tCard6:.3f});")
ITEMS.append(dict(ITEMS[5], k=7))
transform(7, tCard6, tVS, None, first=True); ITEMS.pop()
tShot = max(tClone - .05, tVS + 1.0)
fout("#scD2", tShot - .22)
SC["D3"] = words("lead", "clones your own voice,", 8, .3, .55, top=300, size=64) + words("hv", "ON YOUR OWN", 8, .62, .8, top=376, size=104) + words("hv", "MACHINE.", 8, .9, .9, top=490, size=104) + \
           '<div class="shot" id="shot"><img src="assets/shots/voicestudio.jpg"></div>'
fin("#scD3", tShot, .3)
js(f"tl.fromTo('#shot img',{{scale:1.0}},{{scale:1.07,duration:{max(1, a[9] - tShot):.3f},ease:'sine.inOut',immediateRender:false}},{tShot:.3f});")
NEWS.append((round(tShot, 2), "the real VoiceStudio screenshot, full stage: 'clones your own voice, ON YOUR OWN MACHINE.'"))
fout("#scD3", a[9] - .24)
SC["D4"] = words("lead", "It's new, just", 9, 0, .3, top=420, size=84) + words("hv", "7 MONTHS", 9, .5, .68, acc=("7", "seven"), top=516, size=158) + words("hv", "OLD.", 9, .9, .9, top=694, size=158)
fin("#scD4", a[9] - .04, .28)
NEWS.append((a[9], "words only: 'It's new, just 7 MONTHS OLD.'"))
fout("#scD4", a[10] - .24)
# ---------------------------------------------------------------- E not tested
SC["E"] = words("lead", "We did", 10, 0, .1, top=400, size=84) + words("hv", "NOT TEST", 10, .2, .32, acc=("not",), top=496, size=176) + words("hv", "THESE.", 10, .44, .44, top=690, size=176) + \
          words("lead", "so check each one yourself.", 10, .58, .95, top=910, size=64)
fin("#scE", a[10] - .04, .28); sfx("click_b.ogg", a[10] + .2, -15)
NEWS.append((a[10], "E: words only: 'We did NOT TEST THESE. so check each one yourself.'"))
fout("#scE", a[11] - .24)
# ---------------------------------------------------------------- F the list card
rows = "".join(f'<div class="lr" id="lr{i}" style="top:{118 + i * 100}px"><div class="lt sm">{lg(it["plogo"], 52)}</div><svg class="la" viewBox="0 0 50 30"><path d="M3 15 H44 M44 15 L32 5 M44 15 L32 25" fill="none" stroke="#8d8c86" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg><div class="lt sm">{lg(it["flogo"], 62)}</div><span class="lx">{it["free"]}</span><span class="lf">FREE</span></div>' for i, it in enumerate(ITEMS))
SC["F"] = f'<div class="comp list" id="lcard"><div class="ltit">Save this list</div>{rows}</div>'
fin("#scF", a[11] - .04, .3); sfx("whoosh_b.ogg", a[11] - .1, -16)
rst = min(.2, max(.1, (e(11) - a[11] - 1.0) / 6))
for i in range(5): fin(f"#lr{i}", a[11] + .15 + i * rst, .26, 10, 3)
NEWS.append((a[11], "F: one card: the list of six pairs to save"))
fout("#scF", a[12] - .24)
# ---------------------------------------------------------------- G link in bio, follow
tFol = W("follow", "follow", 13, .5)
SC["G1"] = words("lead", "The setup's in the", 12, 0, .4, top=420, size=84) + words("hv", "LINK IN BIO.", 12, .55, .9, top=516, size=140)
fin("#scG1", a[12] - .04, .28); fout("#scG1", a[13] - .24)
SC["G2"] = words("lead", "Want the next one?", 13, 0, .35, top=400, size=84) + words("hv", "FOLLOW.", 13, .5, .5, acc=("follow",), top=500, size=206) + ring("rgG", 78, 492, 900, 250)
fin("#scG2", a[13] - .04, .28); ring_in("rgG", tFol + .2); sfx("select.ogg", tFol, -13)
NEWS += [(a[12], "G: words only: 'The setup's in the LINK IN BIO.'"), (a[13], "words only: 'Want the next one? FOLLOW.'")]
fout("#scG2", tF - .26)
js(f"tl.set('#rgA',{{opacity:1,scale:1}},{tF:.3f});")
fin("#scA", tF + .02, .4, 0, 6)
NEWS.append((round(tF, 2), "frame 0 returns (loop)"))

scenes = "".join(f'<div class="sc" id="sc{n}">{SC[n]}</div>' for n in SC)
markup = f'<div class="bgw" data-decor></div><div id="cam">{scenes}</div>'
CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;font-weight:500;color:{INK}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}}
.bgw{{position:absolute;left:-20px;top:-20px;width:1120px;height:1960px;background:#ecebe5 url(assets/bg.jpg);background-size:1120px 1960px}}
#cam{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}}
.sc{{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0}} #scA{{opacity:1}}
.sc>*{{position:absolute}}
.lg{{display:block;flex:none;object-fit:contain}}
.ln{{left:108px;white-space:nowrap}} .w{{display:inline-block;opacity:0}}
.lead .w{{font-weight:500;letter-spacing:-.02em;margin-right:.24em}}
.hv .w{{font-weight:900;letter-spacing:-.045em;margin-right:.2em}}
.ring{{overflow:visible;opacity:0;transform-origin:50% 50%}}
.tile{{width:230px;height:230px;background:#fff;border-radius:44px;box-shadow:0 18px 36px rgba(20,20,20,.16);display:flex;flex-direction:column;align-items:center;justify-content:center;transform-origin:50% 50%}}
.tile .lg{{border-radius:30px}} .cwm{{display:block;width:176px;height:42px;margin-top:10px}}
.comp{{left:108px;top:300px;width:864px;height:744px;background:{CARD};border-radius:44px;box-shadow:0 26px 50px rgba(20,20,20,.28);border:2px solid #2b2c32}}
.grp{{position:absolute;left:0;top:0;width:864px;height:744px;opacity:0}} .grp>*{{position:absolute}}
.lt{{width:150px;height:150px;border-radius:34px;background:#fff;display:flex;align-items:center;justify-content:center;flex:none}} .lt .lg{{border-radius:22px}}
.lt.big{{width:190px;height:190px;border-radius:42px}} .lt.sm{{width:76px;height:76px;border-radius:18px}} .lt.sm .lg{{border-radius:10px}}
.prow{{left:56px;top:56px;width:760px;height:150px;display:flex;align-items:center;gap:34px}}
.pn{{position:relative;font-weight:900;letter-spacing:-.04em;color:#f2f2ee;white-space:nowrap;line-height:1.1}}
.sk{{position:absolute;left:-10px;right:-10px;top:52%;height:9px;border-radius:5px;background:#f2f2ee;transform-origin:0 50%;transform:scaleX(0)}}
.arw{{left:101px;top:226px;width:60px;height:90px;opacity:0}}
.frow{{left:36px;top:338px;width:800px;height:190px;display:flex;align-items:center;gap:34px;opacity:0}}
.fn{{font-weight:900;letter-spacing:-.045em;color:#fff;white-space:nowrap}}
.free{{left:258px;top:540px;font-weight:900;font-size:124px;line-height:130px;letter-spacing:-.03em;color:{ORG};opacity:0;transform-origin:0 50%;white-space:nowrap}}
.nt{{left:262px;top:672px;font-weight:500;font-size:44px;line-height:50px;letter-spacing:-.01em;color:#b9b8b2;opacity:0;white-space:nowrap}}
.shot{{left:108px;top:628px;width:756px;height:525px;border-radius:30px;box-shadow:0 26px 50px rgba(20,20,20,.28);overflow:hidden;background:{CARD}}}
.shot img{{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;transform-origin:30% 40%}}
.comp.list{{height:744px}} .ltit{{position:absolute;left:44px;top:30px;font-weight:900;font-size:60px;line-height:70px;letter-spacing:-.03em;color:#fff;white-space:nowrap}}
.lr{{position:absolute;left:44px;right:44px;height:92px;display:flex;align-items:center;gap:16px;opacity:0;white-space:nowrap}}
.la{{width:46px;height:28px;flex:none}} .lx{{margin-left:10px;font-weight:900;font-size:60px;line-height:66px;letter-spacing:-.035em;color:#fff}}
.lf{{margin-left:auto;font-weight:900;font-size:44px;line-height:50px;letter-spacing:.01em;color:{ORG}}}
'''
js(f"tl.fromTo('#cam',{{scale:1}},{{scale:1.012,duration:{D / 4:.3f},ease:'sine.inOut',yoyo:true,repeat:3}},0);")
js(f"tl.fromTo('.bgw',{{x:0,y:0}},{{x:-14,y:-12,duration:{D / 2:.3f},ease:'sine.inOut',yoyo:true,repeat:1}},0);")
NEWS = sorted((round(t, 2), x) for t, x in NEWS)
FLAT = [(NEWS[i][0], NEWS[i + 1][0], NEWS[i][1]) for i in range(len(NEWS) - 1) if NEWS[i + 1][0] - NEWS[i][0] > 2.5]
JS = re.sub(r"tl\.set\(([^,]+),\{", r"tl.set(\1,{immediateRender:false,", "\n".join(J))
SFX.sort(key=lambda x: x["t"]); json.dump(SFX, open(H_ + "/sfx102.json", "w"), indent=1)
if os.environ.get("SHIP") == "1" and STALE: sys.exit("SHIP=1 refused: estimated timeline")
json.dump(dict(version="v3", estimated_timeline=STALE, lines=[dict(n=n, text=LINES[n - 1], start=round(s(n), 3), end=round(e(n), 3)) for n in range(1, NL + 1)],
               D=D, frame0_returns=round(tF, 3), sync={k: dict(t=SYNCT[k], source=SRC[k]) for k in SRC},
               buildup=dict(new_on_screen=[dict(t=t, what=x) for t, x in NEWS], flat_over_2_5s=[dict(start=a_, end=b_, after=x) for a_, b_, x in FLAT]),
               numbers_on_screen=[dict(text="7 MONTHS OLD (VoiceStudio)", source="repo created 2026-04-09, GitHub page via Exa, read 16.11.2026")]), open(H_ + "/cues102.json", "w"), indent=1)
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
const D={D}; const tl=gsap.timeline({{paused:true}});
{JS}
tl.to({{}},{{duration:.001}},D-.001);
window.__timelines=window.__timelines||{{}}; window.__timelines["main"]=tl; tl.seek(0);
window.__reel={{duration:D,seek:t=>{{tl.seek(t)}}}};
</script></body></html>'''
os.makedirs(H_ + "/out", exist_ok=True)
open(H_ + "/hf/index.html", "w").write(html)
say(f"v3 estimated timeline={STALE}  D={D}  js={len(J)} sfx={len(SFX)}")
say("lines: " + "  ".join(f"{n}:{s(n):.2f}-{e(n):.2f}" for n in range(1, NL + 1)))
say("sync: " + "  ".join(f"{k}={v['t']}({'w' if v['source'] == 'words' else 'EST'})" for k, v in json.load(open(H_ + '/cues102.json'))["sync"].items()))
for t, x in NEWS: say(f"  new {t:6.2f}  {x}")
say("FLAT stretches over 2.5 s with nothing new: " + (str(FLAT) if FLAT else "none"))
open(H_ + "/out/build-v3.log", "w").write("\n".join(LOG) + "\n")
