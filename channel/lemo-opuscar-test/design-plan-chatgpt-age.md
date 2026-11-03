# Design plan: "UNDER 18?" (ChatGPT age guess), 30 s, 1080x1920, 24 fps, light

Status: plan only. Nothing built, nothing rendered. Times are provisional: the picture follows the narration, so every time below is retimed from the real voice cue file (`export/retime.py` rule on the channel side; here: `window.CUES` read from whisper word times).

---

## (a) Style choice

### Pick: Living Screencast (`styles/living-screencast`), heavily adapted. Closest fit, not a clean fit.

What I read: STYLE.md of living-screencast, swiss-motion, dataviz, iso-infographic, pictogram-motion, whiteboard, plus AGENTS.md, DIRECTOR.md, TECHNIQUE.md, core/README.md.

Honest comparison on the two hard tests (LIGHT, 9:16) and on the client's "not robotic":

| Style | Light theme without hacks | 9:16 without hacks | Smooth / not robotic | Verdict |
|---|---|---|---|---|
| living-screencast | Yes. STYLE.md s3: "the product's own interface colours rule: follow its real light and dark themes". Overlays are frosted glass with one accent taken from the product. | Layout is drawn from `innerWidth x innerHeight` (TECHNIQUE s2), so no engine limit. But the style is composed as a desktop window floating on wallpaper, so the UI layouts must be redone as a tall phone/sheet layout (new `ui.js`, not an engine patch). | Camera and cursor are spring-eased and smooth. Two clashes: UI "on ones", mascot position stepped to a pixel grid. | **Chosen.** The only style whose contract is "real product UI redrawn + cursor + recording-software camera" which is exactly Settings > Account > Age, and "real UI, no lorem ipsum, every label matches the product". |
| swiss-motion | Yes (paper, ink, one signal colour). | Yes (6 columns instead of 12). | **No, by design**: "nothing bounces", "entrances are wipes, never fades", numerals climb in steps, everything snaps on the beat. That is the robotic feel the client banned. Also "not device renders", no app UI. | Rejected. |
| dataviz | Yes (cream paper). | Yes. | Pencil is organic. | Rejected: the chart is the film and we have no data series; no room for app UI or a quote card. |
| iso-infographic | Yes (pale ground). | Needs a re-frame, doable. | Icon pops use back-ease overshoot; "solids arrive by motion". Heavy. | Rejected: isometric dioramas bury a settings screen and a typed quote; 5-7 hues fights "one lime accent"; highest build cost. |
| pictogram-motion | Partly (light hues exist). | Yes. | **No**: beat-locked, every cut on a drum hit, grid rows jump on beats. | Rejected. |
| whiteboard | Yes (glossy white board). | Needs a re-frame of an 8000x4500 board. | Yes, warm and organic. | Runner-up. Fails on fidelity: real logo and a typed quote card sit oddly on a hand-drawn board, and "redrawn app screen labelled re-created" turns into marker sketches. Stroke engine is also the most expensive to write. |

### Reasons for living-screencast
1. The reel is a product-UI explainer: a quote from a real page, a settings path, an email and an in-app notice. This style's whole grammar is "one feature per sentence, real labels, cursor taps, camera pushes to where it happens".
2. Native "diegetic title" (a title that is a real UI element), "spotlight freeze" (push in + vignette on the one thing to remember = the quote), "moving floor", and the cursor-as-user model.
3. Frosted-glass overlay chips with one accent taken from the product = the client's "accent follows the product" rule (ChatGPT lime).
4. Voice-line-per-feature pacing matches our script (one idea per line).

