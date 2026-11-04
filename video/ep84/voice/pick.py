import glob,json,os,sys,numpy as np,librosa
H=os.path.dirname(os.path.abspath(__file__))
def metrics(wav,c):
    a,b=c["start"],c["end"]; y,sr=librosa.load(wav,sr=16000,offset=a,duration=b-a)
    f0,_,_=librosa.pyin(y,fmin=70,fmax=400,sr=sr,frame_length=1024); ok=~np.isnan(f0)
    if ok.sum()<10: return None
    med=np.nanmedian(f0); st=12*np.log2(f0/med); rng=np.nanpercentile(st[ok],90)-np.nanpercentile(st[ok],10)
    t=np.arange(len(f0))*512/sr; tail=(t>=(b-a)-0.7)&ok; end=float(np.nanmean(st[tail])) if tail.sum()>2 else 0.0
    return dict(rng=float(rng),end=end,f0=float(med),dur=b-a)
mf=H+"/metrics.json"; res=json.load(open(mf)) if os.path.exists(mf) else {}
for w in sorted(glob.glob(H+"/takes/t*.wav")):
    tk=os.path.basename(w)[1:-4]; cj=w[:-4]+"-cues.json"
    if not os.path.exists(cj): continue
    cues=json.load(open(cj))
    for c in cues:
        n=str(c["n"])
        if tk in res.get(n,{}): continue
        m=metrics(w,c)
        if m: res.setdefault(n,{})[tk]=m
json.dump(res,open(mf,"w"),indent=1)
for n in sorted(res,key=int):
    print(n,{t:(round(m["rng"],1),round(m["end"],1),round(m["dur"],2)) for t,m in res[n].items()})
