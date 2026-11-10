#!/usr/bin/env bash
# fin6.sh <tag> : build6 render + mix6 + gate
cd /home/user/videos-ai/video/ep88
T=$1
cat build6_head.py build6_tail.py > build6.py
S=$(date +%s)
VOICE=voice5/final python3 build6.py --render $T 2>&1 | grep -E "rror|Trace|D=|scenes"
echo "render seconds: $(( $(date +%s) - S ))" > out/time-$T.txt
D=$(python3 -c "import json;print(json.load(open('cues6.json'))['D'])")
python3 mix6.py out/narration6.wav out/$T.mp4 $D $T 2>&1 | tail -1
cd ../..
VOL=$(python3 -c "import json;print(round(json.load(open('video/ep88/out/gain5-$T.json'))['lin']*10**(1.3/20),3))")
./export/check_hf.sh video/ep88/hf/index.html video/ep88/out/narration6.wav video/ep88/cues6.json video/ep88/out/ep88-$T.mp4 video/ep88/out/bed5.wav $VOL > video/ep88/out/gate-$T.txt 2>&1
echo done >> video/ep88/out/gate-$T.txt
