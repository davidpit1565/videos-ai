import type { Metadata, Viewport } from "next";
import "./globals.css";
import { Provider } from "./providers";
import Shell from "./shell";
import { SITE_URL } from "@/lib/site";
import { LINKS } from "./site-social";
import localFont from "next/font/local";

/** Archivo Black (SIL Open Font License 1.1, Omnibus-Type via Google Fonts), self-hosted
 *  from app/fonts so no third-party font request is made on a public page. It has one
 *  weight; declaring the face for 400-900 stops the browser from drawing a fake bold
 *  when a heading rule asks for 700 or 800. Hebrew falls through to the next family. */
const display = localFont({
  src: "./fonts/ArchivoBlack-Regular.ttf",
  weight: "400 900",
  style: "normal",
  display: "swap",
  variable: "--font-display",
  fallback: ["Arial Black", "Helvetica Neue", "Arial", "sans-serif"],
});

const DESCRIPTION =
  "AI setups that actually work: short reels about AI tools, and a page for every episode with the steps.";

export const metadata: Metadata = {
  // Required for Next to turn the opengraph-image.tsx files into absolute URLs in the
  // actual meta tags — without it, a crawler that doesn't resolve relative og:image URLs
  // itself (several don't) sees no image at all.
  metadataBase: new URL(SITE_URL),
  // The document is the public site by default; the studio is one private corner of it.
  // Titling the root "Studio" put the private tool's name in the browser tab, the bookmark
  // and the share card of every public page.
  title: { default: "Actually Works", template: "%s · Actually Works" },
  description: DESCRIPTION,
  // Every page inherits this; a page with its own opengraph-image.tsx (the episode pages)
  // gets that image instead automatically — Next resolves the nearest one per route.
  openGraph: {
    siteName: "Actually Works",
    type: "website",
    title: "Actually Works",
    description: DESCRIPTION,
  },
  twitter: {
    card: "summary_large_image",
    title: "Actually Works",
    description: DESCRIPTION,
  },
  alternates: { types: { "application/rss+xml": "/rss.xml" } },
  // The public manifest, and only that. This line used to point at a manifest named
  // "Actually Works Studio" with start_url "/studio" and a description reading "the
  // channel's control centre" — and it sat in the ROOT layout, so every public page
  // advertised it. A visitor who added the site to their home screen got an app called
  // "Studio" that opened the private tool. The PIN stopped them; the leak was that the
  // tool's existence, name, purpose and URL were broadcast to everyone who visited.
  manifest: "/manifest.json",
  appleWebApp: { capable: true, statusBarStyle: "default", title: "Actually Works" },
  // The dark AW tile (logo direction A, 13.11.2026): a black square reads as a shape of
  // its own on a light or a dark tab, where the light mark turns into a grey smudge at
  // 16 px (channel/brand/logo-A-final/README.md). SVG first for sharp tabs, PNGs after.
  icons: {
    icon: [
      { url: "/icon-mark.svg", type: "image/svg+xml" },
      { url: "/icon-32.png", sizes: "32x32", type: "image/png" },
      { url: "/icon-192.png", sizes: "192x192", type: "image/png" },
      { url: "/icon-512.png", sizes: "512x512", type: "image/png" },
    ],
    apple: [{ url: "/apple-touch-icon.png", sizes: "180x180", type: "image/png" }],
  },
  // Proves ownership of the domain to Google Search Console (URL prefix property,
  // HTML tag method) — required before the site can be indexed or its sitemap submitted.
  verification: { google: "87HZR9bS3bdyxXBokek25fhY1zgzjJwI2ug1qdTMb8A" },
};

export const viewport: Viewport = {
  themeColor: "#FFFFFF",
  width: "device-width",
  initialScale: 1,
  // without this, env(safe-area-inset-bottom) is always 0 and the tab bar sits under
  // the home indicator
  viewportFit: "cover",
};

// Real, verifiable facts only — the same "checkable, not trusted on faith" rule the
// /about page states outright. name/sameAs are the actual profile URLs SiteSocial
// already links to; nothing here is a claim this schema invents on its own.
const personSchema = {
  "@context": "https://schema.org",
  "@type": "Person",
  name: "David Pitchkhadze",
  url: SITE_URL,
  sameAs: LINKS.map((l) => l.href),
};
const siteSchema = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  name: "Actually Works",
  url: SITE_URL,
  description: DESCRIPTION,
  author: { "@type": "Person", name: "David Pitchkhadze" },
  // Honest only because /search actually reads and writes ?q= now (see search.tsx) —
  // a SearchAction pointing at a query param the page silently ignored would be exactly
  // the kind of unverifiable claim CLAUDE.md rules out.
  potentialAction: {
    "@type": "SearchAction",
    target: `${SITE_URL}/search?q={search_term_string}`,
    "query-input": "required name=search_term_string",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" dir="ltr" className={display.variable}>
      <head>
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(personSchema) }} />
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(siteSchema) }} />
        {/* The scroll-reveal sections (app/reveal.tsx) start at opacity:0 in CSS and only
            reach opacity:1 once client JS runs and IntersectionObserver fires — meaning a
            visitor, crawler, or reader mode with JavaScript off would see a near-empty
            page below the hero forever, on every episode's own "what it will not do"
            section included. The text is always in the server HTML either way, but a
            page whose real content is only visually true under JS shouldn't ship quietly
            broken for the one case that can't run it. */}
        <noscript>
          <style>{`.reveal{opacity:1!important;transform:none!important}.reveal::before{display:none!important}`}</style>
        </noscript>
      </head>
      <body>
        <Provider>
          <Shell>{children}</Shell>
        </Provider>
      </body>
    </html>
  );
}
