import { whole } from "@/lib/whole";
import { NextResponse } from "next/server";
import { notify, notifyNewRenders, notifyEpisodeLive } from "@/lib/push";
import { hasDb, loadState, saveState, subscribersByEpisode } from "@/lib/db";
import {
  fetchBeehiiv, fetchFacebook, fetchInstagram, fetchInstagramAccountInsights,
  fetchYouTube, refreshInstagramToken,
} from "@/lib/sources";
import { publishToFacebookBusinessPage } from "@/lib/publish";
import { ActivityEvent, AccountInsightSnapshot, MetricStatus, ReelInsightSnapshot, State, uid } from "@/lib/types";
import { realTitleFor, captionTitleFor, reels } from "@/lib/reels";
import { shouldSnapshot } from "@/lib/insights";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 60;


/**
 * The point of the whole system: nobody has to remember to write the numbers down.
 * Vercel's cron calls this once a day, and the app calls it when he pulls to refresh.
 * It reads Instagram and Beehiiv, records what changed since last time, and stops —
 * a number that did not move produces no entry, so the feed only ever shows news.
 */
export async function GET(req: Request) {
  const secret = process.env.CRON_SECRET;
  const auth = req.headers.get("authorization");
  const fromCron = Boolean(req.headers.get("x-vercel-cron")) || (secret && auth === `Bearer ${secret}`);

  // /api/track is classified CRON in lib/routes.ts, so middleware's PIN check skips it
  // for everyone — that's correct for Vercel's own cron call, which carries neither a
  // PIN cookie nor a browser. But it also means a manual (non-cron) call reaches this
  // far with no gate at all: anyone with the URL could trigger a real Instagram/Beehiiv
  // pull and a DB write. The pull he does from inside the studio always carries his PIN
  // cookie, so require it here for every call that isn't the real cron.
  const pin = process.env.STUDIO_PIN;
  if (!fromCron && pin) {
    const cookiePin = req.headers
      .get("cookie")
      ?.split(";")
      .map((c) => c.trim())
      .find((c) => c.startsWith("studio="))
      ?.slice("studio=".length);
    if (cookiePin !== pin) {
      return NextResponse.json({ ok: false, reason: "locked" }, { status: 401 });
    }
  }

  if (!hasDb()) {
    return NextResponse.json({
      ok: false,
      reason: "אין מסד נתונים, ולכן אין לאן לרשום. אחרי חיבור Postgres ופריסה חדשה זה יעבוד לבד.",
    });
  }

  const raw = (await loadState()) as State | null;
  const state = raw ? whole(raw) : null;
  if (!state) return NextResponse.json({ ok: false, reason: "לא נטען מצב מהמסד" });
  // Captured before any mutation below, so saveState can tell whether another writer
  // (the cron and a manual pull can genuinely overlap) landed a save in between.
  const loadedAt = state.updatedAt;

  const feed: ActivityEvent[] = state.activity ?? [];
  const last = feed[0];
  // Was 20 minutes, then 3 — he asked to shorten it after a fix he needed to see reflected
  // sat behind the cooldown for most of that window. Moved back up to 10: with view-count
  // notifications gone (see the push filter below), the only things a manual pull surfaces
  // now are followers/subscribers/likes, which don't move fast enough to need a 3-minute
  // poll, and the tighter interval was mostly buying YouTube's own noisy view-count jitter
  // more chances to page him.
  if (!fromCron && last && Date.now() - Date.parse(last.at) < 10 * 60 * 1000) {
    return NextResponse.json({
      ok: true,
      skipped: true,
      reason: "נמשך כבר בשלוש הדקות האחרונות",
      activity: feed.slice(0, 40),
    });
  }

  // Refresh before reading, only on the cron's run. An Instagram-Login token dies at 60 days
  // and nothing was keeping it alive, which is why the connection broke twice and both repairs
  // were manual. Refreshed daily it never gets close to expiring.
  if (fromCron) {
    const rt = await refreshInstagramToken();
    if (rt.ok) console.log(`[track] instagram token refreshed, ${rt.expiresInDays}d left`);
    else console.log(`[track] instagram token not refreshed: ${rt.reason}`);
  }

  const [ig, bee, yt, fb, igAccount] = await Promise.all([
    fetchInstagram(), fetchBeehiiv(), fetchYouTube(), fetchFacebook(), fetchInstagramAccountInsights(),
  ]);
  // Temporary diagnostic for the brand-new Facebook integration: readable in Vercel's
  // own runtime logs, so a connection failure can be root-caused without needing his
  // PIN to read the JSON response body. Remove once a real pull has been confirmed
  // connected at least once.
  console.log(
    fb.connected
      ? `[track] facebook: connected (${fb.followers ?? "?"} followers, ${fb.videos.length} videos)`
      : `[track] facebook: NOT connected — ${fb.reason}${fb.detail ? " — " + fb.detail : ""}`,
  );

  // Tell him the day a connection breaks, not whenever he next opens the studio. This is the
  // half a refresh cannot cover: today's failure is Meta blocking the app, which no token
  // operation reaches, and it went unnoticed until he happened to look.
  if (!ig.connected) {
    void notify({
      title: "אינסטגרם לא מחובר",
      body: ig.reason + (ig.detail ? ` — ${ig.detail.slice(0, 90)}` : ""),
      url: "/studio",
      tag: "ig-down",
    }).catch(() => {});
  }
  if (!bee.connected) {
    void notify({
      title: "Beehiiv לא מחובר",
      body: bee.reason,
      url: "/studio",
      tag: "bee-down",
    }).catch(() => {});
  }
  const now = new Date().toISOString();
  const fresh: ActivityEvent[] = [];
  // Every field read off a stored state has to tolerate its own absence. activity was
  // guarded and snapshots was not, so any row written before the snapshots field existed
  // crashed the whole pull with "Cannot read properties of undefined (reading 'at')" —
  // which is why the studio showed no numbers at all rather than stale ones.
  const prev = state.snapshots.at(-1) ?? null;

  // He kept having to retype an episode's title into the studio by hand after it was
  // already finalized in channel/episode-0N-youtube.txt — and kept forgetting to, so
  // the public site showed the studio's own placeholder for weeks. The real title
  // exists the moment that file is written; this just stops requiring a human to copy
  // it a second time. Only fills a title that's missing or still the placeholder, so a
  // title he's since edited by hand is never overwritten. Checks both spellings of the
  // placeholder — "פרק חדש" is what older rows in the real database still carry from
  // before the "ריל" rename; renaming only the string this compares against would have
  // silently stopped healing every one of those rows.
  const PLACEHOLDER_TITLES = new Set(["ריל חדש", "פרק חדש"]);
  for (const e of state.episodes) {
    const best = realTitleFor(e.number) ?? captionTitleFor(e.number);
    if (!e.title || PLACEHOLDER_TITLES.has(e.title)) {
      if (best) e.title = best;
      continue;
    }
    if (!best) continue;
    // A row auto-linked before its youtube.txt existed fell back to a caption's raw
    // first line — and when that caption had no line break yet, "first line" was the
    // whole paragraph, so the stored title became the caption text, not a headline
    // ("Your AI agent is already lying to you. Not maliciously — it just doesn't know
    // how to say..." instead of "Your AI agent is already lying to you"). The correct
    // title exists now; nothing since has re-checked a title that already looked non-
    // empty. Healing is safe specifically because one is a plain prefix of the other —
    // two independently-written titles don't coincidentally share a long exact prefix,
    // so this can't be mistaken for a human's deliberate rename in /videos.
    const stored = e.title.trim().replace(/\.$/, "").toLowerCase();
    const freshTitle = best.trim().replace(/\.$/, "").toLowerCase();
    if (stored !== freshTitle && stored.length > 8 && freshTitle.length > 8 && (stored.startsWith(freshTitle) || freshTitle.startsWith(stored))) {
      e.title = best;
    }
  }

  // ONE-TIME repair, not a general mechanism — remove this block once it has run. Episode
  // 1 and 2's YouTube links were swapped, from before any of the checks above existed:
  // confirmed directly against YouTube's own oEmbed API (no guessing from local text),
  // which returned "What an AI agent actually is" — episode 2's real title — for the video
  // linked to episode 1, and "Your ChatGPT keeps giving you the obvious" — episode 1's
  // real title — for the video linked to episode 2. Hardcoded to these two specific,
  // externally-verified video ids on purpose: a generic "trust the algorithm" swap is
  // exactly what wiped a real episode's data earlier today, so this only ever touches the
  // two ids it was actually checked against, nothing inferred at runtime.
  {
    const WRONG_1 = "8LExf9nmW0w"; // really episode 2's video
    const WRONG_2 = "tdvxIK3KX64"; // really episode 1's video
    const e1 = state.episodes.find((e) => e.number === 1);
    const e2 = state.episodes.find((e) => e.number === 2);
    if (e1?.ytVideoId === WRONG_1 && e2?.ytVideoId === WRONG_2) {
      e1.ytVideoId = WRONG_2;
      e2.ytVideoId = WRONG_1;
      fresh.push({
        id: uid(), at: now, source: "studio",
        label: "פרק 1 ופרק 2 ביוטיוב היו מוחלפים — אומת מול היוטיוב עצמו ותוקן",
        value: null, delta: null,
      });
    }
  }

  // A "ONE-TIME repair" used to live here, unlinking episode 9 from Instagram media
  // 18163954408479206 on the claim that its caption read episode 6's title
  // ("Three things your AI agent still breaks on") rather than episode 9's own. That
  // claim was checked directly against the real caption and is false: the post's actual
  // caption is episode 9's own content verbatim ("This agent can send emails by itself.
  // It never does...") and its own text names /e/9. The repair had it backwards — this
  // was always episode 9's real, correctly-linked post, and the block spent every pull
  // since stripping it back off, discarding its real view count each time (191 views
  // sitting unlinked and invisible from every total in the studio). Removed entirely;
  // the ordinary auto-link below reattaches it on the next pull, same as any other post.

  // Every gated reel is a real, shipped episode, whether or not anyone ever pushed it
  // through /pipeline's "לצינור" button — lib/seed.ts only ever created rows 1 through
  // 6, and nothing since has created one for a number beyond that automatically. A
  // number with no row has nothing for the Instagram auto-link below to attach to, no
  // way to show "already published" on /renders, no line on /pipeline — the exact gap
  // that let reel-08 (and 9, 10, 11, 12) sit built, gated and even published, invisible
  // everywhere in the studio, because there was nothing in the list to update.
  const existingNumbers = new Set(state.episodes.map((e) => e.number));
  for (const r of reels()) {
    if (r.kind !== "video" || !r.gate?.passed || r.episode == null) continue;
    if (existingNumbers.has(r.episode)) continue;
    const title = realTitleFor(r.episode) || captionTitleFor(r.episode) || `ריל ${r.episode}`;
    state.episodes.push({
      id: uid(), number: r.episode, title, format: "reel", status: "testing",
      topic: "", tested: true, publishedAt: null, igMediaId: null, igPermalink: null,
      ytVideoId: null, notes: "", views: null, likes: null, saves: null, comments: null,
      shares: null, subsAttributed: null,
    });
    existingNumbers.add(r.episode);
    fresh.push({
      id: uid(), at: now, source: "studio",
      label: `ריל ${r.episode} נוסף אוטומטית לרשימה · ${title}`,
      value: null, delta: null,
    });
  }

  // Real per-episode attribution, replacing what used to be a number typed in by hand
  // with nothing behind it. /api/subscribe now records which episode page a signup
  // happened on; this just counts those rows and writes the real number onto each
  // episode, same as views/saves/likes already work.
  const attributed = await subscribersByEpisode();
  for (const e of state.episodes) {
    const count = attributed.get(e.number) ?? null;
    if (count !== null && count !== e.subsAttributed) {
      fresh.push({
        id: uid(), at: now, source: "studio",
        label: `${count} הרשמות מיוחסות לפרק ${e.number}`,
        value: count, delta: e.subsAttributed == null ? null : count - e.subsAttributed,
      });
      e.subsAttributed = count;
    }
  }

  const note = (
    source: ActivityEvent["source"], label: string,
    value: number | null, before: number | null | undefined,
  ) => {
    if (value == null) return;
    const delta = before == null ? null : value - before;
    if (delta === 0) return;             // no news is not an entry
    fresh.push({ id: uid(), at: now, source, label, value, delta });
  };

  if (ig.connected) note("instagram", "עוקבים באינסטגרם", ig.followers, prev?.igFollowers);
  if (bee.connected && bee.exact)
    note("beehiiv", "נרשמים לניוזלטר", bee.activeSubscribers, prev?.subscribers);
  // He asked for YouTube subscriber alerts too — turns out there was nothing to alert on:
  // yt.subscribers was fetched every pull and then discarded. The snapshot's own ytSubs
  // field only ever copied itself forward from the previous day's row (see below), so this
  // number has never actually been recorded, only silently re-saved as null forever.
  if (yt.connected) note("youtube", "עוקבים ביוטיוב", yt.subscribers, prev?.ytSubs);
  if (fb.connected) note("facebook", "עוקבים בפייסבוק", fb.followers, prev?.fbFollowers);

  // per-episode movement, so a video that keeps growing is visible without opening it.
  // Instagram and YouTube used to run this as two separately hand-written blocks — that's
  // exactly the kind of drift that let a fix land for one platform (the mislink-correction
  // pass below) and quietly never reach the other, which is its own real risk. One
  // function, run once per platform, keeps them provably doing the same thing.
  const newlyLive: number[] = [];
  type LinkableMedia = {
    id: string; text: string; permalink: string | null; timestamp: string | null;
    views: number | null; likes: number | null; saves: number | null;
    comments: number | null; shares: number | null;
    // Instagram-only extras — undefined for YouTube/Facebook, which never set them.
    reach?: number | null;
    reachByFollowerType?: { followers: number | null; nonFollowers: number | null };
    reachByFollowerTypeStatus?: MetricStatus;
    watchAvgSeconds?: number | null;
    watchTotalSeconds?: number | null;
    watchReplays?: number | null;
    watchStatus?: MetricStatus;
  };
  type PlatformConfig = {
    key: "instagram" | "youtube" | "facebook";
    label: string;
    unmatchedPrefix: string;
    getId: (e: State["episodes"][number]) => string | null;
    setId: (e: State["episodes"][number], id: string | null) => void;
    setPermalinkIfMissing: (e: State["episodes"][number], p: string | null) => void;
    setPermalink: (e: State["episodes"][number], p: string | null) => void;
    viewsNoteLabel: (n: number) => string;
    savesNoteLabel: ((n: number) => string) | null;
    // He asked for push alerts on likes and explicitly not on views — but no per-episode
    // like count was ever recorded as an activity event, only written silently onto the
    // episode row. Added so "likes" is a real, notifiable event and not just a number
    // sitting unannounced in /videos.
    likesNoteLabel: (n: number) => string;
    currentLikes: (e: State["episodes"][number]) => number | null;
    /** Where this platform's numbers actually live on the episode. Instagram and YouTube
     *  used to both write e.views/e.likes/e.comments — the same shared field — and since
     *  Instagram was synced first and YouTube second, YouTube's own, much smaller count
     *  silently overwrote Instagram's real one on every single pull for any episode with
     *  both linked. Confirmed against the activity feed: the same timestamp shows a real
     *  Instagram "ריל N · צפיות" write immediately followed by "ריל N · צפיות ביוטיוב"
     *  overwriting the same field. e.views/likes/saves/comments/shares are Instagram's own
     *  now (saves/shares have no YouTube equivalent, which was the tell); YouTube gets its
     *  own ytViews/ytLikes/ytComments so the two can never collide again. */
    currentViews: (e: State["episodes"][number]) => number | null;
    applyMetrics: (e: State["episodes"][number], m: LinkableMedia) => void;
  };

  const syncPlatform = (media: LinkableMedia[], cfg: PlatformConfig) => {
    const byId = new Map(media.map((m) => [m.id, m]));
    for (const e of state.episodes) {
      const id = cfg.getId(e);
      const m = id ? byId.get(id) : undefined;
      if (!m) continue;
      note(cfg.key, cfg.viewsNoteLabel(e.number), m.views, cfg.currentViews(e));
      if (cfg.savesNoteLabel && m.saves != null) note(cfg.key, cfg.savesNoteLabel(e.number), m.saves, e.saves);
      note(cfg.key, cfg.likesNoteLabel(e.number), m.likes, cfg.currentLikes(e));
      cfg.applyMetrics(e, m);
      // backfilled for episodes linked before this field existed — the permalink is what
      // the episode page's embed needs, the media id alone can't build a URL.
      cfg.setPermalinkIfMissing(e, m.permalink);
      if (!e.publishedAt && m.timestamp) e.publishedAt = m.timestamp.slice(0, 10);
      // Additive, precise counterpart to the date-only publishedAt above — every
      // platform's media object already carries a full ISO timestamp, so this
      // backfills retroactively for episodes linked before this field existed, not
      // just newly-linked ones. Never overwrites a value with an identical one (keeps
      // this out of the activity feed's noise), but does correct a stale one.
      if (m.timestamp && e.publishedAtPrecise !== m.timestamp) {
        e.publishedAtPrecise = m.timestamp;
        e.publishedAtPreciseStatus = "AVAILABLE";
      }
      if (e.status !== "live") { e.status = "live"; newlyLive.push(e.number); }
    }

    // Every caption/description we write ends with a "/e/N" link — actually-works.com
    // going forward, actually-works-studio.vercel.app on anything posted before the real
    // domain was live — an exact, unambiguous episode number either way, which is all
    // this regex looks for. Title matching (against the real
    // YouTube-file title when the studio's own title field is still the "ריל חדש"
    // placeholder) is the fallback ONLY for content with no /e/N at all — an older post,
    // or one written by hand without the link. An /e/N that IS present but doesn't
    // resolve to a real unlinked episode must never fall through to the fuzzy title
    // scan below it: that's a plain substring match with no word-boundary check, run
    // across every unlinked episode, and it can silently grab the wrong one even though
    // the content's own number was unambiguous ground truth. Only auto-links when
    // exactly one candidate matches, so an ambiguous case still falls through to the
    // manual path in /videos.
    const linked = new Set(state.episodes.map((e) => cfg.getId(e)).filter((x): x is string => !!x));
    const unlinkedEpisodes = state.episodes.filter((e) => !cfg.getId(e));
    for (const m of media) {
      if (linked.has(m.id)) continue;
      const text = m.text.toLowerCase();
      const epLink = text.match(/\/e\/(\d+)/);
      const hits = epLink
        ? unlinkedEpisodes.filter((e) => e.number === +epLink[1])
        : unlinkedEpisodes.filter((e) => {
            const title = (realTitleFor(e.number) || e.title || "").trim().toLowerCase();
            return title.length > 4 && text.includes(title);
          });
      if (hits.length === 1) {
        const e = hits[0];
        cfg.setId(e, m.id);
        cfg.setPermalink(e, m.permalink);
        cfg.applyMetrics(e, m);
        if (!e.publishedAt && m.timestamp) e.publishedAt = m.timestamp.slice(0, 10);
        if (m.timestamp && e.publishedAtPrecise !== m.timestamp) {
          e.publishedAtPrecise = m.timestamp;
          e.publishedAtPreciseStatus = "AVAILABLE";
        }
        if (e.status !== "live") { e.status = "live"; newlyLive.push(e.number); }
        linked.add(m.id);
        fresh.push({
          id: uid(), at: now, source: cfg.key,
          label: `פוסט קושר אוטומטית לריל ${e.number} · ${e.title}`,
          value: m.views ?? null, delta: null,
        });
      }
    }

    // A link can be wrong even when one already exists — reel 13 showed "already
    // published" while reel 11's real post sat unlinked, because 13's row was carrying
    // 11's actual Instagram media id (a manual mislink in /videos' "link to episode"
    // dropdown, the two numbers one row apart). Every caption/description we write names
    // its own episode with an explicit /e/N — but that's only ground truth about what
    // number the episode carried the DAY it was posted. An episode's number is a plain
    // editable field in /videos, so a post's own /e/N can legitimately go stale if the
    // episode was renumbered afterward — this used to almost never surface, because
    // captions were truncated to 120 characters before this check ever saw them, but
    // fixing that truncation (elsewhere in this change) means it now sees every real
    // number, including stale ones, and a swap-and-wipe here is destructive: it strips a
    // correctly-linked episode's real views/likes/saves and demotes it out of every live
    // count. Flagging the disagreement for a human to look at is the sound version of
    // this check; silently acting on it is not — no automatic swap, only a note in the
    // feed, until there's a way to confirm which number is actually current.
    const byMediaId = new Map(
      state.episodes.filter((e) => cfg.getId(e)).map((e) => [cfg.getId(e) as string, e]),
    );
    const flaggedMismatches = new Set(
      feed.filter((f) => f.label.startsWith(`אי-התאמה אפשרית ב${cfg.label}`)).map((f) => f.label),
    );
    for (const m of media) {
      const linkedEp = byMediaId.get(m.id);
      if (!linkedEp) continue;
      const epLink = m.text.toLowerCase().match(/\/e\/(\d+)/);
      if (!epLink) continue;
      const namedNum = +epLink[1];
      if (namedNum === linkedEp.number) continue;
      const label = `אי-התאמה אפשרית ב${cfg.label}: ריל ${linkedEp.number} מקושר לתוכן שהכיתוב שלו מציין ריל ${namedNum} — יכול להיות מספר ריל ישן, בדוק ב-/videos לפני שמתקנים`;
      if (flaggedMismatches.has(label)) continue;
      fresh.push({ id: uid(), at: now, source: "studio", label, value: null, delta: null });
    }

    // content that exists on the account and is not linked to an episode is worth saying once.
    // A generic "not linked" label used to be the only signal even when the content's own
    // /e/N names an episode that already has a DIFFERENT id linked — the exact shape of a
    // re-upload (a video deleted and re-posted, e.g. for a #Shorts fix) superseding an
    // older, now-stale link. That case looked identical to a genuinely unrelated post, so
    // finding it meant reading every unmatched item by hand. Name the conflict directly.
    const said = new Set(feed.filter((f) => f.label.startsWith(cfg.unmatchedPrefix)).map((f) => f.label));
    for (const m of media) {
      if (linked.has(m.id)) continue;
      const epLink = m.text.toLowerCase().match(/\/e\/(\d+)/);
      const claimedEp = epLink ? state.episodes.find((e) => e.number === +epLink[1]) : undefined;
      const label = claimedEp && cfg.getId(claimedEp)
        ? `${cfg.unmatchedPrefix} · names ריל ${claimedEp.number}, שכבר מקושר לפריט אחר — כנראה העלאה מחדש · ${m.text.slice(0, 40) || m.id}`
        : `${cfg.unmatchedPrefix} · ${m.text.slice(0, 40) || m.id}`;
      if (said.has(label)) continue;
      fresh.push({ id: uid(), at: now, source: cfg.key, label, value: m.views ?? null, delta: null });
    }
  };

  if (ig.connected) {
    syncPlatform(
      ig.media.map((m) => ({
        id: m.id, text: m.caption, permalink: m.permalink, timestamp: m.timestamp,
        // views and reach used to be folded together here (`views: m.views ?? m.reach`)
        // — a real reach number could silently become the displayed "views" whenever
        // Instagram's own views metric came back empty. Never again: they're two
        // entirely separate fields below, on the episode as much as here.
        views: m.views, likes: m.likes, saves: m.saves,
        comments: m.comments, shares: m.shares,
        reach: m.reach,
        reachByFollowerType: m.reachByFollowerType,
        reachByFollowerTypeStatus: m.reachByFollowerTypeStatus,
        watchAvgSeconds: m.watchAvgSeconds,
        watchTotalSeconds: m.watchTotalSeconds,
        watchReplays: m.watchReplays,
        watchStatus: m.watchStatus,
      })),
      {
        key: "instagram",
        label: "אינסטגרם",
        unmatchedPrefix: "פוסט לא מקושר",
        getId: (e) => e.igMediaId,
        setId: (e, id) => { e.igMediaId = id; },
        setPermalinkIfMissing: (e, p) => { if (!e.igPermalink && p) e.igPermalink = p; },
        setPermalink: (e, p) => { e.igPermalink = p; },
        viewsNoteLabel: (n) => `ריל ${n} · צפיות`,
        savesNoteLabel: (n) => `ריל ${n} · שמירות`,
        likesNoteLabel: (n) => `ריל ${n} · לייקים`,
        currentViews: (e) => e.views,
        currentLikes: (e) => e.likes,
        applyMetrics: (e, m) => {
          e.views = m.views ?? e.views;
          e.likes = m.likes ?? e.likes;
          e.saves = m.saves ?? e.saves;
          e.comments = m.comments ?? e.comments;
          e.shares = m.shares ?? e.shares;
          // Additive Instagram-only metrics — see LinkableMedia's comment above.
          if (m.reach !== undefined) {
            e.reach = m.reach;
            e.reachStatus = m.reach != null ? "AVAILABLE" : (e.reachStatus ?? "UNKNOWN");
          }
          if (m.reachByFollowerType !== undefined) e.reachByFollowerType = m.reachByFollowerType;
          if (m.reachByFollowerTypeStatus !== undefined) e.reachByFollowerTypeStatus = m.reachByFollowerTypeStatus;
          if (m.watchStatus !== undefined) {
            e.watchAvgSeconds = m.watchAvgSeconds ?? null;
            e.watchTotalSeconds = m.watchTotalSeconds ?? null;
            e.watchReplays = m.watchReplays ?? null;
            e.watchStatus = m.watchStatus;
          }
        },
      },
    );

    // Historical Reel insight snapshots — one point-in-time reading per episode, kept
    // forever (see ReelInsightSnapshot in types.ts), so a later question like "views
    // after 24 hours" can be answered without having overwritten the answer on the next
    // pull. Runs after syncPlatform above has already applied this pull's fresh numbers
    // onto each episode, so e.views/e.reach/etc. here are this moment's real values.
    // Deduplicated (shouldSnapshot) so the daily cron and a manual pull together don't
    // produce dozens of identical rows, but nothing here ever overwrites or deletes a
    // snapshot already written.
    const dedupeWindowMinutes = Number(process.env.INSTAGRAM_INSIGHTS_SNAPSHOT_DEDUPE_WINDOW ?? 360);
    state.reelInsightSnapshots = state.reelInsightSnapshots ?? [];
    for (const e of state.episodes) {
      if (!e.igMediaId) continue;
      const forEpisode = state.reelInsightSnapshots.filter((s) => s.episodeNumber === e.number);
      const last = forEpisode.at(-1);
      const next = {
        views: e.views ?? null, reach: e.reach ?? null, likes: e.likes ?? null,
        comments: e.comments ?? null, saves: e.saves ?? null, shares: e.shares ?? null,
        watchAvgSeconds: e.watchAvgSeconds ?? null, watchTotalSeconds: e.watchTotalSeconds ?? null,
        watchReplays: e.watchReplays ?? null,
      };
      if (shouldSnapshot(last, next, dedupeWindowMinutes, now)) {
        const snapshot: ReelInsightSnapshot = {
          id: uid(), episodeNumber: e.number, collectedAt: now,
          source: "instagram", snapshotType: "live", ...next,
        };
        state.reelInsightSnapshots.push(snapshot);
      }
    }
  }

  if (yt.connected) {
    syncPlatform(
      yt.videos.map((v) => ({
        id: v.id, text: v.description, permalink: `https://youtu.be/${v.id}`,
        timestamp: v.publishedAt, views: v.views, likes: v.likes, saves: null,
        comments: v.comments, shares: null,
      })),
      {
        key: "youtube",
        label: "יוטיוב",
        unmatchedPrefix: "סרטון לא מקושר ביוטיוב",
        getId: (e) => e.ytVideoId,
        setId: (e, id) => { e.ytVideoId = id; },
        setPermalinkIfMissing: () => {}, // no stored field — always derived from ytVideoId
        setPermalink: () => {},
        viewsNoteLabel: (n) => `ריל ${n} · צפיות ביוטיוב`,
        savesNoteLabel: null,
        likesNoteLabel: (n) => `ריל ${n} · לייקים ביוטיוב`,
        currentViews: (e) => e.ytViews ?? null,
        currentLikes: (e) => e.ytLikes ?? null,
        applyMetrics: (e, m) => {
          e.ytViews = m.views ?? e.ytViews ?? null;
          e.ytLikes = m.likes ?? e.ytLikes ?? null;
          e.ytComments = m.comments ?? e.ytComments ?? null;
        },
      },
    );
  }

  if (fb.connected) {
    syncPlatform(
      fb.videos.map((v) => ({
        id: v.id, text: v.description, permalink: v.permalink,
        timestamp: v.publishedAt, views: v.views, likes: v.likes, saves: null,
        comments: v.comments, shares: null,
      })),
      {
        key: "facebook",
        label: "פייסבוק",
        unmatchedPrefix: "סרטון לא מקושר בפייסבוק",
        getId: (e) => e.fbVideoId ?? null,
        setId: (e, id) => { e.fbVideoId = id; },
        setPermalinkIfMissing: (e, p) => { if (!e.fbPermalink && p) e.fbPermalink = p; },
        setPermalink: (e, p) => { e.fbPermalink = p; },
        viewsNoteLabel: (n) => `ריל ${n} · צפיות בפייסבוק`,
        savesNoteLabel: null,
        likesNoteLabel: (n) => `ריל ${n} · לייקים בפייסבוק`,
        currentViews: (e) => e.fbViews ?? null,
        currentLikes: (e) => e.fbLikes ?? null,
        applyMetrics: (e, m) => {
          e.fbViews = m.views ?? e.fbViews ?? null;
          e.fbLikes = m.likes ?? e.fbLikes ?? null;
          e.fbComments = m.comments ?? e.fbComments ?? null;
        },
      },
    );
  }

  // Auto-mirror to the Facebook business Page — asked for 17.9.2026 after Instagram's own
  // native cross-post (Accounts Center → Automatically Share) turned out to be wired to
  // his personal Facebook account, not the "Actually works.ai" Page, and there was no way
  // to repoint it there. He now uploads reels straight from Instagram's own app, bypassing
  // the studio's publish button entirely, so this is the only place left that ever sees a
  // reel go live and can react. Runs every pull (cron or manual), scoped to episodes the
  // Instagram sync just linked or re-confirmed (igMediaId set) that have no Facebook video
  // yet (fbVideoId null) — an episode already mirrored, by this or by the old manual
  // backfill, is never touched again, so a real API failure here just retries on the next
  // pull instead of double-posting on a rerun.
  const fbMirrorCandidates = state.episodes.filter((e) => e.igMediaId && !e.fbVideoId);
  for (const e of fbMirrorCandidates) {
    const r = reels().find((x) => x.episode === e.number && x.kind === "video" && x.gate?.passed);
    if (!r) continue;
    const igMedia = ig.connected ? ig.media.find((m) => m.id === e.igMediaId) : undefined;
    const caption = r.caption || igMedia?.caption || "";
    const result = await publishToFacebookBusinessPage(r.file, caption);
    if (result.ok) {
      e.fbVideoId = result.postId;
      fresh.push({
        id: uid(), at: now, source: "facebook",
        label: `ריל ${e.number} שוקף אוטומטית לפייסבוק (עמוד) אחרי שפורסם ישירות באינסטגרם`,
        value: null, delta: null,
      });
    } else {
      console.log(`[track] auto-mirror to facebook failed for episode ${e.number}: ${result.reason}`);
    }
  }

  // one snapshot a day, so the growth table stays a history and not a log
  const today = now.slice(0, 10);
  // Only an exact count is recorded. Beehiiv's list endpoint has no total, so past one
  // page the number is a floor — and a floor written into a snapshot becomes a number
  // nobody can tell apart from a measured one.
  const subs = bee.connected && bee.exact ? bee.activeSubscribers ?? null : prev?.subscribers ?? null;
  const fol = ig.connected ? ig.followers ?? null : prev?.igFollowers ?? null;
  // Was always prev?.ytSubs ?? null here — yt.subscribers is fetched above (used in the
  // response payload and now in the note() call) but never actually reached a snapshot;
  // every day's row just copied yesterday's (permanently null) value forward.
  const ytSubsVal = yt.connected ? yt.subscribers ?? null : prev?.ytSubs ?? null;
  const fbFollowersVal = fb.connected ? fb.followers ?? null : prev?.fbFollowers ?? null;
  if (prev?.date === today) {
    prev.subscribers = subs;
    prev.igFollowers = fol;
    prev.ytSubs = ytSubsVal;
    prev.fbFollowers = fbFollowersVal;
  } else {
    state.snapshots.push({
      id: uid(), date: today, subscribers: subs, igFollowers: fol,
      ytSubs: ytSubsVal, fbFollowers: fbFollowersVal, note: "נמדד אוטומטית",
    });
  }

  // Account-wide Instagram Insights (reach/profile visits/website clicks/follows),
  // kept apart from the follower-count-only Snapshot above — a genuinely new kind of
  // data this app never collected before 22.9.2026 (see fetchInstagramAccountInsights).
  // One entry a day, same "update if today already has one" pattern as the Snapshot
  // above; a not-yet-available metric is still worth recording as a real, dated
  // NOT_AVAILABLE/PERMISSION_REQUIRED/API_ERROR answer, not silently skipped.
  if (igAccount.attempted) {
    state.accountInsightSnapshots = state.accountInsightSnapshots ?? [];
    const prevAcc = state.accountInsightSnapshots.at(-1);
    const sameDay = prevAcc?.collectedAt.slice(0, 10) === today;
    const entry: AccountInsightSnapshot = {
      id: sameDay && prevAcc ? prevAcc.id : uid(),
      collectedAt: now,
      followersCount: fol,
      mediaCount: ig.connected ? ig.mediaCount : null,
      periodDays: igAccount.periodDays,
      accountsReached: igAccount.accountsReached,
      accountsReachedStatus: igAccount.accountsReachedStatus,
      profileVisits: igAccount.profileVisits,
      profileVisitsStatus: igAccount.profileVisitsStatus,
      websiteClicks: igAccount.websiteClicks,
      websiteClicksStatus: igAccount.websiteClicksStatus,
      follows: igAccount.follows,
      unfollows: igAccount.unfollows,
      followsStatus: igAccount.followsStatus,
    };
    if (sameDay) state.accountInsightSnapshots[state.accountInsightSnapshots.length - 1] = entry;
    else state.accountInsightSnapshots.push(entry);
  }

  // An episode can end up marked "live" without ever really being one — a manual
  // status edit in /videos, or an auto-link that later got its igMediaId cleared.
  // The homepage's "N episodes live" count and this page's own "already published"
  // badge both read status alone, so a stray row like that inflates a real number
  // silently — exactly what happened: 11 shown live, 10 actually on Instagram. Demote
  // rather than delete (never destroy a row nobody asked to lose) and say so in the
  // feed, once per episode, so it's a visible correction, not a silent rewrite.
  for (const e of state.episodes) {
    if (e.status === "live" && !e.igMediaId && !e.ytVideoId) {
      e.status = "testing";
      fresh.push({
        id: uid(), at: now, source: "studio",
        label: `ריל ${e.number} סומן "פורסם" בלי קישור אמיתי לאינסטגרם או ליוטיוב — הוחזר ל"בדיקה"`,
        value: null, delta: null,
      });
    }
  }

  // He asked directly (22.9.2026) for an automatic nudge so a gate-passed, tested
  // episode never just sits unpublished because he forgot — episodes 43/44 had done
  // exactly that with no error anywhere to explain it. Two checkpoints, each its own
  // one-time push ("must upload" at the short one, "reminder" at the long one), then
  // it repeats once a day past the long checkpoint for as long as the episode stays
  // untouched — "remind me if I forget" means it has to outlast one missed day.
  // Stops the moment a human either publishes it or ticks queuedForPublish — this never
  // publishes anything itself, only says so.
  //
  // Best-effort by construction, not by bug: this only runs when /api/track actually
  // runs — the daily cron, or him opening the studio. There is no hourly cron backing
  // this (he was asked and chose not to add a 4th cron job rather than risk the
  // account's cron-count limit), so the short checkpoint fires whenever /api/track
  // next happens to run after that many hours have passed, not necessarily on the dot.
  const REMINDER_CHECKPOINT_HOURS = (process.env.PUBLISH_REMINDER_CHECKPOINT_HOURS ?? "1,24")
    .split(",").map((s) => Number(s.trim())).filter((n) => Number.isFinite(n) && n > 0).sort((a, b) => a - b);
  const lastCheckpoint = REMINDER_CHECKPOINT_HOURS.at(-1) ?? 24;
  const staleUnpublished: { number: number; title: string; hoursSinceReady: number; first: boolean }[] = [];
  for (const e of state.episodes) {
    if (e.status === "live" || !e.tested || e.queuedForPublish) continue;
    const reel = reels().find((r) => r.kind === "video" && r.episode === e.number && r.gate?.passed);
    if (!reel) continue;
    const hoursSinceReady = (Date.parse(now) - Date.parse(reel.builtAt)) / 3_600_000;

    // The largest checkpoint this pull has actually crossed, if any — each checkpoint
    // fires exactly once, ever, per episode (not deduped by day like the repeat below).
    const crossed = [...REMINDER_CHECKPOINT_HOURS].reverse().find((h) => hoursSinceReady >= h);
    if (crossed !== undefined) {
      const checkpointLabel = `תזכורת: ריל ${e.number} מוכן ${crossed} שעות ולא פורסם ולא בתור לפרסום אוטומטי`;
      const alreadySaid = feed.some((f) => f.label === checkpointLabel);
      if (!alreadySaid) {
        fresh.push({ id: uid(), at: now, source: "studio", label: checkpointLabel, value: null, delta: null });
        staleUnpublished.push({ number: e.number, title: e.title, hoursSinceReady: crossed, first: crossed === REMINDER_CHECKPOINT_HOURS[0] });
        continue; // the checkpoint push already said it — don't also send the daily one below today
      }
    }

    // Past the last checkpoint (the "day" mark) and already reminded about it once —
    // keep nagging once a day, same dedupe shape as the account-insight snapshot above.
    if (hoursSinceReady < lastCheckpoint) continue;
    const dailyLabel = `תזכורת: ריל ${e.number} מוכן ${Math.floor(hoursSinceReady / 24)} ימים ולא פורסם ולא בתור לפרסום אוטומטי`;
    const saidToday = feed.some((f) => f.label === dailyLabel && f.at.slice(0, 10) === today);
    if (saidToday) continue;
    fresh.push({ id: uid(), at: now, source: "studio", label: dailyLabel, value: null, delta: null });
    staleUnpublished.push({ number: e.number, title: e.title, hoursSinceReady, first: false });
  }

  state.activity = [...fresh, ...feed].slice(0, 300);
  state.updatedAt = now;
  // Guarded against the cron and a manual pull genuinely overlapping — both start from
  // the same loaded row, so without this the one whose write lands second would silently
  // discard everything the other computed (new links, corrected mislinks, new episode
  // rows) with no error and no trace. Losing this run's write is safe: nothing external
  // was mutated, only the shared row, and the next cron/pull redoes the same work.
  const saved = await saveState(state, loadedAt);
  if (!saved.ok) {
    return NextResponse.json({
      ok: true,
      skipped: true,
      reason: "עדכון אחר נשמר במקביל — הריצה הזאת דולגה כדי לא לדרוס אותו",
      activity: feed.slice(0, 40),
    });
  }

  // He asked for a push on every new addition/pull, not just connection failures — a
  // pull that found nothing still ran, but only a pull that found something is news.
  //
  // View counts are recorded in `fresh` (and shown in the studio's own activity feed)
  // the same as before — this only decides what's worth interrupting his phone for. He
  // asked directly to stop being paged about views: YouTube's own view count isn't
  // strictly increasing in real time (it dips and recovers as YouTube's backend
  // recalculates and filters spam views), and polling it every few minutes surfaced that
  // churn as alarming-looking negative deltas that were never a real drop in anything.
  // Followers, newsletter subscribers, and likes move slowly enough that a change in
  // them is real news; a "-33" on a view count a minute after a "+33" almost never is.
  const NOTIFIABLE = ["עוקבים באינסטגרם", "עוקבים ביוטיוב", "נרשמים לניוזלטר", "· לייקים"];
  const notifiable = fresh.filter((f) => NOTIFIABLE.some((k) => f.label.includes(k)));
  if (notifiable.length > 0) {
    const body =
      notifiable.length === 1
        ? notifiable[0].label
        : `${notifiable.length} עדכונים: ${notifiable.slice(0, 3).map((f) => f.label).join(", ")}${notifiable.length > 3 ? "…" : ""}`;
    void notify({ title: "עדכון חדש", body, url: "/studio", tag: "activity" }).catch(() => {});
  }

  // And on every render that ships passing the gate — checked here rather than on its
  // own schedule, since a render only becomes visible to the live site at deploy time
  // anyway (the files are static, committed assets).
  void notifyNewRenders(
    reels()
      .filter((r) => r.gate?.passed && r.episode != null)
      .map((r) => ({ episode: r.episode as number, title: r.title })),
  ).catch(() => {});

  // The visitor-facing notification: only for an episode that just actually went live,
  // never for internal state (gate passes, subscriber counts) — that's what notify()
  // above sends, to the studio audience only.
  for (const num of newlyLive) {
    const e = state.episodes.find((x) => x.number === num);
    const title = realTitleFor(num) || e?.title || `Episode ${num}`;
    void notifyEpisodeLive(num, title).catch(() => {});
  }

  // The actual push for the "don't let me forget" reminder computed above — one per
  // day per stale episode, not bundled into the generic "עדכון חדש" notice above so it
  // reads as its own thing and can't get lost inside "3 עדכונים: ...".
  for (const s of staleUnpublished) {
    const age = s.hoursSinceReady < 24
      ? `${Math.round(s.hoursSinceReady)} שעות`
      : `${Math.floor(s.hoursSinceReady / 24)} ימים`;
    void notify({
      title: s.first ? `ריל ${s.number} חייב להתפרסם` : `ריל ${s.number} עדיין לא פורסם`,
      body: `${s.title} — מוכן כבר ${age}. סמן "תור לפרסום אוטומטי" או פרסם ידנית.`,
      url: "/renders",
      tag: `stale-${s.number}`,
    }).catch(() => {});
  }

  // How many of this pull's Instagram posts came back with no fresh metrics because
  // the insights call itself failed — previously invisible; a stuck-looking view count
  // and a real insights failure read identically without this. See lib/sources.ts's
  // IgMedia.insightsError for what's actually being reported here.
  const igInsightsFailures = ig.connected ? ig.media.filter((m) => m.insightsError) : [];

  // Debug summary for the new Instagram Insights layer — status tallies only, never a
  // token/header/raw payload. This is what a real production pull actually got back for
  // the follower-type breakdown, watch-time metrics, and account-level insights — the
  // only honest way to confirm whether Instagram supports them for this account/API
  // version, per this project's "don't assume, verify" rule.
  const tally = (values: (string | undefined)[]) => {
    const out: Record<string, number> = {};
    for (const v of values) out[v ?? "NOT_REQUESTED"] = (out[v ?? "NOT_REQUESTED"] ?? 0) + 1;
    return out;
  };
  const reachByFollowerTypeSample = ig.connected
    ? ig.media.find((m) => m.reachByFollowerTypeDebug)?.reachByFollowerTypeDebug
    : undefined;
  const igInsightsDebug = ig.connected
    ? {
        reachByFollowerTypeStatus: tally(ig.media.map((m) => m.reachByFollowerTypeStatus)),
        reachByFollowerTypeSample,
        watchStatus: tally(ig.media.map((m) => m.watchStatus)),
      }
    : undefined;
  console.log(`[instagram-insights] account insights: ${igAccount.attempted
    ? `reach=${igAccount.accountsReachedStatus} profileVisits=${igAccount.profileVisitsStatus} websiteClicks=${igAccount.websiteClicksStatus} follows=${igAccount.followsStatus}`
    : "not attempted (no token or disabled)"}`);
  if (igInsightsDebug) {
    console.log(`[instagram-insights] reel metrics: ${JSON.stringify(igInsightsDebug)}`);
  }

  return NextResponse.json({
    ok: true,
    instagram: ig.connected ? { followers: ig.followers, posts: ig.media.length } : ig,
    igInsightsFailures: igInsightsFailures.length
      ? { count: igInsightsFailures.length, sample: igInsightsFailures[0].insightsError }
      : undefined,
    igInsightsDebug,
    igAccountInsights: igAccount.attempted
      ? {
          accountsReachedStatus: igAccount.accountsReachedStatus,
          profileVisitsStatus: igAccount.profileVisitsStatus,
          websiteClicksStatus: igAccount.websiteClicksStatus,
          followsStatus: igAccount.followsStatus,
        }
      : { attempted: false },
    beehiiv: bee.connected ? { subscribers: bee.activeSubscribers, exact: bee.exact } : bee,
    youtube: yt.connected ? { subscribers: yt.subscribers, videos: yt.videos.length } : yt,
    facebook: fb.connected ? { followers: fb.followers, videos: fb.videos.length } : fb,
    newEvents: fresh.length,
    activity: state.activity.slice(0, 40),
    checkedAt: now,
  });
}
