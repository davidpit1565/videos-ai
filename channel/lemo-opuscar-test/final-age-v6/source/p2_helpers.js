// ---------- v6 human helpers: wobbly marker strokes, a cursor that travels on a curved wobbly path and presses, typing with a human rhythm, varied entrances ----------
const BIG = new Map();                                     // every entrance registers its start time here (rhythm audit)
const logBig = (k, t) => { if (!BIG.has(k)) BIG.set(k, t); };
// --- marker strokes: points along a hand-drawn path, drawn up to fraction u of the path length with a pen of varying width ---
function polyLen(p) { const L = [0]; for (let i = 1; i < p.length; i++) L.push(L[i - 1] + Math.hypot(p[i][0] - p[i - 1][0], p[i][1] - p[i - 1][1])); return L; }
function strokePath(p, u, col, w, seed = 1, o = {}) {
  if (u <= .002 || p.length < 2) return; const L = polyLen(p), tot = L[L.length - 1], lim = tot * clamp(u);
  g.save(); g.lineCap = 'round'; g.lineJoin = 'round'; g.strokeStyle = col; if (o.alpha) g.globalAlpha *= o.alpha; if (o.mult) g.globalCompositeOperation = 'multiply';
  for (let i = 1; i < p.length; i++) {
    if (L[i - 1] >= lim) break; const f = Math.min(1, (lim - L[i - 1]) / (L[i] - L[i - 1] || 1));
    const ex = p[i - 1][0] + (p[i][0] - p[i - 1][0]) * f, ey = p[i - 1][1] + (p[i][1] - p[i - 1][1]) * f;
    g.lineWidth = w * (.86 + .22 * nz(seed + 3, L[i] / 70)); g.beginPath(); g.moveTo(p[i - 1][0], p[i - 1][1]); g.lineTo(ex, ey); g.stroke();
  }
  g.restore();
}
function roughEllipse(cx, cy, rx, ry, seed = 1, turns = 1.12, a0 = -2.3) {   // a loop that overshoots its own start, like a real marker ring
  const n = 56, p = []; for (let i = 0; i <= n; i++) { const a = a0 + 6.2832 * turns * i / n, k = 1 + .045 * nz(seed, i * .22) + .07 * (i / n) * (rs(seed, 9) > 0 ? 1 : -1);
    p.push([cx + Math.cos(a) * rx * k + 2 * nz(seed + 1, i * .5), cy + Math.sin(a) * ry * k + 2 * nz(seed + 2, i * .5)]); } return p;
}
function roughLine(x0, y0, x1, y1, seed = 1, wob = 3.5) {
  const n = 22, dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L, p = [];
  for (let i = 0; i <= n; i++) { const u = i / n, w = wob * (nz(seed, u * 4.2) + .5 * nz(seed + 5, u * 9)); p.push([x0 + dx * u + nx * w, y0 + dy * u + ny * w]); } return p;
}
function roughRect(x, y, w, h, seed = 1, r = 22) {
  const c = [[x + r, y], [x + w - r, y], [x + w, y + r], [x + w, y + h - r], [x + w - r, y + h], [x + r, y + h], [x, y + h - r], [x, y + r], [x + r + 30, y - 2]], p = [];
  for (let i = 0; i < c.length - 1; i++) roughLine(c[i][0], c[i][1], c[i + 1][0], c[i + 1][1], seed + i, 2.6).forEach(q => p.push(q)); return p;
}
function arrowPaths(x0, y0, x1, y1, bend, seed = 1) {   // curved shaft + two head strokes; returns [shaft, head1, head2]
  const mx = (x0 + x1) / 2, my = (y0 + y1) / 2, dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy) || 1, cx = mx - dy / L * bend, cy = my + dx / L * bend, n = 24, sh = [];
  for (let i = 0; i <= n; i++) { const u = i / n, a = (1 - u) * (1 - u), b = 2 * (1 - u) * u, c = u * u; sh.push([a * x0 + b * cx + c * x1 + 2.5 * nz(seed, u * 5), a * y0 + b * cy + c * y1 + 2.5 * nz(seed + 4, u * 5)]); }
  const ang = Math.atan2(y1 - (2 * (1 - .96) * .96 * cy + .96 * .96 * y1 + (1 - .96) * (1 - .96) * y0), x1 - (2 * (1 - .96) * .96 * cx + .96 * .96 * x1 + (1 - .96) * (1 - .96) * x0)), hl = 34;
  const h1 = [[x1, y1], [x1 - Math.cos(ang - .5) * hl, y1 - Math.sin(ang - .5) * hl]], h2 = [[x1, y1], [x1 - Math.cos(ang + .5) * hl * .9, y1 - Math.sin(ang + .5) * hl * .9]];
  return [sh, h1, h2];
}
function drawArrow(t, t0, dur, x0, y0, x1, y1, bend, col, w = 8, seed = 1) {
  const u = (t - t0) / dur; if (u <= 0) return; const [sh, h1, h2] = arrowPaths(x0, y0, x1, y1, bend, seed); const k = sinIO(u * 1.25);
  strokePath(sh, clamp(k / .8), col, w, seed); strokePath(h1, sm(sg(k, .78, .93)), col, w, seed + 1); strokePath(h2, sm(sg(k, .86, 1)), col, w, seed + 2);
}
function ringMark(t, t0, dur, cx, cy, rx, ry, col, w = 9, seed = 1) { const u = (t - t0) / dur; if (u <= 0) return; strokePath(roughEllipse(cx, cy, rx, ry, seed), sinIO(u), col, w, seed); }
function underline(t, t0, dur, x0, y0, x1, col, w = 9, seed = 1) { const u = (t - t0) / dur; if (u <= 0) return; strokePath(roughLine(x0, y0, x1, y0 + 4 * rs(seed), seed, 4), p3o(u), col, w, seed); }
// --- entrances: each element gets its own kind, duration, and a seeded +-40 ms jitter. No overshoot: long power3/expo curves only. ---
function enter(t, t0, cx, cy, kind, o = {}) {
  const id = o.id ?? (cx * 3.1 + cy * 1.7 + t0 * 13), jit = rs(id, 1) * .04, dur = (o.dur ?? ({ rise: .8, drop: .85, sl: .95, sr: .95, zoom: .75, tilt: .9, fold: .85, fade: .6 })[kind]) * (.92 + .16 * hs(id, 2));
  const u = (t - t0 - jit) / dur; logBig(kind + ':' + Math.round(id * 10), t0 + jit); if (u <= 0) return false;
  const e = p3o(u), e4 = enterE(u), a = sm(u * 2.3); g.save(); g.globalAlpha *= a; g.translate(cx, cy);
  if (kind === 'rise') g.translate(0, (1 - e) * (o.rise ?? 80));
  else if (kind === 'drop') g.translate(0, -(1 - e) * 120);
  else if (kind === 'sl') g.translate(-(1 - e4) * 190, (1 - e) * 14);
  else if (kind === 'sr') g.translate((1 - e4) * 190, (1 - e) * 14);
  else if (kind === 'zoom') { const s = .86 + .14 * expoE(u); g.scale(s, s); }
  else if (kind === 'tilt') { g.rotate((o.rot ?? .1) * (1 - e)); g.translate((o.dx ?? 40) * (1 - e), (1 - e) * 50); }
  else if (kind === 'fold') { g.scale(1, .55 + .45 * enterE(u)); g.translate(0, -(1 - e) * 30); }
  g.translate(-cx, -cy); return true;
}
// --- cursor: leaves on a curved, slightly wobbly path (human, minimum-jerk-ish), hovers with micro-drift, presses with a squash ---
const hEase = u => .55 * sm(u) + .45 * p3o(u);                                    // quick start, slow careful landing
function ptrBase(t, st, segs, seed) {
  let pv = st, pos = [st.x, st.y];
  for (let i = 0; i < segs.length; i++) {
    const s = segs[i], dep = i ? segs[i - 1].tp + .12 + .1 * hs(seed, i) : st.t; if (t < dep) return pos;
    const u = clamp((t - dep) / (s.ta - dep)); const dx = s.x - pv.x, dy = s.y - pv.y, L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L;
    const bend = rs(seed, i + 20) * .16 * L + (rs(seed, i + 30) > 0 ? 1 : -1) * .06 * L, k = Math.sin(Math.PI * u), e = hEase(u), w = 7 * nz(seed + i, u * 4.3) * k;
    pos = [pv.x + dx * e + nx * (bend * k + w), pv.y + dy * e + ny * (bend * k + w)]; if (u < 1) return pos; pv = s;
  }
  return pos;
}
function pointer(t, st, segs, seed, alpha = 1, scale = 1.3) {
  if (alpha < .004) return; const p = ptrBase(t, st, segs, seed), q = ptrBase(t + .04, st, segs, seed), vx = (q[0] - p[0]) / .04, vy = (q[1] - p[1]) / .04;
  let press = 0; segs.forEach(s => { press = Math.max(press, sm(sg(t, s.tp - .09, s.tp)) * (1 - sm(sg(t, s.tp, s.tp + .2)))); });
  const x = p[0] + 2.5 * nz(seed + 70, t * 1.4), y = p[1] + 2.5 * nz(seed + 71, t * 1.3);
  g.save(); g.globalAlpha *= alpha;
  if (press > .01) { g.fillStyle = 'rgba(14,14,14,.14)'; g.beginPath(); g.arc(x + 4, y + 6, 26 + 16 * press, 0, 7); g.fill(); }   // soft finger-contact disc
  g.translate(x, y); g.rotate(-.08 + clamp(vx / 9000, -.12, .12) + .03 * nz(seed + 72, t * .9)); g.scale(scale * (1 - .13 * press), scale * (1 - .17 * press));
  g.shadowColor = 'rgba(0,0,0,.35)'; g.shadowBlur = 12 - 8 * press; g.shadowOffsetY = 7 - 5 * press;
  g.fillStyle = C.ink; g.strokeStyle = '#fff'; g.lineWidth = 3.5; g.beginPath(); g.moveTo(0, 0); g.lineTo(0, 40); g.lineTo(11, 31); g.lineTo(19, 49); g.lineTo(27, 45); g.lineTo(19, 28); g.lineTo(33, 28); g.closePath(); g.stroke(); g.fill(); g.restore();
}
function ripple(x, y, t, t0, col = C.ink) {   // soft, slightly uneven touch ring
  const u = (t - t0) / 1.0; if (u < 0 || u > 1) return; const e = p3o(u); g.save(); g.globalAlpha *= (1 - sm(u)) * .55; g.strokeStyle = col; g.lineWidth = 5 * (1 - u) + 1.5;
  g.beginPath(); for (let i = 0; i <= 28; i++) { const a = i / 28 * 6.2832, r = (16 + 62 * e) * (1 + .05 * nz(t0 * 3 + 5, a * 1.3)); i ? g.lineTo(x + Math.cos(a) * r, y + Math.sin(a) * r * .94) : g.moveTo(x + Math.cos(a) * r, y + Math.sin(a) * r * .94); } g.closePath(); g.stroke(); g.restore();
}
// --- typing with a human rhythm: bursts, pauses after spaces/punctuation, one typo that gets noticed and backspaced ---
function typePlan(str, t0, t1, seed, typo) {   // typo = {at, ch}
  const ops = []; let w = 0; const add = (g_, st) => { w += g_; ops.push([w, st]); };
  for (let i = 0; i < str.length; i++) {
    const sp = 1 + .65 * nz(seed, i * .17), c = str[i];
    if (typo && typo.at === i) { add(.7 * sp + .3, { n: i, x: typo.ch }); add(2.4, { n: i, x: typo.ch }); add(1.0, { n: i, x: '' }); add(1.5, { n: i, x: '' }); }
    add((.55 + .9 * hs(seed, i)) * sp + (c === ' ' ? .5 * hs(seed, i + 500) : 0) + (/[,.“”]/.test(c) ? .8 : 0), { n: i + 1, x: '' });
  }
  const k = (t1 - t0) / w; return ops.map(([a, st]) => ({ t: t0 + a * k, n: st.n, x: st.x }));
}
function typedAt(plan, t) { let r = { n: 0, x: '' }; if (!plan.length || t < plan[0].t) return r; let lo = 0, hi = plan.length - 1; while (lo < hi) { const m = (lo + hi + 1) >> 1; if (plan[m].t <= t) lo = m; else hi = m - 1; } return plan[lo]; }
function caret(x, y, h, t, col, seed = 3) { const a = clamp(.5 + 1.1 * nz(seed, t * 1.7)); g.save(); g.globalAlpha *= a; g.fillStyle = col; g.fillRect(x, y, 4, h); g.restore(); }
function check(cx, cy, r, p = 1, pt = 1) {   // lime disc eases in, the tick is drawn as a pen stroke (no pop)
  g.save(); g.globalAlpha *= clamp(p * 1.4); g.fillStyle = C.lime; g.beginPath(); g.arc(cx, cy, r, 0, 7); g.fill(); g.lineWidth = 3; g.strokeStyle = C.ink; g.stroke(); g.restore();
  strokePath([[cx - r * .4, cy], [cx - r * .1, cy + r * .32], [cx + r * .44, cy - r * .3]], pt, C.ink, 5.5, 8);
}
