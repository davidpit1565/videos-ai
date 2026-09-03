// Does any text in this build land where the platform's own UI will cover it?
//
// Meta publishes the numbers for 9:16 Reels: keep text and key elements out of the
// top 14%, the bottom 35%, and 6% of each side. On 1080x1920 that is 269px, 672px
// and 65px. TikTok does not publish pixels (its safe zone shifts with caption
// length), so --tiktok widens the right margin to 180px for the action column.
//
// This walks the real DOM at sample times instead of eyeballing a render, so a
// caption that sits under the username row is caught before a phone finds it.
//
//   node export/safe_check.js video/reel-01-paced.html [--tiktok] [--every 0.5]
function load() {
  for (const id of ['playwright-core', 'playwright',
                    '/opt/node22/lib/node_modules/playwright-core',
                    '/opt/node22/lib/node_modules/playwright']) {
    try { return require(id); } catch {}
  }
  throw new Error('playwright not found');
}
const { chromium } = load();
const path = require('path');

(async () => {
  const args = process.argv.slice(2);
  const file = path.resolve(args[0]);
  const tiktok = args.includes('--tiktok');
  const every = +(args[args.indexOf('--every') + 1]) || 0.5;
  // Meta's 14/35/6 are guidance with margin in them, and the mock UI panels are a few
  // pixels taller than the band they sit in. Chasing 3px with layout hacks risks the
  // design for nothing, so anything under the tolerance is reported and not failed.
  const tol = +(args[args.indexOf('--tol') + 1]) || 10;
  const W = 1080, H = 1920;
  const SAFE = { top: Math.round(H * 0.14), bottom: Math.round(H * 0.35),
                 left: Math.round(W * 0.06), right: tiktok ? 180 : Math.round(W * 0.06) };

  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--force-device-scale-factor=1', '--hide-scrollbars'],
  });
  const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await p.goto('file://' + file + '?render=1');
  await p.waitForTimeout(2500);
  await p.evaluate(() => {
    document.getElementById('preroll')?.remove();
    document.getElementById('tap')?.classList.add('hide');
  });
  const dur = await p.evaluate(() => window.__reel.duration);

  const worst = new Map(), clashes = new Map();
  for (let t = 0; t <= dur; t += every) {
    await p.evaluate((x) => window.__reel.seek(x), t);
    await p.waitForTimeout(340);   // longer than the build's 0.26-0.3s reveal transitions,
                                   // or half the elements are still mid-fade and invisible
    const hits = await p.evaluate((S) => {
      const out = [];
      const boxes = [];
      for (const el of document.querySelectorAll('*')) {
        // only elements that themselves render text, and are actually visible
        const own = [...el.childNodes].filter(n => n.nodeType === 3)
          .map(n => n.textContent.trim()).join(' ').trim();
        if (!own) continue;
        const cs = getComputedStyle(el);
        if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity < 0.05) continue;
        // A zoom-through scene transition (motion-recipes.md recipe 4) deliberately
        // scales content past the frame edges while blurring it out — that is the
        // "flies past the camera" effect, not readable text sitting in the UI band.
        // A blur past ~2px means the element is mid-transition, not resting content
        // a viewer needs to read, so the safe-area rule (which is about static,
        // legible text) does not apply to it at that instant.
        const blurMatch = /blur\(([\d.]+)px\)/.exec(cs.filter || '');
        if (blurMatch && +blurMatch[1] > 2) continue;
        let hiddenByAncestor = false;
        for (let a = el.parentElement; a; a = a.parentElement) {
          const p = getComputedStyle(a);
          if (p.visibility === 'hidden' || p.display === 'none' || +p.opacity < 0.05) { hiddenByAncestor = true; break; }
          const pBlur = /blur\(([\d.]+)px\)/.exec(p.filter || '');
          if (pBlur && +pBlur[1] > 2) { hiddenByAncestor = true; break; }
        }
        if (hiddenByAncestor) continue;
        const r = el.getBoundingClientRect();
        if (r.width < 2 || r.height < 2) continue;
        // an element marked data-decor is allowed in the platform's UI band: it is
        // there to be lost, and flagging it every run trains you to ignore the report
        if (el.closest('[data-decor]')) continue;
        boxes.push({ el, id: el.id || el.className || el.tagName, text: own.slice(0, 24),
                     t: r.top, b: r.bottom, l: r.left, r: r.right,
                     z: +getComputedStyle(el).zIndex || 0,
                     full: r.width > 1000 && r.height > 1700 });
        const over = {
          top: Math.max(0, S.top - r.top),
          bottom: Math.max(0, r.bottom - (1920 - S.bottom)),
          left: Math.max(0, S.left - r.left),
          right: Math.max(0, r.right - (1080 - S.right)),
        };
        const px = Math.max(over.top, over.bottom, over.left, over.right);
        if (px > 1) {
          out.push({ id: el.id || el.className || el.tagName, text: own.slice(0, 34),
                     px: Math.round(px), side: Object.entries(over)
                       .sort((a, b) => b[1] - a[1])[0][0],
                     rect: [Math.round(r.top), Math.round(r.bottom)] });
        }
      }
      // two text blocks on top of each other is its own defect: moving a caption
      // into the safe area is no good if it lands on the scene's own headline
      const clash = [];
      for (let i = 0; i < boxes.length; i++)
        for (let j = i + 1; j < boxes.length; j++) {
          const a = boxes[i], c = boxes[j];
          // nesting is not a collision, and a full-screen card is meant to cover
          if (a.el.contains(c.el) || c.el.contains(a.el)) continue;
          if (a.full || c.full) continue;
          const fa = a.el.closest('#flash'), fc = c.el.closest('#flash');
          if (!!fa !== !!fc) continue;
          const ov = Math.min(a.b, c.b) - Math.max(a.t, c.t);
          const oh = Math.min(a.r, c.r) - Math.max(a.l, c.l);
          if (ov > 4 && oh > 4)
            clash.push({ a: a.id, b: c.id, ta: a.text, tb: c.text,
                         px: Math.round(Math.min(ov, oh)) });
        }
      return { violations: out, clash };
    }, SAFE);
    for (const c of hits.clash) {
      const key = `CLASH ${c.a} x ${c.b}`;
      if (!clashes.has(key) || clashes.get(key).px < c.px)
        clashes.set(key, { ...c, at: +t.toFixed(2) });
    }
    for (const h of hits.violations) {
      const key = `${h.id}|${h.side}`;
      if (!worst.has(key) || worst.get(key).px < h.px) worst.set(key, { ...h, at: +t.toFixed(2) });
    }
  }
  await b.close();

  console.log(`${path.basename(file)}  ${dur}s  safe box: x ${SAFE.left}-${W - SAFE.right}, ` +
              `y ${SAFE.top}-${H - SAFE.bottom}${tiktok ? '  (tiktok right margin)' : ''}`);
  const all = [...worst.values()].sort((a, b) => b.px - a.px);
  const rows = all.filter(r => r.px >= tol);
  const minor = all.filter(r => r.px < tol);
  if (!rows.length) console.log(`  safe area: clean (tolerance ${tol}px)`);
  for (const r of rows) {
    console.log(`  ${String(r.px).padStart(4)}px past the ${r.side} line   ` +
                `y ${r.rect[0]}-${r.rect[1]}  at ${r.at}s   ${r.id}  "${r.text}"`);
  }
  for (const r of minor) {
    console.log(`  within tolerance: ${r.px}px past the ${r.side} line   ${r.id}  "${r.text}"`);
  }
  const clAll = [...clashes.values()].sort((a, b) => b.px - a.px);
  const cl = clAll.filter(c => c.px >= tol);
  if (!cl.length) console.log(`  overlaps: none over ${tol}px`);
  for (const c of clAll.filter(c => c.px < tol)) {
    console.log(`  within tolerance: ${c.px}px overlap  ${c.a} x ${c.b}`);
  }
  for (const c of cl) {
    console.log(`  overlap ${String(c.px).padStart(4)}px at ${c.at}s   ` +
                `${c.a} "${c.ta}"  x  ${c.b} "${c.tb}"`);
  }
  if (rows.length || cl.length) process.exitCode = 1;
})();
