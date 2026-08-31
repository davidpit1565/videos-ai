/** A second, distinct animation device from the one-time reveals elsewhere on the
 *  page: a continuous ticker, the classic "scrolling band" pattern David pointed at
 *  (dribbble.com/tags/scrolling-animation). Pure CSS — no scroll listener, no client
 *  component — a looping translateX over a doubled list, masked at both edges so the
 *  loop seam never shows. Names come from lib/tools.ts, the same fixed list every
 *  filter chip and track pill on the site already reads from, never a separate list
 *  that could drift out of sync with what "tool" actually means here.
 *
 *  Paused under prefers-reduced-motion via CSS alone (no JS branch needed — see the
 *  animation-name:none rule in globals.css). */
export default function ToolMarquee({ names }: { names: string[] }) {
  return (
    <div className="marquee" aria-hidden="true">
      <div className="marquee-track">
        {[...names, ...names].map((t, i) => (
          <span key={i}>{t}</span>
        ))}
      </div>
    </div>
  );
}
