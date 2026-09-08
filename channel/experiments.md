# Experiments — deliberate tests only

Not every Reel is an experiment. Most episodes just ship and produce another data point
for `channel/content-memory.md`. An entry belongs in this file only when there's an
explicit, stated change and an explicit, stated thing it's meant to move:

> We changed **X** to test whether **Y** changes.

If you can't fill in both X and Y before publishing, it isn't an experiment yet — it's
just the next episode. Log it here *before* publishing, then come back and fill in the
result once the studio's real numbers are in (give it enough days for saves/views to
settle, not the first hour).

---

## Template for a new entry

```
### [date] — [episode #/title]

**Changed:** what specifically is different from the last few episodes.
**To test:** what we expect to move, and in which direction.
**Baseline:** what similar past episodes did on the same metric (or "no comparable
  episode yet" if this is genuinely new).
**Result:** [fill in after the studio has real numbers — cite the actual figures,
  never "seemed to do well"]
**Verdict:** CONFIRMED / REJECTED / INCONCLUSIVE (say why for INCONCLUSIVE — usually
  "not enough plays yet" or "too many things changed at once to isolate the cause")
**Feeds into:** which line in content-memory.md this updates, if any.
```

---

## Before running a hook-type experiment as two full episodes

The production pipeline (voice clone, `voice_doctor.py`, karaoke captions, `safe_check.js`,
full render QA) is expensive per episode — don't spend two full productions just to compare
two hooks on the same underlying content. Instagram's own Trial Reels feature is built for
exactly this: it shows a Reel to non-followers first, before deciding whether to push it
further. Check whether a hook question can be answered that way before defaulting to two
parallel full episodes.

**Checked on this account, 28.8.2026: not available.** No "Trial"/"Test" toggle anywhere
in the share screen (Tag people / Add location / Rename audio / Add AI label / Audience /
Also share on... / More options), and nothing under Settings either. Account is already
Professional. Meta rolls this out gradually per account, not to everyone at once — this is
a FACT about this account right now, not a permanent one.

**Likely explanation (HYPOTHESIS, not confirmed by Meta):** unofficial sources report a
~1,000-follower threshold for eligibility. This account had 94 followers on 28.8.2026 —
well under that reported line. Meta hasn't published the exact number anywhere official,
so treat the threshold itself as unconfirmed, but it's consistent with what we're seeing.
Re-check once follower count is meaningfully past 1,000, not before — no setting to
request early access exists.

## Batch 1 — controlled learning loop, not "which video wins" (8.9.2026)

Prompted directly by David/ChatGPT's review of the Master Table in `content-memory.md`:
episode 1's outlier result (only Reel with any shares, highest save-rate, ~2x the
next-highest engagement rate) is confounded — it's simultaneously the only episode
built around a paste-and-use *utility* mechanism, the weakest topic by measured search
demand (`demand-report.md`: "custom instructions chatgpt" median 11,880 vs. n8n's
233,070 — the single lowest of the nine topics measured), a specific hook, and a
specific 51-second duration. The question worth answering isn't "was episode 1 good"
— it's **which single variable, isolated, actually moves save/share behavior.**

**Why this is a small batch, not six parallel tests:** Trial Reels aren't available on
this account (see the note above — no toggle exists, likely a followers threshold).
Without that mechanism, every test costs one full production (voice, render, full
`check.sh` gate) — expensive enough that running six confounds-worth of tests at once
isn't realistic at this channel's ~4-5 episodes/week pace. Batch 1 is deliberately two
experiments, run as the next two English episodes in the normal slate — not additional
videos on top of it. A candidate list of four more (kept for Batch 2) is at the bottom.

