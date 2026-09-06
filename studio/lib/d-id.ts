/** D-ID's Talks API — talking-head clips from a portrait + narration audio.
 *
 *  Same shape as studio/lib/higgsfield.ts (submit/poll split, same reasoning), chosen as
 *  the avatar-episode path instead of Higgsfield because it needs no paid credit balance
 *  and accepts audio up to 5 minutes per talk (Higgsfield caps at 15s per clip).
 *
 *  Verified against D-ID's own docs (docs.d-id.com/reference/createtalk,
 *  /reference/basic-authentication) — not guessed from another vendor's shape:
 *  - Endpoint: POST https://api.d-id.com/talks
 *  - Auth: HTTP Basic, base64("<api_key>") — D-ID issues the key already in
 *    "username:password" form from the dashboard; base64-encode that whole string.
 *  - Body fields are snake_case (source_url, audio_url), not camelCase.
 *  - The create call returns {id, status:"created"} immediately, never a finished
 *    video — result_url only appears once a poll shows status "done". */

const BASE_URL = "https://api.d-id.com";

function headers(): HeadersInit {
  const key = process.env.D_ID_API_KEY;
  if (!key) {
    throw new Error(
      "D_ID_API_KEY not set — add it in Vercel's project environment variables, the same " +
        "way every other secret in this app is kept out of chat and git. D-ID issues this " +
        "as a single 'username:password'-shaped string from the dashboard; store that " +
        "whole string as-is, this module base64-encodes it.",
    );
  }
  return {
    Authorization: `Basic ${Buffer.from(key).toString("base64")}`,
    "Content-Type": "application/json",
    Accept: "application/json",
  };
}

export async function submitTalk(params: {
  sourceUrl: string;
  audioUrl: string;
}): Promise<{ id?: string; status?: string; [k: string]: unknown }> {
  const r = await fetch(`${BASE_URL}/talks`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({
      source_url: params.sourceUrl,
      script: { type: "audio", audio_url: params.audioUrl, subtitles: false },
      // stitch:true — a natural, non-cropped full-frame result instead of just the
      // generated mouth region on its own.
      config: { stitch: true, result_format: "mp4", pad_audio: 0 },
    }),
  });
  const body = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(`D-ID submit failed: HTTP ${r.status} ${JSON.stringify(body).slice(0, 300)}`);
  return body;
}

/** One status check, not a blocking poll loop — same reasoning as higgsfield.ts's
 *  checkJobSet: the caller (the API route) is polled again by the client every few
 *  seconds instead of this function sleeping inside a single serverless invocation. */
export async function checkTalk(talkId: string): Promise<Record<string, unknown>> {
  const r = await fetch(`${BASE_URL}/talks/${talkId}`, { headers: headers() });
  const body = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(`D-ID status check failed: HTTP ${r.status} ${JSON.stringify(body).slice(0, 300)}`);
  return body;
}

export function talkPhase(data: Record<string, unknown>): "running" | "done" | "failed" {
  const status = String(data.status ?? "").toLowerCase();
  if (status === "done") return "done";
  if (status === "error" || status === "rejected") return "failed";
  return "running"; // created, started
}

/** result_url is the confirmed field name once status is "done" — not a best-effort
 *  guess the way higgsfield.ts's extractVideoUrl() is, since D-ID's own docs name this
 *  field directly. */
export function extractVideoUrl(data: Record<string, unknown>): string | null {
  const v = data.result_url;
  return typeof v === "string" && v ? v : null;
}
