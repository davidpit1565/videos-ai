#!/usr/bin/env node
// Builds public/site/ep98/race.json, the compact replay the /e/98 page plays.
//
//   node scripts/ep98-race-json.mjs <race.json from run_race.mjs> <answers dir>
//
// Input: the full race.json written by video/ep98/arena/run_race.mjs (the real race,
// sha256 efda0893670a53e2afdc4342d752f5e0585c5c3057fc4b814ee2637d29435215 on 14.11.2026)
// and the folder with the five answers as received (chatgpt-A.txt ...).
// It refuses to write if public/site/ep98/arena.js or track.json are not the frozen
// files the race was run with, or if an answer file is not the one the race used.
// Nothing is re-simulated here: positions are copied from the real race, rounded
// (x, y to 0.1 px, angle to 0.01 rad), and cut at the frame each car stopped.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const site = join(here, "..", "public", "site", "ep98");
const sha = (b) => createHash("sha256").update(b).digest("hex");

const [racePath, answersDir] = process.argv.slice(2);
if (!racePath || !answersDir) {
  console.error("usage: node scripts/ep98-race-json.mjs <race.json> <answers dir>");
  process.exit(2);
}
const raceBuf = readFileSync(racePath);
const race = JSON.parse(raceBuf.toString("utf8"));

const arenaSha = sha(readFileSync(join(site, "arena.js")));
const trackSha = sha(readFileSync(join(site, "track.json")));
if (arenaSha !== race.arenaSha256 || trackSha !== race.trackSha256) {
  console.error("public/site/ep98/arena.js or track.json differ from the files the race ran with. Refusing.");
  process.exit(3);
}

const LABEL = { chatgpt: "ChatGPT", gemini: "Gemini", claude: "Claude", meta: "Meta AI", perplexity: "Perplexity" };
const r1 = (v) => Math.round(v * 10) / 10;
const r2 = (v) => Math.round(v * 100) / 100;

const cars = race.cars.map((c) => {
  const res = race.result.find((r) => r.id === c.id);
  const text = readFileSync(join(answersDir, res.file));
  if (sha(text) !== res.fileSha256) {
    console.error(`answer file ${res.file} is not the one the race used. Refusing.`);
    process.exit(4);
  }
  // frames up to and including the first frame that is not "run"
  let end = c.frames.findIndex((f) => f[5] !== "run");
  if (end < 0) end = c.frames.length - 1;
  const f = [];
  const lapFrames = [];
  for (let i = 0; i <= end; i++) {
    const [x, y, a, , lap] = c.frames[i];
    f.push(r1(x), r1(y), r2(a));
    if (i > 0 && lap > c.frames[i - 1][4]) lapFrames.push(i);
  }
  return {
    id: c.id,
    label: LABEL[c.id] || c.id,
    status: res.status,
    endFrame: end,
    finishFrame: res.finishFrame,
    stopFrame: res.stopFrame,
    stopReason: res.stopReason,
    stopSector: res.stopSector,
    progressLaps: res.progressLaps,
    lapFrames,
    fileSha256: res.fileSha256,
    answer: text.toString("utf8"),
    f,
  };
});

const out = {
  format: "AI RACE #1 site replay v1",
  madeFrom: "video/ep98/arena/run_race.mjs race.json",
  sourceRaceSha256: sha(raceBuf),
  arenaSha256: arenaSha,
  trackSha256: trackSha,
  fps: race.fps,
  maxFrames: race.constants.MAX_FRAMES,
  order: race.result.map((r) => r.id),
  cars,
};
const dest = join(site, "race.json");
writeFileSync(dest, JSON.stringify(out) + "\n");
console.log("wrote", dest, readFileSync(dest).length, "bytes, sha256", sha(readFileSync(dest)));
