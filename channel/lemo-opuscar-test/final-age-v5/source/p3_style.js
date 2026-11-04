// ---------- v5 style layer: themes, background (parallax + tapes), camera + shake, kinetic headline ----------
const THEMES = { paper: { fg: C.ink, dark: false }, dark: { fg: '#FFFFFF', dark: true }, lime: { fg: C.ink, dark: false } };
let TN = THEMES.paper, FG = C.ink;
const setTone = tone => { TN = THEMES[tone]; FG = TN.fg; };
const K = (s, t, k = '') => ({ s, t, k });
const pulse = (t, times, tau = .22) => times.reduce((a, ti) => a + (t >= ti ? Math.exp(-(t - ti) / tau) : 0), 0);
// screen shake + scale slam impacts: [t, amplitude px]
const SHK = [];
const addShake = (t, a) => SHK.push([t, a]);
function shake(t) {
  let x = 0, y = 0, z = 0;
  for (const [ti, a] of SHK) { const u = t - ti; if (u < 0 || u > .7) continue; const d = a * Math.exp(-u * 8.5); x += d * Math.sin(u * 83); y += d * .8 * Math.cos(u * 61 + 1); z += a / 900 * Math.exp(-u * 9); }
  return [x, y, z];
}
function cam(t) {
  const [sx, sy, sz] = shake(t);
  const z = 1.026 + .014 * Math.sin(t * 1.1 + .5) + .007 * Math.sin(t * 2.3 + 2) + sz, x = 16 * Math.sin(t * .7) + 7 * Math.sin(t * 1.7 + 1), y = 11 * Math.sin(t * .55 + 1);
  return [z, x + sx, y + sy, .004 * Math.sin(t * .6)];
}
// ---- background: tone + drifting dot grid + far rings + near stickers (different speeds) + two scrolling tapes of the real ChatGPT mark ----
function tape(y, rot, dir, speed, fill, ink, t) {
  g.save(); g.translate(540, y); g.rotate(rot); g.fillStyle = fill; g.fillRect(-900, -44, 1800, 88); g.fillStyle = ink; g.fillRect(-900, -44, 1800, 5); g.fillRect(-900, 39, 1800, 5);
  const step = 150, off = ((dir * speed * t) % step + step) % step;
  for (let i = -8; i <= 8; i++) { const x = i * step + off; g.save(); g.translate(x - 26, -26); g.scale(52 / 320, 52 / 320); g.fillStyle = ink; g.fill(MARK); g.restore(); g.beginPath(); g.arc(x + 75, 0, 7, 0, 7); g.fill(); }
  g.restore();
}
function bg(tone, t) {
  const dk = tone === 'dark', lm = tone === 'lime';
  g.fillStyle = dk ? C.dark : lm ? C.lime : C.paper; g.fillRect(-500, -500, W + 1000, H + 1000);
  const ox = -(t * 34) % 54, oy = (t * 22) % 54; g.fillStyle = dk ? '#262833' : lm ? '#A4D82B' : C.dot;
  for (let x = -108; x < W + 160; x += 54) for (let y = -108; y < H + 160; y += 54) { g.beginPath(); g.arc(x + ox, y + oy, 2.3, 0, 7); g.fill(); }
  // far layer: big rings, slow
  g.lineWidth = 12; g.strokeStyle = dk ? '#1F212A' : lm ? '#C3F55E' : '#EAEADF';
  [[120, 520, 210, 0], [980, 1000, 260, 2], [200, 1500, 190, 4], [900, 260, 170, 1]].forEach(([bx, by, r, ph]) => { g.beginPath(); g.arc(bx + 70 * Math.sin(t * .22 + ph), by + 90 * Math.cos(t * .17 + ph), r, 0, 7); g.stroke(); });
  // near layer: small outlined stickers rising at different speeds along the margins
  const R = rng(31), ink = dk ? '#FFFFFF' : C.ink;
  for (let i = 0; i < 12; i++) {
    const kx = R(), sp = 70 + R() * 110, ph = R() * 1900, kind = i % 4, sz = 16 + R() * 14, fillc = i % 3 === 0 ? (lm ? C.white : C.lime) : (dk ? C.dark3 : lm ? C.white : C.white);
    const x = (i % 2 ? 24 + kx * 70 : 986 + kx * 70) + 18 * Math.sin(t * .8 + ph), y = H + 120 - ((ph + t * sp) % (H + 240));
    g.save(); g.translate(x, y); g.rotate(t * (.6 + kx) + ph); g.lineWidth = 4; g.strokeStyle = ink; g.fillStyle = fillc; g.beginPath();
    if (kind === 0) g.arc(0, 0, sz, 0, 7); else if (kind === 1) { g.rect(-sz, -sz, sz * 2, sz * 2); } else if (kind === 2) { g.moveTo(0, -sz * 1.2); g.lineTo(sz * 1.1, sz); g.lineTo(-sz * 1.1, sz); g.closePath(); } else { g.moveTo(-sz, 0); g.lineTo(sz, 0); g.moveTo(0, -sz); g.lineTo(0, sz); }
    if (kind === 3) g.stroke(); else { g.fill(); g.stroke(); } g.restore();
  }
  // tapes: decor in the platform-UI bands (top 14%, bottom 35%)
  const tf = lm ? C.ink : C.lime, ti = lm ? C.lime : C.ink;
  tape(150, -.045, 1, 130, tf, ti, t); tape(1500, .04, -1, 170, tf, ti, t); tape(1720, -.03, 1, 110, dk ? C.dark3 : C.white, dk ? C.lime : C.ink, t);
}
// ---- kinetic headline: each word slams in at its spoken time (scale 1.25 to 1 + 2-3 px settle), key words in pills that pop ----
function head(t, rows, y0, px, lh, o = {}) {
  const fam = 'InterTight', dark = TN.dark, lm = FG === C.ink && o.limeBg;
  const wOf = (row, f) => { g.font = F(f, 900, fam); return row.reduce((a, k, i) => a + g.measureText(k.s).width + (k.k ? f * .5 : 0) + (i ? f * .28 : 0), 0); };
  let S = 1; rows.forEach(r => { S = Math.min(S, (o.maxW || 860) / wOf(r, px)); }); const f = px * S;
  rows.forEach((row, ri) => {
    const rw = wOf(row, f); let cx = o.center ? 540 - rw / 2 : (o.x || 100); const y = y0 + ri * lh * S;
    row.forEach((k, i) => {
      g.font = F(f, 900, fam); const tw = g.measureText(k.s).width, pad = k.k ? f * .25 : 0, bw = tw + pad * 2; if (i) cx += f * .28;
      const u = t - k.t;
      if (u > -.02) {
        const a = sm(u / .07), e = expoE(u / .2), sc = 1 + .3 * (1 - e) * (k.k ? 1.15 : 1), settle = u < .5 ? -3 * Math.exp(-u * 9) * Math.cos(u * 30) : 0, pp = k.k ? 1 + .09 * Math.sin(Math.PI * clamp(u / .32)) : 1;
        g.save(); g.globalAlpha *= a; g.translate(cx + bw / 2, y - f * .3 + settle + (1 - e) * f * .08); g.rotate((1 - e) * (((i + ri) % 2) ? .05 : -.05)); g.scale(sc * pp, sc * pp); g.translate(-bw / 2, f * .3);
        let col = FG;
        if (k.k) {
          const top = -f * .86, hh = f * 1.06;
          if (k.k === 'lime' || (dark && k.k === 'limeink')) { g.fillStyle = dark ? 'rgba(0,0,0,.45)' : C.ink; rr(f * .08, top + f * .08, bw, hh, f * .26); g.fill(); g.fillStyle = C.lime; rr(0, top, bw, hh, f * .26); g.fill(); g.lineWidth = Math.max(4, f * .05); g.strokeStyle = dark ? C.white : C.ink; rr(0, top, bw, hh, f * .26); g.stroke(); col = C.ink; }
          else { g.fillStyle = dark ? '#fff' : C.ink; rr(0, top, bw, hh, f * .26); g.fill(); col = k.k === 'limeink' ? C.lime : (dark ? C.ink : '#fff'); }
        }
        g.font = F(f, 900, fam); g.fillStyle = col; g.textAlign = 'left'; g.textBaseline = 'alphabetic'; g.fillText(k.s, pad, 0);
        if (u > .32) reg('h:' + k.s + ri + i, k.s, pad, -f * .78, pad + tw, f * .05);
        g.restore();
      }
      cx += bw;
    });
  });
}
