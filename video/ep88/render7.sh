#!/usr/bin/env bash
# render7.sh <tag> : rebuild html from build7 parts, render, mix, gate (no output filtering)
cd /home/user/videos-ai/video/ep88
T=$1
cat build7_head.py build7_top.py build7_style.py build7_tl.py > build7.py
VOICE=voice5/final python3 build7.py > out/build-$T.log 2>&1 || { echo BUILD FAILED >> out/build-$T.log; echo "done BUILDFAIL" > out/gate-$T.txt; exit 1; }
rm -f out/$T.mp4
cd hf; HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 npx --no-install hyperframes render -o ../out/$T.mp4 --format mp4 --quiet > ../out/render-$T.log 2>&1; cd ..
[ -s out/$T.mp4 ] || { echo "done RENDERFAIL" > out/gate-$T.txt; exit 1; }
./post7.sh $T
rm -f out/$T.mp4
