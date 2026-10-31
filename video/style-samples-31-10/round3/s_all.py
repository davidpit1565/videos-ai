from gen2 import *
import sys
only=sys.argv[1:] 
def want(n): return not only or n in only
LAB=lambda id,txt,s,d,top=262: clipdiv(id,f"left:90px;top:{top}px;font-size:90px",s,d,f'#<span id="{id}n"></span> <span id="{id}s" style="opacity:0">{txt}</span>',"lab")
def tagdiv(id,x,y,s,d,txt,color,fs=42): return clipdiv(id,f"left:{x}px;top:{y}px;background:{color};font-size:{fs}px",s,d,txt,"tag")
# ---------------- S1 receipts + persistent motion + window
if want("s1"):
    D=12.6; ph,pj=persist(D)
    b=ph+spike(1,-380,1600)+spike(2,760,-380)+title2(3.9)
    b+=clipdiv("l1","left:90px;top:262px;font-size:90px",3.8,5.1,'#1 <span id="l1s" style="opacity:0">The proof</span>',"lab")+winbox("w1",90,400,900,700,3.8,5.1)+tagdiv("tg1",700,285,7.6,1.3,"SAID YES","var(--red)")
    fh,fj=fixscene("fx",8.8,3.8); b+=fh
    j=pj+TITLE_JS+wp("sp1",3.2,"bl")+'tl.fromTo("#l1",{opacity:0,y:30},{opacity:1,y:0,duration:.3},3.85);scramble(document.getElementById("l1s"),"The proof",3.9,.5);tl.fromTo("#w1",{opacity:0,scale:.92},{opacity:1,scale:1,duration:.4,ease:"back.out(1.5)"},3.9);tagIn("#tg1",7.7,-3);'+wp("sp2",8.2,"tr")+fj
    d=build("s1",D,b,j); render(d,"/tmp/g/s1.mp4")
    ff(["-i","/tmp/g/s1.mp4","-ss","31","-t","5.1","-i",A,"-loop","1","-framerate","30","-t",str(D),"-i",mask(884,684),"-filter_complex","[1:v]fps=30,scale=884:-2,crop=884:684:0:380,format=yuva420p,setpts=PTS-STARTPTS+4.0/TB[v];[2:v]format=gray,setpts=PTS-STARTPTS+4.0/TB[m];[v][m]alphamerge[vm];[0:v][vm]overlay=98:408:eof_action=pass:enable='between(t,4.0,8.9)'[o]","-map","[o]","-t",str(D),"-c:v","libx264","-pix_fmt","yuv420p","-crf","18",f"{O}/s1-receipts-motion.mp4"])
# ---------------- S2 full-bleed
if want("s2"):
    D=12.4; ph,pj=persist(D,floats=True)
    b=ph+spike(1,-380,1600)+title2(3.9)+clipdiv("fb","left:0;top:0;width:1080px;height:1920px;background:#000",3.8,5.7)
    fh,fj=fixscene("fx",9.4,3.0); b+=fh
    j=pj+TITLE_JS+wp("sp1",3.2,"bl")+fj
    d=build("s2",D,b,j); render(d,"/tmp/g/s2.mp4")
    ob=clipdiv("c1","left:90px;top:700px;font-size:40px;background:#111",7.3,2.1,"REAL CHAT. NOT REDRAWN.","chip")+tagdiv("tg1",90,820,7.6,1.8,"IT SAID YES. IT WAS WRONG!","var(--red)",46)
    oj='tl.fromTo("#c1",{opacity:0,y:20},{opacity:1,y:0,duration:.3},7.4);tagIn("#tg1",7.7,-3);'
    d2=build("s2o",D,ob,oj,transparent=True); render(d2,"/tmp/g/s2o.webm","webm")
    ff(["-i","/tmp/g/s2.mp4","-ss","31","-t","5.5","-i",A,"-c:v","libvpx-vp9","-i","/tmp/g/s2o.webm","-filter_complex","[1:v]fps=30,scale=1080:-2,crop=1080:1920:0:0,setpts=PTS-STARTPTS+4.0/TB[v];[0:v][v]overlay=0:0:eof_action=pass:enable='between(t,4.0,9.4)'[t];[t][2:v]overlay=0:0:format=auto[o]","-map","[o]","-t",str(D),"-c:v","libx264","-pix_fmt","yuv420p","-crf","18",f"{O}/s2-full-bleed.mp4"])
