#!/usr/bin/env python3
"""ep88 integrator. lines.txt (8 lines) + VOICE/<n>.wav -> cues.json, out/narration.wav, hf/index.html [--render name].
Env: VOICE (dir with 1..8.wav, default voice/final), GAPS (7 gaps, default below), TAIL (seconds after line 8, default 1.1).
Word times: no whisper here, so words inside a line are placed by sentence: the k-1 longest silences in the line wav split it into its k
sentences, and words are spread over each sentence by letter count. Good to ~0.1-0.2 s; the value card rows use it."""
import json, os, re, sys, subprocess
import soundfile as sf, numpy as np
H = os.path.dirname(os.path.abspath(__file__))
VOICE = os.environ.get("VOICE", H + "/voice/final")
GAPS = [float(x) for x in os.environ.get("GAPS", "0.32,0.34,0.36,0.36,5.0").split(",")]
TAIL = float(os.environ.get("TAIL", "1.1"))
ALL = [l.rstrip("\n") for l in open(H + "/lines.txt") if l.strip()]
assert len(ALL) == 6 and len(GAPS) == 5
sr = 48000


def words_for(x, text, t0):
    """list of [start,end] absolute for each space-separated word."""
    toks = text.split()
    sents = [s for s in re.findall(r"[^.!?]+[.!?]*", text) if s.strip()]
    d = len(x) / sr
    # frame rms 10 ms
    f = int(sr * 0.01); n = len(x) // f
    r = np.sqrt(np.mean(x[:n * f].reshape(n, f) ** 2, axis=1) + 1e-12)
    thr = max(r.max() * 0.04, 1e-4)
    sil = r < thr
    # voiced span
    idx = np.where(~sil)[0]
    a, b = (idx[0], idx[-1] + 1) if len(idx) else (0, n)
    runs = []; i = a
    while i < b:
        if sil[i]:
            j = i
            while j < b and sil[j]: j += 1
            if j - i >= 6: runs.append((j - i, i, j))
            i = j
        else: i += 1
    k = len(sents)
    cuts = sorted(sorted(runs, reverse=True)[:k - 1], key=lambda z: z[1])
    bounds = [a * f / sr]
    segs = []
    for ln, i0, j0 in cuts:
        segs.append((bounds[-1], i0 * f / sr)); bounds.append(j0 * f / sr)
    segs.append((bounds[-1], b * f / sr))
    out = []; wi = 0
    for (s0, s1), s in zip(segs, sents):
        ws = s.split()
        wts = np.array([len(w.strip(".,!?'")) + 2 for w in ws], float); wts /= wts.sum()
        c = s0
        for w, p in zip(ws, wts):
            out.append([round(t0 + c, 3), round(t0 + c + p * (s1 - s0), 3)]); c += p * (s1 - s0)
    assert len(out) == len(toks), (len(out), len(toks), text)
    return out


lines = []; t = 0.0; parts = []
for j in range(6):
    n = j + 1
    x, s = sf.read(f"{VOICE}/{n}.wav"); assert s == sr; x = x if x.ndim == 1 else x[:, 0]
    d = len(x) / sr
    ln = dict(n=n, text=ALL[j], start=round(t, 3), end=round(t + d, 3), words=words_for(x, ALL[j], t))
    lines.append(ln); parts.append((int(t * sr), x)); t += d + (GAPS[j] if j < 5 else 0)
D = round(lines[-1]["end"] + TAIL, 2)
nar = np.zeros(int((D + 0.3) * sr))
for i0, x in parts: nar[i0:i0 + len(x)] += x
os.makedirs(H + "/out", exist_ok=True)
sf.write(H + "/out/narration.wav", nar[:int(D * sr)], sr, subtype="PCM_16")
json.dump(dict(lines=lines, D=D), open(H + "/cues.json", "w"), indent=1)

# ------------------------------------------------------------------ page (round 3: everything enlarged to fill the safe box)
PAL = [("#9ED8FF", "#E8F6FF", "#FFD84D", "#6CC070"), ("#FFB07A", "#FF7E7E", "#FFF1B0", "#5A4A6A"),
       ("#F6D8A8", "#F2B880", "#FFFFFF", "#C9783A"), ("#B8F0D0", "#7FD1AE", "#FFFFFF", "#2F8F6A"),
       ("#D9C8FF", "#A99BFF", "#FFE9A8", "#6A5BC8"), ("#F3E3C3", "#E3C48F", "#FFD0D0", "#B07A45")]


