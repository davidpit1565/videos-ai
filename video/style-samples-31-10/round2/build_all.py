import os, subprocess
from gen import *
from PIL import Image, ImageDraw
def mask(w,h,r,p):
    m=Image.new("L",(w,h),0); ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),r,fill=255); m.save(p)
mask(884,400,32,"/tmp/m3.png");mask(884,724,32,"/tmp/m1.png"); mask(434,584,32,"/tmp/m2.png")
def win(i,x,y,w,h,s,d): return f'<div class="abs win clip" id="w{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px" data-start="{s}" data-duration="{d}" data-track-index="__TR__"></div>'
# ---------- V1
b=title_scene(4.7)+spike(1,-380,1600)
b+=f'<div class="abs lab clip" id="l1" style="left:90px;top:262px" data-start="4.6" data-duration="10.4" data-track-index="__TR__">#1 <span id="ls1" style="opacity:0">The proof</span></div>'
b+=win(1,90,420,900,740,4.6,10.4)
b+='<div class="abs tag clip" id="tg1" style="left:90px;top:1180px;background:var(--red)" data-start="8.4" data-duration="6.6" data-track-index="__TR__">IT SAID YES. IT WAS WRONG!</div>'
j='''words("#t1",0.5,0.38,true);tl.fromTo("#t2 .w",{opacity:0,y:30},{opacity:1,y:0,duration:.3,ease:"power3.out"},3.0);
wipe("#sp1",0,0,150,-260,3.9,40);
tl.fromTo("#l1",{opacity:0,y:30},{opacity:1,y:0,duration:.3},4.65);scramble(document.getElementById("ls1"),"The proof",4.7,.55);
tl.fromTo("#w1",{opacity:0,scale:.92},{opacity:1,scale:1,duration:.4,ease:"back.out(1.5)"},4.7);
tagIn("#tg1",8.5,-3);
'''
build("1proof",15,b,j,None)
# ---------- V2
b=title_scene(4.7)+spike(1,-380,1600)
b+='<div class="abs chip clip" id="c1" style="left:90px;top:285px" data-start="4.6" data-duration="10.4" data-track-index="__TR__">WITHOUT THE SETTING</div><div class="abs chip clip" id="c2" style="left:90px;top:775px;background:var(--acc)" data-start="4.6" data-duration="10.4" data-track-index="__TR__">WITH THE SETTING</div>'
b+=win(1,90,340,900,416,4.6,10.4)+win(2,90,830,900,416,4.6,10.4)
b+='<div class="abs tag clip" id="tg1" style="left:680px;top:270px;background:var(--red);font-size:42px" data-start="8.0" data-duration="7" data-track-index="__TR__">SAID YES</div><div class="abs tag clip" id="tg2" style="left:700px;top:760px;background:var(--green);font-size:42px" data-start="8.6" data-duration="6.4" data-track-index="__TR__">SAID NO</div>'
j='''words("#t1",0.5,0.38,true);tl.fromTo("#t2 .w",{opacity:0,y:30},{opacity:1,y:0,duration:.3,ease:"power3.out"},3.0);
wipe("#sp1",0,0,150,-260,3.9,40);
tl.fromTo(["#c1","#c2"],{opacity:0,y:20},{opacity:1,y:0,duration:.3},4.9);
tl.fromTo("#w1",{opacity:0,x:-80},{opacity:1,x:0,duration:.4,ease:"power3.out"},4.8);tl.fromTo("#w2",{opacity:0,x:80},{opacity:1,x:0,duration:.4,ease:"power3.out"},4.9);
tagIn("#tg1",8.1,-3);tagIn("#tg2",8.7,3);
'''
build("2split",15,b,j,None)
# ---------- V3
b=title_scene(3.6)+spike(1,-380,1600)+spike(2,760,-380)+spike(3,-380,1600)
b+=f'<div class="abs lab clip" id="l1" style="left:90px;top:262px" data-start="3.5" data-duration="5.4" data-track-index="__TR__">#1 <span id="ls1" style="opacity:0">The proof</span></div>'
b+=win(1,90,420,900,740,3.5,5.4)
b+='<div class="abs tag clip" id="tg1" style="left:90px;top:1180px;background:var(--red)" data-start="7.3" data-duration="1.6" data-track-index="__TR__">IT SAID YES. IT WAS WRONG!</div>'
b+=f'<div class="abs lab clip" id="l2" style="left:90px;top:262px" data-start="8.8" data-duration="5.5" data-track-index="__TR__">#2 <span id="ls2" style="opacity:0">The fix</span></div>'
b+='<div class="abs card clip" id="cd" style="left:90px;top:440px;width:900px;min-height:420px" data-start="8.8" data-duration="5.5" data-track-index="__TR__"><div class="chip">Custom instructions</div><br><span id="ty"></span><span class="cur"></span></div>'
b+='<div class="abs keys clip" id="ks" style="top:960px" data-start="8.8" data-duration="5.5" data-track-index="__TR__"><div class="key">Settings</div><div class="arr">→</div><div class="key">Personalization</div><div class="arr">→</div><div class="key">Custom instructions</div></div>'
b+=f'<div class="abs lab clip" id="l3" style="left:90px;top:262px" data-start="14.2" data-duration="5.4" data-track-index="__TR__">#3 <span id="ls3" style="opacity:0">The result</span></div>'
b+=win(2,90,420,900,740,14.2,5.4)
b+='<div class="abs tag clip" id="tg2" style="left:90px;top:1180px;background:var(--green)" data-start="17.5" data-duration="2.1" data-track-index="__TR__">IT SAID NO!</div>'
j='''words("#t1",0.5,0.38,true);tl.fromTo("#t2 .w",{opacity:0,y:30},{opacity:1,y:0,duration:.3,ease:"power3.out"},2.4);
wipe("#sp1",0,0,150,-260,2.9,40);
tl.fromTo("#l1",{opacity:0,y:30},{opacity:1,y:0,duration:.3},3.55);scramble(document.getElementById("ls1"),"The proof",3.6,.5);
tl.fromTo("#w1",{opacity:0,scale:.92},{opacity:1,scale:1,duration:.4,ease:"back.out(1.5)"},3.6);
tagIn("#tg1",7.4,-3);
wipe("#sp2",0,0,-150,260,8.2,-40);
tl.fromTo("#l2",{opacity:0,y:30},{opacity:1,y:0,duration:.3},8.85);scramble(document.getElementById("ls2"),"The fix",8.9,.5);
tl.fromTo("#cd",{opacity:0,y:100,scale:.94},{opacity:1,y:0,scale:1,duration:.5,ease:"back.out(1.5)"},8.95);
const txt="Be honest, not agreeable. Never agree with me just to please me, or because I sound sure.";const o={n:0};
tl.to(o,{n:txt.length,duration:2.6,ease:"none",onUpdate(){document.getElementById("ty").textContent=txt.slice(0,Math.round(o.n))}},9.5);
document.querySelectorAll("#ks .key,#ks .arr").forEach((k,i)=>tl.fromTo(k,{opacity:0,y:30,scale:.8},{opacity:1,y:0,scale:1,duration:.3,ease:"back.out(2)"},11.3+i*.25));
wipe("#sp3",0,0,150,-260,13.5,40);
tl.fromTo("#l3",{opacity:0,y:30},{opacity:1,y:0,duration:.3},14.25);scramble(document.getElementById("ls3"),"The result",14.3,.55);
tl.fromTo("#w2",{opacity:0,scale:.92},{opacity:1,scale:1,duration:.4,ease:"back.out(1.5)"},14.3);
tagIn("#tg2",17.6,3);
'''
build("3list",19.6,b,j,None)
