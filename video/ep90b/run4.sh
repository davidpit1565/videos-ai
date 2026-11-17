#!/usr/bin/env bash
cd /home/user/videos-ai/video/ep90b
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1
python3 build90b4.py > out/build3.log 2>&1 || { tail -3 out/build3.log; exit 1; }
./node_modules/.bin/hyperframes render hf -o /tmp/r90b3.mp4 --format mp4 --quiet > out/render-final4.log 2>&1
[ -s /tmp/r90b3.mp4 ] || { echo RENDERFAIL; tail -3 out/render-final4.log; exit 1; }
D=$(python3 -c "import json;print(json.load(open('duck90b.json'))['D'])")
/opt/v311/bin/python mix90b3.py /tmp/r90b3.mp4 $D final4
cd ../..
(node export/safe_check_hf.js video/ep90b/hf/index.html --every 0.2 2>&1 | grep -v Warn; echo ====; python3 export/qa.py video/ep90b/out/ep90b-final4.mp4 --build video/ep90b/hf/index.html --hf 2>&1 | grep -v Warn) > video/ep90b/out/gate-final4.txt
rm -f /tmp/r90b3.mp4
echo gatedone
