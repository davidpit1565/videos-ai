#!/usr/bin/env python3
"""Move the stress of 'Anthropic(s)' from AN to THRO by editing the three syllable segments (rubberband pitch + tempo, gain, 10 ms equal-power crossfades at the dips).
usage: prosody_edit.py <in.wav> <out.wav> <a> <b> [<clip_before.wav> <clip_after.wav>]   a,b = the word window in seconds (line 2: 0.04 0.616; line 9: from stress.word_window)
Starts from AN -1.5 st / -3 dB, THRO +2 st / +3 dB, PIC unchanged and scales the edit (k = 1.0 ... 2.0, caps: pitch -3.5 / +4 st, gain -5 / +5 dB, tempo 1.12 / 0.88)
until: THRO f0 peak >= AN + 3 st, THRO RMS peak >= AN + 3 dB, THRO longer than AN.  Prints before/after numbers (f0 peak in st re 100 Hz, RMS peak dB, duration)."""
import sys, json, subprocess, numpy as np, soundfile as sf, librosa
sys.path.insert(0, ".")
import rword, syl, stress
SR48, SR = 48000, 16000; I = lambda s: int(round(s * SR48)); XF = int(0.010 * SR48); H = XF // 2

def load48(p):
    x, sr = sf.read(p); x = x if x.ndim == 1 else x[:, 0]
    return x if sr == SR48 else librosa.resample(x, orig_sr=sr, target_sr=SR48)
def to16(y): z = librosa.resample(y, orig_sr=SR48, target_sr=SR); return z / (np.abs(z).max() + 1e-9)
def xfade(a, b, n=XF):
    t = np.linspace(0, np.pi / 2, n); return np.concatenate([a[:-n], a[-n:] * np.cos(t) + b[:n] * np.sin(t), b[n:]])
def rb(x, st, tempo):
    if abs(st) < 0.05 and abs(tempo - 1) < 0.01: return x
    pad = 2400; r = 2 ** (st / 12)
    p = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR48), "-ac", "1", "-i", "-", "-filter:a", f"rubberband=pitch={r}:tempo={tempo}:formant=preserved:pitchq=quality", "-f", "f32le", "-"],
                       input=np.concatenate([np.zeros(pad), x, np.zeros(pad)]).astype(np.float32).tobytes(), capture_output=True, check=True)
    z = np.frombuffer(p.stdout, dtype=np.float32).astype(np.float64); q = int(round(pad / tempo)); n = int(round(len(x) / tempo))
    return z[q:q + n] if len(z) >= q + n else np.concatenate([z[q:], np.zeros(q + n - len(z))])
def refine(env, hop, t, w=0.025):
    i0, i1 = max(0, int((t - w) / hop)), min(len(env), int((t + w) / hop) + 1); return (i0 + int(np.argmin(env[i0:i1]))) * hop

def sylstats(x48, a, b, cuts=None):
    y = to16(x48); c = list(cuts) if cuts else syl.cuts(y, a, b)[0]; hop = 0.0025
    db, _ = rword.env_db(y, hop=hop, win=0.015)
    f0, _, _ = librosa.pyin(y, fmin=70, fmax=400, sr=SR, frame_length=1024, hop_length=int(hop * SR)); t = np.arange(len(f0)) * hop
    out = {}
    for nm, s0, s1 in zip(("AN", "THRO", "PIC"), c[:3], c[1:]):
        w = (t >= s0) & (t < s1); ff = f0[w]; ff = ff[~np.isnan(ff)]
        out[nm] = dict(f0_peak_st=round(float(12 * np.log2(ff.max() / 100.0)), 1) if len(ff) else None, rms_db=round(float(db[int(s0 / hop):int(s1 / hop)].max()), 1), dur=round(float(s1 - s0), 3))
    return out, c

