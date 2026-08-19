import { NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** Subscriber count from Beehiiv. The publication id is public; the key is not. */
export async function GET() {
  const key = process.env.BEEHIIV_API_KEY;
  // The publication id is public, so it ships as a default — only the key is a secret.
  const pub = process.env.BEEHIIV_PUBLICATION_ID || "pub_92556dc6-6f7e-42ab-a414-6e291c61557c";
  if (!key || !pub) {
    return NextResponse.json({
      connected: false,
      reason: !pub ? "BEEHIIV_PUBLICATION_ID is not set" : "BEEHIIV_API_KEY is not set",
    });
  }
  try {
    // limit=1 keeps the payload small — we only want the total from the meta block
    const r = await fetch(
      `https://api.beehiiv.com/v2/publications/${pub}/subscriptions?limit=1&status=active`,
      { headers: { Authorization: `Bearer ${key}` }, cache: "no-store" },
    );
    if (!r.ok) {
      const body = await r.text();
      return NextResponse.json({
        connected: false,
        reason: `Beehiiv returned ${r.status}`,
        detail: body.slice(0, 300),
      });
    }
    const j = (await r.json()) as { total_results?: number; data?: unknown[] };
    return NextResponse.json({
      connected: true,
      activeSubscribers: j.total_results ?? null,
      checkedAt: new Date().toISOString(),
    });
  } catch (e) {
    return NextResponse.json({ connected: false, reason: (e as Error).message });
  }
}
