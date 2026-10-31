# Style research, 31.10.2026: faceless "Claude tips" reels (David's friend Miki sent four TikToks)

Status of every line: FACT (seen in the files or read from a screenshot), HYPOTHESIS, or UNKNOWN. Idea source, not evidence about our channel.

## What the four reels are (first 13-18 s only; originals about 61 s; saved from WhatsApp, 384x848, 60 fps)
1. insiderforce (EN, "5 Secret Claude Codes"): light grey dotted-grid background, black bold type built word by word, typed cursor, selection-bar highlight, orange asterisk, blurred black spiky wipes between sections, dark prompt card with a tag, "#1 /ghost" with scrambling letters. Caption asks to comment "HUMAN" for an ebook. Site sells a $27 bundle. Seen counts: 42.3K likes, 3,237 comments, 11.8K shares.
2. MarketerHub (EN, `/ghost`, `/artifacts`): NOT faceless. Real presenter with a studio mic + real Claude screen capture (typed command, real answer) + stock B-roll + gradient opener + serif-italic word captions. Seen: 9,905 likes, 11.1K saves, 2,942 shares, 51 comments.
3. Max_Simplifia (FR, "Claude Motion"): fully synthetic, cream/orange/black, drawn UI: app tile, typed keys `/MOTION`, a PDF flying in, prompt box with chips, "NOUVEAU" sticker, bold captions with the key word in red.
4. Pierrick IA (FR, "7 prompts"): black background, glossy 3D mascots (Claude and OpenAI logos with faces), crossed-out icons (team, office, funding), sticker "CA PARAIT FOU ?", numbered dots 1-7, typed prompt cards in a drawn Claude window. Seen: 8,556 likes, 10.1K saves, 2,450 shares, 157 comments.
Views were not visible. These are survivors (we see winners only), so they say nothing about how often this style fails.

## What they have in common (FACT)
One fixed identity per account (palette, type, components); text synced to the voice with emphasis words; a drawn or real typing UI; numbered list; stickers; wipes. Saves are at or above likes on two of them.

## Why they may spread (HYPOTHESIS)
- The content is copy-paste utility (a command or prompt): worth saving and sending to "a friend who uses Claude". Our ep 80: 9 likes, 3 saves, 1 send on 786 views. Nothing in our reel was worth keeping; the text lives only on `/e/80`.
- Instagram's own stated signals (Mosseri, via ZoomSphere/Buffer/Hootsuite, Oct 2026): watch time, likes and sends; sends matter more than comments; track sends per reach, likes per reach, average watch time. Comment-keyword funnels (the "HUMAN" ask) are therefore the weaker lever on Instagram (TikTok not checked). Original, non-watermarked content is favoured. Secondary source says a Dec 2025 memo favours "raw, real human content over AI-generated material": not verified at the source.
- Numbered lists ("5 secrets", "7 prompts") promise a finite, savable set.

## Can we build it? (our honest read, before any sample)
- Closest and cheapest: style 3 (cream, drawn UI, typed keys): HTML/GSAP motion, our pipeline can do it.
- Style 4 needs 3D mascot art: stills may come from Canva/Adobe connectors (not tested); we cannot generate realistic video (Higgsfield-like): David would have to supply clips.
- Style 2 needs a presenter: not us.
- 1:1 copy of another account's artwork: no. Same structure in our own design: yes.
- UNKNOWN: whether our result reaches the same polish. Only a sample answers that.

## Tools (read from excerpts; not installed, not tested)
- HyperFrames (heygen-com/hyperframes): HTML/CSS/GSAP to deterministic MP4, Apache-2.0, needs Node 22+ and FFmpeg, `npx skills add heygen-com/hyperframes` (or `claude plugin install hyperframes@hyperframes`), repo active the day it was read. Closest to our current pipeline.
- Remotion official skills (`npx skills add remotion-dev/skills`): React-based, 28+ rule files; the Remotion licence is source-available (not Apache).
- digitalsamba/claude-code-video-toolkit: end-to-end promo pipeline, unverified.
- OpenMontage: AGPL, do not copy code.
- Run `skill-security-scanner` on anything before installing.

## Decisions waiting for David
1. One fixed visual identity for the series (this replaces the "different colour every episode" variety check).
2. Which style to sample first (recommended: style 3).
3. Permission to install HyperFrames (he asked to be reminded).
4. Make reels save-worthy: show the full text on screen for 2-3 s and ask for a send ("send to a friend who...").
5. Success bar (David, 31.10): 5,000-10,000 views per reel; below that it is not counted as success.
