"use client";

import { useEffect, useLayoutEffect, useRef, useState } from "react";

// useLayoutEffect warns when rendered on the server; the effect below only runs in the browser.
const useIsoLayoutEffect = typeof window === "undefined" ? useEffect : useLayoutEffect;

/** Counts up to a real, already-computed value — never invents the number, only
 *  animates arriving at it. He asked directly for the count-up to play on every visit,
 *  hero stat included, rather than sitting still because it happened to already be on
 *  screen at mount — a static number read as broken, not as a fix. Starts at 0 every
 *  time in the browser, but the server renders the REAL value (25.10.2026): the earlier
 *  server-rendered 0 meant crawlers, link previews, no-JS readers and an outside audit saw
 *  "0 episodes live / 0 views measured" on the home page. The count-up is unchanged for
 *  anyone running JavaScript; it is skipped for people who ask for reduced motion. */
export default function CountUp({ value, duration = 900 }: { value: number | null; duration?: number }) {
  const [shown, setShown] = useState(value ?? 0);
  const ref = useRef<HTMLSpanElement>(null);
  const done = useRef(false);

  useIsoLayoutEffect(() => {
    if (value == null) return;
    const el = ref.current;
    if (!el) return;
    if (window.matchMedia?.("(prefers-reduced-motion: reduce)").matches) return;
    // Reset to 0 before the first browser paint of this component, so the count-up still
    // starts from 0 for people with JavaScript while the server HTML carries the real value.
    setShown(0);
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
