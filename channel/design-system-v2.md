# Design System V2 — four modes, one channel

**Status: prototype, not shipping infrastructure.** Built from the brief David and
ChatGPT worked out, together with a real look at `channel/used-designs.json`: every
episode so far has technically had "its own" brass/ember pair, but 44 of 52 episodes
land somewhere in red-orange-amber-gold. Different hex, same hue. That's the actual
problem this solves — not "we need a new color," but "we've been solving repetition
with a palette generator when the repetition is structural."

This document is the spec. `video/design-system-v2-playground.html` is the executable
proof — one file, four scenes, real motion, playable. **Neither ships an episode.**
David reacts to the playground first; a real episode only gets built on top of this
after that review.

---

## The core idea, once, at the top

**Color stops being mood and starts being signal.** The old system picked two hex
values per episode to *feel* like the topic (urgent = reds, neutral = blues) — that's
why the feed converges on warm colors even when every episode "chose" its own pair:
most tech content *feels* urgent, so most episodes pick from the same warm half of the
wheel. A signal-based palette doesn't pick a mood, it picks a **meaning**: cyan always
means "in progress," green always means "confirmed true," red always means "confirmed
false or dangerous," yellow always means "uncertain / needs a second look." The meaning
is fixed across every episode that uses it; only *how much of each* appears changes,
because that's driven by the actual test result, not a vibe.

This is the philosophy behind THE LAB most literally (its whole aesthetic is color-as-
state), but it's the fix for all four modes: BROADSHEET fixes color by using exactly
one signal color per episode instead of two mood colors; INSTRUCTION CARD fixes it by
letting paper/ink carry the frame and using one accent only where something actually
changed; THE INCIDENT fixes it hardest — red is rationed to a single true alert, which
is what makes it read as alarming at all. A palette that is always "on" stops meaning
anything. Four episodes with four different content-shapes will naturally spread
across four different visual textures — that's the actual fix for "the feed looks the
same," not a fifth color pair.

---

## Brand constants — hold across all four modes, no exceptions

1. **Same near-black background world.** `#050709` (body) / `#0A0E14` (`--ink`,
   frame/card background) stay the base in every mode. A mode can add its own accent
   system on top, but none of the four replaces the dark base with a light one as the
   *dominant* surface — INSTRUCTION CARD's "paper" is a warm off-white **card** floating
   on the same dark frame, not a light page.
2. **`Assistant` and `IBM Plex Mono` never leave.** Every mode may swap its *display*
   headline font, but body copy, captions, labels, metadata and citations stay on
   `Assistant` (humanist body warmth) and `IBM Plex Mono` (technical/label voice) in
   every single mode, including BROADSHEET where the headline goes serif. This is the
   single biggest thing that keeps four different aesthetics reading as one channel.
3. **The safe-area caption system is structurally identical everywhere.** Same box
   (x 65–1015, y 269–1248 on 1080×1920), same `.subs` element, same `.pad` padding
   contract (28cqw top / 65cqw bottom, matching the existing reel builds). Only the
   *styling* of `.subs` changes per mode (see each section below) — never its position,
   never the safe-area numbers. This is both brand recognition and a hard technical
   constraint: Instagram's own UI draws over anything placed further down.
4. **Every reel still shows real, sourced evidence.** A mode changes how evidence is
   *framed* — a citation card, an incident evidence-window, a before/after pair, a
   scoreboard — never whether it's real. None of these four modes is a license to stage
   a fake result for the sake of the aesthetic; "we actually tested this" is the brand
   promise all four serve.
5. **A consistent small episode marker, same position, every mode.** `EP. 53` in
   `IBM Plex Mono`, letter-spaced, sits inside the safe box near its top edge (`top:
   26cqw`, `left: 6.5cqw` — inside the box, not decorative, so it's a real, checked
   element in every build). Same position, weight and size regardless of mode.

---

## Mode 1 — THE LAB ("We tested it")

**Use when:** the episode's format is "we ran a test / experiment and measured what
happened" — the closest match to the existing `/e/N` "live test / escalate until it
breaks" format from episode 21 on.

