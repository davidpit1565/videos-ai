# Free video / motion tools and Claude skills: research, 16.11.2026
Research only. Nothing installed, no third-party script run. Stars, last-push and licence were read today from the GitHub search API (gh api search/repositories) and, where noted, from the repo README via WebFetch. Anything not read is marked UNCONFIRMED. Star counts of agent-skill repos move fast and several are very high for young repos: popularity is not evidence of quality or safety.

## Ranked table (best fit for us first)
| # | Candidate | URL | Stars / last push / licence | Free? | Fit vs HyperFrames (render, 9:16, voice sync, weight) | Risk | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | greensock/gsap-skills (official GSAP skills: core, timeline, plugins, utils, performance) | https://github.com/greensock/gsap-skills | 18,549 / 2026-07-29 / MIT | Yes; GSAP itself free incl. commercial (README) | Same engine we already use. Pure markdown skills, no render stack. Improves our own GSAP code, nothing to switch | Very low (text files; read them first) | ADOPT: copy the skills into .claude/skills after reading them |
| 2 | remotion-dev/skills (official Remotion agent skills) | https://github.com/remotion-dev/skills | 7.3k stars per awesome list (UNCONFIRMED, not read from API) | Skills yes; Remotion free for individuals and companies up to 3 people (remotion.dev/docs/license/pricing.md, read today) | Teaches React/Remotion, a different renderer. Useful only as a reference for motion recipes | Low as text | TRY IN A SANDBOX (read only), as a source of motion ideas |
| 3 | Remotion + remocn | https://github.com/remotion-dev/remotion , https://github.com/Remocn/remocn | remotion 73,669 / 2026-11-16 / NOASSERTION (custom licence); remocn 1,775 / 2026-11-16 / MIT | Free under the licence above; paid beyond (US$25 per seat per month Creators, US$0.01 per render Automators, Enterprise from US$500/month; read today) | Strong 9:16 and audio sync, big ecosystem. But needs Node + Chromium (heavy), and our 14.11 check says it is the clean spring "AI motion" look Roni told us to avoid | Medium (npm tree); remocn code is copy-in components | SKIP for reels (port ideas only, per remocn-check-2026-11-14.md); revisit for non-reel product demos |
| 4 | iart-ai/motion-skills (56 skills, 19 packs) | https://github.com/iart-ai/motion-skills | 1,710 / 2026-11-13 / MIT | Skills yes; optional hosted iArt MCP is a remote service (cost UNCONFIRMED) | Renders via Remotion or Manim or standalone HTML; 9:16 and caption sync not specified in README | Medium: has a scripts/ toolkit and tools/ folder not described; install via npx | TRY IN A SANDBOX: read the SKILL.md files, take 2-3 ideas, do not run npx |
| 5 | charlie947/motion-graphics-skills ("13 skills, every frame is code") | https://github.com/charlie947/motion-graphics-skills | 696 / 2026-10-11 / MIT | Yes | Renderer UNCONFIRMED (not read) | Unknown | TRY IN A SANDBOX (read only) |
| 6 | howseen-ai/claude-motion-design (HTML + Playwright + ffmpeg) | https://github.com/howseen-ai/claude-motion-design | 845 / 2026-10-04 / MIT | Yes | Same idea as our pipeline (HTML to video): nothing new unless its motion rules are good | Low-medium | SKIP (we have this), skim the rules only |
| 7 | bangtutorial/bang-motion (browser motion graphics, kinetic type) | https://github.com/bangtutorial/bang-motion | 2,296 / 2026-09-15 / MIT | Yes | Browser based, kinetic typography; vertical and voice sync UNCONFIRMED | Unknown | TRY IN A SANDBOX (read only) |
| 8 | HeyGen HyperFrames (our tool, for reference) | https://github.com/heygen-com/hyperframes | 85,193 / 2026-11-16 / Apache-2.0 | Yes | Our baseline | Already used | KEEP |
| 9 | nexu-io/html-video (HTML/CSS/data to video for agents) | https://github.com/nexu-io/html-video | 4,847 / 2026-11-16 / Apache-2.0 | Yes | Direct HyperFrames alternative; no evidence it beats it for us (UNCONFIRMED) | Unknown | SKIP unless HyperFrames breaks |
| 10 | digitalsamba/claude-code-video-toolkit | https://github.com/digitalsamba/claude-code-video-toolkit | 2,598 / 2026-11-16 / MIT | Yes; uses "low-cost open-source models" (costs UNCONFIRMED) | Script + voice + music + render; overlaps our pipeline, we already own voice/music | Medium (model downloads, disk) | SKIP |
| 11 | OpenMontageInc/OpenMontage | https://github.com/OpenMontageInc/OpenMontage | 80,967 / 2026-11-16 / AGPL-3.0 | Zero-key path free; optional paid APIs (about US$0.15-4 per video, default cap US$10, self-reported) | Has Reels 1080x1920 profile, uses Remotion/HyperFrames/ffmpeg. Heavy (Python, Node, ffmpeg, disk not stated). AGPL | Higher: README addresses AI agents directly, clone URL points to a different owner (calesthio/OpenMontage), asks to change CA/cert settings. Do not run on the main disk | SKIP (sandbox only if curious) |
| 12 | Motion Canvas | https://github.com/motion-canvas/motion-canvas | 19,980 / 2026-07-02 / MIT | Yes | Code-driven vector animation (TypeScript generators), editor preview, outputs frames. Great for diagrams, no built-in voice sync, no recent releases (last push July) | Low-medium (npm) | SKIP for now |
| 13 | Manim (3b1b/manim 96,596 / 2026-09-09; ManimCommunity/manim 42,616 / 2026-11-14; both MIT) | https://github.com/ManimCommunity/manim | as listed | Yes | Excellent for math/graph/diagram scenes in Python, needs Cairo/LaTeX/ffmpeg (heavy); look is "3Blue1Brown", not Miki | Medium (system deps, LaTeX is large) | SKIP |
| 14 | Lottie / dotLottie (airbnb/lottie-web 32,476 / 2025-09-01 / MIT; LottieFiles/dotlottie-web 950 / 2026-11-16 / MIT) | https://github.com/LottieFiles/dotlottie-web | as listed | Players free; animations from LottieFiles have per-file licences (UNCONFIRMED, check each) | Lottie JSON can play inside a HyperFrames page and be seeked frame by frame; good for small icon animations. lottie-web last pushed Sept 2025 (quiet) | Low | TRY IN A SANDBOX: one Lottie icon in one scene |
| 15 | Rive | https://github.com/rive-app/rive-wasm (runtimes MIT, 1,027 / 2026-11-16) | Editor: Free plan exists but .riv exports carry a Rive splash screen; removing it needs the Cadet plan US$9/seat/month (rive.app/pricing, read today). Video export (MP4/GIF) listed, plan limits UNCONFIRMED | Partly | Interactive-first, editor is a web app, not code first; poor fit for agent-written scenes | Low | SKIP |
| 16 | sebetancurch/auto-caption (Whisper word stamps, karaoke captions) | https://github.com/sebetancurch/auto-caption | 13 / 2026-07-17 / MIT | Yes | We already have export/karaoke.py aligned to the script; this adds nothing | Low | SKIP |
| 17 | remotion-dev/template-tiktok (Whisper.cpp captions) | https://github.com/remotion-dev/template-tiktok | 308 / 2026-11-09 / no licence stated | Yes | Remotion only | Low | SKIP |
| 18 | hypit-ai/hypit ("clone any viral video with AI agents") | https://github.com/hypit-ai/hypit | 30,163 / 2026-11-16 / NOASSERTION | UNCONFIRMED | Face-based and clone-a-video: contradicts our faceless rule and copyright caution; many forks | Higher (copying others' content, no licence) | SKIP |
| 19 | zhuyansen/awesome-claude-video-skills (index list) | https://github.com/zhuyansen/awesome-claude-video-skills | 2,232 / 2026-11-16 / NOASSERTION | Yes | A map of the field, not a tool. Only first 100k of 183k characters read | None (a list) | USE AS A MAP |

