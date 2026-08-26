"use client";

import { useEffect, useRef, useState } from "react";

/** The web version of the video house style's own signature transition — brand/house-
 *  style.md §4, "the brass wipe": a thin brass line sweeps across and the new section
 *  is behind it. Same device, just triggered by scroll instead of a cut between shots.
 *
 *  Skips the animation (shows content immediately) for anything already on screen at
 *  mount, and under prefers-reduced-motion — same rule CountUp already follows: a
 *  reveal effect on something the visitor can already see reads as a glitch, not a
 *  flourish, and motion should never fire on someone who asked their OS not to show it. */
export default function Reveal({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const [shown, setShown] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setShown(true);
      return;
    }
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight && rect.bottom > 0) {
      setShown(true);
      return;
    }
    const obs = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        setShown(true);
        obs.disconnect();
      },
      { threshold: 0.15 },
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  return (
    <div ref={ref} className={`reveal${shown ? " in" : ""}${className ? ` ${className}` : ""}`}>
      {children}
    </div>
  );
}
