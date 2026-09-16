# Episode 36 — script, ready to produce

## Topic
ChatGPT uses your conversations — including files you upload and the answers it gives
back — to train future versions of its models, by default, for Free/Plus/Pro accounts.
Verified live (16.9.2026) against OpenAI's own Help Center article ("How your data is
used to improve model performance," help.openai.com) and OpenAI's own article on keeping
history on while disabling training: the toggle lives at Settings → Data Controls →
"Improve the model for everyone." Turning it off stops future conversations from being
used for training — but it does **not** retroactively remove anything already used; once
a conversation has entered the training pipeline, that toggle can't pull it back out.
Separately, "Temporary Chat" is a mode that never enters chat history and is never used
for training in the first place, no setting to remember — off by default, on a per-chat
basis. Business plans and Temporary Chats already have training off by default; this
episode is about the two consumer settings (Free/Plus/Pro) most people have never opened.

## Why this topic, why now
- **Direct response to the reach-first pivot (16.9.2026), not a demand-report pick.**
  David stated the goal explicitly: maximum virality — followers, views, likes — over
  topic-demand or funnel-fit. `channel/demand-report.md` does not cover this topic (it's
  YouTube search-demand for n8n/agents/local-AI/Claude Code, not ChatGPT privacy) — this
  episode is a deliberate exception to the "pick from demand-report" rule, made explicit
  here rather than silently skipping the standing process.
- **Matches the new personal-stakes/plain-language standing rule directly**
  (`hooks-guide.md`'s 16.9.2026 entry, from Roni Michaeli's reference-account example and
  his episode-32 feedback): this is a personal-benefit, secret-reveal topic in plain
  consumer language — "your own conversations, used without you knowing" — zero developer
  jargon, understandable to someone who has never used an automation tool in their life.
  The opposite end of the spectrum from "n8n never tells you when a workflow dies."
- **Checked against our own real data, not just Roni's opinion:** the verified per-post
  Instagram export (`content-memory.md`'s Master performance table) shows this channel's
  actual top performers by real engagement are general, jargon-free, personally-relevant
  claims (ep1, ep13, ep10, ep3) — this topic fits that exact shape, not the n8n-specific
  shape that measured mid-to-low on the same table.

## Hook rules check (against `channel/hooks-guide.md`)
- **Type rotation**: 32 Expert/Authority, 33 You-Focused Appeal + Specific Number,
  34 Shock/Surprise, 35 Contrarian Open. This one is **You-Focused Appeal**
  ("everything you've ever typed") — last used episode 33, not back-to-back, and it's
  the type this channel's own research ties most directly to personal stakes.
- **Personal-stakes/plain-language check (16.9.2026 standing rule):** hook names no
  developer tool, no jargon — "trains," "typed into ChatGPT," "the default" are all
  plain consumer language. Matches Roni's reference-account examples structurally
  ("ChatGPT can find your leaked passwords" — personal stakes, secret framing, plain
  language).
- **Stakes-escalation pass (16.9.2026, per the @rpn reference-creator formula logged in
  `hooks-guide.md`):** first draft was "ChatGPT trains itself on everything you've ever
  typed to it" — accurate but flat, describing the mechanism rather than the stake.
  Reworded to lead with "every **private** thing" — the same underlying fact (ChatGPT
  trains on your input by default), but naming the actual stake (privacy, something
  specific and personal) instead of the neutral word "everything." Nothing invented or
  exaggerated: the setting genuinely applies to every conversation regardless of
  content, so "private" is accurate, not embellished.
- **Cold-read test**: one clause, a real and checkable claim (this AI trains on your own
  conversations, on by default), no vague referent, nothing hypothetical — this is
  current, real, default behavior, verified against OpenAI's own documentation.
- **Specific claim in the first clause**: the surprising part ("and that's the default")
  is in the same sentence as the setup, not deferred.
- **Emotional register**: privacy/personal-stakes, closer to the Fear end of the
  register research already logged in `hooks-guide.md` (13.9.2026 entry) than to neutral
  curiosity — real stake (your own private words being used to train a product), not an
  invented worst case.

## Narration (8 lines)
1. Every private thing you've ever typed into ChatGPT trains its next model — and that's the default.
2. It's not just chat history. The files you upload and the replies you get back become training data too.
3. Switch it off, and everything you type after that stays out of training for good.
4. But it only protects what happens after. Nothing you already sent ever gets pulled back out.
5. There's a separate mode that skips training and history every time, with nothing left to keep track of.
6. It takes about ten seconds, one time, to switch on.
7. The setup's in the link in bio.
8. Follow for the setup that actually works.

(Lines 2, 3, 5, 6 were reworded once against `audio/script_lint.py`'s flags before any
voice generation — "answers," "turn," "completely," "single," and "remember" all carry
endings this voice measurably swallows; reworded around them per this repo's own
"swapping the word costs nothing" rule, not respelled.)

(Lines 7-8 are the locked, pre-approved outro clips — see
`audio/voice/profile/canonical-lines.json` — used byte-for-byte, no regeneration.)

## Simplicity check (per hooks-guide.md's standing rule)
Reread for a viewer with zero AI-tool background: "trains itself," "everything you've
typed," "chat history," "files you upload," "turn it off," "ten seconds" — no product
internals (no "Data Controls," no "Improve the model for everyone," no "Temporary Chat"
spoken aloud). Those exact setting names are introduced only visually, on screen, and in
the setup guide — never spoken, same discipline episode 35 used for "webhook"/"node."

## Verification notes
- "Improve the model for everyone" toggle, its location (Settings → Data Controls), and
  its non-retroactive behavior confirmed live against OpenAI's own Help Center:
  [help.openai.com/en/articles/5722486](https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance)
  and [help.openai.com/en/articles/8983130](https://help.openai.com/en/articles/8983130-what-if-i-want-to-keep-my-history-on-but-disable-model-training).
  Default-on state for Free/Plus/Pro, default-off for Temporary Chats and Business plans,
  confirmed the same way, cross-checked against techradar.com's coverage of the same
  setting for a second, independent confirmation.
- Temporary Chat's behavior (no history, no training, per-chat, off by default) confirmed
  against the same OpenAI Help Center source. Not claimed: Temporary Chat's own 30-day
  server-side safety-monitoring retention window (real, per OpenAI's documentation, but a
  separate detail not load-bearing for this episode's claim and left out of the narration
  to avoid overloading a 45-60s script with a second caveat).