**Baseline every experiment below is measured against**, computed from the 26
non-episode-1 rows of the Master Table in `content-memory.md` (episode 1 itself
excluded — it's the thing being explained, not the baseline):
- Median save-rate: **0.74%** (saves/reach)
- Share-rate: **0%** on 26 of 26 episodes (zero episodes besides ep1 have any share)
- Median engagement-rate: **4.3%** ((likes+comments+shares+saves)/reach)

### Experiment 1 — Utility × Topic (isolates utility from "Custom Instructions" itself)

**Changed:** build the next single-artifact "paste this and use it" episode on a topic
that is NOT ChatGPT/Custom Instructions — e.g. one exact n8n node config (the
idempotency-check fix already shipped as episode 25's *topic*, but reframed here as a
literal "here's the one node, paste these exact settings" artifact) or one CLAUDE.md
rule block. Topic should sit on a *stronger* measured-demand keyword than "custom
instructions chatgpt" (weakest of nine in `demand-report.md`) — n8n or Claude Code,
both already 2-for-2 on this channel per `hooks-guide.md`.

**To test:** H1 from `content-memory.md` — does the *utility mechanism* (single
paste-and-use artifact) drive save/share behavior independent of the specific topic,
or was episode 1's result actually about ChatGPT Custom Instructions itself (unlikely,
given it's the weakest-demand topic measured, but not yet ruled out)?

**Held constant:** hook type (general, checkable claim — the Confirmed pattern from
4.9.2026), duration (~45-55s, matching episode 1's 51s), CTA ("Follow for the setup
that actually works").

**Baseline:** save-rate 0.74%, share-rate 0%, engagement-rate 4.3% (see above).

**Win:** save-rate ≥1.5% (roughly 2x baseline) **or** at least 1 share (breaks the
26-of-26 zero-share pattern) — either alone counts, both together is a strong win.
**Lose:** save-rate ≤1.0% and 0 shares — statistically indistinguishable from the
26-episode baseline, meaning episode 1's result doesn't generalize past its own topic.
**Inconclusive:** anything between (e.g. save-rate 1.0-1.5%, still 0 shares) — say so,
don't force a verdict.

**Result:** [fill in once real numbers are in]
**Verdict:** RUNNING
**Feeds into:** H1 in `content-memory.md`.

### Experiment 2 — Capability × Demo (Engine A / discovery, tests a mechanism episode 1 does NOT use)

**Changed:** the episode after Experiment 1 leads with an unexpected AI capability
reveal — proof-first (the capability shown working, in frame, before any explanation)
— rather than a failure/limitation framing, which is this channel's current dominant
DNA (per `content-memory.md`'s pattern-shapes and losing/winning-formats sections).

**To test:** does a pure "wait — AI can actually do that?" discovery framing move
reach/engagement independent of the failure-and-fix shape that's driven every
Confirmed pattern so far? This is a different axis from Experiment 1 (discovery vs.
utility), deliberately — running both at once would confound which one moved a shared
metric.

**Held constant:** hook type stays a general, checkable claim (same Confirmed rule);
topic drawn from the same demand-report.md pool used for other high performers, so
demand isn't the variable either.

**Baseline:** save-rate 0.74%, share-rate 0%, engagement-rate 4.3%.

**Win:** engagement-rate ≥6% (meaningfully above baseline, in range of episodes 7/8/3
which already do this partially) **or** reach/views meaningfully above the 138/217
medians (discovery framing is a reach play more than a save play, per the ENGINE A
rationale — so a reach win counts even without a matching save-rate win).
**Lose:** engagement-rate and reach both sit at or below baseline — the discovery
framing doesn't outperform the failure-framing DNA already in place.

**Result:** [fill in once real numbers are in]
**Verdict:** RUNNING
**Feeds into:** a new entry in `content-memory.md`'s Current hypotheses (currently
nothing there addresses discovery-vs-failure framing directly).

### Batch 2 candidates (not started — logged so they aren't lost or re-invented)

From the same six-experiment menu David/ChatGPT proposed, these four wait for Batch 1's
results (running two more in parallel now would confound which batch caused what):

- **Utility × Workflow** — does the utility mechanism (Experiment 1) hold up for a
  multi-step workflow artifact, not just a single paste?
- **Failure × Human consequence vs. Failure × mechanism-first** — same failure topic,
  does leading with the human cost ("this can send the wrong email") outperform leading
  with the technical mechanism ("n8n's retry uses at-least-once delivery")? Needs two
  productions of adjacent content, which is why it's deferred, not run in Batch 1.
- **Same concept × 3 hooks** — the most direct test of "packaging is the variable," and
  the most expensive (three productions of near-identical content for one comparison).
- **Failure × Proof-first ordering** — do episodes that show the broken result before
  explaining the mechanism (already partially true for episodes 7, 8, 22) outperform
  ones that explain first? Needs a clean pair that isolates ordering alone.

## Log

### NOT AN EXPERIMENT — Reel 13, "ChatGPT remembers you, even in a new chat"

David confirmed: Reel 13 went out as a normal upload through the studio, not through the
Trial toggle. So this was never actually the trial-mechanism test the earlier version of
this entry described — correcting the record rather than leaving a false RUNNING entry.
Reel 13's real numbers (once in) are just the next ordinary data point for
`content-memory.md`, same as any other episode — not a Trial Reel result, and not a
baseline for comparing Trial Reel performance.

### CANCELLED — Reel 14 as a Trial Reel, "We tried to make Claude flatter us"

Never ran. The Trial toggle isn't available on this account (see the note above) — checked
the share screen and Settings, nothing there. Reel 14 goes out as a normal upload through
the studio instead, same as every other episode so far. Its real numbers are an ordinary
data point for `content-memory.md`, not a Trial Reel result — don't compare it against a
"trial baseline" that never existed.

*(No other deliberate experiment has been run yet. The next candidate after these two,
once episode volume is high enough to have a real baseline to test against, is probably
the hook-type test already flagged as a hypothesis in content-memory.md: a
build-failure-first episode vs. a clean-demo episode on the same tool, holding everything
else constant.)*
