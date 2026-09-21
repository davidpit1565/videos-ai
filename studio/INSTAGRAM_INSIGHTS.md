# Instagram Insights data layer

Added 22.9.2026. This is the historical, honest-about-what's-missing layer for
Instagram/Reel analytics — additive on top of the existing `/api/track` pull. Nothing
that worked before this landed stopped working; this document says exactly what's real,
what's attempted-but-unconfirmed, and what isn't collected at all.

## Where things live

- `studio/lib/types.ts` — the schema. `MetricStatus`, the new `Episode` fields (`reach`,
  `reachByFollowerType`, `watchAvgSeconds`/`watchTotalSeconds`/`watchReplays`/`watchPlays`,
  `publishedAtPrecise`), and the two new history types: `ReelInsightSnapshot`,
  `AccountInsightSnapshot`.
- `studio/lib/sources.ts` — `fetchInstagram()` (extended) and the new
  `fetchInstagramAccountInsights()`. All network calls live here.
- `studio/lib/insights.ts` — pure, network-free decision logic (dedup, calculated
  metrics). Unit-tested (`studio/lib/insights.test.ts`, run with `npm test`).
- `studio/app/api/track/impl.ts` — wires the above into the daily pull: applies new
  metrics onto each `Episode`, appends `ReelInsightSnapshot`/`AccountInsightSnapshot`
  entries, logs status tallies.

## Metric-by-metric

| Metric | Level | Available? | Source field | Status semantics |
|---|---|---|---|---|
| `views` | Reel | ✅ real | `insights?metric=views` (or `crossposted_views` if cross-posted) | was already correct before this change |
| `reach` | Reel | ✅ real, **now separate from views** | `insights?metric=reach` | Before 22.9.2026 this silently became `views` when `views` was null. Fixed — see `reachStatus`. |
| `likes`/`comments` | Reel | ✅ real | media object's `like_count`/`comments_count` | unchanged |
| `saves`/`shares` | Reel | ✅ real | `insights?metric=saved,shares` | unchanged |
| `reachByFollowerType` (followers/non-followers) | Reel | ⚠️ experimental | `insights?metric=reach&breakdown=follow_type` | Real Graph API parameter, implemented and deployed, but only *confirmed* working against this specific account/API-version/token after a live production pull — see "Verification" below. Never derived by subtraction. |
| `watchAvgSeconds`/`watchTotalSeconds`/`watchReplays`/`watchPlays` | Reel | ⚠️ experimental | `insights?metric=ig_reels_avg_watch_time,ig_reels_video_view_total_time,clips_replays_count,ig_reels_aggregated_all_plays_count` | Same caveat as above — real metric names for Graph API v21 Reels insights, confirmed or rejected by the actual response, not assumed from docs. |
| Completion rate / retention curve | Reel | ❌ NOT_AVAILABLE | — | Instagram's public Graph API does not expose a per-second retention curve for Reels; only the aggregate watch-time metrics above. |
| Profile visits / follows / unfollows attributed to a specific Reel | Reel | ❌ NOT_AVAILABLE | — | Instagram does not attribute these to an individual Reel via the Graph API. Only available at the account level (see below), never invented per-Reel. |
| Website/link clicks attributed to a Reel | Reel | ❌ NOT_AVAILABLE | — | Same reason. |
| `publishedAtPrecise` | Reel | ✅ real | media object's `timestamp` | Retroactive — every platform already returned a full ISO timestamp; this just stops truncating it to a date. |
| `followersCount` | Account | ✅ real | profile `followers_count` | unchanged, was already collected |
| `accountsReached`/`profileVisits`/`websiteClicks`/`follows` | Account | ⚠️ experimental | `/insights?metric=reach,profile_views,website_clicks,follows_and_unfollows&period=day` | New endpoint, never called before 22.9.2026. `follows_and_unfollows` is one combined count — `unfollows` stays `null` (no split without its own breakdown call, which isn't implemented). |
| Cover image / audio metadata | Reel | ❌ NOT_REQUESTED | — | Deliberately not implemented — analytics metrics were prioritized per this task's own instructions. |
| Facebook connection | — | independent | `fetchFacebook()` | Already ran in parallel with Instagram before this change; a Facebook failure has never affected the Instagram pull (see `Promise.all` in `impl.ts`). |

## Verification (do this after every deploy that touches insights)

`/api/track`'s JSON response now includes:

```json
{
  "igInsightsDebug": {
    "reachByFollowerTypeStatus": { "AVAILABLE": 12, "NOT_AVAILABLE": 8 },
    "watchStatus": { "AVAILABLE": 20 }
  },
  "igAccountInsights": {
    "accountsReachedStatus": "AVAILABLE",
    "profileVisitsStatus": "PERMISSION_REQUIRED",
    "websiteClicksStatus": "NOT_AVAILABLE",
    "followsStatus": "AVAILABLE"
  }
}
```

These tallies are the real, current answer for this account — read them (or the
equivalent `[instagram-insights]` lines in Vercel's runtime logs) after a deploy instead
of assuming the experimental metrics above work. If a status reads `PERMISSION_REQUIRED`
across the board for one of them, the fix is a Meta permission grant, not more code.

## Historical snapshots

- `state.reelInsightSnapshots[]` — one entry per episode per meaningful change (or every
  `INSTAGRAM_INSIGHTS_SNAPSHOT_DEDUPE_WINDOW` minutes, default 360, if nothing changed).
  Never overwritten or deleted. `snapshotType: "backfill"` marks an entry produced by a
  one-time backfill run rather than an ordinary pull — its `collectedAt` is the day the
  backfill ran, never the episode's real publish day.
- `state.accountInsightSnapshots[]` — one entry per day (same "update today's row" pattern
  the existing follower-count `Snapshot` type already used).

## Backfill (episodes 23–42)

No historical reach/watch-time data existed anywhere before this change, so there is
nothing to "recover" — episodes 23-42's `reachStatus`/`watchStatus` were `UNKNOWN` until
the next real `/api/track` pull, which populates them from Instagram's actual, current
numbers (not the numbers from the day each episode published — Instagram's insights API
only ever returns an item's current lifetime total, not a historical point). Each
episode's very first `reelInsightSnapshots` entry after this deploy is therefore its
current state, correctly kept apart from `publishedAt` (see `ReelInsightSnapshot`'s
comment in `types.ts`) — never presented as what the episode looked like on day one.

## Config

- `INSTAGRAM_INSIGHTS_ENABLED=false` — turns off the three new best-effort calls
  (follower-type breakdown, watch-time metrics, account insights) without a redeploy, if
  one of them ever behaves badly against the real account. The pre-existing pull (views,
  reach, likes, comments, saves, shares) is unaffected either way.
- `INSTAGRAM_INSIGHTS_SNAPSHOT_DEDUPE_WINDOW` — minutes between two snapshots for the
  same episode when nothing changed. Default 360.

## Known, honest gaps (not implemented)

- Per-second retention curve — not exposed by the Graph API for Reels at all.
- Per-Reel profile visits/follows/unfollows/link-click attribution — not exposed by the
  Graph API; only available account-wide.
- Retry-with-backoff for transient (429/5xx) failures — not implemented in this change.
  Today's behavior (an isolated per-media/per-account try/catch that degrades to a
  status rather than crashing) is safe, just not self-healing within a single pull; the
  next day's cron retries naturally.
- CSV/export endpoint — none existed before this change; none was added, to avoid
  building speculative infrastructure. The data is fully available via `/api/state`.
