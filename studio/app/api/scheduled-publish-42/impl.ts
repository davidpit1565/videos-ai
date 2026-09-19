import { NextResponse } from "next/server";
import { publishToInstagram, publishToFacebookBoth, SITE_URL } from "@/lib/publish";
import { loadState } from "@/lib/db";
import { reelByFile } from "@/lib/reels";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 120;

/** One-off: David asked (19.9.2026) for episode 42 to publish itself Monday 11:00 Israel
 *  time (21.9.2026, 08:00 UTC), since Monday is Yom Kippur and he won't touch his phone.
 *
 *  Triggered by a real Vercel cron entry in vercel.json, scheduled for that exact date —
 *  same trust model /api/track and /api/health-check already use (fromCron check below),
 *  not a hand-typed secret pasted into this session (CLAUDE.md: secrets live only in
 *  Vercel env vars). Vercel's cron network is the only caller that can set
 *  x-vercel-cron; anything else needs CRON_SECRET, exactly like the two routes above.
 *
 *  Does exactly what the studio's own Instagram publish button does for reel-42.mp4
 *  (see publish-buttons.tsx / instagram/publish/impl.ts) — Reel, then Facebook (profile
 *  and Page) if the Reel went out. Idempotent (a no-op once episode 42 already has an
 *  igMediaId) so a second cron tick, or this route surviving past Monday, never risks a
 *  duplicate post. Remove the vercel.json cron entry (and this route) once it's shipped —
 *  it's a one-off, not a recurring job. */
export async function GET(req: Request) {
  const secret = process.env.CRON_SECRET;
  const auth = req.headers.get("authorization");
  const fromCron = Boolean(req.headers.get("x-vercel-cron")) || (secret && auth === `Bearer ${secret}`);
  if (!fromCron) return NextResponse.json({ ok: false, reason: "locked" }, { status: 401 });

  try {
    const state = await loadState();
    const already = state?.episodes.find((e) => e.number === 42)?.igMediaId;
    if (already) {
      return NextResponse.json({ ok: true, skipped: true, reason: "episode 42 already has an igMediaId" });
    }

    const file = "reel-42.mp4";
    const reel = reelByFile(file);
    if (!reel) return NextResponse.json({ ok: false, reason: `${file} not found` }, { status: 404 });
    if (!reel.caption?.trim()) return NextResponse.json({ ok: false, reason: "no caption file for episode 42" }, { status: 400 });

    const ig = await publishToInstagram(file, reel.caption);
    const fb = ig.reel.ok ? await publishToFacebookBoth(file, reel.caption) : null;

    if (ig.reel.ok && process.env.CRON_SECRET) {
      await fetch(`${SITE_URL}/api/track`, {
        headers: { authorization: `Bearer ${process.env.CRON_SECRET}` },
      }).catch(() => {});
    }

    return NextResponse.json({ ...ig, facebook: fb?.profile ?? null, facebookPage: fb?.page ?? null });
  } catch (e) {
    return NextResponse.json({ ok: false, reason: e instanceof Error ? e.message : String(e) }, { status: 500 });
  }
}
