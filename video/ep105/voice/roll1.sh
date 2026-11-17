#!/usr/bin/env bash
cd /home/user/videos-ai; D=video/ep105/voice
for sd in "$@"; do
  flock /tmp/tts.lock /opt/v311/bin/python audio/build_voice.py --lines $D/l1.txt --out $D/p/U$sd.wav --exaggeration 0.84 --cfg 0.30 --gap 0.06 --long 0.15 --max-speedup 1.45 --min-rate 5.8 --no-verify --seed $sd > $D/p/ulog$sd.txt 2>&1 < /dev/null
  PATH=/opt/v311/bin:$PATH python3 audio/check_accent.py $D/p/U$sd.wav > $D/p/uacc$sd.txt 2>&1 < /dev/null
done
echo done > $D/p/roll1-done.txt
