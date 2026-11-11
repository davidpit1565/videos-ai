import subprocess,numpy as np,os,json,re,sys
import soundfile as sfile
H=os.path.dirname(os.path.abspath(__file__)); SR=48000; ROOT=os.path.dirname(os.path.dirname(H))
vid,tag,track,preview=sys.argv[1],sys.argv[2],sys.argv[3],(len(sys.argv)>4 and sys.argv[4]=='preview')
dk=json.load(open(H+'/duck90b.json')); D=dk['D']; N=int(D*SR)
def load(p,sr=SR): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
bedp=f"{H}/out/bed-{tag}.wav"
env=dict(os.environ,FORCE_TRACK=track)
subprocess.run(['python3',f'{ROOT}/audio/pick_real_track.py',str(D),bedp,'--mood','punchy'],env=env,check=True,capture_output=True)
bed=load(bedp)[:N]
if len(bed)<N: bed=np.pad(bed,(0,N-len(bed)))
# ducking envelope: tender at the begging line (-8 dB), near-silence before the punchline (-30 dB), groove back (+1.5 dB for 0.6 s as the sting)
t=np.arange(N)/SR; g=np.zeros(N)
def ramp(a,b,db,ra=.3,rb=.15):
    w=np.clip((t-a)/ra,0,1)*np.clip((b-t)/rb,0,1); return db*w
g+=ramp(dk['tender'][0],dk['tender'][1],-8,.4,.4)
g+=ramp(dk['silence'][0],dk['silence'][1],-30,.2,.08)
sting=dk['silence'][1]; g+=1.5*np.clip((t-sting)/.05,0,1)*np.clip((sting+.6-t)/.5,0,1)
bed=bed*10**(g/20)
# bed level: RMS of the un-ducked groove at -22 dBFS (audible on a phone); sfx quiet under it
raw=load(bedp)[:N]; rms=np.sqrt((raw**2).mean()+1e-12); bed=bed/rms*10**(-22/20)
bed*=np.minimum(1,np.minimum(t/0.05+0.0,(D-t)/1.0))      # 50 ms in, 1 s out
ev=json.load(open(H+'/sfx90b.json')); lay=np.zeros(N+SR)
for e in ev:
    x=load(f"{H}/sfx/{e['f']}"); x=x/(np.abs(x).max()+1e-9)*10**((-8+e['g'])/20)
    i0=int(e['t']*SR); n=min(len(x),len(lay)-i0)
    if n>0: lay[i0:i0+n]+=x[:n]
mix=bed+lay[:N]
w=f"{H}/out/mix-{tag}.wav"; sfile.write(w,mix,SR,subtype='PCM_16')
# loudness to -16 LUFS (bed + sfx only, no voice), true peak -1.5
m=subprocess.run(['ffmpeg','-v','info','-i',w,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
I=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',m)[-1]); fix=-16.0-I
w2=f"{H}/out/mix2-{tag}.wav"
subprocess.run(['ffmpeg','-y','-v','error','-i',w,'-af',f'volume={fix}dB,alimiter=limit=0.84:level=false','-ar','48000',w2],check=True)
m2=subprocess.run(['ffmpeg','-v','info','-i',w2,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
I2=re.findall(r'I:\s+(-?[\d.]+) LUFS',m2)[-1]
if preview:
    out=f"{H}/out/ep90b-final2-alt-{tag}-720.mp4"
    subprocess.run(['ffmpeg','-y','-v','error','-i',vid,'-i',w2,'-map','0:v','-map','1:a','-vf','scale=720:-2','-c:v','libx264','-crf','35','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','56k','-ac','2','-t',str(D),out],check=True)
else:
    out=f"{H}/out/ep90b-{tag}.mp4"
    subprocess.run(['ffmpeg','-y','-v','error','-i',vid,'-i',w2,'-map','0:v','-map','1:a','-c:v','libx264','-crf','24','-preset','slow','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-ar','48000','-ac','2','-t',str(D),out],check=True)
    subprocess.run(['ffmpeg','-y','-v','error','-i',out,'-vf','scale=720:-2','-c:v','libx264','-crf','31','-preset','veryfast','-c:a','aac','-b:a','64k',f"{H}/out/ep90b-{tag}-review720.mp4"],check=True)
for f in (w,w2): os.remove(f)
print(tag,track,'loudness',I2,'LUFS; bed raw rms ->-22 dBFS; out',out)
