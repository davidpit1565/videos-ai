/*
 * runner.js: "Add my AI" on /e/99. Runs a visitor's pasted answer in the browser with
 * the same rules as video/ep99/arena/run_maze.mjs (the runner of the real maze race).
 * Same design as /e/98 (public/site/ep98/runner.js):
 *   - the page (actually-works.com) never runs the pasted code. It creates an
 *     <iframe sandbox="allow-scripts" srcdoc=...> (opaque origin, no cookies, no storage,
 *     CSP default-src 'none', so no network) and posts it the texts below;
 *   - inside that iframe, runMaze() (the controller) runs the frozen rules (maze.js)
 *     and asks a Web Worker for one move() answer per step;
 *   - the pasted code runs ONLY in that worker (startWorker). An endless loop there
 *     blocks only the worker; the controller notices the missing reply and terminates it.
 *
 * Budgets as in run_maze.mjs: 50 ms to load; move() may use 5 ms per step on average
 * (a bank that grows 5 ms each step, starting at 50 ms) and never more than 50 ms in one
 * call. A call that never returns is cut after HANG_MS. A throw or a return value that is
 * not one of the four direction strings is NOT the end: the dot stays for that step.
 * Math.random is seeded; Date.now() is 1 second per step. Works in a browser (self.AWM99)
 * and in Node (module.exports) for the tests.
 */
