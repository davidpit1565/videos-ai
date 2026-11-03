#!/usr/bin/env python3
"""Replace ONLY the word "Anthropic's" in the version-1 take of line 9 (voice/l9-v1.wav, already tightened) with the same word cut from a new take.
Edges of both words: forced alignment + nearest energy valleys (rword.py). The new word is sped up by 1.06 (the tighten step the V1 line already had), level-matched to the V1 word (max +-3 dB), joined with an 8 ms equal-power crossfade at both low-energy edges.
usage: splice.py <new_take.wav> <out.wav>   -> prints durations, the joins' levels and a click check"""
import sys, subprocess, numpy as np, soundfile as sf, librosa
sys.path.insert(0, ".")
import rword
SR48 = 48000; XF = int(0.008 * SR48)

def load48(p):
    x, sr = sf.read(p); x = x if x.ndim == 1 else x[:, 0]
    return x if sr == SR48 else librosa.resample(x, orig_sr=sr, target_sr=SR48)

def word_edges(x48):
    y16 = librosa.resample(x48, orig_sr=SR48, target_sr=16000); y16 = y16 / (np.abs(y16).max() + 1e-9)
    a, b, db, hop = rword.edges(y16)
    return a, b

def atempo(x, f):
    p = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR48), "-ac", "1", "-i", "-", "-filter:a", f"atempo={f}", "-f", "f32le", "-"],
                       input=x.astype(np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, dtype=np.float32).astype(np.float64)

def xfade(a, b, n):
    """append b after a, overlapping n samples with equal-power fades"""
    t = np.linspace(0, np.pi / 2, n)
    mid = a[-n:] * np.cos(t) + b[:n] * np.sin(t)
    return np.concatenate([a[:-n], mid, b[n:]])

def main(newp, outp, v1p="voice/l9-v1.wav"):
    y1 = load48(v1p); a1, b1 = word_edges(y1)
    t = load48(newp); a2, b2 = word_edges(t)
    w1 = y1[int(a1 * SR48):int(b1 * SR48)]; w2 = t[int(a2 * SR48):int(b2 * SR48)]
    w2 = atempo(w2, 1.06)
    g = np.sqrt(np.mean(w1 ** 2)) / (np.sqrt(np.mean(w2 ** 2)) + 1e-9); gdb = float(np.clip(20 * np.log10(g), -3, 3)); w2 = w2 * 10 ** (gdb / 20)
    head = y1[:int(a1 * SR48) + XF]; tail = y1[int(b1 * SR48) - XF:]
    out = xfade(xfade(head, w2, XF), tail, XF)
    sf.write(outp, out, SR48, subtype="PCM_16")
    d = np.abs(np.diff(out)); pos = [int(a1 * SR48), int(a1 * SR48) + len(w2)]
    jump = [float(d[max(0, p - XF):p + XF].max()) for p in pos]
    print(f"v1 word {b1-a1:.3f}s new word {len(w2)/SR48:.3f}s (gain {gdb:+.1f} dB) line {len(y1)/SR48:.3f}s -> {len(out)/SR48:.3f}s ({(len(out)-len(y1))/SR48*1000:+.0f} ms); max sample step near joins {jump[0]:.3f} / {jump[1]:.3f} (speech peaks {np.abs(out).max():.2f})")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
