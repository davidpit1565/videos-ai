#!/usr/bin/env bash
# usage: gen.sh <tag> <seedbase>
cd /home/user/videos-ai
T=$1; B=$2
S=""; for i in 1 2 3 4 5 6 7 8; do S="$S$i:$((B+i)),"; done; S=${S%,}
/opt/v311/bin/python audio/build_voice.py --lines video/ep88/lines.txt --out video/ep88/voice/$T.wav --exaggeration 0.76 --line-exaggeration "1:0.82,2:0.74,3:0.72,4:0.74,5:0.7,6:0.74,7:0.7,8:0.76" --line-seeds "$S" --gap 0.3 --closes 8 --pauses "" > video/ep88/voice/$T.log 2>&1
echo done $T >> video/ep88/voice/done.txt
