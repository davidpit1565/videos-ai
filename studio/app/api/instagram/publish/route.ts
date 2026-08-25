import { NextResponse } from "next/server";
import { publishToInstagram } from "@/lib/publish";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 90;

/** He presses a real button for this — publishing to a real public account is not
 *  something to trigger silently the first time this code ever runs. */
export async function POST(req: Request) {
  try {
    const { file, caption } = (await req.json()) as { file?: string; caption?: string };
    if (!file) return NextResponse.json({ ok: false, reason: "חסר שם קובץ" }, { status: 400 });
    const r = await publishToInstagram(file, caption ?? "");
    return NextResponse.json(r);
  } catch (e) {
    return NextResponse.json({ ok: false, reason: e instanceof Error ? e.message : String(e) }, { status: 500 });
  }
}
