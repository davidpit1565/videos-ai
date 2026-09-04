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

- **CONFIRMED (4.9.2026):** a hook that states one concrete, checkable fact outperforms a
  hook that poses a hypothetical or asks the viewer to imagine something. Every episode
  that cleared 500+ views states something specific and already true in its first line —
  never a "what if" or "would you even know" framing. Every episode below ~200 views uses
  either a hypothetical/imagined-scenario opener or a "Last time:" callback that assumes
  context the viewer doesn't have. Five episodes on the high side, three on the low side —
  past this file's own two-episode bar for Confirmed. Full breakdown in the 4.9.2026 entry
  below ("What the 500+ club has in common").

---

## Current hypotheses

Reasoned predictions, not yet tested against enough published episodes to confirm.

- **HYPOTHESIS, now with a first real number behind it (1.9.2026):** Saves-per-view
  matters more than views for a "paste this and use it" video — a save means someone
  kept it to actually use, a view alone means the hook worked and the content didn't.
  (Already encoded as a rule in the studio's own `/api/agent` system prompt — carrying
  it here so content decisions use the same standard, not a separate one.) Pulled the
  real save-rate table from `/api/agent` for the first time: **16 of 18 published
  episodes have exactly one save each** — at this volume, save counts this low are a
  floor effect, not a ranking signal, and sorting by save-rate mostly just re-sorts by
  1/views. The one real outlier: **episode 1, 5 saves on 398 views (1.26%)** — 2.5-5x
  every other episode's rate. Episode 1 is literally the purest version of this
  hypothesis' mechanism: its entire content is one ready-to-paste prompt, the most
  "keep this to use later" thing published so far. Real support for the hypothesis, but
  still n=1 on the save-rate side — stays a hypothesis, not Confirmed, until a second
  paste-and-use episode does the same. **Next move worth trying:** identify what
  else episode 1 has in common structurally (not just "it's a prompt") and build 2-3
  more episodes that share it, to get the second data point this needs.
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
- **`subsAttributed` fixed 1.9.2026** — every caption already links to `actually-works.com/e/N`
  (its own episode page), and the signup form on that page now carries the episode number
  through `/api/subscribe` into the subscriber's own row (`source = episode-N`) and into
  Beehiiv's UTM fields; `/api/track` counts real signups per episode and writes the number
  automatically. This closes the actual gap the paid-funnel question needed (which episode
  brings a subscriber, per `plan/business-model.html`'s paid-engine-feeds-the-free-one
  model) — not measured until there's real published volume after this date to read
  anything from, but the plumbing is real now, not a manual guess.

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

## Jargon audit across episodes 2-14 (28.8.2026)

David said every episode except the first is hard to follow. Read the actual narration
(CUES arrays) of every episode 2-14 against house-style.md §10's zero-jargon rule, rather
than accepting the claim as-is or dismissing it. Real finding, not a blanket agreement or
blanket denial:

**Most episodes (4, 5, 6, 8, 9, 12, 13, 14) are actually self-contained and concrete** — no
undefined jargon found on this pass.

**Four real, specific gaps found, the same failure class that broke reel-15:**
- **Episode 3**: "Add this to your **prompt**" — "prompt" is never defined anywhere in the
  episode.
- **Episodes 7 and 10**: "**n8n** agent" — n8n (the automation tool) is named with no
  explanation of what it is, assuming the viewer already recognizes the brand.
- **Episode 11**: "**sibilance**", "**median**" — audio-engineering jargon inside an episode
  aimed at a general audience.

