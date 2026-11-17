#!/usr/bin/env bash
cd /home/user/videos-ai; D=video/ep105/voice
for sd in "$@"; do
  flock /tmp/tts.lock /opt/v311/bin/python audio/build_voice.py --lines $D/lines.txt --out $D/p/P$sd.wav --exaggeration 0.72 --cfg 0.30 --gap 0.06 --long 0.15 --max-speedup 1.45 --min-rate 5.8 --no-verify --seed $sd --line-exaggeration "1:0.82,2:0.8,12:0.7" > $D/p/log$sd.txt 2>&1 < /dev/null
  PATH=/opt/v311/bin:$PATH python3 audio/check_accent.py $D/p/P$sd.wav > $D/p/acc$sd.txt 2>&1 < /dev/null
done
echo rolled "$@" > $D/p/roll-done.txt
