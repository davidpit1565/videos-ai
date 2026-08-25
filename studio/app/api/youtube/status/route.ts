import { NextResponse } from "next/server";
import { youtubeConnected } from "@/lib/publish";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  return NextResponse.json({ connected: await youtubeConnected() });
}
