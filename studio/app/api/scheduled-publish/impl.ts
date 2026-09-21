import { NextResponse } from "next/server";
import { publishToInstagram, publishToFacebookBoth, SITE_URL } from "@/lib/publish";
import { loadState, saveState } from "@/lib/db";
import { reels } from "@/lib/reels";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 120;

/** The general, repeatable version of the one-off `/api/scheduled-publish-42` (built
 *  19.9.2026 for a single Yom Kippur publish, since removed). David asked (21.9.2026) for
 *  a real fix, not a one-off, after two measured problems in `channel/content-memory.md`
 *  (21.9.2026 entries): same-day double-posting measurably hurts the second post (6 of 8
 *  historical pairs), and posting time has never been consistent (six real timestamps
 *  spanning 04:20-23:57 UTC). A single daily cron, at one fixed hour, structurally fixes
 *  both at once — at most one auto-publish a day, always at the same time.
 *
 *  The fixed hour lives in vercel.json as a UTC cron string, set for Belgium time (his
 *  actual home timezone — David corrected an initial Israel-time assumption on 21.9.2026).
 *  Vercel cron schedules are fixed UTC and do not follow DST: 17:00 UTC is 19:00 Belgium
 *  time while Belgium is on CEST (UTC+2, through late October), but becomes 18:00 local
 *  once Belgium falls back to CET (UTC+1). The schedule needs a manual one-hour bump at
 *  each DST transition to keep the real local hour at 19:00 — nothing here does that
 *  automatically.
 *
 *  Never picks an episode on its own: a human still has to mark it `tested` (the normal
 *  pipeline gate) AND tick "queue for auto-publish" in the studio (`queuedForPublish`) —
 *  this route only decides *when* to press the button that's already been approved, never
 *  *whether* to. Guarded the same way /api/track and /api/health-check already are
 *  (Vercel's own x-vercel-cron header, or CRON_SECRET for anything else). */
export async function GET(req: Request) {
  const secret = process.env.CRON_SECRET;
  const auth = req.headers.get("authorization");
  const fromCron = Boolean(req.headers.get("x-vercel-cron")) || (secret && auth === `Bearer ${secret}`);
  if (!fromCron) return NextResponse.json({ ok: false, reason: "locked" }, { status: 401 });

  try {
    const state = await loadState();
    if (!state) return NextResponse.json({ ok: true, skipped: true, reason: "no state" });

    const queued = state.episodes
      .filter((e) => e.status === "testing" && e.queuedForPublish)
      .sort((a, b) => a.number - b.number);
    const ep = queued[0];
    if (!ep) return NextResponse.json({ ok: true, skipped: true, reason: "nothing queued" });

    const reel = reels().find((r) => r.kind === "video" && r.episode === ep.number && r.gate?.passed);
    if (!reel) {
      return NextResponse.json(
        { ok: false, reason: `episode ${ep.number} is queued but has no gate-passed render` },
        { status: 404 },
      );
    }
    if (!reel.caption?.trim()) {
      return NextResponse.json({ ok: false, reason: `episode ${ep.number} has no caption file` }, { status: 400 });
    }

    const ig = await publishToInstagram(reel.file, reel.caption);
    const fb = ig.reel.ok ? await publishToFacebookBoth(reel.file, reel.caption) : null;

    // Clear the flag regardless of outcome: a failed attempt should surface (the
    // caller can check /videos and its own activity feed) and get a fresh look, not
    // silently retry every day at the same hour with the same result.
    const row = state.episodes.find((e) => e.id === ep.id);
    if (row) row.queuedForPublish = false;
    await saveState(state);

    if (ig.reel.ok && process.env.CRON_SECRET) {
      await fetch(`${SITE_URL}/api/track`, {
        headers: { authorization: `Bearer ${process.env.CRON_SECRET}` },
      }).catch(() => {});
    }

    return NextResponse.json({ episode: ep.number, ...ig, facebook: fb?.profile ?? null, facebookPage: fb?.page ?? null });
  } catch (e) {
    return NextResponse.json({ ok: false, reason: e instanceof Error ? e.message : String(e) }, { status: 500 });
  }
}
