"use client";

import { useEffect } from "react";

/** Two interaction-only motion details for the homepage, picked deliberately narrow —
 *  the hero already spends this page's "one bold moment" on the karaoke headline reveal
 *  (see hero-headline.tsx's own comment), and an ambient 9s glow pulse was already tried
 *  and removed here for reading as "trying hard" rather than calm. Both effects below
 *  only move in response to an actual cursor, never on a timer, so they add nothing to
 *  look at until someone is already interacting — same restraint, applied to hover
 *  instead of load.
 *
 *  1. Card spotlight: a soft brass glow that follows the cursor inside an episode/track
 *     card, on top of the border-color + lift hover already there. Common on premium
 *     SaaS marketing pages (Linear, Vercel, Stripe) and, notably, absent everywhere on
 *     this site until now.
 *  2. Magnetic CTA: the primary "Browse episodes" button leans a few px toward the
 *     cursor as it approaches, then springs back on leave — capped small deliberately,
 *     this is a nudge, not a chase. It's the one button the whole page points at, so
 *     it's the one that gets the extra attention.
 *
 *  Both are desktop-only (a touch device has no cursor to react to, and would risk a
 *  card or button stuck mid-transform with nothing to reset it) and skipped entirely
 *  under prefers-reduced-motion, same rule as every other motion device already on this
 *  page. Delegated to two listeners on `main.site` rather than one per card/button —
 *  the card grid can hold any number of episodes without adding a listener per card. */
export default function PremiumMotion() {
  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
    const root = document.querySelector<HTMLElement>("main.site");
    if (!root) return;

    function onMove(e: PointerEvent) {
      const card = (e.target as HTMLElement).closest<HTMLElement>(".eps a, .tracks a");
      if (card) {
        const r = card.getBoundingClientRect();
        card.style.setProperty("--mx", `${e.clientX - r.left}px`);
        card.style.setProperty("--my", `${e.clientY - r.top}px`);
      }
      const cta = (e.target as HTMLElement).closest<HTMLElement>(".herocta .cta");
      if (cta) {
        const r = cta.getBoundingClientRect();
        const cx = r.left + r.width / 2;
        const cy = r.top + r.height / 2;
        // Capped to a few px — a nudge toward the cursor, not a chase. Divided down
        // from the raw offset so the pull is strongest near the button's own edge and
        // never drags it further than it can spring back from smoothly.
        const dx = Math.max(-6, Math.min(6, (e.clientX - cx) / 4));
        const dy = Math.max(-4, Math.min(4, (e.clientY - cy) / 4));
        cta.style.setProperty("--mtx", `${dx.toFixed(1)}px`);
        cta.style.setProperty("--mty", `${dy.toFixed(1)}px`);
      }
    }
    function onLeaveCta(e: PointerEvent) {
      const cta = (e.target as HTMLElement).closest<HTMLElement>(".herocta .cta");
      if (cta) {
        cta.style.setProperty("--mtx", "0px");
        cta.style.setProperty("--mty", "0px");
      }
    }
    root.addEventListener("pointermove", onMove);
    root.addEventListener("pointerleave", onLeaveCta, true);
    return () => {
      root.removeEventListener("pointermove", onMove);
      root.removeEventListener("pointerleave", onLeaveCta, true);
    };
  }, []);

  return null;
}
