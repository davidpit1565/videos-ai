import { NextResponse } from "next/server";
import { addSub, deviceCount, publicKey } from "@/lib/push";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** GET hands the browser the public key it needs to subscribe. POST stores the result. */
export async function GET() {
  const key = await publicKey();
  if (!key) {
    return NextResponse.json(
      { ok: false, error: "no database, so there is nowhere to keep the subscription" },
      { status: 503 },
    );
  }
  return NextResponse.json({ ok: true, key, devices: await deviceCount() });
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
      b.label ?? "device",
    );
    return NextResponse.json({ ok: true, devices: await deviceCount() });
  } catch (e) {
    return NextResponse.json(
      { ok: false, error: e instanceof Error ? e.message : String(e) },
      { status: 500 },
    );
  }
}
