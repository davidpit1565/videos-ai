"""The decision rule, checked against every row whose answer is known.

Cheap on purpose: it re-measures nothing and generates no audio, so it can run in the gate.
What it protects is the part that actually went wrong twice — a threshold moved by hand until
the numbers agreed with what I wanted. Move BAND and this fails and names the row.

Re-validating the signal extraction itself means regenerating the audio; the calibration file
says how.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import burst

CAL = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "voice", "profile", "calib", "burst-groundtruth.json")

def main():
    rows = json.load(open(CAL))["rows"]
    # In scope: the contrast the rule is calibrated for. The other words are recorded in the
    # calibration file as documented limits — /tr/ groups with /th/, /f/ falls below the band,
    # /s/ spans both — and are printed so the limits stay visible instead of being forgotten.
    SCOPE = ("three", "two", "tea")
    bad, limits = [], []
    for r in rows:
        v = burst.verdict({"peak": r["peak"], "rise": 3.0})
        want = "frication" if r["truth"] == "fricative" else "burst"
        if r["word"] not in SCOPE:
            limits.append(f"{r['word']}-s{r['seed']} peak {r['peak']:+.1f}: {v} "
                          f"(truth {r['truth']}) — out of scope")
            continue
        if v != want:
            bad.append(f"{r['word']}-s{r['seed']} peak {r['peak']:+.1f}: {v}, expected {want}")
    for b in bad:
        print("  FAIL " + b)
    for l in limits:
        print("  note " + l)
    n = sum(1 for r in rows if r["word"] in SCOPE)
    print(f"burst rule: {n - len(bad)}/{n} in-scope rows agree with ground truth "
          f"(BAND={burst.BAND}, scope={burst.IN_SCOPE})")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