### Deviations from STYLE.md (must be disclosed, STYLE.md says "keep all of it")
1. **No pixel mascot.** The reel has no software agent doing work on screen; a lime pixel creature next to a ChatGPT logo would read as an invented ChatGPT mascot (brand-fidelity risk). I keep the style's signature "two resolutions" look through **pixel-grid props only** (the "?" tile, the check mark, a few sparkles), crisp on a hi-res UI. If the library owner insists on the mascot: one small lime pixel "guesser" standing on top of the "UNDER" letters in shots 1-4 only; it adds stepped motion that fights the smoothness rule, so I advise against.
2. **24 fps, not 30.** Client spec. `--fps 24` and `mux.sh ... 24` are supported by the tools. Position stepping is dropped (all motion sub-pixel smooth).
3. **Phone-width layout instead of a desktop window on wallpaper.** The "window" becomes floating UI cards/sheets on the light ground.
4. **Captions are not in a bottom pill** (bottom 35% is Instagram UI). Each shot carries one headline lane inside the safe box, with spoken words lit (see c).
5. **Overlays stay frosted white cards**, but the "key HUD" (keystroke display) is dropped: it would be clutter and nothing is typed except the year digits.

### Engine status
- **No engine patch to `core/`.** TECHNIQUE s2 contract (`window.DUR`, `window.render(t)`, `window.READY`, `window.TEXTS`, `window.EV`) renders any size via `--size 1080x1920`.
- **The living-screencast demo source is NOT in this clone** (sparse checkout; `styles/living-screencast/demo/` is absent). Reference only: `sh plugin/skills/lemo-opuscar/scripts/setup.sh demo living-screencast` after the treatment exists (AGENTS.md "treatment first").
- We write our own `film.js`/`ui.js`. A working 1080x1920 canvas scaffold from an earlier test already exists at `.../scratchpad/lemo-demo/engine.js` + `main.js` (dark keynote, 475 + 162 lines) which can be the shell (UNVERIFIED for this plan: I did not re-run it).
- Font note: `core/fonts/` has display fonts only (Fredoka etc.). Self-host Inter Tight (900/800/700) + Inter (600) + DM Mono (500) from Google Fonts (OFL) into the project's `fonts/`.
- The library's TTS (Kokoro) is NOT used: the channel's own cloned voice, `audio/voice_quality.py`, real-library music and `check.sh` replace it. `mux.sh` (-14 LUFS) is fine for the final mux if the channel pipeline is not used.

### Honest risks
1. **Producibility**: new vertical UI kit (cards, phone sheet, toggle, cursor, quote card, comment box, 3 icons, teaser) written from scratch; about 10 scenes in 30 s. Realistic 2-3 build rounds.
2. **The style leans stepped** (pixel mascot, UI on ones); the client banned robotic motion. I override everything to continuous eased curves, but the library gives no proven reference for that look; it must be proven by looking at frames, not numbers.
3. **Reading time vs 30 s**: DIRECTOR s7 says hold text (letters/15 + 1.5 s). The real quote cannot be fully read in the time available. Mitigation in shot 2.
4. **Brand colour**: client wants lime; OpenAI's own green is `#10A37F`. Lime is a design choice, the mark itself stays unmodified geometry (colour only).
5. **Loop seam**: ending on the Snapchat teaser vs hook frame; `qa.py` loop-seam check may flag it. Mitigation: last 0.5 s drifts the ground tint back to the hook palette (no hook content), or accept the flag.

---

## (b) Shot list (second by second)

Global construction: ONE continuous camera journey over a light "page world". Scenes are stations along a vertical strip; the camera glides from station to station (1.2-1.6 s, ease in-out) while the next scene's elements are already easing in (overlap), so nothing cuts and nothing waits. Zoom always >= 1.00, drifting 1.00 -> 1.05 inside each station. A "scroll down" journey also feels native to Reels viewers.

Lanes (every shot): **Lane A headline** y 285-500; **Lane B visual** y 540-1230; nothing in y > 1248 except decorative ground drift (`data-decor`).

Line timings are targets (voice retimes):

| Shot | Time | Line |
|---|---|---|
| S1 | 0.0-1.8 | L1 "ChatGPT may think you're a kid!" |
| S2 | 1.8-5.0 | L2 "Even if you typed an adult birthday." |
| S3 | 4.2-7.0 | L3 "It guesses from how you use it." |
| S4 | 7.0-9.6 | L4 "Then it can switch on teen rules." |
| S5 | 9.6-12.2 | L5 "You get an email, and a message in the app." |
| S6 | 12.2-15.2 | L6 "Check it: Settings, Account, Age." |
| S7 | 15.2-19.6 | L7 "Adult, and it's wrong? You can prove it with a selfie or an ID." |
| S8 | 19.6-22.6 | L8 "Did it say you're under 18? Tell me below." |
| S9 | 22.6-24.8 | L9 "The setup's in the link in bio." (locked clip) |
| S10 | 24.8-30.0 | L10 "Tomorrow, I'll show what Snapchat's AI can still see in Ghost Mode. Follow, so you can check it too." |

