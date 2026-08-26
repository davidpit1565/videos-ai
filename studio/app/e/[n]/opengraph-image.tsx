import { ImageResponse } from "next/og";
import { episode } from "@/lib/site";
import { articleFor } from "@/lib/articles";

export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default async function OG({ params }: { params: Promise<{ n: string }> }) {
  const n = Number((await params).n);
  const e = await episode(n);
  const a = articleFor(n);
  const title = e?.title || a?.title || `Episode ${n}`;

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
        {/* Satori (next/og's renderer) requires explicit display:flex on any node with
            more than one child — a string mixed with an interpolated expression counts
            as two, which is exactly what silently 500'd this route until display was
            added here. */}
        <div
          style={{
            display: "flex",
            fontSize: 26, letterSpacing: 4, textTransform: "uppercase",
            color: "#3DDC97", fontFamily: "Helvetica, Arial, sans-serif", fontWeight: 700,
            marginBottom: 30,
          }}
        >
          Actually Works · Episode {String(n).padStart(2, "0")}
        </div>
        <div style={{ fontSize: 58, lineHeight: 1.18, maxWidth: 1000, fontWeight: 700 }}>{title}</div>
      </div>
    ),
    size,
  );
}
