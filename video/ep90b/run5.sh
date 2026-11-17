#!/usr/bin/env bash
cd /home/user/videos-ai/video/ep90b
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1
python3 build90b5.py > out/build5.log 2>&1 || { tail -3 out/build5.log; exit 1; }
./node_modules/.bin/hyperframes render hf -o /tmp/r90b5.mp4 --format mp4 --quiet > out/render-final5.log 2>&1
[ -s /tmp/r90b5.mp4 ] || { echo RENDERFAIL; tail -3 out/render-final5.log; exit 1; }
/opt/v311/bin/python mix90b5.py /tmp/r90b5.mp4 final5
rm -f /tmp/r90b5.mp4
cd ../..
./export/check_hf.sh video/ep90b/hf/index.html video/ep90b/out/narration90b.wav video/ep90b/cues90b5.json video/ep90b/out/ep90b-final5.mp4 > video/ep90b/out/gate-final5.txt 2>&1
echo gatedone
