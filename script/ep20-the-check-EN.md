# Episode 20 — "The check that refuses to ship your video"

**Format:** long-form YouTube (target 16–20 min) + a 45s reel
**Topic:** none in the measured set — chosen for the same reason as 19.
**Blocked on:** nothing.

**The premise.** Thirteen automated checks stand between a finished render and being sent. Every
single one exists because a real defect got through first. This episode is the list, and each
item is told as the failure that created it — not as a feature.

---

## The order, which is the order they were written in

| The check | The defect that created it |
|---|---|
| Colour-card duration ≥ 0.45s | He stopped the video on a ten-frame yellow card. It read as a glitch |
| Card must not play over speech | Two cards landed on the narration, so a word was lost under a flash |
| First frame carries picture | The hook faded in over 0.26s, so frame zero was empty — a black thumbnail |
| Length matches the build | Recorded playback drifted up to two seconds against the build's own timings |
| Frozen-picture runs | A scene held still for four seconds and looked like a stall |
| Safe area, all four edges | Captions sat **413px inside** the region Instagram draws its own UI over |
| Text boxes not landing on each other | Two lines overlapped by 79px and both became unreadable |
| −14 LUFS, true peak −1 dBTP | YouTube turns anything louder down and never turns quiet content up |
| Loudness range | A quiet line and a loud line in one reel, and the viewer reaches for the volume |
| Word-final energy | His voice softens unstressed endings — "think" became "thing" |
| Sibilance | One line's S came in 6.5 dB above prediction |
| Pacing per line | A line at 6.5+ syllables a second loses its consonants even when transcribed right |
| **Consonant onset of a watched word** | He said "three" sounded like a hard T. Three times |

## The two moments that make it a video rather than a list

**The check that reported a defect and hid it.** A line was slow, so it was sped up 20%. It was
slow *because it said the phrase twice* — the speed-up compressed the defect instead of removing
it, and hid the thing the check had already noticed. The fix is one condition: never pace a line
whose repetition could not be cut.

**The check that lied about its own result.** The `/join` page was clipped to 700px of a 2500px
page, and the check reported it fine — because clipping makes the scroll height *equal* the
viewport, which is exactly what "fits" looks like. What gave it away was a second number:
`scrollable=false, reached=0px`.

## The line the episode ends on

> **A check you wrote is not a check that works. Break the thing on purpose and see whether it
> notices.**

Both stories above are checks that passed while the defect shipped. The only way that gets found
is deliberately breaking the input — which is now the last step of writing any check here.

## What is on screen

The gate running, live, on a file that fails. Real output, no reconstruction:

```
[BLOCKER] card 7.10-7.43s (10 frames) — plays over the line at 3.46s
413px past the bottom line   y 1571-1661   subs  "Everyone says ."
SOMETHING FAILED — do not send this file
```

Then the same file after the fix, and the line that matters: `ALL CHECKS PASSED`.

## The reel cut (45s)

Hook: *"My own script refuses to let me post this video. Thirteen reasons."*

## Not in this episode

- A claim that the checks are complete. They are not — the list grows every time something gets
  through, which is the point.
- The build tooling itself. That is episode 14, the long one.
