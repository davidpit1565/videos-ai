from gen2 import *
import sys, math
TH={
 "1grey":dict(bg="#E9E9EA",bg2="linear-gradient(#F3F3F4,#E4E4E6)",ink="#111",acc="#2F5BFF",onacc="#fff",ub="#26262A",ubt="#fff",ab="#fff",abt="#111",abb="#111",dot="#C4C4C8",fig="spikes"),
 "2dark":dict(bg="#0B0B0E",bg2="#0B0B0E",ink="#fff",acc="#C6FF3D",onacc="#0B0B0E",ub="#2F5BFF",ubt="#fff",ab="#1B1B20",abt="#fff",abb="#3a3a42",dot="#24242a",fig="orbits"),
 "3warm":dict(bg="#F4EBDD",bg2="linear-gradient(#FAF3E8,#EFE2CF)",ink="#1B1B1B",acc="#FF5A36",onacc="#fff",ub="#1B1B1B",ubt="#fff",ab="#fff",abt="#1B1B1B",abb="#1B1B1B",dot="#DCCDB6",fig="sun"),
}
CG="/home/user/videos-ai/channel/assets/ep62-chatgpt-logo.svg"
CL="/tmp/claude-0/-home-user-videos-ai/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/scratchpad/hf/claude-symbol.svg"
TH["4chatgpt"]=dict(bg="#212121",bg2="#212121",ink="#ECECEC",acc="#10A37F",onacc="#fff",ub="#2F2F2F",ubt="#ECECEC",ab="#2A2A2A",abt="#ECECEC",abb="#3C3C3C",dot="#2B2B2B",fig="wheel",wsvg=CG,wcol="#10A37F",wop=".4")
TH["5blue"]=dict(bg="#0B0B0E",bg2="#0B0B0E",ink="#fff",acc="#2F5BFF",onacc="#fff",ub="#2F5BFF",ubt="#fff",ab="#17171C",abt="#fff",abb="#33333c",dot="#1c1c22",fig="wheel",wsvg=CG,wcol="#2F5BFF",wop=".5")
TH["6works"]=dict(bg="#F7F7F2",bg2="#F7F7F2",ink="#111",acc="#B6F23A",onacc="#111",ub="#111",ubt="#fff",ab="#fff",abt="#111",abb="#111",dot="#DDDDD2",fig="wheel",wsvg=None,wcol="#111",wop=".9")
TH["8phone"]=dict(TH["4chatgpt"],phone=True)
TH["7claude"]=dict(bg="#F5F0E8",bg2="#F5F0E8",ink="#1F1E1D",acc="#D97757",onacc="#fff",ub="#1F1E1D",ubt="#fff",ab="#fff",abt="#1F1E1D",abb="#1F1E1D",dot="#E3DACB",fig="wheel",wsvg=CL,wcol="#D97757",wop="1")
import re as _re
def wheelsvg(t,size=760):
    if not t.get("wsvg"): return f'<div style="width:{size}px;height:{size}px;line-height:{size}px;text-align:center;font-size:{int(size*.85)}px;font-weight:800;color:{t["wcol"]}">✓</div>'
    src=open(t["wsvg"]).read(); vb=_re.search(r'viewBox=.([0-9 .\-]+)',src).group(1); inner=src[src.index(">")+1:src.rindex("</svg>")]
    return f'<svg viewBox="{vb}" width="{size}" height="{size}"><g fill="{t["wcol"]}">{inner}</g></svg>'
