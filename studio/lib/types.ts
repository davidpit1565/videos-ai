/** One vocabulary for "we don't have this metric," used everywhere instead of five
 *  different unlabeled spellings (a bare null, a missing key, a silently-substituted
 *  fallback value). Each meaning is distinct and never interchangeable:
 *  - AVAILABLE — Instagram returned a real value for this metric this pull.
 *  - NOT_AVAILABLE — Instagram's API doesn't support this metric here (wrong media
 *    type, wrong account type, or the metric plain doesn't exist for this account).
 *  - PERMISSION_REQUIRED — the API told us, specifically, that the token lacks the
 *    permission this metric needs.
 *  - API_ERROR — a request failed for some other/temporary reason (network, 5xx,
 *    rate limit) — try again next pull, not a verdict about whether the metric exists.
 *  - NOT_REQUESTED — our own code never asked for this metric at all.
 *  - UNKNOWN — we haven't determined which of the above applies yet. */
export type MetricStatus =
  | "AVAILABLE"
  | "NOT_AVAILABLE"
  | "PERMISSION_REQUIRED"
  | "API_ERROR"
  | "NOT_REQUESTED"
  | "UNKNOWN";

export type Channel = "ig" | "tiktok" | "yt" | "ytlong";
export const CHANNELS: Channel[] = ["ig", "tiktok", "yt", "ytlong"];
export const CHANNEL_HE: Record<Channel, string> = {
  ig: "אינסטגרם", tiktok: "טיקטוק", yt: "Shorts", ytlong: "יוטיוב ארוך",
};

export type Status = "idea" | "script" | "voice" | "render" | "testing" | "live";
export type Format = "reel" | "long" | "both";

export const STATUS_ORDER: Status[] = ["idea", "script", "voice", "render", "testing", "live"];
export const STATUS_HE: Record<Status, string> = {
  idea: "רעיון", script: "תסריט", voice: "קריינות",
  render: "רנדר", testing: "בדיקה", live: "פורסם",
};

