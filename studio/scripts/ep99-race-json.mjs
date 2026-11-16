#!/usr/bin/env node
// Builds public/site/ep99/race.json, the compact replay the /e/99 page plays.
//
//   node scripts/ep99-race-json.mjs <maze-race.json from run_maze.mjs> <answers dir> [--placeholder]
//
// Input: the full maze-race.json written by video/ep99/arena/run_maze.mjs (the real race)
// and the folder with the answers as received (chatgpt-B.txt ...; for --placeholder the folder
// with ref-naive.js and ref-careful.js).
// It refuses to write if public/site/ep99/maze.js or maze.json are not the frozen files the race
// was run with, or if an answer file is not the one the race used. Nothing is re-simulated:
// every dot's cells are copied from the real race, as a flat list x0,y0,x1,y1,...
//
// --placeholder: the input is the run of our two reference bots (video/ep99/arena/ref-maze-race.json).
// They are written with reference:true and a label that says they are our own bots, not AIs,
// and the file says placeholder:true so the page shows a notice. Use it only until the real
// five AI answers have been run.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const site = join(here, "..", "public", "site", "ep99");
const sha = (b) => createHash("sha256").update(b).digest("hex");

const args = process.argv.slice(2);
const placeholder = args.includes("--placeholder");
const [racePath, answersDir] = args.filter((a) => !a.startsWith("--"));
if (!racePath || !answersDir) {
  console.error("usage: node scripts/ep99-race-json.mjs <maze-race.json> <answers dir> [--placeholder]");
  process.exit(2);
}
const raceBuf = readFileSync(racePath);
const race = JSON.parse(raceBuf.toString("utf8"));

const mazeJsSha = sha(readFileSync(join(site, "maze.js")));
const mazeJsonSha = sha(readFileSync(join(site, "maze.json")));
if (mazeJsSha !== race.sha256["maze.js"] || mazeJsonSha !== race.sha256["maze.json"]) {
  console.error("public/site/ep99/maze.js or maze.json differ from the files the race ran with. Refusing.");
  process.exit(3);
}

const LABEL = {
  chatgpt: "ChatGPT", gemini: "Gemini", claude: "Claude", meta: "Meta AI", perplexity: "Perplexity",
  careful: "Reference bot: careful (ours, not an AI)",
  naive: "Reference bot: naive (ours, not an AI)",
};
const COUNT = race.paths.length;
const cars = race.result.map((res) => {
  const text = readFileSync(join(answersDir, res.file));
  if (sha(text) !== res.fileSha256) {
    console.error(`answer file ${res.file} is not the one the race used. Refusing.`);
    process.exit(4);
  }
  const p = race.paths.find((x) => x.id === res.id);
  if (!p) { console.error(`no path for ${res.id}. Refusing.`); process.exit(5); }
  const flat = [];
  for (const [x, y] of p.path) flat.push(x, y);
  return {
    id: res.id,
    label: LABEL[res.id] || res.id,
    reference: placeholder ? true : undefined,
    status: res.status,
    steps: res.steps,
    exitStep: res.exitStep,
    closestDist: res.closestDist,
    closestStep: res.closestStep,
    wallBumps: res.wallBumps,
    invalidSteps: res.invalidSteps,
    firstInvalid: res.firstInvalid,
    stopReason: res.stopReason,
    cellsVisited: res.cellsVisited,
    fileSha256: res.fileSha256,
    p: flat,
  };
});

const out = {
  format: "AI RACE #2 site replay v1",
  placeholder: placeholder || undefined,
  note: placeholder
    ? "PLACEHOLDER: only our two reference bots (not AIs). The five AI results replace this file after the race."
    : undefined,
  madeFrom: "video/ep99/arena/run_maze.mjs maze-race.json",
  sourceRaceSha256: sha(raceBuf),
  mazeJsSha256: mazeJsSha,
  mazeJsonSha256: mazeJsonSha,
  maxSteps: race.constants.MAX_STEPS,
  shortestSteps: race.shortestSteps,
  order: race.result.map((r) => r.id),
  cars,
};
const dest = join(site, "race.json");
writeFileSync(dest, JSON.stringify(out) + "\n");
console.log("wrote", dest, readFileSync(dest).length, "bytes,", COUNT, "dots, sha256", sha(readFileSync(dest)));
