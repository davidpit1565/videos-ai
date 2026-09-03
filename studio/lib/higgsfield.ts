/** Higgsfield's Speak v2 API — talking-head clips from a portrait + narration audio.
 *
 *  Ported from higgsfield/generate_talking_ad.py (PR #235) so the studio can trigger it
 *  without a human running a local script — but the same honesty rules from that script
 *  carry over unchanged:
 *
 *  - Endpoint, auth header shape, and the submit response's top-level shape ({"id",
 *    "type", "jobs"}) come from Higgsfield's own open-source MCP integration
 *    (github.com/QalaLabs/claude-higgsfield-mcp) — the closest thing to a public
 *    reference implementation, since the official docs site isn't scrapable.
 *  - NOT verified: the exact field path to the finished video's URL inside a completed
 *    job-set response. extractVideoUrl() tries the same plausible paths the Python
 *    script did and falls back to the raw JSON — if none of them hit on a real run, open
 *    the raw response, find the real field by hand, and fix this function. One real
 *    completed response is worth more than another guess.
 *
 *  Submit and poll are split into two functions, not one blocking call: a talking-head
 *  render can run past Vercel's function time limit, so the API route built on top of
 *  this submits once and returns immediately, and the client polls status on its own
 *  schedule — same shape as everywhere else in this app that waits on a slow job. */

const BASE_URL = "https://platform.higgsfield.ai";

function headers(): HeadersInit {
  const key = process.env.HF_API_KEY;
  const secret = process.env.HF_SECRET;
  if (!key || !secret) {
    throw new Error(
      "HF_API_KEY / HF_SECRET not set — add them in Vercel's project environment variables, " +
        "the same way every other secret in this app is kept out of chat and git.",
    );
  }
  return {
    Authorization: `Key ${key}:${secret}`,
    "Content-Type": "application/json",
    Accept: "application/json",
  };
}

export type HiggsfieldQuality = "high" | "mid";
export type HiggsfieldDuration = 5 | 10 | 15;

export async function submitTalkingHead(params: {
  imageUrl: string;
  audioUrl: string;
  prompt: string;
  quality?: HiggsfieldQuality;
  duration?: HiggsfieldDuration;
  seed?: number;
}): Promise<{ id?: string; type?: string; jobs?: unknown[]; [k: string]: unknown }> {
  const r = await fetch(`${BASE_URL}/v1/speak/higgsfield`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({
      params: {
        image_url: params.imageUrl,
        audio_url: params.audioUrl,
        prompt: params.prompt,
        quality: params.quality ?? "high",
        duration: params.duration ?? 5,
        seed: params.seed ?? 42,
      },
    }),
  });
  const body = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(`Higgsfield submit failed: HTTP ${r.status} ${JSON.stringify(body).slice(0, 300)}`);
  return body;
}

/** One status check, not a blocking poll loop — the caller (the API route) is called
 *  again by the client every few seconds instead of this function sleeping inside a
 *  single serverless invocation. */
export async function checkJobSet(jobSetId: string): Promise<Record<string, unknown>> {
  const r = await fetch(`${BASE_URL}/v1/job-sets/${jobSetId}`, { headers: headers() });
  const body = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(`Higgsfield status check failed: HTTP ${r.status} ${JSON.stringify(body).slice(0, 300)}`);
  return body;
}

const DONE = new Set(["completed", "succeeded", "done"]);
const FAILED = new Set(["failed", "error"]);

export function jobSetPhase(data: Record<string, unknown>): "running" | "done" | "failed" {
  const status = String(data.status ?? data.state ?? "").toLowerCase();
  if (DONE.has(status)) return "done";
  if (FAILED.has(status)) return "failed";
  return "running";
}

/** Best-effort only — see the module docstring. Same candidate list as the Python
 *  script, kept in sync by hand since there is nothing yet to generate it from. */
export function extractVideoUrl(result: Record<string, unknown>): string | null {
  const tryPaths: Array<(d: Record<string, unknown>) => unknown> = [
    (d) => (d.jobs as any)?.[0]?.results?.raw?.url,
    (d) => (d.jobs as any)?.[0]?.result?.url,
    (d) => (d.jobs as any)?.[0]?.output?.video_url,
    (d) => (d.result as any)?.video_url,
    (d) => d.output_url,
  ];
  for (const get of tryPaths) {
    try {
      const v = get(result);
      if (typeof v === "string" && v) return v;
    } catch {
      continue;
    }
  }
  return null;
}
