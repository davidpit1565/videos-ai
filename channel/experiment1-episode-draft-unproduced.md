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
