import { NextResponse } from "next/server";
import { submitTalk } from "@/lib/d-id";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 30;

/** Submits one talking-head job and returns immediately with its talk id — the render
 *  itself can run past a serverless function's time limit, so this never waits for it.
 *  The client polls /api/d-id/status?id=... on its own schedule instead. Same shape as
 *  /api/higgsfield/submit. */
export async function POST(req: Request) {
  let body: { sourceUrl?: string; audioUrl?: string };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ ok: false, error: "בקשה לא תקינה" }, { status: 400 });
  }

  const { sourceUrl, audioUrl } = body;
  if (!sourceUrl || !audioUrl) {
    return NextResponse.json(
      { ok: false, error: "חסר sourceUrl / audioUrl — שניהם נדרשים" },
      { status: 400 },
    );
  }

  try {
    const submitted = await submitTalk({ sourceUrl, audioUrl });
    const talkId = submitted.id;
    if (!talkId) {
      return NextResponse.json(
        { ok: false, error: "אין id בתשובת השרת", raw: submitted },
        { status: 502 },
      );
    }
    return NextResponse.json({ ok: true, talkId });
  } catch (e) {
    return NextResponse.json({ ok: false, error: (e as Error).message }, { status: 502 });
  }
}
