import { NextResponse } from "next/server";
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import Anthropic from "@anthropic-ai/sdk";
import { IdeaScore } from "@/lib/types";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 60;

/** Truncated, not the whole file — this is grounding context for a judgment call, not
 *  a document the model needs to quote from. Read fresh every request: the report gets
 *  re-measured periodically and a stale cached copy would silently drift from it. */
function demandContext(): string {
  const p = join(process.cwd(), "..", "channel", "demand-report.md");
  try {
    if (!existsSync(p)) return "";
    return readFileSync(p, "utf8").slice(0, 3000);
  } catch {
    return "";
  }
}

const SYSTEM = `You score one candidate episode idea for an AI-education channel called
Actually Works. Its promise: a setup a viewer can copy in two minutes, including what
breaks. Content is in English, no jargon — a rule set after 25.8 specifically because
earlier scripts read as written for people who already understand AI. The owner speaks
Hebrew — answer in Hebrew.

This is your judgment, not a measurement. Say so implicitly by keeping "reasoning" to one
honest paragraph, not a confident-sounding fabricated statistic. Never invent a specific
view count, follower number, or benchmark that isn't in the demand data you're given —
if you don't have a real number for something, say "not measured" rather than estimate
one that sounds real.

Score each category 0-100:
- marketingPotential: does this sell itself in one caption line or hook, no explanation needed?
- hookStrength: would this intrigue someone with zero interest in the topic, not just the target viewer?
- simplicity: can this be explained with no jargon at all, in plain words a non-technical viewer follows in one pass?
- brandFit: does it fit "Actually Works" — a real setup, what it will not do, no hype?
- competitiveSpace: per the demand data's own method (median view count per topic, and whether the
  strongest video is 1M+ or something a new entrant could actually compete with) — is this topic open
  or already owned by an established leader?
- audienceDemand: is there real measured search/view demand behind this (from the data below), or is
  this a guess with nothing to back it?

verdict: "yes" (score it, build it), "no" (real weaknesses, explain which), or "draft" (promising
but needs something specific first — say what).`;

const SCHEMA = {
  type: "object" as const,
  properties: {
    categories: {
      type: "object" as const,
      properties: {
        marketingPotential: { type: "integer", minimum: 0, maximum: 100 },
        hookStrength: { type: "integer", minimum: 0, maximum: 100 },
        simplicity: { type: "integer", minimum: 0, maximum: 100 },
        brandFit: { type: "integer", minimum: 0, maximum: 100 },
        competitiveSpace: { type: "integer", minimum: 0, maximum: 100 },
        audienceDemand: { type: "integer", minimum: 0, maximum: 100 },
      },
      required: [
        "marketingPotential", "hookStrength", "simplicity",
        "brandFit", "competitiveSpace", "audienceDemand",
      ],
      additionalProperties: false,
    },
    verdict: { type: "string", enum: ["yes", "no", "draft"] },
    reasoning: { type: "string", description: "One honest paragraph, in Hebrew." },
  },
  required: ["categories", "verdict", "reasoning"],
  additionalProperties: false,
};

export async function POST(req: Request) {
  if (!process.env.ANTHROPIC_API_KEY) {
    return NextResponse.json({
      ok: false,
      reason: "ANTHROPIC_API_KEY is not set — add it in Vercel → Settings → Environment Variables",
    });
  }
  let idea = "";
  try {
    const body = await req.json();
    idea = String(body.idea ?? "").trim().slice(0, 500);
  } catch {
    return NextResponse.json({ ok: false, reason: "bad request body" }, { status: 400 });
  }
  if (!idea) return NextResponse.json({ ok: false, reason: "idea is required" }, { status: 400 });

  try {
    const client = new Anthropic();
    const response = await client.messages.create({
      model: "claude-opus-5",
      max_tokens: 4096,
      system: SYSTEM,
      messages: [
        {
          role: "user",
          content: `Measured demand data (channel/demand-report.md, may be partial):\n${demandContext()}\n\nIdea to score: ${idea}`,
        },
      ],
      tools: [
        {
          name: "score_idea",
          description: "Return the score for this episode idea.",
          strict: true,
          input_schema: SCHEMA,
        },
      ],
      tool_choice: { type: "tool", name: "score_idea" },
    });

    if (response.stop_reason === "refusal") {
      return NextResponse.json({ ok: false, reason: "the model declined this request" });
    }
    const call = response.content.find((b) => b.type === "tool_use" && b.name === "score_idea");
    if (!call || call.type !== "tool_use") {
      return NextResponse.json({ ok: false, reason: `no score came back (stop reason: ${response.stop_reason})` });
    }
    return NextResponse.json({ ok: true, score: call.input as IdeaScore });
  } catch (e) {
    return NextResponse.json({ ok: false, reason: e instanceof Error ? e.message : String(e) }, { status: 500 });
  }
}
