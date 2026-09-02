import { NextResponse } from "next/server";
import { youtubeConnected } from "@/lib/publish";
import { loadState } from "@/lib/db";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** Same calendar day, in his timezone — not a rolling 24h window, since we don't know
 *  YouTube's own window and a same-day check is the honest approximation. */
function sameBrusselsDay(aIso: string, bIso: string): boolean {
  const fmt = new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Brussels" });
  return fmt.format(new Date(aIso)) === fmt.format(new Date(bIso));
}

export async function GET() {
  const s = await loadState().catch(() => null);
  const lastYoutubeUploadAt = s?.lastYoutubeUploadAt ?? null;
  const uploadedToday = !!lastYoutubeUploadAt && sameBrusselsDay(lastYoutubeUploadAt, new Date().toISOString());
  return NextResponse.json({ connected: await youtubeConnected(), lastYoutubeUploadAt, uploadedToday });
}
