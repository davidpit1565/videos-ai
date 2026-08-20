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