(function (root) {
  'use strict';

  var LOAD_MS = 50, STEP_MS = 5, CALL_CAP_MS = 50;
  var HANG_MS = 1500;          // no reply this long: the call is stuck (endless loop)
  var OVERALL_MS = 45000;      // whole run, wall clock
  var MAX_TEXT = 100000;       // characters accepted from the text box

  /* ---------------- taking the code out of a reply (same order as run_maze.mjs) ---------------- */
  function candidates(text) {
    var out = [], blocks = [], m;
    var fence = /```[^\n`]*\n([\s\S]*?)```/g;
    while ((m = fence.exec(text))) blocks.push(m[1]);
    blocks.forEach(function (b, i) {
      if (/\bmove\b/.test(b)) out.push({ how: 'markdown code block ' + (i + 1) + ' of ' + blocks.length, src: b });
    });
    if (blocks.length > 1) {
      var all = blocks.join('\n');
      if (/\bmove\b/.test(all)) out.push({ how: 'all ' + blocks.length + ' markdown code blocks joined', src: all });
    }
    out.push({ how: 'whole reply as code', src: text });
    var fi = text.search(/function\s+move\s*\(/);
    if (fi >= 0) {
      var open = text.indexOf('{', fi), depth = 0, end = -1;
      for (var i = open; i >= 0 && i < text.length; i++) {
        if (text[i] === '{') depth++;
        else if (text[i] === '}' && --depth === 0) { end = i; break; }
      }
      if (end > 0) out.push({ how: 'brace-matched "function move" taken out of the prose', src: text.slice(fi, end + 1) });
    }
    return out;
  }
  function stripExport(c) {
    var exp1 = /^(\s*)export\s+(default\s+)?(?=(async\s+)?function\s+move\b|(const|let|var)\s+move\b)/m;
    var exp2 = /^\s*export\s+(default\s+move|\{\s*move\s*\})\s*;?\s*$/m;
    if (exp1.test(c.src) || exp2.test(c.src)) {
      return { how: c.how + ' (removed "export")', src: c.src.replace(exp1, '$1').replace(exp2, '') };
    }
    return c;
  }

  /* ---------------- worker side: the ONLY place the pasted code runs ---------------- */
  // g: the worker global. post(msg): reply to the controller. listen(fn): get messages.
  function startWorker(g, post, listen, now) {
    post = post || g.postMessage.bind(g);
    now = now || (g.performance && g.performance.now ? g.performance.now.bind(g.performance) : Date.now);
    listen = listen || function (fn) { g.addEventListener('message', function (e) { fn(e.data); }); };
    var indirectEval = (0, eval);
    var ms = 0, wrapped = null;

    function safeMsg(e) {
      try { return (e && typeof e.message === 'string') ? String(e.message).slice(0, 200) : String(e).slice(0, 200); }
      catch (e2) { return 'error'; }
    }
    function boot(seed) {
      var s = seed >>> 0;
      Math.random = function () { // mulberry32, as in run_maze.mjs
        s = (s + 0x6D2B79F5) >>> 0; var t = s;
        t = Math.imul(t ^ (t >>> 15), t | 1);
        t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
      };
      var RealDate = Date;
      function FixedDate() {
        var a = Array.prototype.slice.call(arguments);
        var d = a.length ? new (Function.prototype.bind.apply(RealDate, [null].concat(a)))() : new RealDate(ms);
        return new.target ? d : d.toString();
      }
      FixedDate.prototype = RealDate.prototype;
      FixedDate.now = function () { return ms; };
      FixedDate.UTC = RealDate.UTC; FixedDate.parse = RealDate.parse;
      g.Date = FixedDate;
      var noop = function () {};
      g.console = { log: noop, info: noop, warn: noop, error: noop, debug: noop, table: noop };
      g.module = { exports: {} }; g.exports = g.module.exports;
      // nothing that reaches out or waits. The real network block is the iframe's CSP
      // (inherited by this blob worker); this is a second layer and matches Node's sandbox.
      ['fetch', 'XMLHttpRequest', 'WebSocket', 'WebSocketStream', 'EventSource', 'importScripts',
       'indexedDB', 'caches', 'BroadcastChannel', 'Worker', 'SharedWorker', 'WebTransport',
       'Request', 'Response', 'Headers', 'navigator', 'location',
       'setTimeout', 'setInterval', 'clearTimeout', 'clearInterval', 'setImmediate',
       'WebAssembly', 'SharedArrayBuffer', 'Atomics', 'require', 'process', 'Buffer'].forEach(function (k) {
        try { delete g[k]; } catch (e) { /* not configurable */ }
        try { if (k in g) Object.defineProperty(g, k, { value: undefined, writable: false, configurable: false }); } catch (e) { /* ignore */ }
        // the browser keeps some of these on WorkerGlobalScope.prototype as well
        for (var p = Object.getPrototypeOf(g); p && p !== Object.prototype; p = Object.getPrototypeOf(p)) {
          try { if (Object.prototype.hasOwnProperty.call(p, k)) delete p[k]; } catch (e) { /* ignore */ }
        }
      });
    }
    var FIND = "(function(){ try { if (typeof move === 'function') return move; } catch (e) {}" +
      " var me = globalThis.module && globalThis.module.exports;" +
      " if (typeof me === 'function') return me;" +
      " if (me && typeof me.move === 'function') return me.move;" +
      " if (me && me.default && typeof me.default === 'function') return me.default;" +
      " return null; })()";
    // v is built here, fresh each call; the answer comes back as a plain string, as in run_maze.mjs
    function wrap(f) {
      return function (u, d, l, r, x, y) {
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
      };
    }

    listen(function (d) {
      if (!d || typeof d !== 'object') return;
      if (d.type === 'load') {
        boot(d.seed);
        var text = String(d.text).slice(0, MAX_TEXT), skipped = [], res = null;
        var list = candidates(text);
        for (var i = 0; i < list.length && !res; i++) {
          var c = stripExport(list[i]);
          try { new Function(c.src); } catch (e) { skipped.push(list[i].how + ': not valid JavaScript (' + safeMsg(e) + ')'); continue; }
          var t0 = now();
          try { indirectEval(c.src); }
          catch (e) { res = { type: 'loaded', ok: false, error: c.how + ': threw while loading: ' + safeMsg(e), dt: now() - t0 }; break; }
          var f = null;
          try { f = indirectEval(FIND); } catch (e) { res = { type: 'loaded', ok: false, error: c.how + ': looking up move failed: ' + safeMsg(e), dt: now() - t0 }; break; }
          if (typeof f !== 'function') { skipped.push(list[i].how + ': no function move'); continue; }
          wrapped = wrap(f);
          res = { type: 'loaded', ok: true, how: c.how, dt: now() - t0 };
        }
        if (!res) res = { type: 'loaded', ok: false, error: 'no runnable function move: ' + skipped.join('; ').slice(0, 600), dt: 0 };
        post(res);
      } else if (d.type === 'step') {
        if (!wrapped) { post({ type: 'r', r: 'Eno move', dt: 0 }); return; }
        ms = d.ms;
        var t1 = now();
        var r = wrapped(d.u, d.d, d.l, d.r, d.x, d.y);
        post({ type: 'r', r: typeof r === 'string' ? r : 'Ewrapper replaced', dt: now() - t1 });
      }
    });
  }

  /* ---------------- controller side: rules + budgets (never runs pasted code) ---------------- */
  // Maze: maze.js API. mazeJson: maze.json object. worker: { send(msg), onReply(fn), kill() }.
  // timers: { set(fn, ms) -> id, clear(id), now() }. Resolves with the dot's result.
  function runMaze(Maze, mazeJson, text, seed, worker, timers) {
    var M = Maze.prepareMaze(mazeJson), C = Maze.CONST;
    return new Promise(function (resolve) {
      var startedAt = timers.now(), pending = null, done = false;
      var bot = Maze.initBot(M), path = [bot.x, bot.y];
      var extraction = null, loadError = null;
      var bank = CALL_CAP_MS - STEP_MS, cap = CALL_CAP_MS;
      var overall = timers.set(function () { fail('the whole run took over ' + (OVERALL_MS / 1000) + ' s'); }, OVERALL_MS);

      function finish() {
        if (done) return; done = true;
        timers.clear(overall); if (pending) timers.clear(pending.timer);
        try { worker.kill(); } catch (e) { /* already gone */ }
        var seen = {}, n = 0;
        for (var i = 0; i < path.length; i += 2) { var k = path[i] + ',' + path[i + 1]; if (!seen[k]) { seen[k] = 1; n++; } }
        resolve({
          status: bot.status, steps: bot.step, exitStep: bot.status === 'exit' ? bot.step : null,
          closestDist: bot.closest, closestAt: bot.closestAt, closestStep: bot.closestStep,
          end: [bot.x, bot.y], invalidSteps: bot.invalid, wallBumps: bot.bumps, firstInvalid: bot.firstInvalid,
          stopReason: bot.stopReason, cellsVisited: n, extraction: extraction, loadError: loadError,
          p: path
        });
      }
      function push(next) { bot = next; path.push(bot.x, bot.y); }
      function stopWith(reason) { bot = Maze.stop(bot, reason); finish(); }
      function fail(reason) { if (done) return; stopWith(reason); }
      function ask(msg, limitMs, onReply, onHang) {
        pending = { onReply: onReply, timer: timers.set(function () { pending = null; try { worker.kill(); } catch (e) { /* */ } onHang(); }, limitMs) };
        worker.send(msg);
      }
      worker.onReply(function (m) {
        if (done || !pending || !m || typeof m !== 'object') return;
        var p = pending; pending = null; timers.clear(p.timer); p.onReply(m);
      });

      function next() {
        if (done) return;
        if (bot.status !== 'run') return finish();
        var v = Maze.view(M, bot);
        bank += STEP_MS;
        cap = Math.max(1, Math.min(CALL_CAP_MS, bank));
        ask({ type: 'step', u: v.up, d: v.down, l: v.left, r: v.right, x: v.x, y: v.y, ms: bot.step * 1000 }, HANG_MS,
          function (m) {
            var dt = typeof m.dt === 'number' && isFinite(m.dt) ? m.dt : 0, r = m.r;
            if (dt > cap) return stopWith(cap >= CALL_CAP_MS ? 'one move() call took over ' + CALL_CAP_MS + ' ms' : 'move() used more than ' + STEP_MS + ' ms per step on average');
            bank -= dt;
            if (bank < 0) return stopWith('move() used more than ' + STEP_MS + ' ms per step on average');
            if (typeof r !== 'string' || !/^[NXE]/.test(r)) return stopWith('move() wrapper was replaced');
            push(r[0] === 'N' ? Maze.step(M, bot, r.slice(1)) : Maze.step(M, bot, undefined, r.slice(1, 201)));
            if (timers.now() - startedAt > OVERALL_MS) return fail('the whole run took over ' + (OVERALL_MS / 1000) + ' s');
            next();
          },
          function () { stopWith('one move() call took over ' + CALL_CAP_MS + ' ms'); });
      }

      ask({ type: 'load', text: String(text).slice(0, MAX_TEXT), seed: seed }, HANG_MS,
        function (m) {
          if (m.type !== 'loaded') { loadError = 'unexpected reply while loading'; return stopWith('did not start: ' + loadError); }
          var dt = typeof m.dt === 'number' && isFinite(m.dt) ? m.dt : 0;
          if (!m.ok) { loadError = String(m.error).slice(0, 800); return stopWith('did not start: ' + loadError); }
          if (dt > LOAD_MS) { loadError = String(m.how) + ': loading took over ' + LOAD_MS + ' ms'; return stopWith('did not start: ' + loadError); }
          extraction = String(m.how).slice(0, 200);
          next();
        },
        function () { loadError = 'loading took over ' + LOAD_MS + ' ms'; stopWith('did not start: ' + loadError); });
    });
  }

  var API = { candidates: candidates, startWorker: startWorker, runMaze: runMaze,
    LIMITS: { LOAD_MS: LOAD_MS, STEP_MS: STEP_MS, CALL_CAP_MS: CALL_CAP_MS, HANG_MS: HANG_MS, OVERALL_MS: OVERALL_MS, MAX_TEXT: MAX_TEXT } };
  if (typeof module === 'object' && module && module.exports) module.exports = API;
  else root.AWM99 = API;
})(typeof self !== 'undefined' ? self : this);
