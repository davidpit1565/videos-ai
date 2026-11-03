// Frame-layout gate for HyperFrames (GSAP) compositions.
//
// export/safe_check.js drives the OLD hand-built reels (window.__reel.seek, 340 ms settle,
// a hard-coded Chromium path). HyperFrames reels are one composition html whose GSAP timeline
// is paused and exposed as window.__timelines.main (and window.__reel.seek). This is the same
// check for them: seek the timeline to each sample time, then flag every visible text box
// outside the usable box (Meta 9:16: top 14% = 269px, bottom 35% = 672px, sides 6% = 65px ->
// x 65-1015, y 269-1248) and every pair of text boxes that land on each other.
//
//   node export/safe_check_hf.js <composition.html> [--every 0.2] [--tol 10] [--tiktok]
//                                [--shots <dir>]   (saves a png of every frame that has a finding)
//
// Differences from safe_check.js, each one needed by how these compositions are built:
//  - Seeking a GSAP timeline is exact and instant (no CSS transitions), so the settle is 60 ms.
//  - Elements with data-start/data-duration (class "clip") are hidden outside their window by
//    the HyperFrames runtime; the runtime is not loaded here, so the window is applied by hand.
//  - Text sitting outside an ancestor with overflow:hidden (the phone screens parked at x:860
//    inside #phone) is not visible and is skipped; partly clipped text is measured as clipped.
//    The composition root / html / body are NOT treated as clips, or off-frame text would hide.
//  - CDN assets (gsap, Inter) are fetched with curl (which honours the container proxy) and
//    served to Chromium from a cache, so the layout is measured with the real font.
//  - Thresholds are the same as safe_check.js: tolerance 10 px, overlap > 4 px both ways.
//  - data-decor elements are skipped, exactly as in safe_check.js.
const fs = require('fs'), os = require('os'), path = require('path');
const { execFileSync } = require('child_process');

function loadPlaywright() {
  for (const id of ['playwright-core', 'playwright',
                    '/opt/node22/lib/node_modules/playwright-core',
                    '/opt/node22/lib/node_modules/playwright']) {
    try { return require(id); } catch {}
  }
  throw new Error('playwright not found (looked in node_modules and /opt/node22/lib/node_modules)');
}
function findChromium() {
  if (process.env.CHROMIUM_PATH) return process.env.CHROMIUM_PATH;
  const base = '/opt/pw-browsers';
  const hits = [];
  try {
    for (const d of fs.readdirSync(base)) {
      for (const sub of ['chrome-linux64/chrome', 'chrome-linux/chrome']) {
        const p = path.join(base, d, sub);
        if (fs.existsSync(p)) hits.push(p);
      }
    }
  } catch {}
  hits.sort().reverse();                       // newest build first
  if (!hits.length) throw new Error('no Chromium under ' + base + ' (set CHROMIUM_PATH)');
  return hits[0];
}
const CACHE = path.join(os.tmpdir(), 'hf-gate-cache');
function fetchCached(url) {
  fs.mkdirSync(CACHE, { recursive: true });
  const f = path.join(CACHE, url.replace(/[^A-Za-z0-9.]/g, '_'));
  if (!fs.existsSync(f) || fs.statSync(f).size === 0) {
    const caArgs = fs.existsSync('/root/.ccr/ca-bundle.crt') ? ['--cacert', '/root/.ccr/ca-bundle.crt'] : [];
    execFileSync('curl', ['-sSfL', '-m', '30', ...caArgs, '-o', f, url]);
  }
  return fs.readFileSync(f);
}