### Typography
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@600;700;800&family=IBM+Plex+Mono:wght@500;600;700&family=Space+Grotesk:wght@600;700&display=swap">
```
- Display/headline: **Space Grotesk** 700 — a technical grotesk, not a warm humanist
  one; it should look like it belongs on an instrument panel, not a magazine.
- Body/lede: `Assistant` 700 (brand constant).
- Metadata/labels/captions: `IBM Plex Mono` 500/600 (brand constant, doing more work
  here than in any other mode).

### Color — semantic state map (the whole point of this mode)
```
--ink:        #0A0E14   (brand constant base)
--panel:      #0F1620   (slightly lifted panel surface, still near-black)
--line:       #1E2A38   (hairline borders on panels/boxes)
--text:       #E8F0F7
--muted:      #6B7C90

--state-idle:    #3A4656   (grey — not yet run)
--state-running: #22D3EE   (cyan — in progress, right now)
--state-pass:    #34D399   (green — confirmed true / worked)
--state-fail:    #F87171   (red — confirmed false / broke)
--state-warn:    #FBBF24   (yellow — uncertain, partial, needs a second look)
```
No `--brass`/`--ember` pair. Color is chosen **per state at render time**, driven by
what the test actually did, never fixed per-episode. A LAB episode that never fails
never shows red — that's correct, not a missed opportunity to "use the color."

### Grid / layout (inside the x 65–1015, y 269–1248 safe box)
- A persistent **metadata rail**: 2–3 stacked label/value rows pinned to the top of the
  safe box (`TEST / 04`, `MODEL / CLAUDE`, `STATUS / RUNNING`), each in Plex Mono,
  letter-spaced, value colored by its current state.
- Below it, a **status strip**: a thin horizontal bar that fills left-to-right like a
  progress bar while `STATUS` reads `RUNNING`, then locks solid in state color the
  instant the result is known.
- Center: the claim/result headline in Space Grotesk, boxed climax word colored by
  final state (not a fixed brass box).
- A **counter** (`ATTEMPT 1/5`, `CONFIDENCE 40%`) is allowed as a small mono readout
  under the headline — it's diagnostic, not decorative.

### Motion (from `motion-kit.js`, plus what's missing)
- `MK.animateWords` / `splitWordsSafe` for the headline — same word-by-word build as
  every mode, this is core infrastructure, not a per-mode choice.
- Status strip fill: reuse the exact math from `renderBars()` in `reel-52.html`
  (`vbarfill` width animated by `smoothIn(clamp01((t-at)/dur))`) — this is already a
  generic "animated bar" primitive, just re-skinned as a progress meter instead of a
  visibility comparison.
- State-lock "snap": reuse `.b`/`.b.on` for the value label itself, but the **color
  change** on lock (idle→running→pass/fail) is new — **not in `motion-kit.js` today**.
  Needed addition: `MK.lockState(el, stateClass, t, at)` — swaps a CSS class at time
  `at` (idle/running/pass/fail/warn) with a very short (80–120ms) flash-then-settle,
  not a slow fade, because a system "deciding" reads as instant, not gradual.
- `MK.impactShake` on the exact frame a result flips to FAIL — small, sharp, once. Do
  not use it on PASS (nothing shakes when something works).
- Scene transitions: a **hard cut with a brief scanline/glitch flicker** (2–3 frames of
  a thin white line sweeping down), not `zoomThroughTransition`'s soft push — a
  diagnostic system doesn't do cinematic camera moves between readouts. **New primitive
  needed**: `MK.scanlineCut(el, t, at, dur)` isn't in `motion-kit.js` yet; until it
  exists, the playground approximates it with a fast opacity cut plus a thin animated
  highlight bar borrowed from `buildHighlightBars`/`animateHighlightBars`.

### Captions
`.subs` styled like a lab transcript: monospace (`IBM Plex Mono`), left-aligned instead
of centered, prefixed with a small `>` marker per line, no brass pill highlight — the
spoken word gets a plain color change to `--state-running` cyan instead of a background
box, because a boxed highlight reads as "editorial," not "instrument readout."

### When to use this mode
Any episode whose whole premise is "we ran X and here's what happened" — reliability
tests, benchmark comparisons, "does it actually work" formats. If the episode has no
real test/result to show, this mode has nothing to do — don't reach for it just because
it looks technical.

---

## Mode 2 — THE BROADSHEET ("Something just changed")

**Use when:** the episode is reporting a genuine capability change or discovery — "AI
can now do X" — the news, not the test.

### Typography
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@600;700;800&family=IBM+Plex+Mono:wght@500;600&family=Instrument+Serif&display=swap">
```
- Display/headline: **Instrument Serif** (regular weight only — it has no bold cut,
  which is correct here: an editorial serif headline gets its authority from scale and
  the grid, not from boldness).
