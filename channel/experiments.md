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

## Log

### [pending] — Reel 13, "ChatGPT remembers you, even in a new chat"

**Changed:** Publish as an Instagram Trial Reel (shown to non-followers first) instead of
a normal full push.
**To test:** Whether retention/completion on the trial clears the bar to justify a full
push. `channel/demand-report.md` doesn't cover this topic at all (ChatGPT memory wasn't
one of the eight measured queries), so this is a genuine UNKNOWN, not a guess dressed up
as a test.
**Baseline:** No comparable episode — first time this mechanism is used.
**Result:** [fill in from Instagram's own Trial Reel screen — retention/completion for a
Trial Reel do **not** flow into `/api/track` or the studio; that pull only ever gets
views/likes/saves/comments/shares. Read the trial numbers directly off Instagram, then
record them here by hand.]
**Verdict:** [fill in after the trial window closes]
**Feeds into:** whether Trial Reels becomes the default publish path for future episodes
with unmeasured demand.

*(No other deliberate experiment has been run yet. The next candidate, once episode volume
is high enough to have a real baseline to test against, is probably the hook-type test
already flagged as a hypothesis in content-memory.md: a build-failure-first episode vs. a
clean-demo episode on the same tool, holding everything else constant.)*
