# Rebrand to logo A, 13.11.2026: what changed

Branch `rebrand-a` (not merged, no PR). All paths under `studio/` unless stated.
Screenshots: `channel/brand/rebrand-shots/` (before = production www.actually-works.com
on 13.11.2026; after = this branch built and served locally).

## Decisions taken on my own (please check)

1. **Studio stays dark**, public site is light. The studio is dense data UI he uses every
   day on his phone; its ~480 lines of CSS assume a dark ground, the app icon is the dark
   tile, and yellow on ink is 15.5:1 while yellow on white is 1.27:1. Same palette, same
   mark, same heading face, just the dark side of it.
2. **Unknown page addresses now get an English 404** instead of the Hebrew PIN page.
   Rule in `middleware.ts`: a path in no list (not site, not studio, not cron) and without
   the studio cookie is *rewritten* to a missing route, so Next shows `app/not-found.tsx`
   with status 404. It is not passed through, so unlisted files in `public/` (e.g.
   `/templates/*.png`, `/build-info.json`) stay hidden from visitors exactly as before.
   Real studio pages still redirect to `/unlock`; every `/api/*` path still answers 401.
   With the studio cookie nothing changed.
3. **Removed the home page's safe-zone demo, tool ticker and "browse by tool" pills**
   (audit: off-audience; the tool filter still exists on `/episodes`).
4. **Removed the episode thumbnails on `/episodes`.** They were the share card (the title
   as text) shrunk until unreadable. A real frame per reel would be the right picture;
   none is stored.
5. **Deleted dead components** nothing imported: `signup.tsx`, `site-notify.tsx`
   (email list removed 1.11). Also deleted the motion/template ones listed below.
6. Headings use Archivo Black at weight 400 (its only weight). The font face is declared
   for 400-900 so the studio's `font-weight:800` headings never get a fake bold.
   Hebrew has no glyphs in it and falls through to IBM Plex Sans Hebrew.
7. Favicons use the **dark** tile (README recommendation). `icon-192/512` and
   `apple-touch-icon` are the full-bleed dark square (`mark-A-dark.svg`); the manifest
   still says `purpose: "any maskable"`. The mark reaches about 41% of the width from the
   centre, the maskable safe circle is 40%: the check's tip may be trimmed a hair on
   Android circle masks. Not checked on a device.
8. Episode page: "Episode 93" stays as a plain line above the title (information, not an
   eyebrow); the "07 / 87" index chip is gone. The three "other episodes" footer links
   became a "More episodes" list.

## Buttons kept SOLID (he has not said whether a button counts as "a word in a filled box")

| Where | Look |
|---|---|
| Home, first screen: **Follow @actually_works.ai** | solid ink, white text |
| 404 page: **Newest episode** | solid ink, white text |
| Error page (site): **Try again** | solid ink, white text |
| Prompt page `/p/*` and skill page `/s/*`: **Copy the whole thing** (`.btn`) | solid ink, white text |
| Studio (dark): every `.btn` (save, publish, PIN "כניסה", etc.) | solid white, ink text |

Everything else is outlined (2 px ink on the site, 1 px grey in the studio). If buttons
count, swap `.button.solid` / `.site .btn` / `.btn` in `app/globals.css` for the outlined
style: three rules.

## What changed, per file

- `app/globals.css`: one palette in tokens (`--aw-ink #0B0B0B`, white, `--aw-yellow
  #FFE600`). Studio tokens remapped to neutral greys on ink, `--brass` now = the yellow
  (so every studio rule and inline `var(--brass)` follows). Public block (~800 lines)
  replaced by a light block of ~300: no gradients, glows, film grain, dot grid, eyebrow,
  uppercase mono labels, lifted cards with tinted shadows, count-ups, scroll reveals,
  page wipe, scroll progress, cursor spotlight, magnetic button, marquee. Lists are rows
  with rules. Studio filled-word fixes: active tab (now a yellow underline stroke),
  `.btn`, `.ch.on`, `.tplnum`, `.pill.pass/.fail`, `.del`, `.feed li.latest`,
  `.answer` gradient, focus tint. The bare `nav{}` studio rule is scoped to `.shell`
  (it leaked into the public header). Focus ring on the site: ink ring + yellow halo.
