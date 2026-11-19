#!/usr/bin/env bash
# run106.sh <tag> "<frame0 lines | separated>" [accent_line_index] : words -> build -> render -> bed -> mix -> gate, for a tag whose voice/narration-<tag>.wav + voice/cues-<tag>.json already exist.
# env: TRACKFILE (library file name, default punchy--trending-instagram-reels-music--bombinsound.mp3), BEDDB (default -8.5), ACCENT_SKIP
set -u; cd /home/user/videos-ai/video/ep106; T=$1; F0=$2; ACC=${3:-}
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 PATH=/opt/v311/bin:$PATH
mkdir -p out
/opt/v311/bin/python voice/words.py $T || { echo WORDSFAIL; exit 1; }
python3 build106.py $T "$F0" $ACC > out/build-$T.log || { echo BUILDFAIL; cat out/build-$T.log; exit 1; }
D=$(python3 -c "import json;print(json.load(open('voice/cues-$T.json'))['D'])"); echo "D=$D"
rm -f out/pic-$T.mp4
../ep89c/node_modules/.bin/hyperframes render hf-$T -o out/pic-$T.mp4 --format mp4 --quiet > out/render-$T.log 2>&1 < /dev/null
[ -s out/pic-$T.mp4 ] || { echo RENDERFAIL; tail -5 out/render-$T.log; exit 1; }
cd ../..
FORCE_TRACK=${TRACKFILE:-punchy--trending-instagram-reels-music--bombinsound.mp3} python3 audio/pick_real_track.py $D video/ep106/out/rawbed-$T.wav --mood punchy --no-record > video/ep106/out/bedpick-$T.log 2>&1
python3 audio/check_music_bed.py video/ep106/out/rawbed-$T.wav > video/ep106/out/bedcheck-$T.txt 2>&1
cd video/ep106
TRACK=out/rawbed-$T.wav START=0 /opt/v311/bin/python mix106.py voice/narration-$T.wav out/pic-$T.mp4 $D $T ${BEDDB:--8.5} 2>&1 < /dev/null | tail -1
rm -f out/mix5-$T*.wav out/sfx-$T.wav
cd ../..
ACCENT_SKIP=${ACCENT_SKIP:-} ./export/check_hf.sh video/ep106/hf-$T/index.html video/ep106/voice/narration-$T.wav video/ep106/voice/cues-$T.json video/ep106/out/ep106-$T.mp4 video/ep106/out/bed106-$T.wav 1.0 > video/ep106/out/gate-$T.txt 2>&1 < /dev/null
grep -E "^=== |ALL CHECKS|SOMETHING" video/ep106/out/gate-$T.txt
