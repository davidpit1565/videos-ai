#!/bin/sh
# usage: export/phone_preview.sh <video.mp4> [outdir]
# Makes what David needs to HEAR a video on his phone in the chat (he cannot play sound in the chat; downloading is a chore):
#   <name>-phone.mp4   720x1280, small, sound on (inline preview, fast to open)
#   <name>-sound.m4a   audio only, AAC 128k (a plain audio file the phone's own player can play)
#   <name>-sound.mp3   same audio as mp3 (fallback if m4a will not play)
# Needs ffmpeg (any version). Never touches the source file.
set -e
IN=$1; [ -f "$IN" ] || { echo "usage: phone_preview.sh <video.mp4> [outdir]"; exit 2; }
OUT=${2:-$(dirname "$IN")}; mkdir -p "$OUT"; B=$(basename "$IN" .mp4)
ffmpeg -y -loglevel error -i "$IN" -vf scale=720:1280 -c:v libx264 -preset medium -crf 27 -pix_fmt yuv420p -c:a aac -b:a 128k -ar 48000 -movflags +faststart "$OUT/$B-phone.mp4"
ffmpeg -y -loglevel error -i "$IN" -vn -c:a aac -b:a 128k -ar 48000 "$OUT/$B-sound.m4a"
ffmpeg -y -loglevel error -i "$IN" -vn -c:a libmp3lame -b:a 160k -ar 44100 "$OUT/$B-sound.mp3"
ls -la "$OUT/$B-phone.mp4" "$OUT/$B-sound.m4a" "$OUT/$B-sound.mp3"
