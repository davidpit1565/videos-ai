// make_maze.mjs: builds maze.json from a seed.
// Run once: `node make_maze.mjs` (writes maze.json next to this file).
// maze.json is the frozen artefact (hashed in HASH.txt); this script only
// documents how it was made. Re-running it gives a byte-identical file.
//
// 1. a perfect maze (one path between any two cells) by depth-first carving
//    from the centre, with a seeded random order (mulberry32);
// 2. LOOPS extra inner walls are knocked out, so there are loops (a dot that
//    only follows one wall can circle an island forever);
// 3. one gap in the outer wall is the exit (side and place from the same seed).
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
export const SEED = 1083;  // chosen in calibration, see README
export const LOOPS = 14;
const W = 21, H = 21;
const BIT = { up: 1, right: 2, down: 4, left: 8 };
const OPP = { up: 'down', down: 'up', left: 'right', right: 'left' };
const DX = { up: 0, right: 1, down: 0, left: -1 };
const DY = { up: -1, right: 0, down: 1, left: 0 };
const DIRS = ['up', 'right', 'down', 'left'];

function mulberry32(seed) {
  let s = seed >>> 0;
  return () => {
    s = (s + 0x6D2B79F5) >>> 0; let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function makeMaze(seed = SEED, loops = LOOPS) {
  const rnd = mulberry32(seed);
  const open = Array.from({ length: H }, () => new Array(W).fill(0));
  const seen = Array.from({ length: H }, () => new Array(W).fill(false));
  const start = { x: 10, y: 10 };
  const stack = [[start.x, start.y]];
  seen[start.y][start.x] = true;
  while (stack.length) {
    const [x, y] = stack[stack.length - 1];
    const next = DIRS.filter((d) => {
      const nx = x + DX[d], ny = y + DY[d];
      return nx >= 0 && ny >= 0 && nx < W && ny < H && !seen[ny][nx];
    });
    if (!next.length) { stack.pop(); continue; }
    const d = next[Math.floor(rnd() * next.length)];
    const nx = x + DX[d], ny = y + DY[d];
    open[y][x] |= BIT[d]; open[ny][nx] |= BIT[OPP[d]];
    seen[ny][nx] = true; stack.push([nx, ny]);
  }
  // knock out inner walls to make loops
  let made = 0, guard = 0;
  while (made < loops && guard++ < 10000) {
    const x = Math.floor(rnd() * W), y = Math.floor(rnd() * H);
    const d = rnd() < 0.5 ? 'right' : 'down';
    const nx = x + DX[d], ny = y + DY[d];
    if (nx >= W || ny >= H || (open[y][x] & BIT[d])) continue;
    open[y][x] |= BIT[d]; open[ny][nx] |= BIT[OPP[d]]; made++;
  }
  // the exit: one gap in the outer wall
  const side = DIRS[Math.floor(rnd() * 4)];
  const pos = Math.floor(rnd() * 21);
  const exit = side === 'up' ? { x: pos, y: 0 } : side === 'down' ? { x: pos, y: H - 1 }
    : side === 'left' ? { x: 0, y: pos } : { x: W - 1, y: pos };
  exit.side = side;
  open[exit.y][exit.x] |= BIT[side];
  return {
    format: 'AI RACE #2 maze.json v1',
    seed, loopsAdded: loops, width: W, height: H,
    openBits: { up: 1, right: 2, down: 4, left: 8 },
    start, exit,
    open: open.map((r) => r.map((v) => v.toString(16)).join('')),
    picture: drawAscii(open, start, exit),
  };
}

function drawAscii(open, start, exit) {
  const out = [];
  for (let y = 0; y < H; y++) {
    let top = '+', mid = '';
    for (let x = 0; x < W; x++) {
      top += (open[y][x] & BIT.up) ? '   +' : '---+';
      mid += (x === 0 ? ((open[y][x] & BIT.left) ? ' ' : '|') : '');
      const ch = x === start.x && y === start.y ? ' S ' : x === exit.x && y === exit.y ? ' E ' : '   ';
      mid += ch + ((open[y][x] & BIT.right) ? ' ' : '|');
    }
    out.push(top, mid);
  }
  let bot = '+';
  for (let x = 0; x < W; x++) bot += (open[H - 1][x] & BIT.down) ? '   +' : '---+';
  out.push(bot);
  return out;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  writeFileSync(join(here, 'maze.json'), JSON.stringify(makeMaze(), null, 1) + '\n');
  console.log('wrote maze.json, seed', SEED, 'loops', LOOPS);
}
