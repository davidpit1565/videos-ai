#!/bin/bash
# gate.sh <tag>...   (music A only)
S=/tmp/claude-0/-home-user-videos-ai/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/scratchpad/ep82
cd /home/user/videos-ai/.claude/worktrees/agent-ae36204d551059fb8
for V in "$@"; do
  VOL=$(python3 -c "import json;print(round(json.load(open('$S/out/gain-$V-A.json'))['lin'],3))")
  ./export/check_hf.sh $S/hf/index-$V.html $S/out/narration-$V-r.wav $S/out/cues-vq-$V.json $S/out/ep82-$V-A.mp4 $S/out/bed-A.wav $VOL > $S/out/gate-$V-A.txt 2>&1
  echo "$V exit $?"; grep -E "^  (PASS|FAIL|SKIP)|^ALL|^SOME" $S/out/gate-$V-A.txt
done
