#!/usr/bin/env python3
"""Per-line pick across whole-script takes by voice_quality's numbers (pitch range, end), then tighten the chosen lines into voice/final/N.wav."""
import glob,json,os,sys,numpy as np,subprocess
import librosa,soundfile as sf
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H)
from tighten import tighten
HOOK={1,3,6,7}
def metrics(wav,c):
    a,b=c["start"],c["end"]; y,sr=librosa.load(wav,sr=16000,offset=a,duration=b-a)
    f0,_,_=librosa.pyin(y,fmin=70,fmax=400,sr=sr,frame_length=1024); ok=~np.isnan(f0)
    if ok.sum()<10: return None
    med=np.nanmedian(f0); st=12*np.log2(f0/med); rng=np.nanpercentile(st[ok],90)-np.nanpercentile(st[ok],10)
    t=np.arange(len(f0))*512/sr; tail=(t>=(b-a)-0.7)&ok; end=float(np.nanmean(st[tail])) if tail.sum()>2 else 0.0
    return dict(rng=float(rng),end=end,f0=float(med),dur=b-a)
def main():
    res={}
    takes=sorted(glob.glob(H+"/voice/take8*.wav"))
    for w in takes:
        cj=w[:-4]+"-cues.json"
        if not os.path.exists(cj): continue
        cues=json.load(open(cj)); tk=os.path.basename(w)[4:-4]
        for c in cues:
            m=metrics(w,c)
            if m: res.setdefault(c["n"],{})[tk]=dict(m,cue=c)
    json.dump({str(k):{t:{x:y for x,y in v.items() if x!="cue"} for t,v in d.items()} for k,d in res.items()},open(H+"/voice/metrics.json","w"),indent=1)
    pick={}
    for n,d in sorted(res.items()):
        best=None
        for t,m in d.items():
            cap=10.0 if n in HOOK else 9.0
            ok=(m["rng"]<=cap) and (m["end"]>=-3.5)
            score=(0 if ok else -100)+min(m["rng"],cap-0.5)+0.8*max(-3.5,min(2,m["end"]))+0.02*m["f0"]
            if best is None or score>best[0]: best=(score,t,m,ok)
        pick[n]=best; print(n,"->",best[1],"rng %.1f end %+.1f f0 %.0f pass=%s"%(best[2]["rng"],best[2]["end"],best[2]["f0"],best[3]),"| options:",{t:(round(m["rng"],1),round(m["end"],1)) for t,m in d.items()})
    if "--apply" in sys.argv:
        os.makedirs(H+"/voice/final",exist_ok=True); tot=0
        for n,(sc,t,m,ok) in pick.items():
            w=f"{H}/voice/take{t}.wav"; c=res[n][t]["cue"]; x,sr=sf.read(w); x=x if x.ndim==1 else x[:,0]
            seg=x[max(0,int((c["start"]-0.08)*sr)):int((c["end"]+0.08)*sr)]
            d=tighten(seg,sr,1.06,f"{H}/voice/final/{n}.wav"); print("final",n,t,round(d,2))
        json.dump({str(n):v[1] for n,v in pick.items()},open(H+"/voice/picked.json","w"))

if __name__=='__main__':
    main()
