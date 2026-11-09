#!/usr/bin/env python3
"""ep88 integrator. lines.txt (8 lines) + VOICE/<n>.wav -> cues.json, out/narration.wav, hf/index.html [--render name].
Env: VOICE (dir with 1..8.wav, default voice/final), GAPS (7 gaps, default below), TAIL (seconds after line 8, default 1.1).
Word times: no whisper here, so words inside a line are placed by sentence: the k-1 longest silences in the line wav split it into its k
sentences, and words are spread over each sentence by letter count. Good to ~0.1-0.2 s; the value card rows use it."""
import json, os, re, sys, subprocess
import soundfile as sf, numpy as np
H = os.path.dirname(os.path.abspath(__file__))
VOICE = os.environ.get("VOICE", H + "/voice/final")
GAPS = [float(x) for x in os.environ.get("GAPS", "0.32,0.3,0.3,0.34,0.36,0.36,3.3").split(",")]
TAIL = float(os.environ.get("TAIL", "1.1"))
ALL = [l.rstrip("\n") for l in open(H + "/lines.txt") if l.strip()]
assert len(ALL) == 8 and len(GAPS) == 7
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
for j in range(8):
    n = j + 1
    x, s = sf.read(f"{VOICE}/{n}.wav"); assert s == sr; x = x if x.ndim == 1 else x[:, 0]
    d = len(x) / sr
    ln = dict(n=n, text=ALL[j], start=round(t, 3), end=round(t + d, 3), words=words_for(x, ALL[j], t))
    lines.append(ln); parts.append((int(t * sr), x)); t += d + (GAPS[j] if j < 7 else 0)
D = round(lines[-1]["end"] + TAIL, 2)
nar = np.zeros(int((D + 0.3) * sr))
for i0, x in parts: nar[i0:i0 + len(x)] += x
os.makedirs(H + "/out", exist_ok=True)
sf.write(H + "/out/narration.wav", nar[:int(D * sr)], sr, subtype="PCM_16")
json.dump(dict(lines=lines, D=D), open(H + "/cues.json", "w"), indent=1)

# ------------------------------------------------------------------ page
PAL = [("#9ED8FF", "#E8F6FF", "#FFD84D", "#6CC070"), ("#FFB07A", "#FF7E7E", "#FFF1B0", "#5A4A6A"),
       ("#F6D8A8", "#F2B880", "#FFFFFF", "#C9783A"), ("#B8F0D0", "#7FD1AE", "#FFFFFF", "#2F8F6A"),
       ("#D9C8FF", "#A99BFF", "#FFE9A8", "#6A5BC8"), ("#F3E3C3", "#E3C48F", "#FFD0D0", "#B07A45")]


def tile(i, x, y, w, h, cls="", extra=""):
    c = PAL[i % 6]
    return (f'<div class="tile {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:linear-gradient(160deg,{c[0]},{c[1]})">'
            f'<i class="sun" style="background:{c[2]}"></i><i class="hill" style="background:{c[3]}"></i>{extra}</div>')


def phone(sfx):
    tiles = ""
    for i in range(6):
        r, c = divmod(i, 3)
        x = 18 + c * 244; y = 58 + r * 154
        tag = ""
        if i in (0, 2, 4):
            tag = f'<b class="tg tgA">NEVER POSTED</b>'
        else:
            tag = f'<b class="tg tgC">ON YOUR PAGE</b>'
        tiles += tile(i, x, y, 232, 142, "pt", tag)
    return f'''<div class="phone" id="phone{sfx}"><div class="pbar"><span>DRAWN EXAMPLE &middot; CAMERA ROLL</span><i class="bdot"></i></div>
{tiles}<div class="shim"></div>
<div class="prompt"><span>Allow suggestions from your camera roll?</span><div class="allow" id="allow{sfx}">Allow</div></div></div>'''


def capblock(n, sfx, size, top):
    toks = ALL[n - 1].split()
    sp = "".join(f'<span class="cw">{w}</span> ' for w in toks)
    return f'<div class="cap" id="cap{n}{sfx}" style="font-size:{size}px;line-height:{int(size*1.06)}px;top:{top}px">{sp}</div>'


def size_for(n):
    L = len(ALL[n - 1])
    return 100 if L <= 46 else (88 if L <= 58 else 78)


