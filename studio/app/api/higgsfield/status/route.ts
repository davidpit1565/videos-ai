import { NextResponse } from "next/server";
import { checkJobSet, jobSetPhase, extractVideoUrl } from "@/lib/higgsfield";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 30;

/** One status check per call — the client (the /higgsfield page) polls this every few
 *  seconds itself; this route never sleeps waiting for the job. */
export async function GET(req: Request) {
  const id = new URL(req.url).searchParams.get("id");
  if (!id) return NextResponse.json({ ok: false, error: "חסר id" }, { status: 400 });

  try {
    const data = await checkJobSet(id);
    const phase = jobSetPhase(data);
    const videoUrl = phase === "done" ? extractVideoUrl(data) : null;
    return NextResponse.json({
      ok: true,
      phase,
      videoUrl,
      // Sent back whole even on success — extractVideoUrl() is best-effort (see
      // lib/higgsfield.ts), so if it comes back null on a real "done" job, the raw
      // response is exactly what's needed to find the real field by hand and fix it,
      // instead of guessing at the path a second time.
      raw: data,
    });
  } catch (e) {
    return NextResponse.json({ ok: false, error: (e as Error).message }, { status: 502 });
  }
}