def motif(i):
    """small drawn 'photo' subjects so the gallery does not look like six copies of one picture"""
    c = PAL[i % 6]
    m = i % 6
    if m == 0:   # beach / hill with sun
        return f'<i class="sun" style="background:{c[2]}"></i><i class="hill" style="background:{c[3]}"></i>'
    if m == 1:   # cat
        return (f'<i class="ab" style="left:30%;top:34%;width:40%;padding-top:40%;border-radius:50%;background:{c[3]}"></i>'
                f'<i class="ab" style="left:31%;top:26%;width:11%;padding-top:11%;background:{c[3]};transform:rotate(45deg)"></i>'
                f'<i class="ab" style="left:58%;top:26%;width:11%;padding-top:11%;background:{c[3]};transform:rotate(45deg)"></i>'
                f'<i class="ab" style="left:39%;top:48%;width:6%;padding-top:6%;border-radius:50%;background:{c[2]}"></i>'
                f'<i class="ab" style="left:55%;top:48%;width:6%;padding-top:6%;border-radius:50%;background:{c[2]}"></i>')
    if m == 2:   # plate of food
        return (f'<i class="ab" style="left:24%;top:14%;width:52%;padding-top:52%;border-radius:50%;background:{c[2]};border:3px solid {c[3]}"></i>'
                f'<i class="ab" style="left:36%;top:30%;width:14%;padding-top:14%;border-radius:50%;background:{c[3]}"></i>'
                f'<i class="ab" style="left:52%;top:42%;width:12%;padding-top:12%;border-radius:50%;background:#E5484D"></i>')
    if m == 3:   # building
        w = "".join(f'<i class="ab" style="left:{x}%;top:{y}%;width:9%;padding-top:9%;background:#fff"></i>' for x in (36, 56) for y in (30, 50, 70))
        return f'<i class="ab" style="left:28%;top:18%;width:44%;height:90%;background:{c[3]}"></i>' + w
    if m == 4:   # flower
        p = "".join(f'<i class="ab" style="left:{x}%;top:{y}%;width:17%;padding-top:17%;border-radius:50%;background:{c[2]}"></i>' for x, y in ((41.5, 20), (41.5, 56), (24, 38), (59, 38)))
        return p + f'<i class="ab" style="left:41.5%;top:38%;width:17%;padding-top:17%;border-radius:50%;background:#E5484D"></i>'
    # boat
    return (f'<i class="ab" style="left:20%;top:62%;width:60%;padding-top:30%;border-radius:0 0 100px 100px;background:{c[3]}"></i>'
            f'<i class="ab" style="left:46%;top:18%;width:4%;height:46%;background:#fff"></i>'
            f'<i class="ab" style="left:50%;top:20%;width:0;height:0;border-left:44px solid {c[2]};border-top:30px solid transparent;border-bottom:50px solid transparent"></i>')


def tile(i, x, y, w, h, cls="", extra=""):
    c = PAL[i % 6]
    return (f'<div class="tile {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:linear-gradient(160deg,{c[0]},{c[1]})">'
            f'{motif(i)}{extra}</div>')


def phone(sfx):
    tiles = ""
    for i in range(6):
        r, c = divmod(i, 3)
        tag = '<b class="tg tgA">NEVER POSTED</b>' if i in (0, 2, 4) else ""
        tiles += tile(i, 18 + c * 304, 52 + r * 162, 290, 152, "pt", tag)
    return f'''<div class="phone" id="phone{sfx}"><div class="pbar"><span>YOUR CAMERA ROLL</span><i class="bdot"></i></div>
{tiles}<div class="shim"></div>
<div class="prompt"><div class="plabel">Camera roll sharing suggestions</div><div class="tgl q" id="tq{sfx}"><b>?</b></div></div></div>
<div class="hunt" id="hunt{sfx}"></div>'''


def cd(sfx):
    nums = "".join(f'<span class="cdn" id="cn{k}{sfx}">0:0{k}</span>' for k in range(5, -1, -1))
    return f'''<div class="cd" id="cd{sfx}">{nums}<div class="cdbar"><div class="cdfill" id="cdr{sfx}"></div></div></div>'''



