import { NextResponse } from "next/server";
import { hashPin } from "@/lib/pin";
import { publishToYoutube, youtubeConnected } from "@/lib/publish";
import { hasDb, loadState, saveState } from "@/lib/db";
import { SITE_URL } from "@/lib/site";
import { fetchYouTube } from "@/lib/sources";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 300;

/** Uploads the live reels that are not on YouTube yet, oldest first, one after another, until the
 *  daily quota says stop (David, 1.11.2026: "as many as possible, in order, and automate the rest").
 *
 *  Runs from Vercel's cron once a day (right after YouTube's quota resets) and by hand with the PIN
 *  cookie: GET /api/yt-backfill?max=6, or ?dry=1 to only list what would go.
 *
 *  The mp4 and the title/description text come from the public GitHub repo, because the deployment
 *  prunes old reels (prune-old-reels) and the site copy of an old reel is a 404. The title is the first
 *  line of channel/episode-NN-youtube.txt and the rest is the description, the same split the studio's
 *  own publish button uses.
 *
 *  Safety: only episodes the studio records as live without a ytVideoId, never the SKIP list, and the
 *  video id is written to the state right after each upload, so a second run can not post it twice. */
const RAW = "https://raw.githubusercontent.com/davidpit1565/videos-ai/main";
/** Episode 2 looks missing in the new database, but the old one had it linked to YouTube. Not guessed
 *  at: David checks the channel first. */
const SKIP = new Set<number>([2]);
const pad = (n: number) => String(n).padStart(2, "0");
const norm = (t: string) => t.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim().slice(0, 60);

async function allowed(req: Request): Promise<boolean> {
  const secret = process.env.CRON_SECRET;
  const auth = req.headers.get("authorization");
  if (req.headers.get("x-vercel-cron") || (secret && auth === `Bearer ${secret}`)) return true;
  const pin = process.env.STUDIO_PIN;
  if (!pin) return false;
  const cookieHash = req.headers
    .get("cookie")
    ?.split(";")
    .map((c) => c.trim())
    .find((c) => c.startsWith("studio="))
    ?.slice("studio=".length);
  return cookieHash === (await hashPin(pin));
}

async function fetchOk(url: string): Promise<Response | null> {
  try {
    const r = await fetch(url, { cache: "no-store" });
    return r.ok ? r : null;
  } catch {
    return null;
  }
}

export async function GET(req: Request) {
  if (!(await allowed(req))) return NextResponse.json({ ok: false, reason: "locked" }, { status: 401 });
  if (!hasDb()) return NextResponse.json({ ok: false, reason: "no database" });

  const url = new URL(req.url);
  const max = Math.max(1, Math.min(12, Number(url.searchParams.get("max")) || 6));
  const dry = url.searchParams.get("dry") === "1";
  const only = Number(url.searchParams.get("episode")) || null;

  if (!(await youtubeConnected())) {
    return NextResponse.json({ ok: false, reason: "YouTube is not connected: open /api/youtube/auth once" });
  }
  const first = await loadState();
  if (!first) return NextResponse.json({ ok: false, reason: "no state" });

  const queue = first.episodes
    .filter((e) => e.status === "live" && !e.ytVideoId && !SKIP.has(e.number) && (!only || e.number === only))
    .map((e) => e.number)
    .sort((a, b) => a - b);
  if (dry) return NextResponse.json({ ok: true, dry: true, count: queue.length, queue });

  const started = Date.now();
  const uploaded: { episode: number; videoId: string }[] = [];
  let stopped: string | null = null;

  // David, 1.11.2026: look at what is really on the channel first, and never upload what is already there.
  // Matched by title (first line of the episode's youtube.txt); a match is recorded in the state and skipped.
  const onChannel = new Map<string, string>();
  const yt = await fetchYouTube();
  if (yt.connected) for (const v of yt.videos) onChannel.set(norm(v.title), v.id);
  const alreadyThere: { episode: number; videoId: string }[] = [];

  for (const n of queue) {
    if (uploaded.length >= max) break;
    if (Date.now() - started > 230_000) {
      stopped = "time budget used, the next run continues";
      break;
    }
    const txt = await fetchOk(`${RAW}/channel/episode-${pad(n)}-youtube.txt`);
    if (!txt) {
      stopped = `episode ${n}: no youtube.txt in the repo`;
      break;
    }
    const lines = (await txt.text()).split("\n");
    const title = (lines[0] ?? "").trim();
    const description = lines.slice(1).join("\n").trim();
    if (!title) {
      stopped = `episode ${n}: empty title`;
      break;
    }
    const existing = onChannel.get(norm(title));
    if (existing) {
      alreadyThere.push({ episode: n, videoId: existing });
      for (let attempt = 0; attempt < 3; attempt++) {
        const st = await loadState();
        if (!st) break;
        const ep = st.episodes.find((e) => e.number === n);
        if (ep) ep.ytVideoId = existing;
        const saved = await saveState(st, (st as { updatedAt?: string | null }).updatedAt ?? null);
        if (saved.ok) break;
      }
      continue;
    }
    const mp4 = (await fetchOk(`${RAW}/studio/public/reels/reel-${pad(n)}.mp4`)) ?? (await fetchOk(`${SITE_URL}/reels/reel-${pad(n)}.mp4`));
    if (!mp4) {
      stopped = `episode ${n}: reel-${pad(n)}.mp4 not found`;
      break;
    }
    const r = await publishToYoutube(Buffer.from(await mp4.arrayBuffer()), title, description);
    if (!r.ok) {
      stopped = `episode ${n}: ${r.reason}`;
      break;
    }
    uploaded.push({ episode: n, videoId: r.videoId });
    // Record it immediately, on a fresh copy of the state (the studio writes to it too).
    for (let attempt = 0; attempt < 3; attempt++) {
      const s = await loadState();
      if (!s) break;
      const ep = s.episodes.find((e) => e.number === n);
      if (ep) ep.ytVideoId = r.videoId;
      s.lastYoutubeUploadAt = new Date().toISOString();
      const saved = await saveState(s, (s as { updatedAt?: string | null }).updatedAt ?? null);
      if (saved.ok) break;
    }
  }

  const left = queue.length - uploaded.length;
  return NextResponse.json({ ok: true, uploaded, alreadyThere, stopped, remaining: left - alreadyThere.length });
}
