#!/usr/bin/env bash
cd /home/user/videos-ai/video/ep90b
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1
python3 build90b7.py > out/build7.log 2>&1 || { tail -3 out/build7.log; exit 1; }
./node_modules/.bin/hyperframes render hf -o /tmp/r90b7.mp4 --format mp4 --quiet > out/render-final7.log 2>&1
[ -s /tmp/r90b7.mp4 ] || { echo RENDERFAIL; tail -3 out/render-final7.log; exit 1; }
/opt/v311/bin/python mix90b7.py /tmp/r90b7.mp4 final7 punchy--hip-hop-beat--themountain.mp3
cp out/bed7-final7.wav out/bed-main.wav
/opt/v311/bin/python mix90b7.py /tmp/r90b7.mp4 cinematic cinematic--dramatic--themountain.mp3 preview
rm -f /tmp/r90b7.mp4
cd ../..
VOL=$(python3 -c "import json;print(json.load(open('video/ep90b/out/vol7-final7.json'))['vol'])")
python3 audio/check_music_bed.py video/ep90b/out/bed-main.wav > video/ep90b/out/bed7-check.txt 2>&1
./export/check_hf.sh video/ep90b/hf/index.html video/ep90b/out/narration90b7.wav video/ep90b/cues90b7.json video/ep90b/out/ep90b-final7.mp4 video/ep90b/out/bed-main.wav $VOL > video/ep90b/out/gate-final7.txt 2>&1
rm -f video/ep90b/out/bed7-*.wav
echo gatedone
