#!/usr/bin/env python3
"""Line-9 variants, round 2 (boundaries read from the energy envelopes of the version-1 take; CTC word stamps were NOT reliable on this take).
V1 take = voice/l9-v1.wav (48 kHz).  Hand-read landmarks (seconds):  'to' = T closure 0.525-0.575, burst 0.578, weak vowel to ~0.598, then the stressed 'A' of Anthropic's starts at ~0.605;
the /s/ of Anthropic's is 1.062-1.128 (HF-rich), silence 1.13-1.17, 'own' 1.18-1.28, 'report' from ~1.285 (r), 'are' at 1.59.
  v3b: 'The links to the report are in the caption.'   head up to the end of 'to' (0.598) | 'the' from line 4 ('the default', 1.575-1.642) | V1 from 'report' (1.285)
  v5b: 'The links to the Anthropic report are in the caption.'  head | 'the' | 'Anthropic' from line 2 (0.040-0.616) | V1 from 'report'
  v6 : 'The links to Anthropic's own report are in the caption.'  head | 'Anthropic' from line 2 | V1 from its own /s/ (1.060, so the possessive 's, the gap and 'own report...' are V1's)
  v4b: same sentence, only the word replaced by the word of <take.wav> (T closure of the take -> after its /s/), tail = V1 from 1.15
Each donor segment: pitch shift (rubberband, formants kept) and gain so the f0 step across the seam is small and the level matches the neighbours, 8 ms equal-power crossfades.
usage: splice9b.py <v3b|v5b|v6|v4b> <out.wav> [take.wav for v4b]   -> prints one RESULT json line with the fluency numbers"""
import sys, json, subprocess, numpy as np, soundfile as sf, librosa
sys.path.insert(0, ".")
import rword, thword
SR48 = 48000; SR = 16000; XF = int(0.008 * SR48); I = lambda s: int(round(s * SR48)); H = XF // 2
VAR, OUT = sys.argv[1], sys.argv[2]; TAKE = sys.argv[3] if len(sys.argv) > 3 else None
import os
MAXSH = float(os.environ.get('MAXSH', '5'))
SYL = dict(v1=14, v3b=11, v5b=14, v6=14, v4b=14)
TO_CUT, REPORT, S_START, SIL_CUT = 0.598, 1.285, 1.060, 1.150
def load48(p):
    x, sr = sf.read(p); x = x if x.ndim == 1 else x[:, 0]
    return x if sr == SR48 else librosa.resample(x, orig_sr=sr, target_sr=SR48)
def to16(y): z = librosa.resample(y, orig_sr=SR48, target_sr=SR); return z / (np.abs(z).max() + 1e-9)
def rms_db(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
def p90(x):
    z = librosa.resample(x, orig_sr=SR48, target_sr=SR); z = z if len(z) > 400 else np.pad(z, (0, 400)); e, _ = rword.env_db(z); return float(np.percentile(e, 90))
def seg(x, a, b=None):          # [a, b] seconds with H samples of pad either side (the crossfade overlaps them)
    s = max(0, I(a) - H); e = len(x) if b is None else min(len(x), I(b) + H); return x[s:e]
def xfade(a, b, n=XF):
    t = np.linspace(0, np.pi / 2, n); return np.concatenate([a[:-n], a[-n:] * np.cos(t) + b[:n] * np.sin(t), b[n:]])
def atempo(x, f):
    p = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR48), "-ac", "1", "-i", "-", "-filter:a", f"atempo={f}", "-f", "f32le", "-"], input=x.astype(np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, dtype=np.float32).astype(np.float64)
def shift(x, st):
    if abs(st) < 0.05: return x
    r = 2 ** (float(st) / 12)
    pr = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR48), "-ac", "1", "-i", "-", "-filter:a", f"rubberband=pitch={r}:formant=preserved:pitchq=quality", "-f", "f32le", "-"],
                        input=np.concatenate([np.zeros(2400), x, np.zeros(2400)]).astype(np.float32).tobytes(), capture_output=True, check=True)
    z = np.frombuffer(pr.stdout, dtype=np.float32).astype(np.float64)
    return z[2400:2400 + len(x)] if len(z) >= 2400 + len(x) else np.concatenate([z[2400:], np.zeros(len(x) - len(z) + 2400)])
