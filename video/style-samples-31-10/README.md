# Style samples, 31.10.2026 (no voice, 12-13 s, 1080x1920)

Four samples built with HyperFrames v0.8.225 (HTML + GSAP to MP4) to compare looks. Sources only; the MP4s are not stored here. Content is episode 80/81 material: user-typed messages and settings text are drawn, no ChatGPT answer is drawn. Sample 4 uses David's real A recording (not stored here).

Build one: `npm i hyperframes`, `hyperframes init <name> --example blank --resolution portrait`, copy the `index.html` and `assets/chatgpt.svg` (logo from `channel/assets/ep62-chatgpt-logo.svg`) into it, then `HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 npx hyperframes check` and `npx hyperframes render -o out.mp4`.

Sample 4: the video layer rendered the page background wrong, so the graphics render alone (cream page, a black placeholder window) and the recording is cropped to 884x714, rounded with a mask and overlaid with ffmpeg at (98,508). The recording clip is `ffmpeg -ss 24 -t 14 -i <A recording> -an -vf fps=30,scale=540:-2`.

Findings: render takes about 20-60 s per sample; `hyperframes check` caught a text overlap, a contrast failure and an empty first frame before rendering. Telemetry is on by default: disable it with the env vars above. Not installed as a repo dependency or skill; no security scan of the package was done beyond reading its README.
