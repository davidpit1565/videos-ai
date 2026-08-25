import { ImageResponse } from "next/og";

export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

/** The generic card for any page a per-page image doesn't override (episode pages do,
 *  in app/e/[n]/opengraph-image.tsx). Same palette as the public site itself — cream
 *  paper, brass accent, serif headline — so a shared link looks like it came from here
 *  even before the page loads. Georgia rather than the site's own Newsreader: next/og
 *  needs an actual font file fetched at request time to use a Google Font, and a
 *  fallback that's already in the site's own CSS stack is a safer bet than a network
 *  fetch on every crawler hit. */
export default function OG() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%", height: "100%", display: "flex", flexDirection: "column",
          justifyContent: "center", padding: "80px",
          background: "#F7F5F1", color: "#16181C",
          fontFamily: "Georgia, serif",
        }}
      >
        <div
          style={{
            fontSize: 28, letterSpacing: 4, textTransform: "uppercase",
            color: "#8A6D1B", fontFamily: "Helvetica, Arial, sans-serif", fontWeight: 700,
            marginBottom: 28,
          }}
        >
          Actually Works
        </div>
        <div style={{ fontSize: 64, lineHeight: 1.15, maxWidth: 980 }}>
          AI setups that actually work.
        </div>
        <div
          style={{
            fontSize: 26, marginTop: 30, color: "#54514B",
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
