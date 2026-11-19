#!/usr/bin/env python3
"""Episode 106 (Replica skills: 'I built an app in half an hour'), Miki style + GSAP.
usage: python3 build106.py <tag> "<frame0 lines separated by |>" [accent_line_index]
reads  voice/cues-<tag>.json ({"lines":[{n,start,end,...}],"D":..}) and voice/words-<tag>.json (Whisper word times)
writes hf-<tag>/index.html (+ assets symlink), sfx-<tag>.json.   Line 1 = the hook (the only part that differs per version), lines 2-11 = shared body.
Safe area: key text x 108-972, y 269-1248; right edge <= 864 below y 1056.  No app screens, no app name, no code on screen, no star count.
"""
import json, os, re, sys
H_ = os.path.dirname(os.path.abspath(__file__))
TAG = sys.argv[1]; F0 = sys.argv[2].split("|"); ACC0 = int(sys.argv[3]) if len(sys.argv) > 3 else len(F0) - 1
OUT = f"{H_}/hf-{TAG}"; os.makedirs(OUT, exist_ok=True)
if not os.path.exists(OUT + "/assets"): os.symlink("../hf/assets", OUT + "/assets")
INK = "#0f0f0f"; ORG = "#D97757"; GREY = "#8a8982"
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
CUES = json.load(open(f"{H_}/voice/cues-{TAG}.json"))
LN = {l["n"]: l for l in CUES["lines"]}; assert len(LN) == 11
s = lambda n: float(LN[n]["start"]); e = lambda n: float(LN[n]["end"])
D = float(CUES["D"]); tF = round(D - .22, 3)
WORDS = [[w["word"], w["start"], w["end"]] for w in json.load(open(f"{H_}/voice/words-{TAG}.json"))]
def W(n, toks, k=0, fallback=.5):
    toks = (toks,) if isinstance(toks, str) else toks; c = 0
    for w, a_, b_ in WORDS:
        if s(n) - .15 <= a_ <= e(n) + .15 and any(norm(w) == t or (len(t) > 3 and norm(w).startswith(t)) for t in toks):
            if c == k: return round(a_, 3)
            c += 1
    return round(s(n) + fallback * (e(n) - s(n)), 3)
CUR = 0
def line(cls, words, top, size, acc=(), ready=False, left=108, lh=1.12, extra="", fast=True):
    out = []
    for i_, (txt, t) in enumerate(words):
        if not ready and fast: t = min(t, CUR + .14 + .1 * i_)
        ac = norm(txt) in acc
        out.append(f'<span class="m"><span class="w{" acc" if ac else ""}{" rdy" if ready else ""}" data-t="{t:.3f}">{txt}</span></span>')
    return f'<div class="ln {cls}" style="left:{left}px;top:{top}px;font-size:{size}px;line-height:{round(size * lh)}px">{"".join(out)}{extra}</div>'
def seq(txt, times):
    ws = txt.split(); assert len(ws) == len(times), (txt, times); return list(zip(ws, times))
def rr(x, y, w, h, r):  # rounded rect as one path (DrawSVG friendly)
    return f"M{x+r} {y} H{x+w-r} Q{x+w} {y} {x+w} {y+r} V{y+h-r} Q{x+w} {y+h} {x+w-r} {y+h} H{x+r} Q{x} {y+h} {x} {y+h-r} V{y+r} Q{x} {y} {x+r} {y} Z"
def P(d, col=INK, sw=6, cls="dr"): return f'<path class="{cls}" d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>'
def svg(id_, left, top, w, h, inner, vb=None): return f'<svg class="sk" id="{id_}" viewBox="0 0 {vb or f"{w} {h}"}" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px" data-decor>{inner}</svg>'
ring = lambda id_, left, top, w, h: (f'<svg class="ring" id="{id_}" viewBox="0 0 400 160" preserveAspectRatio="none" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px" data-decor>'
    f'<path d="M14 84 C6 30 130 8 214 10 C318 12 394 40 388 84 C382 132 270 150 190 148 C96 146 20 132 14 84 Z" fill="none" stroke="{ORG}" stroke-width="5" vector-effect="non-scaling-stroke" stroke-linecap="round"/></svg>')
A = "assets/"; SC = {}; T = {}

