#!/bin/bash
# usage: render.sh A  (renders build/A.html to ./A.png)
R=/root/.cache/hyperframes/chrome/chrome-headless-shell/linux-152.0.7977.30/chrome-headless-shell-linux64/chrome-headless-shell
D=/tmp/claude-0/-home-user-videos-ai/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/scratchpad/memes
$R --no-sandbox --disable-gpu --hide-scrollbars --window-size=1080,1350 --virtual-time-budget=4000 --screenshot=$D/$1.png file://$D/build/$1.html 2>&1 | grep written
