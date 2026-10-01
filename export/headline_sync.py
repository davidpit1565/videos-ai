#!/usr/bin/env python3
"""Sync a fixed on-screen headline's own words to the narration, word by word, instead
of showing a second word-by-word caption underneath it for the same sentence.

David's direct feedback on episode 54: the on-screen headline and the bottom karaoke
caption show the same sentence twice at once. For the real-photo-composite style
(video/reel-template-photo.html), where the headline already carries the full line for
the whole scene, this replaces that duplicate — each headline word pops/brightens in
place exactly when its narration word is spoken (MotionKit.animateWordEmphasis), using
the same per-word timing export/karaoke.py derives from Whisper's alignment, so the
on-screen word and the spoken word can never drift apart. There is no separate caption
track for this style; this script does not touch #subs because the template has none.

The hook's climax phrase (<span class="box">...</span>) stays ONE atomic unit at
runtime (MotionKit.splitWordsSafe's own rule) even when it spans several words, so its
several Whisper windows collapse into one covering the start of its first spoken word
to the end of its last.

  python3 export/headline_sync.py video/reel-54.html deep.json --out video/reel-54-hs.html
"""
import argparse, json, re, sys

from karaoke import align, strip_tags

BOX_RE = re.compile(r'<span class="box">(.*?)</span>', re.S)


def tokenize_headline(inner_html):
    """Return (tokens, box_start, box_end) for one h2's innerHTML — tokens is the
    plain word list in document order, box_start/box_end mark the climax phrase's
    token range (equal when there is no box span)."""
    m = BOX_RE.search(inner_html)
    if not m:
        return strip_tags(inner_html).split(), 0, 0
    pre = strip_tags(inner_html[:m.start()]).split()
    box = strip_tags(m.group(1)).split()
    post = strip_tags(inner_html[m.end():]).split()
    return pre + box + post, len(pre), len(pre) + len(box)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("words", help="the --json written by voice_doctor --deep")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    src = open(a.html, encoding="utf-8").read()
    m = re.search(r"var CUES=(\[.*?\]);", src, re.S)
    if not m:
        sys.exit("no CUES array")
    cues = json.loads(m.group(1))
    heard = json.load(open(a.words))
    heard = heard["words"] if isinstance(heard, dict) else heard
    if not heard:
        sys.exit("no word timings in " + a.words)

    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', src, re.S)
    if len(h2s) != len(cues):
        sys.exit(f"{len(h2s)} headlines, {len(cues)} CUES lines — this script needs 1:1, "
                 "one headline per spoken line")

    scenes_out = []
    for li, (inner, c) in enumerate(zip(h2s, cues)):
        toks, bstart, bend = tokenize_headline(inner)
        if not toks:
            scenes_out.append([])
            continue
        window = [h for h in heard
                  if float(c[0]) - 0.6 <= float(h["at"]) <= float(c[1]) + 0.4]
        if not window:
            scenes_out.append([None] * len(toks))
            continue
        spans = align([(w, li) for w in toks], window)
        # One window per token, box words included — never collapsed into one. The
        # runtime (reel-54.html, reel-template-photo.html) now calls
        # MK.splitWordsSafe({explodeBoxes:true}), which gives every box WORD its own
        # entry in split.words, not one atomic entry for the whole phrase. A collapsed
        # window array here used to be one entry shorter per multi-word box than
        # split.words actually is at runtime — every word after the box then read a
        # window meant for a different word, which is why words were popping early,
        # late, or not at all. (bstart/bend are unused now except by tokenize_headline
        # itself; kept for clarity of what toks[bstart:bend] means.)
        scenes_out.append([list(s) if s else None for s in spans])

    # Line-anchored on purpose, not a dotall .*? across the whole file: this template's
    # own header prose mentions "WORD_WINDOWS" in passing, and a dotall match starting
    # there would swallow everything up to some unrelated "];" much further down.
    # Requiring the WHOLE line to be exactly the assignment can't be fooled that way.
    placeholder_re = re.compile(r"^\s*var WORD_WINDOWS=\[.*\];\s*$", re.M)
    payload = json.dumps(scenes_out)
    if placeholder_re.search(src):
        src = placeholder_re.sub("  var WORD_WINDOWS=" + payload + ";", src, count=1)
    else:
        src = src[:m.end()] + f"\n  var WORD_WINDOWS={payload};" + src[m.end():]

    open(a.out, "w", encoding="utf-8").write(src)
    print(f"{a.html} -> {a.out}")
    total = sum(len(s) for s in scenes_out)
    unmatched = sum(1 for s in scenes_out for w in s if w is None)
    print(f"  {len(scenes_out)} scenes, {total} headline words windowed"
          + (f" ({unmatched} unmatched)" if unmatched else ""))


if __name__ == "__main__":
    main()
