#!/usr/bin/env bash
# fin.sh <tag> : render + mix + gate
cd /home/user/videos-ai/video/ep88
T=$1
VOICE=voice5/final python3 build5.py --render $T 2>&1 | grep -E "rror|Trace|D="
D=$(python3 -c "import json;print(json.load(open('cues5.json'))['D'])")
python3 mix5.py out/narration5.wav out/$T.mp4 $D $T 2>&1 | tail -1
cd ../..
VOL=$(python3 -c "import json;print(round(json.load(open('video/ep88/out/gain5-$T.json'))['lin']*10**(1.3/20),3))")
./export/check_hf.sh video/ep88/hf/index.html video/ep88/out/narration5.wav video/ep88/cues5.json video/ep88/out/ep88-$T.mp4 video/ep88/out/bed5.wav $VOL > video/ep88/out/gate-$T.txt 2>&1
echo done >> video/ep88/out/gate-$T.txt
