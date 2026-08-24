"use client";

import { useEffect, useRef, useState } from "react";

/** Counts up to a real, already-computed value — never invents the number, only
 *  animates arriving at it. Runs once, when the tile scrolls into view. */
export default function CountUp({ value, duration = 900 }: { value: number | null; duration?: number }) {
  const [shown, setShown] = useState(0);
  const ref = useRef<HTMLSpanElement>(null);
  const done = useRef(false);

  useEffect(() => {
    if (value == null) return;
    const el = ref.current;
    if (!el) return;
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
