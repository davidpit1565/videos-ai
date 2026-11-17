#!/usr/bin/env bash
# ep89 recipe (video/ep89b/voice/README.md): 0.78 normal, hook 0.90, last lines 0.82, gap 0.18, min-rate 5.4, then atempo 1.12
cd /home/user/videos-ai
/opt/v311/bin/python audio/build_voice.py --lines video/ep90/voice/lines5.txt --out video/ep90/voice/w6.wav --exaggeration 0.78 --line-exaggeration "1:0.90,4:0.82,6:0.82,7:0.82" --line-seeds "1:6101,2:6102,3:6103,4:6104,5:6105,6:6106,7:6107" --gap 0.18 --min-rate 5.4 --retries 5 --pauses "5,6" --watch "" > video/ep90/voice/w6.log 2>&1
echo done > video/ep90/voice/w6.done
