import glob,json,os,re,numpy as np,librosa
from faster_whisper import WhisperModel
H=os.path.dirname(os.path.abspath(__file__)); L=[open(H+"/h1.txt").read().strip()]; N=[1]
m=WhisperModel("small",device="cpu",compute_type="int8")
nz=lambda s:re.sub(r"[^a-z0-9]","",s.lower())
out=H+"/nn_res.json"; res=json.load(open(out)) if os.path.exists(out) else {}
rms=lambda x:20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
for w in sorted(glob.glob(H+"/takes/n*.wav")):
    tk=os.path.basename(w)[1:-4]
    if tk in res or not os.path.exists(w[:-4]+"-cues.json"): continue
    y,sr=librosa.load(w,sr=16000); r={}
    for c in json.load(open(w[:-4]+"-cues.json")):
        i=c["n"]-1; a,b=c["start"],c["end"]; s=y[int(max(0,a-.1)*sr):int((b+.1)*sr)]
        segs,_=m.transcribe(s,language="en",beam_size=5,condition_on_previous_text=False); t=" ".join(x.text for x in segs).strip()
        yy=y[int(a*sr):int(b*sr)]; f0,_,_=librosa.pyin(yy,fmin=70,fmax=400,sr=sr,frame_length=1024); ok=~np.isnan(f0)
        med=np.nanmedian(f0); st=12*np.log2(f0/med); rng=np.nanpercentile(st[ok],90)-np.nanpercentile(st[ok],10)
        tt=np.arange(len(f0))*512/sr; tail=(tt>=(b-a)-0.7)&ok
        r[N[i]]=dict(t=t,match=nz(t)==nz(L[i]),rng=round(float(rng),1),end=round(float(np.nanmean(st[tail])),1),dur=round(b-a,2),endlvl=round(rms(yy[-int(.15*sr):])-rms(yy),1))
    res[tk]=r
json.dump(res,open(out,"w"),indent=1)
for tk,r in res.items():
    for n,v in r.items(): print(tk,n,v)
