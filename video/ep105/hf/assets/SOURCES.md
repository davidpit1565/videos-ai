# Episode 105 assets - real marks, sourced 18.11.2026 (nothing drawn or redrawn)
PNGs are 512x512 transparent, rendered from the SVG in headless Chromium (no rsvg on this box). Only SVG recolour: Claude wordmark/sparkle fill set from currentColor to the page's own colours.

| File | What | Source | Licence / note |
|---|---|---|---|
| claude-logo-wordmark.svg/.png | Claude sparkle + wordmark (current site header, fill #141413) | inline SVG in header of https://claude.com/contact-sales/claude-for-oss | Anthropic trademark, shown as the product mark |
| claude-sparkle-site.svg/.png | sparkle only (same paths, viewBox cropped to the sparkle, fill #D97757) | same inline SVG; the pre-existing 2023-style Commons mark is below | Anthropic trademark |
| claude-sparkle.svg/.png | sparkle symbol, fill hsl(14.8,63.1%,59.6%) | https://commons.wikimedia.org/wiki/File:Claude_AI_symbol.svg | Commons; trademark of Anthropic. Shape differs a bit from the site's current sparkle: prefer claude-sparkle-site |
| github-mark.svg/.png, github-octicon-mark.svg | GitHub Invertocat mark | Commons File:Octicons-mark-github.svg; primer/octicons mark-github-24.svg (raw.githubusercontent.com) | Octicons MIT; GitHub trademark |
| github-mark-official.png (560 px, white bg) | official GitHub-Mark.png | https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png (the file on github.com/logos; the page itself returned 403 here) | GitHub logo usage guidelines |
| openssf-logo-horizontal-color.svg/.png | OpenSSF primary logo, goose Honk + wordmark | https://raw.githubusercontent.com/ossf/artwork/main/openssf/horizontal/color/openssf-horizontal-color.svg (linked as the logo source from https://openssf.org/about/brand-guidelines/) | OpenSSF/Linux Foundation trademark guidelines apply |
| openssf-icon-color.svg/.png | OpenSSF icon (goose only) | https://openssf.org/wp-content/uploads/2022/10/openssf-icon-color.svg | same |
| openssf-horizontal-white.svg | white version (for dark backgrounds) | https://openssf.org/wp-content/uploads/2023/12/Open-SSF-Logo-horizontal-colorwhite.svg | same; invisible on light bg, no PNG made |
| linux-tux.svg/.png | Tux | https://commons.wikimedia.org/wiki/File:Tux.svg | Larry Ewing, Simon Budig, Anja Gerwinski; free to use with credit |
| python-logo.svg/.png | Python logo | https://commons.wikimedia.org/wiki/File:Python-logo-notext.svg | PSF trademark; Commons file |
| nodejs-logo.svg/.png | Node.js wordmark | https://commons.wikimedia.org/wiki/File:Node.js_logo.svg | OpenJS Foundation trademark |
| claude-for-oss-top.png | real page, 1080x1400 viewport (top), Playwright chromium, no retouching | https://claude.com/contact-sales/claude-for-oss, shot 18.11.2026 | Anthropic page capture |
| claude-for-oss-heading-criteria.png | crop (1080x1090, y 170-1260) of the above: heading + "Who should apply" list | same | crop only |
| claude-for-oss-full.png | full page 1080x3879 | same | |

Not sourced: Linux Foundation's own Linux mark (Tux used, the usual Linux symbol). Linux/Python/Node logos came from Commons, not the vendors' brand pages.

## OpenSSF criticality score (one sentence)
"A project's criticality score defines the influence and importance of a project," as a number from 0 (least critical) to 1 (most critical), derived from signals such as contributors, commit frequency, dependents. Source: https://github.com/ossf/criticality_score (README). The Claude page itself says: "Any repo you maintain has an OpenSSF criticality score of 0.4 or above."
