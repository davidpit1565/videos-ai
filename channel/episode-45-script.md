# Episode 45 — script, ready to produce

## Topic
US phone carriers (Verizon, AT&T, T-Mobile) each run network-level systems that identify or
block suspected spam and scam calls, before the user answers. T-Mobile states directly that
its "Scam Likely" label comes from Scam ID running in its network. Each carrier has a free
app (Verizon Call Filter, AT&T ActiveArmor/Call Protect, T-Mobile Scam Shield) that lets a
user see and manage it directly. It does not catch everything — a scammer calling from a
legitimately-registered, cryptographically-signed number (STIR/SHAKEN only authenticates
that the caller ID isn't spoofed, a separate system from the scam-detection above, and it
says nothing about the caller's actual intent) can still get through clean.

**Revised 22.9.2026 after a second, source-by-source red-team.** The original claim —
"real-time AI scoring on every incoming call, before it rings," and "'Scam Likely' is that
AI's output, not a static blocklist" — bundled three separate factual claims (every call /
AI specifically / pre-ring timing) into one sentence stronger than any single source
supports. Verizon's own language is "analytics and databases that are constantly evolving";
T-Mobile's is network-level behavioral detection with an explicit "Scam ID" name; none of
the three carriers' own pages assert "AI" scores "every" call. Softened to what each source
actually says, and STIR/SHAKEN is now explicitly named as a *separate* system from the
detection itself, not a component of it — the earlier draft's phrasing risked implying
STIR/SHAKEN was "the AI's brain," which it is not.

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

## Verification (live web search, 22.9.2026 — re-checked, second pass, same day)
First pass checked each carrier's own current support documentation and concluded "AI
scoring on every incoming call, before it rings." A second, source-by-source red-team
(same day) found that phrasing stronger than what any single source actually states, and
it was revised. What each source actually supports:
- **What it does**: network-level systems that identify or block suspected spam/scam calls
  before the user answers. Verizon's own wording is "analytics and databases that are
  constantly evolving"; T-Mobile explicitly names its system "Scam ID," running in-network.
  None of the three carriers' own pages say "AI" scores "every" call — that specific
  combination is not sourced, so the script no longer claims it.
- **AT&T**: Call Protect / ActiveArmor — enabled via Features → Call filtering → Call
  Protect (accept terms, toggle on), or managed in the myAT&T / ActiveArmor app.
- **Verizon**: Call Filter — included free on standard/prepaid plans with a compatible
  device; managed via the Call Filter app or My Verizon.
- **T-Mobile**: Scam Shield / Scam ID — free tier includes Scam Likely labeling, Scam
  Block, Caller ID, and spam-to-voicemail; managed via the T-Life app.
- **Real, stated limitation, not smoothed over**: STIR/SHAKEN authenticates that a caller
  ID isn't spoofed — it is a **separate system** from the scam-detection above, not part of
  it, and it does NOT verify the caller's actual intent. A scammer calling from a
  legitimately-registered, signed number still gets through clean.
- **Scope, stated plainly**: US carriers only. Not a claim about carriers in other
  countries, and not a claim that every scam call gets caught.

## Hook rules check (against `channel/hooks-guide.md`)
- **Type**: Contrarian Open. **Checked against the file's actual rule (not a guess):**
  `hooks-guide.md`'s own stated rule is "never repeat the same hook type two episodes in a
  row" — a literal back-to-back check, not a 2-3 episode window. Episode 43 was also
  Contrarian Open, but episode 44 (Shock/Surprise) sits directly between 43 and this one,
  so 45 does not break the rule as written. Flagging this explicitly since it was raised as
  a question, rather than silently assuming it's fine.
- **Specific, checkable claim in the first clause**: names the real, current mechanism
  (AI scoring incoming calls) and, within the first three lines, the real named carriers —
  no vague "your phone company."
- **Personal-stakes, plain language**: scam calls are a near-universal fear; zero jargon
  needed to feel the stake.
- **Cold-read test**: checkable directly by opening the relevant carrier app.

## Narration (draft — subject to the usual voice/accent/pacing revision rounds before shipping)
1. "Your phone carrier may already be screening calls before you even answer."
2. "Verizon, AT&T, and T-Mobile all run network-level systems that flag suspected spam and scam calls."
3. "That 'Scam Likely' label? T-Mobile says it comes from Scam ID, running in its own network."
4. "It doesn't catch everything — a scammer calling from a real, verified number still gets through."
5. "Each carrier has its own free app — Call Filter, ActiveArmor, or Scam Shield — where you can see it working."
6. "Send this to whoever's going to answer the next call they don't recognize."
7. "The setup's in the link in bio."
8. "Follow for the setup that actually works."

(Line 6 is the experiment's actual variable — a natural-recipient line embedded as content,
not an imperative "share this" instruction. Per the second-opinion review: people don't
share because they were told to, they share because mid-video they already thought of
someone. This replaces the earlier, rejected "who would you send this to" framing.)

## Density check
6 distinct ideas across 8 lines (2 locked CTA lines excluded): (1) the core mechanism
(network-level screening, not "AI scores every call"), (2) which three carriers, (3) the
"Scam Likely" label's real, named source (T-Mobile's Scam ID), (4) the real limitation
(a verified number still gets through — STIR/SHAKEN named as a separate system), (5) how
to see/manage it yourself, (6) the natural-recipient line. Slightly above the ~4-5 idea
range this account's own data associates with better save/engagement performance — kept
anyway because the STIR/SHAKEN separation (idea 4) exists specifically to prevent a
factual misunderstanding the second red-team flagged, not as padding.

## Simplicity/length check
No jargon beyond the carrier product names themselves (Call Filter, ActiveArmor, Scam
Shield), each named once. STIR/SHAKEN is deliberately NOT named on camera — the limitation
is stated in plain consequence language ("a scammer using a real, verified number") rather
than the technical standard's name, keeping it inside the channel's plain-language rule.
Length target: 30-45s per the standing floor.

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
