/** Writes lib/reels-manifest.json: everything lib/reels.ts used to read from disk at
 *  request time (the reel list, each reel's gate verdict and ship time, the caption and
 *  YouTube text for every episode).
 *
 *  Why this exists (6.10.2026): reading public/reels/ at runtime made Next's file tracing
 *  pack every .mp4 (~390 MB) into each serverless function that touched the reel list, so
 *  every deployment multiplied the videos by the number of functions. Vercel's
 *  "Functions Storage" reached 162 GB against a 10 GB Hobby limit and the whole team was
 *  paused. With the facts in this small JSON file, no function needs the videos at all.
 *
 *  Runs before every build (prebuild) and before `next dev` (predev), so a newly shipped
 *  reel appears without anyone touching this. Must run BEFORE prune-old-reels.mjs. */
import { readdirSync, statSync, readFileSync, existsSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const studio = fileURLToPath(new URL("..", import.meta.url));
const DIR = join(studio, "public", "reels");
const CHANNEL = join(studio, "..", "channel");

const read = (p) => {
  try {
    return existsSync(p) ? readFileSync(p, "utf8").trim() : null;
  } catch {
    return null;
  }
};

const reels = [];
let names = [];
try {
  names = readdirSync(DIR).filter((f) => /\.(mp4|m4a|wav)$/.test(f));
} catch {
  names = [];
}
for (const file of names) {
  const st = statSync(join(DIR, file));
  const sidecar = read(join(DIR, file.replace(/\.(mp4|m4a|wav)$/, ".built-at.txt")));
  const gateText = /\.mp4$/.test(file) ? read(join(DIR, file.replace(/\.mp4$/, ".gate.txt"))) : null;
  reels.push({
    file,
    bytes: st.size,
    builtAt: sidecar || st.mtime.toISOString(),
    gate: gateText === null ? null : { passed: /ALL CHECKS PASSED/.test(gateText), text: gateText },
  });
}

const texts = { caption: {}, youtube: {} };
try {
  for (const f of readdirSync(CHANNEL)) {
    const m = f.match(/^episode-(\d+)-(caption|youtube)\.txt$/);
    if (!m) continue;
    const t = read(join(CHANNEL, f));
    if (t !== null) texts[m[2]][String(Number(m[1]))] = t;
  }
} catch {
  /* no channel folder (a build outside the repo): the page falls back to empty text */
}

const out = join(studio, "lib", "reels-manifest.json");
writeFileSync(out, JSON.stringify({ reels, texts }) + "\n");
console.log(`reels-manifest.json -> ${reels.length} reels, ${Object.keys(texts.caption).length} captions`);
