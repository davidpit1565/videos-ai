#!/usr/bin/env python3
"""Super Ivy ad (23 s, not an episode): Miki style + GSAP skills, structure from video/ep105/build105n.py.
Reads cues-ivy.json (13 lines) and voice/words-ivy.json; writes hf/index.html, sfx-ivy.json, out/build-ivy.log.
Claims on screen: only the plan's claims table (channel/ad-ivy-plan.md section A). Real marks only: ChatGPT svg (repo, ep86), Claude sparkle (ep105 page),
Gemini icon (repo, ep83 Commons file), Super Ivy app icon and real screenshots/preview frames (App Store media, never retouched, cropped).
Screens: S1 problem (1-2) | S3 Ivy (3) | S4 bring ChatGPT (4) | S5 Claude+Gemini (5) | card with preview/screenshot (6-8, 9-10) | S11 hands full | S12 icon+free | S13 CTA + Ad.
Safe area: key text x 108-972, y 269-1248; right edge <= 864 below y 1056 (55-85% band).
"""
import json, os, re, sys
H_ = os.path.dirname(os.path.abspath(__file__))
INK = "#0f0f0f"; ACC = "#A9783A"; GREY = "#8a8982"
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
LOG = []
def say(x): LOG.append(x); print(x)
CUES = json.load(open(H_ + "/cues-ivy.json"))
LN = {l["n"]: l for l in CUES["lines"]}; assert len(LN) == 13
s = lambda n: float(LN[n]["start"]); e = lambda n: float(LN[n]["end"])
D = float(CUES["D"])
WORDS = [[w["word"], w["start"], w["end"]] for w in json.load(open(H_ + "/voice/words-ivy.json"))]
tF = round(D - .16, 3)
def W(n, toks, k=0, fallback=.5):
    toks = (toks,) if isinstance(toks, str) else toks
    c = 0
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
    ws = txt.split(); assert len(ws) == len(times), (txt, times)
    return list(zip(ws, times))
ring = lambda id_, left, top, w, h: (f'<svg class="ring" id="{id_}" viewBox="0 0 400 160" preserveAspectRatio="none" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px" data-decor>'
                                     f'<path d="M14 84 C6 30 130 8 214 10 C318 12 394 40 388 84 C382 132 270 150 190 148 C96 146 20 132 14 84 Z" fill="none" stroke="{ACC}" stroke-width="5" vector-effect="non-scaling-stroke" stroke-linecap="round"/></svg>')
A = "assets/"
SC = {}; T = {}
NMEM = len(os.listdir(H_ + "/hf/assets/mem")); NACT = len(os.listdir(H_ + "/hf/assets/act"))

# ---------------------------------------------------------------- S1 the problem (lines 1-2): frame 0 complete, the same intro is retyped and fades
BUB = "Hi, a bit about me…"
bub = "".join(f'<div class="bub" id="bub{i}" style="top:{708 + i * 128}px;opacity:{o}"><span>{BUB}</span></div>' for i, o in enumerate((1, .6, .3)))
SC["S1"] = (f'<img class="lg ic" id="ic1" src="{A}icon.png" style="left:108px;top:286px;width:124px;height:124px">'
            f'<div class="ln lead tag" id="vai" style="left:256px;top:322px;font-size:50px;line-height:56px">VOICE AI</div>'
            f'<img class="lg" id="cg" src="{A}chatgpt.svg" style="left:108px;top:452px;width:226px;height:226px">'
            f'<div class="ln hv" id="cgt" style="left:360px;top:492px;font-size:124px;line-height:134px">ChatGPT</div>' + bub +
            line("hv", [("AGAIN.", W(1, "again", 0, .9))], 1052, 190, lh=1.0, fast=False, ready=True))
T["S1"] = dict(t0=0, again=W(1, "again", 0, .9), again2=W(2, "again", 0, .95), brk=round(W(1, "again", 0, .9) - .33, 3), end=s(3))
CUR = s(3)