def scene(k):
    """drawn everyday scenes for the collage tiles (all illustrations)"""
    A = lambda st, inner="": f'<i class="ab" style="{st}">{inner}</i>'
    if k == 0:   # kids at the beach
        return (A("left:0;top:0;width:100%;height:58%;background:linear-gradient(#8FD3FF,#D8F1FF)") + A("left:70%;top:8%;width:15%;padding-top:15%;border-radius:50%;background:#FFD84D")
                + A("left:0;top:44%;width:100%;height:20%;background:#3FA7E0") + A("left:0;top:60%;width:100%;height:40%;background:#F1D9A0")
                + A("left:22%;top:50%;width:11%;padding-top:11%;border-radius:50%;background:#7A4B2A") + A("left:20%;top:63%;width:15%;height:26%;background:#E5484D;border-radius:12px 12px 4px 4px")
                + A("left:48%;top:56%;width:10%;padding-top:10%;border-radius:50%;background:#C98A5A") + A("left:46%;top:67%;width:14%;height:24%;background:#2D7BE0;border-radius:12px 12px 4px 4px")
                + A("left:72%;top:74%;width:14%;height:15%;background:#FF9F1C;border-radius:4px 4px 16px 16px"))
    if k == 1:   # birthday table
        b = "".join(A(f"left:{x}%;top:{y}%;width:12%;padding-top:15%;border-radius:50%;background:{c}") + A(f"left:{x+5.5}%;top:{y+15}%;width:1.2%;height:22%;background:#6b6b6b") for x, y, c in ((8, 8, "#E5484D"), (24, 3, "#FFD84D"), (78, 6, "#86D93F"), (62, 11, "#2D7BE0")))
        return (A("left:0;top:0;width:100%;height:100%;background:#FFE6C9") + b + A("left:0;top:70%;width:100%;height:30%;background:#B8763D")
                + A("left:28%;top:50%;width:44%;height:26%;background:#fff;border-radius:10px;border:4px solid #E5484D") + A("left:28%;top:50%;width:44%;height:9%;background:#FF8FB1;border-radius:10px 10px 0 0")
                + "".join(A(f"left:{x}%;top:38%;width:2.4%;height:13%;background:#2D7BE0") + A(f"left:{x-.6}%;top:32%;width:3.6%;padding-top:5%;border-radius:50%;background:#FFB000") for x in (38, 48, 58)))
    if k == 2:   # messy desk
        return (A("left:0;top:0;width:100%;height:100%;background:#E9EEF3") + A("left:0;top:62%;width:100%;height:38%;background:#A8764A")
                + A("left:14%;top:20%;width:46%;height:34%;background:#2B2F36;border-radius:10px") + A("left:17%;top:23%;width:40%;height:28%;background:#8FD3FF;border-radius:6px") + A("left:8%;top:54%;width:58%;height:7%;background:#555C66;border-radius:6px")
                + A("left:70%;top:50%;width:13%;height:20%;background:#fff;border-radius:6px 6px 14px 14px;border:4px solid #E5484D") + A("left:76%;top:56%;width:8%;height:8%;border:4px solid #E5484D;border-radius:50%")
                + A("left:66%;top:70%;width:20%;height:13%;background:#fff;transform:rotate(14deg);border:2px solid #bbb") + A("left:22%;top:72%;width:22%;height:14%;background:#FFF3A8;transform:rotate(-9deg)") + A("left:50%;top:76%;width:18%;height:12%;background:#fff;transform:rotate(6deg);border:2px solid #bbb")
                + A("left:74%;top:14%;width:14%;height:15%;background:#FFD84D;transform:rotate(7deg)") + A("left:86%;top:30%;width:10%;height:11%;background:#FF8FB1;transform:rotate(-8deg)"))
    # fridge note
    return (A("left:0;top:0;width:100%;height:100%;background:#F3EBDD") + A("left:22%;top:0;width:56%;height:100%;background:#E8EEF2;border:4px solid #9AA6B2;border-radius:14px")
            + A("left:22%;top:38%;width:56%;height:3%;background:#9AA6B2") + A("left:70%;top:14%;width:3.5%;height:18%;background:#9AA6B2;border-radius:4px") + A("left:70%;top:50%;width:3.5%;height:18%;background:#9AA6B2;border-radius:4px")
            + A("left:30%;top:12%;width:28%;height:28%;background:#FFF3A8;transform:rotate(-5deg);box-shadow:0 3px 6px rgba(0,0,0,.25)")
            + "".join(A(f"left:{34}%;top:{y}%;width:{w}%;height:2.4%;background:#555;transform:rotate(-5deg)") for y, w in ((18, 18), (25, 20), (32, 14)))
            + A("left:32%;top:7%;width:6%;padding-top:6%;border-radius:50%;background:#E5484D") + A("left:36%;top:56%;width:26%;height:24%;background:#fff;border:3px solid #bbb;transform:rotate(4deg)")
            + A("left:42%;top:60%;width:8%;padding-top:8%;border-radius:50%;background:#FF9F1C") + A("left:44%;top:70%;width:4%;height:8%;background:#2D7BE0"))


def feed(sfx):
    tiles = ""
    for k in range(4):
        r, c = divmod(k, 2)
        tiles += (f'<div class="ftile" id="ft{k}{sfx}" style="left:{c*446}px;top:{r*374}px">{scene(k)}'
                  f'<b class="tg tgA ftag">NEVER POSTED</b></div>')
    return f'''<div class="feedcard" id="feed{sfx}"><div class="fhead"><div class="flogo"><img src="assets/facebook.svg"></div>
<div class="ftitle"><div class="ft1">Collage made for you</div><div class="ft2">drawn example</div></div></div>
<div class="fgrid">{tiles}</div><div class="fshim" id="fshim{sfx}"></div></div>'''

def capblock(n, sfx, size, top):
    toks = ALL[n - 1].split()
    sp = ""
    for i, w in enumerate(toks):
        hl = " hl" if (n == 1 and i >= 9) else ""
        disp = "5" if (n == 1 and w == "five") else w
        sp += f'<span class="cw{hl}">{disp}</span> ' + ("<br>" if (n == 1 and i in (4, 8)) else "")
    return f'<div class="cap" id="cap{n}{sfx}" style="font-size:{size}px;line-height:{int(size*1.08)}px;top:{top}px">{sp}</div>'


def size_for(n):
    L = len(ALL[n - 1])
    return 104 if L <= 22 else (100 if L <= 46 else (88 if L <= 58 else 78))


