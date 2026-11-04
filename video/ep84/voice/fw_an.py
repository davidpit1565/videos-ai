import glob,json,os,re,sys,numpy as np,librosa,soundfile as sf
sys.path.insert(0,"/home/user/videos-ai/video/ep82")
from tighten import tighten
from faster_whisper import WhisperModel
H=os.path.dirname(os.path.abspath(__file__)); m=WhisperModel("small",device="cpu",compute_type="int8")
out=H+"/fw_res.json"; res=json.load(open(out)) if os.path.exists(out) else {}
rms=lambda x:20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
nz=lambda t:re.sub(r"[^a-z0-9]","",t.lower())
for w in sorted(glob.glob(H+"/takes/f*.wav")):
    tk=os.path.basename(w)[1:-4]
    if tk in res or not os.path.exists(w[:-4]+"-cues.json"): continue
    p=f"{H}/frcut/{tk}.wav"
    if not os.path.exists(p):
        c=json.load(open(w[:-4]+"-cues.json"))[0]; x,sr=sf.read(w); x=x if x.ndim==1 else x[:,0]
        tighten(x[max(0,int((c["start"]-0.08)*sr)):int((c["end"]+0.08)*sr)],sr,1.0,p)
    y,s=sf.read(p); y=y.astype(np.float32)
    segs,_=m.transcribe(p,language="en",word_timestamps=True,condition_on_previous_text=False)
    ws=[q for g in segs for q in g.words]
    f0,_,_=librosa.pyin(y,fmin=70,fmax=400,sr=s,frame_length=2048); tt=np.arange(len(f0))*512/s; med=np.nanmedian(f0)
    t="".join(q.word for q in ws); r=dict(t=t.strip(),match=nz(t)=="chatgptkeptwhatyoutrashed",dur=round(len(y)/s,2))
    # group words
    toks=[(nz(q.word),q) for q in ws]; groups={}; cur="cg"; 
    for k,q in toks:
        if k.startswith("kept") or k in("kit","kep"): cur="kept"
        elif k=="what": cur="what"
        elif k=="you": cur="you"
        elif k.startswith("trash"): cur="trashed"
        groups.setdefault(cur,[]).append(q)
    wd={}
    for g,qs in groups.items():
        a,b=qs[0].start,qs[-1].end; seg=y[int(a*s):int(b*s)+1]; sel=(tt>=a)&(tt<=b)&~np.isnan(f0)
        wd[g]=dict(s=round(a,2),e=round(b,2),d=round(b-a,2),rms=round(rms(seg),1),pk=round(float(12*np.log2(np.nanmax(f0[sel])/med)),1) if sel.any() else None)
    r["w"]=wd; r["endlvl"]=round(rms(y[-int(.15*s):])-rms(y),1)
    res[tk]=r
json.dump(res,open(out,"w"),indent=1)
for tk,r in res.items():
    if r["match"]: print(tk,r["dur"],r["endlvl"],{g:(v["d"],v["rms"],v["pk"]) for g,v in r["w"].items()})
