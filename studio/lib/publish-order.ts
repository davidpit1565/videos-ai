/** The order reels should be posted in, because each closing line promises the next one.
 *  Edit this list when the order changes (10.10.2026: 62 already went out; 60 is held out of the
 *  chain until its closing line is re-rendered). Reels not listed sort after these by number.
 *  69 goes after 68 (Spotify, not built yet): insert 68 before 69 when it exists. When Instagram cannot be
 *  asked (dead token) this list alone decides what is still waiting, so keep it to what is NOT yet published. */
export const PUBLISH_ORDER: number[] = [66, 67, 57, 69];
