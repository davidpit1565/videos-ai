import { NextResponse } from "next/server";
import { scanTodos } from "@/lib/repoHealth";
import { getResolvedHealthIds } from "@/lib/db";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** Real TODO/FIXME markers, evidence-first — see lib/health.ts for why this scans text
 *  instead of shelling out to git (no live .git in this deployment). A finding already
 *  marked resolved never comes back just because its source text is still there. */
export async function GET() {
  const [findings, resolved] = await Promise.all([scanTodos(), getResolvedHealthIds()]);
  const open = findings.filter((f) => !resolved.has(f.id));
  const resolvedCount = findings.length - open.length;
  return NextResponse.json({ findings: open, resolvedCount, scannedAt: new Date().toISOString() });
}
