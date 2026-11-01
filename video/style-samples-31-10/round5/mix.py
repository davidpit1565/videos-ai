import json, subprocess, sys, os, glob, numpy as np
SR=48000
V="/tmp/claude-0/-home-user-videos-ai/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/scratchpad/voice/lines"
def rd(p):
    raw=subprocess.run(["ffmpeg","-loglevel","error","-i",p,"-f","f32le","-ar",str(SR),"-ac","1","-"],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32).copy()
def dur(p): return len(rd(p))/SR
SECTION_END={2,7,10,13}
def cues_from_files(files):
    c=[0]*15; t=0.12
    for i in range(1,15):
        c[i]=round(t,3); d=dur(files[i]); t+=d+(0.75 if i in SECTION_END else 0.35)
    return c
def sfx(kind):
    t=np.arange(int(SR*0.6))/SR
    if kind=="pop":
        n=int(SR*.09); x=np.sin(2*np.pi*(700+500*np.exp(-np.arange(n)/SR*40))*np.arange(n)/SR)*np.exp(-np.arange(n)/SR*45); return x*0.45
    if kind=="click":
        n=int(SR*.05); rng=np.random.default_rng(3); x=rng.standard_normal(n)*np.exp(-np.arange(n)/SR*120); return x*0.5
    if kind=="buzz":
        n=int(SR*.5); tt=np.arange(n)/SR
        x=np.where(tt<.22,np.sign(np.sin(2*np.pi*190*tt)),np.sign(np.sin(2*np.pi*140*tt)))*0.5; x=x*np.exp(-np.maximum(tt-0.35,0)*20)*(tt<0.46); return x*0.55
    if kind=="chime":
        n=int(SR*.7); tt=np.arange(n)/SR
        return (np.sin(2*np.pi*880*tt)+0.7*np.sin(2*np.pi*1320*tt)+0.4*np.sin(2*np.pi*1760*tt))*np.exp(-tt*5)*0.28
    if kind=="whoosh":
        n=int(SR*.55); rng=np.random.default_rng(5); x=rng.standard_normal(n); k=np.ones(40)/40; x=x-np.convolve(x,k,'same')
        env=np.sin(np.pi*np.arange(n)/n)**2; return x*env*0.22
    return np.zeros(10)
def mix(video,events_json,lines_json,out,music_vol=0.2,music_track="confident--innovation--atlasaudio.mp3"):
    ev=json.load(open(events_json)); D=ev["D"]
    files={}
    for e in json.load(open(lines_json))["lines"] if isinstance(json.load(open(lines_json)),dict) else json.load(open(lines_json)):
        files[int(e["number"])]=e["file"] if os.path.isabs(e["file"]) else os.path.join(V,os.path.basename(e["file"]))
    c=cues_from_files(files)
    N=int(SR*(D+0.3)); nar=np.zeros(N,dtype=np.float32); fx=np.zeros(N,dtype=np.float32)
    for i in range(1,15):
        x=rd(files[i]); s=int(c[i]*SR); nar[s:s+len(x)]+=x[:max(0,N-s)]
    for tt,k in ev["events"]:
        x=sfx(k); s=int(tt*SR); fx[s:s+len(x)]+=x[:max(0,N-s)]
    sec=D+0.3
    mp="/tmp/g/music.wav"
    env=dict(os.environ,FORCE_TRACK=music_track)
    subprocess.run(["python3","/home/user/videos-ai/audio/pick_real_track.py",f"{sec:.2f}",mp,"--mood","confident","--no-record"],cwd="/home/user/videos-ai",env=env,check=True,stdout=subprocess.DEVNULL)
    mus=rd(mp)[:N]; mus=np.pad(mus,(0,N-len(mus)))
    # duck music under narration
    env_n=np.convolve(np.abs(nar),np.ones(int(SR*.25))/int(SR*.25),'same'); duck=1-0.55*np.clip(env_n/0.05,0,1)
    mixed=nar*1.0+fx*0.6+mus*music_vol*duck
    mixed=mixed/ max(1e-6,np.max(np.abs(mixed)))*0.9
    wav="/tmp/g/mix.wav"
    subprocess.run(["ffmpeg","-loglevel","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","pipe:0",wav],input=mixed.astype(np.float32).tobytes(),check=True)
    m=subprocess.run(["ffmpeg","-hide_banner","-i",wav,"-af","loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json","-f","null","-"],capture_output=True,text=True).stderr
    import re
    j=json.loads(m[m.rindex("{"):m.rindex("}")+1])
    af=f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,aformat=sample_rates=48000:channel_layouts=stereo"
    subprocess.run(["ffmpeg","-loglevel","error","-y","-i",video,"-i",wav,"-filter_complex",f"[1:a]{af}[a]","-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","-shortest",out],check=True)
    return c
if __name__=="__main__":
    video,events,lines,out=sys.argv[1:5]; print(mix(video,events,lines,out))
