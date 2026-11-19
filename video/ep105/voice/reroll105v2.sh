#!/bin/bash
# reroll105v2.sh <line> <exaggeration> <seed...> ; optional TEXT env overrides the TTS input text (same words, other punctuation)
cd /home/user/videos-ai; D=video/ep105/voice; i=$1; E=$2; shift 2
T=${TEXT:-$(sed -n "${i}p" $D/lines105.txt)}
for seed in "$@"; do
  [ -f $D/pl/V2-L$i-$seed.wav ] && continue
  echo "$T" > $D/pl/V2-rr$i-$seed.txt
  flock /tmp/tts.lock /opt/v311/bin/python audio/build_voice.py --lines $D/pl/V2-rr$i-$seed.txt --out $D/pl/V2-L$i-$seed.wav --exaggeration $E --cfg 0.30 --gap 0.06 --long 0.15 --max-speedup 1.45 --min-rate 5.8 --no-verify --line-seeds "1:$seed" > $D/pl/V2-logrr$i.txt 2>&1 < /dev/null
  sc=$(/opt/v311/bin/python audio/check_accent.py --cues $D/pl/V2-L$i-$seed-cues.json $D/pl/V2-L$i-$seed.wav 2>&1 < /dev/null | grep "ln 1" | sed 's/.*not-american=\([0-9.]*\).*/\1/')
  echo "V2 L$i seed $seed accent $sc (reroll E=$E text='$T')" >> $D/pl/out-v2.txt
done
echo RRDONE$i >> $D/pl/out-v2.txt
