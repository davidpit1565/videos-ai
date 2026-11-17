#!/bin/bash
# reroll.sh <line> <exaggeration> <seed...> : extra takes for one line (does not touch L<i>.ok); accent score appended to pl/out.txt
cd /home/user/videos-ai; D=video/ep102/voice; i=$1; E=$2; shift 2
sed -n "${i}p" $D/lines.txt > $D/pl/line$i.txt
[ -n "$TEXT" ] && echo "$TEXT" > $D/pl/line$i.txt
for seed in "$@"; do
  flock /tmp/tts.lock /opt/v311/bin/python audio/build_voice.py --lines $D/pl/line$i.txt --out $D/pl/L$i-$seed.wav --exaggeration $E --cfg 0.30 --gap 0.06 --long 0.15 --max-speedup 1.45 --min-rate 5.8 --no-verify --line-seeds "1:$seed" > $D/pl/log$i-r.txt 2>&1 < /dev/null
  sc=$(/opt/v311/bin/python audio/check_accent.py --cues $D/pl/L$i-$seed-cues.json $D/pl/L$i-$seed.wav 2>&1 < /dev/null | grep "ln 1" | sed 's/.*not-american=\([0-9.]*\).*/\1/')
  echo "L$i seed $seed accent $sc (reroll E=$E)" >> $D/pl/out.txt
done
