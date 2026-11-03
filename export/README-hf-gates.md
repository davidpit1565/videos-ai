# Gates for HyperFrames reels

`export/check.sh` drives the old `render.sh` reels (a `var DUR`/`var CUES` build, `window.__reel.seek`).
HyperFrames reels (`build_v6.py` -> `hf/index.html` + GSAP timeline) need these instead.

## One command

    ./export/check_hf.sh <composition.html> <narration.wav> <cues.json> <reel.mp4> [music.wav [vol]]

Prints PASS / FAIL / SKIP per check and a summary; exit 0 only if everything that ran passed.
SKIP is listed, never counted as a pass. Audio is measured, not heard.

## The checks, one command line each

| Check | Command |
|---|---|
| Frame layout | `node export/safe_check_hf.js <composition.html> [--every 0.2] [--tol 10] [--tiktok] [--shots dir]` |
| Rendered file | `python3 export/qa.py <reel.mp4> --build <composition.html> --hf` |
| Voice + bed | `/opt/v311/bin/python audio/voice_quality.py <narration.wav> <cues.json> --mix <reel.mp4>` (or `--music <bed.wav> --vol 0.14`) |
| Narration | `python3 export/hf_cues.py <cues.json> /tmp/vd.json && python3 audio/voice_doctor.py <narration.wav> --cues /tmp/vd.json --no-watch` |
| Accent | `python3 audio/check_accent.py ...` (needs `transformers` + a model; SKIPped when missing) |

## What changed and why

- `safe_check_hf.js` (new): opens the composition in the pre-installed Chromium (newest under
  `/opt/pw-browsers`, `--no-sandbox`, headless; override with `CHROMIUM_PATH`), seeks
  `window.__timelines.main`, and applies the same safe box (x 65-1015, y 269-1248), 10 px tolerance
  and overlap rule as `safe_check.js`. HyperFrames-specific handling: `data-start/data-duration`
  windows applied by hand (the runtime is not loaded), text clipped by `overflow:hidden` ancestors
  (phone screens), text covered by an opaque element is skipped, `data-decor` honoured, blur/zoom
  transition frames exempt as in `safe_check.js`. gsap and Inter come from jsdelivr via `curl`
  (cached in `$TMPDIR/hf-gate-cache`) so text is measured with the real font. Each finding shows the
  worst time and the first/last sample over tolerance, so a one-frame transient is distinguishable
  from something that sits on screen. Pitfall fixed: `seek()` returns the GSAP timeline, which has
  `.then()`, and Playwright awaits it forever; the calls are wrapped.
- `qa.py`: `--hf` (auto when the build has `data-composition-id`): length from the root's
  `data-duration`, colour-card check skipped (no cards, and the light base reads as a "bright flat
  card"), and a flat first frame fails (mean luma alone cannot detect a blank light frame). An
  unreadable declared length is now a warning instead of a silent "ok".
- `voice_quality.py`: reads the HyperFrames cue format; `--mix` estimates the bed as mix minus the
  best-fit narration (labelled ESTIMATE) because these reels have no separate bed file.
- `hf_cues.py`: cue format adapter for `voice_doctor.py` / `check_accent.py`.

## Known limits

- Overlaps flagged between a word and its own outline echo (`#e1`, `#e2`) are the design, but the
  gate cannot know; mark such elements `data-decor` in the build to silence them on purpose.
- The bed check via `--mix` is an estimate; pass the real bed + volume when you have them.
- `check_accent.py` could not run here (no `transformers`). `voice_doctor.py --deep` needs whisper
  and was not run; only the per-line pass runs.
