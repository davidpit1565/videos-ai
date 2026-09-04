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
# loudnorm's linear=true mode computes a pure linear gain from the measured stats and
# does not itself enforce the TP target — it can still overshoot on a single hot
# transient (found shipping episode 23: TP=-1.5 targeted, true peak landed at -0.3dBFS,
# 1.2dB over). alimiter after it guarantees the actual ceiling regardless of what
# loudnorm's own correction leaves in the file. -1.1dBFS limit, not -1.0 flat, so a
# render sitting exactly at the qa.py boundary doesn't get flagged by its own rounding.
ffmpeg -hide_banner -loglevel error -y -i "$OUT" -c:v copy \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=${MEAS_I}:measured_TP=${MEAS_TP}:measured_LRA=${MEAS_LRA}:measured_thresh=${MEAS_THRESH}:linear=true,alimiter=limit=0.879:attack=5:release=50,aresample=48000" \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -t "$ACTUAL_DUR" "$TMP/corrected.mp4"
mv "$TMP/corrected.mp4" "$OUT"

ffprobe -hide_banner -v error -show_entries format=duration,size -of default=nw=1 "$OUT"
