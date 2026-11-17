# Whisper check per accepted line (run with /opt/v311/bin/python). Prints the transcript, a similarity ratio and the
# largest gap between words; brand names are often spelled differently by Whisper, so read the transcript by eye.
import sys, re, json, os, difflib
from faster_whisper import WhisperModel
D = os.path.dirname(os.path.abspath(__file__)) + '/'
lines = [l.strip() for l in open(D + 'lines.txt') if l.strip()]
m = WhisperModel('small.en', device='cpu', compute_type='int8')
only = [int(x) for x in sys.argv[1:]]
n = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
for i, l in enumerate(lines, 1):
    if only and i not in only: continue
    if not os.path.exists(D + f'pl/L{i}.ok'): continue
    seed = open(D + f'pl/L{i}.ok').read().strip()
    segs, _ = m.transcribe(D + f'pl/L{i}-{seed}.wav', word_timestamps=True, language='en')
    ws = [w for s in segs for w in s.words]
    txt = ' '.join(w.word.strip() for w in ws)
    gaps = sorted(((round(ws[k + 1].start - ws[k].end, 2), ws[k].word.strip() + '|' + ws[k + 1].word.strip()) for k in range(len(ws) - 1)), reverse=True)[:2]
    r = difflib.SequenceMatcher(None, n(txt), n(l)).ratio()
    dur = round(ws[-1].end - ws[0].start, 2) if ws else 0
    print(f'L{i} seed {seed} ratio {r:.2f} dur {dur} gaps {gaps}\n   said: {txt}\n   want: {l}')
