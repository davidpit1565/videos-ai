#!/usr/bin/env python3
"""nextreel-git integrator (script B). lines-c.txt (11 lines) + voice/final/<n>.wav (n=1..11) + voice/words.json -> cues.json, out/narration.wav, hf/index.html.
Env: TOMORROW=1 adds line 11 (the optional 'Tomorrow...' line) and ends after it; default TOMORROW=0 ends after line 10 plus HOLD seconds (default 3.0; with TOMORROW=1 default 1.6).
GAPS="g1,..": one gap per spoken line but the last. VOICE=<dir>. The single world file scenes-i/world.html builds the whole timeline from the cues (keys L1..L11)."""
import json, os, re, sys, subprocess
import soundfile as sf, numpy as np
H=os.path.dirname(os.path.abspath(__file__))
TOM=os.environ.get("TOMORROW","0")=="1"
N=11 if TOM else 10
GAPS=[float(x) for x in os.environ.get("GAPS","0.4,0.35,0.3,0.4,0.35,0.3,0.3,0.35,0.4,0.45").split(",")][:N-1]
HOLD=float(os.environ.get("HOLD","1.6" if TOM else "3.0"))
VOICE=os.environ.get("VOICE",H+"/voice/final")
ALL=[l.rstrip("\n") for l in open(H+"/lines-c.txt") if l.strip()]; assert len(ALL)==11
sr=48000; lines=[]; t=0.0; out=[]
wj=os.environ.get("WORDS",H+"/voice/words.json"); words=json.load(open(wj)) if os.path.exists(wj) else {}
W5=json.load(open(H+"/voice/words-new5.json")); V1=os.environ.get("V1","1")  # '1' or '1b'
NEW={1:V1,2:"2",8:"8",11:"11"}   # lines re-recorded in voice/new5 (accent-checked); the rest from voice/final
for n,k in NEW.items(): words[str(n)]=W5[k]
if '6' in words and len(words['6'])==10: words['6']=words['6'][:4]+[[words['6'][4][0],words['6'][5][1]]]+words['6'][6:]  # 'GitHub' was aligned as Git+Hub
for k in range(N):
    n=k+1
    wavp=f"{H}/voice/new5/{NEW[n]}.wav" if n in NEW else f"{VOICE}/{n}.wav"
    x,s=sf.read(wavp); assert s==sr; x=x if x.ndim==1 else x[:,0]
    d=len(x)/sr; ln=dict(n=n,key="L%d"%n,text=ALL[k],start=round(t,3),end=round(t+d,3))
    if str(n) in words and len(words[str(n)])==len(ALL[k].split()): ln["words"]=[[round(a+t,3),round(b+t,3)] for a,b in words[str(n)]]
    lines.append(ln); out.append((int(t*sr),x)); t+=d+(GAPS[k] if k<N-1 else 0)
D=round(lines[-1]["end"]+HOLD,2)
nar=np.zeros(int((D+0.3)*sr))
for i0,x in out: nar[i0:i0+len(x)]+=x
os.makedirs(H+"/out",exist_ok=True)
sf.write(H+"/out/narration.wav",nar[:int(D*sr)],sr,subtype="PCM_16")
json.dump(dict(lines=lines,D=D,tomorrow=TOM),open(H+"/cues.json","w"),indent=1)
shell=open(H+"/shell10.html").read()
world=open(H+"/scenes-i/world.html").read()
styles=re.findall(r"<style>(.*?)</style>",world,flags=re.S); scripts=re.findall(r"<script>(.*?)</script>",world,flags=re.S)
markup=re.sub(r"<style>.*?</style>|<script>.*?</script>","",world,flags=re.S)
calls="window.__TOM=%s;\nif(window.buildWorld)window.buildWorld(tl);"%("true" if TOM else "false")
html=(shell.replace("__STYLES__","\n".join(styles)).replace("__MARKUP__",markup).replace("__CHROME__","").replace("__SCRIPTS__","\n".join(scripts))
      .replace("__D__",str(D)).replace("__CUES__",json.dumps(dict(lines=lines,D=D,tomorrow=TOM))).replace("__CALLS__",calls).replace("__NSC__","1"))
os.makedirs(H+"/hf/assets",exist_ok=True); open(H+"/hf/index.html","w").write(html)
print("TOMORROW=",TOM,"D=",D,[(l["key"],l["start"],l["end"]) for l in lines])
if "--render" in sys.argv:
    name=sys.argv[sys.argv.index("--render")+1]
    env=dict(os.environ,HYPERFRAMES_NO_TELEMETRY="1",DO_NOT_TRACK="1")
    r=subprocess.run(["npx","--no-install","hyperframes","render","-o",f"{H}/out/{name}.mp4","--format","mp4","--quiet"],cwd=H+"/hf",env=env,capture_output=True,text=True,timeout=1800)
    print(r.stdout[-400:],r.stderr[-800:])
