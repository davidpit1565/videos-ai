# Rebrand 2, 13.11.2026: making the public site rich again, in the new identity

David after PR #582: "the site looked better before; the rebrand made it more bare; it is
still missing things." This pass brings back what the old site had that was good and
true, restyled in the 13.11 identity (white page, ink type, signal yellow #FFE600 as a
mark only, Archivo Black headings). Paths are under `studio/` unless stated.
Screenshots: `channel/brand/rebrand2-shots/` (after). The "before" of this pass is
`channel/brand/rebrand-shots/after-*` (the PR #582 look); the old dark site is
`rebrand-shots/before-*`.

## Restored (from the old site, `git show fc6e554e:studio/app/page.tsx`)

- **The reels on the first screen.** Old site: Instagram embed beside the hero. Now: a
  row of six **real frames from the rendered reels** (newest first), starting inside the
  first phone screen (about 530 px down at 375x812). Each opens the episode's page.
- **The real numbers**, as one plain sentence under the follow button ("85 episodes so
  far. The newest went out on 9 November.") and the about page's existing proof line
  (episodes, failure modes, views measured). All computed from `catalogue()` and
  `ARTICLES`. No count-up, no big-number tiles.
- **"What breaks"** on the home page: the first limit of each of the three newest
  episodes, quoted from the article, with a link to the episode, plus the real total
  ("277 limits written down so far, across 85 episodes" on the local data) and a link to
  `/failure-modes`. This was the old site's "311 failure modes written down" stat.
- **Episode list with pictures**: home ("Earlier episodes", 6 rows), `/episodes` (all),
  each episode page's "More episodes" (4) and the 404 (3). Row = frame, "Episode N, Mon
  YYYY[, tool]", title, two lines of what you get; the whole row (min 44 px) is the
  link to the setup page.
- **Who makes this** on the home page (two sentences + "How it is made" and the Flow App
  Store link), right column on desktop under the prompts.

## Added

- `scripts/make-frames.mjs` + `lib/frames.json` + `lib/frames.ts` + 95 stills in
  `public/site/frames/N.webp` (360x640, about 12 KB each, 1.2 MB total). The still is
  the most detailed of three candidates at 1.6 / 2.6 / 3.6 s of `public/reels/reel-N.mp4`
  (the hook frame, where the subject is stated). `/site` is already public in
  `lib/routes.ts`; no route change. **When an episode ships, run
  `node scripts/make-frames.mjs` in `studio/` and commit both outputs**; an episode with
  no still gets an empty dashed box, never a stand-in picture.
- `app/ep-rows.tsx`: the one row component for all those lists.
- Episode page: a follow block after the content ("The next test goes out on Instagram
  first." + Follow button), before "More episodes".
- About: "How an episode is made" as a numbered list (it is a real sequence, taken from
  CLAUDE.md's standing rules), "Built here: Flow" with an outlined App Store button,
  "Work with me" (the existing paid-side text, link now opens in a new tab).
- `/episodes`: a live count line ("85 episodes, newest first." / "3 of 85 episodes.").
- Section heads: the ink rule with a short yellow stroke on it (the logo's swipe). No
  text inside it.
- `lib/fmt.ts`: `publicDay()` (English "9 November", Belgium time).
- `lib/site.ts`: public pages drop a leading "TITLE: " from a title (episode 89's stored
  title). The stored value is not changed; the studio data fix is still open.

## Motion (two, both off under prefers-reduced-motion)

1. The six frames rise in once on load, 70 ms apart (CSS only, no JS needed).
2. A frame lifts with a hard ink offset shadow on hover/focus.
Everything else is colour/underline on hover.

## Left out, and why

- **Instagram embed on the home page**: replaced by the real stills (fast, no
  third-party script, no blue "View profile" button). The embed stays on every episode
  page.
- **Count-up numbers, eyebrow labels, gradients, glows, scroll reveals, tool ticker,
  safe-zone demo**: the audit's template tells; not brought back.
- **"Browse by tool" pills on home**: the filter on `/episodes` does that. The chip list
  still shows internal names (HyperFrames, Voice, Skills) from `lib/tools.ts`; not
  changed (copy/taxonomy call).
- **Headline copy** "AI setups that actually work." kept; the 13.11 brand direction
  ("everything about AI, from self experience") may want a new line. His call.
- A "views" number on the home page: kept to the About page only (one number a visitor
  understands on home: the episode count).

## Buttons that are solid (ink fill, white text)

| Where | Button |
|---|---|
| Home, first screen | Follow @actually_works.ai |
| Episode page, after the content (new) | Follow @actually_works.ai |
| 404 | Newest episode |
| Error page (site) | Try again |
| `/p/*`, `/s/*` | Copy the whole thing |
| Studio | every `.btn` (white fill, ink text) |

Outlined: About "Flow on the App Store", 404 "All episodes", filter chips. Yellow never
sits behind a word.

## Found and fixed outside the page files (please review)

- **`lib/db.ts`: a pool deadlock that hung pages.** `migrateSnapshots()` took a client
  from the pool (max 3) and then ran its CREATE TABLE through the pool. Three concurrent
  first loads on a fresh server instance each held one client and waited for a fourth
  forever: `next build` timed out on /sitemap.xml, /rss.xml, and `/e/93` never answered
  under `next start`. Fix: the DDL now runs on the client already held
  (`ensureSnapshots(c)`). After it, `next build` passes at default concurrency. This
  can plausibly hit production on a cold function that gets three requests at once; it
  was not reproduced there.

## Verified

- `npm run check:routes`: 54 routes classified. `npx tsc --noEmit`: clean.
- `npx next build`: passes, against a throwaway local Postgres (SSL on, port 55432)
  loaded with the 85 real episodes in `channel/episodes-database.json` (titles, IG
  links, views, publish dates up to episode 87). Not the production database, so the
  counts in the screenshots are local. `npm run build` (with the prebuild prune) was not
  run, to keep the worktree's tracked reels untouched.
- Playwright (Chromium) at 375x812 @2x and 1280x800: home, /episodes, /e/93, /about,
  404. `document.documentElement.scrollWidth` = 375 / 1280 on all ten; no visible
  link, button or input under 44 px tall (after fixing the section-head links, 27 px).
  Looked at every shot.
- Contrast: body #0B0B0B, secondary #454545 (9.7:1), meta #666666 (5.7:1) on white.

## Not verified

- Real phone, Safari, screen reader, slow network; the frames' look on a real device.
- `/e/93` shows "Not posted yet." locally because episode 93 is not in the local data;
  with the production DB it shows the Instagram embed.
- Locally the public pages called `/api/track` through `providers.tsx` when no
  STUDIO_PIN was set, and the tracker flipped the test episodes to `testing`. The shots
  were taken with a local test PIN set, as production has. Not a production issue as far
  as can be seen, but `providers.tsx` running the tracker from a public page is worth a
  look.
- The studio pages behind the PIN were not opened.
