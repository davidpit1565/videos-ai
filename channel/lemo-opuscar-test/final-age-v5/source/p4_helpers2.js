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
// generic shatter: cv is the offscreen picture of the object (w x h), flying shards
function mkCv(w, h, fn) { const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const keep = g, kr = REC; REC = false; g = cv.getContext('2d'); fn(); g = keep; REC = kr; return cv; }
function shardsG(t, t0, cv, w, h, cols, rows, ix, iy, seed = 21, ox = 0, oy = 0) {   // ox/oy: where the picture's origin sits on the canvas, used to keep shards inside the safe area
  const R = rng(seed), cw = w / cols, ch = h / rows, pts = [];
  for (let j = 0; j <= rows; j++) { pts[j] = []; for (let i = 0; i <= cols; i++) pts[j][i] = [i * cw + ((i > 0 && i < cols) ? (R() - .5) * cw * .6 : 0), j * ch + ((j > 0 && j < rows) ? (R() - .5) * ch * .6 : 0)]; }
  const u = t - t0;
  for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) {
    const a = pts[j][i], b = pts[j][i + 1], c = pts[j + 1][i + 1], d = pts[j + 1][i];
    [[a, b, c], [a, c, d]].forEach(tri => {
      const cx = (tri[0][0] + tri[1][0] + tri[2][0]) / 3, cy = (tri[0][1] + tri[1][1] + tri[2][1]) / 3;
      let dx = cx - ix, dy = cy - iy; const L = Math.hypot(dx, dy) + 1; dx /= L; dy /= L;
      const sp = (300 + R() * 640 + 560 / (1 + L / 90)) * .5, rot = (R() - .5) * 9, delay = L / 3600;
      const uu = Math.max(0, u - delay), e = 1 - Math.exp(-uu * 2.4);
      let px = dx * sp * e / 2.4, py = dy * sp * e / 2.4 + 140 * uu * uu; px = clamp(cx + px + ox, 90, 990) - cx - ox; py = clamp(cy + py + oy, 290, 1220) - cy - oy;
      const al = 1 - sm(sg(uu, .4, .9));
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