markup = f'''
<div class="scn" id="sA" style="visibility:visible;opacity:1">
 <div class="lgo" id="lgo"><img src="assets/facebook.svg"></div>
 {capblock(1, "", 96, 408)}
 {capblock(2, "", size_for(2), 290)}
 {phone("")}
</div>
<div class="scn" id="sB">
 {capblock(3, "", size_for(3), 290)}
 <div class="setc" id="setc"><div class="r1"><div class="lg2"><img src="assets/facebook.svg"></div><div class="t1">Camera roll sharing suggestions</div></div>
  <div class="hr"></div><div class="r2"><div class="t2">Get camera roll suggestions when you're browsing Facebook</div><div class="tgl" id="tglB"><b></b></div></div></div>
 <div class="note2" id="noteB">drawn example of the settings row</div>
</div>
<div class="scn" id="sC">
 {capblock(4, "", size_for(4), 290)}
 <div class="strip" id="strip">{"".join(tile(i, i*214, 0, 200, 150, "st") for i in range(10))}</div>
 <div class="scan" id="scan"></div>
 <div class="collage" id="collage"><div class="mos">{tile(0,0,0,122,122,"mt")}{tile(1,132,0,122,122,"mt")}{tile(2,0,132,122,122,"mt")}{tile(3,132,132,122,122,"mt")}</div>
  <div class="chips"><div class="chip2">Collage</div><div class="chip2">Edit</div></div></div>
</div>
<div class="scn" id="sD">
 {capblock(5, "", size_for(5), 290)}
 <div class="meta" id="meta"><div class="mh">META SAYS</div>
  <div class="mq" id="mq1">&ldquo;You must opt in to use this feature&rdquo;</div>
  <div class="mq" id="mq2">&ldquo;We don't use photos and videos from your camera roll for ads targeting.&rdquo;</div>
  <div class="mf">Meta newsroom, April 2026 &middot; EU and UK</div></div>
</div>
<div class="scn" id="sE">
 {capblock(6, "", size_for(6), 290)}
 <div class="dlg" id="dlg"><div class="dt">Allow suggestions from your camera roll?</div>
  <div class="btns"><div class="btn1">Not now</div><div class="btn2" id="btn2">Allow</div></div><div class="ripple" id="ripple"></div><div class="finger" id="finger"></div></div>
 <div class="note2" id="noteE">drawn example, not the real prompt</div>
</div>
<div class="scn" id="sF">
 <div class="val" id="val"><div class="vh"><span class="vchip">CHECK IT NOW</span><div class="lg3"><img src="assets/facebook.svg"></div></div>
  <div class="vr" id="vr1"><i>1</i><p>Profile picture</p></div>
  <div class="vr" id="vr2"><i>2</i><p>Settings &amp; Privacy</p></div>
  <div class="vr" id="vr3"><i>3</i><p>Settings</p></div>
  <div class="vr big" id="vr4"><i>4</i><p>Camera roll sharing suggestions</p></div>
  <div class="vr" id="vr5"><i>5</i><p>Switch it off</p><div class="tgl on" id="tglF"><b></b></div><span class="offt" id="offt">OFF</span></div>
  <div class="vn" id="vn">menu names can differ by app version</div></div>
</div>
<div class="scn" id="sG">
 {capblock(8, "", size_for(8), 290)}
 <div class="out" id="outb"><div class="mini"><div class="mt1">Camera roll sharing suggestions</div><div class="tgl" id="tglG"><b></b></div></div></div>
 <div class="mum"><div class="av" id="mav">M</div></div>
 <div class="dots2" id="dots2"><b></b><b></b><b></b></div>
 <div class="al" id="al1">Allow</div><div class="al" id="al2">Allow</div><div class="al" id="al3">Allow</div>
</div>
<div class="scn" id="sH">
 <div class="lgo" id="lgoH"><img src="assets/facebook.svg"></div>
 {capblock(1, "H", 96, 408)}
 {phone("H")}
</div>
'''

