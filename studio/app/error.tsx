"use client";
import { useEffect } from "react";
import { usePathname } from "next/navigation";
import { isStudio } from "@/lib/routes";

/** Next's default crash screen says "a client-side exception has occurred" and nothing
 *  else — no message, no line, nothing to act on. This replaces it with the actual
 *  error, and reports it to the server so it lands in the runtime logs too.
 *
 *  A stale tab loading a JS chunk that a newer deploy already deleted from the CDN looks,
 *  to Next, exactly like a real crash — and on a project shipping several deploys a day
 *  that is not a rare case, it is the likely one. The fix is a reload, not a scary screen
 *  and a button asking the visitor to diagnose it themselves. One reload only, tracked in
 *  sessionStorage: a chunk error that survives a fresh load is a real crash, not a stale
 *  tab, and must show the real message rather than reload forever. */
function isChunkLoadError(error: Error): boolean {
  return error.name === "ChunkLoadError" || /Loading chunk [\w-]+ failed/.test(error.message);
}

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  const path = usePathname();
  useEffect(() => {
    if (isChunkLoadError(error)) {
      const key = "chunk-reload-" + (typeof location === "undefined" ? "" : location.pathname);
      if (!sessionStorage.getItem(key)) {
        sessionStorage.setItem(key, "1");
        location.reload();
        return;
      }
    }
    fetch("/api/clientlog", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        message: error.message,
        stack: error.stack,
        digest: error.digest,
        path: typeof location === "undefined" ? "" : location.pathname,
      }),
    }).catch(() => {
      /* reporting a crash must never cause one */
    });
  }, [error]);

  // The reload above fires from an effect, a tick after this first render — so this
  // still has to render *something* for that one tick, and the scary crash screen is
  // the wrong thing to show for what is, in the overwhelming majority of cases, a tab
  // that's simply a few seconds out of date.
  if (isChunkLoadError(error) && typeof sessionStorage !== "undefined") {
    const key = "chunk-reload-" + (typeof location === "undefined" ? "" : location.pathname);
    if (!sessionStorage.getItem(key)) return null;
  }

  // The studio is David's own Hebrew tool and keeps the raw message he can send on.
  // Every other page is the English site: a visitor gets a plain sentence and a retry,
  // never Hebrew and never a stack message (site audit 13.11.2026, finding 1).
  if (path && isStudio(path)) {
    return (
      <div className="crash" lang="he" dir="rtl">
        <h1>משהו נשבר בדף הזה</h1>
        <p>זו השגיאה עצמה, ולא הודעה כללית. היא נרשמה גם בשרת.</p>
        <pre>{error.message || "אין הודעה"}</pre>
        {error.digest ? <p className="dg">digest: {error.digest}</p> : null}
        <button className="btn" onClick={reset}>לנסות שוב</button>
        <p className="dg">אם זה חוזר, הדף לא תקין, לא אתה. תשלח לי את השורה שבמסגרת.</p>
      </div>
    );
  }

  return (
    <main className="site" dir="ltr">
      <h1>This page did not load.</h1>
      <p className="lede">
        Something went wrong on our side, not yours. It has been logged. Try again, or open
        the episode list.
      </p>
      <p className="actions-row">
        <button className="button solid" onClick={reset}>
          Try again
        </button>
        <a className="button" href="/episodes">
          All episodes
        </a>
      </p>
      {error.digest ? <p className="fine">Reference: {error.digest}</p> : null}
    </main>
  );
}
