import { NextResponse } from "next/server";
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** The always-ready backlog of next-episode ideas, read straight from the file in the
 *  repo — the same file-is-the-fact pattern as reels.ts. He asked for a studio agent
 *  that always keeps 5 ideas ahead; the heavy production (voice, render) can't run on
 *  Vercel, but the backlog itself is just text, and text can live here right now. */
export async function GET() {
  const p = join(process.cwd(), "..", "channel", "next-episode-ideas.md");
  if (!existsSync(p)) {
    return NextResponse.json({ ok: false, text: null });
  }
  return NextResponse.json({ ok: true, text: readFileSync(p, "utf8") });
}
