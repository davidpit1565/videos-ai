#!/usr/bin/env python3
"""Does the word "Anthropic('s)" in a take have a real, audible TH, and three vowel nuclei?  (PROXIES, not hearing.)
Uses the CTC forced alignment of 'THE LINKS TO ANTHROPIC'S OWN REPORT ARE IN THE CAPTION' (rword) for the character positions of T,H (the TH) between N and R,
then measures inside that region, relative to the word's own stressed vowel (same idea as audio/burst.py, which is calibrated for 'three' only):
  fric_db   max 3-8 kHz level in the TH region minus the same band at the word's loudest frame   (frication sits close to the vowel, a missing TH sits far below)
  fric_ms   how long the 3-8 kHz band stays within 20 dB of that vowel level in the TH region, unvoiced
  burst_db  largest one-frame (2.5 ms) rise of the 3-8 kHz level in the region (a stop releases one sharp burst; frication rises gently)
  nuclei    count of distinct voiced low-band (<1.5 kHz) bumps in the word (AN, THRO, PIC: want 3)
  heard     what faster-whisper (base.en) writes for the clip of the word with 0.15 s of context on each side (a listen-proxy only)
Reference rows used to read the numbers: V1 word (David: only the R bothered him), line 2's word (accepted), seed 8771 (David heard 'Antopik/Antfik': a known BAD TH).
usage: thword.py <wav|wav:start:end ...>   (wav = a line-9 take, or the line-2 take with a:b = its word window)"""
import sys, json, numpy as np, librosa, torch, torchaudio
sys.path.insert(0, ".")
import rword
SR = 16000

def char_spans(y, txt, word):
    with torch.no_grad(): em, _ = rword._M(torch.tensor(y, dtype=torch.float32)[None])
    em = torch.log_softmax(em, -1); d = {c: i for i, c in enumerate(rword._LAB)}
    al, sc = torchaudio.functional.forced_align(em, torch.tensor([[d[c] for c in txt]]), blank=0)
    sp = torchaudio.functional.merge_tokens(al[0], sc[0]); ratio = len(y) / em.shape[1] / SR
    i = 0
    for w in txt.split("|"):
        s = sp[i:i + len(w)]; i += len(w)
        if w == word: return [(c, x.start * ratio, x.end * ratio) for c, x in zip(w, s)]
    return None

def band_env(y, lo, hi, hop=0.0025, win=0.010):
    S = np.abs(librosa.stft(y, n_fft=256, hop_length=int(hop * SR), win_length=int(win * SR), center=False)) ** 2
    f = librosa.fft_frequencies(sr=SR, n_fft=256); m = (f >= lo) & (f < hi)
    return 10 * np.log10(S[m].sum(0) + 1e-12), hop

def measure(y, txt, word, off=0.0):
    cs = char_spans(y, txt, word)
    if cs is None: return None
    ch = {}
    for k, (c, a, b) in enumerate(cs): ch.setdefault(c, []).append((k, a, b))
    hf, hop = band_env(y, 3000, 8000); lf, _ = band_env(y, 80, 1500)
    w0, w1 = cs[0][1], cs[-1][2]
    i0, i1 = int(w0 / hop), min(len(hf), int(w1 / hop) + 1)
    vow = i0 + int(np.argmax(lf[i0:i1])); vhf = hf[vow - 2:vow + 3].max()
    # TH region: from the T token to the R token (between N and R)
    ta = [x for x in cs if x[0] == "T"][0]; ra = [x for x in cs if x[0] == "R"][0]
    r0, r1 = int((ta[1] - 0.02) / hop), int(ra[1] / hop) + 1
    reg = hf[r0:r1]; lreg = lf[r0:r1]
    fric_db = float(reg.max() - vhf)
    ok = (reg > vhf - 20) & (lreg < lf[vow] - 12)       # noisy and not voiced-loud
    fric_ms = float(ok.sum() * hop * 1000)
    burst_db = float(np.max(np.diff(reg))) if len(reg) > 1 else 0.0
    # vowel nuclei: voiced low-band bumps with >= 4 dB prominence inside the word
    seg = lf[i0:i1]
    from scipy.signal import find_peaks
    pk, pr = find_peaks(seg, prominence=4.0, distance=int(0.06 / hop))
    return dict(word_dur=round(w1 - w0, 3), th_region_ms=round((ra[1] - ta[1]) * 1000), fric_db=round(fric_db, 1), fric_ms=round(fric_ms), burst_db=round(burst_db, 1), nuclei=len(pk))

_W = None
def heard(y, w0, w1):
    global _W
    if _W is None:
        from faster_whisper import WhisperModel; _W = WhisperModel("base.en", device="cpu", compute_type="int8", cpu_threads=2)
    z = y[int(max(0, w0 - 0.15) * SR):int((w1 + 0.15) * SR)]
    segs, _ = _W.transcribe(z.astype(np.float32), language="en", beam_size=5)
    return " ".join(s.text.strip() for s in segs)

if __name__ == "__main__":
    TXT = rword.TXT; out = {}
    for arg in sys.argv[1:]:
        p, *ab = arg.split(":")
        y, _ = librosa.load(p, sr=SR); y = y / (np.abs(y).max() + 1e-9)
        if ab:                                  # line-2 take: cut the word window (alignment text differs)
            a, b = float(ab[0]), float(ab[1]); y2 = y[int(a * SR):int(b * SR)]
            y = np.concatenate([np.zeros(int(0.3 * SR)), y2, np.zeros(int(0.3 * SR))]); txt = "ANTHROPIC"; word = "ANTHROPIC"
            m = measure(y, txt, word); hr = heard(y, 0.3, 0.3 + len(y2) / SR)
        else:
            m = measure(y, TXT, "ANTHROPIC'S"); e = rword.edges(y); hr = heard(y, e[0], e[1]) if e else ""
        m["heard"] = hr; out[arg.split("/")[-1]] = m; print(arg.split("/")[-1], m, flush=True)
    json.dump(out, open("thword.json", "w"), indent=1)
