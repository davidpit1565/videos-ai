# Episode 18 — "Editors squeeze audio to fit the picture. That's backwards"

**Format:** 50s reel + a short long-cut section inside episode 14
**Blocked on:** nothing.

**The claim:** almost every editor cuts the picture first and then stretches or squeezes the
voice to fit it. Do it the other way round — build the voice at its own pace, then move every
timing in the picture to match — and the result stops sounding rushed without a single frame
being re-cut.

---

## The narration

| Line | On screen |
|---|---|
| Your video sounds rushed. The edit isn't why. | A reel that feels hurried |
| You cut the picture, then squeezed the voice to fit. | Waveform being compressed to a grid |
| Everyone does it. It's backwards. | Same, flagged |
| A voice has its own pace. Compress it and consonants disappear. | A word losing its ending, twice, audibly |
| So build the voice first, at the pace it wants. | Waveform, uncompressed |
| Then move the picture to *it*. | Cue times sliding onto the waveform |
| One script does it: every timing, re-derived. | `retime.py` running |
| I tried it the wrong way once. Seven lines ended up overlapping. | The seven overlaps, on screen |
| The picture follows the voice. Never the reverse. | The rule, held |

## The number this rests on

Forcing lines into fixed slots produced **seven overlapping lines** in episode 02 — two voices
audible at once. That is what `--fit` does when it is used for pacing instead of for a cut that
genuinely cannot move. The failure is on disk and it goes on screen.

## The distinction the reel must keep

`--fit` is not wrong. It exists for a cut that truly cannot move — a hard sync to something
visual. Using it for *pacing* is the mistake. If the reel says "never squeeze audio" it is
overstating, and someone will hit a real sync problem with no tool for it.

One line covers it: *"Squeeze it only when the picture genuinely can't move. That's rare."*

## Not in this reel

- How the narration is generated. Episode 15.
- The full build pipeline. Episode 14.
