import { NextResponse } from "next/server";
import { publishEpisode } from "@/lib/publish";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 120;

/** JARVIS's own path to the exact same publish action the studio's own button
 *  triggers (see app/api/instagram/publish/impl.ts). Classified CRON in lib/routes.ts
 *  (bypasses the PIN middleware) and checked here by hand against its own bearer
 *  secret, the same shape as /api/jarvis/reels. This is a real, irreversible public
 *  post — JARVIS is expected to have already confirmed with him before calling this,
 *  the same way the studio's own button confirm()s first; this endpoint itself does
 *  not ask again.
 *
 *  Rebuilt 23.9.2026 to go through `publishEpisode` (lib/publish.ts), by episode
 *  number rather than a bare file+caption — this route used to call
 *  publishToInstagram directly with none of the gate/caption/idempotency checks the
 *  other two publish routes had, and no state update of its own at all. It was the
 *  third independent copy of "publish and hope /api/track sorts out the state later,"
 *  which is the exact pattern behind the episode-45 double-publish incident. */
function isAuthorized(req: Request): boolean {
  const secret = process.env.JARVIS_STUDIO_SECRET;
  if (!secret) return false;
  return req.headers.get("authorization") === `Bearer ${secret}`;
}

export async function POST(req: Request) {
  if (!isAuthorized(req)) return NextResponse.json({ ok: false, reason: "locked" }, { status: 401 });

  try {
    const { episode } = (await req.json()) as { episode?: number };
    if (!episode) return NextResponse.json({ ok: false, reason: "חסר מספר פרק" }, { status: 400 });
    const result = await publishEpisode(episode);
    if (!result.ok) return NextResponse.json(result, { status: 400 });
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
