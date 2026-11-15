# Episode 98 red team (15.11.2026, read-only analysis)

Scope: what could stop ep98 ("AI RACE #1") from spreading, compared with the only valid evidence set (episodes 86, 80, 82, `canon-top3.md`). Nothing was built, voiced, rendered, committed or published.
Sources read: `episode-98-ai-review-prompt.md`, `-plan.md`, `-script.md`, `-results.md`, `canon-top3.md`, `winners-structure-2026-11-09.md`, `episode-86/80/82-script.md`, `content-memory.md` (13.11 virality model, ep89 readings), `score-calibration.md` (recalibration 12.11), `algorithm-2027-notes.md`, `new-formats-2026-11-13.md`, `video/ep98/build98.py` and its log `video/ep98/out/build-v1.log`, and a 1-frame-per-second sheet of `video/ep98/out/pic-v1.mp4` (28.53 s, silent).
Labels: **FACT** = read from a file or seen in the frames. **JUDGEMENT** = my reading.

## Key timings of the current cut (FACT, `build-v1.log` + frame sheet)
| Video time | What happens |
|---|---|
| 0.0-1.9 | Headline "FIVE AIs RACE, ONE HITS THE WALL." over the small track, five small cars on the grid |
| 2.0-4.4 | "SAME JOB FOR EACH AI", note "Teach this car to race." |
| 5.0-5.9 | "HANDS OFF.", lights, tiny chip "PICK ONE, COMMENT IT" |
| 5.87 | Go (race clock starts) |
| 6-9 | Headline is only a product name (CHATGPT, GEMINI, META AI, PERPLEXITY): the roll call |
| **7.4** | The ranking tower puts Claude in slot 1 (rank change at race frame 91) and keeps it there to the end |
| 10.10 | Perplexity stops (first event of the video) |
| 12.03 | Meta AI touches the wall (the event the hook promises) |
| 15.0 | Headline "CLAUDE CROSSES AHEAD" (Claude crosses 15.30) |
| 13.96-16.60 | Slow-motion close-up card |
| 18.46-19.5 | "CLAUDE WINS / GEMINI: 2 TENTHS BEHIND" |
| 20-23 | Headline "SEND IT TO SOMEONE WHO USES META AI" + result card |
| 24-27 | "NEXT: A MAZE" + maze sketch |
| 28.5 | Back to frame 0 (loop) |

## 1. Side by side: ep98 vs the three winners

| | 86 (1,563 views) | 80 (817) | 82 (656) | 98 (current cut) |
|---|---|---|---|---|
| Hook (spoken) | "ChatGPT, don't tell my teacher!" (FACT) | "ChatGPT can cave when you push!" (FACT) | "Some say Claude got dumb on purpose!" (FACT) | "Five AIs race, one hits the wall." (FACT) |
| Hook shape | Brand word 1, personal secret, emotion (betrayal) | Brand word 1, a flaw you can test | Brand early, a rumour (conspiracy) | No brand, a count plus a threat; a contest result, no human emotion (JUDGEMENT) |
| Premise clear at frame 0 | Chat UI + ChatGPT logo; Miki still missed the subject (FACT) | Real caving footage (FACT) | Claude mark with a crack (FACT) | "AIs race" is clear; that **each AI wrote its car's driving** is not on frame 0, it comes at 2-4 s (FACT); a cold viewer may read it as an animation (JUDGEMENT) |
| Time to the first stake | 0 s, result stated 3.1-5.1 s ("It said yes. Then it told!") (FACT) | 0 s, the fold at about 8-18 s (FACT, approx.) | 0 s, answer in line 2 (FACT) | Stake said at 0 s, first event 10.1 s, promised wall 12.0 s (FACT) |
| Payoff position | Told at 3-5 s, twist (Claude) last | Fold in the middle, fix after | Answer line 2, three cards | Winner at 15.0 (headline), 18.5 (said) (FACT) |
| Beats / length | 7-9 lines, 27.5 s | 13 lines, 50.2 s | 9 lines, 28.2 s | 13 lines, 28.5 s (FACT) |
| Quotable words | The AI's own reply read big | "You're right. Buy the phone." | Anthropic's own sentence | None: no words come from the AIs on screen (FACT; code is kept off by rule) |
| Comment / send mechanic | None spoken; 0 shares (FACT) | Send line in caption; 1 share (FACT) | "Tell me below"; 1 share (FACT) | Tiny chip "pick one, comment it" at 5 s; spoken "Send it to a friend. See who they pick." but the screen says "SEND IT TO SOMEONE WHO USES META AI" (FACT: script and build disagree) |
| Loop | Back to frame 0 | No | No | Back to frame 0 (FACT) |
| Easy to miss | Claude refused before any secret | The fix text | The dates | Perplexity parks before anyone touches a wall; Gemini never leads (FACT, results) |
| Visual style | Drawn chat UI, light + lime | Real chat footage + drawn settings | Drawn cards, Claude orange | Miki-style paper, drawn track, real logos on small cars (FACT) |
| Who it happens to | The viewer's own homework secret (JUDGEMENT: personal) | The viewer's own ChatGPT agreeing too fast | The viewer's paid Claude | The viewer's AI "losing a race" (brand loyalty, not personal) (JUDGEMENT) |

