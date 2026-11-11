#!/usr/bin/env python3
"""WCAG contrast of the recording's text before/after the LUT (same curve in R,G,B). Frame at src 9.0 s, 1080x2348 space."""
import sys, subprocess, numpy as np
sys.argv=[sys.argv[0],"voice/cues-noVoice.json"]
import build92 as b
fr=b.one_frame(9.0).astype(float); out=b.LUT[b.one_frame(9.0)].astype(float)
def lum(v):
    c=v/255.0; c=np.where(c<=0.03928,c/12.92,((c+0.055)/1.055)**2.4); return 0.2126*c[...,0]+0.7152*c[...,1]+0.0722*c[...,2]
def ratio(a,bg): return (lum(a)+0.05)/(lum(bg)+0.05)
regions={"body text (answer, rows 813-1513)":(813,1513,30,1050),"bold offer lines (1799-2051)":(1799,2051,30,1050),"bubble (user question) text":(388,560,360,1040)}
for name,(y0,y1,x0,x1) in regions.items():
    a=fr[y0:y1,x0:x1].reshape(-1,3); o=out[y0:y1,x0:x1].reshape(-1,3)
    g=a.mean(1); 
    if "bubble" in name:
        bg=np.median(a,axis=0); idx=g>np.percentile(g,97); 
    else:
        bg=np.array([0,0,0.]); idx=g>np.percentile(g,99)
    t0=np.median(a[idx],axis=0); t1=np.median(o[idx],axis=0); bgo=np.median(o,axis=0) if "bubble" in name else bg
    print(f"{name}: text rgb {t0.round()} -> {t1.round()}; bg {bg.round()} -> {bgo.round()}; WCAG {ratio(t0,bg):.2f}:1 -> {ratio(t1,bgo):.2f}:1")
bgmax=fr[400:500,30:300].max(); print("pure black bg check: max in empty area",bgmax)
