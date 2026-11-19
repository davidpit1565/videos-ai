import numpy as np, soundfile as sf, subprocess
from kokoro import KPipeline
P = KPipeline(lang_code='a')
for v, sp in (('af_heart', 1.0), ('af_heart', .95), ('af_heart', .9), ('af_sarah', 1.0)):
    a = np.concatenate([x[2].numpy() for x in P("Claude and Gemini too.", voice=v, speed=sp)]); sf.write('/tmp/l5.wav', a, 24000)
    subprocess.run(['ffmpeg','-y','-v','error','-i','/tmp/l5.wav','-ar','48000','-ac','1','-sample_fmt','s16',f'takes/{v}-L5-s{sp:.2f}.wav'])
