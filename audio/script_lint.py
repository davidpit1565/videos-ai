"""Check a script before it is spoken, not after.

The measured pattern in his voice: the *end* of a word arrives soft. Words that finish on
an unstressed syllable — an R after a vowel, a dark L, "-le", "-ble", "-ent" — and words
with a flapped T between vowels come out with almost no energy in the tail. Measured on his
own settings: worse −31.4 dB, visible −41.6, harder −20.9, little −23.2, against a −18
threshold where a listener stops hearing the consonant.

Fighting the model does not work; respellings were tried and measured and did not help. So
the fix belongs in the writing. This flags the words and offers a word that lands, before
anything is generated.

    python3 audio/script_lint.py --cues video/reel-02.html
    python3 audio/script_lint.py --text "It makes ChatGPT think harder, not be right more often."
"""
import argparse, json, os, re, sys

# alternatives that carry the same meaning and end on a stressed or plosive sound
SWAP = {
    "harder": ["more", "deeper", "further"],
    "worse": ["bad", "a mess", "unusable"],
    "better": ["good", "right", "sharp"],
    "faster": ["quick", "fast"],
    "smarter": ["sharp", "clever"],
    "cheaper": ["cheap", "low cost"],
    "later": ["after that", "next"],
    "little": ["small", "one", "short"],
    "water": ["a pipe", "liquid"],
    "visible": ["on screen", "you can see it", "in plain sight"],
    "possible": ["it can", "you can"],
    "terrible": ["bad", "broken"],
    "reasonable": ["fair", "sane"],
    "world": ["everyone", "the market", "people"],
    "really": ["actually", "in fact", "genuinely"],
    "usually": ["most times", "as a rule"],
    "finally": ["in the end", "at last"],
    "answers": ["a reply", "an answer"],
    "results": ["the result", "the outcome"],
    "settings": ["the setting", "the panel"],
    "computer": ["laptop", "machine"],
    "remember": ["keep", "hold"],
    "consider": ["weigh", "think about"],
    "another": ["one more", "a second"],
    "toggle": ["the switch", "turn it on"],
    "month": ["a month"], "worth": ["value"], "truth": ["what is true"],
    "north": ["up"], "return": ["send back", "give back"],
    "learn": ["pick up"], "turn": ["switch"],
    "together": ["as one", "in one place"],
}

RULES = [
    # (name, pattern, why)
    ("unstressed -ER", re.compile(r"^[a-z]{3,}er$"), "the R after a vowel drops"),
    ("-LE / -BLE", re.compile(r"^[a-z]{3,}[bpdtgkfv]?le$"), "the final syllable disappears"),
    ("-IBLE / -ABLE", re.compile(r"^[a-z]{3,}[ia]ble$"), "two unstressed syllables, both soft"),
    ("-LY", re.compile(r"^[a-z]{4,}ly$"), "the L is dark and the Y trails off"),
    ("R + cluster", re.compile(r"^[a-z]{2,}(rld|rs|rse|rce|rst|rth|rn)e?$"),
     "R plus a cluster, all at the end"),
    ("flapped T", re.compile(r"^[a-z]*[aeiou]t(er|le|ing|ed)$"), "the T turns into a tap and vanishes"),
    ("-ENT / -ANT", re.compile(r"^[a-z]{4,}[ea]nt$"), "the final T is unreleased"),
    ("-TH", re.compile(r"^[a-z]{3,}th$"), "the TH at the end goes breathy and disappears"),
]

def cues_from_html(path):
    s = open(path, encoding="utf-8").read()
    m = re.search(r"var CUES=(\[.*?\]);", s, re.S)
    if not m:
        sys.exit(f"no CUES array in {path}")
    lines = re.findall(r'"((?:[^"\\]|\\.)*)"\s*\]', m.group(1))
    return [re.sub(r"<[^>]+>", "", l) for l in lines]

BRAND = re.compile(r"actually\s+works", re.I)

def check(line):
    hits = []
    for raw in line.split():
        w = re.sub(r"[^A-Za-z'-]", "", raw).lower()
        if len(w) < 3:
            continue
        for name, pat, why in RULES:
            if pat.match(w):
                hits.append((w, name, why, SWAP.get(w, [])))
                break
    return hits

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cues", help="a video build to read the narration from")
    ap.add_argument("--text", help="a single line or paragraph")
    ap.add_argument("--file", help="a plain text file, one line per line")
    a = ap.parse_args()

    if a.cues:
        lines = cues_from_html(a.cues)
    elif a.file:
        lines = [l.strip() for l in open(a.file, encoding="utf-8") if l.strip()]
    elif a.text:
        lines = [a.text]
    else:
        sys.exit("give --cues, --file or --text")

    total = 0
    for i, line in enumerate(lines, 1):
        hits = check(line)
        if not hits:
            continue
        total += len(hits)
        print(f"\nline {i}: {line}")
        for w, name, why, alts in hits:
            fix = ("  →  try: " + ", ".join(alts)) if alts else "  →  no stock alternative; rewrite the phrase"
            print(f"  {w:12} {name:14} {why}{fix}")
    brand = [i for i, l in enumerate(lines, 1) if BRAND.search(l)]
    if brand:
        print(f"\nthe brand phrase appears on line(s) {brand}. \"actually\" trips the -LY rule and")
        print("cannot be swapped — it is the name. Lock that line once with line_doctor and reuse")
        print("the approved take in every outro instead of regenerating it each episode.")
    print(f"\n{total} risky word(s) across {len(lines)} line(s).")
    if total:
        print("These are not mispronunciations — every one of them transcribes correctly. They are")
        print("endings that arrive too soft to hear. Swapping the word costs nothing; fighting the")
        print("model with respellings was measured and did not work.")

if __name__ == "__main__":
    main()
