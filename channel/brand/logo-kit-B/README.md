# Logo kit B, "The Highlight" (13.11.2026)

Drafts for David to choose from. Files only: nothing here is published, merged, or used by the site.
Basis: `channel/brand/brand-research-round2-2026-11-13.md`. Start with `kit-overview.png`.

Colours: Ink `#0B0B0C`, White `#FFFFFF`, Signal yellow `#FFE600`.
Layer rule: on black the swipe lies over the letter; on white the letter lies over the swipe.

## Files

| Path | What it is |
|---|---|
| `kit-overview.png` | Everything on one image (1600 px wide), labelled a / b / c |
| `a/`, `b/`, `c/` | One folder per variant, same file names in each |
| `X/mark-X-dark.svg`, `mark-X-light.svg` | The avatar as SVG: 1000 x 1000, full-bleed background, polygons only, no text, no external references |
| `X/avatar-X-dark-1024.png`, `avatar-X-light-1024.png` | 1024 x 1024 profile picture. Every point of the mark is within 78.0% of the radius (computed in the build) |
| `X/preview-X.png` | Circle crop at 320, 110, 40, 32, 16 px, dark and light version, on black and on white, plus the 32 and 16 px crops enlarged x5 |
| `X/favicon-32.png` + `favicon-X.svg` | Square icon, mark larger than in the avatar (fits 91% of the half-side; no circle crop in a browser tab) |
| `X/favicon-16.png` + `favicon-X-16.svg` | 16 px version: swipe 14% thicker, feet snapped to a pixel row. The notch is kept (see "Fixed after looking") |
| `X/apple-touch-icon.png` (180), `icon-192.png`, `icon-512.png` | Dark avatar composition. Content is inside 78% of the radius, so inside the centre 80% used for maskable icons |
| `wordmark/wordmark-dark.svg/.png`, `wordmark-light.*` | ACTUALLY / WORKS, Archivo Black, text converted to outlines (the SVG needs no font). PNG 2400 px wide |
| `wordmark/lockup-X-dark.*`, `lockup-X-light.*` | Horizontal lockup as briefed: mark at the left, wordmark with the yellow bar. PNG 2400 px wide |
| `wordmark/lockup-X-*-one-swipe.*` | Alternative lockup without the bar under WORKS (see usage rule 2) |
| `src/` | The generator: `geom.py` (mark geometry), `wordmark.py` (outlines, bar), `build.py` (exports and sheets), `render.js` (Chromium), `construction.json` (all coordinates as built). Rebuild: `cd src && python3 build.py` (needs fonttools, uharfbuzz, pillow, node with playwright) |

Font: `channel/brand/logo-v2/ArchivoBlack-Regular.ttf` (SIL OFL), used only to produce the outlines.

## Construction numbers (1000 x 1000 master canvas, y down)

**a, "B2 clean", exactly as specified**
- A: `425,235 575,235 788,765 592,765 500,521 408,765 212,765`
- Swipe: `177.3,553 892.3,465.2 837.7,615.2 122.7,703` (7 degrees, 150 high, 70-degree ends)

**b, "B2 optical", my corrections**
- A: `414,228 586,228 808,772 594,772 500,541.66 406,772 192,772`
  - height 544 (was 530), base 616 (576), flat apex 172 (150), leg 214 measured horizontally (was 170 to 196)
  - inner edges are parallel to the outer edges, so each leg is one constant-width stroke; in a the leg widens toward the base
  - the notch tip moves from y 521 to 541.66, still under the swipe on black; on white the A gets a heavier cap
- Swipe: `175.56,556.63 910.34,453.37 836.44,619.37 101.66,722.63`
  - 8 degrees (7), 166 high (150), ends cut at 66 degrees (70): a slightly longer chisel face; centre (506, 588), 6 right of the letter's axis so the right overshoot is the longer one
  - feet under the swipe are about 15% taller than in a, which is what keeps two feet visible at 32 px

**c, "B1 marker", hand-cut ends**
- A: same as a
- Swipe (6 points): `170.77,549.45 903.73,463.25 886.27,526.19 841.79,615.25 111.73,708.69 126.22,646.12`
  - long edges are straight; the band narrows 5% toward the right (lift-off) end
  - each end is a cut in two facets instead of one straight 70-degree cut: the break sits 9 units outside the straight line on the left, 7 on the right. No curves, no texture
  - my stand-in, not a traced real marker stroke (the research asks for a trace before the final)

