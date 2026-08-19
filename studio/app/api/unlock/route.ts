import { NextResponse } from "next/server";

export const runtime = "nodejs";

export async function POST(req: Request) {
  const pin = process.env.STUDIO_PIN;
  if (!pin) return NextResponse.json({ ok: true });   // nothing to unlock
  const body = await req.json().catch(() => ({}));
  if (String(body.pin ?? "") !== pin) {
    return NextResponse.json({ ok: false }, { status: 401 });
  }
  const res = NextResponse.json({ ok: true });
  res.cookies.set("studio", pin, {
    httpOnly: true,
    sameSite: "lax",
    secure: true,
    path: "/",
    maxAge: 60 * 60 * 24 * 120,
  });
  return res;
}
