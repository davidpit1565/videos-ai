#!/usr/bin/env node
// run_maze.mjs: runs AI RACE #2 (the maze).
//
//   node run_maze.mjs [--out maze-race.json] name=path/to/answer.txt [name=path ...]
//
// Each answer file is the AI's reply as received (it may contain prose and
// markdown fences). The function `move` is taken out of it and run inside a
// node:vm context with no require, process, fetch, timers, console output or
// host objects, with Math.random seeded and Date frozen to the step clock.
// Each dot runs in its own child process, so a hostile or broken answer can
// hang or crash only its own run. Same sandbox and budgets as episode 98's
// run_race.mjs.
//
// Budgets: 50 ms to load the file; move() may use 5 ms per step on average and
// never more than 50 ms in one call. Over budget ends the run (status "error").
// A throw or a return value that is not one of the four direction strings is
// NOT the end: the dot stays where it is for that step (rule in PROMPT-B.txt),
// counted in invalidSteps.
//
// No network, no clock in the output: the same files give a byte-identical
// result file. Dots run one after another, not in parallel.
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
const STEP_MS = 5;      // average per move() call
const CALL_CAP_MS = 50; // hard cap for one call

/* ======================= child: one dot ======================= */
if (process.argv[2] === '--bot') {
  const file = process.argv[3];
  const seed = Number(process.argv[4]) >>> 0;
  const Maze = require(join(here, 'maze.js'));
  const M = Maze.prepareMaze(JSON.parse(readFileSync(join(here, 'maze.json'), 'utf8')));
  const text = readFileSync(file, 'utf8');
  const send = (m) => process.send(m);

  // --- candidate sources: fenced blocks that mention move, all blocks joined,
  //     the whole text, then a brace-matched slice starting at "function move"
  const candidates = [];
  const fence = /```[^\n`]*\n([\s\S]*?)```/g;
  let m;
  const blocks = [];
  while ((m = fence.exec(text))) blocks.push(m[1]);
  blocks.forEach((b, i) => { if (/\bmove\b/.test(b)) candidates.push({ how: `markdown code block ${i + 1} of ${blocks.length}`, src: b }); });
  if (blocks.length > 1) {
    const all = blocks.join('\n');
    if (/\bmove\b/.test(all)) candidates.push({ how: `all ${blocks.length} markdown code blocks joined`, src: all });
  }
  candidates.push({ how: 'whole reply as code', src: text });
  const fi = text.search(/function\s+move\s*\(/);
  if (fi >= 0) {
    const open = text.indexOf('{', fi);
    let depth = 0, end = -1;
    for (let i = open; i >= 0 && i < text.length; i++) {
      if (text[i] === '{') depth++;
      else if (text[i] === '}' && --depth === 0) { end = i; break; }
    }
    if (end > 0) candidates.push({ how: 'brace-matched "function move" taken out of the prose', src: text.slice(fi, end + 1) });
  }

  // --- sandbox. The global's backing object has no prototype, so nothing in
  //     the context can reach a host constructor through it.
  const BOOT = `
    (function (g, seed) {
      'use strict';
      var s = seed >>> 0;
      Math.random = function () { // mulberry32, fixed seed per dot
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
  const FIND = `(function(){ try { if (typeof move === 'function') return move; } catch (e) {}
      var me = globalThis.module && globalThis.module.exports;
      if (typeof me === 'function') return me;
      if (me && typeof me.move === 'function') return me.move;
      if (me && me.default && typeof me.default === 'function') return me.default;
      return null; })()`;
  // v is built inside the sandbox, fresh each call; the answer comes back as a
  // plain string so no getter or proxy runs outside the time limit
  const WRAP = `(function (f) { return function (u, d, l, r, x, y) {
      try {
        var out = f({ up: u, down: d, left: l, right: r, x: x, y: y });
        if (out === 'up' || out === 'down' || out === 'left' || out === 'right') return 'N' + out;
        if (typeof out === 'string') return 'Xreturned "' + out.slice(0, 40) + '"';
        return 'Xreturned ' + (out === null ? 'null' : typeof out);
      } catch (e) {
        var msg;
        try { msg = (e && typeof e.message === 'string') ? e.message : String(e); } catch (e2) { msg = 'unprintable error'; }
        return 'Ethrew: ' + String(msg).slice(0, 200);
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

  // A candidate that is not valid JavaScript or defines no move() is skipped
  // and the next one is tried. A candidate that IS valid code but throws or
  // runs over the budget while loading stops there: the dot does not start.
  let chosen = null, loadErr = null, ctxUsed = null;
  const skipped = [];
  for (const c of candidates) {
    let src = c.src, how = c.how;
    // the only change we allow to the code: ES-module "export" syntax cannot
    // run as a plain script, so the keyword (or a bare export line) is removed
    const exp1 = /^(\s*)export\s+(default\s+)?(?=(async\s+)?function\s+move\b|(const|let|var)\s+move\b)/m;
    const exp2 = /^\s*export\s+(default\s+move|\{\s*move\s*\})\s*;?\s*$/m;
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
    catch (e) { loadErr = `${how}: looking up move failed: ${safeMsg(e)}`; break; }
    if (!ok) { skipped.push(`${c.how}: no function move`); continue; }
    try { vm.runInContext(`globalThis.__w = (${WRAP})(${FIND});`, env.ctx, { timeout: LOAD_MS }); }
    catch (e) { loadErr = `${how}: ${safeMsg(e)}`; break; }
    chosen = { how, srcSha: sha(src) }; ctxUsed = env; break;
  }
  if (!chosen && !loadErr) loadErr = 'no runnable function move: ' + skipped.join('; ');

  send({ type: 'meta', extraction: chosen ? chosen.how : null, codeSha256: chosen ? chosen.srcSha : null, loadError: chosen ? null : loadErr });

  let bot = Maze.initBot(M);
  const path = [[bot.x, bot.y]];
  if (!ctxUsed) {
    bot = Maze.stop(bot, 'did not start: ' + loadErr);
  } else {
    const stepScript = new vm.Script('__w(__u, __d, __l, __r, __x, __y)');
    let bank = CALL_CAP_MS - STEP_MS; // first call may take up to 50 ms (compiling)
    const box = ctxUsed.box;
    while (bot.status === 'run') {
      const v = Maze.view(M, bot);
      box.__u = v.up; box.__d = v.down; box.__l = v.left; box.__r = v.right; box.__x = v.x; box.__y = v.y;
      box.__ms = bot.step * 1000; // Date.now() inside = 1 second per step
      bank += STEP_MS;
      const cap = Math.max(1, Math.min(CALL_CAP_MS, bank));
      const t0 = process.hrtime.bigint();
      let r;
      try { r = stepScript.runInContext(ctxUsed.ctx, { timeout: Math.ceil(cap) }); }
      catch (e) {
        const msg = safeMsg(e);
        bot = Maze.stop(bot, msg === 'timeout'
          ? (cap >= CALL_CAP_MS ? `one move() call took over ${CALL_CAP_MS} ms` : `move() used more than ${STEP_MS} ms per step on average`)
          : 'sandbox: ' + msg);
        break;
      }
      bank -= Number(process.hrtime.bigint() - t0) / 1e6;
      if (bank < 0) { bot = Maze.stop(bot, `move() used more than ${STEP_MS} ms per step on average`); break; }
      if (typeof r !== 'string' || !/^[NXE]/.test(r)) { bot = Maze.stop(bot, 'move() wrapper was replaced'); break; }
      bot = r[0] === 'N' ? Maze.step(M, bot, r.slice(1)) : Maze.step(M, bot, undefined, r.slice(1));
      path.push([bot.x, bot.y]);
    }
  }
  send({ type: 'done', bot, path });
  process.disconnect();
  process.exit(0);
}

/* ======================= parent ======================= */
const args = process.argv.slice(2);
let out = join(here, 'maze-race.json');
const entries = [];
let allowUnfrozen = false;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--out') out = resolve(args[++i]);
  else if (args[i] === '--allow-unfrozen') allowUnfrozen = true;
  else if (args[i].includes('=')) { const k = args[i].indexOf('='); entries.push({ id: args[i].slice(0, k), file: resolve(args[i].slice(k + 1)) }); }
  else entries.push({ id: basename(args[i]).replace(/\.[^.]+$/, ''), file: resolve(args[i]) });
}
if (!entries.length) {
  console.error('usage: node run_maze.mjs [--out maze-race.json] name=answer.txt [name=answer.txt ...]');
  process.exit(2);
}

const FROZEN = ['maze.js', 'maze.json', 'run_maze.mjs', 'PROMPT-B.txt'];
const shas = Object.fromEntries(FROZEN.map((f) => [f, existsSync(join(here, f)) ? sha(readFileSync(join(here, f))) : null]));
const hashFile = join(here, 'HASH.txt');
if (existsSync(hashFile)) {
  const h = readFileSync(hashFile, 'utf8');
  const frozen = FROZEN.every((f) => shas[f] && h.includes(`${shas[f]}  ${f}`));
  if (!frozen && !allowUnfrozen) {
    console.error(`${FROZEN.join(', ')} differ from HASH.txt: the maze is frozen. Refusing to run (use --allow-unfrozen only for calibration before any AI answer exists).`);
    process.exit(3);
  }
}
const Maze = require(join(here, 'maze.js'));
const C = Maze.CONST;
const WATCHDOG_MS = 5000 + C.MAX_STEPS * STEP_MS + CALL_CAP_MS * 2;

function runBot(entry, index) {
  return new Promise((done) => {
    const res = { meta: null, done: null, killed: null };
    let fileBuf;
    try { fileBuf = readFileSync(entry.file); } catch (e) { res.killed = 'answer file not readable'; return done(res); }
    res.fileSha256 = sha(fileBuf);
    const child = fork(fileURLToPath(import.meta.url), ['--bot', entry.file, String(1000 + index)], {
      execArgv: ['--max-old-space-size=256', '--stack-size=900'],
      stdio: ['ignore', 'ignore', 'ignore', 'ipc'],
      env: {},
      serialization: 'advanced',
    });
    const timer = setTimeout(() => { res.killed = res.killed || `runner stopped the dot: no result after ${WATCHDOG_MS} ms`; child.kill('SIGKILL'); }, WATCHDOG_MS);
    child.on('message', (m) => {
      if (m.type === 'meta') res.meta = m;
      else if (m.type === 'done') res.done = m;
    });
    child.on('error', () => { res.killed = res.killed || 'dot process failed'; });
    child.on('exit', (code, signal) => {
      clearTimeout(timer);
      if (!res.done && !res.killed) res.killed = `dot process ended early (${signal || 'exit ' + code}), probably out of memory`;
      done(res);
    });
  });
}

const M = Maze.prepareMaze(JSON.parse(readFileSync(join(here, 'maze.json'), 'utf8')));
const results = [];
for (let i = 0; i < entries.length; i++) results.push(await runBot(entries[i], i));

const bots = results.map((r, i) => {
  let bot = r.done ? r.done.bot : Maze.stop(Maze.initBot(M), r.killed);
  const path = r.done ? r.done.path : [[M.start.x, M.start.y]];
  return {
    id: entries[i].id,
    file: basename(entries[i].file),
    fileSha256: r.fileSha256 || null,
    extraction: r.meta ? r.meta.extraction : null,
    codeSha256: r.meta ? r.meta.codeSha256 : null,
    loadError: r.meta ? r.meta.loadError : r.killed,
    status: bot.status,
    steps: bot.step,
    exitStep: bot.status === 'exit' ? bot.step : null,
    closestDist: bot.closest,
    closestAt: bot.closestAt,
    closestStep: bot.closestStep,
    end: [bot.x, bot.y],
    invalidSteps: bot.invalid,
    wallBumps: bot.bumps,
    firstInvalid: bot.firstInvalid,
    stopReason: bot.stopReason,
    cellsVisited: new Set(path.map((p) => p[0] + ',' + p[1])).size,
    path,
  };
});

// order: exits by steps, then the rest by closest distance, then who got there first
const order = bots.slice().sort((a, b) => {
  if ((a.status === 'exit') !== (b.status === 'exit')) return a.status === 'exit' ? -1 : 1;
  if (a.status === 'exit') return a.exitStep - b.exitStep;
  if (a.closestDist !== b.closestDist) return a.closestDist - b.closestDist;
  return a.closestStep - b.closestStep;
});
order.forEach((c, i) => { c.place = i + 1; });

const race = {
  format: 'AI RACE #2 maze-race.json v1',
  sha256: shas,
  constants: C,
  budgets: { loadMs: LOAD_MS, stepMs: STEP_MS, callCapMs: CALL_CAP_MS },
  shortestSteps: M.dist[M.start.y][M.start.x],
  start: M.start, exit: M.exit,
  statusMeaning: { exit: 'got out', dnf: 'still inside after 500 steps', error: 'move() did not load, ran over the time budget, or crashed; stopped' },
  pathNote: 'path[k] = the cell after step k (path[0] = start); an unchanged cell = stayed (wall or invalid answer); a cell outside 0..20 = out through the exit',
  result: order.map(({ path, ...rest }) => rest),
  paths: bots.map((c) => ({ id: c.id, path: c.path })),
};
writeFileSync(out, JSON.stringify(race) + '\n');
console.log('wrote', out, 'sha256', sha(readFileSync(out)));
console.log(`shortest possible: ${race.shortestSteps} steps`);
for (const r of race.result) {
  const what = r.status === 'exit' ? `OUT in ${r.exitStep} steps`
    : `${r.status}, closest ${r.closestDist} steps from the exit (step ${r.closestStep})${r.stopReason ? ': ' + r.stopReason : ''}`;
  console.log(`${r.place}. ${r.id.padEnd(12)} ${what}  [visited ${r.cellsVisited}, bumps ${r.wallBumps}, invalid ${r.invalidSteps}] [${r.extraction || r.loadError}]`);
}
