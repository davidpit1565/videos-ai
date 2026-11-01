#!/usr/bin/env python3
"""Convert a HyperFrames build's cue file into the format voice_doctor.py / check_accent.py read.

  python3 export/hf_cues.py <cues.json> <out-cues.json>

In : {"lines":[{"n":"01-new","text":"...","start":0.12,"end":2.17}], "D":25.27}   (build_v6.py)
Out: {"cues":[{"n":1,"line":"...","start":0.12,"end":2.17}]}                        (voice_doctor)
"""
import json, sys

src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src))
lines = d["lines"] if isinstance(d, dict) else d
json.dump({"cues": [{"n": i + 1, "line": c.get("line", c.get("text", "")),
                     "start": float(c["start"]), "end": float(c["end"])}
                    for i, c in enumerate(lines)]}, open(dst, "w"), indent=1)
print(f"{len(lines)} cues -> {dst}")
