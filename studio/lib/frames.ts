import FRAMES from "./frames.json";

/** A real still from each reel (scripts/make-frames.mjs writes public/site/frames/N.webp
 *  and this list). null when an episode has none yet: the pages then show no picture
 *  rather than a stand-in. 360x640, about 12 KB each. */
const HAVE = new Set<number>(FRAMES as number[]);
export const frameFor = (n: number): string | null => (HAVE.has(n) ? `/site/frames/${n}.webp` : null);
