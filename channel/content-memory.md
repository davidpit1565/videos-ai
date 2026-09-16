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

- **H1 (renamed from the earlier "saves-per-view" framing, tightened 8.9.2026 after
  David/ChatGPT's review of the Master Table below — this exact wording is the
  claim, not a looser paraphrase): Immediate personal utility may increase save/share
  behavior. Current evidence: strong signal, n=1.** **VERIFIED DATA:** across all 27
  published Reels (11.8-7.9.2026), episode 1 (Custom Instructions — one paste-and-use
  prompt) has 5 saves on 246 reach (2.03%), the highest save-rate in the set, and is
  **the only one of the 27 with any shares recorded at all** (12 shares; every other
  episode has exactly 0). Its overall engagement rate (11.38%) is roughly double the
  second-highest episode (13, 9.38%). **CONFIDENCE LEVEL: Strong Hypothesis, not
  Confirmed — sample size is n=1** (this file's own bar for Confirmed is two
  independent episodes sharing the mechanism).
  **Explicitly NOT proven, because these are confounded in a single data point and
  the next experiment has to separate them one at a time:** episode 1's result could
  be driven by its *utility* (a ready-to-paste artifact), its *topic* (ChatGPT Custom
  Instructions specifically), its *hook*, its *51-second duration*, or its
  *specificity* (one exact block of text vs. a general method) — or some combination.
  Nothing in the data so far can tell these apart. Do not read this entry as "utility
  is confirmed to drive saves/shares" — it isn't, yet.
  **What would validate it:** a second episode built around the same *utility*
  mechanism (a single, immediately reusable artifact) but on a **different topic**
  clears a save-rate and share-rate meaningfully above the ~0.74% median save-rate /
  0% share-rate baseline the other 26 episodes sit at (see Master Table below for the
  baseline computation). **What would invalidate it:** that second episode performs
  like the baseline (≤1% saves, 0 shares) — meaning episode 1's result was
  topic-specific or a fluke, not the utility mechanism. **Next move:** see "Batch 1
  experiments" in `channel/experiments.md` — Experiment 1 is built specifically to
  test this by holding hook-type and duration roughly constant while changing the
  topic away from ChatGPT/Custom Instructions.
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

- **FACT, first entry here (7.9.2026) — a production-quality judgment, not an audience-data
  pattern, so it's not labeled CONFIRMED/HYPOTHESIS the way the sections above are:**
  a non-lip-synced "talking head" built from a still/idle AI-generated avatar clip (a
  Gemini image animated into a subtle idle loop, played under narration audio) does not
  work as a talking-head format. Tried for episode 26 as the free alternative to a paid
  D-ID avatar. David watched the actual shipped file and called it directly: the avatar
  never talks while the voice plays, and it "looks stuck" — the fundamental problem is that
  there is no real lip-sync without a paid plan (D-ID's free/trial tier also has a separate,
  unrelated blocker: a full-frame tiled watermark). Episode 26 shipped instead in the
  channel's standard animated-typography format, no avatar. **If a talking-head format is
  wanted again, the only real path found is a paid D-ID plan (Pro, $16/mo) — it both removes
  the watermark and gives actual lip-sync** — a non-lip-synced avatar clip is not a viable
  middle ground, it reads as broken, not as a stylistic choice.

## Process lesson: frame-sampling review misses what continuous playback catches (7.9.2026)

Not a content/audience pattern — a note on how episodes get checked before shipping, kept
here because it directly caused the episode 26 avatar format above to ship broken the first
time despite "passing" every automated check and a still-frame visual review.

**What happened:** the avatar version of episode 26 passed `check.sh` (safe-area, loudness,
resolution, no-frozen-frame) and a review that sampled ~15-20 individual still frames spread
across the timeline — and still shipped with captions sitting on top of the avatar's face/
mouth, a caption with no matching audio, and the avatar never visibly speaking. None of those
are things a discrete still frame can show: a static frame can't reveal "this doesn't move
for 50 seconds" or "the mouth never syncs to the words," and the caption-without-audio bug
only surfaced once someone actually listened straight through.

