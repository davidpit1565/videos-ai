import glob,json,os,sys,numpy as np,librosa,soundfile as sf
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H)
from tighten import tighten
from pick import metrics
MAP={1:3,2:6,3:7,4:9}   # take line -> final line
res={}
for w in sorted(glob.glob(H+"/voice/re84*.wav")):
    cj=w[:-4]+"-cues.json"; cues=json.load(open(cj)); tk=os.path.basename(w)[2:-4]
    for c in cues:
        m=metrics(w,c)
        if m:
            y,sr=librosa.load(w,sr=16000,offset=c["start"],duration=c["end"]-c["start"]); m["lvl"]=float(20*np.log10(np.sqrt(np.mean(y**2))+1e-9))
            res.setdefault(MAP[c["n"]],{})[tk]=dict(m,cue=c)
pick={}
for n,d in sorted(res.items()):
    best=None
    for t,m in d.items():
        ok=(m["rng"]<=9.0) and (m["end"]>=-2.0)
        score=(0 if ok else -100)+min(m["rng"],8.5)+0.8*max(-3.5,min(2,m["end"]))+0.02*m["f0"]
        if best is None or score>best[0]: best=(score,t,m,ok)
    pick[n]=best; print(n,"->",best[1],"rng %.1f end %+.1f f0 %.0f lvl %.1f pass=%s"%(best[2]["rng"],best[2]["end"],best[2]["f0"],best[2]["lvl"],best[3]),"|",{t:(round(m["rng"],1),round(m["end"],1),round(m["lvl"],1)) for t,m in d.items()})
if "--apply" in sys.argv:
    for n,(sc,t,m,ok) in pick.items():
        w=f"{H}/voice/re{t}.wav"; c=res[n][t]["cue"]; x,sr=sf.read(w); x=x if x.ndim==1 else x[:,0]
        seg=x[max(0,int((c["start"]-0.08)*sr)):int((c["end"]+0.08)*sr)]
        d=tighten(seg,sr,1.06,f"{H}/voice/final/{n}.wav"); print("final",n,t,round(d,2))