# ---------------------------------------------------------------- S3 meet Super Ivy (line 3)
SC["S3"] = (f'<img class="lg ic" id="ic3" src="{A}icon.png" style="left:108px;top:380px;width:340px;height:340px">' +
            line("hv", seq("SUPER IVY", [W(3, "meet", 0, .1), W(3, "ivy", 0, .35)]), 760, 138, lh=1.0) +
            line("lead", seq("A voice AI. Free.", [W(3, "a", 0, .6), W(3, "voice", 0, .65), W(3, "ai", 0, .72), W(3, "free", 0, .9)]), 920, 80, acc=("free",)) + ring("rgFr", 380, 905, 260, 120))
T["S3"] = dict(t0=s(3), free=W(3, "free", 0, .9), end=s(4))
CUR = s(4)

# ---------------------------------------------------------------- S4 bring what ChatGPT knows (line 4)
SC["S4"] = (f'<img class="lg" id="cg4" src="{A}chatgpt.svg" style="left:108px;top:320px;width:250px;height:250px">'
            f'<svg class="arw" id="arw" viewBox="0 0 300 100" style="left:384px;top:395px;width:290px;height:100px" data-decor><path d="M8 50 H280 M236 14 L284 50 L236 86" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            f'<img class="lg ic" id="ic4" src="{A}icon.png" style="left:702px;top:320px;width:250px;height:250px">' +
            line("lead", seq("Bring what ChatGPT", [W(4, "bring", 0, .05), W(4, "what", 0, .2), W(4, "chatgpt", 0, .4)]), 640, 70) +
            line("hv", seq("KNOWS", [W(4, "knows", 0, .6)]), 720, 150, lh=1.0) +
            line("hv", seq("ABOUT YOU.", [W(4, "about", 0, .75), W(4, "you", 0, .9)]), 880, 130, lh=1.0, acc=("you",)))
T["S4"] = dict(t0=s(4), end=s(5))
CUR = s(5)

# ---------------------------------------------------------------- S5 Claude and Gemini too (line 5)
SC["S5"] = (f'<img class="lg" id="m5a" src="{A}claude-sparkle-site.png" style="left:108px;top:400px;width:330px;height:330px">'
            f'<img class="lg" id="m5b" src="{A}gemini.svg" style="left:520px;top:400px;width:330px;height:330px">' +
            line("hv", seq("TOO.", [W(5, "too", 0, .9)]), 800, 250, lh=1.0, acc=("too",)))
T["S5"] = dict(t0=s(5), claude=W(5, "claude", 0, .1), gem=W(5, "gemini", 0, .5), end=s(6))
CUR = s(6)

# ---------------------------------------------------------------- S6-S10: ONE card in the same slot: real preview segments and the real Memory screenshot
mem = "".join(f'<img class="fr mf" src="{A}mem/m{i:03d}.jpg">' for i in range(1, NMEM + 1))
act = "".join(f'<img class="fr af" src="{A}act/a{i:03d}.jpg">' for i in range(1, NACT + 1))
CARD = f'<div class="vc" id="vc">{mem}<img class="fr" id="shotm" src="{A}shot-memory.jpg">{act}</div>'
T["V"] = dict(t0=s(6), memstart=round(s(6) - .06, 3), shot=round(s(6) - .06 + NMEM / 15 - .1, 3), actstart=round(s(9) - .04, 3), actshow=round(s(9) - .04, 3), end=s(11), nmem=NMEM, nact=NACT)
CUR = s(11)

# ---------------------------------------------------------------- S11 hands full (line 11)
SC["S11"] = (line("hv", seq("HANDS FULL?", [W(11, "hands", 0, .2), W(11, "full", 0, .5)]), 540, 112, lh=1.0) +
             line("hv", seq("TALK.", [W(11, "talk", 0, .9)]), 665, 270, lh=1.0, acc=("talk",)))
T["S11"] = dict(t0=s(11), end=s(12))
CUR = s(12)

