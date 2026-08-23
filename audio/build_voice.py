#!/usr/bin/env python3
"""Speak any script in David's voice, from the stored profile.

The profile is a short reference recording; the model clones the timbre from it,
so new episodes need no new recording. Output is polished with the same chain
every time, then laid out on a timeline with controlled gaps.

  python3 build_voice.py --cues video/reel-01-v3.html --out audio/voice/ep02.wav
  python3 build_voice.py --lines script.txt --out out.wav
"""
import argparse, json, os, re, subprocess, sys, tempfile, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import burst

REF   = "audio/voice/profile/reference.wav"
PRON  = "audio/voice/profile/pronunciation.json"
TONE  = "audio/voice/profile/room-tone.wav"
BREATH= "audio/voice/profile/breaths.wav"
SR_MIX = 48000
GAP, LONG = 0.42, 0.85          # pause after a line, and after a section
SECTION_END = {4, 8, 13, 15}

def cue_times(path):
    src = open(path, encoding="utf-8").read()
    m = re.search(r"var CUES=(\[.*?\]);", src, re.S)
    return [(float(c[0]), float(c[1])) for c in json.loads(m.group(1))]

def stretch(src, dst, factor):
    """rubberband keeps pitch and formants; asetrate would chipmunk the voice."""
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",src,
                    "-af",f"rubberband=tempo={factor:.4f}:pitchq=quality",dst],check=True)

def cues_from_html(path):
    src = open(path, encoding="utf-8").read()
    m = re.search(r"var CUES=(\[.*?\]);", src, re.S)
    if not m:
        sys.exit("no CUES array in " + path)
    out = []
    for c in json.loads(m.group(1)):
        t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c[2])).strip()
        if t:
            out.append(t)
    return out

def load_wav(path):
    if not os.path.exists(path):
        return None
    with wave.open(path) as w:
        if w.getframerate() != SR_MIX:
            return None
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768

def breath_bank():
    """His own intakes of air, lifted from the gaps in the original recording.
    Generated speech is unnaturally clean; a real breath before a line is the
    cheapest thing that makes it sound recorded rather than produced."""
    a = load_wav(BREATH)
    if a is None:
        return []
    fr = int(0.02 * SR_MIX)
    n = len(a) // fr
    e = np.array([np.sqrt((a[i*fr:(i+1)*fr]**2).mean()) for i in range(n)])
    on = e > (e.max() * 0.12)
    out, run = [], []
    for i, v in enumerate(on):
        if v: run.append(i)
        elif run:
            if len(run) >= 4: out.append(a[run[0]*fr:(run[-1]+1)*fr].copy())
            run = []
    if len(run) >= 4: out.append(a[run[0]*fr:(run[-1]+1)*fr].copy())
    return out

def bed(track, tone, level_db=-42):
    """A whisper of his real room under everything. Silence between lines is the
    tell that gives synthetic speech away — rooms are never actually silent."""
    if tone is None or len(tone) < SR_MIX:
        return track
    reps = int(np.ceil(len(track) / len(tone)))
    t = np.tile(tone, reps)[:len(track)]
    t = t / (t.std() + 1e-9) * (10 ** (level_db / 20))
    return track + t

def load_pron():
    if not os.path.exists(PRON):
        return {}, {}
    d = json.load(open(PRON, encoding="utf-8"))
    return d.get("phrases", {}), d.get("words", {})

def respell(text, phrases, words):
    """What the model speaks, not what the viewer reads. A word the model
    mangles gets respelled here; the caption keeps its real spelling."""
    out = text
    for src, dst in phrases.items():                  # phrases first — more specific
        out = re.sub(re.escape(src), dst, out, flags=re.I)
    for src, dst in words.items():
        out = re.sub(r"\b" + re.escape(src) + r"\b", dst, out, flags=re.I)
    return out

def syllables(text):
    """Rough vowel-group count — enough to spot a line that is too dense to be clear."""
    return max(1, len(re.findall(r"[aeiouy]+", text.lower())))

NUMS = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
        "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10"}

