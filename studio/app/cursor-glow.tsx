"use client";

import { useEffect, useRef } from "react";

/** The video house style's own cursor treatment (brand/house-style.md §5: "Cursor in
 *  screen recordings: enlarged 140%, soft brass glow, smoothed path, ripple on click")
 *  brought to the site's real cursor — a small glow that trails the pointer, the same
 *  device viewers already recognize from the screen-recording segments of every episode.
 *
 *  Desktop-with-a-real-mouse only: gated on (hover: hover) and (pointer: fine), so it
 *  never mounts on touch devices, where there's no cursor to decorate and the raw
 *  mousemove listener would be dead weight. Skipped under prefers-reduced-motion — a
 *  glow that trails the pointer is exactly the kind of motion that setting asks to
 *  remove, and the plain system cursor works fine without it. */
export default function CursorGlow() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const el = ref.current;
    if (!el) return;
    let x = window.innerWidth / 2, y = window.innerHeight / 2, vx = x, vy = y;
    let raf = 0;
    const onMove = (e: MouseEvent) => { x = e.clientX; y = e.clientY; };
    window.addEventListener("mousemove", onMove);
    const tick = () => {
      vx += (x - vx) * 0.18;
      vy += (y - vy) * 0.18;
      el.style.transform = `translate(${vx}px, ${vy}px)`;
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => {
      window.removeEventListener("mousemove", onMove);
      cancelAnimationFrame(raf);
    };
  }, []);

  return <div ref={ref} className="cursorglow" aria-hidden />;
}
