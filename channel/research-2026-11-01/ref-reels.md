# ref-reels: measured comparison, insiderforce vs Dan Martell vs our ep 81 (1.11.2026)

Labels: FACT = measured here with ffmpeg + numpy, or read on a frame. HYPOTHESIS = my reading, not proven. UNKNOWN = could not be measured.
No Firecrawl used. Nothing committed, published or sent. No voice model started.

## 0. What I actually measured (and what I could not)

| Clip | File | Spec | How obtained |
|---|---|---|---|
| insiderforce "5 Secret Claude Codes" | `/tmp/claude-0/-home-user-videos-ai/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/scratchpad/refreels/dl/if.mp4` | 576x1024, 30 fps, 61.4 s, AAC audio | FACT: the earlier session only had 4 contact sheets (WhatsApp 384x848). `yt-dlp` failed on TikTok ("Unexpected response from webpage"). I opened `tiktok.com/player/v1/<id>` in the global Playwright, read the `video/mp4` 206 response URL and fetched it with the browser context (script: `.../refreels/js/dl.js`). Clean video, no TikTok UI on it. |
| Dan Martell (Facebook) | `.../scratchpad/fbref/ref.mp4` | 1080x1920, 29.97 fps, 29.07 s | FACT: already downloaded earlier |
| our ep 81 | `/home/user/videos-ai/studio/public/reels/reel-81.mp4` | 1080x1920, 30 fps, 25.27 s | FACT: same size in bytes (17,946,753) as `scratchpad/v6/out/ep81-C-final-music1.mp4` |

Method: each clip decoded to 30 fps RGB at 144x256 (if), 108x192 (fb, ep81), saved as `.npy` in `.../refreels/out/`. "Screen moving" = share of pixels whose luma changes by more than 12 levels versus the previous frame. Sheets at 0.4-0.5 s steps in `.../refreels/out/*.png`. Scripts in `.../refreels/py/`.
Limits (UNKNOWN / not measured): views of insiderforce (only likes 42.3K, comments 3,237, shares 11.8K seen on the player; saves 48K from the earlier sheet); whether insiderforce has a voice-over (audio is a flat -13.2 LUFS, loudness range 1.2 LU, which reads as a music bed only: HYPOTHESIS); no OCR installed, so word timings come from ink counts and frame-by-frame sheets (accuracy about one frame = 0.033 s where I give 2-3 decimals, about 0.2 s where I say "about"). These three reels are survivors: they say nothing about how often this style fails.

## 1. insiderforce, measured (FACT unless marked)

