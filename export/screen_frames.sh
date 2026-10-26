#!/usr/bin/env bash
# Turns a real iPhone screen recording into the 10 fps, 720-wide frame set a dialogue episode's build uses
# (video/gen/ep75/gen.py reads channel/assets/ep<N>-screen/f_NNN.jpg; frame k is at (k-1)/10 seconds).
#   ./export/screen_frames.sh <recording.mp4> <episode>
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="channel/assets/ep$2-screen"; mkdir -p "$OUT"
ffmpeg -loglevel error -y -i "$1" -vf "fps=10,scale=720:-1" -q:v 4 -start_number 1 "$OUT/f_%03d.jpg"
echo "$(ls "$OUT" | wc -l) frames in $OUT; contact sheet: ffmpeg -i $1 -vf fps=1/2,scale=240:-1 sheet_%02d.png"
