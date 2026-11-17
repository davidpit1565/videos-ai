import { NextResponse, type NextRequest } from "next/server";
import { isCron, isSite, isStudio } from "@/lib/routes";
import { hashPin } from "@/lib/pin";

/** The studio holds the whole business. Its URL is unguessable but not private, so when
 *  STUDIO_PIN is set every private page needs the PIN once per device. The public funnel
 *  pages stay open — they are the point.
 *
 *  Which pages those are is decided in lib/routes.ts and nowhere else. The list used to
 *  live here as well as in app/shell.tsx, the two drifted, and /prompts and /search ended
 *  up public but wearing the studio's chrome. */

export async function middleware(req: NextRequest) {
  const pin = process.env.STUDIO_PIN;
  if (!pin) return NextResponse.next();

  const { pathname } = req.nextUrl;
  if (isSite(pathname) || isCron(pathname)) return NextResponse.next();

  const cookie = req.cookies.get("studio")?.value;
  if (cookie && cookie === (await hashPin(pin))) return NextResponse.next();

  // A gated API answers with JSON and a status, never with a login page. Redirecting
  // /api/state to /unlock made every caller's r.json() throw on HTML, and the catch
  // that swallowed it dropped the studio to stale local data without saying so.
  if (pathname.startsWith("/api/")) {
    return NextResponse.json({ error: "locked" }, { status: 401 });
  }

  // A page address no list claims (a typo, an old link to the removed /prompts or
  // /skills pages) is not the studio: an English-speaking visitor from a reel used to land
  // on the Hebrew PIN screen for it. It now gets the English 404 page (app/not-found.tsx).
  // Rewritten to a path that has no route, NOT passed through: passing it through would
  // serve any unlisted file in public/ to anyone, which the PIN gate used to stop.
  // Real studio pages, and every API path above, are gated exactly as before.
  if (!isStudio(pathname)) {
    const missing = req.nextUrl.clone();
    missing.pathname = "/__not-found";
    missing.search = "";
    return NextResponse.rewrite(missing);
  }

  const url = req.nextUrl.clone();
  url.pathname = "/unlock";
  url.search = `?to=${encodeURIComponent(pathname)}`;
  return NextResponse.redirect(url);
}

export const config = { matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"] };
