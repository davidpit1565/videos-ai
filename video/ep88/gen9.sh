#!/usr/bin/env bash
cd /home/user/videos-ai
/opt/v311/bin/python audio/build_voice.py --lines video/ep88/lines9.txt --out video/ep88/voice/V.wav --exaggeration 0.74 --line-exaggeration "1:0.82,2:0.76,3:0.7,4:0.8" --line-seeds "1:8101,2:8102,3:8103,4:8104" --gap 0.3 --closes 4 --pauses "" > video/ep88/voice/V.log 2>&1
