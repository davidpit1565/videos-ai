# Visual upgrade research, 9.11.2026 (read-only research, nothing published)

Labels: SEEN = read off real frames I extracted and viewed. MEASURED = ffmpeg/numpy on the files (crude, see limits). JUDGEMENT = mine. The redesign PNGs are in `channel/visual-upgrade-assets-2026-11-09/` (copies) and `scratchpad/vis/redesign/` (working files). Nothing in `video/ep88` was touched.

Frames viewed: refs A (DOifsT-EyyA), B (DfbG3p_j3FB), C (De7V3pbTWX6), D (Der2L0-T376), E (De13S4Gi8El), F (DfEpwT9SRHe), ref12m (Adam Stewart talking head), ref3 (arturrioni), ref20m (stormy sky); ours: ep88-final4, reel-86, 80, 82, 72.

## 1. What each reference does well (SEEN, concrete)

**A, @arising.ai (7 s, dark, 240k likes).** Pure black frame, ONE white full-width title bar at the top ("Banned Prompt #93", about 60 px bold black on white, 1080 wide, so contrast is maximal). Hero: a real-looking ChatGPT mobile screen, with a photoreal chrome skull about 280 px tall as the only image. Prompt text about 30 px but never meant to be read in one pass. Motion: a 0.5 s fade up from black, then almost nothing. Lesson: one hard-contrast bar plus ONE strong picture object (the skull) is what stops the thumb. It is not about animation.

