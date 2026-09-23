import { NextResponse } from "next/server";
import { publishEpisode } from "@/lib/publish";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 120;

/** He presses a real button for this — publishing to a real public account is not
 *  something to trigger silently the first time this code ever runs. One click does
 *  two independent publishes (Reel, Facebook Page) — each reported on its own, since
 *  one can genuinely succeed while another fails or isn't configured. The Story used
 *  to be a third automatic publish here; see the comment on publishToInstagram in
 *  lib/publish.ts for why that's gone — he shares the Reel to his Story by hand now,
 *  since Instagram's own "Share to Story" makes the version the API physically cannot.
 *
 *  Rebuilt 23.9.2026 to go through `publishEpisode` (lib/publish.ts) — the same
 *  gate-passed/caption/idempotency checks and state update the daily cron already used,
 *  now shared instead of duplicated. Before this, this route took a bare `{file,
 *  caption}` with no gate check, no idempotency check, and no state update of its own —
 *  a stray or repeated call (a manual test against this endpoint, a double-click, a
 *  retry) republished the same episode with no guard against it, which is exactly what
 *  happened to episode 45 minutes after the legitimate cron had already published it. */
export async function POST(req: Request) {
  try {
    const { episode } = (await req.json()) as { episode?: number };
    if (!episode) return NextResponse.json({ ok: false, reason: "חסר מספר פרק" }, { status: 400 });
    const result = await publishEpisode(episode);
    if (!result.ok) return NextResponse.json(result, { status: 400 });
    // Same response shape the frontend (renders/[file]/publish-buttons.tsx) already
    // expects: {reel, story, facebook, facebookPage}. `story` stays null — see the
    // comment above on why the API-made Story publish was dropped.
    if (result.alreadyPublished) {
      return NextResponse.json({
        reel: { ok: true, mediaId: null, permalink: result.igPermalink },
        story: null,
        facebook: null,
        facebookPage: null,
        alreadyPublished: true,
      });
    }
    return NextResponse.json({
      reel: result.reel,
      story: null,
      facebook: result.facebook,
      facebookPage: result.facebookPage,
    });
  } catch (e) {
    return NextResponse.json({ ok: false, reason: e instanceof Error ? e.message : String(e) }, { status: 500 });
  }
}
