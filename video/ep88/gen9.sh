#!/usr/bin/env bash
cd /home/user/videos-ai
/opt/v311/bin/python audio/build_voice.py --lines video/ep88/lines9.txt --out video/ep88/voice/W.wav --exaggeration 0.74 --line-exaggeration "1:0.82,2:0.74,3:0.78,4:0.74,5:0.68,6:0.72" --line-seeds "1:9101,2:9102,3:9103,4:9104,5:9105,6:9106" --gap 0.3 --closes 3,6 --pauses "" > video/ep88/voice/W.log 2>&1
