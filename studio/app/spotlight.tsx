"use client";

import { useEffect } from "react";

/** A cursor-follow glow on card-style links (episode cards, prompt cards, tool
 *  pills, search hits) — the same brass the rest of the identity already uses,
 *  just responding to the mouse instead of sitting static. One listener for the
 *  whole page instead of one per card: the glow itself is a CSS variable each
 *  card's own ::after reads (see globals.css), so moving the mouse never
 *  triggers a React re-render.
 *
 *  Skipped entirely on touch devices (no hover, so a stale glow would sit at the
 *  last tap forever) and under prefers-reduced-motion, same rule every other
 *  motion device on this site already follows. */
export default function Spotlight() {
  useEffect(() => {
    if (!window.matchMedia("(hover: hover)").matches) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    function onMove(e: PointerEvent) {
      const el = (e.target as HTMLElement)?.closest?.(
        ".eps a, .prompts a, .tracks a, .hits > li, .issueteaser, .tplcard",
      ) as HTMLElement | null;
      if (!el) return;
      const r = el.getBoundingClientRect();
      el.style.setProperty("--mx", `${((e.clientX - r.left) / r.width) * 100}%`);
      el.style.setProperty("--my", `${((e.clientY - r.top) / r.height) * 100}%`);
    }
    document.addEventListener("pointermove", onMove, { passive: true });
    return () => document.removeEventListener("pointermove", onMove);
  }, []);

  return null;
}
