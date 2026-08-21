import { loadState } from "./db";
import { Episode } from "./types";

/** What a visitor is allowed to see: episodes that are actually live, newest first.
 *  Nothing else from the state crosses this line — the studio holds revenue, client
 *  notes and unpublished plans, and none of that belongs on a public page. */
export type PublicEpisode = {
  number: number;
  title: string;
  topic: string;
  notes: string;
  ytVideoId: string | null;
  publishedAt: string | null;
};

const toPublic = (e: Episode): PublicEpisode => ({
  number: e.number,
  title: e.title,
  topic: e.topic,
  notes: e.notes,
  ytVideoId: e.ytVideoId,
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
 *  Ranked by views when views exist, and by episode number when they do not, which is
 *  the honest version of "show the ones that did best": with nothing published there is
 *  nothing to rank, and inventing an order would be worse than admitting that. */
export type Entry = {
  n: number;
  title: string;
  blurb: string;
  views: number | null;
  live: boolean;
  ytVideoId: string | null;
  igMediaId: string | null;
};

export async function catalogue(): Promise<Entry[]> {
  const { ARTICLES } = await import("./articles");
  const s = await loadState();
  const live = (s?.episodes ?? []).filter((e) => e.status === "live");
  const byNumber = new Map<number, Entry>();

  for (const a of ARTICLES) {
    byNumber.set(a.n, {
      n: a.n, title: a.title, blurb: a.standfirst,
      views: null, live: false, ytVideoId: null, igMediaId: null,
    });
  }
  for (const e of live) {
    const prev = byNumber.get(e.number);
    byNumber.set(e.number, {
      n: e.number,
      title: e.title || prev?.title || `Episode ${e.number}`,
      blurb: e.topic || prev?.blurb || "",
      views: e.views ?? null,
      live: true,
      ytVideoId: e.ytVideoId ?? null,
      igMediaId: e.igMediaId ?? null,
    });
  }
  return [...byNumber.values()].sort((a, b) => {
    if (a.views != null && b.views != null) return b.views - a.views;
    if (a.views != null) return -1;
    if (b.views != null) return 1;
    return b.n - a.n;
  });
}