What the three winners share and 98 does not (JUDGEMENT on FACT): one named brand in the first words, a human emotion (betrayal, flattery, conspiracy), and words from the AI the viewer can quote. 98 has rivalry and motion instead, which is what the outside contest format runs on (`new-formats-2026-11-13.md`: AI Code Clash 14M on one Short, @ouali.code 303,100), but that evidence is YouTube/TikTok, not our account and not Reels.

## 2. The 10 strongest reasons ep98 could fail (ranked)

| # | Reason | Evidence | Cheap to fix? |
|---|---|---|---|
| 1 | **The winner is spoiled 11 s before the reveal.** The tower shows Claude #1 from 7.4 s, the headline says "CLAUDE CROSSES AHEAD" at 15.0, then "CLAUDE WINS" at 18.5: the answer is given three times, so the curiosity gap (the hook's "which one?") closes early and the slow motion has nothing left to reveal. | build log rank changes (claude to slot 0 at race frame 91); frames 15 s and 19 s | Yes: about 45 min |
| 2 | **Nothing happens for 10 seconds.** Race starts 5.87 s, first event 10.1 s, the promised wall 12.0 s. Our own Insights: about half the viewers are gone by 4-5 s (ep80), and ep93 lost about 45% in 2 s. Most viewers leave before a car moves. The winners state their result by 3-5 s (86). | log; `winners-structure` (86 cues, 80 Insights); `score-calibration` 12.11 | Yes, needs one re-voice of lines 1-4 |
| 3 | **The premise is not on frame 0.** The 14.11 rule: frame 0 and the first spoken line must say that the AIs wrote what drives the cars. Frame 0 says only "FIVE AIs RACE". Blind readers were never run (script: "NOT RUN YET"). | frame 0; CLAUDE.md 14.11 clarity rule | Yes |
| 4 | **The drama is small on screen.** The cars are about 50 px on a 1080 frame, the road sits in the middle third; Meta AI's "wall" is a bump at speed 2.6 of 10 (script says "a bump, not a smash"), Perplexity just stops. The hook promises a crash the picture barely shows; on a phone it reads as five dots on a loop. | frame 0 and sheet; script fact table | Medium: camera zoom on the events, 45 min |
| 5 | **No human stake, no quotable words.** All three winners carry a feeling about the viewer's own AI; 98 is a sports result about steering instructions. Checklist item 1 was already "PARTIAL" in the plan. | canon-top3, plan section 2 | No, it is the concept; partly helped by "pick yours" |
| 6 | **"Rigged" risk.** A Claude-built channel shows Claude winning by 0.20 s, one try each, and Perplexity's answer shares Claude's constants (UNCONFIRMED). The disclosure is only in the caption, below "more". Comments may be about the bias, not the race; the honest version is fine, but the viewer never sees "rules locked first" on screen. | results.md notes; caption | Yes: one line on the result card |
| 7 | **3 s of dead roll call.** 6-9 s the headline is only a product name while the cars leave; the names are already on the cars. | frames 6-9 | Yes |
| 8 | **Untrue-until-confirmed ending.** "NEXT: A MAZE" on screen and "Tomorrow, they face a maze" spoken; ep99 has no arena and no answers. Also the five apps/models and date are UNCONFIRMED (no screenshots). This blocks shipping under the never-fabricate rule, not just reach. | script "PROMISE TO CONFIRM"; results.md | Yes: 5 min decision, re-voice one line |
| 9 | **The comment and send asks are weak and out of sync.** "Pick one, comment it" is a tiny chip for under 1 s and is never spoken before the race; the spoken send line and the on-screen one differ. Our account gets almost no comments (89: 0, 86: 0) and 45 of 50 reels have 0 shares. | frames 5 s, 20 s; algorithm notes | Yes |
| 10 | **A third of the video comes after the payoff, and the card has little save value.** 19.6-28.5 s is send line, link line, maze teaser. The result card is a result, not something to use; our only saves came from a usable prompt (89: 18 saves). | log; content-memory ep89 | Partly: trim to about 4 s; save value stays low |

