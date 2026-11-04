import json,os,subprocess,sys,numpy as np,soundfile as sf
H="/home/user/videos-ai/video/ep84/voice"
def edit(tk,out,cg=0.58,tr=0.65,g=dict(cg=0,kept=2,what=-2,you=-4,trashed=5),gap=0.0):
    w=json.load(open(H+"/fw_res.json"))[tk]["w"]; x,sr=sf.read(f"{H}/frcut/{tk}.wav"); x=x.astype(np.float64)
    order=["cg","kept","what","you","trashed"]
    # boundaries at midpoints between words
    b=[0.0]
    for a,c in zip(order[:-1],order[1:]): b.append((w[a]["e"]+w[c]["s"])/2)
    b.append(len(x)/sr)
    parts=[]
    for i,k in enumerate(order):
        seg=x[int(b[i]*sr):int(b[i+1]*sr)]*10**(g[k]/20)
        d=len(seg)/sr; tgt={"cg":cg,"trashed":tr}.get(k)
        if tgt:
            if k=="cg": tgt=max(tgt,0.01)+ (d-(w[k]["e"]-w[k]["s"]))  # keep surrounding pauses
            if k=="trashed": tgt=tgt+(d-(w[k]["e"]-w[k]["s"]))
            sp=min(2.0,max(0.5,d/tgt))
            if abs(sp-1)>0.02:
                tmp=out+".p.wav"; sf.write(tmp,seg,sr,subtype="PCM_16")
                subprocess.run(["ffmpeg","-v","error","-y","-i",tmp,"-filter:a",f"atempo={sp}","-ar",str(sr),tmp+".o.wav"],check=True)
                seg,_=sf.read(tmp+".o.wav"); os.remove(tmp); os.remove(tmp+".o.wav")
        parts.append(seg)
    f=int(0.02*sr); y=parts[0]
    for p in parts[1:]:
        p=p.copy(); n=min(f,len(y),len(p)); fi=np.linspace(0,1,n)
        y=np.concatenate([y[:-n],y[-n:]*(1-fi)+p[:n]*fi,p[n:]])
    y=np.clip(y,-0.99,0.99); sf.write(out,y,sr,subtype="PCM_16"); return len(y)/sr
if __name__=="__main__":
    for tk in sys.argv[1:]: print(tk,edit(tk,f"{H}/frcut/e{tk}.wav"))
