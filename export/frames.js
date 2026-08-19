// Deterministic capture: instead of recording a live playback and hoping the browser
// keeps up, step the timeline frame by frame and screenshot each one. The output is
// exactly fps * seconds frames, so audio placed at authored times can never drift.
// Slower than recording, so it is meant for reels rather than the long cut.
function load() {
  for (const id of ['playwright-core', 'playwright',
                    '/opt/node22/lib/node_modules/playwright-core',
                    '/opt/node22/lib/node_modules/playwright']) {
    try { return require(id); } catch {}
  }
  throw new Error('playwright not found: install it, or set NODE_PATH to its parent');
}
const { chromium } = load();
const path = require('path');

(async () => {
  const [file, w, h, dur, out, fpsArg] = process.argv.slice(2);
  const W = +w, H = +h, D = +dur, FPS = +(fpsArg || 30);
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--force-device-scale-factor=1', '--hide-scrollbars'],
  });
  const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await p.goto('file://' + file + '?render=1');
  await p.waitForTimeout(2500);                    // let the fonts settle
  // render mode holds a black cover until playback starts, and playback never starts
  // here — so drop the cover and the tap-to-play scrim before capturing.
  await p.evaluate(() => {
    document.getElementById('preroll')?.remove();
    document.getElementById('tap')?.classList.add('hide');
  });
  const total = Math.round(D * FPS);
  for (let i = 0; i < total; i++) {
    await p.evaluate((t) => window.__reel.seek(t), i / FPS);
    await p.screenshot({ path: path.join(out, String(i).padStart(5, '0') + '.png') });
    if (i % 150 === 0) console.log(`frame ${i}/${total}`);
  }
  console.log(`captured ${total} frames at ${FPS} fps`);
  await b.close();
})();
