import subprocess,sys,numpy as np,os,json,re
import soundfile as sf, scipy.signal as sg
# mix102.py (from video/ep100/mix100b.py): voice + sfx + bed (default punchy--hip-hop-beat--themountain from 16 s, the ep89 groove),
# high-passed 140 Hz, shaped by an explicit cue-based envelope (duck under lines, +3 dB lift in gaps), fade-out.
# usage: mix102.py <narration.wav> <pic.mp4> <D> <tag> [speaking_db_under_voice=-10]
H=os.path.dirname(os.path.abspath(__file__)); SF='/home/user/videos-ai/video/ep89c/sfx'
nar,vid,D,tag=sys.argv[1],sys.argv[2],float(sys.argv[3]),sys.argv[4]
TARGET=float(sys.argv[5]) if len(sys.argv)>5 else -10.0
LIFT=3.0; SR=48000
TRACK=os.environ.get('TRACK','/home/user/videos-ai/audio/music-library/punchy--hip-hop-beat--themountain.mp3'); START=float(os.environ.get('START','16'))  # env TRACK/START: bed file and trim start (s)
def load(p,sr=SR): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
def bandpass(x): return sg.sosfilt(sg.butter(4,[300,3500],'bp',fs=SR,output='sos'),x)
cues=json.load(open(H+'/voice/cues-'+tag+'.json'))['lines']; N=int(D*SR)
# bed: decode, loop with crossfade, hp 140
b=load(TRACK)[int(START*SR):]; xf=int(0.5*SR); fi=np.sin(np.linspace(0,np.pi/2,xf))**1; fo=np.cos(np.linspace(0,np.pi/2,xf))
out=b.copy()
while len(out)<N+SR:
    out=np.concatenate([out[:-xf],out[-xf:]*fo+b[:xf]*fi,b[xf:]])
out=out[:N]
out=sg.sosfilt(sg.butter(4,140,'hp',fs=SR,output='sos'),out)
# envelope: 1 while a line speaks, lift in gaps, smoothed
env=np.full(N,10**(LIFT/20)); 
for l in cues:
    env[int(l['start']*SR):int(l['end']*SR)]=1.0
k=int(0.25*SR); env=np.convolve(np.pad(env,(k,k),mode='edge'),np.hanning(k)/np.hanning(k).sum(),mode='same')[k:-k]
# intro: bed starts at full envelope-free level quickly (0.15 s fade-in), fade-out last 1.6 s
fade=np.ones(N); fi_n=int(0.15*SR); fade[:fi_n]=np.linspace(0,1,fi_n); fo_n=int(1.6*SR); fade[-fo_n:]=np.linspace(1,0,fo_n)**1.5
out=out*env*fade
# gain: bed minus voice in 300-3500 Hz over the speaking windows
v=load(nar)[:N]; vb=bandpass(v); bb=bandpass(out)
msk=np.zeros(N,bool)
for l in cues: msk[int(l['start']*SR):int(l['end']*SR)]=True
mv=msk[:len(vb)]; 
pv=np.mean(vb[mv[:len(vb)]]**2); pb=np.mean(bb[msk]**2)
g=TARGET-10*np.log10(pb/pv); out=(out*10**(g/20)).astype(np.float32)
bed=f"{H}/out/bed106-{tag}.wav"; sf.write(bed,out,SR,subtype='FLOAT')
# sfx layer (same as mix100.py)
ev=json.load(open(H+'/sfx-'+tag+'.json')); lay=np.zeros(N+SR)
for e in ev:
    x=load(f"{SF}/{e['f']}")
    if len(x)==0: print("missing",e['f']); continue
    x=x/(np.abs(x).max()+1e-9)*10**((-14+e['g'])/20); i0=int(e['t']*SR); n=min(len(x),len(lay)-i0)
    if n>0: lay[i0:i0+n]+=x[:n]
sfx=f"{H}/out/sfx-{tag}.wav"; sf.write(sfx,lay[:N],SR,subtype='PCM_16')
wav=f"{H}/out/mix5-{tag}.wav"
subprocess.run(['ffmpeg','-y','-v','error','-i',nar,'-i',bed,'-i',sfx,'-filter_complex','[0:a][1:a][2:a]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1:LRA=11[o]','-map','[o]','-ar','48000',wav],check=True)
m=subprocess.run(['ffmpeg','-v','info','-i',wav,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
I=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',m)[-1]); fix=-14.0-I
tmp=wav[:-4]+'-pre.wav'; os.replace(wav,tmp)
subprocess.run(['ffmpeg','-y','-v','error','-i',tmp,'-af',f'volume={fix}dB,alimiter=limit=0.89:level=false','-ar','48000',wav],check=True)
lin=10**(g/20)*10**(fix/20); json.dump(dict(gain_db=float(g),lin=float(lin),fix=float(fix)),open(f'{H}/out/gain5-{tag}.json','w'))
o=f"{H}/out/ep106-{tag}.mp4"
subprocess.run(['ffmpeg','-y','-v','error','-i',vid,'-i',wav,'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(D),o],check=True)
subprocess.run(['ffmpeg','-y','-v','error','-i',o,'-vf','scale=720:-2','-c:v','libx264','-crf','27','-preset','veryfast','-c:a','aac','-b:a','96k',f"{H}/out/ep106-{tag}-review.mp4"],check=True)
gaps=~msk; 
print('integrated',I,'fix',round(fix,2),'bed gain',round(g,2),'; bed-voice speaking',round(10*np.log10(np.mean(bandpass(out)[msk]**2)/pv),1),'dB; gaps bed vs voice-speaking',round(10*np.log10(np.mean(bandpass(out)[gaps]**2)/pv),1),'; lin(for voice_quality --vol, raw track hp)',round(lin,4))
