import subprocess,numpy as np,os,json,re,sys
import soundfile as sfile
H=os.path.dirname(os.path.abspath(__file__)); SR=48000
vid,tag=sys.argv[1],sys.argv[2]
D=json.load(open(H+'/duck90b6.json'))['D']; N=int(D*SR)
def load(p,sr=SR): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
ev=json.load(open(H+'/sfx90b6.json')); lay=np.zeros(N+SR)
for e in ev:
    x=load(f"{H}/sfx/{e['f']}"); x=x/(np.abs(x).max()+1e-9)*10**(e['g']/20)
    i0=int(e['t']*SR); n=min(len(x),len(lay)-i0)
    if n>0: lay[i0:i0+n]+=x[:n]
lay=lay[:N]; lay=lay/np.abs(lay).max()*0.5
fo=int(.6*SR); lay[-fo:]*=np.linspace(1,0,fo)
w=f"{H}/out/sfx-{tag}.wav"; sfile.write(w,lay,SR,subtype='PCM_16')
mm=subprocess.run(['ffmpeg','-v','info','-i',w,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
I0=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',mm)[-1])
w2=f"{H}/out/sfx2-{tag}.wav"
subprocess.run(['ffmpeg','-y','-v','error','-i',w,'-af',f'volume={-18.0-I0}dB,alimiter=limit=0.85:level=false','-ar','48000',w2],check=True)
out=f"{H}/out/ep90b-{tag}.mp4"
subprocess.run(['ffmpeg','-y','-v','error','-i',vid,'-i',w2,'-map','0:v','-map','1:a','-c:v','libx264','-crf','24','-preset','slow','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-ar','48000','-ac','2','-t',str(D),out],check=True)
subprocess.run(['ffmpeg','-y','-v','error','-i',out,'-vf','scale=720:-2','-c:v','libx264','-crf','31','-preset','veryfast','-c:a','aac','-b:a','64k',f"{H}/out/ep90b-{tag}-review720.mp4"],check=True)
m=subprocess.run(['ffmpeg','-v','info','-i',out,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
print(tag,'sfx-only loudness',re.findall(r'I:\s+(-?[\d.]+) LUFS',m)[-1],'LUFS, true peak',re.findall(r'Peak:\s+(-?[\d.]+) dBFS',m)[-1])
for f in (w,w2): os.remove(f)
