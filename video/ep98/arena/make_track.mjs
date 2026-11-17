// make_track.mjs: builds track.json from a handful of control points.
// Run once: `node make_track.mjs` (writes track.json next to this file).
// track.json is the frozen artefact (hashed in HASH.txt); this script only
// documents how it was made. Pure arithmetic, no randomness.
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));

// World = 950 x 808 px, laid out to sit 1:1 in the phone frame at
// x 65-1015, y 440-1248 (plan section 4). y points down. Driving order.
// [x, y, roadWidth]
const CP = [
  [300, 700, 140], // start straight, heading east
  [560, 705, 140],
  [770, 660, 128],
  [865, 490, 122], // long sweep (right side)
  [810, 270, 122],
  [650, 150, 128],
  [480, 160, 134], // top, turning down-left
  [400, 250, 140], // back straight (diagonal)
  [350, 390, 136],
  [300, 500, 124],
  [230, 538, 108], // into the hairpin (arc, centre 230,622, r 84)
  [171, 563, 98],
  [146, 622, 92],  // hairpin apex
  [171, 681, 98],
  [230, 706, 108], // out of the hairpin
];
const SECTORS = [
  // [name, first control point index] (sector runs to the next one)
  ['start straight', 0],
  ['long sweep', 2],
  ['back straight', 6],
  ['hairpin', 10],
  ['start straight', 14],
];

// Closed centripetal Catmull-Rom, sampled finely, then resampled by arc length.
function catmull(p0, p1, p2, p3, t) {
  const a = 0.5;
  const d = (p, q) => Math.pow(Math.hypot(q[0] - p[0], q[1] - p[1]), a);
  const t0 = 0, t1 = t0 + d(p0, p1), t2 = t1 + d(p1, p2), t3 = t2 + d(p2, p3);
  const tt = t1 + (t2 - t1) * t;
  const lerp = (A, B, ta, tb) => A.map((v, i) => ((tb - tt) / (tb - ta)) * v + ((tt - ta) / (tb - ta)) * B[i]);
  const A1 = lerp(p0, p1, t0, t1), A2 = lerp(p1, p2, t1, t2), A3 = lerp(p2, p3, t2, t3);
  const B1 = lerp(A1, A2, t0, t2), B2 = lerp(A2, A3, t1, t3);
  return lerp(B1, B2, t1, t2);
}
const n = CP.length;
const fine = [];
const fineCp = [];
for (let i = 0; i < n; i++) {
  const p0 = CP[(i - 1 + n) % n], p1 = CP[i], p2 = CP[(i + 1) % n], p3 = CP[(i + 2) % n];
  for (let k = 0; k < 200; k++) {
    fine.push(catmull(p0, p1, p2, p3, k / 200));
    fineCp.push(i + k / 200);
  }
}
// cumulative length
const cum = [0];
for (let i = 1; i <= fine.length; i++) {
  const a = fine[i - 1], b = fine[i % fine.length];
  cum.push(cum[i - 1] + Math.hypot(b[0] - a[0], b[1] - a[1]));
}
const total = cum[fine.length];
const STEP = 6;
const N = Math.round(total / STEP);
const center = [];
let j = 0;
for (let k = 0; k < N; k++) {
  const s = (k / N) * total;
  while (cum[j + 1] < s) j++;
  const f = (s - cum[j]) / (cum[j + 1] - cum[j]);
  const a = fine[j], b = fine[(j + 1) % fine.length];
  const ca = fineCp[j], cb = j + 1 < fineCp.length ? fineCp[j + 1] : n;
  const cp = ca + (cb - ca) * f;
  // width: smooth (cosine) blend between the two control points, never overshoots
  const i0 = Math.floor(cp) % n, i1 = (i0 + 1) % n, u = cp - Math.floor(cp);
  const w = CP[i0][2] + (CP[i1][2] - CP[i0][2]) * (1 - Math.cos(Math.PI * u)) / 2;
  center.push({ x: a[0] + (b[0] - a[0]) * f, y: a[1] + (b[1] - a[1]) * f, w, cp });
}
const r3 = (v) => Math.round(v * 1000) / 1000;
// normals and edges. Left = left of the driving direction.
const left = [], right = [], gates = [], sectorOf = [];
for (let k = 0; k < N; k++) {
  const p = center[(k - 1 + N) % N], q = center[(k + 1) % N], c = center[k];
  const tx = q.x - p.x, ty = q.y - p.y, L = Math.hypot(tx, ty);
  // heading (tx,ty); with y down, the driver's left is (ty, -tx)
  const nx = ty / L, ny = -tx / L, h = c.w / 2;
  left.push([r3(c.x + nx * h), r3(c.y + ny * h)]);
  right.push([r3(c.x - nx * h), r3(c.y - ny * h)]);
  let name = SECTORS[0][0];
  for (const [nm, from] of SECTORS) if (c.cp >= from) name = nm;
  sectorOf.push(name);
}
// curvature report (radius from three points 5 samples apart)
function radiusAt(k) {
  const a = center[(k - 5 + N) % N], b = center[k], c = center[(k + 5) % N];
  const A = Math.hypot(b.x - a.x, b.y - a.y), B = Math.hypot(c.x - b.x, c.y - b.y), C = Math.hypot(c.x - a.x, c.y - a.y);
  const area2 = Math.abs((b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x));
  return area2 < 1e-9 ? Infinity : (A * B * C) / (2 * area2);
}
let minR = Infinity, minRk = 0;
const report = {};
for (let k = 0; k < N; k++) {
  const R = radiusAt(k);
  if (R < minR) { minR = R; minRk = k; }
  const s = sectorOf[k];
  report[s] = Math.min(report[s] ?? Infinity, R);
  if (R < center[k].w / 2 + 5) throw new Error(`edge would fold at sample ${k}: R=${R} w=${center[k].w}`);
}
// heading change through the hairpin sector
const hk = sectorOf.map((s, k) => (s === 'hairpin' ? k : -1)).filter((k) => k >= 0);
const head = (k) => { const p = center[k], q = center[(k + 1) % N]; return Math.atan2(q.y - p.y, q.x - p.x); };
let turn = 0;
for (let i = 0; i < hk.length; i++) { let d = head((hk[i] + 1) % N) - head(hk[i]); while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; turn += d; }

// start pose: car centre on the finish line (sample 0), so 2 laps = exactly 2 x lengthPx
const s0 = 0;
const start = { x: r3(center[s0].x), y: r3(center[s0].y), angle: r3(head(s0)) };
const widths = center.map((c) => c.w);
const track = {
  name: 'AI RACE #1 circuit',
  units: 'px, y down, angle in radians (0 = +x, positive = clockwise on screen)',
  world: { width: 950, height: 808, screenOffset: { x: 65, y: 440 } },
  laps: 2,
  lengthPx: r3(total),
  widthMinPx: r3(Math.min(...widths)), widthMaxPx: r3(Math.max(...widths)),
  start,
  finishGate: 0,
  centerline: center.map((c) => [r3(c.x), r3(c.y), r3(c.w)]),
  leftEdge: left,
  rightEdge: right,
  sector: sectorOf,
};
writeFileSync(join(here, 'track.json'), JSON.stringify(track) + '\n');
console.log(JSON.stringify({ samples: N, length: r3(total), widthMin: track.widthMinPx, widthMax: track.widthMaxPx,
  minRadius: r3(minR), minRadiusSector: sectorOf[minRk], minRadiusBySector: Object.fromEntries(Object.entries(report).map(([k, v]) => [k, r3(v)])),
  hairpinTurnDeg: r3((turn * 180) / Math.PI) }, null, 1));
