# Episode 29 — script, ready to produce

## Why this topic, why this hook — the actual analysis David asked for

**The direct question:** why did episodes 23 and 25 both cross 1,200 combined views while
episode 27 barely cleared 400, when 27 shared episode 23's exact topic (Claude Code) and a
comparable production quality? Checked against real data, not a guess:

- **Topic demand does not explain it.** Episode 23 (Claude Code, 159k median demand) and
  episode 27 (also Claude Code, 159k) sit on the *same* topic. If demand explained the gap,
  they'd perform similarly. They didn't.
- **The hook TYPE and FRAMING does.** Checked every winning vs. losing hook against
  `hooks-guide.md`'s own log:
  - Ep23 ("22 episodes. One file keeps us safe.") — Expert/Authority, a general claim about
    the system.
  - Ep25 ("Your n8n retry doesn't just try again.") — Shock/Surprise, a general, checkable
    claim about how n8n itself behaves.
  - Ep27 ("I told Claude Code the wrong bug. On purpose.") — Story/Anecdote Teaser, a
    **first-person account of what the creator did**, not a claim about the tool. The
    payoff is deferred: the viewer has to trust there's a point coming, rather than
    receiving a checkable fact in the first sentence.
  - Ep27's own narration (verified from `video/reel-27.html`'s CUES) confirms the pattern:
    it's framed entirely as "I said... I told it..." — first person, not "Claude Code
    does X."
- **This matches the channel's own Confirmed pattern exactly** (`content-memory.md`,
  4.9.2026): every 500+ episode states a specific, checkable fact about the tool/system in
  its first line, never something the viewer has to wait to verify. Ep27 is now a second,
  independent data point for the *inverse* of that pattern — a first-person anecdote hook,
  even on a proven topic, underperforms the same way Product/Outcome Showcase already did
  (episodes 18, 19, 26). Two different weak hook shapes, two independent confirmations
  each.

**The actual instruction this gives episode 29:** pick the highest-demand topic with the
best track record, and hook it as a **general, checkable claim about how the tool
behaves** — never a personal anecdote, never a hypothetical, never a "Last time" callback.

## Topic

**n8n** — the highest measured demand of any topic shipped so far (233,070 median,
`channel/demand-report.md`) and a **2-for-2 win rate** on this channel (ep7: 658 views,
ep25: 1,200+ views) with zero losses on *hook type* (ep8's 139 views was a "Last time:"
callback hook failure, not an n8n problem — same demand-doesn't-explain-it logic as above).
This is the single best-supported topic choice available, by the data.

**The specific angle is new** — not a repeat of ep25's retry/duplicate-side-effects gotcha.
This one: n8n's **On Error** node setting (formerly "Continue On Fail") can mark a
genuinely failed step as a green "Success" in the Executions list, with the actual error
buried inside that one node's own output — nowhere else.

## Product verification (done this session, not assumed)

Live-researched, current as of 2026:
- **Exact current UI terminology**, per official docs
  (`docs.n8n.io/build/understand-workflows/workflow-components/work-with-nodes`): a node's
  **Settings tab → "On Error" field**, three options — *Stop Workflow* (default),
  *Continue*, *Continue (using error output)*.
- **The behavior**: a node set to Continue that actually errors does not flag the
  workflow — the Executions list shows **Success** (green). The error only appears inside
  that node's own output panel, as data (`error`, `statusCode` fields) — not anywhere in
  the top-level status.
- **Real, dated, first-person source** (not inferred): a community forum thread, "PSA:
  n8n's Continue On Fail silently swallows node errors — your execution log lies to you"
  (community.n8n.io, 10.5.2026), with a second, independent user confirming the same thing
  in production (7.7.2026).
- **Tier**: identical on n8n's free/Cloud tier and self-hosted — this is core
  workflow-engine behavior, not gated by plan.
- **Not claimed as "I built and tested this live this session"** — no n8n account exists
  in this repo/session to spin one up responsibly without asking first, so this episode is
  built the same way ep25 was (a real, sourced, general claim about n8n's behavior,
  illustrated with the mechanism), not a fresh screen recording. Said here plainly so it
  isn't overclaimed as a live demo it isn't.

## Hook — type check against `hooks-guide.md`

Log's last two: 28 The Specific Number, 27 Story/Anecdote Teaser (the type this episode's
own analysis flags as weak). Using **Shock/Surprise** — proven twice already (ep2: 940,
ep25: 1,200+) — on a **general, checkable claim about n8n itself**, not an anecdote.