styles = '''
:root{--acc:#86D93F}
.scn .cap,.scn .lgo,.phone,.setc,.strip,.scan,.collage,.meta,.dlg,.val,.out,.note2{position:absolute}
.cap{left:65px;width:950px;text-align:center;font-weight:900;letter-spacing:-.045em;opacity:0;visibility:hidden}
.cw{display:inline-block;color:#8F8F85;margin:0 8px}
#cap1,#cap1H{opacity:1;visibility:visible}
.lgo{left:65px;top:290px;width:104px;height:104px;border-radius:50%;background:#fff;border:6px solid var(--ink);box-shadow:7px 7px 0 var(--ink);display:flex;align-items:center;justify-content:center;overflow:hidden}
.lgo img{width:112%;height:112%;margin:-6%}
.phone{left:160px;top:748px;width:760px;height:482px;background:#fff;border:7px solid var(--ink);border-radius:44px;box-shadow:10px 10px 0 var(--ink);overflow:hidden}
.pbar{position:absolute;left:0;top:0;width:100%;height:50px;background:#EFEFE8;border-bottom:4px solid var(--ink);display:flex;align-items:center;justify-content:space-between;padding:0 24px;font-weight:800;font-size:22px;letter-spacing:.06em;color:var(--ink2)}
.bdot{display:block;width:20px;height:20px;border-radius:50%;background:#1877F2}
.tile{position:absolute;overflow:hidden;border-radius:14px;border:4px solid var(--ink)}
.sun{position:absolute;right:16%;top:12%;width:22%;padding-top:22%;border-radius:50%}
.hill{position:absolute;left:-20%;bottom:-46%;width:140%;padding-top:70%;border-radius:50%}
.tg{position:absolute;left:8px;bottom:8px;font-weight:900;font-size:21px;letter-spacing:.03em;padding:3px 10px 5px;border:3px solid var(--ink);border-radius:10px;white-space:nowrap;line-height:24px}
.tgA{background:var(--acc);color:var(--ink)}
.tgC{background:#E4E4DC;color:var(--ink2);opacity:0}
.shim{position:absolute;left:0;top:50px;width:110px;height:310px;background:linear-gradient(100deg,rgba(255,255,255,0),rgba(255,255,255,.65),rgba(255,255,255,0));transform:translateX(-200px) skewX(-12deg);opacity:.0}
.prompt{position:absolute;left:0;top:366px;width:100%;height:116px;background:#F4F4EF;border-top:4px solid var(--ink);display:flex;align-items:center;justify-content:space-between;padding:0 26px;font-weight:800;font-size:32px;letter-spacing:-.02em;line-height:36px}
.prompt span{width:440px}
.allow{background:var(--acc);border:5px solid var(--ink);border-radius:28px;box-shadow:5px 5px 0 var(--ink);padding:8px 38px 12px;font-weight:900;font-size:44px}
.setc{left:80px;top:790px;width:920px;background:#fff;border:7px solid var(--ink);border-radius:44px;box-shadow:12px 12px 0 var(--ink);padding:30px 32px 30px}
.setc .r1{display:flex;align-items:center;gap:24px}
.lg2{width:100px;height:100px;flex:none;border-radius:50%;border:5px solid var(--ink);overflow:hidden;background:#fff}.lg2 img{width:112%;height:112%;margin:-6%}
.t1{font-weight:900;font-size:56px;line-height:60px;letter-spacing:-.035em}
.hr{height:5px;background:var(--ink);opacity:.15;margin:24px 0}
.r2{display:flex;align-items:center;justify-content:space-between;gap:20px}
.t2{font-weight:700;font-size:36px;line-height:42px;letter-spacing:-.02em;width:640px;color:var(--ink2)}
.tgl{position:relative;width:124px;height:70px;flex:none;border-radius:35px;border:5px solid var(--ink);background:#D2D2C8}
.tgl b{position:absolute;left:5px;top:5px;width:50px;height:50px;border-radius:50%;background:#fff;border:4px solid var(--ink)}
.tgl.on{background:var(--acc)}.tgl.on b{left:auto;right:5px}
.note2{left:80px;width:920px;text-align:center;font-weight:700;font-size:28px;letter-spacing:.02em;color:var(--ink2)}
#noteB{top:1150px}#noteE{top:1186px}
.strip{left:65px;top:780px;width:2200px;height:150px}
.strip .tile{border-radius:16px}
.scan{left:470px;top:760px;width:140px;height:190px;border:7px solid var(--ink);border-radius:26px;background:rgba(134,217,63,.28);box-shadow:0 0 0 7px rgba(134,217,63,.35)}
.collage{left:150px;top:980px;width:780px;height:264px;background:#fff;border:7px solid var(--ink);border-radius:40px;box-shadow:10px 10px 0 var(--ink)}
.mos{position:absolute;left:22px;top:2px;width:254px;height:254px}
.mt{border-radius:12px}
.chips{position:absolute;left:310px;top:34px;display:flex;flex-direction:column;gap:22px}
.chip2{background:var(--acc);border:5px solid var(--ink);border-radius:26px;box-shadow:5px 5px 0 var(--ink);font-weight:900;font-size:56px;padding:2px 34px 8px;width:fit-content}
.meta{left:80px;top:760px;width:920px;background:#fff;border:7px solid var(--ink);border-radius:44px;box-shadow:12px 12px 0 var(--ink);padding:24px 36px 24px}
.mh{display:inline-block;background:var(--ink);color:#fff;font-weight:900;font-size:34px;letter-spacing:.08em;padding:6px 20px 9px;border-radius:16px}
.mq{margin-top:24px;font-weight:800;font-size:54px;line-height:60px;letter-spacing:-.03em;opacity:0}
.mf{margin-top:18px;font-weight:700;font-size:28px;letter-spacing:.02em;color:var(--ink2);opacity:0}
.dlg{left:130px;top:790px;width:820px;height:360px;background:#fff;border:7px solid var(--ink);border-radius:44px;box-shadow:12px 12px 0 var(--ink);padding:34px 36px}
.dt{font-weight:900;font-size:56px;line-height:60px;letter-spacing:-.035em}
.btns{position:absolute;left:36px;right:36px;bottom:34px;display:flex;gap:28px;justify-content:space-between}
.btn1{flex:1;text-align:center;font-weight:800;font-size:46px;padding:14px 0 20px;border:5px solid var(--ink);border-radius:30px;background:#F1F1EA;color:var(--ink2)}
.btn2{flex:1.25;text-align:center;font-weight:900;font-size:58px;padding:8px 0 16px;border:6px solid var(--ink);border-radius:30px;background:var(--acc);box-shadow:6px 6px 0 var(--ink)}
.ripple{position:absolute;right:140px;bottom:50px;width:90px;height:90px;margin:0;border-radius:50%;border:8px solid var(--ink);opacity:0}
.finger{position:absolute;right:120px;bottom:-34px;width:70px;height:70px;border-radius:50%;background:rgba(14,14,14,.82);opacity:0}
.val{left:80px;top:300px;width:920px;background:#fff;border:8px solid var(--ink);border-radius:48px;box-shadow:14px 14px 0 var(--ink);padding:26px 34px 26px}
.vh{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px}
.vchip{background:var(--acc);border:5px solid var(--ink);border-radius:22px;box-shadow:5px 5px 0 var(--ink);font-weight:900;font-size:42px;letter-spacing:.04em;padding:4px 24px 8px}
.lg3{width:88px;height:88px;border-radius:50%;border:5px solid var(--ink);overflow:hidden}.lg3 img{width:112%;height:112%;margin:-6%}
.vr{display:flex;align-items:center;gap:26px;height:122px;opacity:0;position:relative}
.vr.big{height:170px}
.vr i{flex:none;width:78px;height:78px;border:6px solid var(--ink);border-radius:24px;background:var(--acc);box-shadow:5px 5px 0 var(--ink);font-style:normal;font-weight:900;font-size:52px;line-height:66px;text-align:center}
.vr p{font-weight:900;font-size:62px;line-height:64px;letter-spacing:-.035em;flex:1}
.vr.big p{font-size:60px}
.vr .tgl{margin-right:6px}
.offt{position:absolute;right:170px;top:40px;font-weight:900;font-size:30px;letter-spacing:.06em;background:var(--ink);color:#fff;padding:2px 14px 5px;border-radius:12px;opacity:0}
.vn{margin-top:14px;font-weight:700;font-size:30px;letter-spacing:.01em;color:var(--ink2);text-align:center;opacity:0}
.out{left:320px;top:780px;width:665px;background:var(--ink);border-radius:46px 46px 12px 46px;padding:22px;box-shadow:8px 8px 0 rgba(14,14,14,.25)}
.mini{background:#fff;border-radius:30px;padding:22px 24px;display:flex;align-items:center;gap:18px;justify-content:space-between}
.mt1{font-weight:900;font-size:40px;line-height:44px;letter-spacing:-.03em}
.mum{position:absolute;left:80px;top:1062px}
.av{width:100px;height:100px;border-radius:50%;background:#FFD84D;border:6px solid var(--ink);box-shadow:6px 6px 0 var(--ink);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:56px;opacity:0}
.dots2{position:absolute;left:210px;top:1066px;width:190px;height:92px;background:#fff;border:6px solid var(--ink);border-radius:40px 40px 40px 10px;box-shadow:7px 7px 0 var(--ink);display:flex;align-items:center;justify-content:center;gap:14px;opacity:0}
.dots2 b{display:block;width:20px;height:20px;border-radius:50%;background:var(--ink)}
.al{position:absolute;top:1056px;background:var(--acc);border:6px solid var(--ink);border-radius:36px 36px 36px 10px;box-shadow:7px 7px 0 var(--ink);font-weight:900;font-size:56px;padding:6px 26px 14px;opacity:0}
#al1{left:210px}#al2{left:470px}#al3{left:730px}
'''

