#!/usr/bin/env bash
cd /home/user/videos-ai; D=video/ep105/voice
for sd in "$@"; do
  flock /tmp/tts.lock /opt/v311/bin/python audio/build_voice.py --lines $D/l4.txt --out $D/p/W$sd.wav --exaggeration 0.7 --line-exaggeration "1:0.56,2:0.62,3:0.68,4:0.72,5:0.76,6:0.80" --cfg 0.30 --gap 0.06 --long 0.15 --max-speedup 1.45 --min-rate 5.8 --no-verify --seed $sd > $D/p/wlog$sd.txt 2>&1 < /dev/null
done
echo done > $D/p/roll4-done.txt
