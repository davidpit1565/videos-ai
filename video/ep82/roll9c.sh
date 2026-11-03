#!/bin/bash
# V4: 12 NEW seeds of the full sentence (different from 8601-8671), exaggeration 0.50-0.62, cfg 0.25/0.30/0.35. One TTS job at a time.
S=/tmp/claude-0/-home-user-videos-ai/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/scratchpad/ep82
cd /home/user/videos-ai
EXS=(0.50 0.52 0.54 0.56 0.58 0.60 0.62 0.51 0.53 0.55 0.57 0.59)
CFGS=(0.30 0.25 0.35 0.30 0.25 0.35 0.30 0.25 0.35 0.30 0.25 0.35)
SEEDS=(8701 8711 8721 8731 8741 8751 8761 8771 8781 8791 8801 8811)
for i in $(seq 0 11); do
  B=${SEEDS[$i]}
  [ -f $S/voice/x9$B.wav ] && continue
  /opt/v311/bin/python audio/build_voice.py --lines $S/voice/lines9.txt --out $S/voice/x9$B.wav --exaggeration ${EXS[$i]} --cfg ${CFGS[$i]} --prosody-rolls 4 --seed $B --line-seeds "1:$B" --no-verify > $S/voice/x9$B.log 2>&1
  echo done $B ex=${EXS[$i]} cfg=${CFGS[$i]} >> $S/voice/x9progress.txt
done
echo ALLDONE >> $S/voice/x9progress.txt
