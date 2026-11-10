#!/usr/bin/env bash
cd /home/user/videos-ai
/opt/v311/bin/python audio/build_voice.py --lines video/ep90/lines_b.txt --out video/ep90/voice/b.wav --exaggeration 0.78 --line-exaggeration "1:0.78,2:0.72" --line-seeds "1:6001,2:6002" --gap 0.3 --closes 2 --pauses "" --retries 4 > video/ep90/voice/b.log 2>&1
echo done > video/ep90/voice/b.done