## 3. Fixes that stay true

Real numbers stay as they are: Claude 8.48 s, Gemini 8.68 s, ChatGPT 10.58 s, Meta AI touches the wall at 6.15 s, Perplexity stuck from 4.22 s. Video time below = race time + 2.8 s (race starts at 2.8 s instead of 5.87).

### First 3 seconds
- **Picture, frame 0:** camera starts at about 1.6x on the start grid, so the five cars are about 140-160 px with their logos readable, filling the safe box width. Headline, 2 lines, heavy ink, y 285-420: "EACH AI TAUGHT A CAR. / ONE HITS THE WALL." Under it, handwritten with an arrow down at the cars: "pick yours". 3 lines total, no code, no box. The cars rock on the grid.
- **Spoken 0.0-2.2 s (option A, recommended):** "Each AI taught a car. One hits the wall." (premise + threat; 9 words, longer than the 6-word target, but the 14.11 clarity rule wins). Option B, 7 words: "Five AIs taught these cars. Pick one!" Run `script_lint` (the T in "taught a" may flap) and two blind readers on both before voicing.
- **2.2-2.8 s:** "Pick yours. Go!" with the lights filling quickly; the camera eases out to the full road as the cars leave.
- Cut "SAME JOB FOR EACH AI", the note, "Hands off" and the roll call; the identical request goes to the caption and `/e/98`. Saves about 3.1 s and gets the race moving before the 4-5 s drop.

### Reveal order (keep the suspense, honestly)
1. **No live positions until the finish.** The tower keeps the five logos in a fixed order (the order of the hook, never re-sorted) and shows only status: lap dots, "?" when stopped, "X" at the wall. No numbers 1-5 during the race. This hides nothing that happened; it only stops ranking early. Claude and Gemini are 0.03-0.06 lap apart all race and the cars are drawn side by side, so the road itself does not give the winner away.
2. Race events on the real clock: about 7.0 s "Perplexity just stops!"; about 9.0 s "Meta AI hits the wall!" (camera eases in to about 1.6x on the hairpin for both, never pausing the race); about 10.5 s "Three left. Who wins?"
3. Claude crosses at about 11.3 s, Gemini at 11.5 s. No headline names a leader. Freeze 0.3 s on the line with "?" over both logos.
4. **The reveal is the slow-motion replay** (labelled "REPLAY · 1/4 SPEED"): "Claude, by two tenths." lands as Claude's nose crosses. Not "photo finish": the measured gap is about 78 px, two car lengths (script honesty fix).
5. ChatGPT's finish (13.4 s) shows on the result card ("10.58 s"), not as its own beat.

### Where the seconds go
| Cut | Saved |
|---|---|
| Lines 2-4 (same job, hands off, roll call) folded into the hook | about 3.1 s |
| "ChatGPT takes its time" (to the card) | about 0.9 s |
| Maze teaser shortened to the spoken line only, or dropped | about 2-3 s |
Target: about 21-22 s instead of 28.5 s, with the race taking half of it.

### Comment and send mechanic
- "Pick yours" is spoken AND shown at frame 0, before the race; the viewer's pick is the reason to watch to the end.
- Caption line 1: "Which car did you pick? Did it make it?"
- Send line (spoken and on screen the same): "Send this to someone who uses Meta AI." Specific, playful, true (it touched the wall). Fix the current mismatch either way.

### Reason to watch twice
The ink line each car leaves stays on the road to the end: the second viewing is for your own pick, and for the detail most people miss (Perplexity parks in the bend before anyone touches a wall; Gemini never leads once). Last frame = frame 0 (already built).

