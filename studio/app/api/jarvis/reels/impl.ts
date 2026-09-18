import { NextResponse } from "next/server";
import { reels } from "@/lib/reels";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** Lets JARVIS (the personal-assistant project, a separate machine caller with no
 *  browser and no studio PIN cookie) list the rendered reels waiting for publish, the
 *  same data /renders shows him. Classified CRON in lib/routes.ts (bypasses the PIN
 *  middleware, same shape as /api/claude-usage) and checked here by hand against its
 *  own bearer secret — never the studio PIN, which is a browser-only credential JARVIS
 *  has no way to hold. */
function isAuthorized(req: Request): boolean {
  const secret = process.env.JARVIS_STUDIO_SECRET;
  if (!secret) return false;
  return req.headers.get("authorization") === `Bearer ${secret}`;
}

export async function GET(req: Request) {
  if (!isAuthorized(req)) return NextResponse.json({ ok: false, reason: "locked" }, { status: 401 });

  const list = reels().map((r) => ({
    file: r.file,
    kind: r.kind,
    episode: r.episode,
    title: r.title,
    caption: r.caption,
    builtAt: r.builtAt,
    bytes: r.bytes,
    gatePassed: r.gate?.passed ?? null,
  }));

  return NextResponse.json({ ok: true, reels: list });
}
