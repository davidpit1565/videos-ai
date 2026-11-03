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
const CUES = await get('voices/cues.json', {}); const T = CUES;   // line starts = the real narration cue times (David's cloned voice)
const wt = (l, i) => T[l] + Math.max(0, WD[l][i][1]);                                        // spoken start of word i of line l (lead-in clamp: a negative stamp is silence, not speech)
const DUR = 33.3; window.DUR = DUR;   // narration 33.0 s + .3 s tail
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
