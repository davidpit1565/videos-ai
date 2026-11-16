Publish mode: ASK DAVID (TRIAL or REGULAR; default REGULAR if he does not say)

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
