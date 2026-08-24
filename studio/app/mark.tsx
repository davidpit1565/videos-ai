/** The brand mark: four rising bars on a baseline — a level meter that also reads as a
 *  measured result. Replaces the checkmark, which said "trust us" instead of "we
 *  measured it" — the wrong claim for a channel whose whole premise is that nothing
 *  ships without a number behind it. */
export default function Mark({ size = 20 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 120 120" aria-hidden="true" style={{ flex: "0 0 auto" }}>
      <rect x="20" y="86" width="13" height="16" rx="6.5" fill="var(--brass)" opacity=".4" />
      <rect x="40" y="66" width="13" height="36" rx="6.5" fill="var(--brass)" opacity=".6" />
      <rect x="60" y="44" width="13" height="58" rx="6.5" fill="var(--brass)" opacity=".8" />
      <rect x="80" y="18" width="13" height="84" rx="6.5" fill="var(--brass)" />
    </svg>
  );
}
