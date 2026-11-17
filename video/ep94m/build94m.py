#!/usr/bin/env python3
"""ep94 'Claude Motion' reel, Miki style (light dotted paper, heavy black Inter Display, hand-drawn UI cut-aways).
Reads voice/narration-raw-cues.json (+ voice/words.json from whisper) -> hf/index.html, sfx94m.json, cues94m.json."""
import json, os, re
H_ = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(H_ + "/voice/narration-raw-cues.json"))
C = C if isinstance(C, list) else C["lines"]
L = {c["n"]: (c["start"], c["end"]) for c in C}
s = lambda n: L[n][0]
e = lambda n: L[n][1]
D = round(e(9) + 1.0, 2)
INK = "#0f0f0f"
J = []; SFX = []
def js(x): J.append(x)
def sfx(f, t, g=-6): SFX.append(dict(f=f, t=round(t, 3), g=g))
def fin(sel, t, d=.4, y=30, blur=14, sc=None):
    sc_ = f",scale:{sc}" if sc else ""
    js(f"tl.fromTo('{sel}',{{opacity:0,y:{y},filter:'blur({blur}px)'{sc_}}},{{opacity:1,y:0,scale:1,filter:'blur(0px)',duration:{d},ease:'power2.out',immediateRender:false}},{max(0,t):.3f});")
def fout(sel, t, d=.3, blur=14, y=-20):
    js(f"tl.to('{sel}',{{opacity:0,y:{y},filter:'blur({blur}px)',duration:{d},ease:'power1.in'}},{max(0,t):.3f});")
try:
    WORDS = json.load(open(H_ + "/voice/words.json"))
except Exception:
    WORDS = []
def W(word, k=0, after=0.0, default=None):
    n = 0
    for w, a, b in WORDS:
        if a >= after and re.sub(r"[^a-z0-9]", "", w.lower()) == word:
            if n == k: return a
            n += 1
    return default
BARS = [38, 62, 48, 86, 70]
def chart(p, h=300, w=760):
    bars = "".join(f'<i class="bar" id="{p}b{i}" style="left:{40+i*140}px;height:{v*h//100}px"></i>' for i, v in enumerate(BARS))
    return f'<div class="chart" id="{p}ch" style="width:{w}px;height:{h}px">{bars}<div class="axis"></div>{"".join(f'<b class="ql" style="left:{40+i*140}px">Q{i+1}</b>' for i in range(5))}</div>'
def sheet(p):
    return (f'<div class="sheet" id="{p}sh"><div class="rt1">QUARTERLY REPORT</div>'
            f'<div class="sl" style="top:84px;width:88%"></div><div class="sl" style="top:114px;width:76%"></div>'
            f'{chart(p, 250, 760)}</div>')
