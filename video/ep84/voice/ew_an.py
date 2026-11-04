import json,re,sys,numpy as np,librosa,soundfile as sf
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
rms=lambda x:20*np.log10(np.sqrt(np.mean(x**2))+1e-9); nz=lambda t:re.sub(r"[^a-z0-9]","",t.lower())
def an(p):
    y,s=sf.read(p); y=y.astype(np.float32)
    segs,_=m.transcribe(p,language="en",word_timestamps=True,condition_on_previous_text=False)
    ws=[q for g in segs for q in g.words]
    f0,_,_=librosa.pyin(y,fmin=70,fmax=400,sr=s,frame_length=2048); tt=np.arange(len(f0))*512/s; med=np.nanmedian(f0)
    ok=~np.isnan(f0); st=12*np.log2(f0/med); rng=np.nanpercentile(st[ok],90)-np.nanpercentile(st[ok],10)
    t="".join(q.word for q in ws); g={}; cur="cg"
    for q in ws:
        k=nz(q.word)
        if k.startswith("kept") or k in("kit","kep"): cur="kept"
        elif k=="what": cur="what"
        elif k=="you": cur="you"
        elif k.startswith("trash"): cur="trashed"
        g.setdefault(cur,[]).append(q)
    r=dict(t=t.strip(),match=nz(t)=="chatgptkeptwhatyoutrashed",dur=round(len(y)/s,2),rng=round(float(rng),1),endlvl=round(rms(y[-int(.15*s):])-rms(y),1),lead=round(float(np.where(np.abs(y)>0.02*np.abs(y).max())[0][0]/s),3),w={})
    for k,qs in g.items():
        a,b=qs[0].start,qs[-1].end; sel=(tt>=a)&(tt<=b)&ok
        r["w"][k]=(round(a,2),round(b,2),"d",round(b-a,2),"rms",round(rms(y[int(a*s):int(b*s)+1]),1),"pk",round(float(np.nanmax(st[sel])),1) if sel.any() else None)
    return r,[(q.word,q.start,q.end) for q in ws]
if __name__=="__main__":
    for p in sys.argv[1:]:
        r,w=an(p); print(p.split("/")[-1],json.dumps(r))
