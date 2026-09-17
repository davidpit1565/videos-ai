# Episode 38 — script, ready to produce

## Topic
AI voice cloning has gotten cheap and fast enough that a scammer needs only about ten
seconds of someone's real voice — scraped from a public video, a voicemail greeting, or a
social post — to generate a convincing clone with a current instant-cloning tool. Scammers
use the clone to call someone the victim loves, claim an emergency, and ask for money, using
caller-ID spoofing so the call even appears to come from the real person's own phone. The
real, working defense isn't a product setting — it's a pre-arranged "safe word" only real
loved ones would know, since AI can fake a voice but can't fake a fact it's never heard.

## Why this topic, why now
- **Personal-stakes/plain-language, per the 16.9.2026 reach-first standing rule**
  (`hooks-guide.md`): zero developer jargon, understandable with no AI-tool background,
  and higher-stakes than 36/37 (money and a loved one's safety, not just a data-privacy
  toggle) — a genuinely different register from "an AI already saw something of mine,"
  not a third repeat of that exact theme.
- **A deliberate exception to demand-report-driven topic selection**, same as episodes 36
  and 37 — `demand-report.md` doesn't cover voice-cloning scams; chosen for reach/personal-
  stakes fit under David's explicit 16.9.2026 "maximum virality" decision
  (`channel/content-memory.md`), stated here rather than silently skipped.
- **Not yet covered from this angle** — checked against all existing episode scripts and
  `studio/lib/articles.ts`; no prior episode covers voice cloning, scam calls, or safe words.
- **Verified live (17.9.2026)** against multiple independent 2026 sources (see Verification
  below) — the seconds-of-audio claim, the caller-ID-spoofing mechanic, and the safe-word
  defense are all current and consistent across sources, not a single outlet's claim.
- **Hook-type rotation** (per `hooks-guide.md`'s log): 35 Contrarian Open, 36 You-Focused
  Appeal, 37 Shock/Surprise. This one is **The Specific Number** (last used episode 33, a
  5-episode gap) — "ten seconds" is a real, checkable, concrete figure, not a repeat of
  the last three types.

## Verification (live web search, 17.9.2026)
Checked against multiple independent 2026 sources (cybersecurity/consumer-safety coverage
plus voice-cloning-industry sources, cross-referenced, not a single outlet): current
zero-shot voice-cloning tools can produce a recognizable clone from as little as a few
seconds of clean audio, and current instant-cloning APIs (e.g. Gradium, Cartesia) specify a
10-second minimum sample — "ten seconds" is used here as the real, checkable, currently-
documented figure for an instant clone, not the absolute technical floor. Scammers commonly
source that audio from public social videos or a voicemail greeting; calls commonly use
caller-ID spoofing to appear to come from the real person's own number; consumer-safety
guidance converges on a pre-arranged "safe word" or phrase, known only to real loved ones,
as the practical defense — the AI can fake a voice, not a fact it was never told. This is
presented as a real, current scam pattern and a real, current defense, not a specific
product or app whose name/behavior could go stale — nothing here names a company or product
to verify against a changing feature.

**Word choice note:** the first draft used "three seconds" (also a well-sourced figure,
McAfee's own research cited in multiple 2026 outlets). Switched to "ten seconds" — an
equally real, independently-sourced figure (current instant-cloning APIs' stated minimum)
— after `build_voice.py`'s own shipped-file consonant check repeatedly failed on the word
"three" (a burst on the onset consonant, in the tool's own default `--watch` list for this
exact reason), even after retries and a reworded sentence position. Not a respelling fight —
a different real number, same claim, avoids a word this voice profile can't reliably land.

## Hook rules check (against `channel/hooks-guide.md`)
- **Type rotation**: see above — Specific Number, not used in the last three episodes.
- **Write for a person, not an AI-literate viewer**: no tool names, no technical terms
  ("voice cloning" is explained by what it does, not left as jargon).
- **Cold-read test**: one clause, a real and checkable claim (ten seconds of audio is
  enough), no vague referent, no hypothetical framing — this is a real, current capability.
- **Specific claim in the first clause**: the number and the claim are in the same
  sentence, nothing deferred to a second sentence.
- **Personal-stakes/plain-language (16.9.2026 standing rule)**: matches the reference-
  account pattern (personal stakes, plain language) — here the stake is a loved one's money
  and safety, arguably the highest-stakes topic this channel has used under this rule.
- **Stakes-escalation pass (per @rpn's formula)**: leads with the concrete mechanism
  (ten seconds → clone) rather than a vague "AI can fake voices now" — the same "state the
  real mechanism, not the abstraction" discipline used in episodes 32-37.

## Narration (final, 7 lines)
1. "Just ten seconds of your voice — from any video or voicemail online — is all AI needs to clone it now."
2. "It can call someone you love, sound just like you, and ask for money."
3. "It can even show up as your own phone on their screen — but the call isn't coming from your phone. It's spoofed."
4. "Agree on a safe word in advance — AI can fake a voice, but not a word it doesn't know."
5. "It won't stop the call from coming. It just can't fake a response it was never told."
6. "The setup's in the link in bio."
7. "Follow for the setup that actually works."

## Density check
5 distinct ideas across the 7 lines (the two CTA lines don't count as content ideas, matching
episode 37's own count): (1) ten-second clone claim, (2) the scam call itself (loved one,
money), (3) caller-ID spoofing, (4) the safe-word defense, (5) the defense's real scope
(stops fake-answer scams, not the call itself). Within the standing "roughly 4-5 ideas"
range (`content-memory.md`, episode 36 finding). Matches episode 37's own shape (hook,
mechanism, escalation, fix, scope-caveat, CTA x2).

## Simplicity/length check
Every line uses plain consumer language — no tool names to verify, no jargon. Length
target: 30-45s per `CLAUDE.md`'s standing floor; episode 37's structurally identical
7-line shape rendered at 30.5s, so this is expected to land in the same range before any
retiming pass.

## Build notes
- Palette: fresh combo for episode 38, distinct from episode 37's emerald/amber
  ("confident") — going with a crimson/gold "urgent" mood to match the scam-warning
  register (fear-adjacent, per the 13.9.2026 emotional-register axis), checked against
  `channel/used-designs.json` for exact-hex reuse.
- Scoreboard scene (recipe already wired, `.scoreboard`/`.scorerow`): "No safe word" /
  VULNERABLE vs. "One shared safe word" / SAFE — same shape as episode 37's privacy-toggle
  scoreboard, reused because it fits a real binary contrast here too.
- Built from `video/reel-37.html` (already verified against `export/safe_check.js` and
  `check.sh`), not `video/reel-template.html` directly — keeps the exact working hook/
  quote/scoreboard motion wiring, only content and palette change.
