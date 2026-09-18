import { NextResponse } from "next/server";
import { resolveHealthFinding, unresolveHealthFinding } from "@/lib/db";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST(req: Request) {
  const { id, undo } = (await req.json()) as { id?: string; undo?: boolean };
  if (!id) return NextResponse.json({ ok: false, reason: "חסר id" }, { status: 400 });
  if (undo) await unresolveHealthFinding(id);
  else await resolveHealthFinding(id);
  return NextResponse.json({ ok: true });
}
