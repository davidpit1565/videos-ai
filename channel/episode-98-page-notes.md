# Episode 98: the /e/98 page (task T11, 15.11.2026)

Branch `ship-ep98` (from origin/main), not pushed, not merged.

## What was built
- `studio/lib/articles.ts`: entry `n: 98` (title, standfirst, 10 steps, changes, limits). `python3 export/check_setup_guide.py 98` passes (10 real steps, no Hebrew).
- `studio/app/e/[n]/page.tsx`: renders `<Race98 />` only when `n === 98`, above "The exact clicks".
- `studio/app/e/[n]/race98.tsx` (+ `race98.module.css`): client component with three sections:
  - **The race**: canvas drawing of the frozen road, the five real cars replayed from `race.json` at true speed (60 frames/s), ink trails, **Play the race** / **Pause**, a time slider, per-car status and **Show code** (exact answer text, React-escaped, plain text), and a result box at the end.
  - **The request**: PROMPT A word for word and **Copy the request** (tested: the clipboard text equals PROMPT A in `channel/episode-98-plan.md`).
  - **Race your own AI**: **Add my AI** opens a textarea, **Race** runs it in the sandbox and adds a sixth (yellow) car; **Remove my car**.
- `studio/app/e/[n]/race98-host.ts`: page side of the sandbox (iframe creation, message checks, result validation, ordering, sha256).
- `studio/public/site/ep98/`: `arena.js` and `track.json` (byte copies of the frozen files: sha256 bac5a096... and 0cc3955e..., same as `video/ep98/arena/HASH.txt`), `runner.js` (worker + controller), `race.json` (109 KB).
- `studio/scripts/ep98-race-json.mjs` (makes race.json), `studio/scripts/ep98-runner-test.mjs` (hostile-input test).
- Routes: `/site` is already public in `studio/lib/routes.ts`; `/e` too. `node studio/scripts/check-routes.mjs` passes. No route change.

## How to regenerate race.json
```
cd video/ep98/arena
node run_race.mjs --out /tmp/race-full.json chatgpt=../answers/chatgpt-A.txt gemini=../answers/gemini-A.txt claude=../answers/claude-A.txt meta=../answers/meta-A.txt perplexity=../answers/perplexity-A.txt
# must print sha256 efda0893670a53e2afdc4342d752f5e0585c5c3057fc4b814ee2637d29435215
cd ../../../studio
node scripts/ep98-race-json.mjs /tmp/race-full.json ../video/ep98/answers
```
The script refuses if `public/site/ep98/arena.js`/`track.json` are not the frozen files or an answer file's sha256 differs from the race. Nothing is re-simulated: positions are copied and rounded (x, y 0.1 px, angle 0.01 rad), cut at each car's stop frame. Output on 15.11.2026: 109,140 bytes, sha256 3241193a18468abf3f0d45644de28548d8f912763dc3239ba95c2b1aa837f96e (records `sourceRaceSha256` efda08...).

## Sandbox design
- Page (our origin) never runs pasted code. It creates `<iframe sandbox="allow-scripts" srcdoc=CONTROLLER_HTML>` (no allow-same-origin => opaque origin). The pasted text goes in by `postMessage`, never into HTML.
- The iframe's CSP `default-src 'none'; script-src 'unsafe-inline' 'unsafe-eval' blob:; worker-src blob:` blocks all network; the blob worker inherits it.
- Iframe main thread = controller: frozen physics (arena.js) + budgets. Pasted code runs ONLY in the blob worker (`startWorker`), asked once per step for `{turn, gas}`.
- Budgets as in run_race.mjs: 50 ms load, 5 ms/step average (bank), 50 ms per call (measured in the worker); a call with no reply in 1.5 s => worker terminated ("one steer() call took over 50 ms"); whole run 45 s in the iframe, 60 s in the page, then the iframe is removed.
- Page accepts messages only from that iframe's window with a per-run nonce; `validateResult` allows only known statuses, finite numbers, bounded lengths, cut strings. The iframe is removed after every run.
- Worker also deletes fetch/XHR/WebSocket/importScripts/indexedDB/caches/Worker/timers etc. from the global and its prototypes (second layer; Math.random seeded 1005, Date = race clock, as in Node).

## Security review: ways out and what blocks them (tested in Chrome 153 headless via Playwright, and Node)
| Attempt | Result |
|---|---|
| Read page cookie / localStorage / parent DOM from the sandbox | SecurityError for all three (opaque origin) |
| fetch / XHR from the iframe or a blob worker with fetch NOT deleted | blocked by CSP; local server saw zero /exfil requests |
| Recover fetch from WorkerGlobalScope.prototype | found before the fix, now `undefined` (deleted on prototypes too); CSP blocks anyway |
| importScripts, new Worker inside the worker | not available |
| Endless loop at load / in steer / endless getter on `turn` / throw with endless `message` getter / endless microtask chain / memory bomb / `self.close()` | worker killed after 1.5 s, car stopped with a reason; the page's own 10 ms tick counter kept running at full rate in every case (page never blocked) |
| 8 ms per call average | stopped "more than 5 ms per step on average" |
| Stack overflow, array/string/NaN returns, refusal text | stopped / did not start with the same reasons as run_race.mjs |
| Fake replies via postMessage from the worker | only changes the visitor's own car |
| HTML/script in pasted text or in result strings | rendered by React as text; never in srcdoc |
| Top navigation, popups, forms, modals, downloads | not in the sandbox flags |
Fidelity: the five real answers, run through the browser sandbox (and through Node worker_threads), give the same status, the same finish/stop frame and positions within 0.0005 px of the real race (rounding only). Pasting ChatGPT's answer inside prose and a ```javascript fence gave 10.58 s, the same as the race.

UI test (Chrome, 375 px wide, React 19 from esm.sh, the real component compiled with tsc): no horizontal scroll, replay plays to the result box (Claude 8.48, Gemini 8.68, ChatGPT 10.58, Perplexity did not finish, Meta AI wall 6.15 s), Show code text equals the answer file, no iframe left after runs, no page errors. Type check: `tsc --strict` on race98.tsx + race98-host.ts with @types/react 19 and on articles.ts: clean.

## Not tested / known gaps
- No `next build` and no `npm ci` (no node_modules, disk ~3.2 GB free); page.tsx (2-line change) was not type-checked with Next's types. Vercel build is the first full build.
- Safari / iOS and Firefox not tested. If a browser cannot start a blob Worker in a sandboxed iframe, the run fails with a message (it does not fall back to running on a main thread).
- A memory bomb in the worker can, in some browsers, crash the whole tab (renderer out of memory); in Chrome here the worker was killed by the timeout first.
- Differences from Node: one shared global per run instead of a fresh context per extraction candidate; an endless microtask chain is caught one frame later; other browsers may round Math.sin/cos/atan2 differently, so a car that only scrapes past a wall could differ (said on the page).
- Model/app labels of the five answers are UNCONFIRMED (no screenshots yet); the page names apps only and says so. Perplexity/Claude constant overlap is stated as unconfirmed.
- The page reflects the race of 14.11.2026; the Instagram embed appears only once the episode is published.
