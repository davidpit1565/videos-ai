#!/bin/bash
# hook_take.sh <tag> [seeds] : renders the hook line (voice/pl/H-<tag>.txt) once per seed under flock, writes accent scores to voice/pl/out-<tag>.txt
cd /home/user/videos-ai; D=video/ep103t/voice; PY=/opt/v311/bin/python; T=$1; SEEDS=${2:-"11 22 33"}; E=${EXAH:-0.82}
for seed in $SEEDS; do
  [ -f $D/pl/H-$T-$seed.wav ] && continue
  flock /tmp/tts.lock $PY audio/build_voice.py --lines $D/pl/H-$T.txt --out $D/pl/H-$T-$seed.wav --exaggeration $E --cfg 0.30 --gap 0.06 --long 0.15 --max-speedup 1.45 --min-rate 5.8 --no-verify --line-seeds "1:$seed" > $D/pl/log-H-$T.txt 2>&1 < /dev/null
  sc=$($PY audio/check_accent.py --cues $D/pl/H-$T-$seed-cues.json $D/pl/H-$T-$seed.wav 2>&1 < /dev/null | grep "ln 1" | sed 's/.*not-american=\([0-9.]*\).*/\1/')
  echo "H-$T seed $seed E=$E accent $sc" >> $D/pl/out-$T.txt
done
