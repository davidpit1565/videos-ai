# Episode 46 — script, ready to produce

## Topic
Microsoft 365 Copilot (the "Copilot Chat" and in-app Copilot used inside Word, Excel,
Outlook, and Teams on a work or school account) stores what an employee types to it.
Microsoft's own support documentation describes a **Copilot activity history** — the
user's prompts and Copilot's responses, including citations to whatever it drew on —
that any employee can view and delete themselves from the **My Account** portal
(myaccount.microsoft.com → Data and privacy → Copilot activity history).

Separately, and this is the part a coworker doesn't expect: organizations manage that
same data through **Microsoft Purview**, where prompts and responses can be captured
by **retention policies** the employer's own IT/compliance admin controls — Microsoft's
own guidance states retention can run to about a year on some licenses, or indefinitely,
depending on what the organization configures — and, under a formal legal or compliance
process (**eDiscovery**), an admin holding the right Purview permissions can read the
actual prompt/response content of an employee's Copilot chats. This is not automatic for
every manager or every IT person — Microsoft's own documentation states plainly that
reading prompt/response text needs specific Purview permissions beyond general admin or
manager status — but the capability is real, it exists today, and it is not something
a regular employee can see or control from their own account.

## Why this topic, why now
- **Concept 2 of the same Phase 2 four-concept reach-first list** episode 45 opened
  ("a workplace/shared-account AI privacy setting — what a manager or IT admin can see in
  a workplace AI tool"). Share-trigger: the specific coworker who assumes a work AI chat
  is exactly as private as a personal one. Action step: the exact place to check your own
  employer's tool for this, in your own account, right now.
- **Different company/mechanism from every episode so far**, including every episode in
  this reach-first run (41 ChatGPT/Finances, 42 Android/Scam Detection, 43 Windows/Recall,
  44 WhatsApp/Message Summaries, 45 carrier-network scam-call screening) — this is the
  first to cover Microsoft 365/Copilot and the first to cover a workplace-admin-visibility
  angle rather than a personal-device feature.
- **Verified live (23.9.2026)**, not assumed from memory or from episode 18's old mistake:
  Microsoft 365 Copilot's activity history, Purview retention for Copilot, and Purview's
  audit/eDiscovery access to Copilot prompt/response content are all real, current,
  documented behaviors, confirmed against Microsoft's own Learn and Support pages (not a
  third party's paraphrase) on the day this script was written.

### Scope (hard limits for this script — do not widen)
- Microsoft 365 Copilot / Copilot Chat on a **work or school account** only — not the free
  consumer Copilot, and not every "workplace AI tool" in general.
- Do not claim every manager can read an employee's chats. Reading prompt/response content
  requires specific Purview permissions (eDiscovery/Communication Compliance roles), not
  general admin or manager status — Microsoft's own documentation says this directly.
- Do not claim admins actively watch every chat in real time. The documented capability is
  retention plus access under a formal compliance/legal process, not live monitoring.
- Do not claim a fixed retention period across every organization — it depends on the
  organization's own Purview configuration and license (Microsoft states ranges up to
  roughly a year, or indefinite, not one universal number).
- Do not claim the employee-facing "activity history" deletion in My Account removes the
  organization's own Purview-retained copy — Microsoft does not state that it does; the
  script does not imply it.

## Verification (live web search, 23.9.2026, same day as writing)
- **Microsoft 365 Copilot Chat history is real and stored, in the user's own words from
  Microsoft**: interacting with Copilot stores the prompt and Copilot's response,
  including citations, as Copilot activity history — viewable and deletable by the user
  themselves from My Account (myaccount.microsoft.com) → Data and privacy → Copilot
  activity history, for work/school accounts as well as personal ones.
- **Microsoft Purview governs the organization's own copy, separately from that personal
  view**: Microsoft's Purview documentation states that Copilot prompts and responses can
  be captured under the organization's retention policies, with retention periods that
  vary by license (Microsoft states figures up to about a year, or indefinite, depending
  on configuration) and can be preserved, or deleted automatically at the end of the
  retention period the organization set.
