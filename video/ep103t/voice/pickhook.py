# /opt/v311/bin/python pickhook.py <tag> : among pl/H-<tag>-<seed>.wav keep those whose Whisper text equals the hook text (and "Claude" is one word, no gap > .12 s inside names), pick the lowest accent score. prints the chosen wav path (last line).
import json, os, re, sys, soundfile as sf
from faster_whisper import WhisperModel
D = os.path.dirname(os.path.abspath(__file__)) + '/'; tag = sys.argv[1]
norm = lambda t: re.sub(r"[^a-z0-9 ]", "", t.lower().replace('-', ' ').replace('eleven','11').replace('11','eleven')).split()
want = norm(open(D + f'pl/H-{tag}.txt').read())
acc = {}
for l in open(D + f'pl/out-{tag}.txt'):
    m = re.match(r'H-\S+ seed (\d+) .* accent ([0-9.]+)', l)
    if m: acc[m.group(1)] = float(m.group(2))
m = WhisperModel('small.en', device='cpu', compute_type='int8'); best = None
for seed, a in acc.items():
    p = D + f'pl/H-{tag}-{seed}.wav'
    if not os.path.exists(p): continue
    segs, _ = m.transcribe(p, language='en', word_timestamps=True); ws = [w for s in segs for w in s.words]
    got = norm(' '.join(w.word for w in ws)); ok = got == want
    print('seed', seed, 'accent', a, 'text', 'OK' if ok else 'DIFF', ' '.join(got), file=sys.stderr)
    if ok and (best is None or a < best[0]): best = (a, p)
if best is None: print('NOMATCH'); sys.exit(1)
print(best[1])
