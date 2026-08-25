import { NextResponse } from "next/server";
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { publishToYoutube } from "@/lib/publish";

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
    const p = join(process.cwd(), "public", "reels", file);
    if (!existsSync(p)) return NextResponse.json({ ok: false, reason: "הקובץ לא נמצא" }, { status: 404 });
    const bytes = readFileSync(p);
    const r = await publishToYoutube(bytes, title, description ?? "");
    return NextResponse.json(r);
  } catch (e) {
    return NextResponse.json({ ok: false, reason: e instanceof Error ? e.message : String(e) }, { status: 500 });
  }
}
