#!/usr/bin/env python3
"""Stress edit for 'Anthropic(s)': only the two VOWEL stretches are processed, the TH fricative gap, the /p/ closure, PIC and the /s/ stay byte-identical (the first version processed the segments with the TH noise inside and lost the TH: Whisper wrote 'The traffic').
  AN_v   = from the word's A onset to the start of the quiet TH gap
  THRO_v = from the end of the TH gap to the first dip after THRO's peak (the /p/ closure)
usage: prosody_edit2.py <in.wav> <out.wav> <a_onset_s> [<clip_before.wav> <clip_after.wav>]
Edit (scaled by k until the targets hold): AN pitch -1.5k st (floor -5), THRO +2k st (cap +6), tempo AN 1.12 / THRO 0.88 from k>=1.25, levels: AN = its own level -1 dB, THRO = max(own +1 dB, AN + 3.5 dB).
Targets: THRO f0 peak >= AN + 3 st, THRO RMS peak >= AN + 3 dB, THRO_v longer than AN_v."""
import sys, json, subprocess, numpy as np, soundfile as sf, librosa
sys.path.insert(0, ".")
import rword
SR48, SR = 48000, 16000; I = lambda s: int(round(s * SR48)); XF = int(0.010 * SR48); H = XF // 2; HOP = 0.0025

def load48(p):
    x, sr = sf.read(p); x = x if x.ndim == 1 else x[:, 0]
    return x if sr == SR48 else librosa.resample(x, orig_sr=sr, target_sr=SR48)
def to16(y, ref=None):
    z = librosa.resample(y, orig_sr=SR48, target_sr=SR); return z / ((np.abs(z).max() if ref is None else ref) + 1e-9)
def xfade(a, b, n=XF):
    t = np.linspace(0, np.pi / 2, n); return np.concatenate([a[:-n], a[-n:] * np.cos(t) + b[:n] * np.sin(t), b[n:]])
def rb(x, st, tempo):
    if abs(st) < 0.05 and abs(tempo - 1) < 0.01: return x
    pad = 2400; r = 2 ** (st / 12)
    p = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR48), "-ac", "1", "-i", "-", "-filter:a", f"rubberband=pitch={r}:tempo={tempo}:formant=preserved:pitchq=quality", "-f", "f32le", "-"],
                       input=np.concatenate([np.zeros(pad), x, np.zeros(pad)]).astype(np.float32).tobytes(), capture_output=True, check=True)
    z = np.frombuffer(p.stdout, dtype=np.float32).astype(np.float64); q = int(round(pad / tempo)); n = int(round(len(x) / tempo))
    return z[q:q + n] if len(z) >= q + n else np.concatenate([z[q:], np.zeros(q + n - len(z))])

def th_margin(x, mode):
    import torch, thctc
    y = to16(x)
    if mode == "line9": return thctc.score(y)[0]
    y = y[int(0.04 * SR):int(0.62 * SR)]; y = np.concatenate([np.zeros(3200), y, np.zeros(3200)]); y = y / (np.abs(y).max() + 1e-9)
    with torch.no_grad(): em, _ = rword._M(torch.tensor(y, dtype=torch.float32)[None])
    base = thctc.nll(em, "ANTHROPIC"); al = [thctc.nll(em, a.replace("'S", "").rstrip("S")) for a in thctc.ALT]; return round(min(al) - base, 2)

def segments(x, a):
    y = to16(x); db, _ = rword.env_db(y, hop=HOP, win=0.015); n = len(db)
    i = int((a + 0.10) / HOP); quiet = db < -30
    while i < n and not quiet[i]: i += 1
    g0 = i
    while i < n and quiet[i]: i += 1
    g1 = i                                            # first loud frame after the TH gap
    pv = db[g1:g1 + int(0.08 / HOP)].max()             # THRO's own level (its onset plateau), NOT the louder PIC vowel after it
    j = g1 + int(0.06 / HOP)
    while j < n and db[j] > pv - 8: j += 1            # first dip after THRO = the /p/ closure
    return dict(a=a, an_end=g0 * HOP - 0.004 - float(__import__('os').environ.get('AN_TRIM', '0.0')), thro_start=g1 * HOP + 0.003 + float(__import__("os").environ.get("THRO_ONSET", "0.0")), thro_end=j * HOP)

