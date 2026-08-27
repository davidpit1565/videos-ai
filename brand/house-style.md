# House Style — "Brass on Ink"

The reusable visual identity for every video on this channel. The point of a house style is
recognition: someone should be able to tell one of your videos from a thumbnail, a three-second
scroll, or a single frame — before they read a word.

Rename the brand mark to your channel name; everything else is built to stay fixed.

---

## 1. The idea behind the look

Two materials, and only two.

**Ink** — a deep, slightly blue-biased near-black. This is the machine: the interface, the
system, the thing being explained.

**Brass** — a warm, aged gold. This is *you*: the instruction, the insight, the human decision
laid over the machine. Brass never decorates. It only ever marks the thing the viewer is
supposed to take away.

That rule is the whole identity. If everything is brass, nothing is. One brass element per
frame, two at the absolute most.

---

## 2. Palette

| Token | Hex | Used for |
|---|---|---|
| `ink` | `#0E1116` | Background. Every frame. |
| `ink-2` | `#151A22` | Cards, panels, raised surfaces |
| `surface` | `#1B2029` | Inputs, secondary panels |
| `line` | `#2A313D` | Hairlines, borders, dividers |
| `brass` | `#E8C86A` | The takeaway. Labels, highlights, the one thing that matters |
| `brass-dim` | `#8A7434` | Section eyebrows, inactive brass |
| `steel` | `#6FA8CF` | The "other option" in any comparison |
| `clay` | `#C96A4E` | Limitations, warnings, honest caveats |
| `ok` | `#69B98B` | Confirmations, guarantees, ticks |
| `text` | `#EEF0F3` | Primary text |
| `muted` | `#8C97A8` | Secondary text |

Never introduce a sixth hue. If a frame needs another category, use a shape or a weight
difference, not a new colour.

---

## 3. Typography

| Role | Face | Treatment |
|---|---|---|
| Display / headlines | **Archivo** 700 | Tight tracking (−0.03em), max 3 lines, `text-wrap: balance` |
| Body / captions | **Assistant** 400/600 | Generous line height (1.45), never below 34px at 1080p |
| Labels / data / eyebrows | **IBM Plex Mono** 400 | UPPERCASE, letter-spacing 0.2em, always small |
| Mock interfaces | **Inter** | Only inside a simulated app UI — never for your own graphics |

That last row is the trick that makes screens read as real. Your graphics and the interface you
are demonstrating must never share a typeface. The moment a mock UI uses your display font, the
viewer reads it as a diagram instead of a screen.

---

## 4. Signature devices

Use these in every video. They're what makes the channel recognisable.

**The eyebrow rule.** Every section opens with a small monospace label preceded by a short
brass hairline: `——— 04 · WHERE IT GOES`. Always top-left. Always the same size.

**The index chip.** Top-right, monospace: `03 / 07`. Tells the viewer where they are in the
video without a progress bar.

**The brass wipe.** The only transition between sections: a 3px brass line sweeps across the
frame in 350ms and the new section is behind it. No dissolves, no slides, no zooms.

**Strike cards.** Whenever you say what something is *not*, show it as a card with the text
struck through in clay. Three at a time, never more.

**The takeaway line.** Every section ends on one full-frame sentence in Archivo 700 with
nothing else on screen. If a section doesn't have one, the section isn't finished.

---

## 5. Motion

- Elements enter by rising 24px and fading in over 500ms, ease-out cubic. Nothing else.
- Nothing bounces, spins, or scales on entry.
- Elements that are finished **leave** — a section should never accumulate more than about five
  live elements. Clearing the frame is what keeps the pace up.
- Cursor in screen recordings: enlarged 140%, soft brass glow, smoothed path, ripple on click.
- Respect `prefers-reduced-motion` in any web version.

---

## 6. Framing

| Format | Use | Rules |
|---|---|---|
| 16:9 · 1920×1080 | YouTube long-form | Captions bottom-centre. Safe area 6% |
| 9:16 · 1080×1920 | Instagram Reels, TikTok, Shorts | **Captions in the middle third, never the bottom** — the UI and thumbs cover the bottom 20%. Type ≥ 52px. Burn captions in; most viewers are muted |
| 1:1 | Feed posts | Single takeaway line, no UI |

Vertical is not a crop of horizontal. Reshoot the composition: one idea per frame, stacked, with
much bigger type.

---

## 7. Audio

- Voice: warm mid-range, conversational, ~160 wpm including pauses. Never announcer-voiced.
- Music: minimal ambient, −24 LUFS, ducking 6dB under narration. Starts on the first payoff,
  not on the first frame — silence under a cold open makes it land.
