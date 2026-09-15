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
 *  Publishes to both real Facebook destinations by default (see publishToFacebookBoth's
 *  own comment in lib/publish.ts): the personal profile, where the real audience and view
 *  history live, and the separate "Actually works.ai" business Page, the only destination
 *  Meta's Graph API can ever read view/follower numbers back from. One failing never hides
 *  or blocks the other — they're unrelated credentials and unrelated audiences, reported
 *  separately below.
 *
 *  `target: "page"` restricts this to the business Page only — added 15.9.2026 to
 *  backfill episodes 2-33 onto the Page without touching the personal profile a second
 *  time (those episodes already went to the personal profile when they first shipped).
 *  Every new episode from here on uses the default (both), same as always. */
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
