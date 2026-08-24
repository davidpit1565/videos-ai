"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useStudio } from "./providers";
import { useEffect, useState } from "react";
import { isSite } from "@/lib/routes";
import { localDT } from "@/lib/fmt";
import SiteSocial from "./site-social";

const TABS = [
  { href: "/studio", label: "לוח" },
  { href: "/videos", label: "פרקים" },
  { href: "/analytics", label: "התקדמות" },
  { href: "/week", label: "השבוע" },
  { href: "/renders", label: "רנדרים" },
  { href: "/templates", label: "תבניות" },
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

  /* He asked directly: he cannot tell whether the page in front of him is the current
   * deploy without asking. This is the answer — the real commit this build was made
   * from, written at build time by scripts/write-build-info.mjs, not a guess. */
  const [buildInfo, setBuildInfo] = useState<{ sha: string | null; shortSha: string | null; builtAt: string } | null>(null);
  useEffect(() => {
    fetch("/build-info.json")
      .then((r) => (r.ok ? r.json() : null))
      .then(setBuildInfo)
      .catch(() => {});
  }, []);

  /* Point the installed-app manifest at the studio, but only while a studio page is what is
     on screen. Installing from a public page must never produce an app that opens the private
     tool, which is exactly what a single manifest in the root layout did. */
  useEffect(() => {
    const el = document.querySelector<HTMLLinkElement>('link[rel="manifest"]');
    if (!el) return;
    const want = site ? "/manifest.json" : "/studio.webmanifest";
    if (el.getAttribute("href") !== want) el.setAttribute("href", want);
  }, [site]);

  /* The nav bar "jumping" was 100dvh doing exactly what it is defined to do: recompute as
   * the browser's own address bar collapses and expands while scrolling. Two rounds of a
   * JS fix (track the largest viewport height ever seen, in --app-h) killed the jump but
   * chased its own tail on the installed iOS app: no address bar there to fire the resize
   * event the fix leaned on, so whatever height the first measurement caught — sometimes
   * before the launch animation had settled — locked in permanently as a gap under the nav
   * bar, and no amount of retried delays is a real fix for a race.
   *
   * The actual fix is a CSS unit for exactly this: `lvh` is the LARGE viewport height — the
   * size with browser chrome retracted — fixed at layout time and never recomputed as the
   * chrome animates. No measurement, no race, no JS at all. See globals.css. */

  if (site)
    return (
      <>
        {children}
        <SiteSocial />
      </>
    );

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
        <div className="top-right">
          <span className={badge.cls}>{badge.text}</span>
          {buildInfo && (
            <span className="build-info" title={buildInfo.sha ?? undefined}>
              עודכן {localDT(buildInfo.builtAt)}
              {buildInfo.shortSha ? ` · ${buildInfo.shortSha}` : ""}
            </span>
          )}
        </div>
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
