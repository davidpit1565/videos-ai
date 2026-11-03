// ChatGPT age-prediction film (final). Canvas 2D, pure function of t. Channel identity: light paper + quiet dot grid, ink type, dark UI cards, lime accent, sticker components.
// The real-screen proof is a SLOT: proof.json (image path, caption, zoom, pan, rings). Swap the file + rings, rebuild with `sh build3.sh`.
const W = 1080, H = 1920;
const cv = document.getElementById('c'); let g = cv.getContext('2d');
await Promise.all([700, 800, 900, 600, 500].flatMap(w => [`${w} 40px Inter`, `${w} 40px InterTight`, `${w} 40px JBMono`]).map(f => document.fonts.load(f)));
const get = async (u, d) => { try { const r = await fetch(u); return r.ok ? await r.json() : d; } catch { return d; } };
const WD = await get('voices/words.json', {});
const DJ = await get('voices/dur.json', {});
const IMG = async u => createImageBitmap(await (await fetch(u)).blob());
const TR = await IMG('tr.png'), TC = await IMG('tc.png'), TB = await IMG('trb.png');
const svg = await (await fetch('chatgpt.svg')).text();
const MARK = new Path2D(svg.match(/ d='([^']+)'/)[1]);
const C = { paper: '#F4F4EF', dot: '#E0E0D6', ink: '#0E0E0E', ink2: '#4B4B46', dark: '#14151A', dark2: '#22242C', dark3: '#2E3039', lime: '#B6F23A', limeDeep: '#4E8F0B', wash: '#E4F8B0', white: '#FFFFFF', mute: '#8E908A' };
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const sg = (t, a, b) => clamp((t - a) / (b - a));
const sm = x => { x = clamp(x); return x * x * x * (x * (x * 6 - 15) + 10); };         // smootherstep
const enterE = x => 1 - Math.pow(1 - clamp(x), 4);                                      // long ease-out, no overshoot
const expoE = x => { x = clamp(x); return x >= 1 ? 1 : 1 - Math.pow(2, -10 * x); };
const lerp = (a, b, t) => a + (b - a) * t;
const rng = s => () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
const GAP = .22, T = {}; { let c = .3; for (const k of ['l1','l2','l3','l4','l5','l6','l7','l8','l9']) { T[k] = c; c += DJ[k] + GAP; } }
const wt = (l, i) => T[l] + Math.max(0, WD[l][i][1]);                                        // spoken start of word i of line l (lead-in clamp: a negative stamp is silence, not speech)
const DUR = Math.ceil((T.l9 + DJ.l9 + .35) * 10) / 10; window.DUR = DUR;
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
const fl = (t, ph, amp = 5, per = 5) => Math.sin(t * 6.283 / per + ph) * amp;      // ambient float, each element its own phase/period
// ---------- sticker components ----------
function sticker(x, y, w, h, r, fill, o = {}, fn) {   // thick outline + hard offset shadow, optional local content
  g.save(); g.translate(x + w / 2, y + h / 2); g.rotate(o.rot || 0); g.scale(o.s || 1, o.s || 1); g.translate(-w / 2, -h / 2);
  const off = o.off ?? 8; g.fillStyle = C.ink; rr(off, off, w, h, r); g.fill();
  g.fillStyle = fill; rr(0, 0, w, h, r); g.fill(); g.lineWidth = o.ol ?? 4; g.strokeStyle = C.ink; rr(0, 0, w, h, r); g.stroke();
  if (fn) fn(); g.restore();
}
function dcard(x, y, w, h, r = 34) {   // dark UI card
  g.save(); g.shadowColor = 'rgba(14,14,14,.28)'; g.shadowBlur = 44; g.shadowOffsetY = 18; g.fillStyle = C.dark; rr(x, y, w, h, r); g.fill(); g.restore();
  g.lineWidth = 2; g.strokeStyle = C.dark3; rr(x, y, w, h, r); g.stroke();
}
function tag(x, y, s, o = {}) {   // sticker chip (mono). default 26px = readable at phone size
  const px = o.px || 26; g.font = F(px, 700, 'JBMono'); const w = g.measureText(s).width + 36, h = px + 24;
  const x0 = o.al === 'right' ? x - w : x;
  sticker(x0, y, w, h, h / 2, o.fill || C.white, { rot: o.rot || 0, ol: 3, off: 5, s: o.s || 1 }, () => { tx(s, 18, h / 2 + px * .34, px, 700, 'JBMono', o.col || C.ink, 'left', 'tag:' + s); });
  return w;
}
function badge(n, cx, cy, r, s = 1, fill = C.lime) {   // numbered round badge
  g.save(); g.translate(cx, cy); g.scale(s, s);
  g.fillStyle = C.ink; g.beginPath(); g.arc(7, 7, r, 0, 7); g.fill();
  g.fillStyle = fill; g.beginPath(); g.arc(0, 0, r, 0, 7); g.fill(); g.lineWidth = 4; g.strokeStyle = C.ink; g.stroke();
  tx(String(n), 0, r * .36, r * 1.05, 900, 'InterTight', C.ink, 'center', 'badge' + n); g.restore();
}
function mark(x, y, s, col = C.ink) { g.save(); g.translate(x, y); g.scale(s / 320, s / 320); g.fillStyle = col; g.fill(MARK); g.restore(); }
function logoBadge(x, y, s, sc = 1, rot = 0) {   // real ChatGPT mark alone, in a white sticker square (no caption)
  sticker(x, y, s, s, s * .26, C.white, { rot, s: sc, off: 8 }, () => { g.save(); g.translate(s * .16, s * .16); mark(0, 0, s * .68); g.restore(); });
}
function check(cx, cy, r, p = 1) {
  g.save(); g.globalAlpha *= p; g.fillStyle = C.lime; g.beginPath(); g.arc(cx, cy, r, 0, 7); g.fill(); g.lineWidth = 3; g.strokeStyle = C.ink; g.stroke();
  g.lineCap = 'round'; g.lineJoin = 'round'; g.lineWidth = 4; g.beginPath(); g.moveTo(cx - r * .4, cy); g.lineTo(cx - r * .1, cy + r * .32); g.lineTo(cx + r * .44, cy - r * .3); g.stroke(); g.restore();
}
function cursor(x, y, s = 1, press = 0) {
  g.save(); g.translate(x, y); g.scale(s * (1 - .1 * press), s * (1 - .1 * press)); g.fillStyle = C.ink; g.strokeStyle = '#fff'; g.lineWidth = 3.5;
  g.beginPath(); g.moveTo(0, 0); g.lineTo(0, 40); g.lineTo(11, 31); g.lineTo(19, 49); g.lineTo(27, 45); g.lineTo(19, 28); g.lineTo(33, 28); g.closePath(); g.stroke(); g.fill(); g.restore();
}
function ripple(x, y, t, t0, col = C.ink) { const u = (t - t0) / .9; if (u < 0 || u > 1) return; g.save(); g.globalAlpha *= (1 - u) * .7; g.strokeStyle = col; g.lineWidth = 5; g.beginPath(); g.arc(x, y, 14 + 70 * enterE(u), 0, 7); g.stroke(); g.restore(); }
// scene envelope: opaque within 0.22 s (no half-transparent grey cards), exits in <= 0.17 s
const ev = (t, t0, t1, din = .42, dout = .17) => {
  const p = enterE(sg(t, t0, t0 + din)), q = sm(sg(t, t1, t1 + dout));
  return { a: sm(sg(t, t0, t0 + .13)) * (1 - q), dy: (1 - p) * 44 + q * -16, s: .965 + .035 * p, on: t >= t0 && t < t1 + dout };
};
function wrap(e, fn, cx = 540, cy = 760) { if (e.a <= .003) return; g.save(); g.globalAlpha *= e.a; g.translate(cx, cy + e.dy); g.scale(e.s, e.s); g.translate(-cx, -cy); fn(); g.restore(); }
// ---------- headline: key words in pills. whole:true = full line visible from frame 0, pills form as the words are spoken ----------
// token {s, t, k}: k = '' plain | 'ink' black pill (white text) | 'limeink' black pill (lime text) | 'lime' lime pill, thick outline + hard shadow
function head(t, rows, x, y0, px, lh, o = {}) {
  const fam = 'InterTight';
  const widthOf = (row, f) => { g.font = F(f, 900, fam); return row.reduce((a, k, i) => a + g.measureText(k.s).width + (k.k ? f * .5 : 0) + (i ? f * .25 : 0), 0); };
  let S = 1; rows.forEach(r => { S = Math.min(S, (o.maxW || 860) / widthOf(r, px)); });
  const f = px * S;
  rows.forEach((row, ri) => {
    const rw = widthOf(row, f); let cx = o.center ? 540 - rw / 2 : x; const y = y0 + ri * lh * S;
    row.forEach((k, i) => {
      g.font = F(f, 900, fam); const tw = g.measureText(k.s).width, pad = k.k ? f * .25 : 0, bw = tw + pad * 2;
      if (i) cx += f * .25;
      const dl = o.whole ? .5 : .5 + .1 * (((i * 7 + ri * 3 + k.s.length) % 5) / 4);
      const u = (t - (k.t - .09)) / dl, p = o.whole ? 1 : enterE(u), a = o.whole ? 1 : sm(u * 1.9);
      const bp = k.k ? enterE(u * (o.whole ? 1.5 : 1.15)) : 0;
      if (a > .003) {
        g.save(); g.globalAlpha *= a;
        g.translate(cx + bw / 2, y - f * .3 + (1 - p) * f * .5); g.rotate((1 - p) * (((i + ri) % 2) ? .05 : -.05)); const sc = o.whole ? 1 + (k.k ? .06 : .1) * Math.sin(Math.PI * clamp((t - k.t) / .4)) : ((k.k ? .88 : .94) + (k.k ? .12 : .06) * p); g.scale(sc, sc); g.translate(-bw / 2, f * .3);
        if (k.k && bp > .02) {
          const top = -f * .86, hh = f * 1.06;
          if (k.k === 'lime') { g.fillStyle = C.ink; rr(f * .08, top + f * .08, bw * bp, hh, f * .26); g.fill(); g.fillStyle = C.lime; rr(0, top, bw * bp, hh, f * .26); g.fill(); g.lineWidth = Math.max(4, f * .05); g.strokeStyle = C.ink; rr(0, top, bw * bp, hh, f * .26); g.stroke(); }
          else { g.fillStyle = C.ink; rr(0, top, bw * bp, hh, f * .26); g.fill(); }
        }
        const lit = !o.whole || bp > .4;
        const col = (k.k === 'ink' && lit) ? '#fff' : (k.k === 'limeink' && lit) ? C.lime : C.ink;
        g.font = F(f, 900, fam); g.fillStyle = col; g.textAlign = 'left'; g.textBaseline = 'alphabetic'; g.fillText(k.s, pad, 0);
        reg('h:' + k.s + ri + i, k.s, pad, -f * .78, pad + tw, f * .05);
        g.restore();
      }
      cx += bw;
    });
  });
}
const K = (s, t, k = '') => ({ s, t, k });
// ---------- background: paper + quiet drifting dot grid (like ep 82), a few lime dots ----------
function background(t) {
  g.fillStyle = C.paper; g.fillRect(-300, -300, W + 600, H + 600);
  const ox = -(t * 16) % 54, oy = (t * 10) % 54; g.fillStyle = C.dot;
  for (let x = -108; x < W + 160; x += 54) for (let y = -108; y < H + 160; y += 54) { g.beginPath(); g.arc(x + ox, y + oy, 2.1, 0, 7); g.fill(); }
}
function sparkles(t) {   // 4 small lime dots/rings only, behind everything
  const R = rng(11); g.save(); g.globalAlpha *= .8;
  for (let i = 0; i < 4; i++) {
    const bx = 80 + R() * 920, by = 300 + R() * 900, sp = .35 + R() * .5, ph = R() * 6.28;
    const x = bx + Math.sin(t * sp + ph) * 30, y = by + Math.cos(t * sp * .8 + ph) * 36;
    g.lineWidth = 3.5; g.strokeStyle = C.ink; g.fillStyle = C.lime; g.beginPath(); g.arc(x, y, i % 2 ? 8 : 7, 0, 7); if (i % 2) g.stroke(); else { g.fill(); g.stroke(); }
  }
  g.restore();
}
// ---------- camera: never stops; slow zoom + pan on several sines ----------
function cam(t) {
  const z = 1.018 + .012 * Math.sin(t * .83 + .5) + .006 * Math.sin(t * 1.9 + 2), x = 540 + 14 * Math.sin(t * .56) + 6 * Math.sin(t * 1.35 + 1), y = 758 + 9 * Math.sin(t * .47 + 1);
  return [z, 540, 758, x - 540, y - 758];
}
// ---------- extra helpers ----------
function typed(s, p) { return s.slice(0, Math.floor(s.length * clamp(p))); }
const typeP = (t, a, b, seed = 1) => { const u = sg(t, a, b); return clamp(u + .03 * Math.sin(u * 19 + seed) * u * (1 - u) * 4); };
function caret(x, y, h, t, col = C.lime) { const a = .55 + .45 * Math.sin(t * 6.283 * 1.0); g.fillStyle = col; g.globalAlpha *= a; g.fillRect(x, y, 4, h); g.globalAlpha /= a; }
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
function toggle(x, y, on, p = 1) {   // sticker toggle switch, p = 0..1 knob travel
  const w = 120, h = 60; g.save(); g.translate(x, y);
  g.fillStyle = C.ink; rr(5, 5, w, h, 30); g.fill();
  g.fillStyle = p > .5 ? C.lime : C.white; rr(0, 0, w, h, 30); g.fill(); g.lineWidth = 4; g.strokeStyle = C.ink; rr(0, 0, w, h, 30); g.stroke();
  g.fillStyle = C.ink; g.beginPath(); g.arc(30 + 60 * p, 30, 18, 0, 7); g.fill(); g.restore();
}
function scaleTag(t) { return t; }
// generic shatter: cv is the offscreen picture of the object (w x h), flying shards
function mkCv(w, h, fn) { const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const keep = g, kr = REC; REC = false; g = cv.getContext('2d'); fn(); g = keep; REC = kr; return cv; }
function shardsG(t, t0, cv, w, h, cols, rows, ix, iy, seed = 21) {
  const R = rng(seed), cw = w / cols, ch = h / rows, pts = [];
  for (let j = 0; j <= rows; j++) { pts[j] = []; for (let i = 0; i <= cols; i++) pts[j][i] = [i * cw + ((i > 0 && i < cols) ? (R() - .5) * cw * .6 : 0), j * ch + ((j > 0 && j < rows) ? (R() - .5) * ch * .6 : 0)]; }
  const u = t - t0;
  for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) {
    const a = pts[j][i], b = pts[j][i + 1], c = pts[j + 1][i + 1], d = pts[j + 1][i];
    [[a, b, c], [a, c, d]].forEach(tri => {
      const cx = (tri[0][0] + tri[1][0] + tri[2][0]) / 3, cy = (tri[0][1] + tri[1][1] + tri[2][1]) / 3;
      let dx = cx - ix, dy = cy - iy; const L = Math.hypot(dx, dy) + 1; dx /= L; dy /= L;
      const sp = 300 + R() * 640 + 560 / (1 + L / 90), rot = (R() - .5) * 9, delay = L / 3600;
      const uu = Math.max(0, u - delay), e = 1 - Math.exp(-uu * 2.4);
      const px = dx * sp * e / 2.4, py = dy * sp * e / 2.4 + 500 * uu * uu;
      const al = 1 - sm(sg(uu, .5, 1.05));
      if (al < .01) return;
      g.save(); g.globalAlpha *= al; g.translate(cx + px, cy + py); g.rotate(rot * e * .7); g.translate(-cx, -cy);
      g.beginPath(); g.moveTo(tri[0][0], tri[0][1]); g.lineTo(tri[1][0], tri[1][1]); g.lineTo(tri[2][0], tri[2][1]); g.closePath();
      g.save(); g.clip(); g.drawImage(cv, 0, 0); g.restore();
      g.lineWidth = 2.5; g.strokeStyle = 'rgba(182,242,58,.7)'; g.stroke(); g.restore();
    });
  }
}
function ring(x, y, t, t0, dur = .6, col = C.lime, big = 380) {
  const u = (t - t0) / dur; if (u < 0 || u > 1) return;
  g.save(); g.translate(x, y); g.globalAlpha *= (1 - u) * .9; g.strokeStyle = col; g.lineWidth = 16 * (1 - u) + 3; g.beginPath(); g.arc(0, 0, 40 + big * expoE(u), 0, 7); g.stroke();
  g.globalAlpha *= .5; g.strokeStyle = C.ink; g.lineWidth = 4; g.beginPath(); g.arc(0, 0, 20 + (big + 40) * expoE(u), 0, 7); g.stroke(); g.restore();
}
function stamp(text, cx, cy, px, rot, s, a, col = C.limeDeep, id = 'stamp') {
  if (a < .003) return; g.save(); g.globalAlpha *= a; g.translate(cx, cy); g.rotate(rot); g.scale(s, s);
  g.font = F(px, 900, 'InterTight'); const w = g.measureText(text).width + px * .9, h = px * 1.8;
  g.fillStyle = 'rgba(255,255,255,.97)'; rr(-w / 2, -h / 2, w, h, 16); g.fill(); g.lineWidth = 6; g.strokeStyle = col; rr(-w / 2, -h / 2, w, h, 16); g.stroke(); g.lineWidth = 2; rr(-w / 2 + 8, -h / 2 + 8, w - 16, h - 16, 10); g.stroke();
  tx(text, 0, px * .36, px, 900, 'InterTight', col, 'center', id); g.restore();
}
const EXIT = .17;
// ---------- timeline ----------
const HT = wt('l1', 7) - .1;                 // hero beat: "teen" spoken
const PROF_OUT = T.l2 + .3;                  // profile card leaves
const L2_OUT = T.l3 - .2;                    // l2 scene leaves
const NEWS_IN = T.l3 - .03, NEWS_OUT = NEWS_IN + 3.32;   // TechRadar card on screen 3.3 s
const l5s = [T.l5 + 1.08, T.l5 + 1.5, T.l5 + 1.9];     // Settings, Account, Age (measured on the voice envelope)
const TAP = T.l9 + 3.5;
// ---------- scene A: the claim + profile card, hero beat ----------
function ageFace(label, fill, fg) { sticker(0, 0, 390, 140, 38, fill, { off: 9, ol: 6 }, () => { tx(label, 195, 98, 84, 900, 'InterTight', fg, 'center', 'badge:' + label); }); }
const FACE_ADULT = mkCv(412, 162, () => ageFace('ADULT', C.lime, C.ink));
function sceneA(t) {
  const lo = 1 - sm(sg(t, T.l2 - .2, T.l2 - .2 + EXIT));
  if (lo > .003) { g.save(); g.globalAlpha *= lo; logoBadge(100, 288, 100, 1, -.06 + .02 * Math.sin(t * 1.5)); g.restore(); }
  const hOut = 1 - sm(sg(t, T.l2 - .2, T.l2 - .2 + EXIT));
  if (hOut > .003) { g.save(); g.globalAlpha *= hOut; g.translate(0, -sm(sg(t, T.l2 - .2, T.l2)) * 16 + fl(t, 0, 5, 2.4));
    head(t, [[K('ADULT?', T.l1 + .35, 'lime')], [K('CHATGPT', wt('l1', 1)), K('MAY', wt('l1', 3))], [K('CALL', wt('l1', 4)), K('YOU', wt('l1', 5))], [K('A', wt('l1', 6)), K('TEEN!', wt('l1', 7), 'ink')]], 100, 520, 118, 120, { maxW: 840, whole: true }); g.restore(); }
  // profile card
  const po = 1 - sm(sg(t, PROF_OUT, PROF_OUT + EXIT)); if (po < .003) return;
  const u = t - HT, shake = u > 0 && u < .35 ? Math.sin(t * 85) * 7 * (1 - u / .35) : 0;
  g.save(); g.globalAlpha *= po; g.translate(100 + shake, 940 + fl(t, 0, 7, 4.6) + sm(sg(t, PROF_OUT, PROF_OUT + EXIT)) * 30); g.rotate(-.01 + .006 * Math.sin(t * .9));
  dcard(0, 0, 880, 290, 38);
  tag(850, 20, 'example · re-created', { al: 'right', fill: C.wash });
  g.fillStyle = C.lime; g.beginPath(); g.arc(112, 160, 62, 0, 7); g.fill(); g.lineWidth = 5; g.strokeStyle = C.ink; g.stroke(); icon('user', 112, 160, 1.5);
  tx('Your account', 200, 150, 38, 800, 'InterTight', '#fff', 'left', 'acct'); tx('birth year 1996', 200, 200, 30, 600, 'Inter', '#BFC2B4', 'left', 'born');
  g.save(); g.translate(450, 90);
  if (u < 0) { g.translate(0, fl(t, 3, 3, 2.2)); g.drawImage(FACE_ADULT, 0, 0); tx('ADULT', 195, 98, 84, 900, 'InterTight', C.ink, 'center', 'badgeA'); }
  else {
    // shards of the old ADULT badge (picture only; text of the live badge is not drawn after the beat)
    shardsG(t, HT, FACE_ADULT, 412, 162, 6, 3, 205, 80);
    const k = enterE(sg(u, .06, .5)), sc = 1 + 1.35 * (1 - k), a = sm(sg(u, .06, .2));
    g.save(); g.globalAlpha *= a; g.translate(195, 70 + fl(t, 3, 3, 2.2)); g.rotate(-.1 * (1 - k) + .02 * Math.sin(t * 1.3)); g.scale(sc, sc); g.translate(-195, -70);
    ageFace('TEEN', C.ink, C.lime); g.restore();
  }
  g.restore();
  ring(450 + 195, 90 + 70, t, HT + .06, .65, C.lime, 330);
  g.restore();
}
// ---------- scene B: birthday typed in + OpenAI quote ----------
const QUOTE = [['“It can identify an account as eligible', 0], ['for the ChatGPT for Teens experience', 0], ['even if you already gave your date of', 1], ['birth when you created your account.”', 2]];
function sceneB(t) {
  const T0 = T.l2 - .03;
  wrap(ev(t, T0, L2_OUT, .4, EXIT), () => {
    head(t, [[K('It', wt('l2', 0)), K('can', wt('l2', 1)), K('happen', wt('l2', 2)), K('even', wt('l2', 3))], [K('with', wt('l2', 4)), K('a', wt('l2', 5)), K('birthday', wt('l2', 6), 'ink'), K('typed', wt('l2', 7)), K('in.', wt('l2', 8), 'lime')]], 100, 348, 92, 100, { maxW: 860 });
    // birthday card
    const b0 = enterE(sg(t, T.l2 + .3, T.l2 + .75));
    g.save(); g.translate(0, (1 - b0) * 40 + fl(t, 2, 5, 4.4)); g.globalAlpha *= sm(b0 * 1.6);
    dcard(100, 520, 880, 215, 36); tx('Birthday', 134, 580, 36, 800, 'InterTight', '#fff', 'left', 'bday'); tag(946, 534, 'example · re-created', { al: 'right', fill: C.wash });
    g.fillStyle = C.dark2; rr(130, 610, 820, 94, 24); g.fill();
    const bd = '03 / 14 / 1996', pp = typeP(t, T.l2 + .55, T.l2 + 1.15, 5), s = typed(bd, pp);
    g.strokeStyle = `rgba(182,242,58,${.5 + .5 * sm(sg(t, T.l2 + .5, T.l2 + 1))})`; g.lineWidth = 4; rr(130, 610, 820, 94, 24); g.stroke();
    tx(s, 164, 676, 46, 700, 'JBMono', '#fff', 'left', 'bdval'); g.font = F(46, 700, 'JBMono'); if (pp < 1) caret(164 + g.measureText(s).width + 6, 630, 54, t);
    const ck = enterE(sg(t, T.l2 + 1.2, T.l2 + 1.6)); if (ck > .01) check(150 + 640, 657, 30 * ck, ck);
    g.restore();
    // STILL TEEN? sticker slap
    const su = (t - (T.l2 + 1.25)) / .45, sa = sm(su * 2.6), ss = 1 + .6 * (1 - expoE(su));
    if (sa > .003) { g.save(); g.globalAlpha *= sa; g.translate(800, 650 + fl(t, 4, 5, 3.3)); g.rotate(-.07); g.scale(ss, ss); g.translate(-160, -40);
      sticker(0, 0, 320, 80, 40, C.ink, { off: 8, ol: 4 }, () => { tx('STILL TEEN?', 160, 56, 38, 900, 'InterTight', C.lime, 'center', 'stillteen'); }); g.restore(); }
    ring(800, 650, t, T.l2 + 1.28, .6, C.lime, 200);
    // OpenAI quote card
    const q0 = enterE(sg(t, T.l2 + .5, T.l2 + 1.0)), qa = sm(sg(t, T.l2 + .5, T.l2 + .7));
    g.save(); g.globalAlpha *= qa; g.translate(0, (1 - q0) * 70 + fl(t, 6, 5, 4.6)); g.rotate(-.008 + (1 - q0) * .02);
    sticker(95, 790, 890, 392, 34, C.white, { off: 10, ol: 5 });
    let fs = 39; g.font = F(fs, 700, 'Inter'); const wmax = Math.max(...QUOTE.map(q => g.measureText(q[0]).width)); fs = Math.min(40, 39 * 790 / wmax); g.font = F(fs, 700, 'Inter');
    const total = QUOTE.reduce((a, q) => a + q[0].length, 0), pq = typeP(t, T.l2 + .75, T.l2 + 1.85, 2); let left = Math.floor(total * pq);
    const hs = enterE(sg(t, T.l2 + 1.85, T.l2 + 2.2));
    QUOTE.forEach((q, i) => { const y = 870 + i * 62; const vis = q[0].slice(0, Math.max(0, Math.min(q[0].length, left)));
      if (q[1]) { g.font = F(fs, 700, 'Inter'); let w0 = g.measureText(q[0]).width, x0 = 133; if (q[1] === 2) w0 = g.measureText('birth').width;
        g.fillStyle = C.lime; rr(x0 - 8, y - 42, (w0 + 16) * hs, 56, 12); g.fill(); }
      tx(vis, 133, y, fs, 700, 'Inter', C.ink, 'left', 'q' + i); left -= q[0].length; });
    g.font = F(fs, 700, 'Inter'); if (pq < 1) { const lines = QUOTE.map(q => q[0]); let rem = Math.floor(total * pq), li = 0; while (li < 3 && rem > lines[li].length) { rem -= lines[li].length; li++; } caret(133 + g.measureText(lines[li].slice(0, rem)).width + 6, 870 + li * 62 - 38, 46, t); }
    sticker(133, 1100, 420, 62, 31, C.lime, { off: 6, ol: 4 }, () => { tx('OpenAI Help Center', 28, 42, 28, 800, 'InterTight', C.ink, 'left', 'qsrc'); });
    g.restore();
  }, 540, 760);
}
// ---------- scene C: real news (TechRadar over TechCrunch) ----------
function sceneC(t) {
  wrap(ev(t, T.l3 - .03, T.l4 - .2, .4, EXIT), () => head(t, [[K('News', wt('l3', 0), 'ink'), K('sites', wt('l3', 1)), K('reported', wt('l3', 2))], [K('it', wt('l3', 3)), K('back', wt('l3', 4)), K('in', wt('l3', 5)), K('January.', wt('l3', 6), 'lime')]], 100, 362, 90, 100, { maxW: 860 }), 540, 380);
  const e = ev(t, NEWS_IN, NEWS_OUT, .35, .2); if (!e.on) return;
  const out = sm(sg(t, NEWS_OUT, NEWS_OUT + .2));
  g.save(); g.globalAlpha *= (1 - out); g.translate(0, -out * 30);
  // TechCrunch card, slides in from the left behind
  const ta = enterE(sg(t, NEWS_IN + .06, NEWS_IN + .7)), tw = 860, th = tw * TC.height / TC.width;
  g.save(); g.globalAlpha *= sm(ta * 2); g.translate(110 + 430 + (1 - ta) * -520, 520 + th / 2 + fl(t, 1, 6, 4.2)); g.rotate(-.022 * ta); g.translate(-430, -th / 2);
  g.fillStyle = C.ink; rr(10, 10, tw, th, 18); g.fill(); g.fillStyle = '#fff'; rr(0, 0, tw, th, 18); g.fill(); g.save(); rr(0, 0, tw, th, 18); g.clip(); g.drawImage(TC, 0, 0, tw, th); g.restore(); g.lineWidth = 5; g.strokeStyle = C.ink; rr(0, 0, tw, th, 18); g.stroke(); g.restore();
  // TechRadar headline card, slams in on top
  const ru = (t - NEWS_IN) / .5, rk = enterE(ru), rs = 1 + .28 * (1 - expoE(ru)), rw = 918, rh = rw * TR.height / TR.width;
  g.save(); g.globalAlpha *= sm(ru * 4); g.translate(540, 590 + rh / 2 + fl(t, 3, 5, 4.8)); g.rotate((.012 * (1 - rk)) - .004 * Math.sin(t * .8)); const hz = 1 + .016 * sg(t, NEWS_IN + .5, NEWS_OUT); g.scale(rs * hz, rs * hz); g.translate(-rw / 2, -rh / 2);
  g.fillStyle = C.ink; rr(11, 11, rw, rh, 20); g.fill(); g.fillStyle = '#fff'; rr(0, 0, rw, rh, 20); g.fill();
  g.save(); rr(0, 0, rw, rh, 20); g.clip(); g.drawImage(TR, 0, 0, rw, rh); const k = rw / TR.width;
  // marker sweep over "stuck in teen mode", then a ring on the date
  const m = enterE(sg(t, T.l3 + 1.55, T.l3 + 2.15)); if (m > .01) { g.globalCompositeOperation = 'multiply'; g.fillStyle = C.lime; rr(32 * k, 160 * k, 530 * k * m, 70 * k, 12); g.fill(); g.globalCompositeOperation = 'source-over'; }
  const dp = enterE(sg(t, T.l3 + 2.4, T.l3 + 2.9)); if (dp > .01) { g.strokeStyle = C.limeDeep; g.lineWidth = 5; g.lineCap = 'round'; const x0 = 450 * k, y0 = 262 * k, w0 = 318 * k, h0 = 46 * k, per = 2 * (w0 + h0); g.setLineDash([per * dp, per]); rr(x0, y0, w0, h0, 14); g.stroke(); g.setLineDash([]); }
  g.restore(); g.lineWidth = 5; g.strokeStyle = C.ink; rr(0, 0, rw, rh, 20); g.stroke(); g.restore();
  ring(540, 590 + rh / 2, t, NEWS_IN + .08, .55, C.lime, 300);
  // stamp
  const su = (t - (NEWS_IN + .55)) / .45; stamp('REAL NEWS · Jan 2026', 372, 566 + fl(t, 2, 4, 3.1), 34, -.07, 1 + .6 * (1 - expoE(su)), sm(su * 2.6), C.limeDeep, 'stampnews');
  // source tags
  const ga = sm(sg(t, NEWS_IN + .6, NEWS_IN + .9)); g.save(); g.globalAlpha *= ga; g.translate(0, fl(t, 5, 3, 3.6));
  const w1 = tag(81, 892, 'real page · TechRadar', { px: 24, fill: C.lime, rot: -.006 }); tag(81 + w1 + 16, 892, 'real page · TechCrunch', { px: 24, fill: C.white, rot: .006 }); g.restore();
  // TechRadar bullet strip
  const bu = enterE(sg(t, T.l3 + 1.0, T.l3 + 1.5)); if (bu > .01) { g.save(); g.globalAlpha *= sm(bu * 1.8); g.translate((1 - bu) * 60, fl(t, 7, 4, 3.9));
    sticker(100, 972, 880, 118, 26, C.lime, { off: 8, ol: 5 }, () => { g.globalCompositeOperation = 'multiply'; g.drawImage(TB, 24, 22, 832, 832 * TB.height / TB.width); g.globalCompositeOperation = 'source-over'; }); g.restore(); }
  g.restore();
}
// ---------- scene D: what it guesses from ----------
function sceneD(t) {
  wrap(ev(t, T.l4 - .03, T.l5 - .2, .4, EXIT), () => head(t, [[K('It', wt('l4', 0)), K('guesses', wt('l4', 1), 'ink'), K('from', wt('l4', 2))], [K('what', wt('l4', 3)), K('you', wt('l4', 4)), K('ask,', wt('l4', 5), 'lime'), K('and', wt('l4', 6)), K('when.', wt('l4', 7), 'lime')]], 100, 362, 88, 100, { maxW: 860 }), 540, 380);
  const S0 = NEWS_OUT + .22;
  wrap(ev(t, S0, T.l5 - .2, .4, EXIT), () => {
    const items = [['what you talk about', 'chat', S0], ['times of day you use it', 'clock', S0 + .25], ['how long your account has existed', 'cal', S0 + .5]];
    items.forEach(([s, ic, t0], i) => { const a = enterE(sg(t, t0, t0 + .5)); g.save(); g.globalAlpha *= sm(a * 1.8); g.translate((1 - a) * (i % 2 ? 90 : -90), fl(t, i * 2, 5, 3.7 + i * .4));
      g.font = F(36, 800, 'InterTight'); const w = 880; const y = 560 + i * 150;
      sticker(100, y, w, 120, 60, i === 1 ? C.lime : C.white, { off: 9, ol: 5, rot: (i - 1) * .012 }, () => { icon(ic, 80, 62, 1.15); tx(s, 140, 76, 40, 800, 'InterTight', C.ink, 'left', 'sig' + i); });
      g.restore(); });
    const ca = sm(sg(t, S0 + .9, S0 + 1.2)); g.save(); g.globalAlpha *= ca; g.translate(0, fl(t, 4, 3, 3)); tag(100, 1040, 'signals listed by OpenAI Help Center', { px: 24, fill: C.wash, rot: -.005 }); g.restore();
  }, 540, 800);
}
// ---------- scene E: Settings, Account, Age ----------
function sceneE(t) {
  wrap(ev(t, T.l5 - .03, T.l6 - .2, .4, EXIT), () => {
    const steps = [['Settings', 1, l5s[0]], ['Account', 2, l5s[1]], ['Age', 3, l5s[2]]];
    g.font = F(34, 800, 'InterTight'); const ws = steps.map(s => g.measureText(s[0]).width + 104); let x = 540 - (ws[0] + ws[1] + ws[2] + 40) / 2;
    steps.forEach(([s, n, ts], i) => {
      const u = sg(t, ts - .12, ts + .35), act = t >= ts - .12 && (i === 2 || t < steps[i + 1][2] - .12);
      const sc = 1 + (act ? .06 : 0) * enterE(u), y = 296 + fl(t, i * 2, 3, 4 + i * .7);
      g.save(); g.translate(x + ws[i] / 2, y + 43); g.scale(sc, sc); g.translate(-ws[i] / 2, -43);
      sticker(0, 0, ws[i], 86, 43, act ? C.lime : C.white, { off: 7 }); badge(n, 44, 43, 28, 1, act ? C.white : C.lime);
      tx(s, 86, 56, 34, 800, 'InterTight', C.ink, 'left', 'step' + n); g.restore();
      if (i < 2) { g.save(); g.strokeStyle = C.ink; g.lineWidth = 6; g.lineCap = 'round'; g.lineJoin = 'round'; const ax = x + ws[i] + 6, ay = y + 43; g.beginPath(); g.moveTo(ax, ay); g.lineTo(ax + 20, ay); g.moveTo(ax + 12, ay - 9); g.lineTo(ax + 21, ay); g.lineTo(ax + 12, ay + 9); g.stroke(); g.restore(); }
      x += ws[i] + 20;
    });
    head(t, [[K('See', wt('l5', 0)), K('what', wt('l5', 1)), K('it', wt('l5', 2)), K('says:', wt('l5', 3), 'lime')]], 100, 520, 96, 100, { maxW: 860 });
    // redrawn settings card with two pages
    const c0 = enterE(sg(t, T.l5 + .25, T.l5 + .75));
    g.save(); g.translate(0, (1 - c0) * 70 + fl(t, 1, 5, 4.6)); g.globalAlpha *= sm(c0 * 1.8);
    dcard(100, 600, 880, 560, 40); tag(946, 616, 'example · re-created', { al: 'right', fill: C.wash });
    g.save(); rr(100, 600, 880, 560, 40); g.clip();
    const sw = enterE(sg(t, l5s[1] - .1, l5s[1] + .45));   // page slide 0 -> 1
    const row = (s, y, hi, ic) => { g.fillStyle = hi ? C.lime : C.dark2; rr(130, y, 820, 74, 22); g.fill(); icon(ic, 176, y + 37, .8, hi ? C.ink : '#DDE0D2'); tx(s, 226, y + 50, 36, 700, 'Inter', hi ? C.ink : '#fff', 'left', 'r:' + s);
      g.strokeStyle = hi ? C.ink : C.mute; g.lineWidth = 5; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); g.moveTo(912, y + 24); g.lineTo(926, y + 37); g.lineTo(912, y + 50); g.stroke(); };
    // page 0: Settings
    g.save(); const kr0 = REC; if (sw > .01) REC = false; g.translate(-sw * 880, 0);
    tx('Settings', 134, 668, 38, 800, 'InterTight', '#fff', 'left', 'p0'); icon('gear', 330, 656, .9, C.lime);
    const hi0 = t > l5s[0] + .25 && t < l5s[1] + .3;
    [['General', 'gear'], ['Notifications', 'chat'], ['Personalization', 'user'], ['Account', 'id']].forEach(([s, ic], i) => row(s, 708 + i * 92, s === 'Account' && t > l5s[1] - .15, ic));
    g.restore(); REC = kr0;
    // page 1: Account
    g.save(); const kr1 = REC; if (sw > .01 && sw < .99) REC = false; if (sw < .01) REC = false; g.translate((1 - sw) * 880, 0);
    tx('Account', 134, 668, 38, 800, 'InterTight', '#fff', 'left', 'p1'); icon('id', 350, 656, .9, C.lime);
    [['Profile', 'user'], ['Age', 'clock'], ['Plan', 'cal']].forEach(([s, ic], i) => row(s, 708 + i * 92, s === 'Age' && t > l5s[2] - .1, ic));
    g.restore(); REC = kr1; g.restore();
    // cursor: taps Account then Age, rings on rows
    const cu1 = sm(sg(t, T.l5 + .6, l5s[1] - .02)), cu2 = sm(sg(t, l5s[1] + .25, l5s[2] - .02));
    let cx = lerp(900, 560, cu1), cy = lerp(660, 1010, cu1); cx = lerp(cx, 600, cu2); cy = lerp(cy, 840, cu2);
    const ca = sm(sg(t, T.l5 + .5, T.l5 + .8)); g.save(); g.globalAlpha *= ca * (1 - sm(sg(t, l5s[2] + .6, l5s[2] + .8)));
    ripple(560, 1010, t, l5s[1]); ripple(600, 840, t, l5s[2]); cursor(cx, cy, 1.1, Math.max(0, 1 - Math.abs(t - l5s[1]) / .12, 1 - Math.abs(t - l5s[2]) / .12)); g.restore();
    const rp = enterE(sg(t, l5s[2], l5s[2] + .45)); if (rp > .01) { g.strokeStyle = C.lime; g.lineWidth = 6; g.lineCap = 'round'; const w = 828, h = 82, per = 2 * (w + h); g.setLineDash([per * rp, per]); rr(126, 796, w, h, 26); g.stroke(); g.setLineDash([]); }
    g.restore();
  }, 540, 700);
}
// ---------- scene F: verify ----------
function sceneF(t) {
  const T0 = T.l6 - .03;
  wrap(ev(t, T0, T.l7 - .2, .4, EXIT), () => {
    head(t, [[K('If', wt('l6', 0)), K('it’s', wt('l6', 1)), K('wrong,', wt('l6', 2), 'ink')], [K('OpenAI', wt('l6', 3)), K('says', wt('l6', 5)), K('a', wt('l6', 6)), K('selfie', wt('l6', 7), 'lime')], [K('or', wt('l6', 8)), K('an', wt('l6', 9)), K('ID', wt('l6', 10), 'lime'), K('can', wt('l6', 11)), K('fix', wt('l6', 12)), K('it.', wt('l6', 13))]], 100, 345, 84, 94, { maxW: 860 });
    const c0 = enterE(sg(t, T0 + .35, T0 + .85));
    g.save(); g.translate(0, (1 - c0) * 70 + fl(t, 2, 5, 4.4)); g.globalAlpha *= sm(c0 * 1.8);
    dcard(100, 660, 880, 520, 40); tx('Verify your age', 134, 730, 40, 800, 'InterTight', '#fff', 'left', 'vh');
    // status badge TEEN -> ADULT at the fix
    const fx = wt('l6', 12) - .1, fp = sg(t, fx, fx + .5), sx = Math.abs(Math.cos(fp * Math.PI)) * (fp > 0 && fp < 1 ? 1 : 1), lab = fp > .5 ? 'ADULT' : 'TEEN';
    g.save(); g.translate(830, 712); g.scale(Math.max(.02, sx), 1); sticker(-100, -38, 200, 76, 38, fp > .5 ? C.lime : C.ink, { off: 6, ol: 4 }, () => { tx(lab, 100, 52, 38, 900, 'InterTight', fp > .5 ? C.ink : C.lime, 'center', 'vbadge'); }); g.restore();
    sticker(134, 760, 360, 56, 28, C.wash, { off: 5, ol: 3 }, () => { tx('via a third party', 24, 38, 26, 800, 'InterTight', C.ink, 'left', 'third'); });
    const opts = [['Selfie', 'cam', wt('l6', 7)], ['ID', 'id', wt('l6', 10)]];
    opts.forEach(([s, ic, ts], i) => { const a = enterE(sg(t, T0 + .6 + i * .3, T0 + 1.1 + i * .3)), on = t > ts - .05, pk = Math.sin(Math.PI * clamp((t - ts) / .5));
      g.save(); g.globalAlpha *= sm(a * 1.8); g.translate(0, (1 - a) * 40 + fl(t, i * 3, 4, 3.5 + i * .5));
      sticker(130 + i * 420, 860, 390, 190, 40, on ? C.lime : C.white, { off: 9, ol: 5, s: 1 + .05 * pk, rot: (i ? .015 : -.015) }, () => { icon(ic, 195, 68, 1.4); tx(s, 195, 162, 46, 900, 'InterTight', C.ink, 'center', 'opt' + i); }); g.restore(); });
    tag(134, 1090, 'example · re-created', { px: 24, fill: C.wash });
    g.restore();
    // cursor taps Selfie then ID
    const ts1 = wt('l6', 7), ts2 = wt('l6', 10), c1 = sm(sg(t, ts1 - .55, ts1 - .05)), c2 = sm(sg(t, ts1 + .5, ts2 - .05));
    let cx = lerp(930, 330, c1), cy = lerp(780, 960, c1); cx = lerp(cx, 760, c2); cy = lerp(cy, 970, c2);
    const ca = sm(sg(t, ts1 - .6, ts1 - .3)) * (1 - sm(sg(t, ts2 + .6, ts2 + .8)));
    g.save(); g.globalAlpha *= ca; ripple(330, 960, t, ts1); ripple(760, 970, t, ts2); cursor(cx, cy, 1.1, Math.max(0, 1 - Math.abs(t - ts1) / .12, 1 - Math.abs(t - ts2) / .12)); g.restore();
  }, 540, 760);
}
// ---------- scene G: comment ----------
function sceneG(t) {
  const T0 = T.l7 - .03, TB0 = T.l7 + 2.54;
  wrap(ev(t, T0, T.l8 - .2, .4, EXIT), () => {
    head(t, [[K('Has', wt('l7', 0)), K('ChatGPT', wt('l7', 1), 'ink')], [K('ever', wt('l7', 3)), K('called', wt('l7', 4))], [K('you', wt('l7', 5)), K('a', wt('l7', 6)), K('kid?', wt('l7', 7), 'lime')]], 100, 360, 100, 106, { maxW: 860 });
    const c0 = enterE(sg(t, T0 + .3, T0 + .8));
    g.save(); g.translate(0, (1 - c0) * 70 + fl(t, 2, 5, 4.4)); g.globalAlpha *= sm(c0 * 1.8);
    dcard(100, 700, 880, 470, 40); tx('Comments', 134, 770, 38, 800, 'InterTight', '#fff', 'left', 'ch'); tag(946, 716, 'example · re-created', { al: 'right', fill: C.wash });
    g.fillStyle = C.dark2; rr(130, 800, 820, 92, 46); g.fill();
    g.fillStyle = C.lime; g.beginPath(); g.arc(176, 846, 26, 0, 7); g.fill(); icon('user', 176, 846, .62, C.ink);
    const foc = sm(sg(t, TB0 - .2, TB0 + .3)); g.strokeStyle = `rgba(182,242,58,${.25 + .75 * foc})`; g.lineWidth = 3 + 3 * foc; rr(130, 800, 820, 92, 46); g.stroke();
    tx('Add a comment…', 226, 858, 34, 500, 'Inter', C.mute, 'left', 'ph'); if (foc > .1 && Math.sin(t * 6.283) > -.3) { g.fillStyle = C.lime; g.fillRect(214, 818, 4, 56); }
    const btn = (s, x, y, w, fill, rot, t0, hit) => { const u = enterE(sg(t, t0, t0 + .5)), a = sm(sg(t, t0, t0 + .28)); if (a < .003) return; const pk = hit ? Math.sin(Math.PI * clamp((t - hit) / .4)) : 0; g.save(); g.globalAlpha *= a; g.translate(0, (1 - u) * 34 + fl(t, x, 4, 3.8));
      sticker(x, y, w, 96, 48, fill, { rot: rot * u, off: 8, s: (.92 + .08 * u) * (1 + .07 * pk) }, () => { tx(s, w / 2, 63, 40, 900, 'InterTight', C.ink, 'center', 'btn:' + s); }); g.restore(); };
    const y1 = wt('l7', 7);
    btn('Yes', 130, 960, 220, C.lime, -.03, T0 + .9, y1 + .1); btn('No', 380, 960, 170, C.white, .02, T0 + 1.1); btn('Tell me below ↓', 580, 960, 370, C.lime, -.02, T0 + 1.3, TB0 + .2);
    g.restore();
    const ca = sm(sg(t, T0 + 1.3, T0 + 1.6)) * (1 - sm(sg(t, TB0 + .9, TB0 + 1.1)));
    if (ca > .01) { const u1 = sm(sg(t, T0 + 1.4, y1 + .05)), u2 = sm(sg(t, y1 + .45, TB0 + .15)); let cx = lerp(940, 240, u1), cy = lerp(740, 1030, u1); cx = lerp(cx, 770, u2); cy = lerp(cy, 1040, u2);
      g.save(); g.globalAlpha *= ca; ripple(240, 1030, t, y1 + .1); ripple(770, 1040, t, TB0 + .2); cursor(cx, cy, 1.1, Math.max(0, 1 - Math.abs(t - y1 - .1) / .12, 1 - Math.abs(t - TB0 - .2) / .12)); g.restore(); }
  }, 540, 800);
}
// ---------- scene H: link in bio ----------
function sceneH(t) {
  const T0 = T.l8 - .03;
  wrap(ev(t, T0, T.l9 - .2, .4, EXIT), () => {
    g.save(); g.translate(0, fl(t, 1, 5, 4)); const p = 1 + .015 * Math.sin(t * 6.283 / 1.7);
    g.save(); g.translate(540, 430); g.scale(p, p); g.translate(-540, -430);
    sticker(115, 330, 850, 200, 100, C.lime, { off: 12, ol: 6 }, () => {
      g.strokeStyle = C.ink; g.lineWidth = 11; g.lineCap = 'round'; rr(96, 78, 86, 46, 23); g.stroke(); rr(144, 96, 86, 46, 23); g.stroke();
      tx('Link in bio', 270, 138, 84, 900, 'InterTight', C.ink, 'left', 'linkbio'); });
    g.restore();
    const lp = sm(sg(t, T0 + .45, T0 + 1.3)); g.strokeStyle = C.ink; g.lineWidth = 8; g.lineCap = 'round'; g.setLineDash([2, 16]); g.beginPath(); g.moveTo(222, 640); g.lineTo(222, 640 + 300 * lp); g.stroke(); g.setLineDash([]);
    [['Settings', 1], ['Account', 2], ['Age', 3]].forEach(([s, n], i) => { const a = enterE(sg(t, T0 + .3 + i * .22, T0 + .85 + i * .22)); g.save(); g.globalAlpha *= sm(a * 1.8); g.translate((1 - a) * -60, fl(t, i * 2.2, 4, 3.6 + i * .5));
      sticker(160, 600 + i * 150, 760, 116, 58, i === 2 ? C.lime : C.white, { off: 8, ol: 5 }, () => { tx(s, 150, 76, 50, 800, 'InterTight', C.ink, 'left', 'chip' + i); }); badge(n, 222, 658 + i * 150, 34, 1); g.restore(); });
    g.restore();
  }, 540, 700);
  const ca = sm(sg(t, T0 + .1, T0 + .3)) * (1 - sm(sg(t, T0 + 1.3, T0 + 1.5)));
  if (ca > .01) { const u = sm(sg(t, T0 + .1, T0 + .6)); const x = lerp(900, 780, u), y = lerp(640, 470, u); g.save(); g.globalAlpha *= ca; ripple(790, 480, t, T0 + .6); cursor(x, y, 1.1, Math.max(0, 1 - Math.abs(t - T0 - .6) / .12)); g.restore(); }
}
// ---------- scene I: closing ----------
function sceneI(t) {
  const T0 = T.l9 - .03;
  wrap(ev(t, T0, 99, .45, 0), () => {
    g.save(); g.translate(0, fl(t, 2, 4, 4.2));
    head(t, [[K('I', wt('l9', 0)), K('read', wt('l9', 1)), K('the', wt('l9', 2)), K('fine', wt('l9', 3), 'ink'), K('print', wt('l9', 4), 'ink')], [K('AI', wt('l9', 5)), K('apps', wt('l9', 6)), K('hope', wt('l9', 7))], [K('you', wt('l9', 8)), K('skip.', wt('l9', 9), 'lime')]], 100, 505, 86, 92, { maxW: 860 });
    g.restore();
  }, 540, 700);
  // three AI-setting cards slide in; the toggles flip as "hope you skip" is said
  wrap(ev(t, T0 + .1, 99, .4, 0), () => {
    const cards = [['Memory', T.l9 + .1], ['Age', T.l9 + .55], ['Ads', T.l9 + 1.0]];
    const after = t > TAP + .3 ? sm(sg(t, TAP + .3, TAP + 1.2)) : 0;
    cards.forEach(([s, t0], i) => { const a = enterE(sg(t, t0, t0 + .6)); g.save(); g.globalAlpha *= sm(a * 2); const sy = 790 + i * 120;
      g.translate((1 - a) * 420 + after * (i - 1) * 8, fl(t, i * 2.1, 5, 3.4 + i * .5) + (1 - a) * 20); g.rotate((i - 1) * .016 * a + .006 * Math.sin(t * 1.2 + i));
      sticker(110, sy, 780, 104, 52, i === 1 ? C.lime : C.white, { off: 9, ol: 5 }, () => { tx(s, 50, 68, 46, 900, 'InterTight', C.ink, 'left', 'ai' + i); });
      const tg = sm(sg(t, T.l9 + 1.9 + i * .22, T.l9 + 2.3 + i * .22)); toggle(740, sy + 22, true, tg);
      g.restore(); });
    g.save(); g.translate(0, fl(t, 8, 3, 3.3)); g.globalAlpha *= sm(sg(t, T.l9 + 1.2, T.l9 + 1.5)); tag(110, 1166, 'example · re-created', { px: 24, fill: C.wash, rot: -.004 }); g.restore();
  }, 540, 1000);
  // Follow: pops with the word, one tap, lime burst, settled check, keeps moving
  wrap(ev(t, T.l9 - .03, 99, .45, 0), () => {
    g.save(); g.translate(0, fl(t, 6, 4, 3.9)); const done = sm(sg(t, TAP, TAP + .3)), s = 1 + .025 * Math.sin(t * 3.1) + .08 * Math.sin(Math.PI * clamp((t - TAP) / .5)) * (t > TAP ? 1 : 0);
    sticker(630, 318, 340, 96, 48, done > .5 ? C.white : C.lime, { off: 9, ol: 5, s, rot: .02 }, () => {
      if (done > .5) { check(52, 48, 26, 1); tx('Following', 200, 66, 46, 900, 'InterTight', C.ink, 'center', 'follow'); } else tx('Follow', 170, 66, 50, 900, 'InterTight', C.ink, 'center', 'follow'); });
    g.restore();
    if (t > TAP) { for (let wv = 0; wv < 2; wv++) { const R = rng(5 + wv * 9), T1 = TAP + wv * .55; if (t < T1) continue; for (let i = 0; i < 12; i++) { const ang = R() * 6.283, sp = 120 + R() * 200, u = (t - T1 - R() * .1), e = 1 - Math.exp(-Math.max(0, u) * 2.6); if (u < 0) continue;
      g.save(); g.globalAlpha *= clamp(1 - u / 1.25) * .9; g.fillStyle = i % 3 ? C.lime : C.ink; g.strokeStyle = C.ink; g.lineWidth = 3; g.beginPath(); g.arc(800 + Math.cos(ang) * sp * e, 366 + Math.sin(ang) * sp * e + 60 * u * u, i % 3 ? 9 : 5, 0, 7); g.fill(); if (i % 3) g.stroke(); g.restore(); } } }
    const cu = sm(sg(t, TAP - .9, TAP - .02)); if (cu > .01 && t < TAP + .45) { const x = lerp(960, 880, cu) + Math.sin(cu * 3.14) * -18, y = lerp(560, 395, cu); g.save(); g.globalAlpha *= 1 - sm(sg(t, TAP + .2, TAP + .45)); cursor(x, y + fl(t, 0, 3, 2.7), 1, Math.max(0, 1 - Math.abs(t - TAP) / .12)); g.restore(); }
    ripple(880, 400, t, TAP); ripple(880, 400, t, TAP + .6);
  }, 800, 370);
}
function draw(t) {
  g.setTransform(1, 0, 0, 1, 0, 0); TXT.length = 0;
  const [z, cx, cy, px, py] = cam(t);
  g.save(); g.translate(cx + px, cy + py); g.scale(z, z); g.translate(-cx, -cy);
  background(t); sparkles(t);
  sceneA(t); sceneB(t); sceneC(t); sceneD(t); sceneE(t); sceneF(t); sceneG(t); sceneH(t); sceneI(t);
  g.restore();
}
window.render = (t) => { REC = false; draw(t); };
window.TEXTS = (t) => { REC = true; draw(t); REC = false; return TXT.map(o => ({ ...o })); };
const tb = T.l7 + 2.54;
window.EV = [
  { t: .25, type: 'tick' }, { t: HT, type: 'crash' }, { t: HT + .05, type: 'thud' }, { t: T.l2 - .1, type: 'whoosh' }, { t: T.l2 + 1.3, type: 'thud' }, { t: T.l3 - .1, type: 'whoosh' }, { t: NEWS_IN + .02, type: 'thud' }, { t: NEWS_IN + .56, type: 'thud' },
  { t: T.l4 + .5, type: 'whoosh' }, { t: NEWS_OUT + .1, type: 'whoosh' }, { t: T.l5 - .1, type: 'whoosh' }, { t: l5s[1], type: 'click' }, { t: l5s[2], type: 'click' }, { t: l5s[2] + .3, type: 'ding' },
  { t: T.l6 - .1, type: 'whoosh' }, { t: wt('l6', 7), type: 'click' }, { t: wt('l6', 10), type: 'click' }, { t: wt('l6', 12), type: 'ding' }, { t: T.l7 - .1, type: 'whoosh' }, { t: wt('l7', 7) + .1, type: 'click' }, { t: tb + .2, type: 'click' },
  { t: T.l8 - .1, type: 'whoosh' }, { t: T.l8 + .6, type: 'click' }, { t: T.l9 - .1, type: 'whoosh' }, { t: T.l9 + .1, type: 'pop' }, { t: T.l9 + .55, type: 'pop' }, { t: T.l9 + 1.0, type: 'pop' }, { t: TAP, type: 'ding' }].map(e => e.type === 'pop' ? { t: e.t, type: 'thud' } : e);
window.READY = true;
