import subprocess,sys,numpy as np,os,json,re
H=os.path.dirname(os.path.abspath(__file__)); LIB='/home/user/videos-ai/audio/music-library/'
# usage: mix5.py <narration.wav> <video.mp4> <D> <tag> [bed_track] ; narration + sfx layer + ducked real-library bed -> out/ep89-<tag>.mp4 (+720)
nar,vid,D,tag=sys.argv[1],sys.argv[2],float(sys.argv[3]),sys.argv[4]
MUS=sys.argv[5]   # a bed wav from audio/pick_real_track.py, exact length
SR=48000
def load(p,sr=16000): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
def band(x):
    X=np.abs(np.fft.rfft(x*np.hanning(len(x))))**2; f=np.fft.rfftfreq(len(x),1/16000)
    return 10*np.log10(X[(f>=300)&(f<3500)].sum()/len(x)**2+1e-20)
vb=band(load(nar))
# --- sfx layer: each file peak-normalised, placed at its time, then the whole layer set ~9 dB under the voice RMS peaks
ev=json.load(open(H+'/sfx89c.json')); N=int(D*SR); lay=np.zeros(N+SR)
for e in ev:
    x=load(f"{H}/sfx/{e['f']}",SR)
    if len(x)==0: print("missing",e['f']); continue
    x=x/ (np.abs(x).max()+1e-9) * 10**((-14+e['g'])/20)
    i0=int(e['t']*SR); n=min(len(x),len(lay)-i0)
    if n>0: lay[i0:i0+n]+=x[:n]
sf=np
import soundfile as sfile
sfile.write(f"{H}/out/sfx-{tag}.wav",lay[:N],SR,subtype='PCM_16')
raw=f"{H}/out/bed89-{tag}.wav"
subprocess.run(['ffmpeg','-y','-v','error','-i',MUS,'-ac','1','-ar','48000','-t',str(D),'-af','highpass=f=140',raw],check=True)
g=vb-9-band(load(raw))
fc=(f"[0:a]asplit=2[v1][key];[1:a]volume={g}dB[b];[b][key]sidechaincompress=threshold=0.05:ratio=4:attack=12:release=420[duck];[duck]asplit=2[d1][d2];"
    f"[v1][d1][2:a]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1:LRA=11[o]")
wav=f"{H}/out/mix5-{tag}.wav"; duck=f"{H}/out/duck5-{tag}.wav"
subprocess.run(['ffmpeg','-y','-v','error','-i',nar,'-i',raw,'-i',f"{H}/out/sfx-{tag}.wav",'-filter_complex',fc,'-map','[o]','-ar','48000',wav,'-map','[d2]',duck],check=True)
json.dump(dict(gain_db=g,lin=10**(g/20)),open(f'{H}/out/gain5-{tag}.json','w'))
m=subprocess.run(['ffmpeg','-v','info','-i',wav,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
I=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',m)[-1]); fix=-14.0-I
tmp=wav[:-4]+'-pre.wav'; os.replace(wav,tmp)
subprocess.run(['ffmpeg','-y','-v','error','-i',tmp,'-af',f'volume={fix}dB,alimiter=limit=0.89:level=false','-ar','48000',wav],check=True)
print('integrated',I,'-> corrected by',round(fix,2),'dB')
s16=load(f"{H}/out/sfx-{tag}.wav"); 
out=f"{H}/out/ep89-{tag}.mp4"
subprocess.run(['ffmpeg','-y','-v','error','-i',vid,'-i',wav,'-map','0:v','-map','1:a','-c:v','libx264','-crf','26','-preset','slow','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(D),out],check=True)
subprocess.run(['ffmpeg','-y','-v','error','-i',out,'-vf','scale=720:-2','-c:v','libx264','-crf','28','-preset','veryfast','-c:a','aac','-b:a','96k',f"{H}/out/ep89-{tag}-720.mp4"],check=True)
print('bed ducked vs voice (300-3500 Hz):',round(band(load(duck))-vb,1),'dB; sfx rms vs voice rms (dB):',round(20*np.log10(np.sqrt(np.mean(s16**2)+1e-12)/np.sqrt(np.mean(load(nar)**2)+1e-12)),1),'; fix',round(fix,2),'; lin',10**(g/20)*10**(fix/20))
