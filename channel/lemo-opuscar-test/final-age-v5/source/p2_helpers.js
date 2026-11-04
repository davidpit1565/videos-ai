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
