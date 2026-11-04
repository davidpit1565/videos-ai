// ---------- v5 scenes. Every time below is a cue time (wt/we/T), never a constant. ----------
const TRD = .3, t0s = n => T['l' + n] - .16;       // scene n starts growing out of the previous one .16 s before its line is spoken
function pushIn(t, t0, cx, cy, amt = .4, dur = .3, tilt = 0) { const u = t - t0; if (u < 0) return false; const e = expoE(u / dur); g.save(); g.globalAlpha *= sm(u / .07); g.translate(cx, cy + (1 - e) * 10); g.rotate(tilt * (1 - e)); g.scale(1 + amt * (1 - e), 1 + amt * (1 - e)); g.translate(-cx, -cy); return true; }
function popIn(t, t0, cx, cy, dur = .38, rot = 0) { const u = t - t0; if (u < 0) return false; const b = backE(u / dur); g.save(); g.globalAlpha *= sm(u / .06); g.translate(cx, cy); g.rotate(rot * (1 - b)); const s = .35 + .65 * b; g.scale(s, s); g.translate(-cx, -cy); return true; }
function lcard(x, y, w, h, r = 36) { g.save(); g.shadowColor = 'rgba(0,0,0,.45)'; g.shadowBlur = 40; g.shadowOffsetY = 16; g.fillStyle = '#262932'; rr(x, y, w, h, r); g.fill(); g.restore(); g.lineWidth = 4; g.strokeStyle = C.lime; rr(x, y, w, h, r); g.stroke(); }
const EXAMPLE = 'example · re-created';
// ===== A: the claim =====
const tw1 = i => i === 0 ? .1 : wt('l1', i);                 // first word lands at 0.1 s
const HT = tw1(5) - .02;                                      // "teen" spoken: badge stamped TEEN
function ageFace(label, fill, fg) { sticker(0, 0, 300, 120, 34, fill, { off: 9, ol: 6 }, () => { tx(label, 150, 86, 72, 900, 'InterTight', fg, 'center', 'badge:' + label); }); }
const FACE_ADULT = mkCv(322, 142, () => ageFace('ADULT', C.lime, C.ink));
function sceneA(t) {
  const p = pulse(t, [0, 1, 2, 3, 4, 5, 6, 7].map(tw1), .25), ent = 1 + .14 * (1 - expoE(t / .4));
  // sunburst behind the mark
  g.save(); g.translate(540, 440); g.rotate(t * .4); g.fillStyle = C.wash;
  for (let i = 0; i < 12; i++) { const a = i * Math.PI / 6, R = 400 + 18 * Math.sin(t * 3 + i); g.beginPath(); g.moveTo(0, 0); g.lineTo(Math.cos(a) * R, Math.sin(a) * R); g.lineTo(Math.cos(a + .26) * R, Math.sin(a + .26) * R); g.closePath(); g.fill(); }
  g.restore();
  logoBadge(390, 290, 300, (1 + .08 * p) * ent, -.07 + .06 * Math.sin(t * 1.9) + .05 * p);
  head(t, [[K('CHATGPT', tw1(0)), K('MIGHT', tw1(1))], [K('THINK', tw1(2)), K("YOU'RE", tw1(3))], [K('A', tw1(4)), K('TEEN', tw1(5), 'limeink')], [K('RIGHT', tw1(6)), K('NOW!', tw1(7), 'lime')]], 706, 100, 98, { center: true, maxW: 860 });
  // profile card (example)
  const u = t - HT, sk = u > 0 && u < .35 ? Math.sin(t * 90) * 8 * (1 - u / .35) : 0;
  g.save(); g.translate(100 + sk, 1040 + fl(t, 0, 5, 3.4)); g.rotate(-.008 + .006 * Math.sin(t * .9));
  dcard(0, 0, 880, 200, 36); tag(170, 140, EXAMPLE, { fill: C.wash });
  g.fillStyle = C.lime; g.beginPath(); g.arc(88, 100, 52, 0, 7); g.fill(); g.lineWidth = 5; g.strokeStyle = C.ink; g.stroke(); icon('user', 88, 100, 1.3);
  tx('Your account', 170, 90, 36, 800, 'InterTight', '#fff', 'left', 'acct'); tx('birth year 1996', 170, 128, 26, 600, 'Inter', '#BFC2B4', 'left', 'born');
  g.save(); g.translate(540, 40);
  if (u < 0) { g.translate(0, fl(t, 3, 3, 2.2)); g.drawImage(FACE_ADULT, 0, 0); }
  else {
    shardsG(t, HT, FACE_ADULT, 322, 142, 6, 3, 160, 70, 21, 640, 1080);
    const k = expoE(u / .17), sc = 1 + 1.7 * (1 - k), a = sm(u / .05);
    g.save(); g.globalAlpha *= a; g.translate(150, 60); g.rotate(-.16 * (1 - k) + .02 * Math.sin(t * 1.3)); g.scale(sc, sc); g.translate(-150, -60); ageFace('TEEN', C.ink, C.lime); g.restore();
  }
  g.restore(); g.restore();
  ring(690, 1140, t, HT, .7, C.lime, 380);
}
// ===== B: even with a typed birthday =====
const BD = wt('l2', 5) - .25;
const QUOTE = [['“It can identify an account as eligible', 0], ['for the ChatGPT for Teens experience', 0], ['even if you already gave your date of', 1], ['birth when you created your account.”', 2]];
function sceneB(t) {
  head(t, [[K('EVEN', wt('l2', 0)), K('IF', wt('l2', 1)), K('YOU', wt('l2', 2))], [K('TYPED', wt('l2', 3), 'ink'), K('YOUR', wt('l2', 4))], [K('BIRTHDAY!', wt('l2', 5), 'lime')]], 410, 108, 104, { center: true, maxW: 860 });
  if (pushIn(t, T.l2 + .3, 540, 750, .25, .3)) {   // birthday field
    g.translate(0, fl(t, 2, 4, 3.4)); sticker(100, 675, 880, 150, 34, C.white, { off: 10, ol: 5 });
    tx('Birthday', 134, 718, 30, 800, 'InterTight', C.ink2, 'left', 'bday'); tag(300, 680, EXAMPLE, { fill: C.wash });
    g.fillStyle = '#ECECE4'; rr(130, 735, 820, 76, 20); g.fill(); g.strokeStyle = C.ink; g.lineWidth = 3; rr(130, 735, 820, 76, 20); g.stroke();
    const pp = typeP(t, BD, BD + .6, 5), s = typed('03 / 14 / 1996', pp); tx(s, 160, 788, 46, 700, 'JBMono', C.ink, 'left', 'bdval'); g.font = F(46, 700, 'JBMono'); if (pp < 1) caret(160 + g.measureText(s).width + 6, 746, 54, t, C.limeDeep);
    const ck = backE(sg(t, BD + .65, BD + 1.0)); if (ck > .01) check(620, 773, 28 * ck, clamp(ck));
    g.restore();
  }
  // quote card
  if (pushIn(t, T.l2 + .75, 540, 1050, .3, .3, -.02)) {
    g.translate(0, fl(t, 6, 4, 4.4)); sticker(95, 870, 890, 370, 34, C.white, { off: 10, ol: 5 });
    let fs = 39; g.font = F(fs, 700, 'Inter'); const wmax = Math.max(...QUOTE.map(q => g.measureText(q[0]).width)); fs = Math.min(40, 39 * 790 / wmax); g.font = F(fs, 700, 'Inter');
    const total = QUOTE.reduce((a, q) => a + q[0].length, 0), pq = typeP(t, T.l2 + 1.0, T.l2 + 2.3, 2); let left = Math.floor(total * pq);
    const hs = enterE(sg(t, BD, BD + .5));
    QUOTE.forEach((q, i) => { const y = 950 + i * 60, vis = q[0].slice(0, Math.max(0, Math.min(q[0].length, left)));
      if (q[1] && hs > .01) { g.font = F(fs, 700, 'Inter'); let w0 = g.measureText(q[0]).width; if (q[1] === 2) w0 = g.measureText('birth').width; g.fillStyle = C.lime; rr(125, y - 40, (w0 + 16) * hs, 54, 12); g.fill(); }
      tx(vis, 133, y, fs, 700, 'Inter', C.ink, 'left', 'q' + i); left -= q[0].length; });
    g.font = F(fs, 700, 'Inter'); if (pq < 1) { const lines = QUOTE.map(q => q[0]); let rem = Math.floor(total * pq), li = 0; while (li < 3 && rem > lines[li].length) { rem -= lines[li].length; li++; } caret(133 + g.measureText(lines[li].slice(0, rem)).width + 6, 950 + li * 60 - 38, 46, t, C.limeDeep); }
    sticker(133, 1170, 400, 56, 28, C.lime, { off: 6, ol: 4 }, () => { tx('OpenAI Help Center', 24, 39, 28, 800, 'InterTight', C.ink, 'left', 'qsrc'); });
    g.restore();
  }
  // STILL TEEN? slap
  const su = t - (BD + .85);
  if (su > 0) { const k = expoE(su / .18); g.save(); g.globalAlpha *= sm(su / .05); g.translate(820, 800 + fl(t, 4, 4, 3.3)); g.rotate(-.08 - .1 * (1 - k)); g.scale(1 + 1.1 * (1 - k), 1 + 1.1 * (1 - k)); g.translate(-170, -48);
    sticker(0, 0, 340, 96, 48, C.lime, { off: 8, ol: 5 }, () => { tx('STILL TEEN?', 170, 66, 40, 900, 'InterTight', C.ink, 'center', 'stillteen'); }); g.restore(); ring(820, 800, t, BD + .85, .6, C.lime, 240); }
}
// ===== C: the real news =====
const NEWS_IN = t0s(3) + .1;
function sceneC(t) {
  head(t, [[K('SOME', wt('l3', 0)), K('ADULTS', wt('l3', 1))], [K('GOT', wt('l3', 2)), K('STUCK', wt('l3', 3), 'lime'), K('IN', wt('l3', 4))], [K('TEEN', wt('l3', 5), 'ink'), K('MODE.', wt('l3', 6))]], 376, 94, 90, { center: true, maxW: 860 });
  // TechCrunch card slides in from the right at "News"
  const ta = enterE(sg(t, wt('l3', 7) - .15, wt('l3', 7) + .45)), tw = 860, th = tw * TC.height / TC.width;
  if (ta > .003) { g.save(); g.globalAlpha *= sm(ta * 3); g.translate(110 + 430 + (1 - ta) * 700, 770 + th / 2 + fl(t, 1, 5, 4.2)); g.rotate(-.02 * ta); g.translate(-430, -th / 2);
    g.fillStyle = C.ink; rr(10, 10, tw, th, 18); g.fill(); g.fillStyle = '#fff'; rr(0, 0, tw, th, 18); g.fill(); g.save(); rr(0, 0, tw, th, 18); g.clip(); g.drawImage(TC, 0, 0, tw, th); g.restore(); g.lineWidth = 5; g.strokeStyle = C.ink; rr(0, 0, tw, th, 18); g.stroke(); g.restore(); }
  // TechRadar headline card slams in
  const ru = t - NEWS_IN, rw = 918, rh = rw * TR.height / TR.width;
  if (ru > 0) { const rk = expoE(ru / .3), rs = 1 + .75 * (1 - rk); g.save(); g.globalAlpha *= sm(ru / .06); g.translate(540, 590 + rh / 2 + fl(t, 3, 4, 4.8)); g.rotate(.03 * (1 - rk) - .004 * Math.sin(t * .8)); const hz = 1 + .02 * sg(t, NEWS_IN + .4, NEWS_IN + 3.6); g.scale(rs * hz, rs * hz); g.translate(-rw / 2, -rh / 2);
    g.fillStyle = C.ink; rr(11, 11, rw, rh, 20); g.fill(); g.fillStyle = '#fff'; rr(0, 0, rw, rh, 20); g.fill();
    g.save(); rr(0, 0, rw, rh, 20); g.clip(); g.drawImage(TR, 0, 0, rw, rh); const k = rw / TR.width;
    const m = enterE(sg(t, wt('l3', 3) - .1, wt('l3', 3) + .45)); if (m > .01) { g.globalCompositeOperation = 'multiply'; g.fillStyle = C.lime; rr(32 * k, 160 * k, 530 * k * m, 70 * k, 12); g.fill(); g.globalCompositeOperation = 'source-over'; }
    g.restore(); g.lineWidth = 5; g.strokeStyle = C.ink; rr(0, 0, rw, rh, 20); g.stroke(); g.restore(); ring(540, 590 + rh / 2, t, NEWS_IN, .55, C.lime, 340); }
  // tags + stamp + bullet strip
  const ga = sm(sg(t, NEWS_IN + .5, NEWS_IN + .8)); if (ga > .003) { g.save(); g.globalAlpha *= ga; g.translate(0, fl(t, 5, 3, 3.6)); const w1 = tag(81, 1000, 'real page · TechRadar', { px: 24, fill: C.lime, rot: -.006 }); tag(81 + w1 + 14, 1000, 'real page · TechCrunch', { px: 24, fill: C.white, rot: .006 }); g.restore(); }
  const su = t - (NEWS_IN + .5); if (su > 0) { const k = expoE(su / .2); stamp('REAL NEWS', 905, 1024 + fl(t, 2, 3, 3.1), 26, -.05, 1 + 1.0 * (1 - k), sm(su / .05), C.limeDeep, 'stampnews'); }
  const bu = enterE(sg(t, NEWS_IN + .7, NEWS_IN + 1.15)); if (bu > .01) { g.save(); g.globalAlpha *= sm(bu * 1.8); g.translate((1 - bu) * 90, fl(t, 7, 3, 3.9));
    sticker(100, 1062, 880, 118, 26, C.lime, { off: 8, ol: 5 }, () => { g.globalCompositeOperation = 'multiply'; g.drawImage(TB, 24, 22, 832, 832 * TB.height / TB.width); g.globalCompositeOperation = 'source-over'; }); g.restore(); }
  head(t, [[K('NEWS', wt('l3', 7)), K('SITES', wt('l3', 8)), K('REPORTED', wt('l3', 9)), K('IT.', wt('l3', 10), 'lime')]], 1234, 54, 60, { center: true, maxW: 860 });
}
// ===== D: what it guesses from (lime stage) =====
function sceneD(t) {
  head(t, [[K('IT', wt('l4', 0)), K('GUESSES', wt('l4', 1), 'ink'), K('FROM', wt('l4', 2))], [K('WHAT', wt('l4', 3)), K('YOU', wt('l4', 4)), K('ASK,', wt('l4', 5), 'ink')], [K('AND', wt('l4', 6)), K('WHEN.', wt('l4', 7), 'ink')]], 372, 92, 92, { center: true, maxW: 860 });
  const items = [['what you talk about', 'chat', Math.min(wt('l4', 3) - .05, T.l4 + .5), C.white, C.ink], ['times of day you use it', 'clock', wt('l4', 7) - .1, C.ink, C.lime], ['how long your account has existed', 'cal', wt('l4', 7) + .45, C.white, C.ink]];
  items.forEach(([s, ic, t0, fill, col], i) => { const y = 640 + i * 190; if (!popIn(t, t0, 540, y + 75, .4, (i % 2 ? .06 : -.06))) return; g.translate(0, fl(t, i * 2, 5, 3.7 + i * .4));
    sticker(100, y, 880, 150, 75, fill, { off: 10, ol: 6, rot: (i - 1) * .012 }, () => { icon(ic, 95, 75, 1.6, col); tx(s, 160, 94, 42, 800, 'InterTight', col, 'left', 'sig' + i); }); g.restore(); });
  const ca = sm(sg(t, wt('l4', 7) + .5, wt('l4', 7) + .8)); if (ca > .003) { g.save(); g.globalAlpha *= ca; tag(100, 1178, 'signals listed by OpenAI Help Center', { px: 24, fill: C.white }); g.restore(); }
}
// ===== E: Settings, Account, Age (dark stage) =====
const l5s = [wt('l5', 4), wt('l5', 5), wt('l5', 6)];
function sceneE(t) {
  head(t, [[K('SEE', wt('l5', 0)), K('WHAT', wt('l5', 1))], [K('IT', wt('l5', 2)), K('SAYS:', wt('l5', 3), 'lime')]], 392, 100, 100, { center: true, maxW: 860 });
  const steps = [['Settings', 1, l5s[0]], ['Account', 2, l5s[1]], ['Age', 3, l5s[2]]];
  g.font = F(34, 800, 'InterTight'); const ws = steps.map(s => g.measureText(s[0]).width + 104); let x = 540 - (ws[0] + ws[1] + ws[2] + 40) / 2;
  steps.forEach(([s, n, ts], i) => { const u = t - (ts - .1), act = t >= ts - .1 && (i === 2 || t < steps[i + 1][2] - .1); const sc = 1 + (act ? .1 * Math.sin(Math.PI * clamp(u / .5)) + .04 : 0), y = 522;
    g.save(); g.translate(x + ws[i] / 2, y + 43); g.scale(sc, sc); g.translate(-ws[i] / 2, -43); sticker(0, 0, ws[i], 86, 43, act ? C.lime : C.white, { off: 7 }); badge(n, 44, 43, 28, 1, act ? C.white : C.lime); tx(s, 86, 56, 34, 800, 'InterTight', C.ink, 'left', 'step' + n); g.restore();
    if (i < 2) { g.save(); g.strokeStyle = '#fff'; g.lineWidth = 6; g.lineCap = 'round'; g.lineJoin = 'round'; const ax = x + ws[i] + 4, ay = y + 43; g.beginPath(); g.moveTo(ax, ay); g.lineTo(ax + 20, ay); g.moveTo(ax + 12, ay - 9); g.lineTo(ax + 21, ay); g.lineTo(ax + 12, ay + 9); g.stroke(); g.restore(); }
    x += ws[i] + 20; });
  if (pushIn(t, T.l5 + .15, 540, 940, .22, .3)) {
    const bump = 1 + .02 * pulse(t, [l5s[2]], .3); g.translate(540, 940); g.scale(bump, bump); g.translate(-540, -940); g.translate(0, fl(t, 1, 4, 4.6));
    lcard(100, 650, 880, 545, 40); tag(946, 668, EXAMPLE, { al: 'right', fill: C.wash });
    g.save(); rr(100, 650, 880, 545, 40); g.clip(); const sw = ioE(sg(t, l5s[1] + .08, l5s[1] + .5));
    const row = (s, y, hi, ic) => { g.fillStyle = hi ? C.lime : '#343744'; rr(130, y, 820, 84, 24); g.fill(); icon(ic, 180, y + 42, .85, hi ? C.ink : '#DDE0D2'); tx(s, 232, y + 56, 38, 700, 'Inter', hi ? C.ink : '#fff', 'left', 'r:' + s); g.strokeStyle = hi ? C.ink : C.mute; g.lineWidth = 5; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); g.moveTo(912, y + 27); g.lineTo(926, y + 42); g.lineTo(912, y + 57); g.stroke(); };
    g.save(); const k0 = REC; if (sw > .01) REC = false; g.translate(-sw * 880, 0); tx('Settings', 134, 726, 40, 800, 'InterTight', '#fff', 'left', 'p0'); icon('gear', 340, 714, .9, C.lime);
    [['General', 'gear'], ['Notifications', 'chat'], ['Personalization', 'user'], ['Account', 'id']].forEach(([s, ic], i) => row(s, 765 + i * 108, s === 'Account' && t > l5s[1] - .12, ic)); g.restore(); REC = k0;
    g.save(); const k1 = REC; if (sw < .99) REC = false; g.translate((1 - sw) * 880, 0); tx('Account', 134, 726, 40, 800, 'InterTight', '#fff', 'left', 'p1'); icon('id', 360, 714, .9, C.lime);
    [['Profile', 'user'], ['Age', 'clock'], ['Plan', 'cal']].forEach(([s, ic], i) => row(s, 765 + i * 108, s === 'Age' && t > l5s[2] - .1, ic)); g.restore(); REC = k1; g.restore();
    const rp = enterE(sg(t, l5s[2], l5s[2] + .4)); if (rp > .01) { g.strokeStyle = '#fff'; g.lineWidth = 7; g.lineCap = 'round'; const w = 832, h = 92, per = 2 * (w + h); g.setLineDash([per * rp, per]); rr(126, 869, w, h, 28); g.stroke(); g.setLineDash([]); }
    g.restore();
    // cursor flies: top right -> Account -> Age
    const a1 = sm(sg(t, T.l5 + .35, l5s[1] - .03)), a2 = sm(sg(t, l5s[1] + .2, l5s[2] - .03));
    let cx = lerp(980, 600, a1), cy = lerp(600, 1141, a1) - Math.sin(a1 * Math.PI) * 60; cx = lerp(cx, 650, a2); cy = lerp(cy, 925, a2) - Math.sin(a2 * Math.PI) * 50;
    const ca = sm(sg(t, T.l5 + .3, T.l5 + .5)) * (1 - sm(sg(t, l5s[2] + .55, l5s[2] + .75)));
    if (ca > .003) { g.save(); g.globalAlpha *= ca; ripple(600, 1141, t, l5s[1], C.lime); ripple(650, 925, t, l5s[2], C.lime); g.save(); g.shadowColor = '#000'; g.shadowBlur = 10; cursor(cx, cy, 1.3, Math.max(0, 1 - Math.abs(t - l5s[1]) / .12, 1 - Math.abs(t - l5s[2]) / .12)); g.restore(); g.restore(); }
    g.restore();
  }
}
// ===== F: verify (selfie / ID flip) =====
function sceneF(t) {
  head(t, [[K('IF', wt('l6', 0)), K("IT'S", wt('l6', 1)), K('WRONG,', wt('l6', 2), 'ink')], [K('OPENAI', wt('l6', 3)), K('SAYS', wt('l6', 4)), K('A', wt('l6', 5)), K('SELFIE', wt('l6', 6), 'lime')], [K('OR', wt('l6', 7)), K('AN', wt('l6', 8)), K('ID', wt('l6', 9), 'lime'), K('CAN', wt('l6', 10)), K('FIX', wt('l6', 11)), K('IT.', wt('l6', 12))]], 374, 86, 90, { center: true, maxW: 870 });
  if (!pushIn(t, T.l6 + .1, 540, 900, .22, .3)) return;
  g.translate(0, fl(t, 2, 4, 4.4)); dcard(100, 600, 880, 600, 40); tx('Verify your age', 134, 664, 40, 800, 'InterTight', '#fff', 'left', 'vh');
  const fx = wt('l6', 11) - .05, fp = sg(t, fx, fx + .4), lab = fp > .5 ? 'ADULT' : 'TEEN';
  g.save(); g.translate(830, 650); g.scale(Math.max(.03, Math.abs(Math.cos(fp * Math.PI))), 1 + .08 * Math.sin(fp * Math.PI)); sticker(-105, -40, 210, 80, 40, fp > .5 ? C.lime : C.ink, { off: 6, ol: 4 }, () => { tx(lab, 105, 56, 40, 900, 'InterTight', fp > .5 ? C.ink : C.lime, 'center', 'vbadge'); }); g.restore();
  sticker(134, 690, 360, 54, 27, C.wash, { off: 5, ol: 3 }, () => { tx('via a third party', 22, 37, 26, 800, 'InterTight', C.ink, 'left', 'third'); });
  [['Selfie', 'cam', wt('l6', 6)], ['ID', 'id', wt('l6', 9)]].forEach(([s, ic, ts], i) => { const a = popIn(t, T.l6 + .35 + i * .15, 335 + i * 410, 920, .38); if (!a) return;
    const p = sg(t, ts - .02, ts + .4), sx = Math.max(.04, Math.abs(Math.cos(p * Math.PI))), on = p > .5, x0 = 130 + i * 420;
    g.translate(0, fl(t, i * 3, 4, 3.5 + i * .5)); g.save(); g.translate(x0 + 195, 920); g.scale(sx, 1 + .06 * Math.sin(p * Math.PI)); g.translate(-195, -150);
    sticker(0, 0, 390, 300, 44, on ? C.lime : C.white, { off: 10, ol: 6 }, () => { icon(ic, 195, 120, 2.6); tx(s, 195, 250, 56, 900, 'InterTight', C.ink, 'center', 'opt' + i); if (on) check(340, 56, 30, 1); }); g.restore(); g.restore(); });
  tag(134, 1125, EXAMPLE, { px: 24, fill: C.wash });
  const ts1 = wt('l6', 6), ts2 = wt('l6', 9), c1 = sm(sg(t, ts1 - .6, ts1 - .03)), c2 = sm(sg(t, ts1 + .35, ts2 - .03));
  let cx = lerp(960, 380, c1), cy = lerp(700, 980, c1) - Math.sin(c1 * 3.14) * 50; cx = lerp(cx, 800, c2); cy = lerp(cy, 990, c2) - Math.sin(c2 * 3.14) * 40;
  const ca = sm(sg(t, ts1 - .65, ts1 - .4)) * (1 - sm(sg(t, wt('l6', 11) + .2, wt('l6', 11) + .4)));
  if (ca > .003) { g.save(); g.globalAlpha *= ca; ripple(380, 980, t, ts1, C.lime); ripple(800, 990, t, ts2, C.lime); cursor(cx, cy, 1.3, Math.max(0, 1 - Math.abs(t - ts1) / .12, 1 - Math.abs(t - ts2) / .12)); g.restore(); }
  g.restore();
}
// ===== G: the question (dark stage) =====
const TB0 = wt('l7', 8) - .05;
function sceneG(t) {
  head(t, [[K('DID', wt('l7', 0)), K('CHATGPT', wt('l7', 1), 'ink')], [K('EVER', wt('l7', 2)), K('ACT', wt('l7', 3)), K('LIKE', wt('l7', 4))], [K("YOU'RE", wt('l7', 5)), K('A', wt('l7', 6)), K('KID?', wt('l7', 7), 'lime')]], 372, 104, 106, { center: true, maxW: 860 });
  if (!pushIn(t, T.l7 + .2, 540, 940, .22, .3)) return;
  g.translate(0, fl(t, 2, 4, 4.4)); sticker(100, 690, 880, 535, 40, C.white, { off: 12, ol: 6 }); tx('Comments', 134, 756, 38, 800, 'InterTight', C.ink, 'left', 'ch'); tag(946, 706, EXAMPLE, { al: 'right', fill: C.wash });
  g.fillStyle = '#ECECE4'; rr(130, 786, 820, 92, 46); g.fill(); g.fillStyle = C.lime; g.beginPath(); g.arc(176, 832, 28, 0, 7); g.fill(); g.lineWidth = 3; g.strokeStyle = C.ink; g.stroke(); icon('user', 176, 832, .64, C.ink);
  const foc = sm(sg(t, TB0 - .3, TB0 + .2)); g.strokeStyle = C.ink; g.lineWidth = 3 + 3 * foc; rr(130, 786, 820, 92, 46); g.stroke();
  tx('Add a comment…', 226, 844, 34, 500, 'Inter', C.mute, 'left', 'ph'); if (foc > .1 && Math.sin(t * 6.283) > -.3) { g.fillStyle = C.ink; g.fillRect(214, 806, 4, 52); }
  const btn = (s, x, y, w, fill, rot, t0, hit) => { if (!popIn(t, t0, x + w / 2, y + 55, .38, rot)) return; const pk = hit ? Math.sin(Math.PI * clamp((t - hit) / .4)) : 0; g.translate(0, fl(t, x, 3, 3.8));
    sticker(x, y, w, 110, 55, fill, { off: 9, ol: 6, s: 1 + .08 * pk }, () => { tx(s, w / 2, 74, 46, 900, 'InterTight', C.ink, 'center', 'btn:' + s); }); g.restore(); };
  const yk = wt('l7', 7);
  btn('Yes', 130, 915, 390, C.lime, -.04, T.l7 + .45, yk + .5); btn('No', 560, 915, 390, C.white, .04, T.l7 + .7); btn('Tell me below ↓', 130, 1060, 820, C.lime, -.02, T.l7 + .95, TB0 + .35);
  const ca = sm(sg(t, yk - .5, yk - .3)) * (1 - sm(sg(t, TB0 + .6, TB0 + .8)));
  if (t < yk - .5) { /* idle until the question is asked */ }
  if (ca > .003) { const u1 = sm(sg(t, yk - .5, yk + .5)), u2 = sm(sg(t, yk + .7, TB0 + .3)); let cx = lerp(960, 330, u1), cy = lerp(700, 975, u1) - Math.sin(u1 * 3.14) * 40; cx = lerp(cx, 540, u2); cy = lerp(cy, 1125, u2);
    g.save(); g.globalAlpha *= ca; ripple(330, 975, t, yk + .5); ripple(540, 1125, t, TB0 + .35); cursor(cx, cy, 1.3, Math.max(0, 1 - Math.abs(t - yk - .5) / .12, 1 - Math.abs(t - TB0 - .35) / .12)); g.restore(); }
  g.restore();
}
// ===== H: link in bio (lime stage) =====
function sceneH(t) {
  const lk = wt('l8', 4) - .1;
  const ps = 1 + .03 * Math.sin(t * 3.7);
  if (popIn(t, T.l8 + .05, 540, 420, .45, -.05)) { g.translate(0, fl(t, 1, 5, 4)); g.translate(540, 420); g.scale(ps, ps); g.translate(-540, -420);
    sticker(100, 300, 880, 240, 120, C.ink, { off: 14, ol: 6 }, () => { g.strokeStyle = C.lime; g.lineWidth = 13; g.lineCap = 'round'; rr(104, 94, 96, 52, 26); g.stroke(); rr(160, 118, 96, 52, 26); g.stroke(); tx('Link in bio', 290, 156, 88, 900, 'InterTight', C.lime, 'left', 'linkbio'); }); g.restore(); }
  const steps = [['Settings', 1], ['Account', 2], ['Age', 3]];
  steps.forEach(([s, n], i) => { const t0 = wt('l8', 1) + i * .28; if (!popIn(t, t0, 540, 700 + i * 190 + 75, .4, (i % 2 ? .05 : -.05))) return; g.translate(0, fl(t, i * 2.2, 4, 3.6 + i * .5));
    sticker(100, 660 + i * 190, 880, 150, 75, i === 2 ? C.ink : C.white, { off: 10, ol: 6 }, () => { tx(s, 190, 100, 62, 900, 'InterTight', i === 2 ? C.lime : C.ink, 'left', 'chip' + i); }); badge(n, 170, 735 + i * 190, 44, 1, i === 2 ? C.lime : C.lime); g.restore(); });
  const ca = sm(sg(t, lk - .5, lk - .25)) * (1 - sm(sg(t, lk + .6, lk + .8)));
  if (ca > .003) { const u = sm(sg(t, lk - .5, lk + .05)); const x = lerp(980, 820, u), y = lerp(720, 470, u); g.save(); g.globalAlpha *= ca; ripple(830, 480, t, lk + .05, C.ink); cursor(x, y, 1.3, Math.max(0, 1 - Math.abs(t - lk - .05) / .12)); g.restore(); }
}
// ===== I: the close =====
const TAP = wt('l9', 10) + .22;
function sceneI(t) {
  head(t, [[K('I', wt('l9', 0)), K('READ', wt('l9', 1)), K('THE', wt('l9', 2))], [K('FINE', wt('l9', 3), 'ink'), K('PRINT', wt('l9', 4), 'ink')], [K('AI', wt('l9', 5)), K('APPS', wt('l9', 6)), K('HOPE', wt('l9', 7))], [K('YOU', wt('l9', 8)), K('SKIP.', wt('l9', 9), 'lime')]], 374, 88, 86, { center: true, maxW: 860 });
  const cards = [['Memory', wt('l9', 3)], ['Age', wt('l9', 5)], ['Ads', wt('l9', 6)]];
  cards.forEach(([s, t0], i) => { const y = 662 + i * 98; if (!popIn(t, t0, 540, y + 44, .38, (i - 1) * .05)) return; g.translate(0, fl(t, i * 2.1, 4, 3.4 + i * .5));
    sticker(110, y, 860, 88, 44, i === 1 ? C.lime : C.white, { off: 8, ol: 5 }, () => { tx(s, 44, 60, 44, 900, 'InterTight', C.ink, 'left', 'ai' + i); }); const tg = sm(sg(t, wt('l9', 7) + i * .22, wt('l9', 7) + .4 + i * .22)); toggle(760, y + 14, true, tg); g.restore(); });
  const ta = sm(sg(t, wt('l9', 6) + .2, wt('l9', 6) + .5)); if (ta > .003) { g.save(); g.globalAlpha *= ta; tag(110, 954, EXAMPLE, { px: 24, fill: C.wash }); g.restore(); }
  // Follow button: pops with the word, one tap, burst
  const fo = T.l9 + .12;
  if (popIn(t, fo, 540, 1105, .4, .04)) { const done = sm(sg(t, TAP, TAP + .25)), s = 1 + .025 * Math.sin(t * 3.1) + .1 * Math.sin(Math.PI * clamp((t - TAP) / .5)) * (t > TAP ? 1 : 0); g.translate(0, fl(t, 6, 4, 3.9));
    sticker(190, 1032, 700, 150, 75, done > .5 ? C.white : C.lime, { off: 12, ol: 6, s, rot: .01 }, () => { if (done > .5) { check(110, 75, 40, 1); tx('Following', 410, 98, 66, 900, 'InterTight', C.ink, 'center', 'follow'); } else tx('Follow', 350, 100, 72, 900, 'InterTight', C.ink, 'center', 'follow'); });
    g.restore(); }
  if (t > TAP) for (let wv = 0; wv < 3; wv++) { const R = rng(5 + wv * 9), T1 = TAP + wv * .45; if (t < T1) continue; for (let i = 0; i < 16; i++) { const ang = R() * 6.283, sp = 150 + R() * 260, u = t - T1 - R() * .08, e = 1 - Math.exp(-Math.max(0, u) * 2.4); if (u < 0) continue;
    g.save(); g.globalAlpha *= clamp(1 - u / 1.3) * .95; g.fillStyle = i % 3 ? C.lime : C.ink; g.strokeStyle = C.ink; g.lineWidth = 3; g.beginPath(); g.arc(540 + Math.cos(ang) * sp * e, 1107 + Math.sin(ang) * sp * e * .8 + 70 * u * u, i % 3 ? 11 : 6, 0, 7); g.fill(); if (i % 3) g.stroke(); g.restore(); } }
  const cu = sm(sg(t, TAP - .8, TAP - .02)); if (cu > .01 && t < TAP + .45) { const x = lerp(990, 600, cu), y = lerp(760, 1120, cu) - Math.sin(cu * 3.14) * 70; g.save(); g.globalAlpha *= 1 - sm(sg(t, TAP + .2, TAP + .45)); cursor(x, y, 1.3, Math.max(0, 1 - Math.abs(t - TAP) / .12)); g.restore(); }
  ripple(600, 1125, t, TAP, C.ink); ripple(600, 1125, t, TAP + .45, C.ink);
  head(t, [[K('AND', wt('l9', 11)), K('YOU', wt('l9', 12)), K("WON'T", wt('l9', 13)), K('HAVE', wt('l9', 14)), K('TO.', wt('l9', 15), 'lime')]], 1234, 54, 60, { center: true, maxW: 860 });
}
// ===== scene list + transition engine =====
const SC = [
  { n: 1, t0: 0, tone: 'paper', draw: sceneA },
  { n: 2, t0: t0s(2), tone: 'dark', draw: sceneB, from: [100, 1040, 880, 200, 36] },
  { n: 3, t0: t0s(3), tone: 'paper', draw: sceneC, from: [95, 870, 890, 370, 34] },
  { n: 4, t0: t0s(4), tone: 'lime', draw: sceneD, from: [81, 590, 918, 287, 20] },
  { n: 5, t0: t0s(5), tone: 'dark', draw: sceneE, from: [100, 1030, 880, 150, 75] },
  { n: 6, t0: t0s(6), tone: 'paper', draw: sceneF, from: [100, 650, 880, 585, 40] },
  { n: 7, t0: t0s(7), tone: 'dark', draw: sceneG, from: [100, 600, 880, 600, 40] },
  { n: 8, t0: t0s(8), tone: 'lime', draw: sceneH, from: [100, 690, 880, 535, 40] },
  { n: 9, t0: t0s(9), tone: 'paper', draw: sceneI, from: [100, 300, 880, 240, 120] },
];
function drawScene(s, t) { setTone(s.tone); bg(s.tone, t); s.draw(t); }
function draw(t) {
  g.setTransform(1, 0, 0, 1, 0, 0); TXT.length = 0;
  const [z, px, py, rot] = cam(t);
  g.save(); g.translate(540 + px, 960 + py); g.rotate(rot); g.scale(z, z); g.translate(-540, -960);
  let i = 0; for (let k = 0; k < SC.length; k++) if (t >= SC[k].t0) i = k;
  const s = SC[i], u = i > 0 ? (t - s.t0) / TRD : 2;
  if (u >= 1) drawScene(s, t);
  else {
    const p = SC[i - 1], e = ioE(u), F0 = s.from, fx = F0[0] + F0[2] / 2, fy = F0[1] + F0[3] / 2;
    g.save(); g.translate(fx, fy); g.scale(1 + .1 * e, 1 + .1 * e); g.translate(-fx, -fy); drawScene(p, t); g.restore();
    const rx = lerp(F0[0], -80, e), ry = lerp(F0[1], -80, e), rw = lerp(F0[2], W + 160, e), rh = lerp(F0[3], H + 160, e), rrad = lerp(F0[4], 0, e);
    g.save(); rr(rx, ry, rw, rh, rrad); g.clip(); g.translate(fx, fy); g.scale(1.08 - .08 * e, 1.08 - .08 * e); g.translate(-fx, -fy); drawScene(s, t); g.restore();
    g.save(); g.lineWidth = 8 * (1 - e) + 1; g.strokeStyle = C.ink; rr(rx, ry, rw, rh, rrad); g.stroke(); g.restore();
  }
  g.restore();
}
window.TRANS = SC.slice(1).map(s => [s.t0 - .02, s.t0 + TRD + .02]);
window.render = (t) => { REC = false; draw(t); };
window.TEXTS = (t) => { REC = true; draw(t); REC = false; return TXT.map(o => ({ ...o })); };
// ---- shakes (impacts) and sound events, all from cue times ----
addShake(HT, 20); addShake(tw1(7), 9); addShake(BD + .85, 14); addShake(NEWS_IN + .15, 20); addShake(Math.min(wt('l4', 3) - .05, T.l4 + .5), 6); addShake(wt('l4', 7) - .1, 7); addShake(wt('l4', 7) + .45, 6);
addShake(l5s[1], 5); addShake(l5s[2], 9); addShake(wt('l6', 6), 8); addShake(wt('l6', 9), 8); addShake(wt('l6', 11), 12); addShake(wt('l7', 7), 6); addShake(TB0, 8); addShake(T.l8 + .05, 10); addShake(TAP, 11);
for (let n = 2; n <= 9; n++) addShake(t0s(n) + TRD * .6, 6);
window.EV = [{ t: .25, type: 'tick' }, { t: HT, type: 'crash' }, { t: HT + .05, type: 'thud' }, { t: tw1(7), type: 'thud' }, { t: BD + .85, type: 'thud' }, { t: NEWS_IN + .12, type: 'thud' }, { t: NEWS_IN + .5, type: 'thud' },
  { t: Math.min(wt('l4', 3) - .05, T.l4 + .5), type: 'click' }, { t: wt('l4', 7) - .1, type: 'click' }, { t: wt('l4', 7) + .45, type: 'click' }, { t: l5s[1], type: 'click' }, { t: l5s[2], type: 'click' }, { t: l5s[2] + .2, type: 'ding' },
  { t: wt('l6', 6), type: 'click' }, { t: wt('l6', 9), type: 'click' }, { t: wt('l6', 11), type: 'ding' }, { t: wt('l7', 7), type: 'click' }, { t: TB0 + .35, type: 'click' }, { t: T.l8 + .05, type: 'thud' }, { t: wt('l8', 1), type: 'click' }, { t: wt('l8', 1) + .28, type: 'click' }, { t: wt('l8', 1) + .56, type: 'click' }, { t: wt('l9', 3), type: 'click' }, { t: wt('l9', 5), type: 'click' }, { t: wt('l9', 6), type: 'click' }, { t: TAP, type: 'ding' }]
  .concat(Array.from({ length: 8 }, (_, k) => ({ t: t0s(k + 2) - .02, type: 'whoosh' })));
window.READY = true;
