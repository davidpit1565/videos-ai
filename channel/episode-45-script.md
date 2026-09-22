# Episode 45 — script, ready to produce

## Topic
US phone carriers (Verizon, AT&T, T-Mobile) already run real-time AI scoring on every
incoming call, before it rings — the "Scam Likely" label most people have already seen is
that AI's output, not a static blocklist. Each carrier has a free app (Verizon Call Filter,
AT&T ActiveArmor/Call Protect, T-Mobile Scam Shield) that lets a user see and manage it
directly. It does not catch everything — a scammer using a spoofed but cryptographically
signed number can still get through even with STIR/SHAKEN in place.

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

## Verification (live web search, 22.9.2026)
Checked directly against each carrier's own current support documentation:
- **What it does**: real-time AI scoring of incoming calls against known scam/robocall
  patterns (predictive-dialer signatures, reported numbers, spoofing indicators); flags a
  suspicious call as "Scam Likely" or similar before the phone rings.
- **AT&T**: Call Protect / ActiveArmor — enabled via Features → Call filtering → Call
  Protect (accept terms, toggle on), or managed in the myAT&T / ActiveArmor app.
- **Verizon**: Call Filter — included free on standard/prepaid plans with a compatible
  device; managed via the Call Filter app or My Verizon.
- **T-Mobile**: Scam Shield — free tier includes Scam Likely labeling, Scam Block,
  Caller ID, and spam-to-voicemail; managed via the T-Life app.
- **Real, stated limitation, not smoothed over**: STIR/SHAKEN (the industry standard behind
  part of this) verifies that a caller ID isn't spoofed — it does NOT verify the caller's
  actual intent. A scammer calling from a legitimately-registered, signed number still gets
  through clean. This is the honesty beat the script states directly.
- **Scope, stated plainly**: US carriers only. Not a claim about carriers in other
  countries, and not a claim that every scam call gets caught.

## Hook rules check (against `channel/hooks-guide.md`)
- **Type**: Contrarian Open ("You think X. Actually Y is already doing this.") — last used
  episode 43 (Windows), a 2-episode gap from 44 (Shock/Surprise) and 43 — check against the
  live log before finalizing production; rotate if this repeats episode 43's exact type
  too close together.
- **Specific, checkable claim in the first clause**: names the real, current mechanism
  (AI scoring incoming calls) and, within the first three lines, the real named carriers —
  no vague "your phone company."
- **Personal-stakes, plain language**: scam calls are a near-universal fear; zero jargon
  needed to feel the stake.
- **Cold-read test**: checkable directly by opening the relevant carrier app.

## Narration (draft — subject to the usual voice/accent/pacing revision rounds before shipping)
1. "Your phone already has an AI watching every call before it rings."
2. "Verizon, AT&T, and T-Mobile all score incoming calls in real time — that's what 'Scam Likely' actually is."
3. "It catches known robocall patterns. It does not catch a scammer using a real, verified number."
4. "Each carrier has its own free app — Call Filter, ActiveArmor, or Scam Shield — where you can see it working."
5. "Send this to whoever's going to answer the next call they don't recognize."
6. "The setup's in the link in bio."
7. "Follow for the setup that actually works."

(Line 5 is the experiment's actual variable — a natural-recipient line embedded as content,
not an imperative "share this" instruction. Per the second-opinion review: people don't
share because they were told to, they share because mid-video they already thought of
someone. This replaces the earlier, rejected "who would you send this to" framing.)

## Density check
5 distinct ideas across 7 lines (2 locked CTA lines excluded): (1) the core mechanism, (2)
which three carriers/what "Scam Likely" really is, (3) the real limitation (signed-but-
malicious numbers), (4) how to see/manage it yourself, (5) the natural-recipient line.
Within the ~4-5 idea range this account's own data associates with better save/engagement
performance.

## Simplicity/length check
No jargon beyond the carrier product names themselves (Call Filter, ActiveArmor, Scam
Shield), each named once. STIR/SHAKEN is deliberately NOT named on camera — the limitation
is stated in plain consequence language ("a scammer using a real, verified number") rather
than the technical standard's name, keeping it inside the channel's plain-language rule.
Length target: 30-45s per the standing floor.

## Not yet done
This is a script only — no voice generation, no render, no gate run, no publish. Per the
standing verify-before-writing rule, the carrier/product facts above are current as of
22.9.2026 and should be re-checked if this episode sits unproduced for more than a few
weeks, since carrier app names and features change.
