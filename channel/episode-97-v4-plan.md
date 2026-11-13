# Episode 97 v4 plan: from "four boxes" to a quiz (13.11.2026)

Status: PLAN only. Nothing built, voiced or published. Replaces the v3 concept (`episode-97-script.md`, `video/ep97/build97.py`: four equal boxes, hook "Four Claude AIs. One pelican. Watch it level up.").

David's feedback on v3: (1) the hook "4 Claude AIs..." starts with a number that sounds like a list item, it is too long and not instantly clear; (2) four pictures in a row is boring, "the content may be good, the virality is not"; (3) not just four boxes on screen.

## 0. What the real material actually contains (checked by rendering every SVG with Playwright and reading the SVG source)

Prompt, unchanged, to four models as Claude Code sub-agents: "Draw a pelican riding a bicycle." One try per model per run, two runs.

| Model (from the run logs) | Run 1 file | Run 2 file (`*-r2.svg`) |
|---|---|---|
| claude-haiku-5-5 | No saddle (bird lies on the top tube), no spokes, one leg to the crank, a teal scarf, motion lines, plain pale background, a ground line | Saddle (mostly hidden under the body), spokes, one leg to the crank, sky + grass, NO sun, NO road. 2,940 bytes |
| claude-sonnet-5-5 | Saddle, both legs on the pedals, wing on the handlebar, wheels with no spokes, grass, no sun | SUN, sky + grass, wing reaching the handlebar, wheels with NO spokes, NO road. 3,133 bytes |
| Opus | claude-opus-5 (older Opus 5, not 5.5): saddle, spokes, chain, crest, motion lines, no sun | claude-opus-5-5: SUN, a grey ROAD, motion (speed) lines, spokes, chainring, crest, wing on the handlebar. 3,889 bytes |
| claude-fable-5-2 | Sun, ground shadow, spokes, chain, saddle, crest | SUN, three CLOUDS, a ground SHADOW (ellipse under the bike), a road, speed lines, spokes, chainring, a sky that fades from blue to pale cream. 5,053 bytes |

Not claimable: "the sky is a sunset" (it is a pale cream fade, not a sunset), "Sonnet's pedals float" (they connect to a thin crank), anything about intelligence (Willison himself: the test does not measure every capability).

### Which run to show: RUN 2, and why it is not cherry-picking
- Run 2 is the only run where all four are the CURRENT versions: run 1's "Opus" resolved to the older Opus 5. Showing "Opus 5" next to "Fable 5.2" invites a fair "why not Opus 5.5?" comment.
- Run 2 is the LESS dramatic run (Haiku draws a seat and spokes; the gap is smaller). We pick the run that hurts our story, not the one that helps it. A smaller gap also makes the guess harder, which is what the quiz needs.
- Disclose in the caption: "One try per model, no retries. We ran it twice; this is run 2 (all current versions). Run 1 is on the episode page." Put both runs side by side on `/e/97`. Also say it ran through Claude Code agents, not the chat app.

## A. Three concepts on the same real material

Concept checklist (CLAUDE.md, 4.11.2026): (1) happening to the viewer, (2) a curiosity gap only the video closes, (3) something worth saving, (4) a named person to send it to, (5) a reason to watch twice, (6) checkable by a stranger in 30 s. Scores are judgements, not measurements; my scores do not predict views (Spearman -0.23), so they are labels, not gates.

### Concept 1: "Guess the newest Claude" (hidden-label quiz) - RECOMMENDED
Four drawings, labels hidden as A B C D in a SHUFFLED order (the newest is NOT last), each one gets a short moment on one big stage, then a 1.5 s visible countdown ("pause, comment your letter"), then the reveal from smallest to newest, Fable last. Ends on a screenshot-able ladder card, loops to the hidden deck.
- (1) partial: the AI they use, not their own account; (2) STRONG: which letter is the newest; (3) yes: ladder card with the exact request; (4) yes: a challenge send ("see if they get it"); (5) STRONG: rewatch to check your guess before the reveal; (6) yes: request on screen, paste it into Claude.
- Mechanic: a guess costs one letter in the comments; our account has 0 comments on 46 of 50 reels, and a one-letter answer is the cheapest comment there is.
- Scores (judgement): HOOK 82 | VIRALITY 78 | OVERALL 78 | PREDICTED 400-2,500 views.

