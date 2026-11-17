Publish mode: ASK DAVID (TRIAL or REGULAR; default REGULAR if he does not say)
Published as episode 101 (internal name 102)

# Episode 102 script: FREE TWINS #1, six free alternatives to apps you pay for (built 16.11.2026)

Status: BUILT, not published, not merged. Plan and verification table: `channel/episode-102-plan.md`. Build: `video/ep102/` (build102.py, mix102.py, voice/, hf/). Funnel: TOP. Format: numbered series candidate "Free twins #1". Experiment: a list format, new for us (log in `channel/experiments.md` when it is published).

## TOPIC verdict (first, per the topic rule)
Why a stranger cares today: money that leaves their account every month for apps they know by name (Loom, Notion, Calendly, ElevenLabs), and a free twin for each. Proof: public pricing pages and public GitHub pages, all read on 16.11.2026. Weak side: only part of it is an AI story (VoiceStudio, OpenWhispr, AppFlowy's AI), many viewers cannot host a server, and none of our three canon winners is a list. Compared with the queue (`channel/queued-ideas.md`): the only queued idea with outside proof of engagement (reference reel: 1,414 likes, 609 comments, views not shown) and a saveable payoff. It is an experiment of a new format, not an extension of a proven one.

## Scores (judgement labels, not measurements; our scores have not predicted views so far)
HOOK 72, VIRALITY 70, OVERALL 70, PREDICTED VIEWS about 500 (range 250-1,200). Log real 48 h / 72 h views in `channel/score-calibration.md`.

## Spoken lines (`video/ep102/voice/lines.txt`, 16 lines)
1. Loom, Notion and Calendly have free twins!
2. Six apps, seventy-five bucks a month. Watch it hit zero!
3. The last one is insane. Stay for it.   (the tease, David 16.11.2026)
4. Loom makes screen videos. Cap does it free.
5. Notion? AppFlowy. Notes, docs, even AI.
6. Calendly? Cal D I Y, for personal use only.
7. Intercom bills per seat, and per AI reply.
8. Chatwoot is free if you host it.
9. Wispr Flow? OpenWhispr. You talk, it types.
10. And the big one, ElevenLabs.
11. VoiceStudio clones your own voice, on your own machine.
12. It's new, just seven months old.
13. We did not test these, so check each one yourself.
14. Save the list. Send it to a friend who pays for Loom.
15. The setup's in the link in bio. (locked canonical clip)
16. Want the next one? Follow, and you'll see it.

Hook wording: the plan's "Loom, Notion, Calendly. Free twins exist." came out of the voice at 3.0-3.3 s with 0.4-0.5 s pauses between the names (two seeds), against the hook-gap rule (about 2 s, flowing). Reworded to one sentence with the same names and the same claim; the chosen take is 2.48 s. David can ask for the original wording back.

## The tease line and the reference mechanic (David's instruction, 16.11.2026)
- Reference DfSvS-CTqDA, checked again on 16.11.2026 from the saved download (audio transcribed with Whisper, frames looked at): it has NO spoken "stay till the end" line. Its retention mechanic is structural: (1) the count is promised in the first sentence ("nine GitHub repos that can replace..."); (2) every item is announced with its number ("First is... Second is... And ninth is..."); (3) a counter "N/9" sits top-left on every frame next to a strip of nine mini logos that fill in one by one; (4) the paid logo breaks before each free one appears; (5) the links are held back for the end ("comment REPO").
- What we adopted (structure, not words or artwork): the count in line 2 ("Six apps"), a counter "N/6" plus a strip of six logos that get a check one by one, a running total that falls from $75 to $0 (our own addition), the paid row struck out before each twin, and the saveable list held for the end.
- Our tease, line 3: "The last one is insane. Stay for it." (8 words, present tense, opinion wording, no number). Picture: on the receipt, rows 1-5 dim, a red marker ring is drawn around the sixth row (ElevenLabs) and "STAY FOR #6" appears. It is true to the build: the last pair (ElevenLabs to VoiceStudio) is the payoff beat: "THE BIG ONE", the largest star count (111K+), and the moment the total reaches $0. "Insane" is our opinion, and line 12 says the project is only seven months old.

Wording rules kept: "free twin" / "free alternative", never "replaces"; Cal.diy "personal use only" is spoken and stamped; VoiceStudio "seven months old" is spoken and stamped; "We did not test these" is spoken and on the end card; no promised next episode. Hook type: named products + surprise statement (not a question).
`python3 audio/script_lint.py --file video/ep102/voice/lines.txt`: 3 notes left on purpose: "Calendly" twice (a brand name, shown on screen with its logo) and "month" (the lint's own suggestion is "a month", which is what the line says). Swapped after the first lint run: dollars to bucks, records to makes, answer to reply, computer to machine, first to yourself, whoever to a friend who.

## Numbers on screen (all read 16.11.2026; full list with sources is written by the build into `video/ep102/cues102.json`)
- Prices (cheapest paid plan on each official pricing page): Loom $18, Notion $10, Calendly $10 (yearly billing), Intercom $19 per seat (yearly new-customer rate; $29 otherwise) + $0.99 per AI answer, Wispr Flow $12 (yearly billing; $15 monthly), ElevenLabs $6. Sum $75, tagged "from: cheapest paid plan, per person, Nov 2026".
- Stars, rounded DOWN: Cap 25K+ (25,113), AppFlowy 78K+ (78,984), Cal.diy 50K+ (50,090), Chatwoot 39K+ (39,919), OpenWhispr 11K+ (11,623), VoiceStudio 111K+ (111,733). Method: the GitHub repo pages through Exa's page fetch (github.com and api.github.com answer 403 from this container). AppFlowy, Chatwoot and OpenWhispr returned exactly the same count as in the plan's earlier read the same day, so those three may be a cached snapshot; rounding down covers it. UNCONFIRMED: last commit dates; VoiceStudio's star history (111K in 7 months is unusual).

## BUILD-UP beat list (what is NEW per beat; times are in `cues102.json` under `buildup`)
Open question after the hook: does the total really reach zero, and what is "the big one"?
| Beat | Line | Picture | What is new |
|---|---|---|---|
| 1 | 1 | Receipt: Loom, Notion, Calendly logos, "$75 A MONTH", FREE TWINS stamp | the stake: money + named apps |
| 2 | 2 | The receipt lists six apps with prices, total $75 flashes red | the promise: it goes to zero |
| 3 | 3 | Rows 1-5 dim, a red ring around row six, "STAY FOR #6" | the tease: a reason to stay to the end |
| 4 | 4 | Counter 1/6: Loom $18 struck out, Cap card, real screenshot, total 75 to 57 | first proof |
| 5 | 5 | 2/6: Notion to AppFlowy, real screenshot, total 47 | AI enters |
| 6 | 6 | 3/6: Calendly to Cal.diy, PERSONAL USE ONLY stamp, total 37 | a limit, said out loud |
| 7 | 7 | 4/6: Intercom: "$19 PER SEAT", "+$0.99 PER AI ANSWER" | reversal: you pay per answer |
| 8 | 8 | Chatwoot card, real screenshot, FREE IF YOU HOST IT, total 18 | the condition |
| 9 | 9 | 5/6: Wispr Flow to OpenWhispr, a voice wave turns into typed words, total 6 | a felt demo (illustration, tagged) |
| 10 | 10 | 6/6: THE BIG ONE + the ElevenLabs logo | the teased item arrives |
| 11 | 11 | VoiceStudio card, real screenshot, total hits $0 (green) | the payoff |
| 12 | 12 | NEW: 7 MONTHS OLD stamp | a caution on the biggest claim |
| 13 | 13 | New scene: the saveable card, six rows; "NOT TESTED BY US" | the honest limit + the thing to save |
| 14 | 14 | The rows nudge one by one | save + a named person to send it to |
| 15-16 | 15, 16 | SETUP: LINK IN BIO, then the FOLLOW card | CTA |
Check: (1) the total visibly gets closer to zero on every pair; (2) each pair adds a new kind of fact (screenshot, AI, a limit, a hidden fee, a demo, the biggest name); (3) reasons to stay at about 8-10 s (AI + the falling total) and at two thirds (hidden fee, then the big one); (4) no beat only repeats the picture; (5) the reveal ($0, the sixth app) is teased in line 3 and held until lines 10-11; (6) weakest beat by my own reading: beat 5 (Cal.diy: a caveat, least exciting).

## Blind-reader test, frame 0: NOT COMPLETED (16.11.2026)
- A fresh Sonnet session was started for it ("ep102 blind reader (frame 0)", session_01TRp47UPikjd3HHuddMsZNd) with only the frame-0 picture and the first spoken second. It did NOT answer the two questions: it treated the automatic start message as possibly not coming from David, stopped, and asked him whether to go on. It also read CLAUDE.md on start, so it is no longer a blind reader. No answer exists to log.
- Still to do before publishing: show `video/ep102/out/frame0.jpg` and the first line to a reader who has not seen the script and ask "what is this video about?" and "would you stop scrolling, and why?". My own reading (NOT a blind test): the frame names three known apps by logo, a monthly price and "FREE TWINS"; the weak point is whether "twins" reads as "free alternatives" without the voice.

## Build result (16.11.2026)
- Final: `video/ep102/out/ep102-final.mp4` (1080x1920, 41.27 s, 12.9 MB) and the review copy `video/ep102/out/ep102-final-review.mp4` (720 px, crf 27, 2.4 MB). Frame 0: `video/ep102/out/frame0.jpg`. Re-run everything except TTS with `video/ep102/run.sh <tag>`.
- Gate (`video/ep102/out/gate-v2.txt`, `export/check_hf.sh`): frame layout PASS, rendered file PASS (-14.2 LUFS, peak -1.1 dBFS, no frozen run over 4 s), voice + music quality PASS (pitch ranges 4.1-9.9 st, bed -9.9 dB under the voice in 300-3500 Hz), voice doctor PASS, accent PASS (every line under 0.08 not-american). The gate ran on the render before the final re-encode (crf 24, audio copied); `export/qa.py` was run again on the final file and passed.
- Voice takes: line 1 seed 74 (exaggeration 0.70), line 3 seed 94 (0.72), line 8 seed 63 (TTS input spelled "Chat woot"), line 9 seed 81 (0.66); the rest first passing seed at 0.70-0.80. Pauses inside lines are capped by cutting silence only (`voice/stitch.py`). Whisper per line: all words right except the brand spellings it cannot know ("Calingly", "app flowy", "Chat Woo", "Whisper flow", "11 Labs"). Listen for: "Calendly" in lines 1 and 6, "Chatwoot" in line 8, "Cal D I Y" in line 6.
- Music: `channel/music-notes.md` (punchy hip-hop beat, ep89's bed).
- Length: 41.3 s with the tease line (limit given: about 42 s). Flat stretches over 2.5 s by the build's own log: the hook (0-2.7 s, one frame that breathes) and the end card (31.9-36.6 s).
- NOT done / not verified: the audio was measured, not heard; the video was looked at as still frames, not watched twice at speed; the blind-reader test did not complete (see above); safe area was checked by the tool at x 65-1015 and by eye against x 108-972 (no `--wide` option yet); star counts for AppFlowy, Chatwoot and OpenWhispr may be a cached read; VoiceStudio's star history and all last-commit dates are unconfirmed; logo/brand usage terms were not read; `studio/lib/articles.ts` has no entry yet (text ready in `channel/episode-102-setup.md`); Publish mode is still to be asked.

---

# v3 REBUILD (16.11.2026, after David watched v2). This section replaces the lines, beat list and scores above. v2 is kept for comparison (`video/ep102/out/ep102-v2.mp4`).

What David asked and what was done:
1. The "free twins" hook is gone. The video starts with the subject itself: "Six apps you pay for have free alternatives!" (2.2 s). Frame 0 = that sentence (small lead-in + "FREE ALTERNATIVES", 2 text items) and the six paid apps' real logos, filling the safe box down to y 1215. Calendly: the mark we used IS the official one (same as the logo in calendly.com's own header); it now carries the official Calendly wordmark under it so it cannot be read as a generic icon (`video/ep102/hf/assets/logos/SOURCES.md`).
2. Items 1-5 are fast (9.6 s for five, about 1.4-2.5 s each); #6 gets the stage: a words-only "And the BIG ONE.", the same card for ElevenLabs to VoiceStudio, then the real VoiceStudio screenshot full stage, then "7 MONTHS OLD" (8.6 s in all). The tease and the two closing lines are kept. Length 32.4 s.
3. The paid-to-free change is one fixed beat, same place and same motion for all six: paid logo + name; the name is struck through and greyed; an arrow; the free logo + name appear under it; 0.3 s later the word FREE lands on the free row (never on the paid name). Checked on frames of every item.
4. Style: rebuilt on the episode 89 recipe and `channel/miki-style-checklist-2026-11-16.md` (written first, from frames of reel 89, 98, 99, 100 and 102 v2). One idea per screen: words-only screens (lead-in + heavy capitals built as spoken, one terracotta word with one ring) alternate with ONE dark card that holds real logos or the real screenshot. Removed: the receipt, the running total, the N/6 counter, logo chips, stamps, star counts, prices, source lines, illustrations, offset shadows, bouncing. Build: `video/ep102/build102v3.py`, run with `video/ep102/run3.sh v3`.

## Spoken lines v3 (`video/ep102/voice/lines.txt`, 13 lines; v2 lines kept in `voice/lines-v2.txt`)
1. Six apps you pay for have free alternatives!   (new)
2. The last one is insane. Stay for it.   (kept take)
3. Loom? Try Cap. Notion? AppFlowy.   (new; spliced, see below)
4. Calendly? Cal D I Y, for personal use.   (new)
5. Intercom? Chatwoot, if you host it.   (new)
6. Wispr Flow? OpenWhispr.   (new)
7. And the big one, ElevenLabs.   (kept)
8. VoiceStudio clones your own voice, on your own machine.   (kept)
9. It's new, just seven months old.   (kept)
10. We did not test these, so check each one yourself.   (kept)
11. Save the list. Send it to a friend who pays for Loom.   (kept)
12. The setup's in the link in bio.   (locked clip)
13. Want the next one? Follow, and you'll see it.   (kept)
script_lint: 1 note ("Calendly", a brand name shown with its logo). Dropped from the video (still in the caption and setup text): the $75 a month sum and the per-answer fee of Intercom.

## Beat list v3 (times from `video/ep102/out/build-v3.log`)
| t (s) | Line | Screen (one idea each) | What is new |
|---|---|---|---|
| 0.0 | 1 | Words + six real paid logos | the subject: six apps you pay for have free alternatives |
| 2.5 | 2 | Words only: "The last one is INSANE. STAY FOR IT." | a reason to stay to the end |
| 4.6 | 3 | Card: Loom, struck, arrow, Cap, FREE | pair 1 |
| 6.2 | 3 | Card: Notion to AppFlowy, FREE | pair 2 |
| 7.9 | 4 | Card: Calendly to Cal.diy, FREE, "personal use only" | pair 3 + its limit |
| 10.6 | 5 | Card: Intercom to Chatwoot, FREE, "if you host it yourself" | pair 4 + its condition |
| 13.0 | 6 | Card: Wispr Flow to OpenWhispr, FREE | pair 5 |
| 14.4 | 7 | Words only: "And the BIG ONE." then the card with ElevenLabs | the teased item arrives |
| 16.5 | 8 | Card: ElevenLabs to VoiceStudio, FREE | the payoff pair |
| 17.5 | 8 | The real VoiceStudio screenshot, full stage: "clones your own voice, ON YOUR OWN MACHINE." | what it does, shown on the real app |
| 19.6 | 9 | Words only: "It's new, just 7 MONTHS OLD." | a caution |
| 21.5 | 10 | Words only: "We did NOT TEST THESE. so check each one yourself." | the honest limit |
| 23.9 | 11 | One card: the list of six pairs | the thing to save + who to send it to |
| 26.5 | 12, 13 | Words only: "LINK IN BIO." then "FOLLOW." | CTA |
Build-up check: one open question (what is the last one?) from 2.5 s to 14.4 s; every beat is a new pair or a new fact; the five fast pairs are the build, #6 is staged over four screens; nothing repeats the picture. Flat stretches over 2.5 s by the build log: the list card (23.9-26.5 s) and the FOLLOW screen at the end.

## Scores v3 (judgement labels, not measurements; our scores have not predicted views)
HOOK 70, VIRALITY 70, OVERALL 72, PREDICTED VIEWS about 500 (range 250-1,200). Clearer subject and calmer look than v2; the money stake ($75) is no longer in the hook, which may cost pull.

## Blind-reader test v3: NOT RUN by this agent
The instruction was to use a fresh Sonnet agent through the Agent tool on frame 0 only. This build agent has no Agent tool (and was told not to use create_session), so the test is still open: `video/ep102/out/frame0-v3.jpg` + the first spoken second "Six apps you pay for have free alternatives!", questions "what is this video about?" and "would you stop scrolling, and why?".

## Build result v3
- `video/ep102/out/ep102-v3.mp4` (1080x1920, 32.37 s, 8.3 MB), review copy `ep102-v3-review.mp4` (720 px, 1.4 MB), `frame0-v3.jpg`.
- Gate `out/gate-v3.txt`: 5 of 5 PASS (layout, rendered file -14.3 LUFS / peak -3.0 dBFS, voice + music with the same bed at -9.6 dB under the voice, voice doctor, accent: every line under 0.08). `qa.py` passed again on the re-encoded final file.
- Voice: new takes for lines 1, 4, 5, 6 (line 5 typed as "Chat woot" for the voice; line 6 seed 52 at exaggeration 0.62 after seed 31 swung 10.2 st). Line 3 is a splice (`voice/splice3.py`): "Loom? Try Cap." from a new take + "Notion? AppFlowy." from the v2 take, because six new takes kept blurring "AppFlowy". Whisper still writes "TriCap" and "at/app Flowey": listen to line 3 first.
- Not verified: audio measured, not heard; still frames looked at (0, middle, last and each transition), not watched twice at speed; the splice seam in line 3 was not heard; blind reader open; Publish mode open.

---

# v4 (16.11.2026, after David watched v3). This section replaces the v3 lines, beat list and scores. v3 is kept (`video/ep102/out/ep102-v3.mp4`).

What David asked and what was done:
1. Built with the GSAP and motion skills (read first: gsap-core, gsap-timeline, gsap-plugins, gsap-utils, gsap-performance, motion-animation-principles, motion-kinetic-typography, motion-remotion-notes; model `video/demo-skills/hf/index.html`). Each screen is a function returning a timeline with labels and position parameters; one house curve (CustomEase expoOut for enters, expoIn for exits, in-out for moves, a no-overshoot spring for landings); words rise out of a mask when spoken, the one accent word per screen is split into characters (SplitText masks, 30 ms stagger); rings and arrows are drawn with DrawSVG; staggers 70-90 ms; only transform, opacity and filter are animated. Still Miki: one idea per screen. Build: `video/ep102/build102v4.py`, run `video/ep102/run4.sh v4`.
2. The cube stays as frame 0 and is stronger: six real paid logos in a 2 x 3 grid, centred, filling the safe box (x 108-972, y 520-1240); 3 text items (headline "FREE ALTERNATIVES", "to six apps you pay for", the Calendly wordmark). From 0.2 s each logo's price tag flips to a tick, one by one (90 ms apart), so the first second moves. New hook, surprise in the first word: "Free alternatives to six apps you pay for!" (2.2 s).
3. Length 27.1 s (v3: 32.4 s). Cut: the "Save the list. Send it to a friend..." line (the list card now carries line 9 and the note "Not tested by us. Check each one."), "for personal use" and "if you host it" as spoken words (both stay on screen as notes on their cards and in the caption), shorter pair lines. Kept: the tease and both closing lines.
4. Voice: the Calendly line is no longer a splice. Lines 3 and 5 are single takes. Line 4 is two whole takes of two separate sentences set one after the other ("For Calendly, Cal D I Y." then "For Intercom, Chatwoot.", `voice/join4.py`): nine one-take attempts of the combined sentence either failed the accent check or lost a word. Whisper on the final narration: "For Calendly, CalDIY. For Intercom, Chat Woot." No repeated word.
5. Music: new track, `punchy--punchy-brass-groovy-pop-track--moonpub.mp3` (see `channel/music-notes.md`).

## Spoken lines v4 (`video/ep102/voice/lines.txt`, 11 lines; v3 lines in `voice/lines-v3.txt`)
1. Free alternatives to six apps you pay for!   (new)
2. The last one is insane. Stay for it.
3. For Loom, Cap. For Notion, AppFlowy.   (new)
4. For Calendly, Cal D I Y. For Intercom, Chatwoot.   (new)
5. For Wispr Flow, OpenWhispr.   (new)
6. And the big one, ElevenLabs.
7. VoiceStudio clones your own voice, on your own machine.
8. It's new, just seven months old.
9. We did not test these, so check each one yourself.
10. The setup's in the link in bio.
11. Want the next one? Follow, and you'll see it.
script_lint: 1 note ("Calendly", a brand name shown with its logo).

## Beat list v4 (times from `video/ep102/out/build-v4.log`)
| t (s) | Line | Screen (one idea each) | What is new |
|---|---|---|---|
| 0.0 | 1 | The cube: six real paid logos; price tags flip to ticks 0.2-0.9 s; "FREE ALTERNATIVES to six apps you pay for" | the subject and the surprise |
| 2.4 | 2 | Words only: "The last one is INSANE. STAY FOR IT." | a reason to stay |
| 4.6 | 3 | Card: Loom struck, arrow, Cap, FREE; then Notion to AppFlowy | pairs 1 and 2 |
| 7.3 | 4 | Card: Calendly to Cal.diy ("personal use only"); Intercom to Chatwoot ("if you host it yourself") | pairs 3 and 4, each with its limit |
| 11.2 | 5 | Card: Wispr Flow to OpenWhispr | pair 5 |
| 13.1 | 6 | Words only: "And the BIG ONE." then the card with ElevenLabs | the teased item arrives |
| 15.1 | 7 | Card: ElevenLabs to VoiceStudio, FREE; then the real VoiceStudio screenshot, "ON YOUR OWN MACHINE." | the payoff, on the real app |
| 18.0 | 8 | Words only: "It's new, just 7 MONTHS OLD." | a caution |
| 20.0 | 9 | One card: the list of six pairs + "Not tested by us. Check each one." | the thing to save + the honest limit |
| 22.4 | 10, 11 | Words only: "LINK IN BIO." then "FOLLOW." | CTA |
Build-up check: the open question (what is the last one?) runs from 2.4 s to 13.1 s; five pairs in 8.5 s, every one a new pair; #6 gets four screens (6.9 s); no beat repeats the picture. Flat stretches over 2.5 s by the build log: none.

## Scores v4 (judgement labels, not measurements)
HOOK 74, VIRALITY 71, OVERALL 73, PREDICTED VIEWS about 550 (range 250-1,300). Shorter, a moving first second, surprise word first; still a list format that is new for us.

## Blind-reader test v4: to be run by the parent session on `video/ep102/out/frame0-v4.jpg` (first spoken second: "Free alternatives to six apps...").

## Build result v4
- `video/ep102/out/ep102-v4.mp4` (1080x1920, 27.1 s, 5.8 MB), review copy `ep102-v4-review.mp4` (720 px, 1.2 MB), `frame0-v4.jpg`.
- Gate `out/gate-v4.txt`: 5 of 5 PASS (layout; rendered file -14.3 LUFS, peak -3.4 dBFS, no frozen run; voice + music, bed -9.5 dB under the voice in 300-3500 Hz; voice doctor; accent, every line 0.07 or lower). `qa.py` passed again on the re-encoded final.
- Looked at by eye: frames 0, 0.5, 1.0, the tease, every pair, the big one, the screenshot, the list card, the closing screens, the last frame.
- Not verified: audio measured, not heard (the join in line 4, "AppFlowy" which Whisper writes "App Flowey", the new music); motion judged from stills and code, not watched at speed; the spoken "personal use" caveat for Cal.diy is now on screen and in the caption only; Publish mode open.