def hf_end(y16, a, b):           # end of the /s/ fricative: last frame whose 3-8 kHz level is within 12 dB of the window's max, +12 ms
    hf, hop = thword.band_env(y16, 3000, 8000); i0, i1 = int(a / hop), min(len(hf), int(b / hop)); w = hf[i0:i1]; ok = np.where(w >= w.max() - 12)[0]
    return (i0 + ok[-1]) * hop + 0.012

y = load48("voice/l9-v1.wav"); y16 = to16(y)
d2 = load48("voice/final/2.wav"); d3 = load48("voice/final/3.wav"); d4 = load48("voice/final/4.wav")
parts = []      # (name, array, adjustable)
if VAR == "v4b":
    t = load48(TAKE); t16 = to16(t); e = rword.edges(t16); a2 = e[0]; ws, we = rword.locate(t16)
    b2 = hf_end(t16, we - 0.04, we + 0.25)
    parts = [("head", seg(y, 0, 0.560), False), ("Anthropic's(new)", atempo(seg(t, a2, b2), 1.06), True), ("tail", seg(y, SIL_CUT), False)]
    info = dict(new_word=[round(a2, 3), round(b2, 3)])
else:
    head = seg(y, 0, 0.550)                                   # 'The links' + the silent T closure; V1's own 'to' is only ~20 ms of vowel and cannot stand alone
    to = seg(d3, 1.010, 1.080)                                # a natural reduced 'to' (soft t burst + vowel, ~65 ms) from line 3 ('own up to real'); line 4's 'to' is heavily aspirated and reads as 'sigh'
    import os
    THE = {"l4": seg(d4, 1.575, 1.642), "l4b": seg(d4, 1.575, 1.660), "v1first": seg(y, 0.225, 0.292), "v1cap": seg(y, 2.095, 2.150)}
    the = THE[os.environ.get("THE_SRC", "v1cap")]; anth = seg(d2, 0.040, 0.616)
    if VAR == "v3b": parts = [("head", head, False), ("to(line3)", to, True), ("the(line4)", the, True), ("tail", seg(y, REPORT), False)]
    if VAR == "v5b": parts = [("head", head, False), ("to(line3)", to, True), ("the(line4)", the, True), ("Anthropic(line2)", anth, True), ("tail", seg(y, REPORT), False)]
    if VAR == "v6": parts = [("head", head, False), ("to(line3)", to, True), ("Anthropic(line2)", anth, True), ("tail(V1 from its /s/)", seg(y, S_START), False)]
    info = {}
adj = [i for i, p in enumerate(parts) if p[2]]
lvl = lambda a, b: p90(y[I(a):I(b)])
neighbour = np.mean([lvl(0.28, 0.52), lvl(1.28, 1.50)])            # 'links' and 'report'
targets = {"to(line3)": neighbour - 2.0, "the(line4)": neighbour - 4.0, "Anthropic(line2)": lvl(1.28, 1.50), "Anthropic's(new)": lvl(0.605, 1.06)}
def build(shifts, gains):
    out = parts[0][1]; joins = []
    for k in range(1, len(parts)):
        nm, x, ad = parts[k]
        if ad: j = adj.index(k); x = shift(x, shifts[j]) * 10 ** (gains[j] / 20)
        joins.append((parts[k - 1][0] + "|" + nm, (len(out) - XF / 2) / SR48)); out = xfade(out, x)
    return out, joins
def f0_of(o):
    f0, _, _ = librosa.pyin(to16(o) * 1.0, fmin=70, fmax=400, sr=SR, frame_length=1024, hop_length=160); return f0, np.arange(len(f0)) * 160 / SR
def steps(o, joins):
    f0, t = f0_of(o); res = []
    for _, p in joins:
        b = a = np.array([])
        for w in (0.07, 0.12, 0.2):
            b = f0[(t > p - w) & (t < p)]; a = f0[(t > p) & (t < p + w)]; b = b[~np.isnan(b)]; a = a[~np.isnan(a)]
            if len(a) >= 2 and len(b) >= 2: break
        res.append(round(12 * np.log2(np.median(a[:6]) / np.median(b[-6:])), 1) if len(a) >= 2 and len(b) >= 2 else None)
    return res