**Separately, and worse:** the exact same episode's real narration audio had a genuine ~3.4s
silent gap (dropping "No API key. It's running right here, on this laptop." entirely) and a
word cut off mid-syllable ("off.") — introduced by a mid-session audio-splicing bug, and
invisible to whole-clip average loudness checks (`volumedetect`'s mean/max over an entire
clip doesn't reveal that only part of it is real audio). This shipped through *two* separate
episode-26 releases before David caught it by ear.

**The actual lesson, not just "we found bugs":** still-frame sampling and whole-clip average
audio stats are both real checks worth keeping, but neither one substitutes for actually
watching the full render start-to-finish with sound on, and neither one substitutes for a
full-file fine-grained silence scan (`ffmpeg silencedetect` at a short window, across the
whole file) when narration audio has been hand-edited/spliced rather than generated in one
pass. Both are now the standard for any episode involving spliced/patched audio, not just
episode 26.

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

## Episode 23 crosses 1,200 total views (7.9.2026)

**FACT, per David directly (his own read of the numbers, not independently pulled from
`/api/agent` this session):** episode 23 ("22 episodes. One file keeps us safe." —
Expert/Authority type) passed **1,200 total views in one day, combined across Instagram
and Facebook.** This is the highest single-day number recorded in this file by a wide
margin — every previous high-water mark was Instagram-only and topped out at 940 (ep2).
Not yet broken down by platform or re-verified against `/api/agent` directly, so the
exact Instagram-vs-Facebook split isn't in this entry — worth pulling next time this file
gets a real data update, since Facebook distribution being a real contributor (not just
Instagram) would itself be worth confirming and possibly leaning into more.

## Episode 24 underperformed, episode 25 also crossed 1,200 (7.9.2026)

**FACT, per David directly (his own read, not independently pulled from `/api/agent`
this session):** episode 24 ("Editors squeeze the picture to fit the audio. We do the
opposite." — the `retime.py` episode) did not perform well. Episode 25 (the live
escalate-until-it-breaks format) also passed **1,200 total views**, matching episode 23's
mark. Neither is broken down by platform yet, and neither is re-verified against
`/api/agent` directly — same caveat as the episode 23 entry above. Worth a real pull next
data-review pass: two 1,200+ episodes back to back (23 and 25) is the start of a pattern
worth naming, but it's two data points with different formats (Expert/Authority topic vs.
a live-test format) and no platform breakdown yet, so it stays a note, not a Confirmed
pattern, until that's checked.

## What separates the two 1,200+ episodes from episode 26 (8.9.2026)

