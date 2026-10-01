# Motion recipes — verified upgrades, ready to drop into the next build

David asked directly for a much higher production level, not one clever trick — a real
system where each kind of scene gets the treatment that actually fits it. Every recipe
below was built, rendered frame-by-frame, and checked by him against a real comparison
clip before landing here — none of this is theoretical. Sourced from the real technique
catalog in `.claude/skills/hyperframes-animation/` (rules, blueprints, transitions), not
invented from scratch.

**Status: all five recipes are real, tested code in `export/motion-kit.js`, and all
five are wired into `video/reel-template.html`** — the starter build every new episode
copies. Recipe 4 (zoom-through transitions) has shipped in a real episode (23); recipes
1-3 (hook word-by-word, quote highlight, scoreboard stagger) are wired into the
template and verified there but have not shipped in an episode's actual content yet —
the next real episode built from the template is the first real test of them end to
end, not just in isolation.

---

## 1. Hook scene — word-by-word build + climax-word spotlight

**Use for:** the opening line (the `punch` scene), where a beat-by-beat build creates
real anticipation instead of the whole line landing at once.

**What changed from what's shipped today:** `reel-22.html`'s hook currently pops the
*entire* `<h2>` in as one block (`.b` class, a single opacity+scale transition). This
recipe reveals it word by word, and adds a soft glow bloom behind the boxed climax word
(`ambient-glow-bloom`, peak opacity ≤0.30) landing on the same beat as its spring-pop —
glow and word resolve together, never glow-then-word.

```js
// Per-word entrance — smooth settle, NOT the overshoot bezier .b currently uses
// (a bouncy overshoot is explicitly the #1 agent-video tell — see spring-pop-entrance.md)
function smoothIn(p){ return 1 - Math.pow(1-p, 3); } // power3.out
const WORD_GAP = 0.10, WORD_DUR = 0.30;
words.forEach((el, i) => {
  const at = WORD_START + i * WORD_GAP;
  // per frame: e = smoothIn(clamp01((t-at)/WORD_DUR))
  // el.opacity = e; el.transform = `translateY(${18*(1-e)}px)`
});

// Climax word (the .box span): spring-pop (scale 0->1, no bounce) landing together
// with a glow bloom behind it — same timing, not staggered
// box: opacity=e; transform = `rotate(-1.2deg) scale(${e})`
// glow (a radial-gradient div BEHIND the box, z-index below it):
//   opacity = 0.30 * min(1, e/0.35); transform = `scale(${0.85+0.15*e})`
```

