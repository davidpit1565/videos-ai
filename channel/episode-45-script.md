# Episode 45 — script, ready to produce

## Topic
US phone carriers including Verizon, AT&T, and T-Mobile use network-level systems to
identify or block suspected spam and scam calls. Verizon Call Filter uses evolving
analytics and databases to detect spam calls and can automatically send high-risk spam to
voicemail. AT&T ActiveArmor automatically blocks fraud calls and can label or route spam
calls. T-Mobile says its network-level Scam ID automatically labels suspected scam calls
"Scam Likely," while Scam Block can block those calls before they reach the phone.

Customers can view or manage these protections through the carriers' apps or account
tools, although the network-level protection itself does not necessarily depend on the
app. Important limitation: these systems do not catch every unwanted or fraudulent call.

STIR/SHAKEN is a separate system. It helps authenticate caller ID information; it does not
determine whether the caller's intent is legitimate. Caller-ID authentication is not
presented as proof that a call is safe.

**Revised 22.9.2026, twice, after two source-by-source red-teams.** Round 1 removed "AI
scoring on every incoming call, before it rings" (three bundled claims stronger than any
source states). Round 2 tightened further: "before the user answers" implied a single
timing for all three carriers, when only T-Mobile's Scam Block is sourced as stopping calls
before they reach the phone; "Each carrier has a free app" was corrected since network-level
protection doesn't require the app; the STIR/SHAKEN limitation no longer includes an invented
scenario ("a scammer calling from a legitimately-registered, signed number") beyond what the
FCC's own description supports.

## Why this topic, why now
- This is the first reach-first-era episode built from a **Phase 1/Phase 2 forensic
  investigation done in this session**: 43 episodes showed almost zero shares (1 total),
  and Instagram's own stated ranking factors name sends-per-reach as a top signal. The
  experiment this episode belongs to tests whether content built around a **natural
  recipient** — a specific person the viewer already has in mind — produces more sends
  than the account's default reveal-only format.
- **Red-teamed before writing**, per the second-opinion review of the original 4-concept
  list: the original phrasing ("phone company scam detection") was flagged as too broad
  — it implies universal, cross-carrier, cross-country coverage that isn't true. Narrowed
  here to what's actually verified: **three named US carriers**, not "your phone company"
  in general.
- **Verified live (22.9.2026)**, not assumed: AT&T Call Protect/ActiveArmor, Verizon Call
  Filter, and T-Mobile Scam Shield are all real, current, named products with free tiers,
  each confirmed via the carrier's own support pages.
- **Different company/mechanism from every episode so far** — no prior episode has covered
  carrier-level call scoring (41 was ChatGPT/finance, 42 was Android/live-call audio, 43 was
  Windows/screenshots, 44 was WhatsApp/message summaries).
- **Not yet covered** — checked against every existing episode script and caption (1-44).

### Scope (hard limits for this script — do not widen)
- US carriers only.
- Verizon, AT&T, and T-Mobile only.
- Do not claim that every carrier uses AI.
- Do not claim that every incoming call is scored.
- Do not claim that every call is screened before ringing.
- Do not imply that STIR/SHAKEN is the scam-detection system.
- Do not imply that caller-ID authentication proves a caller is legitimate.
- Do not imply that the carrier systems catch every scam call.
- If showing a carrier app on screen, make clear the network-level protection can operate
  independently of the app, where the carrier states this.

## Verification (live web search, 22.9.2026 — three passes, same day)
- **Verizon Call Filter**: uses "analytics and databases that are constantly evolving" to
  detect spam; can automatically route high-risk spam to voicemail. Free tier on
  standard/prepaid plans with a compatible device; managed via the Call Filter app or My
  Verizon — but the network-level detection itself is not stated as requiring the app.
- **AT&T ActiveArmor / Call Protect**: automatically blocks fraud calls; can label or route
  spam calls; AT&T states real-time protection. Managed via myAT&T/ActiveArmor.
- **T-Mobile Scam ID / Scam Block**: Scam ID is explicitly network-level and automatically
  labels suspected scam calls "Scam Likely" (T-Mobile's own wording, not paraphrased into
  "AI output"). Scam Block can block those calls before they reach the phone — this
  before-the-phone timing is sourced specifically to T-Mobile, not asserted for all three
  carriers. Managed via T-Life, but the network-level protection does not require the app.
- **STIR/SHAKEN**: the FCC describes it as a caller-ID authentication framework, one part of
  the broader anti-robocall effort — a **separate system** from the scam-detection above,
  not a component of it. It authenticates that caller ID information hasn't been spoofed; it
  does not determine whether the caller's intent is legitimate. The script does not go
  further than this (no invented "signed number gets through clean" scenario).
- **Scope, stated plainly**: US carriers only — specifically Verizon, AT&T, and T-Mobile, not
  every carrier or every country. Not a claim that every scam/unwanted call is caught.

