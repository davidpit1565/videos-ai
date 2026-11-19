# /opt/v311/bin/python words.py <tag> : Whisper small.en word times -> words-<tag>.json; silence check per cue line
import json, os, sys, numpy as np, soundfile as sf
from faster_whisper import WhisperModel
D = os.path.dirname(os.path.abspath(__file__)) + '/'; tag = sys.argv[1]
m = WhisperModel('small.en', device='cpu', compute_type='int8')
segs, _ = m.transcribe(D + f'narration-{tag}.wav', word_timestamps=True, language='en')
ws = [dict(word=w.word.strip(), start=round(w.start, 2), end=round(w.end, 2)) for s in segs for w in s.words]
json.dump(ws, open(D + f'words-{tag}.json', 'w'), indent=1)
w, sr = sf.read(D + f'narration-{tag}.wav'); bad = False
for c in json.load(open(D + f'cues-{tag}.json'))['lines']:
    x = w[int(c['start'] * sr):int(c['end'] * sr)]; r = 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)
    if r < -35: print('line', c['n'], 'SILENT'); bad = True
print('HOOK AS SPOKEN:', ' '.join(x['word'] for x in ws if x['start'] < json.load(open(D + f'cues-{tag}.json'))['lines'][0]['end'] + .1))
import re
nz=lambda t: re.sub(r'[^a-z0-9 ]','',t.lower().replace('-',' ').replace('eleven','11')).split()
want=nz(' '.join(c['line'] for c in json.load(open(D + f'cues-{tag}.json'))['lines'])); got=nz(' '.join(x['word'] for x in ws))
if want!=got: print('TEXT MISMATCH:', ' '.join(got)); bad=True
sys.exit(1 if bad else 0)