(async () => {
  const args = process.argv.slice(2);
  if (!args[0]) { console.error('usage: node export/safe_check_hf.js <composition.html> [--every 0.2] [--tol 10] [--tiktok] [--shots dir]'); process.exit(2); }
  const arg = (n, d) => (args.includes(n) ? args[args.indexOf(n) + 1] : d);
  const file = path.resolve(args[0]);
  const tiktok = args.includes('--tiktok');
  const every = +arg('--every', 0.2) || 0.2;
  const tol = +arg('--tol', 10);
  const shots = arg('--shots', null);
  if (shots) fs.mkdirSync(shots, { recursive: true });
  const W = 1080, H = 1920;
  const SAFE = { top: Math.round(H * 0.14), bottom: Math.round(H * 0.35),
                 left: Math.round(W * 0.06), right: tiktok ? 180 : Math.round(W * 0.06) };

  const { chromium } = loadPlaywright();
  const b = await chromium.launch({
    executablePath: findChromium(), headless: true,
    args: ['--no-sandbox', '--force-device-scale-factor=1', '--hide-scrollbars', '--disable-gpu'],
  });
  const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  const pageErrors = [];
  p.on('pageerror', e => pageErrors.push(e.message));
  await p.route(/^https?:\/\/(cdn\.jsdelivr\.net|unpkg\.com|cdnjs\.cloudflare\.com|fonts\.(googleapis|gstatic)\.com)\//, async route => {
    const url = route.request().url();
    try {
      const body = fetchCached(url);
      const type = url.endsWith('.js') ? 'application/javascript' : url.endsWith('.woff2') ? 'font/woff2'
                 : url.endsWith('.css') ? 'text/css' : 'application/octet-stream';
      await route.fulfill({ status: 200, body, contentType: type, headers: { 'access-control-allow-origin': '*' } });
    } catch (e) { console.error('  could not fetch ' + url + ': ' + e.message); await route.abort(); }
  });
  await p.goto('file://' + file);
  await p.waitForFunction(() => !!(window.__timelines && window.__timelines.main), null, { timeout: 15000, polling: 100 })
    .catch(() => { throw new Error('window.__timelines.main never appeared (is this a HyperFrames composition? page errors: ' + pageErrors.join('; ') + ')'); });
  await p.evaluate(() => document.fonts && document.fonts.ready);
  await p.waitForTimeout(500);
  // the video is the composition's declared length; the GSAP timeline can run a little past it
  const dur = await p.evaluate(() => {
    const r = document.querySelector('[data-composition-id]');
    const d = r && +r.getAttribute('data-duration');
    return d > 0 ? d : window.__timelines.main.duration();
  });
  const fontOk = await p.evaluate(() => document.fonts.check('800 40px Inter'));
  if (!fontOk) console.error('WARNING: Inter did not load; text widths are measured with a fallback font');

  const worst = new Map(), clashes = new Map();
  let samples = 0;
  for (let t = 0; t <= dur + 1e-6; t += every) {
    const tt = Math.min(t, dur);
    // braces on purpose: seek() returns the GSAP timeline, which has a .then(), and Playwright
    // would await it as a promise that never resolves
    await p.evaluate(x => { window.__timelines.main.seek(x); }, tt);
    await p.waitForTimeout(60);
    samples++;
    const hits = await p.evaluate(({ S, tt }) => {
      const out = [], boxes = [];
      const root = document.querySelector('[data-composition-id]') || document.body;
      const blurOf = st => { const m = /blur\(([\d.]+)px\)/.exec(st.filter || ''); return m ? +m[1] : 0; };
      const scaleOf = st => { const m = /matrix\(([-\d.]+),/.exec(st.transform || ''); return m ? +m[1] : 1; };
      // same exemption as safe_check.js: a zoom-through transition frame is blurred past reading
      const exempt = st => blurOf(st) > 2 || (scaleOf(st) > 1.05 && blurOf(st) > 1);
      const outsideWindow = el => {                    // HyperFrames clip window, applied by hand
        const s = el.getAttribute && el.getAttribute('data-start'), d = el.getAttribute && el.getAttribute('data-duration');
        if (s === null || d === null || s === undefined || d === undefined) return false;
        return tt < +s - 1e-6 || tt > +s + +d + 1e-6;
      };
      for (const el of document.querySelectorAll('body *')) {
        const own = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join(' ').trim();
        if (!own) continue;
        if (['SCRIPT', 'STYLE'].includes(el.tagName)) continue;
        const cs = getComputedStyle(el);
        if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity < 0.05) continue;
        if (exempt(cs) || outsideWindow(el)) continue;
        let hidden = false;
        let r = el.getBoundingClientRect();
        let clipL = -1e9, clipT = -1e9, clipR = 1e9, clipB = 1e9;
        for (let a = el.parentElement; a; a = a.parentElement) {
          const pc = getComputedStyle(a);
          if (pc.visibility === 'hidden' || pc.display === 'none' || +pc.opacity < 0.05 || exempt(pc) || outsideWindow(a)) { hidden = true; break; }
          if (a !== root && a !== document.body && a !== document.documentElement &&
              (pc.overflow !== 'visible' || pc.overflowX !== 'visible' || pc.overflowY !== 'visible')) {
            const ar = a.getBoundingClientRect();
            clipL = Math.max(clipL, ar.left); clipT = Math.max(clipT, ar.top);
            clipR = Math.min(clipR, ar.right); clipB = Math.min(clipB, ar.bottom);
          }
        }
        if (hidden) continue;
        if (r.width < 2 || r.height < 2) continue;
        if (el.closest('[data-decor]')) continue;
        // clip to overflow:hidden ancestors (phone screens parked off to the side)
        const vis = { left: Math.max(r.left, clipL), top: Math.max(r.top, clipT),
                      right: Math.min(r.right, clipR), bottom: Math.min(r.bottom, clipB) };
        if (vis.right - vis.left < 2 || vis.bottom - vis.top < 2) continue;
        r = { left: vis.left, top: vis.top, right: vis.right, bottom: vis.bottom,
              width: vis.right - vis.left, height: vis.bottom - vis.top };
        // text hidden behind an opaque element (a phone screen sliding over the one before it)
        // is not on screen: probe the centre of the visible box
        const cx = Math.min(1079, Math.max(0, (r.left + r.right) / 2)), cy = Math.min(1919, Math.max(0, (r.top + r.bottom) / 2));
        // (elementsFromPoint, topmost first: elementFromPoint alone would stop at an opacity:0 chip)
        let covered = false;
        for (const s of document.elementsFromPoint(cx, cy)) {
          if (s === el || el.contains(s) || s.contains(el)) break;      // reached the text itself
          const sc = getComputedStyle(s), m = /rgba?\(([^)]+)\)/.exec(sc.backgroundColor);
          const alpha = m ? (m[1].split(',')[3] === undefined ? 1 : +m[1].split(',')[3]) : 0;
          let eff = 1;
          for (let q = s; q; q = q.parentElement) eff *= +getComputedStyle(q).opacity;
          if ((alpha >= 0.9 || ['IMG', 'SVG', 'CANVAS', 'VIDEO'].includes(s.tagName)) && eff >= 0.9) { covered = true; break; }
        }
        if (covered) continue;
        const over = {
          top: Math.max(0, S.top - r.top), bottom: Math.max(0, r.bottom - (1920 - S.bottom)),
          left: Math.max(0, S.left - r.left), right: Math.max(0, r.right - (1080 - S.right)),
        };
        const px = Math.max(over.top, over.bottom, over.left, over.right);
        const id = el.id ? '#' + el.id : (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\s+/).join('.') : el.tagName);
        if (px > 1) out.push({ id, text: own.slice(0, 34), px: Math.round(px),
          side: Object.entries(over).sort((a, b) => b[1] - a[1])[0][0], rect: [Math.round(r.top), Math.round(r.bottom)] });
        // overlap checks use per-line fragments (see safe_check.js for why), clipped like above
        for (const fr of el.getClientRects()) {
          if (fr.width < 2 || fr.height < 2) continue;
          const l = Math.max(fr.left, clipL), tp = Math.max(fr.top, clipT), rr = Math.min(fr.right, clipR), bb = Math.min(fr.bottom, clipB);
          if (rr - l < 2 || bb - tp < 2) continue;
          boxes.push({ el, id, text: own.slice(0, 24), t: tp, b: bb, l, r: rr,
                       full: r.width > 1000 && r.height > 1700 });
        }
      }
      const clash = [];
      for (let i = 0; i < boxes.length; i++)
        for (let j = i + 1; j < boxes.length; j++) {
          const a = boxes[i], c = boxes[j];
          if (a.el.contains(c.el) || c.el.contains(a.el)) continue;
          if (a.full || c.full) continue;
          const ov = Math.min(a.b, c.b) - Math.max(a.t, c.t);
          const oh = Math.min(a.r, c.r) - Math.max(a.l, c.l);
          if (ov > 4 && oh > 4) clash.push({ a: a.id, b: c.id, ta: a.text, tb: c.text, px: Math.round(Math.min(ov, oh)) });
        }
      return { violations: out, clash };
    }, { S: SAFE, tt });
    let flagged = false;
    // per finding: worst px, and the first/last sample where it is over tolerance (+ count), so a
    // one-frame animation transient can be told apart from something that sits on screen
    const note = (map, key, h) => {
      const cur = map.get(key) || { ...h, at: +tt.toFixed(2), n: 0, first: null, last: null };
      if (h.px > cur.px) Object.assign(cur, h, { at: +tt.toFixed(2) });
      if (h.px >= tol) { cur.n++; cur.first = cur.first ?? +tt.toFixed(2); cur.last = +tt.toFixed(2); flagged = true; }
      map.set(key, cur);
    };
    for (const c of hits.clash) note(clashes, `${c.a} x ${c.b}`, c);
    for (const h of hits.violations) note(worst, `${h.id}|${h.side}`, h);
    if (flagged && shots) await p.screenshot({ path: path.join(shots, `t${tt.toFixed(2)}.png`) });
  }
  await b.close();

  console.log(`${path.basename(file)}  ${(+dur).toFixed(2)}s  ${samples} samples every ${every}s  safe box: x ${SAFE.left}-${W - SAFE.right}, y ${SAFE.top}-${H - SAFE.bottom}${tiktok ? '  (tiktok right margin)' : ''}`);
  if (pageErrors.length) console.log('  page errors: ' + [...new Set(pageErrors)].join('; '));
  const all = [...worst.values()].sort((a, b) => b.px - a.px);
  const rows = all.filter(r => r.px >= tol), minor = all.filter(r => r.px < tol);
  if (!rows.length) console.log(`  safe area: clean (tolerance ${tol}px)`);
  for (const r of rows) console.log(`  ${String(r.px).padStart(4)}px past the ${r.side} line   y ${r.rect[0]}-${r.rect[1]}  worst at ${r.at}s, over tol in ${r.n} hits ${r.first}-${r.last}s   ${r.id}  "${r.text}"`);
  for (const r of minor) console.log(`  within tolerance: ${r.px}px past the ${r.side} line   ${r.id}  "${r.text}"`);
  const clAll = [...clashes.values()].sort((a, b) => b.px - a.px);
  const cl = clAll.filter(c => c.px >= tol);
  if (!cl.length) console.log(`  overlaps: none over ${tol}px`);
  for (const c of clAll.filter(c => c.px < tol)) console.log(`  within tolerance: ${c.px}px overlap  ${c.a} x ${c.b}`);
  for (const c of cl) console.log(`  overlap ${String(c.px).padStart(4)}px worst at ${c.at}s, ${c.n} hits ${c.first}-${c.last}s   ${c.a} "${c.ta}"  x  ${c.b} "${c.tb}"`);
  if (rows.length || cl.length) process.exitCode = 1;
})().catch(e => { console.error('safe_check_hf failed: ' + e.message); process.exit(2); });
