# Episode 30 — script, ready to produce

**This episode is Experiment 1 ("Immediate Utility Replication") from `channel/experiments.md`
Batch 1 — not a normal episode.** Full pre-registered hypothesis, metrics, and win/lose
thresholds are locked there (8.9.2026), before this script was written. Do not change
those thresholds after this ships; any correction goes in `experiments.md` as a new
dated note, never an edit to the pre-registered numbers.

## What this episode tests

H1 in `content-memory.md`: does the *immediate personal utility mechanism* (a single,
low-friction, save-worthy artifact) replicate on a different specific artifact than
episode 1 (ChatGPT Custom Instructions), while holding low-friction properties constant —
one action, near-zero prerequisite knowledge, immediate visible payoff, genuine
save/share potential. Deliberately **not** a topic swap to a more technical tool (n8n,
Claude Code) — that framing was caught and corrected before this script was written
(see `experiments.md`'s "corrected 8.9.2026" note) because it would have confounded
utility with prerequisite-knowledge friction.

## The artifact

A single instruction, pasted once into any AI chat's message box (no settings
navigation needed — even lower friction than episode 1), that stops the assistant from
padding its answer with hedging/caveats before actually answering:

> Answer first, in one sentence. Then explain, only if I ask. Skip caveats unless they
> change the answer.

## Real evidence — not staged, not invented

Per David/ChatGPT's explicit QA requirement: the before/after shown on screen must be
a real captured exchange, not a plausible-sounding invented one. Captured live in this
session, in David's own real ChatGPT account:

**Question asked (identical both times):** "should I learn Python or JavaScript first?"

**BEFORE (no instruction given)** — real, verbatim excerpt (full answer was several
paragraphs; excerpted for screen space, not altered):
> "For you specifically, I'd learn JavaScript first, then Python... My recommended
> order: 1. JavaScript → TypeScript ... 2. Python ... The important part: Don't spend 3
> months learning JavaScript syntax in isolation... My vote: JavaScript/TypeScript
> first. 🚀"

**AFTER (same question, same chat, after pasting the instruction above):**
> "JavaScript first."

That's the entire real answer — two words. This is a dramatic, genuine, verified
contrast: headers, bullet lists, multiple sections, and an emoji vs. a direct
two-word answer. Confirmed by David directly (screenshot + copy-pasted text) before
any build work started.

## Product verification

This isn't a claim about a specific AI feature that could go stale — it's a plain
instruction-following behavior, true of any capable chat model regardless of version.
No live-current-feature risk the way a named product feature (like "ChatGPT Work" or
"agent mode") would carry. Explicitly avoided any claim comparing which model handles
this "better" — the video is about the artifact, not a model benchmark (per David/
ChatGPT's explicit instruction).

## Hook — type check against `hooks-guide.md`

Log's last: 29 Shock/Surprise. This episode uses **Contrarian Open** (last used
episode 24, "Editors squeeze the picture...") — a real gap since then.

Hook (revised per QA — "every" softened from an absolute claim to a rhetorical one):
**"AI chats love padding the answer before they actually answer you."**

## Full narration (~40s at natural pace)

1. AI chats love padding the answer before they actually answer you.
2. Ask a direct question, and most of the time you get a paragraph of hedging before the actual point.
3. One instruction, pasted once into the chat, stops it cold.
4. Answer first, in one sentence. Then explain, only if I ask. Skip caveats unless they change the answer.
5. Same question, before the paste: headers, a whole breakdown, before the actual advice.
6. After the paste: two words. "JavaScript first." Nothing else, unless you ask for more.
7. It's not a setting. It's just what you tell the AI.
8. The exact setup's in the link in bio.
9. Follow for the setup that actually works.

## On-screen text cues

- Hook: "AI chats love <box>padding the answer</box><br>before they actually answer you."
- Lede: "Ask a direct question,<br>get a paragraph of<br><strong>hedging</strong> first."
- Lede: "One instruction,<br>pasted once,<br>stops it <strong>cold</strong>."
- Artifact card (the exact paste, shown in full, monospace/terminal styling matching past termbox treatment): "Answer first, in one sentence. Then explain, only if I ask. Skip caveats unless they change the answer."
- Before/after comparison card — **the real captured text**, condensed to fit:
  - "BEFORE" panel: "My recommended order... 1. JavaScript → TypeScript... 2. Python... My vote: JavaScript/TypeScript first. 🚀" (styled as a long, cluttered block — visually communicates "too much")
  - "AFTER" panel: "JavaScript first." (styled as a single clean line — visually communicates "direct")
- Lede: "It's not a setting.<br>It's just what<br>you tell the AI."
- Biocard: link in bio
- Outro (locked): "Follow for the setup that actually works."

## Music

Mood: pick one not used in episodes 28/29 (drive / tense) — use "punchy" (
`trending-vibe--alexmorgan.mp3`) for a snappier, less tense feel matching this episode's
lighter/faster tone (a productivity trick, not a warning about a failure mode).

## Design

Palette: pick two colors distinct from episode 29 (#2ED573/#FF4757). Suggest a
neutral/blue productivity palette — not green/red (which episode 29 already used for a
success/failure metaphor this episode doesn't need).

## Setup guide

Exact steps: open any AI chat (ChatGPT, Claude, or Gemini), paste the instruction once
into the message box, continue the conversation as normal — no settings, no account
changes, works for the rest of that conversation.

## Caption / YouTube text (draft)

> AI chats love padding the answer before they actually answer you. Ask a direct
> question and you often get a paragraph of hedging before the actual point.
>
> One instruction, pasted once into the chat, stops it: "Answer first, in one sentence.
> Then explain, only if I ask. Skip caveats unless they change the answer."
>
> Same real question, before the paste: a whole breakdown before the actual advice.
> After the paste: two words. That's it.
>
> It's not a setting. It's just what you tell the AI — works the same in any chat.
>
> Full setup: actually-works.com/e/30
>
> Follow for the setup that actually works.
>
> #chatgpt #aitools #promptengineering #productivity #aiforbeginners
