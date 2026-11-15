Publish mode: TRIAL (David, 15.11.2026: 'probably a trial too, we will see'; confirm before posting)

# Episode 99: AI RACE #2, the maze (script, written 15.11.2026)

Status: script only. No TTS, no build, no render, no commit. Plan, beat list, facts table and decisions: `channel/episode-99-plan.md`. Facts: `channel/episode-99-results.md` and `video/ep99/arena/maze-race.json` (sha256 cd723db0...). Nothing in this script changes or softens the result.

## Hook
Pick: **"Lost in a maze, five AIs, no map."** (H1; surprise "Lost" is word 1; statement, not a question). Backup H2 "Five AIs, one maze, two stay stuck." Full table in the plan, section 3.

## Spoken script (10 lines, about 32 s; present tense; same text as `video/ep99/voice/lines.txt`)
Race steps are from `maze-race.json`; video times are estimates until the voice exists. The race clock is compressed and fitted to the voice; each line must land on or just after its event, never before it.

| # | Video s (est.) | Line | Real event it sits on |
|---|---|---|---|
| 1 | 0.0-2.0 | Lost in a maze, five AIs, no map. | step 0: all five in the centre, 89 steps from the exit |
| 2 | 2.1-4.6 | I ask each AI to guide one dot out. | setup scene: the request goes to five logo chips, each answers, each dot lights up |
| 3 | 4.7-6.9 | None of them can see the maze. Go! | race starts on "Go" (scaffold rule: the last word of line 3) |
| 4 | 7.5-9.3 | Perplexity is stuck at the start! | steps 3-20: Perplexity paces among 4 cells next to the start (all 500 steps) |
| 5 | 9.8-12.6 | ChatGPT goes the wrong way. Claude leads! | steps 29-61: ChatGPT from 77 to 102 steps away (further than the start); Claude closest to the exit for most of steps 29-59 |
| - | 12.6-15.5 | (no voice: race only) | steps 50-117: Gemini and Meta AI (one doubled dot) take the lead; dead ends marked |
| 6 | 15.5-17.6 | Two dots are out, on the same step! | step 117: Gemini and Meta AI leave together. Names are not spoken here |
| 7 | 17.9-22.0 | Claude turns back ten steps short, then makes it. ChatGPT walks in circles. | step 117: Claude 10 away, back to 23 by step 130, out at 171; ChatGPT paces two cells from step 152 to 500 (tail runs fast, counter visible) |
| 8 | 22.4-25.4 | Gemini and Meta AI tie. Same path, every step. | paths identical cell by cell (checked 15.11); both trails redraw as one line; the result card lands |
| 9 | 25.6-27.1 | The setup's in the link in bio. | LOCKED clip, `audio/voice/profile/canonical-lines.json`, byte for byte |
| 10 | 27.3-31.6 | Tomorrow, a free tool says it fixes Claude Code. Follow, so you see if it works. | **PLACEHOLDER TO CONFIRM** (ep100, the Graphify fact-check). True only if ep100 publishes the next day; else re-voice with "Next," and no day |

Builder notes: `build99.py` expects line NL-2 = result, NL-1 = send line, NL = tomorrow. Here NL-2 (line 8) is the result/reveal, NL-1 (line 9) is the locked setup line (no separate send line, cut for length), NL (line 10) is tomorrow. Lines 4-7 are race lines. The status row shows real "steps to the exit" numbers; the board text must come from the real file, not from today's placeholder `cues99.json`.

Honesty notes per line:
- 2: "guide one dot out" = each AI writes the moves once; nobody touches the dots after that.
- 3: "cannot see the maze" is the prompt's own rule ("You never see the maze, only the four sides of the dot"). Do NOT say "cannot see the walls": they see the four sides next to the dot.
- 4: Perplexity does move (3 cells), so "stuck at the start", never "does not move".
- 5: Claude does not lead the whole stretch (Gemini/Meta AI draw level at times, e.g. step 45); voice line 5 on steps 29-44, where Claude is clearly ahead.
- 6: only "two dots"; never "two AIs copy each other".
- 7: Claude DOES get out ("then makes it"): never let the turn-back read as a loss.
- 8: "tie" = same step count (117) and same path. Why they match is not known and is not said.

## Word checks
`python3 audio/script_lint.py --file video/ep99/voice/lines.txt` = "0 risky word(s) across 10 line(s)" (15.11.2026). Avoided on purpose: three, trust, track, trapped, true (TR/THR clusters), never, later, exit (spoken), gets out (flapped T; "are out" and "guide one dot out" instead), code, move(), function, steps-per-second jargon. Brand names stay: listen for "Meta AI" as ONE name (gap under about 0.12 s between "Meta" and "AI", 15.11 rule; re-roll until it is), "ChatGPT" as one word, "Claude Code" as one name; Whisper may write "Claude" as "clawed" (accepted before). Build with `--gap 0.06 --long 0.15 --max-speedup 1.45`; the hook should take about 2.0 s. Then `voice_doctor.py`, accent check, `voice_quality.py`; his ear decides on "short", "turns", "circles" (R plus consonant).

