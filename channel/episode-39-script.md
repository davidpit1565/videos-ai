# Episode 39 — script, ready to produce

## Topic
Most smart TVs (Samsung, LG, Vizio, and others) run Automatic Content Recognition (ACR) by
default: the TV periodically fingerprints what's on screen — a snapshot, not a recording —
and sends that fingerprint back to the manufacturer to build an ad/viewing profile. It picks
up content from any source connected to the TV (a game console, a cable box, a streaming
stick), not just the TV's own apps. A real setting per brand turns it off.

## Why this topic, why now
- **Personal-stakes/plain-language, per the 16.9.2026 reach-first standing rule**
  (`hooks-guide.md`): no developer jargon, a device almost every viewer already owns,
  distinct mechanism from episodes 36-38 (data collection via a household appliance, not a
  chat app, a photo library, or a phone call).
- **A deliberate exception to demand-report-driven topic selection**, same as episodes 36-38
  — `demand-report.md` doesn't cover smart TV tracking; chosen for reach/personal-stakes fit
  under David's explicit 16.9.2026 "maximum virality" decision (`channel/content-memory.md`).
- **Not yet covered from this angle** — checked against all existing episode scripts and
  `studio/lib/articles.ts`; no prior episode covers smart TVs or ACR.
- **Verified live (17.9.2026)** against multiple independent 2026 sources (see Verification
  below), including active 2026 legal action (a Texas settlement with Samsung, ongoing
  litigation against Sony/LG/Hisense/TCL, and Kentucky's new opt-in law) confirming this is
  current, not stale.
- **Hook-type rotation** (per `hooks-guide.md`'s log): 36 You-Focused Appeal, 37 Shock/
  Surprise, 38 Specific Number. This one is **Contrarian Open** (last used episode 35, a
  3-episode gap) — it contradicts the assumption that a TV is a passive screen, not
  something reporting back.

## Verification (live web search, 17.9.2026)
Checked against multiple independent 2026 sources (consumer-tech and cybersecurity
coverage, cross-referenced): ACR works by periodically fingerprinting on-screen frames
and/or audio and sending that fingerprint (not the video itself) back to the manufacturer
or a third party (e.g. Samsung's Samba TV integration); it captures content from any
connected source, not just built-in apps; frequency varies by brand — Samsung reported as
about once a minute, LG about every 15 seconds. Real, current 2026 legal action confirms
this is an active, not historical, issue: Texas's Attorney General sued Samsung, Sony, LG,
Hisense, and TCL over ACR data collection without informed consent (Samsung settled
February 2026; the rest still litigating), and Kentucky passed the first state law
requiring opt-in consent for ACR in March 2026. Real per-brand opt-out settings exist and
are named accurately in the setup guide below (Samsung: Usage & Diagnostics; LG: Live
Plus; Vizio: Viewing Data; Roku: Personalize ads) — checked against multiple independent
how-to sources, not a single outlet.

## Hook rules check (against `channel/hooks-guide.md`)
- **Type rotation**: see above — Contrarian Open, not used in the last three episodes.
- **Write for a person, not an AI-literate viewer**: no technical acronym in the hook line
  itself ("ACR" only appears once, defined, in the body/caption — never in the spoken hook).
- **Cold-read test**: one clause, a real and checkable claim (the TV reports back what's on
  screen), no vague referent, no hypothetical framing.
- **Specific claim in the first clause**: the surprising part (the TV watches back) is in
  the same sentence as the setup.
- **Personal-stakes/plain-language (16.9.2026 standing rule)**: a device nearly every viewer
  owns, plain consumer language throughout.

## Narration (final, 7 lines)
1. "Your smart TV isn't just playing what's on. It's watching what you watch — and sending that back."
2. "It can fingerprint what's on your screen, from any device plugged into it."
3. "Some TVs check in four times a minute, on anything you're watching — even from a game console or a set-top box."
4. "A real setting, right in the TV's own menu, turns that off."
5. "It won't stop the ads. It just stops them learning from your own screen."
6. "The setup's in the link in bio."
7. "Follow for the setup that actually works."

## Density check
5 distinct ideas across the 7 lines (the two CTA lines don't count as content ideas): (1) the
TV reports back what's on screen by default, (2) it covers any connected source, not just
built-in apps, (3) the real frequency (four times a minute), (4) a real setting
turns it off, (5) the setting's real scope (stops the learning, not the ads themselves).
Within the standing "roughly 4-5 ideas" range (`content-memory.md`, episode 36 finding).

## Simplicity/length check
Plain consumer language throughout, no unexplained acronym in the spoken lines. Length
target: 30-45s per `CLAUDE.md`'s standing floor; matches the 7-line shape that has landed
episodes 37-38 at 30.5-33.4s.

## Build notes
- Palette: fresh combo for episode 39, distinct from episode 38's crimson/gold ("urgent")
  — blue/cyan "tense" mood (music bed), fitting a "your device is watching you" register
  (`diagnostic` was the original plan but isn't one of `audio/pick_real_track.py`'s real
  mapped moods — `tense` is, and reads the same way), checked against
  `channel/used-designs.json` for exact-hex reuse (visual mood label stored as "tense").
- Scoreboard scene: "By default" / TRACKED vs. "One setting" / PRIVATE — same shape as
  episodes 37-38's binary-contrast scoreboard.
- Built from `video/reel-38.html` (already verified against `export/safe_check.js` and
  `check.sh`), keeping the working hook/quote/scoreboard motion wiring, content and
  palette changed.
