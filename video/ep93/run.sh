#!/usr/bin/env bash
cd /home/user/videos-ai/video/ep93; T=$1
GAPS=0.3,0.3,0.3 TAIL=0.5 /opt/v311/bin/python build93.py > out/build-$T.log 2>&1 || { tail -5 out/build-$T.log; exit 1; }
D=$(python3 -c "import json;print(json.load(open('cues93.json'))['D'])")
(cd hf; HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 npx --no-install hyperframes render -o /tmp/r93-$T.mp4 --format mp4 --quiet > ../out/render-$T.log 2>&1)
[ -s /tmp/r93-$T.mp4 ] || { echo RENDERFAIL; exit 1; }
/opt/v311/bin/python mix93.py out/narration93.wav /tmp/r93-$T.mp4 $D $T music/final.wav 2>&1 | tail -2
rm -f /tmp/r93-$T.mp4 out/mix5-$T*.wav out/duck5-$T.wav
cd ../..
VOL=$(python3 -c "import json;print(round(json.load(open('video/ep93/out/gain5-$T.json'))['lin']*10**(1.3/20),3))")
./export/check_hf.sh video/ep93/hf/index.html video/ep93/out/narration93.wav video/ep93/cues93.json video/ep93/out/ep93-$T.mp4 video/ep93/out/bed93-$T.wav $VOL > video/ep93/out/gate-$T.txt 2>&1
grep -E "^=== |SUMMARY|FAIL|PASS|SKIP" video/ep93/out/gate-$T.txt | head -12
