/** Actually publishing to Instagram and YouTube — not just reading numbers back, which is
 *  all sources.ts ever did. Both platforms need something sources.ts's read-only setup
 *  didn't: Instagram needs the video at a public HTTPS URL it fetches itself (the reel's
 *  own page on this deployment is exactly that, once it's live); YouTube needs a real
 *  OAuth-authenticated upload, which a read-only YOUTUBE_API_KEY can never do — uploading
 *  as the channel owner requires a consent grant, once, from a human. */

import { sharedPool, loadState, saveState } from "./db";
import { igRoute, igToken } from "./sources";
import { SITE_URL } from "./site";
import { reels } from "./reels";

export { SITE_URL };

// ───────────────────────── Instagram ─────────────────────────

export type IgPublishResult =
  | { ok: true; mediaId: string; permalink: string | null }
  | { ok: false; reason: string; detail?: string };

/** The three-step container dance (create -> poll until processed -> publish) is
 *  identical for a Reel and for a Story; only media_type and whether a caption applies
 *  differ. Verified against Meta's own Content Publishing docs before writing this —
 *  there is no single "also post to Stories" flag on the Reels container (a few SEO
 *  blog posts claim a `share_to_story` parameter; it isn't in Meta's own reference and
 *  isn't used here), so a Story is genuinely its own container and its own publish. */
async function createAndPublishIgMedia(
  host: string,
  user: string,
  token: string,
  mediaType: "REELS" | "STORIES",
  videoUrl: string,
  caption?: string,
  timeoutMs = 45_000,
  thumbOffsetMs?: number,
): Promise<IgPublishResult> {
  const createUrl = new URL(`${host}/${user}/media`);
  createUrl.searchParams.set("media_type", mediaType);
  createUrl.searchParams.set("video_url", videoUrl);
  if (caption) createUrl.searchParams.set("caption", caption);
  if (thumbOffsetMs != null) createUrl.searchParams.set("thumb_offset", String(thumbOffsetMs));
  createUrl.searchParams.set("access_token", token);
  const created = await fetch(createUrl, { method: "POST", cache: "no-store" });
  const createdBody = (await created.json()) as { id?: string; error?: { message?: string } };
  if (!created.ok || !createdBody.id) {
    return { ok: false, reason: createdBody.error?.message ?? `יצירת המדיה נכשלה (${created.status})` };
  }
  const containerId = createdBody.id;

  // poll until Instagram has actually downloaded and processed the file — publishing
  // too early is the documented cause of a silent failure, not a fast one. The Reel
  // and Story publishes run back to back in one request (120s function budget), so
  // each gets its own share — Reels carries the real video and consistently needed
  // more than the 45s both used to get, which is why episode 21 failed here twice in
  // a row rather than as an occasional flake; a Story publish only ever runs after
  // the Reel already succeeded, so it can afford less.
  const deadline = Date.now() + timeoutMs;
  let status = "IN_PROGRESS";
  while (Date.now() < deadline) {
    const statusUrl = new URL(`${host}/${containerId}`);
    statusUrl.searchParams.set("fields", "status_code");
    statusUrl.searchParams.set("access_token", token);
    const r = await fetch(statusUrl, { cache: "no-store" });
    const j = (await r.json()) as { status_code?: string };
    status = j.status_code ?? status;
    if (status === "FINISHED" || status === "ERROR") break;
    await new Promise((res) => setTimeout(res, 3000));
  }
  if (status !== "FINISHED") {
    return { ok: false, reason: `אינסטגרם לא סיים לעבד את הווידאו (סטטוס: ${status})`, detail: containerId };
  }

  const publishUrl = new URL(`${host}/${user}/media_publish`);
  publishUrl.searchParams.set("creation_id", containerId);
  publishUrl.searchParams.set("access_token", token);
  const published = await fetch(publishUrl, { method: "POST", cache: "no-store" });
  const publishedBody = (await published.json()) as { id?: string; error?: { message?: string } };
  if (!published.ok || !publishedBody.id) {
    return { ok: false, reason: publishedBody.error?.message ?? `הפרסום נכשל (${published.status})` };
  }

  // best-effort permalink lookup — not fatal if it fails, the publish itself already succeeded
  let permalink: string | null = null;
  try {
    const permUrl = new URL(`${host}/${publishedBody.id}`);
    permUrl.searchParams.set("fields", "permalink");
    permUrl.searchParams.set("access_token", token);
    const pr = await fetch(permUrl, { cache: "no-store" });
    const pj = (await pr.json()) as { permalink?: string };
    permalink = pj.permalink ?? null;
  } catch {
    /* not fatal */
  }

  return { ok: true, mediaId: publishedBody.id, permalink };
}

