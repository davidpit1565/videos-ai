import { NextResponse } from "next/server";
import { hasDb } from "@/lib/db";
import { checkConnections } from "@/lib/health";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** Hourly, lightweight — two read-only API calls, no state diff, no snapshot write. Catches a
 *  connection dying between /api/track's once-a-day runs (access-control-gating: same guard as
 *  /api/track, since this reveals connection-failure detail and should not be publicly
 *  triggerable). */
export async function GET(req: Request) {
  const secret = process.env.CRON_SECRET;
  const auth = req.headers.get("authorization");
  const fromCron = Boolean(req.headers.get("x-vercel-cron")) || (secret && auth === `Bearer ${secret}`);
  if (!fromCron) return NextResponse.json({ error: "locked" }, { status: 401 });

  if (!hasDb()) {
    return NextResponse.json({ ok: false, reason: "אין מסד נתונים — אין איפה לשמור מצב קודם" });
  }

  const status = await checkConnections();
  return NextResponse.json({ ok: true, ...status, checkedAt: new Date().toISOString() });
}
