import { ImageResponse } from "next/og";
import { displayFont, OgMark } from "./og-parts";

export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

/** The generic share card for any page a per-page image doesn't override (episode pages
 *  do, in app/e/[n]/opengraph-image.tsx). Rebrand 13.11.2026: the light site's own look,
 *  white ground, ink type in Archivo Black, the AW mark. The old card's line "One setup a
 *  week" was wrong (the channel posts several a week) and is gone; the words now are the
 *  site title and the handle, both true. */
export default async function OG() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%", height: "100%", display: "flex", flexDirection: "column",
          justifyContent: "space-between", padding: "72px 80px",
          background: "#FFFFFF", color: "#0B0B0B", fontFamily: "Archivo Black",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 22 }}>
          <OgMark height={64} />
          <div style={{ fontSize: 40 }}>Actually Works</div>
        </div>
        <div style={{ fontSize: 92, lineHeight: 1.02, maxWidth: 1000, letterSpacing: -2 }}>
          AI setups that actually work.
        </div>
        <div style={{ display: "flex", fontSize: 30, color: "#3A3A3A" }}>@actually_works.ai</div>
      </div>
    ),
    { ...size, fonts: await displayFont() },
  );
}