markup = f'''
<div class="scn" id="sA" style="visibility:visible;opacity:1">
 {feed("")}
</div>
<div class="scn" id="sB">
 {capblock(3, "", size_for(3), 290)}
 <div class="setc" id="setc"><div class="r1"><div class="lg2"><img src="assets/facebook.svg"></div><div class="t1">Camera roll sharing suggestions</div></div>
  <div class="hr"></div><div class="r2"><div class="t2">Get camera roll suggestions when you're browsing Facebook</div><div class="tgl big" id="tglB"><b></b></div></div></div>
 <div class="note2" id="noteB">drawn example of the settings row</div>
</div>
<div class="scn" id="sC">
 {capblock(2, "", size_for(2), 290)}
 <div class="bigallow" id="ba">Allow</div><div class="ripple" id="ripple"></div><div class="finger" id="finger"></div>
 <div class="strip" id="strip">{"".join(f'<div class="tile st" style="left:{i*322}px;top:0;width:300px;height:230px">{scene(i % 4)}</div>' for i in range(10))}</div>
 <div class="scan" id="scan"></div>
</div>
<div class="scn" id="sD">
 {capblock(4, "", size_for(4), 290)}
 <div class="meta" id="meta"><div class="mh">META SAYS</div>
  <div class="mq" id="mq1">&ldquo;You must opt in to use this feature&rdquo;</div>
  <div class="mq" id="mq2">&ldquo;We don't use photos and videos from your camera roll for ads targeting.&rdquo;</div>
  <div class="mf" id="mf">Meta newsroom, April 2026 &middot; EU and UK</div></div>
</div>
<div class="scn" id="sF">
 <div class="val" id="val"><div class="vh"><span class="vchip">HERE'S THE SWITCH</span><div class="lg3"><img src="assets/facebook.svg"></div></div>
  <div class="vr" id="vr1"><i>1</i><p>Profile picture</p></div>
  <div class="vr" id="vr2"><i>2</i><p>Settings &amp; Privacy</p></div>
  <div class="vr" id="vr3"><i>3</i><p>Settings</p></div>
  <div class="vr big" id="vr4"><i>4</i><p>Camera roll sharing suggestions</p></div>
  <div class="vr act" id="vr5"><p>Switch it off</p><span class="offt" id="offt">OFF</span><div class="tgl on big" id="tglF"><b></b></div></div>
  <div class="vshim" id="vshim"></div><div class="vn" id="vn">menu names can differ by app version</div></div>
</div>
<div class="scn" id="sG">
 {capblock(6, "", size_for(6), 290)}
 <div class="out" id="outb"><div class="mini"><div class="mt1">Camera roll sharing suggestions</div><div class="tgl big" id="tglG"><b></b></div></div></div>
 <div class="mum"><div class="av" id="mav">M</div></div>
 <div class="dots2" id="dots2"><b></b><b></b><b></b></div>
 <div class="al" id="al1">Allow</div><div class="al" id="al2">Allow</div><div class="al" id="al3">Allow</div>
</div>
<div class="scn" id="sH">
 {feed("H")}
</div>
'''

