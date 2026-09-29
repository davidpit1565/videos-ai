# Episode 51 — script, ready to produce

## Topic
AI chatbots (ChatGPT, Gemini, Claude, Copilot, and others) confidently answer health and
money questions wrong most of the time, and never flag when they're guessing. Two
independent 2026 studies, plus a third separate finding on confidence language:

- **BMJ Open, published 14 April 2026** (researchers from UCLA, University of Alberta, and
  Wake Forest): tested five major chatbots (Gemini, DeepSeek, Meta AI, ChatGPT, Grok) on
  250 real health questions covering cancer, vaccines, stem cells, nutrition, and athletic
  performance. **49.6% of responses were problematic** — 30% "somewhat problematic," 19.6%
  "highly problematic" (the kind of answer that could plausibly lead someone toward
  ineffective or dangerous treatment).
- **Saturn (a UK fintech firm), "Artificial Authority" report, 2026**: tested ChatGPT,
  Gemini, Claude, and Copilot on 121 financial questions (debt, mortgages, pensions, tax,
  savings, student loans), each asked 5 times for consistency — 10,000+ total responses.
  **57% were incorrect or incomplete overall; 88% on complex queries.** Free-tier models
  did worse (63% wrong) than paid ones (49% wrong).
- **A separate, distinct test** (news-source attribution, not health/finance — kept
  distinct here deliberately, not conflated with the two studies above): ChatGPT gave
  incorrect answers in 134 of 200 queries testing news-source identification, and only
  expressed uncertainty in 15 of those 134 wrong answers.

The payoff/technique: a single, copy-paste prompt that forces the chatbot to disclose its
own confidence instead of answering with flat, undifferentiated certainty — "Rate your
confidence in this answer, 0 to 100, and tell me exactly what could make it wrong or
outdated." This doesn't fix the underlying accuracy problem, and the script says so
explicitly — it's a real, free, zero-setup way to get the chatbot to surface its own doubt
instead of hiding it, which every source above found it does not do on its own.

## Why this topic, why now — continuing the whole-audience pivot
- Direct continuation of the 24.9.2026 standing pivot (episode 49): pick the topic with the
  broadest possible addressable audience, not a subgroup. Health and money questions are
  asked by, functionally, everyone who has ever opened an AI chatbot — broader than
  episode 49's "Google Search users" in one sense (not everyone asks Google Search
  health/financial questions specifically, but the *category* of "asked an AI something
  that actually mattered" is close to universal for anyone who uses these tools at all) and
  carries stronger personal stakes (health, money) than a search-interface quirk.
- **Real emotional stakes + a universally reusable technique**, the same combination
  research and this channel's own data (episode 1, episode 49) point to as the strongest
  driver: the stake is fear (a decision you already made based on an AI answer might have
  been wrong, and it never told you), the payoff is a single, memorable, copy-paste prompt
  that works on any chatbot, for any future question, forever.
- **Verified current, not stale**: all three sources are 2026 publications, checked live
  this session (see Verification below). No product-naming risk here (the claim is about
  chatbot *behavior*, not a single feature that could be retired) — different risk profile
  from episode 18's "ChatGPT agent mode" mistake, but the underlying studies were still
  read directly rather than assumed from a headline.
- **David's own direction, verbatim (translated), given right after approving this topic**:
  "if possible also add real screenshots, that's strong, and with correct integration —
  but really in small amounts, not a lot." See "Screenshot constraint" below for how this
  was actually handled and why it fell back to the channel's existing sourced-citation-card
  style instead of a literal captured screenshot.

## Screenshot constraint — handled honestly, not faked
Attempted to get a real screenshot of the BMJ Open study's own public abstract page via
the Playwright browser tool, to use as a brief, correctly-sourced visual during the health
stat line. **The browser tool failed at the infrastructure level in this environment**
(Chromium sandboxing fails running as root in this container — a real, technical failure,
not a judgment call to skip it). Rather than fabricate a mocked-up "screenshot" that isn't
actually a captured image of anything real (which would be exactly the kind of fabrication
`CLAUDE.md` prohibits), this episode uses the channel's already-established sourced
citation-card style instead (source name + date rendered as on-screen text, same pattern
prior episodes already use for stat citations) — real information, correctly attributed,
just not a literal screen capture. If David can supply a real screenshot of his own (e.g.
an actual chat session using the confidence-check prompt on his own phone), it can be
added in a later pass — flagged to him directly, not silently dropped.

## Candidates compared
1. **AI chatbot health/financial accuracy (this topic) — CHOSEN.** Two independent,
   large-sample 2026 studies, both peer-reviewed or methodologically transparent, covering
   the two highest-stakes categories of question most people actually ask a chatbot.
   Broadest addressable audience combined with the strongest fear/stakes register this
   channel's own research has found (content-memory.md, 4.9.2026: fear-register hooks
   average 264,031 views vs. hope-register's 5,423 — a 49x gap).
2. **The "mirror" ChatGPT prompt (image showing how you treat the AI based on chat
   history)** — considered, then REJECTED before writing anything. Found via one Medium
   listicle-style article only ("7 ChatGPT Prompts That Feel Illegal to Know") with no
   independent corroboration found in a follow-up search — exactly the single-uncorroborated-
   source situation the verify-before-writing rule exists to catch. Not used.
