#!/usr/bin/env python3
"""Build a narration track from a video's cue list using Piper neural TTS.

Each caption cue becomes one spoken line, placed at its cue start time. Lines that
run longer than their slot are tightened via Piper's length-scale rather than
time-stretched afterwards, which keeps the pitch natural.

  python3 build_vo.py <html-file> <out.wav>
"""
import json, re, subprocess, sys, wave, tempfile, os
import numpy as np

MODEL = "/tmp/voices/en_US-lessac-medium.onnx"
SR    = 22050
MIN_LS, MAX_LS = 0.80, 1.10     # below 0.8 it starts to sound clipped

def cues_from(path):
    src = open(path, encoding="utf-8").read()
    m = re.search(r'var CUES=(\[.*?\]);', src, re.S)
    if not m:
        raise SystemExit("no CUES array found in " + path)
    raw = json.loads(m.group(1))
    out = []
    for c in raw:
        txt = re.sub(r'<[^>]+>', '', c[2]).replace('\n', ' ').strip()
        if txt:
            out.append((float(c[0]), float(c[1]), txt))
    return out

def merge_sentences(cues):
    """Caption cues are split for reading, not for speaking. Speak whole sentences
    instead — a fragment read in isolation gets the wrong intonation."""
    out, buf, start = [], [], None
    for s, e, t in cues:
        if start is None:
            start = s
        buf.append(t)
        if t.rstrip().endswith(('.', '!', '?', '…', ':', '"')):
            out.append((start, e, ' '.join(buf)))
            buf, start = [], None
    if buf:
        out.append((start, cues[-1][1], ' '.join(buf)))
    return out

def speak(text, ls, path):
    subprocess.run([
        "piper", "-m", MODEL, "-f", path,
        "--length-scale", str(ls), "--sentence-silence", "0.15",
    ], input=text, text=True, check=True,
       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with wave.open(path) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)

def main(html, out):
    cues = merge_sentences(cues_from(html))
    total = max(c[1] for c in cues) + 1.5
    track = np.zeros(int(total * SR), dtype=np.float32)
    tmp = tempfile.mkdtemp()
    over = []

    for i, (start, end, text) in enumerate(cues):
        wav = os.path.join(tmp, "l%03d.wav" % i)
        a = speak(text, 1.0, wav)
        slot = max(0.6, end - start)
        natural = len(a) / SR
        if natural > slot:
            ls = max(MIN_LS, slot / natural)
            a = speak(text, round(ls, 3), wav)
            if len(a) / SR > slot + 0.25:
                over.append((i, text[:48], round(len(a)/SR, 2), round(slot, 2)))
        seg = a.astype(np.float32) / 32768.0
        pos = int(start * SR)
        n = min(len(seg), len(track) - pos)
        track[pos:pos+n] += seg[:n]          # cues never overlap, so a sum is safe

    peak = np.abs(track).max() or 1.0
    track = np.clip(track / peak * 0.89, -1, 1)
    with wave.open(out, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((track * 32767).astype(np.int16).tobytes())

    print("wrote %s  %.1fs  %d lines" % (out, len(track)/SR, len(cues)))
    if over:
        print("lines still longer than their slot (tighten the copy or widen the cue):")
        for i, t, got, slot in over:
            print("  cue %d  %.2fs in a %.2fs slot  %s…" % (i, got, slot, t))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
