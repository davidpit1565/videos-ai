"""Which sounds does the cloned voice actually get wrong?

Not by ear and not by opinion: every word is generated, transcribed back with Whisper,
and compared to what it was supposed to be. What the transcriber heard instead is the
evidence — if "harder" comes back as "hodder", the D is the problem, and if it comes back
as "hada", the R is. Sounds that fail get respelling candidates and are re-tested, so the
fix is proven rather than assumed.

    python3 audio/phoneme_audit.py                    # audit the stored profile
    python3 audio/phoneme_audit.py --words harder,think --tries 6
"""
import argparse, json, os, subprocess, sys, tempfile, warnings
warnings.filterwarnings("ignore")

REF = "audio/voice/profile/reference.wav"
PRON = "audio/voice/profile/pronunciation.json"

# word, carrier sentence, the sound under test. Carrier sentences matter: a word alone is
# harder for any transcriber than the same word in a phrase, and the videos ship phrases.
CASES = [
    ("harder",  "It makes ChatGPT think harder, not better.",        "post-vocalic R + flapped D"),
    ("think",   "Nobody told it how to think.",                      "voiceless TH"),
    ("that",    "That is the whole job.",                            "voiced TH"),
    ("three",   "Three things break first.",                         "THR cluster"),
    ("really",  "It really does work.",                              "initial R"),
    ("answers", "Your ChatGPT gives you generic answers.",           "NS cluster"),
    ("world",   "The world runs on these.",                          "dark L + RLD"),
    ("little",  "One little block of text.",                         "flapped T"),
    ("water",   "It is like water through a pipe.",                  "flapped T"),
    ("video",   "This video shows the setup.",                       "V versus W"),
    ("worse",   "It gets worse before it works.",                    "W + RS"),
    ("visible", "Nothing is visible until you save.",                "V + B"),
    ("saves",   "Saves per view is the signal.",                     "final Z"),
    ("sixth",   "The sixth thing agents cannot do.",                 "KSTH cluster"),
    ("strong",  "A strong hook earns the view.",                     "STR cluster"),
    ("agent",   "An agent acts on its own.",                         "soft G"),
    ("engine",  "You are my Universal AI Engine.",                   "NJ"),
    ("settings","Open Settings and paste it in.",                    "double T + NGS"),
    ("bit",     "Wait a bit and check again.",                       "short I"),
    ("beat",    "It cannot beat a tested setup.",                    "long E"),
    ("full",    "The full text is in the caption.",                  "OO + dark L"),
    ("fool",    "It will fool you once.",                            "long OO"),
    ("about",   "Ask about the risk.",                               "OW diphthong"),
    ("first",   "Your first agent should be reversible.",            "IR + ST"),
    ("hour",    "It took an hour to break.",                         "silent H + OW"),
    ("results", "The results are in the caption.",                   "LTS cluster"),
    ("model",   "This is not a new model.",                          "D + dark L"),
    ("reasoning","It picks its own reasoning.",                      "Z + NG"),
    ("clearly", "State it clearly, then decide.",                    "KL + R"),
    ("prompt",  "Comment prompt and it is yours.",                   "PR + MPT"),
]

NUMERALS = {"1": "one", "2": "two", "3": "three", "4": "four", "5": "five",
            "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten"}

