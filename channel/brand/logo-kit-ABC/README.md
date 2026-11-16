# Logo kit A / B / C (13.11.2026)

Drafts for David to choose from. Files only: nothing here is published, merged, or used by the site or the profile.
The three directions are the ones from `channel/brand/logo-v2/sheet.png`, each built out as a full kit in dark and light mode.
Start with `kit-ABC-overview.png`, then `kit-A.png`, `kit-B.png`, `kit-C.png`.

Colours: ink `#0B0B0B`, white `#FFFFFF`, signal yellow `#FFE600`. Font: Archivo Black (`logo-v2/ArchivoBlack-Regular.ttf`, SIL OFL), converted to outlines in every SVG.
No word sits inside a filled box or bar anywhere in this kit. Yellow appears only inside the mark and as one thin line under WORKS in the stacked lockup on dark (on white that line is ink).

## Files

| Path | What it is |
|---|---|
| `kit-ABC-overview.png` | All three directions, dark half and light half, 1600 x 1994 px. The one to choose from on a phone |
| `kit-A.png`, `kit-B.png`, `kit-C.png` | One sheet per direction, 1600 x 1352 px, dark half left, light half right: avatar at 320 / 110 / 40 / 32 px in the circle crop, the 32 px file enlarged x5, mock Instagram profile header, mock comment row at 32 px (both avatar files on that background), mock site header, mock browser tab with the favicon, horizontal and stacked lockup |
| `X/mark-X-dark.svg`, `mark-X-light.svg` | The avatar as SVG, 1000 x 1000, full-bleed field, polygons only |
| `X/avatar-X-{dark,light}-1024.png` | 1024 px square profile picture (Instagram does the circle crop itself) |
| `X/avatar-X-{dark,light}-{320,110,40,32}.png` | The circle crop at those sizes, transparent outside the circle |
| `X/favicon-X-{dark,light}-64.png` + `.svg` | 64 px favicon. A and B: rounded square, mark drawn larger than in the avatar. C: the disc |
| `X/lockup-X-horizontal-{dark,light}.svg/.png` | Mark + ACTUALLY / WORKS on two plain lines (option 1 of `wordmark-v3`) |
| `X/lockup-X-stacked-{dark,light}.svg/.png` | Mark above the two lines, thin line under WORKS (option 2 of `wordmark-v3`). The line can be dropped |
| `X/lockup-X-oneline-{dark,light}.svg/.png` | Mark + ACTUALLY WORKS on one line, the one used in the site-header mock |
| `src/` | Generator: `build.py`, `render.js`, `construction.json` (fitted coordinates). It imports the geometry of `logo-kit-B/src/geom.py`. Rebuild: `cd src && NODE_PATH=/opt/node-tools/node_modules python3 build.py` |

"Dark" and "light" for C: the dark file is the yellow disc with ink marks, the light file is the ink disc with yellow marks, as on the v2 sheet.

The sheets are rendered at 2x and stored at 1600 px wide, so a "32 px" avatar on a sheet is 32 real pixels. The thin ring around the circles on the sheets is only there to show the crop edge; it is not part of any file.

All text in the mocks is placeholder. Posts, followers and following are shown as a dash: no numbers were invented.

## What changed against the v2 sheet

**A, tick ligature (tidied).**
- All five strokes now have one width (96 on the 1000 master before fitting) and one slope, including the long arm of the check, which had its own slope and width before. Every joint is a shared flat edge of exactly one stroke width.
- The white (or ink) part now stops in a clean point 26 units before the yellow check instead of running under it. On black, white and yellow are 1.07 : 1 against each other, so where they touched the two colours melted together at small sizes.
- Letter pitch opened from 118 to 132 and the crossbar lowered and thinned (68 high), so the counter of the A stays open at 32 px.
- The mark is placed by its smallest enclosing circle at 80% of the avatar radius.

