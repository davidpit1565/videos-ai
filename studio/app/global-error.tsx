"use client";
import { useEffect } from "react";

/** app/error.tsx covers the page subtree but NOT app/layout.tsx — and the provider and
 *  the chrome both render inside the layout. A throw in either of those still showed
 *  Next's bare "Application error", and the reporting boundary never ran, so its silence
 *  in the logs proved nothing. This one covers the layout, which means the absence of a
 *  report is now real information.
 *
 *  Same stale-chunk auto-reload as app/error.tsx, and for the same reason: this boundary
 *  catches a throw from the layout/provider tree, which is just as reachable by a chunk
 *  that a newer deploy has already deleted from the CDN. */
function isChunkLoadError(error: Error): boolean {
  return error.name === "ChunkLoadError" || /Loading chunk [\w-]+ failed/.test(error.message);
}

export default function GlobalError({
  error,
}: {
  error: Error & { digest?: string };
}) {
  useEffect(() => {
    if (isChunkLoadError(error)) {
      const key = "chunk-reload-" + (typeof location === "undefined" ? "" : location.pathname) + "-global";
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
        path: (typeof location === "undefined" ? "" : location.pathname) + " [layout]",
      }),
    }).catch(() => {});
  }, [error]);

  // Same reasoning as app/error.tsx: this renders once, a tick before the effect above
  // reloads the tab, and a blank body for that one tick beats a "the page broke" screen
  // for what is almost always just a stale chunk.
  const reloading =
    isChunkLoadError(error) &&
    typeof sessionStorage !== "undefined" &&
    !sessionStorage.getItem(
      "chunk-reload-" + (typeof location === "undefined" ? "" : location.pathname) + "-global",
    );

  return (
    <html lang="he" dir="rtl">
      <body style={{ margin: 0, background: "#0A0D12", color: "#EAE6DC",
        fontFamily: "system-ui, sans-serif" }}>
        {!reloading && (
          <div style={{ maxWidth: "40rem", margin: "0 auto", padding: "2.5rem 1.2rem" }}>
            <h1 style={{ fontSize: "1.5rem", margin: "0 0 .5rem" }}>
              הדף נשבר לפני שהוא נטען
            </h1>
            <p style={{ color: "#8B8579" }}>
              זו השגיאה עצמה. היא נרשמה גם בשרת.
            </p>
            <pre style={{ whiteSpace: "pre-wrap", background: "rgba(220,80,60,.12)",
              border: "1px solid rgba(220,80,60,.35)", borderRadius: ".45rem",
              padding: ".9rem 1rem", fontSize: ".85rem", overflowX: "auto" }}>
              {error.message || "אין הודעה"}
            </pre>
            {error.digest ? (
              <p style={{ color: "#8B8579", fontSize: ".85rem" }}>digest: {error.digest}</p>
            ) : null}
          </div>
        )}
      </body>
    </html>
  );
}
