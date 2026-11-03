#!/bin/bash
# V4b: 12 more seeds (8901-9011), exaggeration 0.45-0.58, cfg 0.25/0.30/0.35. One TTS job at a time.
S=/tmp/claude-0/-home-user-videos-ai/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/scratchpad/ep82
cd /home/user/videos-ai
EXS=(0.45 0.47 0.49 0.51 0.53 0.55 0.57 0.46 0.48 0.50 0.52 0.58)
CFGS=(0.30 0.25 0.35 0.30 0.25 0.35 0.30 0.35 0.25 0.30 0.35 0.25)
SEEDS=(8901 8911 8921 8931 8941 8951 8961 8971 8981 8991 9001 9011)
for i in $(seq 0 11); do
  B=${SEEDS[$i]}
  [ -f $S/voice/y9$B.wav ] && continue
  /opt/v311/bin/python audio/build_voice.py --lines $S/voice/lines9.txt --out $S/voice/y9$B.wav --exaggeration ${EXS[$i]} --cfg ${CFGS[$i]} --prosody-rolls 4 --seed $B --line-seeds "1:$B" --no-verify > $S/voice/y9$B.log 2>&1
  echo done $B ex=${EXS[$i]} cfg=${CFGS[$i]} >> $S/voice/y9progress.txt
done
echo ALLDONE >> $S/voice/y9progress.txt