Structure (61.4 s): hook 0-2.87 s, then five tip blocks that start at wipes 2.87 / 10.60 / 21.10 / 28.97 / 38.47 s, then CTA from 47.03 s (hard cut) to 61.4 s.
- Tip block lengths: 7.7, 10.5, 7.9, 9.5, 8.6 s (mean 8.8 s). Tips 2 and 5 contain a 3-4 s beat with a real dark product screenshot (slides in from the top, 2-3 bullets build on the left); tips 1, 3, 4 do not.
- Every block repeats one template: "#N" (the digit arrives 0.3 s after the "#") + command name that scrambles into place ("/ghost", about 0.5-0.7 s, estimate from 0.067-s tiles) -> dark prompt card slides in, black tag with the command, a dashed curve joins tag and card, headline "drop it before your PROMPT" builds -> result line "Claude gives you a FULLY HUMANIZED answer" -> blur-out -> payoff line "one that even passes AI DETECTORS" (letters scramble 0.4 s) -> next wipe. About 4-5 distinct compositions per 10 s.
- Hook timeline: blank grid until 0.27 s (7 frames), "5" at 0.27, "SECRET" 0.5, "claude codes" 0.87-1.2, black selection bar with white "nobody is talking about" fills 1.47-2.0 s (23 characters in about 0.5 s, about 45 characters/s, a wipe-reveal and not human-speed typing), holds 0.8 s, wipe at 2.87.
- Word cadence on the result line (2-frame tiles, 6.5-7.4 s): Claude, gives, you, a, FULLY, HUMANIZED, answer = 7 words in about 0.9 s = 0.13-0.17 s per word (about 7 words/s). The finished line then holds about 0.9 s (7.5 -> 8.37 s) and leaves as one unit through a blur.
- One word's entrance (the last word "answer", full-res frames): it rises 27 px of 1024 (2.6% of the height) while fading in over 5-6 frames (7.33 -> 7.50 s = 0.17 s); the steps are 6,6,6,5,4 px, so a plain ease-out with no overshoot.
- While the text holds, the whole block keeps drifting down about 5 px/s of 1024 (0.5% of the height per second): rows 728 -> 732 in 0.77 s. Measured on one line only.
- Transitions: black, blurred, spiky star wipes from alternating corners. The first one lasts 1.93 s (corner-dark pixels 2.87-4.80 s, peak 21% of the corner area); the old text is gone within 0.07-0.13 s (2-4 frames) under it, then "#" and the digit arrive. Sharpness dips below 55% of the median in 18 runs of 0.3-1.4 s, 11.8 s in total = 19% of the runtime. Real hard cuts (more than 35% of the screen changing in one frame): 6 in 61.4 s (8.4, 16.2, 21.1, 43.57, 47.03, 51.3 s), only one over 60% (47.03 s, into the "Comment HUMAN" ask).
- Screen movement: mean 4.20% of pixels per frame (median 2.18%). Per 10 s: 4.64, 5.69, 4.18, 2.61, 4.41, 4.25 %. Runs of at least 1 s with under 1% moving: 8, together 10.4 s = 17% of the video, longest 2.43 s (58.9 s, the final fade).
- Text size (share of frame height, 1024 px): key word "PROMPT" and "5 SECRET" blocks 6.4% (about 123 px at 1920); light connector words ("drop it before your") 4.1%; "FULLY HUMANIZED" 4.4%; smallest text meant to be read 3.6-4.1%; card text about 1% (decorative, not meant to be read). Key words about 80% of the width.
- Emphasis: weight and size only (heavy caps next to light small words), never colour. The only colour in the video is the coral asterisk (and a small coral line in the ebook): saturated pixels = 0.04% of all pixels sampled.
- Palette (modal values): background #EBEBEB (235,235,235) = 75.7% of pixels, ink #121212, card about #282828, lighter greys #D8D8D8/#C8C8C8 (grid, shadows), coral asterisk about #C57468 (measured median of anti-aliased pixels at 144x256, so approximate), watermark "insiderforce.io" light grey at the bottom, on every frame.
- Grid: dashed lines with darker cross points, pitch about 68 px of 576 wide (11.8% of the width, about 127 px at 1080) horizontally and 59 px of 1024 (5.8% of the height, about 111 px at 1920) vertically; darkest point luma 187 on 235. The grid does not move (during holds under 1% of pixels change).
- Payoff timing: the first command name is fully on screen at about 4.8 s (8% in), the first "what it does" line is complete at 7.5 s (12%). The same structure repeats five times, so a viewer who sees the first payoff has seen the format by 12%.
- CTA: "Comment HUMAN" ask at 47.0 s (77% in), book mock-up, "I'll send you my ebook", then "make sure you Follow InsiderForce" from about 53.5 s, fade to black over the last 2.5 s (58.9-61.4 s).
- Audio: -13.2 LUFS, loudness range 1.2 LU, per-second level 5 dB spread (-11 to -16 dB), no gaps. No clear beat found by autocorrelation (best candidate about 95 bpm at 3% strength: UNKNOWN).

## 2. Dan Martell (Facebook, 29.07 s, 5M views as given by David's brief)

