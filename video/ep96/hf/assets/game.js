// "Build me a game where a cat runs from a vacuum cleaner." One-sentence build, 13.11.2026.
// Deterministic: the whole state is a function of the steps taken, so it can be played live or re-simulated.
(function () {
  const W = 880, H = 760, GROUND = 600, INK = '#0f0f0f', PAPER = '#fbfbf8';
  function rng(seed) { let s = seed >>> 0; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; }
  function make(canvas) {
    const c = canvas.getContext('2d');
    let S;
    function reset() {
      S = { t: 0, y: 0, vy: 0, onGround: true, speed: 520, dist: 0, score: 0, lives: 3, hitT: -9, vac: 150, over: false,
            obs: [], next: 1.0, r: rng(7), puffs: [], best: 0 };
    }
    function spawn() {
      const k = Math.floor(S.r() * 3);            // 0 sock, 1 yarn, 2 slipper
      S.obs.push({ x: W + 60, k, w: [70, 74, 110][k], h: [60, 74, 46][k], passed: false });
      S.next = S.t + 0.95 + S.r() * 0.9;
    }
    function step(dt, jump) {
      if (S.over) return;
      S.t += dt; S.speed = 520 + Math.min(260, S.t * 14); S.dist += S.speed * dt;
      if (jump && S.onGround) { S.vy = 1040; S.onGround = false; }
      S.vy -= 2900 * dt; S.y += S.vy * dt;
      if (S.y <= 0) { S.y = 0; S.vy = 0; S.onGround = true; }
      if (S.t >= S.next) spawn();
      const catX = 470, catW = 120;
      for (const o of S.obs) {
        o.x -= S.speed * dt;
        if (!o.passed && o.x + o.w < catX) { o.passed = true; S.score += 1; }
        const hit = o.x < catX + catW - 26 && o.x + o.w > catX + 26 && S.y < o.h - 8;
        if (hit && S.t - S.hitT > 0.9) { S.hitT = S.t; S.lives -= 1; S.vac += 95; o.passed = true; if (S.lives <= 0) S.over = true; }
      }
      S.obs = S.obs.filter(o => o.x > -160);
      S.vac += (150 + (3 - S.lives) * 95 - S.vac) * Math.min(1, dt * 3);
      if (Math.floor(S.t * 14) !== Math.floor((S.t - dt) * 14)) S.puffs.push({ x: S.vac + 30, y: GROUND - 20 - S.r() * 60, a: 1 });
      for (const p of S.puffs) { p.x -= 60 * dt; p.y -= 40 * dt; p.a -= dt * 1.6; }
      S.puffs = S.puffs.filter(p => p.a > 0);
    }
    function botJump() {                           // a simple player for recordings
      for (const o of S.obs) { const d = o.x - (470 + 120); if (d > 0 && d < S.speed * 0.2 + 14) return true; }
      return false;
    }
    function line(w) { c.lineWidth = w; c.strokeStyle = INK; c.lineCap = 'round'; c.lineJoin = 'round'; }
    function drawCat(x, y, t) {
      const run = S.onGround ? Math.sin(t * 22) : 0.6, hurt = S.t - S.hitT < 0.5;
      c.save(); c.translate(x, y); if (hurt) c.rotate(-0.18);
      line(9); c.fillStyle = INK;
      c.beginPath(); c.ellipse(60, -62, 62, 36, 0, 0, 7); c.fill();                    // body
      c.beginPath(); c.arc(124, -96, 34, 0, 7); c.fill();                               // head
      c.beginPath(); c.moveTo(100, -118); c.lineTo(108, -150); c.lineTo(126, -124); c.fill();
      c.beginPath(); c.moveTo(128, -126); c.lineTo(146, -150); c.lineTo(152, -116); c.fill();
      c.beginPath(); c.moveTo(4, -70); c.quadraticCurveTo(-46, -100 - run * 14, -34, -150); c.stroke(); // tail
      for (const [lx, ph] of [[26, 0], [50, 3.14], [84, 3.14], [106, 0]]) {            // legs
        const a = S.onGround ? Math.sin(t * 22 + ph) * 26 : (lx < 60 ? -30 : 34);
        c.beginPath(); c.moveTo(lx, -36); c.lineTo(lx + a, -2); c.stroke();
      }
      c.fillStyle = PAPER; c.beginPath(); c.arc(134, -100, hurt ? 9 : 6, 0, 7); c.fill();  // eye
      c.restore();
    }
    function drawVac(x, t) {
      const wob = Math.sin(t * 30) * 3;
      c.save(); c.translate(x, GROUND + wob); line(9); c.fillStyle = INK;
      c.beginPath(); c.roundRect(-130, -120, 150, 96, 26); c.fill();                    // body
      c.fillStyle = PAPER; c.beginPath(); c.arc(-56, -74, 20, 0, 7); c.fill(); c.fillStyle = INK;
      c.beginPath(); c.arc(-56, -74, 9, 0, 7); c.fill();                                // angry eye
      c.beginPath(); c.moveTo(-84, -104); c.lineTo(-36, -92); c.stroke();
      c.beginPath(); c.arc(-100, -14, 16, 0, 7); c.fill(); c.beginPath(); c.arc(-20, -14, 16, 0, 7); c.fill();
      line(14); c.beginPath(); c.moveTo(14, -86); c.quadraticCurveTo(70, -130, 86, -40); c.stroke(); // hose
      c.beginPath(); c.roundRect(56, -40, 74, 30, 8); c.fill();                         // nozzle
      c.restore();
    }
    function drawObs(o) {
      c.save(); c.translate(o.x, GROUND); line(8); c.fillStyle = INK;
      if (o.k === 0) { c.beginPath(); c.roundRect(10, -60, 28, 44, 8); c.fill(); c.beginPath(); c.roundRect(10, -30, 60, 30, 14); c.fill(); }
      if (o.k === 1) { c.beginPath(); c.arc(37, -37, 37, 0, 7); c.fill(); c.strokeStyle = PAPER; c.lineWidth = 5;
        for (let i = -1; i <= 1; i++) { c.beginPath(); c.arc(37 + i * 16, -37, 30, -1.0, 1.0); c.stroke(); } }
      if (o.k === 2) { c.beginPath(); c.roundRect(0, -30, 110, 30, 14); c.fill(); c.beginPath(); c.roundRect(40, -46, 70, 30, 18); c.fill(); }
      c.restore();
    }
    function draw() {
      c.fillStyle = PAPER; c.fillRect(0, 0, W, H);
      c.fillStyle = '#d9d6cc';                                                           // floor pattern
      for (let i = 0; i < 12; i++) { const x = ((i * 120 - S.dist * 0.5) % 1440 + 1440) % 1440 - 200; c.fillRect(x, GROUND + 40, 70, 10); }
      line(8); c.beginPath(); c.moveTo(0, GROUND); c.lineTo(W, GROUND); c.stroke();
      for (const p of S.puffs) { c.globalAlpha = Math.max(0, p.a) * 0.5; c.fillStyle = INK; c.beginPath(); c.arc(p.x, p.y, 12, 0, 7); c.fill(); }
      c.globalAlpha = 1;
      for (const o of S.obs) drawObs(o);
      drawVac(S.vac, S.t); drawCat(470, GROUND - S.y, S.t);
      c.fillStyle = INK; c.font = '900 84px Helvetica, Arial, sans-serif'; c.textAlign = 'left'; c.fillText(String(S.score), 40, 104);
      for (let i = 0; i < 3; i++) { c.globalAlpha = i < S.lives ? 1 : 0.18; c.beginPath(); c.arc(W - 60 - i * 62, 72, 22, 0, 7); c.fill(); }
      c.globalAlpha = 1;
      if (S.over) { c.font = '900 96px Helvetica, Arial, sans-serif'; c.textAlign = 'center'; c.fillText('CAUGHT!', W / 2, 300);
        c.font = '700 40px Helvetica, Arial, sans-serif'; c.fillText('tap or press space', W / 2, 364); }
    }
    function simulateTo(time) { reset(); const dt = 1 / 60; for (let t = 0; t < time; t += dt) step(dt, botJump()); draw(); }
    reset();
    return { reset, step, draw, botJump, simulateTo, state: () => S };
  }
  window.CatGame = { make, W, H };
})();
