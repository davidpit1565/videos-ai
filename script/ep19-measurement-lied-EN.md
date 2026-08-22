# Episode 19 — "The measurement that lied to me twice"

**Format:** long-form YouTube (target 14–18 min) + a 50s reel
**Topic:** none in the measured set. This one is not chosen by demand.
**Blocked on:** nothing. Every number in it already exists.

**Why it is in the slate at all.** No channel in this niche publishes its own wrong results.
That is precisely why this one earns trust for the other nineteen: a channel that shows you
its retractions is a channel whose claims mean something. It is also the cheapest episode we
have — the material is already on disk, in the commits, timestamped.

---

## The story, in the order it happened

**The complaint.** He said the word "three" sounded wrong in his own cloned voice. Not a
measurement — an ear. Three separate times.

**The first tool.** `th_check.py`: English /θ/ is a weak fricative lasting 45–160ms; the
substitution is a stop — near-silence, then one sharp transient. Measure frication duration
before voicing and how abruptly the energy rose. Sound reasoning. Wrong anchor.

**The answer it gave.** Ten seeds, five respellings: every one a stop. Verdict: *this voice
cannot make that sound.* Written down as settled.

**Then a sweep of 58 takes, and twelve came back as fricatives.** The conclusion reversed.
The carrier looked like the lever — the word at the start of a sentence worked, buried mid-line
it did not. A clean, publishable finding.

**The control that killed it.** Same position, same settings, words that *must* be stops:

```
three  75.0–82.5 ms   fricative
tree   77.5–82.5 ms   fricative
two    75.0–77.5 ms   fricative      ← there is no /θ/ in "two"
tea    70.0–77.5 ms   fricative      ← or in "tea"
```

The tool was reading the model's **amplitude ramp at the start of the audio**. Long, gradual
and loud is exactly what an onset looks like, so both of its tests passed and the verdict meant
nothing. Twelve findings, zero real.

**And it retracted the original finding too.** The ten seeds that "proved" it impossible were
also single words at the start of a recording — the same artifact, in the other direction. Both
conclusions rested on the same blind spot.

**The second tool.** Anchor on the vowel, which is always there. Compare the high band before
voicing to the high band of *that same word's vowel* — a ratio inside one word, independent of
what came before it. Validated against a set where the answer was known.

**Which promptly failed too**, on a partial view of that set. `/f/` fell below the band, `/s/`
spanned both sides. Both physical: `/f/` is a weak labiodental, `/s/` a sibilant loud enough to
exceed its own vowel. The scope had to shrink to one contrast, and be stated.

**Then the automation worked — and shipped a broken file anyway.** The take measured +10.5 dB,
in band, after seven visible rerolls. The finished mix measured +22.6 dB. The check was in the
wrong place: the polish chain adds +1.5 dB at 4.2kHz and +2 dB at 7.2kHz, both inside the band
being read, and its compressor's 10ms attack lets a 5ms burst through while squashing the vowel
behind it. Three and a half dB of EQ became twelve dB of measurement.

## The one line the episode exists for

> **A measurement that agrees with you is not evidence. It is a hypothesis wearing a number.**

Every retraction here came from the same move: taking something that *must* have a known
answer, and checking that the instrument gets it right. "Two" and "Tea" cost about twenty
minutes and saved shipping a video with a false claim attached.

## What is on screen

The real logs, unedited. The reroll sequence as it actually printed:

```
"three": -0.9 dB   absent    → rerolling
"three": -9.8 dB   absent    → rerolling
"three": +28.7 dB  burst     → rerolling
"three": +19.3 dB  burst     → rerolling
"three": +10.5 dB  frication ← accepted
```

Then the post-assembly line that refused the file. Then the commit messages, which say the
same thing in the same words — because they were written when it happened, not for a video.

## The reel cut (50s)

Hook: *"My tool told me 'Two' and 'Tea' contained a TH sound. Here's how I found out."*

## Not in this episode

- Any suggestion that the tooling is now correct. It is correct **for one contrast**, and the
  file says so.
- The voice-cloning tutorial. That is episode 15.
