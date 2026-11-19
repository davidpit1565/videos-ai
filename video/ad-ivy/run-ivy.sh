#!/usr/bin/env bash
# run-ivy.sh <tag>: Super Ivy ad: build-ivy.py, render, mix, gate. env: TRACK (bed file), START, BEDDB (default -8.5), ACCENT_SKIP, NORENDER=1
cd /home/user/videos-ai/video/ad-ivy; T=$1
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1
python3 build-ivy.py > /dev/null || { echo BUILDFAIL; exit 1; }
D=$(python3 -c "import json;print(json.load(open('cues-ivy.json'))['D'])"); echo "D=$D"
[ -n "$NORENDER" ] && exit 0
../ep89c/node_modules/.bin/hyperframes render hf -o out/pic-$T.mp4 --format mp4 --quiet > out/render-$T.log 2>&1 < /dev/null
[ -s out/pic-$T.mp4 ] || { echo RENDERFAIL; tail -5 out/render-$T.log; exit 1; }
TRACK=${TRACK:?set TRACK} START=${START:-0} /opt/v311/bin/python mix-ivy.py voice/narration-ivy.wav out/pic-$T.mp4 $D $T ${BEDDB:--8.5} 2>&1 < /dev/null | tail -1
rm -f out/mix5-$T*.wav out/sfx-$T.wav
cd ../..
ACCENT_SKIP=${ACCENT_SKIP:-} PATH=/opt/v311/bin:$PATH ./export/check_hf.sh video/ad-ivy/hf/index.html video/ad-ivy/voice/narration-ivy.wav video/ad-ivy/cues-ivy.json video/ad-ivy/out/ad-ivy-$T.mp4 video/ad-ivy/out/bed-ivy-$T.wav 1.0 > video/ad-ivy/out/gate-ivy-$T.txt 2>&1 < /dev/null
grep -E "^=== |ALL CHECKS|SOMETHING" video/ad-ivy/out/gate-ivy-$T.txt
