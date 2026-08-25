import { NextResponse } from "next/server";
import { publishToInstagram, publishToFacebook, SITE_URL } from "@/lib/publish";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 120;

/** He presses a real button for this — publishing to a real public account is not
 *  something to trigger silently the first time this code ever runs. One click now
 *  does three independent publishes (Reel, Story, Facebook Page) — each reported on
 *  its own, since one can genuinely succeed while another fails or isn't configured. */
export async function POST(req: Request) {
  try {
    const { file, caption } = (await req.json()) as { file?: string; caption?: string };
    if (!file) return NextResponse.json({ ok: false, reason: "חסר שם קובץ" }, { status: 400 });
    const ig = await publishToInstagram(file, caption ?? "");
    // Facebook only if the Reel itself actually went out — no point cross-posting a
    // Reel that doesn't exist, and it needs its own credentials regardless.
    const facebook = ig.reel.ok ? await publishToFacebook(file, caption ?? "") : null;
    // A publish that lands on the account and nowhere in the studio's own list looks
    // broken even though it worked — the pull that links a post to its episode
    // (/api/track) otherwise only runs on the nightly cron or a manual pull-to-refresh.
    // Instagram's own post-processing takes a few seconds after publish_id returns, so
    // this fetch races that — a miss here just waits for the next cron/pull, same as
    // before this existed.
    if (ig.reel.ok && process.env.CRON_SECRET) {
      void fetch(`${SITE_URL}/api/track`, {
        headers: { authorization: `Bearer ${process.env.CRON_SECRET}` },
      }).catch(() => {});
    }
    return NextResponse.json({ ...ig, facebook });
  } catch (e) {
    return NextResponse.json({ ok: false, reason: e instanceof Error ? e.message : String(e) }, { status: 500 });
  }
}
