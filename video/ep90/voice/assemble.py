"""narration90.wav = the one render (v5.wav, atempo 1.15 -> v5-fast.wav) re-joined with readable gaps; cues.json from whisper words (mkcues.py output scaled)."""
import json, soundfile as sf, numpy as np, sys
SR=48000
x,s=sf.read('v5-fast.wav'); x=x if x.ndim==1 else x[:,0]
base=json.load(open('cues-fast-raw.json'))['lines']
GAPS=[.34,.34,.34,.40,.85,.85]      # silence after lines 1..6 (between end of one and start of next)
LEAD=.07
out=np.zeros(int(40*SR)); t=LEAD; lines=[]
for i,c in enumerate(base):
    a=max(0,c['start']-.06); b=min(len(x)/SR,c['end']+.06)
    seg=x[int(a*SR):int(b*SR)].copy(); n=int(.012*SR); seg[:n]*=np.linspace(0,1,n); seg[-n:]*=np.linspace(1,0,n)
    off=t-(c['start']-a)                   # file time of the slice start so that voice start lands at t
    i0=int(round(off*SR)); out[i0:i0+len(seg)]+=seg
    d=t-c['start']
    lines.append(dict(n=c['n'],text=c['text'],start=round(t,3),end=round(c['end']+d,3),words=[[w,round(a_+d,3),round(b_+d,3)] for w,a_,b_ in c['words']]))
    t=lines[-1]['end']+(GAPS[i] if i<len(GAPS) else 0)
D=round(lines[-1]['end']+.5,2)
sf.write('narration90.wav',out[:int(D*SR)],SR,subtype='PCM_16')
json.dump(dict(lines=lines,D=D),open('cues.json','w'),indent=1)
print(D,[(l['n'],l['start'],l['end']) for l in lines])
