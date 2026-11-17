#!/usr/bin/env bash
# run4.sh <tag>: v4 (Miki style with the GSAP + motion skills; bed: punchy brass groovy pop, moonpub): stitch pl2 takes, word times, build104.py (SHIP=1), render, mix, gate.
cd /home/user/videos-ai/video/ep104; T=$1
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1
:
SHIP=1 python3 build104.py > /dev/null || { echo BUILDFAIL; exit 1; }
D=$(python3 -c "import json;print(json.load(open('cues104.json'))['D'])"); echo "D=$D"
[ -n "$NORENDER" ] && exit 0
../ep89c/node_modules/.bin/hyperframes render hf -o out/pic-$T.mp4 --format mp4 --quiet > out/render-$T.log 2>&1 < /dev/null
[ -s out/pic-$T.mp4 ] || { echo RENDERFAIL; tail -5 out/render-$T.log; exit 1; }
TRACK=${TRACK:-/home/user/videos-ai/audio/music-library/punchy--hip-hop-beat--themountain.mp3} START=${START:-16} /opt/v311/bin/python mix104.py voice/narration.wav out/pic-$T.mp4 $D $T ${BEDDB:--10} 2>&1 < /dev/null | tail -1
rm -f out/mix5-$T*.wav out/sfx-$T.wav
cd ../..
PATH=/opt/v311/bin:$PATH ./export/check_hf.sh video/ep104/hf/index.html video/ep104/voice/narration.wav video/ep104/cues104.json video/ep104/out/ep104-$T.mp4 video/ep104/out/bed104-$T.wav 1.0 > video/ep104/out/gate-$T.txt 2>&1 < /dev/null
grep -E "^=== |ALL CHECKS|SOMETHING" video/ep104/out/gate-$T.txt