David asked directly why episodes 23 and 25 both crossed 1,200 combined views (Instagram +
Facebook — he said Facebook now carries most of his real views, so this file's future
"total views" entries should be read as cross-platform unless stated otherwise) while
episode 26 didn't clear 400. Checked against three real, checkable things — hook type
(`hooks-guide.md`'s log), the actual opening line, and measured topic demand
(`channel/demand-report.md`) — rather than guessing.

**FACT, checked against the log:** episode 23 used Expert/Authority ("22 episodes. One
file keeps us safe."), episode 25 used Shock/Surprise ("Your n8n retry doesn't just try
again. It can do the exact same thing twice."). Episode 26 used Product/Outcome Showcase
("This is a real AI model. My WiFi is off.") — the same type episodes 18-19 already used
back to back at moderate-not-high results (425, 464 views).

**FACT, checked against `demand-report.md`, and this is the part that rules out the obvious
guess:** episode 26's topic (local/offline AI models, i.e. Ollama) sits at the *highest*
measured median demand of any topic in the report (263,293) — higher than n8n (233,070,
episode 25's topic) and higher than Claude Code (159,426, episode 23's topic). **Topic
demand is not what separated the winners from episode 26** — episode 26 sat on the
single highest-demand topic measured and still underperformed both lower-demand topics.

**What this leaves as the explanation, at HYPOTHESIS strength (three episodes, not yet the
two-independent-repeat bar for a topic-specific claim, but the type-level pattern now has
two separate instances — 18-19 and 26 — pointing the same way):** the hook *type* is doing
more work than the topic here. Both winners state a surprising or credibility-backed claim
that creates tension ("a familiar tool secretly does something wrong," "after N episodes,
here's the mistake caught") — the viewer has something to resolve. Product/Outcome
Showcase just states a capability plainly ("here's a thing that works") with no tension to
resolve, even when the capability itself is demonstrably true and the topic is in high
demand. This matches the general research already logged in `hooks-guide.md` (Product/
Outcome Showcase is rare specifically in the education genre, common only in
general/entertainment TikTok) — our own numbers now agree with that genre distinction on
a second occasion, not just the first.

**Concrete direction for the next hook, not just an observation:** when a demo/capability
episode is the format (as both 26 and 28 are), the hook should not just showcase the
capability — it should be framed as a surprising resolution to a stated tension (per
episode 28's own hook, already built this way: "four rows... only three were actually test
data" states a number that demands resolution, not just a capability). Keep picking topics
from measured demand per the standing rule, but treat hook type as at least as load-bearing
as topic demand until more data says otherwise — don't let a high-demand topic excuse a
flat Product/Outcome opener again.

## Episode 27 barely cleared 400 — the same-topic control case (8.9.2026)

David asked directly why 23 and 25 crossed 1,200 combined views while 27 didn't. This is a
sharper test than the 26 entry above, because **27 shares episode 23's exact topic**
(Claude Code, 159k median demand) — so topic demand is held constant, and the difference
has to be something else.

**FACT, checked against `hooks-guide.md`'s own log and each episode's real CUES text:**
episode 23's hook ("22 episodes. One file keeps us safe.") and episode 25's hook ("Your
n8n retry doesn't just try again.") are both **general, checkable claims about the
tool/system itself** — Expert/Authority and Shock/Surprise respectively. Episode 27's hook
("I told Claude Code the wrong bug. On purpose.") is a **first-person anecdote** — Story/
Anecdote Teaser, "so this happened when I tried X." Verified against `video/reel-27.html`'s
own CUES: every line is framed as "I said... I told it..." — the payoff is deferred, the
viewer has to trust something's coming rather than getting a checkable fact immediately.

**CONFIRMED, moved up from hypothesis — this is now two independent hook shapes with two
episodes each pointing the same way:** Product/Outcome Showcase (episodes 18, 19, 26) and
now Story/Anecdote Teaser (episode 27, and structurally episode 8's "Last time:" callback
before it) both underperform on this channel *regardless of topic demand* — episode 27 sat
on the exact same topic as a 1,200+ winner and still landed under 400. What every 500+
episode shares, restated with this new data point: **a general, checkable claim about how
the tool/system behaves, stated immediately** — never an anecdote the viewer has to wait
out, never a callback, never a hypothetical.

**Applied directly to episode 29:** highest-demand, best-track-record topic (n8n, 2-for-2
on this channel) hooked as a general claim ("Your n8n workflow can fail completely — and
still say 'Success.'"), Shock/Surprise type. Real product verification done live this
session (n8n's own current docs plus a dated, first-person community report), not assumed

## Episode 31 breaks the "it's the hook type, not the topic" hypothesis (13.9.2026)

**FACT, per David directly:** episode 31 (local AI models / Ollama offline capability)
shipped after three separate rounds of hook fixes — reworded per Roni's real marketing
feedback, then reworked again to name a specific chatbot (ChatGPT) instead of a vague
"any AI chatbot," then had a genuine accent-drift defect fixed on top of that. The final
hook, "ChatGPT needs the internet to respond. This AI doesn't — and it just proved it.,"
uses **Direct Address/Question — this channel's single best-performing hook type**
(episode 2's 940 views, its all-time high). It still landed under 200 total views
combined across Instagram and Facebook — David's own words: "יצא לנו ממש ממש גרוע"
(came out really, really bad). This is below every other episode's number in this file,
including the previously-weakest ones (episode 8: 139, episode 22: 119).

**Why this matters, stated plainly: it breaks the standing explanation.** The 8.9.2026
entry above concluded hook *type* was the load-bearing variable, not topic — because
episode 26 (Product/Outcome Showcase, a confirmed-weak type) failed on this exact same
topic while episode 23/25 (different types, different topics) succeeded. Episode 31 was
supposed to be the clean test that confirmed this: same weak topic, but this channel's
*strongest* type instead. If the hypothesis were right, fixing the hook type should have
been enough to save it. It wasn't — episode 31 scored below episode 26 despite a
provably stronger hook by every standing rule in `hooks-guide.md`.

**What this actually leaves us with — two topic-level data points now, not one, and
different hook types on both:** local AI models / Ollama has failed twice on this channel
(episode 26: Product/Outcome Showcase, under 400; episode 31: Direct Address/Question,
under 200) using two different hook types that don't share a common weakness. The
simplest explanation consistent with both facts: **this specific topic may not have real
pull with this channel's actual audience, regardless of how the hook is written** — not
something `hooks-guide.md`'s rules can fix, because those rules are about hook
construction, and this data point held hook construction excellent and still lost.

**Explicitly not yet a Confirmed pattern (this file's own bar: two independent episodes
sharing the *mechanism*, not just two episodes on the same topic) — but strong enough to
change direction now rather than wait for a third data point on a topic already
showing 2/2 losses:** stop picking local AI / Ollama as a topic for the near future.
Every topic with an actual win on this channel (n8n: episodes 7, 25, 29 — 2 confirmed
wins; Claude Code: episode 23 — 1 confirmed win, episode 27 lost on hook type not topic)
stays the safer choice until this file has real evidence local-AI can work here.

**What this does NOT mean:** that hook-writing discipline (cold-read test, checkable
claim in the first clause, no vague referents) was wasted work — episode 26 and 31 are
not directly comparable on hook quality (31's hook is genuinely better by every written
rule), and a bad topic can sink even a well-built hook. The lesson is about topic
selection, not about abandoning the hook rules already confirmed by real data elsewhere
(episodes 23, 25, 28, 29 all still stand as real wins built on those same rules).
from an older episode's research.

## Master performance table — all 27 Instagram Reels, verified per-post export (8.9.2026)

**Source and verification, stated plainly:** David exported this directly from Meta
Business Suite (per-post Insights, 11.8-7.9.2026 window) and ran it through ChatGPT
first, then handed both the raw CSV files and ChatGPT's summary numbers here for
independent verification against the actual rows. Every number ChatGPT reported (27
Reels, median views 217, mean views 215.15, median reach 138, and episode 1's exact
402 views/246 reach/11 likes/12 shares/5 saves/51s duration) was recomputed by hand from
the raw CSV and matched exactly — **VERIFIED DATA**, not something either AI invented.

**What this export does and doesn't contain:** views, reach, likes, shares, comments,
saves, follows, duration — per post. **No retention, no watch-time, no non-follower-
reach breakdown, no demographic data** is in this export; any statement about those
stays MISSING DATA until a richer export is pulled. Instagram and YouTube are kept
separate here on purpose — this table is Instagram only.

**Dataset-level VERIFIED DATA (n=27, recomputed by hand from the raw CSV):**
- Median views: 217 · mean views: 215.15 · max views: 402 (episode 1)
- Median reach: 138 · mean reach: 137.78 · max reach: 246 (episode 1)

**CALCULATED METRICS below** (like/share/save/engagement rate — all as a percentage of
*reach*, not views, per this file's own save-rate convention above) are computed from
the verified raw counts, not invented:

| Ep | Title | Dur(s) | Views | Reach | Likes | Shares | Comments | Saves | Like% | Share% | Save% | Engagement% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | One block of text (Custom Instructions) | 51 | 402 | 246 | 11 | 12 | 0 | 5 | 4.47 | 4.88 | 2.03 | 11.38 |
| 13 | ChatGPT can recall things about you, even in a brand new chat | 39 | 101 | 64 | 5 | 0 | 0 | 1 | 7.81 | 0.00 | 1.56 | 9.38 |
| 10 | Most leads go cold before anyone even replies | 39 | 123 | 82 | 6 | 0 | 0 | 1 | 7.32 | 0.00 | 1.22 | 8.54 |
| 7 | Your n8n agent has no idea it's wrong | 30 | 294 | 138 | 9 | 0 | 1 | 1 | 6.52 | 0.00 | 0.72 | 7.97 |
| 8 | A check said it passed. It lied | 27 | 144 | 101 | 6 | 0 | 1 | 1 | 5.94 | 0.00 | 0.99 | 7.92 |
| 3 | Your AI agent is already lying to you | 29 | 162 | 93 | 6 | 0 | 0 | 1 | 6.45 | 0.00 | 1.08 | 7.53 |
| 26 | This is a real AI model. My WiFi is off | 51 | 109 | 55 | 3 | 0 | 0 | 1 | 5.45 | 0.00 | 1.82 | 7.27 |
| 6 | Three things your AI agent still breaks on | 28 | 201 | 127 | 8 | 0 | 0 | 1 | 6.30 | 0.00 | 0.79 | 7.09 |
| 9 | This agent can send emails by itself. It never does | 35 | 217 | 133 | 7 | 0 | 1 | 1 | 5.26 | 0.00 | 0.75 | 6.77 |
| 14 | Everyone's sharing this claim that AI always lies to please you | 35 | 175 | 107 | 6 | 0 | 0 | 1 | 5.61 | 0.00 | 0.93 | 6.54 |
| 2 | Everyone says agent — almost nobody can tell you where the chatbot ends | 48 | 328 | 193 | 11 | 0 | 0 | 1 | 5.70 | 0.00 | 0.52 | 6.22 |
| 20 | ChatGPT was going to buy things for you | 49 | 127 | 67 | 3 | 0 | 0 | 1 | 4.48 | 0.00 | 1.49 | 5.97 |
| 25 | Your n8n retry doesn't just try again | 37 | 167 | 108 | 4 | 0 | 0 | 2 | 3.70 | 0.00 | 1.85 | 5.56 |
| 12 | Most people think Claude Code is only for programmers | 32 | 198 | 130 | 4 | 0 | 1 | 1 | 3.08 | 0.00 | 0.77 | 4.62 |
| 22 | If it failed right now, would you even know? | 56 | 158 | 100 | 3 | 0 | 0 | 1 | 3.00 | 0.00 | 1.00 | 4.00 |
| 21 | An AI browser can do your errands online now | 52 | 190 | 126 | 4 | 0 | 0 | 1 | 3.17 | 0.00 | 0.79 | 3.97 |
| 15 | Gemini just caught a mistake in this box, before you did | 59 | 239 | 155 | 5 | 0 | 0 | 1 | 3.23 | 0.00 | 0.65 | 3.87 |
| 19 | Claude keeps your files now. Not just this chat | 41 | 228 | 154 | 4 | 0 | 0 | 1 | 2.60 | 0.00 | 0.65 | 3.25 |
| 23 | 22 episodes in, one file keeps this from breaking | 54 | 262 | 185 | 5 | 0 | 0 | 1 | 2.70 | 0.00 | 0.54 | 3.24 |
| 18 | ChatGPT can use a website now. Not read it — click it | 43 | 257 | 157 | 4 | 0 | 0 | 1 | 2.55 | 0.00 | 0.64 | 3.18 |
| 5 | Your captions are hiding behind Instagram | 34 | 243 | 165 | 4 | 0 | 0 | 1 | 2.42 | 0.00 | 0.61 | 3.03 |
| 4 | This video almost shipped broken | 30 | 231 | 166 | 4 | 0 | 0 | 1 | 2.41 | 0.00 | 0.60 | 3.01 |
| 17 | One word broke this video, for someone who already knew the topic | 48 | 243 | 170 | 4 | 0 | 0 | 1 | 2.35 | 0.00 | 0.59 | 2.94 |
| 16 | We spent 15 videos building one system | 54 | 273 | 174 | 4 | 0 | 0 | 1 | 2.30 | 0.00 | 0.57 | 2.87 |
| 24 | Editors squeeze the picture to fit the audio | 51 | 216 | 153 | 3 | 0 | 0 | 1 | 1.96 | 0.00 | 0.65 | 2.61 |
| 11 | AI narration has a flaw you can't consciously name | 40 | 282 | 204 | 4 | 0 | 0 | 1 | 1.96 | 0.00 | 0.49 | 2.45 |
| 27 | I told Claude Code the wrong bug. On purpose | 37 | 239 | 167 | 2 | 0 | 0 | 1 | 1.20 | 0.00 | 0.60 | 1.80 |

**OBSERVATIONS (pattern, not yet a claim of cause):**
- Sorted by engagement rate, the top 6 (episodes 1, 13, 10, 7, 8, 3) are all either the
  paste-and-use mechanism (ep1) or a general, checkable claim about a failure mode
  (ep13's memory recall, ep10's lead response, ep7/8/3's agent-lying/check-lying
  claims) — consistent with, not contradicting, the hook-type findings already
  Confirmed above and in `hooks-guide.md`.
- **Every single one of the 26 non-ep1 episodes has exactly 0 shares.** This isn't
  "ep1 has more shares than average" — it's the only nonzero data point that exists.
  Treat any share-rate claim beyond "ep1 is currently the only episode anyone has
  shared" as unsupported.
- 20 of 27 episodes still show exactly 1 save (the same floor-effect problem flagged
  in the 3.9.2026 entry below still holds) — the save-rate spread above 1 save is
  thin (episodes 1 and 25 are the only two with more than 1).

**MISSING DATA, explicitly:** retention/watch-time/non-follower-reach for all 27 —
without it, no claim here can distinguish "the hook got people to tap" from "the video
held them," and `subsAttributed`/topic tagging gaps already noted in the 3.9.2026 entry
below still apply. YouTube performance for the same 27 concepts is tracked separately
(never combined with these Instagram numbers) and hasn't been cross-referenced against
this table yet — a real next step, not done here.

## Episode 32 — early signal, 7 hours in (14.9.2026)

David reported this directly, not pulled from the studio's tracked `/api/track` data:
**~250 combined Instagram + Facebook views, 7 hours after posting** — his own words,
"that's not what this was supposed to be." Logging this as what it is, not more:

- **UNKNOWN, not FACT**: this is a single early checkpoint, not a final number. Several
  episodes in the master table above (e.g. episode 9: 217, episode 6: 201) sit in a
  similar range as a *final* count after the view window closes — so 250 at 7 hours
  could still be tracking toward a normal-range or even above-average final result. No
  claim of underperformance is supportable yet from this one data point.
- Real per-episode view/engagement numbers live in the studio's own tracked state, not
  this file (per the standing rule above) — this entry exists only because he reported
  a live number directly; it should be reconciled against `/api/track`'s real number
  once the window closes, not treated as the record of truth itself.
- Episode 32 was the first episode built on the new `.tuk-n8n` real-tool UI kit
  (since corrected once already, 14.9.2026, after the CSS-recreation approach was
  flagged as looking fake) and the first episode where the music/narration mix bug
  (silently un-gated by `check.sh`, fixed 14.9.2026) is confirmed to have shipped with
  the bed essentially inaudible. Both are real, plausible confounds for a soft early
  number — genuinely different from prior episodes in two ways at once — but neither
  is confirmed as the cause. **Do not treat this as proof either fix mattered until the
  final number is in and, ideally, a second episode without both confounds is compared
  against it.**
- Action taken, not deferred: the two known defects above are already fixed going
  forward (episode 33 onward). No further action on episode 32 itself — it already
  shipped to Instagram and can't be swapped after the fact.

## Episode 34 — David's direct ear-based feedback after watching it (14.9.2026)

FACT, his own words, not measured: the background music "really disappeared" and there's
no cohesion between his voice/tone and the bed; he also called the delivery "boring." This
is despite `qa.py` measuring 15.2dB separation on this exact file — inside the tool's own
pass range (14-26dB), the same range episode 33 also shipped in (20.8dB there). **His ear
overrides the measurement, per this repo's own standing rule** — logged here so the next
session doesn't re-trust "qa.py passed" as proof the mix actually reads as audible. Pushed
`MUSIC_VOL` from 0.07 to 0.14 (render.sh) as a direct response — retested against episodes
32/33's real stems, lands at 14.2-14.8dB, the loud edge of the pass range rather than the
middle. Not yet re-verified against his ear on a new render; if 14dB-ish still reads as
gone, the fix is qa.py's own target/floor, not another volume bump.

He also flagged, separately, that episode 34's vocabulary and content density are too high
for a simple/general viewer — logged as a standing rule in `channel/hooks-guide.md` ("The
same rule applies to the whole script, not just the hook"), not just here.

**HYPOTHESIS, not yet confirmed**: episodes 32/33's early view numbers (see the 32 entry
above) may be partly explained by this same audibility/energy gap rather than only the
music-silence bug already found — both music and delivery read as "off" to him well after
the technical bugs were fixed. Not enough evidence to state this as fact.

## Delivery energy/tone — a second, separate ear complaint (14.9.2026)

David watched the re-rendered episode 34 and flagged two more things, distinct from the
music level itself: the word "node" (this channel's single most-repeated n8n term)
sometimes comes out sounding accented — logged with real detail in
`audio/voice/profile/pronunciation.json`'s notes, not yet measured or fixed, so the next
session doesn't have to re-discover it from scratch. And separately: **the voice's tone
needs to be genuinely captivating/exciting, in a way that holds an audience** — not just
technically correct (right words, right pacing) but emotionally engaging. This is a
delivery-energy note, not a script-writing one; nothing in this repo currently measures
or targets it (`voice_doctor.py` checks pacing/level/sibilance/endings, none of that is
"does this sound exciting"). Standing rule: keep this in mind for future episodes' voice
generation — likely means testing higher `--exaggeration` and/or a different reference
take for high-energy lines (the hook, the CTA), not something the current pipeline
already does automatically.

## Episode 33's hook is too long, per his direct feedback (14.9.2026)

He confirmed episode 33 ships as-is (not being redone), but flagged independently that
its hook doesn't hold the viewer — too long before it lands. This is a different failure
than the "claim in the first clause" fixes already made to episode 34's hook this
session; episode 33's hook was written and shipped before that discipline was applied
here. Standing note for `channel/hooks-guide.md`'s rotation log and every future
script: re-check hook length/pacing against the "lands in the first ~2 seconds, no
indirection" rule even for episodes that already cleared the wording-level checks —
episode 33 is a real example of a hook that was factually fine but still too slow.

## Episode 34's "node" accent drift — fixed by seed search, not respelling (14.9.2026)

Following up on the delivery-tone note above: he later narrowed the complaint to one
specific word, "node" (this channel's most-repeated n8n word), on episode 34 — "sounds
sometimes like Indian." Measured before guessing, same discipline as every entry in
`pronunciation.json`: `check_accent.py` had flagged exactly lines 1 and 2 (not-american
0.53 / 0.25 vs file median 0.014) — the two lines where "node" sits right after "n8n"
(respelled "en-eight-en"). Tested whether n8n was bleeding accent into node by scoring
several respellings ("nohd", "nowd", a paced comma after n8n) across 4 seeds each with
the same accent classifier — no respelling reliably beat baseline; single-seed wins
reversed on the next seed every time. **Conclusion: this was never a spelling problem,
it's seed variance** — `build_voice.py`'s retry loop only scores WER/rate/burst, never
accent, so a good- or bad-sounding take ships by chance depending on which one happens to
transcribe exactly right. Fix: searched candidate seeds per line for one where WER lands
at exactly 0.00 (so the retry loop has no reason to reroll away from it) AND the accent
classifier reads clean — found `--line-seeds 1:42,2:10` for episode 34, rebuilt, verified
clean (0.04 / 0.01), reshipped. Full detail and the exact numbers are in
`pronunciation.json`'s "node" note. Episode 33 was explicitly left untouched per his
instruction ("33 tashir" — it stays as shipped). **Standing takeaway for future episodes:
an accent-flagged line is a bad-take problem, not a spelling problem — search seeds with
the accent classifier + WER==0, don't reach for a respelling.**

## Real outside feedback from Roni Michaeli (Videya) on episode 32, and David's explicit goal (16.9.2026)

**FACT, direct feedback, screenshotted:** Roni Michaeli (owner of Videya, a marketing
professional already credited for real feedback on episode 31's hook in
`hooks-guide.md`) reviewed episode 32 ("n8n never tells you when a workflow dies") and
said directly: the hook assumes the viewer already knows what n8n is — this is
bottom-funnel content aimed at people already advanced in AI, not the general public.
"No business owner connects with 'hedging in n8n' — that's not the language they
speak." He confirmed n8n content could be right *if* the target audience is AI
technicians specifically, but flagged it as a mismatch for broad reach.

**Checked against our own real data, not accepted or dismissed on say-so:**
- The 28.8.2026 jargon audit already independently flagged "n8n" as unexplained
  brand-name jargon in episodes 7 and 10 — Roni's critique of episode 32 is the same
  finding, a second time, from an outside professional.
- The verified per-post Instagram export (Master performance table, 8.9.2026) shows
  n8n-topic episodes sitting mid-to-low on engagement rate (ep7: 7.97%, rank 4 of 27;
  ep25: 5.56%, rank 13 of 27) — not the top of the real, verified table. The channel's
  actual highest performers by real engagement (ep1, ep13, ep10, ep3) and by the
  "500+ club" analysis (ep2's 940, ep1's 662) are all **general, checkable claims any
  viewer can follow with zero prior AI/tool knowledge** — not n8n-specific, not
  jargon-dependent.
- Countervailing point from `demand-report.md`, stated so it isn't lost: n8n is the
  single highest measured search-demand topic, and its audience specifically overlaps
  with people who buy automation services (the word "sell" appeared 5x more often in
  the top-quartile results) — a real, separate reason n8n content existed here, tied to
  the paid-services engine, not to raw reach.

**David's explicit decision, asked directly and answered directly (16.9.2026): the goal
is maximum virality — followers, views, likes, reach, as much as possible, full stop.**
This resolves the tension above in one direction: reach beats funnel-fit. Consequence for
topic selection going forward: **prioritize general-audience-accessible topics and hooks
over jargon-heavy/insider ones**, even when the jargon-heavy topic has higher measured
YouTube search demand — the real Instagram engagement data already supports this
(general claims outperform n8n-specific ones in the actual verified export), and it now
also matches David's explicitly stated goal, not just this file's read of the numbers.
This doesn't retroactively make n8n content wrong to have made (episodes 7/25/29 were
built on real, then-current reasoning) — it changes what "highest-demand, best-fitting
angle" (the channel's own standing topic-selection rule) should optimize for next: reach
first, service-lead-gen second, when the two point in different directions.

**Not yet decided, flagged so it isn't silently dropped:** this is a real tradeoff
against the two-engine business model in `plan/business-model.html` (the paid engine
feeding the free one) — pure-virality content aimed at a general audience may convert to
paying clients less directly than n8n/automation content aimed at business owners
already searching for that exact service. David made the reach-first call explicitly;
worth revisiting together once there's real data on whether general-audience virality
still produces paid leads, rather than assuming it does or doesn't.

## Roberto Nickson (@rpn) — a real, sourced creator breakdown, not a copy-paste source (16.9.2026)

David asked to research a specific creator (@rpn, 904K followers, an AI-news/culture
account) after Roni pointed at him and after David sent one of his reels directly (a
GPT-5.6/Codex product-update reel). **Explicitly not treated as a script source** — per
the earlier standing decision this same day, copying another creator's script word-for-
word is real copyright/reputational risk and against this channel's own premise; this
entry extracts structure only, from a real third-party analysis, not from watching and
transcribing his content ourselves.

**Source: [blog.sandcastles.ai's creator breakdown of @rpn](https://blog.sandcastles.ai/p/creatorbreakdowns-rpn),
cross-checked against his own Beehiiv/podcast presence for background.** Concrete,
checkable tactics, not vague praise:
- **Topic selection, 5 pillars:** AI model launches, culture/creators, creative tools,
  hardware/devices, emerging AI agents — breaking model-launch news covered within ~24
  hours, treated as his primary content driver, not an occasional angle.
- **Posting cadence:** 8-9 posts/month, 574K average views, 4.5% engagement (the
  analysis's own highest-measured account in its series) — notably not high-frequency
  posting; fewer, higher-effort posts.
- **Five video formats, not one:** *Breakdowns* (~50% of output, "this tool is
  powerful" translation for a lay audience), *Case Studies* (his highest performers —
  "watch this tool BE powerful in real time," a live demonstration, not a description),
  *Skits* (non-news creative angles, 2x+ baseline performance — one example, "POV Life
  With Claude," hit 2.7M views, a 10.5x outlier), *Tutorials* (packaged as a reaction or
  movie-moment framing, not a generic how-to), *Listicles* (the exact same angle, e.g.
  "creators worth following," reframed differently each time it's reused).
- **Hook formula:** stakes escalation — reframing "a new model dropped" as "billions of
  people are unprepared for what happens next," not just stating the update. The
  analysis notes a formula has a ~2-3 iteration lifespan before the audience adapts and a
  fresh angle is needed — matches this file's own repeated finding that a winning hook
  type eventually needs rotation, not infinite reuse.
- **Stated differentiator:** speed (within 24h of real news) combined with cinematic
  visual production — the analysis calls this combination "1 of 1," not any single
  element alone.

**What's actually transferable to this channel, stated plainly so this doesn't become a
copy-the-creator exercise:** the *Case Study* format (show the tool actually doing the
thing, live, rather than describing it) is the closest match to this channel's own
existing standing format ("live test / escalate until it breaks," decided episode 21) —
external confirmation that this shape works elsewhere too, not a new idea to import. The
*Skits* format (a creative, non-news angle massively outperforming baseline) is genuinely
new territory for this channel, worth a real, deliberate experiment rather than assumed.
The stakes-escalation hook framing lines up with the Fear/personal-stakes research
already logged in `hooks-guide.md` (13.9.2026) — a third independent source now agreeing
with the same direction.

## How to update this file

After reviewing real numbers (via the studio, or `/api/agent`'s data), if the same
mechanism shows up in a second, independent episode: move the claim from *Current
hypotheses* to *Confirmed patterns*, and say which two episodes it's based on. If a
hypothesis gets clearly contradicted, don't delete it — mark it **REJECTED** and say why,
so the same idea doesn't get re-proposed later without remembering it was already tested.
