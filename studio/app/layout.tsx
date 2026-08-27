import type { Metadata, Viewport } from "next";
import "./globals.css";
import { Provider } from "./providers";
import Shell from "./shell";
import { SITE_URL } from "@/lib/site";
import { LINKS } from "./site-social";

const DESCRIPTION =
  "AI setups that actually work. One setup per episode: the exact screen, the exact paste, and the part that breaks.";

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
  // The same brass checkmark already used as the PWA icon — there was no favicon at all
  // before this, so every browser tab and bookmark showed a blank page icon.
  icons: {
    icon: [
      { url: "/icon-192.png", sizes: "192x192", type: "image/png" },
      { url: "/icon-512.png", sizes: "512x512", type: "image/png" },
    ],
    apple: "/icon-192.png",
  },
  // Proves ownership of the domain to Google Search Console (URL prefix property,
  // HTML tag method) — required before the site can be indexed or its sitemap submitted.
  verification: { google: "87HZR9bS3bdyxXBokek25fhY1zgzjJwI2ug1qdTMb8A" },
};

export const viewport: Viewport = {
  themeColor: "#0A0D12",
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
    <html lang="en" dir="ltr">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@700;800&family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600;700;800&family=Archivo:wght@700&family=Assistant:wght@400;600;700&display=swap"
        />
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
