import sys, subprocess, re, numpy as np, soundfile as sf, json
from scipy.signal import butter, sosfilt
from scipy.ndimage import uniform_filter1d
bedp, outp = sys.argv[1], sys.argv[2]
C = json.load(open('/tmp/e4/v/cues4.json')); L = {l['n']: l for l in C['lines']}; D = C['D']; SR = 48000; N = int(D * SR)
SFXD = "/home/user/videos-ai/video/ep93/sfx/"
def load(p): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,dtype=np.float32).astype(np.float64)
def sst(x): x=np.clip(x,0,1); return x*x*(3-2*x)
lay = np.zeros(N + SR)
def put(name, t, db):
    x = load(SFXD+name+".ogg"); x = x/(np.abs(x).max()+1e-9)*10**(db/20); i0=int(t*SR); n=min(len(x),len(lay)-i0)
    if n>0 and t<D-0.1: lay[i0:i0+n]+=x[:n]
put("impactsoft",0.03,-24); put("ding",L[3]['words'][4][1]-0.05,-23); put("impactsoft",L[4]['start']-0.02,-24)
nar = load('/tmp/e4/v/narration92v4.wav'); nar=np.pad(nar,(0,max(0,N-len(nar))))[:N]; nar*=10**(-3/20)/np.abs(nar).max()
t=np.arange(N)/SR; mix=lay[:N]+nar
bed=load(bedp); bed=sosfilt(butter(4,150,btype='high',fs=SR,output='sos'),bed); bed=np.pad(bed,(0,max(0,N-len(bed))))[:N]; sf.write('/tmp/e4/bed_hp.wav',bed,SR,subtype='PCM_16')
sos=butter(4,[300,3500],btype='band',fs=SR,output='sos')
sp=uniform_filter1d(np.abs(nar),int(.12*SR)); on=(sp>0.02).astype(float); on=np.clip(uniform_filter1d(on,int(.25*SR))*2.0,0,1)
duck=1-(1-10**(-6/20))*on
shape=np.ones(N)
shape*=1+(10**(2.0/20)-1)*sst((t-L[3]['start']+0.3)/0.5)*(1-sst((t-L[3]['end']-0.3)/0.6))   # small lift on the surprise beat
shape*=1-sst((t-(D-1.6))/1.6)
bs=bed*duck*shape; vb=sosfilt(sos,nar); bb=sosfilt(sos,bs); m=on>0.9
vr=np.sqrt(np.mean(vb[m]**2)); br=np.sqrt(np.mean(bb[m]**2))+1e-9; gain=vr/br*10**(-15/20)
bm=bs*gain; mix=mix+bm
ns=10**(-3/20)/1.0; print("bed gain dB",round(20*np.log10(gain),2),"gain",gain)
sf.write('/tmp/e4/_pre.wav',mix,SR,subtype='PCM_16')
mm=subprocess.run(['ffmpeg','-i','/tmp/e4/_pre.wav','-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
I=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',mm)[-1]); g=-14.0-I
subprocess.run(['ffmpeg','-y','-v','error','-i','/tmp/e4/_pre.wav','-af',f'volume={g}dB,alimiter=limit=0.88:attack=3:release=80:level=false,afade=t=out:st={D-0.35}:d=0.35','-ar','48000','-ac','2',outp],check=True)
sf.write(outp.replace('.wav','-bedonly.wav'),(bm*10**(g/20)).astype(np.float32),SR,subtype='PCM_16')
print("pre",I,"gain",round(g,2))
