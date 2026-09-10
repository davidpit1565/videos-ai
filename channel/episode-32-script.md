# Episode 32 — script, ready to produce

## Why this topic, why this hook — the actual analysis

**Topic selection, per the standing rule (episode 25 on): pick from measured demand, not
what sounds interesting.** Checked `channel/demand-report.md` against what's already
covered:

- `local ai model tutorial` (263,293 median) — covered twice (episodes 26, 31).
- `n8n ai agent tutorial` (233,070 median) — covered three times (episodes 7, 25, 29),
  2-for-2 confirmed win rate on the two with results in.
- `claude code tutorial beginners` (159,426 median) — covered twice (episodes 23, 27).
- **`ai automation for business` (125,777 median) — never covered.** The next-highest
  measured topic with zero episodes on it.

This is also the topic `demand-report.md` itself flags as doubly valuable: "sell" appeared
5x more often in the top-quartile results than everywhere else in the measured set — this
audience isn't just curious about automation, it's shopping for it. `content-memory.md`'s
"Current hypotheses" section has an open, untested hypothesis sitting on exactly this
combination (high demand + the audience that buys the paid service) — this episode is the
first real data point for it.

**Hook type, per `hooks-guide.md`'s own rotation rule:** last three were Shock/Surprise
(29), Contrarian Open (30), Direct Address/Question (31) — none of those again. Going with
**The Specific Number** (last used episode 28, a confirmed-fine type, not overused).

## Product verification (done this session, live search, not assumed)