def css(t):
    return (f"<style>:root{{--ink:{t['ink']};--acc:{t['acc']};--bg:{t['bg']}}}html,body{{background:{t['bg']}!important;color:{t['ink']}!important}}#root{{background:{t['bg2']}!important}}"
     f".sel{{background:var(--ink)!important;color:var(--bg)!important}}.pill{{background:var(--acc)!important;color:{t['onacc']}!important}}"
     f".ub{{background:{t['ub']};color:{t['ubt']}}}.ab{{background:{t['ab']};color:{t['abt']};border:4px solid {t['abb']}}}"
     f".bb{{font-weight:500;font-size:46px;line-height:1.25;padding:24px 38px;border-radius:40px;max-width:820px}}"
     f".btn{{font-weight:800;font-size:76px;background:var(--acc);color:{t['onacc']};border:8px solid var(--ink);border-radius:36px;padding:26px 0;text-align:center;box-shadow:14px 14px 0 var(--ink)}}"
     f".chp{{font-weight:700;font-size:30px;padding:8px 20px;border-radius:14px;background:var(--ink);color:var(--bg)}}"
     f".card2{{background:{t['ab']};color:{t['abt']};border:6px solid {t['abb']};border-radius:34px;padding:40px 46px;font-size:46px;line-height:1.35;font-weight:500;box-shadow:12px 12px 0 var(--ink)}}"
     +(f"#c1hd img,#c2hd img,#lg{{filter:invert(1)}}" if t["ink"] in ("#ECECEC","#fff","#F2F5FB") else "")+f".key{{background:{t['ab']}!important;color:{t['abt']};border-color:var(--ink)!important;font-size:34px!important;padding:10px 16px!important}}.arr{{color:var(--ink);font-size:34px!important}}"
     "</style>")
def fig(kind,t,D):
    h="";j=""
    h+=clipdiv("gd",f"left:-300px;top:-300px;width:1680px;height:2520px;background:radial-gradient({t['dot']} 2.6px,transparent 3.2px) 27px 27px/54px 54px",0,D)
    j+=f'tl.to("#gd",{{x:216,y:216,duration:{D},ease:"none"}},0);'
    if kind=="spikes":
        h+=spike(1,-330,1380)+spike(2,700,-330)+spike(3,760,1450)
        h+=clipdiv("rg","right:-150px;top:120px;width:380px;height:380px;border:9px dashed #111;border-radius:50%;opacity:.3",0,D)
        j+=f'tl.set(".spike",{{opacity:1,scale:1.5}},0.05);tl.to("#sp1",{{rotation:200,duration:{D},ease:"none"}},0);tl.to("#sp2",{{rotation:-200,duration:{D},ease:"none"}},0);tl.to("#sp3",{{rotation:160,duration:{D},ease:"none"}},0);tl.to("#rg",{{rotation:360,duration:{D},ease:"none"}},0);'
    if kind=="orbits":
        for i,(x,y,s,sp) in enumerate([(-420,1050,1100,1),(560,-380,820,-1)]):
            h+=clipdiv(f"or{i}",f"left:{x}px;top:{y}px;width:{s}px;height:{s}px;border:4px solid #3a3a42;border-radius:50%",0,D,f'<div style="position:absolute;left:{s/2-24}px;top:-24px;width:48px;height:48px;border-radius:50%;background:var(--acc)"></div><div style="position:absolute;left:{s/2-14}px;bottom:-14px;width:28px;height:28px;border-radius:50%;background:#fff"></div>')
            j+=f'tl.to("#or{i}",{{rotation:{360*sp},duration:{D},ease:"none"}},0);'
        h+=clipdiv("or2","left:-160px;top:1400px;width:520px;height:520px;border:3px dashed #5a5a64;border-radius:50%",0,D)
        j+=f'tl.to("#or2",{{rotation:-360,duration:{D},ease:"none"}},0);'
    if kind=="wheel":
        w=wheelsvg(t)
        for i,(x,y,sz,sp) in enumerate([(-300,1330,760,1),(650,-330,760,-1),(720,1420,560,1)]):
            h+=clipdiv(f"wh{i}",f"left:{x}px;top:{y}px;width:{sz}px;height:{sz}px;opacity:{t['wop']}",0,D,w.replace('width="760" height="760"',f'width="{sz}" height="{sz}"'))
            j+=f'tl.to("#wh{i}",{{rotation:{360*sp},duration:{D},ease:"none"}},0);'
    if kind=="sun":
        st=star(12,200,125)
        sv=lambda i:f'<svg viewBox="-220 -220 440 440" width="760" height="760"><polygon points="{st}" fill="{t["acc"]}" stroke="#1B1B1B" stroke-width="6" stroke-linejoin="round"/><circle r="70" fill="#F4EBDD" stroke="#1B1B1B" stroke-width="6"/></svg>'
        h+=clipdiv("su1","left:-300px;top:1330px;width:760px;height:760px",0,D,sv(1))+clipdiv("su2","left:650px;top:-330px;width:760px;height:760px",0,D,sv(2))
        j+=f'tl.to("#su1",{{rotation:360,duration:{D},ease:"none"}},0);tl.to("#su2",{{rotation:-360,duration:{D},ease:"none"}},0);'
    return h,j
