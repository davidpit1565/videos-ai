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
