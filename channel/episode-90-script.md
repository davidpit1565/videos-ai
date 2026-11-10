# Episode 90 script: "My idea has 3 flaws. I show AI." (built 10.11.2026)

Animated version of the static meme `channel/memes-2026-11-10/v4/C.png`. A JOKE about tone, labelled so in the caption, NOT a test result: we tested only that ChatGPT tends to agree (episodes 72/73/80); Claude was never tested on this and nothing claims Claude is better. Funnel stage: TOP (meme, shareable). Build: `video/ep90/` (`build90.py`, `run.sh`, `mix90.py`, `gen.sh`). File: `video/ep90/out/ep90-final1.mp4` (1080x1920, 11.83 s, 1.7 MB) plus review copy `ep90-final1-720.mp4` (576 KB). Audio measured, not heard.

## Live product check
Not repeated for facts: the video makes no product claim, only a joke; names ChatGPT and Claude (both current names, per episodes 80/88 work). No feature or limit is stated.

## Beat sheet (times from the voice cues, D = 11.81 s)
| t (s) | Spoken | On screen |
|---|---|---|
| 0.00-2.35 | "My idea has three flaws." (0.06-2.23) | Frame 0: headline "My idea has 3 flaws. / I show AI.", cream idea card with a lightbulb and three hollow red circles, green ChatGPT and orange Claude pills with the real logos (icon only). The three circles pop red one by one on "three flaws". Card sways, pills bob, glow drifts. |
| 2.35-5.5 | "ChatGPT says: perfect idea!" (2.59-5.48) | The green pill grows into the full ChatGPT panel (golden retriever, slow zoom in), headline leaves, the idea card shrinks to a corner. Bubble "Perfect idea!" with a drawn smiley pops on "perfect", a green check stamps on the card. |
| 5.5-8.7 | "Claude says: three problems. Start with one." (5.84-8.75) | Crossfade to the orange Claude panel (tabby cat, slow push-in). Check leaves; the card moves top-left; its three marks light red one by one on "three problems"; bubble "3 problems. / Fix #1 first." pops, pulses on "one". |
| 8.7-11.4 | "Tag someone who needs the cat." (9.11-11.31) | Both panels side by side (icons only, names off), the sentence builds word by word under them, panel bump on "cat." |
| 11.4-11.81 | silence | Soft crossfade (no wipe) back to frame 0 (loop seam 2.1/255). |
No "tomorrow" line, no comment keyword (David's instruction). Text on screen at once: at most 3 (frame 0: 2 lines; ChatGPT scene: name + bubble; Claude scene: name + 2-line bubble; end: 2 lines).

## Voice
Take `a` of `video/ep90/gen.sh a 5000 0.78` (exaggeration 0.78/0.78/0.70/0.74). script_lint: 0 risky words after rewording "number one first" to "Start with one". The render needed retries on lines 1-3 (the model heard "floors", "Chai GPT", "on"); the shipped file is the build tool's accepted take. Line 2 is 2.9 s for 4 words (slow, but passes). `--watch three` reported "three: could not be measured" in the build log. Accent check SKIPPED (needs `transformers`, not installed): not a pass.

## Music and sound
`bright--upbeat--subclair.mp3` via `pick_real_track.py 11.81 --mood bright` (exact length), mean -15.5 dB, no quiet stretch, logged in `channel/music-notes.md`. 23 sfx events from `video/ep88/sfx/` (tick on each mark, pop, ding on the check, whooshes), placed from the voice cues.

## Look
Same dark navy base as C.png, bold white/yellow headline, brand-coloured (ChatGPT green #10a37f, Claude orange #d97757) headers. Real photos (Pexels, credits in the caption) and the real OpenAI and Claude marks from Commons (`channel/memes-2026-11-10/credits.md`). Inter Display (OFL). Drawn: idea card, check, smiley. Names "ChatGPT" and "Claude" sit BESIDE the icon in the panel header (as in C.png), never under it; icons alone on frame 0 and in the end scene.

## Check results (real output of `./export/check_hf.sh`, tag final1)
safe_check_hf PASS (clean at tolerance 10 px; headline within 5 px of the side lines). qa.py --hf PASS (1080x1920, 30 fps, 11.83 s, -14.6 LUFS, peak -3.3 dBFS, visual change median 0.03 s, longest 2.93 s: warns 11.8 s is outside the old 30-90 s band, intended). voice_quality PASS (pitch ranges 7.8 / 6.8 / 6.3 / 6.4 st, ends -0.1 / -0.1 / -0.3 / -0.8 st; bed -8.2 dB un-ducked). voice_doctor PASS; it flags line 3's ending (-46.8 dB vs median -29.1) and a S residual. Accent SKIP. Before the last render the first run FAILED safe_check (headline 53 px past the side lines when scaled, "Claude" panel sliding in from off-screen): fixed by a smaller headline and cross-fades instead of swipes.

## Scores (judgement, not measurement; scale in channel/score-calibration.md)
HOOK 68: subject said and shown in frame 0 (idea with flaws, two AI logos), a relatable joke, but no felt gut-level stake and the payoff is 4 s away. VIRALITY 72: a very tag-able pair of faces (dog vs cat) with a clear "send to someone" line, a loop, a tip in the caption; meme format is not proven for this account. OVERALL 70. PREDICTED VIEWS 300-1,500 (ASSUMPTION), about 55-75 on the scale. Below the 85 floor in CLAUDE.md: shipped as a build because David asked for it; our own validity test showed such scores do not predict views. Real 48 h / 72 h views go into `score-calibration.md`.

## What the blind reader should test
1. Frame 0 only + first spoken second: "what is this about?" (expect: someone showing an idea with flaws to AI; both logos named) and "would you stop scrolling, and why?"
2. After the full watch: do you get the joke without being told ChatGPT vs Claude is a test? Do you read it as "Claude is better" (we do not want that)?
3. Is "Fix #1 first" funny or just a flat line? Does the smiley read as a smiley?
4. Who would you tag? (the sendability claim)
5. Does the 2.9 s line "ChatGPT says: perfect idea!" feel slow?

## Weak spots (honest)
- Frame 0 is clear but calm: a hollow-circle card is not a gut punch; the dog is first seen only at 2.4 s. A tighter cut could open straight on the dog and cat faces.
- Motion between 0 and 2.3 s is gentle drift plus three mark pops; qa's strict metric measures 2.9 s as the longest low-change stretch (over the 2.5 s rule), my own frame-diff found no still run.
- The cat's panel has the idea card over its left ear; the third hollow mark on frame 0 sits right at the card edge.
- Line 2 is slow; line 3 ending is soft by voice_doctor.
- The "Perfect idea!" joke is a generalisation; the Claude side is untested by us (the caption says so).
- Blind reader NOT run (no agent tool here); no listening, no second human viewing: the rendered file was inspected only as contact sheets plus frame 0, not watched twice.

---
# REVISION final2 (10.11.2026): frame 0 is the meme
`video/ep90/out/ep90-final2.mp4` (10.90 s, 1.4 MB) + `ep90-final2-720.mp4` (423 KB). final1 is untouched. Build: `video/ep90/build90b.py`, `run2.sh`, `mix90b.py`, `hf2/` (reads `lines2.txt`, `voice/src2.json`). Audio measured, not heard.

## What changed
- Frame 0 now: headline "My idea has 3 flaws. / I show AI." plus both photos side by side, large (dog in a green-headed panel left, cat in an orange-headed panel right, real logos as icons in the headers, no names), panels y 540-1245, nothing empty inside the safe box.
- Beats (D = 10.88 s): 0-2.4 s photos drift, "3 flaws" bumps, the small idea chip pops in on the seam at ~0.4 s and its 3 marks turn red on "three flaws"; 2.4 s dog panel punches in (photo zoom 1.0 to ~1.3, panel grows upward, cat dims), "Perfect idea!" + smiley bubble pops on "perfect" (2.6 s), green check on the chip; 4.9 s cat punches in, dog dims, the chip's marks light red one by one on "three", bubble "3 problems. / Fix #1 first." pops; 8.2 s headline becomes "Tag someone who needs the cat." word by word, both panels bright again, bump on "cat."; last 0.45 s the same scene eases back to the frame-0 pose (no wipe, no copy).
- Deviation from the request: the "Perfect idea!" bubble is at ~2.6 s, not 0.8 s, because it is synced to the spoken line (a bubble 1.8 s before the voice says it would read as a mistake). 0-2.4 s is carried by the chip and the three marks instead.
- Voice: first word stamp at 0.00 s (line cue 0.06 s). Line 2 re-rendered as "ChatGPT: perfect idea!" (`voice/b.wav`, 2.11 s instead of 2.89 s). A shorter "Claude: three problems. Start with one." was rendered too (3.18 s, longer, retries heard "Clyde") and NOT used; line 3 stays the old take "Claude says: ..." (2.91 s). Lines 1, 3, 4 are the final1 takes.
- Music: `bright--feel-good-beat--tunetank.mp3` at exactly 10.88 s, mean -21.7 dB, no quiet stretch (quiet bed, only 1% under 150 Hz). Logged in `music-notes.md`.

## Check results (`check_hf.sh`, tag final2, real output)
safe_check_hf PASS (clean, no overlaps; two earlier failures fixed: headline and tag text overlapped during the loop-back, and a fromTo that hid the headline at frame 0, caught by looking at the sheet). qa.py --hf PASS: 10.9 s, -14.6 LUFS, peak -3.4 dBFS, visual change median 0.03 s, LONGEST STILL 2.13 s (was 2.93 s), loop seam 1.5/255. voice_quality PASS: pitch ranges 7.8 / 4.2 / 6.3 / 6.4 st, ends -0.1 / -0.1 / -0.3 / -0.9 st, bed -7.3 dB un-ducked at volume 0.50. voice_doctor PASS but flags line 3's ending (-40.0 dB vs median -26.7) and line 2's pitch range of 4.2 st is the flattest line (his liked lines sit at 4.9-8.4). Accent check SKIP (transformers not installed).

## Scores (judgement) for final2
HOOK 74 (the meme is on frame 0 and the subject is stated, dog vs cat is instantly legible), VIRALITY 74, OVERALL 73, PREDICTED VIEWS 400-1,800 (ASSUMPTION), about 58-78 on the scale. Still under the 85 floor; a joke build requested by David.

## Still weak
- The bubble/payoff comes at 2.6 s, not at the start; 0-2.4 s is photos + chip only.
- The chip covers the cat's ears and the dog's forehead area at the seam; the "3 flaws" bump leaves a brief uneven space after "has".
- No names under or beside the icons (icons and colours only), so a viewer who does not know the Claude mark relies on the voice.
- Line 3 ending is soft by voice_doctor; line 2 is flat in pitch; the Claude cat-side remains an untested joke (caption says so). Not watched twice by a human, blind reader not run, audio not heard.

## Blind reader on final2 frame 0 (10.11.2026, fresh agent)
- A) Unclear: a dog and a cat under ChatGPT and an orange logo, "My idea has 3 flaws. I show AI."; does not know what idea or what the animals have to do with it. B) No, would not stop: generic cute-animal AI content, nothing at stake. C) Expects a dog-vs-cat comparison. D) "I show AI" reads oddly; whose idea; animals look like stock photos; orange logo unrecognisable; bottom third dead; dark gradient looks like every AI channel. E) State the actual idea in big words, make the animals react to it.
- Action: final3 requested with a concrete silly idea in the headline, names beside the icons, animal reactions.

