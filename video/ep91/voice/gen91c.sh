#!/usr/bin/env bash
cd /home/user/videos-ai
flock /tmp/tts.lock /opt/v311/bin/python audio/build_voice.py --lines video/ep91/voice/lines91c.txt --out video/ep91/voice/w91c.wav --exaggeration 0.78 --line-exaggeration "1:0.84,2:0.80,3:0.82" --line-seeds "1:6301,2:6302,3:6303" --gap 0.18 --min-rate 5.4 --retries 5 --pauses "" --watch "" > video/ep91/voice/w91c.log 2>&1
echo done > video/ep91/voice/w91c.done
