# Episode 26 — script, ready to produce once D-ID is connected

**Status:** written and verified, not yet built. Blocked only on D-ID account + API key
(`HF_API_KEY`-equivalent for D-ID) and a portrait photo — both on David's list. Everything
else below is ready to hand to `export/produce.sh`-equivalent for the avatar pipeline the
moment those two exist.

## Why this topic, not picked fresh

Per the standing rule (episode 25 on): topic comes from measured demand, not a fresh guess.
`channel/demand-report.md`'s newest row (added 6.9.2026, prompted by a real reel David found):
**"local ai model tutorial" — median 263,293 views, 90th percentile 1,121,719** — higher than
n8n's own 233,070, which is the strongest number in the whole report. Three narrower queries
around the same idea ("run ai offline no internet," "offline ai agent," "meta ai model local")
came back far weaker (13K-52K median), so the real demand is on **running a model locally in
general** (Ollama, LM Studio, etc.), not one vendor's specific release — that's the angle
below, not a single product's name.

## Product verification (done 6.9.2026, before writing a line of script)

Verified live, not from memory — Ollama:
- Real, actively maintained: GitHub `ollama/ollama`, ~180k stars, latest release v0.33.3
  (2.9.2026), frequent point releases through August 2026.
- Install is still a single command: `curl -fsSL https://ollama.com/install.sh | sh`
  (Mac/Linux) or `powershell -c "irm https://ollama.com/install.ps1 | iex"` (Windows).
- Fully offline, no account needed for local use: `ollama pull llama3` then `ollama run llama3`
  works with WiFi off. Llama 3, Mistral, Gemma 2, Phi-3 all still supported.
- Hardware floor: a 16GB-RAM laptop with **no dedicated GPU** can run a 7B-class model at
  usable speed (~10-25 tok/sec on CPU in benchmarks found) — ASSUMPTION-flagged: the exact
  16GB figure is extrapolated from 8GB-class benchmarks, not a direct 16GB measurement, so
  don't put a specific tok/sec number on screen as fact.
- One disclosure to include: Ollama added optional **paid cloud tiers** in 2026 for
  cloud-hosted inference — opt-in, separate from local use. The episode's claim ("free,
  offline") is about local use specifically, not Ollama's whole product line — say that
  explicitly so it isn't a false-by-omission claim.
- Re-verify all of the above if this episode ships more than ~2 months after 6.9.2026 —
  this space moves fast (same caution that caught the ChatGPT agent mode name change
  before episode 18).

## Hook — type check against `hooks-guide.md`

Recent log: 22 You-Focused Question, 23 Expert/Authority, 24 Contrarian Open, 25
Shock/Surprise ("...can do the exact same thing twice"). **Picking Product/Outcome
Showcase for 26** — not used since episodes 18-19, and it's the natural fit for a real,
demonstrable claim.

Passes the dry-sentence + concrete-fact tests (per `hooks-guide.md`, 4.9.2026 addition):
states something specific, checkable, already true — not a hypothetical.

> **"This is a real AI model. My WiFi is off."**

(Spoken over a shot of turning WiFi off, or an on-screen airplane-mode toggle — the avatar
delivers the line to camera, cut to the WiFi-off moment as a quick insert if a screen/phone
cutaway is available; if not, the line still stands alone as a concrete, checkable claim.)

## Full narration (target ~50-60s at natural pace)

1. **(0-4s, hook)** "This is a real AI model. My WiFi is off."
2. **(4-9s)** "No account. No subscription. No API key. It's running right here, on this laptop."
3. **(9-16s)** "The tool is called Ollama — free, open source, and it's been downloaded enough that this isn't some obscure hack."
4. **(16-23s)** "One command installs it. One more command downloads a real model and runs it — fully offline, from that point on."
5. **(23-30s)** "You don't need a gaming PC for this. A normal laptop, no dedicated graphics card, runs a real model at a usable speed."
6. **(30-36s)** "What you get is a private assistant that never sends what you type anywhere — because there's nowhere for it to go."
7. **(36-42s)** "It's not going to out-argue the biggest paid models. But for a real, private, offline assistant — this is free, and it already works."
8. **(42-46s)** "The exact setup's in the link in bio."
9. **(46-49s, locked outro)** "Follow for the setup that actually works." *(use the canonical locked clip — `audio/voice/profile/canonical-lines.json` — same as every other episode, do not regenerate)*

