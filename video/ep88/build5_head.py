#!/usr/bin/env python3
"""ep88 round 5 builder: fast top-funnel cut. lines5.txt (7 lines) + VOICE/<n>.wav -> cues5.json, out/narration5.wav, sfx5.json, hf/index.html [--render name].
Fonts: Big Shoulders Bold (hero, condensed), Fraunces 600 (contrast serif), Inter Display (UI). All open licence (SIL OFL)."""
import json, os, re, sys, subprocess
import soundfile as sf, numpy as np
H = os.path.dirname(os.path.abspath(__file__))
VOICE = os.environ.get("VOICE", H + "/voice5/final")
GAPS = [float(x) for x in os.environ.get("GAPS", "0.3,0.28,0.85,0.3").split(",")]
TAIL = float(os.environ.get("TAIL", "1.4"))
ALL = [l.rstrip("\n") for l in open(H + "/lines5.txt") if l.strip()]
assert len(ALL) == 5 and len(GAPS) == 4
sr = 48000
src = open(H + "/build_head.py").read()
exec(src[src.index("def words_for"):src.index("lines = []; t = 0.0")])   # reuse words_for
tsrc = open(H + "/build_tail_r4a.py").read() if False else open(H + "/build_tail.py").read()
a = tsrc.index("def scene(k):"); b = tsrc.index("def feed(sfx):")
exec(tsrc[a:b])   # drawn everyday scenes

import hashlib
def whisper_words(path, text, t0):
    """real word stamps from faster-whisper (small) when the word count matches the script; None otherwise"""
    cache = H + "/voice5/words-cache.json"
    c = json.load(open(cache)) if os.path.exists(cache) else {}
    key = hashlib.md5(open(path, "rb").read()).hexdigest()
    if key not in c:
        out = subprocess.run(["/opt/v311/bin/python", "-c", "import sys,json;from faster_whisper import WhisperModel;m=WhisperModel('small',device='cpu',compute_type='int8');seg,_=m.transcribe(sys.argv[1],language='en',word_timestamps=True);print(json.dumps([[w.word.strip(),w.start,w.end] for s in seg for w in (s.words or [])]))", path], capture_output=True, text=True).stdout
        try: c[key] = json.loads(out.strip().splitlines()[-1])
        except Exception: c[key] = []
        json.dump(c, open(cache, "w"))
    ws = c[key]
    return [[round(t0 + a, 3), round(t0 + b, 3)] for _, a, b in ws] if len(ws) == len(text.split()) else None

lines = []; t = 0.0; parts = []
for j in range(5):
    n = j + 1
    x, s = sf.read(f"{VOICE}/{n}.wav"); assert s == sr; x = x if x.ndim == 1 else x[:, 0]
    d = len(x) / sr
    wf = whisper_words(f"{VOICE}/{n}.wav", ALL[j], t)
    print('line', n, 'whisper word stamps' if wf else 'sentence-silence estimate')
    lines.append(dict(n=n, text=ALL[j], start=round(t, 3), end=round(t + d, 3), words=wf or words_for(x, ALL[j], t)))
    parts.append((int(t * sr), x)); t += d + (GAPS[j] if j < 4 else 0)
D = round(lines[-1]["end"] + TAIL, 2)
nar = np.zeros(int((D + 0.3) * sr))
for i0, x in parts: nar[i0:i0 + len(x)] += x
os.makedirs(H + "/out", exist_ok=True)
sf.write(H + "/out/narration5.wav", nar[:int(D * sr)], sr, subtype="PCM_16")
json.dump(dict(lines=lines, D=D), open(H + "/cues5.json", "w"), indent=1)
S = lambda n: lines[n - 1]["start"]
E = lambda n: lines[n - 1]["end"]
W = lambda n, i: lines[n - 1]["words"][i][0]

# ---- scene boundaries (all derived from the voice)
B = dict(s1=0.0, s2=S(2) - .05, s3=W(2, 5) - .05, p1=S(3) - .05, p2=W(3, 2) - .05, p3=W(3, 5) - .05, p4=W(3, 6) - .05,
         s5=W(3, 10) - .05, s6=S(4) - .05, s7=S(5) - .05, end=E(5) + .25, loop=E(5) + .45)
T = dict(B)
T.update(dict(tapAllow=W(2, 3), flip=W(3, 12) - .12, slam1=W(1, 6)))
SFX = [  # (file under sfx/, time, gain_db re the -14 dBFS reference)
    ("impactpunch.ogg", 0.04, 0), ("subhit.ogg", 0.04, -3), ("whoosh_a.ogg", 0.0, -2),
    ("click_a.ogg", 0.55, -4), ("click_b.ogg", 0.85, -4), ("click_a.ogg", 1.15, -4),
    ("pop_a.ogg", W(1, 6) - .02, -1),
    ("whoosh_b.ogg", B["s2"] - .06, -2), ("select.ogg", T["tapAllow"], 0), ("pop_b.ogg", T["tapAllow"] + .06, -3),
    ("whoosh_c.ogg", B["s3"] - .05, -4), ("toggle.ogg", B["s3"] + .5, -6),
    ("whoosh_c.ogg", B["p1"] - .05, -5), ("tick.ogg", B["p1"] + .15, -2), ("whoosh_c.ogg", B["p2"] - .05, -6), ("tick.ogg", B["p2"] + .15, -2),
    ("whoosh_c.ogg", B["p3"] - .05, -6), ("tick.ogg", B["p3"] + .15, -2), ("whoosh_c.ogg", B["p4"] - .05, -6), ("tick.ogg", B["p4"] + .15, -2),
    ("whoosh_b.ogg", B["s5"] - .06, -3), ("toggle.ogg", T["flip"] + .22, 0), ("ding.ogg", T["flip"] + .32, -2), ("impactsoft.ogg", T["flip"] + .38, -5),
    ("whoosh_b.ogg", B["s6"] - .06, -3), ("pop_a.ogg", W(4, 2), -3),
    ("riser.ogg", B["s7"] - 2.2, -7), ("whoosh_b.ogg", B["s7"] - .06, -3),
    ("pop_b.ogg", W(5, 5) + .1, -3), ("pop_b.ogg", W(5, 5) + .38, -3), ("ding.ogg", E(5) - .1, -6), ("whoosh_c.ogg", B["loop"] - .1, -5),
]
json.dump([dict(f=f, t=round(tt, 3), g=g) for f, tt, g in SFX if tt < D], open(H + "/sfx5.json", "w"), indent=1)

