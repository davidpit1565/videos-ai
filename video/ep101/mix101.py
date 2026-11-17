import subprocess,sys,numpy as np,re,os
# ep101: silent scroll reel, music bed only (ffmpeg-only: soundfile/scipy are not installed here).
# usage: mix101.py <pic.mp4> <tag>; env TRACK, START
H=os.path.dirname(os.path.abspath(__file__)); vid,tag=sys.argv[1],sys.argv[2]; D=14.5; SR=48000
TRACK=os.environ.get('TRACK','/home/user/videos-ai/audio/music-library/cinematic--dramatic--themountain.mp3'); START=os.environ.get('START','0')
raw=f'{H}/out/bed101-{tag}.wav'; wav=f'{H}/out/mix101-{tag}.wav'
subprocess.run(['ffmpeg','-y','-v','error','-ss',START,'-t',str(D),'-i',TRACK,'-ac','1','-ar',str(SR),'-af',f'highpass=f=140:poles=2,highpass=f=140:poles=2,afade=t=in:d=0.15,afade=t=out:st={D-1.6}:d=1.6:curve=qua','-c:a','pcm_f32le',raw],check=True)
subprocess.run(['ffmpeg','-y','-v','error','-i',raw,'-af','loudnorm=I=-14:TP=-1:LRA=11,alimiter=limit=0.89:level=false','-ar','48000',wav],check=True)
m=subprocess.run(['ffmpeg','-i',wav,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
print('I',re.findall(r'I:\s+(-?[\d.]+) LUFS',m)[-1],'peak',re.findall(r'Peak:\s+(-?[\d.]+) dBFS',m)[-1])
x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',wav,'-ac','1','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
X=np.abs(np.fft.rfft(x))**2; fr=np.fft.rfftfreq(len(x),1/SR)
print('share<150Hz',round(X[fr<150].sum()/X.sum(),2),'300-3500',round(X[(fr>300)&(fr<3500)].sum()/X.sum(),2),'len',len(x)/SR)
o=f'{H}/out/ep101-{tag}.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-i',vid,'-i',wav,'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(D),o],check=True)
subprocess.run(['ffmpeg','-y','-v','error','-i',o,'-vf','scale=720:-2','-c:v','libx264','-crf','27','-preset','veryfast','-c:a','aac','-b:a','96k',f'{H}/out/ep101-{tag}-review.mp4'],check=True)
