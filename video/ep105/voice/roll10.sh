#!/usr/bin/env bash
cd /home/user/videos-ai; D=video/ep105/voice
for sd in "$@"; do
  flock /tmp/tts.lock /opt/v311/bin/python audio/build_voice.py --lines $D/l10.txt --out $D/p/T$sd.wav --exaggeration 0.72 --cfg 0.30 --gap 0.06 --long 0.15 --max-speedup 1.45 --min-rate 5.8 --no-verify --seed $sd > $D/p/tlog$sd.txt 2>&1 < /dev/null
  PATH=/opt/v311/bin:$PATH python3 audio/check_accent.py $D/p/T$sd.wav > $D/p/tacc$sd.txt 2>&1 < /dev/null
done
echo done > $D/p/roll10-done.txt
