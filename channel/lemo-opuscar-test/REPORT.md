# lemo-opuscar plugin: cloud test report (3.11.2026)

Plugin: `lemo-opuscar@lemolab`, version `bebbbe1aa92a`. Repo: https://github.com/lemomo-ai/lemo-opuscar. Tested in this cloud container (4 cores, 15 GB, no GPU).

## Verdict (short)
- **Works in the cloud.** One real 24.6 s vertical film was produced end to end (voice, music, render, mux).
- **Not a drop-in for the channel's Reels.** Usable as an intro/explainer clip or an animation-language prototype. Reasons below.
- The Reel itself was NOT built in the regular pipeline in this session (see "Not done").

## Install (measured by me)
| Step | Result |
|---|---|
| `claude plugin marketplace add` + `install` | worked after the permission rule in commit `1763dbb` (first two attempts were blocked by the permission classifier) |
| `setup.sh` read before running | clones the library into `~/lemo-opuscar`, `npm install`, headless Chromium, a Python venv, and (voice tier) a 354 MB Kokoro model via `tools/fetch.sh`. No telemetry code was seen in this script (I did not audit the rest of the library) |
| `setup.sh deps voice music` | 2 min 14 s |
| ffmpeg | system is 6.1 (plugin wants 7+). Static 7.0.2 from johnvansickle.com in `/opt/ffmpeg7/bin`, used by PATH prefix only; system ffmpeg untouched |
| Node / Python | Node 22, Python 3.13: fine |

## The demo film (made by a subagent, then verified by me)
File: `channel/lemo-opuscar-test/effort-slider.mp4` (3,408,166 bytes). Contact sheet: `final_sheet.jpg`.
- Style: Dark Tech Keynote. Content: only the facts verified on the official Claude Code docs (effort default on Opus 5.5 / Sonnet 5.5 / Haiku 5.5 is medium, `/effort`, levels, max is session only).
- **I verified myself with ffprobe:** h264 yuv420p 1080x1920, 24 fps, 24.58 s; aac 48 kHz stereo; mean -16.5 dB, max -1.2 dB. I also looked at 8 frames (0.5, 4, 8, 11, 14, 18.6, 21, 24.3 s): no overflow, no blank frames, slider/chips/command bar/panel/red "can overthink" chip/"this session only" card all legible.
- **Not heard by anyone.** The audio was measured, not listened to. The agent's own check: Whisper matched 7/7 lines after the hook "Claude's on medium" was rewritten to "Claude is on medium" (it was heard as "Clods on Medium"); "Sonnet" is heard as "son at" and the check was overridden, so that line is unverified by ear.
- Not run: the plugin's full DIRECTOR.md self-check; this repo's `check.sh`, `voice_doctor`, `voice_quality`.

## Time and tokens
| Stage | Time (agent, `date`) |
|---|---|
| demo-source fetch | 2 s |
| fonts download | 1 s |
| look checks (stills) | about 3 s per batch |
| Kokoro voice, 7 lines | 12 s |
| Whisper check | 15 s first run, about 5 s reruns |
| music + foley synthesis | 3 s |
| render, 590 frames, 4 workers, software GL | 28 s |
| mux + loudnorm | 13 s |
| total, first command to final file | 278 s |
Tokens: the agent estimated 60-80k; **the harness meter for that subagent says 160,128 tokens, 29 tool calls, 307 s.** Use the meter. This is for one 25 s film of one style; the plugin's own README says a full film is 30-60 minutes of agent time and a significant amount of tokens.

## Problems found
1. **Vertical is a hack.** `--size 1080x1920` works on the render tools, but the style's `engine.js` hard-codes 1920x1080; the agent copied it and patched `W`/`H`. Safe area is by hand.
2. **No voice cloning.** Stock Kokoro voice (`af_kore`). The channel's Chatterbox clone of David's voice cannot be used inside the plugin pipeline.
3. **Look.** Near-black base with a lime accent; the channel's fixed identity is the light base (episode 81 design). A light variant would need a custom theme.
4. **Music is synthesized** (numpy FM marimba + pad), not the licensed library the repo requires. The VCSL sample library was not fetched.
5. **No real logos or screenshots.** All UI is drawn. CLAUDE.md requires the real mark/screenshot for every named product; the slider UI here is "re-created", not recorded from Claude Code.
6. **Missing/odd bits:** the demo's `fonts/` has only licence files (fonts had to be downloaded from google/fonts raw); rendering uses SwiftShader software WebGL (fine for 2D, slow for 3D styles); `sfx.add` needs stereo buffers; the on-screen caption "Claude is on medium." generalises (only true for models that default to medium).
7. **Setup guide** for `/e/N` is not produced by the plugin.

## Fit for the channel's rules
| Rule | Result |
|---|---|
| David's cloned voice | no |
| 9:16 | yes, by patch |
| light/lime v4 look | no (dark) |
| real logo/screenshot | no |
| licensed music | no |
| `/e/N` setup guide | separate work |
| 3-word hook | the film opens on the proof; hook not designed per hooks-guide |
Honest conclusion: good for an intro/explainer for the site, or to prototype motion; the channel Reel should go through the repo pipeline.

## Not done (and why)
- The episode 83 Reel through `export/produce.sh`: needs (a) rebuilding `/opt/v311` (torch, Chatterbox, faster-whisper; several GB, one voice render at a time), (b) a real `/effort` screen recording or screenshot from David (otherwise the UI must be labelled "re-created"), (c) a decision on the closing line, which must name episode 84 (CLAUDE.md), and (d) the known open item that `produce.sh`'s design-variety check still fails on a repeated colour and has not been updated for the fixed series identity. Script and setup guide are ready in `channel/episode-83-script.md`.
- Nothing published, nothing merged, no secrets or PIN touched.
