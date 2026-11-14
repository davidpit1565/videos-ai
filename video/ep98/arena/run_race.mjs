#!/usr/bin/env node
// run_race.mjs: runs the AI RACE.
//
//   node run_race.mjs [--out race.json] name=path/to/answer.txt [name=path ...]
//
// Each answer file is the AI's reply as received (it may contain prose and
// markdown fences). The function `steer` is taken out of it and run inside a
// node:vm context with no require, process, fetch, timers, console output or
// host objects, with Math.random seeded and Date frozen to the race clock.
// Each car runs in its own child process (cars are ghosts to each other), so a
// hostile or broken answer can hang or crash only its own car.
//
// Budgets: 50 ms to load the file; steer() may use 5 ms per step on average
// and never more than 50 ms in one call. Over budget, a throw,
// or a return value that is not { turn: number, gas: number } stops the car
// (status "error"); the reason is recorded as is.
//
// No network, no clock in the output: the same files give a byte-identical
// race.json (only an answer that really runs close to the time budget could
// behave differently from run to run). Cars run one after another, not in
// parallel, so they do not compete for the CPU.
import { fork } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { dirname, join, basename, resolve } from 'node:path';
import vm from 'node:vm';

const here = dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const sha = (buf) => createHash('sha256').update(buf).digest('hex');

const LOAD_MS = 50;
const STEP_MS = 5;      // average per steer() call
const CALL_CAP_MS = 50; // hard cap for one call
const CHUNK = 120;

