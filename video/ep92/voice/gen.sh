#!/usr/bin/env bash
# ONE TTS render, same pipeline as video/ep90/voice/gen5.sh
cd /home/user/videos-ai
/opt/v311/bin/python audio/build_voice.py --lines video/ep92/voice/lines.txt --out video/ep92/voice/v1.wav --exaggeration 0.74 --line-exaggeration "1:0.80,4:0.78,5:0.76" --line-seeds "1:9201,2:9202,3:9203,4:9204,5:9205" --gap 0.18 --min-rate 5.2 --retries 5 --pauses "4" --watch "" > video/ep92/voice/v1.log 2>&1
echo done > video/ep92/voice/v1.done