3. **A general "AI hallucination" episode with no specific current study** — considered,
   rejected as too vague/stale-feeling next to two dated, named, sourced 2026 studies that
   make the same point with checkable numbers.

## Verification (live web search, 28.9.2026)
- **BMJ Open, 14 April 2026** — corroborated across at least nine independent outlets in
  the initial search pass (The Conversation, AIhub, NYU's Information for Practice,
  Decrypt, Washington Post, News-Medical, Machine Learning for Science, Medical Xpress,
  CIDRAP) — consistent 49.6%/30%/19.6% figures across all of them, and the CIDRAP piece
  names the study venue and the three universities directly.
- **Saturn "Artificial Authority" report, 2026** — corroborated across at least eight
  independent outlets (OECD.AI's own incident database, Silicon UK, Financial Advisor
  magazine, IBS Intelligence, InvestmentNews, BeInCrypto, FF News, GN Crypto News) —
  consistent 57%/88%/121-questions/10,000+-responses figures across all of them.
- **News-source-attribution test (the confidence/uncertainty finding)** — found in the
  first research pass alongside general hallucination-rate coverage; kept in the script as
  its own explicitly separate, distinct test (not merged into the health or finance studies'
  own numbers) specifically to avoid misattributing a finding from one study to another.
- **Scope, stated plainly**: this is about general-purpose AI chatbots answering health and
  financial questions specifically — not a claim about every AI product or every possible
  use case.

## Comprehension test — applied to the ENTIRE script
- **Line 1 (hook)**: "AI" here means the AI chatbots almost everyone already knows by name
  (ChatGPT etc., named explicitly in lines 2-3) — no unexplained feature name, no jargon.
  The claim ("never tells you when it's guessing") is concrete and checkable by anyone who
  has ever used one.
- **Line 2/3**: state the studies' real findings in plain numbers ("almost half," "more than
  half") before any technical framing — no "hallucination," no "LLM," no "training data."
- **Line 4**: "it was wrong 134 times out of 200, and only said it wasn't sure 15 of those
  times" — a plain, countable comparison, no jargon.
- **Line 5**: the fix is stated as literal words to paste, not a described mechanism — a
  first-time viewer can act on it without understanding anything about how AI works
  internally.
- Every sentence re-read cold, as if by someone who has never heard "hallucination" or
  "LLM" used before — holds up standalone, same discipline as episode 49's script.

## Hook rules check (against `channel/hooks-guide.md`)
- **Type: Contrarian Open** — overturns the assumed default (you'd expect an AI to flag
  when it's not sure; it doesn't) while still landing a concrete, checkable claim in the
  first clause, the same shape episode 47's Contrarian Open used. Last used episode 47 (a
  3-episode gap since); not a repeat of episode 48 (Shock/Surprise), episode 49 (The
  Specific Number), or the Flow business episode (50, a different content vertical, not
  part of this rotation).
- **Dry-sentence test**: read cold, states something true and checkable right now, not a
  hypothetical or a tease.
- **Real stake, not reassurance**: health and money are named directly, immediately — the
  strongest fear-register combination this channel's own data has measured.

## Sendability test
Would a specific, real person forward the hook line or caption to one specific other
person, with zero extra clicks?
- **The hook line** ("AI never tells you when it's just guessing — not about your health,
  not about your money.") is a complete, standalone, checkable claim about something nearly
  everyone who uses these tools has personally experienced.
- **The caption's forward-as-is artifact**: the exact confidence-check prompt, ready to
  copy-paste, sits directly in the caption body — a stranger receiving just the caption
  text (no link click required) has the complete, usable fix in hand, the same "episode 1"
  shape that remains this account's only episode with real recorded shares.

## Where the comment-inviting element lives
Caption ends with a direct, personally-answerable question tied to the hook's exact tension
— "Have you ever made a real decision based on an AI's health or money answer, and only
found out later it was wrong? Comment YES or NO." — plus a lower-effort comment-to-DM path:
"Comment CHECK and I'll send you the exact prompt to paste, formatted and ready."

## Narration
1. "AI never tells you when it's just guessing — not about your health, not about your money."
2. "A 2026 medical study tested five AI chatbots on real health questions. Almost half the answers were wrong or misleading."
3. "A separate test ran the same chatbots on ten thousand money questions. More than half were wrong too — worse the more complicated it got."
4. "In a different test, it was wrong 134 times out of 200 — and only admitted it wasn't sure 15 of those times."
5. "Before you trust its next answer, paste this: rate your confidence, zero to a hundred, and tell me exactly what could make this wrong."
6. "Send this to someone who just asked it something that actually matters."
7. "The setup's in the link in bio."
8. "Follow for the setup that actually works."

### Density check
5 distinct ideas across lines 1-5 (no uncertainty disclosure, health-study stat,
money-study stat, confidence-language stat, the fix) — inside the account's own standing
4-5 idea range for a 30-75s reel, same as episodes 48/49.

### Length check
8 lines, comparable density/length to episode 49 (8 lines, 49.6s) — targeting the same
30-75s band, to be confirmed against the real generated narration's duration during
production, not assumed.

## Not yet done at time of writing
Script only as of this point. Voice generation, retiming, captions, render, gate, and
publish happen next. The three sources above are current as of 28.9.2026 and should be
re-checked if this episode sits unproduced for more than a few weeks, per the standing
verify-before-writing rule.