- **n8n's Gmail Trigger → AI draft/reply pipeline is current, real, and exactly as
  demoed**: a Gmail Trigger node watches the inbox, an AI step drafts a response, and a
  Gmail node (Operation: Reply) posts it — n8n handles reply-threading headers
  automatically. Confirmed against n8n's own workflow templates and multiple current
  2026 setup guides.
  Sources: [n8n's own Gmail AI Auto-Responder template](https://n8n.io/workflows/2271-gmail-ai-auto-responder-create-draft-replies-to-incoming-emails/), [n8n's own AI email triage template](https://n8n.io/workflows/9157-ai-powered-email-triage-and-auto-response-system-with-openai-agents-and-gmail/), [Synta's 2026 Gmail Trigger setup guide](https://synta.io/blog/n8n-gmail-trigger-setup-guide)
- **The LLM step is provider-agnostic** — n8n's AI Agent node currently supports OpenAI,
  Anthropic's Claude family, Gemini, and local models via Ollama; no single model is
  required to build this. The build stays deliberately generic ("an AI step drafts the
  reply") rather than naming one specific model, since that's the part most likely to go
  stale fastest.
  Source: [strapi.io's 2026 n8n AI agent guide](https://strapi.io/blog/build-ai-agents-n8n)
- **The stat behind the hook, sourced, not invented:** "78% of customers buy from
  whichever business responds to them first" — this exact figure is independently cited
  across multiple current lead-response-time research roundups (2026). Also checked the
  supporting numbers so the claim isn't overstated: responding within 5 minutes makes a
  lead 21x more likely to qualify (MIT/InsideSales study, cited widely), and email
  replies after 24 hours have close to zero measurable effect on conversion.
  Sources: [Perspective AI's 2026 lead response benchmarks](https://getperspective.ai/blog/lead-response-time-2026-benchmarks-and-what-actually-converts), [GreetNow's 2026 lead response statistics](https://greetnow.com/blog/lead-response-time-statistics), [Casey Response's 2026 5-minute-rule breakdown](https://caseyresponse.com/blog/lead-response-time-statistics)
- **Not claimed as tested live this session**: no real business inbox exists in this
  session/repo to build and run this against without asking first (same reasoning as
  episode 25/29's product-verification notes) — built the same way those were, from a
  real, sourced, current mechanism, illustrated rather than freshly screen-recorded.

## The artifact

An n8n workflow: Gmail Trigger (new email arrives) → AI step reads it and drafts a reply
in the business's own voice → Gmail node posts it as a draft, ready to send with one
click (or auto-sent, for teams comfortable with that). The business never has an
unanswered email sitting for hours — the draft is already waiting.

## Hook — type check against `hooks-guide.md`

Log's last three: 29 Shock/Surprise, 30 Contrarian Open, 31 Direct Address/Question.
Using **The Specific Number** (last used episode 28).

**"78% of customers buy from whichever business responds to them first."**

Passes the cold-read test (lands in one pass, no unpacking) and the checkable-fact test
(a real, sourced, widely-cited figure, not a hypothetical) — states the stakes-bearing
number in the first clause, per the standing rule from episode 31's rework.

**Caught on self-review before this went any further, applying the exact lesson from
episode 31 rather than waiting for someone else to flag it again:** the first draft of
this hook had a second sentence — "This inbox never lets that business be someone
else." — that used an undefined referent ("this inbox") and needed a re-read to parse
("never lets X be someone else" is a double-negative construction). That is the identical
trap Roni's feedback caught on episode 31 ("your AI chatbot" left the viewer to fill in
what's being talked about). Fixed by cutting the hook back to the one clean, standalone
sentence — matching episode 28's actual confirmed-strong hook shape (one factual
sentence, nothing appended to it) — and moving the concrete reveal to its own later line,
stated plainly instead of with a vague pronoun.

## Full narration (~40s at natural pace)

1. 78% of customers buy from whichever business responds to them first.
2. Most businesses take 8 to 12 hours to answer a new email. Most of those leads are already gone by then.
3. This AI agent answers every new email in under a minute — before anyone even opens the inbox.
4. It's built on n8n: a Gmail trigger, one AI step, and a reply node. Free to build, running in the background the whole time.
5. The reply sits as a draft, ready in one click — or sends itself, for teams that want that.
6. Either way, the customer who emailed at 2am gets an answer by 2:01.
7. The exact setup's in the link in bio.
8. Follow for the setup that actually works.

## On-screen text cues

One scene per narration line, 1:1 (8 scenes):

1. Hook: "78% buy from<br>whoever <span class="box">responds first</span>."
2. Termbox ("the real gap"): "Average reply time:<br>8-12 hours" + lede beat "Most
   of those leads<br>are already gone<br>by then."
3. Lede: "This AI answers<br><strong>every email</strong><br>in under a minute."
4. Termbox2 ("the workflow"): "Gmail Trigger →" / "AI drafts reply →" / "Gmail: Reply"
5. Lede: "Sits as a draft,<br>ready in one click —<br>or sends itself."
6. Scoreboard: "Emailed at" → "2:00 AM" / "Answered by" → "2:01 AM"
7. Biocard: link in bio
8. Outro (locked): "Follow for the setup that actually works."

## Music

Mood: "drive" or "confident" — this is a capability/business-value episode, not a
warning or a live test. Distinct from episode 31 ("neutral").

## Design

Palette: distinct from episode 31's purple/amber (#A78BFA/#FBBF24). Suggest a
business-adjacent green/gold (money-adjacent without being cliché neon-green) —
finalize once the build exists, checked against `channel/used-designs.json`.

## Setup guide (draft — finalized once the build exists)

Exact steps: create the n8n workflow → add a Gmail Trigger node (OAuth setup: Google
Cloud project, Gmail API enabled, OAuth credential added to n8n) → add an AI step (any
supported provider) with a system prompt describing the business's tone and what it
should and shouldn't answer on its own → add a Gmail node set to Operation: Reply, wired
to the trigger's message ID so threading works automatically → test on a duplicate/test
inbox first, never production, before connecting the real one.

## Caption / YouTube text (draft)

> 78% of customers buy from whichever business responds to them first. Most businesses
> take 8-12 hours to answer a new email — most of those leads are already gone by then.
>
> This AI agent answers every new email in under a minute, before anyone even opens the
> inbox. It's built on n8n: a Gmail trigger, one AI step, and a reply node — free to
> build.
>
> The reply sits as a draft, ready in one click, or sends itself for teams that want
> that. Either way, the customer who emailed at 2am gets an answer by 2:01.
>
> Full setup, exact clicks: actually-works.com/e/32
>
> Follow for the setup that actually works.
>
> #n8n #aiautomation #smallbusiness #buildinpublic #aiagents
