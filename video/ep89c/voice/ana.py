import sys, subprocess, json, numpy as np, soundfile as sf, librosa
sys.path.insert(0,'..')
from faster_whisper import WhisperModel
m=WhisperModel('small',device='cpu',compute_type='int8')
def run(tag,tempo):
    out=f'{tag}-fast.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'{tag}.wav','-af',f'atempo={tempo}','-ar','48000','-ac','1',out],check=True)
    x,sr=sf.read(out); x=x if x.ndim==1 else x[:,0]
    # voiced extent by energy
    fr=int(.01*sr); e=np.array([20*np.log10(np.sqrt((x[i:i+fr]**2).mean())+1e-9) for i in range(0,len(x)-fr,fr)])
    act=np.where(e>-40)[0]; a,b=act[0]*.01,act[-1]*.01+.01
    seg,_=m.transcribe(out,language='en',word_timestamps=True)
    ws=[(w.word.strip(),w.start,w.end) for s in seg for w in (s.words or [])]
    print(tag,'tempo',tempo,'active %.2f-%.2f'%(a,b),'dur %.2f'%(b-a)); print('  whisper',[(w,round(s,2),round(e_,2)) for w,s,e_ in ws])
    wd={w.lower().strip('.,'):(st,en) for w,st,en in ws}
    g=wd.get('going'); v=wd.get('viral')
    from measure import meas
    meas(out,0,len(x)/sr,{'going':(g[0]+.02,g[1]),'viral':(v[0]+.02,min(v[1],b))})
if __name__=='__main__': run(sys.argv[1],float(sys.argv[2]))
