#!/usr/bin/env bash
cd /home/user/videos-ai
for s in 7101 7102 7103 7104 7105 7106; do
/opt/v311/bin/python audio/build_voice.py --lines video/ep90/voice/l4/l.txt --out video/ep90/voice/l4/t$s.wav --exaggeration 0.82 --line-seeds "1:$s" --gap 0.18 --min-rate 5.4 --retries 2 --watch "" > video/ep90/voice/l4/t$s.log 2>&1
done
echo done > video/ep90/voice/l4/done