export type IgFullPublishResult = {
  reel: IgPublishResult;
  /** Always null now — see the comment above publishToInstagram for why the API-made
   *  Story was dropped rather than kept as a fallback. Left in the type instead of
   *  removed so nothing downstream has to change shape over a feature that's gone. */
  story: IgPublishResult | null;
};

/** Every reel's hook plays the same word-by-word reveal (`START=0.15, GAP=0.10` per
 *  word, a 0.30s pop-in) before the first scene's static text has fully landed — frame
 *  0, which Instagram uses as the cover by default, is just the background with no
 *  caption on it yet. 1.8s clears that reveal for hooks up to ~10 words (the longest
 *  used so far) without yet reaching the scene's 4.5s-4.08s exit transition, so the
 *  cover Instagram picks shows the same fully-formed hook text every episode, without
 *  a manual "Edit thumbnail" step after each upload. */
const REEL_COVER_OFFSET_MS = 1800;

/** Publishes the Reel only. This used to also publish the same raw video file as a
 *  second, independent Story right after — technically real, but visibly worse than
 *  what he'd get by hand: Meta's Content Publishing API has no way to make the
 *  "share this post to your Story" sticker (confirmed against Meta's own docs —
 *  "Publishing stickers is not supported"), so the API version was a bare video with
 *  no link back to the Reel, while tapping Instagram's native "Share to Story" on the
 *  Reel itself produces the linked, branded version in five seconds. He asked for the
 *  automatic one to stop rather than keep shipping the worse one by default. */
export async function publishToInstagram(file: string, caption: string): Promise<IgFullPublishResult> {
  const token = await igToken();
  if (!token) return { reel: { ok: false, reason: "IG_ACCESS_TOKEN לא מוגדר" }, story: null };
  const { host, via } = igRoute(token);
  const user = process.env.IG_USER_ID || (via === "instagram-login" ? "me" : "");
  if (!user) return { reel: { ok: false, reason: "IG_USER_ID לא מוגדר" }, story: null };

  const videoUrl = `${SITE_URL}/reels/${encodeURIComponent(file)}`;
  const reel = await createAndPublishIgMedia(
    host, user, token, "REELS", videoUrl, caption, 75_000, REEL_COVER_OFFSET_MS,
  );
  return { reel, story: null };
}

// ───────────────────────── Facebook ─────────────────────────

export type FbPublishResult =
  | { ok: true; postId: string }
  | { ok: false; reason: string };

/** A genuinely separate platform, not a side effect of the Instagram call — Meta has no
 *  API parameter that cross-posts an Instagram Reel to a Facebook Page automatically
 *  (verified against Meta's own docs; that's a manual toggle inside the Instagram app
 *  only, not exposed to the Graph API). Posting needs its own token (`pages_manage_posts`
 *  scope for a Page, the equivalent user-level scope for a personal profile) — a separate
 *  credential from the Instagram user token, which is why this reads its own env vars
 *  and reports plainly when they're missing instead of quietly reusing the Instagram one.
 *
 *  Two real destinations exist side by side on purpose: `FB_PAGE_ID`/`FB_PAGE_ACCESS_TOKEN`
 *  is David's personal profile — where the real, existing audience and view history live,
 *  and where every episode has actually been publishing until now. `FB_BUSINESS_PAGE_ID`/
 *  `FB_BUSINESS_PAGE_ACCESS_TOKEN` is the separate "Actually works.ai" Page created
 *  7.9.2026 specifically because Meta's Graph API can only ever read view/follower
 *  numbers back from a Page, never a personal profile — a platform limitation, not
 *  something either token's permissions can fix. Publishing to both keeps the personal
 *  profile's real reach while giving the studio one place it can actually measure. */
