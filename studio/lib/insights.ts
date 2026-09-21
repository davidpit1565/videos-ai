/** Pure, network-free helpers for the Instagram Insights data layer — kept apart from
 *  sources.ts (which does the actual fetching) and track/impl.ts (which wires this into
 *  the daily pull) so the decision logic here can be unit-tested with `node --test`
 *  without a database, a token, or a live Instagram account. See INSTAGRAM_INSIGHTS.md. */

import type { MetricStatus } from "./types";

/** Instagram's own error bodies for a missing scope actually contain the word
 *  "permission" (e.g. "(#10) ... requires the 'pages_read_engagement' permission").
 *  Anything else that comes back non-2xx is treated as NOT_AVAILABLE for this metric on
 *  this account/media/API-version combination, not a guess about *why*. */
export function statusFromErrorBody(body: string): MetricStatus {
  return /permission/i.test(body) ? "PERMISSION_REQUIRED" : "NOT_AVAILABLE";
}

export type SnapshotMetrics = {
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

/** true if any metric genuinely moved since the last snapshot. Every field is compared
 *  with `!==`, so a real 0 and a missing null are never treated as equal — the same
 *  zero-vs-null distinction the rest of this layer keeps everywhere else. */
export function metricsChanged(a: SnapshotMetrics, b: SnapshotMetrics): boolean {
  return (
    a.views !== b.views ||
    a.reach !== b.reach ||
    a.likes !== b.likes ||
    a.comments !== b.comments ||
    a.saves !== b.saves ||
    a.shares !== b.shares ||
    a.watchAvgSeconds !== b.watchAvgSeconds ||
    a.watchTotalSeconds !== b.watchTotalSeconds ||
    a.watchReplays !== b.watchReplays
  );
}

/** A new historical snapshot is worth writing when either something actually changed,
 *  or enough time has passed since the last one that "nothing changed" is itself real
 *  information (not just two pulls a minute apart). Without the second condition, a
 *  Reel whose numbers plateau would only ever get one snapshot, ever — which silently
 *  breaks "views after 7 days" for anything that stopped moving before day 7. Without
 *  the first condition, a short dedupe window during a burst of manual pulls would
 *  produce dozens of near-identical rows. */
export function shouldSnapshot(
  last: ({ collectedAt: string } & SnapshotMetrics) | undefined,
  next: SnapshotMetrics,
  dedupeWindowMinutes: number,
  nowIso: string,
): boolean {
  if (!last) return true;
  if (metricsChanged(last, next)) return true;
  const minutesSince = (Date.parse(nowIso) - Date.parse(last.collectedAt)) / 60000;
  return minutesSince >= dedupeWindowMinutes;
}

/** numerator / denominator, only when both are real, non-negative numbers and the
 *  denominator isn't zero — never a fabricated 0 when the denominator is simply
 *  missing (per the project's "never fill 0 for a value that just isn't available"
 *  rule; a genuinely-zero numerator with a real denominator still divides normally). */
export function rate(
  numerator: number | null | undefined,
  denominator: number | null | undefined,
): number | null {
  if (numerator == null || denominator == null || denominator <= 0) return null;
  return numerator / denominator;
}

export type CalculatedMetric = { value: number | null; formula: string; sourceFields: string[] };

/** Every derived metric a Reel can support, computed once, together, each carrying its
 *  own formula and the raw fields it came from — so a client of this data never has to
 *  guess whether a number is something Instagram said or something we computed from it.
 *  Any input that's genuinely missing produces `value: null` for the metrics that need
 *  it, never a 0. `engagementRateByViews` is the pre-existing calculation (kept exactly
 *  as it was — see Episode's own `engagement()` in types.ts) so nothing that already
 *  reads it breaks; `engagementRateByReach` is the new, additive counterpart. */
export function computeCalculatedMetrics(input: {
  views: number | null;
  reach: number | null;
  likes: number | null;
  comments: number | null;
  saves: number | null;
  shares: number | null;
  watchAvgSeconds?: number | null;
  reachByFollowerType?: { followers: number | null; nonFollowers: number | null } | null;
  durationSeconds?: number | null;
}): Record<string, CalculatedMetric> {
  const acts = (input.likes ?? 0) + (input.saves ?? 0) + (input.comments ?? 0) + (input.shares ?? 0);
  const hasAnyEngagementField =
    input.likes != null || input.saves != null || input.comments != null || input.shares != null;
  const engagementNumerator = hasAnyEngagementField ? acts : null;

  return {
    likeRateByReach: {
      value: rate(input.likes, input.reach),
      formula: "likes / reach",
      sourceFields: ["likes", "reach"],
    },
    commentRateByReach: {
      value: rate(input.comments, input.reach),
      formula: "comments / reach",
      sourceFields: ["comments", "reach"],
    },
    saveRateByReach: {
      value: rate(input.saves, input.reach),
      formula: "saves / reach",
      sourceFields: ["saves", "reach"],
    },
    shareRateByReach: {
      value: rate(input.shares, input.reach),
      formula: "shares / reach",
      sourceFields: ["shares", "reach"],
    },
    engagementRateByReach: {
      value: rate(engagementNumerator, input.reach),
      formula: "(likes + comments + saves + shares) / reach",
      sourceFields: ["likes", "comments", "saves", "shares", "reach"],
    },
    // Legacy — matches types.ts's pre-existing engagement()/saveRate() denominator
    // (views), preserved so no existing dashboard number changes because of this work.
    engagementRateByViews: {
      value: rate(engagementNumerator, input.views),
      formula: "(likes + comments + saves + shares) / views  — legacy, kept for continuity",
      sourceFields: ["likes", "comments", "saves", "shares", "views"],
    },
    nonFollowerReachRate: {
      value: rate(input.reachByFollowerType?.nonFollowers ?? null, input.reach),
      formula: "reachByFollowerType.nonFollowers / reach",
      sourceFields: ["reachByFollowerType.nonFollowers", "reach"],
    },
    watchPercentage: {
      value: rate(input.watchAvgSeconds ?? null, input.durationSeconds ?? null),
      formula: "watchAvgSeconds / durationSeconds",
      sourceFields: ["watchAvgSeconds", "durationSeconds"],
    },
  };
}