### Concept 2: "One pelican levels up" (one stage, morphing ladder)
One big stage; the same pelican swaps in place Haiku -> Sonnet -> Opus 5.5 -> Fable, each swap ticks a feature checklist on the side (sun, road, speed lines, clouds, shadow) and a real counter of the code each model wrote (2,940 -> 3,133 -> 3,889 -> 5,053 bytes: rising in run 2, a true number). Ask: "Which level would you post?"
- (1) partial; (2) weak (you can see where it goes); (3) yes (checklist card); (4) weak; (5) weak; (6) yes.
- Scores: HOOK 70 | VIRALITY 62 | OVERALL 66 | PREDICTED 200-700. It is v3 with better motion: still "watch it get better", no question for the viewer.

### Concept 3: "Pelican face-off" (bracket, pick left or right)
Two pairs on a split stage (Haiku vs Sonnet, Opus 5.5 vs Fable), the viewer picks a side for each, winners meet in a final; labels hidden until the end.
- (1) partial; (2) medium (three small gaps instead of one big one); (3) yes (bracket card); (4) medium; (5) medium; (6) yes.
- Scores: HOOK 72 | VIRALITY 68 | OVERALL 68 | PREDICTED 250-1,000. Three votes is too much work in 20 s and splits the stage in half again (two boxes instead of four).

## B. Recommendation: Concept 1, "Guess the newest Claude"

### Hook
- Spoken line 1: **"Guess the newest Claude."** (4 words; the task "guess the newest" in words 1-3, the subject "Claude" in word 4; present tense; no number at the start; no THR/TR/DR words).
- Line 2 names all four at once without a list-number opening: "Same request, four Claude models: a pelican on a bike." ("four" sits mid-sentence, so it cannot sound like "4.")
- Alternatives for a blind-reader comparison BEFORE voicing (rule of 13.11): (b) "Which Claude is the newest?" (c) "Claude has four models. Spot the newest." Ask two fresh agents the two questions (what is it about / would you stop) on frame 0 + first second, log it in the script file.

### Frame 0 (what is shown at 0.0 s, at full contrast, already moving)
- Top (y 285-430): headline, 2 lines, heavy black: **GUESS THE NEWEST / CLAUDE** with the real Claude mark (`assets/claude-mark.svg`) before "CLAUDE".
- Under it, one line chip (y 440-490): "4 models · same request: a pelican on a bike".
- Stage (y 500-1248): the four real drawings as a hand of taped paper cards, fanned and overlapping (rotations -7, -2, 3, 8 degrees; card A in front, slightly larger), each with a big single-letter tape tab A/B/C/D. NO model names visible. Motion from frame 0: the fan breathes (each card drifts 6-10 px out of phase) and card A is already sliding up toward the stage.
- Text count: 3 lines (headline 2 + chip 1). Letters on tapes are labels, not lines.

### Shuffled letters (fixed, used everywhere)
A = Opus 5.5, B = Haiku 5.5, C = Fable 5.2, D = Sonnet 5.5. (Newest is C, not the last card shown; the two most detailed, A and C, are far apart so the guess is a real argument.)

### Beat sheet (estimated from 2.6-2.8 words/s with `--gap 0.06 --long 0.15 --max-speedup 1.45`; final times come from the cues)