## Hook rules check (against `channel/hooks-guide.md`)
- **Type**: Contrarian Open. **Checked against the file's actual rule (not a guess):**
  `hooks-guide.md`'s own stated rule is "never repeat the same hook type two episodes in a
  row" — a literal back-to-back check, not a 2-3 episode window. Episode 43 was also
  Contrarian Open, but episode 44 (Shock/Surprise) sits directly between 43 and this one,
  so 45 does not break the rule as written. Flagging this explicitly since it was raised as
  a question, rather than silently assuming it's fine.
- **Specific, checkable claim in the first clause**: names the real, current mechanism
  (network-level scam/spam detection) and, within the first line, the three real named
  carriers — no vague "your phone company," and no unsourced "AI" claim.
- **Personal-stakes, plain language**: scam calls are a near-universal fear; zero jargon
  needed to feel the stake.
- **Cold-read test**: checkable directly by opening the relevant carrier app.

## Narration (draft — subject to the usual voice/accent/pacing revision rounds before shipping)

**Line 1 rewritten 22.9.2026, after David watched the shipped cut and flagged the hook
directly: the first two seconds didn't make him want to keep watching or follow the
account.** The original line ("Verizon, AT&T, and T-Mobile all run network-level systems to
catch spam and scam calls.") is exactly the flat, informational shape `hooks-guide.md`'s
dry-sentence test warns against — a true, on-topic sentence with no pull (no stakes,
identity, or curiosity). Rewritten as a You-Focused Appeal (rotated off episode 44's
Shock/Surprise, last used episode 42): the specific, checkable claim ("your carrier has
been screening your calls for scams") lands in the first clause, personal register ("your,"
"you"), and the twist ("you just never noticed") is the same secret-reveal shape as the
Roni reference grid, without inventing anything the fact-checked script doesn't already
support (the "always on, no user action needed" claim is the scoreboard scene's own verified
point).
1. "Your carrier's already been screening your calls for scams — you just never noticed it running."
2. "That 'Scam Likely' label? T-Mobile says its own network labels it automatically — before you even see the call."
3. "T-Mobile can even block it before it reaches your phone."
4. "It's not perfect — none of these systems catch every unwanted call."
5. "You can see it working in each carrier's app — but the protection itself runs on the network, not the app."
6. "Send this to whoever's going to answer the next call they don't recognize."
7. "The setup's in the link in bio."
8. "Follow for the setup that actually works."

(Line 6 is the experiment's actual variable — a natural-recipient line embedded as content,
not an imperative "share this" instruction. Per the second-opinion review: people don't
share because they were told to, they share because mid-video they already thought of
someone. This replaces the earlier, rejected "who would you send this to" framing.)

## Density check
5 distinct ideas across 8 lines (2 locked CTA lines excluded): (1) which three carriers run
network-level detection, (2) the "Scam Likely" label's real, named source (T-Mobile's Scam
ID) and its timing, (3) T-Mobile's before-the-phone blocking (sourced only to T-Mobile, not
generalized), (4) the real limitation (not every call is caught), (5) how to see it in each
carrier's app while noting the protection itself isn't app-dependent. Within the ~4-5 idea
range this account's own data associates with better save/engagement performance.

## Simplicity/length check
No jargon beyond the carrier product names themselves (Call Filter, ActiveArmor, Scam
Shield), each named once. Neither "AI" nor "STIR/SHAKEN" is named on camera — the word "AI"
because no source supports it as the mechanism's name, and STIR/SHAKEN because its
limitation is stated in plain consequence language ("none of these systems catch every
unwanted call") rather than the technical standard's name, keeping both inside the
channel's plain-language rule and the scope list above. Length target: 30-45s per the
standing floor.

## Experiment status — Pilot #1, not proof
This episode is **experiment pilot #1 of 4**, testing whether a natural-recipient line
changes sends/reach against this account's baseline. It is not evidence the reach-first
strategy "works" on its own — per this account's own confidence framework, 3+ tests give
an early signal, 5+ a usable direction, 8+ stronger evidence. Primary metric: sends/reach.
Secondary: reach vs. this account's own baseline, follows/reach. Nothing about hook type,
pacing, caption structure, CTA wording, or production quality should change mid-batch
before episodes 46-48 ship with the same principle and a batch analysis runs. Specifically:
**do not "improve" this hook toward a more sensational claim to chase CTR** — the entire
reason this concept survived red-team is that its hook's scope now matches the product's
real scope (the exact failure mode identified in episode 42). Widening the claim again
to sound bigger would reintroduce that same problem on purpose.

## Not yet done
This is a script only — no voice generation, no render, no gate run, no publish. Per the
standing verify-before-writing rule, the carrier/product facts above are current as of
22.9.2026 and should be re-checked if this episode sits unproduced for more than a few
weeks, since carrier app names and features change.
