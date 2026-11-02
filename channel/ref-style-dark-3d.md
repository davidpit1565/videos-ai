# Reference: dark 3D explainer style (saved 2.11.2026, David: "I loved the design and the visuals, I did not follow the content")

Source: https://www.instagram.com/reel/DfKkesFE0nF/ (account jesserurka). Downloaded through the /embed/ URL and kept only in the session scratchpad (`scratchpad/ref-style2/ref.mp4`), NOT in git: it is someone else's video and the repo is public. Re-download with yt-dlp on `.../embed/` if it is needed again.
Decision pending, David's words: after episode 82 is approved we move straight to this style, maybe even the same content. Not started.

## What it is (measured, 2.11.2026)
- 83.7 s, 1080x1920, 60 fps. Long compared with our 25-45 s rule: that rule stays unless David changes it.
- Only 3 hard cuts in 83.7 s (scene-change detector at 0.15). Everything else is one continuous camera: cards fly, stack and slide into the next view. This is what makes it feel alive without cutting.
- Spoken script (auto transcript, product names garbled by the transcriber, so UNVERIFIED): compares four always-on AI assistants by "what wakes them up" (a clock, an event, or both): a bold hook question, an everyday example ("you wake up and it already messaged you"), a simple trigger explanation, one honest limit ("every check uses up your plan"), a price line per product, then a closing line asking viewers to send it to friends. Do not reuse any claim from it without checking the real product pages first (CLAUDE.md rule: verify the product before any script).

## Design language (what we would copy)
- DARK base (near black) with soft spotlight cones, NOT our light paper base. Using it means changing the fixed light identity in CLAUDE.md: David's decision, not mine.
- Glossy 3D mascot characters, one per product (a yellow triangle with glasses and a bow tie, a black glossy ball with eyes, a beige ghost), standing in a row under spotlights; the real brand icon floats above each when it is named.
- Captions: one or two words at a time, centred in the upper third; the current word is white and bold, earlier words fade to grey, the key word is lime green with an underline. No karaoke box.
- Real product screens (inbox, calendar, settings, pricing cards) shown as flat cards and STACKED as 3D layers in perspective, with a lime glow outline on the layer being talked about. Zoom-through moves between layers.
- Simple timeline diagrams (rows labelled alarm / model / computer with a lime bar for when it is awake), pricing cards, a chat-model row at the end that summarises all four.
- Small grey footnote under each screen ("illustration", source text), blurred motion on transitions, soft bloom on the lime accent.
- Colour: black and graphite, one lime accent (the same lime family as our 81 base), each product's own mark in its own colour.

## What to carry into our pipeline (ideas, untested)
1. Continuous-camera scenes instead of cuts (HyperFrames: one long timeline, layers moving in z).
2. Mascots or simple 3D-looking characters as the faces of products (we use no human faces).
3. Stacked-layer screens with a glow on the active layer.
4. One-or-two-word captions with the key word in the accent.
Each of these is a hypothesis; log it in `channel/experiments.md` when a real episode uses it.
