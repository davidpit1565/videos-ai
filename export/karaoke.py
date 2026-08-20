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


def norm(w):
    return NORM.sub("", w.lower())


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

    words, chunk_id = [], 0
    for li, c in enumerate(cues):
        line = strip_tags(c[2])
        toks = [(w, li) for w in line.split() if norm(w)]
        if not toks:
            continue
        # a generous window: the transcriber's first word can start before the cue,
        # and excluding it shifts the whole line's alignment by one word
        window = [h for h in heard
                  if float(c[0]) - 0.6 <= float(h["at"]) <= float(c[1]) + 0.4]
        if not window:
            continue
        spans = align(toks, window)
        for k, ((w, _), (s, e)) in enumerate(zip(toks, spans)):
            if k and k % a.chunk == 0:
                chunk_id += 1
            e = max(e, s + 0.12)          # a zero-length span would never light up
            words.append([round(s, 2), round(e, 2), w, chunk_id])
        chunk_id += 1

    rows = ",\n    ".join(f'[{s},{e},{json.dumps(w, ensure_ascii=False)},{c}]'
                          for s, e, w, c in words)
    src = src[:m.end()] + f"\n  var WORDS=[\n    {rows}\n  ];" + src[m.end():]

    # the caption is now a chunk of words with the spoken one lit, and it clears in the
    # gaps instead of holding a finished sentence on screen
    src = src.replace("""    var txt=''; for(i=0;i<CUES.length;i++) if(t>=CUES[i][0]&&t<=CUES[i][1]){txt=CUES[i][2];break;}
    subs.innerHTML=txt;""",
"""    var here=-1, cur=-1;
    for(i=0;i<WORDS.length;i++){
      if(t>=WORDS[i][0]-0.08&&t<WORDS[i][1]+0.12){cur=i;here=WORDS[i][3];break;}
      if(WORDS[i][0]>t) break;
      here=WORDS[i][3];
    }
    var gap=true;
    for(i=0;i<WORDS.length;i++) if(WORDS[i][3]===here&&t>=WORDS[i][0]-0.25&&t<=WORDS[i][1]+0.30){gap=false;break;}
    var txt='';
    if(!gap&&here>=0){
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
