#!/bin/sh
# usage: build_v6.sh <cues.json> <narration.wav> <ABSOLUTE out.mp4>
#   cues.json = [{n,line,start,end}] (9 lines); narration.wav = the finished narration (NOT re-rendered here), any rate/channels
# does: wav -> 48k mono, forced alignment (per-word times), voice amplitude envelope (100 Hz), page build, foley events, render 24 fps,
#       synthesized music bed at the exact duration (ducked under the voice; NOT the licensed library) + foley mix, -14 LUFS mux, checks
set -e
HERE=$(cd "$(dirname "$0")" && pwd); LIB=/root/lemo-opuscar; export PATH=/opt/ffmpeg7/bin:$PATH
CUES=$(realpath "$1"); WAV=$(realpath "$2"); case "$3" in /*) OUT=$3;; *) echo "out path must be ABSOLUTE"; exit 2;; esac
[ -f "$CUES" ] && [ -f "$WAV" ] || { echo "usage: build_v6.sh <cues.json> <narration.wav> <ABSOLUTE out.mp4>"; exit 2; }
mkdir -p "$HERE/voices" "$HERE/out" "$(dirname "$OUT")"
ffmpeg -y -loglevel error -i "$WAV" -ar 48000 -ac 1 -c:a pcm_s16le "$HERE/voices/narration.wav"
cp "$CUES" "$HERE/voices/cues_in.json"
PY=${ALIGN_PY:-/opt/v311/bin/python}
$PY "$HERE/align.py" "$HERE/voices/cues_in.json" "$HERE/voices/narration.wav"
$PY "$HERE/env.py" "$HERE/voices/narration.wav"
sh "$HERE/assemble.sh"
cd "$LIB"
node core/render/events.mjs "$HERE" --size 1080x1920
node core/render/video.mjs "$HERE" --fps 24 --workers ${WORKERS:-3} --size 1080x1920 --out "$HERE/out/video.mp4"
.venv/bin/python "$HERE/mix.py"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/mix.wav" "$OUT" 24 0
echo "built $OUT"; sh "$HERE/check_v6.sh" "$OUT" "$HERE/voices/cues_in.json"
