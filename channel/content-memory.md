# Content memory — patterns, not topics

The point of this file: when a Reel wins, write down *why it might have won*, not just
that it won. When a claim moves from HYPOTHESIS to CONFIRMED, it's because the same
pattern showed up more than once — one video is a data point, not a rule.

Source of truth for the actual numbers (views, saves, save-rate, engagement) is the
studio's own tracked state — `/api/track` pulls it daily from Instagram and Beehiiv, and
`/api/agent` already answers questions against it with the same rule this file follows:
**never invent a metric.** This file is the *qualitative* memory next to that real data —
what we think a number means, not the number itself. Update it after actually looking at
the studio's data, never from a guess at what "probably" happened.

Every entry below is labeled. Never let a HYPOTHESIS read like a CONFIRMED PATTERN just
because it sounds right.

---

## Confirmed patterns

*(Needs at least two independent episodes showing the same mechanism before anything
moves here from Current hypotheses. Nothing qualifies yet — 12 episodes published is not
enough volume to confirm a pattern without overfitting to one or two videos.)*

---

## Current hypotheses

Reasoned predictions, not yet tested against enough published episodes to confirm.

- **HYPOTHESIS:** Saves-per-view matters more than views for a "paste this and use it"
  video — a save means someone kept it to actually use, a view alone means the hook
  worked and the content didn't. (Already encoded as a rule in the studio's own
  `/api/agent` system prompt — carrying it here so content decisions use the same
  standard, not a separate one.)
- **HYPOTHESIS:** Content that shows a real build failure and how it was found/fixed
  (per `channel/episode-ideas.md`'s "$711 number that wasn't real" idea, and the
  `th_check.py`→`burst.py` correction documented in `channel/slate-20.md`) reads as more
  credible than a clean demo, because it's the one thing a competitor account showing
  polished output can't fake. Unconfirmed — no episode built this way has published yet.
- **HYPOTHESIS:** Topics that are simultaneously high measured demand *and* the same
  audience that buys the paid service (per `channel/demand-report.md`: "sell" was the
  word that separated the top-quartile results from the rest) outperform topics that are
  just high-demand. Only the demand-side half of this is measured; the performance half
  isn't yet.

## Winning formats

*(Empty — no format has repeated enough times with a consistent result to call it a
winner yet. A format goes here only after Confirmed patterns has something to point to.)*

## Losing formats

*(Empty for the same reason.)*

## Open questions

- Does the audience that watches a full build-log episode (long-form, per the
  "מאפס עד 100" flagship idea in `channel/episode-ideas.md`) overlap with the audience
  that watches a 45-75s Reel, or are they functionally two different audiences that need
  separate measurement?
- `channel/demand-report.md` measures YouTube search demand only — Instagram Reels
  demand is explicitly unmeasured there (the doc says so directly: Instagram blocked the
  pull without login). The studio's own tracked saves/views are the real substitute for
  that gap, once there's enough published volume to read anything from them.

## Pattern shapes worth trying

Not categories to fill a quota in — just story shapes that already fit what "Actually
Works" promises (a test, not a claim), useful when picking the angle for a new episode:

- **The Impossible Test** — claim → attempt → escalation → failure or surprise → result.
- **Break the AI** — try to make it fail on purpose; the point is what the failure shows,
  not that it failed.
- **AI vs. Reality** — a claim from online → an actual test → measurement → verdict.
- **Build It** — idea → build → obstacle → iteration → working result. This is already
  the channel's own standing rule ("everything we build becomes an episode") in a
  different name.
- **Human vs. AI** — only when there's a real question worth answering, never because the
  comparison sounds interesting on its own.

These are unconfirmed as *patterns* the same way everything else here is — they're
candidate shapes, not proven winners. Don't tag an episode with one of these and treat the
tag as evidence it will work.

## External landscape research (28.8.2026)

Six parallel research passes, prompted by David after watching reel-15 and not understanding
it. Full write-up: `channel/direction-report-28-8.md`. Summary here for future planning —
every claim below is labeled, and none of it should be read as more certain than the label
says.

- **FACT (two independent research passes agree):** a short-form (Reels/TikTok) account whose
  entire premise is "test an AI claim live, show the real verdict" is almost nonexistent.
  One long-form match found at real scale (Internet of Bugs, ~130k subs). In short-form
  specifically, exactly one account was found doing this (@huskistaken) — framed as comedy,
  not as a tutorial format — and it got 9M+ views on a single video. This is the strongest
  external support yet for the "Pattern shapes worth trying" list above (the Impossible Test,
  AI vs. Reality, Break the AI): not just plausible, actually rare in the wild.
- **HYPOTHESIS, not yet tested on our own numbers:** what the successful adjacent channels
  (Project Farm, RTINGS, Captain Disillusion — none of them AI content) share structurally is
  a repeatable, visible measurement and a stated independence policy, not just "we tested it."
  We don't yet have our own equivalent of Project Farm's test bench — an open question, not
  a decided answer.
- **FACT:** agentic-coding/harness content (Claude Code and similar, explained to non-coders)
  is the thinnest-covered format found in the whole landscape pass — every small channel in it
  (Matt Pocock, IndyDevDan, Brian Casel) gets view counts well above its subscriber count,
  the opposite pattern from the saturated daily-AI-news tier. Episode 12 is already in this
  space; there's room to go deeper, not just once.
- **FACT:** no ranked list surveyed contains a non-English (e.g. Flemish/Dutch) AI-education
  channel. Absence of a competitor in a ranking is not evidence of demand — it's simply
  unmeasured (same caveat as everywhere else demand isn't directly measured).
- **FACT, from the monetization research:** the audience-to-services funnel already in use
  here (channel → paid AI-automation work) is the best-documented path that pays before an
  audience is large — Nate Herk (n8n tutorials + agency, named enterprise clients) is the
  closest real analogue found. **Risk to watch, not yet ours:** in the two most-documented
  cases of this exact funnel (Nick Saraev, Liam Ottley), the community/course side ended up
  outearning the services side, or the founder exited services entirely — a natural drift
  toward the more scalable info-product, not a failure. Worth noticing if it starts happening
  here, not something to prevent pre-emptively.
- **FACT, and important to keep repeating:** no documented case exists of a genuinely
  zero-to-small account reaching millions of views within days without either a structural
  format innovation (e.g. a serialized cliffhanger format) or pre-existing reach the "zero
  followers" framing hid. "Find the right topic and it will happen fast" is not a plan this
  research supports — hook quality and completion rate are real, practicable levers; the
  scale and speed of a specific breakout are not something content quality alone controls.

## How to update this file

After reviewing real numbers (via the studio, or `/api/agent`'s data), if the same
mechanism shows up in a second, independent episode: move the claim from *Current
hypotheses* to *Confirmed patterns*, and say which two episodes it's based on. If a
hypothesis gets clearly contradicted, don't delete it — mark it **REJECTED** and say why,
so the same idea doesn't get re-proposed later without remembering it was already tested.
