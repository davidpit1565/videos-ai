#!/bin/bash
# ep102 voice: one line at a time, one TTS at a time (flock), seed loop until the accent check passes. Resumable (pl/L<i>.ok).
cd /home/user/videos-ai
D=video/ep102/voice
EXA=(0.80 0.80 0.76 0.76 0.76 0.76 0.76 0.76 0.78 0.76 0.74 0.72 0.74 0.70 0.70)
SEEDS=${SEEDS:-"11 22 33 44 55 66 77 88"}
i=0
while IFS= read -r line; do
  i=$((i+1))
  [ -n "$ONLY" ] && [ "$ONLY" != "$i" ] && continue
  [ -f $D/pl/L$i.ok ] && continue
  echo "$line" > $D/pl/line$i.txt
  E=${EXA_OVERRIDE:-${EXA[$((i-1))]}}
  for seed in $SEEDS; do
    flock /tmp/tts.lock /opt/v311/bin/python audio/build_voice.py --lines $D/pl/line$i.txt --out $D/pl/L$i-$seed.wav --exaggeration $E --cfg 0.30 --gap 0.06 --long 0.15 --max-speedup 1.45 --min-rate 5.8 --no-verify --line-seeds "1:$seed" > $D/pl/log$i.txt 2>&1 < /dev/null
    sc=$(/opt/v311/bin/python audio/check_accent.py --cues $D/pl/L$i-$seed-cues.json $D/pl/L$i-$seed.wav 2>&1 < /dev/null | grep "ln 1" | sed 's/.*not-american=\([0-9.]*\).*/\1/')
    echo "L$i seed $seed accent $sc" >> $D/pl/out.txt
    if python3 -c "import sys;sys.exit(0 if float('${sc:-1}')<0.15 else 1)"; then echo $seed > $D/pl/L$i.ok; break; fi
  done
done < $D/lines.txt
echo DONE >> $D/pl/out.txt
