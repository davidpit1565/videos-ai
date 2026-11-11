import sys, json, subprocess, soundfile as sf
from faster_whisper import WhisperModel
m=WhisperModel('small',device='cpu',compute_type='int8')
for s in (5301,5302,5303,5304,5305,5306):
    subprocess.run(['ffmpeg','-v','error','-y','-i',f't{s}.wav','-af','atempo=1.12','-ar','48000','-ac','1','-c:a','pcm_s16le',f't{s}-fast.wav'])
    x,sr=sf.read(f't{s}-fast.wav'); d=len(x)/sr
    seg,_=m.transcribe(f't{s}-fast.wav',language='en',word_timestamps=True,initial_prompt="")
    ws=[(w.word.strip(),round(w.start,2),round(w.end,2)) for g in seg for w in g.words]
    json.dump([dict(n=1,line="I told ChatGPT I'd delete it in 10 seconds.",start=0.05,end=round(d-0.05,3))],open(f't{s}-cues.json','w'))
    print(s,round(d,2),ws)
