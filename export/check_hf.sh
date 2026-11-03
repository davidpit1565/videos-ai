#!/usr/bin/env bash
# One command for the pipeline gates on a HyperFrames reel (export/check.sh is for the old
# export/render.sh reels and cannot drive these). Prints PASS / FAIL / SKIP per check.
#
#   ./export/check_hf.sh <composition.html> <narration.wav> <cues.json> <reel.mp4> [music.wav [vol]]
#
#   composition.html  the HyperFrames composition (data-composition-id root, window.__timelines.main)
#   narration.wav     the voice-only track
#   cues.json         build_v6.py's cues ({"lines":[{n,text,start,end}]}) or the old list format
#   reel.mp4          the finished render (voice + music already mixed by the build)
#   music.wav [vol]   optional: the real bed file + the volume it was mixed at. Without it the bed
#                     is ESTIMATED from the mp4 (voice_quality.py --mix) and the report says so.
#
# Env: PY311 (default /opt/v311/bin/python, has librosa), CHROMIUM_PATH (default: newest under
#      /opt/pw-browsers), EVERY (safe-area sample step, default 0.2).
# Exit 0 only if every check that ran passed. SKIP is not PASS: it is listed in the summary.
# No threshold is relaxed here; each tool keeps its own.
set -uo pipefail
cd "$(dirname "$0")/.."
HTML="${1:-}"; VO="${2:-}"; CUES="${3:-}"; MP4="${4:-}"; MUS="${5:-}"; VOL="${6:-0.14}"
if [ -z "$MP4" ]; then
  echo "usage: ./export/check_hf.sh <composition.html> <narration.wav> <cues.json> <reel.mp4> [music.wav [vol]]" >&2
  exit 2
fi
for f in "$HTML" "$VO" "$CUES" "$MP4"; do [ -f "$f" ] || { echo "missing file: $f" >&2; exit 2; }; done
PY311="${PY311:-/opt/v311/bin/python}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
declare -a RESULTS=()
fail=0; skipped=0

run() {   # run <name> <command...> : capture output, print PASS/FAIL and the output indented
  local name="$1"; shift
  "$@" >"$TMP/out.txt" 2>&1; local rc=$?
  if [ $rc -eq 0 ]; then RESULTS+=("PASS  $name"); echo "=== PASS  $name"
  else RESULTS+=("FAIL  $name (exit $rc)"); echo "=== FAIL  $name (exit $rc)"; fail=1; fi
  grep -v "Warning\|warn(" "$TMP/out.txt" | sed 's/^/    /'
  echo
}

run "frame layout (safe_check_hf.js)" node export/safe_check_hf.js "$HTML" --every "${EVERY:-0.2}"

run "rendered file (qa.py --hf)" python3 export/qa.py "$MP4" --build "$HTML" --hf

if [ -n "$MUS" ]; then
  run "voice + music quality (voice_quality.py)" "$PY311" audio/voice_quality.py "$VO" "$CUES" --music "$MUS" --vol "$VOL"
else
  run "voice + music quality (voice_quality.py, bed ESTIMATED from the mp4)" "$PY311" audio/voice_quality.py "$VO" "$CUES" --mix "$MP4"
fi

python3 export/hf_cues.py "$CUES" "$TMP/vd-cues.json" >/dev/null
run "narration pacing/level/sibilance (voice_doctor.py, per line, no whisper pass)" \
  python3 audio/voice_doctor.py "$VO" --cues "$TMP/vd-cues.json" --no-watch

if python3 -c "import transformers" 2>/dev/null; then
  run "accent drift (check_accent.py)" python3 audio/check_accent.py "$VO" --cues "$TMP/vd-cues.json"
else
  RESULTS+=("SKIP  accent drift (check_accent.py needs the python 'transformers' package and a model; not installed here)")
  echo "=== SKIP  accent drift (needs transformers + model, not installed)"; echo; skipped=$((skipped+1))
fi

echo "================ SUMMARY"
printf '  %s\n' "${RESULTS[@]}"
echo
if [ "$fail" = 0 ]; then
  echo "ALL CHECKS THAT RAN PASSED ($skipped skipped)  -  audio was measured, not heard; watch the file twice before sending"
else
  echo "SOMETHING FAILED - do not send this file"
fi
exit $fail
