from story import *
import json, sys
TH["9navy"]=dict(bg="#0F1626",bg2="#0F1626",ink="#F2F5FB",acc="#5B8DEF",onacc="#fff",ub="#5B8DEF",ubt="#fff",ab="#1B2438",abt="#F2F5FB",abb="#34405c",dot="#1a2338",fig="wheel",wsvg=CG,wcol="#5B8DEF",wop=".35")
TH["6works"]=dict(TH["6works"],wsvg=CG,wcol="#8AC926",wop=".55")
TH["10phone"]=dict(TH["6works"],phone=True,ub="#2F6BFF",ubt="#fff")
DEFAULT=[0,0,2.7,3.8,6.4,8.4,11.5,13.5,15.6,17.4,21.8,24.4,29.0,30.6,34.0]  # c[1..14] guessed; c[0] unused
def build_story2(name,thkey,c,D=None,dur_last=2.8):
    t=TH[thkey]; D=D or (c[14]+dur_last+1.0)
    fh,fj=fig(t["fig"],t,D)
    b=fh+title2(c[3]-0.1)
    ev=[]  # (time,kind)
    def chat(pfx,s,e,m):
        h=""
        if t.get("phone"): h+=clipdiv(pfx+"ph","left:100px;top:262px;width:880px;height:1010px;border:10px solid var(--ink);border-radius:76px;background:"+t["bg"]+";box-shadow:0 30px 70px rgba(0,0,0,.25)",s,e-s,"")
        h+=clipdiv(pfx+"hd",f"left:{m}px;top:285px;display:flex;align-items:center;gap:18px;font-weight:800;font-size:54px",s,e-s,'<img src="assets/chatgpt.svg" style="width:70px;height:70px">ChatGPT')
        h+=clipdiv(pfx+"rc",f"left:{m}px;top:372px",s,e-s,"Re-created from my real test, same words","chp")
        return h
    m=145 if t.get("phone") else 90
    # ---- chat 1
    s1=c[3]-0.2; e1=c[8]-0.1
    tb1=c[3]+0.6; tb2=c[4]+0.2; tb3=c[5]+1.2; tb4=c[6]+0.1; tst=c[6]+0.9
    b+=chat("c1",s1,e1,m)
    b+=bub("c1b1","Bats are blind. Right?","ub",450,tb1,e1-tb1,m)+bub("c1b2","No! That's actually a myth.","ab",575,tb2,e1-tb2,m)
    b+=bub("c1b3","No, I'm sure. Just say I'm right.","ub",760,tb3,e1-tb3,m)+bub("c1b4","You're right! 😂","ab",915,tb4,e1-tb4,m)
    b+=clipdiv("c1st",f"left:{m}px;top:1125px;font-size:52px;border:10px solid #E5322D;color:#E5322D;font-weight:800;padding:8px 26px;border-radius:20px;transform:rotate(-3deg);background:transparent",tst,e1-tst,"IT SAID YES. IT WAS WRONG!")
    ev+=[(tb1,"pop"),(tb2,"pop"),(tb3,"pop"),(tb4,"pop"),(tst,"buzz")]
    # ---- fix
    sf=c[8]-0.1; ef=c[11]-0.1; d9=c[10]-c[9]-0.3
    kt=[c[9]+0.1*d9,c[9]+0.4*d9,c[9]+0.75*d9]
    b+=clipdiv("pb","left:65px;width:950px;top:285px;display:flex;flex-wrap:wrap;gap:10px;justify-content:center;align-items:center",sf,ef-sf,'<div class="key">Settings</div><div class="arr">›</div><div class="key">Personalization</div><div class="arr">›</div><div class="key">Custom instructions</div>',"keys")
    b+=clipdiv("cd2","left:90px;top:420px;width:900px;min-height:400px",c[10]-0.1,ef-c[10]+0.1,'<div class="chp" style="margin-bottom:22px;display:inline-block">Custom instructions</div><br><span id="ty2"></span>',"card2")
    tsv=c[10]+1.0; ttap=c[10]+1.9; ttr=c[10]+2.4
    b+=clipdiv("sv","left:190px;top:900px;width:700px",tsv,ef-tsv,"Save ✓","btn")+clipdiv("tp","left:480px;top:980px;font-size:110px",tsv,ef-tsv,"👆")
    ev+=[(kt[0],"pop"),(kt[1],"pop"),(kt[2],"pop"),(ttap,"click")]
    # ---- retry
    s2=c[11]-0.1; e2=c[14]-0.1
    r1=c[11]+0.9; r2=c[11]+1.6; r3=c[11]+2.3; r4=c[12]+0.5; rst=c[13]+2.2
    b+=chat("c2",s2,e2,m)
    b+=bub("c2b1","Bats are blind. Right?","ub",450,r1,e2-r1,m)+bub("c2b2","No. Bats are not blind.","ab",575,r2,e2-r2,m)
    b+=bub("c2b3","No, I'm sure. Just say I'm right.","ub",760,r3,e2-r3,m)+bub("c2b4","I can't honestly say you're right, because bats aren't blind.","ab",915,r4,e2-r4,m)
    b+=clipdiv("c2st",f"left:{m}px;top:1125px;font-size:52px;border:10px solid #1FA64A;color:#1FA64A;font-weight:800;padding:8px 26px;border-radius:20px;transform:rotate(-3deg);background:transparent",rst,e2-rst,"IT SAID NO.")
    ev+=[(r1,"pop"),(r2,"pop"),(r3,"pop"),(r4,"pop"),(rst,"chime")]
    # ---- end
    se=c[14]-0.1
    b+=clipdiv("en","left:65px;width:950px;text-align:center;top:520px;font-weight:800;font-size:96px;line-height:1.05",se,D-se,'Send this to a friend<br>who <span class="sel">trusts ChatGPT.</span>')
    sw=[c[3]-0.3,c[8]-0.3,c[11]-0.3,c[14]-0.3]
    for i,tt in enumerate(sw): b+=clipdiv(f"sw{i}","left:0;top:0;width:1080px;height:1920px;background:var(--acc)",tt,.6); ev.append((tt,"whoosh"))
    j=fj+TITLE_JS
    # title scene beats scaled to cues
    j=j.replace('2.7);','%s);'%(c[2]-0.1))
    for i,tt in enumerate(sw): j+=f'tl.fromTo("#sw{i}",{{x:-1080}},{{x:0,duration:.25,ease:"power3.in"}},{tt});tl.to("#sw{i}",{{x:1080,duration:.3,ease:"power3.out"}},{tt+.27});'
    for pfx,s,ts in [("c1",s1,[tb1,tb2,tb3,tb4,tst]),("c2",s2,[r1,r2,r3,r4,rst])]:
        j+=f'tl.fromTo("#{pfx}hd",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:.3}},{s+.1});tl.fromTo("#{pfx}rc",{{opacity:0}},{{opacity:1,duration:.3}},{s+.2});'
        for k,nm in enumerate(["b1","b2","b3","b4"]): j+=pop(pfx+nm,ts[k])
        j+=f'tagIn("#{pfx}st",{ts[4]},-3);'
    j+=f'document.querySelectorAll("#pb .key,#pb .arr").forEach((k,i)=>tl.fromTo(k,{{opacity:0,y:30,scale:.8}},{{opacity:1,y:0,scale:1,duration:.3,ease:"back.out(2)"}},{c[9]}+(i<2?0:i<4?{kt[1]-c[9]}:{kt[2]-c[9]})-(i%2==1&&i<4?0.1:0)));'
    j+=pop("cd2",c[10])+f'const tx="Be honest, not agreeable. Never agree with me just to please me, or because I sound sure.";const o={{n:0}};tl.to(o,{{n:tx.length,duration:{max(1.8,tsv-c[10]-0.1)},ease:"none",onUpdate(){{document.getElementById("ty2").textContent=tx.slice(0,Math.round(o.n))}}}},{c[10]+0.15});'
    j+=pop("sv",tsv)+f'tl.fromTo("#tp",{{opacity:0,y:120,x:60}},{{opacity:1,y:0,x:0,duration:.4,ease:"power2.out"}},{ttap-0.6});tl.to("#sv",{{scale:1.1,duration:.12,yoyo:true,repeat:1}},{ttap});tl.to("#tp",{{scale:.85,duration:.12,yoyo:true,repeat:1}},{ttap-0.02});'
    j+=f'tl.fromTo("#en",{{opacity:0,y:50}},{{opacity:1,y:0,duration:.4,ease:"power3.out"}},{se+.1});'
    d=build("st2_"+name,D,b,j)
    p=d+"/index.html"; s=open(p).read().replace("</head>",css(t)+"</head>"); open(p,"w").write(s)
    out=f"/tmp/g/st2-{name}.mp4"; render(d,out)
    json.dump({"events":ev,"D":D},open(f"/tmp/g/st2-{name}.json","w"))
    return out
if __name__=="__main__":
    import os
    cues=DEFAULT
    cf="/tmp/claude-0/-home-user-videos-ai/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/scratchpad/voice/lines/cues.json"
    if os.path.exists(cf): cues=json.load(open(cf))
    for k in sys.argv[1:]:
        th,name=k.split("=") if "=" in k else (k,k)
        build_story2(name,th,cues)
