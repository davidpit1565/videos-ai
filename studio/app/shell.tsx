"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useStudio } from "./providers";

const TABS = [
  { href: "/", label: "לוח" },
  { href: "/videos", label: "פרקים" },
  { href: "/pipeline", label: "צינור" },
  { href: "/agent", label: "סוכן" },
];

/** The funnel pages are public, English and LTR — they must not inherit the studio's
 *  Hebrew chrome, its tab bar or its save badge. */
const PUBLIC = ["/join", "/p/", "/unlock"];

export default function Shell({ children }: { children: React.ReactNode }) {
  const path = usePathname();
  const { mode, saving } = useStudio();

  if (PUBLIC.some((p) => path.startsWith(p))) return <>{children}</>;

  const badge =
    mode === "loading"
      ? { cls: "mode", text: "טוען" }
      : mode === "cloud"
        ? { cls: "mode cloud", text: saving ? "שומר…" : "מסד נתונים" }
        : { cls: "mode local", text: "נשמר בדפדפן" };

  return (
    <div className="shell">
      <div className="top">
        <Link className="brand" href="/">
          <span className="tick" />
          <b>Actually Works</b>
        </Link>
        <span className={badge.cls}>{badge.text}</span>
      </div>
      <nav>
        {TABS.map((t) => (
          <Link key={t.href} href={t.href} aria-current={path === t.href ? "page" : undefined}>
            {t.label}
          </Link>
        ))}
      </nav>
      {children}
      <div className="foot">
        Actually Works Studio · המספרים נמשכים מאינסטגרם ומ-Beehiiv כשהמפתחות קיימים, ומוצגים כריקים כשלא.
        <br />
        שום מספר במערכת הזאת לא מומצא.
      </div>
    </div>
  );
}
