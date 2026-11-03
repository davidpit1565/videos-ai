#!/usr/bin/env python3
"""Line-9 variants built from the version-1 take (voice/l9-v1.wav) with fluency checks.
  v3: 'The links to the report are in the caption.'            (cut "Anthropic's own", insert 'the' from "in the caption")
  v5: 'The links to the Anthropic report are in the caption.'   (as v3 + donor word 'Anthropic' from voice/final/2.wav)
  v4: 'The links to Anthropic's own report are in the caption.' (only the word "Anthropic's" replaced by the word from <take.wav>)
usage: splice9.py <v3|v4|v5> <out.wav> [take.wav for v4]
Each inserted segment gets a pitch shift (librosa, a few rounds) so the f0 step at both joins is small, a gain match to its neighbours,
8 ms equal-power crossfades at energy valleys. Then it verifies: (a) pause/dip at each splice vs the take's own word gaps, (b) f0 step in semitones,
(c) loudness step in dB, (d) click (max sample step vs the take's normal), (e) syllable rate vs V1. Prints one JSON line with the numbers."""
import sys, json, numpy as np, soundfile as sf, librosa, torch, torchaudio
sys.path.insert(0, ".")
import rword
SR48 = 48000; SR = 16000; XF = int(0.008 * SR48); I = lambda s: int(s * SR48)
VAR, OUT = sys.argv[1], sys.argv[2]; TAKE = sys.argv[3] if len(sys.argv) > 3 else None
SYL = dict(v1=14, v3=11, v4=14, v5=14)

def load48(p):
    x, sr = sf.read(p); x = x if x.ndim == 1 else x[:, 0]
    return x if sr == SR48 else librosa.resample(x, orig_sr=sr, target_sr=SR48)
def to16(y): z = librosa.resample(y, orig_sr=SR48, target_sr=SR); return z / (np.abs(z).max() + 1e-9)
def spans(y16, txt):
    with torch.no_grad(): em, _ = rword._M(torch.tensor(y16, dtype=torch.float32)[None])
    em = torch.log_softmax(em, -1); d = {c: i for i, c in enumerate(rword._LAB)}
    al, sc = torchaudio.functional.forced_align(em, torch.tensor([[d[c] for c in txt]]), blank=0)
    sp = torchaudio.functional.merge_tokens(al[0], sc[0]); ratio = len(y16) / em.shape[1] / SR
    out = []; i = 0
    for w in txt.split("|"):
        s = sp[i:i + len(w)]; i += len(w); out.append((w, s[0].start * ratio, s[-1].end * ratio))
    return out
def xfade(a, b, n):
    t = np.linspace(0, np.pi / 2, n); return np.concatenate([a[:-n], a[-n:] * np.cos(t) + b[:n] * np.sin(t), b[n:]])
def atempo(x, f):
    import subprocess
    p = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR48), "-ac", "1", "-i", "-", "-filter:a", f"atempo={f}", "-f", "f32le", "-"], input=x.astype(np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, dtype=np.float32).astype(np.float64)
def p90(x):
    z = librosa.resample(x, orig_sr=SR48, target_sr=SR); e, _ = rword.env_db(z if len(z) > 400 else np.pad(z, (0, 400))); return float(np.percentile(e, 90))
def rms_db(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
def shift(x, st):
    if abs(st) < 0.05: return x
    import subprocess
    r = 2 ** (float(st) / 12)
    pr = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR48), "-ac", "1", "-i", "-", "-filter:a", f"rubberband=pitch={r}:formant=preserved:pitchq=quality", "-f", "f32le", "-"],
                        input=np.concatenate([np.zeros(2400), x, np.zeros(2400)]).astype(np.float32).tobytes(), capture_output=True, check=True)
    z = np.frombuffer(pr.stdout, dtype=np.float32).astype(np.float64)
    z = z[2400:2400 + len(x)] if len(z) >= 2400 + len(x) else np.concatenate([z[2400:], np.zeros(len(x) - len(z) + 2400)])
    return z