### Saveable card
Result card: "AI RACE #1 · 2 LAPS", rows landing slowest first, Claude last, plus one small line "Rules locked before any AI answered. One try each." and footer "race your own AI: link in bio". Honest limit: it is a result, not a tool, so expect few saves; the real saveable thing (the request to paste) lives on `/e/98`.

### Ending
"The setup's in the link in bio." (locked clip). Final line only if ep99 is really ready the next day: "Tomorrow, they face a maze. Follow, so you see who gets lost." Otherwise: "Next race, a maze. Follow, so you see who gets lost." (no day promised), and the on-screen text matches.

## 4. Honest scores (judgements, not measurements; my scores have not predicted our views, Spearman -0.23)
| | Current cut | With the fixes above |
|---|---|---|
| HOOK | 68 (clear subject, a threat, but no brand and no premise at frame 0) | 76 |
| VIRALITY | 64 (rivalry and motion, but spoiled winner, 10 s with no event, weak send) | 72 |
| VALUE | 50 (a result, low save value; real value is on `/e/98`) | 55 |
| OVERALL | 63 | 71 |
| PREDICTED VIEWS | 250-800, most likely about 400 (scale score about 59) | 300-1,200, most likely about 550 (about 64) |
Reasoning: there is no class for this format on our account. Our explainer class sits at 240, the odd-chat class at 580 (`score-calibration.md`, 12.11). A race has more motion and brand rivalry than an explainer but no personal stake and no quotable reply, so I place it between the two; the outside contest format is proven only on YouTube/TikTok and with a low hit rate (ouali.code 2 of 12 posts above 80K).
**Can it reach 85+?** Not honestly with this race. 85+ would need a stake the result does not have: a famous brand clearly crashing at speed in the first 3 s (Meta AI's bump is slow), or a personal angle (your homework AI loses). The fixes lift it from "spoiled" to "fair", not to 100. David's "100 of 100" is not reachable by polish (CLAUDE.md: "a polished render cannot lift a weak concept"); the honest lever for the series is the next challenge picked for a bigger visible failure, not more work on this cut.

## 5. Changes, ranked
| # | Change | When | Effort | Tier |
|---|---|---|---|---|
| 1 | Confirm or drop the maze promise; get the five screenshots (app, model label, date) | Now, blocker | 5 min (David) | any |
| 2 | Hide live positions (fixed-order tower with status only), remove "CLAUDE CROSSES AHEAD", reveal on the slow-motion replay | Now | 45 min in `build98.py` | Sonnet 5 (decided, mechanical) |
| 3 | New frame 0 + lines 1-3 ("Each AI taught a car. One hits the wall." / "Pick yours. Go!"), cut lines 2-4 of the old script, race starts at about 2.8 s | Now | 30 min wording + blind readers, 60-90 min build, one TTS render | Opus for the wording and blind-reader judgement, Sonnet 5 for the build |
| 4 | Camera zoom so cars are about 150 px at frame 0 and 1.6x on the two hairpin events | Now | 45 min + safe_check | Sonnet 5 |
| 5 | Make the spoken and on-screen send lines identical ("Send this to someone who uses Meta AI.") | Now | 10 min | Sonnet 5 |
| 6 | "Rules locked before any AI answered. One try each." on the result card | Now | 10 min | Sonnet 5 |
| 7 | Trim the end to about 4 s; caption line 1 "Which car did you pick? Did it make it?" | Now | 15 min | Sonnet 5 |
| 8 | Two fresh blind readers on the new frame 0 + first spoken second, answers into the script file | Now, before voicing | 15 min | fresh agents (any tier) |
| 9 | Ask David which model Perplexity used (shared constants with Claude) | Later, before the caption is final | 2 min | any |
| 10 | Pick AI RACE #2's challenge for a bigger visible failure at speed (stake in the first 3 s) | Later | 30-60 min | Opus (concept call) |
| 11 | Log the 48 h / 72 h readings against the prediction above in `score-calibration.md` | After publishing | 10 min | Sonnet 5 |

## Outside AI review pasted by David, 15.11.2026 (one AI, unnamed; judgement)
Scores given: HOOK 35, VIRALITY 50, VALUE 70, OVERALL 48; views 150-800 as trial, 500-3,000 as normal reel (guess). Agrees with our red team on: ranking bar spoils the winner, slow start / roll call, too many asks at the end, filler seconds. ACCEPTED: hide ranking, start with cars moving, "pick before the race" prompt ("COMMENT YOUR PICK"), one ask only at the end, shorter (~18-22 s), "Five AI cars race. Two fail." as a hook candidate (true: Meta AI hit the wall, Perplexity got stuck), a named person to send it to ("the friend who always says ChatGPT wins"). REJECTED: cutting the SLOW MOTION label (it is the honesty marker for the slowed finish), "claims the label slows the video" is wrong; removing logos (David's standing real-logo rule; risk noted, his call); "do not post as trial then move after 3 days" (contradicts David's chosen trial-first plan; Instagram's own help center says a trial can be shared to everyone; his call, tracked in experiments.md); spoken "two tenths" (the voice blurs it; we say "right behind" and show 0.2 s on screen).

## Second outside advice, 15.11.2026 (David pasted; unnamed AI) and a hook panel
- Hook claim "Five AI cars race. Two fail." + cold open on the Meta AI crash: blind panel (ordinary viewer) rated clarity 6 / stop 6: "AI cars" sounds like real self-driving cars; "Each AI taught a car. One hits the wall." scored 7 / 7 and was the only one that says WHO made the cars drive. Panel's own idea: "Each AI taught a car. Watch one hit the wall." Decision: keep line 1 "Each AI taught a car. One hits the wall." and open the picture on a real flash of the Meta AI wall hit (true footage from the race) in the first second, then back to the start; test in v3.
- Claim "your regular reels reached 1,182 and 1,332 views": NOT in our files. Our top 3 regular reels: 1,563 / 817 / 656 views (1,180 is ep86's reach); 94-97% of their reach came from non-followers, so a followers-first push is not what carried them. Trials measured so far: ep91 about 130 IG views; ep97 posted 14.11 22:59 (reading due 17.11). n is too small to decide trial vs regular. David decides for ep98.

## Outside AI's answers to our 7 objections, 15.11.2026 (David pasted; checked)
- Logos: it WITHDREW the takedown/reduced-reach claim (confidence low/guess; nominative-use reasoning only). Real logos stay (standing rule). Its alternative (coloured car + name text) not needed.
- SLOW MOTION label: no data that it hurts. Keep honest but smaller/shorter (tiny label, about 1.5 s) in v3.
- Numbers 1,182 / 1,332: it says they came from "a snapshot of organic media content views" it saw on 12.11; withdrawn as unverifiable. David should compare with Instagram Insights (a different metric than our studio "views" could explain it). Until he does: not evidence.
- Trial vs regular: it admits the followers-push reason is a guess (low); description of trials as non-followers-only confirmed (high). It leans regular for ep98 as judgement (broad, not risky). Same as our lean. David decides.
- Hook: it concedes "Five AI cars race. Two fail." is ambiguous; offers "Five AIs teach cars. Two fail." Not tested; our line "Each AI taught a car. One hits the wall." stays (panel 7/7).
- Ending: it suggests one spoken ask ("Comment who you picked"). We keep the current: "Did you pick Claude? Send it to a friend." because Instagram's head said sends per reach correlate most with reach (channel/algorithm-2027-notes.md); caption carries the comment ask. Fixed structure lines (setup link, tomorrow line) stay per CLAUDE.md.
- Its new scores: HOOK 60 / VIRALITY 55 / VALUE 70 / OVERALL 55; views 200-2,000 as a guess. Consistent with ours (about 71 with fixes, judgement); nobody supports 85+.

## Correction 15.11.2026 03:48 (David's Instagram screenshot of the profile)
Real profile numbers (include Facebook views on regular reels, per David): regular reels: teacher essay 1,791; "this prompt viral" 1,362; black hole math 696; Me with Claude/ChatGPT 486; ask ChatGPT to draw you 399. Trial reels: ep97 pelican 246 (about 5 h old), 146, 380, 150. So the outside AI's "1,182 / 1,332" were close to real dashboard figures (1,362 / 1,791 are the real ones); my statement that they "are not in our files" only meant the studio snapshot of 9.11 (top 1,563). Regular looks higher than trial on this small sample (5 vs 4, regular includes Facebook, ages differ): consistent with David's choice of regular for ep98. Dashboard: 19.9K views in the last 30 days.
