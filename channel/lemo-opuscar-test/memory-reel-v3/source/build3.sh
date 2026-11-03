#!/bin/sh
# usage: sh build3.sh [proof.json]   (optional: a new proof config; its "image" file is copied next to main.js first)
set -e
HERE=$(cd "$(dirname "$0")" && pwd); LIB=/root/lemo-opuscar; export PATH=/opt/ffmpeg7/bin:$PATH
OUT=${OUT:-$HERE/chatgpt-memory-v3.mp4}
if [ -n "$1" ]; then
  P=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
  IMG=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['image'])" "$P")
  case "$IMG" in /*) SRC="$IMG";; *) SRC="$(dirname "$P")/$IMG";; esac
  B=$(basename "$SRC"); [ "$SRC" = "$HERE/$B" ] || cp "$SRC" "$HERE/$B"
  python3 - "$P" "$HERE/proof.json" "$B" <<'PY'
import json,sys
d=json.load(open(sys.argv[1])); d['image']=sys.argv[3]; json.dump(d,open(sys.argv[2],'w'),indent=1,ensure_ascii=False)
PY
fi
mkdir -p "$HERE/out"; cd "$LIB"
node core/render/events.mjs "$HERE" --size 1080x1920
node core/render/video.mjs "$HERE" --fps 24 --workers 3 --size 1080x1920 --out "$HERE/out/video.mp4"
.venv/bin/python "$HERE/mix.py"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/mix.wav" "$OUT" 24 0