## On-screen text cues (per line, word-by-word captions per the karaoke pipeline)

- Line 1: toolmark-style badge "WIFI: OFF" appears as the claim lands.
- Line 3: name-card "OLLAMA" + "free · open source" subline.
- Line 5: scoreboard-style contrast — "Gaming PC" [not needed, greyed] vs. "Normal laptop" [win, green] — matches the existing scoreboard component already used in episodes 22/25.
- Line 6: toolmark "100% LOCAL" or similar, echoing the biocard visual language already in use.
- Do **not** put a specific tok/sec number on screen — flagged ASSUMPTION above, not a
  confirmed measurement worth committing to a permanent on-screen claim.

## Shot plan for the avatar format specifically

Unlike episodes 1-25 (fully animated typography builds), this is the first script written
for D-ID: a talking-head clip generated from one portrait photo + this narration's audio.
Two real options once D-ID is connected, worth deciding before building:

1. **Pure avatar, no cutaways** — the D-ID clip runs the whole 46s, with the existing
   on-screen text/caption overlay system composited on top of it (same karaoke.py +
   safe-area rules apply — the avatar's face must stay clear of the on-screen text per
   `channel/motion-recipes.md`'s frame-layout rules, not just the usual background scene).
2. **Avatar for the hook + outro, real screen-recording insert for the middle** — record an
   actual terminal running `ollama run llama3` with WiFi visibly off, cut in during lines
   4-6. Stronger per the "Break the AI"/"AI vs. Reality" pattern shapes in
   `content-memory.md` (a real demo beats a claim), but needs an actual machine with Ollama
   installed to record — a real task, not just a script requirement.

Recommend option 2 if there's time to record the terminal demo; option 1 is the fallback
that needs nothing beyond the D-ID clip itself.

## Setup guide (draft — finalize once the actual build exists, per `check_setup_guide.py`'s requirement for real steps)

1. Open a terminal — Mac: Spotlight → "Terminal"; Windows: Start menu → "PowerShell".
2. Mac/Linux: paste `curl -fsSL https://ollama.com/install.sh | sh` and press Enter.
   Windows: paste `powershell -c "irm https://ollama.com/install.ps1 | iex"` instead.
3. When it finishes, type `ollama run llama3` and press Enter — this downloads the model
   the first time (needs internet once) and then starts a chat, fully offline from then on.
4. Optional, to prove it's offline: turn off WiFi, then run `ollama run llama3` again — it
   still works, because the model already lives on the machine.
5. Type a question directly in the terminal and press Enter to see it answer.
6. To leave the chat, type `/bye`.
7. To try a smaller/faster model instead: `ollama run phi3` (smaller, faster, less capable)
   or `ollama run gemma2` (a middle ground) — swap the model name, same two commands.

## Caption / YouTube text (draft)

Not finalized until the actual build ships (per `produce.sh`'s hard gate) — draft below,
same voice as episodes 22-25:

> This is a real AI model. My WiFi is off.
>
> No account. No subscription. No API key. It's called Ollama — free, open source, and it
> runs fully offline once it's installed. One command installs it, one more downloads a
> real model and runs it — no dedicated graphics card required.
>
> It won't out-argue the biggest paid models. But for a real, private, offline assistant,
> this already works, for free.
>
> Full setup, exact clicks: actually-works.com/e/26
>
> Follow for the setup that actually works.
>
> #ai #ollama #localai #privacy #opensource

## What's still blocked

- D-ID account + API key (David's list) — needed to actually generate the avatar clip.
- Portrait photo (David's list) — same blocker.
- If going with shot option 2: an actual machine with Ollama installed, to record a real
  terminal demo (WiFi off, `ollama run llama3` working) — this is real, not scripted.
- Once unblocked: submit the portrait + this narration's audio to D-ID (`submitTalkingHead`
  in `studio/lib/higgsfield.ts`'s sibling for D-ID, not yet written — needs a small
  `studio/lib/d-id.ts` following the same pattern, submit/poll split, before this can run
  through the studio instead of a one-off script).
