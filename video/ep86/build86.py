#!/usr/bin/env python3
"""ep86 integrator: voice/final/<n>.wav (n=1..6) + scenes/scene-N.html (markup + window.buildScene_N(tl,T0,DUR)) -> cues.json, out/narration.wav, hf/index.html. --render <name> renders the silent video."""
import json, os, re, sys, subprocess
import soundfile as sf, numpy as np
H=os.path.dirname(os.path.abspath(__file__)); GAP=float(os.environ.get("GAP","0.3")); HOOKGAP=float(os.environ.get("HOOKGAP","0.55")); HEAD=0.10; TAIL=float(os.environ.get("TAIL","2.6"))
TEXTS=[l.rstrip("\n") for l in open(H+"/lines.txt") if l.strip()]; N=len(TEXTS); assert N==6
sr=48000; lines=[]; t=HEAD; out=[]
wj=H+"/voice/words.json"; words=json.load(open(wj)) if os.path.exists(wj) else {}
for i,tx in enumerate(TEXTS,1):
    x,s=sf.read(f"{H}/voice/final/{i}.wav"); assert s==sr; x=x if x.ndim==1 else x[:,0]
    d=len(x)/sr; ln=dict(n=i,text=tx,start=round(t,3),end=round(t+d,3))
    if str(i) in words: ln["words"]=[[round(a+t,3),round(b+t,3)] for a,b in words[str(i)]]
    lines.append(ln); out.append((int(t*sr),x)); t+=d+(HOOKGAP if i==1 else GAP)
D=round(lines[-1]["end"]+TAIL,2)
nar=np.zeros(int((D+0.3)*sr))
for i0,x in out: nar[i0:i0+len(x)]+=x
os.makedirs(H+"/out",exist_ok=True)
sf.write(H+"/out/narration.wav",nar[:int(D*sr)],sr,subtype="PCM_16")
json.dump(dict(lines=lines,D=D),open(H+"/cues.json","w"),indent=1)
T0=[0.0]+[round(lines[i]["start"]-0.15,3) for i in range(1,N)]
DUR=[round((T0[i+1] if i<N-1 else D)-T0[i],3) for i in range(N)]
shell=open(H+"/shell.html").read()
styles=[];markup=[];scripts=[]
ONLY=[int(x) for x in os.environ.get("ONLY","1,2,3,4,5,6").split(",")]
for i in range(1,N+1):
    if i not in ONLY: continue
    p=f"{H}/scenes/scene-{i}.html"; src=open(p).read()
    styles+=re.findall(r"<style>(.*?)</style>",src,flags=re.S)
    scripts+=re.findall(r"<script>(.*?)</script>",src,flags=re.S)
    mk=re.sub(r"<style>.*?</style>|<script>.*?</script>","",src,flags=re.S)
    mk=re.sub(r'data-track-index="\d+"',f'data-track-index="{10+i}"',mk)
    mk=re.sub(r'data-start="[^"]*"',f'data-start="{T0[i-1]}"',mk,count=1)
    mk=re.sub(r'data-duration="[^"]*"',f'data-duration="{round(DUR[i-1]+0.12,3)}"',mk,count=1)
    mk=mk.replace(f"__D{i}__",str(DUR[i-1]))
    markup.append(mk)
calls="\n".join(f"if(window.buildScene_{i})window.buildScene_{i}(tl,{T0[i-1]},{DUR[i-1]}); else console.warn('missing scene {i}');" for i in range(1,N+1))
bounds=[T0[i] for i in range(1,N)]
html=(shell.replace("__STYLES__","\n".join(styles)).replace("__MARKUP__","\n".join(markup)).replace("__SCRIPTS__","\n".join(scripts))
      .replace("__D__",str(D)).replace("__CUES__",json.dumps(dict(lines=lines,D=D))).replace("__CALLS__",calls).replace("__BOUNDS__",json.dumps(bounds)).replace("__NSC__",str(N)))
os.makedirs(H+"/hf/assets",exist_ok=True); open(H+"/hf/index.html","w").write(html)
print("D=",D,"T0=",T0,"DUR=",DUR)
if "--render" in sys.argv:
    name=sys.argv[sys.argv.index("--render")+1] if len(sys.argv)>sys.argv.index("--render")+1 else "draft"
    env=dict(os.environ,HYPERFRAMES_NO_TELEMETRY="1",DO_NOT_TRACK="1")
    r=subprocess.run(["npx","--no-install","hyperframes","render","-o",f"{H}/out/{name}.mp4","--format","mp4","--quiet"],cwd=H+"/hf",env=env,capture_output=True,text=True,timeout=1800)
    print(r.stdout[-600:],r.stderr[-1200:])