/* ======================= child: one car ======================= */
if (process.argv[2] === '--car') {
  const file = process.argv[3];
  const seed = Number(process.argv[4]) >>> 0;
  const Arena = require(join(here, 'arena.js'));
  const T = Arena.prepareTrack(JSON.parse(readFileSync(join(here, 'track.json'), 'utf8')));
  const text = readFileSync(file, 'utf8');
  const send = (m) => process.send(m);

  // --- candidate sources: fenced blocks that mention steer, the whole text,
  //     then a brace-matched slice starting at "function steer"
  const candidates = [];
  const fence = /```[^\n`]*\n([\s\S]*?)```/g;
  let m;
  const blocks = [];
  while ((m = fence.exec(text))) blocks.push(m[1]);
  blocks.forEach((b, i) => { if (/\bsteer\b/.test(b)) candidates.push({ how: `markdown code block ${i + 1} of ${blocks.length}`, src: b }); });
  if (blocks.length > 1) {
    const all = blocks.join('\n');
    if (/\bsteer\b/.test(all)) candidates.push({ how: `all ${blocks.length} markdown code blocks joined`, src: all });
  }
  candidates.push({ how: 'whole reply as code', src: text });
  const fi = text.search(/function\s+steer\s*\(/);
  if (fi >= 0) {
    const open = text.indexOf('{', fi);
    let depth = 0, end = -1;
    for (let i = open; i >= 0 && i < text.length; i++) {
      if (text[i] === '{') depth++;
      else if (text[i] === '}' && --depth === 0) { end = i; break; }
    }
    if (end > 0) candidates.push({ how: 'brace-matched "function steer" taken out of the prose', src: text.slice(fi, end + 1) });
  }

  // --- sandbox. The global's backing object has no prototype, so nothing in
  //     the context can reach a host constructor through it.
  const BOOT = `
    (function (g, seed) {
      'use strict';
      var s = seed >>> 0;
      Math.random = function () { // mulberry32, fixed seed per car
        s = (s + 0x6D2B79F5) >>> 0; var t = s;
        t = Math.imul(t ^ (t >>> 15), t | 1);
        t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
      };
      var RealDate = Date;
      g.__ms = 0;
      function FixedDate() {
        var a = Array.prototype.slice.call(arguments);
        var d = a.length ? new (Function.prototype.bind.apply(RealDate, [null].concat(a)))() : new RealDate(g.__ms);
        return new.target ? d : d.toString();
      }
      FixedDate.prototype = RealDate.prototype;
      FixedDate.now = function () { return g.__ms; };
      FixedDate.UTC = RealDate.UTC; FixedDate.parse = RealDate.parse;
      g.Date = FixedDate;
      var noop = function () {};
      g.console = { log: noop, info: noop, warn: noop, error: noop, debug: noop, table: noop };
      g.module = { exports: {} }; g.exports = g.module.exports;
      delete g.SharedArrayBuffer; delete g.Atomics; delete g.WebAssembly;
    })(globalThis, ${seed});`;
  const FIND = `(function(){ try { if (typeof steer === 'function') return steer; } catch (e) {}
      var me = globalThis.module && globalThis.module.exports;
      if (typeof me === 'function') return me;
      if (me && typeof me.steer === 'function') return me.steer;
      if (me && me.default && typeof me.default === 'function') return me.default;
      return null; })()`;
  const WRAP = `(function (f) { return function (a, b, c, d) {
      try {
        var r = f({ front: a, left: b, right: c, speed: d });
        if (r === null || typeof r !== 'object') return 'X' + (r === null ? 'null' : typeof r);
        var t = r.turn, g = r.gas;
        if (typeof t !== 'number' || typeof g !== 'number') return 'Xan object with turn ' + typeof t + ' and gas ' + typeof g;
        return 'N' + t + '|' + g;
      } catch (e) {
        var msg;
        try { msg = (e && typeof e.message === 'string') ? e.message : String(e); } catch (e2) { msg = 'unprintable error'; }
        return 'E' + String(msg).slice(0, 200);
      }
    }; })`;

  function makeContext() {
    const box = Object.create(null);
    const ctx = vm.createContext(box, { codeGeneration: { strings: true, wasm: false }, microtaskMode: 'afterEvaluate' });
    vm.runInContext(BOOT, ctx, { timeout: LOAD_MS });
    return { box, ctx };
  }
  const safeMsg = (e) => {
    try { if (e && e.code === 'ERR_SCRIPT_EXECUTION_TIMEOUT') return 'timeout'; } catch { /* hostile */ }
    try { return (e && typeof e.message === 'string') ? e.message.slice(0, 200) : 'error'; } catch { return 'error'; }
  };

  // A candidate that is not valid JavaScript (SyntaxError) or defines no
  // steer() is skipped and the next one is tried. A candidate that IS valid
  // code but throws or runs over the budget while loading stops there: the car
  // does not start (we never cut code out to get around a runtime failure).
  let chosen = null, loadErr = null, ctxUsed = null;
  const skipped = [];
  for (const c of candidates) {
    let src = c.src, how = c.how;
    // the only change we allow to the code: ES-module "export" syntax cannot
    // run as a plain script, so the keyword (or a bare export line) is removed
    const exp1 = /^(\s*)export\s+(default\s+)?(?=(async\s+)?function\s+steer\b|(const|let|var)\s+steer\b)/m;
    const exp2 = /^\s*export\s+(default\s+steer|\{\s*steer\s*\})\s*;?\s*$/m;
    if (exp1.test(src) || exp2.test(src)) {
      src = src.replace(exp1, '$1').replace(exp2, '');
      how += ' (removed "export")';
    }
    let script;
    try { script = new vm.Script(src, { filename: 'answer.js' }); }
    catch (e) { skipped.push(`${c.how}: not valid JavaScript (${safeMsg(e)})`); continue; }
    let env;
    try { env = makeContext(); } catch (e) { loadErr = 'sandbox failed: ' + safeMsg(e); break; }
    try {
      script.runInContext(env.ctx, { timeout: LOAD_MS });
    } catch (e) {
      const msg = safeMsg(e);
      loadErr = `${how}: ${msg === 'timeout' ? `loading took over ${LOAD_MS} ms` : 'threw while loading: ' + msg}`;
      break;
    }
    let ok = false;
    try { ok = vm.runInContext(`typeof (${FIND}) === 'function'`, env.ctx, { timeout: LOAD_MS }) === true; }
    catch (e) { loadErr = `${how}: looking up steer failed: ${safeMsg(e)}`; break; }
    if (!ok) { skipped.push(`${c.how}: no function steer`); continue; }
    try { vm.runInContext(`globalThis.__w = (${WRAP})(${FIND});`, env.ctx, { timeout: LOAD_MS }); }
    catch (e) { loadErr = `${how}: ${safeMsg(e)}`; break; }
    chosen = { how, srcSha: sha(src) }; ctxUsed = env; break;
  }
  if (!chosen && !loadErr) loadErr = 'no runnable function steer: ' + skipped.join('; ');

  const stepScript = new vm.Script('__w(__a, __b, __c, __d)');
  let bank = CALL_CAP_MS - STEP_MS; // first call may take up to 50 ms (compiling)
  let errorText = null;
  const driver = ctxUsed
    ? (s, car) => {
        const box = ctxUsed.box;
        box.__a = s.front; box.__b = s.left; box.__c = s.right; box.__d = s.speed;
        box.__ms = Math.round((car.frame * 1000) / 60);
        let r;
        // budget: 5 ms per step on average (a bank that grows 5 ms each step,
        // starting at 50 ms), and no single call over 50 ms. A one-off pause of
        // the machine therefore cannot stop a normal answer; an endless loop
        // is stopped within 50 ms.
        bank += STEP_MS;
        const cap = Math.max(1, Math.min(CALL_CAP_MS, bank));
        const t0 = process.hrtime.bigint();
        try { r = stepScript.runInContext(ctxUsed.ctx, { timeout: Math.ceil(cap) }); }
        catch (e) {
          const m = safeMsg(e);
          errorText = m === 'timeout' ? (cap >= CALL_CAP_MS ? `one steer() call took over ${CALL_CAP_MS} ms` : `steer() used more than ${STEP_MS} ms per step on average`) : m;
          return { cmd: null, reason: errorText };
        }
        bank -= Number(process.hrtime.bigint() - t0) / 1e6;
        if (bank < 0) { errorText = `steer() used more than ${STEP_MS} ms per step on average`; return { cmd: null, reason: errorText }; }
        if (typeof r !== 'string') { errorText = 'steer() wrapper was replaced'; return { cmd: null, reason: errorText }; }
        if (r[0] === 'E') { errorText = 'steer() threw: ' + r.slice(1); return { cmd: null, reason: errorText }; }
        if (r[0] === 'X') { errorText = 'steer() returned ' + r.slice(1) + ', not { turn, gas } numbers'; return { cmd: null, reason: errorText }; }
        if (r[0] !== 'N') { errorText = 'steer() wrapper was replaced'; return { cmd: null, reason: errorText }; }
        const [t, g] = r.slice(1).split('|').map(Number);
        if (!Number.isFinite(t) || !Number.isFinite(g)) { errorText = `steer() returned turn ${t}, gas ${g}`; return { cmd: null, reason: errorText }; }
        return { cmd: { turn: t, gas: g } };
      }
    : () => ({ cmd: null, reason: 'did not start: ' + loadErr });

  send({ type: 'meta', extraction: chosen ? chosen.how : null, codeSha256: chosen ? chosen.srcSha : null, loadError: chosen ? null : loadErr });
  const states = [];
  let car = Arena.initCar(T);
  states.push(car);
  const flush = () => { send({ type: 'frames', frames: states.splice(0) }); };
  while (car.status === 'run' && car.frame < Arena.CONST.MAX_FRAMES) {
    const s = Arena.sense(T, car);
    const out = driver(s, car);
    car = Arena.step(T, car, out.cmd || null, out.reason);
    states.push(car);
    if (states.length >= CHUNK) flush();
  }
  flush();
  send({ type: 'done', progress: Arena.progress(T, car), gates: T.gates.length });
  process.disconnect();
  process.exit(0);
}

/* ======================= parent ======================= */
const args = process.argv.slice(2);
let out = join(here, 'race.json');
const entries = [];
let allowUnfrozen = false;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--out') out = resolve(args[++i]);
  else if (args[i] === '--allow-unfrozen') allowUnfrozen = true;
  else if (args[i].includes('=')) { const k = args[i].indexOf('='); entries.push({ id: args[i].slice(0, k), file: resolve(args[i].slice(k + 1)) }); }
  else entries.push({ id: basename(args[i]).replace(/\.[^.]+$/, ''), file: resolve(args[i]) });
}
if (!entries.length) {
  console.error('usage: node run_race.mjs [--out race.json] name=answer.txt [name=answer.txt ...]');
  process.exit(2);
}

const arenaBuf = readFileSync(join(here, 'arena.js'));
const trackBuf = readFileSync(join(here, 'track.json'));
const arenaSha = sha(arenaBuf), trackSha = sha(trackBuf);
const hashFile = join(here, 'HASH.txt');
if (existsSync(hashFile)) {
  const h = readFileSync(hashFile, 'utf8');
  const frozen = h.includes(arenaSha) && h.includes(trackSha);
  if (!frozen && !allowUnfrozen) {
    console.error('arena.js or track.json differ from HASH.txt: the arena is frozen. Refusing to race (use --allow-unfrozen only for calibration before any AI answer exists).');
    process.exit(3);
  }
}
const Arena = require(join(here, 'arena.js'));
const C = Arena.CONST;
const WATCHDOG_MS = 5000 + C.MAX_FRAMES * STEP_MS + CALL_CAP_MS * 2;

function runCar(entry, index) {
  return new Promise((resolveCar) => {
    const res = { meta: null, frames: [], done: null, killed: null };
    let fileBuf;
    try { fileBuf = readFileSync(entry.file); } catch (e) { res.killed = 'answer file not readable'; return resolveCar(res); }
    res.fileSha256 = sha(fileBuf);
    const child = fork(fileURLToPath(import.meta.url), ['--car', entry.file, String(1000 + index)], {
      execArgv: ['--max-old-space-size=256', '--stack-size=900'],
      stdio: ['ignore', 'ignore', 'ignore', 'ipc'],
      env: {},
      serialization: 'advanced',
    });
    const timer = setTimeout(() => { res.killed = res.killed || `runner stopped the car: no result after ${WATCHDOG_MS} ms`; child.kill('SIGKILL'); }, WATCHDOG_MS);
    child.on('message', (m) => {
      if (m.type === 'meta') res.meta = m;
      else if (m.type === 'frames') for (const f of m.frames) res.frames.push(f);
      else if (m.type === 'done') res.done = m;
    });
    child.on('error', () => { res.killed = res.killed || 'car process failed'; });
    child.on('exit', (code, signal) => {
      clearTimeout(timer);
      if (!res.done && !res.killed) res.killed = `car process ended early (${signal || 'exit ' + code}), probably out of memory`;
      resolveCar(res);
    });
  });
}

const r3 = (v) => Math.round(v * 1000) / 1000;
const results = [];
for (let i = 0; i < entries.length; i++) results.push(await runCar(entries[i], i));
const T = Arena.prepareTrack(JSON.parse(trackBuf.toString('utf8')));

const cars = results.map((r, i) => {
  let states = r.frames;
  if (!states.length) states = [Arena.initCar(T)];
  let last = states[states.length - 1];
  if (r.killed && last.status === 'run') {
    last = { ...last, frame: last.frame + 1, status: 'error', speed: 0, stopFrame: last.frame + 1, stopReason: r.killed };
    states = states.concat([last]);
  }
  const prog = r.done ? r.done.progress : Arena.progress(T, last);
  return {
    id: entries[i].id,
    file: basename(entries[i].file),
    fileSha256: r.fileSha256 || null,
    extraction: r.meta ? r.meta.extraction : null,
    codeSha256: r.meta ? r.meta.codeSha256 : null,
    loadError: r.meta ? r.meta.loadError : r.killed,
    status: last.status,
    laps: last.lap,
    finishFrame: last.finishFrame,
    timeS: last.finishFrame != null ? r3(last.finishFrame / C.FPS) : null,
    stopFrame: last.stopFrame,
    stopTimeS: last.stopFrame != null ? r3(last.stopFrame / C.FPS) : null,
    stopReason: last.stopReason,
    stopSector: last.stopSector || (last.status !== 'finish' ? T.sector[Arena.nearestSample(T, last.x, last.y)] : null),
    stopAt: last.status !== 'finish' ? [r3(last.x), r3(last.y)] : null,
    progressGates: prog,
    progressLaps: r3(prog / T.gates.length),
    clampedSteps: last.clamps,
    _states: states,
  };
});

// order: finishers by time, then the rest by distance covered, then by how long they ran
const order = cars.slice().sort((a, b) => {
  if ((a.status === 'finish') !== (b.status === 'finish')) return a.status === 'finish' ? -1 : 1;
  if (a.status === 'finish') return a.finishFrame - b.finishFrame;
  if (b.progressGates !== a.progressGates) return b.progressGates - a.progressGates;
  return (b.stopFrame || 0) - (a.stopFrame || 0);
});
order.forEach((c, i) => { c.place = i + 1; });

const endFrame = Math.max(...cars.map((c) => c._states[c._states.length - 1].frame));
const STATUS = { run: 'run', wall: 'wall', finish: 'finish', error: 'error', dnf: 'dnf' };
for (const c of cars) {
  const fr = [];
  for (let f = 0, k = 0; f <= endFrame; f++) {
    while (k + 1 < c._states.length && c._states[k + 1].frame <= f) k++;
    const s = c._states[k];
    fr.push([r3(s.x), r3(s.y), r3(s.angle), r3(s.speed), s.lap, STATUS[s.status] || s.status]);
  }
  c.frames = fr;
  delete c._states;
}

const race = {
  format: 'AI RACE #1 race.json v1',
  fps: C.FPS,
  frameColumns: ['x', 'y', 'angle', 'speed', 'lap', 'status'],
  statusMeaning: { run: 'driving', wall: 'touched the wall, stopped', finish: 'finished 2 laps', error: 'steer() failed (threw, too slow, bad value, or did not load); stopped', dnf: 'still running at the time limit' },
  arenaSha256: arenaSha,
  trackSha256: trackSha,
  constants: C,
  budgets: { loadMs: LOAD_MS, stepMs: STEP_MS },
  frameCount: endFrame + 1,
  result: order.map((c) => ({
    place: c.place, id: c.id, status: c.status, laps: c.laps, timeS: c.timeS, finishFrame: c.finishFrame,
    stopTimeS: c.stopTimeS, stopFrame: c.stopFrame, stopReason: c.stopReason, stopSector: c.stopSector, stopAt: c.stopAt,
    progressLaps: c.progressLaps, clampedSteps: c.clampedSteps, extraction: c.extraction, loadError: c.loadError,
    file: c.file, fileSha256: c.fileSha256, codeSha256: c.codeSha256,
  })),
  cars: cars.map((c) => ({ id: c.id, frames: c.frames })),
};
writeFileSync(out, JSON.stringify(race) + '\n');
console.log('wrote', out, 'sha256', sha(readFileSync(out)));
for (const r of race.result) {
  console.log(`${r.place}. ${r.id.padEnd(12)} ${r.status.padEnd(6)} laps ${r.laps}  ${r.timeS != null ? r.timeS.toFixed(2) + ' s' : `stopped ${r.stopTimeS} s in ${r.stopSector}: ${r.stopReason}`}  [${r.extraction || r.loadError}]`);
}
