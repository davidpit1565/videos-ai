"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { useStudio } from "./providers";
import { Suspense, useEffect, useState } from "react";
import { isSite } from "@/lib/routes";
import { localDT } from "@/lib/fmt";
import SiteSocial from "./site-social";
import Mark from "./mark";

/** ?debug=1 on any studio page — reads the actual numbers behind the nav-bar-gap report
 *  straight off this device's own DOM, instead of another guess from a screenshot. Env
 *  vars named on the page: safe-area-inset-bottom (0 means this browser context isn't
 *  giving one at all — standalone/PWA only, a plain browser tab doesn't need it and
 *  Safari already handles the home indicator there), the shell's actual height against
 *  window.innerHeight (a real gap under nav means the shell is taller than the visible
 *  area), and the nav's own bounding box. Screenshot this box and that's the real state,
 *  not a photo of pixels open to interpretation. */
/** useSearchParams() opts its caller out of static rendering unless wrapped in Suspense —
 *  this tiny wrapper contains that bailout to just the debug overlay instead of forcing
 *  every studio page (Shell wraps all of them) into dynamic rendering. */
function NavDebugGate() {
  const params = useSearchParams();
  if (params.get("debug") !== "1") return null;
  return <NavDebug />;
}

function NavDebug() {
  const [info, setInfo] = useState<Record<string, string> | null>(null);
  useEffect(() => {
    const read = () => {
      const nav = document.querySelector(".shell:not(.pub) nav");
      const shell = document.querySelector(".shell");
      const probe = document.createElement("div");
      probe.style.cssText = "position:fixed;bottom:0;left:0;height:env(safe-area-inset-bottom);width:1px;visibility:hidden";
      document.body.appendChild(probe);
      const inset = getComputedStyle(probe).height;
      document.body.removeChild(probe);
      const navRect = nav?.getBoundingClientRect();
      const shellRect = shell?.getBoundingClientRect();
      setInfo({
        "safe-area-inset-bottom": inset,
        "window.innerHeight": String(window.innerHeight),
        "shell height": shellRect ? shellRect.height.toFixed(0) : "—",
        "shell bottom": shellRect ? shellRect.bottom.toFixed(0) : "—",
        "nav bottom": navRect ? navRect.bottom.toFixed(0) : "—",
        "nav top": navRect ? navRect.top.toFixed(0) : "—",
        "gap under nav (viewport − nav bottom)": navRect ? (window.innerHeight - navRect.bottom).toFixed(0) : "—",
        standalone: String(window.matchMedia("(display-mode: standalone)").matches),
      });
    };
    read();
    window.addEventListener("resize", read);
    return () => window.removeEventListener("resize", read);
  }, []);
  if (!info) return null;
  return (
    <div
      style={{
        position: "fixed", insetInlineStart: 8, top: 8, zIndex: 9999,
        background: "#000", color: "#0f0", font: "11px/1.5 monospace",
        padding: "8px 10px", borderRadius: 6, direction: "ltr", textAlign: "left",
        maxWidth: "60vw", pointerEvents: "none",
      }}
    >
      {Object.entries(info).map(([k, v]) => (
        <div key={k}>
          {k}: {v}
        </div>
      ))}
    </div>
  );
}

const TABS = [
  { href: "/studio", label: "לוח" },
  { href: "/videos", label: "רילים" },
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

  /* The manifest swap used to happen here, client-side, after hydration — too late for
     "Add to Home Screen" on iOS, which reads whatever was already server-rendered. Every
     studio route now has its own layout (app/(studio)/layout.tsx) exporting the studio
     manifest as real metadata, so it's correct in the very first response and Next's own
     App Router metadata handling keeps it correct across client-side navigation too —
     see that file for why. */

  /* He reported the gap under the nav bar again, on the device itself — every guess so far
   * has come from a screenshot, and a screenshot can't show env(safe-area-inset-bottom) or
   * which viewport unit his exact browser actually resolved. Guessing at more CSS without
   * that number is how the last "fix" made a different thing worse. ?debug=1 reads it
   * straight off the real DOM, once, instead — see NavDebug below. */

  /* The nav bar "jumping" was 100dvh doing exactly what it is defined to do: recompute as
   * the browser's own address bar collapses and expands while scrolling. Two rounds of a
   * JS fix (track the largest viewport height ever seen, in --app-h) killed the jump but
   * chased its own tail on the installed iOS app: no address bar there to fire the resize
   * event the fix leaned on, so whatever height the first measurement caught — sometimes
   * before the launch animation had settled — locked in permanently as a gap under the nav
   * bar, and no amount of retried delays is a real fix for a race.
   *
   * A CSS unit fixes the recompute-jump with no JS at all — but `lvh` (chrome fully
   * retracted, the TALLEST reading) was the wrong one of the three to pick: it stayed
   * taller than the real visible area for as long as the chrome hadn't yet collapsed,
   * which is the normal state on first load — and .shell clips its own overflow, so that
   * extra height was the nav bar itself pushed below the fold, not spare scroll room.
   * `svh` (chrome fully expanded, the SHORTEST reading) is now used instead: it's
   * guaranteed to fit inside the visible area regardless of chrome state, so the bar is
   * never the thing that goes missing — worst case is a harmless gap of background below
   * it once the chrome does collapse. See globals.css. */

  if (site)
    return (
      <>
        {/* A thin brass line that fills with the page's own scroll position — the same
         *  progress bar every reel already draws across the top of its own frame
         *  (export/*.html's .prog), just tied to this page's scroll instead of a video's
         *  playhead. Pure CSS (animation-timeline: scroll()), so browsers without support
         *  simply never grow it — no JS, nothing to break. */}
        <div className="scrollrail" data-decor />
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
      <Suspense fallback={null}>
        <NavDebugGate />
      </Suspense>
      <div className="top">
        <Link className="brand" href="/studio">
          <Mark />
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