export type Episode = {
  id: string;
  number: number;
  title: string;
  format: Format;
  status: Status;
  topic: string;
  tested: boolean;
  publishedAt: string | null;
  /** Instagram media id — how metrics get attached to this episode */
  igMediaId: string | null;
  /** the post's own instagram.com/reel/... URL — what the official embed needs; optional
   *  because rows linked before this field existed only ever stored the id, not this. */
  igPermalink?: string | null;
  ytVideoId: string | null;
  notes: string;
  /** pulled from Instagram; null until the episode is live and a token exists. saves/shares
   *  have no YouTube equivalent, which is the tell that these were always Instagram's own
   *  fields, not a shared "views" — the two platforms used to write into the same field and
   *  YouTube's own, much smaller count silently overwrote Instagram's real one on every pull
   *  that had both linked (confirmed against the activity feed: the same timestamp shows
   *  "ריל N · צפיות" write a real Instagram number, then "ריל N · צפיות ביוטיוב" immediately
   *  overwrite the same `views` field seconds later). See ytViews/ytLikes/ytComments below. */
  views: number | null;
  likes: number | null;
  saves: number | null;
  comments: number | null;
  shares: number | null;
  /** YouTube's own counts, kept apart from the Instagram fields above on purpose — see the
   *  comment on `views`. Optional so a state saved before this field existed still loads. */
  ytViews?: number | null;
  ytLikes?: number | null;
  ytComments?: number | null;
  /** Facebook Page video id — how metrics get attached to this episode. Kept apart from
   *  the Instagram/YouTube fields above for the same reason: three platforms writing into
   *  one shared `views` would silently overwrite each other on every pull. */
  fbVideoId?: string | null;
  fbPermalink?: string | null;
  fbViews?: number | null;
  fbLikes?: number | null;
  fbComments?: number | null;
  /** How many subscribers this episode brought. /api/track now fills this in for real,
   *  counting subscribers whose signup happened on this episode's own page (see
   *  subscribersByEpisode() in lib/db.ts) — it only ever overwrites with a real positive
   *  count, so a manually-typed number from before this existed stays put until real
   *  data for that episode actually arrives. Still hand-editable in /videos as a
   *  fallback for episodes with no tagged signups yet. */
  subsAttributed: number | null;
  /** planned publish date, YYYY-MM-DD. The week view is built from this. */
  publishOn?: string | null;
  /** where it goes out. One build, several platforms, no extra work. */
  channels?: Channel[];
  /** Instagram's own `reach` metric — kept entirely separate from `views`, never a
   *  fallback for it. Before 22.9.2026 /api/track wrote `views: m.views ?? m.reach`,
   *  so a real reach number could silently become the displayed "views" whenever
   *  Instagram's views metric itself came back empty — see reachStatus below and
   *  studio/INSTAGRAM_INSIGHTS.md. Never resurrect that fallback. */
  reach?: number | null;
  reachStatus?: MetricStatus;
  /** Instagram's `reach` metric with `breakdown=follow_type` — whether the viewer
   *  already followed the account when they saw this Reel. Fetched in its own
   *  best-effort request (see fetchInstagram); not guaranteed available for every
   *  account/media/API version, so reachByFollowerTypeStatus is the real answer, not
   *  "both fields present". Never derived as `reach - followers` — Instagram doesn't
   *  document that the two are guaranteed to add up, so we don't invent the subtraction. */
  reachByFollowerType?: { followers: number | null; nonFollowers: number | null };
  reachByFollowerTypeStatus?: MetricStatus;
  /** Reels watch-time/retention metrics, attempted best-effort against Instagram's media
   *  insights endpoint (ig_reels_avg_watch_time, ig_reels_video_view_total_time,
   *  clips_replays_count, ig_reels_aggregated_all_plays_count — the real metric names as
   *  of API v21; confirmed or rejected per account by the actual response, watchStatus
   *  is that real answer, not an assumption from documentation). */
  watchAvgSeconds?: number | null;
  watchTotalSeconds?: number | null;
  watchReplays?: number | null;
  watchPlays?: number | null;
  watchStatus?: MetricStatus;
  /** Exact ISO-8601 publish timestamp straight from the platform's own API field.
   *  `publishedAt` above stays untouched (plain YYYY-MM-DD) for every existing reader
   *  that expects that shape — this is additive, never a replacement, and every writer
   *  of it already has the full timestamp on hand (Instagram/YouTube/Facebook's own
   *  media objects all return one), so this can and does backfill retroactively for
   *  already-linked episodes on their next pull. NOT_AVAILABLE only for a row whose
   *  underlying media is gone before this field existed and never gets pulled again —
   *  the studio never invents a time. */
  publishedAtPrecise?: string | null;
  publishedAtPreciseStatus?: MetricStatus;
  /** Opt-in flag: this tested-but-not-yet-live episode should be published automatically
   *  by /api/scheduled-publish's daily cron, at the one fixed hour set in vercel.json,
   *  instead of waiting for a manual press of the studio's publish button. Exists
   *  because same-day double-posting and an inconsistent posting hour both measurably
   *  hurt reach (see channel/content-memory.md, 21.9.2026) — a single daily cron at a
   *  fixed hour structurally fixes both at once: at most one auto-publish a day, always
   *  at the same time. Cleared automatically once the cron actually publishes it (the
   *  episode still needs a human to check "tested" and tick this box first — it never
   *  auto-selects an episode nobody approved). */
  queuedForPublish?: boolean;
};

export type Snapshot = {
  id: string;
  date: string;
  subscribers: number | null;
  igFollowers: number | null;
  ytSubs: number | null;
  /** Optional so a snapshot saved before this field existed still loads. */
  fbFollowers?: number | null;
  note: string;
};

/** One point-in-time reading of a single Reel's Instagram metrics, kept forever — unlike
 *  the fields on Episode above, which only ever hold the latest value and get overwritten
 *  on every pull. This is what lets us later ask "how many views did episode 40 have 24
 *  hours after it went live" without having already thrown that answer away. Written by
 *  /api/track, deduplicated (see lib/insights.ts's shouldSnapshot) so a daily cron and a
 *  manual pull don't produce hundreds of near-identical rows — but never overwritten or
 *  deleted once written. snapshotType distinguishes a snapshot taken while the episode
 *  was actually live and current ("live") from one produced by a one-time backfill run
 *  against an episode's current numbers on some later day ("backfill") — a backfill
 *  snapshot's collectedAt is the day it was run, never the episode's publish day. */
export type ReelInsightSnapshot = {
  id: string;
  episodeNumber: number;
  collectedAt: string;
  source: "instagram";
  snapshotType: "live" | "backfill";
  views: number | null;
  reach: number | null;
  likes: number | null;
  comments: number | null;
  saves: number | null;
  shares: number | null;
  watchAvgSeconds: number | null;
  watchTotalSeconds: number | null;
  watchReplays: number | null;
};

