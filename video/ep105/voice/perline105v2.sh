#!/bin/bash
# v2: one TTS at a time; takes pl/V2-L<i>-<seed>.wav for every seed (no early stop); line 11 = ep104 clip (no TTS)
cd /home/user/videos-ai; D=video/ep105/voice; PY=/opt/v311/bin/python
EXA=(0.76 0.70 0.68 0.68 0.68 0.68 0.70 0.70 0.68 0.70)
SEEDS=${SEEDS:-"11 22 33"}
i=0
while IFS= read -r line; do
  i=$((i+1)); [ $i -ge 11 ] && break
  [ -n "$ONLY" ] && ! echo " $ONLY " | grep -q " $i " && continue
  echo "$line" > $D/pl/V2-line$i.txt
  E=${EXA_OVERRIDE:-${EXA[$((i-1))]}}
  for seed in $SEEDS; do
    [ -f $D/pl/V2-L$i-$seed.wav ] && continue
    flock /tmp/tts.lock $PY audio/build_voice.py --lines $D/pl/V2-line$i.txt --out $D/pl/V2-L$i-$seed.wav --exaggeration $E --cfg 0.30 --gap 0.06 --long 0.15 --max-speedup 1.45 --min-rate 5.8 --no-verify --line-seeds "1:$seed" > $D/pl/V2-log$i.txt 2>&1 < /dev/null
    sc=$($PY audio/check_accent.py --cues $D/pl/V2-L$i-$seed-cues.json $D/pl/V2-L$i-$seed.wav 2>&1 < /dev/null | grep "ln 1" | sed 's/.*not-american=\([0-9.]*\).*/\1/')
    echo "V2 L$i seed $seed E=$E accent $sc" >> $D/pl/out-v2.txt
  done
done < $D/lines105.txt
echo V2DONE >> $D/pl/out-v2.txt