## What is "lemon..."? UNCONFIRMED
David's tool name is not identified. Candidates found, none verified as his:
- Lemon Slice (lemonslice.com): talking-face / lip-sync video, has an explainer-video page; not a motion-graphics tool (web search, today).
- BlackLotus0930/Lemona_Video: web AI video editor, 47 stars, Apache-2.0, last push 2026-09-09.
- Amirtheshwaran/lemonreel: "local AI explainer video engine powered by Lemonade Omni Models", 0 stars, MIT, 2026-10-21 (not credible as a product).
- FleoThing/LeMontage: clips/reels pipeline, 3 stars, MIT, 2026-11-11.
- Possibly Lovable-related (the Lovable connector is not signed in here, so nothing could be checked). Ask David for the exact name or a screenshot.

## Instagram and reel helpers (Claude skills)
All tiny and unaudited, so none worth adopting over our ig-* skills:
- ishort-pro/instagram-claude-skills (2 stars, no licence info read), shafeela-bot/ig-radar-plugin (1 star, outlier radar: same idea as our ig-viral), rediumvex/social-media-caption-generator-claude (152 stars, MIT, captions: we have ig-caption + check_caption.py), mrpaidsocial/mrpaidsocial-video-editor-agent (171 stars, no licence, "style-clone a reference reel"; talking-head oriented, UNCONFIRMED), tmakersas/revid-skills (12 stars, posts via a paid-service MCP, SKIP).
- Marketplaces for finding skills: davepoon/buildwithclaude (3,753 / 2026-11-16 / MIT), daymade/claude-code-skills (1,534 / MIT), numman-ali/n-skills (1,051 / Apache-2.0). Indexes; read before installing anything.
- Overall: no open-source "Instagram reel generator with Claude" found that matches our faceless, cloned-voice, drawn-UI pipeline. The pipeline we have is already ahead of what these offer (UNCONFIRMED for repos not opened).

