import math, os, shutil
def star(n=14,r1=120,r2=26):
    pts=[]
    for i in range(n*2):
        a=math.pi*i/n; r=r1 if i%2==0 else r2
        r*= (1+0.12*math.sin(i*2.3))
        pts.append(f"{r*math.cos(a):.1f},{r*math.sin(a):.1f}")
    return " ".join(pts)
STAR=star()
HEAD='''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script><style>
@font-face{font-family:"Inter";src:url("https://cdn.jsdelivr.net/npm/@fontsource/inter@5/files/inter-latin-800-normal.woff2") format("woff2");font-weight:800}
@font-face{font-family:"Inter";src:url("https://cdn.jsdelivr.net/npm/@fontsource/inter@5/files/inter-latin-700-normal.woff2") format("woff2");font-weight:700}
@font-face{font-family:"Inter";src:url("https://cdn.jsdelivr.net/npm/@fontsource/inter@5/files/inter-latin-500-normal.woff2") format("woff2");font-weight:500}
:root{--ink:#111;--acc:#2F5BFF;--red:#E5322D;--green:#1FA64A}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#E9E9EA;font-family:Inter,sans-serif;color:var(--ink)}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:radial-gradient(#C4C4C8 2.6px,transparent 3.2px) 27px 27px/54px 54px,linear-gradient(#F3F3F4,#E4E4E6)}
.abs{position:absolute}
.ctr{left:65px;width:950px;text-align:center}
.t1{font-weight:800;font-size:122px;line-height:1.02;letter-spacing:-4px}
.t1 .lt{font-weight:500}
.w{display:inline-block;opacity:0;margin:0 8px}
.sel{background:var(--ink);color:#fff;padding:2px 22px;border-radius:12px;display:inline-block}
.lab{font-weight:800;font-size:120px;letter-spacing:-4px}
.lab small{display:block;font-weight:500;font-size:60px;letter-spacing:-1px}
.win{border-radius:40px;border:8px solid var(--ink);box-shadow:14px 14px 0 var(--ink);background:#000}
.tag{font-weight:800;font-size:50px;color:#fff;padding:10px 28px;border-radius:16px;border:6px solid var(--ink);box-shadow:7px 7px 0 var(--ink)}
.chip{font-weight:700;font-size:34px;padding:8px 22px;border-radius:14px;color:#fff;background:var(--ink)}
.spike{width:700px;height:700px}
.card{background:#26262A;color:#fff;border-radius:34px;padding:44px 48px;font-size:44px;line-height:1.35;font-weight:500;box-shadow:0 30px 60px rgba(0,0,0,.35)}
.card .chip{background:var(--acc);margin-bottom:22px;display:inline-block}
.cur{display:inline-block;width:6px;height:48px;background:#7fa0ff;vertical-align:-8px;margin-left:4px}
.key{font-weight:700;font-size:31px;background:#fff;border:4px solid var(--ink);border-bottom-width:10px;border-radius:16px;padding:12px 22px;opacity:0}
.keys{left:65px;width:950px;display:flex;flex-wrap:wrap;gap:16px;justify-content:center;align-items:center}
.arr{font-weight:800;font-size:34px;opacity:0}
</style></head><body>
'''
def spike(i,x,y):
    return f'''<div class="abs spike clip" id="sp{i}" style="left:{x}px;top:{y}px" data-start="0" data-duration="__DUR__" data-track-index="__TR__"><svg viewBox="-150 -150 300 300" width="700" height="700"><defs><radialGradient id="g{i}"><stop offset="0" stop-color="#3a3a3e"/><stop offset="1" stop-color="#000"/></radialGradient><filter id="b{i}" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/><feDropShadow dx="6" dy="14" stdDeviation="9" flood-opacity=".45"/></filter></defs><polygon points="{STAR}" fill="url(#g{i})" filter="url(#b{i})"/></svg></div>'''
JS_HELP='''
const tl=gsap.timeline({paused:true});tl.set('.spike',{opacity:0},0);
function words(sel,t0,gap,first0){document.querySelectorAll(sel+" .w").forEach((w,i)=>{if(i===0&&first0)tl.set(w,{opacity:1},0);else tl.fromTo(w,{opacity:0,y:40,scale:.92},{opacity:1,y:0,scale:1,duration:.28,ease:"power3.out"},t0+i*gap)})}
function hash(n){const x=Math.sin(n*127.1)*43758.5453;return x-Math.floor(x)}
function scramble(el,text,t0,dur){const o={p:0};const ch="#$%&*?/ABCDEFGHJKLMNPRSTUVWXYZ";tl.to(o,{p:1,duration:dur,ease:"none",onUpdate(){let s="";for(let i=0;i<text.length;i++){s+=(o.p>=(i+1)/text.length||text[i]===" ")?text[i]:ch[Math.floor(hash(i*7+Math.floor(o.p*30))*ch.length)]}el.textContent=s}},t0);tl.set(el,{opacity:1},t0)}
function wipe(id,x0,y0,x1,y1,t0,rot){tl.fromTo(id,{opacity:1,scale:.25,x:x0,y:y0,rotation:0},{scale:2.6,x:x1,y:y1,rotation:rot,duration:.75,ease:"power2.in"},t0);tl.to(id,{opacity:0,duration:.2},t0+.62)}
function shake(id,t0){tl.to(id,{x:"+=8",y:"+=5",duration:.05,repeat:5,yoyo:true},t0)}
function tagIn(id,t0,rot){tl.fromTo(id,{opacity:0,scale:2.2,rotation:rot-14},{opacity:1,scale:1,rotation:rot,duration:.22,ease:"power4.in"},t0);shake(id,t0+.22)}
'''
def title_scene(dur_end):
    return f'''
 <img class="abs clip" id="lg" src="assets/chatgpt.svg" style="left:465px;top:300px;width:150px;height:150px" data-start="0" data-duration="{dur_end}" data-track-index="1">
 <div class="abs ctr t1 clip" id="t1" style="top:500px" data-start="0" data-duration="{dur_end}" data-track-index="2"><span class="w">ChatGPT</span><span class="w lt">doesn't</span><br><span class="w lt">always tell you</span><br><span class="w"><span class="sel">the truth.</span></span></div>
 <div class="abs ctr clip" id="t2" style="top:1010px;font-weight:700;font-size:64px" data-start="0" data-duration="{dur_end}" data-track-index="3"><span class="w" style="opacity:0">Here is the proof.</span></div>'''
def build(name,dur,body,js,windows):
    d=f"v_{name}"
    os.makedirs(d+"/assets",exist_ok=True)
    for f in ["package.json","hyperframes.json","meta.json"]: shutil.copy("cream/"+f,d+"/"+f)
    shutil.copy("cream/assets/chatgpt.svg",d+"/assets/chatgpt.svg")
    html=HEAD+f'<div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920">'+body+'</div><script>'+JS_HELP+js+'window.__timelines["main"]=tl;tl.seek(0);</script></body></html>'
    html=html.replace("__DUR__",str(dur))
    n=[0]
    def tr(m): n[0]+=1; return str(20+n[0])
    import re
    html=re.sub("__TR__",tr,html)
    open(d+"/index.html","w").write(html)
