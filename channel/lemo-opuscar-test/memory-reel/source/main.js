// ChatGPT memory film. Canvas 2D, pure function of t. Light living-screencast adaptation.
const W = 1080, H = 1920;
const cv = document.getElementById('c'), g = cv.getContext('2d');
await Promise.all([500,600,700,800,900].flatMap(w => [`${w} 40px Inter`, `${w} 40px InterTight`, `${w} 40px JBMono`]).map(f => document.fonts.load(f)));
const get = async (u, d) => { try { const r = await fetch(u); return r.ok ? await r.json() : d; } catch { return d; } };
const dur = await get('voices/dur.json', {});
const svg = await (await fetch('chatgpt.svg')).text();
const MARK = new Path2D(svg.match(/ d='([^']+)'/)[1]);
const C = { paper: '#F6F7F2', paper2: '#E7EADD', card: '#FFFFFF', ink: '#0E0F0C', ink2: '#4A4F44', lime: '#A3E635', limeDeep: '#5DA10E', wash: '#E6F8BB', grey: '#E4E7DC', grey2: '#CDD2C2' };
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const sg = (t, a, b) => clamp((t - a) / (b - a));
const sm = x => { x = clamp(x); return x * x * x * (x * (x * 6 - 15) + 10); };      // smootherstep
const enterE = x => 1 - Math.pow(1 - clamp(x), 4);                                   // long ease-out, no overshoot
const lerp = (a, b, t) => a + (b - a) * t;
// line starts (s): picture follows the voice
const T = { l1: .3, l2: 2.95, l3: 5.0, l4: 7.0, l5: 10.4, l6: 13.9, l7: 16.9, l8: 19.0 };
const DUR = 26.2; window.DUR = DUR;
const D = k => dur[k] || 2;
const TXT = [];                       // text boxes registered during a frame (post-camera)
let REC = false, CLIPX = null;
function reg(id, text, x0, y0, x1, y1) {
  if (!REC || g.globalAlpha < .5) return;
  const m = g.getTransform(), p = (x, y) => [m.a * x + m.c * y + m.e, m.b * x + m.d * y + m.f];
  const a = p(x0, y0), b = p(x1, y1);
  if (CLIPX && (Math.max(a[0], b[0]) < CLIPX[0] || Math.min(a[0], b[0]) > CLIPX[1])) return;
  TXT.push({ id, text, x0: Math.min(a[0], b[0]), y0: Math.min(a[1], b[1]), x1: Math.max(a[0], b[0]), y1: Math.max(a[1], b[1]) });
}
const F = (px, wt, fam) => `${wt} ${px}px ${fam}`;
function tx(s, x, y, px, wt, fam, col, al = 'left', id) {
  g.font = F(px, wt, fam); g.fillStyle = col; g.textAlign = al; g.textBaseline = 'alphabetic';
  g.fillText(s, x, y);
  const w = g.measureText(s).width, x0 = al === 'center' ? x - w / 2 : al === 'right' ? x - w : x;
  reg(id || s, s, x0, y - px * .8, x0 + w, y + px * .2);
  return w;
}
const rr = (x, y, w, h, r) => { w = Math.max(0, w); h = Math.max(0, h); g.beginPath(); g.roundRect(x, y, w, h, Math.max(0, Math.min(r, w / 2, h / 2))); };
function card(x, y, w, h, r = 36, o = {}) {
  g.save(); g.shadowColor = 'rgba(14,15,12,.13)'; g.shadowBlur = 40; g.shadowOffsetY = 12;
  g.fillStyle = o.fill || C.card; rr(x, y, w, h, r); g.fill(); g.restore();
  if (o.stroke) { g.strokeStyle = o.stroke; g.lineWidth = o.lw || 2; rr(x, y, w, h, r); g.stroke(); }
}
// enter/exit envelope: returns {a,dy,s}
const env = (t, t0, d = .9, t1 = 1e9, d1 = .5) => {
  const p = enterE(sg(t, t0, t0 + d)), q = sm(sg(t, t1, t1 + d1));
  return { a: sm(sg(t, t0, t0 + d * .7)) * (1 - q), dy: (1 - p) * 40 + q * -24, s: .96 + .04 * p, on: t >= t0 && t < t1 + d1 };
};
function wrap(e, fn, cx = 540, cy = 760) {
  if (e.a <= .002) return;
  g.save(); g.globalAlpha *= e.a; g.translate(cx, cy + e.dy); g.scale(e.s, e.s); g.translate(-cx, -cy); fn(); g.restore();
}
const fl = (t, ph, amp = 4, per = 9) => Math.sin(t * 6.283 / per + ph) * amp;   // ambient float
// word timing inside a line
function wordT(key, words) {
  const s = T[key] + .06, e = T[key] + D(key) - .06, w = words.map(x => x.length + 1.5), tot = w.reduce((a, b) => a + b, 0);
  let acc = 0; return words.map((x, i) => { const a = s + (e - s) * acc / tot; acc += w[i]; return [a, s + (e - s) * acc / tot]; });
}
// headline lines (array of {words,[key], wash}), words lit by spoken time
function headline(t, lines, x, y0, px, lh, o = {}) {
  g.save(); g.font = F(px, 900, 'InterTight');
  let k = 0, S = 1;
  g.font = F(px, 900, 'InterTight');
  lines.forEach(ln => { const t0 = ln.words.map(w => g.measureText(w).width); const fu = t0.reduce((a, b) => a + b, 0) + px * .26 * (ln.words.length - 1); S = Math.min(S, (o.maxW || 890) / fu); });
  lines.forEach((ln, li) => {
    const ws = ln.words, times = ln.times;
    let sp, tot, full; const f = px * S; g.font = F(f, 900, 'InterTight'); tot = ws.map(w => g.measureText(w).width); sp = f * .26;
    full = tot.reduce((a, b) => a + b, 0) + sp * (ws.length - 1);
    let cx = o.center ? 540 - full / 2 : x;
    const y = y0 + li * lh;
    ws.forEach((w, i) => {
      const lit = times ? sm(sg(t, times[i][0] - .05, times[i][0] + .25)) * (o.keepLit ? 1 : 1 - sm(sg(t, times[i][1] + .6, times[i][1] + 1.0)) * (o.fade ?? 0)) : 0;
      const base = ln.wash ? .45 : 0, a = Math.max(base, lit);
      const ent = o.stagger ? enterE(sg(t, o.t0 + (k * .09), o.t0 + k * .09 + .8)) : 1; k++;
      g.save(); g.globalAlpha *= ent; g.translate(0, (1 - ent) * 28);
      if (a > .01) { g.fillStyle = C.lime; g.globalAlpha *= a; rr(cx - 10, y - f * .82, tot[i] + 20, f * .98, 16); g.fill(); g.globalAlpha /= a; }
      g.font = F(f, 900, 'InterTight'); g.fillStyle = C.ink; g.textAlign = 'left'; g.textBaseline = 'alphabetic'; g.fillText(w, cx, y);
      reg('h:' + w + li + i, w, cx, y - f * .78, cx + tot[i], y + f * .05);
      g.restore();
      cx += tot[i] + sp;
    });
  });
  g.restore();
}
const split = (s, key) => { const w = s.split(' '); return { words: w, times: key ? wordT(key, w) : null }; };
function mark(x, y, s, tile = true) {   // real ChatGPT mark, no geometry change; tile optional lime
  g.save(); g.translate(x, y);
  if (tile) { g.fillStyle = C.lime; rr(0, 0, s, s, s * .28); g.fill(); g.translate(s * .14, s * .14); g.scale(s * .72 / 320, s * .72 / 320); }
  else g.scale(s / 320, s / 320);
  g.fillStyle = C.ink; g.fill(MARK); g.restore();
}
function tag(x, y, s, al = 'left') {   // small mono tag
  g.save(); g.font = F(26, 500, 'JBMono'); const w = g.measureText(s).width + 28;
  const x0 = al === 'right' ? x - w : x;
  g.fillStyle = 'rgba(14,15,12,.07)'; rr(x0, y, w, 40, 20); g.fill();
  tx(s, x0 + 14, y + 29, 26, 500, 'JBMono', C.ink2, 'left', 'tag:' + s); g.restore();
}
function note(x, y, text, o = {}) {   // the one recurring object
  const w = 340, h = 80; g.save(); g.translate(x + w / 2, y + h / 2 + (o.fl || 0)); g.rotate(o.rot || 0); g.scale(o.s || 1, o.s || 1); g.translate(-w / 2, -h / 2);
  g.globalAlpha *= o.a ?? 1;
  g.save(); g.shadowColor = 'rgba(14,15,12,.14)'; g.shadowBlur = 22; g.shadowOffsetY = 8; g.fillStyle = C.wash; rr(0, 0, w, h, 22); g.fill(); g.restore();
  g.strokeStyle = 'rgba(93,161,14,.55)'; g.lineWidth = 2; rr(0, 0, w, h, 22); g.stroke();
  g.fillStyle = C.limeDeep; g.beginPath(); g.arc(34, 40, 11, 0, 7); g.fill(); g.fillStyle = 'rgba(255,255,255,.55)'; g.beginPath(); g.arc(31, 37, 4, 0, 7); g.fill();
  tx(text, 60, 51, 30, 700, 'Inter', C.ink, 'left', 'note:' + text);
  g.restore();
}
function bars(x, y, ws, p, col = C.grey) { ws.forEach((w, i) => { g.fillStyle = col; rr(x, y + i * 36, w * p, 15, 8); g.fill(); }); }
function typed(s, p) { const n = Math.floor(s.length * p); return s.slice(0, n); }
function typeP(t, t0, t1, n, seed = 1) {   // natural, uneven typing progress 0..1
  const u = sg(t, t0, t1); const w = u + .035 * Math.sin(u * 17 + seed) * (1 - u) * u * 4; return clamp(w);
}
function caret(x, y, h, t) { const a = .5 + .5 * Math.sin(t * 6.283 * 1.1); g.fillStyle = `rgba(14,15,12,${.25 + .6 * a})`; g.fillRect(x, y, 3, h); }
function trash(x, y, s, col) {
  g.save(); g.translate(x, y); g.scale(s, s); g.strokeStyle = col; g.lineWidth = 3; g.lineCap = 'round'; g.lineJoin = 'round';
  g.beginPath(); g.moveTo(-10, -8); g.lineTo(10, -8); g.moveTo(-4, -12); g.lineTo(4, -12); g.moveTo(-8, -8); g.lineTo(-6.5, 12); g.lineTo(6.5, 12); g.lineTo(8, -8); g.moveTo(-2.5, -3); g.lineTo(-2.5, 7); g.moveTo(2.5, -3); g.lineTo(2.5, 7); g.stroke(); g.restore();
}
function chev(x, y, col = C.ink2) { g.strokeStyle = col; g.lineWidth = 4; g.lineCap = 'round'; g.beginPath(); g.moveTo(x - 6, y - 12); g.lineTo(x + 6, y); g.lineTo(x - 6, y + 12); g.stroke(); }
function ring(x, y, w, h, r, p, col = C.limeDeep) {  // line-draw ring (linear is allowed for line draws)
  if (p <= .03) return; g.save(); g.strokeStyle = col; g.lineWidth = 5; g.lineCap = 'round';
  const per = 2 * (w + h) - (8 - 2 * Math.PI) * r; g.setLineDash([per * p, per]); g.lineDashOffset = 0; rr(x, y, w, h, r); g.stroke(); g.restore();
}
// ---------- camera ----------
const K = [[0, 1.0, 540, 860], [2.9, 1.02, 540, 900], [5.0, 1.0, 540, 860], [6.4, 1.02, 540, 800], [7.2, 1.0, 540, 900], [8.7, 1.018, 540, 980], [10.8, 1.0, 540, 860], [12.5, 1.02, 540, 900], [14.2, 1.0, 540, 860], [16.5, 1.015, 540, 800], [19.5, 1.0, 540, 860], [26.2, 1.024, 540, 880]];
function cam(t) {
  let i = 0; while (i < K.length - 2 && t > K[i + 1][0]) i++;
  const p = (j) => K[Math.max(0, Math.min(K.length - 1, j))], a = p(i), b = p(i + 1), u = clamp((t - a[0]) / (b[0] - a[0])), s = sm(u);
  return [lerp(a[1], b[1], s), lerp(a[2], b[2], s), lerp(a[3], b[3], s)];
}
function background(t) {
  g.fillStyle = C.paper; g.fillRect(-200, -200, W + 400, H + 400);
  const b1 = 1 + .05 * Math.sin(t * 6.283 / 9), b2 = 1 + .06 * Math.sin(t * 6.283 / 13 + 2);
  let gr = g.createRadialGradient(900, 420, 0, 900, 420, 620 * b1); gr.addColorStop(0, 'rgba(163,230,53,.30)'); gr.addColorStop(1, 'rgba(163,230,53,0)'); g.fillStyle = gr; g.fillRect(-200, -200, W + 400, H + 400);
  gr = g.createRadialGradient(120, 1500, 0, 120, 1500, 700 * b2); gr.addColorStop(0, 'rgba(163,230,53,.22)'); gr.addColorStop(1, 'rgba(163,230,53,0)'); g.fillStyle = gr; g.fillRect(-200, -200, W + 400, H + 400);
  const ox = (t * 7) % 54, oy = (t * 5) % 54; g.fillStyle = C.paper2;
  for (let x = -108; x < W + 108; x += 54) for (let y = -108; y < H + 108; y += 54) { g.beginPath(); g.arc(x + ox, y + oy, 2.6, 0, 7); g.fill(); }
}
// ---------- scenes ----------
const CLAIM = [split('CHATGPT CAN KEEP', 'l1'), split('NOTES ABOUT YOU.', 'l1'), split('EVEN AFTER YOU', 'l2'), split('DELETE THE CHAT.', 'l2')];
// per-word times: line 1 words are the first 6 words of L1, spread over both lines
(() => { const all = wordT('l1', ['CHATGPT', 'CAN', 'KEEP', 'NOTES', 'ABOUT', 'YOU']); CLAIM[0].times = all.slice(0, 3); CLAIM[1].times = all.slice(3, 6);
  const a2 = wordT('l2', ['EVEN', 'AFTER', 'YOU', 'DELETE', 'THE', 'CHAT']); CLAIM[2].times = a2.slice(0, 3); CLAIM[3].times = a2.slice(3, 6); CLAIM[2].wash = CLAIM[3].wash = true; })();