- Body/deck/subhead: `Assistant` 600/700 (brand constant) — the grotesk pairing the
  brief calls for.
- Section numbers, rules-labels, bylines: `IBM Plex Mono` (brand constant).

### Color
```
--ink:   #0A0E14   (brand constant base)
--paper: #F4EEE3   (near-ivory, used ONLY on small inset elements — never the full frame)
--rule:  #2A3340   (hairline horizontal rules on dark)
--rule-on-paper: #C9BFA8
--text:  #F6F1E8   (warm near-white, not pure #fff — this is what keeps it "editorial" and not "tech")
--muted: #8A94A3
--signal: <one color per episode, chosen from the episode's actual claim, not a mood>
```
Exactly **one** signal color per episode (e.g. `#3EC6FF` for an episode about a model
update, `#FF6B4A` for one about a shutdown/deprecation) — never a two-color pair. This
is the mode's actual color-repetition fix: one color rotates freely episode to episode
because there's only one slot to fill, instead of two slots both quietly drifting warm.

### Grid / layout
A **fixed editorial grid**, not floating centered cards:
- A numbered section marker (`01`, `02`) in Plex Mono, top-left of each beat, inside the
  safe box.
- A horizontal rule (`--rule`) directly under the section number, drawn full-width
  inside the safe box — this rule is a first-class animated element (see motion below),
  not a static divider.
- Headline sits left-aligned under the rule (not centered) — a real newspaper column
  starts at the margin, it doesn't center.
- A small side-note callout (a vertical rule + short annotation in Plex Mono, sitting to
  one side of the body text) stands in for a pull-quote — this is also where the
  caption's editorial-annotation styling gets its visual language from, so the caption
  bar doesn't feel bolted onto a different design system.

### Motion
- `MK.splitWordsSafe` + `MK.animateWords`, but the **entrance direction** is
  horizontal, not the vertical `translateY` rise every other mode uses — words (or the
  whole headline as one column) slide in from the right like a newspaper column being
  set, landing with `smoothIn`, never an overshoot. This is a genuine, deliberate
  divergence from the shared rise-in the other three modes use for their word-builds;
  it's the one place BROADSHEET's "words arrive like type being set" idea couldn't be
  expressed by reusing `animateWords`'s vertical rise unchanged, so the playground
  passes `riseY` as a horizontal offset applied via a light wrapper instead of touching
  `motion-kit.js`'s shared function.
- Horizontal rule extends via `MK.animateHighlightBars`'s exact math (`scaleX` from 0,
  `transform-origin: left`) — re-skinned from "highlight word" to "extend rule," same
  primitive, different element.
- Scene-to-scene transition is **typographic, not a camera move**: the rule for the
  outgoing section retracts (`scaleX` back to 0) while the next section's number and
  rule build in — this reuses `animateHighlightBars`'s reverse direction, no new
  primitive required, and deliberately does **not** use `zoomThroughTransition`. This is
  the one documented, intentional exception to the "reuse the shared transition"
  pattern in this whole system, because a camera-zoom hard-cut between magazine
  sections reads as a completely different medium than the sections themselves.

