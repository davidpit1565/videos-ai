#!/usr/bin/env bash
# The whole pipeline for one reel, unattended, from a build HTML to a checked file in
# the studio. Exists because running each stage by hand and waiting for a go-ahead
# between them is what was actually slow — not the TTS itself, which was already the
# genuine bottleneck (CPU-bound, no way around it) but ran one command at a time with
# a human in the loop for every step in between.
#
#   ./export/produce.sh <episode> <build.html> <duration> [accept_words] [bpm] [mood]
#
# <episode> e.g. "03" — used to name every intermediate file consistently.
# Requires the build's CUES array to already be final; this does not write scripts,
# it only turns a finished build into a checked, shipped file.
# <bpm> the music bed's tempo — pick it per episode, not a fixed default: a warning
# or exposé earns something more urgent (90-100), a calm walkthrough something
# lower (72-80). Default 82 if you don't have an opinion yet.
# <mood> neutral | urgent | bright — a different chord progression per mood, not just
# a different tempo on the same one. Every episode sounding the same was the bug;
# tempo alone did not fix it.
set -uo pipefail
cd "$(dirname "$0")/.."

EP="$1"; BUILD="$2"; DUR="$3"; ACCEPT="${4:-}"; BPM="${5:-82}"; MOOD="${6:-neutral}"
VO="audio/reel${EP}-narration.wav"
CUES="audio/reel${EP}-narration-cues.json"
VO_R="audio/reel${EP}-narration-r.wav"
CUES_R="audio/reel${EP}-narration-r-cues.json"
BUILD_T="video/reel-${EP}-timed.html"
BUILD_K="video/reel-${EP}-kar.html"
MUSIC="audio/reel${EP}-music.wav"
MP4="/tmp/reel-${EP}.mp4"
DEEP="/tmp/reel${EP}-deep.json"
GATE="/tmp/reel${EP}-gate.txt"

echo "=== [1/9] voice"
if [ ! -f "$VO" ]; then
  python3 audio/build_voice.py --cues "$BUILD" --out "$VO" --exaggeration 0.50 --cfg 0.30 || exit 1
else
  echo "  $VO already exists, reusing"
fi

echo "=== [2/9] level repair"
# The same word list accepted at the final gate has to be accepted here too — this call
# runs the identical shipped-file check and can exit 1 on its own, before the pipeline
# ever reaches check.sh. reel-06 hit exactly this: --accept was wired to the gate only,
# so an already ear-approved word ("three") still failed the build at this earlier stage.
python3 audio/voice_doctor.py "$VO" --cues "$CUES" --repair "$VO_R" ${ACCEPT:+--accept "$ACCEPT"} || exit 1
cp "$CUES" "$CUES_R"

echo "=== [3/9] retime picture to natural pacing (0.9s closing tail)"
python3 export/retime.py "$BUILD" "$CUES_R" --out "$BUILD_T" --tail 0.9 --wav "$VO_R" || exit 1

echo "=== [4/9] word-level captions"
python3 audio/word_stamps.py "$VO_R" --out "$DEEP" || exit 1
python3 export/karaoke.py "$BUILD_T" "$DEEP" --words-cues "$CUES_R" --out "$BUILD_K" || exit 1

echo "=== [5/9] safe-area check"
node export/safe_check.js "$BUILD_K" --every 0.5 || exit 1

NEWDUR=$(python3 -c "
import re
html = open('$BUILD_K').read()
m = re.search(r'var DUR=([\d.]+)', html)
print(m.group(1) if m else '$DUR')
")
# Rotate the key by episode number so two episodes sharing a mood (a real, repeated
# complaint: reel-03/04/07 were all "urgent" back to back) still land in a different
# key, not the same track transposed by nothing. Five roots spread across the cycle.
KEY=$(python3 -c "
roots = [55.0, 49.0, 61.7, 65.4, 73.4]  # A1, G1, B1, C2, D2
try: ep = int(''.join(c for c in '$EP' if c.isdigit()) or 0)
except Exception: ep = 0
print(roots[ep % len(roots)])
")
echo "=== [6/9] music bed at ${NEWDUR}s, ${BPM} bpm, ${MOOD}, key ${KEY}Hz"
python3 audio/build_music.py "$NEWDUR" "$MUSIC" --bpm "$BPM" --mood "$MOOD" --key "$KEY" || exit 1

echo "=== [7/9] render"
FRAMES=1 ./export/render.sh "$BUILD_K" 1080 1920 "$NEWDUR" "$VO_R" "$MP4" "$MUSIC" || exit 1

echo "=== [8/9] gate"
ACCEPT_WORDS="$ACCEPT" ./export/check.sh "$BUILD_K" "$VO_R" "$MP4" 2>&1 | tee "$GATE"
PASSED=$(grep -c "ALL CHECKS PASSED" "$GATE" || true)

if [ "$PASSED" -eq 0 ]; then
  echo ""
  echo "GATE FAILED — not shipped. See $GATE"
  exit 1
fi

echo "=== [9/9] captions"
# A reel that ships without these publishes broken: the Instagram button posts with an
# empty caption (nothing stops it — it just goes out blank), and the YouTube button
# refuses outright because the title comes from line 1 of this file. This isn't a
# reminder, it's a hard stop — a passed gate used to be enough to call a reel done, and
# "done" kept shipping without them. Numbered separately from the gate itself: a video
# can pass every technical check and still not be postable.
CAP="channel/episode-${EP}-caption.txt"
YT="channel/episode-${EP}-youtube.txt"
MISSING=()
[ -s "$CAP" ] || MISSING+=("$CAP")
[ -s "$YT" ] || MISSING+=("$YT")
if [ "${#MISSING[@]}" -gt 0 ]; then
  echo ""
  echo "CAPTIONS MISSING — not shipped:"
  printf '  %s\n' "${MISSING[@]}"
  echo "Write them (real content grounded in this episode's script — see channel/episode-12-caption.txt for the format), then re-run."
  exit 1
fi

cp "$MP4" "studio/public/reels/reel-${EP}.mp4"
cp "$GATE" "studio/public/reels/reel-${EP}.gate.txt"
# Filesystem mtime does not survive a git checkout reliably — Vercel's build showed
# 2018 for every reel because that's what the checkout left on disk, not when it
# actually shipped. This records the real moment, read by lib/reels.ts instead.
date -u +"%Y-%m-%dT%H:%M:%SZ" > "studio/public/reels/reel-${EP}.built-at.txt"
echo ""
echo "SHIPPED: studio/public/reels/reel-${EP}.mp4  (caption + youtube text present)"
