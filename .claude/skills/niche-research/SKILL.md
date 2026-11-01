---
name: niche-research
description: "Find what is already working in a niche before writing a script. Use when the user asks what to post, which format or hook is working, what competitors are doing, or wants ideas for the next episode from real short-form posts. Ranks posts by views divided by the author's followers (the outlier ratio), flags repeated formats and comment-bait hooks, and hands the top few to the breakdown skill. Works from links the user pastes (free) or from a paid Oriane search (credits, always confirmed first)."
metadata:
  version: 1.0.0
---

# Niche research

Goal: decide the next format from evidence, not from taste. A post that gets
several times more views than its author has followers is evidence the
*format* did the work. A post from a 5M-follower account with 5M views is not
evidence of much.

This skill only finds and ranks candidates. It does not write the script.
Next steps: `breakdown` (per post) → hook choice in `channel/hooks-guide.md` →
script. See `channel/research-pipeline.md` for the whole chain.

## Hard rules

1. **Paid calls need a yes first.** Every Oriane call that returns results
   costs credits (see the cost table). Before running one, state the handle or
   query, the limit, the projection and the credit cost, and wait for the user's
   OK. Empty results cost 0.
2. **Public posts only, for inspiration.** Analyse the format and the hook.
   Never re-publish or closely copy someone else's video.
3. **Samples are small.** A ranking from 30 posts is a hypothesis. Say so.
   Confirm a format only after it shows up in two independent posts or episodes
   (the rule in `channel/content-memory.md`).
4. **Never invent numbers.** Every figure comes from the saved data file. Any
   estimate is labelled ASSUMPTION.

## Sources, in order of preference

| Source | Cost | Use it when |
|---|---|---|
| Links the user pastes (Explore, saved reels, competitors) | Free | Always possible. Ask for 10–20 links. |
| Oriane, **handle mode** (`handle`, one competitor account) | 50 credits per call with `default` projection (limit does not change the price, max 100) | The user names 3–10 competitor accounts. Best signal: the full post list with views and followers. |
| Oriane, **caption mode** (`caption`, a phrase) | Same price | Only for a very specific phrase. A broad phrase like "AI tools" pulls in off-niche accounts (tested 2026-11-01: top results were a foundation, a shoe brand and an editing course). |

Oriane's index covers a sample of Instagram posts, not a complete live feed.
Handle mode returned 154 posts for one account and the tool returned the 30 the
call asked for. Check the `totalCount` in the response metadata.

## Procedure

1. **Context first.** Read only the relevant parts of `channel/content-memory.md`
   (what already worked, what was tried) and `channel/demand-report.md` (search
   demand). Do not re-read them if already in this conversation.
2. **Choose the source** (table above). If paid, get the OK.
3. **Save the raw response to a JSON file** in the scratchpad, for example
   `<scratchpad>/niche/<date>-<handle-or-query>.json`. The script reads files,
   not chat output.
4. **Rank:**
   ```
   python3 .claude/skills/niche-research/scripts/outlier.py <file.json> --min-views 20000 --min-ratio 3 --top 20
   ```
   Thresholds are ASSUMPTIONS to tune, not measured values. For hand-made
   links, fill a CSV with the header `handle,views,followers,published,format,caption,url`
   and pass the CSV instead.
5. **Relevance pass (by eye, required).** Drop accounts or posts that are not
   about the channel's niche (AI tools, AI-made video). The script cannot judge
   this.
6. **Pattern pass.** Count the formats among the kept posts, look at the first
   line of each caption (the hook), and check the bait flag. Example seen on
   2026-11-01: all 30 posts pulled from each of two AI-tools accounts (60 of 60)
   opened with "Comment X and I'll send you…". That is a repeated format to
   note, not a reason to copy the bait.
7. **Break down the top 3–5** with the `breakdown` skill (user-level skill, not
   in this repo; it uses `video-download` and `video-analysis`). Pass the post
   URLs.
8. **Write the report** to `channel/niche-research/<YYYY-MM-DD>-<slug>.md`:
   - the source and its credit cost, the thresholds used, sample size
   - the ranked table (top 10)
   - formats and hooks that repeat, each marked as one-post or repeated
   - 2–3 candidate formats for the next episode, with the evidence for each
   - what is unknown (sample size, relevance, data freshness)
9. **Do not write to `content-memory.md` from one search.** Only add a pattern
   there after it shows up in two independent episodes.

## Interpreting the ratio

- `views ÷ followers` (script column `ratio`). `viewsRatePerFollowers` in the
  raw Oriane data is the same thing **times 100** (645 means 6.45x). The script
  computes it from the two counts so the scale cannot be mixed up.
- Big accounts have low ratios even when their videos are good. Compare within
  a similar follower range where possible.
- Calibration from the two handle tests (2026-11-01). On a 31k-follower account
  the top post reached 6.7x and only 4 of 30 posts passed 3x. On a 1.3M-follower
  account the top reached 6.5x. So with the default `--min-ratio 3`, expect only
  a handful of posts per account. Lower the threshold only with an explicit note
  in the report.
- Recent posts matter more. Check the `published` column; posts from several
  months ago may reflect an old trend.

## What this skill cannot tell you

- Why a post worked beyond the format and hook. Use `breakdown` for that.
- Whether a format will work for *this* channel. That is tested by publishing,
  and measured in the studio (`/api/track`).
- Anything about the post's audience. The data has no audience breakdown.

## Tests

`python3 -m unittest discover -s .claude/skills/niche-research/scripts -p "test_*.py" -v`
(stdlib only; the fixture is a trimmed real Oriane response from 2026-11-01).
