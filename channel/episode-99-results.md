# Episode 99 results: AI RACE #2, the maze (run 15.11.2026)

Frozen arena (hashes in `video/ep99/arena/HASH.txt`, written before any answer existed). Each AI got PROMPT-B once, in a new chat, no extra modes, the first answer only. Answers saved verbatim in `video/ep99/answers/*-B.txt` (sha256 in `answers.sha256`). Which model version answered in each app is UNCONFIRMED (no screenshots). Run: `node run_maze.mjs` -> `video/ep99/arena/maze-race.json`, sha256 cd723db0ff39ce918d844180d5e5906c8099e2b2fe3046b76aba87a8c37b3ef2. Shortest possible way out: 89 steps. Limit: 500 steps.

| Rank | AI | Result | Cells visited |
|---|---|---|---|
| 1 (tie) | Gemini | OUT in 117 steps | 110 |
| 1 (tie) | Meta AI | OUT in 117 steps, the exact same path as Gemini | 110 |
| 3 | Claude | OUT in 171 steps | 140 |
| 4 | ChatGPT | did not get out; closest 52 steps from the exit (at step 125), then 29 cells walked in circles for the other 375 steps | 140 |
| 5 | Perplexity | did not get out; stuck among 4 cells next to the start, never got closer than 86 steps (at step 3) | 4 |

Facts checked in the run: no wall bumps or invalid answers by anyone. Gemini and Meta AI path arrays are identical cell by cell (checked 15.11). Perplexity's code keeps its own position and ignores v.x/v.y (visible in its answer file); the cause of its stall was not analysed beyond that. ChatGPT's loop cause was not analysed. The Claude answer redefines `move` at the end of the file (it runs fine in the sandbox).
Not claimed: any ranking of "intelligence"; one run, one prompt, one maze.


David, 15.11.2026: the Claude answer came from Sonnet 5.5 (his words, no screenshot). The other four models are UNCONFIRMED.
