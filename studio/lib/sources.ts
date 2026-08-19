/** One place that talks to Instagram and Beehiiv, so the pages, the API routes and the
 *  nightly tracker all see exactly the same numbers. */

const IG = "https://graph.facebook.com/v21.0";

export type IgMedia = {
  id: string;
  caption: string;
  permalink: string | null;
  timestamp: string | null;
  mediaType: string | null;
  views: number | null;
  reach: number | null;
  saves: number | null;
  shares: number | null;
  likes: number | null;
  comments: number | null;
};

export type IgResult =
  | { connected: false; reason: string; detail?: string }
  | {
      connected: true;
      username: string | null;
      followers: number | null;
      mediaCount: number | null;
      media: IgMedia[];
      checkedAt: string;
    };

export type BeeResult =
  | { connected: false; reason: string; detail?: string }
  | { connected: true; activeSubscribers: number | null; checkedAt: string };

export async function fetchInstagram(): Promise<IgResult> {
  const token = process.env.IG_ACCESS_TOKEN;
  const user = process.env.IG_USER_ID;
  if (!token || !user) {
    return {
      connected: false,
      reason: !user ? "IG_USER_ID לא מוגדר" : "IG_ACCESS_TOKEN לא מוגדר",
    };
  }
  try {
    const prof = await fetch(
      `${IG}/${user}?fields=username,followers_count,media_count&access_token=${token}`,
      { cache: "no-store" },
    );
    if (!prof.ok) {
      return {
        connected: false,
        reason: `אינסטגרם החזיר ${prof.status}`,
        detail: (await prof.text()).slice(0, 300),
      };
    }
    const profile = await prof.json();

    const mr = await fetch(
      `${IG}/${user}/media?fields=id,caption,media_type,permalink,timestamp,like_count,comments_count&limit=25&access_token=${token}`,
      { cache: "no-store" },
    );
    const raw: {
      id: string; caption?: string; media_type?: string; permalink?: string;
      timestamp?: string; like_count?: number; comments_count?: number;
    }[] = mr.ok ? ((await mr.json()).data ?? []) : [];

    // Insight names differ by media type; asking for reel metrics on an image 400s,
    // so each request is scoped and a failure degrades to the basic counts.
    const media = await Promise.all(
      raw.map(async (m): Promise<IgMedia> => {
        const base: IgMedia = {
          id: m.id,
          caption: (m.caption ?? "").slice(0, 120),
          permalink: m.permalink ?? null,
          timestamp: m.timestamp ?? null,
          mediaType: m.media_type ?? null,
          views: null, reach: null, saves: null, shares: null,
          likes: m.like_count ?? null,
          comments: m.comments_count ?? null,
        };
        const metrics =
          m.media_type === "VIDEO" || m.media_type === "REELS"
            ? "views,reach,saved,shares,total_interactions"
            : "views,reach,saved,total_interactions";
        try {
          const ir = await fetch(`${IG}/${m.id}/insights?metric=${metrics}&access_token=${token}`, {
            cache: "no-store",
          });
          if (!ir.ok) return base;
          const j = (await ir.json()) as { data?: { name: string; values: { value: number }[] }[] };
          const v: Record<string, number> = {};
          for (const d of j.data ?? []) v[d.name] = d.values?.[0]?.value ?? 0;
          return {
            ...base,
            views: v.views ?? null,
            reach: v.reach ?? null,
            saves: v.saved ?? null,
            shares: v.shares ?? null,
          };
        } catch {
          return base;
        }
      }),
    );

    return {
      connected: true,
      username: profile.username ?? null,
      followers: profile.followers_count ?? null,
      mediaCount: profile.media_count ?? null,
      media,
      checkedAt: new Date().toISOString(),
    };
  } catch (e) {
    return { connected: false, reason: (e as Error).message };
  }
}

export async function fetchBeehiiv(): Promise<BeeResult> {
  const key = process.env.BEEHIIV_API_KEY;
  // The publication id is public, so it ships as a default — only the key is a secret.
  const pub = process.env.BEEHIIV_PUBLICATION_ID || "pub_92556dc6-6f7e-42ab-a414-6e291c61557c";
  if (!key) return { connected: false, reason: "BEEHIIV_API_KEY לא מוגדר" };
  try {
    // limit=1 keeps the payload small — only the total from the meta block is wanted
    const r = await fetch(
      `https://api.beehiiv.com/v2/publications/${pub}/subscriptions?limit=1&status=active`,
      { headers: { Authorization: `Bearer ${key}` }, cache: "no-store" },
    );
    if (!r.ok) {
      return {
        connected: false,
        reason: `Beehiiv החזיר ${r.status}`,
        detail: (await r.text()).slice(0, 300),
      };
    }
    const j = (await r.json()) as { total_results?: number };
    return {
      connected: true,
      activeSubscribers: j.total_results ?? null,
      checkedAt: new Date().toISOString(),
    };
  } catch (e) {
    return { connected: false, reason: (e as Error).message };
  }
}
