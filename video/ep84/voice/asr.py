import glob,json,os,re,sys,numpy as np,librosa
from faster_whisper import WhisperModel
H=os.path.dirname(os.path.abspath(__file__))
L=[l.strip() for l in open(H+"/../lines.txt") if l.strip()]
m=WhisperModel("small",device="cpu",compute_type="int8")
nz=lambda s:re.findall(r"[a-z0-9']+",s.lower())
f=H+"/asr.json"; res=json.load(open(f)) if os.path.exists(f) else {}
for w in sorted(glob.glob(H+"/takes/t*.wav")):
    if os.path.getsize(w)==0: continue
    tk=os.path.basename(w)[1:-4]; cj=w[:-4]+"-cues.json"
    if not os.path.exists(cj): continue
    y,sr=librosa.load(w,sr=16000)
    for c in json.load(open(cj)):
        n=str(c["n"])
        if tk in res.get(n,{}): continue
        seg=y[int(max(0,c["start"]-.1)*sr):int((c["end"]+.1)*sr)]
        segs,_=m.transcribe(seg,language="en",beam_size=5,condition_on_previous_text=False)
        t=" ".join(s.text for s in segs).strip()
        a,b=nz(L[c["n"]-1]),nz(t)
        # word edit distance
        d=np.zeros((len(a)+1,len(b)+1),int); d[:,0]=range(len(a)+1); d[0,:]=range(len(b)+1)
        for i in range(1,len(a)+1):
            for j in range(1,len(b)+1): d[i,j]=min(d[i-1,j]+1,d[i,j-1]+1,d[i-1,j-1]+(a[i-1]!=b[j-1]))
        res.setdefault(n,{})[tk]=dict(t=t,wer=float(d[-1,-1]/len(a)))
json.dump(res,open(f,"w"),indent=1)