def _watched_in(text, watch):
    """Which watched words this line actually speaks — the script writes "3", not
    "three", so the digit form has to be checked too or a digit line never matches."""
    t = text.lower()
    out = []
    for w in watch:
        digit = NUMS.get(w)
        pat = r"\b(" + w + (r"|" + re.escape(digit) if digit else "") + r")\b"
        if re.search(pat, t):
            out.append(w)
    return out

def _norm(t):
    """Compare meaning, not spelling. The transcriber writes "chat GPT" and drops
    possessives, and neither is a mispronunciation."""
    t = t.lower().replace("\u2019", "'")
    t = re.sub(r"chat\s*gpt", "chatgpt", t)
    t = re.sub(r"([a-z])'s\b", r"\1s", t)
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    # the script writes "3", the transcriber writes "three" (or the
    # reverse). They are the same word for comparison purposes.
    return [NUMS.get(w, w) for w in t.split() if w]

def wer(said, want):
    """Word error rate between what the model produced and what it was asked to say."""
    a, b = _norm(said), _norm(want)
    if not b: return 0.0
    d = np.zeros((len(a)+1, len(b)+1), dtype=np.int32)
    d[:,0] = np.arange(len(a)+1); d[0,:] = np.arange(len(b)+1)
    for i in range(1, len(a)+1):
        for j in range(1, len(b)+1):
            d[i,j] = min(d[i-1,j]+1, d[i,j-1]+1, d[i-1,j-1]+(a[i-1] != b[j-1]))
    return d[len(a), len(b)] / len(b)