**Also apply the multi-phase camera here** (see recipe 4) — a straight linear
`1 + 0.06*f` zoom (what's shipped) reads flat; a pull-back → hold → push timed to land
the push exactly on the climax word is the actual "wow."

---

## 2. Quote / explainer card — physical lift + word-by-word + per-word highlight

**Use for:** any `.quote` scene (the white card with a `qk` label and `qb` body) —
the "read this carefully" beat, not a dramatic one.

**What changed:** the card currently pops in as one block, all text visible at once.
This recipe: the card rises with a *growing* shadow (reads as lifting off the surface,
not just fading in), the label and body build word-by-word, and the emphasized phrase
gets a highlight sweep once the words land.

**The real bug this recipe fixes, not just adds:** a highlight drawn as ONE box
stretched across a phrase that wraps two lines collapses into a thin, glitchy sliver at
the line-wrap point (an absolutely-positioned box has no single rectangle for a
fragmented inline span). The fix is a **bar per highlighted word**, not one bar for the
whole phrase — each word never itself wraps, so a per-word rect is always correct
regardless of where the line breaks:

```js
// After the words are in the DOM (their layout is now final):
function buildHighlightBars(qb, highlightedWordEls){
  const qbRect = qb.getBoundingClientRect();
  return highlightedWordEls.map(el => {
    const r = el.getBoundingClientRect();
    const bar = document.createElement('div');
    bar.className = 'hlbar'; // position:absolute; background:#FFD835; z-index:0 (behind text)
    bar.style.left = (r.left - qbRect.left - 6) + 'px';
    bar.style.top = (r.top - qbRect.top - 4) + 'px';
    bar.style.width = (r.width + 12) + 'px';
    bar.style.height = (r.height + 8) + 'px';
    bar.style.transformOrigin = 'left center';
    qb.insertBefore(bar, qb.firstChild);
    return bar;
  });
}
// Per frame, each bar grows AND fades in together (never just scaleX alone — a bar at
// low scaleX with full opacity reads as a stray glitch line, not a growing highlight):
//   e = smoothIn(clamp01((t - (HL_AT + i*0.06)) / HL_DUR))   // i*0.06 = slight per-word stagger
//   bar.transform = `scaleX(${e})`; bar.opacity = 0.4 * min(1, e/0.35)
```

Card lift:
```js
// le = smoothIn(clamp01((t-CARD_AT)/CARD_DUR))
// card.opacity = le; card.transform = `translateY(${36*(1-le)}px)`
// card.boxShadow = `0 ${10+30*le}px ${40+60*le}px rgba(0,0,0,${0.25*le})`
```

---

## 3. Reveal / contradiction scene — staggered stagger, not simultaneous pop

**Use for:** the scoreboard-style scene where two facts contradict each other (episode
22's "The tool FAILED" / "The dashboard SUCCESS") — the actual point of the episode.

**What changed:** both rows currently land together as one `.b` block, which loses the
contradiction — there's no beat to let the first fact register before the second
undercuts it. This recipe lands the bad news alone first, a genuine pause, then the
ironic "success" SLAMS in bigger/harder with a glow burst and a brief impact shake.

```js
// Row A (bad news) — plain settle, no drama, let it register.
// ae = smoothIn(clamp01((t-A_AT)/A_DUR)); rowA.opacity=ae; rowA.transform=`scale(${ae})`

// ~0.5s later, row B (the ironic "success") — same mechanism, timed later, plus:
// a glow bloom (success-green, same ambient-glow-bloom rule as recipe 1) bursting
// behind it, and one brief impact shake on the whole board (multi-phase-camera's
// "camera shake" variation — high-amplitude, high-frequency, decaying, ~0.22s):
//   sp = t - B_AT; shakeX = sp<0.22 ? Math.sin(sp*70) * 6 * (1 - sp/0.22) : 0
//   board.transform = `translateX(${shakeX}px)`
```

---

## 4. Scene-to-scene transitions — zoom-through, not a hard cut

**The real, repo-wide finding, not a per-scene one:** every transition in every shipped
episode today is `.scene{opacity:0} .scene.active{opacity:1}` — an instant, motionless
cut, for the entire runtime. `hyperframes-animation/transitions/overview.md` states this
directly as a non-negotiable rule for every multi-scene composition: **"Every
composition uses transitions. No exceptions. Scenes without transitions feel like jump
cuts."** This is not a per-scene polish item — it's a gap across the whole pipeline.

For this channel's "urgent" energy episodes (red/ember palette), the matching primary
transition per the energy table in `transitions/overview.md` is **zoom-through**
(`transitions/css-scale.md`):

```js
// Outgoing scene: scales up, blurs, fades — "flies past the camera"
// oe = (t-T)/OUT_DUR cubed (power3.in feel)
// outEl.opacity = 1-oe; outEl.transform = `scale(${1+1.5*oe})`; outEl.filter = `blur(${8*oe}px)`

// Incoming scene: arrives from behind — starts small+blurred, resolves sharp
// ie = smoothIn((t-T2)/IN_DUR)   // T2 starts ~0.35s after the outgoing scene starts leaving
// inEl.opacity = ie; inEl.transform = `scale(${0.5+0.5*ie})`; inEl.filter = `blur(${8*(1-ie)}px)`

// Optional accent: a brief white flash at the crossover (high-energy accent per the table)
```

For calmer, non-urgent episodes, swap the primary per the same table (e.g. blur
crossfade / focus pull for a calm energy) — don't reuse zoom-through for everything;
that's the same "one formula for the whole video" mistake this file exists to fix.

---

## 5. The one hero beat — fragment shatter, reserved for the real reveal

**Use for:** at most one moment per episode — the actual "gotcha," the moment the whole
episode has been building to. Never more than one; a GPU-tier effect used twice in one
video stops reading as special.

This is a genuinely different tier from recipes 1-4 (canvas/GPU work, not CSS) — see
`hyperframes-animation/adapters/html-in-canvas-patterns.md`, effect #3 (Shatter /
Fragment Explosion). Built and verified as a Canvas2D fragment shatter (simpler and more
robust than the full Three.js reference for a 2D badge, same visual idea): the false
claim (e.g. a green "SUCCESS" badge) breaks into deterministic fragments that fly apart
and fade, revealing the real content sitting behind it.

```js
// Deterministic PRNG — Math.random() is banned in HyperFrames renders
function mulberry32(seed){
  return function(){
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const rng = mulberry32(42);

// 1. Draw the false-claim badge once onto an offscreen canvas (the source texture).
// 2. Cut it into an 8x4 fragment grid; give each fragment a seeded random fly-out
//    vector, rotation, and small stagger delay (rng()*0.35).
// 3. Hold the whole badge still and readable for ~1.4s (this IS the "wow" setup —
//    don't rush it, per his own earlier note about giving a viewer time to read).
// 4. Shatter over ~0.85s: each fragment's alpha and displacement driven by the same
//    per-fragment progress (power2.in displacement, power3.out alpha fade).
// 5. The real content behind it fades/rises in starting slightly before the shatter
//    finishes, so the reveal feels continuous, not like two separate cuts.
```

---

## Rewiring this into produce.sh

**Step one is done: `export/motion-kit.js`** is a real, tested `window.MotionKit`
module implementing all five recipes as plain functions (`splitWords`/`animateWords`,
`buildHighlightBars`/`animateHighlightBars`, `animatePop`/`animateGlowBloom`,
`impactShake`, `multiPhaseCamera`, `zoomThroughTransition`/`transitionFlash`,
`buildShatter`) — pure math driven by a single `t` per frame, no `Math.random()`, no
real-time clock, matching the deterministic pattern `FRAMES=1` capture requires. It was
extracted directly from the demo code above and re-verified with its own frame-by-frame
capture (word-by-word build + per-word highlight bars on a line-wrapping phrase,
confirmed correct across the wrap point — no sliver bug) before shipping. Include it
with `<script src="../export/motion-kit.js">` in a reel build and call its functions
from the build's own `render()`/`__frame(t)` loop.

**Step two, partly done: `video/reel-template.html`** is a real starter build — copy it
to start a new episode instead of copying an old shipped episode's file. It wires in
**recipe 4 (zoom-through transitions) universally**: every scene now crosses into the
next with `MotionKit.zoomThroughTransition`, not the flat `.scene{opacity:0/1}` hard-cut
every episode has shipped with so far. Verified the same way as the module itself — a
real frame-by-frame capture (`export/frames.js`) confirmed the transitions actually
render (blur/scale/fade crossing correctly at each scene boundary), and
`node export/safe_check.js video/reel-template.html` came back clean across the whole
runtime, not just eyeballed.

**Step three, now done: recipes 1-3 are wired into the template.** The missing piece
was a markup-safe word-splitter — `MotionKit.splitWords()` only takes plain text, and
calling it on `h2.innerHTML` as-is would have silently mangled the boxed-word markup
every hook scene relies on. `MotionKit.splitWordsSafe(container, opts)` walks the live
DOM instead of retyping it as a string: a `<br>` is left alone (it isn't a word), the
climax word's `.box`/`.ebox` span is treated as one atomic word unit (never split, so
`animatePop()`/`animateGlowBloom()` still target it directly), and any other inline
element (`<strong>`, `<em>`) is recursed into with its own words split individually and
tagged `.hl` when they came from `opts.highlightTag` (default `STRONG`) — that's what
`buildHighlightBars()` reads to find the words to underline. It returns
`{words, highlighted}`.

`video/reel-template.html` now uses it for all three: the hook (`renderHook()`) splits
`h2` and gives the `.box` word the spring-pop + glow bloom while the rest fade in word
by word, with `multiPhaseCamera` timed to push exactly on the climax word instead of the
flat linear zoom; the quote card (`renderQuote()`) lifts with a growing shadow, builds
its label and body word by word, and highlights the `<strong>` phrase with one bar per
word (verified correct across a real line-wrap — no sliver); the scoreboard
(`renderScoreboard()`) lands the bad-news row alone first, then the good-news row ~0.5s
later with a glow bloom and a brief impact shake on the whole board.

**A real bug found wiring this in, not a hypothetical one:** `buildHighlightBars()`
measures each word's `getBoundingClientRect()` — calling it immediately on script load
measures the fallback font's metrics if the Google Fonts webfont hasn't finished
loading yet, so every bar lands at the wrong spot once the real font swaps in (it
rendered behind the first two letters of the wrong word in testing). Fixed by building
the bars only after `document.fonts.ready` resolves.

Verified with `export/frames.js` frame captures at each recipe's key beat (word-by-word
build, climax pop+glow, the corrected highlight bars, the scoreboard's staggered
reveal+shake) and `node export/safe_check.js video/reel-template.html` — clean, no
safe-area or overlap violations. The same pass also carried over episode 23's `.kb`/
transition-compounding fix (drop the per-scene push-in to 0 once the scene's own
outgoing transition begins) into this template, so a new episode built from it doesn't
have to rediscover that bug.

