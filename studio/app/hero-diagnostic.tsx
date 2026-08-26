/** Fills the hero's own right-hand column when there's no video to show yet — that
 *  column used to render nothing at all in that case, leaving a bare gap beside the
 *  headline on any screen wide enough for the two-column layout. Not a stock
 *  illustration: a literal small "diagnostic readout," the same idea the channel's own
 *  "Won't:" signal already carries into words — most points pass (steel), one is
 *  flagged (clay), same two-color system the rest of the site now uses for exactly
 *  that distinction. */
export default function HeroDiagnostic() {
  return (
    <div className="herodiag" aria-hidden="true">
      <div className="herodiag-label">SETUP.LOG</div>
      <svg viewBox="0 0 320 160" width="100%" height="100%" fill="none">
        <polyline
          points="8,120 48,80 88,96 128,40 168,64 208,24 248,52 312,20"
          stroke="var(--gold)"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <circle cx="48" cy="80" r="4" fill="var(--steel)" />
        <circle cx="128" cy="40" r="4" fill="var(--steel)" />
        <circle cx="168" cy="64" r="4.5" fill="var(--clay)" />
        <circle cx="248" cy="52" r="4" fill="var(--steel)" />
      </svg>
      {/* Real site copy, not invented example data — the same three words the hero
          text beside this already uses, never a fabricated pass/fail claim about any
          specific setup. */}
      <div className="herodiag-caption">EXACT SCREEN · EXACT PASTE · WHAT BREAKS</div>
    </div>
  );
}
