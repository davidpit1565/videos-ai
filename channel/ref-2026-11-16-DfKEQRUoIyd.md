# Reel DfKEQRUoIyd: "You don't need a face to go viral" (seen 16.11.2026). NOT a style reference

David commented the keyword on it; the creator sells a paid "AI video skill". This file is what the creator says, what can be checked, and what we can learn or rebuild for free.
Contact sheet: `channel/assets/refs-2026-11-16/DfKEQRUoIyd-sheetA.jpg`. Transcript and frames: session scratchpad `refs16/DfKEQRUoIyd/`.

## Facts (yt-dlp, 16.11.2026)
- Account **@adilet.fndr** (display name "Adilet"; the Gumroad seller name is "Adilet Aussarbekov"). Published 31.10.2026, 62.7 s, 514 likes, 1,710 comments (keyword comments).
- Caption: "I grew this account to 47K in 6 weeks without showing my face once. Every reel here is AI-animated, made with one folder of 191 files ... Drop it into Claude Code, type one line, and it writes, voices, animates and renders the whole reel. It even watches its own video and fixes the weak moments. Comment SKILL and I'll send you the link."

## What the reel says (transcript, faster-whisper)
1. 0-7 s: "You don't need a face to go viral. I grew this account to 47,000 followers in six weeks and I've never shown mine once."
2. 7-22 s: the urgency pitch: "AI-animated reels are where early TikTok was. Almost nobody's making them ... in three months everyone will be doing this ... First come, first served."
3. 22-43 s: the method: "most AI reels look like slop ... the system behind them isn't one prompt. It's 191 files. Hook patterns and pacing rules decoded from my viral reels. Spring physics, whip pans and zoom kicks ... word-timed captions where the keyword lands a beat before it's said, and an audio chain on top of ElevenLabs mastered for Instagram."
4. 43-60 s: "You drop the folder into Claude Code, tell it what the reel's about in one line, and it writes, voices, animates and renders ... It even watches its own video and fixes the weak moments. No camera, no face, no editing."
5. 60-62 s: "Comment skill and I'll send you the link."
- Picture: a cartoon presenter of himself (beanie, glasses, beard) in the lower third, a halftone/paper texture, red accent, italic serif accent words, an animated headline at the top, a new illustrated card every 1.5 s (his own profile screenshot, "47K followers", a "FILLING FAST 9/10" bar, a market of seats, a folder of files, a Claude Code window "Drop to add a skill", a waveform "IN SYNC" card, "MASTERED -14 LUFS").

## What the sales page says (adiletfndr.com and the Gumroad page, read through Exa 16.11.2026; his claims, NOT verified)
- Price: the site shows **$27**; the Gumroad listing "AI Video Editing Skill" shows **$97** (one ZIP, 4.0 MB, 19 ratings). David was quoted **$57** (in the DM, presumably). Three different prices for the same product: treat any price as the seller's, changing, unverified.
- Follower claims differ: "47k followers in 6 weeks" (site and reel) vs "37k followers in 4 weeks" (Gumroad text); "5.9M views", "$2.5k+ in brand deals", an Instagram dashboard screenshot. We cannot verify any of these; dashboard screenshots are easy to stage and also easy to be true. Unverified.
- Contents claimed: "191 files · 4.2 MB": engines 44, library 61 (58 scene files "from my viral reels"), guides 37, fonts 22, tools 10, bonus 2 ("brand-deals.pdf"); SKILL.md, mechanics.js, tts.py, reel.mjs; three styles (classic, 3D, illustrated); spring physics, whip pans, zoom kicks, halftone wipes, depth of field; word-timed kinetic captions; an ElevenLabs audio chain; a cartoon presenter "from one photo" with lip sync; a self-check that "scores its own motion"; works in Claude Code, Cursor or Codex; ElevenLabs free plan; 7-day money-back; no reselling.
- The urgency claim "by 2027 this is saturated, the ones who move first win" is a sales device, not evidence.

## What we already have that does the same (free, in this repo)
| his claim | ours |
|---|---|
| hook patterns and pacing rules | `channel/hooks-guide.md`, the `viral-hook-lab`, `ig-reel` (hookscore, beats.py) skills |
| spring physics / motion | `export/motion-kit.js`, `channel/motion-recipes.md`, HyperFrames + GSAP |
| word-timed captions, keyword a beat early | `export/karaoke.py`, `export/headline_sync.py` (ours lights the word as spoken; his lands it a beat early: a small, testable change) |
| ElevenLabs audio chain, mastered for Instagram | our own cloned voice + `audio/voice_doctor.py`, `voice_quality.py`, -14 LUFS mastering |
| "watches its own video and fixes weak moments" | `export/check.sh` (safe_check, qa.py frozen runs, card durations), blind-reader checks |
| one prompt to finished reel | `export/produce.sh` |
- What his kit has that we lack and could build ourselves: (1) the keyword lands a beat BEFORE it is spoken (try a 0.15-0.25 s lead in `headline_sync.py` as an experiment); (2) a scene library from proven reels (ours would be Miki-style scenes from ep86/89); (3) a texture layer (paper/halftone) for Roni's "must not look AI" rule.
- Learning, not copying: his reel is itself a faceless, cartoon-presenter, 1.5-s-per-card reel; the comment count (1,710 on 514 likes) comes from the keyword-DM mechanic, which he uses to sell.

## Should David buy it? (judgement)
Not needed for the pipeline: almost everything it claims, we have and have measured. If David wants to see the scene library for ideas, the $27 site price is the cheapest of the three and has a 7-day refund (his claim): his call, his money. Nothing from it may be copied into a published reel as-is (his scenes are his).

## To fill when David sends the DM
- DM text (verbatim):
- Price and link in the DM:
- Any claim in the DM we can check:
- Differences from the site/Gumroad claims above:
