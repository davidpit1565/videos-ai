#!/usr/bin/env bash
# final9: build -> render (hyperframes installed in /tmp/e8) -> mix -> gate. All outputs are NEW files (final9).
set -e
cd /home/user/videos-ai/video/ep90b
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1
python3 build90b9.py > out/build9.log 2>&1
(cd /tmp/e8 && ./node_modules/.bin/hyperframes render hf9 -o /tmp/e8/r9.mp4 --format mp4 --quiet > /home/user/videos-ai/video/ep90b/out/render-final9.log 2>&1)
/opt/v311/bin/python mix90b9.py /tmp/e8/r9.mp4 final9 punchy--hip-hop-beat--themountain.mp3
cp out/bed9-final9.wav out/bed-main9.wav
