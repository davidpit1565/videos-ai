#!/bin/sh
# static motion audit of the page source: forbidden patterns must be absent
cd "$(dirname "$0")"
echo "--- forbidden: periodic sine of time, % wrap on time, back/elastic easing, linear-speed loops ---"
grep -n -E "Math\.(sin|cos)\([^)]*\bt\b *\*" main.js | grep -v "Math.PI" || echo "sin/cos(t*k): none"
grep -n -E "% *(54|step|per|H|W)\b" main.js | grep -v ox%54 | grep -v "oy % 54" || echo "modulo scroll: none"
grep -n -E "backE|elastic|bounce" main.js || echo "backE/elastic/bounce: none"
grep -n -E "setLineDash|t \* *[0-9.]+ *\) *%|\(t \* [0-9.]+\) %" main.js || echo "dash / t*k % loops: none"
echo "--- remaining Math.sin uses (each must be a one-shot bell Math.sin(Math.PI*clamp(..)) or a shape) ---"
grep -n -o -E "Math\.sin\([^;]{0,40}" main.js | head -30
