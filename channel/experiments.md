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
