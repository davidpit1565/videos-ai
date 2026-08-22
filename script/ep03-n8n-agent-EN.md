# Episode 03 — "Your first n8n agent, end to end"

**Format:** long-form YouTube (target 22–30 min) + a 55s reel cut from it
**Topic:** `n8n ai agent tutorial` — **median 233,070 views**, the highest in our measurement
**Why third:** it is the highest measured demand *and* the first revenue line. The audience
searching this is not trying to understand agents, it is trying to earn from them — `sell`
appeared 5× more often in the top quartile than any other word.

**Blocked on:** an n8n account (free tier exists; not yet tested here). Nothing else.

**Length is deliberate.** On YouTube 30-minutes-plus has a median of 206,275 against 25,900
for 1.5–10 minutes. The hits in this topic are "Zero to Hero Course" and "8+ Hour Course" —
a complete build, not a glimpse. So this is the flagship long cut, and the reel is a cut *of*
it, never the other way round.

---

## What it builds

An agent that reads a new email, decides whether it needs a reply, drafts one, and **stops**.
It never sends. That choice is the episode's spine, not a limitation to apologise for.

Chosen because: it is the second-highest measured topic that can be built without a paid
account, the failure mode is visible within one screen, and a draft is reversible — which is
the rule the previous episode ends on.

## The spine

| Section | What is on screen | The point |
|---|---|---|
| Cold open | The finished agent drafting a reply, in real time | Proof before promise |
| The account | n8n signup, the free tier, where the limit actually bites | No surprises later |
| The trigger | Gmail node, the OAuth screen, the consent nobody explains | This is where people quit |
| The brain | The model node, the system prompt in full, on screen, readable | The prompt IS the product |
| The tool | Create-draft, not send. The setting that makes it a draft | Reversible by construction |
| **The loop** | It replies to its own draft. Watch it happen | The defect, live |
| **The fix** | The one filter that stops it, and why | Two lines |
| The check | Ten real emails. What it got right, what it did not | Measured, not claimed |
| The cost | Actual API spend for those ten | A real number or none |
| What it cannot do | Attachments, threads, anything time-sensitive | The honest close |

## The defect that gets equal screen time

**The agent answers its own draft.** The draft lands in the mailbox, the trigger sees a new
message, and it goes again. It is the single most common n8n-agent failure and almost no
tutorial shows it, because showing it means admitting the first build was wrong.

We show it running, then fix it, and the fix is boring: filter the trigger to exclude anything
the agent itself authored. Two lines. The lesson is not the filter — it is that **an agent
acting on its own output is the default, and you have to design against it.**

## Numbers this episode must carry

Every one measured on camera, or the claim is cut:

- **API cost for ten emails** — the real figure, whatever it is
- **How many of the ten needed no edit** — counted, not estimated
- **Time from empty canvas to first working draft** — the timer stays on screen
- **The n8n free-tier limit** and when this build hits it

If a number cannot be measured on camera it does not go in the script. There is no estimate
in this episode.

## The reel cut (55s)

Hook is the defect, not the build: *"Your first AI agent will reply to itself. Here's the
two-line fix."* The full build lives in the long cut; the reel exists to send people there,
and the defect is what makes anyone care.

## Not in this episode

- Selling it. That is episode 04, and it needs a real client first.
- Any other trigger — Slack, webhooks, sheets. One trigger, done properly.
- A comparison against Make or Zapier. Different episode, different demand.
