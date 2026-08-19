import { NextResponse, type NextRequest } from "next/server";

/** The studio holds the whole business. Its URL is unguessable but not private, so when
 *  STUDIO_PIN is set every private page needs the PIN once per device. The public funnel
 *  pages stay open — they are the point. */
const PUBLIC = ["/join", "/p/", "/unlock", "/api/unlock", "/manifest.json", "/icon-", "/apple-touch-icon"];

export function middleware(req: NextRequest) {
  const pin = process.env.STUDIO_PIN;
  if (!pin) return NextResponse.next();

  const { pathname } = req.nextUrl;
  if (PUBLIC.some((p) => pathname.startsWith(p))) return NextResponse.next();
  // the cron calls the tracker with its own credential, not with a browser cookie
  if (pathname === "/api/track") return NextResponse.next();

  if (req.cookies.get("studio")?.value === pin) return NextResponse.next();

  const url = req.nextUrl.clone();
  url.pathname = "/unlock";
  url.search = pathname === "/" ? "" : `?to=${encodeURIComponent(pathname)}`;
  return NextResponse.redirect(url);
}

export const config = { matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"] };
