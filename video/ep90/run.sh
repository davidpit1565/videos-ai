#!/usr/bin/env bash
cd /home/user/videos-ai/video/ep90; T=$1
GAPS=0.3,0.3,0.3 TAIL=0.5 /opt/v311/bin/python build90.py > out/build-$T.log 2>&1 || { tail -5 out/build-$T.log; exit 1; }
D=$(python3 -c "import json;print(json.load(open('cues90.json'))['D'])")
(cd hf; HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 npx --no-install hyperframes render -o /tmp/r90-$T.mp4 --format mp4 --quiet > ../out/render-$T.log 2>&1)
[ -s /tmp/r90-$T.mp4 ] || { echo RENDERFAIL; exit 1; }
/opt/v311/bin/python mix90.py out/narration90.wav /tmp/r90-$T.mp4 $D $T music/final.wav 2>&1 | tail -2
rm -f /tmp/r90-$T.mp4 out/mix5-$T*.wav out/duck5-$T.wav
cd ../..
VOL=$(python3 -c "import json;print(round(json.load(open('video/ep90/out/gain5-$T.json'))['lin']*10**(1.3/20),3))")
./export/check_hf.sh video/ep90/hf/index.html video/ep90/out/narration90.wav video/ep90/cues90.json video/ep90/out/ep90-$T.mp4 video/ep90/out/bed90-$T.wav $VOL > video/ep90/out/gate-$T.txt 2>&1
grep -E "^=== |SUMMARY|FAIL|PASS|SKIP" video/ep90/out/gate-$T.txt | head -12
