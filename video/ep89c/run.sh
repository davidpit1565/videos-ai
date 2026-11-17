#!/usr/bin/env bash
cd /home/user/videos-ai/video/ep89c; T=$1; MOOD=${2:-punchy}
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1
python3 build89c.py > out/build-$T.log 2>&1 || { tail -5 out/build-$T.log; exit 1; }
D=$(python3 -c "import json;print(json.load(open('cues89c.json'))['D'])")
mkdir -p music
FORCE_TRACK=${FT:-} python3 ../../audio/pick_real_track.py $D music/final-$T.wav --mood $MOOD | tail -1
python3 ../../audio/check_music_bed.py music/final-$T.wav | tail -2
./node_modules/.bin/hyperframes render hf -o /tmp/r89-$T.mp4 --format mp4 --quiet > out/render-$T.log 2>&1
[ -s /tmp/r89-$T.mp4 ] || { echo RENDERFAIL; tail -5 out/render-$T.log; exit 1; }
/opt/v311/bin/python mix89c.py out/narration89c.wav /tmp/r89-$T.mp4 $D $T music/final-$T.wav 2>&1 | tail -2
rm -f /tmp/r89-$T.mp4 out/mix5-$T*.wav out/duck5-$T.wav out/sfx-$T.wav
cd ../..
VOL=$(python3 -c "import json;print(round(json.load(open('video/ep89c/out/gain5-$T.json'))['lin']*10**(1.3/20),3))")
./export/check_hf.sh video/ep89c/hf/index.html video/ep89c/out/narration89c.wav video/ep89c/cues89c.json video/ep89c/out/ep89-$T.mp4 video/ep89c/out/bed89-$T.wav $VOL > video/ep89c/out/gate-$T.txt 2>&1
grep -E "^=== |SUMMARY|FAIL|PASS|SKIP" video/ep89c/out/gate-$T.txt | head -12