function sceneClaim(t) {   // S1 + S2 : 0 .. 5.3
  const e = env(t, -1, .01, 4.55, .5);
  wrap(e, () => {
    const tile = enterE(sg(t, 0, .01));
    mark(80, 290, 120); tx('ChatGPT', 224, 372, 60, 800, 'InterTight', C.ink, 'left', 'ChatGPT');
    headline(t, CLAIM, 80, 502, 94, 94, { keepLit: false, fade: 0 });
  });
}
function sceneChat(t) {
  // S1 chat card (0..2.9) then shrinks to the left (S2) and dims; notes drop to the right
  const sh = sm(sg(t, 2.95, 4.0)), out = sm(sg(t, 4.6, 5.1));
  const cx = 80, cy = 880, cw = 920, ch = 355;
  const sc = lerp(1, .6, sh), dx = lerp(0, 0, sh), dyv = lerp(0, 1235 - 880 - ch * .6 + 0, sh);
  const al = lerp(1, .62, sh) * (1 - out);
  if (al > .002) {
    g.save(); g.globalAlpha *= al; g.translate(cx, cy + (sh > 0 ? lerp(0, (1235 - cy) - ch * sc, sh) : 0) + fl(t, 0, 3, 10)); g.scale(sc, sc);
    card(0, 0, cw, ch, 40);
    // user bubble, typed
    const p = typeP(t, -.5, 1.4, 26, 3), q = 'what do you know about me?', s0 = typed(q, Math.max(p, .7));
    g.fillStyle = C.wash; rr(330, 25, 590, 84, 30); g.fill();
    const shown = t < 1.4 ? typed(q, .72 + .28 * sm(sg(t, 0, 1.4))) : q;
    tx(shown, 360, 80, 38, 600, 'Inter', C.ink, 'left', 'prompt');
    if (t < 2) { const w = g.measureText(shown).width; caret(360 + w + 4, 48, 44, t); }
    // answer
    const a1 = sm(sg(t, -1, .01));
    tx('You like short answers.', 44, 168, 38, 600, 'Inter', C.ink, 'left', 'ans1');
    bars(44, 200, [640, 520], sm(sg(t, .5, 2.2)) * .8 + .2);
    tag(44, 300, 'example · re-created');
    g.restore();
  }
  // notes (stack right of the chat during S2)
  const slots = [[650, 1135], [650, 1030], [650, 925]], names = ['Likes short answers', 'Studying for exams', 'Has a dog'];
  // note 1: peels out of the chat in S1, flies to slot 0 during 1.7..3.3 (long eased path)
  const n1 = sm(sg(t, 1.5, 3.4));
  const n1x = lerp(650, slots[0][0], n1), n1y = lerp(1030, slots[0][1], n1);
  const nOut = sm(sg(t, 4.6, 5.1));
  if (t > 1.4 && nOut < 1) {
    note(n1x, n1y, names[0], { a: sm(sg(t, 1.4, 2.0)) * (1 - nOut), fl: fl(t, 1), rot: -.03 * (1 - n1), s: 1 });
    [1, 2].forEach(i => { const e = env(t, 3.35 + (i - 1) * .55, 1.0, 4.6, .5); if (e.on) note(slots[i][0], slots[i][1] + e.dy, names[i], { a: e.a, fl: fl(t, i * 2), s: e.s }); });
  }
}
function scenePrompt(t) {   // S3 5.0 .. 7.3
  const e = env(t, 4.7, .9, 6.7, .4);
  wrap(e, () => {
    const w1 = wordT('l3', ['Ask', 'it', 'what', 'do', 'you', 'know', 'about', 'me?']);
    const lane = [{ words: ['ASK', 'IT:'], times: [w1[0], w1[1]] }];
    headline(t, lane, 80, 400, 150, 140, { keepLit: true });
    // prompt card
    g.save(); g.translate(0, fl(t, 3, 3, 8));
    card(80, 560, 920, 140, 36);
    const words = ['what', 'do', 'you', 'know', 'about', 'me?'], tm = w1.slice(2);
    let cx = 120; g.font = F(52, 700, 'Inter');
    words.forEach((w, i) => { const wd = g.measureText(w).width; const lit = sm(sg(t, tm[i][0] - .05, tm[i][0] + .2));
      if (lit > .01) { g.save(); g.globalAlpha *= lit; g.fillStyle = C.lime; rr(cx - 8, 590, wd + 16, 72, 14); g.fill(); g.restore(); }
      g.font = F(52, 700, 'Inter'); g.fillStyle = C.ink; g.textAlign = 'left'; g.fillText(w, cx, 641); reg('p:' + w, w, cx, 600, cx + wd, 650); cx += wd + 16; });
    g.restore();
    // answer card: generic example, deliberately not a full list
    const e2 = env(t, 5.45, .9);
    wrap(e2, () => {
      g.save(); g.translate(0, fl(t, 1, 3, 11));
      card(80, 740, 920, 440, 40);
      const L = ['You like short answers.', 'You’re studying for exams.', 'You have a dog.'];
      L.forEach((s, i) => { const a = sm(sg(t, 5.9 + i * .3, 6.5 + i * .3)); g.save(); g.globalAlpha *= a; g.translate(0, (1 - a) * 18);
        g.fillStyle = C.limeDeep; g.beginPath(); g.arc(128, 835 + i * 92, 12, 0, 7); g.fill();
        tx(s, 160, 848 + i * 92, 44, 600, 'Inter', C.ink, 'left', 'a' + i); g.restore(); });
      const a = sm(sg(t, 6.5, 7.0)); g.save(); g.globalAlpha *= a; tx('…', 160, 1100, 44, 600, 'Inter', C.ink2, 'left', 'dots'); g.restore();
      tag(120, 1124, 'example · re-created');
      tag(960, 1124, 'not the full list', 'right');
      g.restore();
    }, 540, 960);
  }, 540, 760);
}
function sceneTwist(t) {   // S4 7.0 .. 11.2
  const e = env(t, 6.95, .9, 10.4, .5);
  // headline cross-fade
  wrap(env(t, 6.95, .9, 7.85, .3), () => headline(t, [{ words: ['DELETE', 'THE', 'CHAT.'], times: wordT('l4', ['Delete', 'the', 'chat,', 'the', 'note', 'stays']).slice(0, 3) }], 80, 420, 124, 120, { keepLit: true }), 540, 400);
  wrap(env(t, 8.1, .8, 10.0, .3), () => headline(t, [{ words: ['THE', 'NOTE', 'STAYS.'], times: wordT('l4', ['Delete', 'the', 'chat,', 'the', 'note', 'stays']).slice(3) }], 80, 420, 124, 120, { keepLit: true }), 540, 400);
  // stage: chat list + note
  wrap(e, () => {
    const del = sm(sg(t, 7.55, 8.5)), row = 84, listH = lerp(3 * row + 40, 2 * row + 40, del);
    g.save(); g.translate(0, fl(t, 2, 3, 10)); card(80, 560, 500, listH, 32);
    // row1: highlighted, shrinks
    const r1h = row * (1 - del);
    g.save(); g.beginPath(); g.rect(80, 560, 500, listH); g.clip();
    if (r1h > 1) { g.save(); g.globalAlpha *= 1 - del; g.fillStyle = C.wash; rr(100, 580, 460, r1h - 8, 20); g.fill();
      tx('Chat about dinner', 124, 580 + (r1h - 8) / 2 + 12, 30, 600, 'Inter', C.ink, 'left', 'row1');
      const ta = sm(sg(t, 7.1, 7.4)); trash(525, 580 + (r1h - 8) / 2, 1.2, C.ink); g.restore(); }
    const y2 = 580 + r1h; [0, 1].forEach(i => { g.fillStyle = C.grey; rr(124, y2 + i * row + 30, i ? 230 : 300, 15, 8); g.fill(); g.fillStyle = C.paper2; rr(100, y2 + i * row + 62, 460, 2, 1); g.fill(); });
    g.restore();
    ring(512, 572, 52, 52, 26, sm(sg(t, 7.15, 7.6)) * (1 - sm(sg(t, 7.9, 8.2))));
    tag(100, 560 + listH + 16, 'example · re-created');
    g.restore();
    // note card persists, pinned right
    const nA = sm(sg(t, 7.0, 7.8)); note(620, 590 + fl(t, 4, 4, 8), 'Studying for exams', { a: nA });
    ring(612, 582 + fl(t, 4, 4, 8), 356, 96, 28, sm(sg(t, 8.5, 9.1)));
    const sa = sm(sg(t, 8.7, 9.3)); g.save(); g.globalAlpha *= sa; g.translate(0, (1 - sa) * 12); tag(620, 692, 'still here'); g.restore();
  }, 540, 640);
  // quote card
  const qa = sm(sg(t, 7.05, 7.35)) * (1 - sm(sg(t, 10.65, 11.05)));
  if (qa > .002) {
    const p = enterE(sg(t, 7.05, 7.95)), push = 1 + .012 * sm(sg(t, 7.9, 10.7)); g.save(); g.globalAlpha *= qa; g.translate(540, 1078 + (1 - p) * 70 + fl(t, 5, 2, 9)); g.scale(push * (.97 + .03 * p), push * (.97 + .03 * p)); g.translate(-540, -1078);
    card(80, 915, 920, 320, 36, { stroke: 'rgba(93,161,14,.45)', lw: 3 });
    const qs = ['…even if you delete a chat, any saved', 'memories from it can still be used in', 'future conversations.'];
    // marker bands (behind words): "even if you delete a chat" 8.0-8.7, "any saved memories ... can still be used" 8.9-10.0
    const b1 = sm(sg(t, 8.0, 8.6)), b2 = sm(sg(t, 8.9, 9.6));
    g.font = F(40, 600, 'Inter'); const wd = s => g.measureText(s).width;
    g.save(); g.globalAlpha *= b1 * .95; g.fillStyle = C.lime; rr(120 + wd('…'), 954, wd('even if you delete a chat') + 8, 54, 12); g.fill(); g.restore();
    g.save(); g.globalAlpha *= b2 * .95; g.fillStyle = C.lime;
    rr(120 + wd('…even if you delete a chat, '), 954, wd('any saved') + 8, 54, 12); g.fill();
    rr(112, 1018, wd('memories from it can still be used in') + 16, 54, 12); g.fill(); g.restore();
    qs.forEach((s, i) => tx(s, 120, 996 + i * 64, 40, 600, 'Inter', C.ink, 'left', 'q' + i));
    tx('OpenAI Help Center, Memory FAQ', 120, 1212, 28, 500, 'JBMono', C.ink2, 'left', 'qsrc');
    g.restore();
  }
}
function sceneSettings(t) {   // S5 10.4 .. 14.5
  wrap(env(t, 10.4, .9, 13.7, .4), () => {
    const w = wordT('l5', ['Settings', 'Personalization', 'Memory']);
    const L = [{ words: ['Settings'], times: [w[0]] }, { words: ['>', 'Personalization'], times: [[w[1][0], w[1][1]], w[1]] }, { words: ['>', 'Memory'], times: [w[2], w[2]] }];
    headline(t, L, 80, 345, 76, 76, { keepLit: true, maxW: 880 });
  }, 540, 400);
  const e = env(t, 10.95, 1.0, 14.0, .5);
  wrap(e, () => {
    const sx = 115, sy = 590, sw = 850, sh = 600;
    g.save(); g.translate(0, fl(t, 1, 3, 11)); card(sx, sy, sw, sh, 40);
    g.save(); rr(sx, sy, sw, sh, 40); g.clip();
    // header
    g.fillStyle = C.paper; g.fillRect(sx, sy, sw, 84);
    const cur = sm(sg(t, 11.65, 12.3)) + sm(sg(t, 12.5, 13.15));   // 0..2 screen index
    const titles = ['Settings', 'Personalization', 'Memory'];
    const ti = Math.round(cur); tx(titles[ti], sx + sw / 2, sy + 56, 38, 800, 'InterTight', C.ink, 'center', 'title' + ti);
    if (cur > .02) { g.strokeStyle = C.ink2; g.lineWidth = 4; g.lineCap = 'round'; g.beginPath(); g.moveTo(sx + 50, sy + 30); g.lineTo(sx + 38, sy + 42); g.lineTo(sx + 50, sy + 54); g.stroke(); }
    const row = 84, y0 = sy + 100;
    const screen = i => { if (Math.abs(i - cur) >= 1) return; g.save(); { const m = g.getTransform(); CLIPX = [m.a * (sx + 4) + m.e, m.a * (sx + sw - 4) + m.e]; } g.translate((i - cur) * sw, 0);
      if (i === 0) [0, 1, 2, 3, 4].forEach(r => { const y = y0 + r * row; g.fillStyle = C.grey; g.beginPath(); g.arc(sx + 60, y + 38, 22, 0, 7); g.fill();
        if (r === 2) tx('Personalization', sx + 110, y + 50, 36, 600, 'Inter', C.ink, 'left', 'personalization'); else { g.fillStyle = C.grey; rr(sx + 110, y + 30, 150 + (r * 53) % 120, 16, 8); g.fill(); }
        chev(sx + sw - 50, y + 38); g.fillStyle = C.paper2; g.fillRect(sx + 110, y + row - 2, sw - 150, 2); });
      if (i === 1) [0, 1, 2].forEach(r => { const y = y0 + r * row; g.fillStyle = C.grey; g.beginPath(); g.arc(sx + 60, y + 38, 22, 0, 7); g.fill();
        if (r === 0) tx('Memory', sx + 110, y + 50, 36, 600, 'Inter', C.ink, 'left', 'memory-row'); else { g.fillStyle = C.grey; rr(sx + 110, y + 30, 210 + r * 40, 16, 8); g.fill(); }
        chev(sx + sw - 50, y + 38); g.fillStyle = C.paper2; g.fillRect(sx + 110, y + row - 2, sw - 150, 2); });
      if (i === 2) { const tg = 0;
        tx('Memory', sx + 50, y0 + 50, 36, 700, 'Inter', C.ink, 'left', 'memory-toggle');
        g.fillStyle = C.lime; rr(sx + sw - 140, y0 + 12, 90, 50, 25); g.fill(); g.fillStyle = '#fff'; g.beginPath(); g.arc(sx + sw - 50 - 27, y0 + 37, 20, 0, 7); g.fill();
        g.fillStyle = C.grey; rr(sx + 50, y0 + 96, 150, 54, 27); g.fill(); tx('Manage', sx + 125, y0 + 133, 28, 700, 'Inter', C.ink, 'center', 'manage');
        ['Likes short answers', 'Studying for exams', 'Has a dog'].forEach((s, r) => { const a = sm(sg(t, 13.1 + r * .25, 13.7 + r * .25)); g.save(); g.globalAlpha *= a; g.translate(0, (1 - a) * 18);
          const yy = y0 + 190 + r * 92; g.fillStyle = C.wash; rr(sx + 50, yy, sw - 100, 74, 22); g.fill();
          g.fillStyle = C.limeDeep; g.beginPath(); g.arc(sx + 90, yy + 37, 11, 0, 7); g.fill(); tx(s, sx + 120, yy + 48, 32, 700, 'Inter', C.ink, 'left', 'sn' + r); g.restore(); });
        ring(sx + 40, y0 + 182, sw - 80, 290, 30, sg(t, 13.6, 14.0));
      }
      CLIPX = null; g.restore(); };
    screen(0); screen(1); screen(2);
    g.restore();
    // cursor: smooth path with a slight arc; taps at 11.4 and 12.25, rests at row ends
    const P = [[10.9, 900, 1130], [11.5, 930, 880], [11.6, 930, 880], [12.3, 930, 706], [12.4, 930, 706], [13.3, 930, 1000]];
    let i = 0; while (i < P.length - 2 && t > P[i + 1][0]) i++;
    const a = P[i], b = P[i + 1], u = sm(sg(t, a[0], b[0])), cxp = lerp(a[1], b[1], u) + Math.sin(u * Math.PI) * -22, cyp = lerp(a[2], b[2], u);
    const click = Math.max(0, 1 - Math.abs(t - 11.57) / .22) + Math.max(0, 1 - Math.abs(t - 12.37) / .22), cs = 1 - .08 * clamp(click);
    const ca = sm(sg(t, 11.0, 11.3)) * (1 - sm(sg(t, 13.2, 13.6)));
    if (ca > .01) { g.save(); g.globalAlpha *= ca; g.translate(cxp, cyp); g.scale(cs, cs); g.fillStyle = C.ink; g.strokeStyle = '#fff'; g.lineWidth = 3; g.beginPath(); g.moveTo(0, 0); g.lineTo(0, 38); g.lineTo(10, 29); g.lineTo(18, 46); g.lineTo(26, 42); g.lineTo(18, 26); g.lineTo(31, 26); g.closePath(); g.stroke(); g.fill(); g.restore(); }
    tag(sx + 24, sy + sh + 14, 'example · re-created');
    g.restore();
  }, 540, 900);
}
function sceneComment(t) {   // S6 13.9 .. 17.2
  wrap(env(t, 14.05, .9, 16.7, .5), () => {
    const w = wordT('l6', ['Did', 'it', 'get', 'something', 'wrong', 'about', 'you?', 'Tell', 'me', 'below.']);
    headline(t, [{ words: ['WRONG', 'ABOUT', 'YOU?'], times: w.slice(4, 7) }, { words: ['TELL', 'ME', 'BELOW.'], times: w.slice(7) }], 80, 400, 120, 120, { keepLit: true });
  }, 540, 400);
  wrap(env(t, 14.35, 1.0, 16.7, .5), () => {
    g.save(); g.translate(0, fl(t, 2, 4, 9)); card(80, 720, 920, 300, 40);
    g.fillStyle = C.paper; rr(116, 752, 848, 96, 28); g.fill();
    tx('Add a comment…', 150, 813, 38, 500, 'Inter', '#8A9080', 'left', 'comment-ph');
    caret(150 + 330 + 8, 772, 56, t);
    // soft typing dots
    for (let i = 0; i < 3; i++) { const a = .35 + .5 * (.5 + .5 * Math.sin(t * 5 - i * .9)); g.fillStyle = `rgba(14,15,12,${a * .5})`; g.beginPath(); g.arc(150 + i * 28, 905, 8, 0, 7); g.fill(); }
    g.fillStyle = C.lime; rr(790, 880, 174, 90, 45); g.fill(); tx('Post', 877, 940, 36, 800, 'InterTight', C.ink, 'center', 'post');
    g.restore();
  }, 540, 860);
  // the note card lifts out of the settings sheet and tilts toward the field
  const m = sm(sg(t, 14.1, 15.6)), nx = lerp(165, 600, m), ny = lerp(1010, 1065, m) + fl(t, 3, 5, 8);
  const na = sm(sg(t, 14.0, 14.5)) * (1 - sm(sg(t, 16.7, 17.2)));
  if (na > .01) note(nx, ny, 'Studying for exams', { a: na, rot: -.07 * m, s: 1 + .04 * m });
  // arrow (outline) from note toward the field edge
  const aa = sm(sg(t, 15.4, 16.0)) * (1 - sm(sg(t, 16.7, 17.1)));
  if (aa > .01) { g.save(); g.globalAlpha *= aa; g.strokeStyle = C.limeDeep; g.lineWidth = 7; g.lineCap = 'round'; g.lineJoin = 'round'; const by = 1040 - 10 * Math.sin(t * 4);
    g.beginPath(); g.moveTo(520, by + 34); g.lineTo(520, by - 12); g.moveTo(500, by + 6); g.lineTo(520, by - 14); g.lineTo(540, by + 6); g.stroke(); g.restore(); }
}
function sceneEnd(t) {   // S7 16.9..19.4 locked scene A ; S8 19.0..26.4 scene B ; one continuous background
  // S7
  wrap(env(t, 16.7, .9, 18.6, .45), () => {
    g.save(); g.translate(0, fl(t, 1, 4, 9));
    const p = 1 + .02 * Math.sin(t * 6.283 / 1.4);
    g.save(); g.translate(540, 760); g.scale(p, p); g.translate(-540, -760);
    g.fillStyle = C.lime; g.shadowColor = 'rgba(93,161,14,.35)'; g.shadowBlur = 40; g.shadowOffsetY = 12; rr(130, 690, 820, 140, 70); g.fill(); g.shadowColor = 'transparent';
    // chain icon
    g.strokeStyle = C.ink; g.lineWidth = 9; g.lineCap = 'round'; rr(208, 735, 74, 40, 20); g.stroke(); rr(246, 749, 74, 40, 20); g.stroke();
    tx('Link in bio', 385, 790, 70, 900, 'InterTight', C.ink, 'left', 'linkbio'); g.restore();
    const chips = [['Settings', 200], ['Personalization', 330], ['Memory', 200]]; let x = 540 - (200 + 330 + 200 + 80) / 2;
    chips.forEach(([s, w], i) => { const a = sm(sg(t, 17.1 + i * .22, 17.7 + i * .22)); g.save(); g.globalAlpha *= a; g.translate(0, (1 - a) * 18);
      card(x, 890, w, 76, 38); tx(s, x + w / 2, 940, 32, 700, 'Inter', C.ink, 'center', 'chip' + i);
      if (i < 2) tx('>', x + w + 20, 938, 34, 800, 'Inter', C.ink2, 'center', 'chevchip' + i); g.restore(); x += w + 40; });
    g.restore();
  }, 540, 840);
  // S8
  const e8 = env(t, 18.7, 1.0);
  wrap(e8, () => {
    g.save(); g.translate(0, fl(t, 2, 3, 10));
    g.save(); g.globalAlpha *= sm(sg(t, 18.75, 19.3)); tx('TOMORROW', 540, 335, 46, 700, 'JBMono', C.ink2, 'center', 'tomorrow'); g.restore();
    const hw = wordT('l8', 'Tomorrow, I’ll show you how ChatGPT can guess your age from how you use it. Follow, so you can check it too.'.split(' '));
    // words: Tomorrow,0 I'll1 show2 you3 how4 ChatGPT5 can6 guess7 your8 age9
    headline(t, [{ words: ['CHATGPT', 'CAN', 'GUESS'], times: [hw[5], hw[6], hw[7]] }, { words: ['YOUR', 'AGE.'], times: [hw[8], hw[9]] }], 80, 460, 124, 118, { keepLit: true, stagger: true, t0: 18.8 });
    g.restore();
  }, 540, 700);
  wrap(env(t, 19.5, 1.0), () => {
    g.save(); g.translate(0, fl(t, 4, 4, 11));
    card(80, 660, 920, 300, 40); mark(116, 690, 100);
    tx('Birthday', 240, 755, 46, 700, 'Inter', C.ink, 'left', 'birthday');
    const fo = sm(sg(t, 20.9, 21.7));
    g.fillStyle = C.paper; rr(116, 816, 848, 100, 26); g.fill(); g.strokeStyle = fo > 0 ? `rgba(93,161,14,${.25 + .6 * fo})` : C.grey2; g.lineWidth = 3 + 2 * fo; rr(116, 816, 848, 100, 26); g.stroke();
    tx('MM / DD / YYYY', 150, 882, 40, 500, 'Inter', '#8A9080', 'left', 'datefield');
    if (Math.sin(t * 6.283 * 1.1) > -.3) { g.fillStyle = 'rgba(14,15,12,.7)'; g.fillRect(132, 836, 3, 60); }
    g.restore();
    const ta = sm(sg(t, 21.6, 22.5)), tp = enterE(sg(t, 21.6, 22.6));
    g.save(); g.globalAlpha *= ta; g.translate(0, fl(t, 4, 4, 11) + (1 - tp) * 18); g.translate(790, 800); g.scale(.96 + .04 * tp, .96 + .04 * tp); g.translate(-790, -800);
    g.shadowColor = 'rgba(93,161,14,.45)'; g.shadowBlur = 24 + 10 * Math.sin(t * 3); g.fillStyle = C.lime; rr(700, 776, 250, 54, 27); g.fill(); g.shadowColor = 'transparent';
    tx('UNDER 18?', 825, 815, 32, 800, 'InterTight', C.ink, 'center', 'under18'); g.restore();
    for (let k = 0; k < 2; k++) { const u = ((t - 22.6 - k * .9) % 1.8 + 1.8) % 1.8 / 1.8; if (t > 22.6) { g.save(); g.globalAlpha *= (1 - u) * .55 * ta; g.strokeStyle = C.limeDeep; g.lineWidth = 4; rr(700 - 30 * u, 776 - 20 * u + fl(t, 4, 4, 11), 250 + 60 * u, 54 + 40 * u, 27 + 20 * u); g.stroke(); g.restore(); } }
    tag(100, 976, 'example · re-created');
  }, 540, 800);
  wrap(env(t, 23.0, 1.0), () => {
    const gl = .5 + .5 * Math.sin(t * 2.4);
    g.save(); g.translate(0, fl(t, 6, 3, 9)); g.shadowColor = `rgba(163,230,53,${.35 + .3 * gl})`; g.shadowBlur = 34; g.fillStyle = C.ink; rr(350, 1070, 380, 100, 50); g.fill(); g.shadowColor = 'transparent';
    tx('Follow', 540, 1137, 46, 800, 'InterTight', '#fff', 'center', 'follow'); g.restore();
  }, 540, 1120);
}
function draw(t) {
  g.setTransform(1, 0, 0, 1, 0, 0); TXT.length = 0;
  const [z, cx, cy] = cam(t);
  g.save(); g.translate(cx, cy); g.scale(z, z); g.translate(-cx, -cy);
  // camera drift: gentle slow sway
  g.translate(Math.sin(t * .5) * 3, Math.cos(t * .37) * 3);
  background(t);
  sceneClaim(t); sceneChat(t); scenePrompt(t); sceneTwist(t); sceneSettings(t); sceneComment(t); sceneEnd(t);
  g.restore();
}
window.render = (t) => { REC = false; draw(t); };
window.TEXTS = (t) => { REC = true; draw(t); REC = false; return TXT.map(o => ({ ...o })); };
window.EV = [
  { t: .35, type: 'tick' }, { t: 1.5, type: 'whoosh' }, { t: 3.35, type: 'thud' }, { t: 3.9, type: 'thud' }, { t: 4.9, type: 'whoosh' },
  { t: 5.1, type: 'tick' }, { t: 5.9, type: 'whoosh' }, { t: 7.2, type: 'click' }, { t: 7.55, type: 'whoosh' }, { t: 8.5, type: 'ding' }, { t: 11.0, type: 'whoosh' },
  { t: 11.55, type: 'click' }, { t: 12.35, type: 'click' }, { t: 13.15, type: 'thud' }, { t: 14.1, type: 'whoosh' }, { t: 16.9, type: 'whoosh' },
  { t: 18.95, type: 'whoosh' }, { t: 21.7, type: 'thud' }, { t: 23.1, type: 'tick' }];
window.READY = true;
