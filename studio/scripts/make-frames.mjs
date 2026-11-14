// One real still per reel, for the public site's episode lists (rebrand 2, 13.11.2026).
//
// The site had no picture per episode: the /episodes thumbnails were the share card (the
// title as text, shrunk), and the rebrand removed them. A frame from the reel itself is
// the honest picture: it is what the viewer saw on Instagram. The mp4 files are pruned
// from the deployment once an episode is live, so the still is written next to the site's
// other static images (public/site/, already public in lib/routes.ts) and the list of
// episodes that have one goes into lib/frames.json, which the pages import (a serverless
// function cannot list public/ at request time).
//
// Which frame: three candidates in the opening seconds (where the hook states the
// subject, CLAUDE.md "first second"), and the one with the most detail wins (largest
// encoded size), because the very first frames are often mid-fade.
//
// Run from studio/:  node scripts/make-frames.mjs        (only missing frames)
//                    node scripts/make-frames.mjs --all  (redo every frame)
// Needs ffmpeg with libwebp. Run it when an episode ships, then commit both outputs.
import { execFileSync } from "node:child_process";
import { readdirSync, existsSync, mkdirSync, statSync, writeFileSync, rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";

const REELS = "public/reels";
const OUT = "public/site/frames";
const all = process.argv.includes("--all");
mkdirSync(OUT, { recursive: true });
const tmp = join(tmpdir(), `frames-${process.pid}`);
mkdirSync(tmp, { recursive: true });

for (const f of readdirSync(REELS)) {
  const m = /^reel-(\d+)\.mp4$/.exec(f);
  if (!m) continue;
  const n = Number(m[1]);
  const dest = join(OUT, `${n}.webp`);
  if (!all && existsSync(dest)) continue;
  let best = null;
  for (const t of ["1.6", "2.6", "3.6"]) {
    const p = join(tmp, `${n}-${t}.webp`);
    try {
      execFileSync("ffmpeg", ["-v", "error", "-y", "-ss", t, "-i", join(REELS, f), "-frames:v", "1",
        "-vf", "scale=360:640:force_original_aspect_ratio=increase,crop=360:640",
        "-c:v", "libwebp", "-quality", "62", p]);
      const size = statSync(p).size;
      if (!best || size > best.size) best = { p, size };
    } catch { /* a reel shorter than t: skip that candidate */ }
  }
  if (best) {
    execFileSync("cp", [best.p, dest]);
    console.log(`${n}: ${Math.round(best.size / 1024)} KB`);
  }
}
rmSync(tmp, { recursive: true, force: true });

const have = readdirSync(OUT)
  .map((f) => /^(\d+)\.webp$/.exec(f)?.[1])
  .filter(Boolean)
  .map(Number)
  .sort((a, b) => a - b);
writeFileSync("lib/frames.json", JSON.stringify(have) + "\n");
console.log(`lib/frames.json: ${have.length} frames`);
