# Episode (number TBD, draft, ON HOLD) — Flow, the app David built

**Status: DO NOT PRODUCE OR SHIP.** Per David's own instruction (15.9.2026): prepare the
topic and script groundwork here first, but the actual build/render/publish only happens
once `fin-flow` is live on the App Store — it isn't yet (still needs the Apple Developer
account enrollment + a Mac/Xcode build, per that repo's own `APP_STORE_SUBMISSION.md`).
This file exists so the topic is locked and ready the moment it ships — not so it gets
produced early. **Not episode 36** — that number went to a different episode (produced
16.9.2026, general-audience/personal-stakes topic per the reach-first pivot) since this
one is still blocked. Whatever number is next-available when this actually ships is its
real number.

## What the app actually is (read from `davidpit1565/fin-flow`, not assumed)

Flow — App Store listing title "Flow: Budget & Subscriptions" (bundle id
`com.davidpit.flow`). A personal finance tracker, iOS-native (wrapped with Capacitor).
Real, verified features from the source tree (`src/screens/`):
- Transactions, budgets, categories
- **Subscription tracking** (`Subscriptions.tsx`, `SubscriptionDetail.tsx`,
  `AddSubscriptionSheet.tsx`) — likely the sharpest hook: most people have no idea what
  they're actually paying across all their subscriptions
- Debts, goals, net worth tracking
- Insights + a "Year in Review" screen
- Universal (iPhone + iPad), adaptive layout, optional Face ID app lock

**The genuinely differentiating, checkable claim**: per the App Store submission doc's
own Privacy section, the app "makes zero network requests and has no backend" — all data
lives on-device (IndexedDB/local storage), no account, no login, nothing to disclose in
Apple's privacy questionnaire beyond "Data Not Collected." That's a real, verifiable
contrast against typical budgeting apps (Mint-style tools that require linking real bank
logins to a cloud service). This is the strongest angle: not "here's an app," but "here's
a budgeting app that never sees your data at all, and here's why that's rare."

## Angle / hook direction (per `channel/hooks-guide.md`'s type rotation)

Episode 35 was **Contrarian Open** — this one should NOT repeat it. This is naturally a
**Story/Anecdote Teaser / "Build It"** pattern (idea → build → real result), which the
guide lists as a good fit for a build reveal — different type, no rotation conflict.
Possible honest hook direction (not final, needs the actual dry-sentence-test pass once
this is unblocked): open on the specific, checkable claim — a budgeting app that has no
backend at all — not a vague "I built an app" statement, per the guide's "specific claim
in the first clause" rule.

## What's explicitly NOT done yet, and why this stays a draft

- **No demand check performed.** `channel/demand-report.md` is YouTube search-demand data
  for this channel's usual AI/automation/n8n content — it says nothing about "budget app"
  or "subscription tracker" search demand, and no research has been done here to fill that
  gap. Don't invent a demand number for this topic; if it matters before shipping, run the
  same kind of keyword research this channel already does for its other topics, honestly,
  first.
- **No script written.** Per this repo's standing rule, no line of narration gets written
  until the product is verified live and current — here specifically, until it's actually
  on the App Store (the rule that caught the "ChatGPT agent mode" rename before episode 18
  applies just as much to "is this app real and available" as to a third-party tool).
- **No setup-guide page possible yet.** Every episode since 21 ships with a real, followable
  setup path on `/e/N` — for this one that means a real App Store link a viewer can actually
  tap and install from. That doesn't exist until the app is live, so this episode structurally
  can't pass `check_setup_guide.py` yet, on top of not being written yet.

## Next step, once the App Store listing is live

Come back to this file, run the real hook-writing pass against `hooks-guide.md`'s
dry-sentence test, pick the real demand angle if one exists, write the setup-guide entry
in `studio/lib/articles.ts` pointing at the real App Store link, and only then start the
narration/build/render pipeline (`export/produce.sh`) like every other episode.
