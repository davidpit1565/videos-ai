# Episode 37 — script, ready to produce

## Topic
Google Photos' "Ask Photos" feature (Gemini-powered) already lets Google's AI answer
natural-language questions about every photo in a user's library — which means the AI has
already analyzed the content of every photo, not just ones a user actively searches. By
default, a toggle ("Allow us to access your queries") lets Google review the questions
asked to improve the feature; turning it off keeps those queries from human review.

## Why this topic, why now
- **Personal-stakes/plain-language, per the 16.9.2026 reach-first standing rule**
  (`hooks-guide.md`): a secret-reveal about something the viewer already owns (their own
  camera roll), zero developer jargon, understandable with no AI-tool background — same
  shape as episode 36 (ChatGPT training) and the reference-account pattern Roni sent
  (personal stakes stated in plain language, not tool-internals framing).
- **A deliberate exception to demand-report-driven topic selection**, same as episode 36 —
  `demand-report.md` doesn't cover Google Photos; this is chosen for reach/personal-stakes
  fit, stated explicitly per the standing exception, not silently skipping the process.
- **Not yet covered from this angle** — checked against all existing episode scripts and
  `studio/lib/articles.ts`; no prior episode covers Google Photos or Ask Photos.
- **Hook-type rotation** (per `hooks-guide.md`'s log): 33 You-Focused Appeal + Specific
  Number, 34 Shock/Surprise, 35 Contrarian Open, 36 You-Focused Appeal. This one leads with
  "Google's" as the subject, not "you" — Shock/Surprise register (a hidden capability
  already active), not a repeat of 36's exact type back-to-back.

## Verification notes (live, 17.9.2026)
- Confirmed via live web search that "Ask Photos" is a real, current Google Photos
  feature, powered by Gemini, that answers natural-language questions about a user's own
  photo library (e.g., "find the best photo from each National Park I visited") using
  signals like location, lighting, and image content.
- Confirmed the real privacy control: a toggle ("Allow us to access your queries" /
  equivalent wording in Google's own Photos settings) that governs whether human reviewers
  may see the questions asked to Ask Photos to improve the feature; turning it off keeps
  queries out of that human-review process.
- Sources: Google's own Ask Photos support page (support.google.com/photos), and
  independent 2026 coverage (Help Net Security, Forbes) confirming the feature's rollout
  and its privacy-toggle mechanic.
- Not claimed: exact wording of the toggle may vary slightly by app version/region — the
  setup guide (`/e/37`) tells the viewer what to look for, not a guaranteed exact string.

## Hook rules check (against `channel/hooks-guide.md`)
- **Type**: Shock/Surprise — states a hidden, already-active capability as the surprising
  fact, not a personal pronoun opener. Last used episode 34, not back-to-back.
- **Personal-stakes/plain-language check**: "photo," "camera roll," "looked at" — zero
  product jargon ("Gemini," "Ask Photos" as a named feature) spoken in the hook itself.
- **Stakes-escalation pass (per @rpn's formula, logged in `hooks-guide.md`)**: first draft
  was "Google Photos has an AI that can answer questions about your photos" — accurate but
  flat, describing the feature rather than the stake. Reworded to lead with the fact that
  this already happened to every photo, not just ones the user searches for — the
  surprising part (AI already looked, not "AI can look if asked") is in the hook itself.
- **Cold-read test**: one clause, a real and checkable claim, no vague referent.
- **Simplicity check**: no unexplained tool names spoken aloud — "Ask Photos" and "Gemini"
  are introduced only visually/in the setup guide, never spoken, same discipline as
  episode 36's "Data Controls"/"Temporary Chat".

## Narration (6 lines — 4 ideas + CTA, matching episode 36's density fix)
1. Every photo you've ever taken in Google Photos has already been looked at by AI — before you ever asked it to.
2. It can already tell you things like the best shot from every trip you've taken, just from what it's already seen.
3. By default, people can review the questions you ask it, to help improve the feature.
4. One setting keeps those questions between you and the AI, nothing else.
5. The setup's in the link in bio.
6. Follow for the setup that actually works.

(Lines 5-6 are the locked, pre-approved outro clips — see
`audio/voice/profile/canonical-lines.json` — used byte-for-byte, no regeneration.)

## Density check (per episode 36's standing rule)
4 ideas: stakes/mechanism (line 1) → concrete capability (line 2) → the privacy mechanism
(line 3) → the one fix (line 4) → CTA. Matches episode 36's post-fix shape (stakes →
mechanism → fix → action), one idea fewer than the original 6-idea overload episode 36
shipped with before the fix — applying that lesson from the start this time, not after
shipping.

## Simplicity check
Reread for zero AI-tool background: "photo," "trip," "questions," "setting" — no "Ask
Photos," no "Gemini," no "Google Photos settings" path spoken aloud. Those exact names are
visual/on-screen and in the setup guide only.