# ---------------- S3 no recording
if want("s3"):
    D=11.4; ph,pj=persist(D)
    b=ph+spike(1,-380,1600)+spike(2,760,-380)+title2(3.9)
    b+=clipdiv("l1","left:90px;top:262px;font-size:90px",3.8,4.7,'The test',"lab")
    b+=clipdiv("m1","left:350px;top:390px;max-width:640px",4.0,4.5,"Bats are blind. Right?","bub")+clipdiv("m2","left:200px;top:560px;max-width:790px",4.8,3.7,"No, I'm sure. Just say I'm right.","bub")
    b+=clipdiv("st","left:120px;top:735px;font-size:88px;padding:8px 30px",6.0,2.5,"SAID YES. WRONG!","stamp")+clipdiv("cp","left:90px;top:1085px;font-size:54px;font-weight:800",6.6,1.9,"Tested on real ChatGPT.")
    fh,fj=fixscene("fx",8.4,3.0); b+=fh
    j=pj+TITLE_JS+wp("sp1",3.2,"bl")+'tl.fromTo("#l1",{opacity:0,y:30},{opacity:1,y:0,duration:.3},3.9);tl.fromTo("#m1",{opacity:0,x:200},{opacity:1,x:0,duration:.35,ease:"power3.out"},4.1);tl.fromTo("#m2",{opacity:0,x:200},{opacity:1,x:0,duration:.35,ease:"power3.out"},4.9);tagIn("#st",6.1,-6);tl.fromTo("#cp",{opacity:0,y:30},{opacity:1,y:0,duration:.3},6.7);'+wp("sp2",7.8,"tr")+fj
    d=build("s3",D,b,j); render(d,f"{O}/s3-no-recording.mp4")
# ---------------- S4 scoreboard
if want("s4"):
    D=11.6; ph,pj=persist(D)
    b=ph+spike(1,-380,1600)+spike(2,760,-380)+title2(3.9)
    b+=clipdiv("l1","left:90px;top:262px;font-size:90px",3.8,4.8,'The test',"lab")
    card=lambda id,top,lab,mark,col,txt,s: clipdiv(id,f"left:90px;top:{top}px;width:900px;height:290px;background:#fff;border:6px solid #111;border-radius:34px;box-shadow:12px 12px 0 #111;padding:36px 44px",s,8.6-s+0.1,f'<div style="font-weight:700;font-size:38px;letter-spacing:2px">{lab}</div><div style="font-weight:800;font-size:92px;line-height:1.1;margin-top:14px"><span id="{id}n">0</span> of 1</div><div style="font-weight:500;font-size:40px">{txt}</div><div style="position:absolute;right:44px;top:50px;font-weight:800;font-size:170px;color:{col}">{mark}</div>')
    b+=card("c1",410,"WITHOUT THE SETTING","✗","#E5322D","right answers (ChatGPT said yes)",4.2)+card("c2",740,"WITH THE SETTING","✓","#1FA64A","right answers (ChatGPT said no)",5.6)
    fh,fj=fixscene("fx",8.6,3.0); b+=fh
    j=pj+TITLE_JS+wp("sp1",3.2,"bl")+'tl.fromTo("#l1",{opacity:0,y:30},{opacity:1,y:0,duration:.3},3.9);tl.fromTo("#c1",{opacity:0,x:-120},{opacity:1,x:0,duration:.4,ease:"power3.out"},4.3);tl.fromTo("#c2",{opacity:0,x:120},{opacity:1,x:0,duration:.4,ease:"power3.out"},5.7);const o2={n:0};tl.to(o2,{n:1,duration:.5,ease:"none",onUpdate(){document.getElementById("c2n").textContent=Math.round(o2.n)}},6.3);'+wp("sp2",8.0,"tr")+fj
    d=build("s4",D,b,j); render(d,f"{O}/s4-scoreboard.mp4")
