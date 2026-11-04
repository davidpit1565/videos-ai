import { openDemo, closeServer } from '/root/lemo-opuscar/core/render/page.mjs';
const dir = process.argv[2];
const { browser, page } = await openDemo(dir, { w: 1080, h: 1920, q: '', warnings: false });
const r = await page.evaluate(() => { const D = window.DUR; for (let t = 0; t < D; t += 1 / 24) window.render(t); return { big: window.BIGT(), ev: window.EV, scenes: window.TRANS.map(x => x[0] + .02) }; });
const st = a => { const iv = a.slice(1).map((x, i) => x - a[i]); const m = iv.reduce((s, x) => s + x, 0) / iv.length, sd = Math.sqrt(iv.reduce((s, x) => s + (x - m) ** 2, 0) / iv.length); return { n: a.length, mean: +m.toFixed(2), std: +sd.toFixed(2), cv: +(sd / m).toFixed(2), min: +Math.min(...iv).toFixed(2), max: +Math.max(...iv).toFixed(2) }; };
// merge entrances closer than 80 ms into one event (a staggered group counts once)
const merged = []; r.big.forEach(t => { if (!merged.length || t - merged[merged.length - 1] > .08) merged.push(t); });
console.log('scene starts   ', JSON.stringify(st(r.scenes)));
console.log('all entrances  ', JSON.stringify(st(merged)));
const hero = r.ev.filter(e => ['thud', 'crash', 'ding'].includes(e.type)).map(e => e.t).sort((a, b) => a - b);
console.log('hero impacts   ', JSON.stringify(st(hero)), hero.map(x => x.toFixed(2)).join(' '));
console.log('entrance times ', merged.map(x => x.toFixed(2)).join(' '));
await browser.close(); closeServer();
