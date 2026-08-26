import { ImageResponse } from "next/og";

export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

/** The generic card for any page a per-page image doesn't override (episode pages do,
 *  in app/e/[n]/opengraph-image.tsx). Same palette as the public site itself — near-
 *  black ground, mint accent — so a shared link looks like it came from here even
 *  before the page loads. Helvetica rather than the site's own Space Grotesk: next/og
 *  needs an actual font file fetched at request time to use a Google Font, and a
 *  system fallback is a safer bet than a network fetch on every crawler hit. */
export default function OG() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%", height: "100%", display: "flex", flexDirection: "column",
          justifyContent: "center", padding: "80px",
          background: "#0C0E12", color: "#E8E6E1",
          fontFamily: "Helvetica, Arial, sans-serif",
        }}
      >
        <div
          style={{
            fontSize: 28, letterSpacing: 4, textTransform: "uppercase",
            color: "#3DDC97", fontFamily: "Helvetica, Arial, sans-serif", fontWeight: 700,
            marginBottom: 28,
          }}
        >
          Actually Works
        </div>
        <div style={{ fontSize: 64, lineHeight: 1.15, maxWidth: 980, fontWeight: 700 }}>
          AI setups that actually work.
        </div>
        <div
          style={{
            fontSize: 26, marginTop: 30, color: "#8B8F98",
            fontFamily: "Helvetica, Arial, sans-serif",
          }}
        >
          One setup a week — the exact screen, the exact click.
        </div>
      </div>
    ),
    size,
  );
}
