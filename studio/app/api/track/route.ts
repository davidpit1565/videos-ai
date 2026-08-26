import { whole } from "@/lib/whole";
import { NextResponse } from "next/server";
import { notify, notifyNewRenders, notifyEpisodeLive } from "@/lib/push";
import { hasDb, loadState, saveState } from "@/lib/db";
import { fetchBeehiiv, fetchInstagram, fetchYouTube, refreshInstagramToken} from "@/lib/sources";
import { ActivityEvent, State, uid } from "@/lib/types";
import { realTitleFor, captionTitleFor, reels } from "@/lib/reels";

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
  if (!fromCron && last && Date.now() - Date.parse(last.at) < 20 * 60 * 1000) {
    return NextResponse.json({
      ok: true,
      skipped: true,
      reason: "נמשך כבר בעשרים הדקות האחרונות",
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

  const [ig, bee, yt] = await Promise.all([fetchInstagram(), fetchBeehiiv(), fetchYouTube()]);

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
  // the public site showed the studio's own "פרק חדש" placeholder for weeks. The real
  // title exists the moment that file is written; this just stops requiring a human
  // to copy it a second time. Only fills a title that's missing or still the
  // placeholder, so a title he's since edited by hand is never overwritten.
  for (const e of state.episodes) {
    if (e.title && e.title !== "פרק חדש") continue;
    const real = realTitleFor(e.number);
    if (real) e.title = real;
  }

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
    const title = realTitleFor(r.episode) || captionTitleFor(r.episode) || `פרק ${r.episode}`;
    state.episodes.push({
      id: uid(), number: r.episode, title, format: "reel", status: "testing",
      topic: "", tested: true, publishedAt: null, igMediaId: null, igPermalink: null,
      ytVideoId: null, notes: "", views: null, likes: null, saves: null, comments: null,
      shares: null, subsAttributed: null,
    });
    existingNumbers.add(r.episode);
    fresh.push({
      id: uid(), at: now, source: "studio",
      label: `פרק ${r.episode} נוסף אוטומטית לרשימה · ${title}`,
      value: null, delta: null,
    });
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
  };
  type PlatformConfig = {
    key: "instagram" | "youtube";
    label: string;
    unmatchedPrefix: string;
    getId: (e: State["episodes"][number]) => string | null;
    setId: (e: State["episodes"][number], id: string | null) => void;
    setPermalinkIfMissing: (e: State["episodes"][number], p: string | null) => void;
    setPermalink: (e: State["episodes"][number], p: string | null) => void;
    viewsNoteLabel: (n: number) => string;
    savesNoteLabel: ((n: number) => string) | null;
  };

  const syncPlatform = (media: LinkableMedia[], cfg: PlatformConfig) => {
    const byId = new Map(media.map((m) => [m.id, m]));
    for (const e of state.episodes) {
      const id = cfg.getId(e);
      const m = id ? byId.get(id) : undefined;
      if (!m) continue;
      note(cfg.key, cfg.viewsNoteLabel(e.number), m.views, e.views);
      if (cfg.savesNoteLabel && m.saves != null) note(cfg.key, cfg.savesNoteLabel(e.number), m.saves, e.saves);
      e.views = m.views ?? e.views;
      e.likes = m.likes ?? e.likes;
      e.saves = m.saves ?? e.saves;
      e.comments = m.comments ?? e.comments;
      e.shares = m.shares ?? e.shares;
      // backfilled for episodes linked before this field existed — the permalink is what
      // the episode page's embed needs, the media id alone can't build a URL.
      cfg.setPermalinkIfMissing(e, m.permalink);
      if (!e.publishedAt && m.timestamp) e.publishedAt = m.timestamp.slice(0, 10);
      if (e.status !== "live") { e.status = "live"; newlyLive.push(e.number); }
    }

    // Every caption/description we write ends with "actually-works-studio.vercel.app/e/N"
    // — an exact, unambiguous episode number. Title matching (against the real
    // YouTube-file title when the studio's own title field is still the "פרק חדש"
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
        e.views = m.views ?? e.views;
        e.likes = m.likes ?? e.likes;
        e.saves = m.saves ?? e.saves;
        e.comments = m.comments ?? e.comments;
        e.shares = m.shares ?? e.shares;
        if (!e.publishedAt && m.timestamp) e.publishedAt = m.timestamp.slice(0, 10);
        if (e.status !== "live") { e.status = "live"; newlyLive.push(e.number); }
        linked.add(m.id);
        fresh.push({
          id: uid(), at: now, source: cfg.key,
          label: `פוסט קושר אוטומטית לפרק ${e.number} · ${e.title}`,
          value: m.views ?? null, delta: null,
        });
      }
    }

    // A link can be wrong even when one already exists — reel 13 showed "already
    // published" while reel 11's real post sat unlinked, because 13's row was carrying
    // 11's actual Instagram media id (a manual mislink in /videos' "link to episode"
    // dropdown, the two numbers one row apart). Every caption/description we write names
    // its own episode with an explicit /e/N; that's ground truth the studio already has
    // and never checked against the episode a post is actually attached to. Move the
    // link onto the episode it actually names, whenever that episode exists and isn't
    // already carrying a different real link of its own — never onto one that is, so
    // this can't create a new wrong link while fixing an old one.
    const byMediaId = new Map(
      state.episodes.filter((e) => cfg.getId(e)).map((e) => [cfg.getId(e) as string, e]),
    );
    for (const m of media) {
      const wrong = byMediaId.get(m.id);
      if (!wrong) continue;
      const epLink = m.text.toLowerCase().match(/\/e\/(\d+)/);
      if (!epLink) continue;
      const correctNum = +epLink[1];
      if (correctNum === wrong.number) continue;
      const correct = state.episodes.find((e) => e.number === correctNum);
      if (!correct || cfg.getId(correct)) continue;
      cfg.setId(correct, m.id);
      cfg.setPermalink(correct, m.permalink);
      correct.views = wrong.views;
      correct.likes = wrong.likes;
      correct.saves = wrong.saves;
      correct.comments = wrong.comments;
      correct.shares = wrong.shares;
      correct.publishedAt = wrong.publishedAt;
      correct.status = "live";
      // The reassigned episode is going live for the first time from the site's
      // perspective — without this, the public "episode is live" push below never
      // fires for it, and a repair through this path looks like it did nothing.
      newlyLive.push(correct.number);
      cfg.setId(wrong, null);
      cfg.setPermalink(wrong, null);
      wrong.views = null;
      wrong.likes = null;
      wrong.saves = null;
      wrong.comments = null;
      wrong.shares = null;
      wrong.publishedAt = null;
      wrong.status = "testing";
      fresh.push({
        id: uid(), at: now, source: "studio",
        label: `פרק ${wrong.number} הוצג בטעות כמפורסם ב${cfg.label} — הפוסט שייך בפועל לפרק ${correct.number} (לפי הקישור בכיתוב) והועבר אליו`,
        value: null, delta: null,
      });
    }

    // content that exists on the account and is not linked to an episode is worth saying once
    const said = new Set(feed.filter((f) => f.label.startsWith(cfg.unmatchedPrefix)).map((f) => f.label));
    for (const m of media) {
      if (linked.has(m.id)) continue;
      const label = `${cfg.unmatchedPrefix} · ${m.text.slice(0, 40) || m.id}`;
      if (said.has(label)) continue;
      fresh.push({ id: uid(), at: now, source: cfg.key, label, value: m.views ?? null, delta: null });
    }
  };

  if (ig.connected) {
    syncPlatform(
      ig.media.map((m) => ({
        id: m.id, text: m.caption, permalink: m.permalink, timestamp: m.timestamp,
        views: m.views ?? m.reach, likes: m.likes, saves: m.saves,
        comments: m.comments, shares: m.shares,
      })),
      {
        key: "instagram",
        label: "אינסטגרם",
        unmatchedPrefix: "פוסט לא מקושר",
        getId: (e) => e.igMediaId,
        setId: (e, id) => { e.igMediaId = id; },
        setPermalinkIfMissing: (e, p) => { if (!e.igPermalink && p) e.igPermalink = p; },
        setPermalink: (e, p) => { e.igPermalink = p; },
        viewsNoteLabel: (n) => `פרק ${n} · צפיות`,
        savesNoteLabel: (n) => `פרק ${n} · שמירות`,
      },
    );
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
        viewsNoteLabel: (n) => `פרק ${n} · צפיות ביוטיוב`,
        savesNoteLabel: null,
      },
    );
  }

  // one snapshot a day, so the growth table stays a history and not a log
  const today = now.slice(0, 10);
  // Only an exact count is recorded. Beehiiv's list endpoint has no total, so past one
  // page the number is a floor — and a floor written into a snapshot becomes a number
  // nobody can tell apart from a measured one.
  const subs = bee.connected && bee.exact ? bee.activeSubscribers ?? null : prev?.subscribers ?? null;
  const fol = ig.connected ? ig.followers ?? null : prev?.igFollowers ?? null;
  if (prev?.date === today) {
    prev.subscribers = subs;
    prev.igFollowers = fol;
  } else {
    state.snapshots.push({
      id: uid(), date: today, subscribers: subs, igFollowers: fol,
      ytSubs: prev?.ytSubs ?? null, note: "נמדד אוטומטית",
    });
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
        label: `פרק ${e.number} סומן "פורסם" בלי קישור אמיתי לאינסטגרם או ליוטיוב — הוחזר ל"בדיקה"`,
        value: null, delta: null,
      });
    }
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
  if (fresh.length > 0) {
    const body =
      fresh.length === 1
        ? fresh[0].label
        : `${fresh.length} עדכונים: ${fresh.slice(0, 3).map((f) => f.label).join(", ")}${fresh.length > 3 ? "…" : ""}`;
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

  return NextResponse.json({
    ok: true,
    instagram: ig.connected ? { followers: ig.followers, posts: ig.media.length } : ig,
    beehiiv: bee.connected ? { subscribers: bee.activeSubscribers, exact: bee.exact } : bee,
    youtube: yt.connected ? { subscribers: yt.subscribers, videos: yt.videos.length } : yt,
    newEvents: fresh.length,
    activity: state.activity.slice(0, 40),
    checkedAt: now,
  });
}
