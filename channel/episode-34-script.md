# Episode 34 — script, ready to produce

## Topic
n8n's real execution model: a node doesn't run once per workflow execution — it runs
once for every item in the array it receives. Verified live (14.9.2026) against current
n8n docs and community threads: "if you have a list of 3 items passed into a node, n8n
will run that node once for item 1, once for item 2, and once for item 3." This is not
a bug or edge case — it's the whole data model, and it's why an HTTP Request node "on
40 rows" makes 40 real calls, not one call with 40 rows in it. The real fix node is
officially named "Loop Over Items (Split in Batches)" as of n8n's current docs (updated
June 2026) — not just "SplitInBatches," which is its old/internal name only.

## Why this topic, why now
- Genuinely new mechanism — not error-handling, not memory. Episodes 7/25/29/32 (error
  handling) and 33 (memory) are all covered; this is the execution/data model itself,
  which nothing on this channel has touched.
- Directly explains a real, common, costly mistake (surprise API bills, rate-limit
  failures that only show up at scale) — a genuine "oh, THAT'S why" reveal, the same
  shape as this channel's two strongest performers (episode 2: agent vs. chatbot,
  episode 7: n8n agent reliability).
- Uses the new real-tool UI kit (`export/tool-ui-kit.css`) for the first time on a full
  episode — n8n node cards, not the old generic dark termbox.

## Hook rules check (against `channel/hooks-guide.md`)
- **Type rotation**: 30 Contrarian Open, 31 Direct Address/Question, 32 Expert/
  Authority, 33 You-Focused Appeal + Specific Number. This one is **Shock/Surprise**
  (not used since episode 29) — a genuine surprise about how the tool actually works,
  not an anecdote.
- **Cold-read test**: "That n8n node you built didn't run once. It ran once for every
  item you sent it." Clear in one pass, checkable claim in the first two sentences, no
  vague referent.
- **Emotional register**: real, checkable stake — surprise API charges and rate-limit
  failures that only appear at real-world scale are genuine, common costs of not
  knowing this, not an invented worst case.

## Narration (8 lines)
1. That n8n node you built didn't run once. It ran once for every item you sent it.
2. That's n8n's real model: every node takes in a list of items, and runs its whole logic once per item on that list.
3. Send an HTTP Request node 40 rows, and it doesn't make one call with 40 rows in it — it makes 40 real calls.
4. That's why a workflow that "ran fine" on 3 test items can quietly rate-limit or blow through a bill the moment it hits 300.
5. The fix isn't more nodes — it's the Loop Over Items node, officially called Split in Batches, grouping items before they hit the expensive step.
6. Once you see it as items flowing through one at a time, not one batch of data, the whole canvas makes sense.
7. The exact setup's in the link in bio.
8. Follow for the setup that actually works.

## Verification notes
- Per-item node execution confirmed live against current n8n docs and community
  threads — not from memory or an older episode's assumptions.
- The Loop Over Items node's current official name ("Loop Over Items (Split in
  Batches)") confirmed against n8n's own docs, updated June 2026 — using the current
  name, not the old internal one, per the standing "verify the product is still real"
  rule.
