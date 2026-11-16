/*
 * maze.js: AI RACE #2 maze rules. Pure, deterministic functions; no I/O, no
 * randomness, no clock, no Node-only APIs. Works in Node (require) and in a
 * browser (window.Maze), so the /e/99 page can run pasted code with the same rules.
 *
 * Rules (frozen with PROMPT-B.txt):
 *   - the maze is 21 x 21 cells; x = 0..20 left to right, y = 0..20 top to bottom
 *   - the dot starts at the centre cell (10, 10); the exit is one gap in the outer wall
 *   - move(v) is called once per step with a fresh
 *       v = { up, down, left, right, x, y }
 *     each direction is "wall", "open" or "exit" ("exit" = that move leaves the maze);
 *     x, y = the dot's own cell. up = y - 1, down = y + 1, left = x - 1, right = x + 1
 *   - move returns "up", "down", "left" or "right" (exactly these strings)
 *   - any other return value, or a move into a wall, = the dot stays where it is
 *     for that step (counted, the run goes on)
 *   - 500 steps at most. Score = steps to get out (fewer is better); a dot that is
 *     still inside after 500 steps did not finish (dnf), ranked by the closest it
 *     came to the exit (shortest walking distance, in steps)
 *   - code may keep its own memory between calls (global variables)
 */
(function (root) {
  'use strict';

  var C = {
    MAX_STEPS: 500,
    // bits in maze.json "open": 1 = up, 2 = right, 4 = down, 8 = left
    BIT: { up: 1, right: 2, down: 4, left: 8 },
    DX: { up: 0, right: 1, down: 0, left: -1 },
    DY: { up: -1, right: 0, down: 1, left: 0 },
    DIRS: ['up', 'down', 'left', 'right']
  };

  function prepareMaze(m) {
    var W = m.width, H = m.height, open = [], x, y;
    for (y = 0; y < H; y++) {
      var row = [];
      for (x = 0; x < W; x++) row.push(parseInt(m.open[y].charAt(x), 16));
      open.push(row);
    }
    // walking distance to get OUT (exit cell = 1, outside = 0), BFS from the exit
    var dist = [];
    for (y = 0; y < H; y++) { dist.push([]); for (x = 0; x < W; x++) dist[y].push(-1); }
    var q = [[m.exit.x, m.exit.y]];
    dist[m.exit.y][m.exit.x] = 1;
    while (q.length) {
      var c = q.shift();
      for (var i = 0; i < 4; i++) {
        var d = C.DIRS[i];
        if (!(open[c[1]][c[0]] & C.BIT[d])) continue;
        var nx = c[0] + C.DX[d], ny = c[1] + C.DY[d];
        if (nx < 0 || ny < 0 || nx >= W || ny >= H) continue;
        if (dist[ny][nx] < 0) { dist[ny][nx] = dist[c[1]][c[0]] + 1; q.push([nx, ny]); }
      }
    }
    return { raw: m, W: W, H: H, open: open, dist: dist, start: m.start, exit: m.exit };
  }

  function inside(M, x, y) { return x >= 0 && y >= 0 && x < M.W && y < M.H; }

  // what the dot sees in one direction from cell (x, y)
  function look(M, x, y, d) {
    if (!(M.open[y][x] & C.BIT[d])) return 'wall';
    return inside(M, x + C.DX[d], y + C.DY[d]) ? 'open' : 'exit';
  }

  function view(M, bot) {
    return {
      up: look(M, bot.x, bot.y, 'up'), down: look(M, bot.x, bot.y, 'down'),
      left: look(M, bot.x, bot.y, 'left'), right: look(M, bot.x, bot.y, 'right'),
      x: bot.x, y: bot.y
    };
  }

  function initBot(M) {
    var d = M.dist[M.start.y][M.start.x];
    return {
      step: 0, x: M.start.x, y: M.start.y, status: 'run',
      invalid: 0, bumps: 0, firstInvalid: null,
      closest: d, closestAt: [M.start.x, M.start.y], closestStep: 0,
      stopReason: null
    };
  }

  function copy(b) { var o = {}; for (var k in b) o[k] = b[k]; return o; }

  /*
   * One step. dir is what move() returned (any value), or undefined with
   * `why` set when the call failed (threw, returned a non-string). A call that
   * runs over the time budget is NOT a step: the runner calls stop() instead.
   * Returns a NEW bot; the input is not changed.
   */
  function step(M, bot, dir, why) {
    var b = copy(bot);
    if (bot.status !== 'run') return b;
    b.step = bot.step + 1;
    if (dir !== 'up' && dir !== 'down' && dir !== 'left' && dir !== 'right') {
      b.invalid = bot.invalid + 1;
      if (b.firstInvalid == null) b.firstInvalid = 'step ' + b.step + ': ' + (why || describe(dir));
    } else {
      var seen = look(M, bot.x, bot.y, dir);
      if (seen === 'wall') b.bumps = bot.bumps + 1;
      else if (seen === 'exit') {
        b.x = bot.x + C.DX[dir]; b.y = bot.y + C.DY[dir]; // one cell outside the grid
        b.status = 'exit'; b.closest = 0; b.closestAt = [b.x, b.y]; b.closestStep = b.step;
        return b;
      } else {
        b.x = bot.x + C.DX[dir]; b.y = bot.y + C.DY[dir];
        var d = M.dist[b.y][b.x];
        if (d < b.closest) { b.closest = d; b.closestAt = [b.x, b.y]; b.closestStep = b.step; }
      }
    }
    if (b.step >= C.MAX_STEPS) { b.status = 'dnf'; b.stopReason = 'still inside after ' + C.MAX_STEPS + ' steps'; }
    return b;
  }

  // the run ends early (only for a time-budget overrun or a crashed sandbox)
  function stop(bot, reason) {
    var b = copy(bot);
    if (b.status === 'run') { b.status = 'error'; b.stopReason = reason; }
    return b;
  }

  function describe(v) {
    if (typeof v === 'string') return 'returned "' + v.slice(0, 40) + '"';
    if (v === null) return 'returned null';
    return 'returned ' + typeof v;
  }

  /*
   * Run one bot to the end (for the browser page). driver(v, bot) returns
   * { dir, why } or { stop: reason }. Returns the list of bot states (step 0 .. end).
   */
  function simulate(M, driver) {
    var bot = initBot(M), states = [bot];
    while (bot.status === 'run') {
      var out = driver(view(M, bot), bot) || {};
      bot = out.stop ? stop(bot, out.stop) : step(M, bot, out.dir, out.why);
      states.push(bot);
      if (out.stop) break;
    }
    return states;
  }

  var API = {
    CONST: C, prepareMaze: prepareMaze, initBot: initBot, view: view, look: look,
    step: step, stop: stop, simulate: simulate
  };
  if (typeof module === 'object' && module.exports) module.exports = API;
  else root.Maze = API;
})(typeof self !== 'undefined' ? self : this);
