import { NextResponse } from "next/server";
import { publishEpisode } from "@/lib/publish";
import { loadState } from "@/lib/db";

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
 *  (Vercel's own x-vercel-cron header, or CRON_SECRET for anything else).
 *
 *  Rebuilt 23.9.2026 to go through the same `publishEpisode` (lib/publish.ts) the manual
 *  button now uses, instead of its own separate copy of the gate/caption checks and its
 *  own separate, thinner state update (this route used to only ever clear
 *  `queuedForPublish` — never `status`, `igMediaId`, or `igPermalink` — leaving the studio
 *  to reconstruct those later, best-effort, from /api/track matching post text against
 *  captions). Two copies of "publish and update state" had already drifted enough that a
 *  manual test against the other route republished an episode this one had already
 *  correctly published minutes earlier, with no idempotency check catching it either
 *  side. One function, one set of guards, used by both callers now. */
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

    const result = await publishEpisode(ep.number);
    if (!result.ok) return NextResponse.json({ episode: ep.number, ...result }, { status: 400 });
    if (result.alreadyPublished) {
      return NextResponse.json({ episode: ep.number, ok: true, alreadyPublished: true, igPermalink: result.igPermalink });
    }
    return NextResponse.json({
      episode: ep.number,
      reel: result.reel,
      facebook: result.facebook,
      facebookPage: result.facebookPage,
    });
  } catch (e) {
    return NextResponse.json({ ok: false, reason: e instanceof Error ? e.message : String(e) }, { status: 500 });
  }
}