- **Audit and eDiscovery access is real, and permission-gated**: Microsoft's audit
  documentation for Copilot and AI apps states that prompt and response content, the
  files/sites Copilot drew on, and which app or agent was used, can be reconstructed for a
  formal review — but reading the actual prompt/response text needs additional Purview
  permissions on top of being an admin; a manager or general IT admin does not get this by
  default.
- **What the employee can check on their own device, right now**: sign in to
  myaccount.microsoft.com with the work or school account, go to Privacy → Data and
  privacy, and open Copilot activity history — this shows the same prompts/responses
  described above and proves the data exists and is stored, even though it does not show
  the organization's separate Purview-side retention or admin access.

## Hook rules check (against `channel/hooks-guide.md`)
- **Type**: Direct Address (declarative, second-person claim — the same non-question shape
  episode 2's all-time-highest hook used, "What an AI agent actually is," tagged Direct
  Address/definitional in the log). **Rotation check**: episode 45 was Contrarian Open,
  episode 44 was Shock/Surprise — Direct Address/Question was last used episode 40, a
  6-episode gap, and the guide's own research names it the single strongest type for this
  genre. Not repeating 44 or 45's type, and not forcing a question mark where a direct,
  second-person claim lands harder.
- **Specific, checkable claim in the first clause, no second-sentence deferral**: "Your
  Copilot chats at work don't vanish when you close the tab" is a fact the viewer can go
  check themselves in the next thirty seconds, stated and completed inside one sentence —
  the stake ("someone else can read them later") lands in the same sentence, same
  structure as episode 43's "Windows can now take a screenshot of your entire screen every
  few seconds — and save it."
- **Fear/personal-stakes register, not neutral curiosity**: the loss of an assumed
  privacy at work, something the viewer can be genuinely wrong about right now, not a
  hypothetical or an abstract capability.
- **Cold-read/one-second-parse test**: no jargon, no product-internals vocabulary
  ("Purview," "eDiscovery," "retention policy" are explained in plain consequence language
  in the body, never required to parse the hook itself).
