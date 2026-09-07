# Episode 27 — script, ready to produce

**Topic:** Claude Code, beginner-friendly — chosen from measured demand, not picked fresh.
`channel/demand-report.md`: "claude code tutorial beginners" — 159,426 median views, 915,534
90th percentile — third-highest of all nine measured queries, and (per
`channel/content-memory.md`'s 28.8.2026 direction-report entry) agentic-coding content
explained to non-coders is the thinnest-covered format found in the whole competitive
landscape pass. Episode 12 already touched this space ("Most think it's for coders" — a
reassurance/concept angle) but never as a real hands-on demo; this episode is a different,
concrete angle on the same underserved niche, not a repeat.

## Product verification (done 7.9.2026, before writing a line of script)

Verified live, not from memory:
- Claude Code install: `curl -fsSL https://claude.ai/install.sh | bash` (Mac/Linux) or
  `irm https://claude.ai/install.ps1 | iex` (Windows PowerShell). Verify with `claude --version`.
- **Included in the normal Claude Pro plan ($20/month)** and Max — no separate purchase,
  same login as claude.ai. Also works inside VS Code, Cursor, and JetBrains IDEs, not just
  the terminal.
- A dedicated desktop app (macOS/Windows) shipped April 2026 — mentioned as a real, current
  option, not the only way to use it.
- Re-verify if this episode ships more than ~2 months after 7.9.2026 — same standing caution
  as every other episode (this space moves fast).

## The real demo — actually run, not scripted fiction

Per the standing rule (never fabricate a result): this was a real test, run once, transcript
kept.

1. A genuinely broken Python script (`average()` returns the correct sum divided by count,
   then subtracts 1 — an operator-precedence bug: `total / len(numbers) - 1` parses as
   `(total / len(numbers)) - 1`, not what a quick read suggests). Confirmed broken by
   actually running it: `[10,20,30,40,50]` → prints `29.0` instead of `30.0`.
2. Deliberately gave Claude Code the **wrong** diagnosis on purpose: "there's an off-by-one
   error in the loop that skips the first number." (False — the loop is correct; it's a
   `for n in numbers` that covers every element.)
3. Real, unedited response: it did not just patch what was described. It said explicitly
   *"the loop wasn't actually the bug"*, explained the real operator-precedence issue, fixed
   line 5 (`return total / len(numbers) - 1` → `return total / len(numbers)`), and verified
   the corrected output (`30.0`).

This is the episode's entire hook mechanism — not a hypothetical, an actual run kept as
evidence.

## Hook — type check against `hooks-guide.md`

Recent log: 24 Contrarian Open, 25 Shock/Surprise, 26 Product/Outcome Showcase. Picking
**Story/Anecdote Teaser** — not used in any episode so far, and it's the natural shape for
"so this happened when I tried X."

Structure borrowed (mindset, not copied) from a viral hook-analysis Reel David sent
(7.9.2026): danger/setup → anticipation → expectation-flip surprise. Applied here as: state
a wrong instruction was given on purpose (setup) → what most tools would do with it
(anticipation/stakes) → what this one actually did instead (the flip).

> **"I told Claude Code the wrong bug. On purpose."**

Passes the dry-sentence + concrete-fact tests: a specific, already-true, checkable claim —
not a hypothetical, not something the viewer has to imagine.

## Full narration (~50s at natural pace)

1. **(hook)** "I told Claude Code the wrong bug. On purpose."
2. "I said it was an off-by-one loop — skipping the first number in the list."
3. "That's the kind of wrong instruction most AI tools just go along with."
4. "This one didn't. It said the loop wasn't the bug at all."
5. "The real bug was one line down — dividing correctly, then quietly subtracting one."
6. "It fixed the actual problem — not the one I described."
7. "Claude Code comes with a normal Pro plan. Twenty dollars a month, no separate purchase."
8. "The exact setup's in the link in bio."
9. **(locked outro)** "Follow for the setup that actually works."

## On-screen text cues

- Line 1: hook, plain punch text.
- Line 2: termbox-style code snippet showing the false claim ("off-by-one loop — skips
  first number").
- Line 4: quote-card, the real quote — "the loop wasn't actually the bug at all."
- Line 5-6: scoreboard contrast — "What I said: off-by-one loop" [wrong, grey] vs. "What it
  found: operator precedence, line 5" [right, green].
- Line 7: toolmark badge "$20/MONTH · INCLUDED".

## Music

Mood **suspense** (sparse dissonance, slow-build dread — per `studio/lib/templates.ts`'s own
description: "slow-build reveal ... use sparingly") — matches the anticipation-before-flip
structure directly, closest fit to what David asked for ("intense"), distinct from episode
26's "bright".

## Design

Palette must differ from episode 26 (`#5EEAD4`/`#FF8A5B`) per the design-variety gate —
picking a cooler, higher-contrast pair suited to a "suspense" mood (locked in at build time,
recorded in `channel/used-designs.json` automatically by `produce.sh`).

## Setup guide (draft — finalized once the build exists)

1. Open a terminal (Mac: Spotlight → "Terminal"; Windows: Start menu → "PowerShell") — a
   plain window for typed commands, already built into the computer.
2. Mac/Linux: paste `curl -fsSL https://claude.ai/install.sh | bash` and press Enter.
   Windows: paste `irm https://claude.ai/install.ps1 | iex` instead.
3. Type `claude --version` and press Enter — if it prints a version number, the install
   worked.
4. Type `claude` and press Enter inside any project folder — the first time, a browser tab
   opens asking to log in with the same email/password used for claude.ai.
5. Already have a Claude Pro or Max subscription? Nothing else to buy — Claude Code is
   included. On the free plan, it asks to upgrade before it will run.
6. Type a real request in plain English (e.g., "there's a bug in this file, fix it") and
   press Enter — it reads the actual file and responds.
7. Optional: the same tool also works inside VS Code, Cursor, and JetBrains IDEs as an
   extension, not just the terminal — same login, same account.

## Caption / YouTube text (draft)

> I told Claude Code the wrong bug. On purpose. I said it was an off-by-one loop error.
> It wasn't. It found the real bug instead — an operator-precedence mistake one line down —
> and fixed that, not what I described.
>
> Claude Code comes with a normal Pro plan, $20/month. No separate purchase.
>
> Full setup, exact clicks: actually-works.com/e/27
>
> Follow for the setup that actually works.
>
> #claudecode #aitools #coding #buildinpublic #debugging
