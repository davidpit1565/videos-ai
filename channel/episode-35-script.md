# Episode 35 — script, ready to produce

## Topic
n8n's webhook trigger, by default, waits until the whole automation finishes before it
replies "got it" back to whatever triggered it (a payment, a form, an incoming message).
Verified live (15.9.2026) against current n8n docs and community reports: the "Respond"
setting on the Webhook node has an "Immediately" option and a "When Last Node Finishes"
option — the second one is what most people leave it on, and it means the reply is held
until the entire automation is done. If that takes more than a few seconds, whatever sent
the original event has no way to know it's still being handled — from its side, it looks
like the message never arrived, so it does the only reasonable thing: it sends the exact
same event again. n8n has no memory of "I already saw this one" built in, so it treats
the resend as a brand new event and runs the whole automation a second time — real email,
real order, real action, twice. n8n's own cloud platform also hard-cuts a reply at 100
seconds if the automation still hasn't finished, which makes the same failure worse, not
better, the longer an automation takes.

## Why this topic, why now
- Genuinely new mechanism on this channel's highest-demand topic (n8n, 233k median
  search demand per `channel/demand-report.md`) — not covered by any of episodes 7
  (agent doesn't self-check tool failures), 22/29 (Continue-On-Fail masking a failed
  node), 25 (a node's OWN retry setting replaying one step), 32 (no alert on a failed
  run), 33 (memory window default), or 34 (per-item execution). Those are all about a
  workflow failing quietly or replaying one internal step; this is about the trigger
  itself firing the ENTIRE workflow twice from one real-world event.
- Directly costly and checkable: a real double-send (email, order, notification) is the
  kind of "oh, THAT'S why" reveal this channel's two strongest performers (episode 2,
  episode 7) share — a surprising mechanism behind a real, already-felt problem
  ("why did this customer get two emails").
- Uses the n8n UI kit (`export/tool-ui-kit.css`'s `.n8n-diamond`/webhook node styling)
  for the webhook + HTTP flow, continuing this channel's real-tool-screens direction.

## Hook rules check (against `channel/hooks-guide.md`)
- **Type rotation**: 30 Contrarian Open, 31 Direct Address/Question, 32 Expert/
  Authority, 33 You-Focused Appeal + Specific Number, 34 Shock/Surprise. This one is
  **Contrarian Open** (last used episode 30, not back-to-back) — it contradicts the
  natural assumption that "it already said done" means it only happened once.
- **Write for a person, not an AI-literate viewer**: the hook says "automation," not
  "webhook" or "node" — those terms stay out of the hook line entirely and get
  introduced, once, plainly, in the body.
- **Cold-read test**: one clause, a real and checkable claim (an automation can say
  "done" and still repeat itself), no vague referent, no hypothetical/imagined scenario
  — this is a real, current, default behavior, not a "what if."
- **Specific claim in the first clause**: the surprising part ("still do it again") is
  in the same sentence as the setup, not deferred to a second sentence.
- **Emotional register**: mildly unsettling/curiosity — something you already trusted
  ("it said done") quietly wasn't telling the whole truth. Real stake (a duplicate
  email or order), not an invented worst case.

## Narration (8 lines)
1. An automation built in n8n can already say "done" — and still go do the exact same thing again.
2. Here's why: it waits for the whole thing to finish, and only then replies.
3. If it takes more than a few seconds, it looks like the message never arrived — and gets sent again.
4. It has no memory of ever seeing that one. It just runs the entire automation again, real actions included.
5. That's how one real event turns into two real emails, or two real charges — from a system that never once said it failed.
6. The fix: reply right away, then do the real work after — nothing ever sits long enough to be sent twice.
7. The setup's in the link in bio.
8. Follow for the setup that actually works.

(Only lines 1-6 are new; lines 7-8 are the locked, pre-approved outro clips — see
`audio/voice/profile/canonical-lines.json` — used byte-for-byte, no regeneration.
Lines 2/3/5/6 were reworded once against `audio/script_lint.py`'s flags before any
voice generation — "before," "whatever"/"first," "orders," and "instant"/"waiting" all
carry endings this voice measurably swallows; reworded around them per this repo's own
"swapping the word costs nothing" rule, not respelled.

Line 1 measured badly accented (not-american 0.39-0.99) across every one of 10 seeds
tried — not seed variance, a structural problem, unlike episode 34's "node" fix. Tested
the hypothesis directly: dropping "n8n" from the hook entirely still scored badly
(0.64-0.99), but moving "n8n" out of the sentence-initial position ("Your ___ automation
can already say...") to "An automation built in n8n can already say..." scored clean
across all 3 tested seeds (0.06-0.19). The culprit was the opening clause construction
itself, not the product name. A shorter variant ("An n8n automation can already say...")
was tested too and came back inconsistent again (3 of 4 seeds bad) — the exact
"automation built in n8n" phrasing is what measured reliably clean, so that's what
shipped, not the shorter-sounding alternative.

Line 4 hit the identical structural issue — it also opened with "n8n" as the very first
word ("n8n has no memory of..."), and measured badly accented (0.23-0.32) even after a
clean word-timing seed was found for the swallowed "memory." Reworded to "It has no
memory of..." (the referent is already established by lines 1-3) and re-searched: seed
42 measured na=0.005, wer=0.00, clean.

Second round, after the level-repair gate still flagged "event" (line 6) and "already"
(line 4) as swallowed: turned out build_voice.py's own per-line speed-up correction
("sped up x1.20" for line 6, applied at generation time because the raw take ran slower
than the target rate) compresses word durations further than an isolated measurement of
the raw take shows — a seed that measured a healthy margin in isolation still landed
under the rushed floor once the real pipeline's own speed correction ran on it. Fixing
this by hunting for a better seed chased a moving target. Fixed for real by shortening
both lines instead, removing the repeated word each flag landed on rather than trying to
out-run the compression: line 4 -> "It has no memory of ever seeing that one," line 6 ->
"The fix: reply right away, then do the real work after — nothing ever sits long enough
to be sent twice." Shorter lines need less speed correction in the first place.)

## Simplicity check (per hooks-guide.md's 14.9.2026 standing rule)
Reread for a viewer with zero n8n background: "automation," "the whole thing," "whatever
sent it," "the entire automation," "reply back" — no internal product terms (webhook,
node, trigger, Respond to Webhook) anywhere in the spoken narration. Those names are
introduced only visually, on screen, and in the setup guide, never spoken.

## Verification notes
- The Webhook node's "Respond" options ("Immediately" vs "When Last Node Finishes") and
  the resulting duplicate-execution risk on a slow automation, confirmed live against
  n8n's own current docs (`docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook`
  and `.../respondtowebhook`) and a live n8n Community forum thread describing this
  exact failure mode — not from memory or an older episode's assumptions.
- n8n Cloud's 100-second hard timeout on an unanswered webhook (524 response) confirmed
  the same way. No specific third-party sender (Stripe, Twilio, etc.) is named in the
  narration, since their individual retry policies weren't independently verified this
  session — the script states only what n8n's own docs and community confirm.
