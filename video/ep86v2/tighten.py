import soundfile as sf, numpy as np, subprocess, os, sys, json
H=os.path.dirname(os.path.abspath(__file__))
def tighten(x,sr,sp,out):
    h=int(sr*0.01); fr=len(x)//h
    db=np.array([20*np.log10(np.sqrt(np.mean(x[i*h:(i+1)*h]**2))+1e-9) for i in range(fr)])
    loud=db>-42; idx=np.where(loud)[0]; a=max(0,idx[0]-3); b=min(fr,idx[-1]+4)
    o=[]; i=a
    while i<b:
        if loud[i]: o.append(x[i*h:(i+1)*h]); i+=1; continue
        j=i
        while j<b and not loud[j]: j+=1
        run=j-i; keep=run if run<=22 else 15
        o.append(x[i*h:(i+keep)*h]); i=j
    y=np.concatenate(o); f=int(sr*0.004); y[:f]*=np.linspace(0,1,f); y[-f:]*=np.linspace(1,0,f)
    tmp=out+".t.wav"; sf.write(tmp,y,sr,subtype="PCM_16")
    subprocess.run(["ffmpeg","-v","error","-y","-i",tmp,"-filter:a",f"atempo={sp}","-ar","48000","-ac","1","-c:a","pcm_s16le",out],check=True); os.remove(tmp)
    return len(y)/sr/sp
if __name__=="__main__":
    src,cues,order,dst=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]   # order: "1:1,3:2,2:3,..." srcline:finalpos
    x,sr=sf.read(src); x=x if x.ndim==1 else x[:,0]; c=json.load(open(cues))
    SP={1:1.06,2:1.06,3:1.06,4:1.06,5:1.06,6:1.06,7:1.06}
    for pair in order.split(","):
        s,f=map(int,pair.split(":")); L=c[s-1]; seg=x[max(0,int((L["start"]-0.08)*sr)):int((L["end"]+0.08)*sr)]
        print(s,"->",f,round(tighten(seg,sr,SP.get(s,1.06),f"{dst}/{f}.wav"),2))
