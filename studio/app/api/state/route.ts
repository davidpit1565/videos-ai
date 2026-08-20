import { whole } from "@/lib/whole";
import { NextResponse } from "next/server";
import { dbVar, hasDb, loadState, saveState } from "@/lib/db";
import { State } from "@/lib/types";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  if (!hasDb()) {
    // No database yet: the client keeps its own copy in the browser. Saying so
    // explicitly is better than pretending to persist and losing his edits.
    return NextResponse.json({
      mode: "local",
      state: null,
      dbVar: null,
      hint: "אין משתנה סביבה עם כתובת Postgres. אחרי חיבור מסד נתונים צריך פריסה חדשה כדי שהוא ייכנס לתוקף.",
    });
  }
  try {
    // repaired here as well as in the client: a caller that forgets is the bug that
    // took the studio down twice
    const raw = await loadState();
    return NextResponse.json({
      mode: "cloud", state: raw ? whole(raw) : null, dbVar: dbVar(),
    });
  } catch (e) {
    // The variable exists but the connection failed — that is a different problem
    // from having no database, and it deserves a different message.
    return NextResponse.json({
      mode: "local",
      state: null,
      dbVar: dbVar(),
      error: (e as Error).message,
      hint: "נמצאה כתובת מסד נתונים אבל החיבור נכשל. ההודעה למעלה היא מה שהמסד עצמו החזיר.",
    });
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