# ---------------- S5 solution first then proof split
if want("s5"):
    D=13.4; ph,pj=persist(D)
    b=ph+spike(1,-380,1600)+spike(2,760,-380)+title2(3.9)
    fh,fj=fixscene("fx",3.8,3.6); b+=fh
    b+=clipdiv("c1","left:90px;top:285px;font-size:38px;background:#111",7.4,6,"WITHOUT THE SETTING","chip")+clipdiv("c2","left:90px;top:705px;font-size:38px;background:var(--acc)",7.4,6,"WITH THE SETTING","chip")
    b+=winbox("w1",90,330,900,356,7.4,6)+winbox("w2",90,750,900,356,7.4,6)
    b+=tagdiv("tg1",740,270,10.2,3.2,"SAID YES","var(--red)",38)+tagdiv("tg2",740,690,10.8,2.6,"SAID NO","var(--green)",38)
    j=pj+TITLE_JS+wp("sp1",3.2,"bl")+fj+wp("sp2",7.0,"tr")+'tl.fromTo(["#c1","#c2"],{opacity:0,y:20},{opacity:1,y:0,duration:.3},7.6);tl.fromTo("#w1",{opacity:0,x:-80},{opacity:1,x:0,duration:.4,ease:"power3.out"},7.5);tl.fromTo("#w2",{opacity:0,x:80},{opacity:1,x:0,duration:.4,ease:"power3.out"},7.6);tagIn("#tg1",10.3,-3);tagIn("#tg2",10.9,3);'
    d=build("s5",D,b,j); render(d,"/tmp/g/s5.mp4")
    m=mask(884,340)
    ff(["-i","/tmp/g/s5.mp4","-ss","31.5","-t","6","-i",A,"-ss","46","-t","6","-i",B,"-loop","1","-framerate","30","-t",str(D),"-i",m,"-filter_complex","[1:v]fps=30,scale=884:-2,crop=884:340:0:330,format=yuva420p,setpts=PTS-STARTPTS+7.6/TB[a];[2:v]fps=30,scale=884:-2,crop=884:340:0:330,format=yuva420p,setpts=PTS-STARTPTS+7.6/TB[b];[3:v]format=gray,setpts=PTS-STARTPTS+7.6/TB,split[m1][m2];[a][m1]alphamerge[am];[b][m2]alphamerge[bm];[0:v][am]overlay=98:338:eof_action=pass:enable='gte(t,7.6)'[t1];[t1][bm]overlay=98:758:eof_action=pass:enable='gte(t,7.6)'[o]","-map","[o]","-t",str(D),"-c:v","libx264","-pix_fmt","yuv420p","-crf","18",f"{O}/s5-solution-first.mp4"])
# ---------------- S6 big dark spikes, hook only
if want("s6"):
    D=8.6; ph,pj=persist(D,floats=False,ticker=False)
    b=ph+spike(1,-330,1380)+spike(2,700,-330)+spike(3,760,1450)+title2(D)
    j=pj+TITLE_JS+'tl.set(".spike",{opacity:1,scale:1.5},0.05);tl.to("#sp1",{rotation:200,duration:8.6,ease:"none"},0);tl.to("#sp2",{rotation:-200,duration:8.6,ease:"none"},0);tl.to("#sp3",{rotation:160,duration:8.6,ease:"none"},0);tl.fromTo("#t2 .w",{scale:1},{scale:1.08,duration:.4,repeat:8,yoyo:true,ease:"sine.inOut"},3.2);'
    d=build("s6",D,b,j); render(d,f"{O}/s6-big-spikes-hook.mp4")
print("built",only or "all")
