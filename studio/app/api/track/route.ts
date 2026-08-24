import { whole } from "@/lib/whole";
import { NextResponse } from "next/server";
import { notify } from "@/lib/push";
import { hasDb, loadState, saveState } from "@/lib/db";
import { fetchBeehiiv, fetchInstagram, refreshInstagramToken} from "@/lib/sources";
import { ActivityEvent, State, uid } from "@/lib/types";
import { realTitleFor } from "@/lib/reels";

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
      if (!e.publishedAt && m.timestamp) e.publishedAt = m.timestamp.slice(0, 10);
      if (e.status !== "live") e.status = "live";
    }
    // a post that exists on the account and is not linked to an episode is worth saying once
    const linked = new Set(state.episodes.map((x) => x.igMediaId).filter(Boolean));
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

  return NextResponse.json({
    ok: true,
    instagram: ig.connected ? { followers: ig.followers, posts: ig.media.length } : ig,
    beehiiv: bee.connected ? { subscribers: bee.activeSubscribers, exact: bee.exact } : bee,
    newEvents: fresh.length,
    activity: state.activity.slice(0, 40),
    checkedAt: now,
  });
}
