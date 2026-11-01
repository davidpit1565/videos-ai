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
  // After the one-time reveal, "setups" cycles through what the episodes actually cover
  // (David asked for a rotating word, 1.11.2026). All words share one grid cell so the line never reflows.
  const ROTATE = ["setups", "agents", "prompts", "settings"];
  const [rot, setRot] = useState(0);

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

  useEffect(() => {
    if (reduced || lit < words.length - 1) return;
    const id = setInterval(() => setRot((r) => (r + 1) % ROTATE.length), 2600);
    return () => clearInterval(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [reduced, lit]);

  if (reduced)
    return (
      <h1>
        AI setups that <em>actually work</em>.
      </h1>
    );

  return (
    <h1 className="herokar" aria-label="AI setups that actually work.">
      {words.map((w, i) => {
        const settled = w === "actually" || w === "work." ? "brass" : lit > i ? "text" : "dim";
        const isLit = lit === i;
        if (w === "setups") {
          return (
            <span key={i} className={`hk ${settled}${isLit ? " on" : ""} hrot`} aria-hidden="true">
              {ROTATE.map((r, k) => (
                <span key={r} className={k === rot ? "ron" : ""}>
                  {r}
                </span>
              ))}
            </span>
          );
        }
        return (
          <span key={i} className={`hk ${settled}${isLit ? " on" : ""}`}>
            {w}
          </span>
        );
      })}
    </h1>
  );
}
