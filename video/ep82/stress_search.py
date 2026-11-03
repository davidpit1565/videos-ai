#!/usr/bin/env python3
"""Search the mildest stress edit that moves prominence to THRO WITHOUT losing the TH (CTC margin >= 4.0, Whisper still writes Anthropic).
usage: stress_search.py <in.wav> <out.wav> <a_onset> <line2|line9> [clip_before clip_after]"""
import sys, os, json, itertools, numpy as np, librosa, soundfile as sf
sys.path.insert(0, ".")
import prosody_edit2 as P
from faster_whisper import WhisperModel
_W = WhisperModel('base.en', device='cpu', compute_type='int8', cpu_threads=2)
def heard(out):
    y = P.to16(out); y = np.concatenate([np.zeros(8000), y, np.zeros(8000)]).astype(np.float32)
    sg, _ = _W.transcribe(y, language='en', beam_size=5); return ' '.join(t.text.strip() for t in sg)
inp, outp, a, mode = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
x = P.load48(inp); ref = float(np.abs(librosa.resample(x, orig_sr=P.SR48, target_sr=P.SR)).max())
th0 = P.th_margin(x, mode); cands = []
for trim, onset, an_p, th_p in itertools.product((0.0,), (0.05, 0.07, 0.09), (0.0, -1.5, -2.25, -3.0), (2.0, 3.5, 5.0, 6.0)):
    os.environ["AN_TRIM"] = str(trim); os.environ["THRO_ONSET"] = str(onset); sg = P.segments(x, a)
    b = P.stats(x, (sg["a"], sg["an_end"]), (sg["thro_start"], sg["thro_end"]), ref)
    t_an = b["AN"]["rms_db"] - 1.0; t_th = max(b["THRO"]["rms_db"] + 1.0, t_an + 3.5)
    out, san, sth = P.apply(x, sg, (an_p, 1.0), (th_p, 1.0), (t_an, t_th), ref)
    pk = float(np.abs(out).max()); out = out * (0.93 / pk) if pk > 0.93 else out
    af = P.stats(out, san, sth, ref); thm = P.th_margin(out, mode)
    df0 = af["THRO"]["f0_peak_st"] - af["AN"]["f0_peak_st"]; drms = af["THRO"]["rms_db"] - af["AN"]["rms_db"]
    print(f"onset {onset} AN {an_p:+.2f} THRO {th_p:+.1f}: dF0 {df0:+.1f} dRMS {drms:+.1f} TH {thm}", flush=True)
    if thm >= 4.0 and drms >= 3.0: cands.append(dict(df0=df0, mag=abs(an_p) + abs(th_p), onset=onset, an_p=an_p, th_p=th_p, out=out, af=af, thm=thm, sg=sg, b=b, san=san, sth=sth, trim=trim))
meet = [c for c in cands if c["df0"] >= 3.0]
ranked = sorted(meet, key=lambda c: c["mag"]) if meet else sorted(cands, key=lambda c: -c["df0"])
print("candidates meeting every target:", len(meet), "| TH-safe candidates:", len(cands), flush=True)
best = None
for c in ranked:
    h = heard(c["out"]); ok = "anthropic" in h.lower().replace(" ", ""); print("   try", c["onset"], c["an_p"], c["th_p"], "dF0", round(c["df0"], 1), "Whisper:", h, "->", "keeps TH" if ok else "TH lost", flush=True)
    if ok: best = (c["df0"], c["onset"], c["an_p"], c["th_p"], c["out"], c["af"], c["thm"], c["sg"], c["b"], c["san"], c["sth"], h, c["trim"]); break
score, onset, an_p, th_p, out, af, thm, sg, b, san, sth, hh, trim = best
sf.write(outp, out, P.SR48, subtype="PCM_16")
if len(sys.argv) > 6:
    s0, s1 = max(0, a - 0.25), sth[1] + 0.50; sf.write(sys.argv[5], x[P.I(s0):P.I(s1)], P.SR48, subtype="PCM_16"); sf.write(sys.argv[6], out[P.I(s0):P.I(s1)], P.SR48, subtype="PCM_16")
print("BEST " + json.dumps(dict(file=inp, an_trim=trim, onset=onset, AN_pitch_st=an_p, THRO_pitch_st=th_p, before=b, after=af, dF0=round(af["THRO"]["f0_peak_st"] - af["AN"]["f0_peak_st"], 1), dRMS=round(af["THRO"]["rms_db"] - af["AN"]["rms_db"], 1), th_before=th0, th_after=thm, whisper=hh)))