def stats(x, an, th, ref):
    y = to16(x, ref); db, _ = rword.env_db(y, hop=HOP, win=0.015)
    f0, _, _ = librosa.pyin(y, fmin=70, fmax=400, sr=SR, frame_length=1024, hop_length=int(HOP * SR)); t = np.arange(len(f0)) * HOP; out = {}
    for nm, (s0, s1) in (("AN", an), ("THRO", th)):
        w = (t >= s0) & (t < s1); ff = f0[w]; ff = ff[~np.isnan(ff)]
        out[nm] = dict(f0_peak_st=round(float(12 * np.log2(ff.max() / 100.0)), 1) if len(ff) else None, rms_db=round(float(db[int(s0 / HOP):int(s1 / HOP)].max()), 1), dur=round(float(s1 - s0), 3))
    return out

def apply(x, sg, an, th, targets, ref):
    a, e1, s2, e2 = sg["a"], sg["an_end"], sg["thro_start"], sg["thro_end"]
    seg = lambda s, e: x[max(0, I(s) - H):min(len(x), I(e) + H)]
    def edit(piece, st, tp, tg):
        pc = rb(piece, st, tp); z = librosa.resample(pc, orig_sr=SR48, target_sr=SR) / (ref + 1e-9)
        e, _ = rword.env_db(z if len(z) > 400 else np.pad(z, (0, 400)), hop=HOP, win=0.015)
        return pc * 10 ** ((tg - float(e.max())) / 20)
    p_an = edit(seg(a, e1), an[0], an[1], targets[0]); p_th = edit(seg(s2, e2), th[0], th[1], targets[1])
    out = x[:I(a) + H]; s_an = (len(out) - H) / SR48
    out = xfade(out, p_an); an_end = (len(out) - H) / SR48
    mid = x[I(e1) - H:I(s2) + H]                                  # TH gap, untouched
    out = xfade(out, mid); thro_start = (len(out) - H) / SR48
    out = xfade(out, p_th); thro_end = (len(out) - H) / SR48
    out = xfade(out, x[I(e2) - H:])
    return out, (s_an, an_end), (thro_start, thro_end)

def main(inp, outp, a, mode, cb=None, ca=None):
    x = load48(inp); sg = segments(x, a); ref = float(np.abs(librosa.resample(x, orig_sr=SR48, target_sr=SR)).max())
    before = stats(x, (sg["a"], sg["an_end"]), (sg["thro_start"], sg["thro_end"]), ref)
    print("segments", {k: round(v, 3) for k, v in sg.items()}, "before", before)
    t_an = before["AN"]["rms_db"] - 1.0; t_th = max(before["THRO"]["rms_db"] + 1.0, t_an + 3.5)
    best = None; th0 = th_margin(x, mode); print("TH margin before", th0)
    for k in (1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0):
        an = (max(-1.5 * k, -5.0), 1.12 if k >= 1.25 else 1.0); th = (min(2.0 * k, 6.0), 0.88 if k >= 1.25 else 1.0)
        out, san, sth = apply(x, sg, an, th, (t_an, t_th), ref)
        pk = float(np.abs(out).max())
        if pk > 0.93: out = out * (0.93 / pk)            # no clipping
        after = stats(out, san, sth, ref); thm = th_margin(out, mode)
        met = after["THRO"]["f0_peak_st"] - after["AN"]["f0_peak_st"] >= 3.0 and after["THRO"]["rms_db"] - after["AN"]["rms_db"] >= 3.0 and after["THRO"]["dur"] > after["AN"]["dur"]
        th_ok = thm >= 4.0
        print(f"k={k}: AN pitch {an[0]:+.2f} tempo {an[1]}  THRO pitch {th[0]:+.2f} tempo {th[1]}  -> {after}  TH margin {thm}  targets {'met' if met else 'not met'}  TH {'ok' if th_ok else 'LOST'}")
        if th_ok: best = (k, an, th, out, after, san, sth, thm, met)
        if met and th_ok: break
        if not th_ok and best is not None: break
    k, an, th, out, after, san, sth, thm, met = best
    sf.write(outp, out, SR48, subtype="PCM_16")
    if cb:
        s0, s1 = max(0, a - 0.25), sth[1] + 0.50
        sf.write(cb, x[I(s0):I(s1 - (sth[1] - sg["thro_end"]))], SR48, subtype="PCM_16"); sf.write(ca, out[I(s0):I(s1)], SR48, subtype="PCM_16")
    print("REPORT " + json.dumps(dict(file=inp, k=k, AN=dict(pitch_st=round(an[0], 2), tempo=an[1]), THRO=dict(pitch_st=round(th[0], 2), tempo=th[1]), before=before, after=after, dur_before=round(len(x) / SR48, 3), dur_after=round(len(out) / SR48, 3), th_before=th0, th_after=thm, targets_met=bool(met), seg=dict((k2, round(v, 3)) for k2, v in sg.items()))))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4], *(sys.argv[5:7] if len(sys.argv) > 5 else []))
