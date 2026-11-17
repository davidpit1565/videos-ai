/** The brand mark, direction A (David, 13.11.2026): the letters A and W, where the second
 *  half of the W is a signal-yellow check. Geometry copied from
 *  channel/brand/logo-A-final/mark-A-*-nofield.svg, not redrawn.
 *
 *  tone="light" is for a light page: ink letters, and the yellow check carries a thin ink
 *  keyline, because #FFE600 on white is only 1.27:1 and disappears without it.
 *  tone="dark" is for a dark surface (the studio): white letters, plain yellow check. */
export default function Mark({ size = 28, tone = "dark" }: { size?: number; tone?: "light" | "dark" }) {
  const ink = tone === "light" ? "#0B0B0B" : "#FFFFFF";
  const w = Math.round((size * 941.5) / 585.7);
  return (
    <svg
      width={w}
      height={size}
      viewBox="0 0 941.5 585.7"
      aria-hidden="true"
      focusable="false"
      style={{ flex: "0 0 auto", display: "block" }}
    >
      <polygon points="40,545.7 128.3,545.7 249.7,145.7 161.4,145.7" fill={ink} />
      <polygon points="161.4,145.7 249.7,145.7 371,545.7 282.8,545.7" fill={ink} />
      <polygon points="164.3,417.9 246.7,417.9 265.7,480.5 145.3,480.5" fill={ink} />
      <polygon points="295.6,145.7 383.9,145.7 505.3,545.7 417,545.7" fill={ink} />
      <polygon points="417,545.7 505.3,545.7 582.5,291.2 538.4,145.7 538.4,145.7" fill={ink} />
      {tone === "light" ? (
        <g fill="#0B0B0B" stroke="#0B0B0B" strokeWidth="51.49" strokeLinejoin="miter" strokeMiterlimit={3}>
          <polygon points="538.4,145.7 626.7,145.7 748,545.7 659.8,545.7" />
          <polygon points="659.8,545.7 748,545.7 901.5,40 813.2,40" />
        </g>
      ) : null}
      <polygon points="538.4,145.7 626.7,145.7 748,545.7 659.8,545.7" fill="#FFE600" />
      <polygon points="659.8,545.7 748,545.7 901.5,40 813.2,40" fill="#FFE600" />
    </svg>
  );
}
