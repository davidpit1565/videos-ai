"""Does any line drift off his voice's usual American accent?

Found by ear, not by a tool: episode 30's line 6 ("After the paste... JavaScript first...
nothing else unless you ask for more.") came out sounding, in David's words, "a bit
Indian" for most of its second half — a real, audible accent drift on that one take that
none of the existing checks catch. voice_doctor.py measures pacing, level, sibilance and
word endings; none of that is accent. This is a different axis entirely.

What this uses: a pretrained English-accent classifier (dima806/english_accents_classification,
wav2vec2 fine-tuned on Common Voice; labels us/england/indian/australia/canada). Tested
against this exact repo's voice before trusting it here: it is NOT well-calibrated in an
absolute sense — it scores David's own clean reference recording as 92% "indian", and
every normal line in episode 30 splits its top score between "us" and "canada" rather than
landing cleanly on "us". So a flat "is this line American" threshold does not work.

What it IS reliably good at, on the one real case tested so far: catching a line that is
a sharp outlier from the rest of the SAME file. Every clean line in episode 30 scored the
"indian" label at 0.0008-0.0012. The flagged line 6 scored 0.499 — a ~500x jump, not a
borderline call. So this flags a line only when it stands out from its own episode's own
baseline by a wide margin, the same "flag relative to this file's own median" approach
voice_doctor.py already uses for tail energy and sibilance, rather than trusting the
model's absolute label.

Caveat, stated plainly: this has only ever caught one real case, on the "indian" label.
Gating on "england"/"australia" too was tried and immediately produced two false-positive
-looking flags on episode 29 — an already-shipped file David watched twice (per the
check-fix-re-check-send rule) and never once flagged for accent. With no ear-confirmed
case for those two labels, gating the build on them would be inventing a defect, not
catching one — exactly what "never fabricate" rules out. So only "indian" fails the
build; "england"/"australia" still print per line for visibility, in case a real,
ear-confirmed case for one of them ever turns up to calibrate against. The threshold
below (NOT_US_FLOOR and the 8x-median rule) is a first cut on n=1, not a validated
rate — treat a flag as "worth listening to," not as certain, and don't read a long quiet
stretch as proof it works; it may just mean no line has drifted since.

    python3 audio/check_accent.py audio/reel30-narration-r.wav
"""
import argparse, json, os, sys, warnings
import numpy as np

warnings.filterwarnings("ignore")

MODEL_ID = "dima806/english_accents_classification"
# Every non-"us"/"canada" label prints per line for visibility. Only GATED_LABELS fails
# the build — see the caveat above for why "england"/"australia" are shown, not gated.
OFF_LABELS = ("indian", "england", "australia")
GATED_LABELS = ("indian",)
# Absolute floor: below this, a score is noise no matter how it compares to the median
# (the reference clip itself scored "indian" 0.92, so tiny scores are not unusual here).
NOT_US_FLOOR = 0.15
# Multiple of the file's own median for that label before a line counts as an outlier.
OUTLIER_MULT = 8


def load_mono(path, sr_target=16000):
    import soundfile as sf
    y, sr = sf.read(path, always_2d=False)
    if y.ndim > 1:
        y = y.mean(axis=1)
    if sr != sr_target:
        import librosa
        y = librosa.resample(y.astype(np.float32), orig_sr=sr, target_sr=sr_target)
        sr = sr_target
    return y.astype(np.float32), sr


def classify_lines(wav_path, cues):
    from transformers import pipeline
    clf = pipeline("audio-classification", model=MODEL_ID)
    y, sr = load_mono(wav_path)
    rows = []
    for c in cues:
        a, b = int(c["start"] * sr), int(min(c["end"], len(y) / sr) * sr)
        clip = y[a:b]
        if len(clip) < int(0.3 * sr):
            rows.append({"n": c["n"], "line": c["line"], "scores": {}})
            continue
        out = clf({"array": clip, "sampling_rate": sr}, top_k=5)
        rows.append({"n": c["n"], "line": c["line"],
                     "scores": {o["label"]: o["score"] for o in out}})
    return rows


def verdict(rows):
    issues = []
    for label in GATED_LABELS:
        vals = [r["scores"].get(label, 0.0) for r in rows if r["scores"]]
        if not vals:
            continue
        med = float(np.median(vals))
        floor = max(NOT_US_FLOOR, med * OUTLIER_MULT)
        for r in rows:
            s = r["scores"].get(label, 0.0)
            if s >= floor:
                issues.append((r["n"], r["line"], label, s, med))
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("--cues", help="defaults to <wav>-cues.json")
    a = ap.parse_args()

    cues_path = a.cues or os.path.splitext(a.wav)[0] + "-cues.json"
    if not os.path.exists(cues_path):
        sys.exit("no cue file at " + cues_path)
    cues = json.load(open(cues_path))
    cues = cues if isinstance(cues, list) else cues["cues"]

    rows = classify_lines(a.wav, cues)
    issues = verdict(rows)

    print(f"{a.wav}  {len(cues)} lines — accent check ({MODEL_ID})")
    for r in rows:
        s = r["scores"]
        if not s:
            print(f"   ln {r['n']}  (too short to classify)")
            continue
        top = max(s, key=s.get)
        print(f"   ln {r['n']}  top={top} {s[top]:.2f}   "
              f"{ {k: round(v,3) for k,v in s.items() if k in OFF_LABELS} }   "
              f"{r['line'][:44]}")

    if issues:
        print(f"\n  flagged — sounds like a different accent than the rest of this file:")
        for n, line, label, s, med in issues:
            print(f"   ln {n}  {label} {s:.2f} (file median {med:.3f})   {line[:60]}")
        print(f"\n  this is a heuristic, not a certainty (see the file's own docstring) — "
              f"listen to the flagged line(s) before rerolling.")
        sys.exit(1)
    print("\n  nothing stands out from this file's own baseline.")
    sys.exit(0)


if __name__ == "__main__":
    main()