---
# REVISION final3 (10.11.2026): the idea is on screen, animals react
`video/ep90/out/ep90-final3.mp4` (12.27 s, 1.7 MB) + `ep90-final3-720.mp4` (532 KB). final1 and final2 untouched. Build: `video/ep90/build90c.py`, `run3.sh`, `mix90c.py`, `hf3/` (`lines3.txt`, `voice/src3.json`). Audio measured, not heard.

Why: the blind reader on final2 frame 0 (a 17-year-old) did not understand what the idea was or what the animals had to do with it, would not stop, found "I show AI" odd and the orange logo unrecognisable.

## What changed
- Headline (frame 0, three lines, present tense, no company named): "My idea: / sell ice to penguins. / AI, rate this." The "3 flaws" now only live in the answers ("3 problems."). I did NOT use "Uber for socks" because Uber is a real company (your rule: no real company named).
- Line 1 spoken: "My idea: sell ice to penguins. AI, rate this." (new take `voice/c.wav`, 3.5 s, one render at a time). "rate it" was heard as "rated"/"raided it" in 3 takes (flapped T), so it became "rate this". Lines 2, 3, 4 are the final2 takes. Word stamp of the first word 0.00 s.
- Panel headers now carry the NAME beside the icon ("ChatGPT", "Claude"), never under it.
- Panels run y 575-1245 on frame 0 (to y 1245 at the platform line); nothing important below; no new decorations.
- Reactions: the dog tilts its head on "penguins", bounces and wiggles on "Perfect idea!" with a green check; the cat tilts slowly in the first part, then squints (fast push-in to 1.55 with a small tilt) on "problems", the idea chip with 3 marks pops in and the marks light red one by one on "three". Words in the headline bump as they are spoken. Headline shrinks to the yellow idea line while the panels grow, then becomes "Tag someone who needs the cat."; ends easing back to frame 0 (loop seam 1.5/255).

