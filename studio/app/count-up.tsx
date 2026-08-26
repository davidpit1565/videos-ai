"use client";

import { useEffect, useRef, useState } from "react";

/** Counts up to a real, already-computed value — never invents the number, only
 *  animates arriving at it. Runs once, when the tile scrolls into view.
 *
 *  Initial state is the real value, not 0: this used to start at 0 unconditionally, which
 *  is exactly the "fabricated 0" the comment at its call site says never to show — a stat
 *  block above the fold (the homepage hero) rendered that 0 in the server HTML and on
 *  every first paint, before the animation had a chance to run. */
export default function CountUp({ value, duration = 900 }: { value: number | null; duration?: number }) {
  const [shown, setShown] = useState(value ?? 0);
  const ref = useRef<HTMLSpanElement>(null);
  const done = useRef(false);

  useEffect(() => {
    if (value == null) return;
    const el = ref.current;
    if (!el) return;
    // Already on screen at mount (the hero stat, above the fold) — showing the real value
    // and then visibly resetting it to 0 to "reveal" it reads as a glitch, not a flourish.
    // Only animate the reveal for a tile that's actually scrolled into view.
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight && rect.bottom > 0) {
      done.current = true;
      return;
    }
    const obs = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting || done.current) return;
        done.current = true;
        const start = performance.now();
        const from = 0;
        const to = value;
        function tick(now: number) {
          const t = Math.min(1, (now - start) / duration);
          const eased = 1 - Math.pow(1 - t, 3);
          setShown(Math.round(from + (to - from) * eased));
          if (t < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
      },
      { threshold: 0.4 },
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, [value, duration]);

  if (value == null) return <span ref={ref}>—</span>;
  return <span ref={ref}>{shown.toLocaleString("en-US")}</span>;
}
