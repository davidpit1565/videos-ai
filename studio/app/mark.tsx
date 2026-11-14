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

/** The round badge: the same black disc with the white AW and yellow check as the profile
 *  picture (channel/brand/logo-A-final/mark-A-dark.svg, polygons copied unchanged, circle
 *  clip instead of the square field). Same badge on the light site and the dark studio. */
export function Badge({ size = 38 }: { size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 1000 1000"
      aria-hidden="true"
      focusable="false"
      style={{ flex: "0 0 auto", display: "block", borderRadius: "50%" }}
    >
      <circle cx="500" cy="500" r="500" fill="#0B0B0B" />
      <polygon points="161.9,698.5 231.2,698.5 326.5,384.5 257.2,384.5" fill="#FFFFFF" />
      <polygon points="257.2,384.5 326.5,384.5 421.7,698.5 352.5,698.5" fill="#FFFFFF" />
      <polygon points="259.5,598.1 324.2,598.1 339.1,647.2 244.6,647.2" fill="#FFFFFF" />
      <polygon points="362.6,384.5 431.8,384.5 527.1,698.5 457.8,698.5" fill="#FFFFFF" />
      <polygon points="457.8,698.5 527.1,698.5 587.7,498.7 553.1,384.5" fill="#FFFFFF" />
      <polygon points="553.1,384.5 622.4,384.5 717.6,698.5 648.3,698.5" fill="#FFE600" />
      <polygon points="648.3,698.5 717.6,698.5 838.1,301.5 768.8,301.5" fill="#FFE600" />
    </svg>
  );
}