y = load48("voice/l9-v1.wav"); y16 = to16(y); db, hop = rword.env_db(y16); sp = spans(y16, rword.TXT)
g1 = lambda n, k=0: [s for s in sp if s[0] == n][k]
anth, rep, the2, cap = g1("ANTHROPIC'S"), g1("REPORT"), g1("THE", 1), g1("CAPTION")
cut_a = rword.valley(db, hop, anth[1] - 0.09, anth[1] + 0.02); cut_b = rword.valley(db, hop, rep[1] - 0.06, rep[1] + 0.03)
the_a = rword.valley(db, hop, the2[1] - 0.05, the2[1] + 0.02); the_b = rword.valley(db, hop, cap[1] - 0.06, cap[1] + 0.02)
anth_b = rword.valley(db, hop, anth[2] - 0.04, anth[2] + 0.07)
head = y[:I(cut_a) + XF]
if VAR == "v4": tail = y[I(anth_b) - XF:]
else: tail = y[I(cut_b) - XF:]
to_s = g1("TO"); wref = [y[I(to_s[1]):I(to_s[2])], y[I(rep[1]):I(rep[2])]]
ref_db = float(np.mean([20 * np.log10(np.sqrt(np.mean(w ** 2)) + 1e-9) for w in wref])); ref = 10 ** (ref_db / 20)
segs = []                         # inserted segments (raw)
if VAR in ("v3", "v5"): segs.append(("the", y[I(the_a):I(the_b)]))
if VAR == "v5":
    d = load48("voice/final/2.wav"); d16 = to16(d); ddb, dhop = rword.env_db(d16); dsp = spans(d16, "ANTHROPIC|SAYS|IT|NEVER|DOES|THAT")
    d_a = rword.valley(ddb, dhop, max(0, dsp[0][1] - 0.05), dsp[0][1] + 0.03); d_b = rword.valley(ddb, dhop, dsp[0][2] - 0.04, dsp[1][1] + 0.04)
    segs.append(("Anthropic(line2)", d[I(d_a):I(d_b)]))
if VAR == "v4":
    t = load48(TAKE); a2, b2, _, _ = rword.edges(to16(t)); w = atempo(t[I(a2):I(b2)], 1.06); segs.append(("Anthropic's(new)", w))
ref_dur = None

def build(shifts, gains):
    parts = [head]; joins = []; pos = len(head) - XF
    out = head
    for (nm, x), s, g in zip(segs, shifts, gains):
        xs = shift(x, s) * 10 ** (g / 20)
        joins.append((nm + " <", (len(out) - XF) / SR48)); out = xfade(out, xs, XF)
    joins.append(("tail <", (len(out) - XF) / SR48)); out = xfade(out, tail, XF)
    return out, joins

def f0_of(o):
    o16 = librosa.resample(o, orig_sr=SR48, target_sr=SR); f0, _, _ = librosa.pyin(o16, fmin=70, fmax=400, sr=SR, frame_length=1024, hop_length=160)
    return f0, np.arange(len(f0)) * 160 / SR
def steps(o, joins, w=0.07):
    f0, t = f0_of(o); res = []
    for _, p in joins:
        b = f0[(t > p - w) & (t < p)]; a = f0[(t > p) & (t < p + w)]; b = b[~np.isnan(b)]; a = a[~np.isnan(a)]
        res.append(12 * np.log2(np.median(a) / np.median(b)) if len(a) and len(b) else 0.0)
    return res
def lsteps(o, joins, w=0.06):
    return [rms_db(o[I(p):I(p + w)]) - rms_db(o[I(p - w):I(p)]) for _, p in joins]

n = len(segs); shifts = [0.0] * n; gains = [0.0] * n
lvl = lambda a, b: p90(y[I(a):I(b)])
rel_the = lvl(the_a, the_b) - np.mean([lvl(g1("IN")[1], g1("IN")[2]), lvl(cap[1], cap[2])])   # how far below its neighbours the natural 'the' sits
ref_db = float(np.mean([lvl(to_s[1], to_s[2]), lvl(rep[1], rep[2])]))
targets = []
for nm, x in segs:
    targets.append(ref_db + 0.5 * rel_the if nm == "the" else lvl(rep[1], rep[2]))
