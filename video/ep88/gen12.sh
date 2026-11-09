#!/usr/bin/env bash
# usage: gen12.sh <tag> <seedbase>
cd /home/user/videos-ai
T=$1; B=$2
S=""; for i in 1 2 3 4 5 6 7 8 9 10 11 12; do S="$S$i:$((B+i)),"; done; S=${S%,}
/opt/v311/bin/python audio/build_voice.py --lines video/ep88/lines12.txt --out video/ep88/voice5/$T.wav --exaggeration 0.78 --line-exaggeration "1:0.84,2:0.76,3:0.76,4:0.72,5:0.8,6:0.76,7:0.8,8:0.7,9:0.7,10:0.66,11:0.74,12:0.7" --line-seeds "$S" --gap 0.3 --closes 6,12 --pauses "" > video/ep88/voice5/$T.log 2>&1