---

## 6. Spoken-word emphasis — replaces a duplicate caption for a fixed headline

**Use for:** the real-photo-composite style (`video/reel-template-photo.html`), where
the on-screen headline already shows the full line for the whole scene.

**The real bug this fixes:** episode 54 shipped with the full headline on screen AND a
separate word-by-word caption underneath it running the same sentence a second time —
David's direct feedback, third round, after the episode was otherwise live. His
proposed fix: one fixed headline, each spoken word pops/grows in place, no second
caption track. Verified correct before building it: `grep`ping `reel-53.html` showed
the same headline+caption duplication exists in the all-CSS synthetic style too, but
it reads as more redundant in the photo style specifically, which is where this
recipe is scoped for now.

This was the "missing word-splitter" gap this file used to flag as not built — it
turned out the splitter (`MK.splitWordsSafe`) already existed and was already wired
into `video/reel-template.html`'s hook/quote/scoreboard scenes (see the "Rewiring"
section above, step three). The actual missing piece was narrower: a way to drive
emphasis on an ALREADY-VISIBLE headline word from the real spoken-word timing, instead
of building a second caption track from it.

```js
// MK.animateWordEmphasis(el, t, winStart, winEnd, opts) — called once a word's own
// entrance animation has finished. winStart/winEnd are absolute seconds (same clock
// as data-in/data-out); null means "no matched narration word," and the word just
// holds at rest. A short attack/decay (0.07s/0.16s default) means the pop never
// snaps — it's a scale (1 -> ~1.08) and a brightness filter (never a color swap,
// which would need a second color to tween through and read as a flash).
if (entranceDone) {
  w.style.opacity = '1';
  MK.animateWordEmphasis(w, t, win ? win[0] : null, win ? win[1] : null);
}
```