for g_i, (nm, x) in enumerate(segs): gains[g_i] = float(np.clip(targets[g_i] - p90(x), -8, 8))
for rnd in range(5 if n else 0):
    o, joins = build(shifts, gains); st = steps(o, joins)
    if max(abs(s) for s in st) <= 1.2: break
    for k in range(n):               # segment k sits between join k (before) and join k+1 (after)
        shifts[k] += 0.7 * (st[k + 1] - st[k]) / 2
    shifts = [float(np.clip(s, -5, 5)) for s in shifts]
for k, (nm, x) in enumerate(segs): gains[k] = float(np.clip(targets[k] - p90(shift(x, shifts[k])), -8, 8))
o, joins = build(shifts, gains) if n else (y, [])
sf.write(OUT, o, SR48, subtype="PCM_16")

# ---- verification ----
def gaps(db_, hop_, p, w=0.03, drop=22):
    med = np.median(db_[db_ > np.percentile(db_, 40)]); lo = db_ < med - drop; i = int(p / hop_)
    k = i;
    while k > 0 and lo[k]: k -= 1
    j = i
    while j < len(lo) - 1 and lo[j]: j += 1
    return (j - k) * hop_ * (1 if lo[i] else 0)
oo16 = to16(o); odb, ohop = rword.env_db(oo16)
v1gaps = [round(float(gaps(db, hop, (sp[i][2] + sp[i + 1][1]) / 2)), 3) for i in range(len(sp) - 1)]
dip = []
for _, p in joins:
    seg = odb[int((p - 0.03) / ohop):int((p + 0.03) / ohop) + 1]; med = np.median(odb[odb > np.percentile(odb, 40)]); dip.append(round(float(med - seg.min()), 1))
v1dip = []
for i in range(len(sp) - 1):
    p = (sp[i][2] + sp[i + 1][1]) / 2; seg = db[int((p - 0.03) / hop):int((p + 0.03) / hop) + 1]; v1dip.append(float(np.median(db[db > np.percentile(db, 40)]) - seg.min()))
def lstep(sig, p, w=0.04, g=0.016): return rms_db(sig[I(p + g):I(p + g + w)]) - rms_db(sig[I(p - g - w):I(p - g)])
loud_here = [round(lstep(o, p), 1) for _, p in joins]
loud_v1 = [round(abs(lstep(y, (sp[i][2] + sp[i + 1][1]) / 2)), 1) for i in range(len(sp) - 1)]
dd = np.abs(np.diff(o)); norm = float(np.percentile(dd, 99.9))
click = [round(float(dd[max(0, I(p) - XF):I(p) + XF].max() / norm), 2) for _, p in joins]
res = dict(variant=VAR, dur=round(len(o) / SR48, 3), v1_dur=round(len(y) / SR48, 3), joins=[j[0] for j in joins], join_t=[round(j[1], 3) for j in joins],
           shifts_st=[round(s, 2) for s in shifts], gains_db=[round(g, 1) for g in gains],
           f0_step_st=[round(s, 1) for s in steps(o, joins)] if joins else [], seg_vs_target_db=[round(p90(shift(x, sh) * 10 ** (g / 20)) - tg, 1) for (nm, x), sh, g, tg in zip(segs, shifts, gains, targets)],
           loud_step_at_join_db=loud_here, v1_word_boundary_loud_step_median_db=round(float(np.median(loud_v1)), 1), v1_word_boundary_loud_step_max_db=max(loud_v1), dip_db=dip, v1_max_word_dip_db=round(max(v1dip), 1), v1_longest_gap_s=max(v1gaps), click_ratio=click,
           syl_rate=round(SYL[VAR] / (len(o) / SR48), 2), v1_syl_rate=round(SYL["v1"] / (len(y) / SR48), 2))
print("RESULT " + json.dumps(res))
