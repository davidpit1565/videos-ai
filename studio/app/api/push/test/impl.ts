import { NextResponse } from "next/server";
import { notify } from "@/lib/push";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** A notification he asked for and can see arrive. Exists because "it is set up" is not the
 *  same claim as "one reached this device", and only the second one is worth anything. */
export async function POST() {
  const r = await notify({
    title: "Actually Works",
    body: "Notifications work on this device.",
    url: "/studio",
    tag: "test",
  });
  return NextResponse.json({ ok: r.sent > 0, ...r });
}
