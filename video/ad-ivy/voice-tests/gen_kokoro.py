# gen_kokoro.py <voice> <speed> : Kokoro-82M (Apache 2.0) preset voice, both test lines -> ivy-kokoro-<voice>-L<n>.wav 48 kHz mono
import sys, numpy as np, soundfile as sf, subprocess
from kokoro import KPipeline
v, sp = sys.argv[1], float(sys.argv[2])
P = KPipeline(lang_code='a')
T = ["You talk. Ivy drafts the email. Done.", "ChatGPT knows your whole life. Your next AI shouldn't start from zero."]
for n, t in enumerate(T, 1):
    a = np.concatenate([x[2].numpy() for x in P(t, voice=v, speed=sp)])
    sf.write(f'/tmp/k{n}.wav', a, 24000)
    subprocess.run(['ffmpeg','-y','-v','error','-i',f'/tmp/k{n}.wav','-ar','48000','-ac','1',f'ivy-kokoro-{v}-L{n}.wav'])
    print(v, n, len(a)/24000)
