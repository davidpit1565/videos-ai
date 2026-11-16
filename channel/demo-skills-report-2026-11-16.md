# Demo of the free motion skills: report, 16.11.2026
Internal demo, NOT an episode, never to be published. No voice. David approved adopting the skills and asked for one video to see what each gives.

- Video: `video/demo-skills/out/demo-v1.mp4` (1080x1920, 33.0 s, 30 fps, 10.2 MB). Review copy: `video/demo-skills/out/demo-v1-review.mp4` (720 px wide, crf 27, 1.4 MB).
- Build: `video/demo-skills/hf/index.html` (hand-written, one file). Sources and licences: `video/demo-skills/SOURCES.md`.
- Music: quiet real-library bed, `minimal--ambient-soft--avelinemusic.mp3` (mood "ambient"; the picker has no "calm"), at -9 dB. Measured (mean -18.8 dB before the cut, no quiet stretch), NOT heard by me.
- How it was checked: 14 still frames from the rendered file (0, 1.2, 5, 10, 10.9, 11.6, 12.25, 15, 16.4, 18.3, 20, 21.9-22.3, 25, 30, 32.6 s) looked at by eye, and ffmpeg freezedetect (no still stretch of 1 s or more). I cannot watch motion: the smoothness below is judged from the code and from stills, so David's eye decides.
- Scores are labels (my judgement, not measurements).

