# Design plan v2: "IS CHATGPT SAVING STUFF ABOUT YOU?" (ChatGPT Memory), 28 s, 1080x1920, 24 fps, light

Status: plan only. Nothing built, nothing rendered. All times are targets; the picture follows the narration, so the producer retimes every time from the real voice cues (`window.CUES`, from whisper word times).
Inputs read: script-v2.md; previous plan design-plan-chatgpt-age.md; STYLE.md (living-screencast), TECHNIQUE.md, DIRECTOR.md, AGENTS.md, core/README.md (confirmed: every page tool takes `--size WxH`, layout from `innerWidth x innerHeight`).

What I fixed from the previous plan's 3 weak points:
1. Producibility (62): ONE reusable component family instead of ten scenes of new UI: the **note card** (a small lime-wash sticky card) is the through-line of the whole film (appears S1, multiplies S2-S3, survives the delete in S4, is listed in S5, ghosts in S6). Station count cut to 7 plus 2 closing scenes, no pixel mascot, no cursor-heavy flows (one short cursor path only, in S5). A phase-gated build (S1-S4 first) is in (g).
2. Quote readability: the quote is no longer a side beat; it IS the twist. It is shortened with an ellipsis (words unaltered), held 3.4 s fully lit, and the visual surprise (chat vanishes, note stays) plays above it at the same time so the proof and the surprise are one moment.
3. Late payoff and unverified closing: the payoff (the twist) lands at 8.4 s, before the 10 s target; the closing teaser uses only things already in hand (the real ChatGPT mark, a generic empty birthday field), no third-party logo and no third-party claim.

---

## (a) Why this style, honest risks

Pick: **living-screencast, light theme, heavily adapted**. Same reasoning as the previous plan, now stronger: this film is literally a product-UI explainer (a chat, a chat list, a Settings path, a toggle, an official quote). Its grammar is "real labels, redrawn UI, one feature per sentence, camera pushes to where it happens, spotlight freeze on the one promise" = our proof frame. Rejected again: swiss-motion (snaps, "nothing bounces", wipes only = robotic), pictogram-motion (beat-locked), iso-infographic (too heavy), dataviz (no data), whiteboard (a real logo and a real quote sit badly on a marker board, most expensive engine).

Deviations from STYLE.md (disclose to the library owner; "keep all of it" is not possible):
1. No pixel mascot (it would read as an invented ChatGPT character and adds stepped motion).
2. 24 fps, no position stepping (all sub-pixel smooth). UI "on ones" dropped.
3. Phone-width layout: floating cards on a light ground instead of a desktop window on wallpaper.
4. No bottom caption pill (bottom 35% = Instagram UI). One headline lane per shot, spoken words lit.
5. No keystroke HUD.
6. Light ground instead of the style's default product-dark; STYLE.md s3 allows it ("follow the product's real light theme").

Honest risks, what must be custom-built:
- The living-screencast `demo/` source is NOT in this clone (sparse). Everything above `core/` is new: `ui.js` (chat card, chat list, settings sheet, toggle, quote card, comment box, note card, 6 icons), a camera, a cursor, a text typer. A 1080x1920 scaffold exists at `.../scratchpad/lemo-demo/engine.js`+`main.js` (UNVERIFIED, not re-run); use as a shell only if it runs.
- The style leans stepped; I override on paper only. Smoothness must be proven by looking at frames and a motion-energy graph, not asserted.
- Reading time: even the shortened quote is ~95 characters; 3.4 s is enough only because everything else on screen is dimmed and the words are lit in step with speech. DIRECTOR s7 formula (letters/15 + 1.5 s = 7.9 s) is NOT met; this is a deliberate compromise (full quote goes in the post caption).
- Voice mismatch: the brief says Kokoro; the locked line 8 ("The setup's in the link in bio.") is a clip in the channel's cloned voice. Mixing two voices in one film is bad. Either use the locked clip only if the whole film uses the channel voice, or render line 8 with Kokoro and flag that the locked-clip rule is broken. Decision for David, not the producer.
- Lime (`#A3E635`) is our accent, not OpenAI's own green (`#10A37F`); the mark geometry stays untouched, only coloured.
- Loop seam: film ends on the age teaser, starts on the memory hook. Accept a qa.py loop-seam flag or drift the last 0.5 s of ground tint back to the hook tint.
- Official ChatGPT UI images: see (f). Found and fetchable, NOT used.

