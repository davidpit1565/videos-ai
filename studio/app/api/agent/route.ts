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
    openTasks: s.tasks.filter((t) => !t.done).map((t) => t.text),
    ideas: s.ideas.map((i) => i.text),
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
    // The beta surface is where `fallbacks` lives: if the primary model is busy or
    // declines, the API retries on its own instead of handing back an error.
    const res = await client.beta.messages.create({
      model: "claude-opus-5",
      max_tokens: 4000,
      thinking: { type: "adaptive" },
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default",
      system: SYSTEM,
      messages: [
        { role: "user", content: `Studio data:\n${brief(state)}\n\nQuestion: ${question}` },
      ],
    });

    if (res.stop_reason === "refusal") {
      return NextResponse.json({ ok: false, reason: "the model declined this request" });
    }
    const text = res.content
      .map((b) => (b.type === "text" ? b.text : ""))
      .join("\n")
      .trim();
    return NextResponse.json({ ok: true, answer: text });
  } catch (e) {
    return NextResponse.json({ ok: false, reason: (e as Error).message }, { status: 500 });
  }
}
