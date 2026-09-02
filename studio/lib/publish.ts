/** Actually publishing to Instagram and YouTube — not just reading numbers back, which is
 *  all sources.ts ever did. Both platforms need something sources.ts's read-only setup
 *  didn't: Instagram needs the video at a public HTTPS URL it fetches itself (the reel's
 *  own page on this deployment is exactly that, once it's live); YouTube needs a real
 *  OAuth-authenticated upload, which a read-only YOUTUBE_API_KEY can never do — uploading
 *  as the channel owner requires a consent grant, once, from a human. */

import { sharedPool } from "./db";
import { igRoute, igToken } from "./sources";
import { SITE_URL } from "./site";

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
): Promise<IgPublishResult> {
  const createUrl = new URL(`${host}/${user}/media`);
  createUrl.searchParams.set("media_type", mediaType);
  createUrl.searchParams.set("video_url", videoUrl);
  if (caption) createUrl.searchParams.set("caption", caption);
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
  /** null when the reel itself failed — a story of a post that doesn't exist yet isn't attempted */
  story: IgPublishResult | null;
};

/** Publishes the Reel, then — same video, same account, same confirm click he already
 *  gave — also publishes it as a Story. Two independent Graph API objects under the
 *  hood, run as one action because that's how he asked for it to work. The Story
 *  attempt only fires after the Reel really is live, and its own failure never hides
 *  or rolls back a successful Reel publish. */
export async function publishToInstagram(file: string, caption: string): Promise<IgFullPublishResult> {
  const token = await igToken();
  if (!token) return { reel: { ok: false, reason: "IG_ACCESS_TOKEN לא מוגדר" }, story: null };
  const { host, via } = igRoute(token);
  const user = process.env.IG_USER_ID || (via === "instagram-login" ? "me" : "");
  if (!user) return { reel: { ok: false, reason: "IG_USER_ID לא מוגדר" }, story: null };

  const videoUrl = `${SITE_URL}/reels/${encodeURIComponent(file)}`;
  const reel = await createAndPublishIgMedia(host, user, token, "REELS", videoUrl, caption, 75_000);
  if (!reel.ok) return { reel, story: null };

  const story = await createAndPublishIgMedia(host, user, token, "STORIES", videoUrl, undefined, 35_000);
  return { reel, story };
}

// ───────────────────────── Facebook ─────────────────────────

export type FbPublishResult =
  | { ok: true; postId: string }
  | { ok: false; reason: string };

/** A genuinely separate platform, not a side effect of the Instagram call — Meta has no
 *  API parameter that cross-posts an Instagram Reel to a Facebook Page automatically
 *  (verified against Meta's own docs; that's a manual toggle inside the Instagram app
 *  only, not exposed to the Graph API). Posting to the Page needs the Page's own token
 *  (`pages_manage_posts` scope) — a separate credential from the Instagram user token,
 *  which is why this reads its own env vars and reports plainly when they're missing
 *  instead of quietly reusing the Instagram one. */
export async function publishToFacebook(file: string, caption: string): Promise<FbPublishResult> {
  const pageId = process.env.FB_PAGE_ID;
  const pageToken = process.env.FB_PAGE_ACCESS_TOKEN;
  if (!pageId || !pageToken) {
    return { ok: false, reason: "FB_PAGE_ID / FB_PAGE_ACCESS_TOKEN לא מוגדרים — זה חיבור נפרד מאינסטגרם" };
  }
  const videoUrl = `${SITE_URL}/reels/${encodeURIComponent(file)}`;
  const u = new URL(`https://graph.facebook.com/v21.0/${pageId}/videos`);
  u.searchParams.set("file_url", videoUrl);
  u.searchParams.set("description", caption);
  u.searchParams.set("access_token", pageToken);
  const r = await fetch(u, { method: "POST", cache: "no-store" });
  const j = (await r.json()) as { id?: string; error?: { message?: string } };
  if (!r.ok || !j.id) return { ok: false, reason: j.error?.message ?? `הפרסום לפייסבוק נכשל (${r.status})` };
  return { ok: true, postId: j.id };
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
