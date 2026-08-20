import { NextResponse, type NextRequest } from "next/server";

/** The studio holds the whole business. Its URL is unguessable but not private, so when
 *  STUDIO_PIN is set every private page needs the PIN once per device. The public funnel
 *  pages stay open — they are the point. */
const PUBLIC = ["/join", "/p/", "/unlock", "/api/unlock", "/manifest.json", "/icon-",
                "/apple-touch-icon", "/e/", "/about", "/api/site"];
/** matched exactly: startsWith("/") would open the whole studio */
const PUBLIC_EXACT = ["/"];

export function middleware(req: NextRequest) {
  const pin = process.env.STUDIO_PIN;
  if (!pin) return NextResponse.next();

  const { pathname } = req.nextUrl;
  if (PUBLIC_EXACT.includes(pathname) || PUBLIC.some((p) => pathname.startsWith(p)))
    return NextResponse.next();
  // the cron calls the tracker with its own credential, not with a browser cookie
  if (pathname === "/api/track") return NextResponse.next();

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
