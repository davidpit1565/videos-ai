#!/usr/bin/env bash
cd /home/user/videos-ai/video/ep90b
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1
python3 build90b2.py > out/build2.log 2>&1 || { tail -3 out/build2.log; exit 1; }
./node_modules/.bin/hyperframes render hf -o /tmp/r90b2.mp4 --format mp4 --quiet > out/render-final2.log 2>&1
[ -s /tmp/r90b2.mp4 ] || { echo RENDERFAIL; tail -3 out/render-final2.log; exit 1; }
/opt/v311/bin/python mix90b2.py /tmp/r90b2.mp4 final2 punchy--hip-hop-beat--themountain.mp3
/opt/v311/bin/python mix90b2.py /tmp/r90b2.mp4 A cinematic--dramatic--themountain.mp3 preview
/opt/v311/bin/python mix90b2.py /tmp/r90b2.mp4 B punchy--trending-instagram-reels-music--delosound.mp3 preview
cd ../..
python3 audio/check_music_bed.py video/ep90b/out/bed-final2.wav > video/ep90b/out/bed-check.txt 2>&1
for t in A B; do python3 audio/check_music_bed.py video/ep90b/out/bed-$t.wav >> video/ep90b/out/bed-check.txt 2>&1; done
(node export/safe_check_hf.js video/ep90b/hf/index.html --every 0.2 2>&1 | grep -v Warn; echo ====; python3 export/qa.py video/ep90b/out/ep90b-final2.mp4 --build video/ep90b/hf/index.html --hf 2>&1 | grep -v Warn) > video/ep90b/out/gate-final2.txt
rm -f /tmp/r90b2.mp4 video/ep90b/out/bed-*.wav
echo gatedone