# ---------------------------------------------------------------- S12 Super Ivy, free on the App Store (line 12)
SC["S12"] = (f'<img class="lg ic" id="ic12" src="{A}icon.png" style="left:108px;top:340px;width:380px;height:380px">' +
             line("hv", seq("SUPER IVY", [W(12, "super", 0, .1), W(12, "ivy", 0, .3)]), 770, 138, lh=1.0) +
             line("lead", seq("Free on the App Store", [W(12, "free", 0, .5), W(12, "on", 0, .6), W(12, "the", 0, .7), W(12, "app", 0, .8), W(12, "store", 0, .9)]), 930, 70, acc=("free",)))
T["S12"] = dict(t0=s(12), end=s(13))
CUR = s(13)

# ---------------------------------------------------------------- S13 CTA + the Ad tag in the last 2 s (line 13)
SC["S13"] = (line("lead", seq("Download it.", [W(13, "download", 0, .05), W(13, "it", 0, .3)]), 470, 92) +
             line("hv", seq("STOP STARTING", [W(13, "stop", 0, .5), W(13, "starting", 0, .65)]), 590, 104, lh=1.0) +
             line("hv", seq("OVER.", [W(13, "over", 0, .92)]), 700, 250, lh=1.0, acc=("over",)) +
             '<div class="adt" id="adt" data-decor>Ad</div>')
T["S13"] = dict(t0=s(13), adat=round(D - 2.0, 3), end=tF)
for k in T:
    for kk, v in list(T[k].items()):
        if isinstance(v, float): T[k][kk] = round(v, 3)
T["tF"] = tF; T["D"] = D

# ---------------------------------------------------------------- sfx (soft clips from the real library in ep89c/sfx)
SFX = []
def sfx(f, t, g=-13): SFX.append(dict(f=f, t=round(max(0, t), 3), g=g))
sfx("click_a.ogg", .2, -17); sfx("click_a.ogg", T["S1"]["brk"], -17); sfx("select.ogg", T["S1"]["again"], -13); sfx("whoosh_b.ogg", s(3) - .05, -15)
sfx("select.ogg", T["S3"]["free"], -13); sfx("whoosh_b.ogg", s(4) - .05, -17); sfx("click_a.ogg", T["S5"]["claude"], -15); sfx("click_a.ogg", T["S5"]["gem"], -15)
sfx("whoosh_b.ogg", s(6) - .05, -16); sfx("select.ogg", T["V"]["shot"], -16); sfx("whoosh_b.ogg", s(9) - .1, -17); sfx("select.ogg", s(11) + .5, -14)
sfx("whoosh_b.ogg", s(12) - .05, -16); sfx("select.ogg", s(13) + .4, -14)
SFX.sort(key=lambda x: x["t"]); json.dump(SFX, open(H_ + "/sfx-ivy.json", "w"), indent=1)

