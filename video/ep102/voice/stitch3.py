# stitch.py (run with /opt/v311/bin/python): joins the accepted take of every line (pl2/L<i>.ok) into narration-v3.wav
# + narration-v3-cues.json. Pauses INSIDE a line are capped (hook lines 1-3: 0.14 s, others 0.24 s) by cutting only
# silence (below -30 dB of the line's peak) with 6 ms fades: no speech is removed or sped up.
import json, os, numpy as np, soundfile as sf
D = os.path.dirname(os.path.abspath(__file__)) + '/'
lines = [l.rstrip('\n') for l in open(D + 'lines.txt') if l.strip()]
GAP = 0.03
def tighten(x, sr, cap):
    fr = int(.01 * sr); n = len(x) // fr
    rms = np.sqrt((x[:n * fr].reshape(n, fr) ** 2).mean(1) + 1e-12); thr = np.abs(x).max() * 10 ** (-30 / 20)
    sil = rms < thr; out = []; i = 0; cut = 0.0; keep = int(cap / .01)
    segs = []                                   # (start_frame, end_frame) to drop
    while i < n:
        if sil[i]:
            j = i
            while j < n and sil[j]: j += 1
            if j - i > keep and i > 0 and j < n: segs.append((i + keep // 2, j - (keep - keep // 2)))
            i = j
        else: i += 1
    if not segs: return x, 0.0
    f = int(.006 * sr); pos = 0; parts = []
    for a, b in segs:
        p = x[pos:a * fr].copy(); p[-f:] *= np.linspace(1, 0, f); parts.append(p)
        pos = b * fr; cut += (b - a) * .01
    p = x[pos:].copy(); parts.append(p)
    for k in range(1, len(parts)): parts[k][:f] *= np.linspace(0, 1, f)
    return np.concatenate(parts), cut
out = []; cues = []; t = 0.0; sr = None; rep = []
for i, l in enumerate(lines, 1):
    seed = open(D + f'pl2/L{i}.ok').read().strip()
    w, s_ = sf.read(D + f'pl2/L{i}-{seed}.wav'); sr = sr or s_
    if w.ndim > 1: w = w.mean(1)
    c = json.load(open(D + f'pl2/L{i}-{seed}-cues.json'))[0]
    a = max(0, int((c['start'] - 0.04) * sr)); b = min(len(w), int((c['end'] + 0.08) * sr))
    seg, cut = tighten(w[a:b].copy(), sr, .14 if i <= 2 else .22)
    f = int(0.012 * sr); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    g_ = 0.2 if 3 <= i <= 6 else GAP; out.append(seg); out.append(np.zeros(int(g_ * sr)))
    cues.append({'n': i, 'line': l, 'start': round(t + 0.04, 3), 'end': round(t + len(seg) / sr - 0.08, 3)})
    rep.append((i, seed, round(len(seg) / sr - .12, 2), round(cut, 2)))
    t += len(seg) / sr + g_
y = np.concatenate(out); sf.write(D + 'narration-v3.wav', y, sr, subtype='PCM_16')
json.dump(cues, open(D + 'narration-v3-cues.json', 'w'), indent=1)
print(sr, 'total', round(len(y) / sr, 2), 's; (line, seed, spoken s, silence cut s):', rep)