- Talking head, not faceless: presenter plus 2-3 word captions at the bottom centre, each held about 0.5-1.0 s (from 0.5-s tiles, estimate), and screen recordings from about 13 s. ChatGPT logo shown at 0-2.4 s.
- Screen movement: mean 6.58% of pixels per frame (median 4.77%); 98% of 0.5-s windows have over 1% moving; longest quiet run 0.47 s. Per 10 s: 8.21, 5.83, 5.62 %.
- Cuts: 8 distinct events at 1.8, 2.4, 4.9, 8.2, 9.3, 13.0, 16.7, 26.1-26.2 s with the ffmpeg scene filter at 0.12, so about 2.8 per 10 s, plus punch-in framing changes that the filter does not count (visible on the sheet).
- Palette: bright, photographic (blue shirt #184868 region 7%, wall beige-green), white screen cards. No fixed identity colour.
- Payoff: "here's how I reprogram it" at about 6.5 s (22%), screen steps from 13 s (45%), final line "that's how you finally get the AI to be direct with you" at about 25 s. No CTA.

## 3. Our ep 81 against the loved reference (same metrics)

| Metric | insiderforce | ep 81 | Difference |
|---|---|---|---|
| Length | 61.4 s | 25.27 s | ep 81 is 59% shorter (Dan: 29.07 s, ep 81 is 13% shorter) |
| Mean screen change per frame | 4.20% | 2.01% | ep 81 is 52% lower (Dan 6.58%) |
| Median screen change | 2.18% | 0.41% | 81% lower |
| Per 10 s windows | 4.6 / 5.7 / 4.2 / 2.6 / 4.4 / 4.3 | 4.18 / 0.69 / 0.37 (20-25.3 s) | ep 81 holds the reference level only for the first 10 s, then falls 83-91% |
| Time in still runs (under 1% moving, 1 s or longer) | 17%, longest 2.4 s | 50%, longest 5.2 s (15.6-20.8 s) | 3x the still time, 2x the longest still |
| Scene changes per 10 s (sharpness dips) | about 2.8 (17 dips, includes blur-outs inside a block) | 1.2 (3 dips: 2.43, 5.1, 8.87 s) | less than half |
| Time in blur/wipe state | 19% | 11% (2.8 s) | 8 points lower |
| Type of transition | star-shaped black wipe + blur, 1.9 s, content swapped in 0.07-0.13 s | crossfade/blur dissolve, 0.77-0.87 s, no shape | different signature |
| Key-word size | 6.4% of height | 7.8-8.2% in the hook, 9% on "REPROGRAM" | ours 25-40% bigger (fine) |
| Smallest standing text | 3.6-4.1% | 2.1-2.6% (the caption above the phone, 9-25 s) | ours 40-45% smaller; this is 65% of the runtime |
| Share of runtime where the phone fills 40% of the height | 0% (card is decoration, real screenshot 2 of 5 blocks) | 65% (8.9-25.3 s) | |
| Word build speed (result line) | 7 words/s (0.13-0.17 s per word) | about 3.3 words/s (0.1-0.4 s gaps, follows the voice) | ours 2x slower; but ours is voice-locked |
| Emphasis method | weight + size, no colour | lime highlight bar + size | |
| Saturated-colour pixels | 0.04% | 2.76% (lime + green logo wallpaper; pale-lime wallpaper bins about 13% of pixels) | 69x more colour; wallpaper is a busy pattern behind text, the reference has a faint static grid only |
| Background | #EBEBEB, grid static | #F7F7F2 cream (50.6% of pixels), dot grid drifting at 216 px over the video (from build file, FACT), big logo wallpaper | |
| First frame | blank grid until 0.27 s | content already on frame 0 | |
| Payoff: first concrete deliverable on screen | 4.8 s (8%) command, 7.5 s (12%) "what it does" | settings walkthrough starts 8.9 s (35%), the text you must copy is typed 15.6-20.8 s (62-82%) | ours arrives 3x later in relative terms |
| CTA | ask at 77%, 14.4 s of CTA, fade to black | none (David's decision); ends on the "Saved" screen | |
| Audio loudness | -13.2 LUFS, LRA 1.2 | not re-measured here | |

Other things seen on ep 81 (HYPOTHESIS about effect): an outlined double-image of "AGREES" at about 4.7-5.1 s (the zoom-through) can read as a glitch; the line "AGREES with you on everything." stays complete for only about 0.85 s before the exit.

## 4. Rules that would make our reels look like the loved reference

Each rule says how to test it. Numbers are the reference's, converted to 1080x1920 where I say so. Rules 1-3 are about structure; the "(H)" tag marks a rule that rests on one clip and needs a test of its own.

1. One template per tip, repeated: [#N + command, about 2 s] -> [prop card + headline, about 3 s] -> [result line, about 1.5 s] -> [payoff line, about 2 s]. Block length 7.5-10.5 s. Test: block boundaries (wipes) every 8.8 s +/- 1.7 s.
2. Hook is finished by 2.9 s: heavy two-word line, light subline, one black selection bar with white text filling in 0.5 s (about 45 characters/s). First ink at or before 0.3 s. Test: ink count reaches the hook's full value by 2.0 s, wipe starts at 2.8-2.9 s.
3. First concrete deliverable (command name, step 1) fully on screen by 8% of the runtime and the first "what it does" line by 12% (for 61 s: 4.8 s and 7.5 s; for a 25-s reel: 2 s and 3 s). Test: timestamp of the first command/tag.
4. Screen motion floor: at least 4% of pixels change per frame on average in every 10-s window, none below 2.5%. Test: `py/m.py` metric; ep 81 fails with 0.69% and 0.37% in 10-25 s.
5. No still stretch longer than 2.5 s (under 1% of pixels moving), and no more than 17% of the runtime in still runs of 1 s or longer. Test: same metric; ep 81 has 5.2 s and 50%.
6. A new element enters (word, tag, card, bullet, screenshot) at least every 1.2 s. Test: count ink-onset events per second. UNKNOWN: the reference's exact rate; my estimate from the sheets is about one onset per 0.8-1.2 s. (H)
7. Word build: a line is complete within 1.0 s of its first word (about 7 words/s), then holds 0.7-1.0 s, then leaves as one unit. If the voice is slower, start the line early or cut it to at most 5 words; do not stretch the build to the voice. Tension with our "picture follows narration" rule: this needs David's call. Test: first-to-last word time per line is at most 1.0 s.
8. Word entrance: rise about 2.6% of the height (about 50 px at 1920) while fading from 0 to 100% in 0.17 s (5 frames), ease-out, no overshoot. Test: track a word's first-row y and ink over frames.
9. Emphasis by weight and size only: key word heavy caps at 6.4% of the height (about 123 px block at 1920), connector words light and 4.1% (about 79 px). One key phrase per line, no colour change. Test: key/connector height ratio is 1.5-1.7.
10. Text floor: any text meant to be read is at least 3.6% of the height (about 69 px at 1920) and any prop text that is not meant to be read is at most 1% of the height. Ep 81's 2.1-2.6% caption fails this.
11. Colour: background #EBEBEB (+/- 3 levels), ink #121212, card #282828, one accent colour used for one small object. At least 99.5% of pixels neutral grey on non-product frames. Ep 81 (2.76% saturated, lime wallpaper) fails. If lime must stay, make it one fill under one word (bar), not a wallpaper. Test: saturated-pixel share per frame.
12. Background: a faint static dashed grid, pitch 11.8% of the width x 5.8% of the height (about 127 x 111 px), darkest point about 50 levels below the background. No drift, no wallpaper. Test: during a hold, under 1% of pixels change outside the text. (H: the reference grid does not move; whether a moving grid hurts is not tested.)
13. Transition signature: one black, blurred, spiky star wipe per section from alternating corners, 1.9 s long, the old content swapped out in at most 4 frames (0.13 s) under it, then the new "#N" starts. Blur dip below 55% sharpness lasts 0.7-1.2 s. About 19% of the runtime is blur/wipe. Test: low-sharpness runs of 0.7-1.2 s at each block boundary. Draw our own spike shape; do not copy their artwork.
14. Do not use a plain crossfade as the main transition: ep 81's 0.77-0.87 s dissolves are the main difference in look. Test: at a boundary, the frame sequence has a dark shape covering at least 15% of a corner.
15. Keep a slow constant drift on holding text: about 0.5% of the height per second (about 10 px/s at 1920) so no frame is perfectly frozen. Measured on one line (H). Test: block y shifts at least 5 px/s of 1024 while holding.
16. Prop card: dark card about 80% of the width x 11% of the height, soft feathered shadow, slides in; a black tag (white text, about 4% of the height) with the command sits above it, joined by a dashed curve. The card text is decoration. If we want the viewer to copy the prompt, add a separate legible beat of at least 2.5 s at 3.6% or more (this is not in the reference: the reference sells the full text behind "Comment HUMAN").
17. Real product screenshot in 2 of every 5 blocks (40%), as a tall dark panel that slides in from the top for 3-4 s with 2-3 bullets building at the side. Test: share of blocks with a real screen; ep 81 has the phone for 65% of runtime instead, which is the opposite pattern.
18. Never hold a phone mock-up on screen for more than 5 s without a layout change; ep 81 held it 16.4 s. Test: longest run in which more than 80% of the same pixels persist.
19. Command/number scramble: a 6-character command resolves from jittering letters in 0.5-0.7 s; the "#" appears first and the digit follows 0.3 s later (rising 0.33 s). (H, estimate from tiles)
20. Standing mark: small light-grey wordmark on every frame at the same place (bottom, inside the platform's unsafe band, decorative). For ours: on full-bleed screen frames keep the existing rule (drop the handle).
21. Section count: a numbered finite list of 5 is the whole video (reference: 5 tips in 47 s + 14.4 s CTA). If our reel is a single trick, split it into 3-5 numbered beats of the same template instead of one 16-s phone scene. (H: whether 3 beats are enough is untested.)
22. CTA as its own beat from 75-77% of the runtime: one object (book/ebook), a two-line ask, then logo + follow line, fade to black over the last 2.5 s. For us, an ask for a send (style-research decision 4) could take the place of the comment ask: not measured, UNKNOWN which converts better on Instagram.
23. Audio bed: continuous, -13 to -14 LUFS, per-second level within a 5 dB band, no gap over 1 s, no clipping (their true peak was +1.3 dBFS, which we should not copy; our -1 dBTP rule stays). Test: `audio/check_music_bed.py` plus per-second RMS.
24. Blank first frame is allowed for 0.27 s in the reference (grid only); our qa.py wants content at frame 0. Keep our rule; open the hook at 0.0-0.3 s with the first heavy word already rising. (Decision for David: no evidence either way.)
25. Do the check on the frames, not the numbers: after any change, rebuild the two sheets (`py/sheet.py`) at 0.4 s and compare the sequence of compositions with the reference sheet (`out/if_0.0_12.0.png`). If our sheet shows the same layout for three tiles in a row (1.2 s) outside a read beat, it fails rule 4-6.

## 5. What this does not prove

- FACT: these numbers describe the style David likes. HYPOTHESIS: matching them raises views. UNKNOWN: insiderforce's view count and why it spread (the caption funnel "comment HUMAN", an ebook, and the account size could be the cause; no number here separates style from those).
- Ep 81 reached about 200+ views with the lower-motion style, ep 80 got 786; one reel is not a test.
- Time stamps from sheets are accurate to about 0.2 s unless I gave two decimals.
