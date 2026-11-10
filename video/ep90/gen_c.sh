#!/usr/bin/env bash
cd /home/user/videos-ai
/opt/v311/bin/python audio/build_voice.py --lines video/ep90/lines_c.txt --out video/ep90/voice/c.wav --exaggeration 0.8 --line-exaggeration "1:0.8" --line-seeds "1:7001" --gap 0.3 --closes 1 --pauses "" --retries 4 > video/ep90/voice/c.log 2>&1
echo done > video/ep90/voice/c.done
