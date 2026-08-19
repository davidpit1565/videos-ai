import { NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const API = "https://graph.facebook.com/v21.0";

type Media = {
  id: string;
  caption?: string;
  media_type?: string;
  permalink?: string;
  timestamp?: string;
  like_count?: number;
  comments_count?: number;
};

/**
 * Recent media plus per-post insights. Instagram only reports on media created
 * after the account became Professional, so older posts come back empty — that
 * is the API's behaviour, not a gap in this code.
 */
export async function GET() {
  const token = process.env.IG_ACCESS_TOKEN;
  const user = process.env.IG_USER_ID;
  if (!token || !user) {
    return NextResponse.json({
      connected: false,
      reason: !user ? "IG_USER_ID is not set" : "IG_ACCESS_TOKEN is not set",
    });
  }
  try {
    const prof = await fetch(
      `${API}/${user}?fields=username,followers_count,media_count&access_token=${token}`,
      { cache: "no-store" },
    );
    if (!prof.ok) {
      return NextResponse.json({
        connected: false,
        reason: `Instagram returned ${prof.status}`,
        detail: (await prof.text()).slice(0, 300),
      });
    }
    const profile = await prof.json();

    const mr = await fetch(
      `${API}/${user}/media?fields=id,caption,media_type,permalink,timestamp,like_count,comments_count&limit=25&access_token=${token}`,
      { cache: "no-store" },
    );
    const media: Media[] = mr.ok ? ((await mr.json()).data ?? []) : [];

    // Insight names differ by media type; asking for reel metrics on an image 400s,
    // so each request is scoped and a failure degrades to the basic counts.
    const withInsights = await Promise.all(
      media.map(async (m) => {
        const metrics =
          m.media_type === "VIDEO" || m.media_type === "REELS"
            ? "views,reach,saved,shares,total_interactions"
            : "views,reach,saved,total_interactions";
        try {
          const ir = await fetch(
            `${API}/${m.id}/insights?metric=${metrics}&access_token=${token}`,
            { cache: "no-store" },
          );
          const vals: Record<string, number> = {};
          if (ir.ok) {
            const j = (await ir.json()) as { data?: { name: string; values: { value: number }[] }[] };
            for (const d of j.data ?? []) vals[d.name] = d.values?.[0]?.value ?? 0;
          }
          return {
            id: m.id,
            caption: (m.caption ?? "").slice(0, 120),
            permalink: m.permalink ?? null,
            timestamp: m.timestamp ?? null,
            mediaType: m.media_type ?? null,
            views: vals.views ?? null,
            reach: vals.reach ?? null,
            saves: vals.saved ?? null,
            shares: vals.shares ?? null,
            likes: m.like_count ?? null,
            comments: m.comments_count ?? null,
          };
        } catch {
          return {
            id: m.id, caption: (m.caption ?? "").slice(0, 120),
            permalink: m.permalink ?? null, timestamp: m.timestamp ?? null,
            mediaType: m.media_type ?? null,
            views: null, reach: null, saves: null, shares: null,
            likes: m.like_count ?? null, comments: m.comments_count ?? null,
          };
        }
      }),
    );

    return NextResponse.json({
      connected: true,
      username: profile.username ?? null,
      followers: profile.followers_count ?? null,
      mediaCount: profile.media_count ?? null,
      media: withInsights,
      checkedAt: new Date().toISOString(),
    });
  } catch (e) {
    return NextResponse.json({ connected: false, reason: (e as Error).message });
  }
}
