# Making a new hook version (episode 106, reusable for other approved episodes)

Only the opening line (and frame 0 words) changes; the body voice is cached.

    cd /home/user/videos-ai/video/ep106
    ./make_variant.sh "<new hook line>" <fresh-tag> ["LINE1|LINE2|LINE3"] [accent_line_index]

Example: `./make_variant.sh "Claude built my app in thirty minutes." V6 "CLAUDE BUILT|MY APP|IN 30 MIN" 2`

- `<fresh-tag>`: a new name (V6, V7 ...). The script refuses a tag whose `out/ep106-<tag>.mp4` already exists.
- frame 0 words: up to 3 lines, big text, no box. If omitted, the hook is split into up to 3 lines automatically (check the first frame).
- Env: `SEEDS="11 22 33"` (hook takes), `EXAH=0.82` (hook exaggeration; lower to 0.70 if the accent check flags it), `TRACKFILE` (library bed file), `BEDDB` (default -8.5), `ACCENT_SKIP`.

What it does, in order: script_lint on the hook; 3 hook takes (one TTS at a time under `flock /tmp/tts.lock`); Whisper text check + accent score picks the take; stitches it with the cached body takes (`voice/body-picks.json`, `voice/pl/B*-*.wav`), re-times everything; Whisper word times; builds `hf-<tag>/index.html` (`build106.py`); renders; cuts the same real-library bed to the exact new length; mixes; runs `export/check_hf.sh` (output `out/gate-<tag>.txt`).

Cached (never re-run): the 10 body voice lines, the GitHub page screenshot, logos, fonts, the scene code. Re-run per version: 1 hook line of TTS, 1 Whisper pass, 1 render, mix, gate.

Runtime per version (measured here: 4-core CPU box, no GPU): hook TTS about 1 min per take once the model is warm (x3 seeds; the very first TTS after a container start spent about 8 minutes loading the model from disk); Whisper pick about 20 s; accent re-pick of flagged body lines about 1-2 min (cached takes only); words 20 s; render about 1.5 min; mix 10 s; gate about 1.5 min. A version whose hook takes are cached finished in about 3 min (V1 to V2 in the real run); a new hook is about 7-9 min end to end. Versions run one after another (one TTS and one render at a time).

Notes learned in the real run: (1) the accent classifier scores the same body take 0.04 under one hook and 0.98 under another, so `voice/fixaccent.py` re-chooses flagged body takes inside each new stitch (writes `voice/picks-<tag>.json`; the shared `body-picks.json` is not touched); (2) the voice reads "free Claude tool/add-on" as "cloud/clock": put "Claude" at the end of a phrase ("built by Claude", "in Claude"); (3) if no hook take matches its text: `SEEDS="44 55 66" EXAH=0.70 ./make_variant.sh ...`; (4) `out/gate-<tag>.txt` must end with ALL CHECKS THAT RAN PASSED.

To reuse for another approved episode: copy the folder, replace `body.txt` and `build106.py` scenes, re-render the body voice once, and set `voice/body-picks.json`; the same `make_variant.sh` then works unchanged.
