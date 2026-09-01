import { loadState } from "./db";
import { Episode } from "./types";
import { realTitleFor } from "./reels";

// The real domain, bought and connected 26.8 — the fallback for every place that needs
// the site's own absolute URL (sitemap, RSS, OG images, the publish flow) when neither
// env var below is set. Confirmed live by fetching it directly, not from the Vercel
// project's domains list, which was still stale when this changed — a fresh deploy or
// a manual re-check is what would show it there, not a hard requirement to wait on
// before this constant is safe to update. Old captions already shipped still point at
// actually-works-studio.vercel.app in their own text on Instagram/YouTube — Vercel
// keeps serving that domain for the project regardless, so those links don't break.
const KNOWN_DOMAIN = "actually-works.com";
export const SITE_URL = `https://${(
  process.env.NEXT_PUBLIC_SITE_URL ||
  process.env.VERCEL_PROJECT_PRODUCTION_URL ||
  KNOWN_DOMAIN
).replace(/^https?:\/\//, "")}`;

/** What a visitor is allowed to see: episodes that are actually live, newest first.
 *  Nothing else from the state crosses this line — the studio holds revenue, client
 *  notes and unpublished plans, and none of that belongs on a public page. */
export type PublicEpisode = {
  number: number;
  title: string;
  topic: string;
  notes: string;
  ytVideoId: string | null;
  igPermalink: string | null;
  views: number | null;
  publishedAt: string | null;
};

const toPublic = (e: Episode): PublicEpisode => ({
  number: e.number,
  title: realTitleFor(e.number) || e.title,
  topic: e.topic,
  notes: e.notes,
  ytVideoId: e.ytVideoId,
  views: e.views ?? null,
  igPermalink: e.igPermalink ?? null,
  publishedAt: e.publishedAt,
});

export async function published(): Promise<PublicEpisode[]> {
  const s = await loadState();
  const eps = s?.episodes ?? [];
  return eps
    .filter((e) => e.status === "live")
    .sort((a, b) => b.number - a.number)
    .map(toPublic);
}

export async function episode(n: number): Promise<PublicEpisode | null> {
  return (await published()).find((e) => e.number === n) ?? null;
}

/** One list of everything a visitor can read, whatever it was written in.
 *
 *  The home page used to show only episodes the studio had marked live, so episode 01
 *  — finished, with a full page written for it — was unreachable from the front door.
 *  A visitor arriving from a caption link could read it and nobody else could find it.
 *
 *  Ordered by episode number, newest first — a views-first ranking used to sort here
 *  ("show the ones that did best"), but with only a handful of episodes and views only
 *  on some of them, it blended two different orders into one and read as scrambled, not
 *  ranked. He said so directly. Real per-episode performance still lives on /videos in
 *  the studio and drives what gets made next — it just isn't this list's sort key. */
export type Entry = {
  n: number;
  title: string;
  blurb: string;
  views: number | null;
  live: boolean;
  ytVideoId: string | null;
  igPermalink: string | null;
  /** Real publish date, only for an episode the studio actually marked live — an
   *  article-only entry has none, because nothing has actually gone out yet. Lets a
   *  list read as real chronology (see God of Prompt's dated timeline, adapted here)
   *  instead of an undated stack. */
  publishedAt: string | null;
};

export async function catalogue(): Promise<Entry[]> {
  const { ARTICLES } = await import("./articles");
  const s = await loadState();
  const live = (s?.episodes ?? []).filter((e) => e.status === "live");
  const byNumber = new Map<number, Entry>();

  for (const a of ARTICLES) {
    byNumber.set(a.n, {
      n: a.n, title: a.title, blurb: a.standfirst,
      views: null, live: false, ytVideoId: null, igPermalink: null,
      publishedAt: null,
    });
  }
  for (const e of live) {
    const prev = byNumber.get(e.number);
    byNumber.set(e.number, {
      n: e.number,
      title: realTitleFor(e.number) || e.title || prev?.title || `Episode ${e.number}`,
      blurb: e.topic || prev?.blurb || "",
      views: e.views ?? null,
      live: true,
      ytVideoId: e.ytVideoId ?? null,
      igPermalink: e.igPermalink ?? null,
      publishedAt: e.publishedAt ?? null,
    });
  }
  // Listed only once it is actually live — an article gets written in the same commit
  // that ships the render, well before the reel is actually posted to Instagram or
  // YouTube, and the merge above used to leave every article-only entry in the list
  // regardless. That surfaced episode 19 on /episodes and the home page's "Recent
  // episodes" the same day it was built, hours before it went out anywhere. The merge
  // itself stays as-is (an article still enriches a live DB record's title/blurb) —
  // only the final visible list is cut down to what a visitor could actually go watch.
  return [...byNumber.values()]
    .filter((e) => e.live)
    .sort((a, b) => b.n - a.n);
}
