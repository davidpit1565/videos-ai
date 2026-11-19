#!/usr/bin/env bash
# runT.sh <tag> : opening variant of episode 102 (public 1021): build, render, bed (real library, exact length), mix, gate.  Voice: voice/narrationT.wav (stitchT.py).
set -u; cd /home/user/videos-ai/video/ep103t; T=$1
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 PATH=/opt/v311/bin:$PATH
SHIP=1 python3 buildT.py > /dev/null || { echo BUILDFAIL; exit 1; }
D=$(python3 -c "import json;print(json.load(open('cuesT.json'))['D'])"); echo "D=$D"
[ -n "${NORENDER:-}" ] && exit 0
[ -e out/pic-$T.mp4 ] && { echo "out/pic-$T.mp4 exists: fresh tag"; exit 2; }
../ep89c/node_modules/.bin/hyperframes render hf -o out/pic-$T.mp4 --format mp4 --quiet > out/render-$T.log 2>&1 < /dev/null
[ -s out/pic-$T.mp4 ] || { echo RENDERFAIL; tail -5 out/render-$T.log; exit 1; }
cd ../..
FORCE_TRACK=${TRACKFILE:-punchy--punchy-brass-groovy-pop-track--moonpub.mp3} python3 audio/pick_real_track.py $D video/ep103t/out/rawbed-$T.wav --mood punchy --no-record > video/ep103t/out/bedpick-$T.log 2>&1
python3 audio/check_music_bed.py video/ep103t/out/rawbed-$T.wav > video/ep103t/out/bedcheck-$T.txt 2>&1; cat video/ep103t/out/bedcheck-$T.txt | tail -3
cd video/ep103t
TRACK=$PWD/out/rawbed-$T.wav START=0 /opt/v311/bin/python mixT.py voice/narrationT.wav out/pic-$T.mp4 $D $T ${BEDDB:--8.5} 2>&1 < /dev/null | tail -1
rm -f out/mix5-$T*.wav out/sfx-$T.wav
cd ../..
./export/check_hf.sh video/ep103t/hf/index.html video/ep103t/voice/narrationT.wav video/ep103t/cuesT.json video/ep103t/out/ep102-$T.mp4 video/ep103t/out/bedT-$T.wav 1.0 > video/ep103t/out/gate-$T.txt 2>&1 < /dev/null
grep -E "^=== |ALL CHECKS|SOMETHING" video/ep103t/out/gate-$T.txt
