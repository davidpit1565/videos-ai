# wcheck.py <wav> <expected text>: faster-whisper word times, text match, gaps (run with /opt/v311/bin/python)
import sys, re
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
seg, _ = m.transcribe(sys.argv[1], language="en", word_timestamps=True)
w = [x for s in seg for x in s.words]
norm = lambda t: re.sub(r"[^a-z0-9 ]", "", t.lower())
got = norm(" ".join(x.word for x in w)); exp = norm(sys.argv[2])
print("MATCH" if got.split() == exp.split() else "DIFF", "|", got)
print("gaps", [(w[i].word.strip(), w[i+1].word.strip(), round(w[i+1].start - w[i].end, 2)) for i in range(len(w)-1) if w[i+1].start - w[i].end > .1])
print("span", round(w[0].start, 2), round(w[-1].end, 2))