def peak_db(piece, ref):
    z = librosa.resample(piece, orig_sr=SR48, target_sr=SR) / ref; e, _ = rword.env_db(z if len(z) > 400 else np.pad(z, (0, 400)), hop=0.0025, win=0.015); return float(e.max())

def apply(x, a, b, cuts, an, th, pic, targets=None, ref=1.0):
    c1, c2 = cuts
    seg = lambda s, e: x[max(0, I(s) - H):min(len(x), I(e) + H)]
    pre = x[:I(a) + H]; post = x[I(b) - H:]
    parts = []
    for (s, e), (st, db, tp) in zip(((a, c1), (c1, c2), (c2, b)), (an, th, pic)):
        pc = rb(seg(s, e), st, tp)
        tg = targets[len(parts)] if targets else None
        parts.append(pc * 10 ** ((tg - peak_db(pc, ref)) / 20) if tg is not None else pc * 10 ** (db / 20))
    out = pre; seams = [(len(pre) - H) / SR48]
    for p in parts:
        out = xfade(out, p); seams.append((len(out) - H) / SR48)
    seams = seams[:-1] + [seams[-1]]
    out = xfade(out, post)
    return out, [seams[0], seams[1], seams[2], (len(out) - len(post) + H) / SR48]

def main(inp, outp, a, b, cb=None, ca=None):
    x = load48(inp); y = to16(x); before, c = sylstats(x, a, b)
    # refine the two cut points to the quietest frame nearby (the TH gap and the /p/ closure)
    db, hop = rword.env_db(y); c1, c2 = refine(db, hop, c[1]), refine(db, hop, c[2])
    print("cuts", [round(v, 3) for v in (a, c1, c2, b)])
    res = None
    ref = float(np.abs(librosa.resample(x, orig_sr=SR48, target_sr=SR)).max())
    targ_an = before['AN']['rms_db'] - 1.0; targ_th = max(before['THRO']['rms_db'] + 1.0, targ_an + 3.5); targets = [targ_an, targ_th, None]
    for k in (1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0):
        an = (max(-1.5 * k, -5.0), -3.0, 1.0); th = (min(2.0 * k, 6.0), 3.0, 1.0); pic = (0.0, 0.0, 1.0)
        if k >= 1.25: an = (an[0], an[1], 1.12); th = (th[0], th[1], 0.88)          # tempo only when pitch + gain alone were not enough
        out, seams = apply(x, a, b, (c1, c2), an, th, pic, targets, ref)
        after, _ = sylstats(out, a, seams[3], cuts=seams)
        ok = (after["THRO"]["f0_peak_st"] - after["AN"]["f0_peak_st"] >= 3.0) and (after["THRO"]["rms_db"] - after["AN"]["rms_db"] >= 3.0) and (after["THRO"]["dur"] > after["AN"]["dur"])
        print(f"k={k}: AN{an} THRO{th} -> after {after}  {'OK' if ok else 'not yet'}")
        res = (k, an, th, out, after, seams[3])
        if ok: break
    k, an, th, out, after, dend = res
    sf.write(outp, out, SR48, subtype="PCM_16")
    if cb:
        s0, s1 = max(0, a - 0.25), b + 0.25
        sf.write(cb, x[I(s0):I(s1)], SR48, subtype="PCM_16"); sf.write(ca, out[I(s0):I(dend + 0.25)], SR48, subtype="PCM_16")
    rep = dict(file=inp, k=k, AN=dict(pitch_st=an[0], gain_db=an[1], tempo=round(an[2], 2)), THRO=dict(pitch_st=th[0], gain_db=th[1], tempo=round(th[2], 2)), before=before, after=after, dur_before=round(len(x) / SR48, 3), dur_after=round(len(out) / SR48, 3), cuts=[round(v, 3) for v in (a, c1, c2, b)], dend=round(dend, 3))
    print("REPORT " + json.dumps(rep))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), *(sys.argv[5:7] if len(sys.argv) > 5 else []))
