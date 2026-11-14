# AI RACE #1 arena (episode 98, task T1)

Built 14.11.2026, before any AI answer existed. Frozen: `HASH.txt` holds the sha256 of
`arena.js` and `track.json`, and `run_race.mjs` refuses to race if either changes.
Plan and fairness rules: `channel/episode-98-plan.md` sections 1 and 6 (PROMPT A).

## Run it

```
cd video/ep98/arena
node run_race.mjs --out race.json chatgpt=../answers/chatgpt-A.txt gemini=../answers/gemini-A.txt claude=../answers/claude-A.txt meta=../answers/meta-A.txt
```

Node 22, no packages, no network. Prints the result table and the sha256 of `race.json`.
Cars run one after another (each in its own child process); the whole race takes about a second.

## Files

| File | What it is |
|---|---|
| `arena.js` | The physics. Pure functions, no I/O, no randomness, no clock. Node `require` or browser `window.Arena` (for the T11 playable page and the T8 scene). |
| `track.json` | The frozen road: centreline, left/right edge polygons, sector name per sample, start pose. World 950 x 808 px, meant to sit 1:1 at x 65-1015, y 440-1248 of the 1080x1920 frame. |
| `make_track.mjs` | How `track.json` was made (control points, Catmull-Rom, width blend). Re-running it gives a byte-identical file. Not needed to race. |
| `run_race.mjs` | The runner: takes `steer` out of each reply, runs it sandboxed, writes `race.json`. |
| `ref-naive.js` | Our reference driver 1 (not an AI): full gas, never brakes. Must hit a wall. |
| `ref-careful.js` | Our reference driver 2 (not an AI): slows when the wall ahead is close. Must finish 2 laps in 7-11 s. |
| `ref-race.json` | The calibration race of the two reference drivers. |
| `HASH.txt` | sha256 of `arena.js` and `track.json`. |

## Rules as coded (match PROMPT A)

- 60 fixed steps per second; `steer(s)` is called once per step with a fresh
  `s = { front, left, right, speed }`.
- Sensors: distance from the car's nose to the nearest wall, straight ahead, 45 deg left,
  45 deg right, capped at 400. Speed 0-10, in px per step.
- `{ turn, gas }`: turn -1 = full left, 1 = full right; gas 0-1; gas under 0.2 brakes
  (-0.35 per step). Gas 0.2-1 adds `0.16 x gas - 0.02` per step. Turn rate is
  `turn x 0.07 rad` per step at speed 3 or more, scaled down below 3. Finite numbers outside
  the range are clamped and counted (`clampedSteps`); anything else (not an object, turn or gas
  not a number, NaN/Infinity, a throw) stops the car with status `error`.
- The car is 20 px wide, 34 px long. When any part touches a wall the car is placed at the
  contact point and stops (`wall`).
- Laps count only by passing every gate (one every 6 px of centreline) in order, so a car
  cannot gain by turning round. 2 laps finish (`finish`). A car still running after 60 s is
  `dnf`.
- Cars are ghosts: each one is simulated alone. All cars start at the same pose (centre on the
  finish line, facing east). Any visual offset on the grid is a scene choice; `race.json`
  has them on the same spot at frame 0.
- Road: width 92-140 px (prompt: 90-140), length 2,088.8 px per lap. Bends (radius under
  200 px): a sweep of -24 deg (min radius 146), -34 deg (121), a right kink of +40 deg (88)
  and the hairpin, -170 deg at min radius 60. The hairpin is the only bend over 40 deg at a
  tight radius. Sector names (`start straight`, `long sweep`, `back straight`, `hairpin`)
  are written for where a car stops.

## Taking the code out of a reply

In this order, the first one that is valid JavaScript and defines `steer` wins; the method is
written into `race.json` (`extraction`):
1. each markdown code block that mentions `steer`; 2. all code blocks joined;
3. the whole reply; 4. `function steer(...) { ... }` cut out of the prose by brace matching.

A candidate is skipped only if it is not valid JavaScript or has no `steer`. Valid code that
throws or runs too long while loading means the car does not start; we never cut code out to
get around a runtime failure. The only edit to the code: an ES-module `export` in front of
`steer` (or a bare `export default steer;` line) is removed, and the method says so.
`steer` may be a function declaration, `const steer = ...`, or `module.exports`.
`fileSha256` and `codeSha256` (the code actually run) are in the result.

