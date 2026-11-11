#!/usr/bin/env bash
cd /home/user/videos-ai/video/ep90b
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1
python3 build90b6.py > out/build6.log 2>&1 || { tail -3 out/build6.log; exit 1; }
./node_modules/.bin/hyperframes render hf -o /tmp/r90b6.mp4 --format mp4 --quiet > out/render-final6.log 2>&1
[ -s /tmp/r90b6.mp4 ] || { echo RENDERFAIL; tail -3 out/render-final6.log; exit 1; }
/opt/v311/bin/python mix90b6.py /tmp/r90b6.mp4 final6
rm -f /tmp/r90b6.mp4
cd ../..
(node export/safe_check_hf.js video/ep90b/hf/index.html --every 0.2 2>&1 | grep -v Warn; echo ====; python3 export/qa.py video/ep90b/out/ep90b-final6.mp4 --build video/ep90b/hf/index.html --hf 2>&1 | grep -v Warn) > video/ep90b/out/gate-final6.txt
echo gatedone