# ---- S1 frame 0 (hook line): Claude + GitHub marks, <=3 big words lines, drawn phone + eleven dots; complete on frame 0
SZ = int(min(165, 850 / (max(len(x) for x in F0) * 0.6))); F0S = [SZ] * 3
f0 = "".join(f'<div class="ln hv{" a0" if i == ACC0 else ""}" id="s1t{i}" style="left:102px;top:{446 + i * round(SZ * 1.07)}px;font-size:{F0S[i]}px;line-height:{round(SZ * 1.04)}px">{t}</div>' for i, t in enumerate(F0))
ph1 = rr(4, 4, 172, 292, 26)
dots = "".join(f'<i class="dot" style="left:{332 + i * 48}px;top:1100px"></i>' for i in range(11))
SC["S1"] = (f'<div class="wm" id="wm"><img src="{A}claude-logo-wordmark.png"></div>'
            f'<img class="lg" id="gh" src="{A}github-mark.png" style="left:862px;top:294px;width:108px;height:108px">' + f0 +
            svg("ph1", 108, 972, 162, 270, P(ph1) + P("M40 60 H110", GREY, 5) + P(rr(34, 90, 112, 56, 12), GREY, 5) + P(rr(34, 160, 112, 56, 12), GREY, 5) + P("M60 260 H120", GREY, 5)) +
            f'<i class="scan" id="scan1"></i>' + dots)
T["S1"] = dict(t0=0, end=s(2))
# ---- S2 (line 2) "I tell Claude the app I want. That's it."
CUR = s(2)
SC["S2"] = (f'<img class="lg" id="s2m" src="{A}claude-sparkle-site.png" style="left:108px;top:300px;width:210px;height:210px">' +
            line("lead", seq("I tell Claude", [W(2, "i", 0, .02), W(2, "tell", 0, .1), W(2, "claude", 0, .2)]), 540, 84) +
            line("hv", seq("THE APP", [W(2, "the", 0, .3), W(2, "app", 0, .4)]), 664, 210, lh=1.0) +
            line("hv", seq("I WANT.", [W(2, "i", 1, .5), W(2, "want", 0, .6)]), 884, 210, lh=1.0, acc=("want",)) +
            line("lead", seq("That's it.", [W(2, "thats", 0, .8), W(2, "it", 0, .92)]), 1120, 84))
T["S2"] = dict(t0=s(2), end=s(3))
# ---- S3 (line 3) the real repo page panning + headline
CUR = s(3)
SC["S3"] = (line("lead", seq("Then eleven", [W(3, "then", 0, .02), W(3, "eleven", 0, .15)]), 286, 74) +
            line("hv", seq("FREE ADD-ONS", [W(3, "free", 0, .4), W(3, ("addons", "add"), 0, .5)]), 366, 112, lh=1.0, acc=("free",)) +
            f'<div class="shot" id="pg"><img id="pgi" src="{A}replica-repo-crop.png"></div>')
T["S3"] = dict(t0=s(3), end=s(4), run=W(3, ("run", "runs"), 0, .75))
# ---- S4 (line 4) weak spots: a sketch idea card, a magnifier scans, a warning marker pops
CUR = s(4)
bars = "".join(P(f"M60 {70 + i * 76} H{[560, 420, 600][i]}", GREY, 10) for i in range(3))
SC["S4"] = (line("lead", seq("One finds", [W(4, "one", 0, .02), W(4, "finds", 0, .1)]), 286, 80) +
            line("hv", seq("THE WEAK", [W(4, "the", 0, .3), W(4, "weak", 0, .4)]), 376, 164, lh=1.0) +
            line("hv", [("SPOTS", W(4, "spots", 0, .55))], 556, 164, lh=1.0, acc=("spots",)) +
            line("lead", seq("in my idea.", [W(4, "in", 0, .7), W(4, "my", 0, .8), W(4, "idea", 0, .9)]), 746, 80) +
            f'<div class="idea" id="idea"></div>' +
            svg("sk4", 140, 900, 800, 300, bars.replace('class="dr"', 'class="dr4"'), "800 300") +
            f'<i class="mag" id="mag"></i>' +
            f'<svg class="wn" id="wn" viewBox="0 0 100 100" style="left:690px;top:940px;width:130px;height:130px" data-decor><path d="M50 10 L92 86 H8 Z" fill="#fff" stroke="{ORG}" stroke-width="7" stroke-linejoin="round"/><path d="M50 38 V60" stroke="{ORG}" stroke-width="8" stroke-linecap="round"/><circle cx="50" cy="74" r="4.5" fill="{ORG}"/></svg>')
T["S4"] = dict(t0=s(4), end=s(5), spot=W(4, "spots", 0, .55))
# ---- S5 (line 5) how it should look, and why: phone wireframe drawn + note lines
CUR = s(5)
ph5 = (P(rr(4, 4, 312, 592, 44)) + P("M60 70 H180", GREY, 8) + P(rr(40, 120, 240, 130, 20), GREY, 7) + P(rr(40, 276, 112, 110, 18), GREY, 7) + P(rr(168, 276, 112, 110, 18), GREY, 7) +
       P(rr(40, 412, 240, 60, 30), ORG, 8) + P("M70 540 H110 M150 540 H190 M230 540 H270", GREY, 8))
