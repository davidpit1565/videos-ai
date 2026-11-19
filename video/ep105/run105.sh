#!/usr/bin/env bash
# run105.sh <tag>: ep105 (Claude Ultra free for open source) Miki + GSAP build: build105n.py, render, mix, gate.
# env: TRACK (bed file), START (trim start s), BEDDB (bed dB under voice), NORENDER=1 builds only.
cd /home/user/videos-ai/video/ep105; T=$1
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1
python3 build105n.py > /dev/null || { echo BUILDFAIL; exit 1; }
D=$(python3 -c "import json;print(json.load(open('cues105.json'))['D'])"); echo "D=$D"
[ -n "$NORENDER" ] && exit 0
../ep89c/node_modules/.bin/hyperframes render hf -o out/pic-$T.mp4 --format mp4 --quiet > out/render-$T.log 2>&1 < /dev/null
[ -s out/pic-$T.mp4 ] || { echo RENDERFAIL; tail -5 out/render-$T.log; exit 1; }
TRACK=${TRACK:?set TRACK} START=${START:-0} /opt/v311/bin/python mix105.py voice/narration-v105.wav out/pic-$T.mp4 $D $T ${BEDDB:--10} 2>&1 < /dev/null | tail -1
rm -f out/mix5-$T*.wav out/sfx-$T.wav
cd ../..
ACCENT_SKIP=${ACCENT_SKIP:-} PATH=/opt/v311/bin:$PATH ./export/check_hf.sh video/ep105/hf/index.html video/ep105/voice/narration-v105.wav video/ep105/cues105.json video/ep105/out/ep105-$T.mp4 video/ep105/out/bed105-$T.wav 1.0 > video/ep105/out/gate-$T.txt 2>&1 < /dev/null
grep -E "^=== |ALL CHECKS|SOMETHING" video/ep105/out/gate-$T.txt
