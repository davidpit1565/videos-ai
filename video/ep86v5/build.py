#!/usr/bin/env python3
"""ep86 v5 integrator. lines-v5.txt (8 lines) + VOICE/<n>.wav (n = line number 1..8) -> cues-<V>.json, out/narration-<V>.wav, hf/index.html.
V=short : spoken lines 1,2,4,5,6,7  -> scenes hook | ask | chat | gem | cla | try
V=long  : spoken lines 1..8        -> scenes hook | warn | ask | chat | gem | cla(+score line) | try
The last scene (try) is the silent screenshot-able TRY IT card (env TRY seconds, default 4.4); there is no spoken outro. The last frame is meant to cut/loop to frame 0.
Scene file scenes-v5/scene-<name>.html defines window.buildScene_<name>(tl,T0,DUR); scenes-v5/common.html = chrome (series label, source note, voice meter, score strip) + helper window.__e86.
In scene files the token __S__ becomes the scene's element id (s1..sN). Cue lines carry a key (hook, safe, warn, ask, chat, gem, cla, score).
Env: V, VOICE=<dir with 1..8.wav> (default voice/final; tmpvoice/final = placeholder tones), GAPS="g1,g2,.." (one gap per spoken line but the last), TRY, WORDS=<json {"<line n>":[[s,e],..]}> (default voice/words-v5.json if present; used per line only if the token count matches)."""
import json, os, re, sys, subprocess
import soundfile as sf, numpy as np
H=os.path.dirname(os.path.abspath(__file__))
V=os.environ.get("V","short"); assert V in ("short","long")
KEYS=["hook","safe","warn","ask","chat","gem","cla","score"]
USE=[0,1,3,4,5,6] if V=="short" else list(range(8))
SCENES=([("hook",["hook","safe"]),("ask",["ask"]),("chat",["chat"]),("gem",["gem"]),("cla",["cla"]),("try",[])] if V=="short"
        else [("hook",["hook","safe"]),("warn",["warn"]),("ask",["ask"]),("chat",["chat"]),("gem",["gem"]),("cla",["cla","score"]),("try",[])])
DEFG={"short":"0.5,0.4,0.45,0.3,0.4","long":"0.5,0.4,0.35,0.45,0.3,0.35,0.4"}[V]
GAPS=[float(x) for x in os.environ.get("GAPS",DEFG).split(",")]; assert len(GAPS)==len(USE)-1
TRY=float(os.environ.get("TRY","4.4"))
VOICE=os.environ.get("VOICE",H+"/voice/final")
ALL=[l.rstrip("\n") for l in open(H+"/lines-v5.txt") if l.strip()]; assert len(ALL)==8
sr=48000; lines=[]; t=0.0; out=[]
wj=os.environ.get("WORDS",H+"/voice/words-v5.json"); words=json.load(open(wj)) if os.path.exists(wj) else {}
for j,k in enumerate(USE):
    n=k+1
    x,s=sf.read(f"{VOICE}/{n}.wav"); assert s==sr; x=x if x.ndim==1 else x[:,0]
    d=len(x)/sr; ln=dict(n=n,key=KEYS[k],text=ALL[k],start=round(t,3),end=round(t+d,3))
    if str(n) in words and len(words[str(n)])==len(ALL[k].split()): ln["words"]=[[round(a+t,3),round(b+t,3)] for a,b in words[str(n)]]
    lines.append(ln); out.append((int(t*sr),x)); t+=d+(GAPS[j] if j<len(USE)-1 else 0)
byk={l["key"]:l for l in lines}
T0=[0.0]
for name,keys in SCENES[1:]:
    T0.append(round(byk[keys[0]]["start"]-0.12,3) if keys else round(lines[-1]["end"]+0.3,3))
D=round(T0[-1]+TRY,2)
NS=len(SCENES); DUR=[round((T0[i+1] if i<NS-1 else D)-T0[i],3) for i in range(NS)]
nar=np.zeros(int((D+0.3)*sr))
for i0,x in out: nar[i0:i0+len(x)]+=x
os.makedirs(H+"/out",exist_ok=True)
sf.write(H+f"/out/narration-{V}.wav",nar[:int(D*sr)],sr,subtype="PCM_16")
json.dump(dict(lines=lines,D=D,V=V),open(H+f"/cues-{V}.json","w"),indent=1)
shell=open(H+"/shell.html").read(); styles=[];markup=[];scripts=[]
com=open(H+"/scenes-v5/common.html").read()
styles+=re.findall(r"<style>(.*?)</style>",com,flags=re.S); scripts+=re.findall(r"<script>(.*?)</script>",com,flags=re.S)
chrome=re.sub(r"<style>.*?</style>|<script>.*?</script>","",com,flags=re.S)
for i,(name,keys) in enumerate(SCENES,1):
    src=open(H+f"/scenes-v5/scene-{name}.html").read().replace("__S__",f"s{i}")
    styles+=re.findall(r"<style>(.*?)</style>",src,flags=re.S); scripts+=re.findall(r"<script>(.*?)</script>",src,flags=re.S)
    mk=re.sub(r"<style>.*?</style>|<script>.*?</script>","",src,flags=re.S)
    mk=re.sub(r'data-track-index="\d+"',f'data-track-index="{10+i}"',mk)
    mk=re.sub(r'data-start="[^"]*"',f'data-start="{T0[i-1]}"',mk,count=1)
    mk=re.sub(r'data-duration="[^"]*"',f'data-duration="{round(DUR[i-1]+0.12,3)}"',mk,count=1)
    markup.append(mk)
calls="window.__T0=%s; window.__DUR=%s; window.__V=%s;\n"%(json.dumps(T0),json.dumps(DUR),json.dumps(V))+"\n".join(f"if(window.buildScene_{n})window.buildScene_{n}(tl,{T0[i]},{DUR[i]},'s{i+1}'); else console.warn('missing scene {n}');" for i,(n,_) in enumerate(SCENES))+"\nif(window.buildChrome)window.buildChrome(tl);"
html=(shell.replace("__STYLES__","\n".join(styles)).replace("__MARKUP__","\n".join(markup)).replace("__CHROME__",chrome).replace("__SCRIPTS__","\n".join(scripts))
      .replace("__D__",str(D)).replace("__CUES__",json.dumps(dict(lines=lines,D=D,V=V))).replace("__CALLS__",calls).replace("__BOUNDS__",json.dumps([T0[i] for i in range(1,NS-0)][:NS-1])).replace("__NSC__",str(NS)))
os.makedirs(H+"/hf/assets",exist_ok=True); open(H+"/hf/index.html","w").write(html)
print("V=",V,"D=",D,"T0=",T0,"DUR=",DUR)
if "--render" in sys.argv:
    name=sys.argv[sys.argv.index("--render")+1]
    env=dict(os.environ,HYPERFRAMES_NO_TELEMETRY="1",DO_NOT_TRACK="1")
    r=subprocess.run(["npx","--no-install","hyperframes","render","-o",f"{H}/out/{name}.mp4","--format","mp4","--quiet"],cwd=H+"/hf",env=env,capture_output=True,text=True,timeout=1800)
    print(r.stdout[-400:],r.stderr[-800:])
