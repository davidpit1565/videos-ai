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

---
# FINAL2 (11.11.2026) - rebuilt in the ep89c "Miki" language (final1 was rejected: it looked like the older generic drawn style)

File: `video/ep90b/out/ep90b-final2.mp4` (20.9 s) + `ep90b-final2-review720.mp4`; build `video/ep90b/build90b2.py`, mix `mix90b2.py`, runner `run2.sh` (final1 and its files untouched). Same REAL run (David's own ChatGPT, one run, redrawn; caption/YouTube text unchanged and still say so). No voice. A music bed from the real library + quiet sfx.

## Beat sheet
| t (s) | Picture |
|---|---|
| 0-3.3 hook | Real ChatGPT badge (icon alone). Heavy "ChatGPT" on frame 0, "47-day" gets a black selection bar (white text) at 0.18 s, "timeout." rises at 0.32 s. The begging line sits in a dark reply card (ChatGPT logo header) from frame 0 and builds word by word: "Wait..." on frame 0, then can / I / have / a / second / chance? / 😔 by 1.0 s; held to 3.3 s (about 2.3 s fully readable). Text on frame 0: 2 heavy lines + the card (the begging line is in a card, as asked). |
| 3.3-5.7 | Soft scroll. Black tag "PROMPT 1" + dashed curve, dark prompt card types "Choose a number between 0 and 100" letter by letter, send button lights, then "47" appears huge inside a black selection bar (white digits). |
| 5.7-10.7 | Card fades up/out, "PROMPT 2" card types "Now we won't be able to talk for 47 days" (hand-drawn white underline under "47 days"), send lights, then the begging line as black hero type built word by word, black selection bar on "chance?", an orange hand-drawn asterisk turning slowly; held about 2.8 s |
| 10.7-13.3 | "PROMPT 3" card types "Yes", send lights, then "100" in orange (soft fade-up, no pop) with a floating 🧡 |
| 13.3-15.9 | "PROMPT 4" card types "Fahhhhh", send lights, then a dark reply card with three big typing dots for about 1.3 s (music at near-silence, sfx off) |
| 15.9-19.95 | The punchline: HAHAHAHA builds letter by letter with a wobbling 😆, "You gave me a second chance" word by word, "and I STILL" with a black selection bar on STILL, "chose 100 💀" with the orange ring on 100 fading in softly (scale 0.96 -> 1, no stroke drawing) and breathing; clean hold of 1.8 s after the ring is in |
| 19.95-20.9 | Soft blur dissolve back to frame 0 (loop; first vs last frame differ by 1.0/255) |

## Miki-rules checklist (insiderforce, from `channel/style-research-31-10.md` and ep89c)
IN: light grey dotted grid with grain (static grid, slow vertical drift of the page); black heavy type built word by word (hook, begging line, punchline) with the rise-and-fade word entrance; dark rounded prompt card with a small black mono tag (PROMPT 1-4) and a dashed curve joining tag and card; letters typed into the card with a cursor; black selection bar with white text on key words (47-day, 47, chance?, STILL); hand-drawn underline (under "47 days") and an orange hand-drawn asterisk and ring; orange #D97757 as the one accent, only on "100" (digits and ring) and the asterisk; real ChatGPT icon badge alone; soft scrolls and blur dissolves only, ZERO black wipes; smooth eased motion, something moving at least every ~2 s (typing, drift, wobble, scroll).
NOT IN / DIFFERENT: no star-shaped black blurred wipe at all (David: none is fine); no spoken voice-over; block structure is a story (one run), not "#N command name" tips; the screens are drawn placeholders of the real chat (the words are real); light connector words are not used on the hook (the heavy lines carry it); the word cadence is not tied to a voice, it is timed by the build.

## Music (no voice, so the bed carries the feel) - details in `channel/music-notes.md`
Best pick: `punchy--hip-hop-beat--themountain.mp3` (used in ep89c, no complaint). Ducking plan: full groove from 0.0 s (no slow fade-in), -8 dB "tender" dip while the begging hero is on screen (7.8-11.1 s), near-silence (-30 dB, sfx also off) during the typing dots (14.75-16.2 s), the groove returns with a +1.5 dB sting as the punchline lands, 1 s fade-out at the end. Previews with two other beds are in `video/ep90b/out/ep90b-final2-alt-A-720.mp4` (cinematic--dramatic--themountain, David loved it in ep85, but it is dramatic: may over-serious the joke) and `-alt-B-720.mp4` (punchy--trending-instagram-reels-music--delosound, lighter, same family as ep89c). Not heard by me.

## Scores (judgements, not measurements)
HOOK 78 | VIRALITY 72 | OVERALL 75 | PREDICTED VIEWS about 700-2,000 (ASSUMPTION), about 64-79 on the views scale. Higher than final1 because it now uses the style David and Roni already like (ep89c) and the hook builds word by word with the begging card visible from frame 0; still held back by: drawn placeholder screens, a small account, no voice to carry the first second, one run. Below the 90/95 bar in `score-calibration.md`; not inflated.

---
# FINAL3 (11.11.2026) - David's feedback on final2 applied (final1/final2 files untouched)

File: `video/ep90b/out/ep90b-final3.mp4` (20.9 s) + `ep90b-final3-review720.mp4`; build `video/ep90b/build90b3.py`, mix `mix90b3.py`, runner `run3.sh`.
What David said and what changed:
1. Logos: the orange asterisk looked like Claude's mark and the ChatGPT badge repeated. Removed: the asterisk and every star/sparkle shape; the ChatGPT icon now appears ONCE, as the badge on frame 0 of the hook (icon alone, no caption); the logo headers inside the cards and replies are gone.
2. "Not clear that the big text is ChatGPT's answers": roles are now carried by the black tag component (same as the prompt tags). User cards are tagged `ME` (was `PROMPT 1-4`); every ChatGPT answer sits under a black `CHATGPT` tag: the begging line in the hook, "47", the begging hero, "100", the typing dots and the laughing reply.
3. No orange anywhere: palette is black, white, the light grey grid, the dark card black and the black selection bars. Emphasis is by the black bar, a black hand-drawn underline and ring (on "100" in the punchline), size and weight. One caveat: the real reply is "100 🧡"; to keep the real text without any orange the heart emoji is shown in grey (CSS grayscale). The 😔 😆 💀 emoji keep their normal colours (yellow/grey).
4. Music: the library bed is REMOVED (David's ear rejected every bed; he will add a trending sound in Instagram). Audio is only the quiet sfx timed to the beats, with the near-silence (no sfx at all) during the typing dots before the punchline; sfx-only track normalised to about -18 LUFS (single pass, true peak -1.5), not faked louder.
5. 47 and 100 scenes enlarged: "47" is white on a full-width black selection bar (950 px), "100" is 420 px heavy black type with the grey heart, so there is no empty half.
Unchanged: word-by-word build, typed cards with black tag and dashed curve, selection bars, soft scrolls, NO black wipes, the begging hero held about 2.8 s, the punchline hold, the soft loop dissolve.
Scores (judgements): HOOK 76 | VIRALITY 72 | OVERALL 74 | PREDICTED VIEWS about 700-2,000 (ASSUMPTION). Slightly clearer roles than final2; the music-less version leaves the first second to picture and sfx only. Not at the 90/95 bar, not inflated.

---
# FINAL4 (11.11.2026) - two changes on final3 (final1-3 untouched)

File: `video/ep90b/out/ep90b-final4.mp4` (23.3 s) + `ep90b-final4-review720.mp4`; build `video/ep90b/build90b4.py`, runner `run4.sh`. Reason: David's Meta AI account analysis (its view numbers matched the studio on 6 of 6 checks): hooks that state a specific first-person test with a specific number and show the result at once held viewers (skip 40-68%), generic title frames lost them (skip 80-91%), and a "send to" line matters. This is a judgement from one analysis, not a measured effect on this reel.
1. Hook text is now first-person and specific: heavy "I gave ChatGPT" on frame 0, then "a 47-day timeout." builds word by word within the first second (a 0.12 s, 47-day with the black selection bar 0.22 s, timeout. 0.46 s); the begging card under its CHATGPT tag is visible from frame 0 and builds as before; real ChatGPT badge kept; 2 heavy lines + the card.
2. End card: after the punchline hold (about 2 s after the ring is in) a soft scroll brings "Send this to / someone who / ghosts you." as big heavy black type, word by word, with the black selection bar on "ghosts you."; held about 1.9 s, then the soft blur dissolve back to frame 0 (D 20.9 -> 23.3 s).
Everything else unchanged: monochrome, ME / CHATGPT tags, one logo only, sfx-only audio, no orange, no wipes. Caption first line updated (as requested), the rest unchanged.
Scores (judgements): HOOK 80 | VIRALITY 74 | OVERALL 77 | PREDICTED VIEWS about 700-2,200 (ASSUMPTION). The first-person number hook and the send line are the changes David's evidence supports; still drawn placeholders, one run, small account.
