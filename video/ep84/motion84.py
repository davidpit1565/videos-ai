import subprocess,sys,numpy as np
mp4=sys.argv[1]; fps=10; w,h=108,192
raw=subprocess.run(['ffmpeg','-v','error','-i',mp4,'-vf',f'fps={fps},scale={w}:{h},format=gray','-f','rawvideo','-'],capture_output=True).stdout
f=np.frombuffer(raw,dtype=np.uint8).reshape(-1,h,w).astype(np.float32)
d=np.abs(np.diff(f,axis=0)).mean(axis=(1,2)); still=d<0.15
print("frames",len(f),"still share %.0f%%"%(100*still.mean()))
run=0;start=0;res=[]
for i,s in enumerate(still):
    if s:
        if run==0:start=i
        run+=1
    else:
        if run/fps>2.5: res.append((start/fps,run/fps))
        run=0
if run/fps>2.5: res.append((start/fps,run/fps))
print("still stretches >2.5s:",res or "none")
print("per-second mean diff:",[round(float(d[i:i+fps].mean()),2) for i in range(0,len(d),fps)])
