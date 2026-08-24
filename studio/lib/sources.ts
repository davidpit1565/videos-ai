/** One place that talks to Instagram and Beehiiv, so the pages, the API routes and the
 *  nightly tracker all see exactly the same numbers. */

import { sharedPool } from "./db";

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
      canPublish: boolean;
      publishReason: string | null;
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


/** Keep the Instagram token alive without him touching it.
 *
 *  An Instagram-Login long-lived token lasts 60 days and has to be refreshed before it dies.
 *  Nothing was refreshing it, so the connection was always going to break on a timer — and it
 *  did, twice, and both times the repair was manual. The daily tracker calls this; a token
 *  refreshed every day is never within 59 days of expiring.
 *
 *  It cannot fix every failure. Today's is `API access blocked`, which is Meta disabling the
 *  app rather than the token expiring, and no refresh reaches that. This removes the failure
 *  that WOULD have recurred on its own, and the notification tells him about the rest the day
 *  it happens instead of whenever he next looks.
 *
 *  The refreshed value cannot be written back into the environment variable from here — Vercel
 *  env vars are not writable at runtime — so it is stored in the database and preferred over
 *  the variable when present. That also means the variable stays the value he pasted, and a
 *  refresh never silently diverges from what /api/connections reports. */
export async function refreshInstagramToken(): Promise<
  { ok: true; expiresInDays: number } | { ok: false; reason: string }
> {
  const token = await igToken();
  if (!token) return { ok: false, reason: "IG_ACCESS_TOKEN לא מוגדר" };
  if (!/^IG[QA]/.test(token)) {
    // the Facebook-Page route has a different mechanism and a different lifetime
    return { ok: false, reason: "טוקן מסוג פייסבוק — לא נדרש רענון כאן" };
  }
  try {
    const r = await fetch(
      `${IG_HOST}/refresh_access_token?grant_type=ig_refresh_token&access_token=${token}`,
      { cache: "no-store" },
    );
    const j = (await r.json()) as { access_token?: string; expires_in?: number; error?: { message?: string } };
    if (!r.ok || !j.access_token) {
      return { ok: false, reason: j.error?.message ?? `אינסטגרם החזיר ${r.status}` };
    }
    await storeIgToken(j.access_token);
    return { ok: true, expiresInDays: Math.round((j.expires_in ?? 0) / 86400) };
  } catch (e) {
    return { ok: false, reason: (e as Error).message };
  }
}

/** the refreshed token if one has been stored, otherwise the one he pasted */
export async function igToken(): Promise<string | null> {
  const p = sharedPool();
  if (p) {
    try {
      await p.query(`create table if not exists ig_token (
        id int primary key default 1, token text not null,
        refreshed_at timestamptz not null default now())`);
      const r = await p.query<{ token: string }>("select token from ig_token where id = 1");
      if (r.rows[0]?.token) return r.rows[0].token;
    } catch {
      /* fall through to the environment — a database problem must not break the read path */
    }
  }
  return process.env.IG_ACCESS_TOKEN ?? null;
}

async function storeIgToken(token: string): Promise<void> {
  const p = sharedPool();
  if (!p) return;
  await p.query(
    `insert into ig_token (id, token) values (1, $1)
     on conflict (id) do update set token = $1, refreshed_at = now()`,
    [token],
  );
}

/** Whether the token can actually publish, not just read — the two are separate Meta
 *  permissions (`instagram_basic` vs `instagram_business_content_publish`), and a token
 *  can be genuinely "connected" for stats while unable to post anything. Reading
 *  `content_publishing_limit` is the standard non-destructive way to find out: it is a
 *  GET, it changes nothing, and Meta rejects it specifically when the publish permission
 *  is missing rather than for any other reason a normal read would fail. */
async function checkPublishAccess(
  host: string, user: string, token: string,
): Promise<{ canPublish: boolean; reason: string | null }> {
  try {
    const r = await fetch(
      `${host}/${user}/content_publishing_limit?fields=config,quota_usage&access_token=${token}`,
      { cache: "no-store" },
    );
    if (r.ok) return { canPublish: true, reason: null };
    const body = await r.text();
    return { canPublish: false, reason: body.slice(0, 300) };
  } catch (e) {
    return { canPublish: false, reason: (e as Error).message };
  }
}

