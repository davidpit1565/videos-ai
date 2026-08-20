#!/usr/bin/env python3
"""Retime a reel so the video follows the narration, instead of the narration
being squeezed into the video.

The old order was: fixed cue slots in the HTML, then every spoken line
time-stretched (up to 12%) to land inside its slot. When a line was longer than
that, the clamp left it overrunning into the next slot — measured at up to
-0.60s on episode 02, which is two lines talking at once. That is the "words are
cut, no space between sentences" he heard.

So the narration is now built naturally, with a real pause after every line, and
this script moves the picture to match: every timing in the build — caption cues,
section flashes, scene in/out, animation beats, total duration — is mapped
through the same monotonic piecewise-linear curve anchored on the line
boundaries. Visual pacing is preserved; only the gaps grow.

  python3 export/retime.py video/reel-01-v3.html audio/voice/ep01-nat-cues.json \
          --out video/reel-01-v4.html
"""
import argparse, json, re, sys


def html_cues(src):
    m = re.search(r"var CUES=(\[.*?\]);", src, re.S)
    if not m:
        sys.exit("no CUES array")
    return json.loads(m.group(1)), m


def build_map(old, new):
    """Anchor pairs (old_t, new_t) from the line boundaries, plus the origin."""
    pts = [(0.0, 0.0)]
    for o, n in zip(old, new):
        pts.append((float(o[0]), float(n["start"])))
        pts.append((float(o[1]), float(n["end"])))
    pts.sort()
    # a duplicate or non-increasing x would make interpolation ambiguous
    clean = [pts[0]]
    for x, y in pts[1:]:
        if x > clean[-1][0] + 1e-6 and y >= clean[-1][1]:
            clean.append((x, y))
    return clean


def remap(pts, t):
    if t <= pts[0][0]:
        return round(t + (pts[0][1] - pts[0][0]), 3)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if t <= x1:
            f = (t - x0) / (x1 - x0)
            return round(y0 + f * (y1 - y0), 3)
    # past the last line: keep the tail's own length, shifted
    x0, y0 = pts[-1]
    return round(y0 + (t - x0), 3)


def gaps_of(new):
    """The silences between lines, as (start, end) — where a cut belongs."""
    return [(float(a["end"]), float(b["start"])) for a, b in zip(new, new[1:])]


def snap(t, gaps, flashes, fdur, lead=0.06):
    """Pull a cut into the silence it belongs to.

    Proportional remapping alone put the section flash in the middle of a 0.85s
    hole with silence on both sides, and the scene change 0.11s after it — which he
    described as the video stopping and then moving on. A cut has to land ON the
    flash, and the flash has to land at the top of the gap, not floating in it."""
    for g0, g1 in gaps:
        if g0 - 0.35 <= t <= g1 + 0.35:
            fl = [f for f in flashes if g0 - 0.35 <= f <= g1 + 0.35]
            if fl:
                return round(min(max(fl[0] + fdur / 2, g0), g1), 3)
            return round((g0 + g1) / 2, 3)
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("cues", help="the -cues.json written beside the narration wav")
    ap.add_argument("--out", required=True)
    ap.add_argument("--tail", type=float, default=0.5,
                    help="seconds of picture after the last word")
    a = ap.parse_args()

    src = open(a.html, encoding="utf-8").read()
    old, m = html_cues(src)
    new = json.load(open(a.cues))
    new = new if isinstance(new, list) else new["cues"]
    if len(old) != len(new):
        sys.exit(f"{len(old)} cues in the build, {len(new)} in the narration")

    pts = build_map(old, new)
    dur = round(float(new[-1]["end"]) + a.tail, 2)

    # captions carry their own text, so rebuild the array rather than patch numbers
    rows = [f'    [{remap(pts, float(o[0])):.2f},{remap(pts, float(o[1])):.2f},'
            f'{json.dumps(o[2], ensure_ascii=False)}]' for o in old]
    src = src[:m.start(1)] + "[\n" + ",\n".join(rows) + "\n  ]" + src[m.end(1):]

    gaps = gaps_of(new)
    fdur = float((re.search(r"var FDUR=([0-9.]+)", src) or [0, "0.34"])[1])

    # a section flash sits at the top of its gap, so the silence is behind the cut
    mf = re.search(r"var FLASH=(\[.*?\]);", src, re.S)
    flashes = []
    if mf:
        fl = json.loads(mf.group(1))
        for f in fl:
            t = remap(pts, float(f[0]))
            for g0, g1 in gaps:
                if g0 - 0.35 <= t <= g1 + 0.35 and g1 - g0 >= fdur + 0.1:
                    t = round(min(g0 + 0.06, g1 - fdur), 3)
                    break
            flashes.append(t)
        rows = [f'[{t:.2f},{json.dumps(f[1], ensure_ascii=False)},{f[2]}]'
                for t, f in zip(flashes, fl)]
        src = src[:mf.start(1)] + "[" + ",".join(rows) + "]" + src[mf.end(1):]

    # scene cuts land on the flash; animation beats keep their proportional place
    src = re.sub(r'data-(in|out)="([0-9.]+)"',
                 lambda g: f'data-{g.group(1)}="'
                           f'{snap(remap(pts, float(g.group(2))), gaps, flashes, fdur):g}"', src)
    src = re.sub(r'data-at="([0-9.]+)"',
                 lambda g: f'data-at="{remap(pts, float(g.group(1))):g}"', src)

    # a scene must have something on screen the instant the flash lifts. Every scene
    # here opened 0.31-0.38s empty, which after a hidden cut is a visible blank beat.
    edits = []
    for m in re.finditer(r'data-in="([0-9.]+)" data-out="[0-9.]+"(.*?)(?=data-in="|\Z)',
                         src, re.S):
        start = float(m.group(1))
        first = re.search(r'data-at="([0-9.]+)"', m.group(2))
        if not first or float(first.group(1)) - start <= 0.1:
            continue
        edits.append((m.start(2) + first.start(1), m.start(2) + first.end(1),
                      f"{start + 0.03:g}"))
    # apply back to front, or every offset after the first edit is stale
    for i, j, rep in reversed(edits):
        src = src[:i] + rep + src[j:]
    moved = len(edits)

    src = re.sub(r"var DUR=[0-9.]+", f"var DUR={dur:g}", src)
    open(a.out, "w", encoding="utf-8").write(src)

    print(f"{a.html} -> {a.out}")
    print(f"  duration {old[-1][1]}s -> {dur}s")
    worst = min((float(n2['start']) - float(n1['end'])) for n1, n2 in zip(new, new[1:]))
    print(f"  narration built naturally: smallest gap between lines {worst:+.2f}s")
    print(f"  {moved} scenes had their opening beat pulled onto the cut")


if __name__ == "__main__":
    main()
