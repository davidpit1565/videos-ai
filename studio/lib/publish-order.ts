/** The order reels should be posted in, because each closing line promises the next one.
 *  Edit this list when the order changes (10.10.2026: 62 already went out; 60 is held out of the
 *  chain until its closing line is re-rendered). Reels not listed sort after these by number.
 *  69 goes after 68 (Spotify, not built yet): insert 68 before 69 when it exists. 70 (ChatGPT Memory,
 *  16.10.2026) closes with the standard line and promises nothing, so it simply follows 69. When Instagram cannot be
 *  asked (dead token) this list alone decides what is still waiting, so keep it to what is NOT yet published. */
export const PUBLISH_ORDER: number[] = [70];

/** Episodes David posted to Instagram by hand (the studio's own database does not know). Treated as live:
 *  not shown as waiting, and the studio will not publish them a second time. 13.10.2026: 67 (66 is already
 *  recorded live in the database, from the earlier post). 16.10.2026: 57, 65 and 69 added, from David's screenshot
 *  of his Reels tab (4 reels: 69 iPhone notifications, 57 Google live AI, 67 YouTube birthday, 65 Gmail replies). */
export const PUBLISHED_MANUALLY: number[] = [57, 65, 67, 69];
