"use client";

import { useEffect, useRef, useState } from "react";

/** Counts up to a real, already-computed value — never invents the number, only
 *  animates arriving at it. He asked directly for the count-up to play on every visit,
 *  hero stat included, rather than sitting still because it happened to already be on
 *  screen at mount — a static number read as broken, not as a fix. Starts at 0 every
 *  time (server-rendered 0 too): a brief 0 before the count-up lands is the same
 *  convention every stat-tile landing page uses, and is a world apart from the earlier
 *  bug this replaced — a stray permanent 0 with no animation ever following it. */
export default function CountUp({ value, duration = 900 }: { value: number | null; duration?: number }) {
  const [shown, setShown] = useState(0);
  const ref = useRef<HTMLSpanElement>(null);
  const done = useRef(false);

  useEffect(() => {
    if (value == null) return;
    const el = ref.current;
    if (!el) return;
    function run() {
      if (done.current) return;
      done.current = true;
      const start = performance.now();
      const from = 0;
      const to = value as number;
      function tick(now: number) {
        const t = Math.min(1, (now - start) / duration);
        const eased = 1 - Math.pow(1 - t, 3);
        setShown(Math.round(from + (to - from) * eased));
        if (t < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    }
    // Already on screen at mount (the hero stat, above the fold) — play immediately
    // instead of waiting for an intersection event that will never fire.
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight && rect.bottom > 0) {
      run();
      return;
    }
    const obs = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        run();
        obs.disconnect();
      },
      { threshold: 0.4 },
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, [value, duration]);

  if (value == null) return <span ref={ref}>—</span>;
  return <span ref={ref}>{shown.toLocaleString("en-US")}</span>;
}
