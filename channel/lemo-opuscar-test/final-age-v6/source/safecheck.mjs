import { openDemo, closeServer } from '/root/lemo-opuscar/core/render/page.mjs';
const dir = process.argv[2];
const { browser, page } = await openDemo(dir, { w: 1080, h: 1920, q: '', warnings: false });
let bad = 0;
const DURS = await page.evaluate(() => window.DUR);
for (let t = 0; t <= DURS - .05; t += .125) {
  const TR = await page.evaluate(() => window.TRANS); if (TR.some(([a, b]) => t >= a && t <= b)) continue;   // text mid-transition is intentionally scaling/overlapping for 0.3 s
  const L = await page.evaluate(t => window.TEXTS(t), t);
  for (const o of L) { if (o.x0 < 62 || o.x1 > 1018 || o.y0 < 262 || o.y1 > 1252) { if (bad++ < 40) console.log('OUT', t.toFixed(2), o.id, [o.x0, o.y0, o.x1, o.y1].map(Math.round).join(',')); } }
  for (let i = 0; i < L.length; i++) for (let j = i + 1; j < L.length; j++) { const a = L[i], b = L[j];
    const ox = Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0), oy = Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0);
    if (ox > 6 && oy > 6) { if (bad++ < 40) console.log('OVERLAP', t.toFixed(2), a.id, '/', b.id, Math.round(ox) + 'x' + Math.round(oy)); } }
}
console.log('issues', bad); await browser.close(); closeServer();