def dup_tail(words, want):
    """Chatterbox sometimes says the end of a line twice. Line 13 of episode 01 came
    out as "...same model, new method. New method." — he heard it immediately.

    The transcript check scored it 0.25 and accepted it as "best available", because
    word error rate treats a duplicated phrase as a handful of insertions. A repetition
    is not a mispronunciation, it is the wrong content, so it gets its own test.

    Returns the time the repeat starts, so the take can be cut instead of thrown away.
    """
    h = [(n[0], w.start) for w in words for n in [_norm(w.word)] if n]
    t = _norm(want)
    if len(h) < len(t) + 2 or len(t) < 2:
        return None
    # the longest tail of the target that is spoken twice in a row at the end
    for k in range(min(len(t), (len(h)) // 2), 1, -1):
        a1 = [x[0] for x in h[-k:]]
        a2 = [x[0] for x in h[-2 * k:-k]]
        if a1 == a2 == t[-k:]:
            return h[-k][1]
    return None


def polish(src, dst):
    """Same chain every episode, so every video sounds like the same person.

    Measured, not guessed: the voice encoder that does the cloning scores each chain
    against his real recording. The heavy presence and clarity boosts here were tuned
    for the second take, where he sat further off the mic and lost 25 dB of consonant
    energy. On the first take — the one he says sounds like him — those same boosts cost
    identity for nothing, because that recording is already bright. What is left is a
    rumble cut, a nudge in the S band, a light de-esser and gentle levelling."""
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", src,
        "-af", ("highpass=f=75,"
                "equalizer=f=240:t=q:w=1.2:g=-1.5,"
                "equalizer=f=4200:t=q:w=1.4:g=1.5,"
                "equalizer=f=7200:t=q:w=1.6:g=2,"        # this band is the S
                "deesser=i=0.14:m=0.5:f=0.35,"
                "acompressor=threshold=-20dB:ratio=2.2:attack=10:release=200:makeup=1.5,"
                "alimiter=limit=0.95,"
                "loudnorm=I=-17:TP=-1.5:LRA=10"),
        "-ar", str(SR_MIX), "-ac", "1", dst,
    ], check=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cues", help="a video build to read the caption cues from")
    ap.add_argument("--fit", help="same build, but place each line in its exact cue slot,\n                          time-stretching within +/-12%% so the cut does not move")
    ap.add_argument("--lines", help="a plain text file, one spoken line per line")
    ap.add_argument("--out", required=True)
    ap.add_argument("--exaggeration", type=float, default=0.50,
                    help="0.3 flat · 0.5 conversational · 0.7 animated")
    ap.add_argument("--cfg", type=float, default=0.30,
                    help="lower = looser, more natural rhythm")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--line-seeds", default="",
                    help='per-line seed overrides, "7:41,12:8". CLAUDE.md describes a '
                         'take being locked per line and nothing implemented it — the '
                         'whole build had one seed, so fixing one bad word meant '
                         'rerolling every other line with it.')
    ap.add_argument("--retries", type=int, default=3,
                    help="regenerate a line this many times if it is misheard")
    ap.add_argument("--min-rate", type=float, default=4.6,
                    help="syllables a second below which a line is dragging. Measured on "
                         "nineteen reels, the accounts we are chasing run 231-313 words a "
                         "minute (about 5.4-7.3 syl/s) where ours ran 150 (3.5).")
    ap.add_argument("--max-speedup", type=float, default=1.20,
                    help="most a dragging line may be sped up; pitch is preserved")
    ap.add_argument("--max-rate", type=float, default=6.5,
                    help="syllables per second above which a line is judged too dense")
    ap.add_argument("--gap", type=float, default=GAP,
                    help="silence after every line; he asked for more room to breathe")
    ap.add_argument("--long", type=float, default=LONG,
                    help="silence after a section end")
    ap.add_argument("--room-db", type=float, default=-55,
                    help="level of the room-tone bed; -55 matches his real room")
    ap.add_argument("--dry", action="store_true",
                    help="skip breaths and room tone (clinical, for debugging)")
    ap.add_argument("--prosody-rolls", type=int, default=3,
                    help="extra takes allowed to make a statement's pitch land")
    ap.add_argument("--fall", type=float, default=-1.5,
                    help="semitones a statement ending must sit below the line's median")
    ap.add_argument("--no-prosody", action="store_true",
                    help="skip the intonation gate")
    ap.add_argument("--slow", default="",
                    help="lines that keep a lower rate floor. A global floor is the "
                         "right default and the wrong answer for a line carrying the "
                         "one idea the viewer has to follow — he flagged \"it finds "
                         "the risk\" as too fast while asking for the rest to move.")
    ap.add_argument("--slow-rate", type=float, default=5.0)
    ap.add_argument("--pauses", default="",
                    help="line numbers that get the long gap. Separate from --closes "
                         "on purpose: whether a statement must fall and whether it "
                         "earns a pause are different questions, and conflating them "
                         "put a 1.1s hole straight after the hook, which cost the "
                         "opening its momentum. Defaults to --closes.")
    ap.add_argument("--closes", default="",
                    help="line numbers that close a section. Only those, and the last "
                         "line, must land — English rises on the non-final items of a "
                         "list, so a rising \"Open Settings.\" mid-list is correct.")
    ap.add_argument("--watch", default="three",
                    help="comma-separated words whose consonant onset is measured after each\n"
                         "                          take; a hard burst is treated as a failed\n"
                         "                          attempt and the line is rerolled. Only words\n"
                         "                          with ground-truth rows in audio/burst.py are\n"
                         "                          honoured. Empty string turns it off.")
    ap.add_argument("--no-verify", action="store_true",
                    help="skip the transcription check (faster, unverified)")
    a = ap.parse_args()

    src_html = a.fit or a.cues
    lines = cues_from_html(src_html) if src_html else [
        l.strip() for l in open(a.lines, encoding="utf-8") if l.strip()]
    slots = cue_times(a.fit) if a.fit else None
    if not os.path.exists(REF):
        sys.exit("no voice profile at " + REF)

    import torch, torchaudio
    from chatterbox.tts import ChatterboxTTS
    torch.set_num_threads(os.cpu_count() or 4)
    torch.manual_seed(a.seed)
    line_seeds = {}
    for part in a.line_seeds.split(","):
        if ":" in part:
            k, v = part.split(":", 1)
            line_seeds[int(k.strip())] = int(v.strip())
    if line_seeds:
        print(f"      per-line seeds: {line_seeds}", flush=True)

    # Only words with ground-truth rows behind them. Watching a word the metric was never
    # calibrated for would reroll takes on a reading that means nothing — /s/ measures like a
    # burst and /f/ measures like nothing, both by physics, and both are recorded as limits
    # in audio/burst.py.
    watch, skipped = [], []
    for w in (x.strip().lower() for x in a.watch.split(",") if x.strip()):
        (watch if w in burst.IN_SCOPE else skipped).append(w)
    if watch:
        print(f"      watching consonant onset: {', '.join(watch)} "
              f"(band {burst.BAND[0]:+.0f} to {burst.BAND[1]:+.0f} dB)", flush=True)
    if skipped:
        print(f"      not watched, no ground truth for it: {', '.join(skipped)}", flush=True)
    m = ChatterboxTTS.from_pretrained(device="cpu")

    # Generation is stochastic: an unlucky seed swallows a consonant and turns
    # "think" into "thing". Listen back to every line and retry the ones that
    # came out wrong, so the delivered track is verified rather than assumed.
    asr = None
    if not a.no_verify:
        from faster_whisper import WhisperModel
        asr = WhisperModel("small", device="cpu", compute_type="int8")

    phrases, words = load_pron()
    from prosody import final_drop, ends_sentence

    def lands(wav):
        """How far the ending sits under the line's own median pitch, in semitones.
        A statement that ends flat or rising reads as unfinished — he heard exactly
        that on "every chat" before any measurement did."""
        a1 = wav.squeeze().cpu().numpy().astype(np.float32)
        st, _, _ = final_drop(a1, m.sr)
        return st

    def say(text, idx):
        spoken = respell(text, phrases, words)
        if spoken != text:
            print(f"      respelled for clarity: \"{spoken}\"", flush=True)
        syl = syllables(spoken)
        best = None
        for attempt in range(a.retries + 1):
            base = line_seeds.get(idx, a.seed)
            torch.manual_seed(base + attempt * 1000 + idx)
            wav = m.generate(spoken, audio_prompt_path=REF, exaggeration=a.exaggeration,
                             cfg_weight=a.cfg, temperature=0.75)
            rate = syl / max(0.3, wav.shape[-1] / m.sr)
            if asr is None:
                return wav, 0.0
            probe = os.path.join(tmp, "probe.wav")
            torchaudio.save(probe, wav, m.sr)
            subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",probe,
                            "-ar","16000","-ac","1", probe + "16.wav"], check=True)
            segs, _ = asr.transcribe(probe + "16.wav", language="en",
                                     word_timestamps=True)
            segs = list(segs)
            heard = " ".join(sg.text for sg in segs)
            allw = [w for sg in segs for w in (sg.words or [])]
            cut = dup_tail(allw, text)
            if cut is not None and cut > 0.25:
                # cut the second copy off rather than gamble on another roll
                keep = int(cut * m.sr)
                if keep < wav.shape[-1] - int(0.05 * m.sr):
                    # Keep a little of the decay and fade it. Cutting hard on the
                    # repeat's first sample takes the end of the *first* copy with it —
                    # the line stops dead instead of landing, which is the "speaks
                    # outward" quality he heard in the take that used this.
                    keep = min(wav.shape[-1], keep + int(0.06 * m.sr))
                    wav = wav[..., :keep].clone()
                    n = min(int(0.045 * m.sr), wav.shape[-1])
                    if n > 8:
                        ramp = torch.linspace(1.0, 0.0, n, device=wav.device)
                        wav[..., -n:] = wav[..., -n:] * ramp
                    print(f"      said the tail twice — cut the repeat at "
                          f"{cut:.2f}s", flush=True)
                    torchaudio.save(probe, wav, m.sr)
                    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",
                                    "-i",probe,"-ar","16000","-ac","1",probe+"16.wav"],
                                   check=True)
                    segs2, _ = asr.transcribe(probe + "16.wav", language="en")
                    heard = " ".join(sg.text for sg in segs2)
                    cut = None
            rate = syl / max(0.3, wav.shape[-1] / m.sr)
            e = wer(heard, text)
            if cut is not None:
                e += 1.0        # an uncuttable repetition must never win on score

            # He reported "three" sounding like a hard T three separate times, and each round
            # of chasing it by ear cost a day. The retry loop already exists and already has
            # the word timings, so the word is measured here and a burst counts as a failed
            # attempt like a misheard word does. He does not listen to twelve takes; the
            # build rerolls until the consonant lands.
            #
            # Rate matters for the budget: at his settings the word measured in band in 2 of
            # 12 seeds, so this costs a handful of extra rolls on the lines that contain it
            # and nothing at all on the lines that do not.
            for tw in watch:
                hit = burst.find([{"word": w.word, "at": w.start, "dur": w.end - w.start}
                                  for w in allw], tw)
                if hit is None:
                    continue
                # Measure the POLISHED line, not the raw take.
                #
                # The raw take measured +10.5 dB, in band, and the same word in the finished
                # mix measured +22.6 dB. The speed-up was not the cause — 6% cannot move a
                # figure 12 dB. The polish chain is: it adds +1.5 dB at 4.2kHz and +2 dB at
                # 7.2kHz, both inside the 3-8kHz band this metric reads, and its compressor
                # has a 10ms attack, so a 5ms burst passes through untouched while the vowel
                # behind it is compressed down. Boosting the band and squashing the reference
                # both push the ratio the same way.
                #
                # Polish is deterministic per line, so measuring after it makes the take-level
                # check predict the mix instead of describing something that will not ship.
                pb = os.path.join(tmp, f"burst{idx:02d}.wav")
                polish(probe, pb)
                subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",pb,
                                "-ar","16000","-ac","1", pb + "16.wav"], check=True)
                bm = burst.measure(burst.load(pb + "16.wav"), float(hit["at"]),
                                   float(hit["dur"]))
                v = burst.verdict(bm)
                if v == "frication":
                    print(f"      \"{tw}\": {bm['peak']:+.1f} dB, frication", flush=True)
                elif v in ("burst", "absent"):
                    e += 0.5    # loses to a clean take, beats a misheard one
                    print(f"      \"{tw}\": {bm['peak']:+.1f} dB, {v} — rerolling", flush=True)
            # a line crammed past ~6.5 syllables a second loses its consonants even
            # when the transcriber still guesses the words right
            penalty = max(0.0, (rate - a.max_rate) * 0.08)
            score = e + penalty
            if best is None or score < best[1]:
                best = (wav, score, heard, e, rate)
            # e carries the burst penalty, so this also refuses to stop early on a take
            # whose words were right and whose consonant was not
            if e <= 0.001 and rate <= a.max_rate:
                best = (wav, score, heard, e, rate)
                break
            why = f"wer {e:.2f}" if e > 0.001 else f"{rate:.1f} syl/s, too dense"
            print(f"      retry {attempt+1}: heard \"{heard.strip()[:46]}\" ({why})", flush=True)

        # Second gate: the melody. Only for lines that end a sentence, and only after
        # the words are right — an unfinished-sounding ending is worth another take,
        # but not at the cost of a misheard word.
        closes = {int(x) for x in a.closes.split(",") if x.strip()}
        closes.add(len(lines))
        if a.no_prosody or not ends_sentence(text) or (a.closes and idx not in closes):
            return best[0], best[1]
        pick, pick_st = best[0], lands(best[0])
        if pick_st is not None and pick_st <= a.fall:
            return pick, best[1]
        for roll in range(a.prosody_rolls):
            torch.manual_seed(line_seeds.get(idx, a.seed) + 7777 + roll * 131 + idx)
            cand = m.generate(spoken, audio_prompt_path=REF, exaggeration=a.exaggeration,
                              cfg_weight=a.cfg, temperature=0.75)
            st = lands(cand)
            if st is None:
                continue
            if asr is not None:                      # never trade a word for a melody
                probe = os.path.join(tmp, "pros.wav")
                torchaudio.save(probe, cand, m.sr)
                subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",probe,
                                "-ar","16000","-ac","1", probe + "16.wav"], check=True)
                sgs, _ = asr.transcribe(probe + "16.wav", language="en")
                if wer(" ".join(x.text for x in sgs), text) > 0.001:
                    continue
            if pick_st is None or st < pick_st:
                pick, pick_st = cand, st
            if pick_st <= a.fall:
                break
        if pick_st is not None:
            mark = "lands" if pick_st <= a.fall else "still flat"
            print(f"      ending {pick_st:+.1f} st ({mark})", flush=True)
        return pick, best[1]

    tmp = tempfile.mkdtemp()
    LEAD = 0.30
    segs, cues, t = [], [], LEAD
    if not a.fit:
        segs.append(np.zeros(int(LEAD * SR_MIX), dtype=np.float32))
    timeline = np.zeros(0, dtype=np.float32)
    for i, text in enumerate(lines, 1):
        wav, err = say(text, i)
        if err > 0.001:
            print(f"      ! line {i} best available after {a.retries} retries (score {err:.2f})", flush=True)
        raw = os.path.join(tmp, f"{i:02d}.wav")
        torchaudio.save(raw, wav, m.sr)
        pol = os.path.join(tmp, f"{i:02d}p.wav")
        polish(raw, pol)
        # A line that drags is the other half of "it goes too fast": ours was the slowest
        # of nineteen reels measured, and slow reads as unclear rather than calm. Speed is
        # corrected with rubberband, which keeps the pitch, and only up to a cap.
        with wave.open(pol) as w0:
            secs0 = w0.getnframes() / w0.getframerate()
        rate0 = syllables(respell(text, phrases, words)) / max(0.3, secs0)
        slow = {int(x) for x in a.slow.split(",") if x.strip()}
        floor = a.slow_rate if i in slow else a.min_rate
        # Never speed up a line that failed the transcript check. Line 13 measured
        # 2.2 syl/s and was sped up x1.20 — but it was slow *because* it said the
        # phrase twice, so the speed-up compressed the defect instead of removing it
        # and hid the thing the check had already noticed.
        if err > 1.0 and rate0 < floor:
            # Only a repetition that could NOT be cut blocks the floor (dup_tail adds
            # 1.0 to the score for exactly that case). Blocking it on any failed check
            # was too broad: a line whose repeat was successfully cut is honestly
            # short now, and refusing to pace it cost the whole read its energy.
            print(f"      {rate0:.1f} syl/s, and the repetition could not be cut — "
                  f"not speeding it up, that would hide the cause", flush=True)
        elif rate0 < floor:
            f = min(a.max_speedup, floor / rate0)
            if f > 1.01:
                fast = os.path.join(tmp, f"{i:02d}f.wav")
                stretch(pol, fast, f)
                # The take-level watch check in say() measures the polished line before
                # this stretch exists, so a consonant that passed there can still be
                # broken here — rubberband smears the burst, not just the vowel it is
                # sitting next to. Measured on episode 01: "three" left the retry loop
                # in band and came out of a x1.20 stretch at 40+ dB, a clean burst. The
                # end-of-build check below would have caught it, but only by failing the
                # whole file after it was already written — this catches it per line and
                # keeps the slower, correct take instead.
                watched_here = _watched_in(respell(text, phrases, words), watch)
                broke = False
                if watched_here and asr is not None:
                    check16 = fast + "16.wav"
                    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",fast,
                                    "-ar","16000","-ac","1", check16], check=True)
                    segs3, _ = asr.transcribe(check16, language="en", word_timestamps=True)
                    words3 = [{"word": w.word, "at": w.start, "dur": w.end - w.start}
                              for sg in segs3 for w in (sg.words or [])]
                    for tw in watched_here:
                        hit3 = burst.find(words3, tw)
                        if hit3 is None:
                            continue
                        bm3 = burst.measure(burst.load(fast), float(hit3["at"]), float(hit3["dur"]))
                        if burst.verdict(bm3) in ("burst", "absent"):
                            broke = True
                            print(f"      \"{tw}\": {bm3['peak']:+.1f} dB after the x{f:.2f} "
                                  f"stretch — the take was clean, the stretch was not. "
                                  f"Keeping the slower take.", flush=True)
                if broke:
                    print(f"      {rate0:.1f} syl/s, staying slow to protect the consonant", flush=True)
                else:
                    print(f"      {rate0:.1f} syl/s, sped up x{f:.2f}", flush=True)
                    pol = fast
        with wave.open(pol) as w:
            s = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        # trim the silence the model leaves at either end
        env = np.abs(s)
        k = int(0.01 * SR_MIX)
        env = np.convolve(env, np.ones(k) / k, "same")
        loud = np.where(env > env.max() * 0.035)[0]
        start = 0
        if len(loud):
            start = max(0, loud[0] - int(0.05 * SR_MIX))
        # A leading watched word gets one more measurement here, on the exact samples
        # about to ship, because the 3.5%-of-peak threshold above finds where the loud
        # part of the word starts — not where the word itself starts. "Three" opens on
        # an unvoiced /th/, quieter than the vowel that follows it by design, and the
        # trim was cutting straight through it: line 7 measured a clean +9.7 dB
        # frication before this trim and a hard +25.2 dB burst after it, because what
        # was left was the vowel onset alone, with the fricative that made it a "th"
        # instead of a "t" cut away. Anchoring the kept window to the word's own
        # Whisper-measured start — not the loudness threshold — keeps the fricative.
        watched_here = _watched_in(respell(text, phrases, words), watch)
        if watched_here and asr is not None and start > 0:
            check16 = pol + ".16.wav"
            subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",pol,
                            "-ar","16000","-ac","1", check16], check=True)
            segs4, _ = asr.transcribe(check16, language="en", word_timestamps=True)
            words4 = [{"word": w.word, "at": w.start, "dur": w.end - w.start}
                      for sg in segs4 for w in (sg.words or [])]
            starts = [float(burst.find(words4, tw)["at"]) for tw in watched_here
                      if burst.find(words4, tw) is not None]
            if starts:
                protect = int(min(starts) * SR_MIX)
                if protect < start:
                    print(f"      trim would cut into \"{watched_here[0]}\" at "
                          f"{min(starts):.2f}s — starting the kept audio there instead",
                          flush=True)
                    start = max(0, protect)
        if len(loud):
            s = s[start: min(len(s), loud[-1] + int(0.08 * SR_MIX))]
        f = int(0.012 * SR_MIX)
        s[:f] *= np.linspace(0, 1, f); s[-f:] *= np.linspace(1, 0, f)

        if slots:
            want = slots[i-1][1] - slots[i-1][0]
            got = len(s) / SR_MIX
            factor = max(0.88, min(1.12, got / want))     # >1 speeds up
            if abs(factor - 1) > 0.01:
                a1 = os.path.join(tmp, f"{i:02d}s.wav"); b1 = os.path.join(tmp, f"{i:02d}f.wav")
                with wave.open(a1, "w") as o:
                    o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR_MIX)
                    o.writeframes((s * 32767).astype(np.int16).tobytes())
                stretch(a1, b1, factor)
                with wave.open(b1) as w:
                    s = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
            pos = int(slots[i-1][0] * SR_MIX)
            need = pos + len(s) + int(0.5 * SR_MIX)
            if len(timeline) < need:
                timeline = np.concatenate([timeline, np.zeros(need - len(timeline), dtype=np.float32)])
            timeline[pos:pos+len(s)] += s
            cues.append({"n": i, "line": text, "start": round(slots[i-1][0], 2),
                         "end": round(slots[i-1][0] + len(s) / SR_MIX, 2)})
            print(f"  {i:02d}/{len(lines)}  {len(s)/SR_MIX:5.2f}s into a {want:4.2f}s slot "
                  f"(x{factor:.2f})  {text[:40]}", flush=True)
        else:
            cues.append({"n": i, "line": text, "start": round(t, 2), "end": round(t + len(s) / SR_MIX, 2)})
            segs.append(s); t += len(s) / SR_MIX
            src_g = a.pauses or a.closes
            closes_g = {int(x) for x in src_g.split(",") if x.strip()} or SECTION_END
            g = a.long if i in closes_g else a.gap
            if i < len(lines):
                segs.append(np.zeros(int(g * SR_MIX), dtype=np.float32)); t += g
            print(f"  {i:02d}/{len(lines)}  {len(s)/SR_MIX:5.2f}s  {text[:52]}", flush=True)

    if slots:
        track = timeline; t = len(track) / SR_MIX
    else:
        segs.append(np.zeros(int(0.45 * SR_MIX), dtype=np.float32)); t += 0.45
        track = np.concatenate(segs)

    if not a.dry:
        breaths = breath_bank()
        if breaths:
            rng = np.random.default_rng(a.seed)
            placed = 0
            for c in cues[1:]:                      # never before the first line
                br = breaths[rng.integers(len(breaths))] * rng.uniform(0.42, 0.62)
                pos = int(c["start"] * SR_MIX) - len(br) - int(0.05 * SR_MIX)
                if pos < 0 or pos + len(br) > len(track):
                    continue
                if np.abs(track[pos:pos+len(br)]).max() > 0.02:
                    continue                        # the gap is not actually empty
                track[pos:pos+len(br)] += br
                placed += 1
            print(f"  placed {placed} breaths from his own recording")
        track = bed(track, load_wav(TONE), a.room_db)
        print(f"  room tone bed at {a.room_db} dBFS")
    track = np.clip(track, -1, 1)
    with wave.open(a.out, "w") as o:
        o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR_MIX)
        o.writeframes((track * 32767).astype(np.int16).tobytes())
    json.dump(cues, open(os.path.splitext(a.out)[0] + "-cues.json", "w"), indent=1)
    print(f"\nwrote {a.out}  {t:.1f}s  {len(lines)} lines")

    # Measure the watched words again, on the file that actually ships.
    #
    # The first version of this checked inside the retry loop only, and the loop runs before
    # the assembly stage speeds a dragging line up by as much as 1.20. On the very first real
    # build that gap showed itself: the take was accepted at +10.5 dB, in band, and the same
    # word in the finished mix measured +24.9 dB, a burst. Compressing a line by 20% is not
    # neutral to the consonant it contains. So the check ran, passed, and the thing it was
    # protecting shipped broken anyway — the same shape of mistake as measuring a word against
    # a baseline that is not there.
    #
    # This is the guarantee that is worth having: not "the take was measured" but "the audio
    # in this file was measured". It exits non-zero, because a build that quietly writes a
    # file it knows is wrong is worse than one that stops.
    if watch and asr is not None:
        print("\n  the shipped file, measured:", flush=True)
        bad = []
        segs, _ = asr.transcribe(a.out, language="en", word_timestamps=True)
        allw = [{"word": w.word, "at": w.start, "dur": w.end - w.start}
                for sg in segs for w in (sg.words or [])]
        y = burst.load(a.out)
        for tw in watch:
            hit = burst.find(allw, tw)
            if hit is None:
                print(f"    \"{tw}\": not in the transcript of the mix", flush=True)
                continue
            bm = burst.measure(y, float(hit["at"]), float(hit["dur"]))
            v = burst.verdict(bm)
            print(f"    \"{tw}\": {bm['peak']:+.1f} dB, {v}", flush=True)
            if v != "frication":
                bad.append(f"{tw} {bm['peak']:+.1f} dB ({v})")
        if bad:
            print(f"\n  the mix does not hold what the takes measured: {', '.join(bad)}."
                  f"\n  The take-level check measures the polished line, so this should not"
                  f"\n  happen; something between polish and the written file changed the"
                  f"\n  consonant. Suspect the time-stretch first, then the trim.", flush=True)
            sys.exit(1)

if __name__ == "__main__":
    main()
