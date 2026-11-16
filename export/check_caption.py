#!/usr/bin/env python3
"""Caption check before a reel ships (own code, small, no external dependency).
  python3 export/check_caption.py <N>        reads channel/episode-N-caption.txt and -youtube.txt
Checks: Instagram limit 2,200 characters (episode 88 failed at 2,251); YouTube text has no < or >;
what the feed shows before '... more' (about the first 125 characters, a judgement of the display, not a fixed number);
em dashes and a few words that read as machine-written (a prompt to rewrite, not a ban)."""
import re, sys
n = sys.argv[1]
cap = open(f"channel/episode-{n}-caption.txt").read()
bad = False
if len(cap) > 2200:
    print(f"FAIL caption {len(cap)} characters, Instagram refuses over 2,200"); bad = True
else:
    print(f"ok   caption {len(cap)} / 2,200 characters")
try:
    yt = open(f"channel/episode-{n}-youtube.txt").read()
    if re.search(r"[<>]", yt):
        print("FAIL youtube text contains < or >"); bad = True
    else:
        print("ok   youtube text has no < or >")
except FileNotFoundError:
    print("WARN no youtube text file")
first = cap.strip().replace("\n", " ")[:125]
print("what the feed shows before '... more' (about 125 characters):\n   " + first)
if "—" in cap: print("WARN em dash in caption (reads machine-written): rewrite")
words = ["delve", "unlock", "game-changer", "revolutionize", "seamless", "leverage", "elevate", "tapestry", "in today's fast-paced"]
hit = [w for w in words if w in cap.lower()]
if hit: print("WARN words that read machine-written:", ", ".join(hit))
sys.exit(1 if bad else 0)
