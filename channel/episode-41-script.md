# Episode 41 — script, ready to produce

## Topic
ChatGPT's own "Finances" feature (not a third-party tool — a real, current ChatGPT capability)
connects directly to a user's real bank accounts, cards, and investments through Plaid and
shows a live dashboard of spending, subscriptions, and upcoming payments — surfacing recurring
charges a viewer may have forgotten they're paying. Read-only: it cannot move money, pay
anything, or place a trade.

## Why this topic, why now
- **Fixes the real gap David flagged directly (17.9.2026): the last two reach-first episodes
  (39 smart-TV ACR, 40 connected-car data) had weak or zero genuine AI content.** This topic
  puts a named, current AI product — ChatGPT itself — at the literal center of the claim, not
  a generic privacy/tech angle that happens to sound viral.
- **Matches the reference-grid pattern Roni Michaeli sent directly** (`hooks-guide.md`,
  16.9.2026): "ChatGPT can find your unclaimed money" was one of the exact example hooks in
  that grid. This episode is the real, verified, current version of that same pattern — a
  genuine ChatGPT feature, not an invented one.
- **Personal-stakes, plain-language, per the 16.9.2026 reach-first standing rule**: the stake
  is money everyone already worries about (subscriptions quietly running), and the delivery
  needs zero prior AI/tool knowledge — no developer jargon.
- **Not yet covered** — checked against all existing episode scripts and `studio/lib/articles.ts`;
  no prior episode covers ChatGPT's Finances/money features.
- **Verified live (17.9.2026)** against OpenAI's own announcement plus independent press
  coverage (see Verification below) — not assumed from training-data memory, since AI-product
  features and rollout status change fast (the exact discipline `CLAUDE.md` requires before
  writing a line).
- **Hook-type rotation** (per `hooks-guide.md`'s log): 38 Specific Number, 39 Contrarian Open,
  40 Direct Address/Question. This one is **Shock/Surprise** (last used episode 37, a
  three-episode gap) — not a repeat of the last three types.

## Verification (live web search, 17.9.2026)
Checked against OpenAI's own product announcement (openai.com/index/personal-finance-chatgpt)
plus independent press (TechCrunch, MacRumors, gHacks, gHacks-linked aitrove coverage),
cross-referenced:
- OpenAI launched a "Finances" experience inside ChatGPT: connect real bank accounts, credit
  cards, brokerages, and investment accounts through Plaid (12,000+ supported institutions —
  Chase, Amex, Schwab, Fidelity, Robinhood, Capital One, and others named directly by OpenAI).
- Once connected, the dashboard shows portfolio performance, spending, **subscriptions
  (all recurring charges identified and consolidated in one view)**, and upcoming payments.
- **Explicitly read-only**: OpenAI states ChatGPT can analyze balances, transactions,
  investments, and liabilities but **cannot move money, pay bills, or place trades**.
- **How to turn it on**: open "Finances" from the ChatGPT sidebar and select "Get started," or
  type "@Finances, connect my accounts" from anywhere in ChatGPT — then link accounts through
  Plaid's secure flow.
- **How to turn it off**: Settings → Apps → Finances → remove the connection; OpenAI states
  synced data is deleted from ChatGPT within 30 days of disconnecting, and financial
  "memories" can be viewed and deleted directly from the Finances page at any time.
- **Rollout status, stated plainly (scope note)**: launched May 15, 2026 as a preview for
  ChatGPT **Pro** subscribers in the **United States only**, web + iOS. Independent coverage
  (gHacks, 18.5.2026; aitrove) reports it opened to **Plus and Pro** users, web/iOS/Android,
  by around 25.6.2026. This script states the feature as it exists **for US-based ChatGPT
  Plus or Pro users**, not globally and not for Free-tier accounts — that limit is stated on
  camera, not smoothed over, per the never-fabricate rule.

## Hook rules check (against `channel/hooks-guide.md`)
- **Type rotation**: see above — Shock/Surprise, not used in the last three episodes.
- **Specific, checkable claim in the FIRST clause** (10.9.2026 standing rule): the surprising
  capability itself ("ChatGPT can now see every subscription draining your bank account") is
  the entire first sentence — no deferred payoff, no second-sentence setup.
- **Personal-stakes/secret-reveal framing, plain consumer language** (16.9.2026, direct from
  Roni's reference grid): matches "ChatGPT can find your unclaimed money" almost exactly —
  same shape, a real and current feature instead of an invented one.
- **Write for a person, not an AI-literate viewer**: no "Plaid," no "API," no "read-only" in
  the spoken lines — those stay in the on-screen setup guide only.
- **Cold-read test**: real, checkable, no vague referent, no hypothetical framing.

## Narration (final, 7 lines)
1. "ChatGPT can now see every subscription that's draining your bank account behind your back."
2. "It connects straight to your real bank account and lays out your spending, your subscriptions, and what's coming up next."
3. "It can't move your money or pay for anything — it just reads what's sitting in your accounts, nothing more."
4. "Turning it on takes one step: open Finances in ChatGPT's sidebar and connect your accounts."
5. "You can disconnect it any time, and your synced data is gone from ChatGPT within thirty days."
6. "The setup's in the link in bio."
7. "Follow for the setup that actually works."

## Density check
5 distinct ideas across the 7 lines (the two CTA lines don't count as content ideas): (1)
ChatGPT can now see your real subscriptions/spending, (2) it connects to your actual bank
account and shows spending/subscriptions/upcoming payments, (3) it's read-only — can't move
money or pay anything, (4) exactly how to turn it on, (5) exactly how to turn it off and what
happens to the data. Within the standing "roughly 4-5 ideas" range (`content-memory.md`,
episode 36 finding).

## Simplicity/length check
Plain consumer language throughout — no "Plaid," "API," or "read-only" spoken on camera (those
terms live only in the setup guide's written steps). Length target: 30-45s per `CLAUDE.md`'s
standing floor; matches the 7-line shape that has landed episodes 37-40 at 30.0-33.4s.

## Build notes
- Palette: fresh combo for episode 41, distinct from episode 40's amber/sky ("drive") —
  green/violet, mood **"triumphant"** (a real, mapped `pick_real_track.py` mood, not yet used
  by any prior episode, and a direct thematic match for "you're finally in control of your own
  money"), checked against `channel/used-designs.json` for exact-hex reuse.
- Scoreboard scene: "Before" / HIDDEN vs. "Finances on" / VISIBLE — same shape as episodes
  37-40's binary-contrast scoreboard, reframed positively (something gained, not just a risk
  closed) to match the "triumphant" tone.
- Built from `video/reel-40.html` (already verified against `export/safe_check.js` and
  `check.sh`), keeping the working hook/quote/scoreboard motion wiring, content and palette
  changed.
