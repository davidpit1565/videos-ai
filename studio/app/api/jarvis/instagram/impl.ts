import { NextResponse } from "next/server";
import { fetchInstagram } from "@/lib/sources";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** Lets JARVIS read the account's real stats — followers, per-post views/reach/
 *  saves/shares/likes/comments — the same data /api/instagram already returns to
 *  the browser, gated the same way as /api/jarvis/reels. */
function isAuthorized(req: Request): boolean {
  const secret = process.env.JARVIS_STUDIO_SECRET;
  if (!secret) return false;
  return req.headers.get("authorization") === `Bearer ${secret}`;
}

export async function GET(req: Request) {
  if (!isAuthorized(req)) return NextResponse.json({ ok: false, reason: "locked" }, { status: 401 });
  const result = await fetchInstagram();
  return NextResponse.json(result);
}
