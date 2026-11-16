# Logo A, final candidates (13.11.2026)

Files only. Nothing here is published, merged, committed or used by the site, the app or any profile.
Start with `decide-dark-vs-light.png`.

Colours: ink `#0B0B0B`, white `#FFFFFF`, signal yellow `#FFE600`. Wordmark: Archivo Black, converted to outlines. No word sits in a filled box or bar anywhere; the banners carry the mark and the plain wordmark only, no tagline.

## What changed against `logo-kit-ABC/A`

1. **The W is now a letter of its own.** In the kit the A and the W shared one stroke and a black gap cut the W in two, so the eye grouped by colour: white "A + one leg", yellow "V". Fifteen small variants were rendered at 300 / 110 / 32 px (`src/explore-w-variants-round2.png` shows the second round; `src/variants.py` holds all of them). What made the W read was two things together: a 50-unit gap between the A and the W, and the white half and yellow half of the W touching with no gap. Chosen: "v9" (`PARAMS = dict(g=0, sep=50)` in `src/build.py`). Splitting or reshaping the middle peak while keeping the shared stroke (v1, v2, v3, v6, v8, v13) still read "AV + check" at 110 px.
2. **Light version: a black keyline round the yellow check.** Options rendered in `src/explore-light-options.png`:
   - plain yellow on white (the kit): check 1.27 : 1, close to gone at 32 px;
   - darker yellow `#E3B000`: only 2.00 : 1, and it turns mustard, no longer the brand yellow;
   - yellow field with an all-black mark: the strongest at 32 px (15.5 : 1) but the check is no longer a different colour, and black on a yellow disc is the Norton / warning-sign look;
   - yellow field with a white check: 1.27 : 1 again, the check disappears;
   - **black keyline (chosen)**: the yellow stays `#FFE600`, its edge is carried by ink at 19.7 : 1 against white. Keyline is about 2% of the avatar width (1.7 px at 86 px, 0.65 px at 32 px).
3. Dark version unchanged in idea: white A, white first half of the W, yellow check, on ink.

## Files

| File | What |
|---|---|
| `decide-dark-vs-light.png` | 1600 x 2518. Dark avatar (left) against light avatar (right) in: Instagram profile header, reel-author and comment rows, YouTube channel header, each in the app's light and dark UI; site header + browser tab on a dark and a light site. Drawn at 2x like a phone screen, so "32 px" is 64 image pixels |
| `avatar-A-dark-1080.png`, `avatar-A-light-1080.png` | Profile pictures, 1080 x 1080, full-bleed field. The mark sits inside 82.4% of the circle radius (dark 78.4%, light adds the keyline), so the circle crop never touches it |
| `mark-A-{dark,light}.svg` | The same as SVG, 1000 x 1000 |
| `mark-A-{dark,light}-nofield.svg` | Mark only, transparent, for use on a dark / light page |
| `favicon-A-{dark,light}-{32,64}.png` + `.svg` | Rounded-square favicon, mark drawn at 80% of the width |
| `lockup-A-oneline-{dark,light}.svg/.png` | Mark + ACTUALLY WORKS on one line (site header) |
| `banner-youtube-2560x1440-{dark,light}.png` | Lockup 1240 x 120 px at the centre; the safe area is 1546 x 423, so 153 px spare left and right, 151 px above and below |
| `cover-facebook-1640x624-{dark,light}.png` | Lockup 880 x 85 px, x 380 to 1260, y 247 to 332: clear of the bottom-left corner where the profile picture overlaps, and inside the centre strip that phones show |
| `src/` | `build.py` (everything above), `geomA.py` (geometry), `variants.py` and `light.py` (the exploration sheets). Rebuild: `cd src && python3 build.py` |

## Recommendation (from what the renders show)

**Profile picture (Instagram, YouTube, Facebook): the DARK file, `avatar-A-dark-1080.png`.**
- One file serves both interface modes. On a light interface the dark file is a solid black disc with the mark inside: it looks like a profile picture at 86 px and at 32 px. On a dark interface the disc almost melts into the page (ink on Instagram's black is 1.07 : 1, on YouTube's `#0F0F0F` 1.03 : 1), but the white AW and yellow check stay at full strength, so nothing is lost.
- The light file on a light interface has no visible disc (white on white, 1.00 : 1): in the profile header and the comment row it is a small loose mark with empty space round it, and it reads smaller than the dark one at the same size. It only looks like an avatar on dark interfaces.
- The yellow check is the brand's one colour. On ink it is 15.5 : 1 and needs no help. On white it needs the keyline, and at 32 px the keyline makes the check darker and busier than on the dark file.

**Site: either works; if choosing fresh, a light page with the light lockup, and the dark mark as favicon.**
- In the site-header row both lockups are clean and legible. The light lockup with the keyline holds at header size (the keyline is visible there, unlike at 16 px).
- The current visitor site is a light page; staying light avoids a redesign, and long setup guides read better dark-on-light. This is a judgement, not something the mock measures.
- Favicon: the dark one. At 16 px in the tab the light favicon is a thin grey-yellow smudge on a white tab; the dark one is a black tile with a readable AW on both tab colours.

**App icon / studio: dark.** Same reason as the avatar: a filled black tile is a shape of its own on any home screen or tab, and the yellow is at full contrast.

Banners: use the dark ones with the dark avatar, so avatar and banner match.

## Measured contrast (WCAG ratio, computed from the hex values)

| Pair | Ratio |
|---|---|
| yellow check on ink field | 15.53 |
| white letters on ink field | 19.68 |
| ink letters / keyline on white field | 19.68 |
| yellow check on white field (without keyline) | 1.27 |
| white half of the W against the yellow half (they touch) | 1.27 |
| darker yellow `#E3B000` on white (rejected) | 2.00 |
| ink avatar field on Instagram dark UI `#000000` | 1.07 |
| ink avatar field on YouTube dark UI `#0F0F0F` | 1.03 |
| white avatar field on a white UI | 1.00 |

## Still weak

- The W's two halves are told apart by hue only (white against yellow, 1.27 : 1). In greyscale, or for some colour-blind viewers, the dark mark is "AW" with no visible check; the tall right arm is then the only hint. Not tested with a colour-blindness simulation.
- The mark is wider than the kit version (the W is a full letter now), so in the circle the letters are somewhat smaller than before (not measured). At 32 px it reads "AW" in the x5 enlargement, but the crossbar of the A is close to closing.
- The check is still also the right half of a W, so some viewers will read "AW" and not notice a check, others "A, V, check".
- The keyline on the light version is a compromise: it thickens the check, and under about 24 px it turns into a dark blur. The light favicon at 16 px is poor.
- "Letter plus check" is a common idea (verification and to-do products), and a V with a long right arm recalls the Vans wordmark. From memory, not from a search.
- Uppercase ACTUALLY WORKS in Archivo Black is taken over from the earlier kits; kerning judged by eye at one size.

## Not checked

- No trademark search (EUIPO/TMview, BOIP, USPTO) and no reverse-image search for the chosen mark.
- Not seen on a real phone, in the real Instagram, YouTube or Facebook apps, or uploaded anywhere. The mocks are Chromium with a generic font and approximate interface colours; real avatar sizes, rings and banner crops differ per device.
- YouTube safe area (1546 x 423) and the Facebook overlap zone are taken from commonly published template numbers, not verified against the live upload screens today.
- No 16 px hand-tuned favicon, no `.ico`, no app-icon sizes (180, 192, 512), no maskable icon.
- No stacked lockup and no two-line lockup were rebuilt with the new mark; the ones in `logo-kit-ABC/A/` still show the old drawing.
