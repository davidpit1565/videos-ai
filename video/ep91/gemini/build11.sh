#!/usr/bin/env bash
# ep91 final11: final10 recipe (Gemini clip, panel by panel) + crisp lanczos upscale with a light unsharp, 0.15 s soft fades on every panel,
# word-lit captions on a dark plate in the lower safe area + the CTA card drawn in the same Inter Display Black (caps11.py), re-rendered voice, bed, levelled mix.
# usage: build11.sh <cues.json> <mix.wav> <out.mp4> ; needs /tmp/e11/cap.mov (python3 caps11.py <cues.json> /tmp/e11/cap.mov)
G=/root/.claude/uploads/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/a2da4b3e-gemini_generated_video_8854E44C.mp4
CUES=$1; MIX=$2; OUT=$3; SH="unsharp=5:5:0.55:5:5:0.0"
FC="[0:v]split=4[s0][s1][s2][s3];[s0]scale=1080:1920,boxblur=40:8,eq=brightness=-0.15[bg];\
[s1]trim=0:2.6,setpts=PTS-STARTPTS,crop=720:555:0:0,scale=w='1080*(1+0.05*t/2.6)':h=-2:eval=frame:flags=lanczos,crop=1080:832,${SH},format=yuva420p,fade=t=in:st=0:d=0.15:alpha=1,fade=t=out:st=2.45:d=0.15:alpha=1[A];\
[s2]trim=2.7:5.75,setpts=PTS-STARTPTS,crop=720:590:0:690,scale=w='1080*(1+0.05*t/3.05)':h=-2:eval=frame:flags=lanczos,crop=1080:885,${SH},format=yuva420p,fade=t=in:st=0:d=0.15:alpha=1,fade=t=out:st=2.9:d=0.15:alpha=1,setpts=PTS+2.7/TB[B];\
[s3]trim=5.9:10.03,setpts=PTS-STARTPTS,scale=918:1632:flags=lanczos,${SH},format=yuva420p,fade=t=in:st=0:d=0.15:alpha=1,setpts=PTS+5.9/TB[C];\
[bg][A]overlay=0:344:eof_action=pass[b1];[b1][B]overlay=0:330:eof_action=pass[b2];[b2][C]overlay=81:288:eof_action=pass[b3];\
[1:v]format=rgba[cap];[b3][cap]overlay=0:0:eof_action=pass[v]"
ffmpeg -y -v error -i "$G" -i /tmp/e11/cap.mov -i "$MIX" -filter_complex "$FC" -map "[v]" -map 2:a -t 10.03 -r 30 -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart "$OUT"
