import { NextResponse } from "next/server";
import { getUsage, setCurrent, setWeekly } from "@/lib/claudeUsage";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** No separate secret guards the POST, on purpose, and the reason is the shape of the data
 *  rather than laziness. Everything here is a coding-assistant cost figure and a rate-limit
 *  status — nothing that identifies him, nothing that spends money if read, nothing that acts
 *  on his behalf. The write path is a single row (id=1), so the worst a stray POST can do is
 *  show a wrong number in one dashboard card until the next real update overwrites it — the
 *  same trade this codebase already made for /api/track. That is not the trade this project
 *  makes for the Instagram token or the Beehiiv key, and it should not be. */

export async function GET() {
  const u = await getUsage();
  return NextResponse.json(u ?? { weekly: null, current: null, reason: "no database" });
}

export async function POST(req: Request) {
  try {
    const b = await req.json();
    if (b.type === "weekly") {
      await setWeekly(String(b.status), String(b.resetsAt), !!b.isUsingOverage);
    } else if (b.type === "current") {
      await setCurrent(
        Number(b.costUsd), Number(b.inputTokens), Number(b.outputTokens),
        Number(b.cacheReadTokens), Number(b.cacheWriteTokens),
      );
    } else {
      return NextResponse.json({ ok: false, error: "type must be weekly or current" }, { status: 422 });
    }
    return NextResponse.json({ ok: true });
  } catch (e) {
    return NextResponse.json(
      { ok: false, error: e instanceof Error ? e.message : String(e) },
      { status: 500 },
    );
  }
}
