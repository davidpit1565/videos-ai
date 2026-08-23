#!/usr/bin/env bash
# Everything that has to pass before a reel is sent to him.
#   ./export/check.sh <build.html> <narration.wav> [rendered.mp4]
#   ACCEPT_WORDS=three ./export/check.sh ...   — words he has already approved by ear
#                                                 (voice_doctor.py --accept), so the gate
#                                                 doesn't keep failing him on his own call
set -uo pipefail
cd "$(dirname "$0")/.."
BUILD="$1"; VO="$2"; MP4="${3:-}"
fail=0

echo "=== narration"
python3 audio/voice_doctor.py "$VO" ${ACCEPT_WORDS:+--accept "$ACCEPT_WORDS"} || fail=1

echo
echo "=== frame layout"
node export/safe_check.js "$BUILD" --every 0.5 || fail=1

if [ -n "$MP4" ]; then
  echo
  echo "=== rendered file"
  python3 export/qa.py "$MP4" --build "$BUILD" --vo "$VO" || fail=1
fi

echo
[ "$fail" = 0 ] && echo "ALL CHECKS PASSED" || echo "SOMETHING FAILED — do not send this file"
exit $fail
