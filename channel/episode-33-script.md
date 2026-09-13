# Episode 33 — script, ready to produce

## Why this topic, why this hook — the actual analysis (13.9.2026 pivot)

**Direct response to episode 31's real result:** episode 31 shipped with this channel's
single best-performing hook type (Direct Address/Question) after three real rounds of
fixes, on the local AI/Ollama topic — and still landed under 200 combined views, the
worst result recorded in this file. See `content-memory.md`'s 13.9.2026 entry: this
breaks the standing "it's the hook type, not the topic" explanation. David's own call,
made directly: stop experimenting with unproven topics (episode 32's "ai automation for
business" draft is paused, not abandoned) and return to a topic with a **confirmed real
win** — n8n (episodes 7, 25 confirmed wins; episode 29 not yet measured).

**New research done this session, not just re-applying the old hook rules — David asked
directly for this:** looked at real, external data on what actually drives virality,
not just this channel's own 30-some data points.

- **A real case study, not a guess:** Maverick Maltin (mavgpt.ai) grew from ~250 views on
  his first video to 3M+ followers in 15 months. His own stated method: **"I spent my
  days scrolling TikTok, finding AI content that was already going viral, and figuring
  out why it worked"** — pattern-matching proven structures, not inventing from
  scratch. His breakout wasn't luck in the sense David worried about (a fluke that
  can't repeat) — it was the first clean application of a method he then repeated
  (a second video later hit 34M views). Source: [mavgpt.ai/about](https://mavgpt.ai/about)
- **Hook archetype data (The Content Labs, 4,000-video study, 2026):** "Hot Take" and
  "Investigator" hook types average ~140,000 views; "Story" openers (narrative framing,
  e.g. "so basically...") average 7,127 views — a **20x gap**. This independently
  confirms what this channel's own data already found the hard way: episode 27's
  Story/Anecdote Teaser hook ("I told Claude Code the wrong bug...") underperformed on
  the exact same topic as a 1,200+ winner. External data agrees with our own.
  Source: [The Content Labs' 2026 viral-content data study](https://thecontentlabs.app/blog/what-goes-viral-in-2026-data-study)
- **The single biggest lever found, and one this channel has never deliberately used:**
  the same study found hooks built on **Fear** as the primary emotional register average
  264,031 views vs. 5,423 for **Hope** — a **49x gap**. "Most creators default to
  Aspiration or Hope, which rank among the worst performers." Every hook type in
  `hooks-guide.md`'s taxonomy describes *structure* (a question, a number, a contrarian
  claim) — none of it prescribes the *emotional register* the claim should carry. This
  episode is the first deliberate test of combining a proven structure (Expert/Authority,
  this channel's actual highest performer — episode 23, 1,200+ views) with an explicit
  stakes-bearing, fear-adjacent claim, instead of a neutral or curiosity-only one.

**Topic + angle:** n8n (confirmed-strong topic), a genuinely new mechanism not covered by
episode 25 (retry duplication) or episode 29 (On Error: Continue masking a real failure
as "Success") — **n8n workflows have no failure notification at all by default.** A
node errors, the execution shows a red X in the history, and nothing else happens unless
you've explicitly built a separate Error Workflow with an Error Trigger node. Verified
live this session against n8n's own current documentation.
Sources: [n8n's own docs: error handling](https://docs.n8n.io/flow-logic/error-handling/), [n8n's own docs: handle errors gracefully](https://docs.n8n.io/build/flow-logic/handle-errors-gracefully), [n8n's own official "attach a default error handler" workflow template](https://n8n.io/workflows/2312-attach-a-default-error-handler-to-all-active-workflows/)

## Hook — type check against `hooks-guide.md`, plus the new emotional-register axis

Log's last three: 29 Shock/Surprise, 30 Contrarian Open, 31 Direct Address/Question.
Using **Expert/Authority** (this channel's actual all-time-high type, episode 23,
1,200+ views — not used since) — deliberately paired with a fear-adjacent stake
(a workflow can die and nobody is ever told), not a neutral capability statement.

**"By default, n8n never tells you when a workflow dies."**

Passes the cold-read test (clear in one pass, no unpacking — a viewer who has never
touched n8n still understands "dies" and "never tells you" instantly) and the
checkable-fact test (verified against n8n's own docs — no alert exists unless you
build one yourself). Carries real stakes (a business automation could already be
broken right now, silently) rather than a neutral or curious framing — the deliberate
fear-register test this episode is built to try.

## Product verification (done live this session)

- **Confirmed current, n8n's own docs:** by default, a failed node execution shows only
  as a red X in the Executions list — no email, no Slack message, no push notification,
  nothing, unless a separate Error Workflow (starting with an Error Trigger node) is
  explicitly configured in that workflow's own Settings tab.
- **Distinct from episodes 25 and 29:** 25 covered retry-duplication (a workflow doing
  the same side effect twice), 29 covered On Error: Continue masking a real failure as a
  green "Success." This episode covers the **default, no-special-setting case** — most
  workflows built without ever touching the Error Workflow setting, which is the common
  case, not an edge case.
- **Tier:** identical on n8n's free/Cloud tier and self-hosted — core engine behavior,
  not gated.
- **Not claimed as freshly tested live this session** — same reasoning as prior
  n8n episodes: built from n8n's own current, dated documentation and its own official
  workflow template for fixing this exact gap, not invented or assumed from memory.

## The artifact

The fix itself, shown as the payoff: one small n8n workflow (Error Trigger → a
notification node, e.g. Slack or email) attached once as the default Error Workflow for
every other workflow in the account — n8n's own official template exists for exactly
this, confirming it's a real, current, recommended pattern, not something improvised.

## Full narration (~40s at natural pace)

1. By default, n8n never tells you when a workflow dies.
2. A node fails, the execution turns red in your history — and that's it. No email, no Slack message, nothing.
3. Most people never open that history unless something already feels wrong. By then, it could've been broken for weeks.
4. The fix is one setting: an Error Workflow, wired to an Error Trigger node.
5. Set it once, in Settings, and every workflow that fails from then on tells you immediately — Slack, email, whatever you want.
6. It's not a hidden feature. n8n even ships their own template for it. Almost nobody turns it on.
7. The exact setup's in the link in bio.
8. Follow for the setup that actually works.

## On-screen text cues

One scene per narration line, 1:1 (8 scenes):

1. Hook: "n8n never tells<br>you when a <span class="box">workflow dies</span>."
2. Termbox: "Execution status: <span style='color:#F87171'>Failed</span>" + badge "no alert sent"
3. Lede: "Nobody notices<br>until something<br>already feels wrong."
4. Termbox2: "Settings →" / "Error Workflow →" / "Error Trigger node"
5. Lede: "Every future failure<br>tells you immediately —<br>Slack, email, anything."
6. Scoreboard: "Hidden feature" → "No" / "Turned on by default" → "No"
7. Biocard: link in bio
8. Outro (locked): "Follow for the setup that actually works."

## Music

Mood: "tense" or "urgent" — this hook is deliberately stakes-first (per the fear-register
research above), not a calm capability reveal. Distinct from episode 32's paused
"confident" mood and episode 31's "neutral."

## Design

Palette: distinct from episode 31 (#A78BFA/#FBBF24) and episode 32's paused build
(#16A34A/#EAB308). Suggest a red/amber warning-adjacent palette (fits "a workflow can
die silently" without repeating episode 29's exact green/red).

## Setup guide (draft — finalized once the build exists)

Exact steps: create a small new workflow starting with an Error Trigger node → add a
notification node (Slack message or Send Email) using the Error Trigger's own output
(workflow name, error message) → save and activate this workflow → in each existing
workflow's own Settings tab (or account-wide, per n8n's template), set this new workflow
as the Error Workflow → test by deliberately breaking a duplicate/test workflow, never a
production one, and confirming the alert arrives.

## Caption / YouTube text (draft)

> By default, n8n never tells you when a workflow dies. A node fails, the execution
> turns red in your history — and that's it. No email, no Slack message, nothing.
>
> Most people never open that history unless something already feels wrong. By then,
> it could've been broken for weeks. The fix is one setting: an Error Workflow, wired
> to an Error Trigger node.
>
> Set it once and every future failure tells you immediately. It's not a hidden
> feature — n8n even ships their own template for it. Almost nobody turns it on.
>
> Full setup, exact clicks: actually-works.com/e/33
>
> Follow for the setup that actually works.
>
> #n8n #automation #aiagents #buildinpublic #workflowautomation
