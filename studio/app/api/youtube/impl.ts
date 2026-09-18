import { NextResponse } from "next/server";
import { fetchYouTube } from "@/lib/sources";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  return NextResponse.json(await fetchYouTube());
}
