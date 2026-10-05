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

Each `.box` word gets its own window too — box/non-box both go through the same
one-window-per-displayed-word path below (explodeBoxes:true at runtime means a
multi-word box is N separate DOM words, not one, so it needs N separate windows).

A hyphenated script word (e.g. "Fake-face") is one displayed DOM word but Whisper
often transcribes it as two separate tokens ("Fake", "face") with a real gap between
them. Matching the whole hyphenated string against two separate heard tokens fails,
so the aligner falls back to interpolating across the hole — which can stretch that
one word's window across part of the SILENCE before or after it too, not just its own
real spoken duration (caught on episode 54: "Fake-face" read 1.06s, versus its two
Whisper sub-words actually spanning 20.94-21.46, 0.52s — the window included part of
the pause after the previous word). Fixed by splitting on hyphens for alignment only:
each displayed word is aligned as its hyphen-separated parts (matching Whisper's own
granularity), then those parts collapse back into the one window the single displayed
word actually gets.

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
        # Split any hyphenated displayed word into its hyphen-parts for alignment —
        # Whisper transcribes "Fake-face" as two separate tokens, and align() can't
        # match one script token against two heard ones. owner[] tracks which
        # original displayed-word index each alignment unit belongs to.
        align_units, owner = [], []
        for ti, w in enumerate(toks):
            parts = w.split("-") if "-" in w else [w]
            for p in parts:
                align_units.append(p)
                owner.append(ti)
        spans = align([(w, li) for w in align_units], window)
        # One window per token, box words included — never collapsed into one. The
        # runtime (reel-54.html, reel-template-photo.html) now calls
        # MK.splitWordsSafe({explodeBoxes:true}), which gives every box WORD its own
        # entry in split.words, not one atomic entry for the whole phrase. A collapsed
        # window array here used to be one entry shorter per multi-word box than
        # split.words actually is at runtime — every word after the box then read a
        # window meant for a different word, which is why words were popping early,
        # late, or not at all. (bstart/bend are unused now except by tokenize_headline
        # itself; kept for clarity of what toks[bstart:bend] means.)
        #
        # Collapse hyphen-split spans back into one window per displayed word
        # (min start, max end across its parts) — this is a WITHIN-one-displayed-word
        # merge only, scoped by owner[], never across separate displayed words (that
        # was the bug this replaced: collapsing a whole multi-word box into one window).
        merged = [None] * len(toks)
        for ti, s in zip(owner, spans):
            if not s:
                continue
            if merged[ti] is None:
                merged[ti] = [s[0], s[1]]
            else:
                merged[ti][0] = min(merged[ti][0], s[0])
                merged[ti][1] = max(merged[ti][1], s[1])
        # A short function word's real spoken span can be under 0.1s — too brief for
        # the 0.09s color transition to read as a pop rather than a flicker. Floor
        # every window at MIN_HOLD, capped by the next word's own start so two words
        # are never both lit at once.
        MIN_HOLD = 0.22
        for ti in range(len(merged)):
            if merged[ti] is None:
                continue
            start, end = merged[ti]
            if end - start < MIN_HOLD:
                cap = merged[ti + 1][0] if ti + 1 < len(merged) and merged[ti + 1] else None
                new_end = start + MIN_HOLD
                merged[ti][1] = min(new_end, cap) if cap is not None else new_end
        scenes_out.append(merged)

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