notes = "".join(P(f"M0 {20 + i * 74} H{[330, 270, 310][i]}", GREY, 9, "dr5n") + f'<circle class="nd" cx="-30" cy="{20 + i * 74}" r="9" fill="{ORG}"/>' for i in range(3))
SC["S5"] = (line("lead", seq("One draws", [W(5, "one", 0, .02), W(5, "draws", 0, .1)]), 286, 72) +
            line("hv", seq("HOW IT SHOULD", [W(5, "how", 0, .25), W(5, "it", 0, .3), W(5, "should", 0, .38)]), 366, 108, lh=1.0) +
            line("hv", [("LOOK.", W(5, "look", 0, .5))], 480, 108, lh=1.0) +
            svg("ph5", 108, 640, 320, 600, ph5, "320 600") +
            line("hv", seq("AND WHY.", [W(5, "and", 0, .72), W(5, "why", 0, .85)]), 700, 96, lh=1.0, left=480, acc=("why",)) +
            svg("nt5", 510, 860, 354, 240, notes, "354 240"))
T["S5"] = dict(t0=s(5), end=s(6), why=W(5, "why", 0, .85))
# ---- S6 (line 6) "Then I say, build it." typed into an input card
CUR = s(6)
tb = W(6, "build", 0, .6)
typed = "".join(f'<span class="ty">{c}</span>' for c in "build it")
SC["S6"] = (line("lead", seq("Then I say,", [W(6, "then", 0, .02), W(6, "i", 0, .2), W(6, "say", 0, .35)]), 330, 88) +
            f'<div class="inp" id="inp"><img src="{A}claude-sparkle-site.png"><div class="typ" id="typ">{typed}<i class="caret"></i></div><div class="snd" id="snd"><svg viewBox="0 0 40 40"><path d="M20 30 V11 M11 19 L20 10 L29 19" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>' +
            line("hv", [("BUILD IT.", W(6, "it", 0, .85))], 790, 220, lh=1.0, acc=("it", "buildit")))
T["S6"] = dict(t0=s(6), end=s(7), build=tb, send=W(6, "it", 0, .85))
# ---- S7 (line 7) the screens and the logic: three generic phones fill in, then a flow of nodes
CUR = s(7)
def phs(i):
    x = 108 + i * 312; inner = P(rr(3, 3, 234, 414, 34)) + P("M40 56 H130", GREY, 7)
    inner += [P(rr(30, 96, 180, 110, 16), GREY, 6) + P(rr(30, 230, 180, 50, 25), ORG, 7) + P("M40 330 H200 M40 366 H160", GREY, 6),
              P(rr(30, 96, 84, 84, 14), GREY, 6) + P(rr(126, 96, 84, 84, 14), GREY, 6) + P(rr(30, 196, 180, 190, 16), GREY, 6),
              P("M30 110 H210 M30 170 H180 M30 230 H210 M30 290 H150", GREY, 7) + P(rr(30, 340, 180, 50, 25), ORG, 7)][i]
    return svg(f"ph7{i}", x, 480, 240, 420, inner, "240 420")
flow = P("M40 60 H190 M270 60 H420 M500 60 H650", GREY, 8, "dr7f") + "".join(f'<circle class="fn" cx="{c}" cy="60" r="30" fill="#fff" stroke="{INK}" stroke-width="6"/>' for c in (0 + 30, 230, 460, 690)[:0]) 
nodes = "".join(f'<circle class="fn" cx="{40 + i * 230}" cy="60" r="34" fill="#fff" stroke="{INK}" stroke-width="6"/>' for i in range(4))
SC["S7"] = (line("hv", seq("THE SCREENS", [W(7, "the", 0, .3), W(7, "screens", 0, .45)]), 286, 118, lh=1.0) +
            "".join(phs(i) for i in range(3)) +
            line("lead", seq("and the logic", [W(7, "and", 0, .62), W(7, "the", 1, .7), W(7, "logic", 0, .85)]), 944, 90, acc=("logic",)) +
            svg("fl7", 118, 1090, 720, 120, P("M74 60 H196 M304 60 H426 M534 60 H656", GREY, 8, "dr7f") + nodes.replace('cx="40"', 'cx="40"'), "720 120").replace("</svg>", "</svg>"))
