#!/usr/bin/env bash
cd /home/user/videos-ai
/opt/v311/bin/python audio/build_voice.py --lines video/ep88/lines9.txt --out video/ep88/voice/U.wav --exaggeration 0.74 --line-exaggeration "1:0.76,2:0.7,3:0.74,4:0.66" --line-seeds "1:7101,2:7102,3:7103,4:7104" --gap 0.3 --closes 4 --pauses "" > video/ep88/voice/U.log 2>&1
