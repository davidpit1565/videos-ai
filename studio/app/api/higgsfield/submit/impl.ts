import { NextResponse } from "next/server";
import { submitTalkingHead, type HiggsfieldDuration, type HiggsfieldQuality } from "@/lib/higgsfield";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 30;

/** Submits one talking-head job and returns immediately with its job-set id — the render
 *  itself can run well past a serverless function's time limit, so this never waits for
 *  it. The client polls /api/higgsfield/status?id=... on its own schedule instead. */
export async function POST(req: Request) {
  let body: {
    imageUrl?: string;
    audioUrl?: string;
    prompt?: string;
    quality?: HiggsfieldQuality;
    duration?: HiggsfieldDuration;
  };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ ok: false, error: "בקשה לא תקינה" }, { status: 400 });
  }

  const { imageUrl, audioUrl, prompt } = body;
  if (!imageUrl || !audioUrl || !prompt) {
    return NextResponse.json(
      { ok: false, error: "חסר imageUrl / audioUrl / prompt — שלושתם נדרשים" },
      { status: 400 },
    );
  }

  try {
    const submitted = await submitTalkingHead({
      imageUrl,
      audioUrl,
      prompt,
      quality: body.quality,
      duration: body.duration,
    });
    const jobSetId = submitted.id;
    if (!jobSetId) {
      return NextResponse.json(
        { ok: false, error: "אין job id בתשובת השרת", raw: submitted },
        { status: 502 },
      );
    }
    return NextResponse.json({ ok: true, jobSetId });
  } catch (e) {
    return NextResponse.json({ ok: false, error: (e as Error).message }, { status: 502 });
  }
}
