"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useStudio } from "./providers";
import { useEffect } from "react";
import { isSite } from "@/lib/routes";

const TABS = [
  { href: "/studio", label: "לוח" },
  { href: "/videos", label: "פרקים" },
  { href: "/week", label: "השבוע" },
  { href: "/renders", label: "רנדרים" },
  { href: "/pipeline", label: "צינור" },
  { href: "/agent", label: "סוכן" },
];

/** The funnel pages are public, English and LTR — they must not inherit the studio's
 *  Hebrew chrome, its tab bar or its save badge. Which pages those are comes from
 *  lib/routes.ts; the copy that used to live here is what went stale, so /prompts and
 *  /search rendered inside the studio's tab bar. */

export default function Shell({ children }: { children: React.ReactNode }) {
  const path = usePathname();
  const { mode, saving } = useStudio();
  const site = isSite(path);

  /* Point the installed-app manifest at the studio, but only while a studio page is what is
     on screen. Installing from a public page must never produce an app that opens the private
     tool, which is exactly what a single manifest in the root layout did. */
  useEffect(() => {
    const el = document.querySelector<HTMLLinkElement>('link[rel="manifest"]');
    if (!el) return;
    const want = site ? "/manifest.json" : "/studio.webmanifest";
    if (el.getAttribute("href") !== want) el.setAttribute("href", want);
  }, [site]);

  /* The nav bar "jumping" is 100dvh doing exactly what it is defined to do: recompute as the
   * browser's own address bar collapses and expands while scrolling. Each recompute is a real
   * layout change, so the flex column — and the nav pinned to its bottom — visibly resizes
   * mid-scroll. This was reported on the installed iPhone app AND in a plain Chrome tab, which
   * rules out anything PWA-specific; it is the unit itself.
   *
   * The fix used everywhere this problem gets solved properly: track the LARGEST viewport
   * height actually seen and never shrink back below it. The shell then stays sized for the
   * browser-chrome-hidden case at all times; when the address bar reappears it simply covers
   * the top of that fixed-height box instead of the box resizing under it. Nothing to measure
   * before first paint, so 100dvh stays as the CSS fallback until this runs once. */
  useEffect(() => {
    let max = 0;
    const set = () => {
      const h = window.visualViewport?.height ?? window.innerHeight;
      if (h > max) {
        max = h;
        document.documentElement.style.setProperty("--app-h", `${h}px`);
      }
    };
    set();
    window.visualViewport?.addEventListener("resize", set);
    window.addEventListener("resize", set);
    // A rotation can make the true max height smaller than whatever was recorded in the other
    // orientation, so the ceiling has to reset there rather than just calling set() again.
    const reset = () => { max = 0; set(); };
    window.addEventListener("orientationchange", reset);
    return () => {
      window.visualViewport?.removeEventListener("resize", set);
      window.removeEventListener("resize", set);
      window.removeEventListener("orientationchange", reset);
    };
  }, []);

  if (site) return <>{children}</>;

  const badge =
    mode === "loading"
      ? { cls: "mode", text: "טוען" }
      : mode === "cloud"
        ? { cls: "mode cloud", text: saving ? "שומר…" : "מסד נתונים" }
        : { cls: "mode local", text: "נשמר בדפדפן" };

  return (
    <div className="shell" lang="he" dir="rtl">
      <div className="top">
        <Link className="brand" href="/studio">
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
      {/* Its own scroll container so the tab bar never has to be position:fixed —
          on iOS a fixed bottom bar slides with the address bar as it collapses, which
          is the jump he reported. */}
      <div className="scroll">
        {children}
        <div className="foot">
          Actually Works Studio · המספרים נמשכים מאינסטגרם ומ-Beehiiv כשהמפתחות קיימים,
          ומוצגים כריקים כשלא.
          <br />
          שום מספר במערכת הזאת לא מומצא.
        </div>
      </div>
    </div>
  );
}
