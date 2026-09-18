import { NextResponse } from "next/server";

/** A client-side crash is invisible from here: the server logs stay clean and the
 *  browser shows Next's generic "Application error", which names nothing. Twice now
 *  that has cost a round of guessing. The error boundary posts the real message here,
 *  console.error puts it in the runtime logs, and the cause is readable without
 *  anyone having to open a browser console. */
export async function POST(req: Request) {
  let body: unknown = null;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ ok: false }, { status: 400 });
  }
  const b = (body ?? {}) as { message?: string; stack?: string; digest?: string; path?: string };
  console.error(
    "[client-crash]",
    JSON.stringify({
      path: String(b.path ?? "").slice(0, 200),
      digest: String(b.digest ?? "").slice(0, 80),
      message: String(b.message ?? "").slice(0, 500),
      stack: String(b.stack ?? "").slice(0, 2000),
    }),
  );
  return NextResponse.json({ ok: true });
}
