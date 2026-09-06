import { NextResponse } from "next/server";
import { checkTalk, talkPhase, extractVideoUrl } from "@/lib/d-id";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 30;

/** One status check per call — the client (the /d-id page) polls this every few seconds
 *  itself; this route never sleeps waiting for the job. Same shape as
 *  /api/higgsfield/status. */
export async function GET(req: Request) {
  const id = new URL(req.url).searchParams.get("id");
  if (!id) return NextResponse.json({ ok: false, error: "חסר id" }, { status: 400 });

  try {
    const data = await checkTalk(id);
    const phase = talkPhase(data);
    const videoUrl = phase === "done" ? extractVideoUrl(data) : null;
    return NextResponse.json({ ok: true, phase, videoUrl, raw: data });
  } catch (e) {
    return NextResponse.json({ ok: false, error: (e as Error).message }, { status: 502 });
  }
}
