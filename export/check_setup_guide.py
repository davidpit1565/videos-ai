#!/usr/bin/env python3
"""Refuses to ship an episode with no real setup guide on its own /e/N page.

CLAUDE.md's standing rule: every episode ships with a full, exact setup path a
viewer can actually follow, on the episode's own site page — not just spoken
narration a viewer can't pause and copy from. That was a stated rule with
nothing enforcing it: produce.sh's captions-must-exist check blocked a missing
caption, but an episode could still ship with no studio/lib/articles.ts entry
at all, or one with a placeholder-thin steps list, and /e/N would render with
no "The exact clicks" section — a viewer coming from the video to solve the
exact problem it showed would find nothing to follow.

    python3 export/check_setup_guide.py <episode_number>
"""
import re, sys

MIN_STEPS = 3
MIN_STEP_CHARS = 20


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: check_setup_guide.py <episode_number>")
    ep = int(sys.argv[1])
    src = open("studio/lib/articles.ts").read()

    # Each entry in the ARTICLES array starts with a line like "    n: 22,".
    starts = [(m.start(), int(m.group(1))) for m in re.finditer(r"\n\s*n:\s*(\d+),", src)]
    starts.append((len(src), None))  # sentinel marking the last entry's end
    match = next(((s, e) for (s, n), (e, _) in zip(starts, starts[1:]) if n == ep), None)
    if match is None:
        sys.exit(f"NO SETUP GUIDE: studio/lib/articles.ts has no entry for episode {ep} at all — "
                 f"/e/{ep} would render with no \"The exact clicks\" section. Write one before shipping.")

    start, end = match
    block = src[start:end]
    steps_match = re.search(r"steps:\s*\[(.*?)\n\s*\],", block, re.S)
    if not steps_match:
        sys.exit(f"NO SETUP GUIDE: episode {ep}'s article has no steps: [] array — "
                 f"write the real, numbered, boring-path fix before shipping.")

    items = re.findall(r'"((?:[^"\\]|\\.)*)"', steps_match.group(1))
    real = [s for s in items if len(s.strip()) >= MIN_STEP_CHARS]
    if len(real) < MIN_STEPS:
        sys.exit(f"SETUP GUIDE TOO THIN: episode {ep} has only {len(real)} real step(s) "
                 f"(need >= {MIN_STEPS}, each >= {MIN_STEP_CHARS} chars) — a viewer landing on "
                 f"/e/{ep} needs an actual walkthrough, not a placeholder.")

    print(f"  ok — episode {ep} has {len(real)} real steps on /e/{ep}")


if __name__ == "__main__":
    main()
