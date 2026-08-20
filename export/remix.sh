#!/usr/bin/env bash
# Rebuild only the audio of an existing render, keeping the video stream byte for byte.
# Frame capture costs twelve minutes; a mix change costs twenty seconds, and there is no
# reason to pay the former for the latter.
#   ./export/remix.sh <in.mp4> <vo.wav> <music.wav> <out.mp4> [music_volume]
set -euo pipefail
IN="$1"; VO="$2"; MUS="$3"; OUT="$4"; VOL="${5:-0.06}"
ffmpeg -hide_banner -loglevel error -y -i "$IN" -i "$VO" -i "$MUS" \
  -filter_complex "[1:a]aresample=48000,highpass=f=85,\
acompressor=threshold=-18dB:ratio=3:attack=8:release=180[vo];\
[2:a]aresample=48000,volume=${VOL}[mus];\
[vo]asplit=2[vo1][key];\
[mus][key]sidechaincompress=threshold=0.05:ratio=9:attack=12:release=420[duck];\
[vo1][duck]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,\
loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,apad[a]" \
  -map 0:v -map "[a]" -shortest \
  -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart "$OUT"
ffprobe -hide_banner -v error -show_entries format=duration,size -of default=nw=1 "$OUT"
