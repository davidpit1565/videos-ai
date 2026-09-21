/** One place that talks to Instagram and Beehiiv, so the pages, the API routes and the
 *  nightly tracker all see exactly the same numbers. */

import { sharedPool } from "./db";
import type { MetricStatus } from "./types";
import { statusFromErrorBody } from "./insights";

/** Every external call in this file used to be a bare fetch() with no deadline. A
 *  connection that opens but never finishes responding never rejects and never
 *  resolves — it just hangs, and fetchInstagram() alone can issue up to 100 of these
 *  concurrently (one insights call per media item, across up to 4 paginated pages).
 *  One stuck socket anywhere in that batch stalls the whole Promise.all, which stalls
 *  /api/track's single await Promise.all([...]) with no fallback of its own — the
 *  request just hangs until Vercel's platform ceiling kills it, instead of failing
 *  fast and leaving the rest of the pull to still go through. Every fetch below goes
 *  through this instead of the raw global. */
async function timedFetch(url: string, init?: RequestInit, ms = 15000): Promise<Response> {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), ms);
  try {
    return await fetch(url, { ...init, signal: ctrl.signal });
  } finally {
    clearTimeout(t);
  }
}

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
  /** Set only when the insights call itself failed (non-2xx) or threw — the reason
   *  views/reach/etc came back null this pull was never visible anywhere before: the
   *  code silently kept whatever was already stored, which reads identically to "the
   *  numbers just aren't moving" whether the real cause is a stale token, a metric
   *  the API rejected, or Instagram itself. See /api/connections' live.instagram. */
  insightsError?: string;
  /** AVAILABLE/NOT_AVAILABLE per base metric this pull, derived from whether Instagram's
   *  insights response actually named that metric — not from whether the whole request
   *  succeeded. A metric can be individually absent from a successful response (e.g. an
   *  image has no `shares`) without the request itself failing. */
  metricStatus?: Partial<Record<"views" | "reach" | "saves" | "shares", MetricStatus>>;
  /** best-effort, `reach` with `breakdown=follow_type` — see fetchInstagram. */
  reachByFollowerType?: { followers: number | null; nonFollowers: number | null };
  reachByFollowerTypeStatus?: MetricStatus;
  /** best-effort Reels watch-time/retention metrics — see fetchInstagram. */
  watchAvgSeconds?: number | null;
  watchTotalSeconds?: number | null;
  watchReplays?: number | null;
  watchPlays?: number | null;
  watchStatus?: MetricStatus;
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
    const r = await timedFetch(
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
    const r = await timedFetch(
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
    const prof = await timedFetch(
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

    // One page of 25 was the whole account's history at first, so nothing here ever
    // needed a second page — but a post that ages past the newest 25 doesn't just stop
    // showing up here, it drops out of every check downstream too: auto-linking,
    // mislink correction, the "unlinked post" notice. Following the account's own next
    // link keeps that coverage as the account grows past this channel's early size;
    // capped at 4 pages (100 posts, a few months at this channel's pace) so a runaway
    // account can't turn one pull into an unbounded chain of requests.
    type IgMediaRaw = {
      id: string; caption?: string; media_type?: string; permalink?: string;
      timestamp?: string; like_count?: number; comments_count?: number;
    };
    const raw: IgMediaRaw[] = [];
    let next: string | null =
      `${IG}/${user}/media?fields=id,caption,media_type,permalink,timestamp,like_count,comments_count&limit=25&access_token=${token}`;
    for (let page = 0; page < 4 && next; page++) {
      const mr: Response = await timedFetch(next, { cache: "no-store" });
      if (!mr.ok) break;
      const j: { data?: IgMediaRaw[]; paging?: { next?: string } } = await mr.json();
      raw.push(...(j.data ?? []));
      next = j.paging?.next ?? null;
    }

    // Insight names differ by media type; asking for reel metrics on an image 400s,
    // so each request is scoped and a failure degrades to the basic counts.
    const media = await Promise.all(
      raw.map(async (m): Promise<IgMedia> => {
        const base: IgMedia = {
          id: m.id,
          // Every caption we write puts the episode's own "/e/N" link several lines down,
          // well past 120 characters (e.g. reel 11's sits at character 643) — truncating
          // here silently fed the auto-link matcher in /api/track a caption that could
          // never contain its own episode number, which is why matching ever had to fall
          // back to the much less reliable title-substring guess in the first place.
          // Instagram's own caption cap is 2200 characters; that's the only limit needed.
          caption: (m.caption ?? "").slice(0, 2200),
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
          const ir = await timedFetch(`${IG}/${m.id}/insights?metric=${metrics}&access_token=${token}`, {
            cache: "no-store",
          });
          if (!ir.ok) {
            return { ...base, insightsError: `HTTP ${ir.status}: ${(await ir.text()).slice(0, 200)}` };
          }
          const j = (await ir.json()) as { data?: { name: string; values: { value: number }[] }[] };
          const v: Record<string, number> = {};
          for (const d of j.data ?? []) v[d.name] = d.values?.[0]?.value ?? 0;
          // A metric can be individually absent from an otherwise-successful response
          // (an image has no `shares`) — present in `data` is AVAILABLE, absent is
          // NOT_AVAILABLE, regardless of whether the whole request came back 200.
          const metricStatus: IgMedia["metricStatus"] = {
            views: v.views !== undefined ? "AVAILABLE" : "NOT_AVAILABLE",
            reach: v.reach !== undefined ? "AVAILABLE" : "NOT_AVAILABLE",
            saves: v.saved !== undefined ? "AVAILABLE" : "NOT_AVAILABLE",
            shares: v.shares !== undefined ? "AVAILABLE" : "NOT_AVAILABLE",
          };

          // Instagram's own app shows one combined "Views" number for a Reel that also
          // got auto-crossposted to the linked Facebook Page — Instagram views plus
          // Facebook views. The IG media insights endpoint exposes that same combined
          // total directly as its own metric, crossposted_views — no need to look up
          // the Facebook Page's copy of the post separately. It 400s for a Reel that
          // was never crossposted (most of them, if Facebook auto-sharing is off), so
          // it's fetched in its own best-effort call instead of the metric list above,
          // where one bad metric would fail the whole request and null out views/reach
          // for every reel, crossposted or not.
          let crossposted: number | null = null;
          if (m.media_type === "REELS") {
            try {
              const cr = await timedFetch(
                `${IG}/${m.id}/insights?metric=crossposted_views&access_token=${token}`,
                { cache: "no-store" },
              );
              if (cr.ok) {
                const cj = (await cr.json()) as { data?: { name: string; values: { value: number }[] }[] };
                crossposted = cj.data?.[0]?.values?.[0]?.value ?? null;
              }
            } catch {
              // not crossposted, or Facebook not linked — same as Instagram's own app,
              // which just shows the Instagram-only number in that case.
            }
          }

          // reach split by whether the viewer already followed the account —
          // Instagram's own `breakdown=follow_type` parameter on the `reach` metric.
          // Its own request, best-effort: an account/media/API-version combination that
          // doesn't support the breakdown must not null out the plain metrics above,
          // same reasoning as crossposted_views. Never derived by subtracting from
          // plain reach — Instagram doesn't document the two as guaranteed to add up.
          let reachByFollowerType: IgMedia["reachByFollowerType"];
          let reachByFollowerTypeStatus: MetricStatus = "NOT_REQUESTED";
          if (m.media_type === "REELS" || m.media_type === "VIDEO") {
            reachByFollowerTypeStatus = "UNKNOWN";
            try {
              const br = await timedFetch(
                `${IG}/${m.id}/insights?metric=reach&breakdown=follow_type&access_token=${token}`,
                { cache: "no-store" },
              );
              if (br.ok) {
                const bj = (await br.json()) as {
                  data?: {
                    name: string;
                    total_value?: { breakdowns?: { results?: { dimension_values?: string[]; value?: number }[] }[] };
                  }[];
                };
                const results = bj.data?.[0]?.total_value?.breakdowns?.[0]?.results ?? [];
                let followers: number | null = null;
                let nonFollowers: number | null = null;
                for (const r of results) {
                  const dim = r.dimension_values?.[0]?.toLowerCase();
                  if (dim === "follower") followers = r.value ?? null;
                  else if (dim === "non_follower") nonFollowers = r.value ?? null;
                }
                reachByFollowerType = { followers, nonFollowers };
                reachByFollowerTypeStatus = followers !== null || nonFollowers !== null ? "AVAILABLE" : "NOT_AVAILABLE";
              } else {
                reachByFollowerTypeStatus = statusFromErrorBody((await br.text()).slice(0, 300));
              }
            } catch {
              reachByFollowerTypeStatus = "API_ERROR";
            }
          }

          // Reels watch-time/retention metrics — its own best-effort call for the same
          // reason as the two above: a metric name this API version/account doesn't
          // support must not null out views/reach/likes/etc for the whole media item.
          // Real metric names as of Graph API v21's Reels media insights; confirmed or
          // rejected per this account by the actual response (watchStatus), not assumed
          // from documentation — see INSTAGRAM_INSIGHTS.md.
          let watchAvgSeconds: number | null = null;
          let watchTotalSeconds: number | null = null;
          let watchReplays: number | null = null;
          let watchPlays: number | null = null;
          let watchStatus: MetricStatus = "NOT_REQUESTED";
          if (m.media_type === "REELS") {
            watchStatus = "UNKNOWN";
            try {
              const wr = await timedFetch(
                `${IG}/${m.id}/insights?metric=ig_reels_avg_watch_time,ig_reels_video_view_total_time,clips_replays_count,ig_reels_aggregated_all_plays_count&access_token=${token}`,
                { cache: "no-store" },
              );
              if (wr.ok) {
                const wj = (await wr.json()) as { data?: { name: string; values: { value: number }[] }[] };
                const wv: Record<string, number> = {};
                for (const d of wj.data ?? []) wv[d.name] = d.values?.[0]?.value ?? 0;
                watchAvgSeconds = wv.ig_reels_avg_watch_time ?? null;
                watchTotalSeconds = wv.ig_reels_video_view_total_time ?? null;
                watchReplays = wv.clips_replays_count ?? null;
                watchPlays = wv.ig_reels_aggregated_all_plays_count ?? null;
                watchStatus = Object.keys(wv).length > 0 ? "AVAILABLE" : "NOT_AVAILABLE";
              } else {
                watchStatus = statusFromErrorBody((await wr.text()).slice(0, 300));
              }
            } catch {
              watchStatus = "API_ERROR";
            }
          }

          return {
            ...base,
            views: crossposted ?? v.views ?? null,
            reach: v.reach ?? null,
            saves: v.saved ?? null,
            shares: v.shares ?? null,
            metricStatus,
            reachByFollowerType,
            reachByFollowerTypeStatus,
            watchAvgSeconds,
            watchTotalSeconds,
            watchReplays,
            watchPlays,
            watchStatus,
          };
        } catch (err) {
          return { ...base, insightsError: err instanceof Error ? err.message : String(err) };
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

export type AccountInsightsResult =
  | { attempted: false }
  | {
      attempted: true;
      periodDays: number;
      accountsReached: number | null;
      accountsReachedStatus: MetricStatus;
      profileVisits: number | null;
      profileVisitsStatus: MetricStatus;
      websiteClicks: number | null;
      websiteClicksStatus: MetricStatus;
      follows: number | null;
      unfollows: number | null;
      followsStatus: MetricStatus;
    };

/** Account-wide Instagram Insights — reach, profile visits, website clicks, follows —
 *  attempted best-effort, in its own request, gated so it can be switched off without a
 *  deploy (INSTAGRAM_INSIGHTS_ENABLED=false) if it ever misbehaves against a real account.
 *  Unlike fetchInstagram() above, nothing before 22.9.2026 ever called this endpoint at
 *  all — followers_count was the only account-level number this app ever read. A failure
 *  here is a real, useful answer (NOT_AVAILABLE/PERMISSION_REQUIRED/API_ERROR), never a
 *  reason to fail /api/track's pull; the caller always gets a result to store.
 *
 *  Instagram's `follows_and_unfollows` metric is a single combined count, not a
 *  follows/unfollows split — this never invents that split. A real per-direction number
 *  would need the same `breakdown=follow_type`-style parameter fetchInstagram() uses for
 *  reach, which is not attempted here; unfollows stays null until it is. */
export async function fetchInstagramAccountInsights(): Promise<AccountInsightsResult> {
  if (process.env.INSTAGRAM_INSIGHTS_ENABLED === "false") return { attempted: false };
  const token = await igToken();
  if (!token) return { attempted: false };
  const { host, via } = igRoute(token);
  const user = process.env.IG_USER_ID || (via === "instagram-login" ? "me" : "");
  if (!user) return { attempted: false };

  const periodDays = 1;
  const metrics = "reach,profile_views,website_clicks,follows_and_unfollows";
  try {
    const r = await timedFetch(
      `${host}/${user}/insights?metric=${metrics}&period=day&metric_type=total_value&access_token=${token}`,
      { cache: "no-store" },
    );
    if (!r.ok) {
      const status = statusFromErrorBody((await r.text()).slice(0, 300));
      return {
        attempted: true, periodDays,
        accountsReached: null, accountsReachedStatus: status,
        profileVisits: null, profileVisitsStatus: status,
        websiteClicks: null, websiteClicksStatus: status,
        follows: null, unfollows: null, followsStatus: status,
      };
    }
    const j = (await r.json()) as { data?: { name: string; total_value?: { value?: number } }[] };
    const v: Record<string, number> = {};
    for (const d of j.data ?? []) if (d.total_value?.value !== undefined) v[d.name] = d.total_value.value;
    return {
      attempted: true,
      periodDays,
      accountsReached: v.reach ?? null,
      accountsReachedStatus: v.reach !== undefined ? "AVAILABLE" : "NOT_AVAILABLE",
      profileVisits: v.profile_views ?? null,
      profileVisitsStatus: v.profile_views !== undefined ? "AVAILABLE" : "NOT_AVAILABLE",
      websiteClicks: v.website_clicks ?? null,
      websiteClicksStatus: v.website_clicks !== undefined ? "AVAILABLE" : "NOT_AVAILABLE",
      follows: v.follows_and_unfollows ?? null,
      unfollows: null,
      followsStatus: v.follows_and_unfollows !== undefined ? "AVAILABLE" : "NOT_AVAILABLE",
    };
  } catch {
    return {
      attempted: true, periodDays,
      accountsReached: null, accountsReachedStatus: "API_ERROR",
      profileVisits: null, profileVisitsStatus: "API_ERROR",
      websiteClicks: null, websiteClicksStatus: "API_ERROR",
      follows: null, unfollows: null, followsStatus: "API_ERROR",
    };
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
    const r = await timedFetch(
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
  /** Every description we upload starts with this episode's own line, same as an
   *  Instagram caption's "/e/N" — needed so a video can be matched/verified against
   *  the episode it names, the same way Instagram posts already are. */
  description: string;
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
    const chr = await timedFetch(
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

    // Same reasoning as Instagram's media pull: one page used to be the whole channel,
    // so nothing here ever needed a second page — but a video past the newest 25 doesn't
    // just stop showing up, it drops out of matching entirely. Capped at 4 pages (100
    // videos) for the same reason.
    const ids: string[] = [];
    let ytNext: string | null =
      `${YT}/playlistItems?part=snippet&playlistId=${uploadsPlaylist}&maxResults=25&key=${key}`;
    for (let page = 0; page < 4 && ytNext; page++) {
      const pir: Response = await timedFetch(ytNext, { cache: "no-store" });
      if (!pir.ok) break;
      const pij: { items?: { snippet?: { resourceId?: { videoId?: string } } }[]; nextPageToken?: string } =
        await pir.json();
      ids.push(...(pij.items ?? []).map((it) => it.snippet?.resourceId?.videoId).filter((x): x is string => !!x));
      ytNext = pij.nextPageToken
        ? `${YT}/playlistItems?part=snippet&playlistId=${uploadsPlaylist}&maxResults=25&pageToken=${pij.nextPageToken}&key=${key}`
        : null;
    }
    if (ids.length === 0) {
      return {
        connected: true,
        channelTitle: channel.snippet?.title ?? null,
        subscribers: channel.statistics?.subscriberCount ? Number(channel.statistics.subscriberCount) : null,
        videos: [],
        checkedAt: new Date().toISOString(),
      };
    }

    // The videos endpoint caps at 50 ids per call regardless of how many playlist pages
    // were followed above, so a >50-video pull has to go in batches.
    type YtVideoRaw = {
      id: string;
      snippet?: { title?: string; description?: string; publishedAt?: string };
      statistics?: { viewCount?: string; likeCount?: string; commentCount?: string };
    };
    const items: YtVideoRaw[] = [];
    for (let i = 0; i < ids.length; i += 50) {
      const batch = ids.slice(i, i + 50);
      const vr = await timedFetch(`${YT}/videos?part=snippet,statistics&id=${batch.join(",")}&key=${key}`, {
        cache: "no-store",
      });
      const vj: { items?: YtVideoRaw[] } = vr.ok ? await vr.json() : { items: [] };
      items.push(...(vj.items ?? []));
    }
    const videos: YtVideo[] = items.map((v): YtVideo => ({
      id: v.id,
      title: v.snippet?.title ?? v.id,
      description: v.snippet?.description ?? "",
      publishedAt: v.snippet?.publishedAt ?? null,
      views: v.statistics?.viewCount ? Number(v.statistics.viewCount) : null,
      likes: v.statistics?.likeCount ? Number(v.statistics.likeCount) : null,
      comments: v.statistics?.commentCount ? Number(v.statistics.commentCount) : null,
    }));

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

// ───────────────────────── Facebook ─────────────────────────
// A genuinely separate platform from Instagram, not a side effect of it — see
// lib/publish.ts's own comment on publishToFacebook: Meta has no Graph API parameter
// that auto-crossposts an Instagram Reel to a linked Facebook Page (that's a manual
// toggle inside the Instagram app only). Every episode published here goes to
// Facebook as its own independent Page video (via POST /{page-id}/videos), with its
// own video id, so its views have to be pulled separately too — fetchInstagram's
// crossposted_views metric only covers the in-app auto-crosspost case, not this one.
const FB_GRAPH = "https://graph.facebook.com/v21.0";

export type FbVideo = {
  id: string;
  /** Every description we upload starts with this episode's own line, same convention
   *  as YouTube's own description/Instagram's own caption — needed to auto-link this
   *  video back to the episode that names it. */
  description: string;
  permalink: string | null;
  publishedAt: string | null;
  views: number | null;
  likes: number | null;
  comments: number | null;
};

export type FbResult =
  | { connected: false; reason: string; detail?: string }
  | {
      connected: true;
      pageName: string | null;
      followers: number | null;
      videos: FbVideo[];
      /** Set when the /videos edge itself returned an error — otherwise a genuine
       *  zero-videos account reads identically to a silently-failing fetch. This is
       *  the personal-profile equivalent of Instagram's own per-media insightsError:
       *  a real API rejection must not look the same as "nothing to show". */
      videosError?: string;
      checkedAt: string;
    };

export async function fetchFacebook(): Promise<FbResult> {
  const pageId = process.env.FB_PAGE_ID;
  const pageToken = process.env.FB_PAGE_ACCESS_TOKEN;
  if (!pageId) return { connected: false, reason: "FB_PAGE_ID לא מוגדר" };
  if (!pageToken) return { connected: false, reason: "FB_PAGE_ACCESS_TOKEN לא מוגדר" };

  try {
    // Both followers_count and fan_count 400'd with the identical "(#100) Tried
    // accessing nonexisting field" error, on the same object — the field name was
    // never the actual problem. That error shape (not a permissions error) means the
    // Graph API doesn't recognize either field on THIS node at all, which points at
    // FB_PAGE_ID resolving to something other than a plain Page node under this API
    // version/token. Fetching name-only first (every node type supports it) isolates
    // whether the connection itself works before asking for a Page-specific field —
    // and follower count now degrades gracefully (best-effort, like per-video insights
    // below) instead of failing the whole connection over one optional number.
    const pr = await timedFetch(
      `${FB_GRAPH}/${pageId}?fields=id,name&access_token=${pageToken}`,
      { cache: "no-store" },
    );
    if (!pr.ok) {
      return {
        connected: false,
        reason: `פייסבוק החזיר ${pr.status}`,
        detail: (await pr.text()).slice(0, 300),
      };
    }
    const page = (await pr.json()) as { id?: string; name?: string };

    let followers: number | null = null;
    try {
      const fr = await timedFetch(
        `${FB_GRAPH}/${pageId}?fields=fan_count&access_token=${pageToken}`,
        { cache: "no-store" },
      );
      if (fr.ok) {
        const fj = (await fr.json()) as { fan_count?: number };
        followers = fj.fan_count ?? null;
      }
    } catch {
      // follower count temporarily unavailable — connection itself still stands
    }

    // Same reasoning as Instagram/YouTube's own media pulls: one page was the whole
    // account's history at first, so nothing here ever needed a second page — capped
    // at 4 pages (100 videos) for the same reason, so a runaway account can't turn one
    // pull into an unbounded chain of requests.
    type FbVideoRaw = {
      id: string;
      description?: string;
      permalink_url?: string;
      created_time?: string;
      likes?: { summary?: { total_count?: number } };
      comments?: { summary?: { total_count?: number } };
    };
    const raw: FbVideoRaw[] = [];
    let videosError: string | undefined;
    let next: string | null =
      `${FB_GRAPH}/${pageId}/videos?fields=id,description,permalink_url,created_time,likes.summary(true),comments.summary(true)&limit=25&access_token=${pageToken}`;
    for (let page2 = 0; page2 < 4 && next; page2++) {
      const vr: Response = await timedFetch(next, { cache: "no-store" });
      if (!vr.ok) {
        // A real rejection (permissions, deprecated edge) must not read the same as
        // "this account genuinely has zero videos" — the two look identical without this.
        videosError = `/videos החזיר ${vr.status}: ${(await vr.text()).slice(0, 300)}`;
        break;
      }
      const vj: { data?: FbVideoRaw[]; paging?: { next?: string } } = await vr.json();
      raw.push(...(vj.data ?? []));
      next = vj.paging?.next ?? null;
    }

    const videos: FbVideo[] = await Promise.all(
      raw.map(async (v): Promise<FbVideo> => {
        const base: FbVideo = {
          id: v.id,
          description: v.description ?? "",
          permalink: v.permalink_url ? `https://www.facebook.com${v.permalink_url}` : null,
          publishedAt: v.created_time ?? null,
          views: null,
          likes: v.likes?.summary?.total_count ?? null,
          comments: v.comments?.summary?.total_count ?? null,
        };
        // Best-effort, its own call: one video with insights temporarily unavailable
        // must not null out views for every other video in the same pull (the same
        // reasoning as Instagram's crossposted_views fetch above).
        try {
          const ir = await timedFetch(
            `${FB_GRAPH}/${v.id}/video_insights?metric=total_video_views&access_token=${pageToken}`,
            { cache: "no-store" },
          );
          if (ir.ok) {
            const ij = (await ir.json()) as { data?: { name: string; values: { value: number }[] }[] };
            base.views = ij.data?.[0]?.values?.[0]?.value ?? null;
          }
        } catch {
          // insights temporarily unavailable — views stays null, rest of the row is still real
        }
        return base;
      }),
    );

    return {
      connected: true,
      pageName: page.name ?? null,
      followers,
      videos,
      ...(videosError ? { videosError } : {}),
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
    const r = await timedFetch(
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
