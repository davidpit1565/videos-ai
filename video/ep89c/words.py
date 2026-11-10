import json, soundfile as sf, numpy as np, subprocess
SR=48000
x,s=sf.read('/home/user/videos-ai/video/ep89b/voice/narration-fast.wav'); x=x if x.ndim==1 else x[:,0]
cues=json.load(open('/home/user/videos-ai/video/ep89b/voice/cues-fast.json'))
from faster_whisper import WhisperModel
m=WhisperModel('small',device='cpu',compute_type='int8')
out={}
for c in cues:
    a=max(0,c['start']-.08); b=c['end']+.1
    sf.write('/tmp/_l.wav',x[int(a*SR):int(b*SR)],SR,subtype='PCM_16')
    seg,_=m.transcribe('/tmp/_l.wav',language='en',word_timestamps=True)
    ws=[[w.word.strip(),round(a+w.start,3),round(a+w.end,3)] for s_ in seg for w in (s_.words or [])]
    out[c['n']]=ws; print(c['n'],ws)
json.dump(out,open('/home/user/videos-ai/video/ep89c/voice/words.json','w'))