## Check results (`check_hf.sh`, tag final3)
safe_check_hf PASS (clean). qa.py --hf PASS: 12.27 s, -14.4 LUFS, peak -3.2 dBFS, visual change median 0.03 s, longest still 2.07 s, loop seam 1.5/255. voice_quality PASS: pitch ranges 5.6 / 4.2 / 6.3 / 6.4 st, ends -0.3 / -0.1 / -0.3 / -0.8 st; bed -7.4 dB un-ducked at volume 0.46. voice_doctor: nothing flagged. Accent check SKIP (transformers not installed). Music `upbeat-energetic--lnplusmusic.mp3` at 12.24 s, mean -23.8 dB (quiet), logged. Fixed on the way: headline blocks overflowed the side line when scaled (fit-content), the idea chip popped from the wrong origin and left the panel.

## Scores (judgement, not measurement)
HOOK 78 (the idea is stated in big words and spoken, the two faces are on frame 0), VIRALITY 74, OVERALL 75, PREDICTED VIEWS 400-1,800 (ASSUMPTION). Under the 85 floor. Real views go into score-calibration.md.

## Still weak
- 12.27 s, over the 11 s target (line 1 alone is 3.5 s); under the 13 s cap.
- First 3.8 s has only head tilts, word bumps and slow push-ins; no big visual event until the dog punches in at 3.8 s.
- Five text items on frame 0 (3 headline lines + 2 header names), over the "max 3 lines" rule; the names were requested.
- Panels sit close under the headline (about 15 px).
- Line 2 is flat in pitch (4.2 st); the bed is very quiet in the file and has almost no bass; the Claude side is an untested joke (caption says so). Blind reader not re-run on final3, not watched twice, audio not heard.

## Blind reader on final3 frame 0 (10.11.2026, fresh agent)
- A) Understands: someone pitches a joke idea and wants AI to rate it; ChatGPT and Claude shown as a dog and a cat. B) No, would not stop: reads as a random meme, nothing at stake. C) Expects ChatGPT to gush and Claude to be sarcastic (what the video does). D) Ice-to-penguins is an old joke; stock-looking photos; generic dark gradient; empty bottom half. E) Show a real chat screen with both replies visible.
- Verdict: comprehension fixed, stopping power still missing; a real chat screen (David's recording) is the only change the reader asks for.