Payoff arrives at 12.2 s (S6), slightly after the ~10 s target in the house rule; S1-S5 are each their own surprise (see per-shot "new"), and S4-S5 are consequence beats, not setup. If voice allows, tighten L3-L5 to bring S6 to ~11 s.

Ambient layer in EVERY shot (so no frame is ever static): ground dot lattice drifts 10 px/s diagonally; two big soft lime-wash blobs breathe (scale 1.00-1.06, period 9 s and 13 s, opposite phases); every card floats +-5 px on its own sine phase; camera slow drift/zoom.

### S1 0.0-1.8 s: the claim, frame 0 complete (see (d))
- On screen: ChatGPT mark + "ChatGPT"; "UNDER 18?"; field "You typed your birth year: 1998 [example]".
- Words on screen: ChatGPT, UNDER 18?, You typed your birth year, 1998, example, re-created.
- Moves: camera 1.00 -> 1.03; lime pixel "?" tile rocks +-2 deg (sine); a soft lime highlight band sweeps left to right behind "UNDER 18?" (t 0.3-1.5, "it's thinking"); caret in the year field breathes (opacity sine, not blink); field card floats.
- New surprise: the contradiction itself (adult year vs "UNDER 18?").
- Muted test: sound off, a viewer reads "ChatGPT ... UNDER 18? ... typed 1998". Claim clear at 0 s; no word needs the voice. PASS.

### S2 1.8-5.0 s: "even if you typed an adult birthday" + the real proof
- 1.8-2.9: the hook block (UNDER 18?) scales to 0.40 and glides up-left into Lane A as a headline; the year card glides up to the middle; a lime pixel check mark appears on "1998" with the soft tag "adult" (re-created screen, tag "example" stays).
- 2.6-5.0: the **quote card** rises from below and the year card slides up and dims to 40%. Quote card = frosted white card, typed text (not a screenshot): "... even if you already gave your date of birth when you created your account." Source line under it: "OpenAI Help Center: Age prediction in ChatGPT". A lime marker band highlights "even if you already gave your date of birth" word by word in step with L2; the rest of the quote is ink-2 (grey). Push-in 1.00 -> 1.06 on the highlighted words ("spotlight freeze" native move).
- Words on screen: adult, even if you already gave your date of birth, source line. Headline (Lane A): "Even with an adult birthday."
- New surprise: "this is the company's own page".
- Muted test: reading "even if you already gave your date of birth" is possible in about 2 s because everything else is dimmed and only that phrase is lit; the full sentence is not expected to be read. PARTIAL PASS (risk 3).

### S3 4.2-7.0 s: how it guesses (clues)
- Quote card exits upward (scale 0.96, opacity to 0 over 0.7 s); three clue cards enter from below, staggered 0.35 s, overlapping: [speech-bubble icon] "What you chat about", [clock icon] "When you chat", [calendar icon] "How old your account is" (all from the verified list; heading "Some of its clues" because the page lists examples, not a full list).
- A thin lime line draws from card to card into a lime pixel "?" (the guess), the "?" pulses softly.
- Moves: cards float; line draws on a linear-ish long curve; each icon animates (bubble typing dots, clock hand sweeping, calendar page flip-fade).
- New surprise: it is NOT your birthday, it is your habits.
- Muted test: three icons with 3-5 word labels explain the idea. PASS.

### S4 7.0-9.6 s: teen rules switch on
- Clue cards compress into a single row "teen guess"; a toggle labelled "Teen rules" slides OFF -> ON (lime, 0.8 s, ease in-out, thumb glides, no overshoot). Two chips fade/scale up beneath: [crossed-eye icon] "Less scary stuff" and [crossed ad icon] "No ads".
- Words: Teen rules, Less scary stuff, No ads. (Page wording: graphic violence, risky challenges, etc.; we simplify to "scary stuff", true to the claim.)
- New surprise: it changes what you see (the stake). "No ads" also has a real upside, which is honest and not alarmist.
- Muted test: toggle + two chips; PASS.

