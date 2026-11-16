# wcand.py <wav...>: Whisper transcript, spoken duration and the two largest word gaps for candidate takes
import sys
from faster_whisper import WhisperModel
m = WhisperModel('small.en', device='cpu', compute_type='int8')
for f in sys.argv[1:]:
    segs, _ = m.transcribe(f, word_timestamps=True, language='en'); ws = [w for s in segs for w in s.words]
    gaps = sorted(((round(ws[k + 1].start - ws[k].end, 2), ws[k].word.strip() + '|' + ws[k + 1].word.strip()) for k in range(len(ws) - 1)), reverse=True)[:2]
    print(f.split('/')[-1], round(ws[-1].end - ws[0].start, 2) if ws else 0, gaps, '::', ' '.join(w.word.strip() for w in ws))