Hook: **"Your n8n workflow can fail completely — and still say 'Success.'"**

Passes the dry-sentence test (real pull: a workflow you trust might be lying to you — fear
plus curiosity) and the checkable-fact test (a viewer could open n8n's own docs and verify
this claim without watching anything else).

## Full narration (~40s at natural pace)

1. Your n8n workflow can fail completely — and still say "Success."
2. One setting causes it: On Error, set to Continue — built to survive a small hiccup.
3. But when a node actually fails, n8n doesn't flag the workflow at all.
4. The Executions list still reads green. Success. Every single time.
5. The only place it shows is inside that node's own output — buried in error data nobody opens.
6. Real case, from n8n's own community: a workflow silently stopped working for weeks, and the log insisted it was fine.
7. One extra step catches it — a branch that checks for the error field, and alerts you the moment it appears.
8. The exact setup's in the link in bio.
9. Follow for the setup that actually works.

## On-screen text cues

- Hook: "Your n8n workflow can <box>fail completely</box> —<br>and still say <strong>'Success.'</strong>"
- Termbox ("the setting"): "On Error →<br>Continue" (mimicking n8n's own node settings label)
- Lede: "Built to survive<br>a small hiccup."
- Lede (turn): "But when the node<br><strong>actually fails</strong> —<br>nothing flags it."
- Quote card ("real report, n8n's own community"): "\"n8n's execution log<br><strong>shows success</strong>.\""
- Scoreboard: "Executions list" → "Success ✓" / "What actually happened" → "Error, unlogged"
- Lede: "Silently broken<br>for <strong>weeks</strong> —<br>the log said it was fine."
- Lede (fix): "One check catches it:<br>look for the <strong>error field</strong>,<br>alert the moment it appears."
- Biocard: link in bio
- Outro (locked): "Follow for the setup that actually works."

## Music

Mood: "tense" (`audio/pick_real_track.py` → `suspense-tension-building--arpmedia.mp3`,
now safe to use again — the quiet-intro bug that hit episode 27 is fixed, so the cut
starts from the track's first audible point automatically). Distinct from episode 27
("suspense" → alexmorgan's track) and episode 28 ("drive").

## Design

Palette: brass `#2ED573` (the false "Success" green — used ironically, on-brand for the
episode's own point) / ember `#FF4757` (the real, hidden failure). Distinct from episode 28
(`#F5A623`/`#6C63FF`) and episode 27 (`#FF3B6B`/`#3EC6FF`).

## Setup guide (draft — finalized once the build exists)

A new setup path, not a repeat of episode 25's n8n-account steps: how to actually build the
2-node reproduction (Manual Trigger → HTTP Request pointed at a failing URL, On Error set to
Continue) and add the one-node fix (an IF node checking for the error field, wired to a
Slack/email alert node) — working in a test/duplicate workflow first, never production.

## Caption / YouTube text (draft)

> Your n8n workflow can fail completely — and still say "Success." One setting causes it:
> On Error, set to Continue. When a node actually fails, n8n doesn't flag the workflow — the
> Executions list still reads green, every time. The only place the failure shows is inside
> that node's own output, buried in error data nobody opens. Real report from n8n's own
> community: a workflow silently stopped working for weeks, and the log insisted it was fine.
>
> One extra step catches it — a branch that checks for the error field, and alerts you the
> moment it appears.
>
> Full setup, exact clicks: actually-works.com/e/29
>
> Follow for the setup that actually works.
>
> #n8n #automation #aiagents #buildinpublic #workflowautomation
