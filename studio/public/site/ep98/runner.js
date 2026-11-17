/*
 * runner.js: "Add my AI" on /e/98. Runs a visitor's pasted answer in the browser with
 * the same rules as video/ep98/arena/run_race.mjs (the runner of the real race).
 *
 * Where each part runs:
 *   - the page (actually-works.com) never runs the pasted code. It creates an
 *     <iframe sandbox="allow-scripts" srcdoc=...> (opaque origin, no cookies, no storage,
 *     CSP default-src 'none', so no network) and posts it the texts below;
 *   - inside that iframe, runRace() (the controller) runs the frozen physics (arena.js)
 *     and asks a Web Worker for one steer() answer per step;
 *   - the pasted code runs ONLY inside that worker (startWorker). An endless loop there
 *     blocks only the worker; the controller notices the missing reply and terminates it.
 *
 * Budgets as in run_race.mjs: 50 ms to load; steer() may use 5 ms per step on average
 * (a bank that grows 5 ms each step, starting at 50 ms) and never more than 50 ms in one
 * call. A call that never returns is cut after HANG_MS. Math.random is seeded and Date
 * shows the race clock, so a run is repeatable.
 *
 * Works in a browser (self.AW98) and in Node (module.exports) for the tests.
 */
(function (root) {
  'use strict';

  var LOAD_MS = 50, STEP_MS = 5, CALL_CAP_MS = 50;
  var HANG_MS = 1500;          // no reply this long: the call is stuck (endless loop)
  var OVERALL_MS = 45000;      // whole run, wall clock
  var MAX_TEXT = 100000;       // characters accepted from the text box

  /* ---------------- taking the code out of a reply (same order as run_race.mjs) ---------------- */
  function candidates(text) {
    var out = [], blocks = [], m;
    var fence = /```[^\n`]*\n([\s\S]*?)```/g;
    while ((m = fence.exec(text))) blocks.push(m[1]);
    blocks.forEach(function (b, i) {
      if (/\bsteer\b/.test(b)) out.push({ how: 'markdown code block ' + (i + 1) + ' of ' + blocks.length, src: b });
    });
    if (blocks.length > 1) {
      var all = blocks.join('\n');
      if (/\bsteer\b/.test(all)) out.push({ how: 'all ' + blocks.length + ' markdown code blocks joined', src: all });
    }
    out.push({ how: 'whole reply as code', src: text });
    var fi = text.search(/function\s+steer\s*\(/);
    if (fi >= 0) {
      var open = text.indexOf('{', fi), depth = 0, end = -1;
      for (var i = open; i >= 0 && i < text.length; i++) {
        if (text[i] === '{') depth++;
        else if (text[i] === '}' && --depth === 0) { end = i; break; }
      }
      if (end > 0) out.push({ how: 'brace-matched "function steer" taken out of the prose', src: text.slice(fi, end + 1) });
    }
    return out;
  }
  function stripExport(c) {
    var exp1 = /^(\s*)export\s+(default\s+)?(?=(async\s+)?function\s+steer\b|(const|let|var)\s+steer\b)/m;
    var exp2 = /^\s*export\s+(default\s+steer|\{\s*steer\s*\})\s*;?\s*$/m;
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
      Math.random = function () { // mulberry32, as in run_race.mjs
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
    var FIND = "(function(){ try { if (typeof steer === 'function') return steer; } catch (e) {}" +
      " var me = globalThis.module && globalThis.module.exports;" +
      " if (typeof me === 'function') return me;" +
      " if (me && typeof me.steer === 'function') return me.steer;" +
      " if (me && me.default && typeof me.default === 'function') return me.default;" +
      " return null; })()";
    function wrap(f) {
      return function (a, b, c, d) {
        try {
          var r = f({ front: a, left: b, right: c, speed: d });
          if (r === null || typeof r !== 'object') return 'X' + (r === null ? 'null' : typeof r);
          var t = r.turn, gg = r.gas;
          if (typeof t !== 'number' || typeof gg !== 'number') return 'Xan object with turn ' + typeof t + ' and gas ' + typeof gg;
          return 'N' + t + '|' + gg;
        } catch (e) {
          var msg;
          try { msg = (e && typeof e.message === 'string') ? e.message : String(e); } catch (e2) { msg = 'unprintable error'; }
          return 'E' + String(msg).slice(0, 200);
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
          try { f = indirectEval(FIND); } catch (e) { res = { type: 'loaded', ok: false, error: c.how + ': looking up steer failed: ' + safeMsg(e), dt: now() - t0 }; break; }
          if (typeof f !== 'function') { skipped.push(list[i].how + ': no function steer'); continue; }
          wrapped = wrap(f);
          res = { type: 'loaded', ok: true, how: c.how, dt: now() - t0 };
        }
        if (!res) res = { type: 'loaded', ok: false, error: 'no runnable function steer: ' + skipped.join('; ').slice(0, 600), dt: 0 };
        post(res);
      } else if (d.type === 'step') {
        if (!wrapped) { post({ type: 'r', r: 'Eno steer', dt: 0 }); return; }
        ms = d.ms;
        var t1 = now();
        var r = wrapped(d.a, d.b, d.c, d.e);
        post({ type: 'r', r: typeof r === 'string' ? r : 'Ewrapper replaced', dt: now() - t1 });
      }
    });
  }

  /* ---------------- controller side: physics + budgets (never runs pasted code) ---------------- */
  // Arena: arena.js API. track: track.json object. worker: { send(msg), onReply(fn), kill() }.
  // timers: { set(fn, ms) -> id, clear(id), now() }. Resolves with the car's result.
  function runRace(Arena, track, text, seed, worker, timers) {
    var T = Arena.prepareTrack(track), C = Arena.CONST;
    return new Promise(function (resolve) {
      var startedAt = timers.now(), pending = null, done = false;
      var car = Arena.initCar(T), frames = [car.x, car.y, car.angle], lapFrames = [];
      var extraction = null, loadError = null;
      var bank = CALL_CAP_MS - STEP_MS, cap = CALL_CAP_MS;
      var overall = timers.set(function () { fail('the whole run took over ' + (OVERALL_MS / 1000) + ' s'); }, OVERALL_MS);

      function r3(v) { return Math.round(v * 1000) / 1000; }
      function finish() {
        if (done) return; done = true;
        timers.clear(overall); if (pending) timers.clear(pending.timer);
        try { worker.kill(); } catch (e) { /* already gone */ }
        resolve({
          status: car.status, endFrame: car.frame, finishFrame: car.finishFrame,
          stopFrame: car.stopFrame, stopReason: car.stopReason,
          stopSector: car.status === 'finish' ? null : (car.stopSector || T.sector[Arena.nearestSample(T, car.x, car.y)]),
          progressLaps: r3(Arena.progress(T, car) / T.gates.length),
          lapFrames: lapFrames, extraction: extraction, loadError: loadError, clampedSteps: car.clamps,
          f: frames
        });
      }
      function push(next) {
        if (next.lap > car.lap) lapFrames.push(next.frame);
        car = next; frames.push(car.x, car.y, car.angle);
      }
      function stopWith(reason) { // the driver failed: one error step, as in run_race.mjs
        push(Arena.step(T, car, null, reason)); finish();
      }
      function fail(reason) { if (done) return; if (car.status === 'run') stopWith(reason); else finish(); }
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
        if (car.status !== 'run' || car.frame >= C.MAX_FRAMES) return finish();
        var s = Arena.sense(T, car);
        bank += STEP_MS;
        cap = Math.max(1, Math.min(CALL_CAP_MS, bank));
        ask({ type: 'step', a: s.front, b: s.left, c: s.right, e: s.speed, ms: Math.round((car.frame * 1000) / 60) }, HANG_MS,
          function (m) {
            var dt = typeof m.dt === 'number' && isFinite(m.dt) ? m.dt : 0, r = m.r;
            if (dt > cap) return stopWith(cap >= CALL_CAP_MS ? 'one steer() call took over ' + CALL_CAP_MS + ' ms' : 'steer() used more than ' + STEP_MS + ' ms per step on average');
            bank -= dt;
            if (bank < 0) return stopWith('steer() used more than ' + STEP_MS + ' ms per step on average');
            if (typeof r !== 'string') return stopWith('steer() wrapper was replaced');
            if (r[0] === 'E') return stopWith('steer() threw: ' + r.slice(1, 201));
            if (r[0] === 'X') return stopWith('steer() returned ' + r.slice(1, 201) + ', not { turn, gas } numbers');
            if (r[0] !== 'N') return stopWith('steer() wrapper was replaced');
            var parts = r.slice(1).split('|').map(Number), t = parts[0], g = parts[1];
            if (!isFinite(t) || !isFinite(g)) return stopWith('steer() returned turn ' + t + ', gas ' + g);
            push(Arena.step(T, car, { turn: t, gas: g }));
            if (timers.now() - startedAt > OVERALL_MS) return fail('the whole run took over ' + (OVERALL_MS / 1000) + ' s');
            next();
          },
          function () { stopWith('one steer() call took over ' + CALL_CAP_MS + ' ms'); });
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

  var API = { candidates: candidates, startWorker: startWorker, runRace: runRace,
    LIMITS: { LOAD_MS: LOAD_MS, STEP_MS: STEP_MS, CALL_CAP_MS: CALL_CAP_MS, HANG_MS: HANG_MS, OVERALL_MS: OVERALL_MS, MAX_TEXT: MAX_TEXT } };
  if (typeof module === 'object' && module && module.exports) module.exports = API;
  else root.AW98 = API;
})(typeof self !== 'undefined' ? self : this);