The timing data itself comes from `export/headline_sync.py`, a new script parallel to
`export/karaoke.py`: it tokenizes each scene's own headline (keeping the `.box` climax
phrase as ONE collapsed window — start of its first spoken word to end of its last —
the same atomic-unit rule `splitWordsSafe` already applies at runtime), aligns those
tokens against real Whisper word stamps with the exact same `align()` function
`karaoke.py` uses, and writes the result into a `WORD_WINDOWS` array the template
reads. One timing source feeds both the word that's lit and the word that's spoken —
they cannot drift apart.

**A real bug found building this, not a hypothetical one:** the first version of
`headline_sync.py`'s regex for finding the `WORD_WINDOWS` placeholder was `.*?` across
the whole file (dotall), and the template's own header comment happens to mention the
literal text `WORD_WINDOWS=` in passing — the regex matched there instead, consuming
everything up to some unrelated `];` much further down and silently corrupting the
file. Fixed by anchoring the match to a whole line (`^\s*var WORD_WINDOWS=\[.*\];\s*$`
with `re.M`, no dotall) — prose about the variable can no longer pretend to be the
assignment itself.

**Verified with a real alignment run, not just eyeballed:** built a standalone test
copy of the template with real placeholder photos wired in, generated fake-but-
text-matching Whisper stamps for its placeholder headlines, ran `headline_sync.py`
against it, confirmed via `node export/safe_check.js` the result is still safe-area
clean, and read back each word's actual computed `transform`/`filter` at several
timestamps straight from the page (not a screenshot) to confirm each word emphasizes
only inside its own matched window and sits at rest outside it, including the
collapsed `.box` window spanning multiple spoken words correctly.

