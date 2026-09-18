# Episode 42 — script, ready to produce

## Topic
Google's Phone app has a real, current feature called Scam Detection: an on-device AI model
(Gemini Nano) that listens to a live call in real time for conversation patterns common to
scams — urgency, requests for gift cards or passwords, someone claiming to be a bank or
government official — and alerts the user mid-call if it's suspicious. Fully on-device: no
audio or transcript is ever sent to Google's servers. It ships **off by default** and only
works on specific Pixel models.

## Why this topic, why now
- **Genuine AI at the literal center, per the 17.9.2026 standing rule** (`hooks-guide.md`):
  this is a named AI model (Gemini Nano) actually reasoning about a live conversation, not an
  adjacent tech/privacy angle.
- **Deliberate variety from episode 41**: David asked directly not to make every reach-first
  episode about ChatGPT specifically — same standing bar (real AI, personal stakes, plain
  language), different product and different company (Google/Android, not OpenAI).
- **Different mechanism from episode 38** (AI voice-cloning scams — the *attacker* uses AI):
  this episode is the *defensive* side — a real company using AI to protect the viewer, so it
  isn't a repeat angle on the same "AI scams" territory.
- **Personal-stakes, plain-language** (16.9.2026 reach-first standing rule): a real, current
  problem (FTC: $2.95B in reported impersonation-scam losses) that disproportionately hits
  older relatives — a "protect a loved one" stake, same register as episode 38's strongest
  material.
- **Not yet covered** — checked against all existing episode scripts and `studio/lib/articles.ts`.
- **Verified live (18.9.2026)** directly against Google's own support documentation
  (support.google.com/phoneapp) plus independent press — not assumed from memory.
- **Hook-type rotation** (per `hooks-guide.md`'s log): 39 Contrarian Open, 40 Direct
  Address/Question, 41 Shock/Surprise. This one is **You-Focused Appeal** (last used episode
  36) — not a repeat of the last three types.

## Verification (live web search, 18.9.2026)
Checked directly against Google's own support page
(support.google.com/phoneapp/answer/15654065) plus independent press (Android Police,
Tom's Guide, Bleeping Computer, Help Net Security), cross-referenced:
- **What it does**: Scam Detection runs in the background of a live call, using the
  on-device Gemini Nano model to listen for conversation patterns commonly associated with
  scams (urgency, requests for gift cards/passwords/financial info, someone impersonating a
  bank or authority figure). If risk is high, it alerts with a notification, sound, and
  vibration, and gives an audible beep at call start and periodically through the call.
- **Privacy, stated directly by Google**: fully on-device — "No conversation audio or
  transcription is stored on the device, sent to Google servers or anywhere else."
- **Off by default** — a real, current, and directly confirmed fact, not an assumption.
- **How to turn it on**: Phone app → More → Settings → Scam Detection → toggle on.
- **How to turn it off**: for one call, More → Scam Detection during the call; for all
  calls, the same Settings toggle, off.
- **Real, current scope limit, stated plainly (not smoothed over)**: Pixel-only. US: Pixel 6
  and later, plus Pixel 9a/10a. International (Australia, Canada, France, Germany, India,
  Ireland, Italy, Japan, Mexico, Singapore, Spain, UK): Pixel 9 and later. Requires a SIM
  and device location in one of those countries.
- **Real, dated backing for the stakes**: FTC reported $2.95 billion in impersonation-scam
  losses in 2024.

**Scope note, stated plainly:** this is a different, Pixel-only, conversation-listening
feature from Google's separate "fake caller-ID" spoofed-number detection (which works
cross-brand with Samsung/OnePlus but only flags spoofed numbers, not conversation content).
This script covers Scam Detection specifically and states the Pixel-only limit on camera.

## Hook rules check (against `channel/hooks-guide.md`)
- **Type rotation**: see above — You-Focused Appeal, not used in the last three episodes.
- **Specific, checkable claim in the FIRST clause**: the surprising capability + its twist
  (a real AI that catches scammers, but it's off) is the entire first sentence.
- **Personal-stakes/plain-language**: protecting a loved one from a real, dated $2.95B/year
  problem — no developer jargon, no acronym ("Gemini Nano" never spoken on camera).
- **Cold-read test**: real, checkable, no vague referent.
- **Not a repeat of episode 38's angle**: 38 was about scammers using AI against you; this
  is about a real company already using AI to defend you — opposite framing, same broad
  territory but a genuinely different mechanism and claim.

## Narration (final, 7 lines)
1. "Your phone might already have an AI that can catch a scammer mid-call — it's just turned off."
2. "It listens for the exact patterns scammers use: urgency, gift cards, someone claiming to be your bank."
3. "It runs right on your phone. Nothing about the call is ever sent anywhere."
4. "One setting in your phone app turns it on."
5. "It only works on certain Pixel phones right now — check your settings to see if you have it."
6. "The setup's in the link in bio."
7. "Follow for the setup that actually works."

## Density check
5 distinct ideas across the 7 lines (the two CTA lines don't count as content ideas): (1) a
real AI already exists that can catch a scam call live, but ships off, (2) what it actually
listens for, (3) it's fully on-device/private, (4) exactly how to turn it on, (5) its real
scope limit (Pixel only, check your own settings). Within the standing "roughly 4-5 ideas"
range (`content-memory.md`, episode 36 finding).

## Simplicity/length check
Plain consumer language throughout — "Gemini Nano," "on-device," and "conversation
patterns" never spoken on camera (only in the written setup guide). Length target: 30-45s
per `CLAUDE.md`'s standing floor; matches the 7-line shape that landed episodes 37-41 at
30.0-33.4s.

## Build notes
- Palette: fresh combo for episode 42, distinct from episode 41's green/violet — blue/red,
  mood **"urgent"** (a real, mapped `pick_real_track.py` mood, and a direct thematic match
  for a scam-alert topic), checked against `channel/used-designs.json` for exact-hex reuse.
- Scoreboard scene: "Feature exists" / OFF vs. "One toggle" / ON — same shape as prior
  episodes' binary-contrast scoreboard, reframed around the "it's already there, just off"
  twist.
- Built from `video/reel-41.html` (already verified against `export/safe_check.js` and
  `check.sh`), keeping the working hook/quote/scoreboard motion wiring, content and palette
  changed.
