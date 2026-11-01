# Tools scout, 1.11.2026

Method: WebSearch + WebFetch only (no Firecrawl, no installs into the repo, no commits). The GitHub MCP is locked to davidpit1565/videos-ai in this session, so repo facts come from fetching the public GitHub pages. The fetcher summarises pages with a small model, so numbers are "as shown by the fetch", not eyeballed. Tags: FACT (source) / HYPOTHESIS / UNKNOWN. Nothing here was installed or run except one ffmpeg test (section 5).

Container facts (FACT, tested here): Node v22.22.0, ffmpeg 6.1.1, numpy 2.5.3 present; pydub, scipy, soundfile NOT installed. Node 22 satisfies HyperFrames' requirement.

## 1. Skills and plugins

### 1.1 HyperFrames skills (heygen-com/hyperframes) - ADOPT (as the first thing to install, in a scratch branch)
- FACT (https://github.com/heygen-com/hyperframes): 77.0k stars, 7.1k forks, Apache-2.0, 6,596 commits. Last-commit date not shown on the page (UNKNOWN). The 77k figure is large; treat as "as shown", not independently checked.
- FACT: 7 skills. Core: `/hyperframes`, `/hyperframes-cli`, `/hyperframes-registry` (~450 ready blocks: transitions, titles, kinetic type, captions, charts, maps, 3D, camera moves), `/media-use` (music, SFX, voiceover, images, icons, logos, transcripts, cutouts, colour grades, mixing). On demand: `/figma`, `/slideshow` (decks, not MP4), `/remotion-to-hyperframes`.
- FACT: renders by seeking each frame in headless Chrome + FFmpeg, deterministic; supports GSAP, CSS, Lottie, Three.js, Anime.js, WAAPI; shader transitions via `@hyperframes/shader-transitions` (e.g. `flash-through-white`). Needs Node 22+ and FFmpeg only. Install: `claude plugin marketplace add heygen-com/hyperframes` then `claude plugin install hyperframes@hyperframes`, or `npx skills add heygen-com/hyperframes`; one block: `npx hyperframes add <block>`.
- Third-party listing (secondhand, vibeindex.ai): separate lottie / three / animejs / css-animations / captions skills, seven adapters incl. TypeGPU.
- What it does for us: our pipeline is already HTML+GSAP rendered by HyperFrames, so this is the same engine plus ~450 pre-made, tested motion blocks and agent instructions that stop us hand-rolling easing and transitions. Closest fit to the "smooth, premium" goal, and to CLAUDE.md's "motion is smooth, never robotic" rule.
- Cost/licence: free, Apache-2.0 (commercial use fine).
- Effort: low (one command). Risk: (a) `/media-use` can call HeyGen paid services, which would need an account/key: HYPOTHESIS that it is optional, UNKNOWN; do not give it keys. (b) The plugin changes how agents behave in the repo; run the existing `skill-security-scanner` first (already in CLAUDE.md). (c) GPU: README does not discuss GPU, so shader transitions on our CPU-only container are UNKNOWN: test one block, time the render.
- Verdict: ADOPT. Test in a throwaway folder, not in `/home/user/videos-ai`, and render one 10 s clip before touching real episodes.

### 1.2 Remotion skills (remotion-dev/skills) - SKIP for production, TRY only for reading
- FACT (https://github.com/remotion-dev/skills): 6.0k stars, 93 commits, 12 skills (best-practices, create, markup, studio, render, maps, captions, saas, interactivity, docs, upgrade, multimedia). Repo licence not stated on the fetched page (UNKNOWN). Install: `npx skills add remotion-dev/skills`.
- FACT (https://raw.githubusercontent.com/remotion-dev/remotion/main/LICENSE.md): Remotion itself is free for individuals, for-profit orgs with 3 or fewer employees, non-profits; others need a paid company licence (remotion.pro); you may not resell a derivative; the licence "will change slightly in Remotion 5.0". David (one person, employed elsewhere) qualifies for free today, but if the services business grows past 3 employees or he sells video production to clients through an incorporated company, re-check. Not legal advice.
- For us: a second engine means a rewrite of every build (React). HyperFrames ships `/remotion-to-hyperframes`, so the knowledge transfers the other way. The captions and maps rules are worth reading as ideas.
- Verdict: SKIP as an engine. Reading `remotion-captions` for caption ideas: optional.

### 1.3 GSAP official skills (greensock/gsap-skills) - ADOPT
- FACT (https://github.com/greensock/gsap-skills): "Official AI skills for GSAP", 17.7k stars, MIT. Skills: gsap-core (easing, stagger), gsap-timeline, gsap-scrolltrigger, gsap-plugins (incl. SplitText, Flip), gsap-utils, gsap-react, gsap-performance, gsap-frameworks. Install: `npx skills add https://github.com/greensock/gsap-skills`.
- For us: our reels are GSAP timelines; this teaches the agent correct easing/stagger/timeline nesting, which is where "robotic" motion comes from. Skip the scrolltrigger/react/frameworks files (irrelevant to a video).
- Cost: free. Effort: one command. Risk: low; it is text only. Verdict: ADOPT (core, timeline, plugins, utils only if you want to keep context small).

### 1.4 digitalsamba/claude-code-video-toolkit - SKIP
- Aggregator listings (secondhand): MIT; 949 stars (SrcLog, window ending 24.4.2026) vs "over 1,300" (a marketplace page); the two disagree and neither was checked on GitHub. Covers Remotion, ElevenLabs, FFmpeg, Playwright.
- It is Remotion-centred and promo-oriented; ElevenLabs is paid and we have our own voice pipeline. Verdict: SKIP.

### 1.5 Skills already in the repo that matter
FACT (local listing): `.claude/skills` already has `animate`, `animation-vocabulary`, `apple-design`, `emil-design-eng`, `improve-animations`, `find-animation-opportunities`, `website-animation-library`, `whisper`, `video`, `audiocraft-audio-generation`. These are web-UI animation guides; HYPOTHESIS: useful for easing/timing vocabulary, not tested against a render. Audiocraft (MusicGen/AudioGen) can generate SFX but needs a GPU for practical speed (HYPOTHESIS), and our rule says shipped music comes from the licensed library: SKIP for music, TRY for SFX only if CPU speed is tolerable (UNKNOWN).

## 2. Libraries for typography and motion inside HyperFrames

### 2.1 GSAP plugins (SplitText, MorphSVG, Flip, DrawSVG, etc.) - ADOPT
- FACT (https://gsap.com/community/standard-license/, effective 30.4.2025, modified 30.5.2025): "GSAP is now free for everyone, thanks to Webflow's support"; the plugins that used to be members-only, including SplitText and MorphSVG, "can be used in commercial projects at no charge".
- FACT, the one restriction: no use "in tools that allow users to build visual animations without code" that compete with Webflow's visual animation builder ("Competitive Products"); needs written consent. The licence says AI-generated GSAP code is not a prohibited use. A fee-charging end-user clause appears in a third-party tracker's copy only; the official page does not address it (flagged conflict, UNKNOWN: re-read gsap.com before selling a tool built on GSAP).
- Our case: faceless reels and client videos are not a visual animation builder. HYPOTHESIS: safe. If David ever sells a "make your own animation" web app, ask Webflow first.
- Use: `npm i gsap` (the old `gsap-trial` package is deprecated, FACT via npm/jsdelivr README). SplitText gives per-char/word/line splitting that handles wrapping and kerning better than our `MK.splitWordsSafe` (HYPOTHESIS, test on a Hebrew-free English headline). MorphSVG for icon-to-icon morphs. Effort: low. Risk: low. Verdict: ADOPT; check how `export/motion-kit.js` loads GSAP (not found by a quick grep of `video/reel-template.html`, UNKNOWN) so the plugin script is bundled locally, not fetched from a CDN at render time.

### 2.2 Lottie - TRY
- FACT (via HyperFrames listing, secondhand): Lottie runs through lottie-web/dotLottie registered on `window.__hfLottie`, paused for frame-accurate seeking.
- FACT (https://help.lottiefiles.com/hc/en-us/articles/900002438343): free LottieFiles public animations fall under the Lottie Simple License: commercial use free, no attribution needed, no reselling originals or building a competing service. Conflict: LottieFiles' commercial-use page table marks the Free plan "prohibited" for platform use, with public animations excluded; premium and creator animations can have other licences (CC, royalty-free). So: only take items marked under the Simple License and keep the URL and licence in a note.
- For us: small tick/arrow/sparkle accents. Verdict: TRY for a few accents; low value vs typography.

### 2.3 Rive - SKIP
- FACT (secondhand search results): the runtimes (rive-wasm, Flutter package) are MIT; rive-wasm last push shown 14.5.2024. Free-plan terms for the editor and .riv files: UNKNOWN. We have no designer making interactive state machines; Lottie covers accents. Verdict: SKIP.

### 2.4 three.js and shaders - TRY (one hero beat per episode, at most)
- FACT (HyperFrames README): Three.js is a supported adapter; WebGL shader transitions exist. CLAUDE.md already reserves one GPU-tier "fragment shatter" beat per episode. UNKNOWN: render time on 4 CPUs with software WebGL (SwiftShader). Test one shader transition at 1080x1920 for 3 s and record seconds-per-frame before promising anything. Verdict: TRY, measured.

### 2.5 Easing helpers - ADOPT (free, built in)
GSAP's own eases (`power3.out`, `expo.inOut`, `CustomEase`, `CustomBounce`) are included under the same free licence (HYPOTHESIS that CustomEase is part of the freed set; the page names SplitText and MorphSVG explicitly and says formerly members-only plugins are free). Rule of thumb from the repo's own motion rule: long eased curves, no `linear`, overlap tweens with negative offsets. No extra library needed.

## 3. Real product screenshots, recordings, logos

### 3.1 Playwright real-page recording - ADOPT
- FACT (https://playwright.dev/docs/videos): `recordVideo: {dir, size}` on a browser context; default video size is the viewport scaled to fit 800x800, so set `size` equal to the viewport (e.g. 1080x1920 or a 540x960 mobile viewport at 2x); the file is only written after `context.close()`; output is video, not frame-exact. Newer option `show.actions` outlines each action's element (useful as a free "ring").
- Limits (HYPOTHESIS): recording is real-time screencast at a modest frame rate, so it is not as smooth as our frame-by-frame render. Better path for smooth motion: record the real page with `page.screenshot` per step, or capture the real page once and animate it in HTML (CLAUDE.md already wants real motion from real recordings). The container has Playwright + Chromium preinstalled (given in the brief), outbound HTTPS via proxy.
- Hard limit (FACT in CLAUDE.md terms): login-walled apps (ChatGPT, WhatsApp) cannot be recorded without David's session; the repo's existing `channel/assets/ep<N>-screen/` approach (his phone recordings) stays the source for those. Never log in with his credentials from the container.
- Verdict: ADOPT for public pages (docs, pricing pages, product landing pages); keep phone recordings for apps.

### 3.2 Real logos - ADOPT a two-source routine
- Simple Icons: FACT (https://github.com/simple-icons/simple-icons): 26.1k stars, CC0-1.0, over 3,400 brand SVGs, but asks users to read its legal disclaimer (the SVG licence is CC0; the trademark belongs to the brand). Good for a quick mono SVG; our rule says "real current logo", so confirm the shape matches the brand's own page.
- Brand's own press/brand page (official site, Wikimedia Commons) stays the primary source per CLAUDE.md; Simple Icons is the fast fallback. Colour full-colour marks (e.g. Google, Gemini sparkle) are often missing or mono in Simple Icons: HYPOTHESIS.
- Trademark: Pixabay's licence explicitly forbids commercial use of content showing recognisable brands/logos for goods or services (FACT, https://pixabay.com/service/license-summary/). Editorial use of a brand mark in a tips video is a separate legal question: UNKNOWN, not legal advice. Keep marks small, unaltered, never implying endorsement.
- HyperFrames `/media-use` also lists "icons and logos" (FACT, README); check what it fetches from before trusting it (UNKNOWN).

## 4. Reading public reel metadata (Apify and no-login options)

### What David must do for any Apify actor (FACT, https://docs.apify.com/platform/integrations/api)
1. Create a free Apify account (Console). 2. Console, "Settings", "API & Integrations": create a token; turn on "Limit token permissions" so it can only run actors. 3. Put it only in an environment variable or Vercel env var, never in chat, git or a file (CLAUDE.md secrets rule). Tokens can expire and be rotated (old one kept 24 h). Claude in this container does not have a token and should not be given one in chat.
- Free plan: sources agree on $0/month with $5 platform credit per month, no card, not rolled over (https://use-apify.com/docs/what-is-apify/apify-free-plan, and the tubetext page below). The sources disagree on RAM (8 vs 16 GB); irrelevant for us. Check apify.com/pricing before relying on it; I could not open the official page.
- Legal/ToS: HYPOTHESIS that scraping public reels breaks Instagram's terms even if actors market "no login". Use it for our own research on public data at tiny volume, not as a product feature.

| Actor | Gives | Price (as listed) | Verdict |
|---|---|---|---|
| tubetext/instagram-reels-transcript (https://apify.com/tubetext/instagram-reels-transcript) | transcript (Whisper), hook line, caption, hashtags, playCount, likeCount, commentCount, duration, optional SRT/segments; no login/cookies; song-only reels free | $6.00/1000 reels, $4.50 on higher plans, about $0.006 per reel; on-screen text +$0.002; free $5 covers about 800 reels (the page's own estimate). 257 users, 163 monthly, 99.6% success, no ratings, prices "checked October 2026" | TRY: cheapest way to get spoken text + views for competitor reels. New actor, tiny user base: sample 10 reels first. No music name field listed. |
| apify/instagram-reel-scraper (https://apify.com/apify/instagram-reel-scraper) | caption, `videoViewCount`, `videoPlayCount`, likes, comments, `musicInfo` (artist_name, song_name, uses_original_audio, audio_id), transcript via `includeTranscript` (per-minute add-on) | page header "from $1.00/1000 reels"; its README says $2.60/1000 on Free, $2.30 Starter (page contradicts itself, UNKNOWN which is current); transcript and video download are add-ons; $5 credit ~2,000 results at Free rate. 4.39/5, 181,815 users, 22,517 monthly, 100% runs succeeded. Shares need a paid plan | ADOPT as the music + views source: official Apify-made, the only one verified to expose music name and view/play counts. |
| TikTok: clockworks/tiktok-transcript-extractor | transcript | from $1.70/1000 videos (search snippet; fields not verified) | TRY, verify fields first. |
| TikTok: maximedupre/tiktok-transcript-scraper | text, timed segments, SRT/VTT, metadata, engagement counts, music details; no video download | pay-per-event: $0.001 per run + $0.0009 per transcript (search snippet) | TRY: cheapest listed with music details. |
| TikTok: agentx/tiktok-transcript | view_count, audio_artist among fields | not captured | UNKNOWN price. |
Third-party names (brilliant_gum, khadinakbar, etc.) appeared in searches with $1.50-$15/1000 prices; unverified, skip.

### No-login, no-Apify options
- Instagram oEmbed via Meta Graph: FACT (https://developers.facebook.com/docs/instagram-platform/oembed): endpoint documented as `graph.facebook.com/v26.0/instagram_oembed?url=`; sample response shows html/width/provider fields, no views. Whether a token is required: page does not say (UNKNOWN). Gives no view counts or music: not useful for demand data.
- TikTok oEmbed: FACT (https://developers.tiktok.com/doc/embed-videos): plain GET `tiktok.com/oembed?url=`, no auth shown; returns title-less embed fields per the example (version, type, html, width, height); the page says it "will be deprecated soon". No views/music.
- yt-dlp on public reels: search results conflict. One skill page claims metadata-only works without login; a GitHub issue (https://github.com/yt-dlp/yt-dlp/issues/7165) reports "login required" without cookies; another report shows fallback to the embed page with "some metadata might be missing". UNKNOWN for 2026. The repo already has an `anthropic-skills:video-download` skill that uses yt-dlp: TRY it on one public reel before paying for anything; it needs no secret for public posts if it works. Do not pass David's cookies into the container.
- Instaloader: not verified (UNKNOWN); it normally wants a login for reels, which we will not provide. SKIP.
- Our own studio: `/api/state` after David gives the PIN (CLAUDE.md) is the only source of our own reach/saves, and Apify's actors cannot read private insights. Competitor analysis stays HYPOTHESIS-level.

## 5. Audio: SFX libraries and a Python way to add typing/whoosh/pop

### Free SFX with commercial use
- Pixabay Sound Effects: FACT (https://pixabay.com/service/license-summary/ and FAQ): free for commercial use, no attribution; cannot sell/redistribute content unmodified on its own; no commercial use of recognisable brands/trademarks inside content; Content ID not mentioned; no effective date on the page. Same source as our music library, so one routine. ADOPT.
- Freesound: FACT (https://freesound.org/help/faq/): licences CC0, CC-BY, CC-BY-NC; CC0 may be used commercially (even sold) with no attribution; CC-BY needs attribution; CC-BY-NC is not allowed for commercial work; downloading requires a registered, logged-in account (David's task, not ours, and no password in chat). Filter to CC0 only and log each file's URL. TRY for sounds Pixabay lacks.
- Mixkit: I could not read the SFX licence text (fetched pages did not include it), so UNKNOWN. SKIP until read.
- HyperFrames `/media-use`: lists SFX and music via HeyGen or free local tools (FACT); sources and licences of the free path UNKNOWN. TRY after install; read what it downloads from.
- Rule: every SFX gets a line in an `audio/sfx/MANIFEST.md` (file, source URL, licence, date), the way `audio/music-library/MANIFEST.md` works. Never from AI tools unless licence is clear.

### Python/ffmpeg way (tested)
- FACT (ran in this container, scratchpad `/tmp/claude-0/-home-user-videos-ai/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/scratchpad/tools/`): plain ffmpeg places one-shot sounds on a narration at exact times with no new library: `adelay=<ms>:all=1` per SFX, `volume=` per SFX, then `amix=inputs=N:normalize=0:duration=first`. A 6.0 s mix with two delayed sounds came out at exactly 6.000000 s. numpy 2.5.3 is present; pydub/scipy/soundfile are not, and are not needed.
- Proposed small script (not written into the repo; no file was created there except this note): read the build's scene/word cue times from the cues JSON, map event types (`type`, `pop`, `whoosh`, `tick`) to files in `audio/sfx/`, generate the ffmpeg filter graph, write `sfx.wav`, then mix it into the narration bus at -22 to -28 dB under the voice. Run `audio/voice_quality.py` and `check_music_bed.py` afterwards (existing rules). Typing: 40-80 ms tick samples, jittered +-15 ms, never evenly spaced (matches "no stepped rhythm").
- Risk: SFX can mask the voice or hit the voice's soft word endings; keep them off word onsets of flagged lines. HYPOTHESIS: three to five SFX per reel at low level read as "premium"; test A/B on one episode, measure retention, per content-memory rules. Verdict: ADOPT the ffmpeg approach, TRY the SFX effect.

## Ranked summary
| Item | Verdict |
|---|---|
| HyperFrames skills + registry blocks | ADOPT |
| GSAP official skills | ADOPT |
| GSAP SplitText/MorphSVG (free, with Webflow competitor carve-out) | ADOPT |
| Playwright recording of public pages | ADOPT |
| ffmpeg adelay/amix SFX placer + Pixabay SFX | ADOPT |
| apify/instagram-reel-scraper (views + music) | ADOPT (needs David's token) |
| tubetext transcripts, TikTok actors | TRY |
| yt-dlp public-reel test | TRY |
| Simple Icons as logo fallback | TRY (brand page first) |
| Lottie, three.js/shader beat, Freesound CC0 | TRY |
| Remotion, digitalsamba toolkit, Rive, Instaloader, Mixkit | SKIP |

## Five best next actions, in order
1. In a scratch folder (not the repo), run `skill-security-scanner` on heygen-com/hyperframes, then install it and render one existing episode's scene as a HyperFrames block test; record render seconds per frame (answers the GPU/shader UNKNOWN too).
2. Install `greensock/gsap-skills` (core, timeline, plugins, utils) and rebuild one hook headline with free SplitText and a long eased stagger; compare to the current `MK.splitWordsSafe` result frame by frame.
3. Write the small ffmpeg SFX placer plus `audio/sfx/MANIFEST.md`; download 15-20 Pixabay SFX (whoosh, pop, tick, type) with licences logged; A/B on one episode.
4. David creates a free Apify account and a permission-limited token stored only as an env var; run `apify/instagram-reel-scraper` on 10 public competitor reels (est. cost about $0.03 at $2.60/1000, under the $5 free credit; the price is contradictory on the actor page) to get views and music names; try `yt-dlp` on one public reel first, since it may need no account.
5. Make a "brand mark" routine: brand page first, Simple Icons second, a record of source URL per logo, plus a Playwright script that screenshots public product pages at 1080x1920 for real-interface scenes.
