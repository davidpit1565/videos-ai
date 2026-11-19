# /opt/v311/bin/python stitch.py <tag> : hook take (voice/pl/H-<tag>.wav, or pl/H<k>-<seed>.wav via HOOKWAV env) + cached body takes (BODY pick list) -> voice/narration-<tag>.wav, voice/cues-<tag>.json
import json, os, sys, numpy as np, soundfile as sf
D = os.path.dirname(os.path.abspath(__file__)) + '/'
tag = sys.argv[1]; hook_wav = os.environ['HOOKWAV']
PICK = json.load(open(os.environ.get('PICKS', D + 'body-picks.json')))          # {"1": "pl/B1-11.wav", ... "10": ...}  body lines 2-11 = B1..B10
CAP = 0.26                                              # silence kept inside the hook (must flow)
lines = [l.strip() for l in open(D + 'body.txt') if l.strip()]
hook = open(os.environ.get('HOOKTXT', D + 'pl/H-' + tag + '.txt')).read().strip()
def cap_silence(w, sr, cap):
    fr = int(.005 * sr); n = len(w) // fr; thr = 10 ** (-22 / 20) * np.abs(w).max()
    rms = np.sqrt((w[:n * fr].reshape(n, fr) ** 2).mean(1)); sil = rms < thr
    first = np.argmax(~sil); last = n - 1 - np.argmax(~sil[::-1]); keep = np.ones(n, bool); i = first
    while i <= last:
        if sil[i]:
            j = i
            while j <= last and sil[j]: j += 1
            if (j - i) * .005 > cap + .02: keep[i + int(cap / .005):j] = False
            i = j
        else: i += 1
    segs = []; s = 0
    for k in range(n + 1):
        if k == n or (k > 0 and keep[k] != keep[k - 1]):
            if keep[k - 1] and k > s: segs.append((s, k))
            s = k
    parts = []
    for a, b in segs:
        x = w[a * fr:b * fr].copy(); f = min(int(.006 * sr), len(x) // 2)
        if a > 0: x[:f] *= np.linspace(0, 1, f)
        if b < n: x[-f:] *= np.linspace(1, 0, f)
        parts.append(x)
    return np.concatenate(parts + [w[n * fr:]])
srcs = [(hook, hook_wav)] + [(l, D + PICK[str(i + 1)]) for i, l in enumerate(lines)]
out = []; cues = []; t = 0.0; GAP = .06
for n, (l, p) in enumerate(srcs, 1):
    w, sr = sf.read(p)
    if w.ndim > 1: w = w.mean(1)
    if n == 1: w = cap_silence(w, sr, CAP)
    f = int(.01 * sr); w = w.copy(); w[:f] *= np.linspace(0, 1, f); w[-f:] *= np.linspace(1, 0, f)
    out += [w, np.zeros(int(GAP * sr))]
    cues.append({'n': n, 'line': l, 'text': l, 'start': round(t + .05, 3), 'end': round(t + len(w) / sr - .08, 3)}); t += len(w) / sr + GAP
y = np.concatenate(out); sf.write(D + f'narration-{tag}.wav', y, sr, subtype='PCM_16')
json.dump({'version': tag, 'estimated_timeline': False, 'lines': cues, 'D': round(len(y) / sr, 2)}, open(D + f'cues-{tag}.json', 'w'), indent=1)
print(sr, round(len(y) / sr, 2)); [print(c['n'], round(c['end'] - c['start'], 2), c['start']) for c in cues]
