import json,sys,soundfile as sf,os
tag=sys.argv[1]; out=f"voice/{tag}"; os.makedirs(out,exist_ok=True)
d=json.load(open(f"voice/{tag}-cues.json")); L=d if isinstance(d,list) else d.get("cues",d.get("lines"))
x,sr=sf.read(f"voice/{tag}.wav")
for i,c in enumerate(L,1):
    a=int(max(0,c["start"]-0.02)*sr); b=int((c["end"]+0.04)*sr)
    sf.write(f"{out}/{i}.wav",x[a:b],sr,subtype="PCM_16"); print(i,round(c["end"]-c["start"],2),c.get("text",c.get("line","")) [:40])
