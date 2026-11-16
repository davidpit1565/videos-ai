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

---
# FINAL5 (11.11.2026) - with a VOICE, a REAL-pixels proof card and an end card timed to the voice

Trigger: David pasted Meta AI's ratings of the two ghost reels (recording 52 -> 75-78 possible, drawn 68 -> 80-83 possible; its advice: shorter, a voice, big text per second, a real-chat proof element in the drawn one, a cover, low background music added in Instagram). These ratings are an outside opinion, not a measurement of views.
File: `video/ep90b/out/ep90b-final5.mp4` (+ `-review720.mp4`, `cover-ep90b.png`, `f0.png`); build `build90b5.py`, mix `mix90b5.py`, runner `run5.sh`. final1-4 untouched.

## Voice (shared with the recording version)
One TTS render, `video/ep90/voice/` (README there has the exact commands): 7 lines, TRUE to the real run (Meta's invented setup line not used): 1 "I gave ChatGPT a 47-day timeout." 2 "I asked it to pick a number. It picked 47." 3 "So I said: no talking for 47 days." 4 "It begged: can I have a second chance?" 5 "I said yes." 6 "And it still chose 100." 7 "Send this to someone who ghosts you." Cloned voice, exaggeration 0.74 (0.78-0.80 on lines 1/4/6/7), fast take (atempo 1.15), 18.6 s with gaps 0.34-0.85 s. script_lint flagged only "number" (kept word-for-word); voice_doctor nothing flagged; voice_quality line 3 pitch range 11.5 st at the exact window (9.8-10.8 st shifted: a pyin edge); accent check skipped. Measured, not heard; whisper hears "chose" as "shows" in line 6.
For this reel line 7 is delayed by 4.15 s (silence inserted after line 6, `out/narration90b.wav`) so the punchline can hold 1.8 s before the end card; that is the "laugh reading" pause. Total 23.9 s, longer than the 15-17 s asked: voice 18.6 s + 4.15 s hold + soft ending. Levers if it must be shorter: drop the Fahhhhh beat (about -1.1 s), hold 1.5 s (-0.3 s), or speed the voice further.

## Picture (voice-driven; word times from `cues.json`)
Hook: frame 0 "I gave ChatGPT" / "a 47-day timeout." (as final4, words build with the voice), real badge; at 0.45 s a black tag REAL CHAT and a dark card holding REAL PIXELS cropped from David's recording (src 35.4 s: the user bubble "Now we won't be able to talk for 47 days" and the reply "Wait... can I have a second chance?"; contrast lift = the same monotone curve as in `video/ep90/build90h.py`, no other edit) - proof inside the first 2 s, held about 2.4 s. Line 2: ME card types the number prompt, CHATGPT tag + "47" on a black bar. Line 3: ME card types the 47-day message. Line 4: CHATGPT tag + the begging line as black hero type (selection bar on "chance?") built word by word with the voice, and the REAL CHAT card again beneath it (visible 2.2 s). Line 5: ME card "Yes". Line 6: CHATGPT + "100" with the grey heart. Then Fahhhhh (ME), typing dots in silence, the punchline (HAHAHAHA, "You gave me a second chance", "and I STILL chose 100" with the black ring, full hold 1.8 s), then the soft scroll to the end card "Send this to someone who ghosts you." with the black selection bar on "ghosts you." timed to the voice, soft dissolve back to frame 0.
Kept from final4: monochrome, ME/CHATGPT/REAL CHAT tags, one logo badge only, selection bars, soft scrolls, no black wipes, no orange.
Emoji: the real recording shows the PLEADING FACE (🥺) after "Wait... can I have a second chance?", not 😔; the drawn text now uses 🥺 to match the real pixels.
Audio: voice is the main level (-14 LUFS target for the mix), sfx about 13 dB under the voice, NO music bed (David adds a tension beat in Instagram at about 12%).
Cover: `video/ep90b/out/cover-ep90b.png` = the "STILL chose 100" frame with the black ring (1080x1920; key content sits inside the central 4:5 area y 285-1635).
Scores (judgements): HOOK 80 | VIRALITY 76 | OVERALL 78 | PREDICTED VIEWS about 800-2,500 (ASSUMPTION). Gains: real proof + voice + send line; costs: 23.9 s length, drawn placeholders for the rest, voice not heard by me.

---
# FINAL7 (11.11.2026) - drawn Miki-style with the ep89-recipe voice, music bed and sfx (final5/final6 kept)

David listened: the earlier ghost voice was "mushy, AI"; the ep89 voice he loved. The voice was re-rendered with EXACTLY the ep89 recipe: exaggeration 0.78, hook line 0.90, lines 4/6/7 at 0.82, gap 0.18, min-rate 5.4, seeds 6101-6107, long pause after lines 5 and 6, fast take atempo 1.12: `video/ep90/voice/narration90b.wav` (16.78 s) + `cues90b.json`, commands in `video/ep90/voice/README-b.md`. Checks: script_lint only "number" (kept); voice_doctor no BAD (recipe gap note only); voice_quality line 6 pitch range 10.8 st (marginal, consistent over shifted windows; NOT re-rendered because another build uses these cues; David's ear decides), rest clean; accent check skipped; measured, not heard. Line endings to listen for: "47." -45 dB, "you." -38 dB, "100." -33 dB, "timeout." -28 dB.
File: `video/ep90b/out/ep90b-final7.mp4` (+ `-review720.mp4`, `-alt-cinematic-720.mp4` preview, `cover-ep90b.png`, `f0.png`); build `build90b7.py` (picture logic of final5, retimed to cues90b: the punchline holds 1.8 s, line 7 delayed by 4.24 s), mix `mix90b7.py`, runner `run7.sh`. Total 21.9 s (the 15-17 s target is not reachable with this voice plus the 1.8 s hold: levers as in FINAL5).
Audio: voice dominant; real-library bed `punchy--hip-hop-beat--themountain.mp3` (the hip-hop family used under ep89, no complaint) at exact length, high-passed at 140 Hz for phone speakers, 17.5 dB under the voice in 300-3500 Hz, a -4 dB tender dip under the begging card, a -18 dB near-silence during the typing dots before the punchline, groove back with a +2 dB sting, 1.2 s fade-out; sfx 17 dB under the voice rms; final mix about -14 LUFS. Alternative bed as a preview: `cinematic--dramatic--themountain.mp3` (David loved it in ep85, but dramatic). Details and numbers in `channel/music-notes.md`.
Picture: unchanged from FINAL5 (REAL CHAT card of real pixels, ME / CHATGPT tags, one badge, selection bars, soft scrolls, no wipes, no orange, pleading-face emoji to match the real recording).

---
# FINAL8 (11.11.2026) - tight rebuild after Meta AI's critique of final7 (final1-7 untouched)

File: `video/ep90b/out/ep90b-final8.mp4` (17.47 s, 2.2 MB) + `-review720.mp4`, `cover-ep90b-v8.png`, `f0-v8.png` (named so because `f0.png` is final7's), `gate-final8.txt`. Build `video/ep90b/build90b8.py` (composition built into /tmp/e8/hf8 with `bg8.png` = #FAFAF8 + faint 60 px grid, generated in that dir), mix `mix90b8.py`, runner `run8.sh`. Voice = the CURRENT `video/ep90/voice/narration90b.wav` + `cues90b.json` (line 4 "It begged, can I have a second chance?"), not re-rendered, not delayed; padded to 17.47 s.

## Changes vs final7
- 21.9 s -> 17.5 s: the 4.2 s artificial hold before line 7 is gone (the laugh reply lands WITH line 6, the end card starts with line 7), no typed letters, no typing-dots silence beat, no REAL CHAT proof card.
- Light #FAFAF8 with a very faint grid (final7 used #ecebe5 dotted). No keyboard/composer. Each user message is a dark bubble under a black ME tag that pops in at once (soft blur/scale, 0.4 s). Every ChatGPT answer sits under a black CHATGPT tag.
- One thing at a time: 47 giant (640 px, centred) under the number prompt; "Now we won't be able to talk for 47 days" then "Wait... can I have a second chance? 🥺" word by word with the voice; "Yes" then 100 ONCE (430 px, one small heart, grey because no orange); "Fahhhhh" as the user's bubble, then the laugh reply built fast with STILL on a black box (voice "still" 12.16 s, box 12.1 s); end card "Send this to / someone who / ghosts you." with "ghosts" on a black box, held static about 1 s after the last word, then the soft loop dissolve to frame 0. Scene changes are 0.16 s soft dissolves with a gap (no two scenes' text at once), no wipes.
- Frame 0 reads "I gave ChatGPT" + "a 47-day" fully, "timeout." ghosted and building with the voice; real ChatGPT badge once.

## Taken from Meta / rejected
Taken: light base + faint grid, no typing, no keyboard, 47 giant, 100 once, Fahhhhh as the user's bubble, the order, STILL and "ghosts" on black boxes, static end hold, one red-free heart. Rejected: (1) Meta's invented "You gave me a second chance and I STILL chose 100" as a ChatGPT line (we show the real reply, split over lines, and the voice says our own "And it still chose 100."); (2) the red heart: the real reply is an ORANGE heart and David's rule is no orange, so it is a small grey heart, as in finals 3-7; (3) removing the skull: it is part of the real reply, kept small, no circle; (4) 12 s length: the voice is 16 s.
Honest note on "100 once": the real laugh reply itself ends "chose 100", so the digits appear twice in the text; the giant 100 is shown once, the second is ordinary sentence text.

## Correction found while checking against the real frames
The real laugh reply uses the LOUDLY CRYING FACE (😭), not 😆 (zoomed on the recording frame at 56 s). Finals 1-7 of this version and the recording-version notes say 😆; final8 uses 😭. Any other text that says 😆 is wrong (episode-90-script.md line about the HAHAHAHA reply does not name the emoji; the 90b notes above do). The begging reply emoji 🥺 and the skull 💀 and the heart 🧡 match the recording.

## Gates (gate-final8.txt)
safe_check_hf PASS (clean at 10 px tolerance; heart 8 px and "chance" 5 px past the right line, inside tolerance; no overlaps over 10 px); qa.py --hf PASS (-14.0 LUFS, peak -4.6 dBFS, loop seam 0.6/255; the only warn is the 30-90 s band); voice_doctor PASS (only the recipe's 0.16 s gap notes); voice_quality FAIL on line 6 pitch range 10.8 st (same as final7; the voice is fixed and not re-rolled; the other lines 3.2-7.2 st; line 4 now 7.2 st), music 36% under 150 Hz, bed minus voice -14.3 dB in 300-3500 Hz at vol 0.20; check_music_bed ok (mean -17.6 dB, no quiet stretch); accent check SKIPPED (no model installed). Music: `punchy--hip-hop-beat--themountain.mp3` as final7, ducks: -4 dB under the begging line, -18 dB for 0.3 s during "Fahhhhh", +2 dB sting at the laugh. Sfx re-timed. Measured, not heard.

## Watched
Frames every 0.25 s to 3 s, 0.5 s after (360 px contact sheets, not 720; the 720 review file exists). Seen: 47 giant and centred, 100 once, no keyboard, no text-on-text overlap, nothing cut by the safe area, word builds in time with the voice. Not seen live (no playback): motion smoothness beyond frame sampling.

## Weaknesses
Fahhhhh alone is on screen only about 0.4 s (the voice leaves no room); 100 about 0.6 s; the laugh reply is fully there for about 2.6 s. Frames 0-2.5 s are text only (no picture of a chat). Still a redraw, one run, small account, voice line 6 pitch range flagged, hip-hop bed was rejected by David's ear on the voice-less versions (it is the ep89 family with the voice). Caption unchanged (no claim changed).

## Scores (judgements) and prediction
HOOK 78 | VIRALITY 72 | OVERALL 76 (Meta rated final7 72; shorter and cleaner should help, but my scores did not predict views before). PREDICTED VIEWS about 800-2,500 (ASSUMPTION), about 65-80 on the scale. Log real 48 h / 72 h next to this.

---
# FINAL9 (11.11.2026) - fill-the-frame fix on final8 (final1-8 untouched)
Files `video/ep90b/out/ep90b-final9.mp4` (17.47 s) + `-review720.mp4`, `cover-ep90b-v9.png`, `f0-v9.png`, `gate-final9.txt`; build `build90b9.py`, `mix90b9.py`, `run9.sh`. Change: every user bubble now starts centred vertically in the safe box (y 269-1248) and glides up (0.5 s, eased) when ChatGPT's answer arrives, so the bubble-only moments no longer leave the bottom 40% empty; the end card is 4 lines at 152 px (Send this / to someone / who ghosts / you.) spanning y 340-1140; "Wait..." now enters with the voice's "begged" (final8 used "It"), and a dots fade-out overlap bug (dots lingered under "Wait...") is fixed. Same gates as final8: safe_check PASS, qa PASS, voice_doctor PASS, voice_quality FAIL on line 6 (10.8 st, unchanged voice), accent SKIP. Still weak: the hook and the end card end near y 1100-1140 (about 100-150 px above the bottom of the safe box); Fahhhhh about 0.4 s; sheets viewed at 540-720 px, no live playback.