**B, the highlight.** No new drawing: it is variant b ("B2 optical") of `logo-kit-B`, refitted into the circle. Layer rule kept: on black the swipe lies over the letter, on white the letter lies over the swipe.

**C, the wink.** Same dot and check, scaled down to 64% of the radius. On the v2 sheet the tip of the check reached 94% of the radius and almost touched the crop edge.

## Honest notes per direction (my judgement from the renders)

**A, tick ligature**
- Works: the only one of the three that carries the initials, and the check says "works" without a word. On black it holds at 32 px: the x5 enlargement still shows an A and a yellow check. The lockups look like one piece, because the mark is made of the same heavy letters as the wordmark.
- Weak: it reads as "AV" plus a check, or "A" plus a check, more than as "AW". The W exists only if the viewer counts the right leg of the A as its first stroke. At 32 px the middle stroke is a blur between the A and the check.
- Weak on white: the yellow check on white is 1.27 : 1. In the light avatar and the light lockups the check is pale, and at 32 px it is close to gone, so what is left reads as "AV". The dark file is the one to use as the profile picture.
- Could recall: the Vans wordmark (a V whose right arm flies up and out), AV / AVG style monograms, and the generic "letter plus check" marks used by many verification and to-do products.

**B, the highlight**
- Works: the simplest silhouette, a single heavy A. On black it is the most readable of the three at 32 px in my view. The marker swipe matches the "we tested it, here is the part that matters" idea.
- In the stacked lockup on black, B shows two yellow strokes (the swipe and the line under WORKS); kit B had a "one swipe per frame" rule, so for B use the horizontal lockup or drop the line.
- Weak: one letter A says nothing about "works"; many brands are a single A. On white the swipe sits behind the letter and is pale, so at 40 and 32 px the light file is just a black A. In the lockup the mark and the first letter of ACTUALLY are the same letter twice.
- Could recall: a crossed-out A (a strike-through reads as "wrong", the opposite of the name), the Star Trek delta shape, and single-A marks such as Adobe, Autodesk or Arc'teryx only loosely.

**C, the wink**
- Works: by far the strongest at small sizes. The full yellow disc is visible on black and on white, at 32 px and in a 16 px tab. It is the only one with a personality, and it needs no black field to hold together.
- Weak: no letter and no link to the name unless the viewer reads the check as "works". Not everyone sees a face: it can read as "dot, check", a square-root sign, or a bullet point. The ink-disc file disappears on a black interface (see the second comment row of the dark half of `kit-C.png`). It is the furthest from what David said he leans to.
- Could recall: Norton (a yellow disc with a black check: the closest resemblance in this kit and a real risk), generic "done" or "verified" badges, and the emoji wink.

## My ranking

1. **A**, with the dark file as the profile picture: it is the only one that is the name, the tidied joins hold at 32 px on black, and it matches the wordmark. Its light version is weak.
2. **C**: the best small-size performer and the most distinctive on a feed, but the Norton resemblance has to be checked before it could be used, and it carries no letters.
3. **B**: clean and safe, but the least specific to this brand, and the swipe can read as a strike-through.

## Not checked

- **No trademark register search** (EUIPO/TMview, BOIP, USPTO) and **no reverse-image search**. The "could recall" lines above are from memory, not from a search. Needed for the chosen mark before it goes on any profile.
- Not viewed on a real phone, in the real Instagram app, or in a real browser tab. The mocks are a Chromium simulation with a generic interface font (Inter), not Instagram's.
- Instagram takes one profile picture for both interface modes. The comment rows show both files on both backgrounds for that reason; a decision is needed on which single file to upload.
- The 16 px favicon in the tab mock is the 64 px artwork rendered at 16 px; no hand-tuned 16 px version and no `.ico` file were made.
- No greyscale or colour-blind check. Kerning of the wordmark was taken from kit B and judged by eye at one size.
- Nothing outside `channel/brand/logo-kit-ABC/` was changed. Nothing was committed.
