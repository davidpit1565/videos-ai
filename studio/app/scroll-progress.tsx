"use client";

import { useEffect, useRef } from "react";

/** A thin brass line across the very top of every public page, tracking how far
 *  down the page the visitor actually is — the episode pages are the real reason
 *  this exists: "the exact screen, the exact paste, and the part that breaks" is
 *  a long read, and there was no way to see how much of it was left without
 *  scrolling to the end and back. Reads scroll position directly (no React state,
 *  no re-render per pixel) and writes straight to the DOM via a ref. */
export default function ScrollProgress() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    function onScroll() {
      const el = document.documentElement;
      const max = el.scrollHeight - el.clientHeight;
      const pct = max > 0 ? el.scrollTop / max : 0;
      if (ref.current) ref.current.style.transform = `scaleX(${pct})`;
    }
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
    };
  }, []);

  return <div className="scrollbar" ref={ref} aria-hidden="true" />;
}
