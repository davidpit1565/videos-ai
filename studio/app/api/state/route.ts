import { NextResponse } from "next/server";
import { hasDb, loadState, saveState } from "@/lib/db";
import { State } from "@/lib/types";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  if (!hasDb()) {
    // No database yet: the client keeps its own copy in the browser. Saying so
    // explicitly is better than pretending to persist and losing his edits.
    return NextResponse.json({ mode: "local", state: null });
  }
  try {
    return NextResponse.json({ mode: "cloud", state: await loadState() });
  } catch (e) {
    return NextResponse.json(
      { mode: "local", state: null, error: (e as Error).message },
      { status: 200 },
    );
  }
}

export async function PUT(req: Request) {
  if (!hasDb()) return NextResponse.json({ ok: false, mode: "local" });
  try {
    const body = (await req.json()) as State;
    if (!body || body.version !== 1) {
      return NextResponse.json({ ok: false, error: "unrecognised state shape" }, { status: 400 });
    }
    await saveState(body);
    return NextResponse.json({ ok: true, mode: "cloud" });
  } catch (e) {
    return NextResponse.json({ ok: false, error: (e as Error).message }, { status: 500 });
  }
}
