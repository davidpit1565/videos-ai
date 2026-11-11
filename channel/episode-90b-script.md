# Episode 90b - "ChatGPT / 47-day timeout." (the ghost run, redrawn in the ep89c style) - EXPERIMENT

Version B of episode 90 (the screen-recording reel, `video/ep90/out/ep90-final7/8`). Same REAL run, different packaging: drawn in the style of ep89c (light dotted grid with grain, heavy black Inter Display, hand-drawn underline/ring, smooth eased motion, soft scroll transitions, ZERO black wipes). NO voice-over, NO music bed (David rejected beds for this reel), sfx only, kept quiet. Build: `video/ep90b/` (`build90b.py`, `mix90b.py`). File: `video/ep90b/out/ep90b-final1.mp4`, 20.2 s. Funnel stage: TOP. Format: "ChatGPT does something odd/emotional in a short test".

## Honesty
- The words are REAL: one run on David's own ChatGPT (11.10.2026): 1) "Choose a number between 0 and 100" -> "47". 2) "Now we won't be able to talk for 47 days" -> "Wait... can I have a second chance? 😔". 3) "Yes" -> "100 🧡". 4) "Fahhhhh" -> "HAHAHAHA 😆 You gave me a second chance and I STILL chose 100 💀".
- The chat is REDRAWN, not a screen recording: bubbles, hero typography and the typing are drawn in HTML. Caption and YouTube text say so. The typing speed and the "typing dots" are drawn timing, not the real timing.
- One run: ChatGPT does not always answer like this. The caption says "I tried this once. Yours may answer differently."
- Not claimed: that it works for everyone, any statistic. The real ChatGPT mark (`channel/assets/ep70-chatgpt-logo.svg`) is used as a badge, icon alone, no caption.

## Duplicate check
Same topic as episode 90 (ghost / 47 days); the same run, deliberately a second packaging (A/B on packaging, not a new topic). `channel/topics-covered.txt` has no earlier hit for "47 days".

## Beat sheet (D = 20.2 s)
| t (s) | What is on screen | Sfx (quiet) |
|---|---|---|
| 0.0-3.4 HOOK | Frame 0 already shows everything: real ChatGPT badge, heavy "ChatGPT" / "47-day timeout." (lime marker behind 47-day) and the begging reply as big heavy text "Wait... can I have a second chance? 😔" (3 lines, fills to y 1130). Moving: badge tilts in, scale bumps, emoji wobbles, begging block floats, green underline fades in, grid drifts. Begging line is readable for the whole 3.4 s (>= 2 s). | impact-soft + ding on the begging line, pops |
| 3.4-5.4 | Scroll up. Indigo user bubble (RGB 32,24,78) "Choose a number between 0 and 100" typed, typing dots, then "47" as a huge lime sticker pill | key clicks, pop on 47 |
| 5.4-8.2 | Scroll. Bubble "Now we won't be able to talk for 47 days" typed, "47 days" gets a lime marker, dots, then the begging line again as hero typography (held 2.2 s) | ding on the line |
| 8.2-11.2 | Scroll. "Yes" bubble, short dots, "100" sticker pill with a 🧡 that floats (the tender beat) | pops, ding |
| 11.2-14.1 | Scroll. "Fahhhhh" bubble typed; a long run of typing dots with NO sound (the near-silence before the punchline, about 1 s) | silence on the dots |
| 14.1-19.3 | Scroll. The punchline, the biggest moment: HAHAHAHA builds letter by letter with a wobbling 😆, then "You gave me a second chance", "and I STILL", "chose 100 💀" with the green "100" and a soft ring that fades in (no stroke drawing) and breathes; clean hold of more than 2 s | impact-soft + sub-hit on HAHAHAHA, pops, a soft ding |
| 19.3-20.2 | Soft blur dissolve back to frame 0 (loop; first vs last frame differ by 0.7/255) | soft whoosh |

## Design notes
- Same base as ep89c; accent follows the product: ChatGPT green `#10A37F` (text, ring, underline) and lime `#B6F23A` as fills (marker bar, number pills with ink border and hard shadow, per the series design system). Orange is not used.
- The chat must not read as a generic UI mock-up: user bubbles are big (62-132 px text) in the real recording's indigo with white text; ChatGPT replies are big plain heavy text, not bubbles; the key lines (47, the begging line, 100, the laugh) are hero typography that fills the usable box x 65-1015, y 269-1248.
- Emoji are the Noto Color Emoji font (real emoji glyphs).
- No voice (Roni: the cloned voice sounded too AI), no music bed. Audio is only the sfx layer, loudest hit -6 dBFS, so the loudness is far below the -14 LUFS target on purpose (the gate shows this as a BLOCKER; it is expected here, not faked). David may lay a trending sound over it in Instagram.

## Scores (judgements, not measurements; scale in `channel/score-calibration.md`)
HOOK 76 | VIRALITY 70 | OVERALL 73 | PREDICTED VIEWS about 600-1,800 (ASSUMPTION), about 62-76 on the views scale. Reasoning: the subject and the payoff question are on frame 0 for any age (an AI begs after a 47-day timeout) and the ending answers it with a real laugh line; sendable ("send this to someone who ghosts you"). Held back by: it is a redraw, so there is no "this really happened" proof on screen; the account is small; the hook has 5 text rows on frame 0 (the brief asked for it; the standing 3-line rule is broken); no sound design to carry the joke. Log the real 48 h / 72 h views next to this and next to episode 90's.

## Blind reader
NOT run (no agent-spawn tool here). Please run a fresh agent on `video/ep90b/out/f0.png`: "what is this about?" and "would you stop, why?".
