// ChatGPT memory film v3. Canvas 2D, pure function of t. Channel identity: light paper + quiet dot grid, ink type, dark UI cards, lime accent, sticker components.
// The real-screen proof is a SLOT: proof.json (image path, caption, zoom, pan, rings). Swap the file + rings, rebuild with `sh build3.sh`.
const W = 1080, H = 1920;
const cv = document.getElementById('c'); let g = cv.getContext('2d');
await Promise.all([700, 800, 900, 600, 500].flatMap(w => [`${w} 40px Inter`, `${w} 40px InterTight`, `${w} 40px JBMono`]).map(f => document.fonts.load(f)));
const get = async (u, d) => { try { const r = await fetch(u); return r.ok ? await r.json() : d; } catch { return d; } };
const WD = await get('voices/words.json', {});
const PROOF = await get('proof.json', { image: 'phone.png', caption: 'real screen · ChatGPT app · Settings > Personalization', zoom: [1.125, 1.2], pan: [0, 210], rings: [] });
const svg = await (await fetch('chatgpt.svg')).text();
const MARK = new Path2D(svg.match(/ d='([^']+)'/)[1]);
const PH = await createImageBitmap(await (await fetch(PROOF.image)).blob());
const C = { paper: '#F4F4EF', dot: '#E0E0D6', ink: '#0E0E0E', ink2: '#4B4B46', dark: '#14151A', dark2: '#22242C', dark3: '#2E3039', lime: '#B6F23A', limeDeep: '#4E8F0B', wash: '#E4F8B0', white: '#FFFFFF', mute: '#8E908A' };
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const sg = (t, a, b) => clamp((t - a) / (b - a));
const sm = x => { x = clamp(x); return x * x * x * (x * (x * 6 - 15) + 10); };         // smootherstep
const enterE = x => 1 - Math.pow(1 - clamp(x), 4);                                      // long ease-out, no overshoot
const expoE = x => { x = clamp(x); return x >= 1 ? 1 : 1 - Math.pow(2, -10 * x); };
const lerp = (a, b, t) => a + (b - a) * t;
const rng = s => () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
const T = { l1: .3, l2: 2.95, l3: 5.0, l4: 7.0, l5: 10.4, l6: 13.9, l7: 16.9, l8: 19.0 };   // line starts from cues.json
const wt = (l, i) => T[l] + Math.max(0, WD[l][i][1]);                                        // spoken start of word i of line l (lead-in clamp: a negative stamp is silence, not speech)
const DUR = 26.2; window.DUR = DUR;
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
// ---------- scene A: claim + chat card + note ----------
const NOTE = { w: 372, h: 86 };
function note(x, y, text, o = {}) {   // the recurring object: lime sticker note
  sticker(x, y, NOTE.w, NOTE.h, 24, C.lime, { rot: o.rot || 0, s: o.s || 1, off: 7 }, () => {
    g.fillStyle = C.ink; g.beginPath(); g.arc(38, NOTE.h / 2, 11, 0, 7); g.fill();
    tx(text, 64, NOTE.h / 2 + 11, 31, 800, 'InterTight', C.ink, 'left', 'note:' + text);
  });
}
function typed(s, p) { return s.slice(0, Math.floor(s.length * clamp(p))); }
const typeP = (t, a, b, seed = 1) => { const u = sg(t, a, b); return clamp(u + .03 * Math.sin(u * 19 + seed) * u * (1 - u) * 4); };
function caret(x, y, h, t, col = C.lime) { const a = .55 + .45 * Math.sin(t * 6.283 * 1.0); g.fillStyle = col; g.globalAlpha *= a; g.fillRect(x, y, 4, h); g.globalAlpha /= a; }
function chatCardDraw(t) {   // dark chat card in local coords (0,0), 920x410. Whole conversation is already on screen at frame 0
  const w = 920, h = 410;
  dcard(0, 0, w, h, 38);
  mark(34, 28, 50, '#fff');
  tag(w - 34, 22, 'example · re-created', { al: 'right', fill: C.wash });
  g.fillStyle = C.dark3; g.fillRect(34, 98, w - 68, 2);
  const q = 'I’m studying for exams this month.';
  g.fillStyle = C.dark3; rr(w - 34 - 700, 124, 700, 78, 30); g.fill();
  tx(q, w - 34 - 700 + 30, 175, 36, 600, 'Inter', '#fff', 'left', 'user');
  tx('Got it. I’ll keep that in mind.', 34, 262, 37, 600, 'Inter', '#fff', 'left', 'reply');
  g.fillStyle = C.dark2; rr(34, 296, 330, 58, 29); g.fill(); g.fillStyle = C.lime; g.beginPath(); g.arc(32 + 28, 296 + 29, 8 + (t < 2.6 ? 2 * Math.sin(t * 7) : 0), 0, 7); g.fill();
  tx('Memory updated', 34 + 50, 296 + 39, 28, 600, 'Inter', '#DDE0D2', 'left', 'memupd');
}
function shards(t, t0) {   // hero beat: the card fragments fly off
  const R = rng(21), cols = 7, rows = 5, w = 920, h = 410, cw = w / cols, ch = h / rows;
  const pts = []; for (let j = 0; j <= rows; j++) { pts[j] = []; for (let i = 0; i <= cols; i++) pts[j][i] = [i * cw + ((i > 0 && i < cols) ? (R() - .5) * cw * .6 : 0), j * ch + ((j > 0 && j < rows) ? (R() - .5) * ch * .6 : 0)]; }
  const u = t - t0, ix = 460, iy = 250;
  for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) {
    const a = pts[j][i], b = pts[j][i + 1], c = pts[j + 1][i + 1], d = pts[j + 1][i];
    [[a, b, c], [a, c, d]].forEach((tri) => {
      const cx = (tri[0][0] + tri[1][0] + tri[2][0]) / 3, cy = (tri[0][1] + tri[1][1] + tri[2][1]) / 3;
      let dx = cx - ix, dy = cy - iy; if (dy < 0) dy *= .45; const L = Math.hypot(dx, dy) + 1; dx /= L; dy /= L;
      const sp = 380 + R() * 760 + 700 / (1 + L / 140), rot = (R() - .5) * 9, delay = L / 4200;
      const uu = Math.max(0, u - delay), e = 1 - Math.exp(-uu * 2.2);
      const px = dx * sp * e / 2.2, py = dy * sp * e / 2.2 + 520 * uu * uu;
      const al = 1 - sm(sg(uu, .55, 1.15));
      if (al < .01) return;
      g.save(); g.globalAlpha *= al; g.translate(cx + px, cy + py); g.rotate(rot * e * .7); g.translate(-cx, -cy);
      g.beginPath(); g.moveTo(tri[0][0], tri[0][1]); g.lineTo(tri[1][0], tri[1][1]); g.lineTo(tri[2][0], tri[2][1]); g.closePath();
      g.save(); g.clip(); g.drawImage(SH.cv, 0, 0); g.restore();
      g.lineWidth = 2.5; g.strokeStyle = 'rgba(182,242,58,.55)'; g.stroke(); g.restore();
    });
  }
}
const SH = { cv: document.createElement('canvas') }; SH.cv.width = 920 + 60; SH.cv.height = 410 + 60;
(() => { const keep = g, kr = REC; REC = false; g = SH.cv.getContext('2d'); g.clearRect(0, 0, 980, 490); g.save(); chatCardDraw(3.5); g.restore(); g = keep; REC = kr; })();
function sceneA(t) {
  const SHT = 3.92, AX = 2.62, AY = 4.72;   // hook exit 2.62..2.79 ; L2 exit 4.72
  // logo: present at frame 0, stays through the L2 headline
  const lo = 1 - sm(sg(t, AY, AY + .17));
  if (lo > .003) { g.save(); g.globalAlpha *= lo; logoBadge(100, 288, 100, 1, -.06 + .02 * Math.sin(t * 1.5)); g.restore(); }
  // hook: whole line from frame 0; pills form as the words are spoken
  const hOut = 1 - sm(sg(t, AX, AX + .17));
  if (hOut > .003) { g.save(); g.globalAlpha *= hOut; g.translate(0, -sm(sg(t, AX, AX + .17)) * 16 + fl(t, 0, 6, 2.4));
    head(t, [[K('ChatGPT', wt('l1', 0)), K('can', wt('l1', 2))], [K('keep', wt('l1', 3)), K('notes', wt('l1', 4), 'ink')], [K('about', wt('l1', 5)), K('you!', wt('l1', 6), 'lime')]], 100, 490, 112, 124, { maxW: 820, whole: true }); g.restore(); }
  // L2 headline
  wrap(ev(t, 2.88, AY, .4, .17), () => head(t, [[K('Even', wt('l2', 0)), K('after', wt('l2', 1)), K('you', wt('l2', 2))], [K('delete', wt('l2', 3), 'ink'), K('the', wt('l2', 4)), K('chat.', wt('l2', 5), 'lime')]], 100, 490, 108, 126, { maxW: 860 }), 540, 490);
  // chat card: on screen at frame 0, floats, shakes, shatters at 3.92
  if (t < SHT + .02) {
    const shake = t > 3.7 ? Math.sin(t * 90) * 4 * sm(sg(t, 3.7, 3.9)) : 0;
    g.save(); g.translate(80 + shake, 820 + fl(t, 0, 7, 4.6)); g.rotate(-.012 + .006 * Math.sin(t * .9)); g.scale(1 + (t > 3.7 ? .012 * sm(sg(t, 3.7, 3.92)) : 0), 1);
    chatCardDraw(t); g.restore();
  } else {
    g.save(); g.translate(80, 820 + fl(SHT, 0, 7, 4.6)); g.rotate(-.012 + .006 * Math.sin(SHT * .9)); shards(t, SHT); g.restore();
    const u = (t - SHT) / .55;
    if (u < 1) { g.save(); g.translate(540, 1000); g.globalAlpha *= (1 - u) * .9; g.strokeStyle = C.lime; g.lineWidth = 16 * (1 - u) + 3; g.beginPath(); g.arc(0, 0, 40 + 380 * expoE(u), 0, 7); g.stroke(); g.globalAlpha *= .5; g.strokeStyle = C.ink; g.lineWidth = 4; g.beginPath(); g.arc(0, 0, 20 + 420 * expoE(u), 0, 7); g.stroke(); g.restore(); }
  }
  // the note 'Studying for exams': pinned on the card from frame 0 (pulses when "notes" is spoken), then stays on screen after the shatter
  const stay = sm(sg(t, 3.92, 4.75));
  const pulse = 1 + .1 * Math.sin(Math.PI * clamp((t - 1.62) / .5)) * (t > 1.62 && t < 2.12 ? 1 : 0);
  const nx = lerp(540, 330, stay), ny = lerp(1148, 930, stay) + fl(t, 2, 6, 3.6);
  const ns = lerp(1, 1.12, stay) * pulse, nr = lerp(.03, -.05, stay);
  const na = 1 - sm(sg(t, 4.74, 4.9));
  if (na > .003) { g.save(); g.globalAlpha *= na; note(nx, ny, 'Studying for exams', { s: ns, rot: nr }); g.restore(); }
  // STILL HERE stamp slams on the note
  const su = (t - 4.3) / .45, sa = sm(su * 2.5) * (1 - sm(sg(t, 4.74, 4.9)));
  if (sa > .003) { const ss = 1 + .55 * (1 - expoE(su)); g.save(); g.globalAlpha *= sa; g.translate(580, 1062 + fl(t, 2, 6, 3.6)); g.rotate(-.1); g.scale(ss, ss);
    g.font = F(60, 900, 'InterTight'); const w = g.measureText('STILL HERE').width + 52;
    g.fillStyle = 'rgba(244,244,239,.94)'; rr(-w / 2, -50, w, 100, 20); g.fill(); g.lineWidth = 7; g.strokeStyle = C.limeDeep; rr(-w / 2, -50, w, 100, 20); g.stroke(); g.lineWidth = 2; rr(-w / 2 + 9, -41, w - 18, 82, 13); g.stroke();
    tx('STILL HERE', 0, 22, 60, 900, 'InterTight', C.limeDeep, 'center', 'stillhere'); g.restore(); }
}
// ---------- scene B: ask it (4.88 .. 6.78) ----------
function sceneB(t) {
  wrap(ev(t, 4.88, 6.78, .4, .17), () => {
    head(t, [[K('Ask', wt('l3', 0), 'ink'), K('it:', wt('l3', 1))]], 100, 500, 124, 124);
    g.save(); g.translate(0, fl(t, 3, 5, 4.2)); dcard(100, 590, 880, 124, 36);
    mark(128, 626, 50, '#fff');
    const q = 'what do you know about me?', p = typeP(t, 5.12, 5.85, 4), s = typed(q, p);
    tx(s, 208, 674, 40, 600, 'Inter', '#fff', 'left', 'prompt'); g.font = F(40, 600, 'Inter'); if (p < 1) caret(208 + g.measureText(s).width + 6, 640, 46, t);
    g.restore();
    const e2 = ev(t, 5.8, 99, .4, 0);
    wrap(e2, () => {
      g.save(); g.translate(0, fl(t, 1, 6, 5)); dcard(100, 750, 880, 440, 40);
      tag(940, 768, 'example · re-created', { al: 'right', fill: C.wash });
      const L = ['You like short answers.', 'You’re studying for exams.', 'You have a dog.'];
      L.forEach((s, i) => { const a = sm(sg(t, 5.85 + i * .24, 6.1 + i * .24)), y = 846 + i * 100;
        g.save(); g.globalAlpha *= a; g.translate((1 - enterE(sg(t, 5.85 + i * .24, 6.4 + i * .24))) * -36, 0);
        if (i === 1) { const sw = enterE(sg(t, 6.22, 6.6)); g.fillStyle = C.lime; rr(124, y - 4, 832 * sw, 88, 26); g.fill(); }
        check(176, y + 40, 24, 1); tx(s, 226, y + 53, 42, 700, 'Inter', i === 1 ? C.ink : '#fff', 'left', 'a' + i); g.restore(); });
      const a = sm(sg(t, 6.5, 6.7)); g.save(); g.globalAlpha *= a; tx('…', 226, 1156, 46, 700, 'Inter', C.mute, 'left', 'dots'); g.restore();
      g.restore();
    }, 540, 900);
  }, 540, 700);
}
// ---------- scene C0: quote (6.9 .. 10.6) ----------
function sceneQuote(t) {
  const QO = 10.42;   // quote card + bottom row exit
  wrap(ev(t, 6.98, 7.84, .4, .15), () => head(t, [[K('Delete', 7.02, 'ink'), K('the', wt('l4', 1)), K('chat.', wt('l4', 2))]], 100, 460, 120, 120, { maxW: 860 }), 540, 440);
  wrap(ev(t, 8.0, QO, .4, .17), () => head(t, [[K('The', Math.max(8.0, wt('l4', 3))), K('note', wt('l4', 4))], [K('stays.', wt('l4', 5), 'lime')]], 100, 440, 120, 124, { maxW: 860 }), 540, 440);
  // quote card: fully readable ~7.05 .. 10.42 (3.37 s), exits in 0.17 s
  const qin = enterE(sg(t, 6.9, 7.45)), qa = sm(sg(t, 6.9, 7.08)) * (1 - sm(sg(t, QO, QO + .17))), qo = sm(sg(t, QO, QO + .17));
  if (qa > .003) {
    g.save(); g.globalAlpha *= qa; g.translate(540 - qo * 120, 872 + (1 - qin) * 90 + fl(t, 5, 5, 4.4)); g.rotate(-.012 + (1 - qin) * .03 - qo * .03); g.translate(-540, -872);
    sticker(95, 650, 890, 480, 36, C.white, { off: 10, ol: 5 }, () => { tx('“', 34, 90, 110, 900, 'InterTight', C.lime, 'left', 'qm'); });
    const qs = ['even if you delete a chat,', 'any saved memories from it can', 'still be used in future', 'conversations”'];
    g.font = F(48, 700, 'Inter'); const wd = s => g.measureText(s).width;
    const b1 = enterE(sg(t, 7.4, 8.0)), b2 = enterE(sg(t, 8.1, 8.8)), b3 = enterE(sg(t, 8.8, 9.5));
    g.fillStyle = C.lime;
    rr(133, 755, wd(qs[0]) * b1 + 22, 62, 14); g.fill();
    rr(133, 822, wd(qs[1]) * b2 + 22, 62, 14); g.fill();
    rr(133, 889, wd(qs[2]) * b3 + 22, 62, 14); g.fill();
    qs.forEach((s, i) => tx(s, 144, 802 + i * 67, 48, 700, 'Inter', C.ink, 'left', 'q' + i));
    // OpenAI source as a bold chip
    sticker(134, 1030, 560, 64, 32, C.lime, { off: 6, ol: 4 }, () => { tx('OpenAI Help Center · Memory FAQ', 28, 43, 29, 800, 'InterTight', C.ink, 'left', 'qsrc'); });
    // stamp slams on the card corner
    const su = (t - 7.9) / .5, sa = sm(su * 2.6), ss = 1 + .5 * (1 - expoE(su));
    if (sa > .003) { g.save(); g.globalAlpha *= sa; g.translate(800, 676); g.rotate(-.11); g.scale(ss, ss);
      g.font = F(36, 900, 'InterTight'); const w = g.measureText('OPENAI’S WORDS').width + 40;
      g.fillStyle = 'rgba(255,255,255,.96)'; rr(-w / 2, -33, w, 66, 14); g.fill(); g.lineWidth = 5; g.strokeStyle = C.limeDeep; rr(-w / 2, -33, w, 66, 14); g.stroke();
      tx('OPENAI’S WORDS', 0, 13, 36, 900, 'InterTight', C.limeDeep, 'center', 'stamp'); g.restore(); }
    g.restore();
  }
  // bottom: deleted chat row (collapses) + the note stays
  const ba = sm(sg(t, 7.0, 7.3)) * (1 - sm(sg(t, QO, QO + .17)));
  if (ba > .003) { g.save(); g.globalAlpha *= ba; g.translate(0, fl(t, 7, 5, 3.9));
    const del = sm(sg(t, 7.7, 8.5)), rowA = 1 - del;
    if (rowA > .003) { g.save(); g.translate(300 * del, 0); g.globalAlpha *= rowA; dcard(600, 1150, 380, 78, 24);
      tx('Chat about dinner', 626, 1198, 28, 600, 'Inter', '#fff', 'left', 'row1'); g.restore(); }
    if (t > 7.7 && t < 8.7) { g.save(); const k = sg(t, 7.7, 8.7); g.globalAlpha *= (1 - k); g.strokeStyle = C.lime; g.lineWidth = 6; g.beginPath(); g.arc(600 + 300 * del + 340, 1189, 20 + 60 * enterE(k), 0, 7); g.stroke(); g.restore(); }
    note(100, 1136, 'Studying for exams', { rot: .02 + .01 * Math.sin(t * 1.3), s: .96 + .04 * enterE(sg(t, 8.2, 8.8)) });
    const ck = sm(sg(t, 8.7, 9.2)); check(100 + NOTE.w + 46, 1179, 24 * ck, ck);
    g.restore(); }
}
// ---------- scene D: the proof slot (10.45 .. 13.9) ----------
const PWX = 90, PWY = 590, PWW = 900, PWH = 570;    // real-screen window: 900 px wide (83% of frame), y 590..1160
function sceneC(t) {
  const CO = 13.74;   // exit start
  wrap(ev(t, 10.44, CO, .4, .16), () => {
    // step chips: row on top, the spoken step lights lime
    const steps = [['Settings', 1, wt('l5', 0)], ['Personalization', 2, wt('l5', 1)], ['Memory', 3, wt('l5', 2)]];
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
    head(t, [[K('That’s', wt('l5', 3)), K('where', wt('l5', 4)), K('it', wt('l5', 5)), K('lives.', wt('l5', 6), 'lime')]], 100, 500, 92, 100, { maxW: 880 });
    // the real screen: large window, slow pan + zoom, rings from proof.json
    const pe = ev(t, 10.5, 99, .38, 0), sl = (1 - enterE(sg(t, 10.5, 10.95))) * 90;
    g.save(); g.translate(0, sl + fl(t, 1, 5, 4.8));
    g.fillStyle = C.ink; rr(PWX + 12, PWY + 12, PWW, PWH, 44); g.fill();
    g.save(); rr(PWX, PWY, PWW, PWH, 44); g.clip(); g.fillStyle = '#0B0B0D'; g.fillRect(PWX, PWY, PWW, PWH);
    const k = sm(sg(t, 10.7, 13.6)), z = lerp(PROOF.zoom[0], PROOF.zoom[1], k);
    let sc = (PWW / PH.width) * (z / PROOF.zoom[0]); sc = Math.max(sc, PWH / PH.height);   // fit width, then slow zoom; never smaller than the window height
    const iw = PH.width * sc, ih = PH.height * sc, panMax = Math.max(0, ih - PWH);
    const iy = PWY - Math.min(panMax, lerp(PROOF.pan[0], PROOF.pan[1], sm(sg(t, 11.9, 13.6)))) + Math.sin(t * .7) * 2, ix = PWX - (iw - PWW) / 2 + Math.sin(t * .9) * 3;
    g.drawImage(PH, ix, iy, iw, ih);
    (PROOF.rings || []).forEach(r => { const p = sm(sg(t, r.t0, r.t1)); if (p < .03) return;
      g.save(); g.strokeStyle = C.lime; g.lineWidth = 6; g.lineCap = 'round'; const rad = Math.min(r.h * sc / 2, 34), w = r.w * sc, h = r.h * sc, per = 2 * (w + h);
      if (r.style === 'dashed') { g.setLineDash([22, 14]); g.globalAlpha *= p; } else g.setLineDash([per * p, per]);
      rr(ix + r.x * sc, iy + r.y * sc, w, h, rad); g.stroke(); g.restore(); });
    g.restore();
    g.lineWidth = 6; g.strokeStyle = C.ink; rr(PWX, PWY, PWW, PWH, 44); g.stroke();
    g.restore();
    // honest caption, one chip below the screen (does not claim it shows memory notes)
    g.save(); g.translate(0, sl); tag(PWX + 4, 1178, PROOF.caption, { px: 24, fill: C.lime, rot: -.006 }); g.restore();
  }, 540, 700);
}
// ---------- scene E: did it get something wrong (13.9 .. 16.8) ----------
function sceneD(t) {
  const DO = 16.62;
  wrap(ev(t, 13.9, DO, .4, .17), () => {
    head(t, [[K('Did', wt('l6', 0)), K('it', wt('l6', 1)), K('get', wt('l6', 2))], [K('something', wt('l6', 3)), K('wrong', wt('l6', 4), 'ink')], [K('about', wt('l6', 5)), K('you?', wt('l6', 6), 'lime')]], 100, 420, 104, 114, { maxW: 840 });
    // saved-memories card: the real middle-band element
    g.save(); g.translate(0, fl(t, 2, 5, 4.4)); const cy0 = 690; dcard(100, cy0, 880, 340, 38);
    tx('Saved memories', 134, cy0 + 56, 34, 800, 'InterTight', '#fff', 'left', 'memhead'); tag(944, cy0 + 20, 'example · re-created', { al: 'right', fill: C.wash });
    const rows = ['Studying for exams', 'Likes short answers', 'Has a dog'];
    rows.forEach((s, i) => { const a = enterE(sg(t, 14.05 + i * .14, 14.4 + i * .14)), y = cy0 + 92 + i * 80; g.save(); g.globalAlpha *= sm(a * 1.8); g.translate((1 - a) * 40, 0);
      g.fillStyle = C.dark2; rr(130, y, 820, 68, 22); g.fill(); check(172, y + 34, 20, 1);
      tx(s, 212, y + 46, 36, 700, 'Inter', '#fff', 'left', 'mem' + i);
      if (i === 2) { const wp = enterE(sg(t, 15.1, 15.5)); if (wp > .01) { g.strokeStyle = C.lime; g.lineWidth = 6; g.lineCap = 'round'; const w = 820, h = 68, per = 2 * (w + h); g.setLineDash([per * wp, per]); rr(126, y - 4, w + 8, h + 8, 26); g.stroke(); g.setLineDash([]); } }
      g.restore(); });
    // WRONG? sticker on the third row
    const wa = enterE(sg(t, 15.25, 15.7)); if (wa > .01) { g.save(); g.globalAlpha *= sm(wa * 1.6); g.translate(0, (1 - wa) * 22); sticker(700, cy0 + 251, 230, 66, 33, C.ink, { rot: -.07, off: 0, ol: 3 }, () => { tx('WRONG?', 115, 46, 36, 900, 'InterTight', C.lime, 'center', 'wrongchip'); }); g.restore(); }
    g.restore();
    // buttons
    const btn = (s, x, y, w, fill, rot, t0) => { const u = enterE(sg(t, t0, t0 + .5)), a = sm(sg(t, t0, t0 + .28)); if (a < .003) return; g.save(); g.globalAlpha *= a; g.translate(0, (1 - u) * 34 + fl(t, x, 4, 3.8));
      sticker(x, y, w, 92, 46, fill, { rot: rot * u, off: 8, s: .92 + .08 * u }, () => { tx(s, w / 2, 60, 38, 900, 'InterTight', C.ink, 'center', 'btn:' + s); }); g.restore(); };
    btn('Yes, it did', 100, 1090, 310, C.lime, -.03, 14.9); btn('No', 440, 1090, 170, C.white, .02, 15.1); btn('Tell me below ↓', 640, 1090, 340, C.lime, -.02, 15.3);
  }, 540, 760);
  // animated cursor path: tap the wrong row, then Tell me below
  const ca = sm(sg(t, 14.55, 14.85)) * (1 - sm(sg(t, 16.5, 16.7)));
  if (ca > .01) {
    const u1 = sm(sg(t, 14.6, 15.1)), u2 = sm(sg(t, 15.55, 16.22));
    let x = lerp(930, 560, u1), y = lerp(820, 975, u1); x = lerp(x, 835, u2); y = lerp(y, 1150, u2);
    g.save(); g.globalAlpha *= ca; ripple(560, 975, t, 15.1); ripple(835, 1150, t, 16.25);
    cursor(x, y, 1.1, Math.max(0, 1 - Math.abs(t - 15.1) / .12, 1 - Math.abs(t - 16.25) / .12)); g.restore();
  }
}
// ---------- scene F: link in bio (16.85 .. 18.8) ----------
function sceneE(t) {
  wrap(ev(t, 16.84, 18.6, .4, .17), () => {
    g.save(); g.translate(0, fl(t, 1, 5, 4)); const p = 1 + .015 * Math.sin(t * 6.283 / 1.7);
    g.save(); g.translate(540, 430); g.scale(p, p); g.translate(-540, -430);
    sticker(115, 330, 850, 200, 100, C.lime, { off: 12, ol: 6 }, () => {
      g.strokeStyle = C.ink; g.lineWidth = 11; g.lineCap = 'round'; rr(96, 78, 86, 46, 23); g.stroke(); rr(144, 96, 86, 46, 23); g.stroke();
      tx('Link in bio', 270, 138, 84, 900, 'InterTight', C.ink, 'left', 'linkbio'); });
    g.restore();
    // connector line drawing down the badges
    const lp = sm(sg(t, 17.25, 18.1)); g.strokeStyle = C.ink; g.lineWidth = 8; g.lineCap = 'round'; g.setLineDash([2, 16]); g.beginPath(); g.moveTo(222, 640); g.lineTo(222, 640 + 300 * lp); g.stroke(); g.setLineDash([]);
    const items = [['Settings', 1], ['Personalization', 2], ['Memory', 3]];
    items.forEach(([s, n], i) => { const a = enterE(sg(t, 17.15 + i * .22, 17.7 + i * .22)); g.save(); g.globalAlpha *= sm(a * 1.8); g.translate((1 - a) * -60, fl(t, i * 2.2, 4, 3.6 + i * .5));
      sticker(160, 600 + i * 150, 760, 116, 58, i === 2 ? C.lime : C.white, { off: 8, ol: 5 }, () => { tx(s, 150, 76, 50, 800, 'InterTight', C.ink, 'left', 'chip' + i); }); badge(n, 222, 658 + i * 150, 34, 1); g.restore(); });
    g.restore();
  }, 540, 700);
  const ca = sm(sg(t, 17.0, 17.2)) * (1 - sm(sg(t, 18.2, 18.4)));
  if (ca > .01) { const u = sm(sg(t, 17.0, 17.5)); const x = lerp(900, 780, u), y = lerp(640, 470, u); g.save(); g.globalAlpha *= ca; ripple(790, 480, t, 17.45); cursor(x, y, 1.1, Math.max(0, 1 - Math.abs(t - 17.45) / .12)); g.restore(); }
}
// ---------- scene G: tomorrow (18.85 .. 26.2) ----------
function sceneF(t) {
  const hw = n => T.l8 + WD.l8[n][1];
  wrap(ev(t, 18.86, 99, .45, 0), () => {
    g.save(); g.translate(0, fl(t, 2, 4, 4.2));
    logoBadge(100, 288, 100, 1, -.05 + .02 * Math.sin(t * 1.4));
    head(t, [[K('Tomorrow,', 19.0, 'ink')], [K('ChatGPT', hw(5)), K('can', hw(7))], [K('guess', hw(8), 'limeink'), K('your', hw(9))], [K('age.', hw(10), 'lime')]], 100, 540, 100, 112, { maxW: 820 });
    g.restore();
  }, 540, 700);
  wrap(ev(t, 19.1, 99, .4, 0), () => {
    g.save(); g.translate(0, fl(t, 4, 5, 4.7)); g.rotate(-.01 + .008 * Math.sin(t * .8));
    dcard(100, 920, 880, 290, 38); mark(132, 944, 52, '#fff'); tx('Birthday', 204, 986, 40, 700, 'Inter', '#fff', 'left', 'birthday');
    const fo = sm(sg(t, 19.7, 20.4)); g.fillStyle = C.dark2; rr(132, 1010, 816, 100, 26); g.fill();
    g.strokeStyle = fo > 0 ? `rgba(182,242,58,${.35 + .65 * fo})` : C.dark3; g.lineWidth = 3 + 3 * fo + (fo > 0 ? .8 * Math.sin(t * 4) : 0); rr(132, 1010, 816, 100, 26); g.stroke();
    tx('MM / DD / YYYY', 166, 1076, 40, 500, 'Inter', C.mute, 'left', 'datefield'); if (Math.sin(t * 6.283) > -.3) { g.fillStyle = C.lime; g.fillRect(150, 1034, 4, 52); }
    tag(948, 1130, 'example · re-created', { al: 'right', fill: C.wash });
    g.restore();
  }, 540, 1050);
  // UNDER 18? a beat earlier (20.3)
  wrap(ev(t, 20.3, 99, .45, 0), () => {
    g.save(); g.translate(0, fl(t, 4, 5, 4.7));
    sticker(650, 862, 330, 78, 39, C.lime, { rot: .04, off: 7, s: 1 + .025 * Math.sin(t * 4) }, () => { tx('UNDER 18?', 165, 53, 36, 900, 'InterTight', C.ink, 'center', 'under18'); });
    for (let k = 0; k < 2; k++) { const u = (((t - 20.8 - k * .85) % 1.7) + 1.7) % 1.7 / 1.7; if (t > 20.8) { g.save(); g.globalAlpha *= (1 - u) * .7; g.strokeStyle = C.ink; g.lineWidth = 4; rr(650 - 24 * u, 862 - 16 * u, 330 + 48 * u, 78 + 32 * u, 39 + 16 * u); g.stroke(); g.restore(); } }
    g.restore();
  }, 800, 900);
  // Follow: one tap at 24.95, then a lime burst and a settled ✓ keep the last second moving
  const TAP = 24.95;
  wrap(ev(t, 23.4, 99, .45, 0), () => {
    g.save(); g.translate(0, fl(t, 6, 4, 3.9)); const done = sm(sg(t, TAP, TAP + .3)), s = 1 + .025 * Math.sin(t * 3.1) + .08 * Math.sin(Math.PI * clamp((t - TAP) / .5)) * (t > TAP ? 1 : 0);
    sticker(630, 318, 340, 96, 48, done > .5 ? C.white : C.lime, { off: 9, ol: 5, s, rot: .02 }, () => {
      if (done > .5) { check(52, 48, 26, 1); tx('Following', 200, 66, 46, 900, 'InterTight', C.ink, 'center', 'follow'); } else tx('Follow', 170, 66, 50, 900, 'InterTight', C.ink, 'center', 'follow'); });
    g.restore();
    if (t > TAP) { const R = rng(5); for (let i = 0; i < 12; i++) { const ang = R() * 6.283, sp = 120 + R() * 200, u = (t - TAP - R() * .1), e = 1 - Math.exp(-Math.max(0, u) * 2.6); if (u < 0) continue;
      g.save(); g.globalAlpha *= clamp(1 - u / 1.25) * .9; g.fillStyle = i % 3 ? C.lime : C.ink; g.strokeStyle = C.ink; g.lineWidth = 3; g.beginPath(); g.arc(800 + Math.cos(ang) * sp * e, 366 + Math.sin(ang) * sp * e + 60 * u * u, i % 3 ? 9 : 5, 0, 7); g.fill(); if (i % 3) g.stroke(); g.restore(); } }
    const cu = sm(sg(t, 23.9, 24.9)); if (cu > .01 && t < TAP + .45) { const x = lerp(960, 880, cu) + Math.sin(cu * 3.14) * -18, y = lerp(560, 395, cu); g.save(); g.globalAlpha *= 1 - sm(sg(t, TAP + .2, TAP + .45)); cursor(x, y + fl(t, 0, 3, 2.7), 1, Math.max(0, 1 - Math.abs(t - TAP) / .12)); g.restore(); }
    ripple(880, 400, t, TAP);
  }, 800, 370);
}
function draw(t) {
  g.setTransform(1, 0, 0, 1, 0, 0); TXT.length = 0;
  const [z, cx, cy, px, py] = cam(t);
  g.save(); g.translate(cx + px, cy + py); g.scale(z, z); g.translate(-cx, -cy);
  background(t);
  sparkles(t);
  sceneA(t); sceneB(t); sceneQuote(t); sceneC(t); sceneD(t); sceneE(t); sceneF(t);
  g.restore();
}
window.render = (t) => { REC = false; draw(t); };
window.TEXTS = (t) => { REC = true; draw(t); REC = false; return TXT.map(o => ({ ...o })); };
window.EV = [
  { t: .25, type: 'tick' }, { t: 1.7, type: 'thud' }, { t: 2.85, type: 'whoosh' }, { t: 3.9, type: 'crash' }, { t: 4.32, type: 'thud' }, { t: 4.85, type: 'whoosh' },
  { t: 5.15, type: 'tick' }, { t: 6.3, type: 'ding' }, { t: 6.9, type: 'whoosh' }, { t: 7.92, type: 'thud' }, { t: 10.42, type: 'whoosh' }, { t: 10.85, type: 'click' },
  { t: 11.3, type: 'click' }, { t: 11.95, type: 'click' }, { t: 13.1, type: 'ding' }, { t: 13.85, type: 'whoosh' }, { t: 15.1, type: 'click' }, { t: 15.3, type: 'thud' }, { t: 16.25, type: 'click' },
  { t: 16.78, type: 'whoosh' }, { t: 17.45, type: 'click' }, { t: 18.8, type: 'whoosh' }, { t: 20.3, type: 'thud' }, { t: 24.95, type: 'ding' }];
window.READY = true;