shifts = [0.0] * len(adj); gains = [float(np.clip(targets[parts[k][0]] - p90(parts[k][1]), -9, 9)) for k in adj]
from scipy.optimize import lsq_linear
lims = [float(os.environ.get("LIM_FUNC", "2.5")) if parts[k][0].startswith(("to(", "the(")) else 3.5 for k in adj]
for rnd in range(3 if adj else 0):          # f0 step at join j (between parts j and j+1) = step0_j + shift_{j+1} - shift_j  -> bounded least squares, re-measured each round
    o, joins = build(shifts, gains); st = steps(o, joins)
    if all(x is None or abs(x) <= 1.0 for x in st): break
    rows, rhs = [], []
    for jn, x in enumerate(st):
        if x is None: continue
        r = np.zeros(len(adj))
        if (jn + 1) in adj: r[adj.index(jn + 1)] += 1
        if jn in adj: r[adj.index(jn)] -= 1
        rows.append(r); rhs.append(-x)
    sol = lsq_linear(np.array(rows), np.array(rhs), bounds=([-l - sh for l, sh in zip(lims, shifts)], [l - sh for l, sh in zip(lims, shifts)])).x
    shifts = [float(sh + d) for sh, d in zip(shifts, sol)]
for j, k in enumerate(adj): gains[j] = float(np.clip(targets[parts[k][0]] - p90(shift(parts[k][1], shifts[j])), -9, 9))
o, joins = build(shifts, gains)
sf.write(OUT, o, SR48, subtype="PCM_16")

# ---------------- verification ----------------
o16 = to16(o); odb, ohop = rword.env_db(o16); y_db, yhop = rword.env_db(y16)
speech = lambda d: np.median(d[d > np.percentile(d, 40)])
dip = [round(float(speech(odb) - odb[int((p - 0.03) / ohop):int((p + 0.03) / ohop) + 1].min()), 1) for _, p in joins]
natural_dip = round(float(speech(y_db) - y_db[int(1.14 / yhop):int(1.17 / yhop)].min()), 1)     # the real silence between words in V1 (the /s/ -> 'own' gap) is deeper than most
dd = np.abs(np.diff(o)); norm = float(np.percentile(dd, 99.9))
click = [round(float(dd[max(0, I(p) - XF):I(p) + XF].max() / norm), 2) for _, p in joins]
seg_levels = [round(p90(shift(parts[k][1], shifts[j]) * 10 ** (gains[j] / 20)) - targets[parts[k][0]], 1) for j, k in enumerate(adj)]
from faster_whisper import WhisperModel
W = WhisperModel("base.en", device="cpu", compute_type="int8", cpu_threads=2)
pad = np.concatenate([np.zeros(8000), o16, np.zeros(8000)]).astype(np.float32); sg, _ = W.transcribe(pad, language="en", beam_size=5, word_timestamps=True)
words = [(w.word.strip(), round(w.start - 0.5, 2), round(w.end - 0.5, 2)) for s in sg for w in s.words]
to_hit = [w for w in words if w[0].lower().strip(".,'") in ("to", "too", "two")]
import thctc, torch
def th_margin(ctx_b, word, ctx_a, alts):
    with torch.no_grad(): em, _ = rword._M(torch.tensor(o16, dtype=torch.float32)[None])
    base = thctc.nll(em, ctx_b + word + ctx_a); al = {a: thctc.nll(em, ctx_b + a + ctx_a) for a in alts}; b = min(al, key=al.get); return round(al[b] - base, 2), b
th = None
if VAR in ("v6", "v4b"): th = th_margin("THE|LINKS|TO|", "ANTHROPIC'S", "|OWN|REPORT|ARE|IN|THE|CAPTION", thctc.ALT)
if VAR == "v5b": th = th_margin("THE|LINKS|TO|THE|", "ANTHROPIC", "|REPORT|ARE|IN|THE|CAPTION", [a.replace("'S", "").rstrip("S") if "'S" in a else a for a in thctc.ALT])
res = dict(variant=VAR, th_margin=th, dur=round(len(o) / SR48, 3), v1_dur=round(len(y) / SR48, 3), parts=[p[0] for p in parts], seams=[j[0] for j in joins], seam_t=[round(j[1], 3) for j in joins],
           shifts_st=[round(s, 2) for s in shifts], gains_db=[round(g, 1) for g in gains], seg_level_vs_target_db=seg_levels,
           f0_step_st=steps(o, joins), dip_db=dip, v1_gap_dip_db=natural_dip, click_ratio=click,
           syl_rate=round(SYL[VAR] / (len(o) / SR48), 2), v1_syl_rate=round(SYL["v1"] / (len(y) / SR48), 2),
           heard=" ".join(w[0] for w in words), to_heard=bool(to_hit), **info)
print("RESULT " + json.dumps(res))
