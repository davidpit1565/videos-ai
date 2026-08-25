/** Which pages are the site and which are the studio — in one place, because three
 *  places was the bug.
 *
 *  This classification lived independently in middleware.ts and in app/shell.tsx, and the
 *  two drifted: /prompts and /search were added to the site, registered with the
 *  middleware so they stopped redirecting to the PIN gate, and never registered with the
 *  Shell. So they loaded — wrapped in the studio's Hebrew right-to-left chrome and its tab
 *  bar. Clicking "Prompts" on the front door landed the visitor in what looked like the
 *  private tool. Same class of mistake three times: adding a page to the site is not the
 *  same as making it reachable, and it is not the same as making it look like the site.
 *
 *  scripts/check-routes.mjs walks app/ and fails the build if a route appears here in
 *  neither list, so the fourth occurrence cannot reach production. */

/** the private tool: the whole business is in here */
export const STUDIO = [
  "/studio", "/videos", "/analytics", "/week", "/pipeline", "/agent", "/renders", "/templates",
  // named separately from the public manifest, and gated like everything else here: a
  // manifest that can be fetched is a manifest that tells a stranger the tool exists
  "/studio.webmanifest",
  "/api/state", "/api/agent", "/api/instagram", "/api/youtube", "/api/beehiiv", "/api/push",
  "/api/ideas-backlog",
  // /api/youtube/callback is under /api/youtube, already listed — Google's redirect back
  // from the consent screen is a same-browser top-level GET, so the "studio" cookie (set
  // sameSite:lax) still rides along and the PIN gate passes normally.
];

/** Neither the site nor the studio: the nightly tracker, called by Vercel's cron with its
 *  own credential rather than a browser cookie. It was a hand-written special case in the
 *  middleware and belonged nowhere, which is exactly the shape of the bug this file exists
 *  to end — so it is a named third case instead of an exception. */
export const CRON = ["/api/track", "/api/health-check"];

/** the public funnel, plus the endpoints those pages call */
export const SITE = [
  "/", "/e", "/p", "/join", "/about", "/prompts", "/search", "/unlock", "/episodes",
  "/skills", "/s",
  "/api/subscribe", "/api/clientlog", "/api/stream-check", "/api/connections",
  "/api/unlock", "/api/site",
  // a visitor's own "notify me about new episodes" device registration — a separate path
  // from the studio's /api/push so it can never be classified alongside it (see the route
  // file's own comment on why the two must never share a path or a send)
  "/api/subscribe-push",
  "/manifest.json", "/icon-", "/apple-touch-icon",
  // the service worker must be fetchable at the root scope or push cannot register
  "/sw.js",
  // crawlers and readers, not browsers with a cookie: Google reading sitemap.xml,
  // Facebook/Twitter/Slack's link-preview bots reading an episode's og-image, an RSS
  // reader polling the feed. None of them carry the studio's PIN cookie, so each one
  // needs to be named here the same way /reels and /logo-light.png already are.
  "/sitemap.xml", "/robots.txt", "/rss.xml", "/opengraph-image",
  // the site header's own logo mark — a visitor's browser fetches this with no studio
  // cookie, same as the icons above; missing from this list, it redirects to /unlock
  // and the browser shows a broken-image placeholder instead of the mark.
  "/logo-light.png",
  // The rendered mp4 files themselves. Every publish (Instagram, its Story, YouTube's
  // upload) fetches this exact URL from outside any browser — no cookie to carry the PIN.
  // Without this, the "video_url" Instagram is told to download redirects to /unlock
  // instead of serving video bytes, and the container comes back status ERROR — which is
  // silent about the real cause because the failure looks like a bad video, not a locked
  // one. These files are also the ones about to be posted publicly regardless.
  "/reels",
];

/** "/" must match only itself — startsWith("/") would publish the entire studio, which is
 *  why the list it replaces carried that warning twice. Everything else matches itself and
 *  anything beneath it. */
function under(path: string, list: string[]): boolean {
  return list.some((p) => {
    if (p === "/") return path === "/";           // exact, always — see the warning above
    if (p.endsWith("-")) return path.startsWith(p); // asset prefixes: /icon-192.png
    return path === p || path.startsWith(p + "/");
  });
}

export const isSite = (path: string) => under(path, SITE);
export const isStudio = (path: string) => under(path, STUDIO);
export const isCron = (path: string) => under(path, CRON);
/** no list claims it: treated as private, and the build check will already have failed */
export const isClassified = (path: string) => isSite(path) || isStudio(path) || isCron(path);
