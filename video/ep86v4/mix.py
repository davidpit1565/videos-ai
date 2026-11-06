import subprocess,sys,numpy as np,os,json
H=os.path.dirname(os.path.abspath(__file__)); LIB='/home/user/videos-ai/audio/music-library/'
# usage: mix.py <narration.wav> <video.mp4> <D> <tag> ; mixes 3 beds -> out/<tag>-<k>.mp4 (+720p preview)
nar,vid,D,tag=sys.argv[1],sys.argv[2],float(sys.argv[3]),sys.argv[4]
BEDS=[("M","cinematic--dramatic--themountain.mp3",0,0)]
def load(p): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
def band(x):
    X=np.abs(np.fft.rfft(x*np.hanning(len(x))))**2; f=np.fft.rfftfreq(len(x),1/16000)
    return 10*np.log10(X[(f>=300)&(f<3500)].sum()/len(x)**2+1e-20)
vb=band(load(nar)); res={}
for k,f,ss,hp in BEDS:
    raw=f"{H}/out/bed-{k}.wav"
    subprocess.run(['ffmpeg','-y','-v','error','-ss',str(ss),'-t',str(D),'-i',LIB+f,'-ac','1','-ar','48000','-af',f'afade=t=in:d=0.5,afade=t=out:st={D-1.3}:d=1.3,highpass=f=140',raw],check=True)
    g=vb-13-band(load(raw))
    fc=f"[0:a]asplit=2[v1][key];[1:a]volume={g}dB[b];[b][key]sidechaincompress=threshold=0.05:ratio=4:attack=12:release=420[duck];[duck]asplit=2[d1][d2];[v1][d1]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1:LRA=11[o]"
    wav=f"{H}/out/mix-{tag}-{k}.wav"; duck=f"{H}/out/duck-{tag}-{k}.wav"
    subprocess.run(['ffmpeg','-y','-v','error','-i',nar,'-i',raw,'-filter_complex',fc,'-map','[o]','-ar','48000',wav,'-map','[d2]',duck],check=True)
    json.dump(dict(gain_db=g,lin=10**(g/20)),open(f'{H}/out/gain-{tag}-{k}.json','w'))
    # second pass: single-pass loudnorm lands ~2 LU low on a short reel with long reading pauses; measure and correct
    import re as _re
    m=subprocess.run(['ffmpeg','-v','info','-i',wav,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
    I=float(_re.findall(r'I:\s+(-?[\d.]+) LUFS',m)[-1]); fix=-14.0-I
    tmp=wav[:-4]+'-pre.wav'; os.replace(wav,tmp)
    subprocess.run(['ffmpeg','-y','-v','error','-i',tmp,'-af',f'volume={fix}dB,alimiter=limit=0.78:level=false','-ar','48000',wav],check=True)
    print(k,'integrated',I,'-> corrected by',round(fix,2),'dB')
    res[k]=round(band(load(duck))-vb,1)
    out=f"{H}/out/ep86v4-{tag}-{k}.mp4"
    subprocess.run(['ffmpeg','-y','-v','error','-i',vid,'-i',wav,'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(D),out],check=True)
    subprocess.run(['ffmpeg','-y','-v','error','-i',out,'-vf','scale=720:-2','-c:v','libx264','-crf','28','-preset','veryfast','-c:a','aac','-b:a','96k',f"{H}/out/ep86v4-{tag}-{k}-720.mp4"],check=True)
    print(k,f,"bed ducked vs voice (300-3500 Hz):",res[k],"dB")
json.dump(res,open(f"{H}/out/bedlevels-{tag}.json","w"))