## Sandbox

- `node:vm` context whose global's backing object has no prototype (no route to host
  constructors). No `require`, `process`, `Buffer`, `fetch`, timers, `import()` (rejects),
  `SharedArrayBuffer`, `Atomics`, `WebAssembly`. `console.*` exists and does nothing.
- `Math.random` is seeded per car (fixed seeds 1000, 1001, ... in argument order) and `Date`
  shows the race clock, so an answer that uses them is still repeatable.
- Microtasks run inside each timed call (`microtaskMode: afterEvaluate`).
- Time: 50 ms to load the file; `steer` may use 5 ms per step on average (a bank that grows
  5 ms each step) and never more than 50 ms in one call. Results come back as plain strings
  built inside the sandbox, so no getter or proxy runs outside the time limit.
- Each car runs in its own child process (256 MB heap, empty environment, no stdio); the
  parent kills it after 28 s without a result. A crash or kill stops only that car, with the
  reason recorded.

## race.json

`fps`, `constants`, `arenaSha256`, `trackSha256`, `frameCount`, `result[]` (place, id, status,
laps, timeS, finishFrame, stopTimeS, stopFrame, stopReason, stopSector, stopAt, progressLaps,
clampedSteps, extraction, loadError, file, fileSha256, codeSha256) and `cars[].frames`: one
row per frame, `[x, y, angle, speed, lap, status]`, padded with the last state after a car
stops so all cars have `frameCount` rows. Order: finishers by time, then by distance
covered, then by how long they ran. No timestamps or paths, so it is byte-identical run to
run.

## Tests run on 14.11.2026 (Node v22.23.4)

Calibration (reference drivers only; constants were tuned with these two, nothing after):
```
1. careful  finish laps 2  8.67 s   (520 frames)
2. naive    wall   laps 0  stopped 3.733 s in hairpin, at (125.7, 659.0)
```
Determinism, same input three times:
```
refs (naive + careful):            99085182fbcb26f3b8c716f2da02bec6b1c482ee9797d9c4f97a7b271a18be3c  x3 (cmp identical)
10 mixed files (below, incl. 2 hostile): 0f39030970550617d6e9836338550652755bc74db20cb9d14cd1cd6c341dc6f0  x3
```
Extraction and bad answers (files written for the test, then deleted): prose + fenced block +
`export function` -> ran, finished 8.00 s; inline code inside a sentence -> brace-matched,
ran (braked to a stop, `dnf` at 60 s); `const steer = arrow` with `Math.random`/`Date.now`
-> ran, repeatable, hit the wall; throws at speed -> `error` "steer() threw: boom at speed";
returns an array -> `error`; returns strings -> `error`; a refusal with no code -> did not
start ("Unexpected identifier 'can'").

Hostile files (written for the test, then deleted), none hung or crashed the runner, total
run about 1 s, exit 0:
- escape attempts (`this.constructor.constructor('return process')`, the same through
  `globalThis`, `console.log`, `Math.max`, an Error object, `require`, `process`, `fetch`,
  timers, `Buffer`, `import('fs')`, writing a marker file): none worked, no marker file;
  `typeof process` and `typeof require` inside = undefined, `import()` rejected.
- endless loop at load -> did not start (over 50 ms); endless loop in steer at step 20 ->
  stopped "one steer() call took over 50 ms"; endless getter on `turn`; a Proxy that throws an
  object with an endless `message` getter; an endless microtask chain; stack overflow ->
  "Maximum call stack size exceeded"; big allocations / `ArrayBuffer` loop -> stopped at the
  50 ms cap; `process.exit(1)` -> did not start ("process is not defined").
- child crash path, checked on a scratch copy with the heap cut to 16 MB: the child aborted,
  the runner reported "car process ended early (SIGABRT), probably out of memory" for that
  car and the reference car still finished 8.67 s.
- frozen guard, checked on a scratch copy with `track.json` edited: exit 3, "Refusing to race".

## Known limits (say them as they are)

- An answer that genuinely runs close to 5 ms per step on average could stop at a different
  frame on a slower or busier machine. Normal answers take microseconds.
- Out-of-range numbers are clamped, not treated as nonsense (a car returning `gas: 2` drives).
  This rule was set before any answer existed; `clampedSteps` shows when it was used.
- The physics is a simple top-down model (no grip limit, no skidding): the only thing that
  ends a race early is touching a wall.
