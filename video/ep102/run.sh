#!/usr/bin/env bash
# run.sh <tag>: stitch the accepted takes, word times, build (SHIP=1), render, mix (voice + sfx + bed), gate. One TTS-free pass.
cd /home/user/videos-ai/video/ep102; T=$1
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1
if [ -z "$NOVOICE" ]; then /opt/v311/bin/python voice/stitch.py | tail -1; /opt/v311/bin/python voice/words.py 2>&1 < /dev/null | grep -vi warn | tail -1 | cut -c1-120; fi
SHIP=1 python3 build102.py > /dev/null || { echo BUILDFAIL; exit 1; }
D=$(python3 -c "import json;print(json.load(open('cues102.json'))['D'])"); echo "D=$D"
if [ -z "$NORENDER" ]; then
  ../ep89c/node_modules/.bin/hyperframes render hf -o out/pic-$T.mp4 --format mp4 --quiet > out/render-$T.log 2>&1 < /dev/null
  [ -s out/pic-$T.mp4 ] || { echo RENDERFAIL; tail -5 out/render-$T.log; exit 1; }
fi
/opt/v311/bin/python mix102.py voice/narration-raw.wav out/pic-$T.mp4 $D $T ${BEDDB:--10} 2>&1 < /dev/null | tail -2
rm -f out/mix5-$T*.wav out/sfx-$T.wav
cd ../..
VOL=1.0   # bed102-<tag>.wav is written by mix102.py already at its mixed level (gain + envelope), so the check must not scale it again
PATH=/opt/v311/bin:$PATH ./export/check_hf.sh video/ep102/hf/index.html video/ep102/voice/narration-raw.wav video/ep102/cues102.json video/ep102/out/ep102-$T.mp4 video/ep102/out/bed102-$T.wav $VOL > video/ep102/out/gate-$T.txt 2>&1 < /dev/null
grep -E "^=== |ALL CHECKS|SOMETHING" video/ep102/out/gate-$T.txt
