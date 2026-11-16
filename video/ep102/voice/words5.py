# words.json for the stitched narration: faster-whisper small.en word times (run with /opt/v311/bin/python). No TTS.
import json, os
from faster_whisper import WhisperModel
D = os.path.dirname(os.path.abspath(__file__)) + '/'
m = WhisperModel('small.en', device='cpu', compute_type='int8')
segs, _ = m.transcribe(D + 'narration-v5.wav', word_timestamps=True, language='en')
ws = [dict(word=w.word.strip(), start=round(w.start, 2), end=round(w.end, 2)) for s in segs for w in s.words]
json.dump(ws, open(D + 'words-v5.json', 'w'), indent=1)
print(len(ws), 'words:', ' '.join(w['word'] for w in ws))
