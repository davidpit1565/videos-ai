// ChatGPT age film, v6 (organic build). Canvas 2D, pure function of t. ALL timing comes from voices/cues.json + voices/words.json (align.py) and the voice amplitude from voices/env.json (env.py).
// v6 rules: no constant-speed loop, no periodic sine sway (every ambient motion = smooth value noise with its own seed/frequency), no overshoot bounce, only power3/power4/expo/sine-in-out/smootherstep curves.
const W = 1080, H = 1920;
const cv = document.getElementById('c'); let g = cv.getContext('2d');
await Promise.all([700, 800, 900, 600, 500].flatMap(w => [`${w} 40px Inter`, `${w} 40px InterTight`, `${w} 40px JBMono`]).map(f => document.fonts.load(f)));
const get = async (u, d) => { try { const r = await fetch(u); return r.ok ? await r.json() : d; } catch { return d; } };
const SCRIPT = await get('script.json', {});
const TOK = Object.fromEntries(Object.entries(SCRIPT).map(([k, v]) => [k, v.split(/\s+/)]));
const WD = await get('voices/words.json', {});
const DJ = await get('voices/dur.json', {});
const META = await get('voices/meta.json', {});
const ENVD = await get('voices/env.json', []);
const IMG = async u => createImageBitmap(await (await fetch(u)).blob());
const TR = await IMG('tr.png'), TC = await IMG('tc.png'), TB = await IMG('trb.png');
const svg = await (await fetch('chatgpt.svg')).text();
const MARK = new Path2D(svg.match(/ d='([^']+)'/)[1]);
const C = { paper: '#F4F4EF', dot: '#DADACE', ink: '#0E0E0E', ink2: '#4B4B46', dark: '#14151A', dark2: '#22242C', dark3: '#2E3039', lime: '#B6F23A', limeDeep: '#4E8F0B', wash: '#E4F8B0', white: '#FFFFFF', mute: '#8E908A' };
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const sg = (t, a, b) => clamp((t - a) / (b - a));
// ---- easing: smootherstep, power3/power4 out, expo out, sine in-out, power3 in-out. NO back/elastic. ----
const sm = x => { x = clamp(x); return x * x * x * (x * (x * 6 - 15) + 10); };
const p3o = x => 1 - Math.pow(1 - clamp(x), 3);
const enterE = x => 1 - Math.pow(1 - clamp(x), 4);
const expoE = x => { x = clamp(x); return x >= 1 ? 1 : 1 - Math.pow(2, -10 * x); };
const ioE = x => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const sinIO = x => -(Math.cos(Math.PI * clamp(x)) - 1) / 2;
const bell = (t, a, b, c) => sm(sg(t, a, b)) * (1 - sm(sg(t, b, c)));        // smooth rise a->b, smooth fall b->c
const lerp = (a, b, t) => a + (b - a) * t;
const rng = s => () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
// ---- smooth value noise (C2): nz(seed, x) in about [-1,1]; every moving thing gets its own seed and frequency ----
const hash = n => { n = Math.imul(n ^ n >>> 15, 0x2c1b3c6d); n = Math.imul(n ^ n >>> 12, 0x297a2d39); return ((n ^ n >>> 15) >>> 0) / 4294967296; };
const hs = (k, a = 0) => hash((Math.floor(k * 97) + Math.imul(a + 1, 7919)) | 0);            // seeded 0..1 from any number
const rs = (k, a = 0) => hs(k, a) * 2 - 1;                                                    // seeded -1..1
const lat = (s, i) => hash((i * 374761393 + Math.floor(s * 1000) * 668265263) | 0) * 2 - 1;
const nz = (s, x) => { const i = Math.floor(x), f = x - i, u = f * f * f * (f * (f * 6 - 15) + 10); return lat(s, i) * (1 - u) + lat(s, i + 1) * u; };
const fbm = (s, x) => nz(s, x) * .62 + nz(s + 7.3, x * 2.17) * .28 + nz(s + 13.1, x * 4.3) * .1;
// ---- voice amplitude (100 Hz, already smoothed ~80 ms): ENV(t, lag) 0..~1, eased ----
const envAt = t => { const x = t * 100, i = Math.floor(x); if (i < 0 || i >= ENVD.length - 1) return 0; return lerp(ENVD[i], ENVD[i + 1], x - i); };
let NOW = 0;
const V = (lag = 0) => { const e = clamp(envAt(NOW - lag), 0, 1); return e * e * (3 - 2 * e); };
// ---- timing: line starts (T), per-word starts (wt) ----
const T = Object.assign({ l1: .08, l2: 3.57, l3: 7.55, l4: 10.42, l5: 13.95, l6: 17.01, l7: 21.45, l8: 25.14, l9: 27.8 }, await get('voices/cues.json', {}));
const WDC = {};
function wordsOf(l) {
  const toks = TOK[l], w = WD[l];
  if (w && w.length === toks.length) return w;
  const d = (DJ[l] ?? 2.6) * .96, n = s => s.replace(/[^a-z0-9']/gi, '').length + 1.1, tot = toks.reduce((a, s) => a + n(s), 0); let a = 0;
  return toks.map(s => { const r = [s, a / tot * d, (a + n(s) - 1.1) / tot * d]; a += n(s); return r; });
}
const wt = (l, i) => T[l] + Math.max(0, (WDC[l] ??= wordsOf(l))[i][1]);   // spoken start of word i of line l
const we = (l, i) => T[l] + Math.max(0, (WDC[l] ??= wordsOf(l))[i][2]);   // spoken end
const lineEnd = n => T['l' + n] + (DJ['l' + n] ?? 2.6);
const DUR = META.dur ?? 33.3; window.DUR = DUR;
const TXT = []; let REC = false;
function reg(id, text, x0, y0, x1, y1) {
  if (!REC || g.globalAlpha < .5) return;
  const m = g.getTransform(), p = (x, y) => [m.a * x + m.c * y + m.e, m.b * x + m.d * y + m.f];
  const a = p(x0, y0), b = p(x1, y1);
  TXT.push({ id, text, x0: Math.min(a[0], b[0]), y0: Math.min(a[1], b[1]), x1: Math.max(a[0], b[0]), y1: Math.max(a[1], b[1]) });
}
const F = (px, wt, fam) => `${wt} ${px}px ${fam}`;
function tx(s, x, y, px, w, fam, col, al = 'left', id) {
  g.font = F(px, w, fam); g.fillStyle = col; g.textAlign = al; g.textBaseline = 'alphabetic'; g.fillText(s, x, y);
  const wd = g.measureText(s).width, x0 = al === 'center' ? x - wd / 2 : al === 'right' ? x - wd : x;
  reg(id || s, s, x0, y - px * .78, x0 + wd, y + px * .2); return wd;
}
const rr = (x, y, w, h, r) => { w = Math.max(0, w); h = Math.max(0, h); g.beginPath(); g.roundRect(x, y, w, h, Math.max(0, Math.min(r, w / 2, h / 2))); };
// ambient float: smooth noise, its own seed + time scale per call site (per = seconds per wander)
const fl = (t, ph, amp = 5, per = 5) => amp * 1.7 * nz(ph * 3.17 + per * 1.31 + 40, t / per + ph * 5.3);
// ---------- sticker components (ep 82 DNA: thick outline, hard offset shadow) with per-element tilt/offset/shadow/breath ----------
function sticker(x, y, w, h, r, fill, o = {}, fn) {
  const seed = o.seed ?? (x * .37 + y * .71 + w * .13 + h * .29);
  const rot = (o.rot ?? rs(seed, 1) * (o.ra ?? .05)) + .004 * nz(seed, NOW * .31);                 // random static tilt (+-3 deg) + a hair of noise
  const jx = o.jx ?? rs(seed, 2) * 5, jy = o.jy ?? rs(seed, 3) * 4;
  const br = 1 + (o.br ?? .014) * V(.02 + .09 * hs(seed, 4));                                       // breathes with the voice, each with its own lag
  g.save(); g.translate(x + w / 2 + jx, y + h / 2 + jy); g.rotate(rot); const sc = (o.s || 1) * br; g.scale(sc, sc); g.translate(-w / 2, -h / 2);
  const off = o.off ?? 8, ox = off * (.7 + .6 * hs(seed, 5)), oy = off * (.75 + .5 * hs(seed, 6));
  g.fillStyle = C.ink; rr(ox, oy, w, h, r); g.fill();
  g.fillStyle = fill; rr(0, 0, w, h, r); g.fill(); g.lineWidth = o.ol ?? 4; g.strokeStyle = C.ink; rr(0, 0, w, h, r); g.stroke();
  if (fn) fn(); g.restore();
}
function dcard(x, y, w, h, r = 34) {   // the ONE dark UI card (settings)
  g.save(); g.shadowColor = 'rgba(14,14,14,.28)'; g.shadowBlur = 44; g.shadowOffsetY = 18; g.fillStyle = C.dark; rr(x, y, w, h, r); g.fill(); g.restore();
  g.lineWidth = 2; g.strokeStyle = C.dark3; rr(x, y, w, h, r); g.stroke();
}
function tag(x, y, s, o = {}) {   // sticker chip (mono). default 26px = readable at phone size
  const px = o.px || 26; g.font = F(px, 700, 'JBMono'); const w = g.measureText(s).width + 36, h = px + 24;
  const x0 = o.al === 'right' ? x - w : x;
  sticker(x0, y, w, h, h / 2, o.fill || C.white, { rot: o.rot, ra: .03, ol: 3, off: 5, s: o.s || 1, br: .01 }, () => { tx(s, 18, h / 2 + px * .34, px, 700, 'JBMono', o.col || C.ink, 'left', 'tag:' + s); });
  return w;
}
function badge(n, cx, cy, r, s = 1, fill = C.lime) {   // numbered round badge
  g.save(); g.translate(cx, cy); g.scale(s, s);
  g.fillStyle = C.ink; g.beginPath(); g.arc(7, 6, r, 0, 7); g.fill();
  g.fillStyle = fill; g.beginPath(); g.arc(0, 0, r, 0, 7); g.fill(); g.lineWidth = 4; g.strokeStyle = C.ink; g.stroke();
  tx(String(n), 0, r * .36, r * 1.05, 900, 'InterTight', C.ink, 'center', 'badge' + n); g.restore();
}
function mark(x, y, s, col = C.ink) { g.save(); g.translate(x, y); g.scale(s / 320, s / 320); g.fillStyle = col; g.fill(MARK); g.restore(); }
function logoBadge(x, y, s, sc = 1, rot = 0) {   // real ChatGPT mark alone, in a white sticker square (no caption)
  sticker(x, y, s, s, s * .26, C.white, { rot, s: sc, off: 8, br: 0, jx: 0, jy: 0 }, () => { g.save(); g.translate(s * .16, s * .16); mark(0, 0, s * .68); g.restore(); });
}
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
// ---------- v6 style layer: light tones, noise-driven camera, 3-layer parallax background, kinetic headline that breathes with the voice ----------
const THEMES = { paper: { fg: C.ink, lm: false }, lime: { fg: C.ink, lm: true }, wash: { fg: C.ink, lm: false } };
let TN = THEMES.paper, FG = C.ink;
const setTone = tone => { TN = THEMES[tone]; FG = TN.fg; };
const K = (s, t, k = '') => ({ s, t, k });
// impacts: a soft push, not a ring: smooth noise offset that decays; direction differs per impact
const SHK = [];
const addShake = (t, a) => SHK.push([t, a, SHK.length]);
function shake(t) {
  let x = 0, y = 0, z = 0;
  for (const [ti, a, i] of SHK) { const u = t - ti; if (u < 0 || u > .9) continue; const d = a * Math.exp(-u * 6.5) * sm(u / .08); x += d * 2.2 * nz(i * 5 + 1, u * 7); y += d * 1.8 * nz(i * 5 + 2, u * 6.2); z += a / 1100 * Math.exp(-u * 6.5) * sm(u / .08); }
  return [x, y, z];
}
let PARX = 0, PARY = 0;
function cam(t) {
  const [sx, sy, sz] = shake(t);
  const z = 1.026 + .013 * fbm(1, t * .24) + .006 * nz(2, t * .43) + sz + .004 * V(.05);
  const x = 28 * fbm(3, t * .18 + 4) + 8 * nz(4, t * .39), y = 14 * fbm(5, t * .16 + 9) + 4 * nz(6, t * .33);
  return [z, x + sx, y + sy, .006 * fbm(7, t * .15 + 2)];
}
// ---- background: tone + one soft organic lime blob + 3 parallax layers (far: blurred rings, mid: dot grid, near: wandering mini stickers) ----
const NEAR = Array.from({ length: 9 }, (_, i) => ({ x: i % 2 ? 40 + hs(i, 1) * 90 : 950 + hs(i, 1) * 90, y: 200 + (i / 9) * 1500 + 80 * rs(i, 2), kind: i % 4, sz: 15 + hs(i, 3) * 15, fill: i % 3 === 0 ? 'lime' : 'white', fx: .1 + hs(i, 4) * .22, rot: rs(i, 5) * 2 }));
function bg(tone, t) {
  const lm = tone === 'lime', ws = tone === 'wash', ink = C.ink;
  g.fillStyle = lm ? C.lime : ws ? '#EEF9CF' : C.paper; g.fillRect(-500, -500, W + 1000, H + 1000);
  // one soft organic accent: a drifting, breathing blob (no edges)
  { const bx = 540 + 330 * fbm(11, t * .08 + 3), by = 960 + 560 * fbm(12, t * .06 + 8), rx = 620 + 90 * nz(13, t * .2) + 40 * V(.1), gr = g.createRadialGradient(bx, by, 40, bx, by, rx);
    gr.addColorStop(0, lm ? 'rgba(255,255,255,.38)' : ws ? 'rgba(182,242,58,.30)' : 'rgba(205,244,100,.5)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(-500, -500, W + 1000, H + 1000); }
  // far layer (parallax .35, depth blur): big rings wandering on their own noise
  g.save(); g.filter = 'blur(7px)'; g.lineWidth = 14; g.strokeStyle = lm ? '#C9F66A' : ws ? '#E1F3B4' : '#E8E8DC';
  [[120, 520, 210, 0], [980, 1000, 260, 1], [200, 1500, 190, 2], [900, 300, 170, 3]].forEach(([bx, by, r, k]) => { g.beginPath(); g.arc(bx + 110 * fbm(40 + k, t * .07 + k) - PARX * .35, by + 130 * fbm(50 + k, t * .06 + k * 3) - PARY * .35, r * (1 + .06 * nz(60 + k, t * .15)), 0, 7); g.stroke(); });
  g.restore();
  // mid layer (parallax 1): dot grid shifted by noise, never scrolling at a constant speed
  { const ox = 46 * fbm(21, t * .09 + 1) + PARX * .9, oy = 46 * fbm(22, t * .08 + 5) + PARY * .9; g.fillStyle = lm ? '#A4D82B' : ws ? '#D3E8A2' : C.dot;
    for (let x = -108; x < W + 160; x += 54) for (let y = -108; y < H + 160; y += 54) { g.beginPath(); g.arc(x + ox % 54, y + oy % 54, 2.3, 0, 7); g.fill(); } }
  // near layer (parallax 1.8): small outlined stickers that wander; voice makes each swell a little, each at its own lag
  NEAR.forEach((o, i) => {
    const x = o.x + 80 * fbm(100 + i, t * o.fx + i) + PARX * 1.8, y = o.y + 110 * fbm(130 + i, t * o.fx * .8 + i * 2) + PARY * 1.8, sz = o.sz * (1 + .22 * V(.03 + .015 * i)), fillc = o.fill === 'lime' ? (lm ? C.white : C.lime) : C.white;
    g.save(); g.translate(x, y); g.rotate(o.rot + 1.1 * fbm(160 + i, t * .12 + i)); g.lineWidth = 4; g.strokeStyle = ink; g.fillStyle = fillc; g.beginPath();
    if (o.kind === 0) g.arc(0, 0, sz, 0, 7); else if (o.kind === 1) g.rect(-sz, -sz, sz * 2, sz * 2); else if (o.kind === 2) { g.moveTo(0, -sz * 1.2); g.lineTo(sz * 1.1, sz); g.lineTo(-sz * 1.1, sz); g.closePath(); } else { g.moveTo(-sz, 0); g.lineTo(sz, 0); g.moveTo(0, -sz); g.lineTo(0, sz); }
    if (o.kind === 3) g.stroke(); else { g.fill(); g.stroke(); } g.restore();
  });
}
// ---- kinetic headline: each word rises into place at its spoken time (long ease, no overshoot, +-30 ms jitter), key words sit in pills that swell with the voice ----
function head(t, rows, y0, px, lh, o = {}) {
  const fam = 'InterTight', lm = TN.lm;
  const wOf = (row, f) => { g.font = F(f, 900, fam); return row.reduce((a, k, i) => a + g.measureText(k.s).width + (k.k ? f * .5 : 0) + (i ? f * .28 : 0), 0); };
  let S = 1; rows.forEach(r => { S = Math.min(S, (o.maxW || 860) / wOf(r, px)); }); const f = px * S;
  rows.forEach((row, ri) => {
    const rw = wOf(row, f); let cx = o.center ? 540 - rw / 2 : (o.x || 100); const y = y0 + ri * lh * S;
    row.forEach((k, i) => {
      g.font = F(f, 900, fam); const tw = g.measureText(k.s).width, pad = k.k ? f * .25 : 0, bw = tw + pad * 2; if (i) cx += f * .28;
      const sd = ri * 31 + i * 7 + k.s.length * 3, u = t - k.t - rs(sd, 1) * .03;
      if (u > -.02) {
        const e = p3o(u / (.5 + .12 * hs(sd, 2))), a = sm(u / .16), up = (1 - e) * f * (k.k ? .2 : .36), sc = 1 + (k.k ? .1 : .06) * (1 - e);
        const pp = k.k ? 1 + .05 * Math.sin(Math.PI * clamp(u / .55)) + .03 * V(.03 + .012 * i) : 1;
        g.save(); g.globalAlpha *= a; g.translate(cx + bw / 2, y - f * .3 + up); g.rotate((1 - e) * rs(sd, 3) * .05); g.scale(sc * pp, sc * pp); g.translate(-bw / 2, f * .3);
        let col = FG;
        if (k.k) {
          const top = -f * .86, hh = f * 1.06, so = f * (.06 + .04 * hs(sd, 4));
          if (k.k === 'lime') { g.fillStyle = C.ink; rr(so * 1.2, top + so, bw, hh, f * .26); g.fill(); g.fillStyle = lm ? C.white : C.lime; rr(0, top, bw, hh, f * .26); g.fill(); g.lineWidth = Math.max(4, f * .05); g.strokeStyle = C.ink; rr(0, top, bw, hh, f * .26); g.stroke(); col = C.ink; }
          else { g.fillStyle = C.ink; rr(0, top, bw, hh, f * .26); g.fill(); col = k.k === 'limeink' ? C.lime : '#fff'; }
        }
        g.font = F(f, 900, fam); g.fillStyle = col; g.textAlign = 'left'; g.textBaseline = 'alphabetic'; g.fillText(k.s, pad, 0);
        if (u > .5) reg('h:' + k.s + ri + i, k.s, pad, -f * .78, pad + tw, f * .05);
        g.restore();
      }
      cx += bw;
    });
  });
}
function typed(s, p) { return s.slice(0, Math.floor(s.length * clamp(p))); }
function icon(kind, cx, cy, s = 1, col = C.ink) {
  g.save(); g.translate(cx, cy); g.scale(s, s); g.strokeStyle = col; g.fillStyle = col; g.lineWidth = 5; g.lineCap = 'round'; g.lineJoin = 'round';
  const arc = (x, y, r) => { g.beginPath(); g.arc(x, y, r, 0, 7); g.stroke(); };
  if (kind === 'chat') { rr(-24, -22, 48, 34, 10); g.stroke(); g.beginPath(); g.moveTo(-8, 12); g.lineTo(-13, 25); g.lineTo(5, 12); g.stroke(); }
  else if (kind === 'clock') { arc(0, 0, 24); g.beginPath(); g.moveTo(0, -13); g.lineTo(0, 0); g.lineTo(11, 6); g.stroke(); }
  else if (kind === 'cal') { rr(-24, -18, 48, 42, 8); g.stroke(); g.beginPath(); g.moveTo(-24, -4); g.lineTo(24, -4); g.moveTo(-11, -27); g.lineTo(-11, -13); g.moveTo(11, -27); g.lineTo(11, -13); g.stroke(); }
  else if (kind === 'cam') { rr(-27, -14, 54, 38, 9); g.stroke(); arc(0, 5, 10); g.beginPath(); g.moveTo(-11, -14); g.lineTo(-7, -23); g.lineTo(7, -23); g.lineTo(11, -14); g.stroke(); }
  else if (kind === 'id') { rr(-29, -20, 58, 40, 8); g.stroke(); arc(-13, -4, 6); g.beginPath(); g.moveTo(-2, -6); g.lineTo(19, -6); g.moveTo(-2, 6); g.lineTo(15, 6); g.moveTo(-22, 12); g.lineTo(-4, 12); g.stroke(); }
  else if (kind === 'user') { arc(0, -9, 11); g.beginPath(); g.arc(0, 28, 25, Math.PI * 1.12, Math.PI * 1.88); g.stroke(); }
  else if (kind === 'gear') { arc(0, 0, 12); for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4; g.beginPath(); g.moveTo(Math.cos(a) * 18, Math.sin(a) * 18); g.lineTo(Math.cos(a) * 25, Math.sin(a) * 25); g.stroke(); } }
  g.restore();
}
function toggle(x, y, on, p = 1) {   // sticker toggle switch, p = 0..1 knob travel (eased by the caller)
  const w = 120, h = 60; g.save(); g.translate(x, y);
  g.fillStyle = C.ink; rr(5, 5, w, h, 30); g.fill();
  g.fillStyle = p > .5 ? C.lime : C.white; rr(0, 0, w, h, 30); g.fill(); g.lineWidth = 4; g.strokeStyle = C.ink; rr(0, 0, w, h, 30); g.stroke();
  g.fillStyle = C.ink; g.beginPath(); g.arc(30 + 60 * p, 30, 18, 0, 7); g.fill(); g.restore();
}
function mkCv(w, h, fn) { const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const keep = g, kr = REC; REC = false; g = cv.getContext('2d'); fn(); g = keep; REC = kr; return cv; }
function shardsG(t, t0, cv, w, h, cols, rows, ix, iy, seed = 21, ox = 0, oy = 0) {   // the one fragment-shatter hero beat (kept from the approved build): shards drift out on smooth curves and fade
  const R = rng(seed), cw = w / cols, ch = h / rows, pts = [];
  for (let j = 0; j <= rows; j++) { pts[j] = []; for (let i = 0; i <= cols; i++) pts[j][i] = [i * cw + ((i > 0 && i < cols) ? (R() - .5) * cw * .6 : 0), j * ch + ((j > 0 && j < rows) ? (R() - .5) * ch * .6 : 0)]; }
  const u = t - t0;
  for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) {
    const a = pts[j][i], b = pts[j][i + 1], c = pts[j + 1][i + 1], d = pts[j + 1][i];
    [[a, b, c], [a, c, d]].forEach(tri => {
      const cx = (tri[0][0] + tri[1][0] + tri[2][0]) / 3, cy = (tri[0][1] + tri[1][1] + tri[2][1]) / 3;
      let dx = cx - ix, dy = cy - iy; const L = Math.hypot(dx, dy) + 1; dx /= L; dy /= L;
      const sp = (300 + R() * 640 + 560 / (1 + L / 90)) * .5, rot = (R() - .5) * 9, delay = L / 3600;
      const uu = Math.max(0, u - delay), e = 1 - Math.exp(-uu * 2.4) , ee = e * sm(uu / .08);
      let px = dx * sp * ee / 2.4, py = dy * sp * ee / 2.4 + 140 * uu * uu; px = clamp(cx + px + ox, 90, 990) - cx - ox; py = clamp(cy + py + oy, 290, 1220) - cy - oy;
      const al = 1 - sm(sg(uu, .4, .9));
      if (al < .01) return;
      g.save(); g.globalAlpha *= al; g.translate(cx + px, cy + py); g.rotate(rot * ee * .7); g.translate(-cx, -cy);
      g.beginPath(); g.moveTo(tri[0][0], tri[0][1]); g.lineTo(tri[1][0], tri[1][1]); g.lineTo(tri[2][0], tri[2][1]); g.closePath();
      g.save(); g.clip(); g.drawImage(cv, 0, 0); g.restore();
      g.lineWidth = 2.5; g.strokeStyle = 'rgba(182,242,58,.7)'; g.stroke(); g.restore();
    });
  }
}
function stamp(text, cx, cy, px, rot, s, a, col = C.limeDeep, id = 'stamp') {
  if (a < .003) return; g.save(); g.globalAlpha *= a; g.translate(cx, cy); g.rotate(rot); g.scale(s, s);
  g.font = F(px, 900, 'InterTight'); const w = g.measureText(text).width + px * .9, h = px * 1.8;
  g.fillStyle = 'rgba(255,255,255,.97)'; rr(-w / 2, -h / 2, w, h, 16); g.fill(); g.lineWidth = 6; g.strokeStyle = col; rr(-w / 2, -h / 2, w, h, 16); g.stroke(); g.lineWidth = 2; rr(-w / 2 + 8, -h / 2 + 8, w - 16, h - 16, 10); g.stroke();
  tx(text, 0, px * .36, px, 900, 'InterTight', col, 'center', id); g.restore();
}
// ---------- v6 scenes. Every time below is a cue time (wt/we/T) plus a seeded +-40 ms jitter, never a constant grid. ----------
const t0s = n => T['l' + n] - .12;                          // scene n starts .12 s before its line is spoken
const EXAMPLE = 'example · re-created';
const SW = (cx, cy) => { g.translate(cx, cy); };
function flash(x, y, t, t0, r, col = '182,242,58') {          // soft light, not a ring: radial glow that swells and fades
  const a = bell(t, t0, t0 + .12, t0 + .75); if (a < .004) return; const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, `rgba(${col},${.7 * a})`); gr.addColorStop(1, `rgba(${col},0)`);
  g.save(); g.fillStyle = gr; g.fillRect(x - r, y - r, r * 2, r * 2); g.restore();
}
function deco(t, t0, x, y, kind, sz, seed) {                // little sticker shapes that wander (ep 82 DNA); never over text
  if (!enter(t, t0, x, y, 'zoom', { id: seed, dur: .8 })) return;
  const px = x + 14 * fbm(seed, t * .3), py = y + 18 * fbm(seed + 3, t * .27), s = sz * (1 + .1 * V(.04 + .02 * (seed % 5)));
  g.translate(px - x, py - y); g.save(); g.translate(x, y); g.rotate(rs(seed, 4) * .5 + .5 * fbm(seed + 6, t * .22)); g.scale(s / 40, s / 40); g.lineJoin = 'round'; g.lineWidth = 6; g.strokeStyle = C.ink;
  const path = () => { g.beginPath(); if (kind === 'star') { for (let i = 0; i < 10; i++) { const r = i % 2 ? 17 : 40, a = -Math.PI / 2 + i * Math.PI / 5; i ? g.lineTo(Math.cos(a) * r, Math.sin(a) * r) : g.moveTo(Math.cos(a) * r, Math.sin(a) * r); } g.closePath(); }
    else if (kind === 'spark') { g.moveTo(0, -42); g.quadraticCurveTo(5, -5, 42, 0); g.quadraticCurveTo(5, 5, 0, 42); g.quadraticCurveTo(-5, 5, -42, 0); g.quadraticCurveTo(-5, -5, 0, -42); g.closePath(); }
    else if (kind === 'heart') { g.moveTo(0, 36); g.bezierCurveTo(-60, -8, -30, -50, 0, -18); g.bezierCurveTo(30, -50, 60, -8, 0, 36); g.closePath(); }
    else g.arc(0, 0, 30, 0, 7); };
  g.translate(7, 7); g.fillStyle = C.ink; path(); g.fill(); g.translate(-7, -7); g.fillStyle = kind === 'heart' ? '#FF7A8A' : C.lime; path(); g.fill(); path(); g.stroke(); g.restore(); g.restore();
}
// ===== A: the claim (paper) =====
const tw1 = i => i === 0 ? .1 : wt('l1', i);                 // first word is spoken at 0.1 s
const HT = tw1(5) - .02;                                      // "teen" spoken: badge stamped TEEN
function ageFace(label, fill, fg) { sticker(0, 0, 300, 120, 34, fill, { off: 9, ol: 6, rot: 0, jx: 0, jy: 0, br: 0 }, () => { tx(label, 150, 86, 72, 900, 'InterTight', fg, 'center', 'badge:' + label); }); }
const FACE_ADULT = mkCv(322, 142, () => ageFace('ADULT', C.lime, C.ink));
function sceneA(t) {
  const ent = 1 + .12 * (1 - expoE(t / .55));
  // soft rays behind the mark: the whole fan drifts on noise, every ray has its own length and width, the voice swells them
  g.save(); g.translate(540, 440); g.rotate(.5 * fbm(70, t * .11 + 2)); g.fillStyle = C.wash; g.globalAlpha *= .9;
  for (let i = 0; i < 12; i++) { const a = i * Math.PI / 6 + .08 * rs(i, 7), R = (390 + 55 * nz(80 + i, t * .35 + i) + 34 * V(.02 * i)) , wd = .2 + .12 * hs(i, 8); g.beginPath(); g.moveTo(0, 0); g.lineTo(Math.cos(a) * R, Math.sin(a) * R); g.lineTo(Math.cos(a + wd) * R, Math.sin(a + wd) * R); g.closePath(); g.fill(); }
  g.restore();
  const gv = V(.03); if (gv > .01) { const gr = g.createRadialGradient(540, 440, 120, 540, 440, 330); gr.addColorStop(0, `rgba(182,242,58,${.55 * gv})`); gr.addColorStop(1, 'rgba(182,242,58,0)'); g.fillStyle = gr; g.fillRect(190, 90, 700, 700); }
  logoBadge(390, 290, 300, (1 + .06 * V(.03)) * ent, -.06 + .05 * fbm(90, t * .2));
  deco(t, .5, 770, 330, 'star', 50, 201); deco(t, .85, 300, 560, 'spark', 40, 202);
  head(t, [[K('CHATGPT', 0), K('MIGHT', tw1(1))], [K('THINK', tw1(2)), K("YOU'RE", tw1(3))], [K('A', tw1(4)), K('TEEN', tw1(5), 'limeink')], [K('RIGHT', tw1(6)), K('NOW!', tw1(7), 'lime')]], 706, 100, 98, { center: true, maxW: 860 });
  // account card (example, light sticker): card eases up, the ADULT badge shatters at "teen" and TEEN lands
  const u = t - HT;
  if (enter(t, .3, 540, 1140, 'rise', { id: 11, dur: .9, rise: 30 })) {
    g.translate(100, 1040 + fl(t, 0, 5, 3.4));
    sticker(0, 0, 880, 200, 36, C.white, { off: 10, ol: 5, br: .008 }, () => {
      tag(170, 140, EXAMPLE, { fill: C.wash });
      g.fillStyle = C.lime; g.beginPath(); g.arc(88, 100, 52, 0, 7); g.fill(); g.lineWidth = 5; g.strokeStyle = C.ink; g.stroke(); icon('user', 88, 100, 1.3);
      tx('Your account', 170, 90, 36, 800, 'InterTight', C.ink, 'left', 'acct'); tx('birth year 1996', 170, 128, 26, 600, 'Inter', C.ink2, 'left', 'born');
      g.save(); g.translate(540, 40);
      if (u < 0) { g.translate(0, fl(t, 3, 3, 2.2)); g.drawImage(FACE_ADULT, 0, 0); }
      else {
        shardsG(t, HT, FACE_ADULT, 322, 142, 6, 3, 160, 70, 21, 640, 1080);
        const k = expoE(u / .3), sc = 1 + 1.4 * (1 - k), a = sm(u / .08);
        g.save(); g.globalAlpha *= a; g.translate(150, 60); g.rotate(-.14 * (1 - k) + .02 * fbm(95, t * .3)); g.scale(sc * (1 + .04 * V(.02)), sc * (1 + .04 * V(.02))); g.translate(-150, -60); ageFace('TEEN', C.ink, C.lime); g.restore();
        ringMark(t, HT + .3, .6, 150, 62, 196, 84, C.limeDeep, 9, 3);
      }
      g.restore();
    }); g.restore();
  }
  flash(790, 1130, t, HT, 330);
}
// ===== B: even with a typed birthday (lime) =====
const BD = wt('l2', 5) - .25;
const QUOTE = [['“It can identify an account as eligible', 0], ['for the ChatGPT for Teens experience', 0], ['even if you already gave your date of', 1], ['birth when you created your account.”', 2]];
const QS = QUOTE.map(q => q[0]).join(''), QCUM = QUOTE.reduce((a, q) => (a.push(a[a.length - 1] + q[0].length), a), [0]);
const BDP = typePlan('03 / 14 / 1996', T.l2 + .36, T.l2 + 1.3, 5, { at: 13, ch: '7' });          // types ...199 7, notices, backspaces, 6
const QP = typePlan(QS, T.l2 + .55, T.l2 + 1.68, 2, { at: QS.indexOf('eligible') + 2, ch: 'o' });   // "elogible" -> backspace -> "eligible"
const BDEND = BDP[BDP.length - 1].t, QEND = QP[QP.length - 1].t;
function sceneB(t) {
  head(t, [[K('EVEN', wt('l2', 0)), K('IF', wt('l2', 1)), K('YOU', wt('l2', 2))], [K('TYPED', wt('l2', 3), 'ink'), K('YOUR', wt('l2', 4))], [K('BIRTHDAY!', wt('l2', 5), 'lime')]], 410, 108, 104, { center: true, maxW: 860 });
  deco(t, T.l2 + .7, 930, 330, 'spark', 44, 211);
  if (enter(t, T.l2 + .1, 540, 750, 'sl', { id: 21, dur: .95 })) {   // birthday field
    g.translate(0, fl(t, 2, 4, 3.4)); sticker(100, 675, 880, 150, 34, C.white, { off: 10, ol: 5 });
    tx('Birthday', 134, 718, 30, 800, 'InterTight', C.ink2, 'left', 'bday'); tag(300, 680, EXAMPLE, { fill: C.wash });
    g.fillStyle = '#ECECE4'; rr(130, 735, 820, 76, 20); g.fill(); g.strokeStyle = C.ink; g.lineWidth = 3; rr(130, 735, 820, 76, 20); g.stroke();
    const st = typedAt(BDP, t), s = '03 / 14 / 1996'.slice(0, st.n) + st.x; tx(s, 160, 788, 46, 700, 'JBMono', C.ink, 'left', 'bdval'); g.font = F(46, 700, 'JBMono'); if (t < BDEND + .35) caret(160 + g.measureText(s).width + 6, 746, 54, t, C.limeDeep, 4);
    const ck = p3o(sg(t, BDEND + .08, BDEND + .4)); if (ck > .01) check(620 + 150, 773, 28 * ck, ck, sinIO(sg(t, BDEND + .2, BDEND + .55)));
    g.restore();
  }
  if (enter(t, T.l2 + .2, 540, 1050, 'rise', { id: 22, dur: .95, rise: 26 })) {   // quote card
    g.translate(0, fl(t, 6, 4, 4.4)); sticker(95, 870, 890, 370, 34, C.white, { off: 10, ol: 5 });
    let fs = 39; g.font = F(fs, 700, 'Inter'); const wmax = Math.max(...QUOTE.map(q => g.measureText(q[0]).width)); fs = Math.min(40, 39 * 790 / wmax); g.font = F(fs, 700, 'Inter');
    const st = typedAt(QP, t), n = st.n, hsP = sinIO(sg(t, BD + .05, BD + .7)); let cl = 0; while (cl < 3 && n > QCUM[cl + 1]) cl++;
    QUOTE.forEach((q, i) => { const y = 950 + i * 60, cnt = Math.max(0, Math.min(q[0].length, n - QCUM[i])), vis = q[0].slice(0, cnt) + (i === cl ? st.x : '');
      if (q[1] && hsP > .01 && cnt > 0) { g.font = F(fs, 700, 'Inter'); const part = q[1] === 2 ? Math.min(cnt, 5) : cnt, w0 = g.measureText(q[0].slice(0, part)).width; strokePath(roughLine(127, y - 13, 127 + w0 + 6, y - 14, 30 + i, 1.8), hsP, C.lime, 46, 30 + i); }
      tx(vis, 133, y, fs, 700, 'Inter', C.ink, 'left', 'q' + i); });
    g.font = F(fs, 700, 'Inter'); if (t < QEND + .3) { const cnt = Math.max(0, Math.min(QUOTE[cl][0].length, n - QCUM[cl])); caret(133 + g.measureText(QUOTE[cl][0].slice(0, cnt) + st.x).width + 6, 950 + cl * 60 - 38, 46, t, C.limeDeep, 6); }
    sticker(133, 1170, 400, 56, 28, C.lime, { off: 6, ol: 4 }, () => { tx('OpenAI Help Center', 24, 39, 28, 800, 'InterTight', C.ink, 'left', 'qsrc'); });
    g.restore();
  }
  const SB = BDEND + .12;   // STILL TEEN? settles in once the birthday is in
  if (enter(t, SB, 820, 800, 'tilt', { id: 23, rot: .16, dx: 110, dur: .8 })) { g.translate(0, fl(t, 4, 4, 3.3)); sticker(650, 752, 340, 96, 48, C.white, { rot: -.07, off: 8, ol: 5 }, () => { tx('STILL TEEN?', 170, 66, 40, 900, 'InterTight', C.ink, 'center', 'stillteen'); }); g.restore(); }
  flash(820, 800, t, SB + .1, 260);
}
// ===== C: the real news (paper) =====
const NEWS_IN = T.l3 + .42;
function sceneC(t) {
  head(t, [[K('SOME', wt('l3', 0)), K('ADULTS', wt('l3', 1))], [K('GOT', wt('l3', 2)), K('STUCK', wt('l3', 3), 'lime')], [K('IN', wt('l3', 4)), K('TEEN', wt('l3', 5), 'ink'), K('MODE.', wt('l3', 6))]].map(r => r), 376, 94, 90, { center: true, maxW: 860 });
  // TechCrunch card eases in from the right and sits under the TechRadar card like a second paper
  const tw = 860, th = tw * TC.height / TC.width;
  if (enter(t, wt('l3', 7) - .2, 540, 800 + th / 2, 'sr', { id: 31, dur: 1.1 })) { g.translate(0, fl(t, 1, 5, 4.2)); g.translate(50, 800 + th / 2); g.rotate(.022 + .004 * nz(33, t * .3)); g.translate(-430, -th / 2);
    g.fillStyle = C.ink; rr(10, 10, tw, th, 18); g.fill(); g.fillStyle = '#fff'; rr(0, 0, tw, th, 18); g.fill(); g.save(); rr(0, 0, tw, th, 18); g.clip(); g.drawImage(TC, 0, 0, tw, th); g.restore(); g.lineWidth = 5; g.strokeStyle = C.ink; rr(0, 0, tw, th, 18); g.stroke(); g.restore(); g.restore(); }
  // TechRadar headline card: the hero landing, a long fast-then-soft settle (no bounce), voice swells it a little
  const ru = t - NEWS_IN, rw = 918, rh = rw * TR.height / TR.width; logBig('hero:news', NEWS_IN);
  if (ru > 0) { const rk = p3o(ru / .85), rs_ = 1 + .42 * (1 - rk); g.save(); g.globalAlpha *= sm(ru / .22); g.translate(540, 590 + rh / 2 + fl(t, 3, 4, 4.8)); g.rotate(.035 * (1 - rk) - .006 * nz(37, t * .3));
    const hz = (1 + .018 * sg(t, NEWS_IN + .4, NEWS_IN + 3.4)) * (1 + .006 * V(.05)); g.scale(rs_ * hz, rs_ * hz); g.translate(-rw / 2, -rh / 2);
    g.fillStyle = C.ink; rr(11, 12, rw, rh, 20); g.fill(); g.fillStyle = '#fff'; rr(0, 0, rw, rh, 20); g.fill();
    g.save(); rr(0, 0, rw, rh, 20); g.clip(); g.drawImage(TR, 0, 0, rw, rh); const k = rw / TR.width;
    const m = sinIO(sg(t, wt('l3', 3) - .1, wt('l3', 3) + .6)); if (m > .005) { g.save(); g.scale(k, k); strokePath(roughLine(34, 197, 566, 194, 41, 2.2), m, C.lime, 66, 41, { mult: true }); g.restore(); }
    g.restore(); g.lineWidth = 5; g.strokeStyle = C.ink; rr(0, 0, rw, rh, 20); g.stroke(); g.restore(); }
  const ga = sm(sg(t, NEWS_IN + .6, NEWS_IN + 1.0)); if (ga > .003) { g.save(); g.globalAlpha *= ga; g.translate(0, fl(t, 5, 3, 3.6)); const w1 = tag(81, 1000, 'real page · TechRadar', { px: 24, fill: C.lime, rot: -.01 }); tag(81 + w1 + 14, 1000, 'real page · TechCrunch', { px: 24, fill: C.white, rot: .012 }); g.restore(); }
  const su = t - (NEWS_IN + .75); if (su > 0) { const k = expoE(su / .45); stamp('REAL NEWS', 905, 1024 + fl(t, 2, 3, 3.1), 26, -.06 + .01 * nz(39, t * .3), 1 + .5 * (1 - k), sm(su / .15), C.limeDeep, 'stampnews'); }
  if (enter(t, NEWS_IN + .95, 540, 1120, 'sl', { id: 32, dur: .9 })) { g.translate(0, fl(t, 7, 3, 3.9));
    sticker(100, 1062, 880, 118, 26, C.lime, { off: 8, ol: 5 }, () => { g.globalCompositeOperation = 'multiply'; g.drawImage(TB, 24, 22, 832, 832 * TB.height / TB.width); g.globalCompositeOperation = 'source-over'; }); g.restore(); }
  head(t, [[K('NEWS', wt('l3', 7)), K('SITES', wt('l3', 8)), K('REPORTED', wt('l3', 9)), K('IT.', wt('l3', 10), 'lime')]], 1234, 54, 60, { center: true, maxW: 860 });
}
// ===== D: what it guesses from (lime) =====
function sceneD(t) {
  head(t, [[K('IT', wt('l4', 0)), K('GUESSES', wt('l4', 1), 'ink'), K('FROM', wt('l4', 2))], [K('WHAT', wt('l4', 3)), K('YOU', wt('l4', 4)), K('ASK,', wt('l4', 5), 'ink')], [K('AND', wt('l4', 6)), K('WHEN.', wt('l4', 7), 'ink')]], 372, 92, 92, { center: true, maxW: 860 });
  deco(t, T.l4 + .9, 900, 300, 'star', 46, 241);
  drawArrow(t, wt('l4', 5) - .05, .55, 840, 590, 770, 634, 20, C.ink, 8, 77);
  const items = [['what you talk about', 'chat', Math.min(wt('l4', 3) - .05, T.l4 + .5), C.white, 'sl', 100, 860], ['times of day you use it', 'clock', wt('l4', 7) - .1, '#F6FFD6', 'sr', 128, 832], ['how long your account has existed', 'cal', wt('l4', 7) + .45, C.white, 'rise', 88, 888]];
  items.forEach(([s, ic, t0, fill, kind, x0, w0], i) => { const y = 640 + i * 190; if (!enter(t, t0, 540, y + 75, kind, { id: 240 + i, dur: .85 + .1 * i })) return; g.translate(0, fl(t, i * 2, 5, 3.7 + i * .4));
    sticker(x0, y, w0, 150, 75, fill, { off: 10, ol: 6 }, () => { icon(ic, 95, 75, 1.6, C.ink); tx(s, 160, 94, 42, 800, 'InterTight', C.ink, 'left', 'sig' + i); if (i === 1) ringMark(t, wt('l4', 7) + .05, .55, 95, 75, 54, 50, C.limeDeep, 8, 7); }); g.restore(); });
  const ca = sm(sg(t, wt('l4', 7) + .5, wt('l4', 7) + .9)); if (ca > .003) { g.save(); g.globalAlpha *= ca; tag(100, 1178, 'signals listed by OpenAI Help Center', { px: 24, fill: C.white }); g.restore(); }
}
// ===== E: Settings, Account, Age (paper; the settings UI is the one dark card) =====
const l5s = [wt('l5', 4), wt('l5', 5), wt('l5', 6)];
function sceneE(t) {
  head(t, [[K('SEE', wt('l5', 0)), K('WHAT', wt('l5', 1))], [K('IT', wt('l5', 2)), K('SAYS:', wt('l5', 3), 'lime')]], 392, 100, 100, { center: true, maxW: 860 });
  const steps = [['Settings', 1, l5s[0]], ['Account', 2, l5s[1]], ['Age', 3, l5s[2]]], GAP = 44;
  g.font = F(34, 800, 'InterTight'); const ws = steps.map(s => g.measureText(s[0]).width + 104); let x = 540 - (ws[0] + ws[1] + ws[2] + GAP * 2) / 2;
  steps.forEach(([s, n, ts], i) => { const y = 522, ent = wt('l5', 3) + .15 + i * (.17 + .06 * hs(i, 3));
    if (enter(t, ent, x + ws[i] / 2, y + 43, i === 1 ? 'rise' : 'drop', { id: 250 + i, dur: .7 })) { const act = t >= ts - .1 && (i === 2 || t < steps[i + 1][2] - .1), sc = 1 + .09 * bell(t, ts - .15, ts + .1, ts + .6) + (act ? .035 : 0);
      g.translate(x + ws[i] / 2, y + 43); g.scale(sc, sc); g.translate(-ws[i] / 2, -43); sticker(0, 0, ws[i], 86, 43, act ? C.lime : C.white, { off: 7, rot: rs(i, 8) * .04, jx: 0, jy: 0 }); badge(n, 44, 43, 28, 1, act ? C.white : C.lime); tx(s, 86, 56, 34, 800, 'InterTight', C.ink, 'left', 'step' + n); g.restore(); }
    if (i < 2) drawArrow(t, ent + .45 + .1 * i, .45, x + ws[i] + 4, 566 + 3 * rs(i, 9), x + ws[i] + GAP - 6, 565, 7 * (i ? -1 : 1), C.ink, 7, 50 + i);
    x += ws[i] + GAP; });
  if (enter(t, T.l5 + .25, 540, 940, 'rise', { id: 261, dur: .95 })) {
    const bump = 1 + .012 * V(.04); g.translate(540, 940); g.scale(bump, bump); g.translate(-540, -940); g.translate(0, fl(t, 1, 4, 4.6));
    dcard(100, 650, 880, 545, 40); tag(946, 668, EXAMPLE, { al: 'right', fill: C.wash });
    g.save(); rr(100, 650, 880, 545, 40); g.clip(); const sw = ioE(sg(t, l5s[1] + .1, l5s[1] + .62));
    const row = (s, y, hiT, ic) => { const hi = sm(sg(t, hiT - .12, hiT + .1)); g.fillStyle = '#343744'; rr(130, y, 820, 84, 24); g.fill(); if (hi > .003) { g.save(); g.globalAlpha *= hi; g.fillStyle = C.lime; rr(130, y, 820, 84, 24); g.fill(); g.restore(); }
      const dk = hi > .5; icon(ic, 180, y + 42, .85, dk ? C.ink : '#DDE0D2'); tx(s, 232, y + 56, 38, 700, 'Inter', dk ? C.ink : '#fff', 'left', 'r:' + s); g.strokeStyle = dk ? C.ink : C.mute; g.lineWidth = 5; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); g.moveTo(912, y + 27); g.lineTo(926, y + 42); g.lineTo(912, y + 57); g.stroke(); };
    g.save(); const k0 = REC; if (sw > .01) REC = false; g.translate(-sw * 880, 0); tx('Settings', 134, 726, 40, 800, 'InterTight', '#fff', 'left', 'p0'); icon('gear', 340, 714, .9, C.lime);
    [['General', 'gear'], ['Notifications', 'chat'], ['Personalization', 'user'], ['Account', 'id']].forEach(([s, ic], i) => row(s, 765 + i * 108, s === 'Account' ? l5s[1] : 1e9, ic)); g.restore(); REC = k0;
    g.save(); const k1 = REC; if (sw < .99) REC = false; g.translate((1 - sw) * 880, 0); tx('Account', 134, 726, 40, 800, 'InterTight', '#fff', 'left', 'p1'); icon('id', 360, 714, .9, C.lime);
    [['Profile', 'user'], ['Age', 'clock'], ['Plan', 'cal']].forEach(([s, ic], i) => row(s, 765 + i * 108, s === 'Age' ? l5s[2] : 1e9, ic)); g.restore(); REC = k1; g.restore();
    strokePath(roughRect(122, 865, 836, 100, 61, 26), sinIO(sg(t, l5s[2] + .05, l5s[2] + .6)), '#fff', 7, 61);
    const ca = sm(sg(t, T.l5 + .6, T.l5 + .95)) * (1 - sm(sg(t, l5s[2] + .7, l5s[2] + 1.0)));
    ripple(600, 1141, t, l5s[1], C.lime); ripple(650, 925, t, l5s[2], C.lime);
    pointer(t, { x: 1000, y: 610, t: T.l5 + .55 }, [{ x: 600, y: 1141, ta: l5s[1] - .03, tp: l5s[1] }, { x: 650, y: 925, ta: l5s[2] - .03, tp: l5s[2] }], 81, ca);
    g.restore();
  }
}
// ===== F: verify (selfie / ID flip) (wash) =====
function sceneF(t) {
  head(t, [[K('IF', wt('l6', 0)), K("IT'S", wt('l6', 1)), K('WRONG,', wt('l6', 2), 'ink')], [K('OPENAI', wt('l6', 3)), K('SAYS', wt('l6', 4)), K('A', wt('l6', 5)), K('SELFIE', wt('l6', 6), 'lime')], [K('OR', wt('l6', 7)), K('AN', wt('l6', 8)), K('ID', wt('l6', 9), 'lime'), K('CAN', wt('l6', 10)), K('FIX', wt('l6', 11)), K('IT.', wt('l6', 12))]], 374, 86, 90, { center: true, maxW: 870 });
  deco(t, T.l6 + 1.1, 950, 330, 'spark', 44, 261);
  if (!enter(t, T.l6 + .25, 540, 900, 'tilt', { id: 62, rot: -.07, dx: -70, dur: 1.0 })) return;
  g.translate(0, fl(t, 2, 4, 4.4)); sticker(100, 600, 880, 600, 40, C.white, { off: 10, ol: 5 }); tx('Verify your age', 134, 664, 40, 800, 'InterTight', C.ink, 'left', 'vh');
  const fx = wt('l6', 11) - .05, fp = sm(sg(t, fx, fx + .5)), lab = fp > .5 ? 'ADULT' : 'TEEN';
  g.save(); g.translate(830, 650); g.scale(Math.max(.03, Math.abs(Math.cos(fp * Math.PI))), 1 + .08 * Math.sin(fp * Math.PI)); sticker(-105, -40, 210, 80, 40, fp > .5 ? C.lime : C.ink, { off: 6, ol: 4, rot: 0, jx: 0, jy: 0 }, () => { tx(lab, 105, 56, 40, 900, 'InterTight', fp > .5 ? C.ink : C.lime, 'center', 'vbadge'); }); g.restore();
  ringMark(t, fx + .5, .55, 830, 652, 138, 62, C.limeDeep, 8, 63);
  sticker(134, 690, 360, 54, 27, C.wash, { off: 5, ol: 3 }, () => { tx('via a third party', 22, 37, 26, 800, 'InterTight', C.ink, 'left', 'third'); });
  [['Selfie', 'cam', wt('l6', 6), 'sl'], ['ID', 'id', wt('l6', 9), 'sr']].forEach(([s, ic, ts, kind], i) => { if (!enter(t, T.l6 + .8 + i * .22, 335 + i * 410, 920, kind, { id: 64 + i, dur: .9 })) return;
    const p = sm(sg(t, ts - .02, ts + .5)), sx = Math.max(.04, Math.abs(Math.cos(p * Math.PI))), on = p > .5, x0 = 130 + i * 420;
    g.translate(0, fl(t, i * 3, 4, 3.5 + i * .5)); g.save(); g.translate(x0 + 195, 920); g.scale(sx, 1 + .06 * Math.sin(p * Math.PI)); g.translate(-195, -150);
    sticker(0, 0, 390, 300, 44, on ? C.lime : C.white, { off: 10, ol: 6, rot: 0, jx: 0, jy: 0, br: 0 }, () => { icon(ic, 195, 120, 2.6); tx(s, 195, 250, 56, 900, 'InterTight', C.ink, 'center', 'opt' + i); if (on) check(340, 56, 30, 1, sm(sg(t, ts + .3, ts + .7))); }); g.restore(); g.restore(); });
  tag(134, 1125, EXAMPLE, { px: 24, fill: C.wash });
  const ts1 = wt('l6', 6), ts2 = wt('l6', 9);
  ripple(380, 980, t, ts1, C.limeDeep); ripple(800, 990, t, ts2, C.limeDeep);
  pointer(t, { x: 1010, y: 720, t: T.l6 + 1.2 }, [{ x: 380, y: 982, ta: ts1 - .03, tp: ts1 }, { x: 800, y: 992, ta: ts2 - .03, tp: ts2 }], 91, sm(sg(t, T.l6 + 1.2, T.l6 + 1.6)) * (1 - sm(sg(t, wt('l6', 11) + .2, wt('l6', 11) + .55))));
  g.restore();
}
// ===== G: the question (paper) =====
const TB0 = wt('l7', 8) - .05;
function sceneG(t) {
  head(t, [[K('DID', wt('l7', 0)), K('CHATGPT', wt('l7', 1), 'ink')], [K('EVER', wt('l7', 2)), K('ACT', wt('l7', 3)), K('LIKE', wt('l7', 4))], [K("YOU'RE", wt('l7', 5)), K('A', wt('l7', 6)), K('KID?', wt('l7', 7), 'lime')]], 394, 104, 106, { center: true, maxW: 860 });
  deco(t, T.l7 + .8, 940, 640, 'heart', 40, 271);
  if (!enter(t, T.l7 + .15, 540, 940, 'rise', { id: 72, dur: 1.0 })) return;
  g.translate(0, fl(t, 2, 4, 4.4)); sticker(100, 690, 880, 535, 40, C.white, { off: 12, ol: 6 }); tx('Comments', 134, 756, 38, 800, 'InterTight', C.ink, 'left', 'ch'); tag(946, 706, EXAMPLE, { al: 'right', fill: C.wash });
  g.fillStyle = '#ECECE4'; rr(130, 786, 820, 92, 46); g.fill(); g.fillStyle = C.lime; g.beginPath(); g.arc(176, 832, 28, 0, 7); g.fill(); g.lineWidth = 3; g.strokeStyle = C.ink; g.stroke(); icon('user', 176, 832, .64, C.ink);
  const foc = sm(sg(t, TB0 - .3, TB0 + .3)); g.strokeStyle = C.ink; g.lineWidth = 3 + 3 * foc; rr(130, 786, 820, 92, 46); g.stroke();
  tx('Add a comment…', 226, 844, 34, 500, 'Inter', C.mute, 'left', 'ph'); if (foc > .05) caret(214, 806, 52, t, C.ink, 9);
  const yk = wt('l7', 7);
  const btn = (s, x, y, w, fill, t0, kind, hit, id) => { if (!enter(t, t0, x + w / 2, y + 55, kind, { id, dur: .9 })) return; const pk = hit ? bell(t, hit - .08, hit + .1, hit + .55) : 0; g.translate(0, fl(t, x, 3, 3.8));
    sticker(x, y, w, 110, 55, fill, { off: 9, ol: 6, s: 1 + .06 * pk }, () => { tx(s, w / 2, 74, 46, 900, 'InterTight', C.ink, 'center', 'btn:' + s); }); g.restore(); };
  btn('Yes', 130, 915, 390, C.lime, T.l7 + .5, 'sl', yk + .5, 73); btn('No', 560, 915, 390, C.white, T.l7 + .78, 'sr', 0, 74); btn('Tell me below ↓', 130, 1060, 820, C.lime, T.l7 + 1.1, 'rise', TB0 + .4, 75);
  strokePath(roughRect(118, 1048, 844, 134, 76, 40), sinIO(sg(t, TB0 + .5, TB0 + 1.1)), C.ink, 7, 76);
  const ca = sm(sg(t, yk - .6, yk - .25)) * (1 - sm(sg(t, TB0 + .7, TB0 + 1.0)));
  ripple(330, 975, t, yk + .5); ripple(540, 1125, t, TB0 + .4);
  pointer(t, { x: 1000, y: 700, t: yk - .6 }, [{ x: 330, y: 977, ta: yk + .47, tp: yk + .5 }, { x: 540, y: 1127, ta: TB0 + .37, tp: TB0 + .4 }], 101, ca);
  g.restore();
}
// ===== H: link in bio (lime) =====
function sceneH(t) {
  const lk = wt('l8', 4) - .1;
  if (enter(t, T.l8 + .02, 540, 420, 'drop', { id: 81, dur: 1.0 })) { g.translate(0, fl(t, 1, 5, 4));
    sticker(100, 300, 880, 240, 120, C.white, { off: 14, ol: 6, br: .02 }, () => { g.strokeStyle = C.limeDeep; g.lineWidth = 13; g.lineCap = 'round'; rr(104, 94, 96, 52, 26); g.stroke(); rr(160, 118, 96, 52, 26); g.stroke(); tx('Link in bio', 290, 156, 88, 900, 'InterTight', C.ink, 'left', 'linkbio'); underline(t, lk - .3, .5, 292, 178, 800, C.limeDeep, 9, 83); }); g.restore(); }
  const steps = [['Settings', 1, 'sl', 100, 860], ['Account', 2, 'sr', 124, 836], ['Age', 3, 'rise', 90, 890]];
  steps.forEach(([s, n, kind, x0, w0], i) => { const t0 = wt('l8', 1) + i * (.26 + .06 * hs(i, 5)); if (!enter(t, t0, 540, 700 + i * 190 + 75, kind, { id: 85 + i, dur: .9 })) return; g.translate(0, fl(t, i * 2.2, 4, 3.6 + i * .5));
    sticker(x0, 660 + i * 190, w0, 150, 75, i === 2 ? C.wash : C.white, { off: 10, ol: 6 }, () => { tx(s, 190 - (x0 - 100), 100, 62, 900, 'InterTight', C.ink, 'left', 'chip' + i); const cp = p3o(sg(t, lk + .1 + i * (.3 + .05 * i), lk + .55 + i * .3)); if (cp > .01) check(w0 - 70, 75, 34 * cp, cp, sm(sg(t, lk + .25 + i * .3, lk + .7 + i * .3))); }); badge(n, 170 + (x0 - 100) * .2, 735 + i * 190, 44, 1, C.lime); g.restore(); });
  strokePath(roughEllipse(540, 1116, 486, 92, 87, 1.1), sinIO(sg(t, lk + 1.15, lk + 1.85)), C.limeDeep, 9, 87);
  deco(t, lk + .95, 150, 1000 - 460, 'spark', 44, 281); deco(t, lk + 1.45, 940, 1250, 'star', 42, 282);
  ripple(830, 480, t, lk + .05, C.ink);
  pointer(t, { x: 1000, y: 780, t: lk - .7 }, [{ x: 830, y: 478, ta: lk + .02, tp: lk + .05 }], 111, sm(sg(t, lk - .7, lk - .35)) * (1 - sm(sg(t, lk + .6, lk + .95))));
}
// ===== I: the close (paper) =====
const TAP = wt('l9', 10) + .22;
const CF = [TAP, TAP + .43, TAP + .91, TAP + 1.55, TAP + 2.1];
function sceneI(t) {
  head(t, [[K('I', wt('l9', 0)), K('READ', wt('l9', 1)), K('THE', wt('l9', 2))], [K('FINE', wt('l9', 3), 'ink'), K('PRINT', wt('l9', 4), 'ink')], [K('AI', wt('l9', 5)), K('APPS', wt('l9', 6)), K('HOPE', wt('l9', 7))], [K('YOU', wt('l9', 8)), K('SKIP.', wt('l9', 9), 'lime')]], 374, 88, 86, { center: true, maxW: 860 });
  const cards = [['Memory', wt('l9', 3), 'sl', 110, 860], ['Age', wt('l9', 5), 'sr', 92, 884], ['Ads', wt('l9', 6), 'rise', 126, 836]];
  cards.forEach(([s, t0, kind, x0, w0], i) => { const y = 662 + i * 98; if (!enter(t, t0, 540, y + 44, kind, { id: 91 + i, dur: .85 })) return; g.translate(0, fl(t, i * 2.1, 4, 3.4 + i * .5));
    sticker(x0, y, w0, 88, 44, i === 1 ? C.lime : C.white, { off: 8, ol: 5 }, () => { tx(s, 44, 60, 44, 900, 'InterTight', C.ink, 'left', 'ai' + i); }); const tg = sinIO(sg(t, wt('l9', 7) + i * (.2 + .05 * i), wt('l9', 7) + .55 + i * .25)); toggle(x0 + 650, y + 14, true, tg); g.restore(); });
  const ta = sm(sg(t, wt('l9', 6) + .2, wt('l9', 6) + .6)); if (ta > .003) { g.save(); g.globalAlpha *= ta; tag(110, 954, EXAMPLE, { px: 24, fill: C.wash }); g.restore(); }
  deco(t, wt('l9', 9), 930, 318, 'star', 44, 291);
  // Follow button: eases up with the word, one tap, then it changes to Following and the confetti keeps coming in loose waves
  const fo = T.l9 + .15;
  if (enter(t, fo, 540, 1105, 'zoom', { id: 95, dur: 1.0 })) { const done = sm(sg(t, TAP + .02, TAP + .3)), s = 1 + .02 * V(.03) + .1 * Math.sin(Math.PI * clamp((t - TAP) / .7)) * (t > TAP ? 1 : 0); g.translate(0, fl(t, 6, 4, 3.9));
    sticker(190, 1032, 700, 150, 75, done > .5 ? C.white : C.lime, { off: 12, ol: 6, s, br: .02 }, () => { if (done > .5) { check(110, 75, 40, 1, 1); tx('Following', 410, 98, 66, 900, 'InterTight', C.ink, 'center', 'follow'); } else tx('Follow', 350, 100, 72, 900, 'InterTight', C.ink, 'center', 'follow'); });
    g.restore(); }
  CF.forEach((T1, wv) => { if (t < T1) return; const R = rng(5 + wv * 9), n = wv < 3 ? 16 : 9; for (let i = 0; i < n; i++) { const ang = R() * 6.283, sp = 140 + R() * 280, life = 1.1 + R() * .9, u = t - T1 - R() * .12, e = 1 - Math.exp(-Math.max(0, u) * 2.2); if (u < 0 || u > life) continue;
    g.save(); g.globalAlpha *= sm(u / .1) * (1 - sm(sg(u, life * .55, life))) * .95; g.fillStyle = i % 3 ? C.lime : C.ink; g.strokeStyle = C.ink; g.lineWidth = 3; g.beginPath(); g.arc(540 + Math.cos(ang) * sp * e, 1107 + Math.sin(ang) * sp * e * .8 + 60 * u * u, (i % 3 ? 11 : 6) * (.8 + .4 * hs(i, wv)), 0, 7); g.fill(); if (i % 3) g.stroke(); g.restore(); } });
  flash(540, 1107, t, TAP, 420, '182,242,58');
  ripple(600, 1125, t, TAP, C.ink); ripple(600, 1125, t, TAP + .5, C.ink);
  pointer(t, { x: 1000, y: 780, t: TAP - .9 }, [{ x: 600, y: 1122, ta: TAP - .02, tp: TAP }], 121, sm(sg(t, TAP - .9, TAP - .5)) * (1 - sm(sg(t, TAP + .3, TAP + .7))));
  head(t, [[K('AND', wt('l9', 11)), K('YOU', wt('l9', 12)), K("WON'T", wt('l9', 13)), K('HAVE', wt('l9', 14)), K('TO.', wt('l9', 15), 'lime')]], 1234, 54, 60, { center: true, maxW: 860 });
}
// ===== scene list + transition engine: a different organic entrance for every scene =====
const SC = [
  { n: 1, t0: 0, tone: 'paper', draw: sceneA },
  { n: 2, t0: t0s(2), tone: 'lime', draw: sceneB, tr: { type: 'wipe', dur: .6, ang: .42 } },
  { n: 3, t0: t0s(3), tone: 'paper', draw: sceneC, tr: { type: 'slide', dur: .72, dx: -1, dy: 0 } },
  { n: 4, t0: t0s(4), tone: 'lime', draw: sceneD, tr: { type: 'peel', dur: .8, corner: 'br' } },
  { n: 5, t0: t0s(5), tone: 'paper', draw: sceneE, tr: { type: 'grow', dur: .62, from: [100, 1030, 880, 150, 75] } },
  { n: 6, t0: t0s(6), tone: 'wash', draw: sceneF, tr: { type: 'fade', dur: .55 } },
  { n: 7, t0: t0s(7), tone: 'paper', draw: sceneG, tr: { type: 'slide', dur: .68, dx: 0, dy: -1 } },
  { n: 8, t0: t0s(8), tone: 'lime', draw: sceneH, tr: { type: 'wipe', dur: .58, ang: 2.75 } },
  { n: 9, t0: t0s(9), tone: 'paper', draw: sceneI, tr: { type: 'peel', dur: .75, corner: 'bl' } },
];
function drawScene(s, t) { setTone(s.tone); NOW = t; bg(s.tone, t); s.draw(t); }
const M = 140;
function doWipe(t, u, p, s, o) {
  const e = ioE(u), dx = Math.cos(o.ang), dy = Math.sin(o.ang), px = -dy, py = dx, cs = [[-M, -M], [W + M, -M], [W + M, H + M], [-M, H + M]].map(c => c[0] * dx + c[1] * dy), s0 = Math.min(...cs) - 80, s1 = Math.max(...cs) + 80, sp = lerp(s0, s1, e);
  const edge = []; for (let k = 0; k <= 18; k++) { const q = k / 18, along = (q - .5) * 3600, wob = 26 * nz(300 + s.n, q * 5.5 + u * 1.2) + 12 * nz(310 + s.n, q * 13); edge.push([dx * (sp + wob) + px * along, dy * (sp + wob) + py * along]); }
  drawScene(p, t);
  g.save(); g.beginPath(); edge.forEach((q, i) => i ? g.lineTo(q[0], q[1]) : g.moveTo(q[0], q[1])); g.lineTo(edge[18][0] - dx * 4000, edge[18][1] - dy * 4000); g.lineTo(edge[0][0] - dx * 4000, edge[0][1] - dy * 4000); g.closePath(); g.clip(); drawScene(s, t); g.restore();
  const band = edge.map(q => [q[0] + dx * 46, q[1] + dy * 46]), fade = 1 - sm(sg(u, .9, 1));
  g.save(); g.globalAlpha *= fade; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); band.forEach((q, i) => i ? g.lineTo(q[0], q[1]) : g.moveTo(q[0], q[1])); g.strokeStyle = C.ink; g.lineWidth = 118; g.stroke(); g.strokeStyle = C.lime; g.lineWidth = 98; g.stroke(); g.restore();
}
function doSlide(t, u, p, s, o) {
  const e = ioE(u), ox = -o.dx * (1 - e) * (W + 2 * M) * .0 , nxo = -o.dx * (1 - e) * W, nyo = -o.dy * (1 - e) * H;
  g.save(); g.translate(o.dx * e * W * .5, o.dy * e * H * .5); const sc = 1 - .04 * e; g.translate(540, 960); g.scale(sc, sc); g.translate(-540, -960); drawScene(p, t); g.fillStyle = `rgba(0,0,0,${.14 * e})`; g.fillRect(-M, -M, W + 2 * M, H + 2 * M); g.restore();
  g.save(); g.beginPath(); g.rect(nxo - M, nyo - M, W + 2 * M, H + 2 * M); g.clip(); g.translate(nxo, nyo); drawScene(s, t); g.restore();
  const ex = nxo - (o.dx < 0 ? 0 : 0), a = .22 * (1 - e) + .04; g.save(); const gr = o.dx ? g.createLinearGradient(nxo + (o.dx < 0 ? 0 : W) , 0, nxo + (o.dx < 0 ? -90 : W + 90), 0) : g.createLinearGradient(0, nyo + (o.dy < 0 ? 0 : H), 0, nyo + (o.dy < 0 ? -90 : H + 90));
  gr.addColorStop(0, `rgba(0,0,0,${a})`); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(-M, -M, W + 2 * M, H + 2 * M); g.restore();
}
function doPeel(t, u, p, s, o) {
  const e = ioE(u), br = o.corner === 'br', c = br ? [W + M, H + M] : [-M, H + M], oo = br ? [-M, -M] : [W + M, -M]; let nx = c[0] - oo[0], ny = c[1] - oo[1]; const L = Math.hypot(nx, ny); nx /= L; ny /= L;
  const dc = c[0] * nx + c[1] * ny, dO = oo[0] * nx + oo[1] * ny, f = lerp(dc + 6, dO - 30, e), bx = nx * f, by = ny * f, tx_ = -ny, ty_ = nx, B = 4000;
  const half = (sgn) => { g.beginPath(); g.moveTo(bx + tx_ * B, by + ty_ * B); g.lineTo(bx - tx_ * B, by - ty_ * B); g.lineTo(bx - tx_ * B + sgn * nx * B, by - ty_ * B + sgn * ny * B); g.lineTo(bx + tx_ * B + sgn * nx * B, by + ty_ * B + sgn * ny * B); g.closePath(); };
  drawScene(s, t);
  g.save(); const sh = g.createLinearGradient(bx, by, bx + nx * 110, by + ny * 110); sh.addColorStop(0, `rgba(0,0,0,${.32 * Math.sin(Math.PI * clamp(u))})`); sh.addColorStop(1, 'rgba(0,0,0,0)'); half(1); g.clip(); g.fillStyle = sh; g.fillRect(-M, -M, W + 2 * M, H + 2 * M); g.restore();
  g.save(); half(-1); g.clip(); drawScene(p, t); g.restore();
  g.save(); half(-1); g.clip(); g.transform(1 - 2 * nx * nx, -2 * nx * ny, -2 * nx * ny, 1 - 2 * ny * ny, 2 * f * nx, 2 * f * ny); g.beginPath(); g.rect(-M, -M, W + 2 * M, H + 2 * M); g.clip(); drawScene(p, t);
  g.fillStyle = 'rgba(247,247,240,.72)'; g.fillRect(-M, -M, W + 2 * M, H + 2 * M); const cg = g.createLinearGradient(bx, by, bx + nx * 260, by + ny * 260); cg.addColorStop(0, 'rgba(0,0,0,.2)'); cg.addColorStop(.25, 'rgba(255,255,255,.18)'); cg.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = cg; g.fillRect(-M, -M, W + 2 * M, H + 2 * M); g.restore();
}
function doGrow(t, u, p, s, o) {
  const e = ioE(u), F0 = o.from, fx = F0[0] + F0[2] / 2, fy = F0[1] + F0[3] / 2;
  g.save(); g.translate(fx, fy); g.scale(1 + .1 * e, 1 + .1 * e); g.translate(-fx, -fy); drawScene(p, t); g.restore();
  const rx = lerp(F0[0], -M, e), ry = lerp(F0[1], -M, e), rw = lerp(F0[2], W + 2 * M, e), rh = lerp(F0[3], H + 2 * M, e), rrad = lerp(F0[4], 0, e);
  g.save(); rr(rx, ry, rw, rh, rrad); g.clip(); g.translate(fx, fy); g.scale(1.06 - .06 * e, 1.06 - .06 * e); g.translate(-fx, -fy); drawScene(s, t); g.restore();
  g.save(); g.lineWidth = 8 * (1 - e) + 1; g.strokeStyle = C.ink; rr(rx, ry, rw, rh, rrad); g.stroke(); g.restore();
}
function doFade(t, u, p, s) {
  const e = sinIO(u); g.save(); g.translate(540, 960); g.scale(1 + .035 * e, 1 + .035 * e); g.translate(-540, -960); drawScene(p, t); g.restore();
  g.save(); g.globalAlpha = sm(u * 1.15); g.translate(540, 960); g.scale(1.03 - .03 * e, 1.03 - .03 * e); g.translate(-540, -960); drawScene(s, t); g.restore();
}
const TRF = { wipe: doWipe, slide: doSlide, peel: doPeel, grow: doGrow, fade: doFade };
function draw(t) {
  g.setTransform(1, 0, 0, 1, 0, 0); TXT.length = 0; NOW = t;
  const [z, px, py, rot] = cam(t); PARX = px; PARY = py;
  g.save(); g.translate(540 + px, 960 + py); g.rotate(rot); g.scale(z, z); g.translate(-540, -960);
  let i = 0; for (let k = 0; k < SC.length; k++) if (t >= SC[k].t0) i = k;
  const s = SC[i], u = i > 0 ? (t - s.t0) / s.tr.dur : 2;
  if (u >= 1) drawScene(s, t); else TRF[s.tr.type](t, u, SC[i - 1], s, s.tr);
  g.restore();
}
window.TRANS = SC.slice(1).map(s => [s.t0 - .02, s.t0 + s.tr.dur + .02]);
window.render = (t) => { REC = false; draw(t); };
window.TEXTS = (t) => { REC = true; draw(t); REC = false; return TXT.map(o => ({ ...o })); };
window.BIGT = () => [...BIG.values()].sort((a, b) => a - b);
// ---- impacts (soft pushes) and sound events, all from cue times ----
addShake(HT, 16); addShake(tw1(7), 6); addShake(SB_(), 8); addShake(NEWS_IN + .12, 16); addShake(Math.min(wt('l4', 3) - .05, T.l4 + .5), 4); addShake(wt('l4', 7) - .1, 5); addShake(wt('l4', 7) + .45, 4);
addShake(l5s[1], 4); addShake(l5s[2], 7); addShake(wt('l6', 6), 6); addShake(wt('l6', 9), 6); addShake(wt('l6', 11), 9); addShake(wt('l7', 7), 5); addShake(TB0, 6); addShake(T.l8 + .1, 7); addShake(TAP, 8);
for (let n = 2; n <= 9; n++) addShake(t0s(n) + SC[n - 1].tr.dur * .55, 4);
function SB_() { return BDEND + .12; }
window.EV = [{ t: .25, type: 'tick' }, { t: HT, type: 'crash' }, { t: HT + .05, type: 'thud' }, { t: tw1(7), type: 'thud' }, { t: SB_() + .1, type: 'thud' }, { t: NEWS_IN + .12, type: 'thud' }, { t: NEWS_IN + .75, type: 'thud' },
  { t: Math.min(wt('l4', 3) - .05, T.l4 + .5), type: 'click' }, { t: wt('l4', 7) - .1, type: 'click' }, { t: wt('l4', 7) + .45, type: 'click' }, { t: l5s[1], type: 'click' }, { t: l5s[2], type: 'click' }, { t: l5s[2] + .2, type: 'ding' },
  { t: wt('l6', 6), type: 'click' }, { t: wt('l6', 9), type: 'click' }, { t: wt('l6', 11), type: 'ding' }, { t: wt('l7', 7) + .5, type: 'click' }, { t: TB0 + .4, type: 'click' }, { t: T.l8 + .1, type: 'thud' }, { t: wt('l8', 1), type: 'click' }, { t: wt('l8', 1) + .3, type: 'click' }, { t: wt('l8', 1) + .6, type: 'click' }, { t: wt('l9', 3), type: 'click' }, { t: wt('l9', 5), type: 'click' }, { t: wt('l9', 6), type: 'click' }, { t: TAP, type: 'ding' }]
  .concat(typePlan(QS, 0, 1, 2).length ? QP.filter((_, i) => i % 9 === 0).map(o => ({ t: o.t, type: 'tap' })) : [])
  .concat(Array.from({ length: 8 }, (_, k) => ({ t: t0s(k + 2) - .02, type: 'whoosh' })));
window.READY = true;
