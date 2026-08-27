"use client";

import { usePathname } from "next/navigation";
import { useEffect, useRef, useState } from "react";

/** The video house style's own signature transition (brand/house-style.md §4, "the brass
 *  wipe") — a 3px brass line sweeps the frame in 350ms between sections, no dissolves, no
 *  slides. Reveal.tsx already brought this to scroll; this brings the exact same device to
 *  page navigation, which until now was a plain instant swap — the one place left where the
 *  site didn't feel like the same channel as the videos.
 *
 *  Skipped entirely under prefers-reduced-motion, same rule every other motion effect here
 *  follows, and on the very first paint (no prior pathname to have moved from). */
export default function PageWipe() {
  const path = usePathname();
  const prev = useRef(path);
  const [key, setKey] = useState(0);

  useEffect(() => {
    if (prev.current === path) return;
    prev.current = path;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    setKey((k) => k + 1);
  }, [path]);

  if (!key) return null;
  return <div key={key} className="pagewipe" aria-hidden />;
}
