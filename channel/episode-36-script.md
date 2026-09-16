# Episode 36 — script draft (Experiment 1: Immediate Utility Replication)

**Status:** DRAFT — not yet run through `export/produce.sh` / `export/check.sh`. This file is the
script-writing step only; voice, render, and QA still need a real production session (needs
the audio/render toolchain, not available in this planning session).

This episode exists specifically to run Experiment 1, locked 8.9.2026 in `channel/experiments.md`.
Do not treat this as an ordinary slate pick — every constraint below (artifact shape, hook
type, duration, CTA) is set by that experiment's pre-registered design, not by this episode's
own judgment.

## Artifact chosen (confirmed with David, 16.9.2026)

A single, reusable prompt block that turns any AI chat (ChatGPT, Claude, Gemini — not
platform-specific) into a fact-checker for whatever text you paste under it. Chosen over two
other candidates (a bug-check-your-own-work prompt, a PDF-to-checklist prompt) because it
needs zero setup material — anyone can test it on a sentence they just typed, not just people
who happen to have a long document handy — which is the strictest read of Experiment 1's
"near-zero prerequisite knowledge" requirement.

Checked against Experiment 1's four low-friction conditions:
- **One single action:** paste the block, paste your text under it, send.
- **Near-zero prerequisite knowledge:** no login beyond a normal free account, no settings
  screen, no concept the viewer needs to already know.
- **Immediate, visible payoff:** the reply visibly marks each claim ✅ / ⚠️ / ❌ in the same
  message — provable on screen, not asserted.
- **Genuine save/share potential:** the kind of thing you'd actually forward to someone
  before they hit send on something wrong.

**Different underlying mechanism from episode 1** (ChatGPT's permanent Custom Instructions
settings field) — this is a one-off message pasted into any ongoing chat, not a saved setting,
and works identically across three platforms rather than one. That keeps the topic distinct
enough that a replication here answers "does the utility mechanism generalize," not "did we
just re-run episode 1."

## Current-product verification (done 16.9.2026, live search — required before writing a line)

- ChatGPT's free tier (GPT-5.6 Luna, current default as of Sept 2026) has no message cap on
  everyday text chat and includes basic web search — the artifact works on the free tier, no
  paid plan needed for the setup guide to be honest about cost.
- Automatic multi-step agentic browsing is Plus-only (Agent Mode), but that's not what this
  artifact depends on — a single reply that reasons over pasted text does not require it.
- No named feature/product in this artifact could be "retired" the way "ChatGPT agent mode"
  was (episode 18's near-miss) — the artifact is a prompting technique, not a named product
  feature, which lowers (not eliminates) staleness risk. Still re-verify the free-tier claim
  above if this episode ships more than a few weeks after 16.9.2026.
- Sources: morphllm.com, tech-insider.org, techrepublic.com (free-tier/model-default figures,
  September 2026 — see chat log for full list if needed for the episode's own "Verified"
  citation line).

## Hook

**Hook type:** Direct Address / Question — rotated off episode 35's Shock/Surprise (and
episode 34's, since 35 was never logged — see hooks-guide.md update below). Last used at
episode 31, so it's had five episodes off.

**Line:** "Before you send that text, paste it here first."

Dry-sentence test: this is an imperative pointing at something real and immediately doable —
not a hypothetical ("would you even know"). It creates pull (a small, specific pre-send ritual
the viewer can picture doing themselves right now), not just information.

## Narration (draft — durations are estimates, real timing comes from `build_voice.py` +
`retime.py`, per the picture-follows-narration rule)

1. **(0–3s) Hook:** "Before you send that text, paste it here first."
2. **(3–10s) Setup:** "Not a new app. One block of text you paste into any AI chat you
   already use — ChatGPT, Claude, Gemini, doesn't matter which."
3. **(10–20s) Show the artifact on screen:** "It reads whatever you paste under it and marks
   every claim: verified, unverified, or wrong — right there, in the same reply."
4. **(20–35s) Live demo beat:** paste a real sentence with one true claim and one shaky one
   (e.g. a stat from an old episode's own script, so it's genuinely checkable on screen — pick
   the actual line when this goes to production, don't invent one now) → show the model's real,
   unedited reply flagging the shaky one.
5. **(35–45s) Honest limit:** "It won't catch everything — treat a ⚠️ as 'go look this up
   yourself,' not as proof either way." (Channel's testing ethos — never oversell the artifact.)
