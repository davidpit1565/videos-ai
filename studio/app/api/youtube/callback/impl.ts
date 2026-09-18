import { NextResponse } from "next/server";
import { exchangeYoutubeCode } from "@/lib/publish";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** Where Google sends him back after he grants access. A plain page instead of a JSON
 *  blob because a human, on a phone, just clicked a consent screen and needs to see in
 *  Hebrew that it worked — not read a JSON object. */
function page(title: string, body: string) {
  return new NextResponse(
    `<!doctype html><html lang="he" dir="rtl"><meta charset="utf-8">
     <body style="font-family:system-ui;padding:40px;text-align:center">
     <h1>${title}</h1><p>${body}</p></body></html>`,
    { headers: { "content-type": "text/html; charset=utf-8" } },
  );
}

export async function GET(req: Request) {
  const url = new URL(req.url);
  const code = url.searchParams.get("code");
  const error = url.searchParams.get("error");
  if (error) return page("החיבור בוטל", error);
  if (!code) return page("שגיאה", "לא התקבל קוד מ-Google");
  const r = await exchangeYoutubeCode(code);
  if (!r.ok) return page("החיבור נכשל", r.reason);
  return page("YouTube מחובר ✓", "אפשר לסגור את הדף הזה ולחזור לסטודיו.");
}
