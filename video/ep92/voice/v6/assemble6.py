import json, soundfile as sf, numpy as np, os
V='/home/user/videos-ai/video/ep92/voice/'; SR=48000
x,_=sf.read(V+'narration92.wav'); x=x if x.ndim==1 else x[:,0]
base={l['n']:l for l in json.load(open(V+'cues.json'))['lines']}
ORDER=[1,2,3,4,5]; GAPS=[.25,.22,.22,.28]; LEAD=.07
out=np.zeros(int(40*SR)); t=LEAD; lines=[]
for k,n in enumerate(ORDER):
    c=base[n]; xs=x
    a=max(0,c['start']-.06); b=min(len(xs)/SR,c['end']+.06)
    seg=xs[int(a*SR):int(b*SR)].copy(); m=int(.012*SR); seg[:m]*=np.linspace(0,1,m); seg[-m:]*=np.linspace(1,0,m)
    off=t-(c['start']-a); i0=int(round(off*SR)); out[i0:i0+len(seg)]+=seg
    d=t-c['start']
    lines.append(dict(n=k+1,text=c['text'],orig=n,start=round(t,3),end=round(c['end']+d,3),words=[[w,round(a_+d,3),round(b_+d,3)] for w,a_,b_ in c['words']]))
    t=lines[-1]['end']+(GAPS[k] if k<len(GAPS) else 0)
D=round(lines[-1]["end"]+0.45,2)
sf.write('narration92v6.wav',out[:int(D*SR)],SR,subtype='PCM_16')
json.dump(dict(lines=lines,D=D),open('cues6.json','w'),indent=1)
json.dump([dict(n=l['n'],line=l['text'],start=l['start'],end=l['end'],words=l['words']) for l in lines],open('narration92v6-cues.json','w'),indent=1)
print(D,[(l['n'],l['start'],l['end']) for l in lines])
for l in lines: print(l['n'],[w[0] for w in l['words']])
