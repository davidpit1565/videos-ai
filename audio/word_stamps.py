"""Word timestamps for any wav, in the shape audio/plosives.py wants. Exists so a
measurement can be run on a recording that has no build or cue file behind it —
his own raw reference, a Flemish take, a competitor's clip."""
import sys, json, argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("--out", required=True)
    ap.add_argument("--lang", default="en")
    a = ap.parse_args()
    from faster_whisper import WhisperModel
    m = WhisperModel("medium", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(a.wav, language=a.lang, word_timestamps=True,
                           vad_filter=False)
    words = []
    for s in segs:
        for w in (s.words or []):
            words.append(dict(word=w.word.strip(), at=round(w.start, 3),
                              dur=round(w.end - w.start, 3)))
    json.dump({"words": words}, open(a.out, "w"), ensure_ascii=False, indent=1)
    print(f"{a.wav}: {len(words)} words -> {a.out}")
    print("  " + " ".join(w["word"] for w in words[:22]))

if __name__ == "__main__":
    main()
