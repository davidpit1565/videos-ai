---
name: motion-remotion-notes
description: Our own short notes on motion ideas taken from the official Remotion agent skills, rewritten for GSAP + HyperFrames. Use when choosing an ease, a scale animation, a scene transition or a hand-drawn highlight for a reel. Knowledge only; we do not use Remotion.
---

# Motion ideas from the Remotion skills, in our terms

These are notes in our own words, NOT a copy (see SOURCE.md for why). We render with HyperFrames and GSAP, not Remotion. Miki style rules win over anything here.

1. **Spring with no bounce.** Remotion's "nice push with no bounce" is a spring with very high damping. In GSAP use a function ease from a closed-form critically damped spring: `f(t) = 1 - (1 + w t) e^(-w t)`, divided by `f(1)`, with `w` about 9. Fast launch, long soft landing, never overshoots. Used in `video/demo-skills/hf/index.html` (`spring(zeta, w)`).
2. **Default enter curve.** `cubic-bezier(0.16, 1, 0.3, 1)`; in GSAP `CustomEase.create("expoOut", "0.16,1,0.3,1")`. Always clamp: a value must not run past its end state.
3. **Scale needs a perceptual curve.** A linear scale tween looks as if it slows down as the object grows. Tween scale with an ease-out, or tween `Math.log(scale)` linearly, so growth looks even.
4. **Several keyframes, one ease per segment.** For in / hold / out, give each segment its own ease instead of one ease over the whole move. In GSAP: separate tweens on a timeline, or `keyframes` with `easeEach`.
5. **Transitions overlap, so the timeline gets shorter.** A crossfade of d seconds means both scenes are on screen for d: plan total length as the sum of scenes minus the sum of overlaps. An overlay on the cut (a soft light sweep) does not shorten anything.
6. **Hand-drawn marks driven by progress.** A highlight, circle or underline is drawn from a 0-1 progress tied to the video clock, never by a timer. Ours: an SVG path with DrawSVG or `stroke-dashoffset`. One ring per screen (Miki); never a filled box behind a word (standing rule).
7. **Posterize on purpose.** Sampling an animation every 2nd or 3rd frame gives a hand-made, stop-motion feel. Possible answer to "must not look AI" for one element (a ring, a doodle), not for text.
8. **Lottie.** Load the data before the first frame, never autoplay, and drive the frame from the video clock. Ours: `lottie.loadAnimation({autoplay:false, animationData})` and a GSAP tween that calls `goToAndStop(frame, true)`.
9. **One scene, one component.** Each scene is its own function returning a timeline; the parent only places scenes on labels. Same as GSAP nested timelines.