6. **(45–50s) CTA:** "Follow for the setup that actually works." — **use the already-locked
   canonical clip** for this exact line (`audio/voice/profile/canonical-lines.json`), don't
   regenerate it.

Target total: ~48–55s, inside the 45–75s rule and comfortably over the 30s floor.

## The artifact itself (what goes on screen, and in the /e/36 setup guide)

```
Fact-check everything in the text below. For each claim: mark it
✅ verified, ⚠️ unverified / no source you can find, or ❌ contradicted
by evidence you can find. Don't soften an uncertain claim — flag it
plainly, and say exactly what you'd need to check to confirm the ones
you can't verify yourself.

[paste your text here]
```

## Setup guide steps (draft, for `studio/lib/articles.ts` once production starts —
not added to the file yet, per `explain-steps`: boring path, interface labels in both
languages, optional steps marked)

1. Open ChatGPT, Claude, or Gemini in a browser or the app (any of the three works the same
   way) — free account is enough, no paid plan needed.
2. Copy the exact prompt block above.
3. Paste it into a new message, then paste the text you actually want checked directly
   underneath it, in the same message.
4. Send it and read the reply — each claim comes back marked ✅ / ⚠️ / ❌.
5. Treat a ⚠️ or ❌ as "go verify this yourself before you send/publish it," not as a final
   verdict — the model can be wrong too.
6. (Optional) Save the prompt block itself somewhere reusable (a notes app, a text expander)
   so it's one paste instead of retyping it each time.

## Experiment bookkeeping

- This is Experiment 1 from `channel/experiments.md`, now assigned to **episode 36**.
- Held constant per the experiment's own lock: hook type is new (Direct Address/Question, not
  reused two episodes running), duration ~45–55s, CTA is the standard locked line.
- **Do not revise Experiment 1's Win/Strong win/Inconclusive/Lose thresholds** — those stay as
  locked 8.9.2026. This file only records which episode number/date carries out the test.
- Measurement: no earlier than 7 days after publish, against the studio's real save-rate,
  share count, and reach — never against a guess.

## What's still needed before this can actually ship

1. Pick the real on-screen demo sentence (one true + one shaky claim) — should be something
   genuinely checkable on camera, not fabricated for the demo.
2. Run `python3 audio/script_lint.py --cues <build>` once the build exists.
3. Build the HTML per `video/reel-template.html`, run `export/produce.sh`.
4. Full `export/check.sh` gate, watched twice per the episode-25-on standing rule, before it
   goes to David for approval.
5. Add the real `studio/lib/articles.ts` entry (steps above, adjusted to match whatever demo
   sentence gets used) — required by `export/check_setup_guide.py` before shipping.

None of this has been run yet. This file is the script/plan only.
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

## Narration (7 lines — cut from 8, then one restored, see "Density fix" and "Length fix" below)
1. Every private thing you've ever typed into ChatGPT trains its next model — and that's the default.
2. It's not just chat history. The files you upload and the replies you get back become training data too.
3. Switch it off, and future conversations stay out of training for good.
4. There's a separate mode that skips training and history every time, with nothing left to keep track of.
5. It takes ten seconds, once, to switch on.
6. The setup's in the link in bio.
7. Follow for the setup that actually works.

**Still cut entirely from spoken narration (moved to caption + `/e/36` setup guide only):**
"But it only protects what happens after — nothing you already sent ever gets pulled
back out" (the non-retroactive caveat). True and documented in the caption/setup guide
for a viewer who wants the full picture — it's a limiting caveat, not an action, and
doesn't earn its place back in the spoken track the way the Temporary Chat mode did
(see "Length fix" below for why that one line came back).

