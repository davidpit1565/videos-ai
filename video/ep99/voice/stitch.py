import json,glob,os,numpy as np,soundfile as sf,sys
D='/home/user/videos-ai/video/ep99/voice/'
lines=[l.rstrip('\n') for l in open(D+'lines.txt') if l.strip()]
out=[];cues=[];t=0.0;sr=None
gap=0.07
targets={}
import sys
try:
    if '--notargets' in sys.argv: raise Exception('notargets')
    targets={int(k):v for k,v in json.load(open('/home/user/videos-ai/video/ep99/cues99.json'))['targets'].items()}
except Exception as e: print('no targets',e)
for i,l in enumerate(lines,1):
    seed=open(D+f'pl/L{i}.ok').read().strip()
    w,s=sf.read(D+f'pl/L{i}-{seed}.wav'); sr=sr or s
    if w.ndim>1:w=w.mean(1)
    c=json.load(open(D+f'pl/L{i}-{seed}-cues.json'))[0]
    a=max(0,int((c['start']-0.04)*sr)); b=min(len(w),int((c['end']+0.08)*sr))
    seg=w[a:b].copy(); f=int(0.012*sr); seg[:f]*=np.linspace(0,1,f); seg[-f:]*=np.linspace(1,0,f)
    want=targets.get(i)
    if want is not None and want>t+0.04:
        pad=want-(t+0.04); out.append(np.zeros(int(pad*sr))); t+=pad
    out.append(seg); out.append(np.zeros(int(gap*sr)))
    cues.append({'n':i,'line':l,'start':round(t+0.04,3),'end':round(t+len(seg)/sr-0.08,3)})
    t+=(len(seg)/sr)+gap
y=np.concatenate(out); sf.write(D+'narration-raw.wav',y,sr,subtype='PCM_16')
json.dump(cues,open(D+'narration-raw-cues.json','w'),indent=1)
print(sr,round(len(y)/sr,2),[(c['n'],round(c['end']-c['start'],2)) for c in cues])