T["S7"] = dict(t0=s(7), end=s(8), logic=W(7, "logic", 0, .85))
# ---- S8 (line 8) a clock face sweeps half an hour
CUR = s(8)
clock = (f'<circle cx="240" cy="240" r="228" fill="#fff" stroke="{INK}" stroke-width="7"/>' +
         '<path class="pie" d="M240 126 A114 114 0 0 1 240 354" fill="none" stroke="' + ORG + '" stroke-width="228" stroke-opacity=".28" vector-effect="non-scaling-stroke"/>' +
         "".join(f'<path d="M{240 + 196 * __import__("math").sin(a * 0.5236):.1f} {240 - 196 * __import__("math").cos(a * 0.5236):.1f} L{240 + 216 * __import__("math").sin(a * 0.5236):.1f} {240 - 216 * __import__("math").cos(a * 0.5236):.1f}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>' for a in range(12)) +
         f'<g id="hand"><path d="M240 240 V70" stroke="{INK}" stroke-width="12" stroke-linecap="round"/></g><circle cx="240" cy="240" r="16" fill="{INK}"/>')
SC["S8"] = (line("lead", seq("I did all of it in", [W(8, "i", 0, .02), W(8, "did", 0, .08), W(8, "all", 0, .15), W(8, "of", 0, .22), W(8, "it", 0, .28), W(8, "in", 0, .34)]), 290, 66) +
            svg("clk", 300, 400, 480, 480, clock, "480 480") +
            line("lead", [("my run", .3)], 900, 48, left=108) +
            line("hv", seq("HALF AN HOUR", [W(8, "half", 0, .7), W(8, "an", 0, .8), W(8, "hour", 0, .88)]), 985, 104, lh=1.0, acc=("half",)))
T["S8"] = dict(t0=s(8), end=s(9), half=W(8, "half", 0, .7))
# ---- S9 (line 9, first part) the fine print as a card; S10 the saveable card
CUR = s(9)
tAnd = W(9, "and", 0, .8)
def rowhtml(i, mark, txt, bad): return f'<div class="fp" id="fp{i}"><b class="{"no" if bad else "ok"}">{mark}</b><span>{txt}</span></div>'
SC["S9"] = (line("lead", seq("It's not", [W(9, "its", 0, .02), W(9, "not", 0, .1)]), 286, 80) +
            line("hv", [("MAGIC.", W(9, "magic", 0, .2))], 376, 200, lh=1.0, acc=("magic",)) +
            '<div class="fpc" id="fpc">' + rowhtml(0, "✓", "Rebuilds how it works", 0) + rowhtml(1, "✕", "Never its logo", 1) + rowhtml(2, "✕", "Never its code", 1) + '</div>')
T["S9"] = dict(t0=s(9), end=tAnd, rows=[W(9, "rebuilds", 0, .3), W(9, "logo", 0, .6), W(9, "code", 0, .72)])
CUR = tAnd
names = ["recon", "architect", "design", "build", "backend", "test", "diff", "entrepreneur", "brand", "launch", "deploy"]
li = "".join(f'<div class="cr" id="cr{i}" style="left:{44 + (i // 6) * 400}px;top:{104 + (i % 6) * 84}px"><b>{i + 1}</b><span>{n}</span></div>' for i, n in enumerate(names))
SC["S10"] = (f'<div class="sv" id="sv"><div class="sh" id="sh">THE ELEVEN, IN ORDER</div>{li}'
             '<div class="inst" id="inst">Paste the repo link into Claude,<br>then say: install skill.<br><em>Rename it before launch.</em></div></div>')
T["S10"] = dict(t0=tAnd, end=s(11))
# ---- S11 (line 11) follow; frame 0 returns after
CUR = s(11)
SC["S11"] = (line("lead", seq("Want the next one?", [W(11, "want", 0, .02), W(11, "the", 0, .2), W(11, "next", 0, .4), W(11, "one", 0, .6)]), 420, 90) +
             line("hv", [("FOLLOW.", W(11, "follow", 0, .8))], 540, 200, acc=("follow",), fast=False) + ring("rgF", 78, 524, 900, 250) +
             f'<img class="lg" id="m11a" src="{A}claude-sparkle-site.png" style="left:108px;top:870px;width:230px;height:230px">'
             f'<img class="lg" id="m11b" src="{A}github-mark.png" style="left:400px;top:890px;width:190px;height:190px">')
T["S11"] = dict(t0=s(11), acc=W(11, "follow", 0, .8), end=tF)
for k in T:
    for kk, v in list(T[k].items()):
        if isinstance(v, float): T[k][kk] = round(v, 3)