## What was installed
| Folder in `.claude/skills/` | From | How |
|---|---|---|
| `gsap-core`, `gsap-timeline`, `gsap-plugins`, `gsap-utils`, `gsap-performance` | greensock/gsap-skills, commit aed9cfd, MIT | copied unchanged, text only |
| `motion-kinetic-typography` | iart-ai/kinetic-typography-skills, commit 2b79c81, MIT | SKILL.md + 1 reference; install/script lines and advert footer removed |
| `motion-animation-principles` | iart-ai/motion-design-skills, commit b85e50c, MIT | SKILL.md + 2 references; advert footer removed |
| `motion-remotion-notes` | remotion-dev/skills, commit 3e20ac7 | OUR OWN notes, nothing copied (no licence file; Remotion's licence is not MIT; our repo is public) |
Each has a SOURCE.md (the five gsap ones point to `gsap-SOURCE.md`). No name clash with existing skills. Nothing was run or installed.

## Rejected, and why
- iart-ai/motion-skills itself: the repo holds NO skills, only a README, a showcase and shell tools; the skills live in 19 pack repos. Two packs were read; from them only the two skills above. Not copied: all `scripts/` (shell), the After Effects `.jsx` scripts, `showcase.html`, plugin manifests, the hosted "iArt MCP" (a paid remote service that wants an API key).
- Remotion skills as text: not copied (licence), and they instruct `npx remotion add` / `bunx remotion add` installs for a renderer we do not use.
- gsap-react, gsap-frameworks, gsap-scrolltrigger: no use in a rendered video.
- Lottie animations with expressions (ripple, starfish, lights in the lottie-web test folder): they need the full lottie build, which evaluates code strings stored inside the JSON. Used the light build (no `eval`) and an animation with no expressions.
- NVIDIA SkillSpector scan: not run (not installed; it needs a pip install from GitHub and the disk had 2.3 GB free). The review was by reading every copied file plus a pattern search. Nothing addressed the agent to fetch, exfiltrate, change settings or hide text. The only "steering" found: gsap-core tells the agent to recommend GSAP, and the iart files carried advert links (removed).

## Clip 1 (0-11 s): GSAP skills
What it uses: one master timeline with three nested clip timelines on labels; `defaults`; labels and the position parameter (`'<0.18'`, `'ring+=0.1'`) instead of absolute times; SplitText with masks for the header and the words; DrawSVG for the hand-drawn ring and for the path; `stagger: {each, from: 'center'}` in and `from: 'edges'` out; MotionPath for the dot; `gsap.utils.selector/toArray`, `gsap.parseEase`; CustomEase; `autoAlpha`.
- Compared with how we built before: our builds (`video/ep102/build102v3.py`) emit hundreds of `tl.fromTo(..., <absolute time>)` lines from Python with `power2`/`sine` eases and pre-split words in the HTML. Here the whole 11 s clip is about 40 lines, and moving one label moves everything after it.
- Real gains: (1) mask reveal per letter/word with SplitText instead of opacity pops: the type looks set, not faded; (2) the ring is truly drawn along its path, and any SVG path can be drawn the same way; (3) stagger from the centre/edges in one line; (4) an object can follow a curve.
- No difference: easing quality as such. `power2.out` vs the skill's advice is the same engine; the skill does not make a tween smoother. Also our voice-synced word builds need absolute times from the cues anyway, so labels help only inside a scene.
- Flaw seen in the stills: the ring sits tight on "ONE" and its left edge is at about x 84, outside the 108 line (decorative, but not clean).
- Adopt: SplitText masks for heavy lines, DrawSVG for the ring, nested scene timelines with labels inside each scene, CustomEase for one house curve. Do not adopt: back/elastic/bounce eases (against Miki).
- Label: STRONG as a way of working, PROMISING as visible quality. About 78/100 for the clip.

## Clip 2 (11-22 s): motion rules (iart-ai skills + Remotion notes)
What it uses: static type locked first, split by LINE; mask reveal 110% to 0; enter on `cubic-bezier(0.16,1,0.3,1)` at 0.6 s per line, 80 ms between lines, whole reveal under 0.8 s; exit on an ease-in and faster than the enter; blur-in for the lead line; stroke draw-on underline (dash-offset recipe); then anticipation (a 0.11 s counter-move), an arc instead of a straight slide, a no-bounce spring for the travel (Remotion idea), follow-through (shadow 60 ms late, inner dot and bar settle later), and only one of three items moving at a time.
- Compared with before: we chose durations and staggers by feel per episode. These files give numbers (stagger 40-80 ms, cap a group reveal near 0.7 s, enter out / exit in / move in-out). That is a checklist, which we did not have.
- Real gains: the line-mask reveal is calmer and more "designed" than our word-opacity build; anticipation + arc + late shadow makes a card move look like an object, not a slide.
- No difference / caution: nothing here is new technology, it is all plain GSAP. About a third of the advice (overshoot "branded pop", bouncy springs, squash and stretch) is the opposite of the Miki checklist and must be ignored. The pill scene is abstract: it shows craft, not a reel idea. The underline touches the top of the next line.
- Adopt: the timing table as defaults (in `channel/motion-recipes.md` on the next tooling pass), line-mask reveal for text-only screens, exits faster than enters, follow-through on card landings. Our word-by-word build as spoken stays for narrated lines.
- Label: PROMISING. About 74/100.

## Clip 3 (22-33 s): Lottie
What it uses: lottie-web 5.12.2 light build as one local file, a free demo animation from the lottie-web repo (80 frames), its frame driven by a GSAP tween on the main timeline (first loop eased in, then real speed, three loops), inside one card that drifts slowly.
- Compared with before: we draw every moving thing ourselves in HTML/SVG. Lottie plays a ready After Effects animation (character, icon) that we could not draw by hand in reasonable time, and it rendered frame-exact with HyperFrames at the first try; render time for the whole video was 2 min 14 s, no slower than usual.
- Limits: (1) we have no After Effects, so we depend on other people's files, and each file needs its own licence check (LottieFiles files were not tested; the one used ships in an MIT repo with no author named); (2) a cartoon cat is exactly the "drawn character" the Miki checklist forbids: the look is the file's, not ours; (3) only the playhead can be eased, not the drawing; (4) files with expressions need the full build that evaluates code from the JSON: avoid.
- Adopt: keep as an option for one small real-world icon animation inside a card (a loader, a tick, a product's own animated mark), not as a style. Not for characters.
- Label: works technically (STRONG), fit for our reels WEAK to UNCLEAR. About 60/100 for usefulness.

## Overall
- Layout: at most 3 text blocks per frame (header counts as 2: name block + repo line), everything inside x 108-972 and y 269-1248 except the ring edge noted above; soft blur crossfades, no hard cuts. Frame 0 shows "Made with" and the repo line; the name builds in the first 0.8 s.
- Honest verdict: the biggest practical win is GSAP used properly (SplitText, DrawSVG, labels), which costs nothing and changes no pipeline. The motion rules are a useful checklist. Lottie works but does not fit the Miki look. None of this touches topic, hook or build-up, which is where our views are decided.
- Could not do: watch the motion or hear the music; run SkillSpector; test a LottieFiles file or dotLottie; copy Remotion text (licence). `export/check_hf.sh` was not run (no voice, not an episode).