async function publishToFacebookTarget(
  file: string,
  caption: string,
  pageId: string | undefined,
  pageToken: string | undefined,
  missingReason: string,
): Promise<FbPublishResult> {
  if (!pageId || !pageToken) return { ok: false, reason: missingReason };
  const videoUrl = `${SITE_URL}/reels/${encodeURIComponent(file)}`;

  // Episode 38 shipped through the plain `/{page-id}/videos` endpoint below and landed
  // 10 views on a Page with one follower, against David's own "usually hundreds" baseline
  // — while the same file's Instagram Reel tracked right along Instagram's own "typical
  // reel" line. A plain Page video post only ever reaches roughly its follower count; a
  // real Facebook Reel gets pushed through Facebook's separate Reels distribution
  // regardless of follower count, the same way Instagram's own Reels algorithm doesn't
  // require followers either. Meta's Reels Publishing API (verified against Meta's own
  // docs and its official Postman sample collection, 17.9.2026) is a genuinely different,
  // three-step endpoint — start a session, hand it the hosted file over rupload's own
  // host via a `file_url` header (no local bytes to hold in a serverless function),
  // then finish/publish — not a parameter on the endpoint already in use.
  const startUrl = new URL(`https://graph.facebook.com/v21.0/${pageId}/video_reels`);
  startUrl.searchParams.set("upload_phase", "start");
  startUrl.searchParams.set("access_token", pageToken);
  const startRes = await fetch(startUrl, { method: "POST", cache: "no-store" });
  const startBody = (await startRes.json()) as {
    video_id?: string;
    error?: { message?: string };
  };
  if (!startRes.ok || !startBody.video_id) {
    return { ok: false, reason: startBody.error?.message ?? `אתחול הריל נכשל (${startRes.status})` };
  }
  const videoId = startBody.video_id;

  const uploadRes = await fetch(`https://rupload.facebook.com/video-upload/v21.0/${videoId}`, {
    method: "POST",
    headers: { Authorization: `OAuth ${pageToken}`, file_url: videoUrl },
    cache: "no-store",
  });
  if (!uploadRes.ok) {
    const uploadBody = (await uploadRes.json().catch(() => ({}))) as { error?: { message?: string } };
    return { ok: false, reason: uploadBody.error?.message ?? `העלאת הריל נכשלה (${uploadRes.status})` };
  }

  const finishUrl = new URL(`https://graph.facebook.com/v21.0/${pageId}/video_reels`);
  finishUrl.searchParams.set("upload_phase", "finish");
  finishUrl.searchParams.set("video_id", videoId);
  finishUrl.searchParams.set("video_state", "PUBLISHED");
  finishUrl.searchParams.set("description", caption);
  finishUrl.searchParams.set("access_token", pageToken);
  const finishRes = await fetch(finishUrl, { method: "POST", cache: "no-store" });
  const finishBody = (await finishRes.json()) as { success?: boolean; error?: { message?: string } };
  if (!finishRes.ok || finishBody.success !== true) {
    return { ok: false, reason: finishBody.error?.message ?? `פרסום הריל נכשל (${finishRes.status})` };
  }
  return { ok: true, postId: videoId };
}

export async function publishToFacebook(file: string, caption: string): Promise<FbPublishResult> {
  return publishToFacebookTarget(
    file,
    caption,
    process.env.FB_PAGE_ID,
    process.env.FB_PAGE_ACCESS_TOKEN,
    "FB_PAGE_ID / FB_PAGE_ACCESS_TOKEN לא מוגדרים — זה חיבור נפרד מאינסטגרם",
  );
}

export async function publishToFacebookBusinessPage(file: string, caption: string): Promise<FbPublishResult> {
  return publishToFacebookTarget(
    file,
    caption,
    process.env.FB_BUSINESS_PAGE_ID,
    process.env.FB_BUSINESS_PAGE_ACCESS_TOKEN,
    "FB_BUSINESS_PAGE_ID / FB_BUSINESS_PAGE_ACCESS_TOKEN לא מוגדרים",
  );
}

