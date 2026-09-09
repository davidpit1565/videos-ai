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

What it IS reliably good at: catching a line that is a sharp outlier from the rest of
the SAME file. Every clean line in episode 30 scored the "indian" label at 0.0008-0.0012;
the flagged line 6 scored 0.499 — a ~500x jump, not a borderline call. So this flags a
line only when it stands out from its own episode's own baseline by a wide margin, the
same "flag relative to this file's own median" approach voice_doctor.py already uses for
tail energy and sibilance, rather than trusting the model's absolute label.

Widened 9.9.2026, after a second real case: episode 31's lines 1-2 got flagged by ear
("almost every T/D still sounds a bit Indian, not American enough") but this checker's
first version, which gated on the "indian" label alone, missed it — line 1 actually
scored top=england 0.59 (indian was only 0.048, under the old floor), and line 2 was
clean by that narrow measure too even though the same ear-flagged quality was present
across both lines. Gating on "indian" alone was too literal a reading of what David's ear
reported ("sounds Indian") — the real signal both times was the SAME thing: whatever
made those lines not sound like his own reference voice, regardless of which foreign-
accent label the classifier happened to attach to that quality. So this now gates on
1 - P(us) - P(canada) — how far a line sits from the "sounds like his own voice" bucket
overall — instead of picking one specific foreign-accent label to chase. Every clean
line measured so far (episodes 29 and 30) splits its top score between "us" and "canada"
and keeps this combined total below roughly 0.5-0.6; the two confirmed-bad cases (ep30
line 6, ep31 lines 1-2) all pushed it well above that.

Caveat, stated plainly: this is now calibrated on two real, ear-confirmed episodes, not
one — better than the first cut, but still not a validated rate. Treat a flag as "worth
listening to," not as certain, and don't read a long quiet stretch as proof it works; it
may just mean no line has drifted since.

    python3 audio/check_accent.py audio/reel30-narration-r.wav
"""
import argparse, json, os, sys, warnings
import numpy as np

warnings.filterwarnings("ignore")

MODEL_ID = "dima806/english_accents_classification"
# Printed per line for visibility, alongside the gating metric below.
OFF_LABELS = ("indian", "england", "australia")
# What actually gates the build: 1 - P(us) - P(canada), i.e. how far a line sits from
# the "sounds like his own reference voice" bucket, not any one specific foreign-accent
# label — see the docstring above for why this replaced a narrower "indian only" gate.
AMERICAN_LABELS = ("us", "canada")
# Absolute floor: below this, a score is noise no matter how it compares to the median.
NOT_AMERICAN_FLOOR = 0.45
# Multiple of the file's own median before a line counts as an outlier.
OUTLIER_MULT = 4


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


def not_american(scores):
    return 1.0 - scores.get("us", 0.0) - scores.get("canada", 0.0)


def verdict(rows):
    issues = []
    vals = [not_american(r["scores"]) for r in rows if r["scores"]]
    if not vals:
        return issues
    med = float(np.median(vals))
    floor = max(NOT_AMERICAN_FLOOR, med * OUTLIER_MULT)
    for r in rows:
        if not r["scores"]:
            continue
        na = not_american(r["scores"])
        if na >= floor:
            issues.append((r["n"], r["line"], na, med))
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
        print(f"   ln {r['n']}  top={top} {s[top]:.2f}  not-american={not_american(s):.2f}   "
              f"{ {k: round(v,3) for k,v in s.items() if k in OFF_LABELS} }   "
              f"{r['line'][:44]}")

    if issues:
        print(f"\n  flagged — sounds less like his own reference voice than the rest of this file:")
        for n, line, na, med in issues:
            print(f"   ln {n}  not-american {na:.2f} (file median {med:.3f})   {line[:60]}")
        print(f"\n  this is a heuristic, not a certainty (see the file's own docstring) — "
              f"listen to the flagged line(s) before rerolling.")
        sys.exit(1)
    print("\n  nothing stands out from this file's own baseline.")
    sys.exit(0)


if __name__ == "__main__":
    main()
