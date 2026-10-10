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

/** Which episodes are already published ("live") in the studio's database. David asked (10.10.2026)
 *  that every reel still waiting to be published stays in the studio, and that a published one is
 *  dropped from the deployment to free the quota. The status lives in Supabase (studio_state), so it
 *  is read here at build time. Any failure (no connection string, no network) returns null and the
 *  old rule applies: keep the newest KEEP videos. A publish only frees space on the NEXT deploy. */
async function liveEpisodes() {
  const url = ["DATABASE_URL", "POSTGRES_URL", "POSTGRES_URL_NON_POOLING", "POSTGRES_PRISMA_URL", "SUPABASE_DB_URL"]
    .map((n) => process.env[n]).find((v) => v && v.startsWith("postgres"));
  if (!url) return null;
  let client;
  try {
    const { default: pg } = await import("pg");
    const u = new URL(url);
    u.searchParams.delete("sslmode");
    client = new pg.Client({ connectionString: u.toString(), ssl: { rejectUnauthorized: false }, connectionTimeoutMillis: 8000 });
    await client.connect();
    const r = await client.query("select data->'episodes' as eps from studio_state limit 1");
    const eps = r.rows[0]?.eps;
    if (!Array.isArray(eps)) return null;
    return new Set(eps.filter((e) => e && e.status === "live").map((e) => Number(e.number)));
  } catch (e) {
    console.log("prune-old-reels: could not read published episodes:", e.message);
    return null;
  } finally {
    try { await client?.end(); } catch {}
  }
}
const live = await liveEpisodes();
const epOf = (f) => { const m = f.match(/(\d+)/); return m ? Number(m[1]) : null; };
const MAX_WAITING = Number(process.env.KEEP_UNPUBLISHED || 14);
let drop;
if (live && live.size > 0) {
  const waiting = videos.filter((v) => !live.has(epOf(v.f)));
  const keepSet = new Set(waiting.slice(0, MAX_WAITING).map((v) => v.f));
  drop = videos.filter((v) => !keepSet.has(v.f));
  console.log(`prune-old-reels: ${live.size} published episodes read from the database, keeping ${keepSet.size} unpublished`);
} else {
  drop = videos.slice(KEEP);
}
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
console.log(`prune-old-reels: kept ${videos.length - drop.length}, removed ${drop.length}`);