export type FbBothPublishResult = { profile: FbPublishResult; page: FbPublishResult };

/** Publishes to both real destinations, independently — one failing must never hide or
 *  block the other succeeding, since they're unrelated credentials and unrelated audiences.
 *
 *  FB_PAGE_ID and FB_BUSINESS_PAGE_ID turned out to be the same Facebook Page (confirmed
 *  16.9.2026 — Business Settings and facebook.com/pages/?category=your_pages both list
 *  exactly one Page, "Actually works.ai"; the "personal profile" destination this env
 *  var pair was named for never existed as a separate Page). Posting the same video
 *  twice to the same Page isn't "both destinations," it's a duplicate — so this checks
 *  for that exact case first and posts once, mirroring the one real result into both
 *  fields rather than genuinely calling the Graph API twice for the same upload. */
export async function publishToFacebookBoth(file: string, caption: string): Promise<FbBothPublishResult> {
  if (process.env.FB_PAGE_ID && process.env.FB_PAGE_ID === process.env.FB_BUSINESS_PAGE_ID) {
    const page = await publishToFacebookBusinessPage(file, caption);
    return { profile: page, page };
  }
  const [profile, page] = await Promise.all([
    publishToFacebook(file, caption),
    publishToFacebookBusinessPage(file, caption),
  ]);
  return { profile, page };
}

// ───────────────────────── The one guarded entry point ─────────────────────────

export type EpisodePublishResult =
  | { ok: false; reason: string }
  | { ok: true; alreadyPublished: true; igPermalink: string | null }
  | {
      ok: true;
      alreadyPublished: false;
      reel: IgPublishResult;
      facebook: FbPublishResult | null;
      facebookPage: FbPublishResult | null;
    };

/** The single path both the manual "פרסם" button and the daily cron now go through —
 *  built 23.9.2026 after a real incident: a manual test call to the old bare
 *  file+caption endpoint published episode 45 a second time, with an empty caption,
 *  minutes after the legitimate daily cron had already published it correctly. Two
 *  separate code paths (the manual route and the cron route) each did their own
 *  version of "check caption, check gate, publish, maybe update state" — they'd
 *  already drifted (only the cron route cleared `queuedForPublish` or touched
 *  `status`/`igMediaId` at all; the manual route published and left the studio to
 *  find out later, best-effort, via the next /api/track pull matching on caption
 *  text — which is exactly the fragile link that let today's empty-caption post go
 *  untracked and the real one get confused for it).
 *
 *  Every real safety check lives here now, once: a gate-passed render must exist, a
 *  real caption must exist, and — the one that was missing entirely — an episode
 *  already marked `live` with a real `igMediaId` is refused outright rather than
 *  quietly published again. State is updated in the same request that publishes,
 *  not left for a later best-effort pull to reconstruct by matching text. */
