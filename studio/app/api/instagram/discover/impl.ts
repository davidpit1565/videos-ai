import { NextResponse } from "next/server";
import { igToken, igRoute } from "@/lib/sources";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** Reads public Business/Creator accounts through Instagram's official Business Discovery
 *  field, using the token the studio already holds. Read-only, named accounts only, at most
 *  10 per call. Behind the studio PIN (/api/instagram is a STUDIO prefix). Whether an
 *  Instagram-Login token (IGAA…) is allowed to use business_discovery is NOT known: that is
 *  what this route finds out, and an API refusal comes back verbatim per account (never the
 *  token) so the answer is visible instead of guessed. */
const FIELDS =
  "username,name,followers_count,media_count," +
  "media.limit(12){caption,like_count,comments_count,media_type,permalink,timestamp}";

export async function GET(req: Request) {
  const names = (new URL(req.url).searchParams.get("u") ?? "")
    .split(",")
    .map((s) => s.trim().replace(/^@/, "").toLowerCase())
    .filter((s) => /^[a-z0-9._]{1,30}$/.test(s))
    .slice(0, 10);
  if (!names.length) {
    return NextResponse.json({ ok: false, reason: "use ?u=name1,name2 (max 10)" }, { status: 400 });
  }
  const token = await igToken();
  if (!token) return NextResponse.json({ ok: false, reason: "IG_ACCESS_TOKEN not set" }, { status: 503 });
  const { host, via } = igRoute(token);
  const me = via === "instagram-login" ? "me" : (process.env.IG_USER_ID ?? "");
  if (!me) return NextResponse.json({ ok: false, reason: "IG_USER_ID not set", via }, { status: 503 });

  const results = [];
  for (const u of names) {
    try {
      const url =
        `${host}/${me}?fields=${encodeURIComponent(`business_discovery.username(${u}){${FIELDS}}`)}` +
        `&access_token=${token}`;
      const r = await fetch(url, { cache: "no-store" });
      const j = await r.json();
      if (!r.ok || j.error) {
        const msg = String(j?.error?.message ?? r.status).split(token).join("[token]").slice(0, 300);
        results.push({ username: u, ok: false, status: r.status, code: j?.error?.code ?? null, error: msg });
      } else {
        results.push({ username: u, ok: true, data: j.business_discovery });
      }
    } catch (e) {
      results.push({ username: u, ok: false, error: (e as Error).message.split(token).join("[token]") });
    }
  }
  return NextResponse.json({ ok: true, via, results });
}
