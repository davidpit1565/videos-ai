#!/usr/bin/env python3
"""pick_claude.py <w91d.wav> <w91d-cues.json> : for each take of 'Me with Claude, it listens.' find 'Claude' (faster-whisper word times) and
measure the pitch slope over its last 150 ms (semitones, f0 via librosa.pyin). Prints one row per take; lowest rise preferred."""
import sys, json, numpy as np, soundfile as sf, librosa
from faster_whisper import WhisperModel
wav, cj = sys.argv[1:3]; x, sr = sf.read(wav); x = x if x.ndim == 1 else x[:, 0]
cues = json.load(open(cj)); m = WhisperModel("small", device="cpu", compute_type="int8")
for c in cues:
    a = max(0, c["start"] - 0.08); b = min(len(x) / sr, c["end"] + 0.1); seg = x[int(a * sr):int(b * sr)]
    sf.write("/tmp/_pc.wav", seg, sr, subtype="PCM_16")
    ws, _ = m.transcribe("/tmp/_pc.wav", language="en", word_timestamps=True)
    words = [(w.word.strip(), w.start, w.end) for s in ws for w in (s.words or [])]
    cl = [w for w in words if "laud" in w[0].lower() or "claud" in w[0].lower()]
    if not cl: print(c["n"], "no Claude found", words); continue
    w_, s_, e_ = cl[0]; t1 = e_; t0 = max(s_, e_ - 0.15)
    y = seg.astype(np.float32); f0, vf, _ = librosa.pyin(y, fmin=70, fmax=400, sr=sr, frame_length=2048, hop_length=256)
    ts = librosa.times_like(f0, sr=sr, hop_length=256); sel = (ts >= t0) & (ts <= t1) & vf & ~np.isnan(f0)
    if sel.sum() < 3: print(c["n"], "Claude %.2f-%.2f: too few voiced frames (%d)" % (s_, e_, sel.sum()), words); continue
    tt = ts[sel]; ff = 12 * np.log2(f0[sel]); slope = np.polyfit(tt, ff, 1)[0] * (t1 - t0)   # semitone change over the last 150 ms
    pre = (ts >= s_) & (ts < t0) & vf & ~np.isnan(f0); base = np.median(12 * np.log2(f0[pre])) if pre.sum() else float("nan")
    print("take %d  'Claude' %.2f-%.2f  heard '%s'  last150ms slope %+.2f st  (end vs earlier part of word %+.2f st)  dur %.2f" % (c["n"], s_, e_, w_, slope, np.median(ff) - base, c["end"] - c["start"]), "| words:", [w[0] for w in words])
