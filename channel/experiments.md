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

*(Empty — no deliberate experiment has been run yet. The first candidate, once episode
volume is high enough to have a real baseline to test against, is probably the hook-type
test already flagged as a hypothesis in content-memory.md: a build-failure-first episode
vs. a clean-demo episode on the same tool, holding everything else constant.)*