**B, @ballauraofficial (40 s, dark).** Flat near-black (#18181B) with a rainbow-gradient ring 600 px wide as the only colour device. Real logos 60-120 px fall, collide and MERGE into one huge logo (Perplexity ends at about 320 px, the Claude burst about 420 px). Particle confetti on every merge. Fixed bottom question in 30 px white. Lesson: real logos as the actual actors, scale change as the payoff, particles as feedback. Needs physics, not a drawing.

**C, @auraguy.ai (72 s, light, our family).** Off-white page with dot grid, orange accent. Same visual family as ours, but: a persistent top chrome (a 12-segment progress bar with the Claude burst at its left, y about 80), a bottom black-outlined caption bar (key word in orange), and every scene is ONE big object that fills 80-85% of the width: real Instagram logo about 400 px with the orange burst crashing into it, a real GitHub page screenshot in a browser frame, a 3x4 grid of black-bordered command tiles, a "26" at about 130 px heavy with a numbered 1-26 grid. Real proof is used (GitHub screenshot, marked "GITHUB, OCT 25 2026"). Flat, hard shadows (the same neo-brutalist 6 px offset as ours). So C is NOT more premium than our frames in rendering; its edge is structure (progress chrome, one object per scene, a real screenshot, a counted list).

**D, @auraguy.ai (72 s, light).** Soft layered shadows instead of hard ones, a 3D-rendered orange asterisk (about 330 px tall, standing, with a floor shadow), real dark skills.sh screenshot card (black, "INSTALLS 3.9M" about 50 px mono), a pixel-grid "1.4 million" wall, an install-count bar list with real names. Section chrome: a tab row at the top (find-skills / next skill) and "1 THE SKILL" step label under it. Bottom caption pill with a light shadow. Depth comes from soft multi-layer shadows and one 3D object.

**E, @cookin.code (28 s, dark then light).** Pure dark (#050505 with a faint grid and vignette). Hero object 300 px with a REAL glow (orange rim light plus orbiting particles), then a second big number "7,000,000,000+" at about 140 px with a gold "+" and a soft white text glow. Orbit rings with small real provider icons (60 px) circling the GitHub logo (about 220 px, purple halo). One word per beat at the top (60 px, thin grey, the live word brighter). At 12.5 s a hard switch to a light grid page with white soft-shadow cards (repo card with stars/forks, server card). Lesson: light (glow, halo, vignette) creates depth that a flat card cannot, and the dark-to-light switch is the one big visual change in 28 s.

**F, @breakingbreach (63 s, light pastel).** Background is a pastel blue/pink MESH gradient with large blurred blobs, never flat. Frosted white cards with 2-3 layer soft shadows and a blur-depth effect: cards behind are blurred and faded (see "Hide API keys", the back card at 40% and blurred). Headline at the top, 70 px bold black, with ONE word in blue inside a pale blue highlight pill; words arrive with a blur-in. A 3D orange pixel creature (the AI) about 250 px. Each of 27 beats = one mini-UI that SHOWS the item (login card with tick, /admin 403 chip, upload check), small floating chips with red "!" badges around the card. Bottom: a pill progress bar "09/27 SECURITY PASS" at y about 1100. Lesson: mesh background, layered blur depth, floating annotation chips and a visible progress pill make a drawn UI look expensive. Closest to a premium look; fully buildable in HTML/CSS.

**ref3, @arturrioni (42 s, editorial light).** Warm beige, serif headline ("Connect ChatGPT to your Instagram", about 64 px Lora-like), tiny mono kicker row at the top ("FIELD NOTE / @ARTURRIONI" about 12 px) and a thin 1-px progress line under it, real ChatGPT and Instagram app icons at 130 px with a connecting line, window-chrome cards ("ChatGPT, Settings" with a toggle) at about 530 px width, cards shown with a natural soft shadow, a mono breadcrumb at the bottom. Calm and premium because there is much white space and a serif, but the type is SMALL (cards 20-28 px) and most of the frame is empty. It is the opposite of our "fill the box" rule and would fail our size floors.

**ref12m, Adam Stewart (talking head, ~12M).** Not a drawn visual: real face full-bleed, a real ChatGPT phone screen (about 450 px wide, black) inserted as a picture-in-picture with a real keyboard, big white heavy caption with black outline at y about 880 (one or two words at a time, about 60 px). Motion = a real person. This is what a drawn style cannot copy (section 5).

**ref20m / R2, stormy sky (6 s).** Real, dramatic photo footage (a dark sky that moves), a 44 px all-caps text block at the top, centre. No UI at all. Cinematic depth comes entirely from the footage.

## 2. Our frames, the same facts, and the 6 gaps

**ep88 final4 (SEEN).** Light #F4F4EF with a very faint dot grid. One card per scene, white, 6 px black outline and a 10 px hard black offset shadow, radius about 44. Frame 0: a 2x2 flat clip-art collage (beach, cake, laptop, fridge) in a card about 950 x 990 px (y 270-1260). Facebook logo about 90 px top-left of the card. A "drawn example" label at about 14 px. Headline words appear only from scene 2 on, so the first frame states the product through a logo only. Scene 4: black-outlined card with the toggle, an ink wipe elsewhere. MEASURED: 22% of frame pairs still (refs: F 2%, B 0%, C 27%, D 42%, E 31%).

**ep86 (SEEN).** Real ChatGPT chat typed in a drawn phone, black speech bubbles, a lime hook word, the keyboard filling the lower half. Strong content, small type inside the phone (chat text about 36 px), no depth.

**ep80 (SEEN).** Dark green-black gradient, a thin 50 px label strip at y about 200, real chat screen recordings dimmed to 20% behind a white answer card, lime outline ring. Cinematic enough, but the picture is a dimmed screen recording with tiny text, and the top strip is small.

**ep82 (SEEN).** Our light style with the orange accent: pills around words, a dark "Agent log" card with a red BUG sticker, a 48 px black ink zig-zag wipe covering almost half the frame in two of six samples. Closest to C structurally, but the wipe hides the content and cards are small (about 600 px wide, 25% of the usable height) with empty space under them.

**ep72 (SEEN).** Black, real ChatGPT answer screenshot, a lime ring, headline in white at the top right. Real proof, but dark and dense, the screenshot text at about 30 px.

MEASURED limits: the "content coverage inside the safe box" numbers are crude (colour difference from the median colour at 108x192), so I do not quote them as facts. The visible, defensible finding is this: **our frames do fill the safe box (ep88 card spans y 270-1260). Size is NOT the main gap.** The gap is depth, light, focal hierarchy and real proof.

### The 6 biggest gaps (ours vs theirs)
1. **Flat, no depth.** Ours: hard black offset shadow, one plane. Theirs (D, E, F): 2-3 layer soft shadows, a rim/inner highlight, blurred and faded cards behind the hero, glow under the hero, parallax. Our frames have exactly one layer plus the grid.
2. **Cartoon clip-art as the hero, not a real thing.** ep88 frame 0 is a drawn collage labelled "drawn example". C, D, E show real screenshots (GitHub page, skills.sh, repo card), real app icons at large size, a real photo (A, ref20m). Where we show real proof (ep86, 72) it is small and dim.
3. **Background is an empty beige page.** E has a vignette plus glow, F has a mesh gradient with blurred blobs, B a coloured ring. Ours: #F4F4EF flat plus faint dots. The page adds nothing, so the card carries everything.
4. **No hero hierarchy: equal-weight pieces and small secondary type.** ep88 frame 0 is four equal tiles and a 14 px label; ep82 has 25-30 px text in dark cards. Refs use ONE object (a 300-420 px logo, a 140 px number, a 330 px 3D object, a skull) with one giant number or word. Rule of thumb from refs: the second-largest element is at most half the hero.
5. **No persistent chrome, so no sense of progress or series.** C: a segmented progress bar, D: a tab row and "1 THE SKILL", F: "09/27 SECURITY PASS" pill, ref3: kicker row. Ours has nothing, and so every scene looks like an isolated card. Chrome also gives the eye something to stay on.
6. **Motion is "cards appear", theirs is "something always travels".** E: orbiting icons, glowing counter, flow dots; B: falling and merging; F: blur-in words, chips popping around a card; D: a 3D object turning. Ours: a card appears and holds (22% still plus long holds in ep80/72), and ep82's black zig-zag wipe covers content.

(A secondary gap, not drawn: no 3D object or photographic image anywhere in our set.)

## 3. Upgrade spec for OUR style (faceless, light base, product accent, real logos, drawn UI, safe box x 65-1015, y 269-1248)
Keeps: paper base, black Inter Display Black type, lime for "useful", product colour as the second accent, the hard-shadow STICKER as the series signature. Changes the cards, background and hierarchy.

**Layers (back to front):**
- L0 paper: radial gradient, `#FFFFFF` centre (50% x 36%) to `#F8F8F4` 45% to `#EEEEE6` edges.
- L1 two blurred colour blobs (no text over them): product accent 760-820 px, blur 90-110 px, opacity .18-.30, behind the hero (it becomes the glow under the hero); lime 620 px opacity .10 bottom-left.
- L2 dot grid 54 px pitch, 2.4 px dots, opacity .55, masked to an ellipse so it fades toward the edges; drifts at 40% of camera speed.
- L3 grain: SVG feTurbulence at 6% multiply. Removes the "vector flat" look.
- L4 back cards: 1-2 duplicates of the hero card, rotated -3 to +3 degrees, offset 40-60 px, opacity .5-.8, blur 0-2 px.
- L5 hero (80-100% of box width, 480-640 px tall).
- L6 floating chips and stickers (max 1 sticker, hard shadow kept).
- L7 type.

**Shadows:** soft cards `0 1px 2px rgba(14,14,14,.08), 0 8px 18px -4px rgba(14,14,14,.12), 0 40px 70px -18px rgba(14,14,14,.28)`; hero photos `0 2px 4px .2, 0 30px 50px -12px .45`; plus an inset top highlight `inset 0 1.5px 0 #fff` and a 1.5 px hairline `rgba(14,14,14,.07)`. Pills and stickers keep the 6-8 px hard offset (series signature). Never mix a hard-shadowed card and a soft-shadowed card at the same level.

**Type scale (px, 1080 wide; floors raised):** hook 104-124 / 900 / line-height .98, tracking -.035em; scene statement 112-124; hero word or number 150-200; card title 56-60; card body 48-72 (never under 44 for anything the viewer must read); chip/label 36 min on a sticker, 20 only inside a photo tag; kicker/progress 30 min. Widths: about 16 caps-and-lowercase characters per 950 px at 104 px.

**Hierarchy rule:** one hero object per scene covering at least 85% of the box width, one focal word at 100+ px, nothing else above 56 px.

**Persistent chrome (new, series identity):** a progress pill in the top safe margin y 280-320 or directly under the headline (step dots N/total, the current one a 64x22 accent pill) on list scenes; "step N of M" only where there is a list. Never in the bottom 35%.

**Background treatment per scene:** the accent blob moves 60-90 px over the scene with `sine.inOut`; one scene per video switches to dark (card-dark `#14151A` as the whole hero card or the whole frame) for a real screenshot or quote, like E's single dark/light switch. It must be a deliberate beat, and the dark card gets a 90 px accent glow, not a flat black rectangle.

**Real proof inside a card:** (a) a real screenshot of the product's settings/help page in a browser or phone frame (capture it per the logo rule; for ep88 the real Meta help page and the real Settings screen on a phone), cropped to the one line that matters with a highlight bar, (b) a real quote in a dark chrome card with the source name in the URL field, (c) real photos only when they ARE the proof (a store front, a product), never as a background, (d) the real app logo at 128-180 px as a white rounded badge with a soft shadow, icon alone. Mark anything drawn as drawn, in 28 px not 14 px.

**Motion (smooth, never robotic):** keep the design-system curves. Add: back cards drift 20-30 px on `sine.inOut`; hero fans open from a stacked pile in 0.9 s `power3.out` with 0.08-0.14 s seeded jitter between cards; the accent blob drifts; chips settle with a shadow that grows 0.15 s after the body. No frame static longer than 2.5 s: the drift counts, but a drifting still is still a still for retention, so the CHANGE events (new card, number, highlight) must land every 2.5-3.5 s.

## 4. Redesign of ep88 (HTML/CSS, rendered with Playwright)
Files: `channel/visual-upgrade-assets-2026-11-09/ep88-redesign.html` (one file, `?s=0..3` picks the scene; needs `facebook.svg` next to it and the fonts folder copied from `video/ep88/hf/assets/fonts` as `fonts/`), PNGs `v5_s0..s3.png`, side-by-side `before_after_ep88.png` (top row = current final4 at 0.1, 13, 21, 28.5 s; bottom = redesign).
Working copy with all iterations: `/tmp/claude-0/-home-user-videos-ai/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/scratchpad/vis/redesign/` (v1 to v5, the final is `v5_s0.png` to `v5_s3.png` and `v5_sheet.png`).

What changed and why:
- **Frame 0** now says the subject in the first second: Facebook logo badge 128 px + "made this from photos you [never posted.]" (104 px / 900, blue pill with a hard shadow), in the top 440 px; hero below: three photo cards with white borders, rotated -7 / 0 / +7 degrees, overlapping, 400 x 520-540 each, strong soft shadows, a blue glow under the pile, a frosted "Collage made for you" notification with the real Facebook logo across the bottom of the hero (y 1100-1232), one lime "CAMERA ROLL" sticker. Whole hero fills x 62-1018, y 640-1232. The first version of this frame (headline above a normal card) had a hero only 480 px tall and looked worse than the original; the layered fan fixed that. Current ep88 frame 0 has no headline at all, so this also fixes the "subject said AND shown" rule.
- **Scene 2 ("Meta says it's opt-in")**: 122 px headline with a lime pill, a dark browser card (the series dark card) with a blue 90 px glow, the real quote at 72 / 48 px with a lime highlight on "opt in".
- **Scene 3 ("Here's the switch")**: 124 px headline with the logo badge, a green OFF sticker, three slim frosted step cards (56 px) and the 4th step as a bigger white card with a 7 px Facebook-blue ring and glow and a large toggle (170 x 92).
- **Scene 4 ("Send this to mum")**: 124 px headline, a larger chat card with a Mum avatar, a bubble, three lime Allow pills at 72 px.
- Honest check: in the side-by-side the new frames read as deeper and cleaner and the type is larger, but the OLD frames have more graphic punch in their heavy outlines and a bigger first-frame hero. The redesign is better in depth and in stating the subject; it is not 10 times better, and the photo tiles are still drawn (gradients and shapes, no real photograph). A real screenshot of the real Meta page in scene 2 and of the real Settings screen in scene 3 would add more than any further CSS.
- Not done: no animation, a still render only; no safe_check.js run on these (they are not a build); no word-timing. The sticker and the notification text positions were checked by eye only.

## 5. What a drawn style cannot do vs those references (honest)
1. **Real presence (ref12m, A's skull photo, ref20m's moving sky).** A face, a hand, a real room, a real dramatic sky give trust and a stop-the-thumb reflex that a drawing does not. We cannot be faceless AND have a person. A real photograph of a real object as proof (inside a card) is the closest allowed thing.
2. **Real light.** Photoreal glow, lens depth, volumetric light (E's rim-lit icon, D's rendered asterisk) need 3D or compositing. CSS gives soft shadows and blob glows, not materials.
3. **Particles and physics (B).** Falling, colliding, merging logos and confetti need a physics/canvas layer. Buildable in canvas but it is a different pipeline, and the genre is someone else's trend and off-brand for us (6.10 lesson).
4. **3D mascots and objects (D, F).** We do not have a 3D pipeline; a flat mascot would look worse than none.
5. **Real screen recordings with real motion** are already our v4 strength; a drawn UI can look cleaner but never carries the "this is real" credibility. Use real captures wherever we make a claim.
6. **A trend, an account and a timing** are not visual at all. C and E have audiences and comment gates; the visual alone does not give reach. Judgement: a better visual might lift hold and saves; I have no data and no calibration to say by how much (ASSUMPTION: modest).
