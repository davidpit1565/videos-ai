#!/usr/bin/env bash
# run4.sh <tag>: v4 (Miki style with the GSAP + motion skills; bed: punchy brass groovy pop, moonpub): stitch pl2 takes, word times, build102v4.py (SHIP=1), render, mix, gate.
cd /home/user/videos-ai/video/ep102; T=$1
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1
if [ -z "$NOVOICE" ]; then /opt/v311/bin/python voice/stitch4.py | tail -1; /opt/v311/bin/python voice/words4.py 2>&1 < /dev/null | grep -vi warn | tail -1 | cut -c1-160; fi
SHIP=1 python3 build102v4.py > /dev/null || { echo BUILDFAIL; exit 1; }
D=$(python3 -c "import json;print(json.load(open('cues102.json'))['D'])"); echo "D=$D"
[ -n "$NORENDER" ] && exit 0
../ep89c/node_modules/.bin/hyperframes render hf -o out/pic-$T.mp4 --format mp4 --quiet > out/render-$T.log 2>&1 < /dev/null
[ -s out/pic-$T.mp4 ] || { echo RENDERFAIL; tail -5 out/render-$T.log; exit 1; }
TRACK=${TRACK:-/home/user/videos-ai/audio/music-library/punchy--punchy-brass-groovy-pop-track--moonpub.mp3} START=${START:-0} /opt/v311/bin/python mix102.py voice/narration-v4.wav out/pic-$T.mp4 $D $T ${BEDDB:--10} 2>&1 < /dev/null | tail -1
rm -f out/mix5-$T*.wav out/sfx-$T.wav
cd ../..
PATH=/opt/v311/bin:$PATH ./export/check_hf.sh video/ep102/hf/index.html video/ep102/voice/narration-v4.wav video/ep102/cues102.json video/ep102/out/ep102-$T.mp4 video/ep102/out/bed102-$T.wav 1.0 > video/ep102/out/gate-$T.txt 2>&1 < /dev/null
grep -E "^=== |ALL CHECKS|SOMETHING" video/ep102/out/gate-$T.txt
