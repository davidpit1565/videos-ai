import { NextResponse } from "next/server";
import { BEEHIIV_PUB, fetchInstagram, fetchBeehiiv, fetchYouTube } from "@/lib/sources";
import { deviceCount, publicKey } from "@/lib/push";
import { dbVar, loadState } from "@/lib/db";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** Twice now a connection was "set" and still did not work, and each time the loop cost a
 *  day: the value was pasted into the wrong Vercel environment, or it carried a newline, or
 *  the sibling variable was missing. This endpoint answers the only question that was ever
 *  actually in doubt — is the value THERE, on THIS deployment, and does the service accept
 *  it — without ever returning the value. Shape only: present, length, prefix, whitespace.
 *  It is public on purpose: a check I cannot read myself is a check that does not end the
 *  loop. */

type Shape = {
  set: boolean;
  length: number;
  /** the first two characters, which for a token are its public family prefix (EA…, IG…) */
  starts: string;
  /** the most common invisible cause: a copied trailing newline or space */
  edgeSpace: boolean;
  innerSpace: boolean;
};

function shape(v: string | undefined): Shape {
  const raw = v ?? "";
  return {
    set: raw.length > 0,
    length: raw.length,
    starts: raw.slice(0, 2),
    edgeSpace: raw !== raw.trim(),
    innerSpace: /\s/.test(raw.trim()),
  };
}

/** A variable reported missing has four possible causes and they need different fixes:
 *  saved under a slightly different name, saved to Preview instead of Production, saved on
 *  a different Vercel project, or never saved. "Not set" cannot tell them apart, and I
 *  guessed wrong once already — I said a redeploy would fix it and the next build still
 *  came back empty. So: the NAMES of variables that look related, which are not secrets,
 *  and the total count, which distinguishes "wrong project" from "wrong name". */
const RELATED = /BEEHIIV|BEEHIV|BEHIIV|NEWSLETTER|SUBSCRIB|^IG_|INSTAGRAM|ANTHROPIC|POSTGRES|DATABASE|STUDIO_PIN/i;

function relatedNames(): string[] {
  return Object.keys(process.env).filter((k) => RELATED.test(k)).sort();
}

