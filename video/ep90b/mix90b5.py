import subprocess,numpy as np,os,json,re,sys
import soundfile as sfile
H=os.path.dirname(os.path.abspath(__file__)); SR=48000
vid,tag=sys.argv[1],sys.argv[2]
D=json.load(open(H+'/duck90b.json'))['D']; N=int(D*SR)
def load(p,sr=SR): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
voice=load(H+'/out/narration90b.wav')[:N]
if len(voice)<N: voice=np.pad(voice,(0,N-len(voice)))
vr=np.sqrt((voice[np.abs(voice)>1e-3]**2).mean())
ev=json.load(open(H+'/sfx90b.json')); lay=np.zeros(N+SR)
for e in ev:
    x=load(f"{H}/sfx/{e['f']}"); x=x/(np.abs(x).max()+1e-9)*10**(e['g']/20)
    i0=int(e['t']*SR); n=min(len(x),len(lay)-i0)
    if n>0: lay[i0:i0+n]+=x[:n]
lay=lay[:N]; lr=np.sqrt((lay[np.abs(lay)>1e-3]**2).mean()); lay=lay/lr*vr*10**(-17/20)   # sfx rms 13 dB under the voice rms
mix=voice+lay
fo=int(.5*SR); mix[-fo:]*=np.linspace(1,0,fo)
w=f"{H}/out/mix-{tag}.wav"; sfile.write(w,mix,SR,subtype='PCM_16')
w2=f"{H}/out/mix2-{tag}.wav"
mm=subprocess.run(['ffmpeg','-v','info','-i',w,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
I0=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',mm)[-1])
subprocess.run(['ffmpeg','-y','-v','error','-i',w,'-af',f'volume={-14.0-I0}dB,alimiter=limit=0.84:level=false','-ar','48000',w2],check=True)
out=f"{H}/out/ep90b-{tag}.mp4"
subprocess.run(['ffmpeg','-y','-v','error','-i',vid,'-i',w2,'-map','0:v','-map','1:a','-c:v','libx264','-crf','24','-preset','slow','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-ar','48000','-ac','2','-t',str(D),out],check=True)
subprocess.run(['ffmpeg','-y','-v','error','-i',out,'-vf','scale=720:-2','-c:v','libx264','-crf','31','-preset','veryfast','-c:a','aac','-b:a','64k',f"{H}/out/ep90b-{tag}-review720.mp4"],check=True)
m=subprocess.run(['ffmpeg','-v','info','-i',out,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
print(tag,'loudness',re.findall(r'I:\s+(-?[\d.]+) LUFS',m)[-1],'LUFS; sfx 17 dB under voice rms')
for f in (w,w2): os.remove(f)
