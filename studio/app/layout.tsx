import type { Metadata, Viewport } from "next";
import "./globals.css";
import { Provider } from "./providers";
import Shell from "./shell";

export const metadata: Metadata = {
  // The document is the public site by default; the studio is one private corner of it.
  // Titling the root "Studio" put the private tool's name in the browser tab, the bookmark
  // and the share card of every public page.
  title: { default: "Actually Works", template: "%s · Actually Works" },
  description: "AI setups that actually work. One setup per episode: the exact screen, the exact paste, and the part that breaks.",
  // The public manifest, and only that. This line used to point at a manifest named
  // "Actually Works Studio" with start_url "/studio" and a description reading "the
  // channel's control centre" — and it sat in the ROOT layout, so every public page
  // advertised it. A visitor who added the site to their home screen got an app called
  // "Studio" that opened the private tool. The PIN stopped them; the leak was that the
  // tool's existence, name, purpose and URL were broadcast to everyone who visited.
  manifest: "/manifest.json",
  appleWebApp: { capable: true, statusBarStyle: "default", title: "Actually Works" },
};

export const viewport: Viewport = {
  themeColor: "#0A0D12",
  width: "device-width",
  initialScale: 1,
  // without this, env(safe-area-inset-bottom) is always 0 and the tab bar sits under
  // the home indicator
  viewportFit: "cover",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" dir="ltr">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@700;800&family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Newsreader:opsz,wght@6..72,400;6..72,600;6..72,700&display=swap"
        />
      </head>
      <body>
        <Provider>
          <Shell>{children}</Shell>
        </Provider>
      </body>
    </html>
  );
}
