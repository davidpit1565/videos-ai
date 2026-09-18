import { NextResponse } from "next/server";
import { hasDb, listClaudeSessions, upsertClaudeSession } from "@/lib/db";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** Ingests per-session Claude Code usage from the Stop hooks running on his own machine
 *  (~/.claude/hooks/cost-tracker.js) — this app has no other way to see them, they never
 *  touch a browser. Classified CRON in lib/routes.ts (bypasses the PIN middleware, same as
 *  /api/track), so both callers are checked here by hand: the hook's own secret, or the
 *  studio's own PIN cookie for the page's GET. */
function callerKind(req: Request): "hook" | "studio" | null {
  const secret = process.env.CLAUDE_USAGE_SECRET;
  const auth = req.headers.get("authorization");
  if (secret && auth === `Bearer ${secret}`) return "hook";
  const pin = process.env.STUDIO_PIN;
  if (pin) {
    const cookiePin = req.headers
      .get("cookie")
      ?.split(";")
      .map((c) => c.trim())
      .find((c) => c.startsWith("studio="))
      ?.slice("studio=".length);
    if (cookiePin === pin) return "studio";
  }
  return null;
}

export async function POST(req: Request) {
  if (!callerKind(req)) return NextResponse.json({ ok: false, reason: "locked" }, { status: 401 });
  if (!hasDb()) return NextResponse.json({ ok: false, reason: "no database configured" });

  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ ok: false, reason: "bad request body" }, { status: 400 });
  }

  const sessionId = String(body.sessionId ?? "").slice(0, 128);
  if (!sessionId) {
    return NextResponse.json({ ok: false, reason: "sessionId is required" }, { status: 400 });
  }
  const num = (v: unknown) => (Number.isFinite(Number(v)) ? Number(v) : 0);

  try {
    await upsertClaudeSession({
      sessionId,
      project: body.project ? String(body.project).slice(0, 200) : null,
      model: body.model ? String(body.model).slice(0, 100) : null,
      inputTokens: num(body.inputTokens),
      outputTokens: num(body.outputTokens),
      cacheWriteTokens: num(body.cacheWriteTokens),
      cacheReadTokens: num(body.cacheReadTokens),
      estimatedCostUsd: num(body.estimatedCostUsd),
      turns: num(body.turns),
      ageMinutes: num(body.ageMinutes),
    });
  } catch (e) {
    return NextResponse.json({ ok: false, reason: (e as Error).message }, { status: 500 });
  }
  return NextResponse.json({ ok: true });
}

export async function GET(req: Request) {
  if (!callerKind(req)) return NextResponse.json({ ok: false, reason: "locked" }, { status: 401 });
  if (!hasDb()) return NextResponse.json({ ok: true, sessions: [] });
  const sessions = await listClaudeSessions();
  return NextResponse.json({ ok: true, sessions });
}
