# Motion recipes — verified upgrades, ready to drop into the next build

David asked directly for a much higher production level, not one clever trick — a real
system where each kind of scene gets the treatment that actually fits it. Every recipe
below was built, rendered frame-by-frame, and checked by him against a real comparison
clip before landing here — none of this is theoretical. Sourced from the real technique
catalog in `.claude/skills/hyperframes-animation/` (rules, blueprints, transitions), not
invented from scratch.

**Status: verified in isolated demos, not yet wired into `produce.sh` or a shipped
episode.** The next real step is pulling these into the actual scene templates the
pipeline builds from — this file is the reference for doing that, not a replacement for
it.

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

**Not done yet:** the reel template `produce.sh` actually builds from doesn't call
`MotionKit` anywhere — no shipped episode uses it. The real next step: update that
template so a new episode gets the right recipe per scene type automatically — hook
scenes get recipe 1, `.quote` scenes get recipe 2, contradiction/scoreboard scenes get
recipe 3, every scene transition gets recipe 4 (matched to the episode's mood), and
recipe 5 gets used once, deliberately, at the actual reveal beat. Not a rewrite of every
past episode — applied going forward, the same rule the jargon-audit fix used.
