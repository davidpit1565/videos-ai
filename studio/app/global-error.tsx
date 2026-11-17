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

  // English: this replaces the root layout for every page, public ones included, and it
  // cannot know the route before the layout itself has failed. Light, like the site.
  return (
    <html lang="en" dir="ltr">
      <body style={{ margin: 0, background: "#FFFFFF", color: "#0B0B0B",
        fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" }}>
        {!reloading && (
          <div style={{ maxWidth: "40rem", margin: "0 auto", padding: "2.5rem 1.2rem" }}>
            <h1 style={{ fontSize: "1.6rem", lineHeight: 1.2, margin: "0 0 .6rem" }}>
              This page did not load.
            </h1>
            <p style={{ color: "#4A4A4A", lineHeight: 1.6 }}>
              Something went wrong on our side, not yours. It has been logged. Reload the
              page to try again.
            </p>
            <p>
              <a href="/" style={{ color: "#0B0B0B", fontWeight: 700 }}>Go to the home page</a>
            </p>
            {error.digest ? (
              <p style={{ color: "#4A4A4A", fontSize: ".85rem" }}>Reference: {error.digest}</p>
            ) : null}
          </div>
        )}
      </body>
    </html>
  );
}
