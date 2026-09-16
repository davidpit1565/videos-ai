import { NextResponse } from "next/server";
import { publishToFacebookBoth, publishToFacebookBusinessPage } from "@/lib/publish";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 60;

/** A standalone retry for the Facebook post(s), independent of Instagram. The combined
 *  "ריל + פייסבוק" button only attempts Facebook right after a fresh Reel publish, so a
 *  Reel that already went out (episodes 21 and 22 both did) has no way back to Facebook
 *  without this — clicking the combined button again would re-publish a second, duplicate
 *  Reel just to retry the platform that actually failed.
 *
 *  Publishes via publishToFacebookBoth by default (see its own comment in lib/publish.ts):
 *  FB_PAGE_ID and FB_BUSINESS_PAGE_ID turned out to be the same Facebook Page (confirmed
 *  16.9.2026 — there's exactly one Page, "Actually works.ai"; a separate "personal
 *  profile" destination never existed), so that function now posts once and mirrors the
 *  result into both `facebook`/`facebookPage` fields below instead of genuinely
 *  double-posting the same video to the same Page.
 *
 *  `target: "page"` restricts this to a single explicit call to the business Page —
 *  added 15.9.2026 to backfill episodes 2-34 without relying on the (at the time,
 *  broken) default path. Every new episode from here on uses the default. */
export async function POST(req: Request) {
  try {
    const { file, caption, target } = (await req.json()) as {
      file?: string;
      caption?: string;
      target?: "both" | "page";
    };
    if (!file) return NextResponse.json({ ok: false, reason: "חסר שם קובץ" }, { status: 400 });
    if (target === "page") {
      const page = await publishToFacebookBusinessPage(file, caption ?? "");
      return NextResponse.json({ facebook: null, facebookPage: page });
    }
    const { profile, page } = await publishToFacebookBoth(file, caption ?? "");
    return NextResponse.json({ facebook: profile, facebookPage: page });
  } catch (e) {
    return NextResponse.json({ ok: false, reason: e instanceof Error ? e.message : String(e) }, { status: 500 });
  }
}
