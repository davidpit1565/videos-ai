import Link from "next/link";
import Mark from "./mark";
import { LINKS, IG_HANDLE, IG_URL } from "./site-social";

/** One footer for every public page, rendered once by Shell. Before the 13.11.2026
 *  rebrand there were five different hand-written footers plus an icon-only social row,
 *  and the Instagram handle was never written out as text anywhere on the site. */
export default function SiteFooter() {
  return (
    <footer className="sitefoot" dir="ltr">
      <div className="sitefoot-in">
        <p className="sitefoot-follow">
          New reels go out on Instagram first:{" "}
          <a href={IG_URL} target="_blank" rel="noopener noreferrer">
            {IG_HANDLE}
          </a>
        </p>
        <nav className="sitefoot-links" aria-label="Footer">
          <Link href="/episodes">Episodes</Link>
          <Link href="/search">Search</Link>
          <Link href="/failure-modes">Failure modes</Link>
          <Link href="/about">About</Link>
          {LINKS.filter((l) => l.name !== "Instagram").map((l) => (
            <a key={l.name} href={l.href} target="_blank" rel="noopener noreferrer">
              {l.name}
            </a>
          ))}
        </nav>
        <p className="sitefoot-brand">
          <Mark size={16} tone="light" />
          <span>Actually Works</span>
        </p>
      </div>
    </footer>
  );
}
