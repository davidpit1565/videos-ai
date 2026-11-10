#!/usr/bin/env bash
# motion.sh <mp4> : scene-change frames per second at three thresholds (270 px wide), as David/coordinator measured
F=$1; D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $F)
for TH in 0.01 0.03 0.08; do
  N=$(ffmpeg -nostats -i $F -vf "scale=270:-2,select='gt(scene,$TH)',showinfo" -an -f null - 2>&1 | grep -c pts_time)
  python3 -c "print('scene>$TH: $N frames over ${D}s = ', round($N/$D,2), '/s')"
done
