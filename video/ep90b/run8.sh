#!/usr/bin/env bash
# final8: build -> render (hyperframes installed in /tmp/e8) -> mix -> gate. All outputs are NEW files (final8).
set -e
cd /home/user/videos-ai/video/ep90b
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1
python3 build90b8.py > out/build8.log 2>&1
(cd /tmp/e8 && ./node_modules/.bin/hyperframes render hf8 -o /tmp/e8/r8.mp4 --format mp4 --quiet > /home/user/videos-ai/video/ep90b/out/render-final8.log 2>&1)
/opt/v311/bin/python mix90b8.py /tmp/e8/r8.mp4 final8 punchy--hip-hop-beat--themountain.mp3
cp out/bed8-final8.wav out/bed-main8.wav
