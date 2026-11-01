import os, re, shutil, subprocess
import gen
from gen import star, STAR, spike, JS_HELP
from PIL import Image, ImageDraw
HEAD=gen.HEAD.replace("radial-gradient(#C4C4C8 2.6px,transparent 3.2px) 27px 27px/54px 54px,","")
HEAD=HEAD.replace("</style>",".key{font-size:26px!important;padding:10px 15px!important}.arr{font-size:26px!important}.keys{gap:10px!important}.pill{display:inline-block;background:var(--acc);color:#fff;font-weight:800;font-size:92px;letter-spacing:-2px;padding:6px 36px;border-radius:24px}.glyph{font-weight:800;opacity:.5}.big{font-weight:800;font-size:150px;line-height:1;letter-spacing:-5px}.big .lt{font-weight:500}.bub{font-weight:500;font-size:52px;padding:30px 44px;border-radius:44px;background:#26262A;color:#fff}.stamp{font-weight:800;font-size:110px;border:14px solid var(--red);color:var(--red);padding:14px 40px;border-radius:26px;text-transform:uppercase;background:rgba(233,233,234,.6)}</style>")
O="/tmp/claude-0/-home-user-videos-ai/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/scratchpad/out"
A="/root/.claude/uploads/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/c7ed1d47-ScreenRecording_10-31-2026_22-47-17_1.mp4"
B="/root/.claude/uploads/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/b6fff252-ScreenRecording_10-31-2026_23-52-52_1.mp4"
def mask(w,h,r=32):
    p=f"/tmp/mk{w}x{h}.png"; m=Image.new("L",(w,h),0); ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),r,fill=255); m.save(p); return p
def build(name,dur,body,js,transparent=False):
    d=f"s_{name}"; os.makedirs(d+"/assets",exist_ok=True)
    for f in ["package.json","hyperframes.json","meta.json"]: shutil.copy("cream/"+f,d+"/"+f)
    shutil.copy("cream/assets/chatgpt.svg",d+"/assets/chatgpt.svg")
    head=HEAD
    if transparent: head=head.replace("background:#E9E9EA;","background:transparent;")
    root_bg='' if transparent else ''
    html=head+f'<div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920" {"style=\"background:transparent\"" if transparent else ""}>'+body+'</div><script>'+JS_HELP+js+'window.__timelines["main"]=tl;tl.seek(0);</script></body></html>'
    html=html.replace("__DUR__",str(dur)); n=[0]
    def tr(m): n[0]+=1; return str(10+n[0])
    html=re.sub("__TR__",tr,html)
    open(d+"/index.html","w").write(html); return d
def clipdiv(id,style,s,d,inner="",cls=""):
    return f'<div class="abs {cls} clip" id="{id}" style="{style}" data-start="{s}" data-duration="{d}" data-track-index="__TR__">{inner}</div>'
def persist(dur,ticker=True,floats=True,ring=True,grid=True):
    h="";j=""
    if grid:
        h+=clipdiv("gd","inset:auto;left:-300px;top:-300px;width:1680px;height:2520px;background:radial-gradient(#C4C4C8 2.6px,transparent 3.2px) 27px 27px/54px 54px",0,dur)
        j+=f'tl.to("#gd",{{x:216,y:216,duration:{dur},ease:"none"}},0);'
    if floats:
        g=[("✓","#1FA64A",30,330,100),("✗","#E5322D",930,560,90),("✦","#111",20,880,80),("✓","#1FA64A",940,980,80),("○","#111",960,300,70),("✗","#E5322D",40,1100,70)]
        for i,(c,col,x,y,fs) in enumerate(g):
            h+=clipdiv(f"fl{i}",f"left:{x}px;top:{y}px;font-size:{fs}px;color:{col}",0,dur,c,"glyph")
            j+=f'tl.fromTo("#fl{i}",{{y:0,rotation:-12}},{{y:{50+i*9},rotation:{20+i*6},duration:{dur/2},ease:"sine.inOut",yoyo:true,repeat:1}},0);'
    if ring:
        h+=clipdiv("rg","right:-150px;top:120px;width:380px;height:380px;border:9px dashed #111;border-radius:50%;opacity:.22",0,dur)
        j+=f'tl.to("#rg",{{rotation:360,duration:{dur},ease:"none"}},0);'
    if ticker:
        txt=("ACTUALLY WORKS ✓ TESTED ON REAL CHATGPT ✓ "*6)
        h+=clipdiv("tk","left:-80px;top:1170px;width:1300px;height:76px;background:#111;color:#fff;transform:rotate(-2deg);overflow:hidden;font-weight:800;font-size:36px;line-height:76px;white-space:nowrap",0,dur,f'<span id="tki" style="display:inline-block">{txt}</span>')
        j+=f'tl.to("#tki",{{x:-1100,duration:{dur},ease:"none"}},0);'
    return h,j
