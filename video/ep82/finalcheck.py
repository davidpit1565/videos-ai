import sys, json, numpy as np, librosa
sys.path.insert(0,".")
from faster_whisper import WhisperModel
W=WhisperModel("base.en",device="cpu",compute_type="int8",cpu_threads=2)
for V in sys.argv[1:]:
    c=json.load(open(f"out/cues-{V}.json"))["lines"][8]
    y,_=librosa.load(f"out/narration-{V}-r.wav",sr=16000,offset=c["start"]-0.1,duration=c["end"]-c["start"]+0.2)
    y=np.concatenate([np.zeros(8000),y,np.zeros(8000)]).astype(np.float32)
    sg,_=W.transcribe(y,language="en",beam_size=5,word_timestamps=True)
    print(V,"line9 in the FINAL repaired narration:"," ".join(w.word.strip() for s in sg for w in s.words))
