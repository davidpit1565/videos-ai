import { NextResponse } from "next/server";
import { SITE_URL } from "@/lib/site";
import { publishToYoutube } from "@/lib/publish";
import { loadState, saveState } from "@/lib/db";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 90;

export async function POST(req: Request) {
  try {
    const { file, title, description } = (await req.json()) as {
      file?: string; title?: string; description?: string;
    };
    if (!file || !title) {
      return NextResponse.json({ ok: false, reason: "חסר קובץ או כותרת" }, { status: 400 });
    }
    // Only ever the reel filename, never a path — this reads straight off disk with no
    // sanitization beyond that, so a caller could otherwise walk out of the reels folder.
    if (file.includes("/") || file.includes("..")) {
      return NextResponse.json({ ok: false, reason: "שם קובץ לא חוקי" }, { status: 400 });
    }
    // Fetched from the site's own /reels/ folder instead of read off the function's disk:
    // reading it from disk made every function carry every video (see lib/reels.ts).
    const res = await fetch(`${SITE_URL}/reels/${encodeURIComponent(file)}`);
    if (!res.ok) return NextResponse.json({ ok: false, reason: "הקובץ לא נמצא" }, { status: 404 });
    const bytes = Buffer.from(await res.arrayBuffer());
    const r = await publishToYoutube(bytes, title, description ?? "");
    // Best-effort — a real upload that just succeeded should never be reported as failed
    // because this bookkeeping write hiccuped.
    if (r.ok) {
      try {
        const s = await loadState();
        if (s) await saveState({ ...s, lastYoutubeUploadAt: new Date().toISOString() });
      } catch {
        /* the upload itself is what matters; this is just the next warning's memory */
      }
    }
    return NextResponse.json(r);
  } catch (e) {
    return NextResponse.json({ ok: false, reason: e instanceof Error ? e.message : String(e) }, { status: 500 });
  }
}
