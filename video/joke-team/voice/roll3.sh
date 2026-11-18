#!/usr/bin/env bash
cd /home/user/videos-ai; D=video/joke-team/voice
for sd in "$@"; do
  flock /tmp/tts.lock /opt/v311/bin/python audio/build_voice.py --lines $D/l3.txt --out $D/p/Q$sd.wav --exaggeration 0.74 --line-exaggeration "1:0.66,2:0.66,3:0.66" --cfg 0.30 --gap 0.06 --long 0.15 --max-speedup 1.45 --min-rate 5.8 --no-verify --seed $sd > $D/p/log$sd.txt 2>&1 < /dev/null
  PATH=/opt/v311/bin:$PATH python3 audio/check_accent.py $D/p/Q$sd.wav > $D/p/qacc$sd.txt 2>&1 < /dev/null
done
echo done > $D/p/roll3-done.txt
