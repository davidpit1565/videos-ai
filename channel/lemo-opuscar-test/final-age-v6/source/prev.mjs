import { openDemo, closeServer } from '/root/lemo-opuscar/core/render/page.mjs';
import fs from 'fs';
const dir = process.argv[2]; const ts = process.argv.slice(3).map(Number);
const { browser, page } = await openDemo(dir, { w: 1080, h: 1920, q: '', warnings: false });
fs.mkdirSync(dir + '/pv', { recursive: true });
for (const t of ts) { await page.evaluate(t => window.render(t), t); await new Promise(r => setTimeout(r, 120)); await page.screenshot({ path: `${dir}/pv/p_${t}.png` }); }
await browser.close(); closeServer();
