#!/usr/bin/env bash
# Render a playable video build to a finished MP4 with narration.
#   ./render.sh <html> <width> <height> <duration-seconds> <narration.wav> <out.mp4>
set -euo pipefail
HTML="$1"; W="$2"; H="$3"; DUR="$4"; VO="$5"; OUT="$6"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

node /tmp/record.js "$(realpath "$HTML")" "$W" "$H" "$DUR" "$TMP"
RAW="$(ls "$TMP"/*.webm)"

# the page holds a black frame until playback starts — find where it ends
START="$(ffmpeg -hide_banner -i "$RAW" -vf blackdetect=d=0.2:pix_th=0.02 -f null - 2>&1 \
  | grep -o 'black_end:[0-9.]*' | head -1 | cut -d: -f2)"
START="${START:-0}"
echo "trimming ${START}s of pre-roll"

ffmpeg -hide_banner -loglevel error -y -ss "$START" -i "$RAW" -i "$VO" \
  -filter_complex "[0:v]fps=30,scale=${W}:${H}:flags=lanczos,setpts=PTS-STARTPTS[v];\
[1:a]aresample=48000,highpass=f=90,acompressor=threshold=-18dB:ratio=3:attack=8:release=180,\
loudnorm=I=-14:TP=-1.5:LRA=11,apad[a]" \
  -map "[v]" -map "[a]" -t "$DUR" \
  -c:v libx264 -preset slow -crf 19 -profile:v high -pix_fmt yuv420p -movflags +faststart \
  -c:a aac -b:a 192k "$OUT"

ffprobe -hide_banner -v error -show_entries format=duration,size -of default=nw=1 "$OUT"