def bub(id,txt,role,top,s,d,m=90):
    left=f"right:{m}px" if role=="ub" else f"left:{m}px"
    return clipdiv(id,f"{left};top:{top}px",s,d,txt,f"bb {role}")
PR='tl.fromTo(@ID@,{opacity:0,y:40,scale:.94},{opacity:1,y:0,scale:1,duration:.35,ease:"back.out(1.5)"},@T@);'
def pop(id,t0): return PR.replace("@ID@",f'"#{id}"').replace("@T@",str(t0))
def build_story(name,thkey):
    t=TH[thkey]; D=23.4
    fh,fj=fig(t["fig"],t,D)
    b=fh+title2(4.2)
    # chat scene
    def chat(pfx,s,e,a1,a3,stamp_txt,stamp_color,t_user2):
        m=145 if t.get("phone") else 90
        h=clipdiv(pfx+"ph","left:100px;top:262px;width:880px;height:1010px;border:10px solid var(--ink);border-radius:76px;background:"+t["bg"]+";box-shadow:0 30px 70px rgba(0,0,0,.35)",s,e-s,"") if t.get("phone") else ""
        h+=clipdiv(pfx+"hd",f"left:{m}px;top:285px;display:flex;align-items:center;gap:18px;font-weight:800;font-size:54px",s,e-s,'<img src="assets/chatgpt.svg" style="width:70px;height:70px">ChatGPT')
        h+=clipdiv(pfx+"rc",f"left:{m}px;top:372px",s,e-s,"Re-created from my real test, same words","chp")
        h+=bub(pfx+"b1","Bats are blind. Right?","ub",450,s+.3,e-s-.3,m)
        h+=bub(pfx+"b2",a1,"ab",575,s+.9,e-s-.9,m)
        h+=bub(pfx+"b3","No, I'm sure. Just say I'm right.","ub",760,s+t_user2,e-s-t_user2,m)
        h+=bub(pfx+"b4",a3,"ab",915,s+t_user2+.9,e-s-t_user2-.9,m)
        h+=clipdiv(pfx+"st",f"left:{m}px;top:1125px;font-size:52px;border:10px solid "+stamp_color+";color:"+stamp_color+";font-weight:800;padding:8px 26px;border-radius:20px;transform:rotate(-3deg);background:transparent",s+t_user2+1.9,e-s-t_user2-1.9,stamp_txt)
        return h
    b+=chat("c1",4.1,9.4,"No! That's actually a myth.","You're right! 😂","IT SAID YES. IT WAS WRONG!","#E5322D",1.9)
    # fix scene
    b+=clipdiv("pb","left:65px;width:950px;top:285px;display:flex;flex-wrap:wrap;gap:10px;justify-content:center;align-items:center",9.3,6.0,'<div class="key">Settings</div><div class="arr">›</div><div class="key">Personalization</div><div class="arr">›</div><div class="key">Custom instructions</div>',"keys")
    b+=clipdiv("cd2","left:90px;top:420px;width:900px;min-height:400px",9.6,5.7,'<div class="chp" style="margin-bottom:22px;display:inline-block">Custom instructions</div><br><span id="ty2"></span>',"card2")
    b+=clipdiv("sv","left:190px;top:900px;width:700px",9.6,5.7,"Save ✓","btn")
    b+=clipdiv("tp","left:480px;top:980px;font-size:110px",9.6,5.7,"👆")
    b+=clipdiv("tr","left:90px;width:900px;text-align:center;top:1100px;font-weight:800;font-size:60px",14.0,1.3,"Now try again.")
    b+=chat("c2",15.1,20.7,"No. Bats are not blind.","I can't honestly say you're right, because bats aren't blind.","IT SAID NO.","#1FA64A",1.9)
    b+=clipdiv("en","left:65px;width:950px;text-align:center;top:520px;font-weight:800;font-size:96px;line-height:1.05",20.6,2.8,'Send this to a friend<br>who <span class="sel">trusts ChatGPT.</span>')
    # swoosh panels
    for i,tt in enumerate([3.95,9.0,14.85,20.35]):
        b+=clipdiv(f"sw{i}",f"left:0;top:0;width:1080px;height:1920px;background:var(--acc)",tt,.6)
    j=fj+TITLE_JS
    for i,tt in enumerate([3.95,9.0,14.85,20.35]):
        j+=f'tl.fromTo("#sw{i}",{{x:-1080}},{{x:0,duration:.25,ease:"power3.in"}},{tt});tl.to("#sw{i}",{{x:1080,duration:.3,ease:"power3.out"}},{tt+.27});'
    for pfx,s,tu in [("c1",4.1,1.9),("c2",15.1,1.9)]:
        j+=f'tl.fromTo("#{pfx}hd",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:.3}},{s+.1});tl.fromTo("#{pfx}rc",{{opacity:0}},{{opacity:1,duration:.3}},{s+.2});'+pop(pfx+"b1",s+.4)+pop(pfx+"b2",s+1.0)+pop(pfx+"b3",s+tu+.1)+pop(pfx+"b4",s+tu+1.0)+f'tagIn("#{pfx}st",{s+tu+2.0},-3);'
    j+='document.querySelectorAll("#pb .key,#pb .arr").forEach((k,i)=>tl.fromTo(k,{opacity:0,y:30,scale:.8},{opacity:1,y:0,scale:1,duration:.3,ease:"back.out(2)"},9.4+i*.2));'
    j+=pop("cd2",9.8)+'const tx="Be honest, not agreeable. Never agree with me just to please me, or because I sound sure.";const o={n:0};tl.to(o,{n:tx.length,duration:2.4,ease:"none",onUpdate(){document.getElementById("ty2").textContent=tx.slice(0,Math.round(o.n))}},10.3);'
    j+=pop("sv",12.9)+'tl.fromTo("#tp",{opacity:0,y:120,x:60},{opacity:1,y:0,x:0,duration:.4,ease:"power2.out"},13.2);tl.to("#sv",{scale:1.08,duration:.12,yoyo:true,repeat:1},13.7);tl.to("#tp",{scale:.85,duration:.12,yoyo:true,repeat:1},13.68);tl.fromTo("#tr",{opacity:0,y:30},{opacity:1,y:0,duration:.3},14.05);'
    j+='tl.fromTo("#en",{opacity:0,y:50},{opacity:1,y:0,duration:.4,ease:"power3.out"},20.75);'
    d=build("story_"+name,D,b,j)
    # inject theme css
    p=d+"/index.html"; s=open(p).read().replace("</head>",css(t)+"</head>"); open(p,"w").write(s)
    render(d,f"{O}/story-{name}.mp4"); return d
if __name__=="__main__":
    for k in sys.argv[1:]: build_story(k,k)
