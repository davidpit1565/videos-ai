#!/usr/bin/env bash
# Render a playable video build to a finished MP4 with narration and (optionally) music.
#   ./render.sh <html> <width> <height> <seconds> <narration.wav> <out.mp4> [music.wav]
set -euo pipefail
HTML="$1"; W="$2"; H="$3"; DUR="$4"; VO="$5"; OUT="$6"; MUS="${7:-}"
# Decomposing the mix against both stems: at 0.34 the bed sat 11.2 dB under the voice
# during speech and rose to about voice level in the gaps. The target is 18-20 dB under,
# so the bed comes down ~8 dB. (Comparing gap level to speech level directly is
# misleading here — the gaps are louder than the ducked bed under the voice.)
MUSIC_VOL="${MUSIC_VOL:-0.135}"
# FRAMES=1 captures frame by frame instead of recording playback: slower, but the
# timeline cannot drift, which matters when narration is cut to authored times.
FRAMES="${FRAMES:-0}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

if [ "$FRAMES" = "1" ]; then
  node "$(dirname "$0")/frames.js" "$(realpath "$HTML")" "$W" "$H" "$DUR" "$TMP" 30
  RAW="$TMP/%05d.png"
  VIN=(-framerate 30 -i "$RAW")
  START=0
else
  node "$(dirname "$0")/record.js" "$(realpath "$HTML")" "$W" "$H" "$DUR" "$TMP"
  RAW="$(ls "$TMP"/*.webm)"
fi

if [ "$FRAMES" = "1" ]; then
  echo "frame capture: no pre-roll to trim"
else
  # the page holds a black frame until playback starts — find where that ends
  START="$(ffmpeg -hide_banner -i "$RAW" -vf blackdetect=d=0.2:pix_th=0.02 -f null - 2>&1 \
    | grep -o 'black_end:[0-9.]*' | head -1 | cut -d: -f2)"
  START="${START:-0}"
  echo "trimming ${START}s of pre-roll"
  VIN=(-ss "$START" -i "$RAW")
fi

VCHAIN="[0:v]fps=30,scale=${W}:${H}:flags=lanczos,setpts=PTS-STARTPTS[v]"
VOCHAIN="[1:a]aresample=48000,highpass=f=85,acompressor=threshold=-18dB:ratio=3:attack=8:release=180[vo]"

if [ -n "$MUS" ]; then
  # music ducks under the voice rather than sitting at a fixed level, so the bed
  # is audible in the gaps and never fights the narration
  ffmpeg -hide_banner -loglevel error -y "${VIN[@]}" -i "$VO" -i "$MUS" \
    -filter_complex "$VCHAIN;$VOCHAIN;\
[2:a]aresample=48000,volume=${MUSIC_VOL}[mus];\
[vo]asplit=2[vo1][key];\
[mus][key]sidechaincompress=threshold=0.05:ratio=9:attack=12:release=420[duck];\
[vo1][duck]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,\
loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,apad[a]" \
    -map "[v]" -map "[a]" -t "$DUR" \
    -c:v libx264 -preset slow -crf 19 -profile:v high -pix_fmt yuv420p -movflags +faststart \
    -c:a aac -b:a 192k -ar 48000 -ac 2 "$OUT"
else
  ffmpeg -hide_banner -loglevel error -y "${VIN[@]}" -i "$VO" \
    -filter_complex "$VCHAIN;$VOCHAIN;[vo]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,apad[a]" \
    -map "[v]" -map "[a]" -t "$DUR" \
    -c:v libx264 -preset slow -crf 19 -profile:v high -pix_fmt yuv420p -movflags +faststart \
    -c:a aac -b:a 192k -ar 48000 -ac 2 "$OUT"
fi

# The loudnorm above runs inside a real-time filter graph with no first pass to measure
# against, and it has landed at -15.8 LUFS (vs the -14 target) on two separate renders now
# — always low, never high, so it isn't noise. A genuine two-pass loudnorm (measure, then
# apply with linear=true and the measured stats) fixes it for good instead of a manual
# ffmpeg patch every time the gate catches it.
echo "loudness correction: measuring the render's true stats"
ffmpeg -hide_banner -i "$OUT" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2> "$TMP/loudstats.log"
read -r MEAS_I MEAS_TP MEAS_LRA MEAS_THRESH <<STATS
$(python3 -c "
import json
text = open('$TMP/loudstats.log').read()
data = json.loads(text[text.rfind('{'):])
print(data['input_i'], data['input_tp'], data['input_lra'], data['input_thresh'])
")
STATS
ACTUAL_DUR="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")"
# loudnorm's linear=true mode does NOT always apply a pure linear gain — ffmpeg's own
# implementation silently falls back to its non-linear "dynamic" mode (the same
# unpredictable compressor/gate behavior as a plain single-pass loudnorm) whenever the
# measured stats don't meet its internal conditions for linear correction, with no
# warning printed.
#
# Fixed by dropping loudnorm from this second pass entirely and computing the gain
# ourselves: a flat dB shift so the file's own measured loudness lands exactly on
# target is arithmetic, not a filter with its own fallback behavior to second-guess.
#
# The real, second bug this uncovered, found shipping episode 24 — two completely
# different correction methods (the loudnorm two-pass above, then this flat-gain
# replacement) both landed the file at the exact same wrong place (-11.5 LUFS, true
# peak near 0dBFS), regardless of the very different math feeding into them. The
# common factor was alimiter itself: its `level` option defaults to true, which
# auto-normalizes alimiter's OWN output level (a built-in makeup gain) — silently
# undoing whatever gain was applied before it and re-inflating the signal back up
# near its own internal target, no matter what that input gain was. `level=disabled`
# makes it a pure ceiling with no makeup gain, so the gain computed above is the one
# that actually reaches the file. limit=0.75 (~-2.5dBFS sample peak) still leaves
# real margin for the aresample + AAC encode after it to reconstruct a peak slightly
# higher than any discrete sample alimiter saw.
GAIN_DB="$(python3 -c "print(-14 - (${MEAS_I}))")"
ffmpeg -hide_banner -loglevel error -y -i "$OUT" -c:v copy \
  -af "volume=${GAIN_DB}dB,alimiter=limit=0.75:attack=5:release=50:level=disabled,aresample=48000" \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -t "$ACTUAL_DUR" "$TMP/corrected.mp4"
mv "$TMP/corrected.mp4" "$OUT"

ffprobe -hide_banner -v error -show_entries format=duration,size -of default=nw=1 "$OUT"
