#!/usr/bin/env bash
# Render a playable video build to a finished MP4 with narration and (optionally) music.
#   ./render.sh <html> <width> <height> <seconds> <narration.wav> <out.mp4> [music.wav]
set -euo pipefail
HTML="$1"; W="$2"; H="$3"; DUR="$4"; VO="$5"; OUT="$6"; MUS="${7:-}"
# Measured on the first mixes: at 0.34 the bed came back 0.5 dB LOUDER than the
# narration in the gaps, because loudnorm lifts the whole mix afterwards. The bed
# belongs 15-20 dB under the voice, which is this.
MUSIC_VOL="${MUSIC_VOL:-0.06}"
# FRAMES=1 captures frame by frame instead of recording playback: slower, but the
# timeline cannot drift, which matters when narration is cut to authored times.
FRAMES="${FRAMES:-0}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

if [ "$FRAMES" = "1" ]; then
  node "$(dirname "$0")/frames.js" "$(realpath "$HTML")" "$W" "$H" "$DUR" "$TMP" 30
  RAW="$TMP/%05d.png"
  VIN=(-framerate 30 -i "$RAW")
  START=0
else
  node "$(dirname "$0")/record.js" "$(realpath "$HTML")" "$W" "$H" "$DUR" "$TMP"
  RAW="$(ls "$TMP"/*.webm)"
fi

if [ "$FRAMES" = "1" ]; then
  echo "frame capture: no pre-roll to trim"
else
  # the page holds a black frame until playback starts — find where that ends
  START="$(ffmpeg -hide_banner -i "$RAW" -vf blackdetect=d=0.2:pix_th=0.02 -f null - 2>&1 \
    | grep -o 'black_end:[0-9.]*' | head -1 | cut -d: -f2)"
  START="${START:-0}"
  echo "trimming ${START}s of pre-roll"
  VIN=(-ss "$START" -i "$RAW")
fi

VCHAIN="[0:v]fps=30,scale=${W}:${H}:flags=lanczos,setpts=PTS-STARTPTS[v]"
VOCHAIN="[1:a]aresample=48000,highpass=f=85,acompressor=threshold=-18dB:ratio=3:attack=8:release=180[vo]"

if [ -n "$MUS" ]; then
  # music ducks under the voice rather than sitting at a fixed level, so the bed
  # is audible in the gaps and never fights the narration
  ffmpeg -hide_banner -loglevel error -y "${VIN[@]}" -i "$VO" -i "$MUS" \
    -filter_complex "$VCHAIN;$VOCHAIN;\
[2:a]aresample=48000,volume=${MUSIC_VOL}[mus];\
[vo]asplit=2[vo1][key];\
[mus][key]sidechaincompress=threshold=0.05:ratio=9:attack=12:release=420[duck];\
[vo1][duck]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,\
loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,apad[a]" \
    -map "[v]" -map "[a]" -t "$DUR" \
    -c:v libx264 -preset slow -crf 19 -profile:v high -pix_fmt yuv420p -movflags +faststart \
    -c:a aac -b:a 192k -ar 48000 -ac 2 "$OUT"
else
  ffmpeg -hide_banner -loglevel error -y "${VIN[@]}" -i "$VO" \
    -filter_complex "$VCHAIN;$VOCHAIN;[vo]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,apad[a]" \
    -map "[v]" -map "[a]" -t "$DUR" \
    -c:v libx264 -preset slow -crf 19 -profile:v high -pix_fmt yuv420p -movflags +faststart \
    -c:a aac -b:a 192k -ar 48000 -ac 2 "$OUT"
fi

ffprobe -hide_banner -v error -show_entries format=duration,size -of default=nw=1 "$OUT"
