#!/bin/sh
set -e
HERE=$(cd "$(dirname "$0")" && pwd); LIB=${LIB:-/root/lemo-opuscar}; export LIB PATH=/opt/ffmpeg7/bin:$PATH
cd "$LIB"
.venv/bin/python core/tts/tts.py "$HERE/lines.json" "$HERE/voices"      # voice (Kokoro af_heart)
.venv/bin/python core/tts/asr_check.py "$HERE/lines.json" "$HERE/voices"
node core/render/events.mjs "$HERE" --size 1080x1920
node core/render/video.mjs "$HERE" --fps 24 --workers 3 --size 1080x1920 --out "$HERE/out/video.mp4"
.venv/bin/python "$HERE/mix.py"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/mix.wav" "$HERE/chatgpt-memory.mp4" 24 0
