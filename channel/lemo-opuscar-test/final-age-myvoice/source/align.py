import json, torch, torchaudio, soundfile as sf, re
import torchaudio.functional as F
from torchaudio.pipelines import WAV2VEC2_ASR_BASE_960H as B
m=B.get_model().eval(); lab=B.get_labels(); d={c:i for i,c in enumerate(lab)}
x,sr=sf.read('voices/narration.wav',dtype='float32'); assert sr==48000
import soxr; x16=soxr.resample(x,48000,16000).astype('float32')
cues=json.load(open('voices/cues_in.json'))
asr={1:"Adult Chat GPT may call you a teen",2:"It can happen even with a birthday typed in",3:"News sites reported it back in January",4:"It guesses from what you ask and when",5:"See what it says Settings Account Age",6:"If it's wrong Open AI says a selfie or an ID can fix it",7:"Has Chat GPT ever called you a kid Tell me below",8:"The setup's in the link in bio",9:"I read the fine print AI apps hope you skip Follow and you won't have to"}
words={};dur={};cuesout={}
for c in cues:
    n=c['n'];a=max(0,c['start']-.25);b=c['end']+.35
    seg=torch.from_numpy(x16[int(a*16000):int(b*16000)])[None]
    with torch.no_grad(): em,_=m(seg)
    em=torch.log_softmax(em,-1)
    ws=asr[n].upper().split()
    toks=[];idx=[]
    for wi,w in enumerate(ws):
        for ch in w: toks.append(d[ch]); idx.append(wi)
        if wi<len(ws)-1: toks.append(d['|']); idx.append(-1)
    al,sc=F.forced_align(em,torch.tensor([toks],dtype=torch.int32),blank=0)
    sp=torchaudio.functional.merge_tokens(al[0],sc[0].exp())
    ratio=(seg.shape[1]/em.shape[1])/16000
    # spans in order for tokens (non-blank), map to tokens
    assert len(sp)==len(toks),(n,len(sp),len(toks))
    st={};en={}
    for s,wi in zip(sp,idx):
        if wi<0: continue
        t0=a+s.start*ratio;t1=a+s.end*ratio
        st.setdefault(wi,t0);en[wi]=t1
    words[f'l{n}']=[[ws[i].lower(),round(st[i]-c['start'],3),round(en[i]-c['start'],3)] for i in range(len(ws))]
    dur[f'l{n}']=round(c['end']-c['start'],3);cuesout[f'l{n}']=c['start']
json.dump(words,open('voices/words.json','w'));json.dump(dur,open('voices/dur.json','w'));json.dump(cuesout,open('voices/cues.json','w'))
for k,v in words.items(): print(k,cuesout[k],dur[k],[(w[0],round(w[1]+cuesout[k],2)) for w in v])