T["tF"] = tF; T["D"] = D
# ---- sfx
SFX = []
def sfx(f, t, g=-13): SFX.append(dict(f=f, t=round(max(0, t), 3), g=g))
sfx("whoosh_b.ogg", .08, -15); sfx("click_a.ogg", s(2) + .25, -16); sfx("click_a.ogg", s(3) + .3, -16); sfx("select.ogg", T["S4"]["spot"], -14)
sfx("click_a.ogg", s(5) + .3, -16); sfx("select.ogg", T["S5"]["why"], -15); sfx("click_a.ogg", T["S6"]["build"], -15); sfx("select.ogg", T["S6"]["send"], -13)
sfx("click_a.ogg", s(7) + .3, -16); sfx("click_a.ogg", s(7) + 1.0, -16); sfx("select.ogg", T["S8"]["half"], -14); sfx("click_a.ogg", s(9) + .5, -16)
sfx("whoosh_b.ogg", tAnd - .05, -17); sfx("select.ogg", T["S11"]["acc"], -14)
SFX.sort(key=lambda x: x["t"]); json.dump(SFX, open(f"{H_}/sfx-{TAG}.json", "w"), indent=1)
scenes = "".join(f'<div class="sc" id="sc{n[1:]}">{SC[n]}</div>' for n in SC)
CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;font-weight:500;color:{INK};font-kerning:none}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}}
.bgw{{position:absolute;left:-20px;top:-20px;width:1120px;height:1960px;background:#ecebe5 url(assets/bg.jpg);background-size:1120px 1960px;will-change:transform}}
#cam{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}}
.sc{{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0;visibility:hidden;will-change:transform,opacity}} #sc1{{opacity:1;visibility:visible}}
.sc>*{{position:absolute}}
.lg{{display:block;flex:none;object-fit:contain}} .ln{{white-space:nowrap}}
.m{{display:inline-block;overflow:hidden;vertical-align:top;padding:0 .05em .08em 0;margin-right:.2em}} .lead .m{{margin-right:.24em}}
.w{{display:inline-block;transform:translateY(112%);will-change:transform}} .w.rdy{{transform:none}}
.lead .w{{font-weight:500;letter-spacing:-.02em;color:#33322f}} .hv .w{{font-weight:900;letter-spacing:-.045em}} .w.acc{{color:{INK}}}
.ring{{overflow:visible}} .hv{{font-weight:900;letter-spacing:-.045em}} .sk{{overflow:visible}}
.wm{{position:absolute;left:104px;top:292px;width:600px;height:131px;overflow:hidden}} .wm img{{position:absolute;left:0;top:-234.4px;width:600px;height:600px;max-width:none}}
.a0{{color:{ORG}}}
.dot{{position:absolute;width:36px;height:36px;border-radius:18px;background:#d3d1c7}}
.scan{{position:absolute;left:122px;top:1014px;width:152px;height:6px;border-radius:3px;background:{ORG};opacity:.9}}
.shot{{left:108px;top:500px;width:864px;height:748px;overflow:hidden;background:#fbfaf7;border-radius:40px;box-shadow:0 30px 60px rgba(20,20,20,.18);opacity:0;visibility:hidden}} .shot img{{position:absolute;left:0;top:0;width:864px;height:1062px;max-width:none}}
.idea{{left:108px;top:880px;width:864px;height:340px;border-radius:40px;background:#fff;box-shadow:0 30px 60px rgba(20,20,20,.16);opacity:0;visibility:hidden}}
.mag{{left:140px;top:930px;width:110px;height:110px;border-radius:55px;border:8px solid {ORG};background:rgba(217,119,87,.10);opacity:0;visibility:hidden}}
.wn{{opacity:0;visibility:hidden}}
.inp{{left:108px;top:470px;width:864px;height:220px;border-radius:48px;background:#fff;box-shadow:0 30px 60px rgba(20,20,20,.16);opacity:0;visibility:hidden}}
.inp img{{position:absolute;left:40px;top:62px;width:96px;height:96px}} .typ{{position:absolute;left:168px;top:0;height:220px;line-height:220px;font-weight:800;font-size:84px;letter-spacing:-.02em;white-space:nowrap}}
.ty{{display:inline-block;opacity:0;white-space:pre}} .caret{{display:inline-block;width:6px;height:88px;background:{ORG};margin-left:8px;vertical-align:middle;animation:bl 1s steps(1) infinite}} @keyframes bl{{50%{{opacity:0}}}}
.snd{{position:absolute;right:36px;top:50px;width:120px;height:120px;border-radius:60px;background:{ORG}}} .snd svg{{position:absolute;left:30px;top:30px;width:60px;height:60px}}
.fpc{{left:108px;top:640px;width:864px;height:560px;border-radius:44px;background:#fff;box-shadow:0 30px 60px rgba(20,20,20,.16);opacity:0;visibility:hidden;padding:30px 0 0 44px}}
.fp{{display:flex;align-items:center;gap:30px;height:170px;opacity:0;border-bottom:2px solid #eeede7;width:776px}} .fp:last-child{{border-bottom:0}}
.fp b{{flex:none;width:84px;height:84px;border-radius:42px;text-align:center;line-height:84px;font-weight:900;font-size:48px;color:#fff}} .fp b.ok{{background:{INK}}} .fp b.no{{background:{ORG}}}
.fp span{{font-weight:900;font-size:52px;letter-spacing:-.02em;white-space:nowrap}}
.sv{{left:108px;top:272px;width:864px;height:976px;border-radius:44px;background:#fff;box-shadow:0 30px 60px rgba(20,20,20,.16);opacity:0;visibility:hidden;overflow:hidden}}
.sh{{position:absolute;left:44px;top:34px;font-weight:900;font-size:32px;letter-spacing:.06em;color:{GREY};opacity:0}}
.cr{{position:absolute;display:flex;align-items:center;gap:20px;height:70px;opacity:0}} .cr b{{flex:none;width:54px;height:54px;border-radius:27px;background:{ORG};color:#fff;text-align:center;line-height:54px;font-weight:900;font-size:30px}} .cr span{{font-weight:900;font-size:40px;letter-spacing:-.02em;white-space:nowrap}}
.inst{{position:absolute;left:44px;top:640px;font-weight:800;font-size:46px;line-height:68px;letter-spacing:-.015em;white-space:nowrap;opacity:0}} .inst em{{font-style:normal;font-weight:500;color:{GREY};font-size:40px}}
'''
JS = r'''
gsap.registerPlugin(SplitText, DrawSVGPlugin, CustomEase);
const T=__T__, ORG='__ORG__', INK='__INK__';
const expoOut=CustomEase.create("expoOut","0.16,1,0.3,1"), expoIn=CustomEase.create("expoIn","0.7,0,0.84,0"), inOut=CustomEase.create("mvInOut","0.65,0,0.35,1");
const spring=(w=>{const f=t=>1-(1+w*t)*Math.exp(-w*t), n=f(1); return t=>f(t)/n})(9);
const show=id=>gsap.fromTo(id,{autoAlpha:0,y:10,filter:'blur(6px)'},{autoAlpha:1,y:0,filter:'blur(0px)',duration:.3,ease:'power2.out',immediateRender:false});
const hide=id=>gsap.to(id,{autoAlpha:0,y:-12,filter:'blur(8px)',duration:.22,ease:expoIn});
function type(t,id,S){
  gsap.utils.toArray(id+' .w:not(.rdy)').forEach(w=>{
    const at=Math.max(0,+w.dataset.t-S-.07);
    if(w.classList.contains('acc')){ gsap.set(w,{y:0,yPercent:0}); const sp=SplitText.create(w,{type:'chars',mask:'chars',aria:'none'});
      t.fromTo(sp.chars,{yPercent:112},{yPercent:0,duration:.5,ease:expoOut,stagger:.03},at).to(sp.chars,{color:ORG,duration:.3,ease:'power1.out',stagger:.03},at+.12); }
    else t.fromTo(w,{yPercent:112,y:0},{yPercent:0,y:0,duration:.46,ease:expoOut,immediateRender:false},at); });
}
function ringDraw(t,id,at){ t.fromTo(id+' path',{drawSVG:'0%'},{drawSVG:'100%',duration:.8,ease:'power2.inOut',immediateRender:false},at) }
gsap.set('.ring path, .dr, .dr4, .dr5n, .dr7f, .pie',{drawSVG:'0%'}); gsap.set('#ph1 .dr',{drawSVG:'100%'});
const card=(t,sel,at,y)=>t.fromTo(sel,{autoAlpha:0,y:y||40},{autoAlpha:1,y:0,duration:.55,ease:spring,immediateRender:false},at);
function scr(id,o,fn,opt){ opt=opt||{}; const S=o.t0-.04, t=gsap.timeline(); t.add(show(id),0); type(t,id,S);
  t.to(id+' .ln',{x:8,duration:Math.max(.6,o.end-o.t0-.5),ease:'sine.inOut',stagger:.05},.4);
  if(fn) fn(t,a=>a-S,S); if(!opt.keep) t.add(hide(id),Math.max(.3,o.end-S-.22)); return t; }
const draw=(t,sel,at,d,each)=>t.fromTo(sel,{drawSVG:'0%'},{drawSVG:'100%',duration:d||.7,ease:'power2.inOut',stagger:each||0,immediateRender:false},at);
const pops=(t,sel,at,each)=>t.fromTo(sel,{autoAlpha:0,y:36,scale:.9},{autoAlpha:1,y:0,scale:1,duration:.55,ease:spring,stagger:each,immediateRender:false},at);
const tl=gsap.timeline({paused:true});
tl.fromTo('#cam',{scale:1},{scale:1.014,duration:T.D/4,ease:'sine.inOut',yoyo:true,repeat:3},0)
  .fromTo('.bgw',{x:0,y:0},{x:-14,y:-12,duration:T.D/2,ease:'sine.inOut',yoyo:true,repeat:1},0);
/* S1 frame 0: complete on the first frame; dots light up, a scan line runs down the phone, marks breathe */
tl.add((()=>{ const o=T.S1,t=gsap.timeline();
  t.fromTo('#gh',{y:0},{y:-8,duration:1.0,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false},0)
   .fromTo('#sc1 .dot',{backgroundColor:'#d3d1c7'},{backgroundColor:ORG,duration:.3,ease:'power1.out',stagger:.16,immediateRender:false},.2)
   .fromTo('#scan1',{y:0},{y:170,duration:Math.max(1.2,o.end-.5),ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false},0)
   .fromTo('#s1t0,#s1t1,#s1t2,#wm',{x:0},{x:8,duration:1.9,ease:'sine.inOut',stagger:.05},.1)
   .fromTo('#s1t2',{scale:1.05,transformOrigin:'0% 50%'},{scale:1,duration:.9,ease:spring,immediateRender:false},.1);
  t.add(hide('#sc1'),o.end-.24); return t; })(),0);
tl.add(scr('#sc2',T.S2,(t,r)=>{ pops(t,'#s2m',.05,0); t.fromTo('#s2m',{rotation:0},{rotation:8,duration:1.4,ease:'sine.inOut',yoyo:true,repeat:1,immediateRender:false},.7); }),T.S2.t0-.04);
tl.add(scr('#sc3',T.S3,(t,r)=>{ card(t,'#pg',.3); t.fromTo('#pgi',{y:0},{y:-314,duration:Math.max(1.8,T.S3.end-T.S3.t0-.9),ease:'sine.inOut',immediateRender:false},.7); }),T.S3.t0-.04);
tl.add(scr('#sc4',T.S4,(t,r)=>{ card(t,'#idea',.3,30); draw(t,'#sc4 .dr4',.6,.6,.25);
  t.fromTo('#mag',{autoAlpha:0,x:0,y:0},{autoAlpha:1,x:520,y:40,duration:Math.max(1.4,r(T.S4.spot)-.2),ease:'sine.inOut',immediateRender:false},.7);
  t.fromTo('#wn',{autoAlpha:0,scale:.4,transformOrigin:'50% 70%'},{autoAlpha:1,scale:1,duration:.6,ease:spring,immediateRender:false},Math.max(1.2,r(T.S4.spot)+.1));
  t.fromTo('#wn',{rotation:-6},{rotation:6,duration:.5,yoyo:true,repeat:3,ease:'sine.inOut',immediateRender:false},Math.max(1.8,r(T.S4.spot)+.7)); }),T.S4.t0-.04);
tl.add(scr('#sc5',T.S5,(t,r)=>{ draw(t,'#ph5 .dr',.2,.55,.3); draw(t,'#nt5 .dr5n',Math.max(.9,r(T.S5.why)),.5,.22);
  t.fromTo('#nt5 .nd',{attr:{cx:-30}},{attr:{cx:-20},duration:.01},0).fromTo('#nt5 .nd',{autoAlpha:0},{autoAlpha:1,duration:.3,stagger:.22,immediateRender:false},Math.max(.9,r(T.S5.why))); }),T.S5.t0-.04);
tl.add(scr('#sc6',T.S6,(t,r)=>{ card(t,'#inp',.25,30);
  t.fromTo('#typ .ty',{opacity:0},{opacity:1,duration:.05,stagger:.085,immediateRender:false},Math.max(.45,r(T.S6.build)-.05));
  t.fromTo('#snd',{scale:1,transformOrigin:'50% 50%'},{scale:1.14,duration:.35,yoyo:true,repeat:1,ease:'sine.inOut',immediateRender:false},Math.max(1.1,r(T.S6.send))); }),T.S6.t0-.04);
tl.add(scr('#sc7',T.S7,(t,r)=>{ [0,1,2].forEach(i=>{ const a=.25+i*.62; draw(t,'#ph7'+i+' .dr',a,.5,.12); });
  draw(t,'#fl7 .dr7f',Math.max(1.5,r(T.S7.logic)),.6,0); t.fromTo('#fl7 .fn',{autoAlpha:0,scale:.5,transformOrigin:'50% 50%'},{autoAlpha:1,scale:1,duration:.5,ease:spring,stagger:.2,immediateRender:false},Math.max(1.5,r(T.S7.logic))-.1);
  t.fromTo('#sc7 .sk',{y:0},{y:-10,duration:1.2,ease:'sine.inOut',yoyo:true,repeat:1,stagger:.1,immediateRender:false},1.2); }),T.S7.t0-.04);
tl.add(scr('#sc8',T.S8,(t,r)=>{ t.fromTo('#clk',{autoAlpha:0,scale:.9,transformOrigin:'50% 50%'},{autoAlpha:1,scale:1,duration:.6,ease:spring,immediateRender:false},.15);
  const d=Math.max(1.6,T.S8.end-T.S8.t0-.7);
  t.fromTo('#hand',{rotation:0,svgOrigin:'240 240'},{rotation:180,duration:d,ease:'sine.inOut',immediateRender:false},.5);
  t.fromTo('#clk .pie',{drawSVG:'0%'},{drawSVG:'100%',duration:d,ease:'sine.inOut',immediateRender:false},.5); }),T.S8.t0-.04);
tl.add(scr('#sc9',T.S9,(t,r)=>{ card(t,'#fpc',.3,30);
  T.S9.rows.forEach((a,i)=>t.fromTo('#fp'+i,{autoAlpha:0,y:24},{autoAlpha:1,y:0,duration:.5,ease:expoOut,immediateRender:false},Math.max(.45+i*.3,r(a)-.25))); }),T.S9.t0-.04);
tl.add(scr('#sc10',T.S10,(t,r)=>{ card(t,'#sv',.02,30); t.fromTo('#sh',{opacity:0},{opacity:1,duration:.3,immediateRender:false},.15);
  t.fromTo('#sv .cr',{autoAlpha:0,x:-20},{autoAlpha:1,x:0,duration:.35,ease:expoOut,stagger:.07,immediateRender:false},.25);
  t.fromTo('#inst',{autoAlpha:0,y:20},{autoAlpha:1,y:0,duration:.5,ease:expoOut,immediateRender:false},1.0);
  t.fromTo('#sv',{scale:1,transformOrigin:'50% 40%'},{scale:1.03,duration:Math.max(1.5,T.S10.end-T.S10.t0),ease:'sine.inOut',immediateRender:false},.2); }),T.S10.t0-.04);
tl.add(scr('#sc11',T.S11,(t,r)=>{ ringDraw(t,'#rgF',r(T.S11.acc)+.1); pops(t,'#m11a',.3,0); pops(t,'#m11b',.45,0);
  t.fromTo('#m11a,#m11b',{rotation:0},{rotation:6,duration:.8,yoyo:true,repeat:1,ease:'sine.inOut',stagger:.15,immediateRender:false},.9); },{keep:true}),T.S11.t0-.04);
tl.to('#sc11',{autoAlpha:0,filter:'blur(6px)',duration:.12,ease:'power1.in'},T.tF-.12).set('#sc1',{autoAlpha:0},T.tF-.3).fromTo('#sc1',{autoAlpha:0,filter:'blur(6px)'},{autoAlpha:1,filter:'blur(0px)',duration:.2,ease:'power2.out',immediateRender:false},T.tF).to({},{duration:.001},T.D-.001);
window.__timelines=window.__timelines||{}; window.__timelines["main"]=tl; tl.seek(0);
window.__reel={duration:T.D,seek:t=>{tl.seek(t)}};
'''.replace("__T__", json.dumps(T, separators=(",", ":"))).replace("__ORG__", ORG).replace("__INK__", INK)
CDN = "https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/"
html = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="{CDN}gsap.min.js"></script><script src="{CDN}SplitText.min.js"></script><script src="{CDN}DrawSVGPlugin.min.js"></script><script src="{CDN}CustomEase.min.js"></script>
<style>
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Black.otf");font-weight:900}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-ExtraBold.otf");font-weight:800}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Medium.otf");font-weight:500}}
{CSS}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
<div class="bgw" data-decor></div><div id="cam">{scenes}</div>
</div>
<script>
{JS}
</script></body></html>'''
open(OUT + "/index.html", "w").write(html)
print(f"ep106 {TAG} D={D} sfx={len(SFX)}"); print("screens: " + "  ".join(f"{k}:{v['t0']:.2f}-{v['end']:.2f}" for k, v in T.items() if isinstance(v, dict) and 't0' in v))
