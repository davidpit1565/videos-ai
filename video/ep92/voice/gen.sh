#!/usr/bin/env bash
# ONE TTS render, ep89 recipe (video/ep89b/gen.sh): exaggeration 0.78, line 1 0.90, lines 4-5 0.82, gap 0.18, min-rate 5.4, seeds 5201-5205
cd /home/user/videos-ai
/opt/v311/bin/python audio/build_voice.py --lines video/ep92/voice/lines.txt --out video/ep92/voice/v1.wav --exaggeration 0.78 --line-exaggeration "1:0.9,2:0.78,3:0.78,4:0.82,5:0.82" --line-seeds "1:5201,2:5202,3:5203,4:5204,5:5205" --gap 0.18 --min-rate 5.4 --retries 5 --pauses "" --watch "" > video/ep92/voice/v1.log 2>&1
echo done > video/ep92/voice/v1.done
