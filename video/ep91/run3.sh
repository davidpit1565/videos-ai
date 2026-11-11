#!/usr/bin/env bash
cd /home/user/videos-ai/video/ep91; T=$1
GAPS=0.3,0.3,0.3 TAIL=0.35 /opt/v311/bin/python build91c.py > out/build-$T.log 2>&1 || { tail -5 out/build-$T.log; exit 1; }
D=$(python3 -c "import json;print(json.load(open('cues91c.json'))['D'])")
python3 ../../audio/pick_real_track.py $D music/final3.wav --mood bright | tail -1
python3 ../../audio/check_music_bed.py music/final3.wav | tail -2
(cd hf3; HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 npx --no-install hyperframes render -o /tmp/r91-$T.mp4 --format mp4 --quiet > ../out/render-$T.log 2>&1)
[ -s /tmp/r91-$T.mp4 ] || { echo RENDERFAIL; exit 1; }
/opt/v311/bin/python mix91c.py out/narration91c.wav /tmp/r91-$T.mp4 $D $T music/final3.wav 2>&1 | tail -2
rm -f /tmp/r91-$T.mp4 out/mix5-$T*.wav out/duck5-$T.wav out/sfx-$T.wav
cd ../..
VOL=$(python3 -c "import json;print(round(json.load(open('video/ep91/out/gain5-$T.json'))['lin']*10**(1.3/20),3))")
./export/check_hf.sh video/ep91/hf3/index.html video/ep91/out/narration91c.wav video/ep91/cues91c.json video/ep91/out/ep91-$T.mp4 video/ep91/out/bed91-$T.wav $VOL > video/ep91/out/gate-$T.txt 2>&1
grep -E "^=== |SUMMARY|FAIL|PASS|SKIP" video/ep91/out/gate-$T.txt | head -12