| Time | Spoken | Shown | Motion |
|---|---|---|---|
| 0.0-1.35 | L1 "Guess the newest Claude." | Frame 0 as above | Fan breathes; on "newest" the headline word pulses (scale 1.04, eased); card A lifts out of the fan |
| 1.4-2.8 | L2 starts "Same request, four Claude models..." | Card A flies to the BIG STAGE (950 x 712, x 65-1015, y 470-1182, rotated -1.5 deg, tape on two corners); the other three shrink into a lineup tray along the bottom (y 1190-1248, 4 small cards, the active slot lit) | Fly-in 0.45 s power3.inOut; on stage a slow push-in 1.00 -> 1.04 |
| 2.8-4.2 | "...a pelican on a bike." | Card B swaps onto the stage | Card A slides back into the tray while B rises (overlapping, no hard cut); tray slot B lights |
| 4.2-5.4 | L3 "Pause, and comment your letter." | Card C on stage | Same swap, eased |
| 5.4-6.4 | (end of L3) | Card D on stage | Same swap |
| 6.4-7.9 | (no voice: ticks + music) | All four as a scattered taped collage (not a grid: unequal sizes 430-520 px wide, rotations -5/4/-3/6, 20-40 px overlaps), big countdown disc centre "3 2 1" in Claude orange, chip "comment A, B, C or D" | Each number scales in 0.9 -> 1.0 and fades; the cards jiggle 1-2 deg on every tick; tick SFX on each number |
| 8.0-9.9 | L4 "B is Haiku, the smallest: no sun." | B returns to the stage; a rubber stamp "HAIKU 5.5 · SMALLEST" lands at the top-left of the card; a hand-drawn dashed empty circle in B's sky with "no sun" | Stamp drops scale 1.3 -> 1.0, rotate -6 deg, soft settle; dashed circle draws itself (stroke-dashoffset 0.5 s) |
| 10.0-12.0 | L5 "D adds a sun. A adds a road." | D on stage (stamp "SONNET 5.5"), ring around its sun; at "A" a fast swap to A (stamp "OPUS 5.5"), ring along its grey road | Two eased swaps inside one line; rings drawn over 0.4 s each, measured on the SVG coordinates (Sonnet sun cx 680 cy 90 r 46 of 800x600; Opus road y 372-386 of 600x450) |
| 12.1-14.3 | L6 "C is Fable, the newest: clouds and a shadow." | C on stage (stamp "FABLE 5.2 · NEWEST", the only stamp in Claude orange), rings on the clouds (cx 150/190/480) then on the ground shadow (y 504) | Stage push-in 1.00 -> 1.08 for the payoff; one soft impact SFX on "newest" |
| 14.3-17.0 | L7 "Send it to a buddy. See if they get it." | Ladder card (screenshot-able): title "SAME REQUEST, 4 CLAUDES", the exact request in quotes, four thumbnails stepping up left-to-right like stairs, smallest to newest, each with its letter, model name and what it adds (Haiku: start / Sonnet: + sun / Opus 5.5: + road / Fable 5.2: + clouds, shadow) | Thumbnails climb in one by one (0.18 s stagger), a small pelican icon is NOT added (only the real drawings); slow drift of the whole card |
| 17.0-18.2 | (music tail) | The ladder cards fold back into the fanned hand with the letters hidden again = frame 0 | Eased re-fan 0.8 s; the last frame equals frame 0, so the loop is seamless |

Total about 18.2 s. Transitions: soft swaps and crossfades only, no black zig-zag wipe (rule of 3.11).

### Layout (safe box x 65-1015, y 269-1248)
Headline y 285-430 (during the gallery it shrinks to one line, "GUESS THE NEWEST CLAUDE", y 285-360, so the stage can start at y 380 when needed). The big stage is the hero: 950 px wide, 4:3, about 712 px tall, filling the box edge to edge. The tray of four small cards (about 210 x 58 visible strip, the cards peek up from below) sits y 1190-1248, never below 1248. No empty zone: in the countdown the collage fills x 65-1015, y 470-1248. Nothing covers what a drawing shows: stamps sit on the card's white border or plain sky, rings sit around features, not on them.

### Engagement line and loop
- Engagement: the countdown chip "comment A, B, C or D" plus L3 "Pause, and comment your letter." Free, one character, and nothing fake: we do not claim anything about the comments.
- Send: L7 "Send it to a buddy. See if they get it." (a challenge send; named person = a buddy).
- Loop: the end re-forms the hidden fan = frame 0; a second watch is how a viewer checks his guess before the reveal (reason 5).
- Caption pinned-comment idea (David posts it by hand if he wants): "Answer key in the video. What did you guess?"

