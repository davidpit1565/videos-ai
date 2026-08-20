#!/usr/bin/env python3
"""Turn the full-sentence subtitle into a word-by-word caption, timed to the voice.

The measured convention in short-form is a burned-in animated caption showing two to
four words at a time with the current word highlighted — 80.2% of 13.5M clips in
OpusClip's corpus carry captions and 78.6% animate them, against 1.6% static. Our
build was printing the whole sentence at the bottom of frame, which also repeated the
scene's own headline word for word.

The timings come from the narration itself: Whisper's word stamps, aligned back onto
the script so the text shown is what was written, not what the transcriber heard
("ChatGPT" comes back as "chat" + "GPT"). Words the aligner cannot match keep their
share of the line's remaining time, so a caption can never run ahead of the voice.

  python3 export/karaoke.py video/reel-01-v3.html deep.json --out video/reel-01-kar.html
"""
import argparse, difflib, json, re, sys

NORM = re.compile(r"[^a-z0-9]+")


NUMS = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
        "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10"}

def norm(w):
    # the script writes "3", the transcriber writes "three" (or the reverse); the
    # aligner has to treat them as the same word or the step lines never match up
    t = NORM.sub("", w.lower())
    return NUMS.get(t, t)


def strip_tags(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def align(script, heard):
    """Give every script word a start and end. Matched words take the transcriber's
    stamps; a run of unmatched script words splits the time between its neighbours."""
    sm = difflib.SequenceMatcher(None, [norm(w) for w, _ in script],
                                 [norm(h["word"]) for h in heard])
    out = [None] * len(script)
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            h = heard[b + k]
            out[a + k] = (float(h["at"]), round(float(h["at"]) + float(h["dur"]), 3))
    # fill the holes, keeping the order strictly increasing
    i = 0
    while i < len(out):
        if out[i] is not None:
            i += 1
            continue
        j = i
        while j < len(out) and out[j] is None:
            j += 1
        lo = out[i - 1][1] if i else (out[j][0] if j < len(out) else 0.0)
        hi = out[j][0] if j < len(out) else lo + 0.3 * (j - i)
        step = (hi - lo) / max(1, j - i)
        for k in range(i, j):
            out[k] = (round(lo + step * (k - i), 3), round(lo + step * (k - i + 1), 3))
        i = j
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("words", help="the --json written by voice_doctor --deep")
    ap.add_argument("--out", required=True)
    ap.add_argument("--chunk", type=int, default=3, help="words on screen at once")
    ap.add_argument("--words-cues", help="the cue file the word stamps were measured "
                    "against; word times are shifted per line onto the build's cues, "
                    "which is exact because regap moves a line without stretching it")
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

    shifts = None
    if a.words_cues:
        old = json.load(open(a.words_cues))
        old = old if isinstance(old, list) else old["cues"]
        if len(old) != len(cues):
            sys.exit(f"{len(old)} cues in the word reference, {len(cues)} in the build")
        # each line's audio is untouched by a re-gap, so one rigid shift per line is exact
        shifts = [(float(o["start"]), float(o["end"]), float(c[0]) - float(o["start"]))
                  for o, c in zip(old, cues)]
        moved = []
        for h in heard:
            t0 = float(h["at"])
            d = min(shifts, key=lambda s: 0 if s[0] <= t0 <= s[1]
                    else min(abs(t0 - s[0]), abs(t0 - s[1])))
            moved.append(dict(h, at=round(t0 + d[2], 3)))
        heard = moved
        print(f"  word stamps shifted per line: "
              f"{min(s[2] for s in shifts):+.2f}s to {max(s[2] for s in shifts):+.2f}s")

    words, chunk_id = [], 0
    for li, c in enumerate(cues):
        line = strip_tags(c[2])
        # A lone em dash is dropped by the normaliser, so the word before it stops
        # looking like a phrase end — which is how "ChatGPT reasons — not" became the
        # single chunk "CHATGPT REASONS NOT". The dash is folded onto its neighbour.
        raw = line.split()
        toks = []
        for j, w in enumerate(raw):
            if not norm(w):
                if toks:
                    toks[-1] = (toks[-1][0] + w, toks[-1][1], True)
                continue
            toks.append((w, li, bool(re.search(r"[,.;:!?]$", w))))
        if not toks:
            continue
        # a generous window: the transcriber's first word can start before the cue,
        # and excluding it shifts the whole line's alignment by one word
        window = [h for h in heard
                  if float(c[0]) - 0.6 <= float(h["at"]) <= float(c[1]) + 0.4]
        if not window:
            continue
        spans = align([(w, li) for w, li, _ in toks], window)
        # a caption may never appear before the voice: the transcriber's first word can
        # start ahead of the cue, and the wide search window lets that leak through
        if spans:
            s0 = max(float(c[0]), spans[0][0])
            spans[0] = (s0, max(spans[0][1], s0 + 0.12))
        held = 0
        for k, ((w, _, _), (s, e)) in enumerate(zip(toks, spans)):
            # A fixed three-word window cuts across phrases: "how ChatGPT reasons — not
            # how often it's right" came out as "CHATGPT REASONS NOT", which reads as a
            # different sentence. A chunk ends at punctuation or at the word limit,
            # whichever comes first.
            if k and (held >= a.chunk or toks[k-1][2]):
                chunk_id += 1
                held = 0
            held += 1
            e = max(e, s + 0.12)          # a zero-length span would never light up
            words.append([round(s, 2), round(e, 2), w.rstrip("—–-"), chunk_id])
        chunk_id += 1

    # A chunk is only read if it is on screen long enough to be read. "Five" held the
    # frame for 0.12s and the chunk after it started at the same timestamp, so it was
    # overwritten on the same frame and the step number was never visible at all. The
    # four other step numbers ran 0.19-0.31s, under the 0.45s this project already
    # treats as a glitch elsewhere. Rather than special-case the numbers, merge any
    # chunk that cannot be read into the one that follows it.
    MIN_ON = 0.42
    merged, i = 0, 0
    while i < len(words):
        cid = words[i][3]
        run = [j for j in range(i, len(words)) if words[j][3] == cid]
        nxt = run[-1] + 1
        if nxt < len(words):
            on = words[nxt][0] - words[run[0]][0]      # until the next chunk takes over
            if on < MIN_ON:
                tgt = words[nxt][3]
                for j in run:
                    words[j][3] = tgt
                merged += 1
                continue                               # re-test the widened chunk
        i = run[-1] + 1
    if merged:
        ids = sorted({w[3] for w in words})
        remap = {c: n for n, c in enumerate(ids)}
        for w in words:
            w[3] = remap[w[3]]
        print(f"  merged {merged} chunk(s) that would have been on screen under "
              f"{MIN_ON:.2f}s")
        chunk_id = len(ids)

    rows = ",\n    ".join(f'[{s},{e},{json.dumps(w, ensure_ascii=False)},{c}]'
                          for s, e, w, c in words)
    src = src[:m.end()] + f"\n  var WORDS=[\n    {rows}\n  ];" + src[m.end():]

    # the caption is now a chunk of words with the spoken one lit, and it clears in the
    # gaps instead of holding a finished sentence on screen
    src = src.replace("""    var txt=''; for(i=0;i<CUES.length;i++) if(t>=CUES[i][0]&&t<=CUES[i][1]){txt=CUES[i][2];break;}
    subs.innerHTML=txt;""",
"""    /* The chunk on screen is the one the last spoken word belongs to, and it holds
       until the next chunk's first word — otherwise the caption blanks for a third of
       a second between chunks while the voice is still going. It clears only between
       lines, where the silence is real. */
    /* The window has to close the ordinary gaps. The scene's own headline is written to
       disappear before the next one arrives, so a caption that blanks in a 0.42s gap
       leaves the whole screen textless — measured at eleven places, 0.13s each. Reaching
       0.32s back and 0.15s forward covers those, and the only remaining blanks fall
       inside the 0.80s section gaps, where the colour card fills the frame anyway. After
       the last line the caption holds to the end rather than leaving a blank tail. */
    var inLine=false;
    for(i=0;i<CUES.length;i++) if(t>=CUES[i][0]-0.32&&t<=CUES[i][1]+0.15){inLine=true;break;}
    if(t>CUES[CUES.length-1][1]) inLine=true;
    var here=-1, cur=-1;
    /* the lit word is the last one that started, not only the one still sounding:
       Whisper's word boundaries are tight, so gating on the word's own end left the
       highlight off for 13.4s of the reel */
    for(i=0;i<WORDS.length;i++) if(WORDS[i][0]<=t+0.08){ here=WORDS[i][3]; cur=i; }
    var txt='';
    if(inLine&&here>=0){
      for(i=0;i<WORDS.length;i++) if(WORDS[i][3]===here)
        txt+=(i===cur?'<b class="on">':'<b>')+WORDS[i][2]+'</b> ';
    }
    subs.innerHTML=txt;""")
    open(a.out, "w", encoding="utf-8").write(src)
    print(f"{a.html} -> {a.out}")
    print(f"  {len(words)} words in {chunk_id} chunks of up to {a.chunk}")
    print(f"  first {words[0][:3]}  last {words[-1][:3]}")


if __name__ == "__main__":
    main()
