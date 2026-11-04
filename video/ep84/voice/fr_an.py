import glob,json,os,re,sys,numpy as np,librosa,soundfile as sf
sys.path.insert(0,"/home/user/videos-ai/video/ep82")
from tighten import tighten
from faster_whisper import WhisperModel
H=os.path.dirname(os.path.abspath(__file__)); m=WhisperModel("small",device="cpu",compute_type="int8")
out=H+"/fr_res.json"; res=json.load(open(out)) if os.path.exists(out) else {}
os.makedirs(H+"/frcut",exist_ok=True)
rms=lambda x:20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
for w in sorted(glob.glob(H+"/takes/f*.wav")):
    tk=os.path.basename(w)[1:-4]
    if tk in res or not os.path.exists(w[:-4]+"-cues.json"): continue
    c=json.load(open(w[:-4]+"-cues.json"))[0]; x,sr=sf.read(w); x=x if x.ndim==1 else x[:,0]
    p=f"{H}/frcut/{tk}.wav"; d=tighten(x[max(0,int((c["start"]-0.08)*sr)):int((c["end"]+0.08)*sr)],sr,1.0,p)
    y,s=sf.read(p); y=y.astype(np.float32)
    segs,_=m.transcribe(p,language="en",word_timestamps=True,condition_on_previous_text=False)
    ws=[q for g in segs for q in g.words]; txt="".join(q.word for q in ws)
    nz=lambda t:re.sub(r"[^a-z0-9]","",t.lower())
    fl=[nz(q.word) for q in ws]
    # first word = merge until 'kept'
    k=next((i for i,q in enumerate(fl) if q.startswith("kept")),None)
    fw_end=ws[k].start if k else None
    env=np.abs(y); idx=np.where(env>0.02*env.max())[0]; lead=idx[0]/s
    f0,_,_=librosa.pyin(y,fmin=70,fmax=400,sr=s,frame_length=2048); ok=~np.isnan(f0); med=np.nanmedian(f0); st=12*np.log2(f0/med)
    rng=np.nanpercentile(st[ok],90)-np.nanpercentile(st[ok],10); tt=np.arange(len(f0))*512/s; tail=(tt>=len(y)/s-0.5)&ok
    res[tk]=dict(t=txt.strip(),match=nz(txt)=="chatgptkeptwhatyoutrashed",dur=round(len(y)/s,2),firstword=round(fw_end-ws[0].start,2) if fw_end else None,lead=round(lead,3),rng=round(float(rng),1),end=round(float(np.nanmean(st[tail])),1),endlvl=round(rms(y[-int(.15*s):])-rms(y),1),rise=round(rms(y[int(.0*s):int(.3*s)])-rms(y),1),words=[(q.word,round(q.start,2),round(q.end,2)) for q in ws])
json.dump(res,open(out,"w"),indent=1)
for tk,r in res.items(): print(tk,{k:v for k,v in r.items() if k!="words"})