def title2(end):
    return (clipdiv("lg","left:465px;top:300px;width:150px;height:150px",0,end).replace('<div','<img src="assets/chatgpt.svg"',1).replace('></div>','>')
     +clipdiv("t1","left:65px;width:950px;text-align:center;top:490px",0,end,'<span class="w">ChatGPT</span><span class="w lt">doesn\'t</span><br><span class="w lt">always tell you</span><br><span class="w"><span class="sel">the truth.</span></span>',"t1")
     +clipdiv("t2","left:65px;width:950px;text-align:center;top:1010px",0,end,'<span class="w pill">Here\'s the proof.</span>'))
TITLE_JS='words("#t1",0.5,0.38,true);tl.fromTo("#t2 .w",{opacity:0,y:40,scale:.8},{opacity:1,y:0,scale:1,duration:.35,ease:"back.out(2)"},2.7);'
def fixscene(id,s,d):
    h=clipdiv(id+"a","left:65px;width:950px;text-align:center;top:330px;font-size:130px",s,d,'<span class="w">ONE</span><span class="w">SETTING</span><br><span class="w lt">changed</span><span class="w"><span class="sel">its answer.</span></span>',"big")
    h+=clipdiv(id+"b","left:65px;width:950px;top:1060px;display:flex;flex-wrap:wrap;gap:16px;justify-content:center;align-items:center",s,d,'<div class="key">Settings</div><div class="arr">→</div><div class="key">Personalization</div><div class="arr">→</div><div class="key">Custom instructions</div>',"keys")
    h+=clipdiv(id+"c","left:0;width:1080px;text-align:center;top:880px;font-size:130px;font-weight:800;color:#1FA64A",s,d,"✓")
    j=f'document.querySelectorAll("#{id}a .w").forEach((w,i)=>tl.fromTo(w,{{opacity:0,y:50,scale:.9}},{{opacity:1,y:0,scale:1,duration:.3,ease:"back.out(1.6)"}},{s}+.1+i*.22));document.querySelectorAll("#{id}b .key,#{id}b .arr").forEach((k,i)=>tl.fromTo(k,{{opacity:0,y:30,scale:.8}},{{opacity:1,y:0,scale:1,duration:.3,ease:"back.out(2)"}},{s}+1.0+i*.22));tl.fromTo("#{id}c",{{opacity:0,scale:3,rotation:-30}},{{opacity:1,scale:1,rotation:-8,duration:.3,ease:"power4.in"}},{s}+1.4);'
    return h,j
def wp(id,t,corner):
    return f'wipe("#{id}",0,0,{150 if corner=="bl" else -150},{-260 if corner=="bl" else 260},{t},{40 if corner=="bl" else -40});'
def render(d,out,fmt="mp4"):
    env=dict(os.environ,HYPERFRAMES_NO_TELEMETRY="1",DO_NOT_TRACK="1")
    subprocess.run(["npx","--no-install","hyperframes","render","-o",out,"--format",fmt,"--quiet"],cwd=d,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=280)
def winbox(id,x,y,w,h,s,d): return clipdiv(id,f"left:{x}px;top:{y}px;width:{w}px;height:{h}px",s,d,"","win")
def ff(args): subprocess.run(["ffmpeg","-loglevel","error","-y"]+args,check=True)
