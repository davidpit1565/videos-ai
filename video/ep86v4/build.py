#!/usr/bin/env python3
"""ep86 v3 integrator. voice/final/<n>.wav for lines 1..12 (see lines-all.txt) -> cues-<V>.json, out/narration-<V>.wav, hf/index.html.
V=a: hook = line 1 (result-first). V=b: hook = line 12 (question). Scenes (line groups): S1 hook | S2 lines 2-3 | S3 line 4 | S4 lines 5-6 | S5 lines 7-8 | S6 lines 9-10 | S7 line 11.
Scene file scenes/scene-N.html (N=1..7; scene-1a/scene-1b for the two hooks) defines window.buildScene_N(tl,T0,DUR) and may read window.__CUES.lines[k] ({n,text,start,end,words}) for exact line/word times."""
import json, os, re, sys, subprocess
import soundfile as sf, numpy as np
H=os.path.dirname(os.path.abspath(__file__)); GAP=float(os.environ.get("GAP","0.28")); TAIL=float(os.environ.get("TAIL","2.8")); HEAD=0.10
V=os.environ.get("V","a")
ALL=[l.rstrip("\n") for l in open(H+"/lines-all.txt") if l.strip()]; assert len(ALL)==15
ORDER=[13 if V=="a" else 12,1]+list(range(2,12))+[14,15]   # hook, setup (line 1), lines 2..11, save card, send-to
GROUPS=[[0,1],[2,3],[4],[5,6],[7,8],[9,10],[11],[12,13]]   # indexes into ORDER -> scenes 1..8 (1 hook+setup | 2 promises | 3 roles | 4 ChatGPT | 5 Gemini | 6 Claude | 7 board | 8 save card + send-to + #2)
sr=48000; lines=[]; t=HEAD; out=[]
wj=H+"/voice/words.json"; words=json.load(open(wj)) if os.path.exists(wj) else {}
for k,n in enumerate(ORDER):
    x,s=sf.read(f"{H}/voice/final/{n}.wav"); assert s==sr; x=x if x.ndim==1 else x[:,0]
    d=len(x)/sr; ln=dict(n=k+1,src=n,text=ALL[n-1],start=round(t,3),end=round(t+d,3))
    if str(n) in words: ln["words"]=[[round(a+t,3),round(b+t,3)] for a,b in words[str(n)]]
    lines.append(ln); out.append((int(t*sr),x)); t+=d+(0.5 if k==0 else GAP)
D=round(lines[-1]["end"]+TAIL,2)
nar=np.zeros(int((D+0.3)*sr))
for i0,x in out: nar[i0:i0+len(x)]+=x
os.makedirs(H+"/out",exist_ok=True)
sf.write(H+f"/out/narration-{V}.wav",nar[:int(D*sr)],sr,subtype="PCM_16")
json.dump(dict(lines=lines,D=D),open(H+f"/cues-{V}.json","w"),indent=1)
NS=len(GROUPS)
T0=[0.0]+[round(lines[GROUPS[i][0]]["start"]-0.15,3) for i in range(1,NS)]
DUR=[round((T0[i+1] if i<NS-1 else D)-T0[i],3) for i in range(NS)]
shell=open(H+"/shell.html").read(); styles=[];markup=[];scripts=[]
ONLY=[int(x) for x in os.environ.get("ONLY","1,2,3,4,5,6,7,8").split(",")]
for i in range(1,NS+1):
    if i not in ONLY: continue
    p=H+(f"/scenes/scene-1{V}.html" if i==1 else f"/scenes/scene-{i}.html"); src=open(p).read()
    styles+=re.findall(r"<style>(.*?)</style>",src,flags=re.S); scripts+=re.findall(r"<script>(.*?)</script>",src,flags=re.S)
    mk=re.sub(r"<style>.*?</style>|<script>.*?</script>","",src,flags=re.S)
    mk=re.sub(r'data-track-index="\d+"',f'data-track-index="{10+i}"',mk)
    mk=re.sub(r'data-start="[^"]*"',f'data-start="{T0[i-1]}"',mk,count=1)
    mk=re.sub(r'data-duration="[^"]*"',f'data-duration="{round(DUR[i-1]+0.12,3)}"',mk,count=1)
    markup.append(mk.replace(f"__D{i}__",str(DUR[i-1])))
calls="\n".join(f"if(window.buildScene_{i})window.buildScene_{i}(tl,{T0[i-1]},{DUR[i-1]}); else console.warn('missing scene {i}');" for i in range(1,NS+1))
html=(shell.replace("__STYLES__","\n".join(styles)).replace("__MARKUP__","\n".join(markup)).replace("__SCRIPTS__","\n".join(scripts))
      .replace("__D__",str(D)).replace("__CUES__",json.dumps(dict(lines=lines,D=D))).replace("__CALLS__",calls).replace("__BOUNDS__",json.dumps([T0[i] for i in range(1,NS)])).replace("__NSC__",str(NS)))
os.makedirs(H+"/hf/assets",exist_ok=True); open(H+"/hf/index.html","w").write(html)
print("D=",D,"T0=",T0,"DUR=",DUR)
if "--render" in sys.argv:
    name=sys.argv[sys.argv.index("--render")+1]
    env=dict(os.environ,HYPERFRAMES_NO_TELEMETRY="1",DO_NOT_TRACK="1")
    r=subprocess.run(["npx","--no-install","hyperframes","render","-o",f"{H}/out/{name}.mp4","--format","mp4","--quiet"],cwd=H+"/hf",env=env,capture_output=True,text=True,timeout=1800)
    print(r.stdout[-400:],r.stderr[-800:])
