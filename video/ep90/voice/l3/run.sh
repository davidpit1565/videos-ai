#!/usr/bin/env bash
cd /home/user/videos-ai
for job in A:7301 B:7301 A:7302 B:7302 C:7301 A:7303 B:7303; do
 c=${job%%:*}; s=${job##*:}
 flock /tmp/tts.lock /opt/v311/bin/python audio/build_voice.py --lines video/ep90/voice/l3/$c.txt --out video/ep90/voice/l3/$c$s.wav --exaggeration 0.78 --line-seeds "1:$s" --gap 0.18 --min-rate 5.4 --retries 3 --watch "" > video/ep90/voice/l3/$c$s.log 2>&1
done
echo done > video/ep90/voice/l3/done
