import { whole } from "@/lib/whole";
import { NextResponse } from "next/server";
import { notify, notifyNewRenders, notifyEpisodeLive } from "@/lib/push";
import { hasDb, loadState, saveState } from "@/lib/db";
import { fetchBeehiiv, fetchInstagram, refreshInstagramToken} from "@/lib/sources";
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

  const [ig, bee] = await Promise.all([fetchInstagram(), fetchBeehiiv()]);

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

  // per-episode movement, so a video that keeps growing is visible without opening it
  const newlyLive: number[] = [];
  if (ig.connected) {
    const byId = new Map(ig.media.map((m) => [m.id, m]));
    for (const e of state.episodes) {
      const m = e.igMediaId ? byId.get(e.igMediaId) : undefined;
      if (!m) continue;
      note("instagram", `פרק ${e.number} · צפיות`, m.views ?? m.reach, e.views);
      note("instagram", `פרק ${e.number} · שמירות`, m.saves, e.saves);
      e.views = m.views ?? m.reach ?? e.views;
      e.likes = m.likes ?? e.likes;
      e.saves = m.saves ?? e.saves;
      e.comments = m.comments ?? e.comments;
      e.shares = m.shares ?? e.shares;
      // backfilled for episodes linked before this field existed — the permalink is what
      // the episode page's Instagram embed needs, the media id alone can't build a URL.
      if (!e.igPermalink && m.permalink) e.igPermalink = m.permalink;
      if (!e.publishedAt && m.timestamp) e.publishedAt = m.timestamp.slice(0, 10);
      if (e.status !== "live") { e.status = "live"; newlyLive.push(e.number); }
    }
    // Every caption we write ends with "actually-works-studio.vercel.app/e/N" — an
    // exact, unambiguous episode number, checked first. Title matching (against the
    // real YouTube-file title when the studio's own title field is still the "פרק
    // חדש" placeholder) is the fallback for older posts or a caption written by hand
    // without the link — he kept seeing the "not linked" note for posts that were
    // obviously the right episode from the caption alone, and had to go link them by
    // hand in /videos every time. Only auto-links when exactly one candidate matches,
    // so an ambiguous caption still falls through to the manual path.
    const linked = new Set(state.episodes.map((x) => x.igMediaId).filter(Boolean));
    const unlinkedEpisodes = state.episodes.filter((e) => !e.igMediaId);
    for (const m of ig.media) {
      if (linked.has(m.id)) continue;
      const caption = (m.caption || "").toLowerCase();
      const epLink = caption.match(/\/e\/(\d+)/);
      const byNumber = epLink ? unlinkedEpisodes.filter((e) => e.number === +epLink[1]) : [];
      const hits =
        byNumber.length === 1
          ? byNumber
          : unlinkedEpisodes.filter((e) => {
              const title = (realTitleFor(e.number) || e.title || "").trim().toLowerCase();
              return title.length > 4 && caption.includes(title);
            });
      if (hits.length === 1) {
        const e = hits[0];
        e.igMediaId = m.id;
        e.igPermalink = m.permalink;
        e.views = m.views ?? m.reach ?? e.views;
        e.likes = m.likes ?? e.likes;
        e.saves = m.saves ?? e.saves;
        e.comments = m.comments ?? e.comments;
        e.shares = m.shares ?? e.shares;
        if (!e.publishedAt && m.timestamp) e.publishedAt = m.timestamp.slice(0, 10);
        if (e.status !== "live") { e.status = "live"; newlyLive.push(e.number); }
        linked.add(m.id);
        fresh.push({
          id: uid(), at: now, source: "instagram",
          label: `פוסט קושר אוטומטית לפרק ${e.number} · ${e.title}`,
          value: m.views ?? null, delta: null,
        });
      }
    }
    // a post that exists on the account and is not linked to an episode is worth saying once
    const said = new Set(feed.filter((f) => f.label.startsWith("פוסט לא מקושר")).map((f) => f.label));
    for (const m of ig.media) {
      if (linked.has(m.id)) continue;
      const label = `פוסט לא מקושר · ${m.caption.slice(0, 40) || m.id}`;
      if (said.has(label)) continue;
      fresh.push({ id: uid(), at: now, source: "instagram", label, value: m.views ?? null, delta: null });
    }
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

  state.activity = [...fresh, ...feed].slice(0, 300);
  state.updatedAt = now;
  await saveState(state);

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
    newEvents: fresh.length,
    activity: state.activity.slice(0, 40),
    checkedAt: now,
  });
}
