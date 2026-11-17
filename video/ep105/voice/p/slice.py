import json,sys,soundfile as sf
from faster_whisper import WhisperModel
m=WhisperModel('small.en',device='cpu',compute_type='int8')
for sd in sys.argv[1:]:
    c=json.load(open(f'P{sd}-cues.json')); w,sr=sf.read(f'P{sd}.wav')
    if w.ndim>1: w=w.mean(1)
    for i,x in enumerate(c):
        a=max(0,int((x['start']-.05)*sr)); b=int((x['end']+.08)*sr); f=f'S{i+1}-{sd}.wav'
        sf.write(f,w[a:b],sr)
        segs,_=m.transcribe(f,word_timestamps=True,language='en'); ws=[q for s_ in segs for q in s_.words]
        g=sorted(((round(ws[k+1].start-ws[k].end,2),ws[k].word.strip()+'|'+ws[k+1].word.strip()) for k in range(len(ws)-1)),reverse=True)[:1]
        print(sd,i+1,round(x['end']-x['start'],2),g,'::',' '.join(q.word.strip() for q in ws))
