#!/usr/bin/env python3
"""Set the silence between spoken lines to an exact length, without regenerating a word.

The gaps are built into the assembled narration, so changing one used to mean a
fifteen-minute re-run of the model. This edits the silence instead: it finds the
quiet stretch between two lines, trims or pads it to the target, and writes a new
cue file with the shifted times so the picture can be retimed to match.

He flagged the section breaks specifically — "he stops, then moves on". A 0.85s
hole with a flash card floating in the middle of it reads as a stall, where 0.42s
between ordinary sentences reads as breathing.

  python3 audio/regap.py audio/voice/ep01-paced.wav --gap 0.42 --long 0.55 \
      --sections 4,8,13,15 --out audio/voice/ep01-tight.wav
"""
import argparse, json, os, wave
import numpy as np


def load(path):
    with wave.open(path) as w:
        sr = w.getframerate()
        y = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return y, sr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("--cues", help="defaults to <wav>-cues.json")
    ap.add_argument("--out", required=True)
    ap.add_argument("--gap", type=float, default=0.42)
    ap.add_argument("--long", type=float, default=0.55)
    ap.add_argument("--sections", default="", help="line numbers a section ends on")
    a = ap.parse_args()

    cues_path = a.cues or os.path.splitext(a.wav)[0] + "-cues.json"
    cues = json.load(open(cues_path))
    cues = cues if isinstance(cues, list) else cues["cues"]
    sections = {int(x) for x in a.sections.split(",") if x.strip()}

    y, sr = load(a.wav)
    out, new, shift = [], [], 0.0
    for i, c in enumerate(cues):
        s, e = float(c["start"]), float(c["end"])
        a0, b0 = int(s * sr), int(e * sr)
        if i == 0:
            out.append(y[:a0])                       # keep the head exactly as built
        out.append(y[a0:b0])
        new.append(dict(c, start=round(s + shift, 3), end=round(e + shift, 3)))
        if i + 1 == len(cues):
            out.append(y[b0:])                       # and the tail
            break
        nxt = float(cues[i + 1]["start"])
        want = a.long if c["n"] in sections else a.gap
        have = nxt - e
        n_have, n_want = int(have * sr), int(want * sr)
        room = y[b0:int(nxt * sr)]
        if n_want <= n_have:
            # keep the room tone from both edges of the original gap, drop the middle
            half = n_want // 2
            out.append(np.concatenate([room[:half], room[len(room) - (n_want - half):]])
                       if n_want else room[:0])
        else:
            # extend with the quietest 60 ms of the gap, not with the gap itself —
            # tiling a gap that holds a breath or a stray syllable repeats it
            k = max(1, int(0.06 * sr))
            if n_have >= k:
                win = np.array([np.abs(room[i:i + k]).mean()
                                for i in range(0, max(1, n_have - k), max(1, k // 2))])
                q = int(np.argmin(win)) * max(1, k // 2)
                quiet = room[q:q + k]
            else:
                quiet = room
            reps = int(np.ceil((n_want - n_have) / max(1, len(quiet))))
            pad = np.tile(quiet, reps)[:n_want - n_have]
            out.append(np.concatenate([room, pad]))
        shift += want - have

    track = np.clip(np.concatenate(out), -1, 1)
    with wave.open(a.out, "w") as o:
        o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr)
        o.writeframes((track * 32767).astype(np.int16).tobytes())
    json.dump(new, open(os.path.splitext(a.out)[0] + "-cues.json", "w"), indent=1)

    print(f"{a.wav} {len(y)/sr:.2f}s -> {a.out} {len(track)/sr:.2f}s")
    for c1, c2 in zip(new, new[1:]):
        print(f"  after line {c1['n']:>2}: {c2['start'] - c1['end']:.2f}s"
              f"{'  (section)' if c1['n'] in sections else ''}")


if __name__ == "__main__":
    main()