### S5 9.6-12.2 s: you get a message
- Two re-created notices float in from the sides and settle: an envelope with a lime "1" dot labelled "Email", and a chat bubble with greeked grey bars (no invented wording) labelled "In the app". A small lime tick runs between them.
- Both tagged "re-created".
- New surprise: it tells you (and so you can act).
- Muted test: icons + two labels. PASS. Greeked bars on purpose: the exact banner text is unverified, so it is not invented.

### S6 12.2-15.2 s: THE PAYOFF, check it
- Camera glides to a tall UI sheet (x 115-965). Lane A headline "Settings > Account > Age" (words lit in order). Cursor travels a smooth minimum-jerk path and taps "Settings" row, sheet slides to "Account" list, taps "Age", sheet slides to the "Age" screen showing a row "Age category" with a value chip that soft-rolls between "Adult" and "Under 18" (both tagged "example"). A lime ring (outline only) draws around the row.
- Words: Settings, Account, Age, Age category, example, re-created.
- New surprise: you can see your own category right now (payoff: something to copy).
- Muted test: breadcrumb + three taps. PASS.
- Note: Settings > Account > Age shows the category and does not let you edit the birthday: keep the screen without any "edit birthday" field.

### S7 15.2-19.6 s: wrong? prove it
- Headline: "Wrong? Prove you're an adult." Two large pictograms: a round selfie viewfinder (face-less circle with lime corner brackets that breathe in) and an ID card (rounded rect with lines). Between them the word "or". A lime pixel check on "Adult" lands softly at the end.
- Small honest note under, 34 px: "Not on every account yet" is NOT in the script; use "Availability varies" only if the voice script adds it. Default: omit text, note in the caption of the post.
- Moves: viewfinder brackets slide in 0.6 s, ID card slides in with a light parallax; a soft scan line passes over the ID card (linear, 1.4 s).
- New surprise: there is a way to fix it.
- Muted test: selfie + ID icons + "Wrong?" PASS.

### S8 19.6-22.6 s: comment trigger
- A re-created comment box (white card, empty field, a soft typing-dots "..." loop, caret) and the headline "Did it say under 18?" with a soft lime down-arrow (inside safe box, y <= 1180) pointing at the field. No fake comments, no fake avatars with text.
- New surprise: a direct question to me.
- Muted test: "Did it say under 18? ... below". PASS.

### S9 22.6-24.8 s: "The setup's in the link in bio." (locked scene A)
- Background locks to ONE pose, shared with S10 (camera drift continues smoothly across the S9-S10 boundary, no re-zoom/reset). A large lime pill "Link in bio" with a chain-link icon, soft pulse (scale 1.00-1.03, 1.4 s period); beneath it the 3-step route "Settings, Account, Age" as three small chips (the "setup").
- No @handle (full-bleed screen rule).
- Muted test: "Link in bio" + the 3 steps. PASS.

