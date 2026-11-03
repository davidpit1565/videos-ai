#!/usr/bin/env python3
"""ep83 integrator, preview mode (no voice yet): scenes/scene-N.html + estimated line durations -> hf/index.html, then `node preview.js` screenshots frames.
Each scene file = <style>, markup (root div id=sN class="scn clip"), and window.buildScene_N(tl,T0,DUR). Real narration cues replace EST later (same file layout as ep82)."""
import json, os, re, sys
H=os.path.dirname(os.path.abspath(__file__))
TEXTS=[l.rstrip("\n") for l in open(H+"/lines.txt") if l.strip()]; N=len(TEXTS)
_c=json.load(open(H+"/cues.json")) if os.path.exists(H+"/cues.json") else None
EST=(_c["durations"] if "durations" in _c else [round(l["end"]-l["start"],3) for l in _c["lines"]]) if _c else None
EST=EST or ([round(0.32*len(t.split())+0.5,2) for t in TEXTS])
_x=( else 0
GAP=0.3; HEAD=0.10; HOOKGAP=0.55; TAIL=0.9
t=HEAD; lines=[]
for i,(tx,d) in enumerate(zip(TEXTS,EST),1):
    lines.append(dict(n=i,text=tx,start=round(t,3),end=round(t+d,3))); t+=d+(HOOKGAP if i==1 else GAP)
D=round(lines[-1]["end"]+TAIL,2)
T0=[0.0]+[round(lines[i]["start"]-0.15,3) for i in range(1,N)]
DUR=[round((T0[i+1] if i<N-1 else D)-T0[i],3) for i in range(N)]
shell=open(H+"/shell.html").read(); styles=[];markup=[];scripts=[]
ONLY=[int(x) for x in os.environ["ONLY"].split(",")] if os.environ.get("ONLY") else None
OUT=os.environ.get("OUT","index")
for i in range(1,N+1):
    p=f"{H}/scenes/scene-{i}.html"
    if not os.path.exists(p) or (ONLY and i not in ONLY): continue
    src=open(p).read()
    styles+=re.findall(r"<style>(.*?)</style>",src,flags=re.S); scripts+=re.findall(r"<script>(.*?)</script>",src,flags=re.S)
    mk=re.sub(r"<style>.*?</style>|<script>.*?</script>","",src,flags=re.S)
    mk=re.sub(r'data-track-index="\d+"',f'data-track-index="{10+i}"',mk)
    mk=re.sub(r'data-start="[^"]*"',f'data-start="{T0[i-1]}"',mk,count=1)
    mk=re.sub(r'data-duration="[^"]*"',f'data-duration="{round(DUR[i-1]+0.12,3)}"',mk,count=1)
    markup.append(mk.replace(f"__D{i}__",str(DUR[i-1])))
calls="\n".join(f"if(window.buildScene_{i})window.buildScene_{i}(tl,{T0[i-1]},{DUR[i-1]}); else console.warn('missing scene {i}');" for i in range(1,N+1))
html=(shell.replace("__STYLES__","\n".join(styles)).replace("__MARKUP__","\n".join(markup)).replace("__SCRIPTS__","\n".join(scripts))
 .replace("__D__",str(D)).replace("__CUES__",json.dumps(dict(lines=lines,D=D))).replace("__CALLS__",calls).replace("__BOUNDS__",json.dumps([T0[i] for i in range(1,N)])).replace("__NSC__",str(N)))
os.makedirs(H+"/hf/assets",exist_ok=True); open(f"{H}/hf/{OUT}.html","w").write(html)
os.system(f"cp -n {H}/assets/* {H}/hf/assets/ 2>/dev/null")
json.dump(dict(lines=lines,D=D,T0=T0,DUR=DUR),open(H+"/preview-cues.json","w"),indent=1)
print("page: hf/"+OUT+".html")
print("D=",D,"T0=",T0,"DUR=",DUR)
