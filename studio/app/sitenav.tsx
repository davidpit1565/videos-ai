import Link from "next/link";
import Mark from "./mark";

/** The same header on every public page, because a visitor who lands on one of them from
 *  a caption has no other way to discover the rest.
 *
 *  Rebrand 13.11.2026: one row, the AW mark and the name as plain text (Archivo Black, no
 *  box or bar behind either word), and two links. The old header was five pills plus an
 *  icon row, which wrapped to about four rows on a phone before any content. Search,
 *  Failure modes and the social accounts now live in the one shared footer
 *  (site-footer.tsx); the follow link is in the home page's first screen. */
export default function SiteNav({ here }: { here?: string }) {
  const items = [
    { href: "/episodes", label: "Episodes" },
    { href: "/about", label: "About" },
  ];
  return (
    <header className="sitenav">
      <Link className="mark" href="/" aria-label="Actually Works, home">
        <Mark size={22} tone="light" />
        <span>Actually Works</span>
      </Link>
      <nav className="links" aria-label="Site">
        {items.map((i) => (
          <Link key={i.href} href={i.href} aria-current={here === i.href ? "page" : undefined}>
            {i.label}
          </Link>
        ))}
      </nav>
    </header>
  );
}
