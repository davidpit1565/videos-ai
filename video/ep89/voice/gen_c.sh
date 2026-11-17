#!/usr/bin/env bash
cd /home/user/videos-ai
for p in "c1 3001 0.8" "c2 3002 0.72" "c3 3003 0.84"; do set -- $p
/opt/v311/bin/python audio/build_voice.py --lines video/ep89/lines2.txt --out video/ep89/voice/$1.wav --exaggeration $3 --line-seeds "1:$2" --gap 0.25 --closes 1 --pauses "" --retries 4 --max-speedup 1.35 --watch three > video/ep89/voice/$1.log 2>&1
done
echo finished > video/ep89/voice/gen_c.done
