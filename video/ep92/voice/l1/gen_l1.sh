#!/usr/bin/env bash
# re-roll ONLY line 1, ep89 recipe, sequential (one TTS at a time)
cd /home/user/videos-ai
for s in 5301 5302 5303 5304 5305 5306; do
  /opt/v311/bin/python audio/build_voice.py --lines video/ep92/voice/l1/line1.txt --out video/ep92/voice/l1/t$s.wav --exaggeration 0.9 --line-exaggeration "1:0.9" --line-seeds "1:$s" --gap 0.18 --min-rate 5.4 --retries 5 --pauses "" --watch "" > video/ep92/voice/l1/t$s.log 2>&1
  echo $s >> video/ep92/voice/l1/done.txt
done
