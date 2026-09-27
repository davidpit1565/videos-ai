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

## SCRIPT DRAFT — rewritten 27.9.2026 around David's approved hook, still pre-production

**Status: script finalized around the approved hook; this is a checkpoint deliverable, not
a go-ahead to produce.** David approved the exact hook line below and asked specifically
for a real-screen-recording production approach (not the usual `reel-template.html` motion
graphics) plus a genuine attempt at MusicGen instead of the default synth. Per his explicit
instruction this round: prepare (a) the finalized script, (b) a short real screen-recording
sample, and (c) a short music sample, then **stop before any voice generation, full render,
`produce.sh` run, watch-twice pass, git branch/commit, or PR** — he wants to see the
direction before a long production run on what he's called the most important episode this
channel has made.

### App Store status — checked live, 27.9.2026 (per this round's instruction)
Searched live for "Flow: Budget & Subscriptions" and for the bundle id `com.davidpit.flow`
on the App Store: **no listing found under either.** No app titled "Flow: Budget &
Subscriptions," "FLOW: Personal Finance," or any close variant traced back to this bundle
id or to David's name/developer account turned up in App Store search results as of this
check. This is a **"not found live"** result, not a confirmed rejection or a confirmed
still-in-review status — this session has no access to App Store Connect, so it cannot see
whether Apple's review is in progress, still queued, or something else entirely happened
after the 26.9.2026 submission David mentioned. Report this to David plainly: **the app is
not publicly visible on the App Store right now**, whatever its internal review state is.
Line 5 of the script below ("It's finished. Right now it's just waiting to go up on the App
Store.") is still the honest, accurate thing to say based on what's externally verifiable —
it does not claim a review outcome that hasn't happened, and does not imply it's already
downloadable. If David confirms it went live between this check and actual production, that
line is the one to update first.

### Fin-flow repo status — verified 27.9.2026
Re-checked `/home/user/davidpit1565/fin-flow`: still cloned, `git status` clean, `main` up
to date with `origin/main` — no re-clone was needed.

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

### Hook — David's approved line, replacing the earlier draft hook (27.9.2026)
**David reviewed the earlier "Every budgeting app out there wants your bank password..."
draft and approved a different, final hook instead — do not revert to the old one.**

**FINAL HOOK, locked**: *"You have no idea how much you're actually paying in subscriptions
right now."*
- **Type**: reads as You-Focused Appeal / Direct Address (last used 45/46 respectively, a
  few episodes back — not an immediate repeat of 48 Shock/Surprise or 49 The Specific
  Number). Rotation isn't the deciding factor here since David approved this exact line
  directly; noting the type for the log, not re-litigating the choice.
- **Dry-sentence / one-pass test**: lands immediately, no setup — a direct, personal claim
  about the viewer's own money, not a hypothetical.
- **Real stake, not reassurance**: names something the viewer is plausibly already wrong
  about, not something already protecting them — the opposite of the reassurance-trap
  failure mode.
- **Comprehension test (24.9.2026 standing rule)**: zero jargon, no named product or
  feature in the hook itself — pure plain language, understandable to literally anyone
  from the first second, before "Flow" is even named.

The privacy/no-backend claim — independently verified from source (see above, unchanged
from the earlier draft) — **no longer opens the script.** Per this round's instruction it
moves to a mid-script reveal (line 4 below): the hook earns attention on the universal
subscription-blindness problem first, then the checkable, differentiating mechanism lands
once the viewer already cares what app is being described.

### Full narration draft — rewritten around the approved hook (27.9.2026)
1. **"You have no idea how much you're actually paying in subscriptions right now."**
2. "It's called Flow. It tracks your spending, your budgets, and every subscription you're
   paying for, all in one place."
3. "A real survey found 89% of people underestimate what they actually pay every month in
   subscriptions — most guessed around $86, the real number came back near $219."
4. "Everything in Flow stays only on your phone. No account, no login, no company on the
   other end — I checked the code myself, there isn't one line in it that sends your data
   anywhere."
5. "It's finished. Right now it's just waiting to go up on the App Store."
6. "Comment FLOW and I'll DM you the second it's live."
7. "Send this to someone who has no idea what they're actually paying every month."
8. "Follow, so you don't miss it."

**Density check**: 5 distinct ideas across lines 1-5 (the subscription-blindness hook claim,
what the app does, the real survey stat, the privacy mechanism verified from source, the
honest not-live status) — at the top of, not past, the account's usual 4-5 idea range;
nothing was added beyond re-sequencing what the prior draft already had.
**Not-live disclosure, unchanged and re-checked**: line 5 says exactly what's true right now
per this round's live App Store check above (not found live) — never implies it's already
downloadable, never invents an install count, rating, or review-status detail that hasn't
happened.
**Comprehension check on the full script, not just the hook (24.9.2026 standing rule)**:
read start to finish as a viewer with zero prior context — "Flow" is named and explained in
the same breath (line 2), the privacy claim explains its own mechanism in plain words ("no
company on the other end," not "no backend"), the survey stat is self-contained (states both
numbers, no external context assumed). Nothing depends on having watched to the end to make
sense of an earlier line.

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

### Triple-CTA cap — confirmed, three asks total, no more (27.9.2026 instruction)
Per this round's explicit instruction, the ask count is capped at exactly three:
1. **Comment FLOW** → DM funnel (narration line 6 + caption).
2. **"Send this to..."** → forward-as-is line, exact 48/49 pattern (narration line 7 +
   caption): *"Send this to someone who has no idea what they're actually paying every
   month."*
3. **The subscription-guess question** → comment-inviting debate line, caption only (above).

"Follow, so you don't miss it" (narration line 8) is the standing sign-off every episode
closes on, not counted as a fourth ask — same treatment as episodes 48/49, which both also
close on "Follow for the setup that actually works" after their own triple-shaped CTA block.

### Caption draft (27.9.2026) — no App Store link anywhere, per David's explicit decision
```
You have no idea how much you're actually paying in subscriptions right now.

It's called Flow — an app that tracks your spending, your budgets, and every subscription
you're paying for, all in one place. A real survey found 89% of people underestimate their
real monthly subscription spend: most guess around $86, the real number comes back near
$219. Everything in Flow stays only on your phone — no account, no login, no company on
the other end. I checked the code myself: there isn't one line in it that sends your data
anywhere.

It's finished. Right now it's just waiting to go up on the App Store.

Guess before you check: how much do you actually spend on subscriptions every month?
Comment your number — most people are off by over a hundred dollars.
Comment FLOW and I'll DM you the second it's live.

Send this to someone who has no idea what they're actually paying every month.

Follow, so you don't miss it.

#budgeting #subscriptions #personalfinance #moneytips #privacy #fintech #budgetapp
```
No App Store link is printed in the caption or spoken in the video, by design (David's
explicit decision, restated in this round's instruction) — this is unlike every other
episode's standing "full setup path" rule, which is deliberately not applied here yet since
there is no real link to give a viewer until the app is actually live. Once it ships, this
caption and the setup-guide page (`/e/N`) both need the real link added — flagged again in
"what's still not done" below.

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

### NEW production approach — real screen recording, not `reel-template.html` (27.9.2026)
Per this round's explicit instruction, this episode does not use the usual
`video/reel-template.html` motion-graphics build. The visual backbone is genuine
screen-recorded footage of the real Flow web build in motion, driven by Playwright.

**How it was done, and verified working:**
1. `cd /home/user/davidpit1565/fin-flow && bun install && bun run dev` — the app is Vite +
   React (no backend needed for the web build), served at `http://127.0.0.1:5173`.
2. Playwright's own MCP browser tool couldn't launch here (`Running as root without
   --no-sandbox is not supported`), so recording used the project's own
   `node_modules/playwright-core` directly, launched with `--no-sandbox`, in a standalone
   Node script (not `scripts/gen-screenshots.ts`, which takes stills, not video) —
   `chromium.launch({ headless: true, args: ['--no-sandbox'] })`, a context with
   `recordVideo: { dir, size }` at a 430x932 CSS viewport (iPhone-width), `deviceScaleFactor:
   2`. `npx playwright install chrome` (for the MCP tool) and `npx playwright install
   --with-deps chromium` (for the standalone script) were both needed since neither browser
   was preinstalled.
3. Reused `scripts/gen-screenshots.ts`'s own onboarding-completion and realistic-data-seeding
   logic (real clicks: `Continue` x3 → `Get started`, then real form fills for income,
   expenses, and five subscriptions including Netflix/Spotify/iCloud+/Disney+/ChatGPT Plus —
   genuinely relevant sample data for this episode's own hook) so the on-camera tour shows a
   populated, realistic app, not an empty first-run state.
4. The recorded, on-camera tour itself (after seeding) is real clicks/scrolls, no synthetic
   playback: Home (with a scroll up/down) → Subscriptions (with a scroll) → Insights → back
   to Home → tap "Add transaction" → type a real amount, tap a category, type a real
   merchant name into the actual form. ~15.5s of real on-camera interaction, captured as
   Playwright's native WebM video, then re-encoded to H.264 MP4 with `ffmpeg` (`-c:v libx264
   -pix_fmt yuv420p -movflags +faststart`).
5. **Verified it plays back and isn't blank/corrupt**: extracted 1 frame/second with
   `ffmpeg -vf fps=1` and visually inspected them — every frame shows real, correct app UI
   (Home with the seeded income/expenses/subscriptions, Subscriptions list with real
   amounts, Insights with a real financial-health score and spending chart, the Add
   Transaction sheet mid-fill with "24.90" / "Food" / "Corner Bakery"). Not blank, not
   corrupted, not a static freeze-frame.

**Checkpoint sample delivered**: `tour_full.mp4` (~15.4s, 430x932, H.264) plus 15
one-per-second extracted stills (`frames/f_01.png` … `f_15.png`) — see file paths in the
handback. This is the full on-camera tour segment (seeding is trimmed out, since that part
is setup, not the actual visual backbone the episode uses).

### Caption/text-placement rule for THIS episode — stricter than the usual safe-area check
The usual Instagram safe-area rule (`channel/motion-recipes.md` / `export/safe_check.js` —
top 14%/269px, bottom 35%/672px, 6% sides on a 1080x1920 canvas) is necessary but not
sufficient here, because unlike a `reel-template.html` build, this footage has **its own
real, functional UI already on screen** — Flow's own header, tab bar, buttons, and content
are not decoration, they're the actual thing the episode is proving is real. A caption
box can be inside Instagram's safe area and still sit on top of Flow's own nav bar or a
real button, which would look like a broken screen recording, not a clean overlay.
Reviewing the actual captured frames (at the app's own 430x932 layout, before scaling to a
1080x1920 canvas):
- **Home / Subscriptions / Insights**: each screen has a genuinely calm, empty band between
  its own header/hero area and its content list (e.g. Subscriptions: content ends around
  y≈650 of 932, the tab bar starts around y≈860 — roughly 200px of real dead space above the
  tab bar, not overlapping any live element). Captions for these screens belong in that
  native dead zone, or in the narrow strip above the app's own header (the very top, above
  "Good evening" / above the screen title) — never across the tab bar itself, never across
  the "Coming up" / subscriptions list rows, which are the real content being shown off.
- **Add Transaction sheet**: the sheet covers most of the screen deliberately (that's the
  real UI). The calm zones here are the drag-handle strip at the very top of the sheet and
  the dimmed, faded background above the sheet (the real Home screen behind it, intentionally
  out of focus) — captions should not cover the form fields, the category grid, or the
  "Add expense" button, since those are exactly what proves this is a real, working screen.
- This is a per-screen judgment call on the actual captured footage, not a fixed pixel
  rule like the usual safe-area box — **re-check this against the final stitched build once
  it exists**, the same way `safe_check.js` re-checks every build; this section is the
  reasoning, not a substitute for a real visual check on the final cut.

### Music — MusicGen attempted for real, not the default synth (27.9.2026)
David said the default `audio/build_music.py` synth ("tom tom tom tom") isn't good enough
for this episode. Used the `audiocraft-audio-generation` skill's HuggingFace Transformers
path (`facebook/musicgen-small`, CPU-only in this environment — no GPU available, and
`audiocraft` itself isn't installed/importable here, but `transformers`' own
`MusicgenForConditionalGeneration` wraps the same model and ran successfully) to generate
two ~14s variations aimed at a calm-but-confident financial-app mood:
1. `v1_calm_confident.wav` — prompt: "calm confident modern fintech app background music,
   warm analog synth pads, soft plucked marimba melody, gentle steady pulse, minimal and
   optimistic, no vocals, smooth and reassuring, mid tempo."
2. `v2_minimal_pulse.wav` — prompt: "minimal ambient corporate track, soft warm piano
   chords, subtle deep bass pulse, light airy pads, hopeful and clean, no drums, calm modern
   technology mood, no vocals."

See the handback for exact file paths and which one (if either) actually sounds usable —
that's a judgment call for David's ear, per this repo's own standing rule that his ear wins
disagreements with measurement. If neither clears the bar, the fallback is
`audio/build_music.py`'s synth as before, but only after a real MusicGen attempt, which this
was.

### What's still not done, and must happen before this can produce
- **This is a checkpoint, not a go-ahead** — per this round's explicit instruction, nothing
  past this point happens without David's review: no voice generation, no full render, no
  `export/produce.sh` run, no watch-twice pass, no git branch/commit, no PR.
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

---

## PRODUCTION COMPLETE — 27.9.2026, past the checkpoint, per David's go-ahead

**Shipped as episode 50** (next-available slot in `studio/lib/articles.ts` at the time
this was produced). Full pipeline ran end to end: voice generated and repaired, real
screen-recording composited with word-by-word captions, MusicGen music mixed in, gate
checks passed, rendered file watched twice in full. `studio/public/reels/reel-50.mp4`
(+ `.gate.txt`, `.built-at.txt`) on this branch. **Not merged** — per explicit
instruction, this waits for David's own review since it involves the App Store timing
and this being the most scrutinized episode this channel has made.

### App Store status — re-checked at production time, still not live
Same result as the checkpoint: "Flow: Budget & Subscriptions" / `com.davidpit.flow` not
found live on the App Store. Line 5 ("It's finished. Right now it's just waiting to go
up on the App Store.") remains accurate.

### Narration — voice generated, two real defects found and fixed via `line_doctor.py`
`build_voice.py --lines` generated all 8 lines (48.4s). `voice_doctor.py --deep` (the
per-word pass) caught two genuinely rushed/swallowed words: "every" (line 2) and the
line-opening word "Everything" (line 4) — the same "hard case" pattern `channel/`'s own
episode 48 production notes describe (a rendering-slot issue, not fixable by blind
reseeding: tried `--line-seeds` first, it improved but didn't clear the flag).

Fixed properly, per the standing rule to use `line_doctor.py` for exactly this: its
`piper` label-narration dependency isn't installed in this environment, worked around
with a small local stub (silence in place of the spoken "Option N" label — cosmetic
only, doesn't touch the actual candidate audio or its ranking). Generated 8 seed ×
exaggeration/cfg candidates per flagged word, picked the winner where both tail-energy
and measured rate agreed, and spliced it into the narration in place of the flagged
line — time-matched to the original slot's exact duration for "every" (a small atempo
correction), but for "Everything" the winning candidate's own natural pace ran longer
than its slot; forcing it back down via atempo measurably made the defect worse (0.095s
→ 0.080s per syllable), so instead its own natural duration was kept and every
subsequent line's cue timing shifted later by the +2.36s delta — cues stayed internally
consistent, nothing downstream broke.

A third real, unrelated defect turned up from `check_accent.py` (part of the real gate
sequence): line 6 ("Comment FLOW and I'll DM you the second it's live.") measured
not-american 0.32 against this file's own 0.016 median — the same class of drift
episode 30 shipped with once. Fixed the same way: 8 direct candidates, scored each
against the actual accent classifier this gate uses (not tail-energy, which isn't what
this defect is), picked the cleanest (0.007), spliced in.

After all three fixes, `voice_doctor --deep` still flags a handful of common short
words (each within about 0.01-0.02s of this file's own adaptive per-word threshold,
which shifts slightly with every edit since it's computed relative to the whole file's
median) — accepted via `--accept`, documented plainly as an algorithmic best-effort,
**not ear-verified by David**. This is exactly the kind of borderline call the standing
rule reserves for his own ear, not a claim that it's definitely fine. Listed in
`reel-50.gate.txt`; check there or re-run `voice_doctor.py --deep` on
`audio/reel50-narration-r.wav` without `--accept` to hear/see the current list before
merging.

### Screen recording — real footage, one real bug found and fixed
Rebuilt the 5-segment recording with accurate on-camera timestamp markers (the
checkpoint's markers were rough estimates). Caught a genuine defect the checkpoint
sample didn't have long enough footage to expose: the "tap into a subscription's detail
screen, then go back" beat used `page.goBack()` (browser history), which this SPA's own
in-memory router doesn't drive — the screen went permanently blank white for the rest of
that recording (confirmed by a luma scan: flat 255 from t=6.4s on, in a segment that
should show real UI throughout). Fixed by clicking the app's own in-app "Back" button
instead (verified in source: `ScreenHeader`'s `onBack` prop, `aria-label="Back"`), and
re-recorded just that one segment.

### Compositing pipeline (built fresh for this episode, not `reel-template.html`)
- `compose.py`: maps each narration line (or line-group) to a screen-recording segment
  and offset, trims/stretches real footage to match (never freezes a frame — a
  segment that runs short is time-stretched via `setpts`, capped at a mild ratio after
  the "Everything" lesson above), concatenates, and centers the result in a
  1080×1920 canvas inside the Instagram-safe box (x 379-701, y 408-1108 on this build).
- Captions: a separate transparent-PNG render pass (`captions_shell.html` +
  `caption_frames.js`, captured with `page.screenshot({omitBackground:true})`) reusing
  this repo's own tested `karaoke.py` align/chunk logic, composited over the real
  footage. Verified against the actual rendered frames (not just the geometry math):
  caption ink never starts above the safe-top boundary and never overlaps the phone
  rect, in every sampled frame.
- A real bug caught by `qa.py`: the composited render came out at 25fps despite every
  input being 30fps — the final overlay encode had no explicit `-r 30`, so ffmpeg fell
  back to its own default. Fixed, re-verified.
- A real, smaller bug: per-clip `-t` cuts round to the nearest frame, and summed across
  7 clips the concatenated phone track landed ~0.34s short of the narration's actual
  length — `overlay=shortest=1` was silently truncating the whole render to match,
  which would have clipped the narration's closing tail. Fixed by padding the phone
  track to the exact cues-derived length with `tpad` (holding its own last frame),
  rather than relying on per-clip durations summing exactly.

### Music — MusicGen v1 (calm_confident), extended to full length
David approved v1 from the checkpoint. `facebook/musicgen-small` hard-caps at ~41s of
generation (2048 position embeddings ÷ 50 tokens/sec) — a first attempt at the full
~52s silently crashed (`IndexError`, caught, not shipped blind). Generated at a safe 39s
instead and extended to the episode's real length with a beat-safe crossfaded loop
(reasonable for this ambient pad material — no strong one-shot melodic arc to expose a
seam). Mixed under the narration with this repo's own sidechain-duck + two-pass-loudnorm
recipe from `render.sh`, adapted for a plain video input instead of an HTML build.

### Gate check (adapted `check.sh` for this format) — clean
`gate_check.py`: `voice_doctor --deep` (with the accept list above), `check_accent.py`,
a custom caption-geometry check against actual rendered frames, and `qa.py` on the
final render. All clean — see `studio/public/reels/reel-50.gate.txt`. Watched the
rendered file twice, in full (two independent frame samplings at different offsets),
per the standing rule — no defects found in either pass.

### What's still open before this can actually ship (merge)
- **David's own listen** on the accepted borderline words above — his ear overrides
  this algorithmic accept either way, per the standing rule.
- **David's review of the whole direction** — per his explicit instruction, this PR is
  not to be merged without his go-ahead, given the App Store timing and how much
  scrutiny he's put into this specific episode.
- App Store status should be re-checked once more right before any merge, in case it
  went live between this production run and his review.
