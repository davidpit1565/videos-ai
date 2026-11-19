# gen_ivy.py [voice] : Kokoro-82M takes per line at speeds 1.05/1.10/1.15 -> takes/<voice>-L<n>-s<speed>.wav (48 kHz mono). Deterministic; one TTS at a time (run under flock /tmp/tts.lock)
import sys, os, numpy as np, soundfile as sf, subprocess
from kokoro import KPipeline
V = sys.argv[1] if len(sys.argv) > 1 else 'af_heart'
D = os.path.dirname(os.path.abspath(__file__)) + '/'
P = KPipeline(lang_code='a')
for n, t in enumerate([l.strip() for l in open(D + 'lines-ivy.txt') if l.strip()], 1):
    for sp in (1.05, 1.10, 1.15):
        a = np.concatenate([x[2].numpy() for x in P(t, voice=V, speed=sp)])
        sf.write('/tmp/ivy-k.wav', a, 24000)
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', '/tmp/ivy-k.wav', '-ar', '48000', '-ac', '1', '-sample_fmt', 's16', D + f'takes/{V}-L{n}-s{sp:.2f}.wav'])
print('done')
