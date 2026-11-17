import { ImageResponse } from "next/og";
import { episode } from "@/lib/site";
import { articleFor } from "@/lib/articles";
import { displayFont, OgMark } from "../../og-parts";

export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

/** One episode's share card, also used as the thumbnail on /episodes. Light, like the
 *  site (rebrand 13.11.2026). The title size steps down for long titles so the longest
 *  real ones still fit in four lines. */
export default async function OG({ params }: { params: Promise<{ n: string }> }) {
  const n = Number((await params).n);
  const e = await episode(n);
  const a = articleFor(n);
  const title = e?.title || a?.title || `Episode ${n}`;
  const fontSize = title.length > 90 ? 50 : title.length > 60 ? 60 : 72;

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%", height: "100%", display: "flex", flexDirection: "column",
          justifyContent: "space-between", padding: "64px 80px",
          background: "#FFFFFF", color: "#0B0B0B", fontFamily: "Archivo Black",
        }}
      >
        {/* Satori needs display:flex on any node with more than one child, and a string
            mixed with an interpolated expression counts as two. */}
        <div style={{ display: "flex", fontSize: 34 }}>Episode {String(n)}</div>
        <div style={{ display: "flex", fontSize, lineHeight: 1.06, maxWidth: 1040, letterSpacing: -1 }}>
          {title}
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 18, fontSize: 28 }}>
          <OgMark height={44} />
          <div style={{ display: "flex" }}>Actually Works</div>
          <div style={{ display: "flex", color: "#3A3A3A", marginLeft: 12 }}>@actually_works.ai</div>
        </div>
      </div>
    ),
    { ...size, fonts: await displayFont() },
  );
}