- `app/layout.tsx`: Archivo Black via `next/font/local` (`app/fonts/`), Google Fonts link
  removed from public pages, new icons, `themeColor` white, description rewritten
  ("One setup per episode..." → "short reels about AI tools, and a page for every
  episode with the steps").
- `app/(studio)/layout.tsx`, `app/studio-fonts.tsx`: studio theme colour ink; Hebrew + mono
  fonts load only in the studio and on `/unlock`.
- `app/mark.tsx`: the AW mark from `logo-A-final` polygons; `tone="light"` keylines the check.
- `app/sitenav.tsx`: one row: mark + "Actually Works" (plain text), Episodes, About.
  44 px targets. Fits 375 px on one line (measured).
- `app/site-footer.tsx` (new), `app/site-social.tsx`: one footer on every public page,
  rendered by Shell, with `@actually_works.ai` written as a link; YouTube/Facebook as words.
- `app/shell.tsx`: public chrome also for unclassified paths (the 404); page wipe and
  scroll bar removed; no footer on `/unlock`.
- `app/page.tsx`: rewritten (first screen: title, one sentence, follow, newest reel).
- `app/e/[n]/page.tsx`, `app/p/[slug]/page.tsx`, `app/s/[slug]/page.tsx`, `app/about`,
  `app/episodes`, `app/search`, `app/failure-modes`: eyebrows and per-page footers
  removed; `/p` and `/s` now use `<main class="site">` (their header was unstyled); their
  tab titles no longer read "X — Actually Works · Actually Works".
- `app/not-found.tsx` (new), `app/error.tsx` (English on site routes, Hebrew kept on studio
  routes), `app/global-error.tsx` (English, light).
- `app/unlock/page.tsx` + CSS: no longer clipped at 390 px (full-height studio layout opted out).
- `app/opengraph-image.tsx`, `app/e/[n]/opengraph-image.tsx`, `app/og-parts.tsx`: light
  cards in Archivo Black with the mark; text = site title and handle only.
- `app/(studio)/renders/page.tsx`: two inline filled-yellow pills made outlined.
- `lib/routes.ts`: `/apple-touch-icon.png` added to SITE (it was behind the PIN gate).
- `middleware.ts`: the 404 rule above.
- `next.config.mjs`: traces the font file into functions for the share cards.
- `public/`: `icon-mark.svg`, `icon-32.png`, `favicon.ico`, `apple-touch-icon.png`,
  `icon-192.png`, `icon-512.png`, `logo-dark.png`, `logo-light.png` (all from
  `logo-A-final`, rendered with Playwright); `manifest.json` white, `studio.webmanifest` ink.
- Deleted: `hero-headline`, `hero-parallax`, `hero-diagnostic`, `premium-motion`,
  `tool-marquee`, `safe-zone-demo`, `page-wipe`, `scroll-progress`, `signup`, `site-notify`.
  `public/site/safe-zone-frame.jpg` is now unused (left in place).

## Copy changed (only where it was wrong)

- Share card "One setup a week" → removed (channel posts several a week).
- Search empty state "it grows one episode a week" → "Try one word, like the name of the app."
- `/p` and `/s` "Reply to any issue and it reaches a person" → removed (no newsletter exists).
- Home "No email needed to read them" → removed with the old section.
- Site description and home sentence rewritten to say what is there (reels, a page per
  episode with steps). Nothing new is claimed.

## Findings NOT fixed

- **Episode 89's title in the database starts with "TITLE: "** (seen on the live site:
  `/e/89` heading "TITLE: This ChatGPT prompt is making the rounds..."). It is data in
  the studio database, not code; fix the title in the studio.
- `/about`: "Flow, a personal finance app ... heading toward the App Store" and "the paid
  side" with no contact route: could not verify either; left as is.
- Episode-page sub-heading "One AI setup per episode. The exact screen, the exact paste,
  and the part that breaks." (on `/episodes`) and the about page's positioning still speak
  the old "setup log" voice; the 13.11 brand direction is "everything about AI, from self
  experience". A copy rewrite is his call.
- Em dashes in `lib/articles.ts` (563) and page copy: not touched (low priority in the audit).
- `brand/house-style.md` (repo root, "Brass on Ink") is now wrong for the site; not in this
  sparse checkout, not edited.
- `count-up.tsx` still animates numbers inside the studio's `/analytics` (private page).
- The Instagram embed is Instagram's own white card with a blue "View profile" button:
  third-party, not styleable.

## Not verified

- **Studio pages behind the PIN were not opened** (no PIN used): `/studio`, `/videos`,
  `/analytics`, `/week`, `/renders`, `/renders/[file]`, `/trials`, `/agent`, `/health`.
  They rely on the token remap, `tsc` and the build. Only `/unlock` was seen.
- Local run used a throwaway local Postgres filled with six real public episodes
  (titles and Instagram links copied from the live pages), not the real database, so the
  numbers on the after-screenshots ("6 episodes") are local, not production.
- Not seen on a real phone, in Safari, or with a screen reader; tab icons not checked in
  a real browser tab bar; maskable icon not checked on Android.
- Share cards were rendered locally (`next start`), not by Vercel; the font file read
  depends on `outputFileTracingIncludes` working there.
- No trademark search for the mark (see `logo-A-final/README.md`).
