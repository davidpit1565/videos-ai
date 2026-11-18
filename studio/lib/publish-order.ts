/** The order reels should be posted in, because each closing line promises the next one.
 *  Edit this list when the order changes (10.10.2026: 62 already went out; 60 is held out of the
 *  chain until its closing line is re-rendered). Reels not listed sort after these by number.
 *  69 goes after 68 (Spotify, not built yet): insert 68 before 69 when it exists. 70 (ChatGPT Memory,
 *  16.10.2026) closes with the standard line and promises nothing, so it simply follows 69. When Instagram cannot be
 *  asked (dead token) this list alone decides what is still waiting, so keep it to what is NOT yet published. */
export const PUBLISH_ORDER: number[] = [101, 103, 102, 104];

/** Episodes David posted to Instagram by hand (the studio's own database does not know). Treated as live:
 *  not shown as waiting, and the studio will not publish them a second time. 13.10.2026: 67 (66 is already
 *  recorded live in the database, from the earlier post). 16.10.2026: 57, 65 and 69 added, from David's screenshot
 *  of his Reels tab (4 reels: 69 iPhone notifications, 57 Google live AI, 67 YouTube birthday, 65 Gmail replies).
 *  17.11.2026: 91 (trial moved to everyone early), 93 (posted by hand 12.11) and 98 (regular, 15.11) added: the studio never linked their Instagram posts, so they showed as waiting. 17.10.2026: 70 added (posted by hand Friday 16.10.2026 evening; about 130 views by Saturday night). 18.10.2026: 71 added (v4, posted by hand by David Sunday 18.10.2026). */
export const PUBLISHED_MANUALLY: number[] = [57, 60, 65, 67, 69, 70, 71, 72, 73, 77, 83, 91, 93, 98];

/** Reels that exist as files but were skipped on purpose and must never show as waiting (David, 17.11.2026: 50 and 68 "let it go"; 2 skipped earlier). */
export const SKIPPED_FOR_GOOD: number[] = [2, 50, 68];
