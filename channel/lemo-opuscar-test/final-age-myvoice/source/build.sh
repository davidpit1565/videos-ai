#!/bin/sh
set -e
HERE=$(cd "$(dirname "$0")" && pwd); LIB=/root/lemo-opuscar; export PATH=/opt/ffmpeg7/bin:$PATH
cat "$HERE/head.js" "$HERE/scenes.js" > "$HERE/main.js"
OUT=${OUT:-$HERE/chatgpt-age-myvoice.mp4}
mkdir -p "$HERE/out"; cd "$LIB"
node core/render/events.mjs "$HERE" --size 1080x1920
node core/render/video.mjs "$HERE" --fps 24 --workers 3 --size 1080x1920 --out "$HERE/out/video.mp4"
.venv/bin/python "$HERE/mix.py"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/mix.wav" "$OUT" 24 0
