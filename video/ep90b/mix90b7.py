import subprocess,numpy as np,os,json,re,sys
import soundfile as sfile
H=os.path.dirname(os.path.abspath(__file__)); SR=48000; ROOT=os.path.dirname(os.path.dirname(H))
vid,tag,track=sys.argv[1],sys.argv[2],sys.argv[3]; preview=len(sys.argv)>4 and sys.argv[4]=='preview'
dk=json.load(open(H+'/duck90b7.json')); D=dk['D']; N=int(D*SR); t=np.arange(N)/SR
def load(p,sr=SR): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
def band(x):
    X=np.abs(np.fft.rfft(x*np.hanning(len(x))))**2; f=np.fft.rfftfreq(len(x),1/SR)
    return 10*np.log10(X[(f>=300)&(f<3500)].sum()/len(x)**2+1e-20)
voice=load(H+'/out/narration90b7.wav')[:N]; voice=np.pad(voice,(0,max(0,N-len(voice))))
bedp=f"{H}/out/bed7-{tag}.wav"
subprocess.run(['python3',f'{ROOT}/audio/pick_real_track.py',str(D),bedp,'--mood','punchy'],env=dict(os.environ,FORCE_TRACK=track),check=True,capture_output=True)
raw=load(bedp)[:N]; raw=np.pad(raw,(0,max(0,N-len(raw))))
raw=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-f','f32le','-ar','48000','-ac','1','-i','-','-af','highpass=f=140','-f','f32le','-'],input=raw.astype(np.float32).tobytes(),capture_output=True).stdout,dtype=np.float32)   # phone speakers: no sub-bass
act=np.abs(voice)>0.01
gain=10**((band(voice[act])-14-band(raw))/20)          # bed 14 dB under the voice in 300-3500 Hz (un-ducked)
g=np.zeros(N)
def ramp(a,b,db,ra=.3,rb=.2): return db*np.clip((t-a)/ra,0,1)*np.clip((b-t)/rb,0,1)
g+=ramp(dk['tender'][0],dk['tender'][1],-4,.5,.5)                 # tender dip under the begging card
g+=ramp(dk['silence'][0],dk['silence'][1],-18,.25,.1)             # near-silence before the punchline
sg=dk['punch']; g+=2.0*np.clip((t-sg)/.05,0,1)*np.clip((sg+.6-t)/.5,0,1)   # groove back with a small sting
bed=raw*gain*10**(g/20)*np.minimum(1,np.minimum(t/0.05,(D-t)/1.2))
ev=json.load(open(H+'/sfx90b7.json')); lay=np.zeros(N+SR)
for e in ev:
    x=load(f"{H}/sfx/{e['f']}"); x=x/(np.abs(x).max()+1e-9)*10**(e['g']/20)
    i0=int(e['t']*SR); n=min(len(x),len(lay)-i0)
    if n>0: lay[i0:i0+n]+=x[:n]
lay=lay[:N]; vr=np.sqrt((voice[act]**2).mean()); lr=np.sqrt((lay[np.abs(lay)>1e-3]**2).mean()); lay=lay/lr*vr*10**(-17/20)
mix=voice+bed+lay; mix[-int(.5*SR):]*=np.linspace(1,0,int(.5*SR))
w=f"{H}/out/mix7-{tag}.wav"; sfile.write(w,mix,SR,subtype='PCM_16')
def meas(p):
    m=subprocess.run(['ffmpeg','-v','info','-i',p,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS',m)[-1]), float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS',m)[-1])
I0,_=meas(w); fix=-13.2-I0; lim=0.85
w2=f"{H}/out/mix7b-{tag}.wav"
for _ in range(3):
    subprocess.run(['ffmpeg','-y','-v','error','-i',w,'-af',f'volume={fix}dB,alimiter=limit={lim}:level=false','-ar','48000',w2],check=True)
    I2,P2=meas(w2)
    if P2<-1.2: break
    lim-=0.05
if preview:
    out=f"{H}/out/ep90b-final7-alt-{tag}-720.mp4"
    subprocess.run(['ffmpeg','-y','-v','error','-i',vid,'-i',w2,'-map','0:v','-map','1:a','-vf','scale=720:-2','-c:v','libx264','-crf','35','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','56k','-ac','2','-t',str(D),out],check=True)
else:
    out=f"{H}/out/ep90b-{tag}.mp4"
    subprocess.run(['ffmpeg','-y','-v','error','-i',vid,'-i',w2,'-map','0:v','-map','1:a','-c:v','libx264','-crf','24','-preset','slow','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-ar','48000','-ac','2','-t',str(D),out],check=True)
    subprocess.run(['ffmpeg','-y','-v','error','-i',out,'-vf','scale=720:-2','-c:v','libx264','-crf','31','-preset','veryfast','-c:a','aac','-b:a','64k',f"{H}/out/ep90b-{tag}-review720.mp4"],check=True)
    json.dump(dict(vol=round(float(gain),4)),open(f"{H}/out/vol7-{tag}.json",'w'))
print(tag,track,'LUFS',round(I2,1),'peak',P2,'dBFS (post-aac may differ); bed gain',round(20*np.log10(gain),1),'dB; fix',round(fix,1))
for f in (w,w2): os.remove(f)
