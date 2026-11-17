#!/usr/bin/env python3
"""Real vertical scroll of the recording, by matching text-line tops against the document's line tops (robust to fast scroll).
Writes scroll.json = [[src_time, scroll_px_in_1080_space], ...] at 30 fps from 8.0 s."""
import subprocess, json, numpy as np
SRC="/root/.claude/uploads/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/739398dd-ScreenRecording_11-11-2026_05-10-31_1.mp4"
T0,T1,FPS=8.0,13.97,30; W,H=1080,2348
# doc line tops (scroll 0), measured on the 9.0 s frame and the final frame (final scroll 825)
DOC=[388,457,529,705,813,877,984,1049,1113,1220,1286,1349,1414,1479,1587,1694,1799,1864,1928,1985]
DOC+= [t+825 for t in (1277,1341,1406,1513,1579,1685,1794)]
DOC=np.array(DOC,float)
p=subprocess.run(["ffmpeg","-v","error","-ss",str(T0),"-t",str(T1-T0),"-i",SRC,"-vf",f"fps={FPS},scale={W}:{H},format=gray","-f","rawvideo","-"],capture_output=True).stdout
fr=np.frombuffer(p,np.uint8).reshape(-1,H,W)
def tops(im):
    m=(im[330:2090,30:700]>60).sum(1)>0
    t=[]; prev=False
    for y,v in enumerate(m):
        if v and not prev: t.append(y+330)
        prev=v
    return np.array(t,float)
out=[]; last=0
for i in range(len(fr)):
    tp=tops(fr[i]); best=(-1,last)
    for s in range(max(0,last-60),901):
        d=np.abs((tp[:,None]+s)-DOC[None,:]).min(1)
        score=(d<=4).sum()
        if score>best[0] or (score==best[0] and abs(s-last-30)<abs(best[1]-last-30)): best=(score,s)
    last=best[1]; out.append([T0+i/FPS,float(last),int(best[0]),len(tp)])
json.dump([[a,b] for a,b,c,d in out],open("scroll.json","w"))
for o in out[::6]: print(o)
