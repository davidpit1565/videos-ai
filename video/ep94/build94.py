#!/usr/bin/env python3
"""ep94 first 2.5 s, hook C "Flagged as AI. Your own essay." - Miki style (paper + dotted grid, heavy black type, black stamp).
Picture-only first cut: word times below are ESTIMATES until the voice is rendered (then edit WT). Writes hf/index.html."""
import os
H_ = os.path.dirname(os.path.abspath(__file__))
D = 2.5
INK = "#0f0f0f"
# spoken word times (estimates): Flagged .10-.50, as .50-.62, AI .62-.90, Your 1.00-1.20, own 1.20-1.45, essay 1.45-1.90
WT = dict(stamp=.10, your=1.00, own=1.20, essay=1.45)
css = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#ecebe5;font-family:IDisp,Inter,Helvetica,Arial,sans-serif;font-weight:500;color:{INK}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#ecebe5}}
.bgw{{position:absolute;left:0;top:0;width:1080px;height:1920px;background:#ecebe5 url(assets/bg.jpg);background-size:1080px 1920px}}
#cam{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 760px}}
.hd{{position:absolute;left:65px;top:290px;width:950px;font-size:176px;line-height:176px;font-weight:900;letter-spacing:-.045em;white-space:nowrap}}
.hd .w{{display:inline-block;margin-right:34px}} .hd .br{{display:block;height:0}}
.hd .ul{{position:absolute;left:0;top:326px;width:620px;height:40px}}
.sheet{{position:absolute;left:110px;top:760px;width:860px;height:470px;background:#fbfbf8;border:4px solid {INK};border-radius:6px;box-shadow:14px 14px 0 {INK}}}
.ln{{position:absolute;left:60px;height:30px;border-radius:15px;background:#d4d4d8;filter:blur(6px)}}
.stamp{{position:absolute;left:100px;top:890px;width:880px;height:230px;border:14px solid {INK};border-radius:14px;background:rgba(251,251,248,.0);display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(-7deg);opacity:0}}
.stamp b{{font-size:106px;line-height:110px;font-weight:900;letter-spacing:-.04em;white-space:nowrap}}
.stamp i{{position:absolute;left:-14px;top:-62px;height:56px;padding:0 24px;background:{INK};color:#fff;font:700 34px/56px JBM,monospace;letter-spacing:.06em;font-style:normal;border-radius:6px}}
'''
html = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Black.otf");font-weight:900}}
@font-face{{font-family:"IDisp";src:url("assets/fonts/InterDisplay-Medium.otf");font-weight:500}}
@font-face{{font-family:"JBM";src:url("assets/fonts/JetBrainsMono-Bold.ttf");font-weight:700}}
{css}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
<div class="bgw" data-decor></div>
<div id="cam">
 <div class="hd" id="hd"><span class="w" id="w1">YOUR</span><span class="w" id="w2">OWN</span><span class="br"></span><span class="w" id="w3">ESSAY</span>
  <svg class="ul" viewBox="0 0 620 40" preserveAspectRatio="none"><path id="ulp" d="M6 24 C 100 6, 200 34, 320 18 S 520 8, 614 20" pathLength="1" stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round" stroke-dasharray="1 1" stroke-dashoffset="1"/></svg></div>
 <div class="sheet" id="sheet">
  <div class="ln" style="top:50px;width:420px"></div><div class="ln" style="top:110px;width:700px"></div><div class="ln" style="top:170px;width:640px"></div>
  <div class="ln" style="top:330px;width:690px"></div><div class="ln" style="top:390px;width:520px"></div>
 </div>
 <div class="stamp" id="stamp"><i>AI DETECTOR</i><b>FLAGGED AS AI</b></div>
</div>
</div>
<script>
const D={D}; const tl=gsap.timeline({{paused:true}});
// whole picture drifts slowly the whole time (never still)
tl.fromTo('#cam',{{scale:1.0,y:0}},{{scale:1.035,y:-14,duration:D,ease:'sine.inOut'}},0);
// frame 0 already shows the subject: heading + sheet. Words go from grey to black as they are spoken (ghost -> ink).

// only the stamp moves first: drops, lands, the sheet shudders once
tl.fromTo('#stamp',{{opacity:0,y:-520,scale:1.25}},{{opacity:1,y:0,scale:1,duration:.34,ease:'expo.out'}},{WT['stamp']});
tl.to('#sheet',{{x:-7,duration:.06,ease:'sine.out'}},{WT['stamp']+.34});
tl.to('#sheet',{{x:5,duration:.1,ease:'sine.inOut'}},{WT['stamp']+.40});
tl.to('#sheet',{{x:0,duration:.18,ease:'sine.out'}},{WT['stamp']+.50});
// underline draws under the heading while "essay" is said
tl.to('#ulp',{{strokeDashoffset:0,duration:.5,ease:'sine.inOut'}},{WT['essay']});
tl.to({{}},{{duration:.001}},D-.001);
window.__timelines=window.__timelines||{{}}; window.__timelines["main"]=tl; tl.seek(0);
window.__reel={{duration:D,seek:t=>tl.seek(t)}};
</script></body></html>'''
open(H_ + "/hf/index.html", "w").write(html)
print("ok D=", D)
