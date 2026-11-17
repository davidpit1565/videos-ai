// check_rules.mjs: checks that PROMPT-B.txt says what maze.js and maze.json do.
// `node check_rules.mjs` prints each check and exits 1 on any failure.
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
const here = dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const Maze = require(join(here, 'maze.js'));
const raw = JSON.parse(readFileSync(join(here, 'maze.json'), 'utf8'));
const M = Maze.prepareMaze(raw);
const P = readFileSync(join(here, 'PROMPT-B.txt'), 'utf8').replace(/\s+/g, ' ');
let bad = 0;
const ok = (name, cond) => { console.log((cond ? 'ok   ' : 'FAIL ') + name); if (!cond) bad++; };
const says = (s) => P.includes(s);

ok('prompt: one function move(v)', says('function move(v) { ... }'));
ok('size 21 x 21 = maze.json', says('21 x 21 maze') && raw.width === 21 && raw.height === 21);
ok('x 0..20 left to right, y 0..20 top to bottom', says('x 0 to 20 from left to right') && says('y 0 to 20 from top to bottom'));
ok('start x 10, y 10 = maze.json start', says('starts at x 10, y 10') && raw.start.x === 10 && raw.start.y === 10);
const b0 = Maze.initBot(M), v0 = Maze.view(M, b0);
ok('v has exactly up, down, left, right, x, y', JSON.stringify(Object.keys(v0).sort()) === JSON.stringify(['down', 'left', 'right', 'up', 'x', 'y']));
ok('v.x, v.y = own cell', v0.x === 10 && v0.y === 10);
const vals = new Set();
for (let y = 0; y < 21; y++) for (let x = 0; x < 21; x++) { const v = Maze.view(M, { x, y }); ['up', 'down', 'left', 'right'].forEach((d) => vals.add(v[d])); }
ok('sides are only "wall" | "open" | "exit"', [...vals].sort().join() === 'exit,open,wall' && says('"wall", "open" or "exit"'));
let exits = 0;
for (let y = 0; y < 21; y++) for (let x = 0; x < 21; x++) { const v = Maze.view(M, { x, y }); ['up', 'down', 'left', 'right'].forEach((d) => { if (v[d] === 'exit') exits++; }); }
const e = raw.exit, onEdge = e.x === 0 || e.y === 0 || e.x === 20 || e.y === 20;
ok('exactly one exit, a gap in the outer wall', exits === 1 && onEdge && says('one gap in the outer wall'));
// find a cell with an open side up and one with an open side right
let cu = null, cr = null;
for (let y = 1; y < 21 && !(cu && cr); y++) for (let x = 0; x < 20; x++) { const v = Maze.view(M, { x, y }); if (!cu && v.up === 'open') cu = { x, y }; if (!cr && v.right === 'open') cr = { x, y }; }
const sU = Maze.step(M, { ...Maze.initBot(M), ...cu }, 'up');
const sR = Maze.step(M, { ...Maze.initBot(M), ...cr }, 'right');
ok('"up" is y minus 1, "right" is x plus 1', says('Up is y minus 1, right is x plus 1') && sU.y === cu.y - 1 && sU.x === cu.x && sR.x === cr.x + 1 && sR.y === cr.y);
const wallDir = ['up', 'down', 'left', 'right'].find((d) => v0[d] === 'wall');
const sW = Maze.step(M, b0, wallDir), sI = Maze.step(M, b0, 'Up'), sN = Maze.step(M, b0, undefined, 'threw: x');
ok('move into a wall: stays, step counted, run goes on', sW.x === 10 && sW.y === 10 && sW.step === 1 && sW.status === 'run');
ok('anything else ("Up", a throw): stays, step counted, run goes on', sI.x === 10 && sI.step === 1 && sI.status === 'run' && sN.status === 'run' && says('Anything else, or a move into a wall, keeps the dot where it is'));
let b = Maze.initBot(M); while (b.status === 'run') b = Maze.step(M, b, wallDir);
ok('500 steps, then the run ends (dnf)', Maze.CONST.MAX_STEPS === 500 && b.step === 500 && b.status === 'dnf' && says('You get 500 steps'));
// "exit" side: moving through it ends the run
const ex = Maze.step(M, { ...Maze.initBot(M), x: e.x, y: e.y }, e.side);
ok('"exit" means that move leaves the maze', ex.status === 'exit' && says('"exit" means that move leaves the maze'));
// dead ends and loops exist
let dead = 0, edges = 0;
for (const row of M.open) for (const c of row) { const n = [1, 2, 4, 8].filter((k) => c & k).length; if (n === 1) dead++; edges += n; }
const inner = (edges - 1) / 2; // the exit gap is counted once
ok(`dead ends (${dead}) and loops (${inner - (21 * 21 - 1)} more passages than a tree)`, dead > 0 && inner > 21 * 21 - 1 && says('dead ends and loops'));
ok('memory between calls is allowed (run_maze keeps one sandbox per dot)', says('keep its own memory between calls'));
ok('goal: fewest steps', says('reach the exit in as few steps as possible'));
process.exit(bad ? 1 : 0);
