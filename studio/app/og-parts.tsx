import { readFile } from "node:fs/promises";
import { join } from "node:path";

/** Shared pieces of the two share cards (app/opengraph-image.tsx and
 *  app/e/[n]/opengraph-image.tsx): the self-hosted Archivo Black, and the AW mark drawn
 *  from the same polygons as app/mark.tsx (light tone: ink letters, keylined yellow check). */
export async function displayFont() {
  const data = await readFile(join(process.cwd(), "app/fonts/ArchivoBlack-Regular.ttf"));
  return [{ name: "Archivo Black", data, weight: 400 as const, style: "normal" as const }];
}

export function OgMark({ height }: { height: number }) {
  const width = Math.round((height * 941.5) / 585.7);
  return (
    <svg width={width} height={height} viewBox="0 0 941.5 585.7">
      <polygon points="40,545.7 128.3,545.7 249.7,145.7 161.4,145.7" fill="#0B0B0B" />
      <polygon points="161.4,145.7 249.7,145.7 371,545.7 282.8,545.7" fill="#0B0B0B" />
      <polygon points="164.3,417.9 246.7,417.9 265.7,480.5 145.3,480.5" fill="#0B0B0B" />
      <polygon points="295.6,145.7 383.9,145.7 505.3,545.7 417,545.7" fill="#0B0B0B" />
      <polygon points="417,545.7 505.3,545.7 582.5,291.2 538.4,145.7" fill="#0B0B0B" />
      <polygon points="538.4,145.7 626.7,145.7 748,545.7 659.8,545.7" fill="#0B0B0B" stroke="#0B0B0B" strokeWidth="51.49" />
      <polygon points="659.8,545.7 748,545.7 901.5,40 813.2,40" fill="#0B0B0B" stroke="#0B0B0B" strokeWidth="51.49" />
      <polygon points="538.4,145.7 626.7,145.7 748,545.7 659.8,545.7" fill="#FFE600" />
      <polygon points="659.8,545.7 748,545.7 901.5,40 813.2,40" fill="#FFE600" />
    </svg>
  );
}
