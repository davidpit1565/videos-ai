#!/usr/bin/env bash
# sheet.sh <mp4> <out.png> <start> <dur> <fps> <cols> <rows> [width]
ffmpeg -y -v error -ss $3 -t $4 -i $1 -vf "fps=$5,scale=${8:-240}:-1,tile=$6x$7:padding=4:color=0x888888" -frames:v 1 $2
