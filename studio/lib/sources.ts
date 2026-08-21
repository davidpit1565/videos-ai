/** One place that talks to Instagram and Beehiiv, so the pages, the API routes and the
 *  nightly tracker all see exactly the same numbers. */

/** Meta has two different Instagram APIs and they do not accept each other's tokens.
 *  A token minted by "Generate token" inside Instagram's own API setup (Instagram Login)
 *  is an IGAA…/IGQ… token for graph.instagram.com; sending it to graph.facebook.com comes
 *  back as "Invalid OAuth access token - Cannot parse access token", which reads like a
 *  broken paste and is not one. So the host follows the token instead of being assumed,
 *  and the Instagram-Login path resolves the account as `me` — no IG_USER_ID needed. */
const FB_HOST = "https://graph.facebook.com/v21.0";
const IG_HOST = "https://graph.instagram.com/v21.0";

export type IgLogin = "instagram-login" | "facebook-login";

export function igRoute(token: string): { host: string; via: IgLogin } {
  return /^IG[QA]/.test(token)
    ? { host: IG_HOST, via: "instagram-login" }
    : { host: FB_HOST, via: "facebook-login" };
}

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
  | { connected: false; reason: string; detail?: string; via?: IgLogin }
  | {
      connected: true;
      via: IgLogin;
      username: string | null;
      followers: number | null;
      mediaCount: number | null;
      media: IgMedia[];
      checkedAt: string;
    };

export type BeeResult =
  | { connected: false; reason: string; detail?: string }
  | {
      connected: true;
      activeSubscribers: number | null;
      /** false when the list ran past one page, so the count above is a floor and not the
       *  number. A floor presented as a number is a made-up number. */
      exact: boolean;
      /** the response's top-level key names — not values — so a count that comes back null
       *  can be diagnosed without the key ever leaving Vercel */
      shape: string[];
      checkedAt: string;
    };

export async function fetchInstagram(): Promise<IgResult> {
  const token = process.env.IG_ACCESS_TOKEN;
  if (!token) return { connected: false, reason: "IG_ACCESS_TOKEN לא מוגדר" };

  const { host, via } = igRoute(token);
  // Instagram Login identifies the account from the token itself; only the Facebook-Page
  // route needs the numeric id, and there it is genuinely required.
  const user = process.env.IG_USER_ID || (via === "instagram-login" ? "me" : "");
  if (!user) return { connected: false, reason: "IG_USER_ID לא מוגדר", via };

  const IG = host;
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
        via,
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
      via,
      username: profile.username ?? null,
      followers: profile.followers_count ?? null,
      mediaCount: profile.media_count ?? null,
      media,
      checkedAt: new Date().toISOString(),
    };
  } catch (e) {
    return { connected: false, reason: (e as Error).message, via };
  }
}

/** The publication id is public, so it ships as a default — only the key is a secret. It
 *  lives here and is imported, because /api/subscribe had its own copy of this line WITHOUT
 *  the default: with the environment variable unset it answered "beehiiv not configured" and
 *  every signup was stored by us and never forwarded, while the dashboard showed Beehiiv
 *  connected. */
export const BEEHIIV_PUB =
  process.env.BEEHIIV_PUBLICATION_ID || "pub_92556dc6-6f7e-42ab-a414-6e291c61557c";

export async function fetchBeehiiv(): Promise<BeeResult> {
  const key = process.env.BEEHIIV_API_KEY;
  const pub = BEEHIIV_PUB;
  if (!key) return { connected: false, reason: "BEEHIIV_API_KEY לא מוגדר" };
  try {
    // There is no total to read. The diagnostic reported the response's keys as
    // ["data","has_more","limit","next_cursor"] — cursor pagination, no count anywhere — so
    // the count has to come from the rows themselves. One page of 100 is the exact number
    // while the list is under 100, and has_more says so rather than leaving it assumed.
    // Deliberately not following the cursor: the parameter name for it is not something I
    // have seen in a real response, and a guessed parameter that silently returns page one
    // forever would report a wrong number as a certain one.
    const r = await fetch(
      `https://api.beehiiv.com/v2/publications/${pub}/subscriptions?limit=100&status=active`,
      { headers: { Authorization: `Bearer ${key}` }, cache: "no-store" },
    );
    if (!r.ok) {
      return {
        connected: false,
        reason: `Beehiiv החזיר ${r.status}`,
        detail: (await r.text()).slice(0, 300),
      };
    }
    const j = (await r.json()) as {
      data?: unknown[];
      has_more?: boolean;
      // kept in the type because older publications may still answer with a total
      total_results?: number;
      meta?: { total_results?: number; total?: number };
    };
    const total = j.total_results ?? j.meta?.total_results ?? j.meta?.total ?? null;
    const rows = Array.isArray(j.data) ? j.data.length : null;
    return {
      connected: true,
      activeSubscribers: total ?? rows,
      // a total is exact by definition; a page count is exact only if there is no next page
      exact: total !== null ? true : rows !== null && j.has_more !== true,
      shape: Object.keys(j).sort(),
      checkedAt: new Date().toISOString(),
    };
  } catch (e) {
    return { connected: false, reason: (e as Error).message };
  }
}