**Status: real, tested code (`MK.animateWordEmphasis` in `export/motion-kit.js`,
`export/headline_sync.py`), wired into `video/reel-template-photo.html` — which also
no longer has a `.subs` div or any caption-track code at all for this style.**

**Shipped for real on episode 54 the same night**, after David watched the first round's
picture and flagged, in Hebrew, that he'd asked for this in English by mistake and that
the duplicate caption was still there — he hadn't misread anything; the fix had only
been built and verified on the template, not applied to the actual episode. Applying it
to the real shipped file surfaced two more real bugs this recipe's own text didn't carry
over from the template demo:

- **Two adjacent words could visually overlap and read as one glued word** at the exact
  frame a word's emphasis pop peaked — "fake-face" and "tools" read as "fake-facetools"
  in a still frame, because a `transform:scale()` pop expands past a `display:inline-block`
  span's own edges without pushing its neighbor away. Fixed two ways together: `peakScale`
  dropped from 1.12 to 1.08, and a small permanent `h2 .wd{margin:0 .08em}` gives every
  word breathing room regardless of scale.
- **Removing the duplicate caption also removed its incidental visual churn**, which used
  to help the render pass `qa.py`'s frame-to-frame "picture nearly still" check between
  word-pops. A scene with a long duration and a subtle, by-the-book Ken Burns drift can
  legitimately read as a multi-second near-still stretch at 30fps frame-to-frame diffing,
  even though the photo is visibly panning over its full length — this is a measurement
  artifact of sampling at native frame rate, not a motion deficit a reasonable Ken Burns
  bump can fix without breaking the "slow, subtle drift" convention (`kenBurns()`'s own
  ~1.06-1.12 scale guidance). `check.sh` treats it as a warning, not a failure, for exactly
  this reason — accepted as a known, honest tradeoff of dropping the duplicate caption, not
  chased into over-animating the photo.

Re-verified end to end on the real episode: `headline_sync.py` run against real Whisper
alignment (53 headline words across 8 scenes, 0 unmatched), `safe_check.js` clean, full
`check.sh` gate ALL CHECKS PASSED, and watched twice in full before shipping.

**A fourth round, same night, after David watched this version too and gave three more
real notes in Hebrew — all confirmed correct before fixing, none argued with:**

- **A multi-word climax phrase popping in as one instant block still didn't feel like
  real emphasis — it read as a slab of text appearing, not a climax.** Several of this
  episode's own `.box` phrases run 8-11 words (`"a program that swaps a scammer's own
  face for someone else's, live."`). Fixed by adding `opts.explodeBoxes` to
  `MK.splitWordsSafe()`: a multi-word box now builds word-by-word like the rest of the
  sentence (each word still tagged `.box` so the existing CSS color/weight still
  applies), instead of appearing all at once. A single-word box — the short climax-word
  case recipe 1 was originally built for — is untouched either way, since splitting one
  word changes nothing. The camera-push beat still times off the phrase's first word.
- **The per-word entrance itself read as too gentle — "it only pops a little."** The
  original entrance was a plain opacity fade with a 14px rise, no scale change at all.
  Replaced with a real scale pop (0.82→1, same no-overshoot power3-out curve, no
  bounce). A first attempt combined scale with the translateY rise and pushed a
  near-the-safe-line word 11px past the top tolerance (`safe_check.js` caught it,
  "Call" in scene 6) — transform functions compose, and the rise and the scale were
  interacting in a way that pushed the word higher than either alone. Fixed by dropping
  translateY entirely and using scale alone for the pop.