js = r'''
const S=n=>L[n-1].start,E=n=>L[n-1].end,W=(n,i)=>L[n-1].words[i][0],WE=(n,i)=>L[n-1].words[i][1];
const EA="sine.inOut",EO="power2.out",EI="power2.inOut";
const show=(el,t,d)=>tl.to(el,{autoAlpha:1,duration:d||.3,ease:EA},t);
const hide=(el,t,d)=>tl.to(el,{autoAlpha:0,duration:d||.22,ease:EA},t);
const Q=s=>document.querySelector(s), QA=s=>[...document.querySelectorAll(s)];
// captions: lit words
function cap(id,n,tshow,thide){
  const els=QA('#'+id+' .cw');
  els.forEach((e,i)=>{ if(W(n,i)<=0.001){ tl.set(e,{color:"#0E0E0E"},0);} else tl.to(e,{color:"#0E0E0E",duration:.16,ease:EA},W(n,i)-0.02); });
  if(tshow>0) tl.fromTo('#'+id,{autoAlpha:0,y:10},{autoAlpha:1,y:0,duration:.3,ease:EO},tshow);
  if(thide) hide('#'+id,thide,.2);
}
function phoneAnim(sfx,t0,t1){
  // float + scale drift over [t0,t1]
  tl.fromTo('#phone'+sfx,{y:0,scale:1},{y:-10,scale:1.025,duration:t1-t0,ease:EA},t0);
  // shimmer sweeps
  for(let t=t0+.2;t<t1-.8;t+=1.6){ tl.fromTo('#phone'+sfx+' .shim',{x:-200,opacity:0},{x:880,opacity:1,duration:1.5,ease:EA},t); tl.to('#phone'+sfx+' .shim',{opacity:0,duration:.3},t+1.3); }
  // allow pulse
  for(let t=t0+.6;t<t1-.4;t+=1.1){ tl.to('#allow'+sfx,{scale:1.1,duration:.5,ease:EA,transformOrigin:"50% 50%"},t); tl.to('#allow'+sfx,{scale:1,duration:.5,ease:EA},t+.5); }
  // tag breathing
  QA('#phone'+sfx+' .tgA').forEach((e,i)=>{ for(let t=t0+.3+i*.25;t<t1-.5;t+=1.4){ tl.to(e,{scale:1.07,duration:.7,ease:EA,transformOrigin:"0% 100%"},t); tl.to(e,{scale:1,duration:.7,ease:EA},t+.7);} });
}
// ---- scene A: line 1 + 2 (phone, tags). frame 0 is already fully drawn.
const tA1=E(2);
tl.fromTo('#lgo',{scale:1},{scale:1.06,duration:E(1),ease:EA},0);
cap('cap1',1,0,E(1)+.04);
hide('#lgo',E(1)+.04,.22);
cap('cap2',2,E(1)+.16,tA1);   // fade in after cap1 is gone
phoneAnim('',0,tA1);
// line 2: untagged tiles say ON YOUR PAGE, tagged ones ring
QA('#phone .tgC').forEach((e,i)=>tl.to(e,{opacity:1,duration:.4,ease:EA},W(2,2)+.05+i*.12));
QA('#phone .pt').forEach((e,i)=>{ if(i%2==0){ tl.to(e,{boxShadow:"0 0 0 9px rgba(134,217,63,.9)",duration:.5,ease:EA},W(2,6)+i*.05); } });
hide('#sA',tA1,.2);
// ---- scene B: line 3
show('#sB',S(3)-.08,.3);
tl.fromTo('#setc',{y:30,opacity:0},{y:0,opacity:1,duration:.55,ease:EO},S(3)-.05);
tl.fromTo('#noteB',{opacity:0},{opacity:1,duration:.4},S(3)+.4);
cap('cap3',3,S(3)-.05,0);
tl.fromTo('#setc',{scale:1},{scale:1.03,duration:E(3)-S(3)+.3,ease:EA},S(3));
tl.to('#tglB b',{x:0,duration:.01},S(3));
tl.to('#tglB',{boxShadow:"0 0 0 10px rgba(134,217,63,.7)",duration:.5,ease:EA},W(3,4)); tl.to('#tglB',{boxShadow:"0 0 0 0px rgba(134,217,63,0)",duration:.5,ease:EA},W(3,4)+.6);
hide('#sB',E(3),.2);
// ---- scene C: line 4
show('#sC',S(4)-.1,.3);
cap('cap4',4,S(4)-.05,0);
tl.fromTo('#strip',{x:140,opacity:0},{x:0,opacity:1,duration:.5,ease:EO},S(4)-.05);
tl.fromTo('#strip',{x:0},{x:-1100,duration:E(4)-S(4)+.4,ease:EA},S(4)+.2);
tl.fromTo('#scan',{opacity:0,scale:.9},{opacity:1,scale:1,duration:.4,ease:EO},S(4)+.1);
tl.to('#scan',{scale:1.06,duration:.8,ease:EA,yoyo:true,repeat:2},S(4)+.5);
tl.fromTo('#collage',{y:50,opacity:0,scale:.94},{y:0,opacity:1,scale:1,duration:.6,ease:EO},W(4,5)-.05);
tl.fromTo('#collage .mt',{scale:.6,opacity:0},{scale:1,opacity:1,duration:.45,ease:EO,stagger:.12},W(4,5)+.1);
tl.fromTo('#collage .chip2',{x:-20,opacity:0},{x:0,opacity:1,duration:.45,ease:EO,stagger:.35},W(4,6)+.1);
tl.to('#collage',{y:-8,duration:E(4)-W(4,5),ease:EA},W(4,5)+.6);
hide('#sC',E(4),.2);
// ---- scene D: line 5
show('#sD',S(5)-.1,.3);
cap('cap5',5,S(5)-.05,0);
tl.fromTo('#meta',{y:30,opacity:0},{y:0,opacity:1,duration:.55,ease:EO},S(5)-.05);
tl.to('#mq1',{opacity:1,duration:.5,ease:EA},W(5,1));
tl.to('#mq2',{opacity:1,duration:.5,ease:EA},W(5,7)-.1);
tl.to('#mf',{opacity:1,duration:.5,ease:EA},W(5,12));
tl.fromTo('#meta',{scale:1},{scale:1.03,duration:E(5)-S(5)+.3,ease:EA},S(5));
hide('#sD',E(5),.2);
// ---- scene E: line 6
show('#sE',S(6)-.1,.3);
cap('cap6',6,S(6)-.05,0);
tl.fromTo('#dlg',{y:40,opacity:0},{y:0,opacity:1,duration:.55,ease:EO},S(6)-.05);
tl.fromTo('#noteE',{opacity:0},{opacity:1,duration:.4},S(6)+.4);
tl.to('#btn2',{scale:1.07,duration:.55,ease:EA,transformOrigin:"50% 50%"},S(6)+.4);tl.to('#btn2',{scale:1,duration:.5,ease:EA},S(6)+.95);
// tap on the word Allow
const tp=W(6,5);
tl.fromTo('#finger',{opacity:0,y:50,x:20},{opacity:1,y:-30,x:0,duration:.5,ease:EO},tp-.45);
tl.to('#btn2',{scale:.95,duration:.22,ease:EA},tp);
tl.fromTo('#ripple',{opacity:.9,scale:.5},{opacity:0,scale:2.6,duration:.9,ease:EO},tp+.05);
tl.to('#btn2',{scale:1,duration:.4,ease:EA},tp+.22);
tl.to('#finger',{opacity:0,duration:.5,ease:EA},tp+.6);
tl.fromTo('#dlg',{scale:1},{scale:1.03,duration:E(6)-S(6)+.3,ease:EA},S(6));
hide('#sE',E(6),.2);
// ---- scene F: line 7 value card (held after speech)
show('#sF',S(7)-.1,.3);
tl.fromTo('#val',{y:30,opacity:0},{y:0,opacity:1,duration:.55,ease:EO},S(7)-.05);
[[1,3],[2,5],[3,8],[4,9],[5,13]].forEach(([r,wi])=>{ tl.fromTo('#vr'+r,{opacity:0,x:-30},{opacity:1,x:0,duration:.5,ease:EO},W(7,wi)-.12); });
tl.to('#vn',{opacity:1,duration:.5,ease:EA},W(7,13)+.2);
// flip the toggle ON -> OFF on the words "switch it off"
const tf=W(7,15)-.15;
tl.to('#tglF b',{right:70,duration:.5,ease:EI},tf);
tl.to('#tglF',{backgroundColor:"#D2D2C8",duration:.5,ease:EI},tf);
tl.to('#offt',{opacity:1,duration:.4,ease:EA},tf+.35);
tl.fromTo('#val',{scale:1},{scale:1.02,duration:E(7)+GAP7-S(7),ease:EA},S(7)+.3);
hide('#sF',S(8)-.5,.3);
// ---- scene G: line 8
show('#sG',S(8)-.02,.3);
cap('cap8',8,S(8)-.02,0);
tl.fromTo('#outb',{x:80,y:20,opacity:0,scale:.94},{x:0,y:0,opacity:1,scale:1,duration:.6,ease:EO},S(8)+.1);
tl.fromTo('#mav',{opacity:0,scale:.7},{opacity:1,scale:1,duration:.4,ease:EO},W(8,3));
tl.fromTo('#dots2',{opacity:0,scale:.8},{opacity:1,scale:1,duration:.35,ease:EO},W(8,4));
tl.to('#dots2 b',{y:-8,duration:.3,ease:EA,yoyo:true,repeat:3,stagger:.1},W(8,4)+.1);
tl.to('#dots2',{opacity:0,duration:.2},W(8,5)+.08);
[1,2,3].forEach((k,i)=>tl.fromTo('#al'+k,{opacity:0,scale:.7,y:14},{opacity:1,scale:1,y:0,duration:.45,ease:EO},W(8,5)+.12+i*.3));
tl.fromTo('#outb',{rotate:0},{rotate:-1.5,duration:E(8)-S(8),ease:EA},S(8)+.7);
hide('#sG',E(8)+.1,.35);
// ---- loop-back: frame 0 again
tl.set('#sH',{autoAlpha:0},0);
tl.fromTo('#sH',{autoAlpha:0},{autoAlpha:1,duration:.35,ease:EA},E(8)+.38);
QA('#capH .cw').forEach((e,i)=>{ if(i==0) tl.set(e,{color:"#0E0E0E"},0); });
tl.fromTo('#phoneH',{y:0},{y:-6,duration:D-E(8)-.3,ease:EA},E(8)+.4);
'''

# hold after line 7 as JS constant
GAP7 = GAPS[6]
shell = open(H + "/shell8.html").read()
html = (shell.replace("__STYLES__", styles).replace("__MARKUP__", markup).replace("__CHROME__", "").replace("__SCRIPTS__", "")
        .replace("__D__", str(D)).replace("__CUES__", json.dumps(dict(lines=lines, D=D)))
        .replace("__CALLS__", f"const GAP7={GAP7};\n" + js).replace("__NSC__", "1"))
os.makedirs(H + "/hf", exist_ok=True)
open(H + "/hf/index.html", "w").write(html)
print("D=", D, [(l["n"], l["start"], l["end"]) for l in lines])
if "--render" in sys.argv:
    name = sys.argv[sys.argv.index("--render") + 1]
    env = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1", DO_NOT_TRACK="1")
    r = subprocess.run(["npx", "--no-install", "hyperframes", "render", "-o", f"{H}/out/{name}.mp4", "--format", "mp4", "--quiet"],
                       cwd=H + "/hf", env=env, capture_output=True, text=True, timeout=2400)
    print(r.stdout[-400:], r.stderr[-800:])
