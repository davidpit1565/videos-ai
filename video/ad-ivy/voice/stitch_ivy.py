# stitch_ivy.py (/opt/v311/bin/python): joins the chosen Kokoro af_heart takes -> narration-ivy.wav, ../cues-ivy.json, words-ivy.json (Whisper), with a silence check on every cue window.
# Per take: trim edge silence, cap inner pauses to CAP s by cutting only digital-quiet frames (<-40 dB of peak), gain to about -19.5 dB RMS (peak kept under -1 dBFS), 10 ms fades, GAP between lines.
import json, os, sys, numpy as np, soundfile as sf
D = os.path.dirname(os.path.abspath(__file__)) + '/'
PICK = {1: 1.15, 2: 1.05, 3: 1.10, 4: 1.10, 5: 1.05, 6: 1.10, 7: 1.15, 8: 1.05, 9: 1.10, 10: 1.10, 11: 1.10, 12: 1.10, 13: 1.10}
CAPS = {1: 0.05}; CAP = 0.09; GAP = 0.09; TARGET = -19.5
lines = [l.strip() for l in open(D + 'lines-ivy.txt') if l.strip()]
def tidy(w, sr, CAP):
    fr = int(.005 * sr); n = len(w) // fr; thr = 10 ** (-40 / 20) * np.abs(w).max()
    sil = np.sqrt((w[:n * fr].reshape(n, fr) ** 2).mean(1)) < thr
    a = np.argmax(~sil); b = n - np.argmax(~sil[::-1]); keep = np.ones(n, bool); i = a
    while i < b:
        if sil[i]:
            j = i
            while j < b and sil[j]: j += 1
            if (j - i) * .005 > CAP + .01: keep[i + int(CAP / .005):j] = False
            i = j
        else: i += 1
    x = np.concatenate([w[k * fr:(k + 1) * fr] for k in range(max(a - 4, 0), min(b + 4, n)) if keep[k] or k < a or k >= b])
    return x
out = []; cues = []; t = 0.0
for n, l in enumerate(lines, 1):
    w, sr = sf.read(D + f'takes/af_heart-L{n}-s{PICK[n]:.2f}.wav')
    w = tidy(w, sr, CAPS.get(n, CAP)); r = 20 * np.log10(np.sqrt((w ** 2).mean()) + 1e-9); w = w * 10 ** ((TARGET - r) / 20)
    pk = np.abs(w).max()
    if pk > 10 ** (-1 / 20): w = w * 10 ** (-1 / 20) / pk
    f = int(.01 * sr); w[:f] *= np.linspace(0, 1, f); w[-f:] *= np.linspace(1, 0, f)
    out += [w, np.zeros(int(GAP * sr))]
    cues.append({'n': n, 'line': l, 'text': l, 'start': round(t + .02, 3), 'end': round(t + len(w) / sr - .02, 3)}); t += len(w) / sr + GAP
y = np.concatenate(out); sf.write(D + 'narration-ivy.wav', y, sr, subtype='PCM_16'); Dd = round(len(y) / sr, 2)
json.dump({'version': 'v1', 'estimated_timeline': False, 'lines': cues, 'D': Dd}, open(D + '../cues-ivy.json', 'w'), indent=1)
json.dump(cues, open(D + 'narration-ivy-cues.json', 'w'), indent=1)
from faster_whisper import WhisperModel
ws = [dict(word=w.word.strip(), start=round(w.start, 2), end=round(w.end, 2)) for s in WhisperModel('small.en', device='cpu', compute_type='int8').transcribe(D + 'narration-ivy.wav', word_timestamps=True, language='en')[0] for w in s.words]
json.dump(ws, open(D + 'words-ivy.json', 'w'), indent=1)
bad = False
for c in cues:
    x = y[int(c['start'] * sr):int(c['end'] * sr)]; r = 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9); bad |= r < -35
    print('line', c['n'], 'dur %.2f' % (c['end'] - c['start']), 'start %.2f' % c['start'], 'RMS %.1f' % r, 'SILENT!' if r < -35 else '')
print('D', Dd, 'words', len(ws)); sys.exit(1 if bad else 0)