styles = '''
:root{--acc:#86D93F}
.scn .cap,.scn .lgo,.phone,.setc,.strip,.scan,.collage,.meta,.dlg,.val,.out,.note2,.hunt,.cd,.bigallow{position:absolute}
.cap{left:65px;width:950px;text-align:center;font-weight:900;letter-spacing:-.045em;opacity:0;visibility:hidden}
.cw{display:inline-block;color:#2A2A26;margin:0 8px;border-radius:14px}
.cw.hl{background:rgba(134,217,63,.6);padding:0 6px;font-size:70px;margin:0 3px;white-space:nowrap}
#cap1,#cap1H{opacity:1;visibility:visible;left:45px;width:990px}
.feedcard{position:absolute;left:65px;top:269px;width:950px;height:979px;background:#fff;border:8px solid var(--ink);border-radius:52px;box-shadow:12px 12px 0 var(--ink);overflow:hidden}
.fhead{position:absolute;left:34px;top:26px;width:880px;height:140px;display:flex;align-items:center;gap:28px}
.flogo{width:132px;height:132px;flex:none;border-radius:50%;border:7px solid var(--ink);overflow:hidden;background:#fff}.flogo img{width:112%;height:112%;margin:-6%}
.ft1{font-weight:900;font-size:76px;line-height:80px;letter-spacing:-.04em}
.ft2{font-weight:700;font-size:26px;letter-spacing:.05em;color:var(--ink2);margin-top:4px}
.fgrid{position:absolute;left:34px;top:186px;width:882px;height:750px}
.ftile{position:absolute;width:436px;height:362px;border-radius:26px;border:6px solid var(--ink);overflow:hidden;background:#fff}
.ftag{left:14px;bottom:14px;font-size:32px;line-height:36px;padding:5px 16px 8px}
.fshim{position:absolute;left:0;top:0;width:200px;height:100%;background:linear-gradient(100deg,rgba(255,255,255,0),rgba(255,255,255,.55),rgba(255,255,255,0));transform:translateX(-300px) skewX(-12deg);opacity:0;pointer-events:none}
.ab{position:absolute;display:block}
.lgo{left:65px;top:276px;width:180px;height:180px;border-radius:50%;background:#fff;border:8px solid var(--ink);box-shadow:9px 9px 0 var(--ink);display:flex;align-items:center;justify-content:center;overflow:hidden}
.lgo img{width:112%;height:112%;margin:-6%}
.cd{left:775px;top:292px;width:240px;height:150px;background:#fff;border:7px solid var(--ink);border-radius:40px;box-shadow:8px 8px 0 var(--ink);overflow:hidden}
.cdn{position:absolute;left:0;top:6px;width:226px;height:104px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:92px;letter-spacing:-.03em;opacity:0}
.cdbar{position:absolute;left:18px;right:18px;bottom:16px;height:18px;border-radius:9px;background:#E4E4DC;border:3px solid var(--ink);overflow:hidden}
.cdfill{width:100%;height:100%;background:var(--acc);transform-origin:0 50%}
.phone{left:65px;top:760px;width:950px;height:486px;background:#fff;border:7px solid var(--ink);border-radius:44px;box-shadow:10px 10px 0 var(--ink);overflow:hidden}
.pbar{position:absolute;left:0;top:0;width:100%;height:44px;background:#EFEFE8;border-bottom:4px solid var(--ink);display:flex;align-items:center;justify-content:space-between;padding:0 26px;font-weight:800;font-size:24px;letter-spacing:.08em;color:var(--ink2)}
.bdot{display:block;width:20px;height:20px;border-radius:50%;background:#1877F2}
.tile{position:absolute;overflow:hidden;border-radius:16px;border:4px solid var(--ink)}
.sun{position:absolute;right:16%;top:12%;width:22%;padding-top:22%;border-radius:50%}
.hill{position:absolute;left:-20%;bottom:-46%;width:140%;padding-top:70%;border-radius:50%}
.tg{position:absolute;left:10px;bottom:10px;font-weight:900;font-size:25px;letter-spacing:.03em;padding:4px 12px 6px;border:3px solid var(--ink);border-radius:11px;white-space:nowrap;line-height:28px}
.tgA{background:var(--acc);color:var(--ink)}
.shim{position:absolute;left:0;top:44px;width:140px;height:330px;background:linear-gradient(100deg,rgba(255,255,255,0),rgba(255,255,255,.65),rgba(255,255,255,0));transform:translateX(-200px) skewX(-12deg);opacity:0}
.prompt{position:absolute;left:0;top:372px;width:100%;height:100px;background:#F4F4EF;border-top:4px solid var(--ink);display:flex;align-items:center;justify-content:space-between;padding:0 34px}
.plabel{width:640px;font-weight:900;font-size:44px;line-height:48px;letter-spacing:-.03em}
.sk{width:520px}.sk u{display:block;height:22px;width:100%;border-radius:11px;background:#CFCFC5;margin:10px 0;text-decoration:none}
.tgl{position:relative;width:124px;height:70px;flex:none;border-radius:35px;background:#BCC0C4;box-shadow:inset 0 0 0 3px rgba(14,14,14,.18)}
.tgl b{position:absolute;left:5px;top:5px;width:60px;height:60px;border-radius:50%;background:#fff;box-shadow:0 3px 7px rgba(14,14,14,.4);font-style:normal;font-weight:900;font-size:40px;line-height:60px;text-align:center;color:var(--ink2)}
.tgl.on{background:var(--acc)}.tgl.on b{left:auto;right:5px}
.tgl.big{width:176px;height:96px;border-radius:48px}
.tgl.big b{width:84px;height:84px;top:6px;left:6px}
.tgl.big.on b{left:auto;right:6px}
.tgl.q{width:174px;height:78px;border-radius:39px}
.tgl.q b{width:66px;height:66px;top:6px;left:6px}
.hunt{left:0;top:0;width:150px;height:110px;border:8px solid var(--acc);border-radius:26px;box-shadow:0 0 0 5px rgba(14,14,14,.9);opacity:0;pointer-events:none}
.setc{left:65px;top:668px;width:950px;background:#fff;border:8px solid var(--ink);border-radius:48px;box-shadow:14px 14px 0 var(--ink);padding:40px 40px 40px}
.setc .r1{display:flex;align-items:center;gap:30px}
.lg2{width:140px;height:140px;flex:none;border-radius:50%;border:6px solid var(--ink);overflow:hidden;background:#fff}.lg2 img{width:112%;height:112%;margin:-6%}
.t1{font-weight:900;font-size:80px;line-height:84px;letter-spacing:-.04em}
.hr{height:6px;background:var(--ink);opacity:.15;margin:34px 0}
.r2{display:flex;align-items:center;justify-content:space-between;gap:24px}
.t2{font-weight:700;font-size:46px;line-height:54px;letter-spacing:-.02em;width:640px;color:var(--ink2)}
.note2{left:65px;width:950px;text-align:center;font-weight:700;font-size:28px;letter-spacing:.02em;color:var(--ink2)}
#noteB{top:1206px}
.bigallow{left:125px;top:700px;width:830px;text-align:center;font-weight:900;font-size:170px;line-height:200px;padding:10px 0 24px;border:10px solid var(--ink);border-radius:90px;background:var(--acc);box-shadow:14px 14px 0 var(--ink);opacity:0}
.ripple{position:absolute;left:770px;top:760px;width:120px;height:120px;border-radius:50%;border:10px solid var(--ink);opacity:0}
.finger{position:absolute;left:790px;top:880px;width:90px;height:90px;border-radius:50%;background:rgba(14,14,14,.82);opacity:0}
.strip{left:65px;top:700px;width:3300px;height:230px;opacity:0}
.strip .tile{border-radius:22px}
.scan{left:430px;top:680px;width:340px;height:270px;border:9px solid var(--ink);border-radius:32px;background:rgba(134,217,63,.28);box-shadow:0 0 0 8px rgba(134,217,63,.35);opacity:0}
.collage{left:65px;top:970px;width:950px;height:276px;background:#fff;border:8px solid var(--ink);border-radius:44px;box-shadow:10px 10px 0 var(--ink);opacity:0}
.mos{position:absolute;left:30px;top:6px;width:250px;height:250px}
.mt{border-radius:14px}
.chips{position:absolute;left:340px;top:30px;display:flex;flex-direction:column;gap:22px}
.chip2{background:var(--acc);border:6px solid var(--ink);border-radius:30px;box-shadow:6px 6px 0 var(--ink);font-weight:900;font-size:78px;line-height:84px;padding:0 44px 8px;width:fit-content}
.meta{left:65px;top:652px;width:950px;background:#fff;border:8px solid var(--ink);border-radius:48px;box-shadow:14px 14px 0 var(--ink);padding:34px 44px 34px;opacity:0}
.mh{display:inline-block;background:var(--ink);color:#fff;font-weight:900;font-size:44px;letter-spacing:.08em;padding:6px 26px 10px;border-radius:18px}
.mq{margin-top:30px;font-weight:800;font-size:64px;line-height:70px;letter-spacing:-.03em;opacity:0}
.mf{margin-top:24px;font-weight:700;font-size:34px;letter-spacing:.02em;color:var(--ink2);opacity:0}
.val{left:65px;top:286px;width:950px;background:#fff;border:8px solid var(--ink);border-radius:52px;box-shadow:14px 14px 0 var(--ink);padding:26px 36px 24px;opacity:0;overflow:hidden}
.vh{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.vchip{background:var(--acc);border:6px solid var(--ink);border-radius:24px;box-shadow:6px 6px 0 var(--ink);font-weight:900;font-size:54px;letter-spacing:.02em;padding:4px 28px 10px}
.lg3{width:110px;height:110px;border-radius:50%;border:6px solid var(--ink);overflow:hidden}.lg3 img{width:112%;height:112%;margin:-6%}
.vr{display:flex;align-items:center;gap:28px;height:130px;opacity:0;position:relative}
.vr.big{height:180px}
.vr i{flex:none;width:92px;height:92px;border:7px solid var(--ink);border-radius:28px;background:var(--acc);box-shadow:6px 6px 0 var(--ink);font-style:normal;font-weight:900;font-size:62px;line-height:76px;text-align:center}
.vr p{font-weight:900;font-size:78px;line-height:80px;letter-spacing:-.04em;flex:1}
.vr.big p{font-size:72px;line-height:76px}
.vr.act{margin-top:8px;height:136px;border:7px solid var(--ink);border-radius:34px;padding:0 28px;background:#F4F4EF}
.vr.act p{font-size:68px}
.offt{position:static;margin-right:12px;font-weight:900;font-size:36px;letter-spacing:.06em;background:var(--ink);color:#fff;padding:2px 16px 6px;border-radius:14px;opacity:0}
.vshim{position:absolute;left:0;top:0;width:150px;height:100%;background:linear-gradient(100deg,rgba(255,255,255,0),rgba(134,217,63,.28),rgba(255,255,255,0));transform:translateX(-200px) skewX(-12deg);opacity:0;pointer-events:none}
.vn{margin-top:18px;font-weight:700;font-size:34px;letter-spacing:.01em;color:var(--ink2);text-align:center;opacity:0}
.out{left:105px;top:652px;width:870px;background:var(--ink);border-radius:56px 56px 14px 56px;padding:28px;box-shadow:10px 10px 0 rgba(14,14,14,.25);opacity:0}
.mini{background:#fff;border-radius:38px;padding:34px 34px;display:flex;align-items:center;gap:20px;justify-content:space-between}
.mt1{font-weight:900;font-size:62px;line-height:68px;letter-spacing:-.04em}
.mum{position:absolute;left:65px;top:1086px}
.av{width:130px;height:130px;border-radius:50%;background:#FFD84D;border:7px solid var(--ink);box-shadow:7px 7px 0 var(--ink);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:74px;opacity:0}
.dots2{position:absolute;left:225px;top:1096px;width:230px;height:112px;background:#fff;border:7px solid var(--ink);border-radius:50px 50px 50px 12px;box-shadow:8px 8px 0 var(--ink);display:flex;align-items:center;justify-content:center;gap:18px;opacity:0}
.dots2 b{display:block;width:26px;height:26px;border-radius:50%;background:var(--ink)}
.al{position:absolute;top:1086px;background:var(--acc);border:7px solid var(--ink);border-radius:44px 44px 44px 12px;box-shadow:8px 8px 0 var(--ink);font-weight:900;font-size:68px;line-height:78px;padding:6px 26px 14px;opacity:0}
#al1{left:212px}#al2{left:478px}#al3{left:744px}
'''

