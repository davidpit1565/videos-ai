// ChatGPT age film, v5 (alive build). Canvas 2D, pure function of t. ALL timing comes from voices/cues.json + voices/words.json (written by align.py from the cues JSON + narration wav).
// If words.json is missing or does not match script.json, per-word times fall back to character count inside each line's cue window.
const W = 1080, H = 1920;
const cv = document.getElementById('c'); let g = cv.getContext('2d');
await Promise.all([700, 800, 900, 600, 500].flatMap(w => [`${w} 40px Inter`, `${w} 40px InterTight`, `${w} 40px JBMono`]).map(f => document.fonts.load(f)));
const get = async (u, d) => { try { const r = await fetch(u); return r.ok ? await r.json() : d; } catch { return d; } };
const SCRIPT = await get('script.json', {});
const TOK = Object.fromEntries(Object.entries(SCRIPT).map(([k, v]) => [k, v.split(/\s+/)]));
const WD = await get('voices/words.json', {});
const DJ = await get('voices/dur.json', {});
const META = await get('voices/meta.json', {});
const IMG = async u => createImageBitmap(await (await fetch(u)).blob());
const TR = await IMG('tr.png'), TC = await IMG('tc.png'), TB = await IMG('trb.png');
const svg = await (await fetch('chatgpt.svg')).text();
const MARK = new Path2D(svg.match(/ d='([^']+)'/)[1]);
const C = { paper: '#F4F4EF', dot: '#E0E0D6', ink: '#0E0E0E', ink2: '#4B4B46', dark: '#14151A', dark2: '#22242C', dark3: '#2E3039', lime: '#B6F23A', limeDeep: '#4E8F0B', wash: '#E4F8B0', white: '#FFFFFF', mute: '#8E908A' };
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const sg = (t, a, b) => clamp((t - a) / (b - a));
const sm = x => { x = clamp(x); return x * x * x * (x * (x * 6 - 15) + 10); };         // smootherstep
const enterE = x => 1 - Math.pow(1 - clamp(x), 4);
const expoE = x => { x = clamp(x); return x >= 1 ? 1 : 1 - Math.pow(2, -10 * x); };
const backE = x => { x = clamp(x); const c1 = 2.0, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };   // overshoot pop
const ioE = x => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const lerp = (a, b, t) => a + (b - a) * t;
const rng = s => () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
// ---- timing: line starts (T), per-word starts (wt) ----
const T = Object.assign({ l1: .08, l2: 3.57, l3: 7.55, l4: 10.42, l5: 13.95, l6: 17.01, l7: 21.45, l8: 25.14, l9: 27.8 }, await get('voices/cues.json', {}));
const WDC = {};
function wordsOf(l) {
  const toks = TOK[l], w = WD[l];
  if (w && w.length === toks.length) return w;
  const d = (DJ[l] ?? 2.6) * .96, n = s => s.replace(/[^a-z0-9']/gi, '').length + 1.1, tot = toks.reduce((a, s) => a + n(s), 0); let a = 0;
  return toks.map(s => { const r = [s, a / tot * d, (a + n(s) - 1.1) / tot * d]; a += n(s); return r; });
}
const wt = (l, i) => T[l] + Math.max(0, (WDC[l] ??= wordsOf(l))[i][1]);   // spoken start of word i of line l
const we = (l, i) => T[l] + Math.max(0, (WDC[l] ??= wordsOf(l))[i][2]);   // spoken end
const lineEnd = n => T['l' + n] + (DJ['l' + n] ?? 2.6);
const DUR = META.dur ?? 33.3; window.DUR = DUR;
