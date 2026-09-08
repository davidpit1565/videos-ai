import { NextResponse } from "next/server";
import Anthropic from "@anthropic-ai/sdk";
import { ClaudeSession } from "@/lib/db";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 60;

/** Same streaming-answer shape as /api/agent, scoped to a different question: not the
 *  channel's content metrics, but his own Claude Code usage across every project. Kept as
 *  its own endpoint rather than folded into /api/agent's prompt — the two answer different
 *  questions from different data, and mixing them would blur both. */
const SYSTEM = `You advise David on his own Claude Code usage across every project he
works in (an AI-content channel, a trading bot, and others) — not on the channel's content
metrics, which is a separate agent's job. He is already always on Sonnet 5, so a model-tier
switch is not an available lever for him; the two real levers are session length (a long
session keeps re-sending cached context every turn) and image-heavy work (frame extraction,
screenshots) — both a real, unavoidable cost, not a bug to fix.

Rules you must hold to:
- Answer only from the session data given. Never invent a session, a number, or a trend.
- If the data is too thin for a real answer, say exactly that.
- Be specific and short: name the project/session and the concrete next action.
- A session past ~90 minutes or ~30 turns is a candidate to close and start fresh for the
  next distinct task — say so plainly when the data shows one, don't soften it.`;

function brief(sessions: ClaudeSession[]) {
  return JSON.stringify(
    sessions.map((s) => ({
      project: s.project,
      model: s.model,
      turns: s.turns,
      ageMinutes: Math.round(s.ageMinutes),
      costUsd: +s.estimatedCostUsd.toFixed(2),
      inputTokens: s.inputTokens,
      outputTokens: s.outputTokens,
      cacheReadTokens: s.cacheReadTokens,
      lastSeen: s.lastSeen,
    })),
  );
}

export async function POST(req: Request) {
  if (!process.env.ANTHROPIC_API_KEY) {
    return NextResponse.json({
      ok: false,
      reason: "ANTHROPIC_API_KEY is not set — add it in Vercel → Settings → Environment Variables",
    });
  }
  let question = "";
  let sessions: ClaudeSession[] = [];
  try {
    const body = await req.json();
    question = String(body.question ?? "").slice(0, 2000);
    sessions = Array.isArray(body.sessions) ? body.sessions : [];
  } catch {
    return NextResponse.json({ ok: false, reason: "bad request body" }, { status: 400 });
  }
  if (!question) {
    return NextResponse.json({ ok: false, reason: "question is required" }, { status: 400 });
  }

  try {
    const client = new Anthropic();
    const stream = client.beta.messages.stream({
      model: "claude-opus-5",
      max_tokens: 4000,
      thinking: { type: "adaptive" },
      output_config: { effort: "medium" },
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default",
      system: SYSTEM,
      messages: [{ role: "user", content: `Sessions:\n${brief(sessions)}\n\nQuestion: ${question}` }],
    });

    const enc = new TextEncoder();
    const body = new ReadableStream<Uint8Array>({
      async start(c) {
        const send = (o: unknown) => c.enqueue(enc.encode(JSON.stringify(o) + "\n"));
        send({ open: true });
        try {
          let any = false;
          for await (const ev of stream) {
            if (ev.type === "content_block_delta" && ev.delta.type === "text_delta" && ev.delta.text) {
              any = true;
              send({ t: ev.delta.text });
            }
          }
          const final = await stream.finalMessage();
          if (final.stop_reason === "refusal") {
            send({ error: "the model declined this request" });
          } else if (!any) {
            console.error("[claude-agent] empty answer", JSON.stringify({ stop: final.stop_reason, usage: final.usage }));
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
          console.error("[claude-agent] stream failed", raw);
          const network = /terminated|aborted|fetch failed|ECONNRESET|socket hang up/i.test(raw);
          send({ error: network ? "החיבור לשירות נפל באמצע התשובה. מה שהתקבל מוצג למעלה — נסה שוב." : raw });
        }
        c.close();
      },
    });

    return new Response(body, {
      headers: {
        "content-type": "application/x-ndjson; charset=utf-8",
        "cache-control": "no-store, no-transform",
        "x-accel-buffering": "no",
      },
    });
  } catch (e) {
    return NextResponse.json({ ok: false, reason: (e as Error).message }, { status: 500 });
  }
}
