#!/usr/bin/env bash
# SUPERSEDED by export/produce.sh — that script already does everything this one
# does (voice through render + gate) *and* the parts this one was missing: ships
# the file to studio/public/reels/, refuses to ship without captions written,
# and checks the episode isn't reusing the last one's color palette. Built this
# one without realizing produce.sh already existed; found out the hard way when
# episode 18 passed every check here and still never reached the studio. Use
# produce.sh for any new episode — this file stays only so nothing that already
# points at it breaks.
#
# One command for the whole pipeline from a finished build to a checked, rendered file.
#   ./export/make_reel.sh reel-NN [seconds-guess]
#
# Runs every step in the order CLAUDE.md describes, stops at the first one that fails,
# and tells you which file to look at and fix. It does not write the build's script or
# pick the topic — that's still a real creative decision. Everything after "the HTML
# exists" is mechanical, and mechanical is exactly what kept costing real minutes this
# session: a duration typo, a heading that overflowed the safe box, three manual reruns
# to get back to green. One script, one order, nothing skipped, nothing invented.
#
# Requires: video/<name>.html already written, with a `var CUES=[...]` array of
# [start,end,"line"] triples (the placeholder timing only has to be in the right order —
# retime.py remaps it to the real generated voice).
set -euo pipefail
cd "$(dirname "$0")/.."

NAME="${1:?usage: make_reel.sh reel-NN}"
BUILD="video/${NAME}.html"
[ -f "$BUILD" ] || { echo "no such build: $BUILD"; exit 1; }

VO="audio/${NAME}-narration.wav"
VO_CUES="audio/${NAME}-narration-cues.json"
VO_FIXED="audio/${NAME}-narration-fixed.wav"
VO_FIXED_CUES="audio/${NAME}-narration-fixed-cues.json"
DEEP="audio/${NAME}-narration-deep.json"
PACED="video/${NAME}-paced.html"
KAR="video/${NAME}-kar.html"
MUSIC="audio/${NAME}-music.wav"
MP4="video/${NAME}.mp4"

step() { echo; echo "── $* ──"; }

step "1/9  pronunciation lint"
python3 audio/script_lint.py --cues "$BUILD"

step "2/9  voice generation (this is the slow one — roughly 90-100s per narration line,"
echo "     plus up to 3 extra passes for any line that needs its pitch to land)"
python3 audio/build_voice.py --cues "$BUILD" --out "$VO" --exaggeration 0.5 --cfg 0.3

step "3/9  word-level timestamps"
python3 audio/word_stamps.py "$VO" --out "$DEEP"

step "4/9  retime the build onto the real narration"
python3 export/retime.py "$BUILD" "$VO_CUES" --out "$PACED"

step "5/9  word-by-word captions"
python3 export/karaoke.py "$PACED" "$DEEP" --out "$KAR"

step "6/9  safe-area + overlap check"
node export/safe_check.js "$KAR"
echo "   ^ if this failed: the fix is almost always shortening on-screen text in $BUILD,"
echo "     then re-running this script from the top (the spoken line can stay as-is —"
echo "     only the big on-screen card needs to be shorter)."

step "7/9  voice doctor — repair anything flagged"
if ! python3 audio/voice_doctor.py "$VO"; then
  echo "   repairing…"
  # --repair's own exit code reflects what it found on the ORIGINAL file, not
  # whether the repair succeeded — it was aborting the whole script here via
  # set -e before the cp below ever ran, silently skipping straight past the
  # re-check on line 61 and shipping the unrepaired take with no error shown.
  python3 audio/voice_doctor.py "$VO" --repair "$VO_FIXED" || true
  cp "$VO_CUES" "$VO_FIXED_CUES"
  python3 audio/voice_doctor.py "$VO_FIXED"
  FINAL_VO="$VO_FIXED"
else
  FINAL_VO="$VO"
fi

step "8/9  music, generated to the exact retimed length"
# The build's own declared DUR (retime.py's last-beat timing), not the audio
# file's raw length — repair can leave trailing room-tone past the last cue,
# and rendering to that longer length trips qa.py's "length matches the
# build" check with no defect actually present (found on reel-18: 42.6s
# declared vs. 42.95s raw file, a silent QA failure with no code cause).
DUR="$(grep -o 'var DUR=[0-9.]*' "$KAR" | head -1 | cut -d= -f2)"
[ -n "$DUR" ] || DUR="$(python3 -c "import wave;w=wave.open('$FINAL_VO');print(f'{w.getnframes()/w.getframerate():.2f}')")"
python3 audio/build_music.py "$DUR" "$MUSIC"

step "9/9  render (frame-by-frame — this is the second slow step, a minute or two)"
FRAMES=1 ./export/render.sh "$KAR" 1080 1920 "$DUR" "$FINAL_VO" "$MP4" "$MUSIC"

echo
echo "── final check ──"
./export/check.sh "$KAR" "$FINAL_VO" "$MP4"
