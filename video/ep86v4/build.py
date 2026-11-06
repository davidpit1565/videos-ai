#!/usr/bin/env python3
"""ep86 v4 integrator. lines-v4.txt (8 lines) + voice/final/<n>.wav n=1..8 -> cues.json, out/narration.wav, hf/index.html.
Scenes (GROUPS over the 8 lines): S1 lines 1-2 hook | S2 line 3 role switch | S3 line 4 ChatGPT | S4 line 5 Gemini | S5 lines 6-7 Claude + score | S6 line 8 fixes + tail.
Scene file scenes-v4/scene-N.html defines window.buildScene_N(tl,T0,DUR); scenes-v4/common.html holds the persistent chrome (series label + score strip, window.buildChrome) and the shared helper.
Env: VOICE=<dir with 1..8.wav> (default voice/final; use tmpvoice/final for placeholder timing tests), GAPS="0.45,0.25,..." (7 values), TAIL (default 5.0 s: S6 needs the fix cards + honest limit + send chip after the one spoken line), WORDS=<json {"1":[[s,e],..]} per line, optional; default voice/words-v4.json if present>.
Word times: real if the words json has the right token count for a line, else spread by characters (pauses after , : .)."""
import json, os, re, sys, subprocess
import soundfile as sf, numpy as np
H=os.path.dirname(os.path.abspath(__file__))
GAPS=[float(x) for x in os.environ.get("GAPS","0.45,0.25,0.5,0.35,0.55,0.3,0.6").split(",")]
TAIL=float(os.environ.get("TAIL","5.0")); HEAD=0.0
VOICE=os.environ.get("VOICE",H+"/voice/final")
ALL=[l.rstrip("\n") for l in open(H+"/lines-v4.txt") if l.strip()]; assert len(ALL)==8 and len(GAPS)==7
GROUPS=[[0,1],[2],[3],[4],[5,6],[7]]
sr=48000; lines=[]; t=HEAD; out=[]
wj=os.environ.get("WORDS",H+"/voice/words-v4.json"); words=json.load(open(wj)) if os.path.exists(wj) else {}
for k in range(8):
    n=k+1
    x,s=sf.read(f"{VOICE}/{n}.wav"); assert s==sr; x=x if x.ndim==1 else x[:,0]
    d=len(x)/sr; ln=dict(n=n,text=ALL[k],start=round(t,3),end=round(t+d,3))
    if str(n) in words and len(words[str(n)])==len(ALL[k].split()): ln["words"]=[[round(a+t,3),round(b+t,3)] for a,b in words[str(n)]]
    lines.append(ln); out.append((int(t*sr),x)); t+=d+(GAPS[k] if k<7 else 0)
D=round(lines[-1]["end"]+TAIL,2)
nar=np.zeros(int((D+0.3)*sr))
for i0,x in out: nar[i0:i0+len(x)]+=x
os.makedirs(H+"/out",exist_ok=True)
sf.write(H+"/out/narration.wav",nar[:int(D*sr)],sr,subtype="PCM_16")
json.dump(dict(lines=lines,D=D),open(H+"/cues.json","w"),indent=1)
NS=len(GROUPS)
T0=[0.0]+[round(lines[GROUPS[i][0]]["start"]-0.12,3) for i in range(1,NS)]
DUR=[round((T0[i+1] if i<NS-1 else D)-T0[i],3) for i in range(NS)]
shell=open(H+"/shell.html").read(); styles=[];markup=[];scripts=[]
com=open(H+"/scenes-v4/common.html").read()
styles+=re.findall(r"<style>(.*?)</style>",com,flags=re.S); scripts+=re.findall(r"<script>(.*?)</script>",com,flags=re.S)
chrome=re.sub(r"<style>.*?</style>|<script>.*?</script>","",com,flags=re.S)
ONLY=[int(x) for x in os.environ.get("ONLY","1,2,3,4,5,6").split(",")]
for i in range(1,NS+1):
    if i not in ONLY: continue
    src=open(H+f"/scenes-v4/scene-{i}.html").read()
    styles+=re.findall(r"<style>(.*?)</style>",src,flags=re.S); scripts+=re.findall(r"<script>(.*?)</script>",src,flags=re.S)
    mk=re.sub(r"<style>.*?</style>|<script>.*?</script>","",src,flags=re.S)
    mk=re.sub(r'data-track-index="\d+"',f'data-track-index="{10+i}"',mk)
    mk=re.sub(r'data-start="[^"]*"',f'data-start="{T0[i-1]}"',mk,count=1)
    mk=re.sub(r'data-duration="[^"]*"',f'data-duration="{round(DUR[i-1]+0.12,3)}"',mk,count=1)
    markup.append(mk.replace(f"__D{i}__",str(DUR[i-1])))
calls="window.__T0=%s; window.__DUR=%s;\n"%(json.dumps(T0),json.dumps(DUR))+"\n".join(f"if(window.buildScene_{i})window.buildScene_{i}(tl,{T0[i-1]},{DUR[i-1]}); else console.warn('missing scene {i}');" for i in range(1,NS+1))+"\nif(window.buildChrome)window.buildChrome(tl);"
html=(shell.replace("__STYLES__","\n".join(styles)).replace("__MARKUP__","\n".join(markup)).replace("__CHROME__",chrome).replace("__SCRIPTS__","\n".join(scripts))
      .replace("__D__",str(D)).replace("__CUES__",json.dumps(dict(lines=lines,D=D))).replace("__CALLS__",calls).replace("__BOUNDS__",json.dumps([T0[i] for i in range(1,NS)])).replace("__NSC__",str(NS)))
os.makedirs(H+"/hf/assets",exist_ok=True); open(H+"/hf/index.html","w").write(html)
print("D=",D,"T0=",T0,"DUR=",DUR)
if "--render" in sys.argv:
    name=sys.argv[sys.argv.index("--render")+1]
    env=dict(os.environ,HYPERFRAMES_NO_TELEMETRY="1",DO_NOT_TRACK="1")
    r=subprocess.run(["npx","--no-install","hyperframes","render","-o",f"{H}/out/{name}.mp4","--format","mp4","--quiet"],cwd=H+"/hf",env=env,capture_output=True,text=True,timeout=1800)
    print(r.stdout[-400:],r.stderr[-800:])