CODE = ["scene = Motion(", '  title="Q3 at a glance",', "  bars=[38, 62, 48, 86, 70],", "  speed=1.0,", ")", "scene.play()"]
code_html = "".join(f'<div class="cl" id="cl{i}">{"".join(f"<span class=L>{c if c!=chr(32) else chr(160)}</span>" for c in t)}</div>' for i, t in enumerate(CODE))
MARK = '<img class="mk" id="{id}" src="assets/claude-mark.svg">'
markup = f'''
<div class="bgw" data-decor></div>
<div id="cam">
 <div id="s1">
  {MARK.format(id="mk1")}
  <div class="h1c" id="h1c">CLAUDE</div><div class="h1n" id="h1n">NOBODY READS<br>YOUR REPORT</div><div class="h1a" id="h1a">REPORT → VIDEO</div>
  <div class="card1" id="card1">{sheet("a")}
   <div class="stamp" id="stamp">UNREAD</div><div class="film" id="film"></div><div class="play" id="play"></div></div>
  <div class="tag" id="tg1" style="top:1180px;left:100px">NEW · CLAUDE MOTION</div>
 </div>
 <div id="s2"><div class="mkbig" id="mkbig">{MARK.format(id="mk2")}</div><div class="h2a" id="h2a">CLAUDE</div><div class="h2b" id="h2b">MOTION</div>
  <div class="tag" id="tg2a" style="top:1150px;left:330px">NEW</div><div class="tag" id="tg2b" style="top:1150px;left:490px">BETA</div></div>
 <div id="s3"><div class="ui" id="ui"><div class="uih"><span class="chip dark" id="chOut">Output ▾ Motion</span><span class="chip" id="chFile">quarterly-report</span></div>
   <div class="typed" id="typed"></div>
   <div class="chips"><span class="chip big" id="cWho">WHO WATCHES</span><span class="chip big" id="cLong">HOW LONG</span></div></div>
  <div class="tag" id="tg3" style="top:1130px;left:100px">EXAMPLE FROM ANTHROPIC'S HELP PAGE</div></div>
 <div id="s4"><div class="card1 c4" id="card4"><div class="mt">Q3 at a glance</div>{chart("d", 330, 760)}<div class="big18" id="n4">+18%</div></div>
  <div class="tag" id="tg4" style="top:1170px;left:100px">ANTHROPIC SAYS · DRAWN EXAMPLE</div></div>
 <div id="s5"><div class="h5a" id="h5a">NO AI</div><div class="h5b" id="h5b">FOOTAGE</div>
  <div class="codep" id="codep"><div class="dots"><i></i><i></i><i></i></div>{code_html}</div>
  <div class="tag" id="tg5" style="top:1170px;left:100px">CODE · STAND-IN EXAMPLE</div></div>
 <div id="s6"><div class="card1 c4" id="card6"><div class="mt">Q3 at a glance</div>{chart("f", 330, 760)}<div class="big18 q" id="n6a">12%</div><div class="big18 q" id="n6b">18%</div>
   <svg class="rings6" viewBox="0 0 880 700"><rect id="rg6" x="560" y="24" width="290" height="140" rx="22" pathLength="1" fill="none" stroke="{INK}" stroke-width="7" stroke-dasharray="1 1" stroke-dashoffset="1"/></svg></div>
  <div class="tag" id="tg6" style="top:1170px;left:100px">ONE NUMBER CHANGES. THE REST STAYS.</div></div>
 <div id="s7"><div class="exp" id="exp">Export</div><div class="cursor" id="cursor"></div><div class="mp4" id="mp4"><b>MP4</b><span>explainer.mp4</span></div></div>
 <div id="s8"><div class="plans" id="plans"><span class="pl" id="pl0">Free</span><span class="pl" id="pl1">Pro</span><span class="pl" id="pl2">Max</span><span class="pl on" id="pl3">Team</span><span class="pl on" id="pl4">Enterprise</span></div>
  <div class="beta" id="beta">BETA</div><div class="tag" id="tg8" style="top:1140px;left:100px">ANTHROPIC SAYS</div></div>
 <div class="tag" id="tgs" style="top:350px;left:740px;z-index:60">SEND THIS</div>
</div>
'''
css = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;font-weight:500;color:{INK}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}}
.bgw{{position:absolute;left:0;top:0;width:1080px;height:1920px;background:#ecebe5 url(assets/bg.jpg);background-size:1080px 1920px}}
#cam{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}}
#s1,#s2,#s3,#s4,#s5,#s6,#s7,#s8{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
#s2,#s3,#s4,#s5,#s6,#s7,#s8,#tgs{{opacity:0}}
.mk{{position:absolute;width:150px;height:150px;left:90px;top:332px}}
.h1c{{position:absolute;left:250px;top:326px;font-size:100px;line-height:100px;font-weight:900;letter-spacing:-.045em;white-space:nowrap}}
.h1a{{position:absolute;left:92px;top:446px;font-size:104px;line-height:104px;font-weight:900;letter-spacing:-.045em;white-space:nowrap;opacity:0}}
.h1n{{position:absolute;left:92px;top:444px;font-size:96px;line-height:98px;font-weight:900;letter-spacing:-.045em;white-space:nowrap}}
.stamp{{position:absolute;left:380px;top:140px;padding:0 26px;height:120px;border:9px solid {INK};border-radius:14px;font-size:84px;line-height:102px;font-weight:900;letter-spacing:-.03em;transform:rotate(-9deg);background:rgba(251,251,248,.92);opacity:0;z-index:5}}
.h1b{{position:absolute;left:260px;top:444px;font-size:112px;line-height:112px;font-weight:900;letter-spacing:-.045em;white-space:nowrap;opacity:.4}}
.card1{{position:absolute;left:100px;top:660px;width:880px;height:510px;background:#fbfbf8;border:4px solid {INK};border-radius:8px;box-shadow:14px 14px 0 {INK};overflow:hidden}}
.sheet{{position:absolute;left:50px;top:26px;width:780px;height:458px}}
.rt1{{position:absolute;left:0;top:18px;font:700 36px/40px JBM,monospace;letter-spacing:.06em}}
.sl{{position:absolute;left:0;height:14px;border-radius:7px;background:#d4d4d8}}
.chart{{position:absolute;left:10px;bottom:60px}}
.bar{{position:absolute;bottom:0;width:90px;background:{INK};border-radius:6px 6px 0 0;transform-origin:50% 100%}}
.ql{{position:absolute;bottom:-52px;width:90px;text-align:center;font:700 30px/34px JBM,monospace}}
.axis{{position:absolute;left:0;right:0;bottom:-6px;height:6px;background:{INK};border-radius:3px}}
.film{{position:absolute;left:14px;top:14px;right:14px;bottom:14px;border:10px solid {INK};border-radius:12px;opacity:0}}
.play{{position:absolute;left:350px;top:190px;width:0;height:0;border-left:140px solid {INK};border-top:90px solid transparent;border-bottom:90px solid transparent;opacity:0}}
.mkbig{{position:absolute;left:340px;top:330px;width:400px;height:400px}} .mkbig .mk{{left:0;top:0;width:400px;height:400px}}
.h2a{{position:absolute;left:100px;width:880px;text-align:center;top:770px;font-size:160px;line-height:160px;font-weight:900;letter-spacing:-.05em}}
.h2b{{position:absolute;left:100px;width:880px;text-align:center;top:935px;font-size:160px;line-height:160px;font-weight:900;letter-spacing:-.05em}}
.ui{{position:absolute;left:100px;top:420px;width:880px;height:640px;background:#fff;border:4px solid {INK};border-radius:28px;box-shadow:14px 14px 0 {INK}}}
.uih{{position:absolute;left:34px;top:30px;display:flex;gap:16px}}
.chip{{display:inline-block;height:56px;padding:0 24px;border:4px solid {INK};border-radius:28px;font:700 30px/48px JBM,monospace;background:#fbfbf8;white-space:nowrap}}
.chip.dark{{background:{INK};color:#fff}} .chip.big{{height:78px;font-size:38px;line-height:70px;padding:0 30px;border-radius:39px;border-style:dashed}} .chip.lit{{border-style:solid;background:{INK};color:#fff}}
.typed{{position:absolute;left:44px;top:130px;width:790px;font-size:62px;line-height:72px;font-weight:500;letter-spacing:-.02em}}
.chips{{position:absolute;left:34px;bottom:34px;display:flex;gap:18px}}
.tag{{position:absolute;height:64px;padding:0 26px;background:{INK};color:#fff;font:700 34px/64px JBM,monospace;letter-spacing:.05em;border-radius:6px;white-space:nowrap;opacity:0}}
.c4{{top:330px;height:790px}} .mt{{position:absolute;left:50px;top:36px;font-size:70px;line-height:70px;font-weight:900;letter-spacing:-.04em}}
.c4 .chart{{left:50px;bottom:40px}}
.big18{{position:absolute;right:50px;top:30px;font-size:130px;line-height:130px;font-weight:900;letter-spacing:-.05em;opacity:0}} .big18.q{{opacity:0}}
.rings6{{position:absolute;left:0;top:0;width:880px;height:790px;overflow:visible}}
.h5a{{position:absolute;left:75px;top:300px;font-size:170px;line-height:170px;font-weight:900;letter-spacing:-.05em;white-space:nowrap;opacity:0}}
.h5b{{position:absolute;left:75px;top:470px;font-size:170px;line-height:170px;font-weight:900;letter-spacing:-.05em;white-space:nowrap;opacity:0}}
.codep{{position:absolute;left:100px;top:700px;width:880px;height:440px;background:{INK};border-radius:14px;box-shadow:14px 14px 0 #8a8a86;padding:30px 40px;color:#fff;font:700 38px/58px JBM,monospace;opacity:0}}
.dots{{position:absolute;right:30px;top:20px}} .dots i{{display:inline-block;width:18px;height:18px;border-radius:50%;background:#555;margin-left:10px}}
.cl{{white-space:nowrap;margin-top:0}} .cl:first-of-type{{margin-top:34px}} .L{{opacity:0}}
.exp{{position:absolute;left:290px;top:560px;width:500px;height:150px;border:6px solid {INK};border-radius:28px;background:#fbfbf8;box-shadow:12px 12px 0 {INK};font-size:84px;line-height:138px;text-align:center;font-weight:900;letter-spacing:-.03em;opacity:0}}
.cursor{{position:absolute;left:560px;top:690px;width:0;height:0;border-left:30px solid {INK};border-top:22px solid transparent;border-bottom:22px solid transparent;transform:rotate(-30deg);opacity:0}}
.mp4{{position:absolute;left:230px;top:820px;width:620px;height:300px;border:5px solid {INK};border-radius:16px;background:#fff;box-shadow:12px 12px 0 {INK};opacity:0}}
.mp4 b{{position:absolute;left:34px;top:24px;font-size:150px;line-height:150px;font-weight:900;letter-spacing:-.05em}} .mp4 span{{position:absolute;left:38px;bottom:30px;font:700 36px/40px JBM,monospace;color:#55565c}}
.plans{{position:absolute;left:100px;top:420px;width:880px;display:flex;flex-direction:column;gap:18px}}
.pl{{display:block;height:110px;border:6px dashed #9a9a96;border-radius:70px;font-size:64px;line-height:98px;text-align:center;font-weight:900;letter-spacing:-.03em;color:#9a9a96;opacity:0}}
.pl.on{{border:6px solid {INK};background:{INK};color:#fff}}
.beta{{position:absolute;left:700px;top:300px;height:90px;padding:0 34px;border:6px solid {INK};border-radius:45px;font:700 48px/78px JBM,monospace;opacity:0;transform:rotate(-6deg);background:#fbfbf8}}
'''
t_report = W("report", 0, default=1.0); t_video = W("video", 0, default=1.8)
t_motion = W("motion", 0, default=s(2) + .6); t_new = W("new", 0, after=s(2), default=s(2) + 1.4)
t_watch = W("watching", 0, after=s(3), default=s(3) + 1.8); t_long = W("long", 0, after=t_watch, default=s(3) + 2.8)
t_anim = W("animation", 0, after=s(4), default=s(4) + 1.0)
t_nofoot = W("footage", 0, after=s(5), default=s(5) + .8); t_code = W("code", 0, after=t_nofoot, default=s(5) + 2.4)
t_word = W("word", 0, after=s(6), default=s(6) + 1.2); t_stays = W("stays", 0, after=t_word, default=s(6) + 2.4)
t_exp = W("export", 0, after=s(7), default=s(7) + .5); t_mp4 = W("mp4", 0, after=t_exp, default=s(7) + 1.4)
t_beta = W("beta", 0, after=s(8), default=s(8) + .2); t_team = W("team", 0, after=t_beta, default=s(8) + 1.0); t_ent = W("enterprise", 0, after=t_team, default=s(8) + 1.6)
t_hav = t_ent + .35; t_says = t_hav
# ---------------------------------------------------------------- timeline
js(f"tl.fromTo('#cam',{{scale:1.0,y:0}},{{scale:1.03,y:-12,duration:{D},ease:'sine.inOut'}},0);")
def pulse_bars(p, t0, t1, amp=.22):
    for i in range(5):
        t = t0 + .12 * i
        while t < t1 - .4:
            js(f"tl.to('#{p}b{i}',{{scaleY:{1-amp-0.05*i:.2f},duration:.9,ease:'sine.inOut',yoyo:true,repeat:1,transformOrigin:'50% 100%'}},{t:.3f});")
            t += 1.8
# S1 hook: report sheet with live bars -> film frame + play. Mark + REPORT -> VIDEO.
js("gsap.set('#film,#play',{opacity:0});")
for i in range(5):
    js(f"tl.fromTo('#ab{i}',{{scaleY:.05}},{{scaleY:1,duration:.8,ease:'power2.out',transformOrigin:'50% 100%',immediateRender:false}},{.12+i*.09:.3f});")
pulse_bars("a", 1.0, s(2))
js(f"tl.fromTo('#mk1',{{rotate:-25}},{{rotate:0,duration:.7,ease:'sine.out',immediateRender:false}},0);")
js(f"tl.fromTo('#h1c',{{x:-18}},{{x:0,duration:.5,ease:'power2.out',immediateRender:false}},0);")
js(f"tl.fromTo('#stamp',{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:.18,ease:'expo.out',immediateRender:false}},{max(.45,t_report+.05):.3f});")
js(f"tl.to('#stamp',{{opacity:0,scale:.92,duration:.2,ease:'power1.in'}},{t_video-.12:.3f});")
js(f"tl.to('#h1n',{{opacity:0,y:-14,filter:'blur(8px)',duration:.22,ease:'power1.in'}},{t_video-.18:.3f});tl.fromTo('#h1a',{{opacity:0,y:16,filter:'blur(8px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:.3,ease:'power2.out',immediateRender:false}},{t_video-.02:.3f});")
sfx("impactpunch.ogg", max(.45,t_report+.05)+.04, -6)
js(f"tl.to('#film',{{opacity:1,duration:.4,ease:'sine.out'}},{t_video-.05:.3f});tl.to('#ash .sl',{{opacity:.0,duration:.3}},{t_video:.3f});tl.to('#play',{{opacity:1,duration:.35,ease:'sine.out'}},{t_video+.12:.3f});")
js("gsap.set('#tg1',{opacity:0});")
fin("#tg1", t_video + .35, .35, 14, 6)
sfx("pop_a.ogg", .2, -8); sfx("impactsoft.ogg", t_report, -7); sfx("pop_b.ogg", t_video + .1, -7)
fout("#s1", s(2) - .08, .3)
# S2 Claude Motion
js("gsap.set('#s2',{opacity:1}); gsap.set('#mkbig,#h2a,#h2b,#tg2a,#tg2b',{opacity:0});")
fin("#mkbig", s(2) + .02, .5, 30, 10, .9)
js(f"tl.to('#mk2',{{rotate:360,duration:{e(2)-s(2)+.2:.2f},ease:'sine.inOut'}},{s(2):.3f});")
fin("#h2a", s(2) + .12, .35, 24, 8); fin("#h2b", t_motion - .05, .4, 24, 8); sfx("impactsoft.ogg", t_motion, -5)
fin("#tg2a", t_new - .05, .3, 14, 6); fin("#tg2b", t_new + .15, .3, 14, 6); sfx("tick.ogg", t_new, -8)
fout("#s2", s(3) - .08, .3)
# S3 the message box: typed example, chips light with the spoken words
js("gsap.set('#s3',{opacity:1}); gsap.set('#ui,#tg3,#chOut,#chFile,#typed,#cWho,#cLong',{opacity:0});")
fin("#ui", s(3) + .02, .45, 40, 12, .97); sfx("whoosh_b.ogg", s(3) - .04, -9)
fin("#chOut", s(3) + .3, .3, 14, 6); fin("#chFile", s(3) + .45, .3, 14, 6); sfx("pop_a.ogg", s(3) + .35, -9)
TXT = "Turn this quarterly report into a 30-second explainer for our all-hands."
js(f"gsap.set('#typed',{{opacity:1}}); (function(){{var el=document.getElementById('typed');el.innerHTML='';var sp=[];for(var i=0;i<{len(TXT)};i++){{var q=document.createElement('span');q.textContent={json.dumps(TXT)}[i];q.style.opacity=0;el.appendChild(q);sp.push(q);}}window.__sp=sp;}})();")
t0 = s(3) + .7; tn = max(1.6, (t_watch - t0) - .1)
js(f"tl.to(window.__sp,{{opacity:1,duration:.02,stagger:{tn/len(TXT):.4f}}},{t0:.3f});")
fin("#cWho", t_watch - .3, .3, 14, 6); fin("#cLong", t_long - .25, .3, 14, 6)
js(f"tl.to('#cWho',{{backgroundColor:'#0f0f0f',color:'#fff',borderStyle:'solid',duration:.25}},{t_watch:.3f});tl.to('#cLong',{{backgroundColor:'#0f0f0f',color:'#fff',borderStyle:'solid',duration:.25}},{t_long:.3f});")
sfx("tick.ogg", t_watch, -7); sfx("tick.ogg", t_long, -7)
fin("#tg3", s(3) + 1.0, .35, 14, 6)
fout("#s3", s(4) - .08, .3)
# S4 the animation plays
js("gsap.set('#s4',{opacity:1}); gsap.set('#card4,#tg4,#n4',{opacity:0});")
fin("#card4", s(4) + .02, .45, 40, 12, .97); sfx("whoosh_a.ogg", s(4) - .04, -9)
for i in range(5):
    js(f"tl.fromTo('#db{i}',{{scaleY:.05}},{{scaleY:1,duration:.9,ease:'power2.out',transformOrigin:'50% 100%',immediateRender:false}},{s(4)+.45+i*.12:.3f});")
fin("#n4", t_anim + .3, .45, 20, 8, .9); sfx("pop_b.ogg", t_anim + .35, -7)
pulse_bars("d", s(4) + 1.6, s(5))
fin("#tg4", s(4) + .8, .35, 14, 6)
fout("#s4", s(5) - .08, .3)
# S5 no AI footage = code
js("gsap.set('#s5',{opacity:1}); gsap.set('#h5a,#h5b,#codep,#tg5',{opacity:0});")
fin("#h5a", s(5) + .02, .35, 24, 8); fin("#h5b", t_nofoot - .12, .4, 24, 8); sfx("impactsoft.ogg", t_nofoot - .05, -5)
fin("#codep", s(5) + .5, .45, 30, 10)
n = 0
for i, tline in enumerate(CODE):
    for j in range(len(tline)):
        tj = t_code - .5 + n * .028 + (0 if j else .05 * i)
        js(f"tl.to('#cl{i} .L:nth-child({j+1})',{{opacity:1,duration:.02}},{tj:.3f});"); n += 1
for k in range(0, 18, 3): sfx("click_a.ogg" if k % 2 == 0 else "click_b.ogg", t_code - .5 + k * .09, -14)
fin("#tg5", s(5) + 1.3, .35, 14, 6)
fout("#s5", s(6) - .08, .3)
# S6 change one word / number
js("gsap.set('#s6',{opacity:1}); gsap.set('#card6,#tg6,#n6a,#n6b',{opacity:0});")
fin("#card6", s(6) + .02, .45, 40, 12, .97); sfx("whoosh_a.ogg", s(6) - .04, -9)
fin("#n6a", s(6) + .5, .4, 20, 8, .92)
js(f"tl.to('#rg6',{{strokeDashoffset:0,duration:.5,ease:'sine.inOut'}},{t_word-.1:.3f});")
js(f"tl.to('#n6a',{{opacity:0,y:-24,filter:'blur(8px)',duration:.25,ease:'power1.in'}},{t_word+.2:.3f});tl.fromTo('#n6b',{{opacity:0,y:24,filter:'blur(8px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:.35,ease:'power2.out',immediateRender:false}},{t_word+.3:.3f});")
sfx("tick.ogg", t_word + .1, -7); sfx("pop_b.ogg", t_word + .35, -6)
pulse_bars("f", s(6) + .5, s(7), .12)
fin("#tg6", t_stays - .5, .35, 14, 6)
fout("#s6", s(7) - .08, .3)
# S7 export -> MP4
js("gsap.set('#s7',{opacity:1}); gsap.set('#exp,#cursor,#mp4',{opacity:0});")
fin("#exp", t_exp - .35, .4, 26, 8); sfx("pop_a.ogg", t_exp - .3, -8)
js(f"tl.fromTo('#cursor',{{opacity:0,x:180,y:180}},{{opacity:1,x:0,y:0,duration:.5,ease:'sine.inOut',immediateRender:false}},{t_exp:.3f});")
js(f"tl.to('#exp',{{scale:.94,duration:.1,ease:'sine.inOut',yoyo:true,repeat:1}},{t_exp+.55:.3f});")
sfx("click_a.ogg", t_exp + .58, -6)
fin("#mp4", t_mp4 - .05, .45, 50, 12, .96); sfx("ding.ogg", t_mp4 + .1, -9)
fout("#s7", s(8) - .08, .3)
# S8 plans
js("gsap.set('#s8',{opacity:1}); gsap.set('#plans .pl,#beta,#tg8',{opacity:0});")
for i in range(5):
    fin(f"#pl{i}", s(8) + .05 + i * .1, .3, 20, 6)
js(f"tl.fromTo('#pl3',{{scale:1}},{{scale:1.04,duration:.25,ease:'sine.out',yoyo:true,repeat:1}},{t_team:.3f});tl.fromTo('#pl4',{{scale:1}},{{scale:1.04,duration:.25,ease:'sine.out',yoyo:true,repeat:1}},{t_ent:.3f});")
sfx("tick.ogg", t_team, -7); sfx("tick.ogg", t_ent, -7)
fin("#beta", t_beta - .05, .35, 14, 6, .8); sfx("pop_b.ogg", t_beta, -8)
fin("#tg8", t_hav - .1, .35, 14, 6)
fout("#s8", s(9) - .1, .3)
# S9 loop: back to hook frame
js(f"tl.fromTo('#s1',{{opacity:0,filter:'blur(14px)'}},{{opacity:1,filter:'blur(0px)',duration:.4,ease:'power2.out',immediateRender:false}},{s(9)-.02:.3f});")
js(f"tl.set('#tg1',{{opacity:0}},{s(9)-.02:.3f});")
fin("#tgs", s(9) + .3, .3, 14, 6); sfx("whoosh_c.ogg", s(9) - .05, -10)
JS = "\n".join(J)
json.dump(SFX, open(H_ + "/sfx94m.json", "w"), indent=1)
json.dump(dict(lines=[dict(n=c["n"], text=c["line"], start=c["start"], end=c["end"]) for c in C], D=D), open(H_ + "/cues94m.json", "w"), indent=1)
html = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Black.otf");font-weight:900}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Medium.otf");font-weight:500}}
@font-face{{font-family:"JBM";src:url("assets/fonts/JetBrainsMono-Bold.ttf");font-weight:700}}
{css}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
{markup}
</div>
<script>
const D={D}; const tl=gsap.timeline({{paused:true}});
{JS}
tl.to({{}},{{duration:.001}},D-.001);
window.__timelines=window.__timelines||{{}}; window.__timelines["main"]=tl; tl.seek(0);
window.__reel={{duration:D,seek:t=>tl.seek(t)}};
</script></body></html>'''
open(H_ + "/hf/index.html", "w").write(html)
print("D=", D, "sfx", len(SFX), "js", len(J))
