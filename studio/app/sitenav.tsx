import Link from "next/link";
import Image from "next/image";

/** The same header on every public page, because a visitor who lands on one of them
 *  from a caption has no other way to discover the rest. Episode 01 had a full page
 *  written for it and no route to it from the front door. */
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
        <Image className="logo" src="/logo-light.png" alt="" width={28} height={28} priority />
        Actually Works
      </Link>
      <nav className="links">
        {items.map((i) => (
          <Link key={i.href} href={i.href} aria-current={here === i.href ? "page" : undefined}>
            {i.label}
          </Link>
        ))}
      </nav>
    </header>
  );
}
