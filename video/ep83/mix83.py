import subprocess,sys,numpy as np,os,json
H=os.path.dirname(os.path.abspath(__file__)); R='/home/user/videos-ai'
# usage: mix83.py <narration.wav> <silent.mp4> <D> <tag> <track.mp3|-> [bandgap_dB=8]
nar,vid,D,tag,track=sys.argv[1:6]; gap=float(sys.argv[6]) if len(sys.argv)>6 else 8
def load(p): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
def band(x):
    X=np.abs(np.fft.rfft(x*np.hanning(len(x))))**2; f=np.fft.rfftfreq(len(x),1/16000)
    return 10*np.log10(X[(f>=300)&(f<3500)].sum()/len(x)**2+1e-20)
raw=f"{H}/out/bed-{tag}.wav"
env=dict(os.environ,FORCE_TRACK=os.path.basename(track))
subprocess.run(['python3',f'{R}/audio/pick_real_track.py',str(D),raw,'--mood','confident','--no-record'],check=True,env=env)
g=band(load(nar))-gap-band(load(raw))
fc=f"[0:a]asplit=2[v1][key];[1:a]volume={g}dB[b];[b][key]sidechaincompress=threshold=0.05:ratio=4:attack=12:release=420[duck];[duck]asplit=2[d1][d2];[v1][d1]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1:LRA=11[o]"
wav=f"{H}/out/mix-{tag}.wav"; duck=f"{H}/out/duck-{tag}.wav"
subprocess.run(['ffmpeg','-y','-v','error','-i',nar,'-i',raw,'-filter_complex',fc,'-map','[o]','-ar','48000',wav,'-map','[d2]',duck],check=True)
json.dump(dict(gain_db=g,lin=10**(g/20)),open(f'{H}/out/gain-{tag}.json','w'))
out=f"{H}/out/ep83-{tag}.mp4"
subprocess.run(['ffmpeg','-y','-v','error','-i',vid,'-i',wav,'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(D),out],check=True)
print(tag,track,"gain",round(g,1),"dB; bed ducked vs voice 300-3500:",round(band(load(duck))-band(load(nar)),1),"dB ->",out)
