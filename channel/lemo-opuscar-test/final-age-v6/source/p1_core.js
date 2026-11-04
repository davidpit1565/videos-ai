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
