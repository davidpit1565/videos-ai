import { NextResponse } from "next/server";
import { youtubeAuthUrl } from "@/lib/publish";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** The one link he has to click, once, from whichever device is logged into the
 *  channel's Google account — everything after this is automatic. */
export async function GET() {
  const r = youtubeAuthUrl();
  if (!r.ok) return NextResponse.json(r, { status: 400 });
  return NextResponse.redirect(r.url);
}
