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
