# Episode 43 — script, ready to produce

## Topic
Windows 11 has a real, current feature called Recall: an on-device AI model that takes a
snapshot of your screen every few seconds and builds a searchable, AI-readable timeline of
everything you've ever looked at on your PC — every app, every chat, every website. It's
opt-in and off by default on new Copilot+ PCs, encrypted locally, and gated behind Windows
Hello. A security researcher (Alexander Hagenah) published a tool in April 2026, TotalRecall
Reloaded, that walks past those protections and extracts every screenshot Recall has ever
taken on a machine.

## Why this topic, why now
- **Genuine AI at the literal center, per the 17.9.2026 standing rule** (`hooks-guide.md`):
  Recall's whole feature is an AI model indexing your screen history — not an adjacent
  privacy angle bolted onto a non-AI product.
- **Deliberate variety from episodes 41-42**: 41 was OpenAI/ChatGPT, 42 was Google/Android.
  This is Microsoft/Windows — a third distinct company and product, continuing David's
  direct note not to repeat the same company two episodes running.
- **Different mechanism from episodes 38/42**: 38 was an attacker using AI against the
  viewer, 42 was a company using AI to defend the viewer from someone else. This is a
  company's own AI creating a new personal risk (a searchable archive of your private
  screen activity) — a genuinely different angle from either.
- **Personal-stakes, plain-language** (16.9.2026 reach-first standing rule): "everything
  you've ever typed or looked at on your computer, saved and searchable" is a stake anyone
  understands instantly, no technical background required.
- **Not yet covered** — checked against every existing episode script and
  `studio/lib/articles.ts` (1-42).
- **Verified live (20.9.2026)** directly against Microsoft's own support/Learn documentation
  plus independent press — not assumed from memory or from what Recall looked like at its
  original 2024 announcement (it shipped opt-out at first, then was rebuilt opt-in after
  backlash — using the old, opt-out version would have been stale and wrong).
- **Hook-type rotation** (per `hooks-guide.md`'s log): 40 Direct Address/Question, 41
  Shock/Surprise, 42 You-Focused Appeal. This one is **Contrarian Open** (last used episode
  39, a 4-episode gap) — not a repeat of the last three types.

## Verification (live web search, 20.9.2026)
Checked directly against Microsoft's own Learn/Support documentation plus independent press
(Wikipedia's maintained Recall timeline, Computerworld, XDA Developers, nGuard), cross-
referenced:
- **What it does**: Recall saves a snapshot of your active screen roughly every few seconds
  and whenever the active window's content changes, then uses an on-device AI model to make
  that whole history searchable in plain language (e.g. "the recipe site I looked at last
  week").
- **Opt-in, not opt-out**: after the 2024 privacy backlash, Microsoft rebuilt Recall to be
  fully opt-in and off by default on Copilot+ PCs — a real, current, and directly confirmed
  correction to the original design, stated plainly here rather than treating the original
  controversy as the current state.
- **How to turn it on**: Windows 11 Settings → Privacy & security → Recall & snapshots →
  turn on snapshots. Requires Windows Hello enrollment; "proof of presence" (re-authenticating
  with Windows Hello) is required every time you open or search your Recall timeline.
- **Where the data lives**: stored and encrypted locally on the device — Microsoft states
  snapshots are not sent to Microsoft's servers.
- **Real, current limitation stated plainly (not smoothed over)**: on 9.4.2026, security
  researcher Alexander Hagenah published a tool (TotalRecall Reloaded) that bypasses Recall's
  protections and extracts every stored snapshot from a machine — a real, dated, named
  incident, not a hypothetical risk.
- **Hardware/software scope**: Recall requires a Copilot+ PC (specific NPU-equipped
  hardware) and a supported Windows 11 build — it is not available on every Windows PC.

## Hook rules check (against `channel/hooks-guide.md`)
- **Type rotation**: see above — Contrarian Open, last used episode 39, not a repeat of the
  last three episodes' types.
- **Specific, checkable claim in the FIRST clause**: the capability itself (a screenshot
  every few seconds, saved and searchable) is stated directly, with no hedge or hypothetical.
- **Personal-stakes/plain-language**: "everything on your screen, saved" needs no AI or
  Windows background to feel the stake.
- **Cold-read test**: checkable directly against Microsoft's own support page; no vague
  referent ("Windows," "Recall," and "screenshot" are all named plainly).
- **Not a repeat of episode 39's angle** (smart-TV ACR tracking, a company watching what you
  watch): this is a company's AI recording what you *do*, and — the twist — a real published
  tool that can steal that record, a materially different mechanism and stake.

## Narration (final, 7 lines)
1. "Windows can now take a screenshot of your entire screen every few seconds — and save it."
2. "It's a real feature called Recall — an AI that lets you search back through screenshots of everything it's ever seen on your PC."
3. "It's off by default, and Microsoft locks it with your face or fingerprint."
4. "But this April, someone published a tool that walks right past that lock and pulls every screenshot off the machine."
5. "One setting in Windows tells you if it's already turned on."
6. "The setup's in the link in bio."
7. "Follow for the setup that actually works."

(Reworded post-lint, 20.9.2026: "searchable" (-LE), "researcher" (unstressed -ER), and
"yours" (R+cluster) all flagged by `audio/script_lint.py` — none have a stock respelling
fix, so each line was rephrased to drop the risky word rather than fight the model with a
respelling, per the standing rule in `CLAUDE.md`.)

(Reworded again post-gate, 20.9.2026: "every" in line 2 and "behind" in line 3 kept landing
swallowed/clipped per `audio/voice_doctor.py --deep`'s per-word check, across three
different seeds each — not a one-off roll, a structural pacing problem with those two
words in that sentence position. Reworded to drop them ("every screenshot" →
"screenshots of everything"; "locks it behind" → "locks it with") rather than keep
re-rolling seeds against the same wall.)

## Density check
5 distinct ideas across the 7 lines (the two CTA lines don't count as content ideas): (1) the
core capability (a screenshot every few seconds, saved), (2) what it actually is and does
(Recall, an AI-searchable history), (3) it's opt-in/locked behind biometrics, (4) the real
published bypass tool and what it does, (5) how to check your own setting. Within the
standing "roughly 4-5 ideas" range (`content-memory.md`, episode 36 finding).

## Simplicity/length check
Plain consumer language throughout — no "NPU," "Copilot+ PC," or "on-device inference"
spoken on camera (only in the written setup guide, where precision matters more than brevity).
Length target: 30-45s per `CLAUDE.md`'s standing floor; matches the 7-line shape that landed
episodes 37-42 at 30.0-33.4s.

## Build notes
- Palette: fresh combo for episode 43, distinct from episode 42's blue/red — violet/cyan
  (`#7C3AED` / `#22D3EE`), mood **"tense"** (a real, mapped mood, thematic match for a
  surveillance/privacy-exposure topic), checked against `channel/used-designs.json` for
  exact-hex reuse — no prior episode used this exact pair.
- Scoreboard scene: "Screenshot every few seconds" / SAVED vs. "One setting" / CHECK IT —
  same binary-contrast shape as prior episodes, reframed around "it's already logging you,
  here's how to see it."
- Built from `video/reel-42.html` (already verified against `export/safe_check.js` and
  `check.sh`), keeping the working hook/quote/scoreboard motion wiring, content and palette
  changed.
