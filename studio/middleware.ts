import { NextResponse, type NextRequest } from "next/server";
import { isCron, isSite } from "@/lib/routes";

/** The studio holds the whole business. Its URL is unguessable but not private, so when
 *  STUDIO_PIN is set every private page needs the PIN once per device. The public funnel
 *  pages stay open — they are the point.
 *
 *  Which pages those are is decided in lib/routes.ts and nowhere else. The list used to
 *  live here as well as in app/shell.tsx, the two drifted, and /prompts and /search ended
 *  up public but wearing the studio's chrome. */

export function middleware(req: NextRequest) {
  const pin = process.env.STUDIO_PIN;
  if (!pin) return NextResponse.next();

  const { pathname } = req.nextUrl;
  if (isSite(pathname) || isCron(pathname)) return NextResponse.next();

  if (req.cookies.get("studio")?.value === pin) return NextResponse.next();

  // A gated API answers with JSON and a status, never with a login page. Redirecting
  // /api/state to /unlock made every caller's r.json() throw on HTML, and the catch
  // that swallowed it dropped the studio to stale local data without saying so.
  if (pathname.startsWith("/api/")) {
    return NextResponse.json({ error: "locked" }, { status: 401 });
  }

  const url = req.nextUrl.clone();
  url.pathname = "/unlock";
  url.search = `?to=${encodeURIComponent(pathname)}`;
  return NextResponse.redirect(url);
}

export const config = { matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"] };
