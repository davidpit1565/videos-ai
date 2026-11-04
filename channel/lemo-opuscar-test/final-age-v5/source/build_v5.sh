#!/bin/sh
# usage: build_v5.sh <cues.json> <narration.wav> [out.mp4]
#   cues.json = [{n,line,start,end}] (9 lines, same shape as myvoice/narration-cues.json); narration.wav = the narration, any rate/channels
# does: wav -> 48k mono, forced alignment (per-word times; char-count fallback is reported), page build, foley events (re-timed from cues), render 24 fps,
#       synthesized music bed regenerated at the exact duration (ducked ~17 dB under the voice; NOT the licensed library) + foley mix, -14 LUFS mux
set -e
HERE=$(cd "$(dirname "$0")" && pwd); LIB=/root/lemo-opuscar; export PATH=/opt/ffmpeg7/bin:$PATH
CUES=$1; WAV=$2; OUT=${3:-$HERE/chatgpt-age-v5.mp4}
[ -f "$CUES" ] && [ -f "$WAV" ] || { echo "usage: build_v5.sh <cues.json> <narration.wav> [out.mp4]"; exit 2; }
mkdir -p "$HERE/voices" "$HERE/out"
ffmpeg -y -loglevel error -i "$WAV" -ar 48000 -ac 1 -c:a pcm_s16le "$HERE/voices/narration.wav"
cp "$CUES" "$HERE/voices/cues_in.json"
${ALIGN_PY:-/opt/v311/bin/python} "$HERE/align.py" "$HERE/voices/cues_in.json" "$HERE/voices/narration.wav"
sh "$HERE/assemble.sh"
cd "$LIB"
node core/render/events.mjs "$HERE" --size 1080x1920
node core/render/video.mjs "$HERE" --fps 24 --workers ${WORKERS:-3} --size 1080x1920 --out "$HERE/out/video.mp4"
.venv/bin/python "$HERE/mix.py"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/mix.wav" "$OUT" 24 0
echo "built $OUT"; sh "$HERE/check_v5.sh" "$OUT" "$HERE/voices/cues_in.json"
