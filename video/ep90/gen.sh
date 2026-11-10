#!/usr/bin/env bash
# gen.sh <tag> <seedbase> <exag>
cd /home/user/videos-ai
T=$1; B=$2; X=$3
S=""; for i in 1 2 3 4; do S="$S$i:$((B+i)),"; done; S=${S%,}
/opt/v311/bin/python audio/build_voice.py --lines video/ep90/lines.txt --out video/ep90/voice/$T.wav --exaggeration $X --line-exaggeration "1:$X,2:$X,3:0.7,4:0.74" --line-seeds "$S" --gap 0.3 --closes 4 --pauses "" --retries 4 --watch three > video/ep90/voice/$T.log 2>&1
echo done > video/ep90/voice/$T.done
