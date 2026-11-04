import sys,json,os,time,soundfile as sf
sys.path.insert(0,"/home/user/videos-ai/video/ep82")
from tighten import tighten
H=os.path.dirname(os.path.abspath(__file__))
EX=json.load(open(H+"/takes_ex.json"))
def fin(n,tk,notes="",out=None):
    w=f"{H}/takes/t{tk}.wav"; c=json.load(open(w[:-4]+"-cues.json"))[n-1]
    x,sr=sf.read(w); x=x if x.ndim==1 else x[:,0]
    seg=x[max(0,int((c["start"]-0.08)*sr)):int((c["end"]+0.08)*sr)]
    out=out or f"{H}/final/{n}.wav"
    d=tighten(seg,sr,1.0,out)
    ex=EX[tk][n] if n in (1,2) else EX[tk][0]
    if out.endswith(f"/final/{n}.wav"):
        st=json.load(open(H+"/status.json"))
        st["lines"][str(n)]=dict(state="done",seed=int(tk)+n,take_seed=tk,exaggeration=ex,take=f"{H}/takes/t{tk}.wav",final=out,dur=round(d,2),notes=notes)
        json.dump(st,open(H+"/status.json","w"),indent=1)
        open(H+"/progress.txt","a").write(f"line {n} final from take {tk} dur {d:.2f}s {time.strftime('%T')}\n")
    print(n,tk,round(d,2),ex); return d
if __name__=="__main__":
    for p in sys.argv[1:]:
        n,tk=p.split(":"); fin(int(n),tk,"interim from take 8401 (first whole-script roll), more seeds rolling")
