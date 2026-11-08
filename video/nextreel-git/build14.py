#!/usr/bin/env python3
"""nextreel-git integrator (script B). lines-c.txt (11 lines) + voice/final/<n>.wav (n=1..11) + voice/words.json -> cues.json, out/narration.wav, hf/index.html.
Env: TOMORROW=1 adds line 11 (the optional 'Tomorrow...' line) and ends after it; default TOMORROW=0 ends after line 10 plus HOLD seconds (default 3.0; with TOMORROW=1 default 1.6).
GAPS="g1,..": one gap per spoken line but the last. VOICE=<dir>. The single world file scenes-i/world5.html builds the whole timeline from the cues (keys L1..L11)."""
import json, os, re, sys, subprocess
import soundfile as sf, numpy as np
H=os.path.dirname(os.path.abspath(__file__))
TOM=os.environ.get("TOMORROW","0")=="1"
N=11 if TOM else 10
GAPS=[float(x) for x in os.environ.get("GAPS","0.4,0.35,0.3,0.4,0.35,0.3,0.3,0.35,0.4,0.45").split(",")][:N-1]
HOLD=float(os.environ.get("HOLD","2.6"))
VOICE=os.environ.get("VOICE",H+"/voice/final")
ALL0=[l.rstrip("\n") for l in open(H+"/lines-c.txt") if l.strip()]; assert len(ALL0)==11
sr=48000; lines=[]; t=0.0; out=[]
HOOK="AI broke your app? GitHub undoes it."
HW=H+"/voice/new8/hook.wav"; HWORDS=json.load(open(H+"/voice/new8/hook-words.json"))
W7=json.load(open(H+"/voice/new7/words.json"))
ALLD=[l.rstrip("\n") for l in open(H+"/lines-d.txt") if l.strip()]; assert len(ALLD)==8
SEQ=[(HOOK,HW,HWORDS)]+[(ALLD[k],f"{H}/voice/new7/{k+1}.wav",W7[str(k+1)]) for k in range(8)]
N=len(SEQ); GAPS=[0.3,0.3,0.3,0.35,0.3,0.3,0.3,0.4][:N-1]
for k,(txt,wavp,w) in enumerate(SEQ):
    x,s_=sf.read(wavp); assert s_==sr; x=x if x.ndim==1 else x[:,0]
    x=x*(10**(({8:1.6}.get(k+1,0))/20))
    d=len(x)/sr; ln=dict(n=k+1,key="L%d"%(k+1),text=txt,start=round(t,3),end=round(t+d,3))
    if w and len(w)==len(txt.split()): ln["words"]=[[round(a+t,3),round(b+t,3)] for a,b in w]
    else: print("NO WORDS for line",k+1,len(w or []),len(txt.split()))
    lines.append(ln); out.append((int(t*sr),x)); t+=d+(GAPS[k] if k<N-1 else 0)
D=round(lines[-1]["end"]+HOLD,2)
nar=np.zeros(int((D+0.3)*sr))
for i0,x in out: nar[i0:i0+len(x)]+=x
os.makedirs(H+"/out",exist_ok=True)
sf.write(H+"/out/narration-s4.wav",nar[:int(D*sr)],sr,subtype="PCM_16")
json.dump(dict(lines=lines,D=D,tomorrow=TOM),open(H+"/cues-s4.json","w"),indent=1)
shell=open(H+"/shell10.html").read()
world=open(H+"/scenes-i/world5.html").read()
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
