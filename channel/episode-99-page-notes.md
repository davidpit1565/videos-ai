# Episode 99: the /e/99 page, AI RACE #2 (the maze) (15.11.2026)

Built on the working branch, not committed, not pushed, not merged. Modelled on the /e/98 page
(`studio/app/e/[n]/race98.tsx`, `race98-host.ts`, `studio/public/site/ep98/*`, which live on main and
`ship-ep98` and were read from there; see `channel/episode-98-page-notes.md` on that branch).

## What was built
- `studio/app/e/[n]/maze99.tsx` (+ `maze99.module.css`): three sections. **The maze**: canvas drawing of
  the frozen 21 x 21 maze (walls from `maze.json`), the dots replayed from `race.json` at 30 steps a second,
  ink trails, Play / Pause, a step slider, per dot "steps so far" and "closest so far, in steps from the exit",
  and a result box at the end. **The request**: PROMPT B word for word, **Copy the request**. **Run your own
  AI**: **Add my AI**, a paste box, **Run**, **Remove my dot**. No code of the reference dots or of any AI is
  shown (no "Show code"); the only code-like text on the page is the request and the paste box.
- `studio/app/e/[n]/maze99-host.ts`: page side of the sandbox (iframe, message checks, result validation, order, sha256).
- `studio/app/e/[n]/page.tsx`: `import Maze99` and `{n === 99 ? <Maze99 /> : null}` above "The exact clicks".
  NOTE: on this branch page.tsx has no ep98 wiring (it is on main / ship-ep98), so a merge with ship-ep98 touches
  the same two places and needs both lines kept.
- `studio/public/site/ep99/`: `maze.js` and `maze.json` (byte copies of the frozen files, sha256 e82cbb3c... and
  022ad448..., equal to `video/ep99/arena/HASH.txt`), `runner.js` (worker + controller, `AWM99`), `race.json`.
- `race.json` TODAY IS A PLACEHOLDER: `placeholder: true`, only our two reference bots (careful, naive), labelled
  "Reference bot ... (ours, not an AI)"; the page shows a notice. 5.2 KB.
- `studio/scripts/ep99-race-json.mjs`, `studio/scripts/ep99-runner-test.mjs`.
- No change to `routes.ts` (`/e` and `/site` are already public). `node studio/scripts/check-routes.mjs` passes.
- `articles.ts`: NOT touched (needs the real results).

## Make the real race.json (after the five answers exist)
```
cd video/ep99/arena
node run_maze.mjs --out maze-race.json chatgpt=../answers/chatgpt-B.txt gemini=../answers/gemini-B.txt claude=../answers/claude-B.txt meta=../answers/meta-B.txt perplexity=../answers/perplexity-B.txt
cd ../../../studio
node scripts/ep99-race-json.mjs ../video/ep99/arena/maze-race.json ../video/ep99/answers
```
It refuses if `public/site/ep99/maze.js` / `maze.json` differ from the files the race ran with, or an answer file's
sha256 differs from the race's. Nothing is re-simulated: cells are copied. Placeholder (already done, repeatable):
`node scripts/ep99-race-json.mjs ../video/ep99/arena/ref-maze-race.json ../video/ep99/arena --placeholder`.
Then replace the placeholder text in the page only if wanted (the notice disappears by itself when `placeholder` is absent).

## Sandbox design (same as /e/98)
- The page never runs pasted code. `<iframe sandbox="allow-scripts" srcdoc=CONTROLLER_HTML>` (no allow-same-origin:
  opaque origin). The pasted text goes in by `postMessage`, never into HTML.
- iframe CSP `default-src 'none'; script-src 'unsafe-inline' 'unsafe-eval' blob:; worker-src blob:` blocks all network;
  the blob worker inherits it. The worker also deletes fetch / XHR / WebSocket / importScripts / indexedDB / caches /
  Worker / timers from its global and prototypes (second layer).
- The iframe's main thread runs the frozen rules (`maze.js`) and the budgets; the pasted code runs only in the worker.
- Budgets as in `run_maze.mjs`: 50 ms load; `move` 5 ms per step on average (bank starting at 50 ms), 50 ms in one call;
  a call with no reply in 1.5 s ends the worker ("one move() call took over 50 ms"); whole run 45 s in the iframe,
  60 s in the page, then the iframe is removed. Math.random seeded (visitor seed 1005), Date.now() = 1 s per step.
- A throw or a return value that is not one of the four strings is NOT the end: the dot stays, the step counts
  (`invalidSteps`), as in the real runner.
- Messages are accepted only from that iframe's window with a per-run nonce. `validateResult`: known statuses only,
  whole cells in -1..21, one-cell moves only, length at most 501 cells, strings cut short; React renders strings as text.
- Before a visitor run the page hashes `maze.js` and `maze.json` and compares them with `race.json`
  (`mazeJsSha256`, `mazeJsonSha256`); a mismatch stops the run.

## Tests run
- `node studio/scripts/ep99-runner-test.mjs` (Node, worker_threads standing in for the browser worker): 16 hostile or
  odd answers (endless loop at load and in move, 80 ms call, 8 ms every step, endless message getter, stack overflow,
  memory bomb, "Up", undefined, throw every step, wall walking, refusal text, export in prose + fence, process/require/
  fetch/setTimeout escape, constructor escape, Math.random repeatability), all as expected; plus fidelity: the two
  reference bots through this runner give the SAME status, steps, closest distance and every cell as `race.json`
  (careful: out in 183 steps; naive: dnf, closest 86).
- Real browser: Chrome (google-chrome, headless, Playwright core) running the compiled `maze99-host.ts` with the real
  sandbox iframe + blob worker: careful and naive give identical cells to race.json; endless loops at load and at step
  20 and a memory bomb are stopped after about 1.5 s with the page's own timer ticking at full rate meanwhile; a try
  to `fetch('/exfil')` reached the local server 0 times; `fetch`, XMLHttpRequest, importScripts, Worker, localStorage,
  document are not reachable in the worker; the iframe is removed after each run; no page errors.
- `tsc --strict` on `maze99.tsx` and `maze99-host.ts` with @types/react 19: clean.
- `node studio/scripts/check-routes.mjs`: passes (53 routes classified).

## Not tested / known gaps
- No `npm run check:routes` through npm and no `next build` (no `studio/node_modules`): `page.tsx` was not type-checked
  with Next's types; the Vercel build is the first full build.
- The React page itself (canvas drawing, replay, layout at 375 px) was type-checked but NOT rendered in a browser.
- Safari / iOS and Firefox not tested. If a browser cannot start a blob Worker in a sandboxed iframe, the run fails with a
  message (no fallback to the main thread).
- A memory bomb can crash the whole tab in some browsers; in Chrome here the timeout came first.
- Differences from Node: one shared global per run instead of a fresh context per extraction candidate; browsers may
  differ in Math rounding (does not matter for a maze that uses only whole cells).
- The page shows no AI results yet: race.json is the placeholder. Model/app labels of the AI answers are unconfirmed
  until there are screenshots.