**Placement in the avatar (all variants).** The circle centre is put between the centre of the letter and the centre of the smallest circle around letter + swipe (30% of the way horizontally, 40% vertically), then the mark is scaled until its farthest point is at 78% of the radius. Scale factors: a 0.9384, b 0.8826, c 0.9118. The fitted coordinates are the ones in the SVG files and in `src/construction.json`.

**Wordmark.** Archivo Black caps, cap height = 688 font units, tracking -6 units plus hand kerning LL -10, LY -14, WO -6. Baseline to baseline 1.47 cap heights (1.34 in the one-swipe lockup). Bar: 2 degrees, 70-degree chisel ends; top edge 0.08 cap above the cap line at the left edge of WORKS, bottom edge 0.10 cap under the baseline at its right edge (about 1.3 cap high in total); 0.35 cap past the word on the left, 0.5 on the right. WORKS is always Ink on the bar. Lockup: the A runs from the cap line of ACTUALLY to the baseline of WORKS; gap between mark and text 1.25 cap (0.9 in the one-swipe lockup).

## Usage rules

1. **Yellow is never text and never sits alone on white.** `#FFE600` on white is 1.27 : 1. The yellow is a fill behind Ink, and it must always touch Ink.
2. **One swipe per frame.** The briefed lockup (mark + bar under WORKS) shows two yellow strokes at two angles, which breaks this rule; that is why the one-swipe lockup exists. Use the mark alone, the wordmark alone, or the one-swipe lockup. My judgement, David decides.
3. **Layer rule:** black background = swipe over the letter; white or paper = letter over the swipe.
4. **Never change:** the angle, the end cuts, the thickness, the colours. No ring, shadow, gradient, transparency, brush texture, rounded ends, or a second accent colour.
5. **Minimum sizes (my judgement from the renders, not tested on a phone):**
   - avatar a or b, dark: readable down to the 32 px circle; at 16 px in a circle it is only a white and yellow dot
   - light versions: 40 px and larger (the yellow is separated from white by hue only)
   - variant c: 110 px and larger; under that the cut ends are not visible and it is the same as a
   - browser tab: use `favicon-32.png` and `favicon-16.png`, not a scaled avatar
   - wordmark: 160 px wide and larger; lockup: 240 px wide and larger
6. Clear space around mark or wordmark: one leg width of the A.

## Fixed after looking at the renders

- The first avatar fit centred the swipe, which pushed the A up and left the lower third empty. Placement now follows the letter.
- Variant c, first draft: small zigzag nicks on the ends looked like rendering errors. Second draft: the end cuts leaned the wrong way. Redrawn as two-facet cuts on the same 70-degree line as a.
- Variant b: ends at 62 degrees made long sharp tips that cost size in the circle; set to 66.
- Wordmark: with the bar tilted 2 degrees, the top-left corner of the W stood outside the bar (invisible on black). The bar is now built from the letters outward so no letter is uncovered. Line spacing opened so the rising bar does not crowd ACTUALLY.
- 16 px favicon: the research suggested dropping the notch. Rendered both: the solid wedge reads as a hat, the version with two feet reads as an A. The notch is kept, the swipe thickened and the feet snapped to the pixel grid.
- Preview sheet: the enlarged crops ran off the panel; sheet widened.

## Not checked

- **No trademark register search** (EUIPO/TMview, BOIP, USPTO) and **no reverse-image search** of this artwork. Needed before it goes on any profile.
- Not viewed on a real phone, in Instagram's real comment list, or in Instagram dark mode. The circle crops here are a browser simulation.
- The maskable 80% safe zone is the commonly quoted figure; not checked against the W3C manifest spec.
- No `favicon.ico` file was made; only PNG and SVG.
- No greyscale or colour-blind check. Paper (`#ECEAE4`) version of the mark not exported.
- The lockup kerning was judged by eye from renders at one size.
- Nothing in `studio/` or anywhere outside this folder was changed.
