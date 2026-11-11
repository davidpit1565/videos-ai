#!/usr/bin/env python3
"""Measure the real vertical scroll of the recording (frame to frame row-shift on a half-res grey copy). Writes scroll.json: src time -> scaled-px scroll (1080-wide space)."""
import subprocess, json, numpy as np
SRC="/root/.claude/uploads/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/739398dd-ScreenRecording_11-11-2026_05-10-31_1.mp4"
T0,T1,FPS=8.0,13.97,30
w,h=540,1174
p=subprocess.run(["ffmpeg","-v","error","-ss",str(T0),"-t",str(T1-T0),"-i",SRC,"-vf",f"fps={FPS},scale={w}:{h},format=gray","-f","rawvideo","-"],capture_output=True).stdout
fr=np.frombuffer(p,np.uint8).reshape(-1,h,w).astype(np.float32)
print(len(fr))
band=slice(15,w-15); y0,y1=175,1020
tot=0.0; out=[[T0,0.0]]
for i in range(1,len(fr)):
    a,b=fr[i-1][:,band],fr[i][:,band]
    best=None
    for s in range(0,70):
        # content moved up by s: cur[y]=prev[y+s]
        d=np.abs(a[y0+s:y1+s]-b[y0:y1]).mean()
        if best is None or d<best[0]: best=(d,s)
    d0=np.abs(a[y0:y1]-b[y0:y1]).mean()
    s=best[1] if best[0]<d0*0.85 else 0
    tot+=s*2; out.append([T0+i/FPS,tot])
json.dump(out,open("scroll_raw.json","w"))
print(out[::10]); print(tot)
