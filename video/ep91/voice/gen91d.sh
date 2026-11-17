#!/usr/bin/env bash
cd /home/user/videos-ai
flock /tmp/tts.lock /opt/v311/bin/python audio/build_voice.py --lines video/ep91/voice/lines91d.txt --out video/ep91/voice/w91d.wav --exaggeration 0.78 --line-exaggeration "1:0.84,2:0.84,3:0.84,4:0.84" --line-seeds "1:6401,2:6402,3:6403,4:6404" --gap 0.6 --min-rate 5.4 --retries 3 --pauses "" --watch "" > video/ep91/voice/w91d.log 2>&1
echo done > video/ep91/voice/w91d.done