- One sound effect only: a soft, short tick for the brass wipe. Nothing else.

---

## 8. Thumbnails

- Ink background, one brass element, three to five words maximum in Archivo 700 at ≥120px.
- No face required, no arrows, no red circles.
- Test at 320px wide. If the words aren't readable, cut words — never shrink type.

---

## 9. What this style never does

- No purple-to-blue gradients. No glowing brains, no android faces, no circuit boards.
- No stock footage of people at laptops.
- No emoji as section markers.
- No more than two accent colours in a single frame.
- No claim the video can't back — see `assets/guaranteed-vs-model-behaviour.md`. The honesty
  section is part of the format, not a disclaimer bolted on the end.

---

## 10. What the script says

He watched episode 13 and did not understand it himself — someone who already knew what the
video was supposed to be about. The word that broke it was "column": said once, never defined,
assuming the viewer already knows what a spreadsheet column or a database field is. He was
explicit about the bar: written for someone with zero background on the topic, not a beginner
who at least knows the vocabulary — "even a child," his words, means don't assume ANY prior
knowledge, not "assume less."

This is not a one-time note on one script. It is a standing rule, checked on every script
before voice generation, the same way the safe-area check runs before every render:

- **One concrete thing carries the whole idea, all the way through.** Episode 13's rewrite
  uses "a box" — Instagram writes a number in the box, TikTok writes over it, no warning, you
  never know it happened. Never introduces the underlying real mechanism as a second, separate
  vocabulary — "box" is not a simplification of "shared field" that gets swapped in later, it
  IS the explanation, start to finish.
- **A technical word is either replaced or defined the instant it's said, never left standing
  on its own.** "Column," "field," "sync," "endpoint," "API," "webhook" — any word a working
  professional in the topic would use without a second thought is exactly the word a
  zero-background viewer stops on. If the real term has to appear (a tool name, a button
  label), it's introduced through the concrete thing, not before it.
- **Read it as the ten-year-old test, literally.** If a sentence needs the viewer to already
  know what the last sentence's jargon meant, the script isn't done — cut the word, not just
  slow down on it.
- **The structure a proven video uses is not optional flavor — measure it.** Before a script
  is called finished, check it against videos in the same topic that actually got real
  comments, likes and follows: not just their hook, but their sentence-by-sentence writing —
  what they say, what they deliberately don't say, and why. A hook can be perfect and the
  script can still lose the viewer one sentence later; the whole script gets the same scrutiny
  the hook already gets.

He asked directly for research into what the highest-performing AI-tools content on Instagram
and TikTok actually does — structure, wording, visual format, not just hooks. Real sourcing
found (creator interviews and case studies, not this channel's own guesses — see the research
agent's report for full citations):

- **Name the tool in the first sentence, not after a tease.** The creators with documented
  viral AI-tips videos (Maverick Maltin: "I always try to have the AI tool that I'm talking
  about in the actual hook") open with the concrete thing, never a curiosity gap that makes
  the viewer wait to find out what tool it even is.
- **Write the hook after the demo is built, not before.** Riley Brown (20M views on his first
  AI TikTok) films the whole walkthrough first and writes the opening line from what actually
  turned out interesting — the opposite of scripting the hook, then building content to match
  it.
- **A script that reads as AI-written is a failure mode, not a neutral choice.** Riley Brown's
  own words: "the more you use AI for writing your scripts, the more you're going to sound
  like AI... sounding like AI is suicide." Independent 2026 research backs this from the
  audience side: preference for visibly AI-generated creator content fell from 60% (2023) to
  26% (2025), and one surveyed heuristic was literally "if you do not make mistakes, people
  will suspect it is AI." A script needs a visible human judgment call somewhere in it — a
  stated limitation, a specific mistake avoided, an opinion — not just a clean list of
  benefits.
- **Screen-record the tool actually doing the thing, narrated live, as the primary visual
  mode.** Both documented viral cases did this, not talking-head-to-camera and not pure motion
  graphics. Matches what this channel already does (text-on-screen + voiceover over the real
  interface); the standing lesson is to keep leaning on the real screen, not drift toward
  more produced/animated visuals as a way to seem more polished.
- **Optimize for saves and shares, not raw watch time.** Instagram's 2026 ranking weights DM
  shares and saves above likes. The practical test for a script: would a viewer actually
  forward this to a colleague because it's a specific, usable thing — not because it was
  entertaining for 40 seconds.
