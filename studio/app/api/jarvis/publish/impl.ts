import { NextResponse } from "next/server";
import { publishToInstagram, publishToFacebookBoth, SITE_URL } from "@/lib/publish";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 120;

/** JARVIS's own path to the exact same publish action the studio's own button
 *  triggers (see app/api/instagram/publish/impl.ts, which this deliberately mirrors
 *  rather than modifies — the browser-triggered button keeps its own PIN-gated path
 *  unchanged). Classified CRON in lib/routes.ts (bypasses the PIN middleware) and
 *  checked here by hand against its own bearer secret, the same shape as
 *  /api/jarvis/reels. This is a real, irreversible public post — JARVIS is expected
 *  to have already confirmed with him before calling this, the same way the studio's
 *  own button confirm()s first; this endpoint itself does not ask again. */
function isAuthorized(req: Request): boolean {
  const secret = process.env.JARVIS_STUDIO_SECRET;
  if (!secret) return false;
  return req.headers.get("authorization") === `Bearer ${secret}`;
}

export async function POST(req: Request) {
  if (!isAuthorized(req)) return NextResponse.json({ ok: false, reason: "locked" }, { status: 401 });

  try {
    const { file, caption } = (await req.json()) as { file?: string; caption?: string };
    if (!file) return NextResponse.json({ ok: false, reason: "חסר שם קובץ" }, { status: 400 });

    const ig = await publishToInstagram(file, caption ?? "");
    const fb = ig.reel.ok ? await publishToFacebookBoth(file, caption ?? "") : null;
    const facebook = fb?.profile ?? null;
    const facebookPage = fb?.page ?? null;

    if (ig.reel.ok && process.env.CRON_SECRET) {
      await fetch(`${SITE_URL}/api/track`, {
        headers: { authorization: `Bearer ${process.env.CRON_SECRET}` },
      }).catch(() => {});
    }

    return NextResponse.json({ ...ig, facebook, facebookPage });
  } catch (e) {
    return NextResponse.json({ ok: false, reason: e instanceof Error ? e.message : String(e) }, { status: 500 });
  }
}
