#!/usr/bin/env bash
# gen.sh <tag> <seedbase> <exag>
cd /home/user/videos-ai
T=$1; B=$2; X=$3
S=""; for i in 1 2 3 4 5 6 7; do S="$S$i:$((B+i)),"; done; S=${S%,}
/opt/v311/bin/python audio/build_voice.py --lines video/ep89b/lines.txt --out video/ep89b/voice/$T.wav --exaggeration $X --line-exaggeration "1:0.9,2:$X,3:$X,4:0.82,5:$X,6:$X,7:0.82" --line-seeds "$S" --gap 0.18 --min-rate 5.4 --retries 5 --pauses "" --watch two,five > video/ep89b/voice/$T.log 2>&1
echo done > video/ep89b/voice/$T.done
