"""Shorten the silence *inside* sentences, and leave the speaking speed alone.

The reference speaker reaches 187 words a minute at 5.90 syllables a second. Ours ran
151 words a minute at 6.19 syllables a second — already the faster tongue, and still
the slower read, because 38% of our runtime is silence against his 18%. Speeding the
voice up was pushing the one lever that was already past the target; the silence is
the lever that was never touched.

Between-line gaps are regap.py's job. This is the other half: the pauses the model puts
in the middle of a line, which no setting controls.

Cues are rewritten, so export/retime.py moves the picture to match.
"""
import sys, json, argparse, wave, numpy as np

def read(p):
    with wave.open(p) as w:
        sr, n, ch = w.getframerate(), w.getnframes(), w.getnchannels()
        y = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
    if ch > 1:
        y = y.reshape(-1, ch).mean(1)
    return y, sr

def write(p, y, sr):
    with wave.open(p, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())

def runs(y, sr, floor_db, min_len):
    """silent stretches, as (start, end) sample indices"""
    h = int(0.010 * sr)
    f = y[:len(y) // h * h].reshape(-1, h)
    rms = 20 * np.log10(np.sqrt((f ** 2).mean(1)) + 1e-9)
    ref = np.percentile(rms, 95)
    quiet = rms < ref + floor_db
    out, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            if (j - i) * 0.010 >= min_len:
                out.append((i * h, j * h))
            i = j
        else:
            i += 1
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("--cues", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--floor", type=float, default=-38.0,
                    help="dB below the line's own 95th percentile that counts as silence")
    ap.add_argument("--min", type=float, default=0.26,
                    help="only pauses at least this long are shortened")
    ap.add_argument("--to", type=float, default=0.16,
                    help="what they are shortened to")
    ap.add_argument("--edge", type=float, default=0.05,
                    help="silence this close to a line's own edge is the gap, not a pause")
    a = ap.parse_args()

    y, sr = read(a.wav)
    cues = json.load(open(a.cues))
    keep = np.ones(len(y), dtype=bool)
    cut_total, cut_n = 0.0, 0

    for c in cues:
        s, e = int(float(c["start"]) * sr), int(float(c["end"]) * sr)
        seg = y[s:e]
        if len(seg) < int(0.2 * sr):
            continue
        for r0, r1 in runs(seg, sr, a.floor, a.min):
            # a silence touching the line's own boundary belongs to the gap
            if r0 <= int(a.edge * sr) or r1 >= len(seg) - int(a.edge * sr):
                continue
            drop = (r1 - r0) - int(a.to * sr)
            if drop <= 0:
                continue
            mid = (r0 + r1) // 2
            keep[s + mid - drop // 2: s + mid - drop // 2 + drop] = False
            cut_total += drop / sr
            cut_n += 1

    # cues move by however much was removed before them
    removed = np.cumsum(~keep) / sr
    def at(t):
        i = min(len(removed) - 1, max(0, int(t * sr)))
        return round(t - float(removed[i]), 3)
    new = [dict(c, start=at(float(c["start"])), end=at(float(c["end"]))) for c in cues]

    write(a.out, y[keep], sr)
    json.dump(new, open(a.out.rsplit(".", 1)[0] + "-cues.json", "w"), indent=1)
    print(f"{a.wav} -> {a.out}")
    print(f"  {cut_n} pauses inside lines shortened to {a.to:.2f}s")
    print(f"  {cut_total:.2f}s removed  ({len(y)/sr:.2f}s -> {keep.sum()/sr:.2f}s)")

if __name__ == "__main__":
    main()

# Run against episode 01's narration it found ZERO pauses to shorten, and that negative
# is the useful part: the longest silence anywhere inside the reel is 0.36s. The 19% of
# runtime that is silence is not a few long pauses inside sentences — it is the gaps
# between lines that the build itself sets, five of which were 1.10s only because the
# colour cards are 0.90s long and have to fit inside one. Five decorative cards were
# buying 5.5 seconds of dead air in a 45-second video. The lever was the card length,
# not the pauses, and this tool is what ruled the pauses out.