export async function publishEpisode(episodeNumber: number): Promise<EpisodePublishResult> {
  const state = await loadState();
  if (!state) return { ok: false, reason: "אין מסד נתונים מוגדר" };
  const row = state.episodes.find((e) => e.number === episodeNumber);
  if (!row) return { ok: false, reason: `פרק ${episodeNumber} לא קיים בסטייט` };

  // The idempotency guard itself — this is the check today's incident shows was missing.
  if (row.status === "live" && row.igMediaId) {
    return { ok: true, alreadyPublished: true, igPermalink: row.igPermalink ?? null };
  }

  const reel = reels().find((r) => r.kind === "video" && r.episode === episodeNumber && r.gate?.passed);
  if (!reel) return { ok: false, reason: `אין רנדר שעבר את השער לפרק ${episodeNumber}` };
  if (!reel.caption?.trim()) return { ok: false, reason: `אין קובץ כיתוב לפרק ${episodeNumber} — לא מפרסם בלי כיתוב` };

  const ig = await publishToInstagram(reel.file, reel.caption);
  const fb = ig.reel.ok ? await publishToFacebookBoth(reel.file, reel.caption) : null;

  // Write the real outcome into state from the same request that published, rather than
  // waiting on the next /api/track pull to reconstruct it by matching caption text —
  // that match is best-effort and is exactly what mis-linked today's incident. A save
  // conflict here (the cron and a manual click racing each other) is safe to drop: the
  // platform-side publish already happened either way, and the next /api/track pull
  // still backfills anything this request's write loses the race on.
  const loadedAt = state.updatedAt;
  const freshRow = state.episodes.find((e) => e.number === episodeNumber);
  if (freshRow) {
    if (ig.reel.ok) {
      freshRow.status = "live";
      freshRow.igMediaId = ig.reel.mediaId;
      freshRow.igPermalink = ig.reel.permalink;
      freshRow.publishedAt = new Date().toISOString().slice(0, 10);
    }
    freshRow.queuedForPublish = false;
  }
  state.updatedAt = new Date().toISOString();
  await saveState(state, loadedAt).catch(() => {});

  if (ig.reel.ok && process.env.CRON_SECRET) {
    await fetch(`${SITE_URL}/api/track`, {
      headers: { authorization: `Bearer ${process.env.CRON_SECRET}` },
    }).catch(() => {});
  }

  return { ok: true, alreadyPublished: false, reel: ig.reel, facebook: fb?.profile ?? null, facebookPage: fb?.page ?? null };
}

// ───────────────────────── YouTube ─────────────────────────

const GOOGLE_OAUTH = "https://accounts.google.com/o/oauth2/v2/auth";
const GOOGLE_TOKEN = "https://oauth2.googleapis.com/token";
const YT_UPLOAD = "https://www.googleapis.com/upload/youtube/v3/videos";

async function db() {
  const p = sharedPool();
  if (!p) return null;
  await p.query(`create table if not exists youtube_token (
    id int primary key default 1, refresh_token text not null,
    created_at timestamptz not null default now())`);
  return p;
}

function redirectUri(): string {
  return `${SITE_URL}/api/youtube/callback`;
}

/** The one-time consent link — only a human logged into the channel's Google account can
 *  complete this, which is exactly why it can't be automated further than "here's the
 *  link to click". */
export function youtubeAuthUrl(): { ok: true; url: string } | { ok: false; reason: string } {
  const clientId = process.env.GOOGLE_CLIENT_ID;
  if (!clientId) return { ok: false, reason: "GOOGLE_CLIENT_ID לא מוגדר" };
  const uri = redirectUri();
  const u = new URL(GOOGLE_OAUTH);
  u.searchParams.set("client_id", clientId);
  u.searchParams.set("redirect_uri", uri);
  u.searchParams.set("response_type", "code");
  u.searchParams.set("scope", "https://www.googleapis.com/auth/youtube.upload");
  u.searchParams.set("access_type", "offline");
  u.searchParams.set("prompt", "consent");
  return { ok: true, url: u.toString() };
}

export async function exchangeYoutubeCode(code: string): Promise<{ ok: true } | { ok: false; reason: string }> {
  const clientId = process.env.GOOGLE_CLIENT_ID;
  const clientSecret = process.env.GOOGLE_CLIENT_SECRET;
  if (!clientId || !clientSecret) return { ok: false, reason: "GOOGLE_CLIENT_ID/SECRET לא מוגדרים" };
  const body = new URLSearchParams({
    code, client_id: clientId, client_secret: clientSecret,
    redirect_uri: redirectUri(), grant_type: "authorization_code",
  });
  const r = await fetch(GOOGLE_TOKEN, { method: "POST", body, cache: "no-store" });
  const j = (await r.json()) as { refresh_token?: string; error_description?: string; error?: string };
  if (!r.ok || !j.refresh_token) {
    // Google omits refresh_token on a repeat consent unless prompt=consent forced a new
    // one — already set above, but worth naming if it still happens
    return { ok: false, reason: j.error_description ?? j.error ?? `Google החזיר ${r.status}` };
  }
  const p = await db();
  if (!p) return { ok: false, reason: "אין מסד נתונים לשמור בו את הטוקן" };
  await p.query(
    `insert into youtube_token (id, refresh_token) values (1, $1)
     on conflict (id) do update set refresh_token = $1, created_at = now()`,
    [j.refresh_token],
  );
  return { ok: true };
}