export async function fetchInstagram(): Promise<IgResult> {
  const token = await igToken();
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

    const publish = await checkPublishAccess(IG, user, token);

    return {
      connected: true,
      via,
      canPublish: publish.canPublish,
      publishReason: publish.reason,
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

/** YouTube Data API v3. Unlike Instagram this needs no OAuth dance for read access — a
 *  plain API key from Google Cloud Console reads public channel/video data, so there is
 *  no token to refresh and nothing to expire on a timer. Set YOUTUBE_API_KEY and either
 *  YOUTUBE_CHANNEL_ID or YOUTUBE_HANDLE (the @handle, without the @) in Vercel. */
const YT = "https://www.googleapis.com/youtube/v3";

export type YtVideo = {
  id: string;
  title: string;
  publishedAt: string | null;
  views: number | null;
  likes: number | null;
  comments: number | null;
};

export type YtResult =
  | { connected: false; reason: string; detail?: string }
  | { connected: true; channelTitle: string | null; subscribers: number | null; videos: YtVideo[]; checkedAt: string };

export async function fetchYouTube(): Promise<YtResult> {
  const key = process.env.YOUTUBE_API_KEY;
  if (!key) return { connected: false, reason: "YOUTUBE_API_KEY לא מוגדר" };
  const channelId = process.env.YOUTUBE_CHANNEL_ID;
  const handle = process.env.YOUTUBE_HANDLE;
  if (!channelId && !handle) return { connected: false, reason: "YOUTUBE_CHANNEL_ID או YOUTUBE_HANDLE לא מוגדרים" };

  try {
    const chParam = channelId ? `id=${channelId}` : `forHandle=${handle}`;
    const chr = await fetch(
      `${YT}/channels?part=snippet,statistics,contentDetails&${chParam}&key=${key}`,
      { cache: "no-store" },
    );
    if (!chr.ok) {
      return { connected: false, reason: `יוטיוב החזיר ${chr.status}`, detail: (await chr.text()).slice(0, 300) };
    }
    const chj = await chr.json();
    const channel = chj.items?.[0];
    if (!channel) return { connected: false, reason: "הערוץ לא נמצא — בדוק את ה-ID או ה-handle" };

    const uploadsPlaylist = channel.contentDetails?.relatedPlaylists?.uploads;
    if (!uploadsPlaylist) return { connected: false, reason: "לא נמצאה רשימת ההעלאות של הערוץ" };

    const pir = await fetch(
      `${YT}/playlistItems?part=snippet&playlistId=${uploadsPlaylist}&maxResults=25&key=${key}`,
      { cache: "no-store" },
    );
    const pij = pir.ok ? await pir.json() : { items: [] };
    const ids: string[] = (pij.items ?? [])
      .map((it: { snippet?: { resourceId?: { videoId?: string } } }) => it.snippet?.resourceId?.videoId)
      .filter(Boolean);
    if (ids.length === 0) {
      return {
        connected: true,
        channelTitle: channel.snippet?.title ?? null,
        subscribers: channel.statistics?.subscriberCount ? Number(channel.statistics.subscriberCount) : null,
        videos: [],
        checkedAt: new Date().toISOString(),
      };
    }

    const vr = await fetch(`${YT}/videos?part=snippet,statistics&id=${ids.join(",")}&key=${key}`, {
      cache: "no-store",
    });
    const vj = vr.ok ? await vr.json() : { items: [] };
    const videos: YtVideo[] = (vj.items ?? []).map(
      (v: {
        id: string;
        snippet?: { title?: string; publishedAt?: string };
        statistics?: { viewCount?: string; likeCount?: string; commentCount?: string };
      }): YtVideo => ({
        id: v.id,
        title: v.snippet?.title ?? v.id,
        publishedAt: v.snippet?.publishedAt ?? null,
        views: v.statistics?.viewCount ? Number(v.statistics.viewCount) : null,
        likes: v.statistics?.likeCount ? Number(v.statistics.likeCount) : null,
        comments: v.statistics?.commentCount ? Number(v.statistics.commentCount) : null,
      }),
    );

    return {
      connected: true,
      channelTitle: channel.snippet?.title ?? null,
      subscribers: channel.statistics?.subscriberCount ? Number(channel.statistics.subscriberCount) : null,
      videos,
      checkedAt: new Date().toISOString(),
    };
  } catch (e) {
    return { connected: false, reason: (e as Error).message };
  }
}

export type LatestIssue = { title: string; url: string; publishedAt: string } | null;

/** The most recent published issue, for the homepage: someone deciding whether to hand
 *  over an email has nothing to judge the newsletter by if the signup form is the only
 *  thing they see. Returns null on anything wrong — no key, no posts yet, a bad response
 *  — rather than fabricating a preview, since "nothing to show" is an honest state and
 *  a wrong one is not. */
export async function fetchLatestBeehiivIssue(): Promise<LatestIssue> {
  const key = process.env.BEEHIIV_API_KEY;
  if (!key) return null;
  try {
    const r = await fetch(
      `https://api.beehiiv.com/v2/publications/${BEEHIIV_PUB}/posts?limit=1&status=confirmed&order_by=publish_date&direction=desc`,
      { headers: { Authorization: `Bearer ${key}` }, cache: "no-store" },
    );
    if (!r.ok) return null;
    const j = (await r.json()) as {
      data?: Array<{ title?: string; web_url?: string; publish_date?: number }>;
    };
    const p = j.data?.[0];
    if (!p?.title || !p.web_url) return null;
    return {
      title: p.title,
      url: p.web_url,
      publishedAt: p.publish_date
        ? new Date(p.publish_date * 1000).toISOString()
        : new Date().toISOString(),
    };
  } catch {
    return null;
  }
}
