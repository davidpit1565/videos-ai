#!/usr/bin/env bash
# fin7.sh <tag> : build7 render + mix7 + gate
cd /home/user/videos-ai/video/ep88
T=$1
cat build7_head.py build7_top.py build7_style.py build7_tl.py > build7.py
S=$(date +%s)
VOICE=voice5/final python3 build7.py --render $T 2>&1 | grep -E "rror|Trace|D=|scenes|File|line "
echo "render seconds: $(( $(date +%s) - S ))" > out/time-$T.txt
D=$(python3 -c "import json;print(json.load(open('cues7.json'))['D'])")
python3 mix7.py out/narration7.wav out/$T.mp4 $D $T 2>&1 | tail -1
cd ../..
VOL=$(python3 -c "import json;print(round(json.load(open('video/ep88/out/gain5-$T.json'))['lin']*10**(1.3/20),3))")
./export/check_hf.sh video/ep88/hf/index.html video/ep88/out/narration7.wav video/ep88/cues7.json video/ep88/out/ep88-$T.mp4 video/ep88/out/bed5.wav $VOL > video/ep88/out/gate-$T.txt 2>&1
echo done >> video/ep88/out/gate-$T.txt
