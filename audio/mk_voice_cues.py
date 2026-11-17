#!/usr/bin/env python3
"""mk_voice_cues.py <raw.wav> <raw-cues.json> <out-narration.wav> <out-cues.json> [tempo=1.12]
ep89 recipe step 3: fast take (atempo) + faster-whisper word times per line -> cues json {lines:[{n,text,start,end,words}],D}."""
import sys, json, subprocess, soundfile as sf
raw, rc, outw, outc = sys.argv[1:5]; T = float(sys.argv[5]) if len(sys.argv) > 5 else 1.12
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"atempo={T}", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", outw], check=True)
x, s = sf.read(outw); x = x if x.ndim == 1 else x[:, 0]
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
lines = []
for c in json.load(open(rc)):
    a0, b0 = c["start"] / T, c["end"] / T
    a = max(0, a0 - .08); b = min(len(x) / s, b0 + .1)
    sf.write("/tmp/_l.wav", x[int(a * s):int(b * s)], s, subtype="PCM_16")
    seg, _ = m.transcribe("/tmp/_l.wav", language="en", word_timestamps=True)
    ws = [[w.word.strip(), round(a + w.start, 3), round(a + w.end, 3)] for sg in seg for w in (sg.words or [])]
    lines.append(dict(n=c["n"], text=c["line"], start=round(a0, 3), end=round(b0, 3), words=ws))
json.dump(dict(lines=lines, D=round(len(x) / s, 2)), open(outc, "w"), indent=1)
print(outw, round(len(x) / s, 2), "s;", [(l["n"], l["start"], l["end"]) for l in lines])
