import sys,re,json
from faster_whisper import WhisperModel
wav,line=sys.argv[1],sys.argv[2]
m=WhisperModel('small.en',device='cpu',compute_type='int8')
segs,_=m.transcribe(wav,word_timestamps=True,language='en')
ws=[w for s in segs for w in s.words]
txt=' '.join(w.word.strip() for w in ws)
n=lambda s:re.sub(r'[^a-z0-9 ]','',s.lower().replace('-',' ')).split()
D={'10':'ten','1':'one','2':'two','3':'three','4':'four','5':'five','6':'six'}
import re as _r
t2=_r.sub(r'\d+',lambda m:D.get(m.group(),m.group()),txt)
a,b=n(t2),n(line)
ok=''.join(a)==''.join(b)
gap=None
for i in range(len(ws)-1):
    if ws[i].word.strip().lower().strip('.,!') =='meta' and ws[i+1].word.strip().lower().strip('.,!')=='ai':
        gap=round(ws[i+1].start-ws[i].end,3)
if gap is not None and gap>=0.12: ok=False
print('WHISPER',ok,'|',txt,'| metagap',gap)
sys.exit(0 if ok else 1)
