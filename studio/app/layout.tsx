import type { Metadata, Viewport } from "next";
import "./globals.css";
import { Provider } from "./providers";
import Shell from "./shell";

export const metadata: Metadata = {
  title: "Actually Works — Studio",
  description: "ניהול הערוץ: פרקים, מדדים, הכנסות וסוכן שמסתכל על המספרים",
  manifest: "/manifest.json",
  appleWebApp: { capable: true, statusBarStyle: "black-translucent", title: "Studio" },
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
    <html lang="he" dir="rtl">
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
