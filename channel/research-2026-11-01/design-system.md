# Series design system, "Actually Works" (spec for a builder), 1.11.2026

Labels: FACT = read in a file or measured here. SOURCED = from a web page I read (weak sources, see section 12). HYPOTHESIS = my design judgement, not proven for this channel. UNKNOWN = needs a test.
Scope: one fixed identity for every reel, 1080x1920, HTML + GSAP rendered by HyperFrames. This replaces the "new colour every episode" rule (David's decision 1 in `channel/style-research-31-10.md`). Nothing here has been rendered; it is a spec.

## 0. What I read, and what the current v6 does (FACT, from the files)
- `build_v6.py` / `template.html`: light theme (`BG #F7F7F2`, lime `#B6F23A`, ink `#111`, dots `#DADACF`), dot grid drifting linearly (`ease:"none"`, 216 px over the whole video), three real ChatGPT-logo wheels rotating at constant speed plus a dashed ring, scenes joined by blur+scale zoom-through (0.85 s in / 0.65 s out), words revealed at spoken-word times (`power2.out`, 0.75 s), after landing every word bobs `y:-10` with the SAME 1.5 s sine yoyo, whole stage drifts rotation +-0.9 deg, phone scene with tap circle (0.85 s sine.inOut), typed card with a sine-wobble `typeEase`, CSS-var highlight bars.
- Fonts: Inter 500/700/800 loaded from `cdn.jsdelivr.net/@fontsource` at render time (a network dependency inside the render).
- Style research file: the reference reel (insiderforce) has dotted grid, black bold type word by word, typed cursor, selection bar, blurred black spiky wipes, dark prompt card. One fixed identity per account is the one thing all four reference reels share (FACT). Why they spread is HYPOTHESIS (copy-paste utility, finite numbered list), not proven.
- `motion-recipes.md` already rules: no overshoot bounce ("#1 agent-video tell"), power3-style settles, per-word highlight bars (one box across a wrapped phrase breaks), zoom-through transitions, one hero beat per episode, `MK.animateWordEmphasis` is a plain colour toggle (David: "the simplest thing").
- Fonts on the container (FACT, `fc-list`): Inter (Thin to Black, static OTF in `/usr/share/fonts/opentype/inter/`), Inter Display (same weights, optical-size cut for large type), JetBrains Mono (Thin to ExtraBold, TTF in `/usr/share/fonts/truetype/jetbrains-mono/`). Space Grotesk, DM Sans, Manrope, Bricolage, Poppins, Montserrat are NOT installed.

## 1. Identity in one sentence
A light grey graph-paper page where black heavy type is typed onto the page by the voice, lime is the only colour that means "this", and every real thing (logo, screen, text the viewer can copy) sits in a dark card or white phone that floats over the grid.
Why this and not another: it is the style David already loves (reference) and approved (light + lime base, CLAUDE.md "colour stays light unless he says otherwise"), it is already built in v6, and one accent colour means a thumbnail is recognisable in a grid of 9 posts. HYPOTHESIS that recognisability helps; the four reference accounts all keep one identity (FACT), which is not proof it causes growth.

## 2. Palette tokens (all hex, define on `:root`, no other colours allowed)
| Token | Hex | Role | Reasoning / measured contrast (WCAG ratio, computed here) |
|---|---|---|---|
| `--paper` | `#F4F4EF` | page background | warm light grey, close to current `#F7F7F2`, slightly darker so white phone and white cards separate from it |
| `--dot` | `#D6D6CC` | dot grid | 1.33:1 on paper: intentionally faint texture, never carries text |
| `--ink` | `#0E0E0E` | all headline type, borders | 17.5:1 on paper |
| `--ink-2` | `#5B5B55` | secondary labels | 6.19:1 on paper |
| `--lime` | `#B6F23A` | the ONE accent: fills, highlight bar, caret in dark card | NEVER as text on paper (1.21:1). Always a fill with `--ink` text on it (14.48:1) |
| `--card-dark` | `#14151A` | prompt card, typed-text card | 16.24:1 with `--card-ink` |
| `--card-ink` | `#F2F2EE` | text in dark card | |
| `--paper-white` | `#FFFFFF` | phone screen, sticker bodies | black on white 19.3:1 |
| `--red` | `#E5322D` | "wrong / OFF / bad" tag, crossed-out marks | 3.94:1 on paper (large text only, 3:1 rule for 28 px+ bold); white text on it 4.35:1 |
| `--green` | `#1F9D4A` | "right / ON / done" tag | 3.18:1 on paper (large bold only); use white text inside a green pill, not green text on paper |
Rules: lime and red never touch each other in one element; at most 2 accent colours visible in one frame (lime + one of red/green). The brand logo keeps its own real colours (see section 9), logo wheels in the background are tinted `#8AC926` at 0.36 opacity today: keep, but cap at 0.30 so they never compete with type (HYPOTHESIS, needs a look at the render).
Dark mode variant: none. One identity means one palette (the v6 "warm" and "dark" themes in `THEMES` should be deleted, not kept as options).

## 3. Typefaces (2)
1. Headline and UI: **Inter Display** (weights 800 and 900 for headlines, 500 for light words). Inter and Inter Display are SIL OFL fonts and are on Google Fonts (the Google Fonts variable Inter has an `opsz` axis; FACT for the OFL licence of Inter, from memory, not re-checked today). Installed locally as static OTF: FACT.
2. Prompt/typed text: **JetBrains Mono** (weights 500 and 700), installed locally: FACT. Monospace makes "typed" text read as typed and keeps character count stable while it grows (no reflow jitter).
Embedding (important, FACT about the current weakness): v6 pulls Inter from jsdelivr at render time. Replace with files copied into `hf/assets/fonts/` and `@font-face{src:url("assets/fonts/InterDisplay-ExtraBold.otf")}` (and Black, Medium, JetBrainsMono-Medium/Bold). UNKNOWN whether HyperFrames' Chrome also sees system-installed fonts by name; the local `@font-face` route does not depend on that. Test one render and compare glyph shapes before trusting it.
Tight tracking: headlines `letter-spacing:-0.04em` (current value, keep), line-height 1.04; mono 0, line-height 1.4.

## 4. Type scale (px on 1080x1920; minimum legible size on a phone = 30)
| Style | Size | Weight | Use |
|---|---|---|---|
| `t-hero` | 200 (285 only for one 5-letter word) | 900 | the one slam word of a hook |
| `t-display` | 150 | 800 | hook lines |
| `t-h1` | 112 | 800 | scene statements |
| `t-h2` | 92 | 800 / 500 | secondary line |
| `t-cap` | 64 | 800 | key-word captions under a phone scene |
| `t-card` | 40 (never below 36) | Mono 500 | text inside the prompt card |
| `t-label` | 30 | 700 | tags, chips, step labels |
v6's phone card text is 29.5 px: below the 30 floor, and the card is the thing a viewer should save. Show the final prompt/answer full-width on the dark card at 40 px for 2-3 s (decision 4 in the style-research file); the phone version stays as context only.
Width budget: usable box x 65-1015 (950 px). Inter Display ExtraBold averages ~0.58 em per capital at -0.04em tracking, so 950 px holds about 8 caps at 200 px or about 11 lowercase letters at 150 px (HYPOTHESIS from font metrics, run `safe_check.js`, do not trust the estimate). Break lines by meaning, 2-4 words each.

## 5. Grid and safe zones (FACT numbers from CLAUDE.md)
- Canvas 1080x1920. Safe box: x 65-1015, y 269-1248 (top 14% = 269, bottom 35% = 672 px, sides 65). Height available: 979 px.
- Vertical zones inside the safe box: Z1 headline y 290-650 (hook/statement), Z2 hero object y 650-1230 (phone, dark card, logo, real screen), caption row (key-word bar) y 1120-1240 only when the hero object is shorter. Nothing enters y > 1248 except `data-decor` (wheels, grid).
- 8 px baseline unit; card radius 32; phone radius 76 (current); gaps 24/48.
- On full-bleed real-screen scenes: no handle, no tags over what the screen shows (David 18.10); overlays only where the recording is empty, verified per frame (`channel/assets/ep<N>-screen/`).
- Gate: `node export/safe_check.js` plus a manual look; it measures text boxes, not whether a sticker covers a keyboard.

## 6. Component kit (each with markup contract, so a builder can write them once)
1. **Page** (always present): `--paper` + dot grid (radial dots 2.6 px, 54 px pitch, drift in section 7) + 2-3 background logo wheels (decor, section 9). Never changes between scenes.
2. **Hook headline**: 2-4 rows, words are `<span class="w">` revealed at the spoken-word stamp. One word per hook gets `.pill` (lime fill, ink text, 7 px ink border, 9 px hard shadow) or `.sel` (selection bar: ink fill, paper text, radius 24) or `.red` colour. Max ONE emphasis device per row, max two per scene.
3. **Selection-bar highlight**: the reference's look. Bar is a background gradient on the word itself (`background-size: 0% -> 100%`, per word, never one box across wrapped lines, per motion-recipes bug note). Ink bar for statements, lime bar for "this is the useful part". Grows 0.45 s `power2.out` left to right, text colour flips at 40% of the grow (not at the start).
4. **Number badge** (for "1 of 5" lists): 150 px circle, ink fill, lime numeral, 8 px offset hard shadow; sits above the headline in Z1; count-up is not allowed (it is a robotic tell), the numeral just scales in with `power3.out` 0.5 s. A step indicator (see 9) shows N/total.
5. **Prompt card (dark)**: `--card-dark`, radius 32, padding 44, 2 px `#2A2C34` border, header row with a 3-dot mark and a real product logo (icon only, no text caption under the logo: CLAUDE.md), body JetBrains Mono 40 px, lime caret 5x44 px. Full width of the safe box (950) for the "save this" moment.
6. **Typed-text card**: same card; text appears by characters at a human rhythm: base 22-34 chars/s with per-character jitter (seeded, deterministic: `Math.random()` is banned in renders, use `mulberry32`), a 120-220 ms pause after punctuation, 0-2 short hesitations per card. Caret blinks only while paused (530 ms period, `sine` opacity, not a square on/off) and is solid while typing.
7. **Phone frame**: white screen, 10 px ink border, radius 76, soft shadow `0 26px 60px rgba(0,0,0,.22)`, drawn UI only (never imitate a real answer; typed user text only per episode 80/81 practice). Phone and drawn rows are in the lowest z-level of scene content so the tap circle (84 px) sits above.
8. **Sticker**: rounded-rectangle or 5-point burst, lime or white fill, 6 px ink outline, hard shadow, rotated -6 to +6 degrees, 30-46 px bold text ("NEW", "SAVE THIS", "TESTED"). Max one sticker per scene; it arrives by scale 0.7->1 with `power3.out` 0.5 s and then holds still (no wiggle loop).
9. **Wipe (spiky blur)**: the reference's blurred black spiky wipe. Spec: a 1080x2400 SVG band of ink-black zigzag spikes (12-16 spikes, amplitude 140 px) with `filter: blur(14px)`, travelling bottom to top across 0.7 s with `power2.inOut`, covering the cut midway (scene swap at 50% = 0.35 s). Real hard cut between scenes happens UNDER the wipe, so no scene needs its own fade. Use for section changes only (about every 8-12 s), not for every line change. Between lines of the same section use the soft scale/blur exchange already in v6, shortened (section 7). UNKNOWN: render cost of a full-screen blur filter in HyperFrames; v6 already blurs full-screen scenes and rendered, so it is probably fine, time one render.
10. **Step / progress indicator**: row of N small dots (22 px) inside Z1 top edge (y 290), current dot is a lime pill 64x22 with ink border, done dots ink. Pill slides to the next dot over 0.5 s `power2.inOut` (it does not jump). Required on every numbered list reel; optional otherwise. A thin progress line across the whole bottom is forbidden (platform UI sits there).
11. **Logo badge**: the product's real logo/icon alone, in a 150-250 px white rounded square or free-standing; never a caption underneath (CLAUDE.md, 5.10).
12. **Key-word caption** (section 8).

## 7. Motion spec (what "smooth, not robotic" means in GSAP)
Why the current build still reads robotic, from the code (FACT about the code, HYPOTHESIS about why David feels it): every word uses the identical 0.75 s `power2.out` rise; after landing every word runs the identical 1.5 s yoyo so the whole text breathes in lockstep; scenes drift with the same 0.9 deg sine; wheels rotate at one constant speed with `ease:"none"`; tap circles always take 0.85 s; all scene transitions have the same 0.85/0.65 s. Identical timing on many elements is the clearest mechanical signature (HYPOTHESIS; the general guidance that linear/uniform timing "feels robotic" is SOURCED from tutorial pages only).
Principles taken from classic animation (SOURCED from student/blog summaries of Johnston and Thomas, not the book): slow in/slow out, overlapping action, follow-through, secondary action only if it supports the main action.

### 7.1 Curves (use ONLY these, named tokens)
| Token | GSAP | Use |
|---|---|---|
| `E_SETTLE` | `power3.out` | everything arriving (words, cards, badges): fast start, long soft stop |
| `E_SLAM` | `expo.out` | the single slam word / pill only |
| `E_MOVE` | `power2.inOut` | anything that travels between two resting places (phone push, indicator slide, camera move) |
| `E_DRIFT` | `sine.inOut` | continuous ambient motion, always with `yoyo` over >= 4 s |
| `E_EXIT` | `power2.in` | things leaving; shorter than their entrance |
| `E_WIPE` | `power2.inOut` | wipe band |
Never: `ease:"none"` on anything except a constant-speed rotation of a background wheel (and even then vary speed per wheel); `back.out` / `elastic` / `bounce` (motion-recipes: overshoot is the #1 tell); `steps()`; CSS `ease` keywords. An optional custom cubic-bezier close to Material's "emphasized decelerate" `cubic-bezier(0.05, 0.7, 0.1, 1)` (SOURCED: several third-party Material-3 ports agree on these numbers; they disagree about the plain "emphasized" curve; official m3 spec not read) can replace `E_SETTLE` for cards; test it against `power3.out` by eye.

### 7.2 Durations (seconds)
Word in 0.55-0.7 (jitter +-0.08 seeded per word, never identical neighbours); slam word 0.9; card rise 0.7 with shadow growing; badge/sticker 0.5; highlight bar 0.45; typed card as in 6.6; phone push 0.9-1.0; indicator slide 0.5; exits 0.35-0.45; scene soft exchange 0.6 in / 0.45 out; wipe 0.7; tap approach 0.55-0.9 (random-ish per tap, seeded), tap press 0.14 down / 0.22 up, ripple 0.8. Floor: nothing visible moves faster than 0.25 s except a typed character; ceiling for a single move: 1.1 s (longer reads as lag).

### 7.3 Overlap and stagger
- Words: start each word 60 ms BEFORE its spoken stamp (v6 does -50 ms, keep), and let the entrance (0.6 s) overlap the next word: the line is in constant motion, never "word, stop, word". Stagger inside a row that arrives together (cards, rows): 0.09-0.14 s with `from:"start"`, never uniform; add +-20 ms seeded jitter.
- Anticipation 1-2 frames: slam word starts at scale 1.2 -> 1 with the 40 px rise (v6 values are fine), plus the previous words dim 8% for 0.3 s so the slam has room (secondary action supporting the main action).
- Follow-through: when a card or phone settles, the shadow finishes growing 0.15 s after the body stops; text inside a card settles 0.1 s after the card.
- Overlap scenes: incoming scene starts 0.15-0.25 s before the outgoing one finishes leaving (v6 `IN = 0.15`); wipes: scene swap exactly at the wipe's midpoint.

### 7.4 Camera and ambient drift
- Camera = one container (`#cam`) that holds Page + scene content; animate `scale 1.00 -> 1.04` and `x/y +-14 px` with `E_DRIFT` over each scene's whole length, direction alternating per scene. Hard cap +-1.0 deg rotation and 1.06 scale (IBM guidance, SOURCED: broad camera moves become distracting).
- Dot grid: parallax, moves at 40% of the camera speed and in the OPPOSITE direction; speed eases (`sine.inOut`) between scene waypoints instead of one linear 216 px sweep.
- Logo wheels: each has its own period (22, 31, 47 s), own direction, plus the waypoint travel already in v6. Opacity breathes 0.24-0.32 over 9-13 s per wheel.
- Secondary motion on text: NOT a bob on every word. Bob only the one emphasised word per scene, amplitude 6 px, period 2.4 s, started 0.5 s after it lands. The rest of the text is carried by camera drift only.

### 7.5 What must hold still
Settled text never wiggles. A static frame is allowed to be static as long as the camera drift is running (drift counts as motion), see rhythm.

### 7.6 Exact "robotic" tells to avoid, list A (motion)
1. Same duration and same ease on every word of a line.
2. Stagger with a fixed step (0.10, 0.10, 0.10) and no jitter.
3. Linear (`none`) movement of anything that is not a continuous rotation.
4. Bounce/overshoot/elastic entrances.
5. Looped yoyo with identical period on many elements, so they breathe together.
6. Counters that count up digit by digit at constant speed; typed text at constant characters per second; caret that blinks with a square on/off.
7. Cursor/tap that moves in a straight line at constant speed and stops dead (use a slightly curved path: GSAP `MotionPathPlugin` with a 2-point curve, or two eased moves with a 40 px overshoot-free arc via `y` on a different ease). UNKNOWN whether HyperFrames bundles MotionPath; two-tween fallback works with core GSAP.
8. Everything stops at the same instant at a scene change (all elements share one exit time).
9. Hard pops (opacity 0 -> 1 in one frame) for anything other than the wipe midpoint swap.
10. A transition style applied identically to every cut in the video.

## 8. Caption styles for the key word
Two captions exist in the reel; they must not both be on screen at once and must not repeat the headline word for word (CLAUDE.md karaoke note).
- **Headline words ARE the caption** (hook and statement scenes): spoken word turns from `--ink` at 38% opacity to 100% (what v6 `.cap span` already does); the key word additionally gets the selection bar or lime pill. No separate caption track.
- **Bar caption** (scenes where the hero object is a phone/real screen): one or two lines in `t-cap` (64 px) at y 275-445 or at y 1120-1240, never over the screen; the word being said sits on a lime bar (ink text), already-said words ink 100%, upcoming 38%. Chunk = 2-4 words. The lime bar glides from word to word (x/width tween 0.2 s `power2.out`) instead of switching on/off: smoother and still the "simplest thing" colour logic David asked for, but UNKNOWN whether he prefers the glide to the plain toggle: render both for one scene, he decides (his rejection of the moving highlight box on episode 74 is FACT in CLAUDE.md, so do NOT use a box that roams over real answer text; this glide is on the headline bar only, never over a real screen).
- Key-word colour: lime bar (useful) or red pill (the bad thing). Never lime text.

## 9. Real logos, photos and screen recordings (CLAUDE.md rules, FACT)
- Every product named gets its real logo, sourced from official/Wikimedia brand pages, never redrawn. v6 reuses `channel/assets/ep62-chatgpt-logo.svg` and `round5/claude-symbol.svg` (Wikimedia Commons "Claude AI symbol.svg"). Keep a `channel/assets/logos/<brand>.svg` library with source URL and date in a manifest next to it (UNKNOWN: does it exist, I did not look; create if not).
- Logo placement: as a white rounded badge (150-250 px) near the headline, icon alone; in the background, as the tinted wheels only for the product the episode is about (v6 uses ChatGPT wheels; for a Claude episode swap the SVG, not the layout).
- Real screen recordings (the v4 standard): shown inside the phone frame or a card, played at natural speed (`data-rt`/`data-dl`), start on the proof frame, no overlay over what the screen shows, no handle on full-bleed. HyperFrames' own video layer broke the page background in the earlier samples (FACT, round-1 README): the working path was overlaying with ffmpeg, so a recording scene needs that two-step render. Specify it as part of the series pipeline, not a per-episode hack.
- Photos: the standing "real photo backgrounds" rule from episode 55 conflicts with the new dot-grid identity. UNKNOWN which wins: decision for David (my recommendation, HYPOTHESIS: photo only as a framed image inside a card or phone, never as a full background, so the page identity stays constant). His own photos: never from his home/window, no street identification (CLAUDE.md).
- Face pre-check still applies to any photo with a person.

## 10. Scene rhythm
- Target: a new visual event every 2.5-4 s, where "event" = a cut/wipe, a new card/object, or a hero-object state change (typed card starts, highlight lands, phone page pushes). That is 2.5-4 events per 10 s. Cuts proper (full scene swaps): 1-1.5 per 10 s, the rest are in-scene events. Sources only give rules of thumb: "new visual every 3-4 s" and median scene about 3.7 s (SOURCED, vendor blogs, not a study); film research warns against reading pacing as a rate (SOURCED). So: starting HYPOTHESIS, to be tuned by retention data that does NOT exist for this account (watch time is NOT_AVAILABLE per CLAUDE.md).
- Max time any frame is truly static (no element moving anywhere): 0.6 s. Max time without a NEW event: 4.5 s, except the save-this moment, which holds the dark card at 2-3 s with camera drift still running.
- Hook: first frame already shows the proof state (v4 rule), first word on screen by 0.12 s, hook scene 2.5-4 s with 3 events.
- Order of a standard reel: Hook (3 s) -> Problem felt (4 s) -> Fix, step by step with indicator (bulk) -> Save-this card (3 s) -> link-in-bio line -> tomorrow line (CLAUDE.md order, verify).
- Wipe budget: one wipe per section, at most 4 per 45-75 s reel.

## 11. DO NOT lists
**List B: layout/typography tells**
1. Text below 30 px, or the key text only inside a phone at 29.5 px.
2. Lime text on paper (1.21:1) or red/green text under 28 px.
3. Every row the same size and weight (no hierarchy), or 3+ emphasis devices per scene.
4. Caption repeating the headline; caption or handle over the answer/keyboard on a real screen.
5. A text caption under a logo badge; a redrawn or "approximated" brand mark.
6. Elements in the bottom 672 px or outside 65 px sides (except `data-decor`).
7. Random per-episode colour, font or component styling (the whole point is one identity).
**List C: pipeline tells**
1. Fonts loaded from a CDN at render time; Math.random(); any untimed motion (everything is a seeded GSAP timeline).
2. Copy-pasting one transition for every cut; a wipe on every line.
3. Overshoot or bounce to "add energy"; the energy comes from speed variation and the voice, not from wobble.
4. A moving highlight box over real answer text (rejected on episode 74).
5. Slow-motion of a real screen segment to fill a line (v4 rule).
6. Shipping without watching the render twice (CLAUDE.md) because the numbers passed.

## 12. Reference styles researched (6-10 requested)
Honest note: web search returned mostly vendor blogs and tool pages. Nothing below is verified by a primary source except where marked; the "borrow" column is my design judgement.
| Style | What I can say (source quality) | What to borrow (never copy artwork) |
|---|---|---|
| Hormozi-style captions | SOURCED (Riverside, OpusClip, Choppity vendor pages): yellow word-by-word captions on dark, jump cuts every 1-3 s, punchy zooms, SFX. | Only the word-level highlight idea (our lime bar). Not the 1-3 s jump cuts: our content is explanatory, and the cuts there are for talking heads. |
| Ali Abdaal captions | SOURCED, sources disagree on colour: handwritten-style captions, desaturated grade with selective colour pop. | Selective colour: one accent only, same as lime-only. |
| Leila Hormozi (slower) | SOURCED (one Choppity page): 3-8 s shots, minimal captions. | Permission for slower scenes when the hero object (typed card) is the content. |
| Kurzgesagt-type flat explainer | SOURCED only that it is flat, bright, consistent; palette/motion analysis NOT found. | One consistent illustration language across episodes; cards/stickers with flat fills and a single outline weight. |
| Kinetic typography shorts | SOURCED (DesignRush, Hera, Livepeer playbook pages): timed text works on silent-scroll feeds; zooms, slides, colour changes, glow. | Words timed to the voice (we do), colour change as emphasis (we do). No glows (not in our palette). |
| insiderforce reference reel (David's) | FACT from style-research file: dot grid, word-by-word black type, typed cursor, selection bar, spiky wipes, dark prompt card. | This is the base of the system; own artwork, same structure. |
| MarketerHub reference reel | FACT: real screen capture + presenter + serif-italic captions. | The real screen capture proof only (presenter not possible). |
| Max_Simplifia reference reel | FACT: cream/orange/black, drawn UI, typed keys, "NOUVEAU" sticker, key word in red. | Sticker as a component, red key word. |
| Pierrick IA reference reel | FACT: black background, 3D mascots, numbered dots 1-7, typed prompt cards in a drawn window. | Numbered dots as the step indicator, typed prompt card. Not 3D mascots (cannot be built, per style-research). |
| Classic animation principles | SOURCED (student notes, blogs; original book not read): slow in/out, overlap, follow-through, secondary action. | Section 7. |
UNKNOWN: Duolingo/Notion/Linear-style product explainers, Nas Daily and Vox were not found in the searches; I did not rely on any claim about them.

## 13. Files to change in `build_v6.py` / `template.html` (not done, per instruction)
`build_v6.py`
1. `THEMES`: replace the three-theme dict with one `PALETTE` using the tokens in section 2 (`BG #F4F4EF`, `DOT #D6D6CC`, `INK #0E0E0E`, new `CARDD`, `CARDINK`, `GREEN`); delete `warm`/`dark` and the `--theme` arg.
2. Add a font-copy step: copy Inter Display Black/ExtraBold/Medium and JetBrains Mono Medium/Bold into `hf/assets/fonts/`; add replacement tokens `__FONTS__`.
3. `sizes` dict for captions (44/54/38/52): re-base to `t-cap` 64 and the card text to 40.
4. `reveal`-related: write a seeded jitter table (`mulberry32`) into the generated project, pass `__SEED__`.
5. Add `--wipe` section markers: pass section boundary times (replacing the current `FIRSTIDX` scene logic) so the template can draw a wipe at those times.
6. `SMV`/`__ZOOM__` options: drop (one identity, one smoothness); keep `--no-render`.
`template.html`
1. `@font-face`: switch from jsdelivr woff2 to local `assets/fonts/*` (Inter Display, JetBrains Mono); `font-family` on `html,body` and a `.mono` class for card text.
2. CSS `:root`: replace colour vars with the new tokens; add `.pill`, `.sel`, `.sticker`, `.badge`, `.stepdots`, `.pcard` (dark prompt card), `.wipe`, `.hlw` (per-word highlight) classes per section 6; `.stage` stays top 300 / height 900.
3. `#card` (29.5 px, inside phone): add the full-width dark `#pcard` at 40 px mono for the save-this moment; keep the phone for context.
4. JS motion: replace `reveal()` with jittered durations/staggers (E_SETTLE tokens) and bob only the emphasised word; delete the global per-word yoyo bob; replace `drift()` with the `#cam` container drift of 7.4 (scale 1.00-1.04, x/y +-14 px); change the dot grid from linear `ease:"none"` to waypoint `sine.inOut` with opposite-direction parallax; give each wheel its own period (22/31/47 s) and opacity breathing.
5. Transition block: keep a short soft exchange within a section (0.6/0.45 s) and add the spiky blurred wipe (`#wipe`, SVG band, 0.7 s `power2.inOut`, scene swap at 0.35 s) at section boundaries.
6. `typeEase` sine-wobble: replace with a seeded per-character schedule (22-34 cps, punctuation pauses, hesitations); caret blink via `sine` opacity only while paused.
7. `tap()`: seeded approach duration 0.55-0.9, curved path (two eased tweens), press 0.14/0.22.
8. Add `E_*` constants at the top of the script and ban literal ease strings elsewhere (grep check).
9. Add the step-dots component and number badge for numbered lists.
10. `WP` waypoint table: keep, but vary each wheel's rotation period and cap opacity 0.30.
Unchanged: composition root attributes (`data-composition-id`, `data-start`, `data-duration`), timeline registration, `window.__reel`.

## 14. Test before locking (UNKNOWN items, in priority order)
1. Render one 10 s test with local fonts and compare to the CDN render (glyphs identical?).
2. Time one render with the full-screen blurred spike wipe.
3. Render bar-caption glide vs plain colour toggle; David chooses.
4. Look at lime bar, red pill and the logo wheels at 0.30 opacity against `--paper` in actual frames (CLAUDE.md "a real look, every time").
5. Decision for David: photo backgrounds vs fixed dot-grid identity (section 9).
