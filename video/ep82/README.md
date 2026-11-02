# Episode 82 build sources (2.11.2026)

HyperFrames reel assembled from nine scene fragments (`scenes/scene-N.html`, each a scoped style, markup and `window.buildScene_N(tl,T0,DUR)`), a shell (`shell.html`), and the cloned-voice lines.
Run order used: `build_voice.py` takes (whole script, per-line seeds, higher exaggeration on lines 1, 3, 6, 7) -> `pick.py --apply` (per-line pick by `voice_quality` numbers, then `tighten.py`) -> `build82.py --render draft` -> `voice_doctor.py --repair` on the narration -> `mix.py` (three beds) -> `check_hf.sh`.
Logos: `assets/claude.svg` (Wikimedia Commons "Claude AI symbol.svg", recoloured #D97757) and `assets/anthropic.svg` (Wikimedia Commons "Anthropic logo.svg").
Paths inside the scripts point at the scratchpad of the session that built it; adjust `H` before reuse.
