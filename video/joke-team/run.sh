#!/usr/bin/env bash
cd /home/user/videos-ai/video/joke-team; T=$1; export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1
python3 build.py > /dev/null || { echo BUILDFAIL; exit 1; }
D=$(python3 -c "import json;print(json.load(open('cues.json'))['D'])"); echo D=$D
../ep89c/node_modules/.bin/hyperframes render hf -o out/pic-$T.mp4 --format mp4 --quiet > out/render-$T.log 2>&1 < /dev/null
[ -s out/pic-$T.mp4 ] || { echo RENDERFAIL; tail -5 out/render-$T.log; exit 1; }
TRACK=${TRACK} START=${START:-0} /opt/v311/bin/python mix.py voice/narration.wav out/pic-$T.mp4 $D $T ${BEDDB:--11} 2>&1 | tail -2