(Lines 2, 3, 5, 6 were reworded once against `audio/script_lint.py`'s flags before any
voice generation — "answers," "turn," "completely," "single," and "remember" all carry
endings this voice measurably swallows; reworded around them per this repo's own
"swapping the word costs nothing" rule, not respelled.

Second round, first production attempt: the gate flagged "everything" in line 3 as
rushed/clipped — 0.090s/syllable, well under the 0.100s floor, "likely swallowed."
Same known failure class as episode 35's line 6/4 swallows: `build_voice.py`'s own
per-line speed-up correction (this line sped up x1.12) compresses word durations
further than the raw take. Fixed the same way episode 35's notes prescribe — shortened
the line rather than re-rolling seeds: "Switch it off, and everything you type after
that stays out of training for good" → "Switch it off, and every new conversation
stays out of training for good," removing the flagged word entirely and cutting the
line's length so it needs less speed correction in the first place.)

(Lines 5-6 are the locked, pre-approved outro clips — see
`audio/voice/profile/canonical-lines.json` — used byte-for-byte, no regeneration.)

## Density fix, after David's real feedback on the first shipped cut (16.9.2026)

He watched the shipped file and said directly: he had to really concentrate to follow
it, it didn't flow smoothly, and it didn't pull him toward watching to the end — despite
every line individually being jargon-free per the simplicity check above. Root cause,
once actually counted rather than assumed: the 8-line version packed **six distinct
ideas** into 38 seconds (the training claim, files/replies included, the toggle, a
non-retroactive caveat, a wholly separate Temporary Chat mode, and the CTA). Plain
vocabulary was never the same thing as low cognitive load — this channel's own real
top performers (episode 2, episode 1) state exactly **one** claim and stop. Fixed by
cutting the caveat and the Temporary Chat mode out of the spoken track entirely (kept in
the caption/setup guide), down to four ideas: stakes → mechanism → one fix → one action.
Full reasoning and the new standing rule this creates are logged in
`content-memory.md`'s 16.9.2026 "Episode 36" entry — check idea count, not just
vocabulary, before shipping the next one.

## Third swallowed-word round (16.9.2026)

Re-running after the density/music fixes hit the same failure class a third time —
"every" in the (re-timed) line 3 flagged rushed/clipped at 0.080s/syllable. Same fix
pattern as before: shortened/reworded rather than re-rolling seeds — "Switch it off, and
every new conversation stays out of training for good" → "Switch it off, and future
conversations stay out of training for good" (also a small clarity win: "future"
signals the not-retroactive point implicitly, without needing the cut caveat line).

## Fourth swallowed-word round (16.9.2026)

"takes" in line 4 flagged rushed/clipped (0.090s/syllable) on the third rebuild, on a
line that hadn't changed text and was sped up x1.20 — likely alignment jitter right at
the 0.100s threshold rather than a real change, but treated the same way regardless per
this repo's discipline (don't chase seeds, shorten instead): "It takes about ten
seconds, one time, to switch on" → "It takes ten seconds, once, to switch on" — drops
"about" and shortens "one time" to "once," meaningfully cutting syllable count so the
line needs less speed correction.

## Length fix — cutting density undershot the channel's own minimum (16.9.2026)

The 6-line, 4-idea version rendered at **25.5 seconds** — `qa.py` flagged it as outside
the 30-90s band, and `CLAUDE.md`'s own standing rule is explicit: "Do not go under
30s" (per Buffer's 1.1M-video study and Socialinsider's 11M-post set, both cited there).
Cutting two ideas for density fixed the concentration problem but overshot into a real,
separate length violation. Fixed by restoring **one** of the two cut ideas — the
Temporary Chat mode, not the non-retroactive caveat — since it's an actionable
alternative a viewer can actually use, not a limiting caveat that mostly adds a "but."
Back to 5 ideas (stakes → mechanism → fix → alternative → action) instead of 4 or the
original 6 — a real middle point between "too dense to follow" and "too short to meet
the channel's own format standard," not a return to the original problem.

He also said the background music sat "a bit too high, even though it's subtle."
Root-caused against `render.sh`/`qa.py`, not guessed: the shipped file measured 8.6dB
separation (bed under voice) — technically inside `qa.py`'s pass range (6-26dB) and
close to episode 34's approved 8.7-9.1dB, but episode 36 used a different, punchier
track (`trending-vibe--alexmorgan.mp3`, mood `punchy`) than episode 34's smoother bed.
**New finding: the same measured dB separation does not read as equally present across
different music tracks** — a percussive/rhythmic track likely masks speech more at an
identical measured level. Fixed by lowering `MUSIC_VOL` specifically for this re-render
(see the production log below for the exact value used) rather than changing the
global default off one data point on one track.

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