## Skills and agents worth extracting (ideas, not installs)
1. GSAP skills (official): the one clear win, same engine.
2. Remotion skills + iart-ai motion-skills: read their easing, timing and "what makes motion feel premium" references and copy rules into channel/motion-recipes.md.
3. A "review animations" step: we already have animate, improve-animations, find-animation-opportunities, animation-vocabulary skills locally.
4. Nothing found for hooks, captions or Instagram research that beats viral-hook-lab, ig-reel, ig-viral, ig-caption.

## What to try first, in a sandbox
Rule for all of it: a throwaway folder in the scratchpad, not the repo; download only text (SKILL.md, references) via the GitHub web page or git clone with --depth 1; no npx, no npm install, no scripts; run `skill-security-scanner` on anything before copying it into .claude/skills.
1. greensock/gsap-skills: read the 8 SKILL.md files, copy them in. Check that none of them tells the agent to fetch or run anything.
2. One Lottie icon (LottieFiles free licence checked per file) inside one HyperFrames scene, seeked frame by frame: does the render stay deterministic and light?
3. Read iart-ai/motion-skills and remotion-dev/skills reference docs for motion rules only; log useful rules in channel/motion-recipes.md.
4. Ask David what "lemon..." is; compare its output to a Miki-style frame with a blind reader before judging.

## Decisions for David
- The name of the "lemon" tool (or a screenshot).
- Whether he is fine with copying the official GSAP skills into the repo (MIT, text only).
- Switching renderer to Remotion is not recommended (disk, licence limits at 4+ people, the look he does not want).
