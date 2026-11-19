# /opt/v311/bin/python pickbody.py : per body line choose the take whose Whisper text equals the line and with the lowest accent score; writes body-picks.json
import json, os, re, sys
from faster_whisper import WhisperModel
D = os.path.dirname(os.path.abspath(__file__)) + '/'
norm = lambda t: re.sub(r"[^a-z0-9 ]", "", t.lower().replace('-', ' ').replace('eleven','11').replace('11','eleven')).split()
lines = [l.strip() for l in open(D + 'body.txt') if l.strip()]
acc = {}
for l in open(D + 'pl/out.txt'):
    m = re.match(r'B(\d+) seed (\d+) .* accent ([0-9.]+)', l)
    if m: acc[(int(m.group(1)), m.group(2))] = float(m.group(3))
m = WhisperModel('small.en', device='cpu', compute_type='int8'); picks = {}; okc = {}
for i, ln in enumerate(lines, 1):
    want = norm(ln); cands = []
    for (k, seed), a in sorted(acc.items()):
        if k != i: continue
        p = f'pl/B{i}-{seed}.wav'
        if not os.path.exists(D + p): continue
        segs, _ = m.transcribe(D + p, language='en'); got = norm(' '.join(s.text for s in segs))
        cands.append((got == want, a, p)); print(i, seed, a, 'OK' if got == want else 'DIFF', ' '.join(got))
    ok = [c for c in cands if c[0]]; okc[str(i)] = [c[2] for c in ok]
    if ok: picks[str(i)] = min(ok, key=lambda c: c[1])[2]
    else: print('NO MATCH line', i)
json.dump(picks, open(D + 'body-picks.json', 'w'), indent=1); json.dump(okc, open(D + 'ok-cands.json', 'w'), indent=1); print(picks)
