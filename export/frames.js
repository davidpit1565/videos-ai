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

// A long-lived single page stepping through hundreds of sequential seek+screenshot
// calls can hit a renderer crash or deadlock partway through (observed: episode 54's
// second build hung indefinitely at the same frame across three separate attempts,
// with no error surfaced — page.evaluate/page.screenshot have no timeout of their own,
// so a wedged renderer just blocks the loop forever). Single-frame probes of the exact
// same timestamps, each on a fresh page, never reproduced it — pointing at accumulated
// per-page state over hundreds of frames, not the content at that timestamp. Rather
// than guess at the root cause further, this makes the loop itself resilient: a frame
// that doesn't land within FRAME_TIMEOUT_MS gets one retry on a freshly relaunched page,
// re-seeked to the same timestamp, so a single wedged renderer costs one relaunch
// instead of the whole capture hanging forever.
const FRAME_TIMEOUT_MS = 20000;

async function withTimeout(promise, ms, label) {
  let timer;
  const timeout = new Promise((_, reject) => {
    timer = setTimeout(() => reject(new Error(`timed out after ${ms}ms: ${label}`)), ms);
  });
  try {
    return await Promise.race([promise, timeout]);
  } finally {
    clearTimeout(timer);
  }
}

(async () => {
  const [file, w, h, dur, out, fpsArg] = process.argv.slice(2);
  const W = +w, H = +h, D = +dur, FPS = +(fpsArg || 30);

  async function openPage(browser) {
    const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
    await page.goto('file://' + file + '?render=1');
    await page.waitForTimeout(2500);                 // let the fonts settle
    // render mode holds a black cover until playback starts, and playback never starts
    // here — so drop the cover and the tap-to-play scrim before capturing.
    await page.evaluate(() => {
      document.getElementById('preroll')?.remove();
      document.getElementById('tap')?.classList.add('hide');
    });
    return page;
  }

  let b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--force-device-scale-factor=1', '--hide-scrollbars'],
  });
  let p = await openPage(b);

  const total = Math.round(D * FPS);
  for (let i = 0; i < total; i++) {
    const t = i / FPS;
    const framePath = path.join(out, String(i).padStart(5, '0') + '.png');
    try {
      await withTimeout(p.evaluate((t) => window.__reel.seek(t), t), FRAME_TIMEOUT_MS, `seek frame ${i}`);
      await withTimeout(p.screenshot({ path: framePath }), FRAME_TIMEOUT_MS, `screenshot frame ${i}`);
    } catch (e) {
      console.log(`  frame ${i} wedged (${e.message}) — relaunching and retrying once`);
      try { await b.close(); } catch {}
      b = await chromium.launch({
        executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
        args: ['--no-sandbox', '--force-device-scale-factor=1', '--hide-scrollbars'],
      });
      p = await openPage(b);
      await p.evaluate((t) => window.__reel.seek(t), t);
      await p.screenshot({ path: framePath });
    }
    if (i % 150 === 0) console.log(`frame ${i}/${total}`);
  }
  console.log(`captured ${total} frames at ${FPS} fps`);
  await b.close();
})();