- **Exploding box words into individual spans then collided with the existing
  spoken-word emphasis** (recipe 6 above): the climax word's own entrance scale, the
  camera-push beat, AND a spoken-word emphasis pop could all land on the same word at
  once, compounding past the safe-area line again. Fixed by never applying
  `animateWordEmphasis` to a `.box` word — it's already visually distinct (accent
  color) and already gets its own camera-push beat, so it doesn't need a second,
  separate pulse once it's spoken.

Re-verified again end to end after all three fixes: `safe_check.js` clean (the "Call"
overflow gone), full `check.sh` gate ALL CHECKS PASSED, watched twice in full — once
confirming the box phrase now visibly builds word by word instead of popping as a
block, and once confirming "Call" sits cleanly inside the safe area at its own peak
scale.

**A separate, unrelated bug found in the same round, worth recording because nothing
caught it automatically**: three consecutive shipped rounds of this episode had no
background music at all. `render.sh`'s `[music.wav]` argument is the last positional
argument and every re-render in this session's earlier rounds simply omitted it — no
check in `check.sh` verifies a music track is present, so it shipped silently clean
three times. A stale music file also existed in `audio/` from before the episode's
duration was re-timed (37.15s vs. the current 36.65s build) and would have been the
wrong length if reused as-is. See CLAUDE.md's new standing note on this.

**A fifth round, same night: David watched again and said this was still wrong, in
two real ways, plus one real timing bug his report led straight to.**

- **"The blue text doesn't pop at all"** — correct, and a direct regression from the
  previous round's safe-area fix: excluding `.box` words from `animateWordEmphasis`
  entirely (to stop the scale pop compounding with the camera-push) also meant a
  `.box` word never did ANYTHING when spoken — no emphasis at all, which reads as
  "frozen," exactly as reported.
- **"Make it the simplest thing — like every other video we've made"**: his own
  description of what he wanted was, word for word, `export/karaoke.py`'s classic
  caption mechanism (`.subs b.on{color:accent}`) — a word turns color exactly while
  it's spoken, nothing else. Not a new idea; the simplest version already existed
  elsewhere in this repo and this recipe had drifted from it by adding scale,
  brightness-filter, and attack/decay easing that the classic version never needed.
  Fixed by rewriting `MK.animateWordEmphasis` to be exactly that: `el.classList.
  toggle('spoken', t is inside its window)`, with the actual color change done in
  CSS (`h2 .wd.spoken{color:accent}`, `h2 .wd.box.spoken{color:#fff}` — a plain word
  lights up accent, a box word, already accent at rest, flips to white instead).
  Color has no layout effect at all, so there is no scale-compounding risk left, and
  the exclusion on `.box` words was removed — every word, box or not, now gets the
  same simple treatment.
- **"It's still missing some words, or popping too early or too late"** — a real bug,
  not an exaggeration. `export/headline_sync.py` was still collapsing a multi-word
  `.box` phrase's individual Whisper-aligned windows down into ONE combined window
  (a leftover from before `explodeBoxes` existed, when the box really was one atomic
  DOM element). At runtime, with `explodeBoxes:true`, a multi-word box is N separate
  entries in `split.words`, not one — so `WORD_WINDOWS[scene]` was one entry shorter
  per box phrase than `split.words` actually is, and every word positioned after a
  box in that scene read a window meant for a different word, one position off. This
  is exactly "missing some words, popping early or late": not a perception issue, an
  index misalignment. Fixed by never collapsing — one window per token, always,
  matching `split.words` 1:1. Episode 54's own count went from "53 headline words"
  (wrongly collapsed) to a verified "104 headline words, 0 unmatched" (one per actual
  token), matching a plain whitespace-split word count of the same headlines exactly.

Re-verified end to end a third time: `safe_check.js` clean, full `check.sh` gate ALL
CHECKS PASSED (and this time with zero `qa.py` "nearly still" warnings at all — the
uniform color-toggle, now applied to every word including box ones, happens to
provide enough frame-to-frame visual churn on its own). Watched twice in full,
checking specifically that words light up in the right place at the right moment
relative to the spoken line, and that `.box` phrases now visibly flash white
word-by-word as they're said rather than sitting static.

