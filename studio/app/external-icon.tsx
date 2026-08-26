/** A raw "↗" character was standing in for "this opens somewhere else" everywhere on
 *  the public site — plain text, not an icon, so a phone's own emoji font renders it as
 *  a boxed, colored glyph that doesn't belong to this site's visual system at all (see
 *  the screenshot that flagged this: a blue arrow in a white rounded square, sitting
 *  next to hand-drawn SVG icons everywhere else on the page). One small vector arrow,
 *  drawn the same way the social icons already are, replaces every one of those. */
export default function ExternalIcon({ className = "" }: { className?: string }) {
  return (
    <svg
      className={`ext-icon${className ? ` ${className}` : ""}`}
      viewBox="0 0 16 16"
      width="11"
      height="11"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M6.5 4h5.5v5.5" />
      <path d="M12 4 4 12" />
    </svg>
  );
}
