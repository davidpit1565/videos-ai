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

---

## SCRIPT DRAFT — prepared 25.9.2026, per David's direct instruction

**Status: script only, still on hold.** Per David's message today and this file's own
standing instruction above: the App Store listing is confirmed still not live (verified
just now — `APP_STORE_SUBMISSION.md` sections 6-7 are still open: no Apple Developer
account enrolled yet, no Mac/Xcode build, so no submission has happened; the earlier
"submitted, awaiting review" framing was corrected — it's actually not submitted yet).
No render, voice generation, build, or publish happens until it's actually live and there's
a real link for the setup guide. This section only prepares the script and the research
that feeds it, so production can start the moment it's unblocked.

### Real screenshots confirmed usable — no Playwright needed
`ios/fastlane/screenshots/en-US/iphone_6.9/` (in `davidpit1565/fin-flow`, cloned read-only
to verify) has four real 1290×2796 captures, rendered from the actual running app with
realistic sample data, not mockups: `01_home.png`, `02_subscriptions.png`, `03_insights.png`,
`04_add_transaction.png`. These are the genuine on-screen footage this episode needs — use
them directly for the screen-capture beats when the build stage starts. (A fifth beat,
"add subscription," would need a real capture of `AddSubscriptionSheet.tsx` — not present in
the four already generated; either accept the four that exist or ask for one more before
building, don't fabricate a fifth.)

### Privacy/no-backend claim — verified directly from source, not from the doc alone
Checked myself, independently of `APP_STORE_SUBMISSION.md`'s own claim:
- `package.json` dependencies: no `axios`, no `fetch` wrapper, no Supabase/Firebase SDK, no
  analytics/crash-reporting SDK (Sentry, PostHog, Mixpanel, Amplitude) — only Capacitor
  native-bridge packages, React, `recharts`, and `lucide-react`.
- `grep` across `src/` for `fetch(`, `axios`, `XMLHttpRequest`, `supabase`, `firebase`,
  `websocket`, any hardcoded `http://`/`https://` call: zero real network calls found (the
  only `.get(`/`.set(` hits are `Map`/`IndexedDB` calls in `src/lib/storage.ts`, `calc.ts`,
  `debt.ts` — unrelated to networking).
- Storage is `IndexedDB` only (`src/lib/storage.ts`).
- `index.html` loads nothing but the app's own local bundle — no external `<script src>`.
- The app's own in-app Legal screen states this directly to the end user
  (`src/lib/i18n/en/legal.ts`): *"Flow does not use analytics, crash reporting,
  advertising, or any third-party services. There is nothing to disable because there is
  nothing collecting data."*
**Conclusion: the zero-backend, on-device-only claim holds up in the current source code
as of today (25.9.2026)** — not just asserted in the submission doc. Safe to use as the
hook's core checkable claim.

### Hook type — chosen against the real rotation log in `channel/hooks-guide.md`
Last six episodes' types, in order: 44 Shock/Surprise, 45 You-Focused Appeal,
46 Direct Address, 47 Contrarian Open, 48 Shock/Surprise, 49 The Specific Number.
**Chosen type: Problem/Solution Setup** ("Struggling with X? Try this instead" —
`hooks-guide.md`'s table) — not used anywhere in the last six episodes, so this both
rotates cleanly off 49 and doesn't repeat any recent type. Genuinely earned by the content:
the real problem (every mainstream budgeting app wants a bank login) and the real,
checkable solution (this one structurally cannot ask) is exactly what this type is for,
not a forced fit.

**Hook line**: *"Every budgeting app out there wants your bank password. This one can't
even ask — there's nowhere for it to send it."*
- **Dry-sentence test**: real pull, not just informative — it names a genuine, familiar
  risk (handing a bank password to an app) before revealing the twist in the same
  sentence, per the 10.9.2026 first-clause rule.
- **One-pass/cold-read test**: read once, lands immediately — no setup, no hypothetical,
  no second sentence needed to understand the claim.
- **Real stake, not reassurance-trap**: the stake (your bank password going somewhere) is
  named plainly before the relief comes in the second clause — checked directly against
  the failure mode episode 45's first draft fell into.
- **Comprehension test (24.9.2026 standing rule)**: no jargon — "bank password," "send it,"
  nothing assumes prior AI/tech literacy. Deliberately avoids the word "server," even
  though that's the technically precise term, in favor of "nowhere to send it," so the
  claim lands for a viewer who has never heard the word "backend" or "server" used this way.

### Full narration draft
1. "Every budgeting app out there wants your bank password. This one can't even ask —
   there's nowhere for it to send it."
2. "It's called Flow. It tracks your spending, your budgets, and every subscription you're
   paying for, all in one place."
3. "Everything stays only on your phone. No account, no login, no company on the other
   end — I checked the code myself, there isn't one line in it that sends your data
   anywhere."
4. "A real survey found 89% of people underestimate what they actually pay every month in
   subscriptions — most guessed around $86, the real number came back near $219."
5. "It's finished. Right now it's just waiting to go up on the App Store."
6. "Comment FLOW and I'll DM you the second it's live."
7. "Follow, so you don't miss it."

**Density check**: 4 distinct ideas across the 5 non-CTA lines (the risk/solution claim,
what the app does, the privacy mechanism verified from source, the real subscription-spend
stat), within the account's usual 4-5 idea range.
**Not-live disclosure, stated plainly, per the never-fabricate rule**: line 5 says exactly
what's true right now (finished, not yet listed) — never implies it's already downloadable,
never invents an install count, rating, or review-status detail that hasn't happened.

### Sourced research used in the script (not invented)
- **West Monroe subscription-spend survey** (cited across multiple 2026 outlets,
  including gcn.com): people estimate ~$86/month in subscriptions on average; an itemized
  tally comes back around $219/month; 89% of consumers underestimate their real total,
  66% by more than $200. Used directly in narration line 4, numbers as reported, not
  rounded up for effect.

### Comment-to-DM funnel — why this is the right CTA shape for THIS episode specifically
No public link exists yet (app isn't listed), so the usual "setup's in the link in bio"
closing line does not apply — a different closer is needed until there's a real link.
Researched live (25.9.2026), general comment-to-DM mechanics, cited for the reasoning
behind picking this CTA shape (not claimed as this channel's own measured result — this
account's own numbers on this mechanic don't exist yet):
- Comment-to-DM automation (a keyword comment auto-triggering a DM) is reported to convert
  roughly 12-18% of commenters in industry write-ups on the mechanic, and keyword-CTA
  comments are reported to outperform a plain link-in-bio call by several times, because
  the action (typing one word) has no extra clicks or context-switch compared with tapping
  out to a browser.
- This matches this channel's own already-adopted 23.9.2026 sendability/comment-inviting
  standing rule in `hooks-guide.md` — every caption needs both a forward-as-is artifact and
  a real comment-inviting element, not just "follow for more."
- **Applied here**: "Comment FLOW and I'll DM you the second it's live" (line 6) uses the
  literal app name, not a generic word, so a commenter is unambiguous about what they're
  asking for and ManyChat's keyword trigger (already used elsewhere in this repo's
  automation, per `channel/instagram-automation.md`) can match on it directly.

### Comment-inviting element for the caption (separate from the DM-funnel line)
A genuinely debatable, personal question, distinct from the DM-funnel CTA itself, per the
23.9.2026 dual-path structure already used on episodes 48-49: *"Guess before you check:
how much do you actually spend on subscriptions every month? Comment your number — most
people are off by over a hundred dollars."* This is answerable from real personal
experience (not hypothetical), and creates a natural second reason to comment beyond the
FLOW keyword itself.

### Organic app marketing research — real case studies, not guesses (live search, 25.9.2026)
- **TikTok's own stated mechanism**: a video is tested in a small interest pool regardless
  of follower count or account age — a brand-new account can reach non-followers on day
  one on the strength of the video alone, not accumulated audience size. Directly relevant
  here: this account (86 followers per `plan/business-model.html`) is not structurally
  blocked from reach on this specific video.
- **Dyme (budgeting app, TikTok)**: grew via short, relatable "everyday money struggle"
  videos, not produced/glossy demos — the tone that performs in this exact genre is closer
  to a real, plain claim than a polished feature tour, consistent with this channel's own
  existing hook rules.
- **KOHO Financial (fintech, TikTok)**: real-user-demonstrated videos (creators showing
  their own actual use of the product) drove a reported 33% increase in new account
  registrations and 26% increase in app installs over a campaign — the common thread with
  Dyme is authenticity/real demonstration over polish, which is exactly what the four real
  app screenshots (not mockups) already support for this episode.
- **A Series B personal-finance app** (reported case study, name not independently
  re-verified beyond the aggregator source, so not stated as fact in the script itself):
  20 purely organic videos (before any paid boost) produced meaningful account growth and
  installs on their own — organic-first, paid-second is the reported winning sequence
  generally, and this episode is organic-only per David's no-paid-promotion-until-validated
  standing rule already in `hooks-guide.md`.
- **Caveat, stated honestly**: none of these case studies are this channel's own measured
  data — they inform *why* the comment-to-DM/authentic-screenshot approach is a reasonable
  bet, not a promise of a specific outcome. Per the "measure, don't guess" rule, this
  episode's actual performance goes into `content-memory.md` after it ships, same as every
  other episode, not assumed in advance from someone else's numbers.

### What's still not done, and must happen before this can produce
- App Store listing is still not live — Apple Developer enrollment and the Xcode build
  (`APP_STORE_SUBMISSION.md` sections 6-7) are still open. No render/voice/build/publish
  starts until that's done and there's a real install link.
- No setup-guide entry can be written in `studio/lib/articles.ts` yet (needs the real link)
  — `export/check_setup_guide.py` will correctly refuse this episode until then.
- The demand-check gap flagged above (no YouTube/search-demand research exists for
  "budget app"/"subscription tracker" as a topic) is still open — worth doing before
  shipping if there's time, though this episode's case for existing doesn't depend on
  search demand the way the channel's usual topics do (it's a first-party product launch,
  not a demand-sourced tutorial topic).
- Episode number stays TBD — whatever is next-available in `studio/lib/articles.ts` and
  `channel/episode-*-script.md` when this actually ships is its real number.
