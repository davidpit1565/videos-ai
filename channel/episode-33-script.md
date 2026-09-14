# Episode 33 — script, ready to produce

## Topic
n8n's AI Agent node ships with `contextWindowLength` defaulted to 5 — the agent
only re-reads the last 5 exchanges on every message. Verified live (13.9.2026)
against current n8n community docs and setup guides: this is n8n's real,
current default, not a stale or deprecated behavior. A customer-facing agent
built on the default forgets what was said a few messages back and reads as
broken, not smart — a real, checkable business risk, not an invented one.

## Why this topic, why now
- Highest measured demand cluster in `channel/demand-report.md`: "n8n ai agent
  tutorial" (233k median) and "build ai agent no code" — the channel's two
  strongest performers (episode 2, episode 7) both sit on this exact cluster.
- Not yet covered from this angle. Episodes 7, 25, and 32 are all about n8n
  error-handling/reliability (agent doesn't know it's wrong, retry duplicates,
  silent failure). This is memory/context — a different mechanism entirely,
  so it doesn't repeat an already-used angle on the same topic.

## Hook rules check (against `channel/hooks-guide.md`)
- **Type rotation**: episode 32 was Expert/Authority. This one is
  **You-Focused Appeal** combined with **The Specific Number** (5) — a
  different structural type, not a repeat.
- **Cold-read test**: "Nothing's wrong with your n8n AI agent. It's forgetting
  on purpose — every 5 messages." Clear in one pass, checkable claim (the
  number 5) lands in the first two sentences, no vague referent. (Reworded
  14.9.2026 — the original "Your n8n AI agent isn't broken" opened with a
  monosyllabic first word that the voice failed on across three different
  seeds; this keeps the same claim with a first word the voice handles.)
- **Emotional register**: real, checkable stake — a customer-facing agent
  that appears to forget mid-conversation reads as broken to whoever is
  talking to it. Not fabricated: this is the literal, documented default
  behavior, not an exaggerated worst case.

## Narration (8 lines)
1. Nothing's wrong with your n8n AI agent. It's forgetting on purpose — every 5 messages.
2. That number, 5, is the Agent node's default memory window. No one sets it — it just ships that way.
3. Ask it a question. Follow up six messages later, and it has no idea what you're talking about.
4. To whoever's talking to it, that looks like your bot forgot the conversation two seconds in.
5. The fix: raise the context window — 20 to 50 exchanges covers a normal conversation.
6. And if you're running queue mode, Simple Memory doesn't even survive across workers — switch to Postgres or Redis memory instead.
7. The exact setup's in the link in bio.
8. Follow for the setup that actually works.

## Verification notes
- `contextWindowLength` default of 5 and the "sliding window on replay, not on
  storage" behavior confirmed live via search against current (2026) n8n
  setup guides — not from memory or an old episode's assumptions.
- Queue-mode + Simple Memory not surviving across workers, and Postgres/Redis
  as the persistent alternatives, confirmed the same way.
- Nothing here is n8n's own marketing claim being repeated uncritically — it's
  a real, current default setting with a real, checkable consequence.
