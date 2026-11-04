import glob,json,os,re,sys,numpy as np,librosa,soundfile as sf
sys.path.insert(0,"/home/user/videos-ai/video/ep82")
from tighten import tighten
from faster_whisper import WhisperModel
H=os.path.dirname(os.path.abspath(__file__)); m=WhisperModel("small",device="cpu",compute_type="int8")
out=H+"/seg_res.json"; res=json.load(open(out)) if os.path.exists(out) else {}
os.makedirs(H+"/segcut",exist_ok=True)
rms=lambda x:20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
nz=lambda t:re.sub(r"[^a-z0-9]","",t.lower())
exp=["chatgptkept","whatyou","trashed"]
for w in sorted(glob.glob(H+"/takes/s*.wav")):
    tk=os.path.basename(w)[1:-4]
    if tk in res or not os.path.exists(w[:-4]+"-cues.json"): continue
    x,sr=sf.read(w); x=x if x.ndim==1 else x[:,0]; r={}
    for c in json.load(open(w[:-4]+"-cues.json")):
        n=c["n"]; p=f"{H}/segcut/{tk}_{n}.wav"
        d=tighten(x[max(0,int((c["start"]-0.08)*sr)):int((c["end"]+0.08)*sr)],sr,1.0,p)
        segs,_=m.transcribe(p,language="en",word_timestamps=True,condition_on_previous_text=False)
        ws=[q for g in segs for q in g.words]; t="".join(q.word for q in ws)
        y,s=sf.read(p); y=y.astype(np.float32)
        f0,_,_=librosa.pyin(y,fmin=70,fmax=400,sr=s,frame_length=2048); tt=np.arange(len(f0))*512/s
        per=[]
        for q in ws:
            seg=y[int(q.start*s):max(int(q.end*s),int(q.start*s)+100)]; sel=(tt>=q.start)&(tt<=q.end)&~np.isnan(f0)
            per.append((q.word.strip(),round(q.start,2),round(q.end,2),round(rms(seg),1),round(float(np.nanmax(f0[sel])),0) if sel.any() else None))
        rg=np.nanpercentile(12*np.log2(f0[~np.isnan(f0)]/np.nanmedian(f0)),90)-np.nanpercentile(12*np.log2(f0[~np.isnan(f0)]/np.nanmedian(f0)),10)
        r[n]=dict(t=t.strip(),match=nz(t)==exp[n-1],dur=round(d,2),rng=round(float(rg),1),endlvl=round(rms(y[-int(.15*s):])-rms(y),1),words=per)
    res[tk]=r
json.dump(res,open(out,"w"),indent=1)
for tk,r in res.items():
    for n,v in r.items(): print(tk,n,v["match"],v["t"],v["dur"],"rng",v["rng"],"end",v["endlvl"],v["words"])