---

## (b) Shot list

Global construction: one continuous camera over a light "page world"; stations along a vertical strip, camera glides 1.2-1.6 s between them while the next station's elements are already easing in (overlap), zoom >= 1.00 drifting to 1.05 per station. Lanes: **A headline y 285-520**, **B stage y 540-1235**; nothing needed below y 1248.

Ambient layer (every shot, so no frame is still): dot lattice drifts 10 px/s diagonally; two lime-wash blobs breathe (scale 1.00-1.06, periods 9 s and 13 s, opposite phases); every card floats +-5 px on its own sine phase; camera drift.

| Shot | Time | Line |
|---|---|---|
| S1 | 0.0-2.6 | L1 Is ChatGPT saving stuff about you? |
| S2 | 2.6-5.6 | L2 It can, on its own. Ask it to show you. |
| S3 | 5.6-8.4 | L3 Type: what do you know about me? |
| S4 | 8.4-12.4 | L4 Now the twist: delete the chat, and the note can stay. |
| S5 | 12.4-15.6 | L5 To see them: Settings, Personalization, Memory. |
| S6 | 15.6-19.4 | L6 Don't want that? Switch memory off, or use a Temporary Chat. |
| S7 | 19.4-22.0 | L7 What did it know about you? Tell me below. |
| S8 | 22.0-23.8 | L8 The setup's in the link in bio. (locked) |
| S9 | 23.8-28.0 | L9 Tomorrow, I'll show how ChatGPT can guess your age. Follow, so you can check it too. |

Payoff = S4 at 8.4 s; the "thing to copy" (the question to type) is shown at 5.6 s.

### S1 0.0-2.6 hook (frame 0 complete, see (d))
- Screen: ChatGPT mark + "ChatGPT"; headline IS CHATGPT / SAVING STUFF / ABOUT YOU?; chat card with a user bubble typing "what do you know about me?" and answer lines already starting.
- Moves: user bubble types 0-1.6 s (seeded 70-130 ms per char); at 0.5 s answer line 1 fades in (a generic example note sentence), 1.0 s and 1.5 s two greeked bars grow in from the left (width ease, 0.9 s); the first note card peels out of answer line 1 and floats toward the right at 1.8-2.6 s; lime band behind "ABOUT YOU?" sweeps left to right once (0.3-1.8); camera 1.00 -> 1.03.
- New surprise: the answer starts to list things about "you" before the voice has said anything.
- Muted test: reads "ChatGPT / saving stuff about you? / what do you know about me? -> it answers". PASS.
- Words: IS CHATGPT SAVING STUFF ABOUT YOU?, what do you know about me?, example, re-created.

### S2 2.6-5.6 "It can, on its own." (note cards appear without a click)
- Headline lane (A): "It saves notes. By itself." (6 words max, spoken words lit by lime band).
- Stage: the chat card from S1 slides down-left to 70% and dims; three note cards drop one by one (0.5 s apart, enter curve) from the chat into a small stack at right, each stamped with a tiny lime pin; note texts are generic examples: "Likes short answers", "Studying for exams", "Has a dog" (tag example, no real details). A small label chip "no button pressed" is NOT added (claim beyond script); instead the pins appear with no cursor in the frame, which shows "on its own" visually.
- Then (4.4-5.6) a hint arrow-less nudge: the chat bubble reappears at the bottom as an empty input with a soft caret: "Ask it to show you" -> sets up S3.
- New surprise: it writes notes about you while you only chat.
- Muted test: "It saves notes. By itself." + three note cards. PASS.

