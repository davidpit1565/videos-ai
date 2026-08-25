"use client";
import { useEffect } from "react";

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

  return (
    <div className="crash">
      <h1>משהו נשבר בדף הזה</h1>
      <p>זו השגיאה עצמה, ולא הודעה כללית. היא נרשמה גם בשרת.</p>
      <pre>{error.message || "אין הודעה"}</pre>
      {error.digest ? <p className="dg">digest: {error.digest}</p> : null}
      <button onClick={reset}>לנסות שוב</button>
      <p className="dg">
        אם זה חוזר — הדף לא תקין, לא אתה. תשלח לי את השורה שבמסגרת.
      </p>
    </div>
  );
}