**On the standing closing-photo direction (separate note, not acted on yet):** this
same round, David clarified he does still want *some* standing, cross-episode
treatment for the two closing-CTA scenes specifically — not literally the one
hardcoded file the previous round removed, but some consistent direction/design for
those two sentences across every episode, still to be figured out. Explicit
instruction: don't touch episode 54's current closing scenes (they're fine as
shipped), think about what that standing direction could be, and apply it to a
future episode once decided. Tracked, not yet designed.

**Round 3 — a second, different cause of the same "pops too early/late" symptom,
plus the music-source mistake it arrived alongside.** David reported two things
together: the real music library wasn't being used (see CLAUDE.md's new standing
rule on `pick_real_track.py` vs `build_music.py` — a separate mistake, not a motion
one), and the word-sync was "much better... but still not 100% accurate," with the
explicit comparison that synthetic-style episodes had this "automatically perfect."
Measured, not assumed: dumped every scene's `WORD_WINDOWS` alongside each word's
duration and found two outlier-long windows in scene 3, both roughly 1.06s against
a ~0.22s median. Checked each against the raw Whisper word stamps before concluding
anything:
- `"it."` at `[22.58, 23.64]` — genuinely correct. Whisper itself has `{'word':
  'it.', 'at': 22.58, 'dur': 1.06}`; the narrator actually held the word that long
  (also flagged, independently, by `voice_doctor.py`'s own "held too long" check
  back when the narration was first generated). A long window is not automatically
  a bug — check it against the source before treating it as one.
- `"Fake-face"` at `[20.4, 21.46]` — a real bug. Whisper transcribed the single
  hyphenated script word as TWO separate tokens (`{'word': 'Fake', 'at': 20.94}`,
  `{'word': 'face', 'at': 21.12, 'dur': 0.34}`, true span 20.94-21.46), but
  `tokenize_headline()` kept "Fake-face" as one whitespace-split token. `align()`
  (SequenceMatcher-based, in `karaoke.py`) can't match one script token against two
  heard tokens, so the match failed at that position and `align()`'s own gap-fill
  logic stretched the window back to the END of the PRECEDING matched word ("chin."
  at 20.2-20.4) instead of the real start — the word would have visually lit up
  ~0.5s before it was actually said. Same root shape as every alignment bug in this
  file: a mismatch between how the DOM splits a word and how Whisper splits the
  same audio.
  Fixed in `export/headline_sync.py`: for the alignment pass only, split any
  hyphenated displayed word into its hyphen-parts (so "Fake-face" aligns as "Fake"
  and "face", matching Whisper's own granularity) via an `owner[]` array that
  tracks which original displayed-word index each alignment unit belongs to; after
  `align()` returns, collapse each hyphenated word's sub-token spans back into ONE
  window (min start, max end) before writing `WORD_WINDOWS`, so the array stays
  exactly one entry per displayed word — the same invariant the box-collapsing fix
  above exists to protect, this time scoped to splitting-and-rejoining within a
  single displayed word, never across separate ones. Checked the rest of the
  episode's headlines for the same risk (any other hyphenated compound): "real-time"
  in scene 1 and "fake-face" in scene 4 both came back matching their raw Whisper
  spans exactly after the fix, with no regression in word count (still 104, 0
  unmatched against the correctly re-timed `reel-54-timed.html`).
  One real near-miss worth recording: the first re-run of `headline_sync.py` this
  round was pointed at the wrong source file (`video/reel-54.html`, the pre-retime
  build with CUES still running to 58s) instead of `video/reel-54-timed.html` (the
  actual 36.65s retimed build the render pipeline uses) — produced "23 unmatched"
  immediately, which is what caught it. Always confirm which build file a CUES
  array's own duration matches the render's actual duration before trusting a
  headline_sync run's word count.
  Verified against the real rendered output, not just the generated HTML: extracted
  exact frames by frame index (not `-ss`, which can land on the wrong frame near a
  seek point) around both "Fake-face" and "real-time," sampled pixel color over the
  text region across consecutive frames, and confirmed each one flips color within
  one video frame (~33ms) of its real Whisper timestamp. Full `check.sh` gate ALL
  CHECKS PASSED; watched the final render in full twice, checking specifically for
  the previously-wrong word and for the real music track's continuous presence
  (confirmed via `check_music_bed.py` run against the actual rendered file's own
  audio track, not just the input wav).
