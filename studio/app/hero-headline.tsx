"use client";

import { useEffect, useState } from "react";

/** The channel's other signature device, brought to the one line on the site that
 *  deserves it: word-by-word captions lit in brass as they're spoken (karaoke.py,
 *  brand/house-style.md's "2-3 word chunks with the spoken word lit in brass"). The
 *  hero headline plays the same reveal once on load — each word lights brass as it
 *  "lands," then settles, with "actually work" staying lit the way <em> already did.
 *  One deliberate bold moment, not a loop, not repeated anywhere else on the page —
 *  spending it everywhere would just be a generic word-stagger effect instead of the
 *  specific thing this channel is already known for.
 *
 *  Skipped entirely under prefers-reduced-motion; the final state (identical markup,
 *  "actually work" in <em>) renders immediately either way, so there's no flash of
 *  wrong content for anyone who doesn't see the animation. */
export default function HeroHeadline() {
  const words = ["AI", "setups", "that", "actually", "work."];
  const [lit, setLit] = useState<number>(-1);
  const [reduced, setReduced] = useState(false);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setReduced(true);
      return;
    }
    let i = -1;
    const id = setInterval(() => {
      i++;
      setLit(i);
      if (i >= words.length - 1) clearInterval(id);
    }, 130);
    return () => clearInterval(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (reduced)
    return (
      <h1>
        AI setups that <em>actually work</em>.
      </h1>
    );

  return (
    <h1 className="herokar">
      {words.map((w, i) => {
        const settled = w === "actually" || w === "work." ? "brass" : lit > i ? "text" : "dim";
        const isLit = lit === i;
        return (
          <span key={i} className={`hk ${settled}${isLit ? " on" : ""}`}>
            {w}
          </span>
        );
      })}
    </h1>
  );
}
