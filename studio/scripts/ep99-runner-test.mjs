// Node test of public/site/ep99/runner.js with hostile answers (worker_threads stands in for the
// browser worker; the real browser sandbox is tested in a browser, see channel/episode-99-page-notes.md).
//   node scripts/ep99-runner-test.mjs
// Also checks fidelity: the two reference bots, run through this runner, must give the same
// status, steps and cells as the real maze race (public/site/ep99/race.json).
import { Worker } from 'node:worker_threads';
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
const require = createRequire(import.meta.url);
const SITE = new URL('../public/site/ep99/', import.meta.url).pathname;
const ARENA = new URL('../../video/ep99/arena/', import.meta.url).pathname;
const Maze = require(SITE + 'maze.js');
const AW = require(SITE + 'runner.js');
const mazeJson = JSON.parse(readFileSync(SITE + 'maze.json', 'utf8'));
const WORKER = `const { parentPort } = require('node:worker_threads');
const AW = require(${JSON.stringify(SITE + 'runner.js')});
const { performance } = require('node:perf_hooks');
const post = (m) => parentPort.postMessage(m);
AW.startWorker(globalThis, post, (fn) => parentPort.on('message', fn), () => performance.now());`;
async function run(text, seed = 1005) {
  const w = new Worker(WORKER, { eval: true, resourceLimits: { maxOldGenerationSizeMb: 128 } });
  let replyFn = null;
  w.on('message', (m) => replyFn && replyFn(m));
  w.on('error', () => {});
  const worker = { send: (m) => w.postMessage(m), onReply: (fn) => { replyFn = fn; }, kill: () => w.terminate() };
  const timers = { set: (f, ms) => setTimeout(f, ms), clear: (id) => clearTimeout(id), now: () => performance.now() };
  return AW.runMaze(Maze, mazeJson, text, seed, worker, timers);
}
let bad = 0;
const check = (cond, msg) => { if (!cond) { bad++; console.log('  FAIL: ' + msg); } };

const fn = (body) => `function move(v){ ${body} }`;
const cases = {
  'endless loop at load': ['while(true){} function move(){return "up"}', { status: 'error' }],
  'endless loop in move at step 20': ['var n=0; function move(v){ if(++n===20) for(;;){} return "up"; }', { status: 'error', steps: 19 }],
  'slow move 80 ms once': ['var n=0; function move(v){ if(++n===10){var t=Date.now(),t0=performance.now(); while(performance.now()-t0<80){}} return "up"; }', { status: 'error' }],
  'slow move 8 ms every step (average)': ['function move(v){var t=performance.now(); while(performance.now()-t<8){} return "up"; }', { status: 'error' }],
  'throws object with endless message getter': ['function move(){ throw { get message(){ for(;;){} } }; }', { status: 'error' }],
  'stack overflow (counts as a throw, run goes on)': ['function move(v){ return move(v); }', { status: 'dnf', steps: 500 }],
  'big allocations': ['var a=[]; function move(){ for(;;) a.push(new Array(1e6).fill(1)); }', { status: 'error' }],
  'returns "Up" (stays, goes on)': [fn('return "Up";'), { status: 'dnf', steps: 500, invalidSteps: 500 }],
  'returns undefined': [fn(''), { status: 'dnf', invalidSteps: 500 }],
  'throws every step (stays, goes on)': [fn('throw new Error("boom");'), { status: 'dnf', invalidSteps: 500 }],
  'walks into walls (counted as bumps)': [fn('return "up";'), { status: 'dnf', steps: 500 }],
  'refusal no code': ["I can't help with that, sorry.", { status: 'error' }],
  'export function in prose + fence': ['Sure! Here it is:\n```js\nexport function move(v){ return v.right==="exit"?"right":"right"; }\n```\nGood luck!', { status: 'dnf' }],
  'process / require escape': ['var leaked = typeof process + "/" + typeof require + "/" + typeof fetch + "/" + typeof setTimeout; function move(){ throw new Error(leaked); }', { status: 'dnf', firstInvalidHas: 'undefined/undefined/undefined/undefined' }],
  'constructor escape': ['function move(){ var p; try { p = this.constructor.constructor("return typeof process")(); } catch(e){ p = "blocked:"+e.message; } throw new Error(String(p)); }', { status: 'dnf' }],
  'Math.random repeatable': [fn('return ["up","down","left","right"][Math.floor(Math.random()*4)];'), { status: 'dnf', repeat: true }],
};
for (const [name, [code, want]] of Object.entries(cases)) {
  const t0 = performance.now();
  const r = await run(code);
  const r2 = want.repeat ? await run(code) : null;
  console.log(`${name.padEnd(48)} ${String(r.status).padEnd(5)} steps ${String(r.steps).padEnd(4)} invalid ${String(r.invalidSteps).padEnd(4)} bumps ${String(r.wallBumps).padEnd(4)} ${(r.stopReason || r.firstInvalid || '').slice(0, 90)} ${(performance.now() - t0).toFixed(0)} ms`);
  check(r.status === want.status, `status ${r.status}, wanted ${want.status}`);
  if (want.steps != null) check(r.steps === want.steps, `steps ${r.steps}, wanted ${want.steps}`);
  if (want.invalidSteps != null) check(r.invalidSteps === want.invalidSteps, `invalid ${r.invalidSteps}`);
  if (want.firstInvalidHas) check((r.firstInvalid || '').includes(want.firstInvalidHas), `firstInvalid ${r.firstInvalid}`);
  if (r2) check(JSON.stringify(r2.p) === JSON.stringify(r.p), 'Math.random run not repeatable');
  check(r.p.length === (r.steps + 1) * 2, 'path length does not match steps');
}

console.log('--- fidelity against the real maze race (race.json) ---');
const race = JSON.parse(readFileSync(SITE + 'race.json', 'utf8'));
for (const c of race.cars) {
  const file = c.id === 'careful' ? 'ref-careful.js' : c.id === 'naive' ? 'ref-naive.js' : null;
  if (!file) continue;
  const r = await run(readFileSync(ARENA + file, 'utf8'), 1005);
  const same = r.status === c.status && r.steps === c.steps && r.closestDist === c.closestDist &&
    r.cellsVisited === c.cellsVisited && JSON.stringify(r.p) === JSON.stringify(c.p);
  console.log(`${c.id.padEnd(8)} ${r.status} steps ${r.steps} closest ${r.closestDist}  ${same ? 'identical to race.json' : 'DIFFERENT'}`);
  check(same, `${c.id} differs from race.json`);
}
console.log(bad ? `${bad} FAILED` : 'all ok');
process.exit(bad ? 1 : 0);