## On-screen text (at most 3 lines at once; no code; no word in a filled box)
| Video s | Headline (draft) |
|---|---|
| 0.0 | LOST IN A MAZE. / FIVE AIs. NO MAP. |
| 2.1 | SAME REQUEST FOR EACH AI |
| 4.7 | THEY CAN'T SEE THE MAZE + chip "pick one before it starts" |
| 7.5 | PERPLEXITY: STUCK |
| 9.8 | CHATGPT: WRONG WAY |
| 12.6 | (none: the race and the status row carry it) |
| 15.5 | TWO OUT. SAME STEP. |
| 17.9 | CLAUDE: 10 STEPS SHORT... / then "OUT IN 171" |
| 22.4 | SAME PATH. EVERY STEP. |
| 25.6 | result card + footer "the request: link in bio" |

## Blind-reader test (run BEFORE voicing on a frame-0 mock, again on the rendered frame 0)
1. Two fresh agents, no script, no file names. Tell each only: "This is the first frame of an Instagram Reel, 1080x1920. The bottom 35% is covered by Instagram's buttons and caption, so it is empty on purpose."
2. Give each: the frame-0 PNG and "Spoken in the first second: 'Lost in a maze, five AIs, no map.'"
3. Ask, in this order, and record word for word:
   a. "What is this video about? One sentence."
   b. "What did the AIs do here? Who moves the dots?"
   c. "Would you stop scrolling? Why or why not?"
   d. "Name the apps you see."
4. Pass = both name AI apps (at least three of five logos) AND the topic (AIs trying to get out of a maze / a race). (b) and (c) are findings, not vetoes.
5. A third fresh agent gets only the line list above (no picture) and answers: "Read the lines in order. At which line would you scroll away, and why? Which line made you want to see the end?" (15.11 build-up rule).
6. A fourth fresh agent ranks hooks H1-H6 (plan, section 3) for clarity and would-stop, one line each.

Blind readers, ep99: NOT RUN YET.

## Scores (labels, not gates)
HOOK 76 · VIRALITY 72 · OVERALL 72 · predicted views 300-1,200, most likely about 550. Reasoning in the plan, section 7. Log 48 h / 72 h in `channel/score-calibration.md`.

## BUILD-UP beat list, as built (pic-v1, 15.11.2026; video times from `video/ep99/cues99.json`, D 30.1 s; every race headline is asserted against `maze-race.json` in `build99.py`)
| Video s | Line | Real step | What is NEW here |
|---|---|---|---|
| 0.0 | 1 | 0 | frame 0: the maze, five logo dots in the centre, EXIT, "LOST IN A MAZE. / FIVE AIs. NO MAP." (3 text items) |
| 2.35 | 2 | 0 | the request goes to the five chips, each thinks, each answers, its dot lights up |
| 4.5 | 3 | 0 | the walls fade (they cannot see the maze); "pick one before it starts"; Go at 5.98 |
| 6.6 | 4 | 3-27 | Perplexity only paces 2 cells from step 5 (first casualty, the reason to stay at about 8 s) |
| 9.0 | 5 | 29-44 | ChatGPT's way out grows (76 to 82, 102 at step 61); "Claude leads" is said on steps 39-43, where Claude is the only front dot |
| 11.5-14.7 | none | 44-117 | race only: at step 61 Gemini and Meta AI (one doubled dot) take the front; dead-end marks; the numbers under the chips fall; the clock slows for the last 12 steps |
| 14.7 | 6 | 117 | two dots leave on the same step (the twist, at about half; names not said) |
| 16.75 | 7 | 118-500 | Claude 10 steps short, back to 22, out at step 171 on "makes it"; ChatGPT circles while the counter runs to 500 |
| 20.8 | 8 | replay | the tie is named late: both winning trails are drawn again and close into one line |
| 23.9 | 9 | board | rows land worst first, the tie last |
| 25.9 | 10 | board | tomorrow line: UNCONFIRMED, red banner on screen |
Longest stretch without a visual change, measured on the mixed file: 3.43 s (qa.py limit 4 s; the 2.5 s target is not met there: check where before v2). Headline holds over 2.5 s: "CLAUDE: 10 STEPS SHORT" (the stage moves under it) and "SAME PATH. EVERY STEP." (the trails redraw under it).

## Hook decision 15.11.2026 (David chose option 1): "Meta AI and Gemini just killed Claude."
Voice lines now: 1 "Meta AI and Gemini just killed Claude." 2 "I put five AIs in a maze race." 3 "None of them can see the maze. Go!" (line 3 take unchanged), 4-9 as before, 10 "Want the next one? Follow, and you'll see it." Truth check: Gemini and Meta AI both beat Claude (117 vs 171 steps); "killed" is David's slang for "beat by a lot". Visual direction from David: the picture should look like Claude really gets beaten (cartoon game K.O. style, not violence), and the hook is only the setup: the HOW (Claude leads early at steps 29-44, turns back 10 steps short at step 117, the other two walk the identical path) is what holds the viewer; the tie reveal stays late.
TOPIC verdict (rule 15.11): a known brand (Claude) beaten by two rivals in a game anyone understands; proof = real code run on a frozen maze, replayable on /e/99. Honest weakness: a contest between AIs is a medium topic by our own data (no number yet for the format; ep98 not published), and a viewer who does not use these AIs has no personal stake. David asked whether to continue with the maze or move another topic forward: answer pending.
