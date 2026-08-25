import { NextResponse } from "next/server";
import { addSub, deviceCount, publicKey } from "@/lib/push";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** Same shape as /api/push/subscribe (the studio's own device registration), deliberately
 *  a separate route at a separate path rather than a shared one with a flag — a visitor
 *  calling this can never end up on the studio's own audience by accident, whatever a
 *  client sends, and it can never collide with /api/push's STUDIO classification in
 *  lib/routes.ts either. See lib/push.ts on why the two audiences must never share a send. */
export async function GET() {
  const key = await publicKey();
  if (!key) {
    return NextResponse.json({ ok: false, error: "no database" }, { status: 503 });
  }
  return NextResponse.json({ ok: true, key, devices: await deviceCount("public") });
}

export async function POST(req: Request) {
  try {
    const b = (await req.json()) as {
      sub?: { endpoint?: string; keys?: { p256dh?: string; auth?: string } };
      label?: string;
    };
    const s = b.sub;
    if (!s?.endpoint || !s.keys?.p256dh || !s.keys.auth) {
      return NextResponse.json({ ok: false, error: "incomplete subscription" }, { status: 422 });
    }
    await addSub(
      { endpoint: s.endpoint, keys: { p256dh: s.keys.p256dh, auth: s.keys.auth } },
      b.label ?? "visitor",
      "public",
    );
    return NextResponse.json({ ok: true, devices: await deviceCount("public") });
  } catch (e) {
    return NextResponse.json(
      { ok: false, error: e instanceof Error ? e.message : String(e) },
      { status: 500 },
    );
  }
}
