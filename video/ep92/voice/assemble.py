"""narration92.wav = the one TTS render (v1.wav, atempo 1.12 -> v1-fast.wav) re-joined with gaps timed to the picture; cues.json from whisper word times (mkcues.py)."""
import json, soundfile as sf, numpy as np
SR=48000
x,s=sf.read('v1-fast.wav'); x=x if x.ndim==1 else x[:,0]
base=json.load(open('cues-fast-raw2.json'))['lines']
GAPS=[2.45,.34,.55,.45]      # silence after lines 1..4 (line 1 -> 2 covers rewind, typing, send)
LEAD=.07
out=np.zeros(int(40*SR)); t=LEAD; lines=[]
for i,c in enumerate(base):
    xs=sf.read(c['src'])[0] if 'src' in c else x; xs=xs if xs.ndim==1 else xs[:,0]
    a=max(0,c['start']-.06); b=min(len(xs)/SR,c['end']+.06)
    seg=xs[int(a*SR):int(b*SR)].copy(); n=int(.012*SR); seg[:n]*=np.linspace(0,1,n); seg[-n:]*=np.linspace(1,0,n)
    off=t-(c['start']-a); i0=int(round(off*SR)); out[i0:i0+len(seg)]+=seg
    d=t-c['start']
    lines.append(dict(n=c['n'],text=c['text'],start=round(t,3),end=round(c['end']+d,3),words=[[w,round(a_+d,3),round(b_+d,3)] for w,a_,b_ in c['words']]))
    t=lines[-1]['end']+(GAPS[i] if i<len(GAPS) else 0)
D=round(lines[-1]['end']+.5,2)
sf.write('narration92.wav',out[:int(D*SR)],SR,subtype='PCM_16')
json.dump(dict(lines=lines,D=D),open('cues.json','w'),indent=1)
print(D,[(l['n'],l['start'],l['end']) for l in lines])