export async function youtubeConnected(): Promise<boolean> {
  const p = await db();
  if (!p) return false;
  const r = await p.query("select 1 from youtube_token where id = 1");
  return (r.rowCount ?? 0) > 0;
}

async function youtubeAccessToken(): Promise<{ ok: true; token: string } | { ok: false; reason: string }> {
  const clientId = process.env.GOOGLE_CLIENT_ID;
  const clientSecret = process.env.GOOGLE_CLIENT_SECRET;
  if (!clientId || !clientSecret) return { ok: false, reason: "GOOGLE_CLIENT_ID/SECRET לא מוגדרים" };
  const p = await db();
  if (!p) return { ok: false, reason: "אין מסד נתונים" };
  const r = await p.query<{ refresh_token: string }>("select refresh_token from youtube_token where id = 1");
  const refreshToken = r.rows[0]?.refresh_token;
  if (!refreshToken) return { ok: false, reason: "YouTube לא מחובר עדיין — צריך לאשר גישה פעם אחת" };
  const body = new URLSearchParams({
    refresh_token: refreshToken, client_id: clientId, client_secret: clientSecret,
    grant_type: "refresh_token",
  });
  const tr = await fetch(GOOGLE_TOKEN, { method: "POST", body, cache: "no-store" });
  const tj = (await tr.json()) as { access_token?: string; error_description?: string };
  if (!tr.ok || !tj.access_token) return { ok: false, reason: tj.error_description ?? `Google החזיר ${tr.status}` };
  return { ok: true, token: tj.access_token };
}

export type YtPublishResult = { ok: true; videoId: string } | { ok: false; reason: string };

/** Uploads the reel's own file bytes — read straight from the deployment's bundled public
 *  folder, the same file /renders already serves — as a resumable-simple upload. A
 *  vertical video under 3 minutes is *eligible* to be a Short, but the first real
 *  upload through this endpoint (1.9.2026, episode 11 — the first publish since
 *  YouTube OAuth was actually connected) landed as a regular video, not a Short, even
 *  though episodes 1-10 (uploaded by hand, directly in YouTube Studio) all show as
 *  Shorts. The difference is the upload path, not the video itself: YouTube's Shorts
 *  classification for an API upload is unreliable without the #Shorts tag in the
 *  title or description — manual uploads through youtube.com don't need it, API
 *  uploads do. Appended here, once, so every future publish gets it regardless of
 *  what the caller's own description text happens to include. */
export async function publishToYoutube(
  fileBytes: Buffer,
  title: string,
  description: string,
): Promise<YtPublishResult> {
  const auth = await youtubeAccessToken();
  if (!auth.ok) return auth;

  const taggedDescription = /#shorts\b/i.test(description)
    ? description
    : `${description}${description ? "\n\n" : ""}#Shorts`;
  const metadata = {
    snippet: { title: title.slice(0, 100), description: taggedDescription },
    status: { privacyStatus: "public" },
  };
  const boundary = "aw_boundary_" + Date.now();
  const body = Buffer.concat([
    Buffer.from(
      `--${boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n${JSON.stringify(metadata)}\r\n` +
        `--${boundary}\r\nContent-Type: video/mp4\r\n\r\n`,
    ),
    fileBytes,
    Buffer.from(`\r\n--${boundary}--`),
  ]);

  const r = await fetch(`${YT_UPLOAD}?uploadType=multipart&part=snippet,status`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${auth.token}`,
      "Content-Type": `multipart/related; boundary=${boundary}`,
    },
    body,
  });
  const j = (await r.json()) as { id?: string; error?: { message?: string } };
  if (!r.ok || !j.id) return { ok: false, reason: j.error?.message ?? `ההעלאה נכשלה (${r.status})` };
  return { ok: true, videoId: j.id };
}
