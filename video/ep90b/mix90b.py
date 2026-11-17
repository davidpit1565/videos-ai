import subprocess,numpy as np,os,json,re,sys
import soundfile as sfile
H=os.path.dirname(os.path.abspath(__file__)); SR=48000
vid,D,tag=sys.argv[1],float(sys.argv[2]),sys.argv[3]
def load(p,sr=SR): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
ev=json.load(open(H+'/sfx90b.json')); N=int(D*SR); lay=np.zeros(N+SR)
for e in ev:
    x=load(f"{H}/sfx/{e['f']}"); x=x/(np.abs(x).max()+1e-9)*10**((e['g'])/20)
    i0=int(e['t']*SR); n=min(len(x),len(lay)-i0)
    if n>0: lay[i0:i0+n]+=x[:n]
lay=lay[:N]
# quiet but present: loudest hit at -6 dBFS (no voice, no music bed)
pk=np.abs(lay).max(); lay=lay/pk*10**(-6/20)
fo=int(.6*SR); lay[-fo:]*=np.linspace(1,0,fo)
w=f"{H}/out/sfx-{tag}.wav"; sfile.write(w,lay,SR,subtype='PCM_16')
out=f"{H}/out/ep90b-{tag}.mp4"
subprocess.run(['ffmpeg','-y','-v','error','-i',vid,'-i',w,'-map','0:v','-map','1:a','-c:v','libx264','-crf','24','-preset','slow','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-ar','48000','-ac','2','-t',str(D),out],check=True)
subprocess.run(['ffmpeg','-y','-v','error','-i',out,'-vf','scale=720:-2','-c:v','libx264','-crf','31','-preset','veryfast','-c:a','aac','-b:a','64k',f"{H}/out/ep90b-{tag}-review720.mp4"],check=True)
m=subprocess.run(['ffmpeg','-v','info','-i',out,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
print('sfx layer peak -6 dBFS; loudness', re.findall(r'I:\s+(-?[\d.]+) LUFS',m)[-1], 'LUFS')
