import Link from "next/link";
import { SocialIcons } from "./site-social";

/** The same header on every public page, because a visitor who lands on one of them
 *  from a caption has no other way to discover the rest. Episode 01 had a full page
 *  written for it and no route to it from the front door.
 *
 *  The real accounts (Instagram/YouTube/Facebook) used to live only in the page footer
 *  — real, but invisible unless a visitor scrolled to the very bottom of a long episode
 *  page, which read as "the links are gone." They're in the header now, next to the
 *  nav, so they're on screen from the first paint on every public page. The footer
 *  keeps its own full row too (with the Agently credit) — this one is deliberately
 *  icon-only, so it doesn't crowd the nav links it sits beside. */
export default function SiteNav({ here }: { here?: string }) {
  const items = [
    { href: "/", label: "Home" },
    { href: "/episodes", label: "Episodes" },
    { href: "/prompts", label: "Prompts" },
    { href: "/skills", label: "Skills" },
    { href: "/search", label: "Search" },
    { href: "/about", label: "About" },
  ];
  return (
    <header className="sitenav">
      <Link className="mark" href="/">
        {/* eslint-disable-next-line @next/next/no-img-element -- a small, rarely-changing
            static asset; the image optimizer's own cache showed a broken image on a device
            that hit the URL before this file's first deploy finished, and never recovered.
            A plain img always re-fetches the real static file, no separate cache to go stale. */}
        <img className="logo" src="/logo-light.png" alt="" width={28} height={28} />
        Actually Works
      </Link>
      <div className="sitenav-right">
        <nav className="links">
          {items.map((i) => (
            <Link key={i.href} href={i.href} aria-current={here === i.href ? "page" : undefined}>
              {i.label}
            </Link>
          ))}
        </nav>
        <SocialIcons size={17} />
      </div>
    </header>
  );
}
