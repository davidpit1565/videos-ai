import { NextResponse } from "next/server";
import { publishToInstagram, publishToFacebook } from "@/lib/publish";

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
    return NextResponse.json({ ...ig, facebook });
  } catch (e) {
    return NextResponse.json({ ok: false, reason: e instanceof Error ? e.message : String(e) }, { status: 500 });
  }
}
