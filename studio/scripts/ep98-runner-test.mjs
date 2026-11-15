// Node test of public/site/ep98/runner.js with hostile answers (worker_threads stands in for the
// browser worker; the real browser sandbox was tested in Chrome, see channel/episode-98-page-notes.md).
//   node scripts/ep98-runner-test.mjs
import { Worker } from 'node:worker_threads';
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
const require = createRequire(import.meta.url);
const SITE = new URL('../public/site/ep98/', import.meta.url).pathname;
const Arena = require(SITE + 'arena.js');
const AW = require(SITE + 'runner.js');
const track = JSON.parse(readFileSync(SITE + 'track.json', 'utf8'));
const WORKER = `const { parentPort } = require('node:worker_threads');
const AW = require(${JSON.stringify(SITE + 'runner.js')});
const { performance } = require('node:perf_hooks');
const post = (m) => parentPort.postMessage(m);
AW.startWorker(globalThis, post, (fn) => parentPort.on('message', fn), () => performance.now());`;
async function race(text, seed) {
  const w = new Worker(WORKER, { eval: true, resourceLimits: { maxOldGenerationSizeMb: 128 } });
  let replyFn = null;
  w.on('message', (m) => replyFn && replyFn(m));
  w.on('error', () => {});
  const worker = { send: (m) => w.postMessage(m), onReply: (fn) => { replyFn = fn; }, kill: () => w.terminate() };
  const timers = { set: (f, ms) => setTimeout(f, ms), clear: (id) => clearTimeout(id), now: () => performance.now() };
  return AW.runRace(Arena, track, text, seed, worker, timers);
}
const ok = 'function steer(s){return {turn:(s.right-s.left)/100, gas: s.front<80&&s.speed>3?0:0.6};}';
const cases = {
  'endless loop at load': 'while(true){} function steer(){return {turn:0,gas:1}}',
  'endless loop in steer at step 20': 'var n=0; function steer(s){ if(++n===20) for(;;){} return {turn:(s.right-s.left)/100,gas:0.5}; }',
  'slow steer 80 ms once': 'var n=0; function steer(s){ if(++n===10){var t=performance.now(); while(performance.now()-t<80){}} return {turn:(s.right-s.left)/100,gas:0.5}; }',
  'slow steer 8 ms every step (average)': 'function steer(s){var t=performance.now(); while(performance.now()-t<8){} return {turn:(s.right-s.left)/100,gas:0.5}; }',
  'endless getter on turn': 'function steer(){ return { get turn(){ for(;;){} }, gas: 1 }; }',
  'throws object with endless message getter': 'function steer(){ throw { get message(){ for(;;){} } }; }',
  'stack overflow': 'function steer(s){ return steer(s); }',
  'big allocations': 'var a=[]; function steer(){ for(;;) a.push(new Array(1e6).fill(1)); }',
  'returns array': 'function steer(){ return [0,1]; }',
  'returns strings': 'function steer(){ return {turn:"0",gas:"1"}; }',
  'returns NaN': 'function steer(){ return {turn:NaN,gas:1}; }',
  'refusal no code': "I can't help with that, sorry.",
  'export function in prose + fence': 'Sure! Here it is:\n```js\nexport function steer(s){ return {turn:(s.right-s.left)/100, gas: s.front<80&&s.speed>3?0:0.6}; }\n```\nGood luck!',
  'process / require escape': 'var leaked = typeof process + "/" + typeof require + "/" + typeof fetch + "/" + typeof setTimeout; function steer(){ throw new Error(leaked); }',
  'constructor escape': 'function steer(){ var p; try { p = this.constructor.constructor("return typeof process")(); } catch(e){ p = "blocked:"+e.message; } throw new Error(String(p)); }',
  'Math.random repeatable': 'function steer(s){ return {turn:(s.right-s.left)/100 + (Math.random()-0.5)*0.4, gas: s.front<80&&s.speed>3?0:0.6}; }',
  'reference ok driver': ok,
};
for (const [name, code] of Object.entries(cases)) {
  const t0 = performance.now();
  const r = await race(code, 1005);
  const r2 = name === 'Math.random repeatable' ? await race(code, 1005) : null;
  console.log(`${name.padEnd(42)} ${String(r.status).padEnd(6)} stopFrame ${String(r.stopFrame).padEnd(5)} ${(r.stopReason||'').slice(0,110)} ${r2 ? (JSON.stringify(r2.f)===JSON.stringify(r.f)?'[repeat: identical]':'[repeat: DIFFERENT]') : ''} ${(performance.now()-t0).toFixed(0)} ms`);
}
process.exit(0);
