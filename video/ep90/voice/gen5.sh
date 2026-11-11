#!/usr/bin/env bash
# one TTS render, same pipeline as video/ep89b/gen.sh
cd /home/user/videos-ai
/opt/v311/bin/python audio/build_voice.py --lines video/ep90/voice/lines5.txt --out video/ep90/voice/v5.wav --exaggeration 0.74 --line-exaggeration "1:0.80,4:0.78,6:0.78,7:0.78" --line-seeds "1:4101,2:4102,3:4103,4:4104,5:4105,6:4106,7:4107" --gap 0.18 --min-rate 5.2 --retries 5 --pauses "5,6" --watch "" > video/ep90/voice/v5.log 2>&1
echo done > video/ep90/voice/v5.done