### S10 24.8-30.0 s: tomorrow teaser + follow (locked scene B; same background as S9)
- 24.8-26.4: the "Tomorrow" kicker and a Snapchat-yellow (#FFFC00) rounded card rise in with the REAL Snapchat ghost mark (to be sourced) and a re-created switch "Ghost Mode" (tag "re-created").
- 26.4-28.8: the switch glides ON (2.4 s linear-ish ease) while a pixel eye "?" hovers near it; headline "Tomorrow: Snapchat's AI + Ghost Mode"; subline "What can it still see?" (question, not a claim).
- 28.8-30.0: card drifts up 40 px; a lime "Follow" pill below fills with a soft glow and a pixel check; "so you can check it too".
- New surprise: a concrete next thing (reason to follow).
- Muted test: "Tomorrow", Snapchat logo, Ghost Mode, Follow. PASS only if the Snapchat claim is verified live (see Open items).

Sound (channel pipeline): voice first; music bed from the real library at -6 to -18 dB band under voice; soft foley (card whooshes, a muted tick on toggle) kept off word onsets. Measured, not heard.

---

## (c) Palette tokens, type, easing, motion rules

```
:root {
  --paper:      #F6F7F2;  /* ground, warm light */
  --paper-2:    #EBEEE3;  /* lattice dots, section tint */
  --card:       #FFFFFF;  /* cards, frosted at 92% */
  --ink:        #0E0F0C;  /* headlines, heavy type */
  --ink-2:      #4A4F44;  /* secondary text, 8:1 on paper */
  --lime:       #A3E635;  /* accent fills: pills, ring, toggle, marker band */
  --lime-deep:  #5DA10E;  /* thin strokes only (never text) */
  --lime-wash:  #E6F8BB;  /* blobs, highlight washes */
  --shadow:     rgba(14,15,12,.10);
  --snap-yellow:#FFFC00;  /* guest colour, S10 teaser card only (real Snapchat brand yellow) */
}
```
Rules: lime is never text colour on white (contrast). Black text sits on lime (13:1). No second accent except the teaser's yellow. No dark ground anywhere.

Type (English only, self-hosted, OFL):
- Display: Inter Tight 900 (headline, "UNDER 18?"), 800 for labels, tracking -2%.
- UI/body: Inter 600, 38-48 px for on-screen words; **minimum on-screen size 34 px** (phone legibility; "re-created" and "example" tags use DM Mono 500 at 30 px, still above 28).
- Headline lane: 84-96 px 900, max 3 lines; sentence-case; at most 6 words per shot.

Easing (only these):
- `enter`: cubic-bezier(.16,1,.3,1), 0.9-1.2 s, for elements arriving (critically damped feel, zero overshoot).
- `camera`: cubic-bezier(.45,.05,.25,1), 1.2-1.6 s, for glides between stations.
- `settle`: critically damped spring (zeta = 1), 0.7 s, for toggles/chips.
- `ambient`: sine, periods 7-13 s, amplitudes 4-8 px.
- `cursor`: minimum-jerk (smootherstep) along a cubic bezier with slight arc; speed 700-1100 px/s; click = scale 0.92 -> 1.00 over 0.25 s.
- Typing (year digits, comment dots): per-character delay 70-130 ms from a seeded sequence (no stepped cadence).
- Never: linear on moving UI (except the scan line and line-draw), back-ease, bounce, hard cut, pop.

Motion rules:
1. Every element enters with opacity 0 -> 1 AND translate 40 px + scale 0.96 -> 1 together, over >= 0.9 s; exits start before the next scene's camera glide ends (overlap >= 0.4 s).
2. Max still time for any pixel-region of interest: 2.0 s (budget under 2.5 s). Ambient drift runs always.
3. Nothing begins or ends on frame 0/last frame as a fade from nothing: frame 0 is complete (QA blank-first-frame check).
4. Spoken-word emphasis: lime marker band behind the word (not text colour change), fades in 0.25 s, no scale.
5. Everything is a pure function of t (seeded noise; `mulberry` from `core/lib.js`).
6. Pixel props (the "?" tile, check, sparkles) scale/fade smoothly; they sit on a fixed 8 px grid and never step in position.

---

## (d) Hook frame 0: composition (1080x1920, safe box x 65-1015, y 269-1248)

All boxes are inside the safe box. Camera at 1.00 at t = 0.

| Element | Box (x0-x1, y0-y1) | Detail |
|---|---|---|
| ChatGPT mark tile | 80-212, 290-422 | 132 px lime rounded tile (r 36), real mark in ink `#0E0F0C`, mark scaled to 84 px, centred |
| "ChatGPT" | 236-520, 322-392 | Inter Tight 800, 64 px, ink |
| "UNDER" | 80-905, 455-670 | Inter Tight 900, 250 px, ink, cap top y 470, baseline y 652 |
| "18" | 80-560, 690-1010 | Inter Tight 900, 400 px, ink, baseline y 992 |
| "?" pixel tile | 600-890, 705-995 | lime tile r 48, black pixel-grid "?" (8 px cells), rocks +-2 deg |
| Field card | 80-1000, 1050-1230 | white, r 40, soft shadow (blur 40, y 12) |
| field label | 120-700, 1075-1110 | "You typed your birth year" Inter 600, 34 px, ink-2 |
| field value | 120-420, 1118-1200 | "1998" Inter Tight 800, 84 px, ink + soft breathing caret |
| "example" pill | 690-940, 1118-1176 | lime pill, ink text 34 px |
| "re-created" tag | 690-960, 1190-1222 | DM Mono 30 px, ink-2 |

Why it works muted: three reads in 3 s, top to bottom: **ChatGPT -> UNDER 18? -> You typed: 1998 (example)**. The contradiction needs no sound. The "?" tile is the only lime mass in the headline, so the eye lands on the question.
Instagram profile-grid crop (centre 1:1 ~ y 420-1500): "UNDER 18?" and the field are inside it.
Risks to check at render: block height 455-1010 + card to 1230 is dense; if safe_check flags overlap, reduce "18" to 360 px and shift the card to y 1030.

---

## (e) "Nothing covers what the screen shows": per-shot checklist

General rule: overlays are only (1) the headline in Lane A y 285-500 (above all UI), (2) outline-only marks (rings, underlines) that sit on borders, (3) the cursor resting at the right end of a row. Run `node export/safe_check.js` (text inside the safe box, text vs text) AND look at frames.

- [ ] S1: nothing over the year field text; the highlight band is BEHIND the headline letters (z below ink); "re-created" tag outside the value box.
- [ ] S2: the lime marker band lives behind the quote words; source line below the card, not on it; dimmed year card never overlaps the quote card (>= 24 px gap).
- [ ] S3: connector line passes in the 24 px gutters between cards, never across a label; "?" has its own space right of the cards.
- [ ] S4: toggle thumb and label do not touch the chips; chips are below the toggle (>= 30 px gap).
- [ ] S5: tick/line between the two notices passes through the gap, not over bars or labels; the "1" dot sits on the envelope corner, outside the "Email" label box.
- [ ] S6: breadcrumb in Lane A, sheet starts y >= 540; cursor tip rests on the row's chevron at the right (x ~ 900), never on the row label; the ring is a 8 px outline hugging the row, no fill; value chip not overlapped by the cursor at the moment it is read (cursor moves out 0.5 s before the chip rolls).
- [ ] S7: ID card and viewfinder are the subjects; the scan line is a 4 px line crossing the ID, no text on the ID is hidden (ID uses abstract lines, no real data); "or" sits between them in the gutter.
- [ ] S8: arrow tip points at the field edge (not over it); the typing dots are inside the field, left aligned, the caret does not collide with the placeholder text.
- [ ] S9: link pill and the 3 step chips are separate rows (>= 40 px gap); nothing sits where Instagram draws UI (y > 1248).
- [ ] S10: yellow card text sits left of the ghost mark; the switch thumb never covers the "Ghost Mode" label; the Follow pill below the card (>= 40 px), its glow is outside the label.
- [ ] No @handle anywhere (full-bleed screens).
- [ ] No frame where a headline word lands on a UI word (cross-check at every scene boundary, because enter/exit overlap).

---

## (f) Real vs re-created

| Item | Status | How shown / labelled |
|---|---|---|
| ChatGPT mark | **REAL** (Wikimedia Commons `chatgpt.svg`, no fill set) | Geometry unchanged; coloured ink on a lime tile. Never redrawn. Check the mark is still the current one (OpenAI re-branded the mark in 2025; verify against the file's source page before ship) |
| "OpenAI Help Center: Age prediction in ChatGPT" quote | **REAL TEXT, typed** from the page (verified by the channel on 3 Nov 2026: "... even if you already gave your date of birth when you created your account.") | Card shows the exact words and the page name; re-read the page on the day of publishing (page changes) |
| Birth-year field "1998" | **Re-created** | Tag "example" and "re-created" |
| "UNDER 18?" | **Our headline**, phrased as a question, not a banner | Not styled as an app banner |
| Clue cards (chat, time, account age) | **Real facts** (verified signal examples), our icons | Heading "Some of its clues" (examples, not complete) |
| Teen rules toggle, chips | **Re-created** | "Less scary stuff", "No ads" paraphrase verified teen rules; toggle is a metaphor, tag "re-created" |
| Email and in-app notice | **Re-created, greeked** | No invented wording; tag "re-created" |
| Settings > Account > Age screens | **Re-created** | Tag "re-created"; "Adult" / "Under 18" chip labelled "example"; no "edit birthday" field (the real screen doesn't have it) |
| Selfie / ID | **Our pictograms**; the Persona flow is real but not shown | No Persona branding (not needed, would need a real logo) |
| Comment box | **Re-created** | Empty field, no invented comments |
| Link in bio pill, Follow pill | **Generic UI**, not Instagram-branded | No platform logo drawn |
| Snapchat ghost mark | **REAL, still TO SOURCE** (Snap brand page or Wikimedia Commons) | Never redrawn; yellow card uses Snap's real yellow |
| Ghost Mode switch | **Re-created** | Tag "re-created" |
| Pixel "?" and check | **Our decoration** | Not a brand mark |

Never present as real: any banner or email wording, any app UI text we did not read on the page.

Open items before build (house rules): (1) live-verify Snapchat "My AI" and Ghost Mode wording and that tomorrow's episode will exist (the promise is binding); (2) source the Snapchat mark; (3) re-open the Help Center page and compare the typed quote character for character; (4) confirm the path name "Settings > Account > Age" on the day (it is from the page; UI labels move); (5) run `audio/script_lint.py --cues` on the lines (already 0 risky words per the channel's check); (6) the face pre-check is not needed (no photos).

---

## (g) Self-score of the plan (strict)

| Criterion | /100 | Why |
|---|---|---|
| Muted clarity | 86 | Frame 0 carries the claim; every shot has icons plus 3-6 words. Loses points: S2's real quote cannot be read fully in time; S7 relies on icons for "prove it". |
| Aliveness (no still > 2.5 s) | 88 | Ambient layer on every shot plus continuous camera; per-shot motion specified. Loses points: S2 hold on the quote card, S9 locked scene (pulse + drift only); not yet measured. |
| 8-year-old clarity | 84 | Simple words ("kid", "clues", "scary stuff"). Weak spots: "Teen rules", "ID", "category" and "verify" ideas; "Under 18" itself for the youngest. |
| Hook per shot | 82 | Each shot has a named "new" beat. S5 (email) and S9 (CTA) are the weakest surprises; S8 is a prompt, not a reveal. |
| Brand / real-logo fidelity | 76 | ChatGPT mark real; quote real. Deductions: Snapchat mark not yet sourced; lime is not OpenAI's official `#10A37F`; many "re-created" tags add small clutter; real-logo for any other named product: none else named. |
| Smoothness (not robotic) | 80 | All easings are continuous and overlapping by rule. Deduction: the chosen style leans stepped and I have only overridden it on paper; toggles and typed digits need frame review. |
| Producibility with this library | 62 | No engine patch needed, but the demo source is absent, the vertical UI kit is all new code, 10 scenes in 30 s, two sourcing blockers (Snap mark, live verification) and a reading-time compromise. A 2-3 round build. |

Overall (simple mean): **79 / 100**.

### The 3 weakest points
1. **Producibility (62)**: everything above engine level (vertical UI kit, icons, cursor, quote card, teaser) is new code; the demo to learn from must be fetched after the treatment; style leans stepped. Mitigation: build the kit as pure functions of t on the existing 1080x1920 scaffold, review contact sheets after each station, cap the build at S1-S6 first.
2. **Quote card readability and timing (S2)**: the proof frame is the real text, but a 30 s film gives it about 2.5 s on screen. Viewers will read only the lit phrase; the rest is texture. If retention on the proof beat is the concern, shorten the quote to "even if you already gave your date of birth" and keep the full sentence in the caption.
3. **Closing beat depends on unverified, unfinished things**: the Snapchat teaser needs a live check of the product/feature, a real logo not yet in hand, and a binding promise for tomorrow's episode; and the payoff (S6) lands at 12.2 s, later than the house target of ~10 s.