- **David's direct note on episode 45 ("the first two seconds didn't make me want to keep
  watching OR follow") — addressed on both counts**: the hook itself is rewritten to be a
  real, personally relevant, surprising claim (not the flatter "phone carriers already
  screen calls" shape that read as informational); separately, the reason to *follow* is
  made explicit near the end, before the locked outro line — see "Solving for follow,
  not just watch-through" below.

## Solving for follow, not just watch-through
Per David's direct flag: a hook proving "this one video is good" doesn't by itself give a
reason to hit follow — that has to be a distinct, deliberate beat, not assumed to follow
automatically from a good hook. This channel already has five reach-first episodes behind
it (41 ChatGPT/Finances, 42 Android/Scam Detection, 43 Windows/Recall, 44 WhatsApp/Message
Summaries, 45 carrier scam-call screening), each a different real, named, currently-live
AI feature already running on the viewer without them knowing. That is a real, stated
pattern — not invented for this script — and it is stated directly, once, right before the
existing locked outro line ("Follow for the setup that actually works."), so the CTA's
promise ("actually works") lands on top of an explicit, checkable claim about what
following gets you: **the next one of these, on a schedule this channel has already kept**.
No new gimmick, no invented mechanic — the same locked line, earned by a stated, true
track record right before it.

## Narration (final — revised once for `audio/script_lint.py`'s soft-ending flags before voice generation)
1. "Your Copilot chats at work don't vanish when you close the tab — someone else can still read them." (rewrote "read them later" → "still read them": "later" is an unstressed -ER ending script_lint flags)
2. "Microsoft's own privacy page is direct about it — your prompts and its reply get saved to your own history of it." (rewrote through three passes: "says it plainly ... its answers ... your activity history" → "is direct about it ... its reply ... your own activity history" (fixed "plainly"'s flagged -LY and "answers"'s flagged R+cluster) → final: "your own history of it" — "activity" kept re-measuring as swallowed (0.095s/syllable, then 0.075s/syllable even with a buffer word added) across two separate reroll rounds; per CLAUDE.md's documented pattern ("if reseeding fails, reword the line to drop the offending word"), the word itself was dropped rather than fought a third time. No accuracy lost: the claim itself — prompts/responses are saved and viewable — stays intact; the setup guide's own steps[] still name the real UI label, "Copilot activity history," precisely)
3. "Your company's own IT side can keep that same copy for up to a year — sometimes even more, based on what they've set." (rewrote twice: "sometimes longer" → "sometimes even more" fixed "longer"'s flagged unstressed -ER; "depending on" → "based on" after a later full-file `--deep` pass flagged "depending" at 0.087s/syllable — "likely swallowed, re-roll this line" — on this same, otherwise-unchanged line)
4. "It's not just any boss. Reading the actual chat needs a specific compliance permission, not just being an admin." (rewrote twice: "manager" → "boss" fixed a flagged unstressed -ER; "It's not every boss" → "It's not just any boss" after a later full-file `--deep` pass flagged "every" at 0.093s/syllable — "likely swallowed, re-roll this line" — same real claim, same word count, no accuracy change)
5. "You can check your own copy right now — your account, Privacy, Copilot activity history." (rewrote "Microsoft account" → "your account" after the first full render measured "Microsoft" at 0.053s/syllable — "likely swallowed, re-roll this line"; dropping it costs nothing since the on-screen scoreboard scene never showed "Microsoft" text either, and the exact myaccount.microsoft.com path is still spelled out in full on the episode's own setup-guide page)
6. "Five hidden AI features so far this year. This one makes six." (rewrote away from "the sixth hidden AI feature ... this month": "sixth" and "month" both end in a flagged breathy -TH, "people" a flagged -LE/-BLE — same true claim, restated with cardinal "six" instead of the ordinal)
7. "The setup's in the link in bio."
8. "Follow for the setup that actually works." (the locked brand line — "actually" always flags on -LY per script_lint's own note; accepted, not rewritten, per the canonical-lines manifest)

## Density check
5 distinct ideas across 8 lines (2 locked CTA lines excluded): (1) the core claim — work
Copilot chats are stored, not gone, (2) where that's documented in Microsoft's own words
(activity history), (3) the organization's separate retention window, (4) the real limit —
not every manager, a specific permission is required, (5) the exact, personal, doable
action step (check your own account). Within the ~4-5 idea range this account's own data
associates with better save/engagement performance, matching episode 45's own density.

## Simplicity/length check
No unexplained jargon: "Purview," "eDiscovery," and "retention policy" are never spoken —
"your company's own IT side," "keep that same copy," and "a specific compliance
permission" carry the same real meaning in plain language, the same substitution episode
45 made for STIR/SHAKEN. "Copilot" and "Microsoft account" are named directly (per the
episode 7/n8n precedent — naming the real, specific product does not appear to cost a
hook on this channel's own data). Length target: 30-45s, matching the standing floor.

## Experiment status — pilot within the same reach-first batch as 41-45
This is the sixth reach-first-era episode. It carries forward episode 45's pilot #1
natural-recipient mechanic in spirit (the coworker who assumes privacy is the natural
recipient a viewer would think of), but its primary content addition is the follow-problem
fix above — a distinct, unsolved axis from the sends/reach experiment, per David's direct
flag today. Per the reach-first batch's own confidence framework (3+ tests = early signal,
5+ = usable direction, 8+ = stronger evidence), nothing about hook type, density, or CTA
structure should change again mid-batch before a real batch analysis runs against the
studio's tracked numbers.

## Not yet done
This is a script only, at the point of writing — no voice generation, no render, no gate
run, no publish, until the production steps below run. Per the standing verify-before-
writing rule, the Microsoft 365 Copilot / Purview facts above are current as of 23.9.2026
and should be re-checked if this episode sits unproduced for more than a few weeks, since
Microsoft's own admin-console names and retention defaults change.
