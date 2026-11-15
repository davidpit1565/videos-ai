/*
 * arena.js: AI RACE #1 physics. Pure, deterministic functions; no I/O, no
 * randomness, no clock. Works in Node (require) and in a browser (window.Arena).
 *
 * Rules (frozen with PROMPT A, channel/episode-98-plan.md section 1):
 *   - fixed step, 60 steps per second; steer(s) is called once per step
 *   - s = { front, left, right, speed }: distance in px from the car's nose to
 *     the wall straight ahead, 45 deg left, 45 deg right (0..400, capped);
 *     speed 0..10 (px per step)
 *   - steer returns { turn, gas }: turn -1 (full left) .. 1 (full right),
 *     gas 0..1; gas under 0.2 brakes. Finite numbers outside the range are
 *     clamped (and counted); anything else stops the car ("error").
 *   - the car is 20 px wide (34 px long); touching a wall stops that car
 *   - 2 laps to finish; laps count only when every gate is passed in order
 *   - cars are ghosts to each other: each car is simulated on its own
 */
(function (root) {
  'use strict';

  var C = {
    FPS: 60,
    CAR_W: 20,
    CAR_L: 34,
    MAX_SPEED: 10,       // px per step
    SENSOR_MAX: 400,     // px
    ACCEL: 0.16,         // speed gained per step at gas 1
    ROLL: 0.02,          // speed lost per step while gas >= 0.2
    BRAKE: 0.35,         // speed lost per step while gas < 0.2
    BRAKE_BELOW: 0.2,
    MAX_YAW: 0.07,       // rad per step at full turn ...
    YAW_FULL_AT: 3,      // ... once speed >= 3 (scaled down below that)
    LAPS: 2,
    MAX_FRAMES: 3600,    // 60 s; a car still running then is "dnf"
    CONTACT_ITER: 12     // bisection steps to place a crashed car at the wall
  };

  function clamp(v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; }

  /* ---------- track preparation ---------- */
  function polyArea(p) {
    var a = 0;
    for (var i = 0, n = p.length; i < n; i++) {
      var q = p[(i + 1) % n];
      a += p[i][0] * q[1] - q[0] * p[i][1];
    }
    return a / 2;
  }

  function prepareTrack(t) {
    var L = t.leftEdge, R = t.rightEdge;
    var outer = Math.abs(polyArea(L)) > Math.abs(polyArea(R)) ? L : R;
    var inner = outer === L ? R : L;
    var walls = [];
    [L, R].forEach(function (p) {
      for (var i = 0, n = p.length; i < n; i++) {
        var a = p[i], b = p[(i + 1) % n];
        walls.push([a[0], a[1], b[0], b[1]]);
      }
    });
    var gates = [];
    for (var i = 0; i < L.length; i++) gates.push([L[i][0], L[i][1], R[i][0], R[i][1]]);
    return {
      raw: t, outer: outer, inner: inner, walls: walls, gates: gates,
      sector: t.sector, laps: t.laps || C.LAPS, start: t.start
    };
  }

  /* ---------- geometry ---------- */
  function pointInPoly(x, y, p) {
    var inside = false;
    for (var i = 0, j = p.length - 1; i < p.length; j = i++) {
      var xi = p[i][0], yi = p[i][1], xj = p[j][0], yj = p[j][1];
      if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) inside = !inside;
    }
    return inside;
  }
  function onRoad(T, x, y) { return pointInPoly(x, y, T.outer) && !pointInPoly(x, y, T.inner); }

  // segment p1-p2 vs segment p3-p4 (proper or touching)
  function segHit(x1, y1, x2, y2, x3, y3, x4, y4) {
    var d = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3);
    if (d === 0) return false;
    var u = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / d;
    var v = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / d;
    return u >= 0 && u <= 1 && v >= 0 && v <= 1;
  }

  function corners(x, y, a) {
    var c = Math.cos(a), s = Math.sin(a), hl = C.CAR_L / 2, hw = C.CAR_W / 2;
    // front-left, front-right, back-right, back-left (left = -90 deg on screen)
    return [
      [x + c * hl + s * hw, y + s * hl - c * hw],
      [x + c * hl - s * hw, y + s * hl + c * hw],
      [x - c * hl - s * hw, y - s * hl + c * hw],
      [x - c * hl + s * hw, y - s * hl - c * hw]
    ];
  }

  function touchesWall(T, x, y, a) {
    var k = corners(x, y, a), i, w;
    for (i = 0; i < 4; i++) if (!onRoad(T, k[i][0], k[i][1])) return true;
    var minx = Math.min(k[0][0], k[1][0], k[2][0], k[3][0]), maxx = Math.max(k[0][0], k[1][0], k[2][0], k[3][0]);
    var miny = Math.min(k[0][1], k[1][1], k[2][1], k[3][1]), maxy = Math.max(k[0][1], k[1][1], k[2][1], k[3][1]);
    for (var j = 0; j < T.walls.length; j++) {
      w = T.walls[j];
      if (Math.max(w[0], w[2]) < minx || Math.min(w[0], w[2]) > maxx || Math.max(w[1], w[3]) < miny || Math.min(w[1], w[3]) > maxy) continue;
      for (i = 0; i < 4; i++) {
        var p = k[i], q = k[(i + 1) % 4];
        if (segHit(p[0], p[1], q[0], q[1], w[0], w[1], w[2], w[3])) return true;
      }
    }
    return false;
  }

  // distance along a ray to the nearest wall, capped at SENSOR_MAX
  function ray(T, x, y, a) {
    var dx = Math.cos(a), dy = Math.sin(a), best = C.SENSOR_MAX;
    for (var j = 0; j < T.walls.length; j++) {
      var w = T.walls[j];
      var ex = w[2] - w[0], ey = w[3] - w[1];
      var d = dx * ey - dy * ex;
      if (d === 0) continue;
      var t = ((w[0] - x) * ey - (w[1] - y) * ex) / d;   // along the ray
      var u = ((w[0] - x) * dy - (w[1] - y) * dx) / d;   // along the wall
      if (t >= 0 && u >= 0 && u <= 1 && t < best) best = t;
    }
    return best;
  }

  /* ---------- car ---------- */
  function initCar(T) {
    return {
      frame: 0, x: T.start.x, y: T.start.y, angle: T.start.angle, speed: 0,
      lap: 0, nextGate: 1, status: 'run', finishFrame: null, stopFrame: null,
      stopReason: null, clamps: 0
    };
  }

  function sense(T, car) {
    var hl = C.CAR_L / 2;
    var nx = car.x + Math.cos(car.angle) * hl, ny = car.y + Math.sin(car.angle) * hl;
    return {
      front: ray(T, nx, ny, car.angle),
      left: ray(T, nx, ny, car.angle - Math.PI / 4),
      right: ray(T, nx, ny, car.angle + Math.PI / 4),
      speed: car.speed
    };
  }

  function copy(car) { var o = {}; for (var k in car) o[k] = car[k]; return o; }

  /*
   * One fixed step. cmd is { turn, gas } (any values) or null when the driver
   * failed (threw, timed out, returned something that is not two numbers).
   * Returns a NEW car object; the input is not changed.
   */
  function step(T, car, cmd, reasonIfNull) {
    var c = copy(car);
    c.frame = car.frame + 1;
    if (car.status !== 'run') return c;
    if (!cmd || typeof cmd.turn !== 'number' || typeof cmd.gas !== 'number' || !isFinite(cmd.turn) || !isFinite(cmd.gas)) {
      c.status = 'error'; c.speed = 0; c.stopFrame = c.frame;
      c.stopReason = reasonIfNull || 'steer() did not return { turn, gas } as numbers';
      return c;
    }
    var turn = cmd.turn, gas = cmd.gas;
    if (turn < -1 || turn > 1 || gas < 0 || gas > 1) c.clamps = car.clamps + 1;
    turn = clamp(turn, -1, 1); gas = clamp(gas, 0, 1);

    var v = car.speed;
    if (gas < C.BRAKE_BELOW) v = Math.max(0, v - C.BRAKE);
    else v = clamp(v + C.ACCEL * gas - C.ROLL, 0, C.MAX_SPEED);
    var yaw = turn * C.MAX_YAW * Math.min(1, v / C.YAW_FULL_AT);
    var a1 = car.angle + yaw;
    var x1 = car.x + Math.cos(a1) * v, y1 = car.y + Math.sin(a1) * v;

    if (touchesWall(T, x1, y1, a1)) {
      // place the car at the last free point along this step (bisection)
      var lo = 0, hi = 1;
      for (var i = 0; i < C.CONTACT_ITER; i++) {
        var m = (lo + hi) / 2;
        if (touchesWall(T, car.x + (x1 - car.x) * m, car.y + (y1 - car.y) * m, car.angle + yaw * m)) hi = m; else lo = m;
      }
      c.x = car.x + (x1 - car.x) * lo; c.y = car.y + (y1 - car.y) * lo; c.angle = car.angle + yaw * lo;
      c.speed = 0; c.status = 'wall'; c.stopFrame = c.frame; c.stopReason = 'touched the wall';
      c.stopSector = T.sector[nearestSample(T, c.x, c.y)];
      return c;
    }

    // gate crossing (only the next gate counts; gate 0 is the finish line)
    // gates are 6 px apart and a car moves up to 10 px, so one step may pass several
    for (var gi = 0; gi < 4 && c.status === 'run'; gi++) {
      var g = T.gates[c.nextGate];
      if (!segHit(car.x, car.y, x1, y1, g[0], g[1], g[2], g[3])) break;
      if (c.nextGate === 0) {
        c.lap = c.lap + 1;
        if (c.lap >= T.laps) { c.status = 'finish'; c.finishFrame = c.frame; }
      }
      c.nextGate = (c.nextGate + 1) % T.gates.length;
    }
    c.x = x1; c.y = y1; c.angle = a1; c.speed = v;
    if (c.status === 'run' && c.frame >= C.MAX_FRAMES) { c.status = 'dnf'; c.stopFrame = c.frame; c.stopReason = 'still running at the time limit'; }
    return c;
  }

  function nearestSample(T, x, y) {
    var cl = T.raw.centerline, best = 0, bd = Infinity;
    for (var i = 0; i < cl.length; i++) {
      var d = (cl[i][0] - x) * (cl[i][0] - x) + (cl[i][1] - y) * (cl[i][1] - y);
      if (d < bd) { bd = d; best = i; }
    }
    return best;
  }

  // progress along the circuit in gates passed (car starts on gate 0, the finish line) (for ordering cars that did not finish)
  function progress(T, car) {
    return car.lap * T.gates.length + (car.nextGate - 1 + T.gates.length) % T.gates.length;
  }

  /*
   * Run one car to the end. driver(s, car) returns { cmd, reason } where cmd is
   * { turn, gas } or null. Returns the list of states (frame 0 .. end).
   */
  function simulate(T, driver) {
    var car = initCar(T), states = [car];
    while (car.status === 'run' && car.frame < C.MAX_FRAMES) {
      var s = sense(T, car);
      var out = driver(s, car) || {};
      car = step(T, car, out.cmd || null, out.reason);
      states.push(car);
    }
    return states;
  }

  var API = {
    CONST: C, prepareTrack: prepareTrack, initCar: initCar, sense: sense, step: step,
    simulate: simulate, progress: progress, onRoad: onRoad, touchesWall: touchesWall,
    nearestSample: nearestSample
  };
  if (typeof module === 'object' && module.exports) module.exports = API;
  else root.Arena = API;
})(typeof self !== 'undefined' ? self : this);
