#!/usr/bin/env bash
cd /home/user/videos-ai
/opt/v311/bin/python audio/build_voice.py --lines video/ep91/voice/lines91b.txt --out video/ep91/voice/w91b.wav --exaggeration 0.78 --line-exaggeration "1:0.90,3:0.82,4:0.82" --line-seeds "1:6201,2:6202,3:6203,4:6204" --gap 0.18 --min-rate 5.4 --retries 5 --pauses "" --watch "" > video/ep91/voice/w91b.log 2>&1
echo done > video/ep91/voice/w91b.done
