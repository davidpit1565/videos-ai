"use client";

import { useEffect } from "react";

/** The hero's ambient glow drifts slower than the page as you scroll past it — real
 *  depth, not just a static blob sitting on top of the content. Written to the CSS
 *  `translate` property (not `transform`) specifically so it never fights the glow's
 *  own one-time entrance animation in globals.css, which already owns `transform:
 *  scale()` — two rules touching `transform` on the same element is how one of them
 *  silently loses, and this way neither has to.
 *
 *  rAF-throttled so a fast scroll never queues more than one write per frame, capped
 *  to a small range so it reads as depth rather than the background swimming, and
 *  skipped entirely under prefers-reduced-motion — same rule every other motion
 *  device on this site already follows. */
export default function HeroParallax() {
  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const hero = document.querySelector<HTMLElement>(".site .hero");
    if (!hero) return;

    let ticking = false;
    function apply() {
      ticking = false;
      const rect = hero!.getBoundingClientRect();
      // Only move while the hero is anywhere near the viewport — a page with a tall
      // hero scrolled far out of view has no reason to keep computing this on every
      // frame of an unrelated section's scroll.
      if (rect.bottom < -200 || rect.top > window.innerHeight + 200) return;
      const y = Math.max(-40, Math.min(40, window.scrollY * -0.15));
      hero!.style.setProperty("--hero-px", `${y.toFixed(1)}px`);
    }
    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(apply);
    }
    apply();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return null;
}