/** One day's account-wide Instagram reading beyond the follower count the existing
 *  Snapshot type above already tracks. followersCount/mediaCount are point-in-time;
 *  accountsReached/profileVisits/websiteClicks/follows/unfollows (when Instagram
 *  provides them at all — see the *Status fields) are totals over periodDays, and the
 *  two kinds are never conflated as if they meant the same thing. Attempted on every
 *  /api/track pull, best-effort — a status of NOT_AVAILABLE/PERMISSION_REQUIRED/
 *  API_ERROR here is itself a real, useful recorded answer, not a failed pull. */
export type AccountInsightSnapshot = {
  id: string;
  collectedAt: string;
  followersCount: number | null;
  mediaCount: number | null;
  periodDays: number | null;
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

export type RevenueLine = {
  id: string;
  name: string;
  status: Status;
  mrrEur: number;
  needsAudience: string;
  nextStep: string;
};

/** Something that changed, recorded automatically so he never has to notice it himself. */
export type ActivityEvent = {
  id: string;
  at: string;
  source: "instagram" | "beehiiv" | "youtube" | "facebook" | "studio";
  label: string;
  value: number | null;
  delta: number | null;
};

/** The agent's read on one idea, 0-100 per category — his own judgment call, not a
 *  measured metric, framed that way in the prompt that produces it. Six categories,
 *  each answering a different question so they don't just restate each other:
 *  the original six (marketing/content-interesting/content-needed/branding/
 *  importance/demand) had real overlap between "importance" and everything else. */
export type IdeaScore = {
  categories: {
    /** Does this sell itself in one line — a caption, a thumbnail text, a hook? */
    marketingPotential: number;
    /** Does the hook intrigue someone with zero interest in the topic, not just the target viewer? */
    hookStrength: number;
    /** Can this be explained with no jargon, in plain words, per the channel's own rule? */
    simplicity: number;
    /** Does it fit "Actually Works": a real setup, what breaks, no hype? */
    brandFit: number;
    /** Is this an open topic (per demand-report.md's method) or one where a 1M+ leader already owns it? */
    competitiveSpace: number;
    /** Is there real measured search/view demand behind this, or is it a guess? */
    audienceDemand: number;
  };
  verdict: "yes" | "no" | "draft";
  reasoning: string;
};
export type Idea = { id: string; text: string; score?: IdeaScore | null };

export type State = {
  version: 1;
  episodes: Episode[];
  snapshots: Snapshot[];
  revenue: RevenueLine[];
  ideas: Idea[];
  /** optional so states saved before the feed existed still load */
  activity?: ActivityEvent[];
  /** set by /api/youtube/publish right after a successful upload — YouTube's own daily
   *  upload quota is per-channel and undocumented, and a new/low-trust channel's real
   *  limit runs well under the general range, so the studio warns before a second
   *  same-day attempt instead of letting it fail live against the platform. */
  lastYoutubeUploadAt?: string | null;
  /** History /api/track has been writing since 22.9.2026 — see ReelInsightSnapshot and
   *  AccountInsightSnapshot above. Optional so a state saved before this existed still
   *  loads; missing/empty means "not collected yet", never "zero activity". */
  reelInsightSnapshots?: ReelInsightSnapshot[];
  accountInsightSnapshots?: AccountInsightSnapshot[];
  updatedAt: string;
};

export const uid = () =>
  (globalThis.crypto?.randomUUID?.() ?? String(Date.now() + Math.random())).slice(0, 12);

/** Engagement rate is the number that actually predicts reach. */
export function engagement(e: Episode): number | null {
  if (!e.views) return null;
  const acts = (e.likes ?? 0) + (e.saves ?? 0) + (e.comments ?? 0) + (e.shares ?? 0);
  return acts / e.views;
}

/** Saves-per-view is the signal for a "paste this" video: did anyone keep it? */
export function saveRate(e: Episode): number | null {
  if (!e.views || e.saves == null) return null;
  return e.saves / e.views;
}

/** Sunday to Friday. Saturday is off — his rule, and the schedule respects it. */
export function weekDays(from: Date): string[] {
  const d = new Date(from);
  d.setDate(d.getDate() - ((d.getDay() + 7) % 7));   // back to Sunday
  const out: string[] = [];
  for (let i = 0; i < 6; i++) {
    const x = new Date(d);
    x.setDate(d.getDate() + i);
    out.push(x.toISOString().slice(0, 10));
  }
  return out;
}

export const DAY_HE = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"];
