# Episode 21 — "Your ChatGPT can already leave the chat box"

**Format:** 45s reel (this is the one requested — full YouTube cut can follow later)
**Topic:** ChatGPT Agent Mode — from `channel/next-episode-ideas.md` idea #2.
**Why this one, now:** measured, not guessed.

- **Demand is real and the space is open.** `channel/demand-report.md`: "chatgpt agent mode"
  median 32,128 views, but the strongest video in the topic is only 183,738 — every other
  measured topic's leader is 1M+. Nobody has made the big video here yet.
- **The hook pattern that already worked for us.** Looked at the real view counts across our
  last 9 reels (screenshot he sent, 26.8): the top two by far are the ones that (a) name a tool
  everyone already knows — "ChatGPT," not "n8n" or "agent" — and (b) frame a test or a reveal in
  one plain sentence, not a claim. *"Your ChatGPT keeps giving you the obvious"* — 654 views.
  *"The test that settles it: Can't act without you? It's a chatbot"* — 923 views, our best. The
  weakest — *"Last time: a check said it passed. It lied"* — needed context from a prior video to
  even make sense: 114 views. This episode's hook is built from what actually worked, not from
  what sounds clever to someone who already knows the tools.
- **Zero jargon, on purpose.** He flagged directly that recent scripts read as written for people
  who already understand AI. Nothing here — "agent," "prompt," "automation" — needed. "ChatGPT
  can click things now" is the whole idea, and it's true whether the viewer has opened ChatGPT
  once or every day.

**Not fabricated:** no view-count promise is made anywhere in this file. What follows is the
best version of the reel that real data can justify — a topic with open competitive space, a
hook built from our own two highest performers, and language a non-technical viewer follows in
one pass. Whether it clears 15,000 or 100,000 views is not something any script can guarantee,
and this doesn't claim to.

---

## The premise

Almost everyone who has used ChatGPT has only ever done one thing with it: type a question,
read an answer. Most don't know it can also do something — open a real page, click a real
button, fill in a real form — while you wait, the same way a person would. That gap between
"everyone knows the name" and "almost nobody knows the feature" is the entire hook.

## The one small thing shown on screen

One real, small, finished task — booking or checking something on an actual site — done start
to end inside ChatGPT with Agent Mode turned on, so the viewer watches it happen rather than
being told it can.

## Narration (reel cut, ~45s, plain language throughout)

1. **(0.0–3.2)** "You've used ChatGPT a hundred times. You've never actually seen this."
2. **(3.4–7.0)** "This isn't ChatGPT answering you. This is ChatGPT doing something — by itself."
3. **(7.2–11.0)** "It opens a real page. It clicks the real button. You just watch."
4. **(11.2–15.5)** "No code. No app to install. It's already inside ChatGPT, turned off by default."
5. **(15.7–19.5)** "Here's exactly where to turn it on, and what to type first."
6. **(19.7–24.0)** [on-screen demo: Settings → the feature → one plain-English instruction typed]
7. **(24.2–28.5)** [demo continues: the task finishing itself on screen, real result visible]
8. **(28.7–32.5)** "That's it. That's the whole trick nobody tells you about."
9. **(32.7–36.0)** "It won't do anything you didn't ask it to. It still needs you to say what."
10. **(36.2–39.5)** "The setup's in the link in bio."
11. **(39.7–43.0)** "Follow for the ChatGPT features you didn't know you had."

Lines 6–7 are the real screen-recorded demo, not narrated text over a mock UI — matches the
channel's own rule (`CLAUDE.md`: "the picture follows the narration"), and Line 9 keeps the
channel's standing promise: say what it will not do, in the same reel as the hook, not buried.

## What happens next (not done yet, said plainly, not silently skipped)

This file is the script only. Building the actual reel from here needs, in order:

1. `python3 audio/script_lint.py --cues <build>` once the HTML build exists, before narration.
2. Real narration in his own cloned voice — `audio/build_voice.py --lines <this file's lines>
   --out ep21-vo.wav` — not yet run. This sandbox has `chatterbox`/`torch` available but no GPU
   (`nvidia-smi` not found), so a run here would be slow; worth doing on his machine or a GPU
   session if that matters for turnaround.
3. The actual demo screen-recording for lines 6–7 — needs a real ChatGPT Agent Mode session,
   which only he can do (an account action, same category as the Instagram publish button).
4. Build the HTML scene file once the audio exists, `export/retime.py` to match real timings,
   then `export/render.sh` per the standard pipeline.
5. Full `export/check.sh` gate before it goes anywhere near him for approval — voice_doctor,
   safe_check.js, qa.py, same as every other reel. Nothing skips this because the topic tested
   well on paper.

**Not claimed:** that this is rendered, tested, or ready to post. It is the script and the
reasoning behind every line in it — the part that was actually possible to finish in this
session without either a real ChatGPT Agent Mode demo (his account) or a long unattended
CPU voice-synthesis run.