### S3 5.6-8.4 "Type: what do you know about me?" (the thing to copy)
- Headline: "Ask: what do you know about me?" with the question words lit as spoken (this exact text is also a copyable line; it is large, 56 px, inside a white prompt card y 560-700).
- Stage: the note stack fans out into a vertical list of 4 answer lines (y 740-1180), each line a short "You ..." sentence with its note card sliding in staggered 0.35 s, last one half-greeked so no wording is invented.
- Camera pushes 1.00 -> 1.05 on the prompt card then glides down to the list.
- New surprise: the list is about you and it is right there.
- Muted test: the prompt is on screen as text; PASS.

### S4 8.4-12.4 THE TWIST: a chat disappears, a note stays
- 8.4-9.2 Lane A headline "Delete the chat." (lit as spoken); stage upper half (y 540-860): a mini chat list, three rows ("Chat about dinner" highlighted, two others greeked) on the left and one note card ("Studying for exams") on the right, pinned.
- 9.0-10.0 a trash icon in the highlighted row glows (lime ring draws, 0.5 s); the row shrinks (height 100 -> 0, opacity 1 -> 0, 0.9 s ease) and the rows below slide up to close the gap. A soft particle-free fade, no pop. The note card does NOT move except for its float; a lime ring draws around it and a small tag "still here" fades in. At 10.4 s headline changes to "The note stays." (cross-fade 0.4 s, same lane).
- 9.2-12.6 proof frame: the **real quote card** rises into y 900-1235 (card x 80-1000, enters from y +60, 1.0 s, enter curve). Text (Inter 600, 42 px, 4 lines): "...even if you delete a chat, any saved memories from it can still be used in future conversations." Source line (DM Mono 30 px): "OpenAI Help Center, Memory FAQ". A lime marker band lights "even if you delete a chat" at 9.6-10.4 and "any saved memories ... can still be used" at 10.6-12.2; the rest at ink-2 but fully legible (not dimmed below contrast 7:1). Slow push 1.00 -> 1.04 on the card (spotlight freeze), vignette at 6% only on the stage, never on the quote. Fully lit and readable from 10.0 to 12.6 = 2.6 s plus 0.8 s of the entry/partial = at least 3.4 s on screen, as required. The quote card stays through the S4/S5 camera glide (exit starts 12.4, ends 13.0).
- New surprise: deleting did not delete the note; the company says so itself.
- Muted test: "Delete the chat. -> chat row vanishes -> note stays -> quote from OpenAI Help Center". PASS (quote partly read, rest is the proof texture).

### S5 12.4-15.6 "To see them: Settings, Personalization, Memory."
- Headline (lane A): "Settings › Personalization › Memory" in three lines or one at 76 px; each word lit in order.
- Stage: tall settings sheet x 115-965, y 560-1230 (re-created). One cursor path (smootherstep, 800 px/s, slight arc, 0.25 s click scale) taps "Settings" -> sheet slides left, list shows "Personalization" -> tap -> slides -> "Memory" screen with a toggle (ON, lime), a "Manage" button, and a short list of 3 note rows (the same 3 note texts as S2, so the viewer recognises them: payoff of the through-line). Ring outlines the memory list. Tag re-created.
- Cursor rests on the row chevron at x ~ 900, never on a label.
- Labels must be live-verified before the build (UI labels move). Generic fallback: "Memory" row + toggle + "Manage".
- New surprise: the notes are readable, in a place you can open.
- Muted test: breadcrumb + 3 taps + the 3 notes. PASS.