export async function GET() {
  const [instagram, beehiiv, youtube] = await Promise.all([
    fetchInstagram(),
    fetchBeehiiv(),
    fetchYouTube(),
  ]);

  // The one question this endpoint couldn't answer: not "is the connection alive" but
  // "did the auto-link actually run, and what did it decide" — which used to be readable
  // only from inside the PIN, so diagnosing it needed a screenshot from him every time.
  // Nothing here is secret — episode numbers, titles and unlinked-post captions are
  // already public on the site itself; this just saves a round trip.
  const state = await loadState().catch(() => null);
  const episodes = state
    ? {
        total: state.episodes.length,
        live: state.episodes.filter((e) => e.status === "live").length,
        // the exact activity-feed labels a human would otherwise have to open /studio to read
        recentFlags: (state.activity ?? [])
          .filter(
            (f) =>
              f.label.startsWith("פוסט לא מקושר") ||
              f.label.startsWith("סרטון לא מקושר ביוטיוב") ||
              f.label.startsWith("אי-התאמה אפשרית"),
          )
          .slice(0, 20)
          .map((f) => ({ at: f.at, label: f.label })),
        lastPullAt: state.activity?.[0]?.at ?? null,
        // The full recent feed, not just the flagged subset — the only way to see when a
        // given episode's views field last actually changed, and by how much, instead of
        // guessing why a stored number looks frozen.
        recentActivity: (state.activity ?? []).slice(0, 40).map((f) => ({ at: f.at, label: f.label, value: f.value, delta: f.delta })),
        // Which real Instagram post every tracked episode is actually pulling its number
        // from — the only way to tell "linked to the right post" apart from "linked to
        // A post" without opening the database. Views/caption are already public on the
        // account itself, so showing them here is not exposing anything new.
        links: state.episodes
          .filter((e) => e.igMediaId)
          .map((e) => {
            const live = instagram.connected ? instagram.media.find((m) => m.id === e.igMediaId) : undefined;
            return {
              number: e.number,
              igMediaId: e.igMediaId,
              storedViews: e.views,
              liveViews: live ? live.views : "not in current fetch window",
              liveReach: live ? live.reach : undefined,
              publishedAt: e.publishedAt,
              title: e.title,
            };
          }),
      }
    : null;

  // Every real post/video on an account that the sync could not attach to any tracked
  // episode — its views never reach the total on /analytics, silently, however large
  // they are. This is the thing a screenshot of the grid could show him and the
  // dashboard total could not: exactly which posts are sitting outside the count, and
  // how many views each is missing. YouTube used to only surface this buried in the
  // activity feed as a "סרטון לא מקושר ביוטיוב" line — real, but one entry per pull, with
  // no titles or view counts beside it to actually act on.
  const unmatched = {
    instagram:
      state && instagram.connected
        ? instagram.media
            .filter((m) => !state.episodes.some((e) => e.igMediaId === m.id))
            .map((m) => ({
              id: m.id,
              caption: m.caption.slice(0, 200),
              views: m.views ?? m.reach,
              eLink: m.caption.toLowerCase().match(/\/e\/(\d+)/)?.[1] ?? null,
              timestamp: m.timestamp,
            }))
        : null,
    youtube:
      state && youtube.connected
        ? youtube.videos
            .filter((v) => !state.episodes.some((e) => e.ytVideoId === v.id))
            .map((v) => ({
              id: v.id,
              title: v.title,
              description: v.description.slice(0, 200),
              views: v.views,
              eLink: v.description.toLowerCase().match(/\/e\/(\d+)/)?.[1] ?? null,
              timestamp: v.publishedAt,
            }))
        : null,
  };

  // Whether notifications can work at all, readable from outside the PIN. The endpoints that
  // do the work are private, and correctly so — but that left no way to check them without
  // his password, which means the first sign of a problem would have been him pressing the
  // button and getting an error. The VAPID public key is public by design and the device count
  // is not sensitive; the private key is never touched here.
  let push: { ready: boolean; devices: number; keyPrefix: string | null; reason?: string };
  try {
    const key = await publicKey();
    push = {
      ready: !!key,
      devices: await deviceCount(),
      keyPrefix: key ? key.slice(0, 6) : null,
      ...(key ? {} : { reason: "no database, so no keypair and nowhere to keep a subscription" }),
    };
  } catch (e) {
    push = {
      ready: false,
      devices: 0,
      keyPrefix: null,
      reason: e instanceof Error ? e.message : String(e),
    };
  }

  return NextResponse.json({
    // Which deployment answered. A variable saved for Production only is simply absent
    // here when a preview URL answers, and that looked identical to "I never saved it".
    deployment: {
      env: process.env.VERCEL_ENV ?? "local",
      branch: process.env.VERCEL_GIT_COMMIT_REF ?? null,
      commit: (process.env.VERCEL_GIT_COMMIT_SHA ?? "").slice(0, 7) || null,
    },
    push,
    // names only, never values — this is what tells a typo apart from a wrong environment
    named: relatedNames(),
    // which publication id is actually in force, and whether it came from the environment or
    // from the built-in default. It is public, so it can be shown.
    beehiivPublication: { id: BEEHIIV_PUB, fromEnv: !!process.env.BEEHIIV_PUBLICATION_ID },
    totalVars: Object.keys(process.env).length,
    episodes,
    unmatched,
    vars: {
      IG_USER_ID: shape(process.env.IG_USER_ID),
      IG_ACCESS_TOKEN: shape(process.env.IG_ACCESS_TOKEN),
      BEEHIIV_API_KEY: shape(process.env.BEEHIIV_API_KEY),
      // Reported raw. This line used to fall back to the built-in default before measuring,
      // so it answered set:true for a variable that was not set — a diagnostic lying about
      // presence, which is the exact failure it exists to catch. The `named` list above was
      // the only thing telling the truth.
      BEEHIIV_PUBLICATION_ID: shape(process.env.BEEHIIV_PUBLICATION_ID),
      // the provider decides the name (Supabase POSTGRES_URL, Neon DATABASE_URL), so
      // report the one the app actually found rather than the one I guessed
      database: { varName: dbVar(), set: dbVar() !== null },
      ANTHROPIC_API_KEY: shape(process.env.ANTHROPIC_API_KEY),
      STUDIO_PIN: { set: (process.env.STUDIO_PIN ?? "").length > 0 },
    },
    // the live verdict from the services themselves, which is the only thing that counts
    live: {
      // `via` names which of Meta's two Instagram APIs the token was sent to. It is
      // derived from the token's own prefix, so a rejection now says whether the wrong
      // API was asked rather than only that the token was refused.
      instagram: instagram.connected
        ? {
            connected: true,
            via: instagram.via,
            username: instagram.username,
            followers: instagram.followers,
            canPublish: instagram.canPublish,
            publishReason: instagram.publishReason,
            // The pull caps at 4 pages / 100 items, newest first, on purpose — see the
            // comment in sources.ts. If the account's real total is past that, the oldest
            // posts silently fall outside every pull from then on, and their stored
            // numbers freeze forever no matter how many pulls run. This is the number that
            // tells the two apart instead of guessing from how stale a post looks.
            accountMediaCount: instagram.mediaCount,
            fetchedThisPull: instagram.media.length,
            // Surfaces what used to be invisible: a media item whose insights call
            // itself failed silently kept whatever view count was already stored, which
            // read identically to "the numbers just aren't moving." See lib/sources.ts's
            // IgMedia.insightsError.
            insightsFailures: instagram.media
              .filter((m) => m.insightsError)
              .map((m) => ({ id: m.id, error: m.insightsError })),
          }
        : {
            connected: false,
            via: instagram.via ?? null,
            reason: instagram.reason,
            detail: instagram.detail ?? null,
          },
      beehiiv: beehiiv.connected
        ? {
            connected: true,
            activeSubscribers: beehiiv.activeSubscribers,
            exact: beehiiv.exact,
            shape: beehiiv.shape,
          }
        : { connected: false, reason: beehiiv.reason, detail: beehiiv.detail ?? null },
      // Separate from /api/youtube/status on purpose: that endpoint reports the OAuth
      // publish connection (GOOGLE_CLIENT_ID/SECRET, a refresh token in the DB) — this is
      // the unrelated read-only stats fetch (YOUTUBE_API_KEY + CHANNEL_ID/HANDLE) that
      // fills in ytViews. "Connected" on one has never implied anything about the other,
      // and this endpoint used to say nothing about this half at all.
      youtube: youtube.connected
        ? {
            connected: true,
            channelTitle: youtube.channelTitle,
            subscribers: youtube.subscribers,
            fetchedVideos: youtube.videos.length,
          }
        : { connected: false, reason: youtube.reason, detail: youtube.detail ?? null },
    },
  });
}
