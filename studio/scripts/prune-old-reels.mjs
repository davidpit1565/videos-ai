/** Keeps only the newest reels in the DEPLOYED copy of public/reels/ (the build machine's
 *  checkout), never in the repo. Every deployment used to carry all ~60 videos (~390 MB);
 *  Vercel's Deployment Storage hit 17 GB against a 10 GB limit. The videos stay in git.
 *
 *  Only runs on a build server (VERCEL / NETLIFY / CI) so a local `next dev` never deletes
 *  anything. Runs after write-reels-manifest.mjs, so the list of reels stays complete; an
 *  old reel's page still lists it, its video file just isn't served from the deployment.
 *  Publishing only ever uses a recent reel, so KEEP covers it with room to spare. */
import { readdirSync, statSync, readFileSync, existsSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const KEEP = Number(process.env.KEEP_REELS || 6);
if (!(process.env.VERCEL || process.env.NETLIFY || process.env.CI)) {
  console.log("prune-old-reels: not a build server, leaving public/reels alone");
  process.exit(0);
}
const DIR = join(fileURLToPath(new URL("..", import.meta.url)), "public", "reels");
const when = (f) => {
  const p = join(DIR, f.replace(/\.mp4$/, ".built-at.txt"));
  try {
    if (existsSync(p)) return readFileSync(p, "utf8").trim();
  } catch {}
  return statSync(join(DIR, f)).mtime.toISOString();
};
const videos = readdirSync(DIR).filter((f) => f.endsWith(".mp4")).map((f) => ({ f, t: when(f) }));
videos.sort((a, b) => b.t.localeCompare(a.t));
const drop = videos.slice(KEEP);
for (const { f } of drop) rmSync(join(DIR, f));
// Tell the app which videos are no longer in this deployment, so a reel page shows a plain
// "archived" note instead of a black player with a crossed-out play button (8.10.2026).
const MANIFEST = join(fileURLToPath(new URL("..", import.meta.url)), "lib", "reels-manifest.json");
try {
  const gone = new Set(drop.map((d) => d.f));
  const m = JSON.parse(readFileSync(MANIFEST, "utf8"));
  for (const r of m.reels) r.archived = gone.has(r.file) ? true : undefined;
  writeFileSync(MANIFEST, JSON.stringify(m));
} catch (e) {
  console.log("prune-old-reels: could not mark archived reels in the manifest:", e.message);
}
console.log(`prune-old-reels: kept ${Math.min(KEEP, videos.length)}, removed ${drop.length}`);
