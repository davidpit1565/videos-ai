#!/usr/bin/env bash
# run.sh <tag> : build -> render -> mix (music/final.wav) -> gate.   GAPS/TAIL as used for the shipped timing
cd /home/user/videos-ai/video/ep89; T=$1
GAPS=0.3,0.3,0.3 TAIL=0.55 /opt/v311/bin/python build89.py > out/build-$T.log 2>&1 || { tail -5 out/build-$T.log; exit 1; }
D=$(python3 -c "import json;print(json.load(open('cues89.json'))['D'])")
(cd hf; HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 npx --no-install hyperframes render -o ../out/r-$T.mp4 --format mp4 --quiet > ../out/render-$T.log 2>&1)
[ -s out/r-$T.mp4 ] || { echo RENDERFAIL; exit 1; }
/opt/v311/bin/python mix89.py out/narration89.wav out/r-$T.mp4 $D $T music/final.wav 2>&1 | tail -2
rm -f out/r-$T.mp4 out/mix5-$T*.wav out/duck5-$T.wav
cd ../..
VOL=$(python3 -c "import json;print(round(json.load(open('video/ep89/out/gain5-$T.json'))['lin']*10**(1.3/20),3))")
./export/check_hf.sh video/ep89/hf/index.html video/ep89/out/narration89.wav video/ep89/cues89.json video/ep89/out/ep89-$T.mp4 video/ep89/out/bed89-$T.wav $VOL > video/ep89/out/gate-$T.txt 2>&1
grep -E "^=== |SUMMARY|FAIL|PASS|SKIP" video/ep89/out/gate-$T.txt | head -12
