# stitch105.py v2 (/opt/v311/bin/python): joins chosen v2 takes into narration-v105.wav, narration-v105-cues.json, ../cues105.json
# Line 10 = locked canonical clip; line 11 = real ep104 take cut from ../../ep104/voice/narration.wav 43.74-46.00 s (pl/L11-ep104cut.wav; the earlier pl/L13-ep104.wav was digital silence).
# CAP: pauses inside a line are shortened by cutting only silence (below -22 dB (line 1: its pause sits at -28..-32 dB, room tone is not silent) of the line peak), 6 ms fades; no speech touched.
import json, os, numpy as np, soundfile as sf
D = os.path.dirname(os.path.abspath(__file__)) + '/'
PICK = {1: 33, 2: 22, 3: 33, 4: 22, 5: 33, 6: 22, 7: 11, 8: 22, 9: 44, 10: 11}
CAP = {1: 0.26}          # seconds of silence kept inside the line (hook must flow)
lines = [l.strip() for l in open(D + 'lines105.txt') if l.strip()]
def cap_silence(w, sr, cap):
    fr = int(.005 * sr); n = len(w) // fr; thr = 10 ** (-22 / 20) * np.abs(w).max()
    rms = np.sqrt((w[:n * fr].reshape(n, fr) ** 2).mean(1)); sil = rms < thr
    first = np.argmax(~sil); last = n - 1 - np.argmax(~sil[::-1]); keep = np.ones(n, bool); i = first
    while i <= last:
        if sil[i]:
            j = i
            while j <= last and sil[j]: j += 1
            if (j - i) * .005 > cap + .02:
                keep[i + int(cap / .005):j] = False
            i = j
        else: i += 1
    out = []; start = None
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
out = []; cues = []; t = 0.0; GAP = .06
for n, l in enumerate(lines, 1):
    p = D + ('pl/L11-ep104cut.wav' if n == 11 else f'pl/V2-L{n}-{PICK[n]}.wav')
    w, sr = sf.read(p)
    if w.ndim > 1: w = w.mean(1)
    if n in CAP: w = cap_silence(w, sr, CAP[n])
    f = int(.01 * sr); w = w.copy(); w[:f] *= np.linspace(0, 1, f); w[-f:] *= np.linspace(1, 0, f)
    out += [w, np.zeros(int(GAP * sr))]
    cues.append({'n': n, 'line': l, 'text': l, 'start': round(t + .05, 3), 'end': round(t + len(w) / sr - .08, 3)}); t += len(w) / sr + GAP
y = np.concatenate(out); sf.write(D + 'narration-v105.wav', y, sr, subtype='PCM_16')
json.dump(cues, open(D + 'narration-v105-cues.json', 'w'), indent=1)
json.dump({'version': 'v2', 'estimated_timeline': False, 'lines': cues, 'D': round(len(y) / sr, 2)}, open(D + '../cues105.json', 'w'), indent=1)
print(sr, round(len(y) / sr, 2)); [print(c['n'], round(c['end'] - c['start'], 2), c['start']) for c in cues]