### Captions
`.subs` styled as an editorial annotation: smaller than the other three modes, set as a
labeled aside (a short vertical rule to the caption's left, like a printed margin note)
rather than a bold centered karaoke line. The spoken word is underlined (reusing the
per-word highlight bar primitive, thinned to a 2px underline) instead of boxed.

### When to use this mode
A real, verified capability change or discovery — new feature, new model behavior, a
retirement/deprecation. Not a test result (that's THE LAB) and not a how-to (that's
THE INSTRUCTION CARD).

---

## Mode 3 — THE INSTRUCTION CARD ("Do this")

**Use when:** the episode is a utility/setup walkthrough — the mode closest to what
`/e/N` setup-guide pages already promise, and the mode every episode from 21 on is
required to ship a setup path for regardless of which visual mode it uses.

### Typography
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@600;700;800&family=IBM+Plex+Mono:wght@500;600;700&family=Archivo:wght@800;900&display=swap">
```
- Display/step headline: **Archivo** 900 (the existing brand display font, kept here on
  purpose — this mode is the least "new," it's a disciplined version of the current
  system, not a reinvention).
- Body: `Assistant` (brand constant).
- Step index, field labels: `IBM Plex Mono` (brand constant) — carries almost all of
  this mode's "manual" feeling.

### Color
```
--ink:    #0A0E14   (brand constant base)
--paper:  #EDE6D8   (warm paper-toned card, floating on the dark base — never full-frame)
--ink-on-paper: #1B1B18
--rule:   #2A3340
--accent: <one accent per episode, e.g. #FFB020>
```
One accent color, used only for the step-index numerals and the single "changed" thing
in a before/after pair — everything else is paper/ink. The "paper+ink+one-accent feel
even on a dark background" from the brief means: the *card* is paper-colored, the
*frame around it* stays the dark brand base — never a full light-mode reel.

### Grid / layout
- A **persistent step-index** pinned to the same corner of the safe box across the
  whole episode (`01`, `02`, `03`... in accent color, Plex Mono) — viewers should be
  able to tell how far through the setup they are at a glance, the way a real numbered
  field guide works.
- Each step is a paper-toned card: a mono-labeled header (`01 PROBLEM`, `02 CHANGE`,
  `03 RESULT`) then the step's plain-language line in Archivo.
- No floating drop-shadowed cards spinning in — cards sit flat, square-cornered
  (`border-radius` near 0, a deliberate departure from the rounded cards every other
  mode uses), because a field guide page doesn't float.

### Motion
- **Before/after reveal, not zoom-through** — the brief is explicit here.
  `motion-kit.js` has no before/after wipe primitive today; the playground builds it as
  a straightforward clip-path wipe (`clip-path: inset(0 X% 0 0)` animated with
  `smoothIn`) driven by the same `t`/`at`/`dur` calling convention every other primitive
  uses, so it's a drop-in future addition to `motion-kit.js` (`MK.beforeAfterWipe(el,
  t, at, dur)`) rather than a one-off in the build file.
- Step cards enter with a plain, flat rise (`MK.animatePop`-style scale-in, no glow
  bloom — glow reads as dramatic, this mode is procedural) and the step index numeral
  advances with a hard cut, not a cross-fade, because a checklist number ticking over
  should feel discrete, not blended.
- Scene transition: the outgoing step card slides straight up and out (a plain
  `translateY` exit, reusing `smoothIn` timing) while the next slides up into place —
  this is the "boring path over the clever one" applied to motion itself, and it is a
  second deliberate departure from `zoomThroughTransition` for the same reason as
  BROADSHEET: a manual's pages turn, they don't zoom through the camera.

### Captions
`.subs` styled as a literal instruction line: same size and weight as the current
karaoke captions (brand recognition matters most here since this mode is closest to
what already ships), but the spoken word gets a small accent-colored checkmark-style
tick appended rather than a colored pill, reading as "step confirmed," not "word
emphasized."

### When to use this mode
Any setup/how-to/walkthrough episode — this is the mode `/e/N`'s existing setup-guide
requirement was already describing before this system existed; it should feel like the
natural visual home for that requirement, not a new obligation on top of it.

---

## Mode 4 — THE INCIDENT ("It broke")

**Use when:** the episode is a failure story — something an AI tool or workflow
actually got wrong, verified, not speculative.

### Typography
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@600;700;800&family=IBM+Plex+Mono:wght@500;600;700&family=Archivo:wght@800;900&display=swap">
```
- Display: **Archivo** 900 condensed feel achieved via negative letter-spacing and a
  narrow column width (no separate condensed font import needed — the brief calls for
  "mostly monospace/condensed grotesk," and Archivo already reads condensed at tight
  tracking, so this avoids adding a fifth font family to the system for one mode).
- The incident-number and all header-block fields: `IBM Plex Mono` (brand constant) —
  this mode leans on it harder than any mode except THE LAB.
- Body/annotations: `Assistant` (brand constant).

### Color
```
--ink:   #0A0E14   (brand constant base)
--panel: #10151C
--line:  #2A3340
--text:  #E8EDF3
--muted: #6B7280
--alert: #EF4444   (the ONLY red in the build — used once, meaningfully, never as a
                    background wash, never on more than one element at a time)
```
Red is rationed on purpose: most of the frame is near-monochrome grey/ink, and the one
`--alert` red appears exactly where the confirmed-bad fact is — a header field
(`STATUS: CONFIRMED`), a single annotation arrow, or the redaction-lift reveal. If red
is on screen constantly, an incident report stops reading as alarming; that's the same
"always-on color stops being a signal" principle as THE LAB, applied to a single color
instead of a four-way map.

### Grid / layout
- An **incident-report header block** at the top of the safe box: `INCIDENT 052`,
  then a row of field/value pairs (`STATUS: CONFIRMED`, `CAUSE: UNKNOWN`, `IMPACT: ...`)
  in Plex Mono — deliberately bureaucratic, not designed.
- **Asymmetric layout**: a giant incident number (oversized, cropped by the frame edge
  on one side) sits off to one side, with an "evidence window" (a bordered panel
  showing the actual failing output/screenshot, labeled `EVIDENCE`) placed
  asymmetrically opposite it — never centered, never symmetric, which is the clearest
  visual break from every other mode's centered composition.
- Annotation arrows/brackets point from the header block to the specific evidence they
  refer to — hand-drawn-feeling but still built from CSS (a rotated line + arrowhead),
  not an SVG asset.

### Motion
- **Redaction/reveal**: a row of solid black bars sits over the real result; the bars
  lift (translate up and off, staggered) to reveal the evidence underneath. This is the
  mode's signature beat and needs a genuinely new primitive:
  `MK.redactionLift(bars, t, startAt, dur, stagger)` — structurally identical to
  `animateHighlightBars` (an array of elements, staggered `smoothIn` progress) but
  driving a `translateY` lift-and-fade instead of a `scaleX` grow, so it can literally
  share `buildHighlightBars`' bar-generation geometry logic. **Not in `motion-kit.js`
  today; the playground implements it inline as the concrete spec for that future
  addition.**
- **Aggressive short-punch captions** get their own beat timing (see below) rather than
  new motion primitives — the punch comes from caption rhythm, not extra animation.
- Scene transition: a hard, unglamorous cut with a single `MK.impactShake` on cut —
  reusing the existing primitive, no new motion needed here, because the brief's
  "forensic case file" feeling is about starkness, not smoothness. No
  `zoomThroughTransition` here either — three of four modes now deliberately don't use
  the flagship zoom-through, which is a real tension the report below calls out
  explicitly.

### Captions
`.subs` styled as aggressive short-punch fragments: 1–3 words per chunk instead of the
usual 2–3 word karaoke chunks, all-caps, tight tracking, and the current spoken chunk
flashes white-on-red (`--alert`) for a single frame before settling to plain white —
the one caption style across all four modes that uses a hard color flash instead of a
smooth color/scale change, matching the mode's overall "stark, not smooth" motion
language.

### When to use this mode
A genuine, verified failure — something broke, and there's real evidence of it. Not a
mixed result (that's THE LAB, where color state can legitimately land on yellow/warn)
and not a subjective disappointment — "it broke" needs the same standard of evidence as
every other claim this channel makes.

---

## Anti-AI-slop checklist — apply to all four modes

- **No glassmorphism.** No frosted/blurred translucent panels anywhere in any mode.
  `.quote`'s existing solid white card is the ceiling for "panel with depth" — a blur
  filter on a background panel is out.
- **No gratuitous glow.** THE LAB's state-cyan and BROADSHEET/INSTRUCTION's signal
  accents are flat color, not neon bloom. The one glow primitive that exists
  (`animateGlowBloom`) stays reserved for the hook's climax-word beat, same as today —
  it does not become a background treatment for every headline in every mode.
- **No gradient-everything.** A single gradient fill on a bar (`vbarfill.actual` in the
  existing `reel-52.html`) is fine because it reads as a physical meter. A gradient
  background on every panel, card and button is the actual slop pattern — don't do it.
- **Don't just reskin the same layout in four colors.** This is the whole point of
  having four *modes*, not four *palettes*. If a build only changes `--brass`/`--ember`
  and keeps every card centered, every headline the same size, every transition
  `zoomThroughTransition` — that is the old system with new hex values, not this one.
  Concretely: BROADSHEET's grid is left-aligned and numbered, not centered.
  INSTRUCTION CARD's cards are square-cornered and flat, not floating with drop
  shadows. THE INCIDENT is asymmetric, not centered. THE LAB replaces "cinematic camera
  push" with "system reacting." If a new build reuses the exact centered-card,
  cinematic-zoom shape from the old system and only swaps colors, it has not actually
  adopted this system.
- **No 3D.** No CSS 3D transforms, no perspective tilt, no fake depth via `rotateX`/
  `rotateY` on cards. Every mode stays flat/2D; depth comes from layout (asymmetry,
  grid, scale hierarchy), not from simulated dimensionality.
- **No bounce/overshoot easing anywhere**, in any mode — this was already the rule
  (`spring-pop-entrance.md`'s "#1 instant AI-video tell") and nothing about four modes
  changes it. Every eased motion in this system, across all four modes, uses
  `smoothIn`/`power3.out` or a flat linear ramp — never a back/elastic curve.
- **Every mode still needs a reason, not a vibe.** A mode is chosen by what kind of
  claim the episode is making (tested / discovered / how-to / broke), never by "this
  one looks cool for this topic."

---

## Real, honest tension — read this before building an episode on this system

- **Three of the four modes deliberately do not use `zoomThroughTransition`**, the one
  motion recipe that's actually shipped in a real episode (23) and is wired into
  `video/reel-template.html` as the universal scene-to-scene transition today. THE LAB
  uses a scanline/hard-cut, BROADSHEET uses a rule-retract/rule-build, INSTRUCTION CARD
  uses a slide-up page-turn, and only THE INCIDENT keeps a hard-cut-plus-shake that's
  also not zoom-through. That means **adopting this system in full retires the
  channel's one verified, already-shipped transition recipe as the default** — it
  doesn't delete `zoomThroughTransition` (it's still the right choice for act-to-act
  cuts inside this very playground, and nothing stops a future mode-specific episode
  from reaching for it deliberately), but if "zoom-through everywhere" was itself
  becoming a recognizable channel signature, this system trades that consistency for
  four more legible, more differentiated ones. Worth deciding on purpose, not by
  accident.
- **BROADSHEET is the mode under the most real strain against the "one channel" brand
  constants.** A serif display headline, a left-aligned numbered grid, and a near-
  monochrome ivory/black palette is, by design, the aesthetic most different from
  everything the channel has shipped through episode 52. `Assistant`/`Plex Mono` in the
  supporting type and the same dark base keep it technically compliant with every
  brand constant, but it is the one mode where a viewer scrubbing past it fast might
  genuinely wonder if they landed on a different account for a second before the
  caption bar and episode marker resolve that. That's not necessarily wrong — the
  entire premise of this system is that the four modes should be *legibly different*
  — but it's the one that pushes hardest, and it deserves a real look from David rather
  than an assumption that "brand constants present = automatically still recognizable."
- **Two new motion primitives, `redactionLift` and `beforeAfterWipe`, plus a state-lock
  helper (`lockState`) and a `scanlineCut`, are specified above but not yet added to
  `motion-kit.js`.** The playground builds their exact behavior inline (so what's
  demoed is real, working code, not a mockup) but they are not yet promoted to shared,
  reusable functions the way the five existing recipes are. That promotion — extract,
  verify in isolation, re-verify with a frame-capture check — is real follow-up work
  this prototype doesn't do, matching the same process every existing recipe went
  through before landing in `motion-kit.js`.
