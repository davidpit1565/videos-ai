import { NextResponse } from "next/server";
import Anthropic from "@anthropic-ai/sdk";
import { engagement, saveRate, State } from "@/lib/types";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 60;

const SYSTEM = `You advise on an AI-education channel called Actually Works. Its promise is
setups a viewer can copy in two minutes, including what breaks. Content is in English and
is moving mainly to AI agents. The owner speaks Hebrew — answer in Hebrew.

The email list is the business: newsletter subscribers matter more than followers, because
sponsors pay per send and followers are rented from a platform.

Rules you must hold to:
- Answer only from the data given. If the data cannot support an answer, say which number is
  missing and what would produce it. Never invent a metric, a benchmark or a trend.
- Saves-per-view is the signal that matters for a "paste this" video: it means someone kept it.
  Views without saves mean the hook worked and the content did not.
- Be specific and short. Name the episode, the number, and the next action.
- If the honest answer is "there is not enough published yet to tell", say exactly that.`;

function brief(s: State) {
  const eps = s.episodes.map((e) => ({
    n: e.number, title: e.title, status: e.status, format: e.format, topic: e.topic,
    tested: e.tested, publishedAt: e.publishedAt,
    views: e.views, likes: e.likes, saves: e.saves, comments: e.comments,
    subsAttributed: e.subsAttributed,
    engagementPct: engagement(e) == null ? null : +(engagement(e)! * 100).toFixed(2),
    saveRatePct: saveRate(e) == null ? null : +(saveRate(e)! * 100).toFixed(2),
  }));
  const last = s.snapshots.at(-1);
  return JSON.stringify({
    episodes: eps,
    live: eps.filter((e) => e.status === "live").length,
    latestSnapshot: last ?? null,
    growth: s.snapshots.map((x) => ({ date: x.date, subs: x.subscribers, ig: x.igFollowers })),
    revenue: s.revenue.map((r) => ({ name: r.name, status: r.status, mrrEur: r.mrrEur })),
    // The idea-score agent (/api/idea-score) already scored some of these across 6
    // categories with a verdict — pass that along too, so "which idea should I do
    // next" is answered from the real evaluation already done, not blind to it.
    ideas: s.ideas.map((i) => ({ text: i.text, score: i.score ?? null })),
  });
}

export async function POST(req: Request) {
  if (!process.env.ANTHROPIC_API_KEY) {
    return NextResponse.json({
      ok: false,
      reason: "ANTHROPIC_API_KEY is not set — add it in Vercel → Settings → Environment Variables",
    });
  }
  let question = "";
  let state: State | null = null;
  try {
    const body = await req.json();
    question = String(body.question ?? "").slice(0, 2000);
    state = body.state ?? null;
  } catch {
    return NextResponse.json({ ok: false, reason: "bad request body" }, { status: 400 });
  }
  if (!question || !state) {
    return NextResponse.json({ ok: false, reason: "question and state are both required" }, { status: 400 });
  }

  try {
    const client = new Anthropic();

    // Streamed, and not for elegance. The previous version held the connection open for
    // up to 60 seconds without sending a single byte, and on a phone that is exactly
    // what gets killed: the server logged 200 while the browser reported "Load failed".
    // Streaming puts bytes on the wire immediately and keeps them coming, so neither
    // the platform nor the browser ever sees an idle socket. It is also what the API
    // documentation prescribes for any request with a large token allowance.
    const stream = client.beta.messages.stream({
      model: "claude-opus-5",
      max_tokens: 16000,
      thinking: { type: "adaptive" },
      output_config: { effort: "medium" },
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default",
      system: SYSTEM,
      messages: [
        { role: "user", content: `Studio data:\n${brief(state)}\n\nQuestion: ${question}` },
      ],
    });

    // Newline-delimited JSON: one object per line. Simpler than SSE to produce and to
    // read, and every line is independently parseable, so a truncated tail cannot
    // corrupt what already arrived.
    const enc = new TextEncoder();
    const body = new ReadableStream<Uint8Array>({
      async start(c) {
        const send = (o: unknown) => c.enqueue(enc.encode(JSON.stringify(o) + "\n"));
        // first byte before the model has said anything, so the socket is never idle
        send({ open: true });
        try {
          let any = false;
          for await (const ev of stream) {
            if (ev.type === "content_block_delta" && ev.delta.type === "text_delta") {
              if (ev.delta.text) {
                any = true;
                send({ t: ev.delta.text });
              }
            }
          }
          const final = await stream.finalMessage();
          if (final.stop_reason === "refusal") {
            send({ error: "the model declined this request" });
          } else if (!any) {
            // never finish silently: an empty answer is a failure with a named cause
            console.error(
              "[agent] empty answer",
              JSON.stringify({ stop: final.stop_reason, usage: final.usage }),
            );
            send({
              error:
                final.stop_reason === "max_tokens"
                  ? "The answer was cut off before it started — the allowance is too small."
                  : `No text came back (stop reason: ${final.stop_reason}).`,
            });
          } else {
            send({ done: true, stop: final.stop_reason });
          }
        } catch (e) {
          const raw = e instanceof Error ? e.message : String(e);
          console.error("[agent] stream failed", raw);
          // Connection-level failures arrive as one bare word — "terminated",
          // "fetch failed", "aborted" — which tells the reader nothing. Anything else
          // is passed through, because a real API message is worth reading.
          const network = /terminated|aborted|fetch failed|ECONNRESET|socket hang up/i.test(raw);
          send({
            error: network
              ? "החיבור לשירות נפל באמצע התשובה. מה שהתקבל מוצג למעלה — נסה שוב."
              : raw,
          });
        }
        c.close();
      },
    });

    return new Response(body, {
      headers: {
        "content-type": "application/x-ndjson; charset=utf-8",
        "cache-control": "no-store, no-transform",
        // proxies that buffer would defeat the whole point of streaming
        "x-accel-buffering": "no",
      },
    });
  } catch (e) {
    return NextResponse.json({ ok: false, reason: (e as Error).message }, { status: 500 });
  }
}