js = r'''
const S=n=>L[n-1].start,E=n=>L[n-1].end,W=(n,i)=>L[n-1].words[i][0],WE=(n,i)=>L[n-1].words[i][1];
const EA="sine.inOut",EO="power2.out",EI="power2.inOut";
const show=(el,t,d)=>tl.to(el,{autoAlpha:1,duration:d||.3,ease:EA},t);
const hide=(el,t,d)=>tl.to(el,{autoAlpha:0,duration:d||.2,ease:EA},t);
const Q=s=>document.querySelector(s), QA=s=>[...document.querySelectorAll(s)];
function cap(id,n,tshow,thide){
  const els=QA('#'+id+' .cw');
  els.forEach((e,i)=>{ if(W(n,i)<=0.001){ tl.set(e,{color:"#0E0E0E"},0);} else tl.to(e,{color:"#0E0E0E",duration:.16,ease:EA},W(n,i)-0.02); });
  if(tshow>0) tl.fromTo('#'+id,{autoAlpha:0,y:10},{autoAlpha:1,y:0,duration:.3,ease:EO},tshow);
  if(thide) hide('#'+id,thide,.2);
}
function countdown(sfx,t0){   // 0:05 -> 0:00 over 5 s from t0, with a bar that empties
  tl.set('#cn5'+sfx,{opacity:1},t0);
  tl.fromTo('#cdr'+sfx,{scaleX:1},{scaleX:0,duration:5,ease:"none"},t0);
  for(let k=4;k>=0;k--){ const t=t0+(5-k);
    tl.to('#cn'+(k+1)+sfx,{opacity:0,y:-10,duration:.22,ease:EA},t-.02);
    tl.fromTo('#cn'+k+sfx,{opacity:0,y:12},{opacity:1,y:0,duration:.3,ease:EO},t+.02); }
  tl.to('#cd'+sfx,{scale:1.05,duration:.5,ease:EA,transformOrigin:"50% 50%",yoyo:true,repeat:9},t0);
}
function phoneAnim(sfx,t0,t1){
  tl.fromTo('#phone'+sfx,{y:0,scale:1},{y:-8,scale:1.015,duration:t1-t0,ease:EA},t0);
  for(let t=t0+.2;t<t1-.8;t+=1.6){ tl.fromTo('#phone'+sfx+' .shim',{x:-200,opacity:0},{x:1100,opacity:1,duration:1.5,ease:EA},t); tl.to('#phone'+sfx+' .shim',{opacity:0,duration:.3},t+1.3); }
  QA('#phone'+sfx+' .tgA').forEach((e,i)=>{ for(let t=t0+.3+i*.25;t<t1-.5;t+=1.4){ tl.to(e,{scale:1.07,duration:.7,ease:EA,transformOrigin:"0% 100%"},t); tl.to(e,{scale:1,duration:.7,ease:EA},t+.7);} });
}
// ---- scene A: frame 0 = ONE giant feed card "Collage made for you" (4 drawn everyday scenes, each NEVER POSTED)
const tA1=E(1);
function feedAnim(sfx,t0,t1){
  tl.fromTo('#feed'+sfx,{y:0,scale:1},{y:-8,scale:1.012,duration:t1-t0,ease:EA},t0);
  [0,1,2,3].forEach(k=>{ tl.fromTo('#ft'+k+sfx,{scale:1},{scale:1.025,duration:1.3,ease:EA,yoyo:true,repeat:Math.max(1,Math.floor((t1-t0)/1.3/2)),transformOrigin:"50% 50%"},t0+.3+k*.35); });
  for(let t=t0+.3;t<t1-.8;t+=1.7){ tl.fromTo('#fshim'+sfx,{x:-300,opacity:0},{x:1200,opacity:1,duration:1.6,ease:EA},t); tl.to('#fshim'+sfx,{opacity:0,duration:.3},t+1.35); }
  QA('#feed'+sfx+' .ftag').forEach((e,i)=>{ for(let t=t0+.4+i*.3;t<t1-.5;t+=1.5){ tl.to(e,{scale:1.06,duration:.75,ease:EA,transformOrigin:"0% 100%"},t); tl.to(e,{scale:1,duration:.75,ease:EA},t+.75);} });
}
feedAnim('',0,tA1);
hide('#sA',tA1+.0,.2);
// ---- scene B: line 3
show('#sB',S(3)-.08,.3);
tl.fromTo('#setc',{y:30,opacity:0},{y:0,opacity:1,duration:.55,ease:EO},S(3)-.05);
tl.fromTo('#noteB',{opacity:0},{opacity:1,duration:.4},S(3)+.4);
cap('cap3',3,S(3)-.05,0);
tl.fromTo('#setc',{scale:1},{scale:1.02,duration:E(3)-S(3)+.3,ease:EA},S(3));
for(let t=S(3)+.3;t<E(3)-.5;t+=1.2){ tl.to('#tglB',{boxShadow:"0 0 0 12px rgba(134,217,63,.7)",duration:.55,ease:EA},t); tl.to('#tglB',{boxShadow:"0 0 0 0px rgba(134,217,63,0)",duration:.55,ease:EA},t+.55); }
tl.to('#setc',{y:-8,duration:E(3)-S(3),ease:EA,immediateRender:false},S(3)+.6);
hide('#sB',E(3),.2);
show('#sC',S(2)-.08,.3);
cap('cap2',2,S(2)-.05,0);
const tp=W(2,3);
tl.fromTo('#ba',{y:30,opacity:0,scale:.94},{y:0,opacity:1,scale:1,duration:.5,ease:EO},S(2)+.1);
tl.fromTo('#finger',{opacity:0,y:50},{opacity:1,y:0,duration:.45,ease:EO},tp-.45);
tl.to('#ba',{scale:.95,duration:.2,ease:EA,transformOrigin:"50% 50%"},tp);
tl.fromTo('#ripple',{opacity:.9,scale:.5},{opacity:0,scale:2.6,duration:.9,ease:EO},tp+.05);
tl.to('#ba',{scale:1,duration:.35,ease:EA},tp+.2);
tl.to('#finger',{opacity:0,duration:.4,ease:EA},tp+.5);
tl.to('#ba',{opacity:0,y:-20,duration:.35,ease:EA},W(2,4)-.1);
tl.fromTo('#strip',{x:140,opacity:0},{x:0,opacity:1,duration:.5,ease:EO},W(2,4)-.05);
tl.fromTo('#strip',{x:0},{x:-1250,duration:E(2)-W(2,4)+.4,ease:EA},W(2,4)+.2);
tl.fromTo('#scan',{opacity:0,scale:.9},{opacity:1,scale:1,duration:.4,ease:EO},W(2,5));
tl.to('#scan',{scale:1.05,duration:.8,ease:EA,yoyo:true,repeat:2},W(2,5)+.4);
hide('#sC',E(2),.2);
// ---- scene D: line 5
show('#sD',S(4)-.08,.3);
cap('cap4',4,S(4)-.05,0);
tl.fromTo('#meta',{y:30,opacity:0},{y:0,opacity:1,duration:.55,ease:EO},S(4)-.05);
tl.to('#mq1',{opacity:1,duration:.5,ease:EA},W(4,2));
tl.to('#mq2',{opacity:1,duration:.5,ease:EA},W(4,5)-.1);
tl.to('#mf',{opacity:1,duration:.5,ease:EA},W(4,8));
tl.fromTo('#meta',{scale:1},{scale:1.015,duration:E(4)-S(4)+.3,ease:EA},S(4));
hide('#sD',E(4),.2);
// ---- scene F: line 6 value card (held after speech)
show('#sF',S(5)-.08,.3);
tl.fromTo('#val',{y:30,opacity:0},{y:0,opacity:1,duration:.55,ease:EO},S(5)-.05);
[[1,3],[2,5],[3,8],[4,9],[5,13]].forEach(([r,wi])=>{ tl.fromTo('#vr'+r,{opacity:0,x:-30},{opacity:1,x:0,duration:.5,ease:EO},W(5,wi)-.12); });
tl.to('#vn',{opacity:1,duration:.5,ease:EA},W(5,13)+.2);
const tf=W(5,15)-.1;
tl.to('#tglF b',{right:90,duration:.5,ease:EI},tf);
tl.to('#tglF',{backgroundColor:"#BCC0C4",duration:.5,ease:EI},tf);
tl.to('#offt',{opacity:1,duration:.4,ease:EA},tf+.35);
for(let t=W(5,13);t<S(6)-1.2;t+=1.7){ tl.fromTo('#vshim',{x:-200,opacity:0},{x:1100,opacity:1,duration:1.5,ease:EA},t); tl.to('#vshim',{opacity:0,duration:.25},t+1.3); }
for(let t=tf+.6;t<S(6)-.8;t+=1.2){ tl.to('#tglF',{boxShadow:"0 0 0 12px rgba(134,217,63,.55)",duration:.6,ease:EA},t); tl.to('#tglF',{boxShadow:"0 0 0 0px rgba(134,217,63,0)",duration:.6,ease:EA},t+.6); }
tl.fromTo('#val',{y:0},{y:-8,duration:E(5)+GAP5-S(5)-.6,ease:EA,immediateRender:false},S(5)+.6);
hide('#sF',S(6)-.5,.3);
// ---- scene G: line 7
show('#sG',S(6)-.02,.3);
cap('cap6',6,S(6)-.02,0);
tl.fromTo('#outb',{x:80,y:20,opacity:0,scale:.94},{x:0,y:0,opacity:1,scale:1,duration:.6,ease:EO},S(6)+.1);
tl.fromTo('#mav',{opacity:0,scale:.7},{opacity:1,scale:1,duration:.4,ease:EO},W(6,3));
tl.fromTo('#dots2',{opacity:0,scale:.8},{opacity:1,scale:1,duration:.35,ease:EO},W(6,4));
tl.to('#dots2 b',{y:-10,duration:.3,ease:EA,yoyo:true,repeat:3,stagger:.1},W(6,4)+.1);
tl.to('#dots2',{opacity:0,duration:.2},W(6,5)+.08);
[1,2,3].forEach((k,i)=>tl.fromTo('#al'+k,{opacity:0,scale:.7,y:14},{opacity:1,scale:1,y:0,duration:.45,ease:EO},W(6,5)+.12+i*.3));
tl.fromTo('#outb',{rotate:0},{rotate:-1.5,duration:E(6)-S(6),ease:EA},S(6)+.7);
hide('#sG',E(6)+.1,.35);
// ---- loop-back: frame 0 again
tl.set('#sH',{autoAlpha:0},0);
tl.fromTo('#sH',{autoAlpha:0},{autoAlpha:1,duration:.35,ease:EA},E(6)+.38);
feedAnim('H',E(6)+.45,D);
tl.to('#al1,#al2,#al3',{y:-8,duration:.9,ease:EA,yoyo:true,repeat:3,stagger:.2},E(6)-1.6);
tl.to('#mini,#outb',{y:-6,duration:1.1,ease:EA,yoyo:true,repeat:2},E(6)-2.0);
'''

GAP5 = GAPS[4]
shell = open(H + "/shell8.html").read()
html = (shell.replace("__STYLES__", styles).replace("__MARKUP__", markup).replace("__CHROME__", "").replace("__SCRIPTS__", "")
        .replace("__D__", str(D)).replace("__CUES__", json.dumps(dict(lines=lines, D=D)))
        .replace("__CALLS__", f"const GAP5={GAP5};\n" + js).replace("__NSC__", "1"))
os.makedirs(H + "/hf", exist_ok=True)
open(H + "/hf/index.html", "w").write(html)
print("D=", D, [(l["n"], l["start"], l["end"]) for l in lines])
if "--render" in sys.argv:
    name = sys.argv[sys.argv.index("--render") + 1]
    env = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1", DO_NOT_TRACK="1")
    r = subprocess.run(["npx", "--no-install", "hyperframes", "render", "-o", f"{H}/out/{name}.mp4", "--format", "mp4", "--quiet"],
                       cwd=H + "/hf", env=env, capture_output=True, text=True, timeout=2400)
    print(r.stdout[-400:], r.stderr[-800:])
