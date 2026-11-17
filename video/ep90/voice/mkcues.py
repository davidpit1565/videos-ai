import json, soundfile as sf, numpy as np
from faster_whisper import WhisperModel
SR=48000; T=1.15
raw=json.load(open('v5-cues.json'))
x,s=sf.read('narration90.wav'); x=x if x.ndim==1 else x[:,0]
m=WhisperModel('small',device='cpu',compute_type='int8')
lines=[]
for c in raw:
    a0,b0=c['start']/T,c['end']/T
    a=max(0,a0-.08); b=min(len(x)/s,b0+.1)
    sf.write('/tmp/_l.wav',x[int(a*s):int(b*s)],s,subtype='PCM_16')
    seg,_=m.transcribe('/tmp/_l.wav',language='en',word_timestamps=True)
    ws=[[w.word.strip(),round(a+w.start,3),round(a+w.end,3)] for sg in seg for w in (sg.words or [])]
    lines.append(dict(n=c['n'],text=c['line'],start=round(a0,3),end=round(b0,3),words=ws)); print(c['n'],ws)
json.dump(dict(lines=lines,D=round(len(x)/s,2)),open('cues.json','w'),indent=1)
