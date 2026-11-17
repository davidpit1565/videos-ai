# video/demo-skills: internal demo, NOT an episode, never to be published (16.11.2026)
One 33 s video, three clips, no voice. Report: `channel/demo-skills-report-2026-11-16.md`.

| File | What | Source | Licence / note |
|---|---|---|---|
| `hf/lib/lottie_light-5.12.2.min.js` | lottie-web 5.12.2, LIGHT build (SVG renderer, no expression engine, contains no `eval(`) | https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie_light.min.js, fetched with curl 16.11.2026, sha256 23cd2c01be3d4da8bb664645d03afaff40879c62dc5f8dfe075ab3aa35c108f3 | MIT (airbnb/lottie-web). No npm install. |
| `hf/assets/lottie/gatin.json` | "gatin" (a sitting cat), 80 frames at 25 fps, 15 shape layers, no images, no expressions, no URLs inside | https://cdn.jsdelivr.net/gh/airbnb/lottie-web@v5.12.2/demo/gatin/data.json | It ships in the MIT-licensed airbnb/lottie-web repo as a demo. The repo names no separate author or licence for this artwork: fine for an internal demo, CHECK before any public use. |
| `hf/assets/lottie/gatin.js` | the same JSON wrapped as `window.LOTTIE_GATIN=...` so it loads without a fetch | made here | |
| GSAP 3.15.0 core, SplitText, DrawSVGPlugin, CustomEase, MotionPathPlugin | loaded at render time from cdn.jsdelivr.net/npm/gsap@3.15.0 (the same pinned package every episode build loads) | | GSAP standard licence, free incl. commercial use |
| `hf/assets/fonts/`, `hf/assets/bg.jpg`, `hf/assets/github-mark.svg` | copied from `video/ep102/hf/assets/` | see `video/ep102/hf/assets/logos/SOURCES.md` | GitHub mark usage terms were not opened |
| Music | `audio/music-library/minimal--ambient-soft--avelinemusic.mp3` via `audio/pick_real_track.py 33 ... --mood ambient` (there is no "calm" mood), mixed at -9 dB with fades | real library (Pixabay) | restored from git for the run, removed again |

Render: `cd video/ep89c && HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 ./node_modules/.bin/hyperframes render ../demo-skills/hf -o ../demo-skills/out/pic-v1.mp4 --format mp4 --quiet`, then ffmpeg adds the bed (`out/demo-v1.mp4`) and makes the 720 px crf 27 review copy (`out/demo-v1-review.mp4`).
The Lottie is NOT registered in `window.__hfLottie`; its frame is driven by a GSAP tween (`goToAndStop`) on the main timeline, so there is one clock.
