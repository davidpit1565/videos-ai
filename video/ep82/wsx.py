import sys, numpy as np, librosa
from faster_whisper import WhisperModel
m=WhisperModel("base.en",device="cpu",compute_type="int8",cpu_threads=2)
for f in sys.argv[1:]:
    y,_=librosa.load(f,sr=16000); y=np.concatenate([np.zeros(8000),y,np.zeros(8000)]).astype(np.float32)
    segs,_=m.transcribe(y,language="en",word_timestamps=True,beam_size=5)
    print(f,[(w.word.strip(),round(w.start-0.5,2),round(w.end-0.5,2)) for s in segs for w in s.words])
