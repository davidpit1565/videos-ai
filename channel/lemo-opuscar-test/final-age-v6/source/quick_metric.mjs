// quick motion estimate without encoding: node quick_metric.mjs <dir> <t0> <t1>  -> per-0.5s mean abs diff on 108x192 gray (same metric as metric.py)
import { openDemo, closeServer } from '/root/lemo-opuscar/core/render/page.mjs';
import { spawnSync } from 'child_process';
const [dir, a, b] = [process.argv[2], +process.argv[3], +process.argv[4]];
const { browser, page } = await openDemo(dir, { w: 1080, h: 1920, q: '' });
const frames = [];
for (let f = Math.round(a * 24); f < Math.round(b * 24); f++) {
  await page.evaluate(t => window.render(t), f / 24); const buf = await page.screenshot({ type: 'jpeg', quality: 60, clip: { x: 0, y: 0, width: 1080, height: 1920 } });
  const r = spawnSync('/opt/ffmpeg7/bin/ffmpeg', ['-v', 'error', '-i', 'pipe:0', '-vf', 'scale=108:192,format=gray', '-f', 'rawvideo', '-'], { input: buf, maxBuffer: 1e8 }); frames.push(r.stdout);
}
const d = []; for (let i = 1; i < frames.length; i++) { let s = 0; const p = frames[i - 1], q = frames[i]; for (let k = 0; k < q.length; k++) s += Math.abs(p[k] - q[k]); d.push(s / q.length); }
const w = []; for (let i = 0; i + 12 <= d.length; i += 12) w.push(d.slice(i, i + 12).reduce((x, y) => x + y, 0) / 12);
console.log(w.map(x => x.toFixed(1)).join(' ')); await browser.close(); closeServer();