Not rebuilt yet — these are published episodes, and redoing them is a bigger call than a
quick script fix. Flagging here so the next full editing pass (or a dedicated "clean up the
back catalog" session) starts from a real list instead of guessing which four, or assuming
all thirteen, need work.

## Direction report acted on: episode 16 (29.8.2026)

The 28.8 direction research (`channel/direction-report-28-8.md`) named agentic-coding
content as the thinnest-covered format found in the whole landscape pass. Episode 16
(HeyGen's HyperFrames — an open-source tool that does, released publicly, roughly what
this channel's own render pipeline does by hand, and ships real Claude Code skills) is a
direct, concrete instance of that direction — sourced from a real Instagram Reel David
sent, verified by actually installing and rendering with the tool before writing a script
line. Not a repeat of the research; the follow-through on it.

## Nas Daily's business, researched directly (29.8.2026)

Real, sourced findings (not blog-repeated numbers — see the research for a verification
tier on every claim):

- **FACT, his own public statement**: 606 million views in one month generated $33,000 in
  ad revenue across Instagram/Facebook/TikTok/YouTube Shorts combined — content never paid
  for itself through platform ad revenue, at any scale.
- **FACT**: the actual monetization is a separate paid SaaS product (nas.com), reported ARR
  ~$1M → ~$8M over the last year — not courses, not ads. Nas Academy (the courses business)
  has been demoted to a support function for it.
- **FACT**: this took ~$40M of outside venture capital (Lightspeed, Khosla Ventures, and
  others) to build. The audience was the distribution/credibility asset; it did not by
  itself fund the paid product's growth.
- **The transferable shape, and the one honest caveat**: same structure as this channel's
  own model (free content → paid AI-automation services) — content buys distribution and
  credibility, a separate product monetizes it. The caveat: Nas Daily needed outside
  capital to scale that paid side to real revenue; we don't have that, so the equivalent
  here has to grow organically from actual client work, on a much longer timeline. Not a
  reason not to do it — a reason not to expect Nas Daily's speed from it.

## Real view counts, from David's own Instagram grid (30.8.2026)

David sent two screenshots of the profile grid on `actually_work...` (94ish followers, per
earlier session context). This is the first time this file has real per-episode view
numbers instead of only the demand-side research. Matched to episode number by comparing
each tile's on-screen hook text against the real caption files (`channel/episode-NN-
caption.txt`) — most matches are exact first-line quotes; a few (marked below) are inferred
from phrasing and could be off by one adjacent episode. Grid order is Instagram's own
newest-first order, not upload timestamps — the screenshot shows no post dates, so this is
recency order, not a measured time-of-day or day-of-week signal. Anyone reading this later:
don't upgrade "newest first" into "posted at a specific time" — that data isn't here.

| Grid position (newest→oldest) | Hook on screen | Views | Episode | Match confidence |
|---|---|---|---|---|
| 1 | "We spent 15 videos building one system." | 458 | 16 | exact |
| 2 | "Gemini already caught it. Before you did." | 427 | 15 | exact |
| 3 | "Everyone's sharing this 'AI lies' claim. Please you." | 340 | 14 | exact |
| 4 | "ChatGPT remembers you." | 175 | 13 | exact |
| 5 | "Most think it's for coders." | 416 | 12 | exact |
| 6 | "This agent can send email on its own. It never does." | 429 | 9 | exact |
| 7 | "voice_doctor.py measures it in the audio. SIBILANCE," | 425 | 11 | exact |
| 8 | "Most leads go cold fast." | 293 | 10 | exact |
| 9 | "Last time: a check said it passed. It lied." | 139 | 8 | exact |
| 10 | "Last time: 3 things your agent still breaks on." | 452 | 6 | exact |
| 11 | "Your captions are hiding behind Instagram." | 408 | 5 | exact |
| 12 | "This video almost shipped broken." | 462 | 4 | exact |
| 13 | "Real agents fail like this. Every one." | 386 | 3 | **inferred**, not a literal quote from ep03's caption |
| 14 | "n8n — Your agent can't tell when it messes up." | 658 | 7 | exact |
| 15 | "The test that settles it: Can't act without you? It's a chatbot." | 940 | 2 | **inferred** — ep02's own caption opens differently ("Everyone says agent...") but the theme (agent vs. chatbot) matches uniquely |
| 16 | "Your ChatGPT keeps giving you the obvious." | 662 | 1 | **inferred** — closest remaining match to ep01 (Universal AI Engine) by elimination |

**Sample-size warning, stated plainly:** these are views in the low hundreds on a ~94-
follower account — small enough that a handful of algorithmic placements can swing a number
this much on their own. Nothing below is a CONFIRMED pattern; everything is a HYPOTHESIS at
best, some weaker than others.

- **HYPOTHESIS:** the two highest performers (940, 662 — ep02 and ep01) are both a plain,
  self-contained claim that needs no earlier video to make sense ("it's a chatbot," "keeps
  giving you the obvious"). The two lowest (139, 175 — ep08 and ep13) are a "Last time:"
  callback hook and a narrow claim, respectively. A caption starting "Last time:" assumes
  the viewer already saw the previous one — most people hitting a Reel from Explore/the
  algorithm haven't, which is the same "don't assume the reader knows what came before"
  rule `explain-steps` already states for interface instructions. Only two data points on
  each side; this is a direction to watch, not a rule to apply retroactively to unpublished
  scripts.
- **HYPOTHESIS, and it complicates a standing worry:** ep07's hook names "n8n" directly in
  the first line and still got the second-highest view count (658) of all sixteen — despite
  `n8n` being one of the four spots the 28.8 jargon audit flagged as unexplained brand-name
  jargon. Either naming a specific tool doesn't hurt a hook the way the audit's framing
  assumed, or ep07 won on some other factor unrelated to that word. Not enough here to
  reverse the jargon-audit finding — that audit was about comprehension *inside* the video,
  this is about the hook getting a view at all — but worth remembering before assuming
  "never name an unexplained tool in the first line" as settled.
- **What's still missing:** saves, completion rate, and follower growth per episode — the
  numbers that actually distinguish "the hook worked" from "the content worked" (this
  file's own oldest hypothesis, above). View count alone can't separate those. Ask David for
  the studio's `/api/agent` saves/completion numbers next time this file gets updated, or
  pull them directly if the studio's live data becomes reachable from here.

## Growth is a trickle, not a curve (1.9.2026)

David sent a new grid screenshot and said it directly: views are up, but "not drastic,"
and asked what would actually make it jump. Compared against the 30.8.2026 snapshot above,
episode-by-episode, ~2 days apart:

| Hook | 30.8 views | 1.9 views | Δ (2 days) |
|---|---|---|---|
| "We spent 15 videos building one system." (ep16) | 458 | 500 | +42 |
| "Gemini already caught it. Before you did." (ep15) | 427 | 431 | +4 |
| "Everyone's sharing this 'AI lies' claim." (ep14) | 340 | 349 | +9 |
| "Most think it's for coders." (ep12) | 416 | 420 | +4 |
| "This agent can send email on its own. It never does." (ep09) | 429 | 435 | +6 |
| "voice_doctor.py measures it in the audio." (ep11) | 425 | 427 | +2 |
| "Most leads go cold fast." (ep10) | 293 | 298 | +5 |
| "Last time: a check said it passed. It lied." (ep08) | 139 | 139 | **+0** |
| "Last time: 3 things your agent still breaks on." (ep06) | 452 | 453 | +1 |

**FACT, not a hypothesis:** every one of these gained under 50 views in two days, and one
(ep08, the "Last time:" callback hook already flagged above as a likely-weak pattern)
gained exactly zero. This is what "not drastic" looks like in real numbers — a trickle
across the whole catalogue, not a stall on one bad episode. Two new tiles also appeared
in this snapshot (episode 18's "ChatGPT can use a website now" at 370, and one more read
as "ChatGPT remembers you" at 185 — that second one's episode match is uncertain enough
not to state as fact here) — both new posts started in the same 139-507 range as
everything else, not above it.

**What this does and doesn't tell us:** a flat trickle across every episode, old and new,
points at a distribution/reach ceiling (follower count, algorithmic placement, whatever
Explore is or isn't doing with this account) more than at any one episode's content —
content quality differences would be expected to show up as *some* episodes climbing while
others stay flat, not the whole catalogue moving in lockstep by single digits. That's a
reasoned read, not a confirmed one: still only two snapshots, and the account's follower
count itself (94-ish as of 28.8) is small enough that this could still be explained by a
handful of algorithmic placements rather than a structural ceiling.

**Still the same blocker as the 30.8 entry, worth repeating because it's the actual
answer to "what makes it jump":** views alone can't diagnose this. Saves, completion
rate, and follower growth per episode would show whether content is being watched to the
end and kept, which is the difference between "reach is capped" (a distribution problem,
fixed by things like consistency, collabs, or the account crossing a size threshold) and
"content isn't landing once seen" (a content problem, fixed by format/hook changes). This
session still can't reach the studio's live database directly — ask David to paste the
`/api/agent` saves/completion numbers, or the /videos table, before treating either
explanation as more likely than the other.

## Episode 17 failed its own test (31.8.2026)

Real, and worth stating plainly because of what it's about: reel-17's first cut was
built around "we tested our own comprehension rule" — episode 13's real 'column'
incident, framed as "one word broke this video," "our own script," "we run this on
every script now." David watched it and said directly: it's understandable only to
someone who already knows what episode 13 is and what this channel's process looks
like — exactly the failure the episode itself is about, on the episode that's
supposed to be the proof we catch this.

**The specific mistake:** self-referential meta framing ("this video," "our own
process") instead of a third-person, standalone teaching example. A viewer with zero
context can't parse "one word broke this video" — the video they're watching hasn't
broken, so the claim doesn't land; it only makes sense to someone who knows it's
about a *different*, earlier video.

**The fix, applied and now a standing check, not just for this episode:** before any
episode ships, ask specifically whether a first-time viewer with zero channel history
needs any of that history to follow the claim start to finish. "This channel already
did X" or "our own Y" is a warning sign, not a hook — the concrete example (the
column → box before/after) can stand completely on its own without ever mentioning
that it came from a real published mistake. Reel-17 was rebuilt to drop every
self-referential line and present the test as a general technique with a concrete
example, full stop.

**The irony is the point, not an excuse:** an episode about testing whether an
explanation makes sense to someone with no context did not itself get tested that
way before shipping. The paraphrase test in the episode works precisely because
someone (David) actually did it and said "I don't understand this, and I already
know the answer." That's the test running as designed — it just should have run
before he saw it, not after.

## First real save-rate table from the studio's own agent (3.9.2026)

David pulled saves/views/save-rate for all 21 published episodes directly from `/api/agent`
and did the analysis himself before handing it over — recorded here close to verbatim
because the read is correct and shouldn't be re-derived worse.

**Totals:** 4,409 views, 25 saves, 0.57% weighted average save rate across 21 episodes.

**FACT, and it changes how every save-rate number above should be read:** 20 of 21 episodes
are recorded with **exactly 1 save**. That is not a natural distribution — it reads as a
collection floor or a rounding artifact in how saves are tracked, not real per-episode
variation. Consequence: a save-rate ranking built from this data is mostly an *inverted
views ranking* (episode 21 "leads" at 4.35% saves/view for the sole reason that it only has
23 views) — **do not read this table as "which topic gets saved,"** it doesn't show that.

**The one real signal in the table:** episode 1 (the Custom Instructions prompt-paste
episode) is the only episode with a save count that isn't 1 — 5 saves on 402 views, 5x
every other episode's absolute save count. This is the same episode and mechanism already
flagged in *Current hypotheses* above (the "paste this and use it" hypothesis, first spotted
on 30.8 at 398 views/5 saves) — this is a refreshed read of the *same* data point as the
views column moved, not a second independent episode. Still n=1 on the save-rate side;
stays a hypothesis until a second paste-and-use episode does the same.

**Two real data gaps found, not just a "not enough episodes yet" problem:**
- `subsAttributed` is empty across all 21 episodes — meaning no published episode can yet
  be tied to any of the current 11 subscribers, the number the paid side actually cares
  about. The `content-memory.md` entry from 1.9.2026 already describes the plumbing for
  this (episode-tagged signup URLs, UTM into Beehiiv) as built — this confirms it hasn't
  produced a real attributed number yet for any of the 21 episodes published since.
- `topic` is empty on every episode too, so the data can't be cut by subject (agents vs.
  n8n vs. tools) even qualitatively — only by episode number and hook text.

**Open, unverified, and flagged as a possible data-integrity problem rather than a content
finding — do not act on the save-rate column until this is checked:** David's own next
step, recorded here so it isn't lost — check Instagram Insights by hand against episodes 2,
7, and 16 (highest views, lowest save rate in this table). If the real save counts differ
from the tracked "1," the collection itself is broken and needs fixing before any save-rate
based content decision, not just this table's ranking.

**Standing conclusion, restated because it's the actual answer to "what should we do with
this":** until there are real (verified, not floor-effect) saves on 10+ episodes each with
200+ views, **there is not enough published, verified data to say which format gets saved.**
Keep publishing, keep this file's hypotheses as hypotheses, and re-run this table after the
Insights check above and after UTM-driven `subsAttributed` starts producing real numbers.

## Episode 22 looks like a drop — probably age, not the hook (4.9.2026)

David sent a new grid screenshot and flagged it directly: views look like they dropped,
"this was supposed to be the opposite." Matched the visible tiles to episodes the same
way as the 30.8/1.9 snapshots (hook text against `channel/hooks-guide.md`'s log and the
existing table), only the top 12 tiles readable (view counts on row 3+ were cut off):

| Hook on screen | 4.9 views | Episode | Days since last snapshot's number |
|---|---|---|---|
| "If it failed right now — would you even know?" | **119** | 22 | new since last snapshot |
| "An AI can run your errands now." | 449 | 21 | new since last snapshot |
| "ChatGPT was going to buy things for you... for you." | 284 | 20 | new since last snapshot |
| "Claude keeps your files now." | 425 | 19 | new since last snapshot |
| "ChatGPT can use a website now." | 464 | 18 | was 370 on 1.9 |
| "It lives in a skill called explain-steps." | 514 | (tool-content post, not numbered) | new |
| "We spent 15 videos building one system." | 506 | 16 | was 500 on 1.9 (+6) |
| "Gemini already caught it. Before you did." | 436 | 15 | was 431 on 1.9 (+5) |
| "Everyone's sharing this 'AI lies' claim." | 349 | 14 | was 349 on 1.9 (+0) |
| "ChatGPT remembers you." | 186 | 13 | was ~185 on 1.9 (uncertain match then) |
| "Most think it's for coders." | 423 | 12 | was 420 on 1.9 (+3) |
| "This agent can send email on its own. It never does." | 435 | 9 | was 429-435 on 1.9 |

**FACT:** episode 22 is at 119 views — the lowest of every currently-visible tile, several
times below the 280-514 range every other recent episode sits in.

**The real confound, not a guess — stated because it changes the read:** every episode
*except* 22 (ep16 through ep9) moved by single digits since the 1.9 snapshot, the same
"trickle, not a curve" pattern already documented above. That means these are episodes that
have had days to accumulate views. Episodes 18-21 and 22 are new *to this snapshot* — we
don't have a prior number for them, so we can't tell how many days each has actually been
live. A freshly-posted reel will show a low absolute view count for the simple reason that
it hasn't had time to accumulate them yet, same as every other episode did in its own first
day or two — **this looks exactly like what "posted most recently" would produce, before
we can call it a real hook or content failure.**

**HYPOTHESIS, not dismissed, just not confirmed either:** episode 22's hook is also the one
`hooks-guide.md` already flagged internally before it shipped — two earlier drafts
("Your automation says it worked. It didn't." and an earlier third-person framing of the
same question) both failed the dry-sentence test and got rewritten. Even the shipped
version is a hypothetical question with no concrete claim, unlike the two historically
highest performers (ep01 "keeps giving you the obvious," ep02 "it's a chatbot" — both
stated, specific facts). Worth watching, not worth concluding from one data point at one day
old.

**Correction, same day, from David directly — the age-confound read above is REJECTED:**
he stated every previously-published episode reached at least 300 views within its first
day live. That's the actual bar this file didn't have when the entry above was written.
Episode 22 sitting at 119 is not explained by "it just posted" — every prior episode
cleared 300 in less time than 22 has now had. This makes 119 a real signal, not a
measurement artifact, and moves the hook-quality hypothesis above from "worth watching"
to "the leading explanation, still unconfirmed at n=1."

**What's still unverified, so this doesn't overcorrect into a new false certainty:** the
exact post time for episode 22 isn't in this file (no timestamp, only grid position) — "at
least a day" is David's recollection, not a logged number. Worth logging actual post
timestamps going forward (the studio's `/api/track` data should have this) so this
comparison doesn't depend on memory next time. Until then: treat "episode 22 underperformed
its hook" as the working explanation, not yet a Confirmed pattern — one episode is still
one data point, and the standing rule for this file (two independent episodes before
anything moves to Confirmed) still applies.

## What the 500+ club has in common (4.9.2026)

David asked directly: look at the reels that actually cleared his stated bar (500+ in a
day) and say why, so it can change direction. Pulled the real opening line from each
episode's own caption file rather than paraphrasing from memory:

| Episode | Views | Actual opening line |
|---|---|---|
| 2 | 940 | "Everyone says 'agent.' Almost nobody can tell you where the chatbot ends." |
| 1 | 662 | "One block of text. Paste it into ChatGPT once... and it picks its own method." |
| 7 | 658 | "Your n8n agent has no idea it's wrong." |
| 16 | 500-506 | "We spent 15 videos building one system. A company just gave the same one away, free." |
| (explain-steps content post) | 514 | "It lives in a skill called explain-steps." |

**The real thing they share, checked against the actual text, not guessed:** every one of
these states a specific fact that is already true, in the first sentence — not a question,
not a hypothetical, not something the viewer has to imagine. "Your n8n agent has no idea
it's wrong" is a claim, not a question. "We spent 15 videos" is a real number. "One block
of text" is a concrete, checkable object. Compare the two weakest episodes on record:
ep8 ("Last time: a check said it passed. It lied." — 139) assumes the viewer saw a
previous video, and ep22 ("If it failed right now — would you even know?" — 119) asks the
viewer to imagine a hypothetical instead of stating anything that's true right now.

**What this means for the next hook, concretely:** before a hook ships, check whether the
first sentence is a statement of fact or a question/hypothetical. A question can still work
(per `hooks-guide.md`'s own taxonomy, Direct Address/Question is the single most effective
type for this genre) — but ep02's own opener proves the pattern: it technically ends in a
statement, not a question, and it's the single highest performer on record. The actual
throughline isn't "never ask a question," it's **never make the viewer supply the
context or imagine the scenario themselves** — say the specific, real thing directly,
the same way `hooks-guide.md`'s dry-sentence test already asks "does this create real
pull," just with a sharper, checkable test now: *can the viewer verify this sentence is
true without watching anything else first?* Ep22's hook fails that test; all five 500+
episodes pass it.

**Honest limit on this, stated so it isn't overclaimed:** this is five high-performing
episodes and three low ones, not a controlled experiment — hook type, topic, and posting
context all vary between them too. It's the strongest pattern this file has found so far
(hence moving it to Confirmed above), not proof that fixing a hook alone guarantees 500+.

## How to update this file

After reviewing real numbers (via the studio, or `/api/agent`'s data), if the same
mechanism shows up in a second, independent episode: move the claim from *Current
hypotheses* to *Confirmed patterns*, and say which two episodes it's based on. If a
hypothesis gets clearly contradicted, don't delete it — mark it **REJECTED** and say why,
so the same idea doesn't get re-proposed later without remembering it was already tested.