def norm(s):
    out = []
    for w in s.lower().split():
        w = "".join(c for c in w if c.isalnum())
        out.append(NUMERALS.get(w, w))
    return " ".join(out).strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--words", help="comma-separated subset to test")
    ap.add_argument("--tries", type=int, default=3, help="respelling attempts per failure")
    ap.add_argument("--exaggeration", type=float, default=0.40)
    ap.add_argument("--cfg", type=float, default=0.60)
    ap.add_argument("--ref", default=REF)
    ap.add_argument("--lang", default=None, help="language id for the multilingual model")
    ap.add_argument("--out", default="audio/voice/phoneme-report.json")
    a = ap.parse_args()

    cases = CASES
    if a.words:
        want = {w.strip().lower() for w in a.words.split(",")}
        cases = [c for c in CASES if c[0] in want]

    import librosa, torch, torchaudio
    import sys as _sys
    _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from line_doctor import tail_energy
    torch.set_num_threads(os.cpu_count() or 4)
    if a.lang:
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS as TTS
        m = TTS.from_pretrained(device="cpu")
    else:
        from chatterbox.tts import ChatterboxTTS as TTS
        m = TTS.from_pretrained(device="cpu")
    from faster_whisper import WhisperModel
    asr = WhisperModel("small", device="cpu", compute_type="int8")
    tmp = tempfile.mkdtemp()

    def say(text, seed, target=None):
        torch.manual_seed(seed)
        kw = dict(audio_prompt_path=a.ref, exaggeration=a.exaggeration,
                  cfg_weight=a.cfg, temperature=0.75)
        if a.lang:
            kw["language_id"] = a.lang
        wav = m.generate(text, **kw)
        p = os.path.join(tmp, "w.wav")
        torchaudio.save(p, wav, m.sr)
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",p,
                        "-ar","16000","-ac","1",p+"16.wav"], check=True)
        segs, _ = asr.transcribe(p + "16.wav", language=a.lang or "en", word_timestamps=True)
        segs = list(segs)
        heard = " ".join(s.text for s in segs).strip()
        tail = None
        if target:
            words = [(w.word.strip(" ,.!?—").lower(), w.start, w.end)
                     for s in segs for w in (s.words or [])]
            hit = next((w for w in words if w[0] == target.lower()), None)
            if hit:
                y, sr = librosa.load(p, sr=None, mono=True)
                tail = tail_energy(y, sr, hit[1], hit[2])
                if tail is not None:
                    tail = round(float(tail), 1)
        return heard, tail

    # respelling candidates, tried in order until the transcriber hears the real word
    RESPELL = {
        "harder": ["harderr", "har-der", "hard-er", "hahrder"],
        "think":  ["thinnk", "th-ink"],
        "three":  ["thuree", "th-ree"],
        "world":  ["wurld", "wor-ld"],
        "worse":  ["wurse", "worss"],
        "video":  ["vidio", "vee-dio"],
        "sixth":  ["siksth", "six-th"],
        "first":  ["furst", "fir-st"],
        "hour":   ["our", "ah-our"],
        "little": ["littel", "lit-tle"],
        "water":  ["wauter", "wah-ter"],
    }

    # a tail this weak is what he hears as a swallowed letter; measured on his chosen settings
    WEAK = -18.0

    rows = []
    for word, sentence, sound in cases:
        heard, tail = say(sentence, 7, word)
        ok = word.lower() in norm(heard).split()
        soft = ok and tail is not None and tail < WEAK
        fix = None
        if not ok or soft:
            for cand in RESPELL.get(word, [])[: a.tries]:
                h2, t2 = say(sentence.replace(word, cand), 7, word)
                heard_ok = word.lower() in norm(h2).split()
                # only accept a respelling that keeps the word AND lands the ending harder
                if heard_ok and (not ok or (t2 is not None and tail is not None and t2 > tail + 1.0)):
                    fix, heard, tail, ok = cand, h2, t2, True
                    soft = t2 is not None and t2 < WEAK
                    break
        rows.append({"word": word, "sound": sound, "ok": ok, "soft": bool(soft),
                     "tail_db": tail, "heard": heard, "respell": fix})
        mark = "FAIL" if not ok else ("soft" if soft else ("fix " if fix else "ok  "))
        print(f"{mark} {word:10} {sound:26} tail {str(tail):>6}  heard: {heard[:46]}", flush=True)

    bad = [r for r in rows if not r["ok"]]
    soft = [r for r in rows if r.get("soft")]
    fixed = [r for r in rows if r["respell"]]
    tails = [r["tail_db"] for r in rows if r["tail_db"] is not None]
    print(f"\n{len(rows)-len(bad)}/{len(rows)} intelligible · {len(soft)} still soft at the end · "
          f"{len(fixed)} improved by a respelling", flush=True)
    if tails:
        import statistics
        print(f"word-final energy: median {statistics.median(tails):.1f} dB, "
              f"worst {min(tails):.1f} dB", flush=True)
    for r in sorted(soft, key=lambda x: x["tail_db"] or 0)[:10]:
        print(f"  soft: {r['word']:10} {r['tail_db']} dB — {r['sound']}", flush=True)
    json.dump(rows, open(a.out, "w"), ensure_ascii=False, indent=1)

    if fixed:
        # fold the working respellings into the stored profile so every future line uses them
        pron = json.load(open(PRON, encoding="utf-8")) if os.path.exists(PRON) else {"words": {}, "phrases": {}}
        for r in fixed:
            pron.setdefault("words", {})[r["word"]] = r["respell"]
            pron["words"][r["word"].capitalize()] = r["respell"].capitalize()
        json.dump(pron, open(PRON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"wrote {len(fixed)} respellings into {PRON}", flush=True)

if __name__ == "__main__":
    main()