## C. Spoken lines (7) and checks

1. Guess the newest Claude.
2. Same request, four Claude models: a pelican on a bike.
3. Pause, and comment your letter.
4. B is Haiku, the smallest: no sun.
5. D adds a sun. A adds a road.
6. C is Fable, the newest: clouds and a shadow.
7. Send it to a buddy. See if they get it.

Truth check against run 2 (SVG source + render): Haiku r2 has no sun circle and no road (sky rect + grass rect only): true. Sonnet r2 has a sun (`circle r=46 fill #ffe27a`) and no road: "D adds a sun" true. Opus 5.5 r2 has a grey road (`rect y=372 h=14 fill #8a8a8a`): "A adds a road" true (it also has a sun). Fable r2 has three cloud ellipses and a shadow ellipse (`opacity 0.15`, y 504): true. "Smallest" for Haiku and "newest" for Fable 5.2 (released 9.11.2026, the latest of the four per `pelican-research-2026-11-13.md`): re-verify both live before voicing, per the product-check rule.
Voice check: no THR/TR/DR words ("draw", "three", "try" avoided). Watch-list for `script_lint`: "models" (-LS ending), "words" avoided (R + cluster), "Claude" (Whisper writes "clawed": accepted before). "bike" instead of "bicycle" (-CLE ending). Present tense throughout.

## D. Build spec (for the programmer)
HyperFrames HTML + GSAP 3.15, 1080x1920, Miki-style background (`assets/bg.jpg` grid paper, black heavy type IDisp 900, taped cards with 4 px ink border and 10 px hard shadow), the four run-2 SVGs embedded as `<img src="assets/draw/<model>-r2.svg">` inside `.card` elements (white paper, two tape strips, a letter tab). Elements: `#hl` headline (2 lines, shrinks to 1 at s(2)), `#chip`, `.card#cA..#cD` (absolute, transform-driven), `#stage` (an invisible 950x712 target box at x65,y470), `#tray` slots, `#count` disc with three numbers, `.stamp#sB/#sD/#sA/#sC` (rubber-stamp text, transparent fill, ink border, `mix-blend-mode:multiply`), `.ring` SVG paths (stroke-dashoffset draw), `#ladder` end card. Timings from `voice/narration-raw-cues.json` and `words.json`: fan breathe 0 -> s(2); card A to stage at s(1)+0.3; swaps B, C, D evenly spaced between W("pelican") and e(3) (each swap 0.45 s power3.inOut, outgoing card returns to its tray slot at the same time); collage + countdown from e(3)+0.05 for 1.5 s (numbers every 0.5 s, tick SFX); reveal B at s(4) with stamp at W("haiku") and dashed circle at W("sun"); D at s(5), ring at W("sun"); A at W("a",1 after s(5)), ring at W("road"); C at s(6), stamp at W("fable"), clouds ring at W("clouds"), shadow ring at W("shadow"), push-in 1.00 -> 1.08 across line 6; ladder card at e(6)+0.05, thumbnails stagger 0.18 s; re-fan to the exact frame-0 transforms at e(7)+0.2 over 0.8 s, D = e(7)+1.2. All eases sine/power2-3 inOut, no linear; every second has motion (breathe, push-in or drift). Run `safe_check.js`, then `check.sh`, then the first-frame blind reader.

## Honest odds
- Realistic reach (judgement): most likely 300-1,500 views; 2,500+ only if the comment mechanic actually fires. Our median is about 211; ep89 (Miki style, drawn) reached about 1,194.
- Main risk: the content is low-stakes (a drawn bird, nothing happening to the viewer), so the first 2 seconds have to be carried by the game, not by fear or identity; our account rarely gets comments (46 of 50 reels with zero), so the quiz may not spark them. Second risk: Fable's card looks the most detailed, so many viewers will guess right; that is fine (people comment when they feel smart) but it reduces the surprise.
- Log as an experiment in `channel/experiments.md`: "hidden-label quiz with a visible countdown: do comments rise above 0?"
