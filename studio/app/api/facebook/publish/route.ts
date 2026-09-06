import { NextResponse } from "next/server";
import { publishToFacebook } from "@/lib/publish";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 60;

/** A standalone retry for the Facebook Page post, independent of Instagram. The combined
 *  "ריל + פייסבוק" button only attempts Facebook right after a fresh Reel publish, so a
 *  Reel that already went out (episodes 21 and 22 both did) has no way back to Facebook
 *  without this — clicking the combined button again would re-publish a second, duplicate
 *  Reel just to retry the one platform that actually failed. This calls publishToFacebook
 *  on its own, on a file that's already live, so the real Facebook-side reason (missing
 *  credentials, an expired Page token, a Graph API error) surfaces without touching
 *  Instagram at all. */
export async function POST(req: Request) {
  try {
    const { file, caption } = (await req.json()) as { file?: string; caption?: string };
    if (!file) return NextResponse.json({ ok: false, reason: "חסר שם קובץ" }, { status: 400 });
    const facebook = await publishToFacebook(file, caption ?? "");
    return NextResponse.json({ facebook });
  } catch (e) {
    return NextResponse.json({ ok: false, reason: e instanceof Error ? e.message : String(e) }, { status: 500 });
  }
}
