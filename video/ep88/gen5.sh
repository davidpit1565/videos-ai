#!/usr/bin/env bash
cd /home/user/videos-ai
T=$1; B=$2
S=""; for i in 1 2 3 4 5 6; do S="$S$i:$((B+i)),"; done; S=${S%,}
/opt/v311/bin/python audio/build_voice.py --lines video/ep88/lines5.txt --out video/ep88/voice/$T.wav --exaggeration 0.76 --line-exaggeration "1:0.84,2:0.84,3:0.74,4:0.7,5:0.72,6:0.76" --line-seeds "$S" --gap 0.3 --closes 6 --pauses "" > video/ep88/voice/$T.log 2>&1
echo done $T >> video/ep88/voice/done5.txt
