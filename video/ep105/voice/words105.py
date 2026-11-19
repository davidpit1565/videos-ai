# words105.py (/opt/v311/bin/python): faster-whisper small.en word times for narration-v105.wav -> words-v105.json (same format as words.json), and a silence check on every cue window (fails under -35 dB)
import json, os, sys, numpy as np, soundfile as sf
from faster_whisper import WhisperModel
D = os.path.dirname(os.path.abspath(__file__)) + '/'
m = WhisperModel('small.en', device='cpu', compute_type='int8')
segs, _ = m.transcribe(D + 'narration-v105.wav', word_timestamps=True, language='en')
ws = [dict(word=w.word.strip(), start=round(w.start, 2), end=round(w.end, 2)) for s in segs for w in s.words]
json.dump(ws, open(D + 'words-v105.json', 'w'), indent=1)
w, sr = sf.read(D + 'narration-v105.wav'); bad = False
for c in json.load(open(D + 'narration-v105-cues.json')):
    x = w[int(c['start'] * sr):int(c['end'] * sr)]; r = 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)
    print('line', c['n'], 'RMS %.1f dB' % r, 'SILENT!' if r < -35 else ''); bad |= r < -35
for k, v in enumerate(ws[:-1]):
    g = ws[k + 1]['start'] - v['end']
    if g > .1 and ws[k + 1]['start'] < 3: print('gap', v['word'], ws[k + 1]['word'], round(g, 2))
print(' '.join(x['word'] for x in ws[:8]), '...', ' '.join(x['word'] for x in ws[-9:]), ws[-9]['start'], ws[-1]['end'])
sys.exit(1 if bad else 0)
