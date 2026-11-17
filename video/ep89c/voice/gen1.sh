#!/usr/bin/env bash
cd /home/user/videos-ai
for spec in "m1 0.60 3101" "m2 0.60 3102" "m3 0.65 3103" "m4 0.55 3104"; do
  set -- $spec
  /opt/v311/bin/python audio/build_voice.py --lines video/ep89c/voice/line1.txt --out video/ep89c/voice/$1.wav --exaggeration $2 --line-exaggeration "1:$2" --line-seeds "1:$3" --gap 0.18 --retries 3 --pauses "" > video/ep89c/voice/$1.log 2>&1
  echo done > video/ep89c/voice/$1.done
done
