# Episode 40 — script, ready to produce

## Topic
Most new cars sold today have embedded telematics that track speed, braking, and location
automatically. Automakers have sold that driving data to data brokers (LexisNexis Risk
Solutions, Verisk) who build consumer reports used to help set insurance rates — sometimes
through enrollment/disclosure processes regulators called unclear or misleading. Real,
current 2026 enforcement: California's Attorney General settled with GM for $12.75M in May
2026 over this exact practice. The real, working defenses: check your car's own connected-
services setting, and use your federal right (FCRA) to request your own consumer file from
LexisNexis for free, the same way you'd request a credit report.

## Why this topic, why now
- **Personal-stakes/plain-language, per the 16.9.2026 reach-first standing rule**
  (`hooks-guide.md`): no developer jargon, a device (a car) nearly every viewer already
  owns or rides in, distinct mechanism from episodes 36-39 (a household device/chat app
  reporting to its own maker, vs. a car's data being sold on to third-party brokers who
  affect a real, checkable dollar outcome — insurance rates).
- **A deliberate exception to demand-report-driven topic selection**, same as episodes
  36-39 — `demand-report.md` doesn't cover connected-car data brokering; chosen for
  reach/personal-stakes fit under David's explicit 16.9.2026 "maximum virality" decision
  (`channel/content-memory.md`).
- **Not yet covered from this angle** — checked against all existing episode scripts and
  `studio/lib/articles.ts`; no prior episode covers cars, telematics, or insurance data.
- **Verified live (17.9.2026)** against multiple independent 2026 sources (see Verification
  below), anchored to a real, dated enforcement action (California DOJ vs. GM, $12.75M,
  May 2026) rather than an outdated single-source claim.
- **Hook-type rotation** (per `hooks-guide.md`'s log): 37 Shock/Surprise, 38 Specific
  Number, 39 Contrarian Open. This one is **Direct Address/Question** (last used episode
  31, a long gap) — not a repeat of the last three types.

## Verification (live web search, 17.9.2026)
Checked against multiple independent 2026 sources (auto/insurance trade press,
cybersecurity/privacy coverage, cross-referenced): 91% of new US cars as of 2026 have
embedded telematics collecting detailed driving data; California's Attorney General
announced a $12.75M settlement with GM (May 2026, subject to court approval) over selling
driving/location data — collected as often as every 3 seconds for some drivers — to data
brokers LexisNexis Risk Solutions and Verisk, who then sold that to insurers; GM says the
OnStar Smart Driver program is opt-in and un-enrollable, but regulators in California,
Texas, and federally said the enrollment/disclosure process was unclear or misleading; as
of March 2026 OnStar customer data is no longer shared with LexisNexis or Verisk
specifically, but the broader industry practice (Ford, Toyota, Hyundai, Kia and others
sharing with brokers) continues — this script is framed around the ongoing, real, current
industry practice and the still-valid FCRA consumer-disclosure right, not the
already-resolved GM/OnStar-to-LexisNexis pipeline specifically. LexisNexis's real, current
consumer disclosure process (a free report request under federal law, by mail/online at
consumer.risk.lexisnexis.com or by phone) is verified directly against LexisNexis's own
site.

**Scope note, stated plainly:** Verisk's current involvement in driving-data collection is
ambiguous in available sources (one source suggests it exited this specific business) — the
setup guide below focuses on LexisNexis, whose current process is directly confirmed, and
names Verisk only as a secondary contact to try, not a guaranteed-active one.

## Hook rules check (against `channel/hooks-guide.md`)
- **Type rotation**: see above — Direct Address/Question, not used in the last three
  episodes.
- **Write for a person, not an AI-literate viewer**: no technical acronym in the hook
  itself ("telematics" never appears in the spoken lines; "data brokers" is explained by
  what they do, not left undefined).
- **Cold-read test**: a real and checkable claim (your car tracks and reports driving
  behavior), no vague referent, no hypothetical framing.
- **Specific claim in the first clause**: the surprising part (someone is already grading
  your driving) is in the same sentence as the question.
- **Personal-stakes/plain-language (16.9.2026 standing rule)**: the stake is a real dollar
  outcome (insurance rate), plain consumer language throughout.

## Narration (final, 7 lines)
1. "Do you know who's already grading how you drive, every time you get in the car?"
2. "It can track your speed, your braking, your location — without you doing anything."
3. "That data can get sold to companies that help set your insurance rate — sometimes without you knowing."
4. "One setting in your car's own app can switch that off."
5. "It won't undo what's already gone out. You can still see your own file — for free."
6. "The setup's in the link in bio."
7. "Follow for the setup that actually works."

## Density check
5 distinct ideas across the 7 lines (the two CTA lines don't count as content ideas): (1)
the car tracks driving behavior automatically, (2) the specific data points (speed, braking,
location), (3) that data is sold, tied to a real dollar outcome (insurance rate), (4) a real
setting turns off the sharing, (5) the setting's real scope (doesn't undo past sharing, but a
free consumer-file request exists). Within the standing "roughly 4-5 ideas" range
(`content-memory.md`, episode 36 finding).

## Simplicity/length check
Plain consumer language throughout, no unexplained acronym in the spoken lines. Length
target: 30-45s per `CLAUDE.md`'s standing floor; matches the 7-line shape that has landed
episodes 37-39 at 30.1-33.4s.

## Build notes
- Palette: fresh combo for episode 40, distinct from episode 39's blue/cyan ("tense") —
  amber/sky "drive" mood (a real, mapped `pick_real_track.py` mood, and a direct thematic
  match for a driving-data topic), checked against `channel/used-designs.json` for
  exact-hex reuse.
- Scoreboard scene: "Connected services on" / SHARING vs. "Turned off" / PRIVATE — same
  shape as episodes 37-39's binary-contrast scoreboard.
- Built from `video/reel-39.html` (already verified against `export/safe_check.js` and
  `check.sh`), keeping the working hook/quote/scoreboard motion wiring, content and
  palette changed.