scenes = "".join(f'<div class="sc" id="sc{n[1:]}">{SC[n]}</div>' for n in SC)
CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;font-weight:500;color:{INK};font-kerning:none}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}}
.bgw{{position:absolute;left:-20px;top:-20px;width:1120px;height:1960px;background:#ecebe5 url(assets/bg.jpg);background-size:1120px 1960px;will-change:transform}}
#cam{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}}
.sc{{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0;visibility:hidden;will-change:transform,opacity}} #sc1{{opacity:1;visibility:visible}}
.sc>*{{position:absolute}}
.lg{{display:block;flex:none;object-fit:contain}} .ic{{border-radius:22.4%;box-shadow:0 24px 44px rgba(20,20,20,.22)}}
.ln{{white-space:nowrap}}
.m{{display:inline-block;overflow:hidden;vertical-align:top;padding:0 .05em .08em 0;margin-right:.2em}} .lead .m{{margin-right:.24em}}
.w{{display:inline-block;transform:translateY(112%);will-change:transform}} .w.rdy{{transform:none}}
.lead .w{{font-weight:500;letter-spacing:-.02em;color:#33322f}} .hv .w{{font-weight:900;letter-spacing:-.045em}}
.w.acc{{color:{INK}}}
.tag{{font-weight:800;letter-spacing:.14em;color:#55544f}}
.ring,.arw{{overflow:visible}}
.hv{{font-weight:900;letter-spacing:-.045em}}
.bub{{position:absolute;left:108px;width:864px;height:112px;padding:0 44px;border-radius:40px;background:#e6e5df;display:flex;align-items:center;font-weight:500;font-size:62px;letter-spacing:-.02em;color:#1d1d1b;white-space:nowrap}}
.vc{{position:absolute;left:108px;top:270px;width:864px;height:978px;border-radius:44px;overflow:hidden;background:#0b0e13;box-shadow:0 30px 60px rgba(20,20,20,.25);opacity:0;visibility:hidden}}
.fr{{position:absolute;left:0;top:0;width:864px;height:978px;display:none}} #shotm{{display:block;opacity:0}}
.adt{{position:absolute;left:880px;top:280px;font-weight:800;font-size:38px;letter-spacing:.08em;color:#6a6963;border:3px solid #6a6963;border-radius:12px;padding:2px 16px;opacity:0}}
'''
JS = r'''
gsap.registerPlugin(SplitText, DrawSVGPlugin, CustomEase);
const T=__T__, ACC='__ACC__', INK='__INK__';
const expoOut=CustomEase.create("expoOut","0.16,1,0.3,1"), expoIn=CustomEase.create("expoIn","0.7,0,0.84,0");
const spring=(w=>{const f=t=>1-(1+w*t)*Math.exp(-w*t), n=f(1); return t=>f(t)/n})(9);
const show=id=>gsap.fromTo(id,{autoAlpha:0,y:10,filter:'blur(6px)'},{autoAlpha:1,y:0,filter:'blur(0px)',duration:.3,ease:'power2.out',immediateRender:false});
const hide=id=>gsap.to(id,{autoAlpha:0,y:-12,filter:'blur(8px)',duration:.22,ease:expoIn});
function type(t,id,S){
  gsap.utils.toArray(id+' .w:not(.rdy)').forEach(w=>{
    const at=Math.max(0,+w.dataset.t-S-.07);
    if(w.classList.contains('acc')){ gsap.set(w,{y:0,yPercent:0}); const sp=SplitText.create(w,{type:'chars',mask:'chars',aria:'none'});
      t.fromTo(sp.chars,{yPercent:112},{yPercent:0,duration:.5,ease:expoOut,stagger:.03},at).to(sp.chars,{color:ACC,duration:.3,ease:'power1.out',stagger:.03},at+.12); }
    else t.fromTo(w,{yPercent:112,y:0},{yPercent:0,y:0,duration:.46,ease:expoOut,immediateRender:false},at); });
}
function ringDraw(t,id,at){ t.fromTo(id+' path',{drawSVG:'0%'},{drawSVG:'100%',duration:.8,ease:'power2.inOut',immediateRender:false},at) }
gsap.set('.ring path, .arw path',{drawSVG:'0%'});
const pops=(t,sel,at,each)=>t.fromTo(sel,{autoAlpha:0,y:36,scale:.9},{autoAlpha:1,y:0,scale:1,duration:.55,ease:spring,stagger:each,immediateRender:false},at);
const pulse=(t,sel,at,k,each)=>t.fromTo(sel,{scale:1,transformOrigin:'50% 50%'},{scale:k,duration:.5,yoyo:true,repeat:1,ease:'sine.inOut',stagger:each||0,immediateRender:false},at);
function scr(id,o,fn,opt){ opt=opt||{}; const S=o.t0-.04, t=gsap.timeline(); t.add(show(id),0); type(t,id,S);
  t.to(id+' .ln',{x:8,duration:Math.max(.6,o.end-o.t0-.5),ease:'sine.inOut',stagger:.05},.4);
  if(fn) fn(t,a=>a-S,S); if(!opt.keep) t.add(hide(id),Math.max(.3,o.end-S-.22)); return t; }
/* typed text, slightly varying pace */
function typeChars(t,sel,at,dur){ const el=document.querySelector(sel); const sp=SplitText.create(el,{type:'chars',charsClass:'c',aria:'none'}); const n=sp.chars.length; let w=[],tot=0;
  for(let i=0;i<n;i++){ const v=.7+.6*Math.abs(Math.sin(i*2.3+1)); w.push(v); tot+=v; } let c=at;
  t.set(sp.chars,{opacity:0},Math.max(0,at-.001)); sp.chars.forEach((ch,i)=>{ t.set(ch,{opacity:1},c); c+=dur*w[i]/tot; }); }
const tl=gsap.timeline({paused:true});
tl.fromTo('#cam',{scale:1},{scale:1.014,duration:T.D/4,ease:'sine.inOut',yoyo:true,repeat:3},0)
  .fromTo('.bgw',{x:0,y:0},{x:-14,y:-12,duration:T.D/2,ease:'sine.inOut',yoyo:true,repeat:1},0);
/* S1: complete on frame 0; each bubble then retypes the same sentence (the repeating), the break after "ChatGPT" is a beat */
tl.add((()=>{ const o=T.S1,t=gsap.timeline();
  t.to('#sc1 .hv .w:not(.x)',{color:ACC,duration:.35,ease:'power1.out'},o.again-.05); typeChars(t,'#bub0 span',.12,.7); typeChars(t,'#bub1 span',o.brk,.6); typeChars(t,'#bub2 span',o.again+.3,.6);
  t.fromTo('#cg',{scale:1,transformOrigin:'50% 50%'},{scale:1.06,duration:.5,yoyo:true,repeat:1,ease:'sine.inOut',immediateRender:false},.25)
   .fromTo('#cg',{rotation:0},{rotation:5,duration:1.3,yoyo:true,repeat:2,ease:'sine.inOut',immediateRender:false},1.6)
   .fromTo('#bub1',{scale:1,transformOrigin:'0% 50%'},{scale:1.03,duration:.35,yoyo:true,repeat:1,ease:'sine.inOut',immediateRender:false},o.brk)
   .fromTo('#sc1 .hv .w',{scale:1,transformOrigin:'0% 50%'},{scale:1.07,duration:.4,yoyo:true,repeat:1,ease:'sine.inOut',immediateRender:false},o.again2);
  t.to('#bub0',{x:8,duration:1.6,ease:'sine.inOut',yoyo:true,repeat:1},0);
  t.add(hide('#sc1'),o.end-.24); return t; })(),0);
tl.add(scr('#sc3',T.S3,(t,r)=>{ pops(t,'#ic3',.05,0); pulse(t,'#ic3',.9,1.06); ringDraw(t,'#rgFr',Math.max(1.0,r(T.S3.free)+.35)); t.fromTo('#ic3',{rotation:-4,transformOrigin:'50% 50%'},{rotation:4,duration:1.8,ease:'sine.inOut',immediateRender:false},.2); }),T.S3.t0-.04);
tl.add(scr('#sc4',T.S4,(t,r)=>{ pops(t,'#cg4',.05,0); pops(t,'#ic4',.35,0); t.fromTo('#arw path',{drawSVG:'0%'},{drawSVG:'100%',duration:.6,ease:'power2.inOut',immediateRender:false},.25); pulse(t,'#ic4',1.0,1.07); }),T.S4.t0-.04);
tl.add(scr('#sc5',T.S5,(t,r)=>{ pops(t,'#m5a',Math.max(.05,r(T.S5.claude)-.25),0); pops(t,'#m5b',Math.max(.2,r(T.S5.gem)-.3),0); pulse(t,'#m5a',.7,1.08); pulse(t,'#m5b',.8,1.08); }),T.S5.t0-.04);
/* the card: preview frames play at real speed (15 fps stills of the real preview), then the real Memory screenshot, then the real Actions segment */
const V=T.V, mf=gsap.utils.toArray('.mf'), af=gsap.utils.toArray('.af'); let cur=null;
const setFr=el=>{ if(cur===el) return; if(cur) cur.style.display='none'; cur=el; if(el) el.style.display='block'; };
tl.fromTo('#vc',{autoAlpha:0,y:40},{autoAlpha:1,y:0,duration:.5,ease:spring,immediateRender:false},V.memstart-.04);
const mo={i:0}; tl.fromTo(mo,{i:0},{i:V.nmem-1,duration:(V.nmem-1)/15,ease:'none',onUpdate:()=>setFr(mf[Math.round(mo.i)]),immediateRender:false},V.memstart);
tl.fromTo('#shotm',{opacity:0},{opacity:1,duration:.25,ease:'power1.out',immediateRender:false},V.shot).fromTo('#shotm',{scale:1,transformOrigin:'50% 40%'},{scale:1.05,duration:V.actshow-V.shot,ease:'sine.inOut',immediateRender:false},V.shot)
  .add(()=>{ setFr(null); },V.shot+.26);
tl.set('#shotm',{opacity:0},V.actshow-.0).add(()=>{ document.getElementById('shotm').style.display='none'; },V.actshow-.0);
const ao={i:0}; tl.fromTo(ao,{i:0},{i:V.nact-1,duration:(V.nact-1)/15,ease:'none',onUpdate:()=>setFr(af[Math.round(ao.i)]),immediateRender:false},V.actstart);
tl.to('#vc',{autoAlpha:0,y:-14,filter:'blur(8px)',duration:.22,ease:expoIn},V.end-.24);
tl.add(scr('#sc11',T.S11,(t,r)=>{ pulse(t,'#sc11 .hv',.9,1.05,.15); pulse(t,'#sc11 .hv',1.5,1.04,.15); }),T.S11.t0-.04);
tl.add(scr('#sc12',T.S12,(t,r)=>{ pops(t,'#ic12',.05,0); pulse(t,'#ic12',.9,1.05); t.fromTo('#ic12',{rotation:-3,transformOrigin:'50% 50%'},{rotation:3,duration:1.6,ease:'sine.inOut',immediateRender:false},.2); }),T.S12.t0-.04);
tl.add(scr('#sc13',T.S13,(t,r)=>{ t.fromTo('#adt',{autoAlpha:0},{autoAlpha:1,duration:.3,immediateRender:false},r(T.S13.adat)); pulse(t,'#sc13 .hv',1.0,1.04,.15); },{keep:true}),T.S13.t0-.04);
/* the problem look returns for the loop */
tl.to('#sc13',{autoAlpha:0,filter:'blur(6px)',duration:.1,ease:'power1.in'},T.tF-.1).set('#sc1',{autoAlpha:0},T.tF-.3).fromTo('#sc1',{autoAlpha:0,filter:'blur(6px)'},{autoAlpha:1,filter:'blur(0px)',duration:.16,ease:'power2.out',immediateRender:false},T.tF).to({},{duration:.001},T.D-.001);
window.__timelines=window.__timelines||{}; window.__timelines["main"]=tl; tl.seek(0);
window.__reel={duration:T.D,seek:t=>{tl.seek(t)}};
'''.replace("__T__", json.dumps(T, separators=(",", ":"))).replace("__ACC__", ACC).replace("__INK__", INK)
CDN = "https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/"
html = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="{CDN}gsap.min.js"></script>
<script src="{CDN}SplitText.min.js"></script>
<script src="{CDN}DrawSVGPlugin.min.js"></script>
<script src="{CDN}CustomEase.min.js"></script>
<style>
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Black.otf");font-weight:900}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-ExtraBold.otf");font-weight:800}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Medium.otf");font-weight:500}}
{CSS}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
<div class="bgw" data-decor></div><div id="cam">{scenes}{CARD}</div>
</div>
<script>
{JS}
</script></body></html>'''
os.makedirs(H_ + "/out", exist_ok=True)
open(H_ + "/hf/index.html", "w").write(html)
say(f"ad-ivy build D={D} sfx={len(SFX)} mem={NMEM} act={NACT}")
say("screens: " + "  ".join(f"{k}:{v['t0']:.2f}-{v['end']:.2f}" for k, v in T.items() if isinstance(v, dict) and 't0' in v))
open(H_ + "/out/build-ivy.log", "w").write("\n".join(LOG) + "\n")
