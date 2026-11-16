Publish mode: REGULAR (David, 15.11.2026: 99 goes first)

# Episode 99 plan: AI RACE #2, the maze (written 15.11.2026, PLAN ONLY)

Status: plan and script only. No voice, no build, no render, no commit. Scores are judgements, not measurements.
Format: **AI RACE #N** (numbered format, slot = the challenge; #1 = the car race, episode 98). Funnel: TOP. Next step for a viewer: the request and the replay on `/e/99` (MID), once that page is live with the real race.

One sentence: five AIs (ChatGPT, Gemini, Claude, Meta AI, Perplexity) each write the moves for one dot that must get out of a maze it cannot see; the five real answers run at once in one maze; two never get out, Claude gets out late, and Gemini and Meta AI tie on the exact same path.

---

## 1. Duplicate check (done before anything was written)
- `grep -n -i -E "race|maze|arena|contest|versus| vs |labyrinth|perplexity|gemini" channel/topics-covered.txt`: 0 hits for race / maze / arena / contest / versus / labyrinth / Perplexity. "Gemini" hits lines 15, 61, 82 (Gemini privacy and formula topics) and 85 (secret test, ep86): none is a contest. Note: `topics-covered.txt` ends at ep90; ep98 (AI RACE #1, the car race) is not in it yet. Add 98 and 99 when they ship.
- `grep -n -i -E "maze|ai race" channel/content-memory.md`: 0 hits.
- Nearest in our own list: ep98 (same format, a different challenge: cars on a road vs a dot in a maze; a different result: there Claude wins, here Gemini and Meta AI tie and Claude is third). ep97 (four Claude models draw a pelican) is a different format. Not a repeat; it is episode #2 of a numbered format (the 10.11 rule: extending a format comes before inventing a topic). David's 13.11 "bored of chat tests" rule: this is not a chat test.

## 2. The facts this video rests on (all measured from `video/ep99/arena/maze-race.json`, sha256 cd723db0...; do not change or soften)
From `channel/episode-99-results.md` plus my own pass over `paths[]` (scratch script, distances = shortest way out from the dot's cell, computed from `maze.json`):

| Step | Event (measured) | Used in line |
|---|---|---|
| 0 | all five dots in the centre cell (10, 10), 89 steps from the exit (the best possible) | 1-3 |
| 3 | Perplexity reaches its closest ever (86 away), then paces among 4 cells next to the start for the remaining 497 steps | 4 |
| 8 | ChatGPT splits from the others | (picture) |
| 29-59 | Claude splits from Gemini/Meta AI at step 29 and is the closest dot to the exit for most of steps 29-59 (e.g. step 30: Claude 67, Gemini/Meta AI 69, ChatGPT 77) | 5 |
| 30-61 | ChatGPT walks AWAY from the exit: 77 steps away at step 30, 102 at step 61 (further than where it started) | 5 |
| 50-117 | Gemini and Meta AI lead (always together: identical cell every step) | (picture, status row) |
| 117 | Gemini and Meta AI leave the maze at the same step. At that moment Claude is 10 steps from the exit | 6 |
| 118-130 | Claude turns away: 10 away at step 117, 23 away at step 130 | 7 |
| 125 | ChatGPT's closest ever: 52 steps from the exit | (picture: ring on its closest cell) |
| 152-500 | ChatGPT paces between two cells, (15, 4) and (15, 3), until the 500-step limit (results file: "29 cells walked in circles for the other 375 steps" from step 125) | 7 |
| 171 | Claude gets out (3rd) | 7 |
| 500 | limit: ChatGPT and Perplexity still inside | board |

Dead ends entered: Gemini/Meta AI 3 (steps 57, 67, 92), Claude 8 (48, 63, 73, 86, 108, 130, 143, 149), ChatGPT 2. Cells visited: Gemini/Meta AI 110, Claude 140, ChatGPT 140, Perplexity 4.
Tie, checked: Gemini's and Meta AI's paths are identical cell by cell (re-checked 15.11 in my pass: `paths` equal, 118 cells each). Their answer files are different files (different sha256). Why they produce the same path was NOT analysed: never say they "copied" each other or "think alike".
Not claimed: a ranking of intelligence; which model each app ran (UNCONFIRMED, no screenshots); why ChatGPT circles or why Perplexity stalls.

**Scaffold warning for the builder:** `video/ep99/cues99.json` today holds PLACEHOLDER data (reference bots: "chatgpt wins in 183 steps"). Its events and headline drafts are NOT the real race. Re-run `build99.py` on `arena/maze-race.json` (it picks that file up by default now that it exists) and replace the drafted headlines.

## 3. Hook options (statement, not a question; surprise word in the first 3 words; all pass `script_lint`)
| # | Spoken hook | Type | Surprise in words 1-3 | Clear at frame 0? | Note |
|---|---|---|---|---|---|
| H1 | "Lost in a maze, five AIs, no map." | felt situation + subject | "Lost" (word 1) | yes with the picture (logos in the maze centre) | the viewer feels "lost, no map" before anything else; subject (five AIs, maze) inside the same breath |
| H2 | "Five AIs, one maze, two stay stuck." | result tease (stake) | no: "stuck" is word 7 | yes | strongest stake, but the surprise sits last (the ep88 mistake) |
| H3 | "Five AIs, lost in one maze, no map." | subject first | "lost" (word 3) | yes | safest for comprehension, a little flatter |
| H4 | "Your AI, lost in a maze, no map." | identity ("your") | "Your AI, lost" | partly: "my AI?" may confuse a cold viewer | personal stake (why-stuck rule 7), but risks the first-second test |
| H5 | "Stuck in a maze, five AIs, one way out." | felt situation + goal | "Stuck" (word 1) | yes | 9 words, a bit long for a 6-word target |
| H6 | "Blind in a maze, five AIs, one dot each." | felt situation | "Blind" (word 1) | partly: "one dot each" needs the picture | "blind" is vivid but may read as about blind people |

**Pick: H1, "Lost in a maze, five AIs, no map."** The surprise and the feeling ("lost") is word 1, the subject (five AIs, a maze) arrives by word 6, the stake ("no map") closes it, and it is true for all five at step 0. It is a statement, about 7 words, one breath with commas (target about 2.0 s, `--gap 0.06 --long 0.15 --max-speedup 1.45`). Weak spot written down: "lost" says nothing about who wins, so the pull is the situation, not a result. **Backup: H2** if both blind readers miss what is happening, or H3 if they miss the subject. Compare H1 / H2 / H3 with blind agents before voicing (13.11 rule).
Comment mechanic: on screen only, a small handwritten chip at "Go": "pick one before it starts" (underline stroke, no box). The hook itself stays a statement.

## 4. BUILD-UP beat list (15.11 rule: each beat adds something NEW, tension rises, the reveal is staged)
Video time is an estimate (about 2.7 words a second plus race-only stretches); the builder fits the race clock to the voice (`retime.py`), never the reverse.

| Beat | Video s (est.) | Line | Real event | What is NEW here | Open question carried forward |
|---|---|---|---|---|---|
| B1 hook | 0.0-2.0 | 1 | step 0: five logo dots in the centre | the situation: lost, no map, five rival AIs | which one gets out? |
| B2 premise as a process | 2.1-4.6 | 2 | (setup scene) | the request flies from a phone to five logo chips, each "answers" (thinking dots, no code), each dot lights up with its logo | will their moves work? |
| B3 rules + Go | 4.7-6.9 | 3 | step 0 | they cannot see the maze; chip "pick one before it starts"; Go on the last word | race starts |
| B4 first casualty (reason to stay at about 8 s) | 7.5-9.3 | 4 | steps 3-20: Perplexity paces 4 cells by the start | one is out of the game at once: the stakes are real | will others fail too? |
| B5 split and wrong way | 9.8-12.6 | 5 | steps 29-61: ChatGPT walks away from the exit (to 102); Claude ahead | the most famous AI goes backwards; a leader appears | can Claude hold it? |
| (race-only) | 12.6-15.5 | none | steps 50-117: Gemini/Meta AI take the lead together (a doubled dot: two logos touching), dead ends light up as hand-drawn X marks; status row shows steps to the exit falling | the lead changes without a word; the doubled dot is the detail to catch on a second watch | who is that pair? |
| B6 the twist (reason to stay at about two thirds) | 15.5-17.6 | 6 | step 117: two dots leave at the same step | not one winner but two, at the very same step; names NOT spoken yet (logos visible) | how can two tie exactly? |
| B7 near miss and the loser | 17.9-22.0 | 7 | step 117: Claude 10 away, turns back to 23; out at 171; ChatGPT paces two cells from step 152, the tail runs fast to 500 (counter shows it) | a near miss, a late finish, a dot looping forever | how did the two tie? |
| B8 the reveal | 22.4-25.4 | 8 | paths of Gemini and Meta AI overlaid | the payoff: they took the SAME path, every single step; the two ink trails redraw as one line; result card lands (saveable) | closed |
| B9 setup | 25.6-27.1 | 9 | card footer | where to get the request | |
| B10 tomorrow | 27.3-31.6 | 10 | card folds, back to the frame-0 layout for a clean loop | next promise | tomorrow's episode |
Total about 32 s (inside 30-40). Every beat adds a new fact; nothing only explains the picture; the winners' names come last.

Two honest weak spots: the race-only stretch (12.6-15.5) has no voice and must carry itself with motion (dead-end X marks, the falling numbers, the doubled dot pulling ahead); and the tie is the twist but the logos are visible at step 117, so a fast viewer reads the names before line 8. That is fine: line 8's new fact is "same path, every step", not the names.

## 5. Shot list in short (Miki style paper, `video/ep89c` + the ep99 scaffold; the frame is filled)
- Stage: the maze 798 px square at x 141-939, y 450-1248 (scaffold), the status row of five logo chips with "steps to the exit" at y about 309. That fills the safe box; nothing else is added to fill space.
- Frame 0 (must pass the blind test): the maze, five logo dots stacked in the centre, the EXIT gap marked with a hand-drawn arrow, and at most 3 lines: "LOST IN A MAZE." / "FIVE AIs. NO MAP." Real logos (`hf/assets/logos/`, sources in `SOURCES.md`). No code, no "move()", no "v.up", no "500 steps" jargon beyond a plain step counter.
- B2: a phone bubble with the plain request "get this dot out of the maze" (plain words; the real prompt lives on `/e/99`), five chips answer with thinking dots, each dot lights up.
- Gemini and Meta AI: drawn as two touching dots that move as one from step 0 (all five start on one cell; the scaffold fans them a few px apart). Do not hide that they overlap; it is the detail that rewards a second watch.
- B8 reveal: replay strip, both trails redraw from start to exit at once and merge into one line; label "same path, every step" handwritten (no box).
- Result card (saveable): "AI RACE #2 · THE MAZE"; rows land worst first, the tie last: Perplexity "stuck by the start"; ChatGPT "lost, closest 52 steps away"; Claude "out in 171 steps"; Gemini "out in 117"; Meta AI "out in 117, same path". Footer: "best possible: 89 steps". 
- No word inside a filled box, no handle, no black wipes, nothing still for 2.5 s, soft eased motion.

## 6. Concept checklist (4.11 list) and the 14.11 pre-publish checklist
| # | Check | Result |
|---|---|---|
| 1 | Something specific happening to the viewer's own account | PARTIAL: the AIs they use daily, losing in public; not their own account |
| 2 | Curiosity gap only the video closes | YES: who gets out; then how two can tie |
| 3 | Something worth saving | PARTIAL: the result card; the request on `/e/99` once live |
| 4 | A named person to send it to | WEAK: the friend who swears by ChatGPT (not spoken; a send line was cut for length) |
| 5 | Reason to watch twice | YES: the doubled dot, the dead-end marks, your own pick's route; the end returns to frame 0 |
| 6 | Checkable by a stranger in 30 s | YES only once `/e/99` is live with the real race (today its race.json is a placeholder) |
| P1 | Subject clear at frame 0 | J: likely, to be tested by blind readers |
| P2 | Promise paid by about 10 s | J: yes, Perplexity's stall at about 8 s is the first payoff |
| P3 | One theme | yes |
| P9 | Original, full resolution | yes |
| P10 | Short caption | about 1,400 characters, the result is in the first lines |

## 7. Scores (labels, not gates; my scores have not predicted our views, Spearman -0.23)
HOOK 76: a felt situation in word 1 and a clear picture; no result tease. VIRALITY 72: one stage in constant motion, five rival brands, a side to pick, a real twist (an exact tie) and a famous AI walking in circles; but a dot in a maze is about the AIs, not about the viewer (why-stuck point 4), and our account rarely gets comments. OVERALL 72. **Predicted views: 300-1,200, most likely about 550** (the race format is untested on our account: 98 has not been published).

## 8. What David must decide
1. **99 goes out before 98:** then "AI RACE #2" on screen and in the caption comes before #1 exists. Options: keep #2 (98 follows as a "prequel"), renumber this one #1, or drop the number on screen. And episode 98's last line ("Tomorrow, they face a maze") must be re-voiced if 98 goes out after 99.
2. **The tomorrow line (line 10) is a PLACEHOLDER TO CONFIRM:** "Tomorrow, a free tool says it fixes Claude Code. Follow, so you see if it works." True only if episode 100 (the Graphify fact-check) is written, verified live and publishes the next day. If not, re-voice as "Next, a free tool says it fixes Claude Code..." without a day.
3. **The date of the five answers** (and screenshots if any) for the caption and `/e/99`.
4. **`/e/99` live with the real race** before the caption's "link in bio" line is true (today the page is on a branch with a placeholder race.json).
5. Hook H1 vs H2 after the blind readers.
