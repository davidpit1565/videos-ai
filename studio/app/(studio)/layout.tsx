import type { Metadata, Viewport } from "next";
import StudioFonts from "../studio-fonts";

/** shell.tsx used to swap <link rel="manifest"> client-side, after hydration, based on
 *  the current path. That's too late for "Add to Home Screen": the icon he adds from a
 *  studio page kept opening the public site, because the manifest iOS actually reads is
 *  whatever was already in the server-rendered <head> when he tapped it, not whatever a
 *  useEffect mutated in afterward. Every route under this group is a studio page (see
 *  shell.tsx's own TABS list) — giving them a real, server-rendered layout with their own
 *  metadata is what makes the override land before the page ever paints, not a race
 *  against one. The root layout's manifest ("/manifest.json") still applies to every
 *  public page outside this group. */
export const metadata: Metadata = {
  manifest: "/studio.webmanifest",
  appleWebApp: { capable: true, statusBarStyle: "black", title: "Studio" },
};

/** The public site is light, the studio stays dark (rebrand 13.11.2026): the browser bar
 *  follows each surface instead of flashing white above a black tool. */
export const viewport: Viewport = { themeColor: "#0B0B0B" };

export default function StudioLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <StudioFonts />
      {children}
    </>
  );
}
