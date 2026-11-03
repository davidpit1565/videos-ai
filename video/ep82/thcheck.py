import sys,json,glob,os,numpy as np,subprocess
sys.path.insert(0,'/home/user/videos-ai/audio')
import burst
from faster_whisper import WhisperModel
M=WhisperModel("base.en",device="cpu",compute_type="int8")
def stdb(y,sr,hop=0.01,win=0.03):
    h,w=int(hop*sr),int(win*sr); n=max(1,(len(y)-w)//h)
    return np.array([20*np.log10(np.sqrt(np.mean(y[i*h:i*h+w]**2))+1e-9) for i in range(n)])
def check(wav,a,b):
    import librosa
    y,sr=librosa.load(wav,sr=16000,offset=max(0,a-0.05),duration=b-a+0.1); y=y/(np.abs(y).max()+1e-9)
    segs,_=M.transcribe(y,word_timestamps=True,language="en")
    ws=[w for s in segs for w in s.words]
    w=burst.find([dict(word=x.word,start=x.start,end=x.end) for x in ws],"three")
    if not w: return dict(found=False,heard=[x.word for x in ws])
    db=stdb(y,sr); med=float(np.median(db[db>-45]))
    ws0,we0=w["start"],w["end"]; i0,i1=int(ws0*100),int(we0*100)+1; wk=float(db[i0:i1].max()) if i1>i0 else float('nan')
    r=burst.measure(y,ws0,we0-ws0)
    return dict(found=True,heard=[x.word for x in ws],word_over_median_db=round(wk-med,1),burst=r,verdict=burst.verdict(r))
if __name__=="__main__":
    out={}
    for w in sorted(glob.glob(sys.argv[1])):
        cj=w[:-4]+"-cues.json"
        if not os.path.exists(cj): continue
        cues=json.load(open(cj))
        for c in cues:
            if "three" in c["line"].lower():
                out[f"{os.path.basename(w)}#{c['n']}"]=r=check(w,c["start"],c["end"]); print(os.path.basename(w),c["n"],r,flush=True)
    json.dump(out,open(sys.argv[2],'w'),indent=1)