### S6 15.6-19.4 "Don't want that? Switch it off, or use a Temporary Chat."
- Headline: "Two ways out." (not in the script; replace with spoken-word lit "Switch memory off / Temporary Chat" if the producer wants zero added words: default = lit script words).
- Upper stage (y 540-840): the Memory toggle from S5 slides ON -> OFF (0.8 s, settle curve, lime -> grey), the 3 note cards next to it go to 30% ghost (opacity + slight shrink).
- Lower stage (y 900-1230), from 17.0: a card "Temporary Chat" with a dashed-outline bubble; a fresh note card tries to drift into it and fades out softly before touching (0.9 s) with a small "no notes" badge. Verified fact: Temporary Chats do not use or create memories.
- New surprise: you have two real exits.
- Muted test: toggle going grey + dashed chat + "no notes". PASS.

### S7 19.4-22.0 "What did it know about you? Tell me below."
- Headline "What did it know about you?" A large white comment card (x 80-1000, y 700-1000), empty field, soft typing dots loop, caret. A big lime note card drifts in and tilts toward the field (it is the viewer's own note about to be shared). Lime down-arrow at y <= 1150 pointing at the field edge. No fake comments, no avatars.
- New surprise: a direct challenge that uses the thing they just saw.
- Muted test: PASS.

### S8 22.0-23.8 "The setup's in the link in bio." (locked scene A)
- Background pose locked and shared with S9 (camera drift continues across the boundary, no reset). Lime pill "Link in bio" with a chain icon (pulse 1.00-1.03, 1.4 s), below it three chips "Settings", "Personalization", "Memory" as the setup. No handle.
- Muted test: PASS.

### S9 23.8-28.0 tomorrow teaser (locked scene B, same background)
- 23.8-25.6 kicker "TOMORROW" (ink) and a white card rising in with the real ChatGPT mark and an empty birthday field "Birthday  __ / __ / ____" (re-created, no digits). 
- 25.4-26.6 a lime tag "UNDER 18?" scales in (0.96 -> 1.00 with opacity) on the field's right edge, with a soft glow ring; the empty field gets a thin lime outline.
- 26.2-28.0 headline "ChatGPT can guess your age"; Follow pill below fills with a soft glow and a pixel check; last 0.5 s ground tint eases toward the hook tint.
- New surprise: the next thing, already visible (the follow reason).
- Muted test: Tomorrow + ChatGPT mark + birthday field + UNDER 18? + Follow. PASS. The promise is binding (episode must exist tomorrow).

Sound: voice first; music bed from the channel's real library (not synthesised) -6 to -18 dB under voice in 300-3500 Hz; soft foley (card whoosh, a muted tick on toggle and trash) offset from word onsets. Measured, not heard.

---

## (c) Palette, type, easing, motion rules

```
:root {
  --paper:     #F6F7F2;  /* ground */
  --paper-2:   #EBEEE3;  /* lattice dots, tints */
  --card:      #FFFFFF;  /* cards at 92% */
  --ink:       #0E0F0C;  /* headlines, heavy type */
  --ink-2:     #4A4F44;  /* secondary text, >= 7:1 on card */
  --lime:      #A3E635;  /* ChatGPT accent: fills, ring, toggle, marker band */
  --lime-deep: #5DA10E;  /* thin strokes only, never text */
  --lime-wash: #E6F8BB;  /* blobs, note cards */
  --shadow:    rgba(14,15,12,.10);
}
```
Lime is never text on white; black on lime is 13:1. No second accent, no dark ground anywhere.

Type (self-host, OFL): Inter Tight 900 headlines (-2% tracking), 800 labels; Inter 600 UI/body 38-48 px; DM Mono 500 30 px tags. Minimum on-screen size 30 px for tags, 34 px for readable words. Headline lane 84-120 px, max 3 lines, at most 6 words per shot.

Easing (only these): `enter` cubic-bezier(.16,1,.3,1) 0.9-1.2 s, no overshoot; `camera` cubic-bezier(.45,.05,.25,1) 1.2-1.6 s; `settle` critically damped spring zeta=1, 0.7 s (toggle, chips); `ambient` sine 7-13 s, 4-8 px; `cursor` smootherstep on a cubic with slight arc, 700-1100 px/s, click 0.92 -> 1.00 in 0.25 s; typing delay 70-130 ms seeded per char; linear only for line-draw and ring-draw. Never: back-ease, bounce, pop, hard cut.

Motion rules: (1) every element enters with opacity + 40 px translate + scale 0.96 -> 1 together over >= 0.9 s; (2) exits start before the next camera glide ends (overlap >= 0.4 s); (3) no still region longer than 2.0 s (budget 2.5 s); ambient always on; (4) frame 0 complete (no fade from nothing); (5) spoken-word emphasis = lime band behind the word, 0.25 s fade, no scale, no colour swap; (6) all motion a pure function of t, seeded noise (`mulberry` in `core/lib.js`); (7) the note card is the one recurring object, same size and pin in every shot, so the eye follows it.

---

## (d) Frame 0 composition (1080x1920, safe box x 65-1015, y 269-1248; camera 1.00)

| Element | Box (x0-x1, y0-y1) | Detail |
|---|---|---|
| ChatGPT mark tile | 80-200, 290-410 | 120 px lime rounded tile r 34, the real SVG (no fill set) filled ink #0E0F0C, 76 px, centred |
| "ChatGPT" | 220-520, 318-382 | Inter Tight 800, 60 px, ink |
| Headline line 1 "IS CHATGPT" | 80-1000, 440-560 | Inter Tight 900, 120 px, baseline y 548 |
| line 2 "SAVING STUFF" | 80-1000, 565-685 | same, ~840 px wide |
| line 3 "ABOUT YOU?" | 80-1000, 690-810 | lime marker band 70-640 x 700-800 behind "ABOUT YOU?" (band sweeps in over 0.3-1.8 s; at t=0 it is already 35% filled) |
| Chat card | 80-1000, 870-1235 | white r 40, shadow blur 40 y 12 |
| user bubble | 330-980, 895-985 | lime-wash, text "what do you know about me?" Inter 600 40 px, at t=0 already typed to "what do you know a|", caret breathing |
| answer line 1 | 120-960, 1015-1065 | already visible at t=0 (example sentence, generic, Inter 600 38 px) |
| answer bars 2-3 | 120-820 and 120-640, 1090-1105 / 1125-1140 | grey greeked bars, start at 20% width and grow |
| note card #1 | 700-960, 1165-1215 | lime-wash with pin, half out of answer line, floats |
| tags | 120-520, 1195-1228 | DM Mono 30 px "example · re-created" |

Muted reading order in 3 s: ChatGPT -> IS CHATGPT SAVING STUFF ABOUT YOU? -> what do you know about me? -> answer starts. The Instagram profile-grid crop (centre ~ y 420-1500) contains headline and chat. Risk: block 440-1235 is dense; if safe_check/overlap flags, reduce headline to 108 px and card top to y 850.

---

## (e) Per-shot "nothing covers the screen" checklist

General: overlays are only (1) headline in lane A above all UI, (2) outline-only marks (rings, underlines) hugging borders, (3) lime bands BEHIND text, (4) the cursor at a row's right end.
- [ ] S1: band behind letters (z below ink); tags outside the answer text; note card #1 never overlaps answer line 1's text after 2.0 s.
- [ ] S2: note cards land in a right-hand stack that does not touch the dimmed chat card (>= 24 px gap); the empty input at the bottom is inside y <= 1235.
- [ ] S3: prompt card text unobstructed; list lines >= 20 px apart; note cards beside, not over, sentences.
- [ ] S4: the vanishing row and the persistent note card are >= 40 px apart; ring is outline only; "still here" tag outside the note text; headline cross-fade does not overlap the stage (lane A only); quote card entry (from below) starts after the stage content has compressed above y 880; marker band behind quote words only.
- [ ] S5: breadcrumb in lane A, sheet starts y >= 560; cursor never rests on a label; cursor leaves the toggle 0.5 s before it is read.
- [ ] S6: toggle thumb never touches its label; the "no notes" badge sits beside the Temporary Chat card, not on the bubble text; the fading note card dissolves before reaching the card text.
- [ ] S7: arrow tip on the field edge, not inside; dots inside the field, left aligned, caret clear of placeholder.
- [ ] S8: pill and chips in separate rows (>= 40 px); nothing below y 1248.
- [ ] S9: card text left of the ChatGPT mark; "UNDER 18?" tag on the field's edge, not over the empty slashes; Follow pill >= 40 px below the card; glow outside the label.
- [ ] Whole film: no @handle; at every scene boundary (enter/exit overlap) no headline word lands on a UI word. Verify with `window.TEXTS(t)` bbox test at 8 fps plus eyes on contact sheets.

---

## (f) Real vs re-created

| Item | Status | How shown |
|---|---|---|
| ChatGPT mark | REAL: `/tmp/.../scratchpad/logos/chatgpt.svg` (no fill set; Wikimedia-derived raw files in same folder) | Geometry unchanged, coloured ink on lime tile; check the mark is the current one (OpenAI re-branded in 2025; compare with raw_OpenAI2025.svg) |
| Quote "even if you delete a chat, any saved memories from it can still be used in future conversations" | REAL TEXT, typed; source OpenAI Help Center, Memory FAQ (verified 3 Nov per script-v2) | Leading words shortened with "..." only; no word altered; re-open the page on the day of publishing and compare character by character |
| Prompt "what do you know about me" | Our wording of a documented behaviour (OpenAI: "just ask") | Shown as plain prompt, not as an OpenAI quote |
| Chat card, answers, note cards, notes text | RE-CREATED example, generic content | Tags "example" and "re-created"; no real person's answer, no personal details |
| Chat list, trash, vanishing row | RE-CREATED | Tag re-created |
| Settings > Personalization > Memory sheet, toggle, Manage | RE-CREATED; path from OpenAI page; label wording must be live-checked | Tag re-created; generic fallback if labels moved |
| Temporary Chat card, "no notes" | RE-CREATED; fact verified (no use, no creation of memories) | Tag re-created |
| Comment box | RE-CREATED, empty | No fake comments |
| Link in bio / Follow pills | Generic UI | No platform logo |
| Birthday field, "UNDER 18?" tag | RE-CREATED teaser, empty field | Tag re-created; binding promise for tomorrow |
| Official OpenAI memory-UI images | FOUND, FETCHED, NOT USED | below |

Official OpenAI memory UI images (requested check):
- OpenAI Help Center "Memory in ChatGPT", image on help.openai.com article 8590148: `https://images.ctfassets.net/j22is2dtoxu1/4HqlKblQXe9gvo2Q7NeI6P/91b47c9c42f6be15c3ef9cb3ff1c6294/8.png?q=80&fm=webp&w=1176` (curl through the proxy: HTTP 200, webp 1176x2096, 732 KB, saved at `/tmp/claude-0/-home-user-videos-ai/55529e32-2ffe-57f5-a74d-513316ab2ea5/scratchpad/oa/help8.png` and `help8.jpg`). It shows a phone with a "Sources" sheet ("Memory: You love Mexican food", menu "Why this memory?").
- OpenAI blog "Memory and new controls for ChatGPT" (2024) image: `https://images.ctfassets.net/kftzwdyauwt9/4EHJ2SA51mDPNnTqT9nz1/712f0b2f37c5fe52bc0a49f6e646c95d/memory-and-new-controls-for-chatgpt.png?w=1200&q=80&fm=png` (HTTP 200, 1200x1200 PNG, saved at `.../scratchpad/oa/blog.jpg`/`blog.webp`). Shows the old "Manage Memory" dialog with example notes incl. "Has a 2 year old daughter named Lina".
- The article pages themselves return 403 to curl (bot protection), so I could NOT read any terms or licence for these images. I claim no licence. Recommendation: do not use either in the film (blog image is the 2024 UI = stale, and contains a child's name; help image is dimmed and not our screens). Use the redrawn UI labelled re-created. They are fetchable as reference only; using them needs David's decision after reading OpenAI's terms.

---

## (g) Build recipe for a producer subagent

Work in a new project folder `/tmp/claude-0/-home-user-videos-ai/55529e32-2ffe-57f5-a74d-513316ab2ea5/scratchpad/lemo-memory/` with `LIB=/root/lemo-opuscar`. Do not edit `core/` or `styles/`. No git, no /home/user/videos-ai changes (read-only copies of channel assets are fine).

1. Setup (once): `cd $LIB && sh plugin/skills/lemo-opuscar/scripts/setup.sh deps` then `... deps voice`. Check `ffmpeg -version` >= 7 (6.x breaks `mux.sh`).
2. Fonts: download Inter Tight (900, 800), Inter (600), DM Mono (500) from github.com/google/fonts/tree/main/ofl into `lemo-memory/fonts/`; `@font-face` them, `document.fonts.ready` before `READY = true`. Copy `logos/chatgpt.svg` to `assets/` and inline it as an SVG in the page (so fill can be set to ink).
3. Files to write:
   - `index.html`: root 1080x1920 layout from `innerWidth x innerHeight`, CSS tokens from (c), `window.DUR=28`, `window.render=(t)=>`, `window.READY`, `window.TEXTS=(t)=>` (every visible text with bbox, from DOM measurement), `window.EV` (foley events).
   - `film.js`: the timeline: `CUES` (word times, filled from step 5), `S = {s1:[0,2.6], ...}`, helper `ease(name,x)`, `typed(str,t0,t1,seed)`, `W(word)` returns the spoken-word time for lit bands. Everything a pure function of t, `mulberry` for seeds.
   - `ui.js`: state-to-DOM for chat card, chat list, settings sheet, toggle, quote card, comment box, note card (one component, props: text, pin, ghost), icons (trash, chain, bubble), cursor.
   - `lines.json` (9 lines, spelled-out for TTS), `build.sh`, `mix.py`.
4. Build in phases (producibility): phase 1 = S1-S4 only (frame 0 + twist + quote), review contact sheets, fix; phase 2 = S5-S6; phase 3 = S7-S9. Do not start the next phase before the last passes the checklist in (e).
5. Voice (Kokoro): `$LIB/.venv/bin/python core/tts/tts.py lines.json out/` then `core/tts/asr_check.py` until exit 0 (watch "ChatGPT", "Temporary Chat", "Personalization"; re-spell if mis-heard). Word timestamps from asr_check go into `CUES`; retime `film.js` windows to them. Per the channel rules, run `audio/script_lint.py --cues` on the lines if the channel's pipeline is used. Resolve the voice question from (a) with David before final render; do not silently mix voices. Say plainly the audio was measured, not heard.
6. Music: use the channel's real library, read-only: `python3 /home/user/videos-ai/audio/pick_real_track.py 28 out/music.wav --mood <mood>` (energetic, not synthesised; never `build_music.py`), then `audio/check_music_bed.py`. If that path is unavailable, stop and report; do not fall back to synthesis silently.
7. Mix: `mix.py` = voice (compressed) + music ducked ~ -6 to -18 dB under voice + foley from `window.EV` via `core/audio/sfx.py`; output `out/mix.wav` mono/stereo 48 kHz, exactly 28.000 s.
8. Review stills (no video yet): `node core/render/still.mjs lemo-memory 1.2 --size 1080x1920 --range 0:28:1` then `python core/render/sheet.py` contact sheet; at least two passes; strips at 0.2 s around 8.4-12.6 (the twist) and every scene boundary. `node core/render/readcheck.mjs lemo-memory --size 1080x1920` (text stays long enough; confirm the quote >= 3 s).
9. Render: `node core/render/events.mjs lemo-memory` then `node core/render/video.mjs lemo-memory --size 1080x1920 --fps 24 --workers 3 --out lemo-memory/out/video.mp4`. 1080x1920 needs no hack: the page lays out from `innerWidth/innerHeight` and every page tool takes `--size`.
10. Mux: `sh core/render/mux.sh out/video.mp4 out/mix.wav out/memory.mp4 24` (two-pass loudnorm -14 LUFS; no grain on light). For the channel pipeline instead: `FRAMES=1 ./export/render.sh ...` is the channel's own path and then `check.sh`; use only if David wants it in his pipeline.
11. Verify the final file: ffprobe (1080x1920, 24 fps, 48 kHz, 28.0 s); `ffmpeg -af ebur128` (-14 LUFS, TP <= -1); `blackdetect`; `freezedetect=n=-50dB:d=2.0` (must find no still run >= 2.0 s; also compute per-second frame difference to confirm change every <= 2.5 s); first frame not blank; whisper on the final mix vs script; bbox script on `window.TEXTS` against x 65-1015, y 269-1248 and text-text overlaps; compare the typed quote against the Help Center page the same day; watch twice with sound off, twice on.
12. Report: what was verified by measurement, what by eye, what is untested, and the open items (live label check for Settings path, voice mismatch, tomorrow's promise).

---

## (h) Strict self-score

| Criterion | /100 | Why |
|---|---|---|
| Muted clarity | 88 | Frame 0 carries question + logo + typing + answer. Every shot has 3-6 words plus an icon/object. Loses: S4 quote is only partly readable; S6 "two ways out" relies on icons. |
| Aliveness (no still > 2.5 s) | 89 | Ambient layer always on, overlapping enters, note card travels. Loses: S4 quote hold and S8 locked scene (drift + pulse only); not yet measured. |
| 8-year-old clarity | 86 | One object (the note) explains the whole idea; words "memory", "temporary" are concrete. Loses: "Personalization", the legal-sounding quote, "twist". |
| Hook per shot | 87 | Each shot has a named new beat (self-writing notes, list about you, chat vanishes/note stays, readable list, two exits, direct question, tomorrow). S7 and S8 are prompts, not reveals. |
| Brand / real-logo fidelity | 82 | Real ChatGPT mark and real quote; no other product named. Loses: lime is not OpenAI green, all UI re-created, official images found but unusable here (licence unread), 8 shots carry re-created tags (clutter). |
| Smoothness (not robotic) | 82 | Continuous curves by rule, one cursor path. Loses: the style leans stepped and my override is only on paper; typed text and toggle need frame review. |
| Producibility with this library | 74 | Better than 62: one component family, phased build, no mascot, no third-party logo. Still custom: whole UI kit, no demo source, voice mismatch decision, live label check. 2 build rounds realistic. |

Overall (simple mean): **84 / 100**.

### 3 weakest points
1. **Producibility (74) and the voice question**: all UI above `core/` is new code, and the locked line 8 is in the channel's cloned voice while the brief asks for Kokoro; a two-voice film is a quality failure. Needs David's call before the final render.
2. **Quote reading time in S4**: 3.4 s on screen for a ~95-character quote; viewers will read the lit phrase, not the sentence. Mitigation is already in (shortened, lit in step with speech, twist and proof in the same moment), but retention at 9-12 s must be measured after posting.
3. **Re-created UI everywhere and unverified labels**: the Settings path labels and the generic note texts are ours; official OpenAI images exist and are fetchable but their licence could not be read (pages 403), and the one with a child's name is stale 2024 UI. Fidelity rests on the labels, so they must be live-checked on build day.
