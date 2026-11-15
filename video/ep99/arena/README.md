# AI RACE #2 maze (episode 99, task T14)

Built 15.11.2026, before any AI answer existed. Frozen: `HASH.txt` holds the sha256 of
`maze.js`, `maze.json`, `run_maze.mjs` and `PROMPT-B.txt`; `run_maze.mjs` refuses to run if
any of them changes. Model: `video/ep98/arena/` (same sandbox, budgets and hashing).

## Run it

```
cd video/ep99/arena
node run_maze.mjs --out maze-race.json chatgpt=../answers/chatgpt-B.txt gemini=../answers/gemini-B.txt claude=../answers/claude-B.txt meta=../answers/meta-B.txt perplexity=../answers/perplexity-B.txt
node check_rules.mjs   # PROMPT-B.txt says what the engine does
```

Node 22, no packages, no network. Prints the table and the sha256 of the result file.

## Files

| File | What it is |
|---|---|
| `maze.js` | The rules. Pure functions, no I/O, randomness or clock. Node `require` or browser `window.Maze` (for the /e/99 page). |
| `maze.json` | The frozen maze: 21 x 21, `open[y]` = one hex digit per cell (1 up, 2 right, 4 down, 8 left = open side), start, exit, an ASCII `picture`. |
| `make_maze.mjs` | How `maze.json` was made: seed 1083, depth-first carving from the centre, 14 extra inner walls knocked out (loops), one exit gap. Re-running gives a byte-identical file. |
| `run_maze.mjs` | The runner: takes `move` out of each reply, runs it sandboxed, writes the result file with every dot's full path. |
| `PROMPT-B.txt` | The exact text David pastes into each AI. |
| `check_rules.mjs` | 16 checks that the prompt text matches `maze.js` / `maze.json`. |
| `ref-naive.js`, `ref-careful.js` | Our two reference bots (not AIs). `ref-maze-race.json` = their run. |

## Rules as coded

- Start (10, 10), exit gap on the left wall at (0, 20). Shortest way out: 89 steps.
  38 dead ends, 14 loops (passages beyond a tree).
- `move(v)` once per step, `v = { up, down, left, right, x, y }`, fresh each call; sides are
  `"wall"`, `"open"` or `"exit"`. up = y - 1, right = x + 1.
- Return exactly `"up" | "down" | "left" | "right"`. A move into a wall, any other value, or a
  throw: the dot stays, the step counts, the run goes on (`wallBumps`, `invalidSteps`,
  `firstInvalid`).
- 500 steps max. Got out = `exit` (score = steps). Else `dnf`, ranked by `closestDist` (the
  fewest steps from the exit it ever was), then who got there first.
- Memory: one sandbox per dot for the whole run, so globals persist.
- Ends early only on the time budget or a failed load (`error`).

## Sandbox (same as ep98)

`node:vm` with a prototype-less global, no `require`/`process`/`fetch`/timers/WebAssembly,
silent `console`, seeded `Math.random` (1000, 1001, ... in argument order), `Date.now()` =
1 s per step. 50 ms to load; `move` may use 5 ms per step on average, never 50 ms in one
call. Each dot in its own child process (256 MB heap); the parent kills it after 7.6 s.

## Result file

`sha256` of the four frozen files, `shortestSteps`, `start`, `exit`, `result[]` (place, id,
status, steps, exitStep, closestDist, closestAt, closestStep, end, invalidSteps, wallBumps,
firstInvalid, stopReason, cellsVisited, extraction, loadError, file and code sha256) and
`paths[]`: per dot, the cell after each step (`path[0]` = start; a cell outside 0..20 = out
through the exit). Byte-identical run to run.

## Tests run on 15.11.2026 (Node v22.23.4)

Calibration (the seed was picked so that these hold; nothing changes after the hash):
```
1. careful  OUT in 183 steps  (visited 162 cells)
2. naive    dnf, closest 86 steps from the exit (walks back and forth on 4 cells)
```
Same input three times: identical sha256. Other bots tried on this maze (not frozen, only
to see the spread): memory + backtracking with other direction orders: 129, 139, 141 steps
and one dnf; right-hand and left-hand wall follower: dnf (they circle an island); random
walk: dnf. Extraction and bad answers (scratch files): prose + fenced block + `export` ran;
`"Up"` and a throw = stays, run goes on; an endless loop = stopped at 50 ms; escape attempts
(`process`, `require`, `constructor.constructor`) saw `undefined`; a refusal with no code did
not start; `Math.random` answer repeatable.

## Known limits

- A dnf ranks by closest distance, which a lucky wander can win over a tidy search.
- An answer running close to 5 ms per step on average could stop at a different step on a
  slower machine. Normal answers take microseconds.
